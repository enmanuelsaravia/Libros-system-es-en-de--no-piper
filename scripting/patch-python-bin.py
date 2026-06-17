import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import glob
import re

for filepath in glob.glob(f"{PROJECT_ROOT}/scripting/vociferate-*.sh'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Define PY_BIN after SCRIPT_DIR
    py_bin_logic = """
if command -v python3.12 >/dev/null 2>&1; then PY_BIN=python3.12
elif command -v python3.11 >/dev/null 2>&1; then PY_BIN=python3.11
elif command -v python3.10 >/dev/null 2>&1; then PY_BIN=python3.10
elif command -v python3.9 >/dev/null 2>&1; then PY_BIN=python3.9
elif command -v python3.8 >/dev/null 2>&1; then PY_BIN=python3.8
else PY_BIN=python3; fi
"""
    if "PY_BIN=" not in content:
        content = content.replace('SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"', 'SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"\n' + py_bin_logic)
    
    # Replace all 'python3 ' with '"$PY_BIN" '
    # Be careful not to replace python3 if it's already patched
    content = content.replace('python3 "$', '"$PY_BIN" "$')
    content = content.replace('python3 scripting/generar_htm.py', '"$PY_BIN" scripting/generar_htm.py')
    content = content.replace('python3 $', '"$PY_BIN" $')
    content = content.replace(' command -v python3 ', ' command -v "$PY_BIN" ')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")
