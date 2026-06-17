#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"


# Versión simplificada y probada
echo "=== Limpiador de PDFs ==="
echo ""

# Crear carpeta de destino
mkdir -p pdfs_limpios

# Contador
count=0
total=$(ls *.pdf 2>/dev/null | wc -l)

if [ $total -eq 0 ]; then
    echo "No hay archivos PDF en esta carpeta"
    exit 1
fi

echo "Procesando $total archivos..."

for pdf in *.pdf; do
    count=$((count + 1))
    echo "[$count/$total] Procesando: $pdf"
    
    # Nombre de salida
    output="pdfs_limpios/${pdf%.pdf}_limpio.pdf"
    
    # Limpiar con exiftool y qpdf
    exiftool -all= "$pdf" -o temp.pdf > /dev/null 2>&1
    qpdf --linearize temp.pdf "$output" > /dev/null 2>&1
    
    # Limpiar temporal
    rm -f temp.pdf
    
    # Mostrar resultado
    if [ -f "$output" ]; then
        echo "  ✓ Completado: $(du -h "$output" | cut -f1)"
    else
        echo "  ✗ Error: No se pudo procesar"
    fi
done

echo ""
echo "Proceso completado!"
echo "Archivos limpios en: ./pdfs_limpios/"
ls -lh pdfs_limpios/