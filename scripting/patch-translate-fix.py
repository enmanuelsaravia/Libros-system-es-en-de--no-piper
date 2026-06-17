import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import glob
import re

for filepath in glob.glob(f"{PROJECT_ROOT}/scripting/vociferate-*.sh'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_block = """    if [ -f "$HOME/googletrans/venv/bin/python3" ]; then
        "$HOME/googletrans/venv/bin/python3" "$WORKDIR/translator.py"
    else
        python3 "$WORKDIR/translator.py"
    fi"""
    
    new_block = """    "$PY_BIN" "$WORKDIR/translator.py" """
    
    old_block_2 = """    if [ -f "$HOME/googletrans/venv/bin/python3" ]; then
        "$HOME/googletrans/venv/bin/python3" "$WORKDIR/translator.py"
    else
        "$PY_BIN" "$WORKDIR/translator.py"
    fi"""
    
    content = content.replace(old_block, new_block)
    content = content.replace(old_block_2, new_block)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")
