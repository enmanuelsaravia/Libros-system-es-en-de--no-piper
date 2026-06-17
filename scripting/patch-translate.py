import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import glob
import re

for filepath in glob.glob(f"{PROJECT_ROOT}/scripting/vociferate-*.sh'):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We want to change translate_text behavior to always prefer the venv if available
    old_block = """    if [ -n "$PORTABLE_MODE" ]; then
        python3 "$WORKDIR/translator.py"
    elif [ -f "$HOME/googletrans/venv/bin/python3" ]; then
        "$HOME/googletrans/venv/bin/python3" "$WORKDIR/translator.py"
    else
        python3 "$WORKDIR/translator.py"
    fi"""
    
    new_block = """    if [ -f "$HOME/googletrans/venv/bin/python3" ]; then
        "$HOME/googletrans/venv/bin/python3" "$WORKDIR/translator.py"
    else
        python3 "$WORKDIR/translator.py"
    fi"""
    
    content = content.replace(old_block, new_block)
    
    # Also wrap translate_text calls with if ! translate_text ... || true to prevent set -e crashes
    content = content.replace('translate_text "$LANG" "$WORKDIR/raw_page.txt" "$FINAL_TXT"\n', 'translate_text "$LANG" "$WORKDIR/raw_page.txt" "$FINAL_TXT" || true\n')
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Patched {filepath}")
