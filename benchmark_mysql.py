#!/usr/bin/env python3
"""
Benchmark MySQL:
  - deployment time
  - throughput (req/s)
  - latency (mean, p95, p99)
  - CPU and memory of mysqld under load
"""

import time, statistics, argparse, csv, json, threading
from datetime import datetime
import psutil
import mysql.connector
from concurrent.futures import ThreadPoolExecutor, as_completed


# ---------- helpers -------------------------------------------------
def wait_for_mysql(host, port, user, password, timeout=120):
    """Return seconds until MySQL is reachable."""
    start = time.perf_counter()
    deadline = start + timeout
    while True:
        try:
            mysql.connector.connect(
                host=host, port=port, user=user, password=password, connection_timeout=2
            ).close()
            return time.perf_counter() - start
        except Exception:
            if time.perf_counter() > deadline:
                raise RuntimeError("MySQL did not become ready in time")
            time.sleep(1)


def worker(host, port, user, password, db, sql, latencies):
    """Executes one simple query and records latency in seconds."""
    conn = mysql.connector.connect(
        host=host, port=port, user=user, password=password, database=db
    )
    cur = conn.cursor()
    t0 = time.perf_counter()
    cur.execute(sql)
    cur.fetchall()
    latencies.append(time.perf_counter() - t0)
    cur.close()
    conn.close()


def sample_resources(pid, stop_event, samples):
    """Record mysqld CPU% and RSS each second until stop_event is set."""
    p = psutil.Process(pid)
    while not stop_event.is_set():
        with p.oneshot():
            samples.append(
                {
                    "timestamp": datetime.utcnow().isoformat(),
                    "cpu_percent": p.cpu_percent(interval=None),
                    "rss_mb": p.memory_info().rss / (1024 * 1024),
                }
            )
        time.sleep(1)


# ---------- main benchmark -----------------------------------------
def run_benchmark(
    host="mysql",
    port=3306,
    user="benchmark",
    password="benchmark",
    db="benchmark_db",
    sql="SELECT 1",
    duration=30,
    concurrency=20,
):
    # 1) Tiempo de implementación
    deployment_time = wait_for_mysql(host, port, user, password)
    print(f"✅ MySQL disponible tras {deployment_time:.2f} s")

    # 2) Preparar monitor de recursos
    mysqld_pid = next(proc.pid for proc in psutil.process_iter(["name"]) if proc.info["name"] == "mysqld")
    samples, stop_evt = [], threading.Event()
    sampler_thr = threading.Thread(target=sample_resources, args=(mysqld_pid, stop_evt, samples))
    sampler_thr.start()

    # 3) Fase de carga
    latencies = []
    end_time = time.perf_counter() + duration
    total_requests = 0
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures = []
        while time.perf_counter() < end_time:
            futures.append(
                pool.submit(worker, host, port, user, password, db, sql, latencies)
            )
            total_requests += 1
        # esperar a que terminen
        for f in as_completed(futures):
            pass

    # 4) Detener muestreo y guardar CSV
    stop_evt.set()
    sampler_thr.join()
    with open("resource_usage.csv", "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["timestamp", "cpu_percent", "rss_mb"])
        writer.writeheader()
        writer.writerows(samples)

    # 5) Estadísticas
    mean_lat = statistics.mean(latencies)
    p95 = statistics.quantiles(latencies, n=100)[94]
    p99 = statistics.quantiles(latencies, n=100)[98]
    throughput = total_requests / duration

    summary = {
        "deployment_seconds": deployment_time,
        "duration_seconds": duration,
        "concurrency": concurrency,
        "total_requests": total_requests,
        "throughput_rps": throughput,
        "latency_seconds": {
            "mean": mean_lat,
            "p95": p95,
            "p99": p99,
        },
        "resource_samples": len(samples),
        "resource_csv": "resource_usage.csv",
    }

    with open("summary.json", "w") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


# ---------- CLI -----------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Benchmark MySQL")
    parser.add_argument("--host", default="mysql")
    parser.add_argument("--port", type=int, default=3306)
    parser.add_argument("--user", default="benchmark")
    parser.add_argument("--password", default="benchmark")
    parser.add_argument("--db", default="benchmark_db")
    parser.add_argument("--sql", default="SELECT 1")
    parser.add_argument("--duration", type=int, default=30, help="seconds of load")
    parser.add_argument("--concurrency", type=int, default=20)
    args = parser.parse_args()

    run_benchmark(
        host=args.host,
        port=args.port,
        user=args.user,
        password=args.password,
        db=args.db,
        sql=args.sql,
        duration=args.duration,
        concurrency=args.concurrency,
    )
