import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os

dirs = [os.path.join(PROJECT_ROOT, 'htm'), os.path.join(PROJECT_ROOT, 'htm+audio')]

old_html = """                <button id="next-page" title="Siguiente página">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
                </button>"""

new_html = """                <button id="next-page" title="Siguiente página">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
                </button>
                <span id="sano-clock"></span>"""

old_css = """        body.sano-mode #main-container {
            opacity: 0;
            pointer-events: none;
        }"""

new_css = """        #sano-clock {
            display: none;
            font-weight: bold;
            font-size: 1.1rem;
            margin-left: 10px;
            font-variant-numeric: tabular-nums;
            color: var(--text-color);
        }

        body.sano-mode #sano-clock {
            display: inline-block;
        }

        body.sano-mode #main-container {
            opacity: 0;
            pointer-events: none;
        }"""

old_js = """        const sanoBtn = document.getElementById('sano-btn');
        if (sanoBtn) {
            sanoBtn.addEventListener('click', () => {
                document.body.classList.toggle('sano-mode');
                if (document.body.classList.contains('sano-mode') && headerEl && headerEl.style.display === 'none') {
                    headerEl.style.display = 'flex';
                    if (showHeaderBtn) showHeaderBtn.style.display = 'none';
                }
            });
        }"""

new_js = """        const sanoBtn = document.getElementById('sano-btn');
        if (sanoBtn) {
            sanoBtn.addEventListener('click', () => {
                document.body.classList.toggle('sano-mode');
                if (document.body.classList.contains('sano-mode') && headerEl && headerEl.style.display === 'none') {
                    headerEl.style.display = 'flex';
                    if (showHeaderBtn) showHeaderBtn.style.display = 'none';
                }
            });
        }

        function updateSanoClock() {
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
        }
        setInterval(updateSanoClock, 1000);
        updateSanoClock();"""

count = 0
for d in dirs:
    for root, _, files in os.walk(d):
        for file in files:
            if file.endswith('.htm'):
                f_path = os.path.join(root, file)
                try:
                    with open(f_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    modified = False
                    if old_html in content:
                        content = content.replace(old_html, new_html)
                        modified = True
                    if old_css in content:
                        content = content.replace(old_css, new_css)
                        modified = True
                    if old_js in content:
                        content = content.replace(old_js, new_js)
                        modified = True
                        
                    if modified:
                        with open(f_path, 'w', encoding='utf-8') as f:
                            f.write(content)
                        count += 1
                except Exception as e:
                    print(f"Error processing {f_path}: {e}")

print(f"Done processing {count} files.")
