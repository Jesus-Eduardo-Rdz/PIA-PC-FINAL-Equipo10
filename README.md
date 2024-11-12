Proyecto de Ciberseguridad - Menú Principal y Módulos de Análisis

Este repositorio contiene un proyecto de ciberseguridad que incluye un script principal (main_script.py) y 16 módulos que ejecutan diversas tareas de análisis de seguridad. Este proyecto está diseñado para funcionar en sistemas Windows, Linux y macOS, y permite la ejecución de scripts de PowerShell, Python y Bash según el sistema operativo detectado.

Estructura del Proyecto

Proyecto
├── scripts
│   ├── powershell
│   │   ├── PowerShell_Scripts_Menu.ps1
│   │   ├── System_Usage_Review.psm1
│   │   ├── Get_Hidden_Files.psm1
│   │   ├── Get_Hash.psm1
│   │   └── Find_Suspicious_Processes.psm1
│   ├── python
│   │   ├── shodan_alerts.py
│   │   ├── ip-url_checker.py
│   │   ├── port_scanner.py
│   │   └── unauthorized_processes.py
│   └── bash
│       ├── escaneo_puertos.sh
│       └── prueba_penetracion.sh
└── main_script.py

Descripción General

El script principal (main_script.py) actúa como un menú que permite al usuario seleccionar y ejecutar cualquiera de los módulos de análisis de seguridad. Según el sistema operativo, el menú muestra solo los scripts compatibles y los ejecuta en nuevas ventanas de terminal.

Módulos y Funcionalidades

- PowerShell (scripts/powershell):
  - PowerShell_Scripts_Menu.ps1: Menú de análisis con opciones de funciones específicas.
  - System_Usage_Review.psm1: Monitorea el uso del sistema.
  - Get_Hidden_Files.psm1: Lista archivos ocultos.
  - Get_Hash.psm1: Calcula hashes de archivos.
  - Find_Suspicious_Processes.psm1: Detecta procesos sospechosos.

- Python (scripts/python):
  - shodan_alerts.py: Genera alertas de Shodan.
  - ip-url_checker.py: Verifica reputación de IPs y URLs.
  - port_scanner.py: Escaneo de puertos.
  - unauthorized_processes.py: Detecta conexiones no autorizadas.

- Bash (scripts/bash):
  - escaneo_puertos.sh: Escaneo básico de puertos.
  - prueba_penetracion.sh: Prueba de penetración simple.

Requisitos del Sistema

- Windows, Linux, o macOS
- Python 3
- Acceso a PowerShell y Bash
- Permisos de ejecución

Instalación y Configuración

1. Clonar el repositorio:
   git clone https://github.com/tu_usuario/proyecto_ciberseguridad.git
   cd proyecto_ciberseguridad

2. Instalar dependencias de Python:
   pip install -r requirements.txt

3. Ejecutar el script principal:
   python main_script.py

Detalles de los Reportes Generados

Cada script genera un reporte en un formato específico, según la tarea.
"""
# Dependencias para el proyecto de ciberseguridad

# Módulos de Python utilizados en scripts individuales
shodan==1.27.0  # Para shodan_alerts.py
requests==2.31.0  # Para ip-url_checker.py
fpdf==1.7.2  # Para generación de PDFs en ip-url_checker.py y shodan_alerts.py
psutil==5.9.5  # Para unauthorized_processes.py

# Otros módulos estándar de Python que no necesitan instalación:
# - datetime
# - hashlib
# - json
# - csv
# - sys
# - time
# - re
# - logging
# - socket
# - subprocess
