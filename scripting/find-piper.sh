#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# find-piper.sh
# Helper to locate piper, its libs, and models reliably.

PIPER_EXE=""
PIPER_MODEL_DIR=""
PIPER_LIB_DIR=""

# Discover where models actually are
if [ -d "$PORTABLE_ROOT/portable-bin-for-gentoo-2026-PATH/share/piper" ]; then
    DISCOVERED_MODEL_DIR="$PORTABLE_ROOT/portable-bin-for-gentoo-2026-PATH/share/piper"
elif [ -d "$PORTABLE_ROOT/${SELECTED_PORTABLE_DIR:-portable-bin-for-rocky-linux-8-PATH}/share/piper" ]; then
    DISCOVERED_MODEL_DIR="$PORTABLE_ROOT/${SELECTED_PORTABLE_DIR:-portable-bin-for-rocky-linux-8-PATH}/share/piper"
else
    DISCOVERED_MODEL_DIR="$HOME/piper"
fi

# 1. Check ~/piper/install/piper (Native build)
if [ -x "$HOME/piper/install/piper" ]; then
    PIPER_EXE="$HOME/piper/install/piper"
    PIPER_MODEL_DIR="$DISCOVERED_MODEL_DIR"
    PIPER_LIB_DIR="$HOME/piper/build/pi/lib64"
# 2. Check ~/piper/piper (Alternative native build)
elif [ -x "$HOME/piper/piper" ]; then
    PIPER_EXE="$HOME/piper/piper"
    PIPER_MODEL_DIR="$HOME/piper"
    PIPER_LIB_DIR="$HOME/piper/build/pi/lib64"
# 3. Check system command
elif command -v piper >/dev/null 2>&1; then
    PIPER_EXE="$(command -v piper)"
    PIPER_MODEL_DIR="$DISCOVERED_MODEL_DIR"
# 4. Check SELECTED_PORTABLE_DIR
elif [ -n "$SELECTED_PORTABLE_DIR" ] && [ -x "$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/bin/piper" ]; then
    PIPER_EXE="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/bin/piper"
    PIPER_MODEL_DIR="$DISCOVERED_MODEL_DIR"
    PIPER_LIB_DIR="$PORTABLE_ROOT/$SELECTED_PORTABLE_DIR/lib"
# 5. Fallback to gentoo dir
elif [ -x "$PORTABLE_ROOT/portable-bin-for-gentoo-2026-PATH/bin/piper" ]; then
    PIPER_EXE="$PORTABLE_ROOT/portable-bin-for-gentoo-2026-PATH/bin/piper"
    PIPER_MODEL_DIR="$DISCOVERED_MODEL_DIR"
    PIPER_LIB_DIR="$PORTABLE_ROOT/portable-bin-for-gentoo-2026-PATH/lib"
# 6. Fallback to rocky dir
elif [ -x "$PORTABLE_ROOT/portable-bin-for-rocky-linux-8-PATH/bin/piper" ]; then
    PIPER_EXE="$PORTABLE_ROOT/portable-bin-for-rocky-linux-8-PATH/bin/piper"
    PIPER_MODEL_DIR="$DISCOVERED_MODEL_DIR"
    PIPER_LIB_DIR="$PORTABLE_ROOT/portable-bin-for-rocky-linux-8-PATH/lib"
fi

# Fallback for library searching if not explicitly set above or if it doesn't exist
if [ -z "$PIPER_LIB_DIR" ] || [ ! -d "$PIPER_LIB_DIR" ]; then
    for d in "$PORTABLE_ROOT/${SELECTED_PORTABLE_DIR:-portable-bin-for-rocky-linux-8-PATH}/lib" "$HOME/piper/build/pi/lib64" "$HOME/piper/install/lib" "$HOME/piper/build/p/src/piper_phonemize_external-build"; do
        if [ -d "$d" ] && ls "$d"/libpiper_phonemize.so* >/dev/null 2>&1; then
            PIPER_LIB_DIR="$d"
            break
        fi
    done
fi

if [ -z "$PIPER_EXE" ] || [ ! -x "$PIPER_EXE" ]; then
    echo "❌ Dependencia faltante: piper"
    echo "Por favor compila piper desde -> https://github.com/rhasspy/piper.git o instálalo en tu distro."
    exit 1
fi

# We don't globally export LD_LIBRARY_PATH so we don't break pdfinfo and other commands.
# Instead, we create a wrapper script for piper in /tmp and use that as PIPER_EXE.
PIPER_WRAPPER="/tmp/piper_wrapper_$$.sh"
cat << 'WRAPPER' > "$PIPER_WRAPPER"
#!/bin/bash
LD_LIBRARY_PATH="${PIPER_LIB_DIR}:${LD_LIBRARY_PATH:-}" exec "${PIPER_REAL_EXE}" "$@"
WRAPPER
chmod +x "$PIPER_WRAPPER"

# Export the real exe and lib dir so the wrapper can use them
export PIPER_REAL_EXE="$PIPER_EXE"
export PIPER_LIB_DIR="$PIPER_LIB_DIR"

# Redefine PIPER_EXE to point to our safe wrapper
PIPER_EXE="$PIPER_WRAPPER"

# Test if it runs
if ! "$PIPER_EXE" --version > /dev/null 2>&1; then
    echo "[WARNING] Piper binary $PIPER_EXE cannot run (missing libraries or incompatibility). Audio generation may fail."
    PIPER_EXE=""
fi

if [ -z "$PIPER_MODEL_DIR" ]; then
    echo "[WARNING] Piper Model directory not found; audio generation will be disabled."
fi
