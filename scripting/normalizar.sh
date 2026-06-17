#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"


# Recorremos todos los archivos .pdf del directorio actual
for archivo in *.pdf; do
    # Saltamos si no hay archivos pdf
    [ -e "$archivo" ] || continue

    # 1. Quitar la extensión para procesar solo el nombre
    nombre_base="${archivo%.*}"
    extension="${archivo##*.}"

    # 2. Procesar el nombre:
    # - iconv: Transliteración para quitar tildes (de UTF-8 a ASCII)
    # - tr: Pasar a minúsculas
    # - sed: Cambiar espacios por guiones bajos y eliminar caracteres raros
    nuevo_nombre=$(echo "$nombre_base" | iconv -f utf-8 -t ascii//TRANSLIT | tr '[:upper:]' '[:lower:]' | sed -e 's/ /_/g' -e 's/[^a-z0-9._-]//g')

    # 3. Reconstruir el nombre completo
    nombre_final="${nuevo_nombre}.${extension}"

    # 4. Renombrar solo si el nombre cambió y el destino no existe
    if [ "$archivo" != "$nombre_final" ]; then
        if [ ! -e "$nombre_final" ]; then
            mv "$archivo" "$nombre_final"
            echo "Renombrado: '$archivo' -> '$nombre_final'"
        else
            echo "Error: '$nombre_final' ya existe. Saltando '$archivo'..."
        fi
    fi
done