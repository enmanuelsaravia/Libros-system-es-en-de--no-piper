import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os
import glob
import re

htm_dir = f"{PROJECT_ROOT}/htm+audio"
files = glob.glob(os.path.join(htm_dir, "*.htm"))

count = 0
for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content

    # 1. Update activeAudio.onended block
    # Since there are multiple possible previous states (one with langToContinue, one without), let's use regex
    # The previous block was:
    #             activeAudio.onended = () => {
    #                 const langToContinue = activeLang;
    #                 stopAllAudio();
    # ...
    #                             onNextPage();
    #                             setTimeout(() => {
    #                                 toggleAudio(langToContinue);
    #                             }, 400);
    # ...
    
    # We want to replace it entirely up to `};` at the end of onended.
    pattern_onended = re.compile(r'activeAudio\.onended\s*=\s*\(\)\s*=>\s*\{.*?\n            \};\n', re.DOTALL)
    
    replacement_onended = """activeAudio.onended = () => {
                stopAllAudio();
                
                const autoplayActive = document.getElementById('autoplay-toggle')?.checked;
                if (autoplayActive && pageNum < pdfDoc.numPages) {
                    if (pageTurnAudio) {
                        pageTurnAudio.play().catch(e => console.error("Error reproduciendo sonido de cambio:", e));
                        pageTurnAudio.onended = () => {
                            onNextPage();
                        };
                    } else {
                        onNextPage();
                    }
                }
            };
"""
    new_content = pattern_onended.sub(replacement_onended, new_content)

    # 2. Update toggleAudio to shift fallbackChain
    target_toggle = """            activeAudio = new Audio(pageAudioSrc);
            activeLang = lang;

            btn.textContent = 'Stop ' + lang;"""
    
    replacement_toggle = """            activeAudio = new Audio(pageAudioSrc);
            activeLang = lang;
            
            // Put this lang at the top of the fallback chain so it persists on next pages
            const idx = fallbackChain.indexOf(lang);
            if (idx > -1) fallbackChain.splice(idx, 1);
            fallbackChain.unshift(lang);

            btn.textContent = 'Stop ' + lang;"""
    if target_toggle in new_content:
        new_content = new_content.replace(target_toggle, replacement_toggle, 1)

    # 3. Update updateAudioButtons logic
    # Previous:
    #             if (autoplayActive && document.body.classList.contains('sano-mode')) {
    #                 for (let i = 0; i < fallbackChain.length; i++) {
    #                     const l = fallbackChain[i];
    #                     if (audioMap[num] && audioMap[num][l]) {
    #                         setTimeout(() => toggleAudio(l), 400);
    #                         break;
    #                     }
    #                 }
    #             }
    pattern_update = re.compile(r'// Autoplay only if Sano Mode is currently active\n            if \(autoplayActive && document\.body\.classList\.contains\(\'sano-mode\'\)\) \{\n                for \(let i = 0; i < fallbackChain\.length; i\+\+\) \{\n                    const l = fallbackChain\[i\];\n                    if \(audioMap\[num\] && audioMap\[num\]\[l\]\) \{\n                        setTimeout\(\(\) => toggleAudio\(l\), 400\);\n                        break;\n                    \}\n                \}\n            \}')
    
    replacement_update = """// Autoplay only if Sano Mode is currently active
            if (autoplayActive && document.body.classList.contains('sano-mode')) {
                let played = false;
                for (let i = 0; i < fallbackChain.length; i++) {
                    const l = fallbackChain[i];
                    if (audioMap[num] && audioMap[num][l]) {
                        setTimeout(() => toggleAudio(l), 400);
                        played = true;
                        break;
                    }
                }
                
                if (!played && pageNum < pdfDoc.numPages) {
                    if (pageTurnAudio) {
                        pageTurnAudio.play().catch(e => console.error("Error reproduciendo sonido de cambio:", e));
                        pageTurnAudio.onended = () => {
                            onNextPage();
                        };
                    } else {
                        setTimeout(() => onNextPage(), 400);
                    }
                }
            }"""
            
    new_content = pattern_update.sub(replacement_update, new_content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} files.")
