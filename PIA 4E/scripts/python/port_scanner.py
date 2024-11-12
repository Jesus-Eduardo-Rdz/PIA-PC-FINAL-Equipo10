import socket
import hashlib
import csv
from datetime import datetime

def is_port_open(host: str, port: int) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except:
        return False

def scan_ports(host: str, ports: list) -> str:
    # Nombre del archivo de reporte
    report_file = f"port_scan_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(report_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Port", "Status"])

        for port in ports:
            status = "Open" if is_port_open(host, port) else "Closed"
            writer.writerow([port, status])

    # Calcular el hash del archivo de reporte
    with open(report_file, "rb") as f:
        report_hash = hashlib.sha256(f.read()).hexdigest()

    print(f"Se ejecutó 'Escaneo de Puertos' el {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Hash del reporte: {report_hash}")
    print(f"Ubicación del reporte: {report_file}")

    return report_file

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "-help":
        print("Uso: python port_scanner.py")
        print("Escanea una lista de puertos en una dirección IP o nombre de host y genera un reporte.")
    else:
        target_host = input("Introduce la IP o el host a escanear: ")
        ports_to_check = [22, 80, 443, 8080]
        scan_ports(target_host, ports_to_check)
