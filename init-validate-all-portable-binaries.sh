#!/bin/bash
# init-validate-all-portable-binaries.sh
# Valida que todos los binarios portables puedan ejecutarse correctamente
# en el sistema actual, verificando que no haya errores de librerías (GLIBC, etc).

PORTABLE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TARGET_PORTABLE_DIR="${1:-portable-bin-PATH}"
BIN_DIR="$PORTABLE_ROOT/$TARGET_PORTABLE_DIR/bin"
LIB_DIR="$PORTABLE_ROOT/$TARGET_PORTABLE_DIR/lib"

if [ ! -d "$BIN_DIR" ]; then
    echo "❌ Error: No se encontró el directorio $BIN_DIR"
    exit 1
fi

# Replicamos el entorno de librerías de init.sh
export LD_LIBRARY_PATH="/usr/lib64:$PORTABLE_ROOT/$TARGET_PORTABLE_DIR/lib64:$LIB_DIR:${LD_LIBRARY_PATH:-}"

DEBUG=${DEBUG:-0}

if [ "$DEBUG" = "1" ]; then
    echo "============================================================"
    echo "🔎 Validando binarios portables en: $BIN_DIR"
    echo "============================================================"
fi

total=0
success=0
failed=0

for bin_path in "$BIN_DIR"/*; do
    if [ -f "$bin_path" ] && [ -x "$bin_path" ]; then
        name="$(basename "$bin_path")"
        total=$((total + 1))
        
        # Verificamos si tiene problemas de enlazado usando ldd
        out=$(LC_ALL=C ldd "$bin_path" 2>&1)
        code=$?
        
        # Si no es un ejecutable dinámico (script bash, script python, etc), ldd devuelve error o dice "not a dynamic executable"
        if echo "$out" | grep -q "not a dynamic executable"; then
            [ "$DEBUG" = "1" ] && echo "✅ [OK]     $bin_path (Script)"
            success=$((success + 1))
        # Si ldd dice "not found", faltan librerías
        elif echo "$out" | grep -q "not found"; then
            echo "❌ [ERROR]  $bin_path -> Faltan librerías compartidas"
            echo "$out" | grep "not found" | sed 's/^/   └─ /'
            failed=$((failed + 1))
        # Si el ldd falla por otra razón
        elif [ $code -ne 0 ]; then
            echo "❌ [ERROR]  $bin_path -> Error de Dynamic Linker"
            echo "   └─ $(echo "$out" | head -n 1)"
            failed=$((failed + 1))
        else
            [ "$DEBUG" = "1" ] && echo "✅ [OK]     $bin_path"
            success=$((success + 1))
        fi
    fi
done

if [ "$DEBUG" = "1" ]; then
    echo "============================================================"
    echo "📊 RESUMEN: $success funcionales, $failed fallidos (Total: $total)"
    echo "============================================================"
fi

if [ "$failed" -gt 0 ]; then
    exit 1
else
    exit 0
fi
