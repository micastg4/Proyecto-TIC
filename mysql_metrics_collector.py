#!/usr/bin/env python3
"""
MySQL Deployment Benchmark Tool
------------------------------
Mide y registra las siguientes métricas al desplegar y probar un servidor MySQL:

- Tiempo de implementación
- Rendimiento (consultas por segundo)
- Latencia (tiempo de respuesta promedio)
- Uso de CPU y memoria bajo carga

Requiere:
- mysql-connector-python
- psutil
"""

import argparse
import csv
import subprocess
import time
from datetime import datetime, timezone

import mysql.connector
import psutil


def measure_deployment_time(cmd):
    print(f"Ejecutando: {' '.join(cmd)}")
    start = time.time()
    subprocess.run(cmd, check=True)
    end = time.time()
    return end - start


def run_queries(host, port, user, password, query, count):
    conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=password
    )
    cursor = conn.cursor()

    latencies = []
    start_ts = time.time()

    for _ in range(count):
        t0 = time.time()
        cursor.execute(query)
        _ = cursor.fetchall()
        t1 = time.time()
        latencies.append(t1 - t0)

    end_ts = time.time()
    cursor.close()
    conn.close()

    total_time = end_ts - start_ts
    avg_latency = sum(latencies) / len(latencies)
    qps = count / total_time

    return qps, avg_latency, total_time


def measure_resource_usage(duration):
    cpu_samples = []
    mem_samples = []
    for _ in range(duration):
        cpu_samples.append(psutil.cpu_percent(interval=1))
        mem_samples.append(psutil.virtual_memory().percent)
    return sum(cpu_samples)/len(cpu_samples), sum(mem_samples)/len(mem_samples)


def main():
    parser = argparse.ArgumentParser(description="Benchmark de despliegue y rendimiento MySQL")
    parser.add_argument('--deploy-cmd', nargs='+', required=True, help='Comando para desplegar MySQL')
    parser.add_argument('--host', default='127.0.0.1')
    parser.add_argument('--port', type=int, default=3306)
    parser.add_argument('--user', required=True)
    parser.add_argument('--password', required=True)
    parser.add_argument('--query', default='SELECT 1', help='Consulta SQL para medir')
    parser.add_argument('--count', type=int, default=100, help='Número de consultas')
    parser.add_argument('--output', default='app_test_metrics.csv')
    args = parser.parse_args()

    deploy_time = measure_deployment_time(args.deploy_cmd)
    print(f"Tiempo de implementación: {deploy_time:.2f} segundos")

    print("Ejecutando consultas de prueba…")
    qps, latency, total_query_time = run_queries(
        args.host, args.port, args.user, args.password, args.query, args.count
    )
    print(f"QPS: {qps:.2f}, Latencia promedio: {latency*1000:.2f} ms")

    print("Midiendo uso de CPU/memoria bajo carga…")
    cpu_usage, mem_usage = measure_resource_usage(int(total_query_time))
    print(f"Uso medio de CPU: {cpu_usage:.1f}%, Memoria: {mem_usage:.1f}%")

    with open(args.output, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow([
            'timestamp_utc', 'deployment_time_s', 'qps', 'avg_latency_ms', 'cpu_percent', 'mem_percent'
        ])
        writer.writerow([
            datetime.now(timezone.utc).isoformat(),
            round(deploy_time, 2),
            round(qps, 2),
            round(latency * 1000, 2),
            round(cpu_usage, 1),
            round(mem_usage, 1)
        ])
    print(f"Métricas guardadas en {args.output}")


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\nInterrumpido por el usuario. Saliendo…")
