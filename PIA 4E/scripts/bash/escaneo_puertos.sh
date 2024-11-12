#!/bin/bash

# Función de ayuda
if [[ "$1" == "-help" ]]; then
    echo "Uso: ./escaneo_puertos.sh"
    echo "Script para realizar un escaneo de puertos y generar un informe."
    echo "Opciones:"
    echo "    1. Escaneo de puertos en una IP objetivo."
    echo "    2. Generar informe de puertos escaneados."
    echo "    3. Salir del script."
    exit 0
fi

# Función para validar la dirección IP
validar_ip() {
    if [[ ! "$1" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "Formato de dirección IP no válido."
        exit 1
    fi
}

# Función para escanear puertos
escanear_puertos() {
    local IP_OBJETIVO=$1
    local PUERTO_INICIO=$2
    local PUERTO_FIN=$3
    local ARCHIVO_REPORTE="reporte_escaneo_puertos_$(date +%Y%m%d%H%M%S).txt"

    echo "Escaneando puertos abiertos en $IP_OBJETIVO desde el puerto $PUERTO_INICIO hasta el puerto $PUERTO_FIN..."

    for ((puerto=$PUERTO_INICIO; puerto<=$PUERTO_FIN; puerto++)); do
        nc -zv -w 1 $IP_OBJETIVO $puerto 2>&1 | grep succeeded >> "$ARCHIVO_REPORTE"
    done

    echo "Escaneo de puertos completado. Reporte guardado en $ARCHIVO_REPORTE"

    # Generar hash y mostrar resumen en terminal
    local HASH=$(sha256sum "$ARCHIVO_REPORTE" | awk '{print $1}')
    echo "Se ejecutó 'Escaneo de Puertos' el $(date)"
    echo "Hash del reporte: $HASH"
    echo "Ubicación del reporte: $(realpath "$ARCHIVO_REPORTE")"
}

# Menú principal
while true; do
    echo "           Menu    
    	  1. Iniciar escaneo de puertos
    	  2. Generar informe de escaneo
          3. Salir"
    echo "Elige una opción:"
    read -r OP

    case $OP in
        1)
            echo "Introduce la dirección IP objetivo:"
            read -r IP_OBJETIVO
            validar_ip "$IP_OBJETIVO"

            echo "Introduce el puerto de inicio (por defecto 1):"
            read -r PUERTO_INICIO
            PUERTO_INICIO=${PUERTO_INICIO:-1}

            echo "Introduce el puerto final (por defecto 1000):"
            read -r PUERTO_FIN
            PUERTO_FIN=${PUERTO_FIN:-1000}

            if [[ "$PUERTO_INICIO" -lt 1 || "$PUERTO_FIN" -gt 65535 || "$PUERTO_INICIO" -gt "$PUERTO_FIN" ]]; then
                echo "Rango de puertos no válido. Introduce un rango válido (1-65535)."
                continue
            fi

            escanear_puertos "$IP_OBJETIVO" "$PUERTO_INICIO" "$PUERTO_FIN"
            ;;

        2)
            echo "Opción de informe seleccionada. El informe se generará automáticamente después del escaneo."
            ;;

        3)
            echo "Saliendo..."
            exit 0
            ;;

        *)
            echo "Opción no válida. Elige 1, 2 o 3."
            ;;
    esac
done
