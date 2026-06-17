import os
import glob
import re

def patch_file(file_path):
    print(f"Patching: {file_path}")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Add .pagination-group CSS
    old_css_pc = """        .page-controls {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
            width: 100%;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }"""
    
    new_css_pc = """        .pagination-group {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
        }

        .page-controls {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1.5rem;
            width: 100%;
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }"""

    if old_css_pc in content:
        content = content.replace(old_css_pc, new_css_pc)
    else:
        # Fallback if whitespace differs
        content = re.sub(
            r'\.page-controls\s*\{\s*display:\s*flex;\s*align-items:\s*center;\s*justify-content:\s*center;\s*gap:\s*1\.5rem;\s*width:\s*100%;\s*background:\s*transparent\s*!important;\s*border:\s*none\s*!important;\s*padding:\s*0\s*!important;\s*\}',
            new_css_pc,
            content
        )

    # 2. Modify body.sano-mode #sano-clock and add time/date and page-controls styles
    old_clock_sano = """        body.sano-mode #sano-clock {
            display: inline-block;
        }"""

    new_clock_sano = """        body.sano-mode #sano-clock {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            text-align: center;
            margin-left: 0;
        }

        body.sano-mode .sano-time {
            font-size: 2.2rem;
            font-weight: 800;
            color: var(--text-color);
            margin: 0;
            padding: 0;
            line-height: 1;
        }

        body.sano-mode .sano-date {
            font-size: 1.4rem;
            font-weight: 500;
            color: var(--text-color);
            opacity: 0.85;
            margin-top: 0.25rem;
        }

        body.sano-mode .page-controls {
            flex-direction: column;
            gap: 1.5rem;
            align-items: center;
            justify-content: center;
        }"""

    if old_clock_sano in content:
        content = content.replace(old_clock_sano, new_clock_sano)
    else:
        content = re.sub(
            r'body\.sano-mode\s*#sano-clock\s*\{\s*display:\s*inline-block;\s*\}',
            new_clock_sano,
            content
        )

    # 3. HTML structure update: wrap pagination controls inside .pagination-group
    old_html = """            <div class="page-controls">
                <button id="prev-page" title="Página anterior">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg>
                </button>
                <input type="number" id="page-num" value="1" min="1">
                <span class="total-pages">/ <span id="page-count">0</span></span>
                <button id="next-page" title="Siguiente página">
                    <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
                </button>
                <span id="sano-clock"></span>
            </div>"""

    new_html = """            <div class="page-controls">
                <div class="pagination-group">
                    <button id="prev-page" title="Página anterior">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m15 18-6-6 6-6"/></svg>
                    </button>
                    <input type="number" id="page-num" value="1" min="1">
                    <span class="total-pages">/ <span id="page-count">0</span></span>
                    <button id="next-page" title="Siguiente página">
                        <svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="m9 18 6-6-6-6"/></svg>
                    </button>
                </div>
                <span id="sano-clock"></span>
            </div>"""

    if old_html in content:
        content = content.replace(old_html, new_html)
    else:
        # Fallback regex search for robustness
        pattern = re.compile(
            r'<div\s+class="page-controls">\s*'
            r'(<button\s+id="prev-page".*?</button>)\s*'
            r'(<input\s+type="number"\s+id="page-num".*?>)\s*'
            r'(<span\s+class="total-pages">.*?</span>)\s*'
            r'(<button\s+id="next-page".*?</button>)\s*'
            r'(<span\s+id="sano-clock"></span>)\s*'
            r'</div>',
            re.DOTALL
        )
        content = pattern.sub(
            r'<div class="page-controls">\n                <div class="pagination-group">\n                    \1\n                    \2\n                    \3\n                    \4\n                </div>\n                \5\n            </div>',
            content
        )

    # 4. JS clock update to split into sano-time and sano-date
    old_js = """clockEl.textContent = `${hh}:${mm}:${ss} ${ampm} ${dayName} ${dd}/${mo}/${yyyy}`;"""
    new_js = """clockEl.innerHTML = `<div class="sano-time">${hh}:${mm}:${ss} ${ampm}</div><div class="sano-date">${dayName} ${dd}/${mo}/${yyyy}</div>`;"""

    if old_js in content:
        content = content.replace(old_js, new_js)
    else:
        # fallback regex
        content = re.sub(
            r'clockEl\.textContent\s*=\s*`\$\{hh\}:\$\{mm\}:\$\{ss\}\s+\$\{ampm\}\s+\$\{dayName\}\s+\$\{dd\}/\$\{mo\}/\$\{yyyy\}`;',
            new_js,
            content
        )

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)

def main():
    scripting_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(scripting_dir)
    
    # 1. Patch the template
    template_path = os.path.join(scripting_dir, "htm.htm")
    if os.path.exists(template_path):
        patch_file(template_path)
    
    # 2. Patch all generated htm files
    htm_dirs = [os.path.join(project_root, "htm"), os.path.join(project_root, "htm+audio")]
    patched_count = 0
    for d in htm_dirs:
        if os.path.exists(d):
            files = glob.glob(os.path.join(d, "*.htm"))
            for f in files:
                patch_file(f)
                patched_count += 1
                
    print(f"Successfully patched template and {patched_count} generated files!")

if __name__ == "__main__":
    main()
