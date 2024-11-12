import psutil
import hashlib
import csv
from datetime import datetime

UNAUTHORIZED_PORTS = [22, 135, 445, 3389]
UNAUTHORIZED_PROCESS = ['malware.exe', 'virus.exe', 'backdoor.sh']

def detect_unauthorized_connections_and_processes():
    report_file = f"unauthorized_activity_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    with open(report_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Type", "Details"])

        # Detectar conexiones no autorizadas
        for connection in psutil.net_connections(kind='inet'):
            if connection.laddr and connection.laddr.port in UNAUTHORIZED_PORTS:
                writer.writerow(["Unauthorized Connection", f"{connection.laddr} -> {connection.raddr}"])

        # Detectar procesos no autorizados
        for proc in psutil.process_iter(attrs=['name']):
            if proc.info['name'] in UNAUTHORIZED_PROCESS:
                writer.writerow(["Unauthorized Process", proc.info['name']])

    # Calcular el hash del archivo de reporte
    with open(report_file, "rb") as f:
        report_hash = hashlib.sha256(f.read()).hexdigest()

    print(f"Se ejecutó 'Detección de Procesos/Conexiones no Autorizadas' el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Hash del reporte: {report_hash}")
    print(f"Ubicación del reporte: {report_file}")
    return report_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "-help":
        print("Uso: python unauthorized_processes.py")
        print("Detecta conexiones y procesos no autorizados y genera un reporte en CSV.")
    else:
        detect_unauthorized_connections_and_processes()
