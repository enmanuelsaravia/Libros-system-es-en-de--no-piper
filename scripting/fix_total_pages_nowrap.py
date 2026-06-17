import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os

dirs = [os.path.join(PROJECT_ROOT, 'htm'), os.path.join(PROJECT_ROOT, 'htm+audio')]

old_css = """        .total-pages {
            color: #000000;
            font-size: 1.1rem;
            font-weight: bold;
        }"""

new_css = """        .total-pages {
            color: #000000;
            font-size: 1.1rem;
            font-weight: bold;
            white-space: nowrap;
        }"""

count = 0
for d in dirs:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.htm'):
                f_path = os.path.join(root, file)
                try:
                    with open(f_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if old_css in content:
                        content = content.replace(old_css, new_css)
                        with open(f_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {f_path}: {e}")

print(f"Done processing {count} files.")
