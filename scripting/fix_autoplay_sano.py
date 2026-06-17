import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import os

dirs = [os.path.join(PROJECT_ROOT, 'htm+audio')]

old_js = """        function updateAudioButtons(num) {
            stopAllAudio();
            const langs = ['en', 'es', 'de'];
            langs.forEach(lang => {
                const btn = document.getElementById('play-' + lang);
                if (btn) {
                    const hasAudio = audioMap[num] && audioMap[num][lang];
                    if (hasAudio) {
                        btn.removeAttribute('disabled');
                        btn.textContent = 'Play ' + lang;
                    } else {
                        btn.setAttribute('disabled', 'true');
                        btn.textContent = 'Play ' + lang + ' (Sin audio)';
                    }
                }
            });
        }"""

new_js = """        function updateAudioButtons(num) {
            stopAllAudio();
            const langs = ['en', 'es', 'de'];
            langs.forEach(lang => {
                const btn = document.getElementById('play-' + lang);
                if (btn) {
                    const hasAudio = audioMap[num] && audioMap[num][lang];
                    if (hasAudio) {
                        btn.removeAttribute('disabled');
                        btn.textContent = 'Play ' + lang;
                    } else {
                        btn.setAttribute('disabled', 'true');
                        btn.textContent = 'Play ' + lang + ' (Sin audio)';
                    }
                }
            });

            // Start in Sano mode and Autoplay if checked
            const autoplayActive = document.getElementById('autoplay-toggle')?.checked;
            if (autoplayActive) {
                // Ensure sano mode is active
                if (!document.body.classList.contains('sano-mode')) {
                    document.body.classList.add('sano-mode');
                    if (typeof headerEl !== 'undefined' && headerEl && headerEl.style.display !== 'none') {
                        headerEl.style.display = 'none';
                        if (typeof showHeaderBtn !== 'undefined' && showHeaderBtn) showHeaderBtn.style.display = 'block';
                    }
                }
                
                // Play Spanish by default
                if (audioMap[num] && audioMap[num]['es']) {
                    setTimeout(() => toggleAudio('es'), 400);
                } else if (audioMap[num] && audioMap[num]['en']) {
                    setTimeout(() => toggleAudio('en'), 400);
                } else if (audioMap[num] && audioMap[num]['de']) {
                    setTimeout(() => toggleAudio('de'), 400);
                }
            }
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
