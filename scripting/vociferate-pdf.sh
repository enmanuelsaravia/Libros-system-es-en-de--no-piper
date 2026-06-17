#!/bin/bash

set -e

PDF="$1"

if [ ! -f "$PDF" ]; then
    echo "No existe: $PDF"
    exit 1
fi

# Calcular el directorio portable y de scripts de forma dinamica
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if command -v python3.12 >/dev/null 2>&1; then PY_BIN=python3.12
elif command -v python3.11 >/dev/null 2>&1; then PY_BIN=python3.11
elif command -v python3.10 >/dev/null 2>&1; then PY_BIN=python3.10
elif command -v python3.9 >/dev/null 2>&1; then PY_BIN=python3.9
elif command -v python3.8 >/dev/null 2>&1; then PY_BIN=python3.8
else PY_BIN=python3; fi

PORTABLE_ROOT="${PORTABLE_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"
MONOLITHS_DIR="${MONOLITHS_DIR:-$SCRIPT_DIR}"

WORKDIR="$PORTABLE_ROOT/personal"
mkdir -p "$WORKDIR"

cp -v "$PDF" "$WORKDIR/"

NOMBRE=$(basename "$PDF")

cd "$WORKDIR" || exit 1

TXT="${NOMBRE%.pdf}.txt"

echo "[*] Extrayendo texto..."

pdftotext -layout "$NOMBRE" "$TXT"

if [ ! -f "$TXT" ]; then
    echo "No se generó TXT"
    exit 1
fi

echo "[*] Quitando cortes de palabras con guion..."

sed -i ':a;N;$!ba;s/-\n//g;s/\n\([^\n]\)/ \1/g' "$TXT"

echo "[*] Limpiando..."

"$PY_BIN" "$MONOLITHS_DIR/limpiador.py" "$TXT"

echo "[*] Preparando..."

dash "$MONOLITHS_DIR/preparar_literatura.sh" "$TXT"

echo "[*] Limpiando simbolos solos..."

sed -i '/^[!?.,:;ʼ”“()-]*$/d' "$TXT"

echo "[*] Ejecutando lectura..."

# Limpiamos cualquier señal de stop previa
rm -f /tmp/STOP

# Ejecutamos el script de lectura (en segundo plano)
dash "$MONOLITHS_DIR/script-literatura.sh" "$TXT" &
LIT_PID=$!

# Abrimos el PDF en xournalpp (en primer plano para esperar su cierre)
echo "[*] Abriendo Xournalpp..."
xournalpp "$NOMBRE"

# Al cerrar xournalpp, detenemos la vociferación si aún está activa
if kill -0 $LIT_PID 2>/dev/null; then
    echo "[*] Xournalpp cerrado. Deteniendo vociferación..."
    touch /tmp/STOP
    killall osd_cat 2>/dev/null
    
    # Esperamos a que el script de literatura termine por su cuenta al ver el archivo STOP.
    # Solo si tarda demasiado (más de 10 segundos) lo forzamos.
    COUNT=0
    while kill -0 $LIT_PID 2>/dev/null && [ $COUNT -lt 20 ]; do
        sleep 0.1
        COUNT=$((COUNT + 1))
    done

    if kill -0 $LIT_PID 2>/dev/null; then
        echo "[*] Forzando detención de audio..."
        # Matar el grupo de procesos para detener mpv y piper también
        kill -TERM -$LIT_PID 2>/dev/null || kill $LIT_PID 2>/dev/null || true
    fi
fi

echo "listo"