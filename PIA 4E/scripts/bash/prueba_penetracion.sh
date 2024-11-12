#!/bin/bash

# Función de ayuda
if [[ "$1" == "-help" ]]; then
    echo "Uso: ./prueba_penetracion.sh <IP>"
    echo "Script para realizar pruebas de penetración básicas y generar informes."
    echo "Opciones:"
    echo "    1. Escaneo de puertos."
    echo "    2. Escaneo de vulnerabilidades web."
    echo "    3. Prueba de conexión al puerto 80."
    echo "    4. Salir del script."
    exit 0
fi

# Verificar si se proporciona un argumento
if [ -z "$1" ]; then
    echo "Por favor, proporciona una dirección IP o dominio para escanear."
    echo "Uso: $0 <dirección IP o dominio>"
    exit 1
fi

IP=$1

# Comprobar si Nmap está instalado
if ! command -v nmap &> /dev/null; then
    echo "Error, Nmap no está instalado."
    exit 1
fi

# Comprobar si Nikto está instalado
if ! command -v nikto &> /dev/null; then
    echo "Error, Nikto no está instalado."
    exit 1
fi

# Menú principal
while true; do
    echo "		Menu
		1. Escaneo de puertos
		2. Encontrar vulnerabilidades
		3. Probar conexiones
		4. Salir"
    read -p "Elija una opción: " op

    case $op in
        1)
            # Escaneo de puertos
            REPORT_PORTS="reporte_escaneo_puertos_$(date +%Y%m%d%H%M%S).txt"
            echo "Iniciando escaneo de puertos en $IP..."
            nmap -p- --open $IP > "$REPORT_PORTS"
            echo "Escaneo completado. Reporte guardado en $REPORT_PORTS."

            # Mostrar hash y ubicación del reporte
            HASH=$(sha256sum "$REPORT_PORTS" | awk '{print $1}')
            echo "Se ejecutó 'Escaneo de Puertos' el $(date)"
            echo "Hash del reporte: $HASH"
            echo "Ubicación del reporte: $(realpath "$REPORT_PORTS")"
            ;;

        2)
            # Escaneo de vulnerabilidades web
            REPORT_VULNS="reporte_vulnerabilidades_$(date +%Y%m%d%H%M%S).txt"
            echo "Iniciando escaneo de vulnerabilidades en $IP..."
            nikto -h "$IP" > "$REPORT_VULNS"
            echo "Escaneo de vulnerabilidades completado. Reporte guardado en $REPORT_VULNS."

            # Mostrar hash y ubicación del reporte
            HASH=$(sha256sum "$REPORT_VULNS" | awk '{print $1}')
            echo "Se ejecutó 'Escaneo de Vulnerabilidades' el $(date)"
            echo "Hash del reporte: $HASH"
            echo "Ubicación del reporte: $(realpath "$REPORT_VULNS")"
            ;;

        3)
            # Prueba de conexión al puerto 80
            REPORT_CONNECTION="reporte_conexion_$(date +%Y%m%d%H%M%S).txt"
            echo "Verificando conexión al puerto 80 en $IP..."
            nc -zv $IP 80 &> "$REPORT_CONNECTION"
            echo "Prueba de conexión completada. Reporte guardado en $REPORT_CONNECTION."

            # Mostrar hash y ubicación del reporte
            HASH=$(sha256sum "$REPORT_CONNECTION" | awk '{print $1}')
            echo "Se ejecutó 'Prueba de Conexión' el $(date)"
            echo "Hash del reporte: $HASH"
            echo "Ubicación del reporte: $(realpath "$REPORT_CONNECTION")"
            ;;

        4)
            echo "Saliendo..."
            exit 0
            ;;

        *)
            echo "Opción no válida. Selecciona una opción del 1 al 4."
            ;;
    esac
done
