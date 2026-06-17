import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR
import os
import glob
import re

htm_dirs = [f"{PROJECT_ROOT}/htm', f"{PROJECT_ROOT}/htm+audio']
files = []
for d in htm_dirs:
    files.extend(glob.glob(os.path.join(d, '*.htm')))

for file_path in files:
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. z-index
    content = re.sub(r'(\.loading-overlay\s*\{[^}]*z-index:\s*)90(;[^}]*\})', r'\g<1>999999\g<2>', content)
    
    # 2. spinner
    spinner_pattern = r'(\.spinner\s*\{)([^}]*)(\})'
    content = re.sub(spinner_pattern, r'\g<1>\n            display: none;\n        \g<3>', content)

    # 3. loading div
    old_loading_div = '''    <div id="loading" class="loading-overlay">
        <div class="spinner"></div>
        <p style="margin-top: 1rem; font-weight: 500;">Preparando tu lectura offline...</p>
    </div>'''
    
    new_loading_div = '''    <div id="loading" class="loading-overlay">
        <div class="spinner"></div>
        <p id="loading-text" style="margin-top: 1rem; font-size: 1.2rem; font-weight: bold; font-family: monospace;">Navegador web cargando 0.00mb a la memoria RAM</p>
        <p id="loading-time" style="font-size: 1rem; color: #666; margin-top: 10px; font-family: monospace;">Tiempo estimado: calculando...</p>
    </div>

    <script>
        (function() {
            let simulatedMb = 0.0;
            const startTime = Date.now();
            let estimatedTotalMb = 10.0;
            let estimatedSeconds = 3.0;
            
            window.loadingProgressInterval = setInterval(() => {
                const elapsed = (Date.now() - startTime) / 1000;
                const speed = 10.0 / 3.0; 
                simulatedMb += speed * 0.1; 
                
                if (simulatedMb > estimatedTotalMb) {
                    estimatedTotalMb += 5.0; 
                    estimatedSeconds += 1.5;
                }
                
                const textEl = document.getElementById('loading-text');
                const timeEl = document.getElementById('loading-time');
                if (textEl) {
                    textEl.textContent = `Navegador web cargando ${simulatedMb.toFixed(2)}mb a la memoria RAM`;
                }
                if (timeEl) {
                    let remaining = Math.max(0.1, estimatedSeconds - elapsed);
                    timeEl.textContent = `Tiempo estimado: ${remaining.toFixed(1)}s`;
                }
            }, 100);
        })();
    </script>'''
    
    content = content.replace(old_loading_div, new_loading_div)

    # 4. Clear interval
    old_then = '''document.getElementById('page-count').textContent = pdfDoc.numPages;
                document.getElementById('loading').style.display = 'none';'''
    
    new_then = '''document.getElementById('page-count').textContent = pdfDoc.numPages;
                if (window.loadingProgressInterval) clearInterval(window.loadingProgressInterval);
                document.getElementById('loading').style.display = 'none';'''
    
    content = content.replace(old_then, new_then)

    old_catch = '''}).catch(err => {
                document.getElementById('loading').innerHTML = "<h2>Error: " + err.message + "</h2>";'''
    
    new_catch = '''}).catch(err => {
                if (window.loadingProgressInterval) clearInterval(window.loadingProgressInterval);
                document.getElementById('loading').innerHTML = "<h2>Error: " + err.message + "</h2>";'''
    
    content = content.replace(old_catch, new_catch)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

print(f"Patched {len(files)} files.")
