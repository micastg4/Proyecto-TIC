import subprocess
import time
import os
import matplotlib.pyplot as plt
from monitor_metrics import measure_metrics

os.makedirs("../results", exist_ok=True)

def run_test(name, script_path):
    print(f"⚙️ Ejecutando: {name}")
    start_time = time.time()
    
    # Iniciar monitoreo
    metrics = measure_metrics(["bash", script_path], duration=10)
    
    end_time = time.time()
    total_time = end_time - start_time
    metrics["boot_time"] = total_time

    print(f"⏱️ {name} completado en {total_time:.2f}s")
    return metrics

# Correr pruebas en ambos entornos
vm_metrics = run_test("Codespaces (VM)", "../scripts/vm_setup.sh")
docker_metrics = run_test("Docker", "../scripts/docker_setup.sh")

# Guardar resultados
with open("../results/metrics.txt", "w") as f:
    for label, value in vm_metrics.items():
        f.write(f"VM_{label}={value:.2f}\n")
    for label, value in docker_metrics.items():
        f.write(f"Docker_{label}={value:.2f}\n")

# Gráfico comparativo
labels = ["boot_time", "cpu", "memory", "disk_write", "network"]
vm_values = [vm_metrics[k] for k in labels]
docker_values = [docker_metrics[k] for k in labels]

x = range(len(labels))
plt.figure(figsize=(10, 5))
plt.bar(x, vm_values, width=0.4, label="VM", align="center")
plt.bar([i + 0.4 for i in x], docker_values, width=0.4, label="Docker", align="center")
plt.xticks([i + 0.2 for i in x], labels)
plt.ylabel("Medición (segundos / MB / %)")
plt.title("Comparativa de rendimiento: Docker vs Codespaces")
plt.legend()
plt.tight_layout()
plt.savefig("../results/full_benchmark.png")
print("📊 Gráfico guardado en results/full_benchmark.png")