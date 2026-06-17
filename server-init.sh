#!/usr/bin/env bash

# ==============================================================================
# Script: server-init.sh
# Descripción: Inicializa el entorno portable, configura variables dinámicas,
#              actualiza los modos de Apertium y lanza el servicio de lectura
#              offline en segundo plano con autoreinicios automáticos.
# ==============================================================================

set -euo pipefail

# 1. Obtener la ruta raíz portable absoluta
PORTABLE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
export PORTABLE_MODE=1
export PORTABLE_ROOT

# =========================================================
# AUTO-REPARAR RUTAS ABSOLUTAS EN EL ESPACIO DE TRABAJO
# =========================================================
echo "⚙️  Auto-reparando rutas absolutas para esta copia del proyecto..."
if command -v python3 >/dev/null 2>&1; then
    python3 "$PORTABLE_ROOT/scripting/patch_workspace_paths.py" "$PORTABLE_ROOT"
fi

if [ -z "${SELECTED_PORTABLE_DIR:-}" ]; then
    if [ -d "$PORTABLE_ROOT/portable-bin-for-gentoo-2026-PATH" ] && bash "$PORTABLE_ROOT/init-validate-all-portable-binaries.sh" "portable-bin-for-gentoo-2026-PATH" > /dev/null 2>&1; then
        SELECTED_PORTABLE_DIR="portable-bin-for-gentoo-2026-PATH"
    elif [ -d "$PORTABLE_ROOT/portable-bin-for-rocky-linux-8-PATH" ]; then
        SELECTED_PORTABLE_DIR="portable-bin-for-rocky-linux-8-PATH"
    else
        echo "❌ No portable bin directory found."
        exit 1
    fi
fi
export SELECTED_PORTABLE_DIR

echo "======================================================================"
echo "📚 INICIALIZANDO ENTORNO PORTABLE OFFLINE: BIBLIOTECA LIBROS"
echo "======================================================================"
echo "[+] Directorio raíz portable: $PORTABLE_ROOT"
echo "[+] Directorio portable seleccionado: $SELECTED_PORTABLE_DIR"

# 2. Configurar variables de entorno para redirección portable
# Crear un espejo temporal en /tmp para evadir bloqueos de ejecución (noexec) en el USB
TEMP_ROOT="/tmp/pdf-portable-root-$(id -u)"
TEMP_BIN_DIR="$TEMP_ROOT/bin"
TEMP_LIB_DIR="$TEMP_ROOT/lib"

