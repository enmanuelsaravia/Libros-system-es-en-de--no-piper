import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import glob
import re

for filepath in glob.glob(f"{PROJECT_ROOT}/scripting/vociferate-*.sh'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to replace:
    # python3 "$MONOLITHS_DIR/limpiador.py" "$WORKDIR/raw_page.txt" > /dev/null 2>&1
    # With:
    # if [ -f "$MONOLITHS_DIR/limpiador.py" ]; then python3 "$MONOLITHS_DIR/limpiador.py" "$WORKDIR/raw_page.txt" > /dev/null 2>&1 || true; else echo "    [WARNING] limpiador.py no encontrado. Omitiendo limpieza."; fi
    
    content = content.replace(
        'python3 "$MONOLITHS_DIR/limpiador.py" "$WORKDIR/raw_page.txt" > /dev/null 2>&1',
        'if [ -f "$MONOLITHS_DIR/limpiador.py" ]; then python3 "$MONOLITHS_DIR/limpiador.py" "$WORKDIR/raw_page.txt" > /dev/null 2>&1 || true; else echo "    [WARNING] limpiador.py no encontrado. Omitiendo limpieza."; fi'
    )
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")
