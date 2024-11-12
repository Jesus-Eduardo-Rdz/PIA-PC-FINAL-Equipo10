import argparse
import platform
import os
import subprocess

# Detecta la ruta base automáticamente desde la ubicación de main_script.py
DEFAULT_BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCRIPTS_DIR = os.path.join(DEFAULT_BASE_DIR, "scripts")

# Permite al usuario ingresar una ruta base o usar la predeterminada
def set_base_directory():
    print(f"Ruta base detectada automáticamente: {DEFAULT_BASE_DIR}")
    custom_base_dir = input("Ingrese la ruta base de los scripts o presione Enter para usar la detectada automáticamente: ").strip()
    return custom_base_dir if custom_base_dir else DEFAULT_BASE_DIR

# Detectar el sistema operativo y filtrar los scripts compatibles
def get_compatible_scripts(base_dir):
    scripts_dir = os.path.join(base_dir, "scripts")
    current_os = platform.system()
    
    # Definir los scripts compatibles para cada sistema operativo
    scripts_by_os = {
        "Windows": [
            os.path.join(scripts_dir, "powershell", "PowerShell_Scripts_Menu.ps1"),  # Archivo principal de PowerShell
            os.path.join(scripts_dir, "python", "shodan_alerts.py"),
            os.path.join(scripts_dir, "python", "ip-url_checker.py"),
            os.path.join(scripts_dir, "python", "port_scanner.py"),
            os.path.join(scripts_dir, "python", "unauthorized_processes.py"),
        ],
        "Linux": [
            os.path.join(scripts_dir, "python", "shodan_alerts.py"),
            os.path.join(scripts_dir, "python", "ip-url_checker.py"),
            os.path.join(scripts_dir, "python", "port_scanner.py"),
            os.path.join(scripts_dir, "python", "unauthorized_processes.py"),
            os.path.join(scripts_dir, "bash", "escaneo_puertos.sh"),
            os.path.join(scripts_dir, "bash", "prueba_penetracion.sh"),
        ],
        "Darwin": [
            os.path.join(scripts_dir, "python", "shodan_alerts.py"),
            os.path.join(scripts_dir, "python", "ip-url_checker.py"),
            os.path.join(scripts_dir, "python", "port_scanner.py"),
            os.path.join(scripts_dir, "python", "unauthorized_processes.py"),
        ],
    }
    
    compatible_scripts = scripts_by_os.get(current_os, [])
    print(f"Sistema operativo detectado: {current_os}")
    print("Scripts compatibles:")
    for i, script in enumerate(compatible_scripts, start=1):
        print(f"{i}. {os.path.basename(script)}")
    return compatible_scripts

# Función para ejecutar un script en una nueva ventana de terminal
def open_terminal(script_path, show_help=False):
    current_os = platform.system()
    script_path_quoted = f'"{script_path}"'  # Coloca la ruta entre comillas para manejar espacios
    try:
        # Verificar si el archivo existe
        if not os.path.exists(script_path):
            print(f"Error: El archivo {script_path} no existe.")
            return
        
        if script_path.endswith(".ps1") and current_os == "Windows":
            # Ejecutar PowerShell en una nueva ventana
            cmd = f'start powershell -NoExit -ExecutionPolicy Bypass -File {script_path_quoted}'
            if show_help:
                cmd += " -help"  # Agregar ayuda si es necesario
            subprocess.Popen(cmd, shell=True)
        elif script_path.endswith(".sh") and current_os == "Linux":
            # Ejecutar Bash en Linux
            if show_help:
                subprocess.Popen(["gnome-terminal", "--", "bash", script_path, "--help"])
            else:
                subprocess.Popen(["gnome-terminal", "--", "bash", script_path])
        elif script_path.endswith(".py"):
            # Ejecutar scripts de Python en la terminal correspondiente
            if current_os == "Windows":
                if show_help:
                    subprocess.Popen(f'cmd /k python {script_path_quoted} --help', shell=True)
                else:
                    subprocess.Popen(f'cmd /k python {script_path_quoted}', shell=True)
            elif current_os == "Linux":
                if show_help:
                    subprocess.Popen(["gnome-terminal", "--", "python3", script_path, "--help"])
                else:
                    subprocess.Popen(["gnome-terminal", "--", "python3", script_path])
            elif current_os == "Darwin":
                if show_help:
                    subprocess.Popen(["open", "-a", "Terminal.app", "python3", script_path, "--help"])
                else:
                    subprocess.Popen(["open", "-a", "Terminal.app", "python3", script_path])
        else:
            print(f"El script {script_path} no es compatible con el sistema operativo actual.")
    except Exception as e:
        print(f"Error al intentar abrir el script en una nueva terminal: {e}")

