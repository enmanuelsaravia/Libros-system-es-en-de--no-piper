import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os
import glob

dirs = [os.path.join(PROJECT_ROOT, 'htm'), os.path.join(PROJECT_ROOT, 'htm+audio')]

old_css = """        #show-header-btn {
            position: fixed;
            top: 0;
            left: 50%;
            transform: translateX(-50%);
            z-index: 1000;
            background: var(--toolbar-bg);
            border: 2px solid var(--border-color);
            border-top: none;
            border-radius: 0 0 10px 10px;
            padding: 6px 20px;
            font-weight: 900;
            font-size: 1.2rem;
            cursor: pointer;
            display: none;
            color: var(--text-color);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.2s;
        }"""

new_css = """        #show-header-btn {
            position: fixed;
            top: 0;
            right: 0;
            z-index: 1000;
            background: var(--toolbar-bg);
            border: 2px solid var(--border-color);
            border-top: none;
            border-right: none;
            border-radius: 0 0 0 10px;
            padding: 6px 20px;
            font-weight: 900;
            font-size: 1.2rem;
            cursor: pointer;
            display: none;
            color: var(--text-color);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.2s;
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
