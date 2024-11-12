import requests
import logging
from fpdf import FPDF
import re
import json
import hashlib
import sys
import shutil
import datetime

# Asegurar que el sistema maneje correctamente la codificación UTF-8 para el sistema de salida
sys.stdout.reconfigure(encoding='utf-8')

# Configuración de logs
current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
log_filename = f'ip_abuse_logs_{current_time}.log'
logging.basicConfig(filename=log_filename, level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s', encoding='utf-8')

# URL de la API de AbuseIPDB
API_URL = 'https://api.abuseipdb.com/api/v2/check'

# Clase para el reporte en PDF
class PDF(FPDF):
    def header(self):
        self.set_font('Arial', 'B', 12)
        self.cell(0, 10, 'IP Abuse Report', 0, 1, 'C')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Page {self.page_no()}', 0, 0, 'C')

# Función de ayuda mejorada
def show_help():
    help_text = """
    Uso: python ip-url_checker.py [opciones]
    
    Este script genera un reporte de abuso de IP en formato PDF y un reporte de URLs sospechosas en formato texto.
    
    Opciones disponibles:
    - api_key: Clave de API para acceder a AbuseIPDB.
    - ips_to_check: Lista de direcciones IP a verificar, separadas por comas.
    - max_entries: Número máximo de reportes de abuso por IP a incluir (0 para todos).
    - -help o Get-Help p -help: Muestra esta ayuda.

    Ejemplo de uso:
    python ip-url_checker.py

    El script solicitará la clave de API de AbuseIPDB y la lista de IPs a analizar. Generará un reporte de abuso en PDF y,
    opcionalmente, un análisis de URLs sospechosas en texto.

    Reportes:
    - Se genera un reporte de abuso de IP en PDF.
    - Si el usuario elige analizar URLs sospechosas, se genera un reporte en texto.
    
    Importante:
    Asegúrese de tener una clave de API válida de AbuseIPDB y conexión a Internet para que el script funcione correctamente.
    """
    print(help_text)

# Función para eliminar o reemplazar caracteres no válidos en el texto
def sanitize_text(text):
    return ''.join([i if ord(i) < 256 else '?' for i in text])

# Función para validar si una entrada es una dirección IP válida
def validate_ip(ip):
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    return bool(ip_pattern.match(ip))

# Función para consultar los datos de una IP en la API de AbuseIPDB
def check_ip(ip, api_key):
    try:
        if not validate_ip(ip):
            raise ValueError(f"Invalid IP address: {ip}")

        headers = {'Key': api_key, 'Accept': 'application/json'}
        params = {
            'ipAddress': ip,
            'maxAgeInDays': 365,
            'verbose': 'true'
        }
        response = requests.get(API_URL, headers=headers, params=params)
        response.raise_for_status()  # Lanza una excepción para códigos de error HTTP

        response.encoding = 'utf-8'
        data = response.json()
        logging.debug(f"API Response for {ip}: {json.dumps(data, indent=4, ensure_ascii=False)}")
        return data.get('data', None)

    except ValueError as e:
        logging.error(f"Validation error for IP {ip}: {e}")
        print(f"Error: {e}")
    except requests.exceptions.RequestException as e:
        logging.error(f"Request error for IP {ip}: {e}")
        print(f"Error in request for IP {ip}: {e}")
    return None

# Función para verificar si una URL es sospechosa
def is_malicious_url(url: str) -> bool:
    try:
        if len(re.findall(r'\d', url)) > 6:
            return True
        if re.search(r'[<>;"\'{}|^~\[\]`]', url):
            return True
        suspicious_tlds = ['.tk', '.xyz', '.cc', '.ml', '.ga', '.ru', '.cn']
        if any(url.endswith(tld) for tld in suspicious_tlds):
            return True
        if len(url) > 75:
            return True
        phishing_keywords = ['login', 'secure', 'account', 'update', 'verify', 'banking', 'confirm']
        if any(keyword in url.lower() for keyword in phishing_keywords):
            return True
        if re.search(r'\d+[a-zA-Z]+|\d+[A-Z][a-z]', url):
            return True
        if url.count('.') > 3:
            return True
        if re.match(r'^https?://\d+\.\d+\.\d+\.\d+', url):
            return True
        if url.startswith("http://") and re.match(r"https?://(www\.)?(facebook|google|amazon|bank)\.com", url):
            return True
        if re.search(r'[1l0oO]', url):
            return True
    except re.error as e:
        logging.error(f"Regex error while checking URL {url}: {e}")
    return False

# Función para extraer y verificar URLs desde los comentarios
def extract_and_check_urls(ip_data):
    suspicious_urls = set()
    url_pattern = re.compile(r'(https?://\S+)')
    for report in ip_data.get('reports', []):
        comment = report.get('comment', '')
        urls = url_pattern.findall(comment)
        for url in urls:
            if is_malicious_url(url):
                suspicious_urls.add(url)
    return list(suspicious_urls)

# Función para generar el reporte de URLs sospechosas en texto
def generate_url_report(suspicious_urls):
    try:
        url_report_filename = f'url_analysis_report_{current_time}.txt'
        with open(url_report_filename, "w", encoding="utf-8") as f:
            if suspicious_urls:
                f.write("Suspicious URLs found:\n")
                for url in suspicious_urls:
                    f.write(f"{url}\n")
            else:
                f.write("No suspicious URLs found in the report.\n")

        with open(url_report_filename, "rb") as f:
            url_report_hash = hashlib.sha256(f.read()).hexdigest()

        print(f"Se ejecutó 'Generación de Reporte de URLs' el {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Hash del reporte: {url_report_hash}")
        print(f"Ubicación del reporte: {url_report_filename}")
        return url_report_filename

    except IOError as e:
        logging.error(f"Error writing URL report: {e}")
        print(f"Error generating URL report: {e}")
    return None

# Función para generar el reporte de abuso de IP en PDF
def generate_report(ips, api_key, max_entries):
    pdf = PDF()
    pdf.add_page()
    all_suspicious_urls = []

    for ip in ips:
        result = check_ip(ip.strip(), api_key)
        if result:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, sanitize_text(f'Report for IP: {ip}'), 0, 1)
            pdf.set_font('Arial', '', 10)
            pdf.cell(0, 10, sanitize_text(f'Total Reports: {result.get("totalReports", 0)}'), 0, 1)
            pdf.cell(0, 10, sanitize_text(f'Last Reported: {result.get("lastReportedAt", "N/A")}'), 0, 1)
            pdf.cell(0, 10, sanitize_text(f'Abuse Confidence Score: {result.get("abuseConfidenceScore", "N/A")}'), 0, 1)

            reports = result.get('reports', [])
            if max_entries > 0:
                reports = reports[:max_entries]

            for report in reports:
                pdf.cell(0, 10, sanitize_text(f"Reported At: {report['reportedAt']}"), 0, 1)
                pdf.cell(0, 10, sanitize_text(f"Comment: {report.get('comment', 'N/A')}"), 0, 1)
                pdf.cell(0, 10, sanitize_text(f"Categories: {', '.join(map(str, report.get('categories', [])))}"), 0, 1)
                pdf.ln(10)

            suspicious_urls = extract_and_check_urls(result)
            all_suspicious_urls.extend(suspicious_urls)
            logging.info(f"Generated report for IP {ip}")
        else:
            pdf.set_font('Arial', 'B', 12)
            pdf.cell(0, 10, sanitize_text(f'No Reports Available for IP {ip} in the last 365 days.'), 0, 1)
            logging.warning(f'No reports available for IP {ip} in the last 365 days.')

    current_time = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f'ip_abuse_and_url_report_{current_time}.pdf'
    try:
        pdf.output(filename)
        print(f"Report generated successfully: {filename}")
    except IOError as e:
        logging.error(f"Error writing PDF report: {e}")
        print(f"Error generating PDF report: {e}")

    print(f"Logs saved successfully as: {log_filename}")

    # Preguntar al usuario si quiere analizar URLs, con validación de entrada
    while True:
        use_url_checker = input("Would you like to analyze the suspicious URLs found in the report? (y/n): ").strip().lower()
        if use_url_checker in ['y', 'n']:
            break
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    # Generar reporte de URLs solo si el usuario selecciona "y"
    if use_url_checker == 'y' and all_suspicious_urls:
        generate_url_report(all_suspicious_urls)
    elif use_url_checker == 'y':
        print("No suspicious URLs were found.")

# Bloque principal del programa
if __name__ == '__main__':
    # Verificar si se solicita ayuda
    if len(sys.argv) > 1 and (sys.argv[1] == "-help" or sys.argv == ["Get-Help", "p", "-help"]):
        show_help()
    else:
        try:
            api_key = input("Please enter your IP Abuse API key: ")
            if not api_key.isalnum():
                raise ValueError("Invalid API key format. The key should be alphanumeric.")

            print("Note: The generated report will only cover data from the last 365 days.")

            ips_to_check = input("Enter the IP addresses to check (separated by commas): ").split(',')
            if not ips_to_check:
                raise ValueError("Please enter at least one IP address.")

            max_entries = int(input("Enter the maximum number of abuse reports to include per IP (0 for all): "))

            all_ip_results = []
            for ip in ips_to_check:
                ip_result = check_ip(ip.strip(), api_key)
                if ip_result:
                    all_ip_results.append(ip_result)

            generate_report(ips_to_check, api_key, max_entries)

        except ValueError as e:
            print(f"Error: {e}")
            logging.error(e)
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            logging.error(e)
