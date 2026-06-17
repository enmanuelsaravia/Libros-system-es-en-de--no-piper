import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os

dirs = [os.path.join(PROJECT_ROOT, 'htm'), os.path.join(PROJECT_ROOT, 'htm+audio')]

old_css = """        #show-header-btn {
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
        }

        #hide-header-btn:hover, #show-header-btn:hover {
            opacity: 0.8;
        }"""

new_css = """        #top-right-controls {
            position: fixed;
            top: 0;
            right: 0;
            z-index: 10000;
            display: flex;
        }

        #sano-btn {
            background: var(--toolbar-bg);
            border: 2px solid var(--border-color);
            border-top: none;
            border-right: 1px solid var(--border-color);
            border-radius: 0 0 0 10px;
            padding: 6px 15px;
            font-weight: 900;
            font-size: 1rem;
            cursor: pointer;
            color: var(--text-color);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        #show-header-btn {
            background: var(--toolbar-bg);
            border: 2px solid var(--border-color);
            border-top: none;
            border-right: none;
            border-left: none;
            border-radius: 0 0 0 10px;
            padding: 6px 20px;
            font-weight: 900;
            font-size: 1.2rem;
            cursor: pointer;
            display: none;
            color: var(--text-color);
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            transition: all 0.2s;
        }

        #hide-header-btn:hover, #show-header-btn:hover, #sano-btn:hover {
            opacity: 0.8;
        }

        body.sano-mode #main-container {
            opacity: 0;
            pointer-events: none;
        }

        body.sano-mode header {
            background: transparent !important;
            border-color: transparent !important;
            box-shadow: none !important;
            backdrop-filter: none !important;
        }

        body.sano-mode header > .title-group,
        body.sano-mode header .controls > *:not(.page-controls) {
            display: none !important;
        }"""

old_html = """    <button id="show-header-btn" title="Mostrar Menú">
        ↓
    </button>"""

new_html = """    <div id="top-right-controls">
        <button id="sano-btn" title="Modo Sano">
            <span id="sano-btn-text">o-o</span>
        </button>
        <button id="show-header-btn" title="Mostrar Menú">
            ↓
        </button>
    </div>"""

old_js = """        if (hideHeaderBtn && showHeaderBtn && headerEl) {
            hideHeaderBtn.addEventListener('click', () => {
                headerEl.style.display = 'none';
                showHeaderBtn.style.display = 'block';
                window.dispatchEvent(new Event('resize'));
            });

            showHeaderBtn.addEventListener('click', () => {
                headerEl.style.display = 'flex';
                showHeaderBtn.style.display = 'none';
                window.dispatchEvent(new Event('resize'));
            });
        }"""

new_js = """        if (hideHeaderBtn && showHeaderBtn && headerEl) {
            hideHeaderBtn.addEventListener('click', () => {
                headerEl.style.display = 'none';
                showHeaderBtn.style.display = 'block';
                window.dispatchEvent(new Event('resize'));
            });

            showHeaderBtn.addEventListener('click', () => {
                headerEl.style.display = 'flex';
                showHeaderBtn.style.display = 'none';
                window.dispatchEvent(new Event('resize'));
            });
        }

        const sanoBtn = document.getElementById('sano-btn');
        if (sanoBtn) {
            sanoBtn.addEventListener('click', () => {
                document.body.classList.toggle('sano-mode');
                const isSano = document.body.classList.contains('sano-mode');
                
                const sanoBtnText = document.getElementById('sano-btn-text');
                if (sanoBtnText) {
                    sanoBtnText.textContent = isSano ? 'U_U' : 'o-o';
                }

                if (isSano && headerEl && headerEl.style.display === 'none') {
                    headerEl.style.display = 'flex';
                    if (showHeaderBtn) showHeaderBtn.style.display = 'none';
                }
            });
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
                    
                    modified = False
                    if old_css in content:
                        content = content.replace(old_css, new_css)
                        modified = True
                    if old_html in content:
                        content = content.replace(old_html, new_html)
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
