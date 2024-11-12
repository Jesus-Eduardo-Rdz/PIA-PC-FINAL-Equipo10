import shodan
from fpdf import FPDF
import hashlib
import datetime
import time

def get_user_input():
    api_key = input("Ingrese su clave API de Shodan: ")
    devices = input("Ingrese las direcciones IP o dominios a monitorizar (separadas por comas): ").split(',')
    interval = int(input("Ingrese el intervalo (en segundos) entre cada escaneo (por ejemplo, 3600 para 1 hora): "))
    return api_key, devices, interval

def shodan_scan(api_key, devices, interval):
    api = shodan.Shodan(api_key)
    results = {}
    for device in devices:
        try:
            host = api.host(device.strip())
            open_ports = [item['port'] for item in host['data']]
            results[device] = {'open_ports': open_ports}
        except shodan.APIError as e:
            results[device] = {'error': str(e)}
        time.sleep(interval)
    return results

class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'Shodan Scan Report', 0, 1, 'C')

def generate_shodan_report(results):
    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f'shodan_scan_report_{current_time}.pdf'
    
    pdf = PDF()
    pdf.add_page()
    pdf.set_font('Arial', '', 10)
    for device, data in results.items():
        if "error" in data:
            pdf.cell(0, 10, f"Device: {device} - Error: {data['error']}", 0, 1)
        else:
            pdf.cell(0, 10, f"Device: {device}", 0, 1)
            pdf.cell(0, 10, f"Open ports: {data['open_ports']}", 0, 1)
        pdf.ln(5)

    pdf.output(report_file)

    # Calcular el hash del archivo de reporte
    with open(report_file, "rb") as f:
        report_hash = hashlib.sha256(f.read()).hexdigest()

    print(f"Se ejecutó 'Escaneo Shodan' el {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Hash del reporte: {report_hash}")
    print(f"Ubicación del reporte: {report_file}")
    return report_file

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "-help":
        print("Uso: python shodan_alerts.py")
        print("Escanea dispositivos con Shodan y genera un reporte de puertos abiertos en PDF.")
    else:
        api_key, devices, interval = get_user_input()
        results = shodan_scan(api_key, devices, interval)
        generate_shodan_report(results)
