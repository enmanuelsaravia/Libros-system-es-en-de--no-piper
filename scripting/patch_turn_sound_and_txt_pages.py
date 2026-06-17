import os
import base64
import glob

def get_base64_audio():
    wav_path = "/home/user/Libros-system-es-en-de--no-piper/var/sonido-cambio-pagina.wav"
    if not os.path.exists(wav_path):
        wav_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "var", "sonido-cambio-pagina.wav")
    
    if os.path.exists(wav_path):
        with open(wav_path, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode('utf-8')
    return ""

def patch_file(file_path, audio_b64):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    changed = False

    # 1. Update #top-right-controls z-index
    old_tr = """        #top-right-controls {
            position: fixed;
            top: 0;
            right: 0;
            z-index: 10000;
            display: flex;
        }"""
    new_tr = """        #top-right-controls {
            position: fixed;
            top: 0;
            right: 0;
            z-index: 100000;
            display: flex;
        }"""
    if old_tr in content:
        content = content.replace(old_tr, new_tr)
        changed = True

    # 2. Update playPageTurnSound
    old_sound_func = """        function playPageTurnSound() {
            try {
                const AudioContext = window.AudioContext || window.webkitAudioContext;
                if (!AudioContext) return;
                const ctx = new AudioContext();
                const bufferSize = ctx.sampleRate * 0.15;
                const buffer = ctx.createBuffer(1, bufferSize, ctx.sampleRate);
                const data = buffer.getChannelData(0);
                for (let i = 0; i < bufferSize; i++) {
                    data[i] = Math.random() * 2 - 1;
                }
                const noise = ctx.createBufferSource();
                noise.buffer = buffer;
                const filter = ctx.createBiquadFilter();
                filter.type = 'bandpass';
                filter.frequency.value = 350;
                filter.Q.value = 1.0;
                const gain = ctx.createGain();
                gain.gain.setValueAtTime(0.08, ctx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, ctx.currentTime + 0.15);
                noise.connect(filter);
                filter.connect(gain);
                gain.connect(ctx.destination);
                noise.start();
            } catch (e) {
                console.error("AudioContext error:", e);
            }
        }"""
    
    new_sound_func = f"""        let pageTurnAudio = null;
        function playPageTurnSound() {{
            try {{
                if (!pageTurnAudio) {{
                    pageTurnAudio = new Audio("data:audio/wav;base64,{audio_b64}");
                }}
                pageTurnAudio.currentTime = 0;
                pageTurnAudio.play().catch(e => console.error("Audio play failed:", e));
            }} catch (e) {{
                console.error("Audio error:", e);
            }}
        }}"""
    
    if old_sound_func in content:
        content = content.replace(old_sound_func, new_sound_func)
        changed = True

    # 3. Update renderPage to call playPageTurnSound on page changes
    old_render_vars = """        let pdfDoc = null,
            pageNum = initialPage,
            pageRendering = false,
            pageNumPending = null,
            scale = 1.5,
            canvasContainer = document.getElementById('pdf-viewer');

        function renderPage(num) {
            pageRendering = true;"""
            
    new_render_vars = """        let pdfDoc = null,
            pageNum = initialPage,
            pageRendering = false,
            pageNumPending = null,
            scale = 1.5,
            canvasContainer = document.getElementById('pdf-viewer'),
            lastPageNum = null;

        function renderPage(num) {
            if (lastPageNum !== null && lastPageNum !== num) {
                playPageTurnSound();
            }
            lastPageNum = num;
            pageRendering = true;"""
            
    if old_render_vars in content:
        content = content.replace(old_render_vars, new_render_vars)
        changed = True

    # 4. Update U_U transition to keep showHeaderBtn visible
    old_transition = """                } else if (currentVal === 'U_U') {
                    // Transition to txt (Text/Vociferar)
                    sanoBtnText.textContent = 'txt';
                    document.body.classList.remove('sano-mode');
                    document.body.classList.add('txt-mode');
                    const overlay = document.getElementById('fullscreen-overlay');
                    if (overlay) overlay.style.display = 'flex';
                    
                    if (headerEl && headerEl.style.display === 'none') {
                        headerEl.style.display = 'flex';
                        if (showHeaderBtn) showHeaderBtn.style.display = 'none';
                    }
                    speakCurrentPage();"""

    new_transition = """                } else if (currentVal === 'U_U') {
                    // Transition to txt (Text/Vociferar)
                    sanoBtnText.textContent = 'txt';
                    document.body.classList.remove('sano-mode');
                    document.body.classList.add('txt-mode');
                    const overlay = document.getElementById('fullscreen-overlay');
                    if (overlay) overlay.style.display = 'flex';
                    
                    // En modo texto grande, queremos ver el indicador de página (show-header-btn) siempre
                    if (showHeaderBtn) showHeaderBtn.style.display = 'block';
                    
                    speakCurrentPage();"""

    if old_transition in content:
        content = content.replace(old_transition, new_transition)
        changed = True

    # 5. Update exitTxtMode to restore showHeaderBtn properly
    old_exit = """        function exitTxtMode() {
            isReading = false;
            if (typeof speechSynthesis !== 'undefined' && speechSynthesis.speaking) {
                speechSynthesis.cancel();
            }
            const overlay = document.getElementById('fullscreen-overlay');
            if (overlay) overlay.style.display = 'none';
            document.body.classList.remove('txt-mode');
            const sanoBtnText = document.getElementById('sano-btn-text');
            if (sanoBtnText) {
                sanoBtnText.textContent = 'o-o';
            }
            const globalPlayBtn = document.getElementById('global-play-btn');
            if (globalPlayBtn) {
                globalPlayBtn.textContent = '>';
            }
        }"""

    new_exit = """        function exitTxtMode() {
            isReading = false;
            if (typeof speechSynthesis !== 'undefined' && speechSynthesis.speaking) {
                speechSynthesis.cancel();
            }
            const overlay = document.getElementById('fullscreen-overlay');
            if (overlay) overlay.style.display = 'none';
            document.body.classList.remove('txt-mode');
            const sanoBtnText = document.getElementById('sano-btn-text');
            if (sanoBtnText) {
                sanoBtnText.textContent = 'o-o';
            }
            const globalPlayBtn = document.getElementById('global-play-btn');
            if (globalPlayBtn) {
                globalPlayBtn.textContent = '>';
            }
            // Restaurar visualización de showHeaderBtn según visibilidad del header
            const headerEl = document.querySelector('header');
            const showHeaderBtn = document.getElementById('show-header-btn');
            if (headerEl && showHeaderBtn) {
                if (headerEl.style.display === 'none') {
                    showHeaderBtn.style.display = 'block';
                } else {
                    showHeaderBtn.style.display = 'none';
                }
            }
        }"""

    if old_exit in content:
        content = content.replace(old_exit, new_exit)
        changed = True

    # 6. Update showHeaderBtn click listener to prevent hiding in txt-mode
    old_click = """        showHeaderBtn.addEventListener('click', () => {
            if (headerEl) headerEl.style.display = 'flex';
            showHeaderBtn.style.display = 'none';
        });"""

    new_click = """        showHeaderBtn.addEventListener('click', () => {
            if (document.body.classList.contains('txt-mode')) return;
            if (headerEl) headerEl.style.display = 'flex';
            showHeaderBtn.style.display = 'none';
        });"""

    if old_click in content:
        content = content.replace(old_click, new_click)
        changed = True

    # 7. Update utterance.onerror to handle not-allowed
    old_utt_onerror = """                utterance.onerror = (e) => {
                    if (e && e.error === 'interrupted') return;
                    setTimeout(() => {
                        currentChunkIndex++;
                        playNext();
                    }, 150);
                };"""
    new_utt_onerror = """                let resumeOnInteraction = null;
                utterance.onerror = (e) => {
                    if (e && e.error === 'not-allowed') {
                        console.warn("SpeechSynthesis blocked by autoplay policy. Waiting for user interaction...");
                        if (!resumeOnInteraction) {
                            resumeOnInteraction = () => {
                                document.removeEventListener('click', resumeOnInteraction);
                                document.removeEventListener('keydown', resumeOnInteraction);
                                playNext();
                            };
                            document.addEventListener('click', resumeOnInteraction);
                            document.addEventListener('keydown', resumeOnInteraction);
                        }
                        return;
                    }
                    if (e && e.error === 'interrupted') return;
                    setTimeout(() => {
                        currentChunkIndex++;
                        playNext();
                    }, 150);
                };"""
    if old_utt_onerror in content:
        content = content.replace(old_utt_onerror, new_utt_onerror)
        changed = True

    # 8. Update mensaje.onerror to handle not-allowed (for generated files)
    old_msg_onerror = """            mensaje.onerror = (e) => {
                if (e && e.error !== 'interrupted') {
                    console.error("SpeechSynthesis error:", e);
                }
                stopAllAudio();
            };"""
    new_msg_onerror = """            let resumeOnInteraction = null;
            mensaje.onerror = (e) => {
                if (e && e.error === 'not-allowed') {
                    console.warn("SpeechSynthesis blocked by autoplay policy. Waiting for user interaction...");
                    if (!resumeOnInteraction) {
                        resumeOnInteraction = () => {
                            document.removeEventListener('click', resumeOnInteraction);
                            document.removeEventListener('keydown', resumeOnInteraction);
                            toggleAudio(lang);
                        };
                        document.addEventListener('click', resumeOnInteraction);
                        document.addEventListener('keydown', resumeOnInteraction);
                    }
                } else if (e && e.error !== 'interrupted') {
                    console.error("SpeechSynthesis error:", e);
                }
                stopAllAudio();
            };"""
    if old_msg_onerror in content:
        content = content.replace(old_msg_onerror, new_msg_onerror)
        changed = True

    if changed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Patched: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
    return False

def main():
    print("Encoding audio...")
    audio_b64 = get_base64_audio()
    if not audio_b64:
        print("Error: Could not find/encode sonido-cambio-pagina.wav")
        return

    print("Scanning files to patch...")
    target_files = []

    for root, dirs, files in os.walk("/home/user"):
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file == "htm.htm":
                target_files.append(os.path.join(root, file))
            elif file.endswith(".htm"):
                if "Processed_" in root:
                    target_files.append(os.path.join(root, file))

    print(f"Found {len(target_files)} potential target files.")
    patched_count = 0
    for path in target_files:
        if patch_file(path, audio_b64):
            patched_count += 1

    print(f"Done. Patched {patched_count} files.")

if __name__ == "__main__":
    main()