# Menú principal con ayuda y manejo de errores
def main_menu(base_dir):
    compatible_scripts = get_compatible_scripts(base_dir)
    while True:
        # Mostrar menú de opciones
        print("\nSeleccione un script para ejecutar, 'h' para ayuda o '0' para salir:")
        for i, script in enumerate(compatible_scripts, start=1):
            print(f"{i}. {os.path.basename(script)}")
        print("0. Salir")
        print("Ingrese 'help' para ver la documentación general o 'h<num>' para la ayuda detallada de un script específico.")

        # Obtener selección del usuario y validar
        choice = input("Ingrese su elección: ").strip().lower()

        if choice == '0':
            print("Saliendo del programa...")
            break
        elif choice == 'help':
            show_help()
        elif choice.startswith("h") and choice[1:].isdigit():
            script_index = int(choice[1:]) - 1
            if 0 <= script_index < len(compatible_scripts):
                script_path = compatible_scripts[script_index]
                open_terminal(script_path, show_help=True)
            else:
                print("Número de ayuda no válido.")
        elif choice.isdigit() and 1 <= int(choice) <= len(compatible_scripts):
            script_path = compatible_scripts[int(choice) - 1]
            open_terminal(script_path)
        else:
            print("Opción no válida, por favor ingrese un número válido, 'help' o 'h<num>' para ayuda.")

# Función de ayuda general
def show_help():
    help_text = """
    Uso: python main_script.py [-help]
    
    Este es un menú de ciberseguridad que permite ejecutar los siguientes scripts según el sistema operativo detectado.
    Para ejecutar un script, seleccione el número correspondiente en el menú. Cada tarea se abrirá en una nueva terminal 
    donde podrá ingresar los parámetros interactivos.
    
    Opciones de ayuda:
    - help: Muestra este mensaje de ayuda.
    - 0: Salir del programa.
    - h<num>: Muestra la ayuda específica para un script (por ejemplo, 'h1' para ayuda del primer script).
    
    Documentación sobre las funciones en PowerShell_Scripts_Menu.ps1:
    - Función 1: Find-SuspiciousProcesses - Encuentra procesos sospechosos en el sistema.
    - Función 2: Get-Hash - Calcula el hash de un archivo específico.
    - Función 3: Get-HiddenFiles - Lista los archivos ocultos en un directorio.
    - Función 4: System-UsageReview - Revisa el uso general del sistema.
    
    Scripts disponibles:
    1. PowerShell_Scripts_Menu.ps1 - Ejecuta el menú principal de scripts de PowerShell.
    2. shodan_alerts.py - Realiza un análisis de dispositivos mediante Shodan.
    3. ip-url_checker.py - Verifica direcciones IP y URLs sospechosas.
    4. port_scanner.py - Escanea puertos en una dirección IP o dominio.
    5. unauthorized_processes.py - Detecta procesos y conexiones no autorizadas.
    6. escaneo_puertos.sh (Linux) - Escanea puertos utilizando Bash.
    7. prueba_penetracion.sh (Linux) - Realiza una prueba de penetración básica.
    """
    print(help_text)

# Configuración de argparse para mostrar ayuda desde línea de comandos
def setup_argparse():
    parser = argparse.ArgumentParser(description="Menú de Ciberseguridad")
    parser.add_argument("-help", action="store_true", help="Muestra ayuda del menú principal")
    args = parser.parse_args()
    if args.help:
        show_help()
        exit(0)

if __name__ == "__main__":
    setup_argparse()
    base_dir = set_base_directory()
    main_menu(base_dir)