if [ ! -d "$TEMP_ROOT" ]; then
    echo "[*] Creando espejo de ejecución en /tmp (bypass noexec)..."
    mkdir -p "$TEMP_BIN_DIR" "$TEMP_LIB_DIR"
    
    # Copiar los binarios que NO estén instalados en el sistema anfitrión
    # Si el sistema ya los tiene, preferimos los nativos para evitar conflictos de GLIBC
    for binary_path in "$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/bin/"*; do
        [ -e "$binary_path" ] || continue
        name=$(basename "$binary_path")
        if command -v "$name" >/dev/null 2>&1; then
            echo "    [+] Usando versión nativa del sistema: $name"
        else
            echo "    [+] Copiando versión portable al espejo: $name"
            cp -rf "$binary_path" "$TEMP_BIN_DIR/"
        fi
    done
    
    cp -rf "$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/lib/"* "$TEMP_LIB_DIR/"
    chmod +x "$TEMP_BIN_DIR"/* 2>/dev/null || true
    echo "    ✅ Espejo portable listo y activado."
fi

export PATH="$TEMP_BIN_DIR:$PATH"
export LD_LIBRARY_PATH="$TEMP_LIB_DIR:${LD_LIBRARY_PATH:-}"
export PYTHONPATH="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/python/site-packages:${PYTHONPATH:-}"
export PERL5LIB="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/perl:${PERL5LIB:-}"
export TESSDATA_PREFIX="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/share/tessdata"
export MONOLITHS_DIR="$PORTABLE_ROOT/scripting"
export PYTHONUNBUFFERED=1

# Variables para Apertium
export APERTIUM_PATH="$TEMP_BIN_DIR"
export APERTIUM_DATADIR="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/share/apertium"

# 3. Configurar dinámicamente los archivos de modo de Apertium para asegurar relocalización
echo "[*] Configurando diccionarios y modos de traducción..."
MODES_DIR="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/share/apertium/modes"
REAL_DATADIR="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/share/apertium"

if [ -d "$MODES_DIR" ]; then
    for mode_file in "$MODES_DIR"/*.mode; do
        if [ -f "$mode_file" ]; then
            # Reemplazar marcador de plantilla @PORTABLE_DATADIR@ con la ruta absoluta actual
            sed -i "s|@PORTABLE_DATADIR@|$REAL_DATADIR|g" "$mode_file"
            # Reemplazar cualquier ruta absoluta anterior por la nueva ruta absoluta actual
            sed -i -E "s|/[^']+/portable-bin-[^/]+/share/apertium|$REAL_DATADIR|g" "$mode_file"
        fi
    done
    echo "    ✅ Modos de Apertium listos y relocalizados."
else
    echo "    ⚠️ Advertencia: No se encontró el directorio de modos de Apertium."
fi

# 4. Asegurar detección robusta de variables gráficas (DISPLAY, XAUTHORITY)
echo "[*] Verificando entorno gráfico..."
if [ -z "${DISPLAY:-}" ]; then
    # Intentar detectar el DISPLAY de un servidor Xorg corriendo para el usuario actual
    DETECTED_DISPLAY=$(pgrep -u "$USER" -a Xorg 2>/dev/null | grep -o -E ':[0-9]+' | head -n 1 || true)
    if [ -n "$DETECTED_DISPLAY" ]; then
        export DISPLAY="$DETECTED_DISPLAY"
        echo "    ✅ DISPLAY detectado automáticamente: $DISPLAY"
    else
        export DISPLAY=":0"
        echo "    ⚠️ DISPLAY no detectado, usando valor por defecto: :0"
    fi
else
    echo "    ✅ DISPLAY configurado: $DISPLAY"
fi

if [ -z "${XAUTHORITY:-}" ]; then
    if [ -f "$HOME/.Xauthority" ]; then
        export XAUTHORITY="$HOME/.Xauthority"
        echo "    ✅ XAUTHORITY configurado por defecto en: $XAUTHORITY"
    else
        # Buscar un archivo .Xauthority en el sistema de archivos temporal o runtime
        DETECTED_XAUTH=$(find /run/user/$(id -u) /tmp -name ".Xauthority" -user "$USER" 2>/dev/null | head -n 1 || true)
        if [ -n "$DETECTED_XAUTH" ]; then
            export XAUTHORITY="$DETECTED_XAUTH"
            echo "    ✅ XAUTHORITY detectado automáticamente: $XAUTHORITY"
        else
            echo "    ⚠️ XAUTHORITY no detectado. Puede haber limitaciones gráficas."
        fi
    fi
else
    echo "    ✅ XAUTHORITY configurado: $XAUTHORITY"
fi

# 5. Configurar el apagado limpio del servicio (Ctrl-C / Cierre de terminal)
mkdir -p "$PORTABLE_ROOT/var"
PID_FILE="$PORTABLE_ROOT/var/service.pid"
SERVER_PID_FILE="$PORTABLE_ROOT/var/server.pid"
PYTHON_PID=""
SERVER_PID=""

cleanup() {
    # Desactivar traps para evitar recursión
    trap - INT TERM HUP EXIT
    
    echo ""
    echo "======================================================================"
    echo "⏹️  DETENIENDO SERVICIOS DE LA BIBLIOTECA PORTABLE"
    echo "======================================================================"
    
    if [ -n "$PYTHON_PID" ]; then
        echo "[*] Deteniendo el lector de portapapeles (PID: $PYTHON_PID)..."
        kill -TERM "$PYTHON_PID" 2>/dev/null || true
    fi
    
    if [ -n "$SERVER_PID" ]; then
        echo "[*] Deteniendo el servidor web (PID: $SERVER_PID)..."
        kill -TERM "$SERVER_PID" 2>/dev/null || true
    fi
    
    sleep 0.5
    
    if [ -n "$PYTHON_PID" ]; then
        kill -9 "$PYTHON_PID" 2>/dev/null || true
    fi
    if [ -n "$SERVER_PID" ]; then
        kill -9 "$SERVER_PID" 2>/dev/null || true
    fi
    
    # Eliminar archivos PID y espejo temporal al salir
    rm -f "$PID_FILE"
    rm -f "$SERVER_PID_FILE"
    if [ -d "${TEMP_ROOT:-}" ]; then
        echo "[*] Limpiando espejo temporal de ejecución..."
        rm -rf "$TEMP_ROOT"
    fi
    
    echo "✅ Todos los servicios detenidos limpiamente."
    echo "======================================================================"
    exit 0
}

# Capturar Ctrl-C, cierre de terminal y señales comunes de parada
trap cleanup INT TERM HUP

# Matar instancias previas del lector para evitar conflictos de portapapeles
if [ -f "$PID_FILE" ]; then
    PREV_PID=$(cat "$PID_FILE")
    if kill -0 "$PREV_PID" 2>/dev/null; then
        echo "[*] Deteniendo instancia previa del lector (PID: $PREV_PID)..."
        kill -TERM "$PREV_PID" 2>/dev/null || kill -9 "$PREV_PID" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
fi

# Buscar un puerto disponible empezando en 9090
SERVER_PORT=9090
while [ -n "$(lsof -t -i:$SERVER_PORT 2>/dev/null || true)" ]; do
    echo "[*] Puerto $SERVER_PORT ocupado. Probando puerto $((SERVER_PORT+1))..."
    SERVER_PORT=$((SERVER_PORT+1))
done
export SERVER_PORT
echo "[*] Puerto disponible encontrado: $SERVER_PORT"

echo "======================================================================"
echo "🎉 ENTORNO PORTABLE CONFIGURADO CON ÉXITO"
echo "======================================================================"
echo "[+] Las variables de entorno han sido configuradas correctamente."
echo "[+] Iniciando servicios en primer plano..."
echo "======================================================================"
echo ""

echo "======================================================================"
echo "🚀 SERVICIOS DE LA BIBLIOTECA ACTIVOS"
echo "======================================================================"
echo "[+] Lector de portapapeles: Activo (escuchando copiados)"
echo "[+] Servidor web: Activo en http://localhost:$SERVER_PORT"
echo "[+] PRESIONA Ctrl+C O CIERRA ESTA VENTANA PARA APAGAR TODO"
echo "======================================================================"
echo ""

# Bucle de control con autoreinicio automático
while true; do
    # Monitorear/Iniciar Lector
    if [ -z "$PYTHON_PID" ] || ! kill -0 "$PYTHON_PID" 2>/dev/null; then
        if [ -n "${PYTHON_PID:-}" ]; then
            echo "[!] El lector de portapapeles se detuvo. Reiniciando..."
        fi
        python3 "$PORTABLE_ROOT/scripting/python_book_reader_service.py" &
        PYTHON_PID=$!
        echo "$PYTHON_PID" > "$PID_FILE"
    fi

    # Monitorear/Iniciar Servidor Web en puerto $SERVER_PORT
    if [ -z "$SERVER_PID" ] || ! kill -0 "$SERVER_PID" 2>/dev/null; then
        if [ -n "${SERVER_PID:-}" ]; then
            echo "[!] El servidor web se detuvo. Reiniciando..."
        fi
        python3 "$PORTABLE_ROOT/scripting/servidor_htm+audio.py" &
        SERVER_PID=$!
        echo "$SERVER_PID" > "$SERVER_PID_FILE"
    fi

    # Esperar a que cualquiera de los dos procesos termine
    wait -n 2>/dev/null || true
    sleep 1
done
