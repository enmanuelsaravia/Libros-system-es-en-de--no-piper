import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os
import glob
import re

scripts = glob.glob(f"{PROJECT_ROOT}/scripting/vociferate-*.sh")

for s in scripts:
    with open(s, "r") as f:
        content = f.read()
    
    # Remove old Piper resolution logic from .from.en.to.es.and.de--page-by-page.sh
    content = re.sub(r'# Resolve Piper binary with priority:.*?PIPER_MODEL_DIR=""\nfi\n', '', content, flags=re.DOTALL)
    
    # Replace PIPER_DIR= and PIPER_EXE= in the portable mode blocks
    content = re.sub(r'\s*PIPER_DIR=.*?\n', '\n', content)
    content = re.sub(r'\s*PIPER_EXE=.*?\n', '\n', content)
    
    # Replace models definitions
    models_block = """
source "$SCRIPT_DIR/find-piper.sh"
declare -A MODELS
MODELS[en]="$PIPER_MODEL_DIR/en_US-ryan-high.onnx"
MODELS[es]="$PIPER_MODEL_DIR/es_MX-claude-high.onnx"
MODELS[de]="$PIPER_MODEL_DIR/de_DE-thorsten-high.onnx"
"""
    # Replace old declare -A MODELS block
    content = re.sub(r'declare -A MODELS\n(?:MODELS\[\w+\]=.*?\n)+', models_block, content, flags=re.MULTILINE)
    
    with open(s, "w") as f:
        f.write(content)
    print(f"Patched {s}")
