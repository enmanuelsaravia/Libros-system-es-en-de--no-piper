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

    # 1. Add URL parsing for reqLang
    target_1 = """        const pageTurnSoundSrc ="""
    if "const urlParamsAudio = new URLSearchParams(" not in new_content and target_1 in new_content:
        replacement_1 = """        // Get requested lang from URL
        const urlParamsAudio = new URLSearchParams(window.location.search);
        const reqLang = urlParamsAudio.get('lang');
        const fallbackChain = [];
        if (reqLang) fallbackChain.push(reqLang.toLowerCase());
        ['es', 'en', 'de'].forEach(l => {
            if (!fallbackChain.includes(l)) fallbackChain.push(l);
        });

        const pageTurnSoundSrc ="""
        new_content = new_content.replace(target_1, replacement_1, 1)

    # 2. Change the autoplay logic
    target_2 = """            if (autoplayActive && document.body.classList.contains('sano-mode')) {
                if (audioMap[num] && audioMap[num]['es']) {
                    setTimeout(() => toggleAudio('es'), 400);
                } else if (audioMap[num] && audioMap[num]['en']) {
                    setTimeout(() => toggleAudio('en'), 400);
                } else if (audioMap[num] && audioMap[num]['de']) {
                    setTimeout(() => toggleAudio('de'), 400);
                }
            }"""
    
    replacement_2 = """            if (autoplayActive && document.body.classList.contains('sano-mode')) {
                for (let i = 0; i < fallbackChain.length; i++) {
                    const l = fallbackChain[i];
                    if (audioMap[num] && audioMap[num][l]) {
                        setTimeout(() => toggleAudio(l), 400);
                        break;
                    }
                }
            }"""

    if target_2 in new_content:
        new_content = new_content.replace(target_2, replacement_2, 1)
    
    # 3. Alternative target_2 if they have different spaces or it was modified before
    target_3 = """            // Autoplay only if Sano Mode is currently active
            if (autoplayActive && document.body.classList.contains('sano-mode')) {
                if (audioMap[num] && audioMap[num]['es']) {
                    setTimeout(() => toggleAudio('es'), 400);
                } else if (audioMap[num] && audioMap[num]['en']) {
                    setTimeout(() => toggleAudio('en'), 400);
                } else if (audioMap[num] && audioMap[num]['de']) {
                    setTimeout(() => toggleAudio('de'), 400);
                }
            }"""
    
    replacement_3 = """            // Autoplay only if Sano Mode is currently active
            if (autoplayActive && document.body.classList.contains('sano-mode')) {
                for (let i = 0; i < fallbackChain.length; i++) {
                    const l = fallbackChain[i];
                    if (audioMap[num] && audioMap[num][l]) {
                        setTimeout(() => toggleAudio(l), 400);
                        break;
                    }
                }
            }"""
    
    if target_3 in new_content:
        new_content = new_content.replace(target_3, replacement_3, 1)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        count += 1

print(f"Updated {count} files.")
