import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os

dirs = [os.path.join(PROJECT_ROOT, 'htm'), os.path.join(PROJECT_ROOT, 'htm+audio')]

old_js = """        function updateSanoClock() {
            const clockEl = document.getElementById('sano-clock');
            if (!clockEl) return;
            const now = new Date();
            clockEl.textContent = now.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
        }"""

new_js = """        function updateSanoClock() {
            const clockEl = document.getElementById('sano-clock');
            if (!clockEl) return;
            const now = new Date();
            const days = ['Dom', 'Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb'];
            const dayName = days[now.getDay()];
            const hh = String(now.getHours()).padStart(2, '0');
            const mm = String(now.getMinutes()).padStart(2, '0');
            const ss = String(now.getSeconds()).padStart(2, '0');
            const dd = String(now.getDate()).padStart(2, '0');
            const mo = String(now.getMonth() + 1).padStart(2, '0');
            const yyyy = now.getFullYear();
            clockEl.textContent = `${hh}:${mm}:${ss} ${dayName} ${dd}/${mo}/${yyyy}`;
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
                    
                    if old_js in content:
                        content = content.replace(old_js, new_js)
                        with open(f_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {f_path}: {e}")

print(f"Done processing {count} files.")
