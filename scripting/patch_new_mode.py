import os
import sys

def patch_file(file_path):
    print(f"Reading {file_path}...")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False

    changed = False

    # 1. Styles
    old_styles = """        input:checked + .slider:before {
            transform: translateX(16px);
        }
    </style>"""
    new_styles = """        input:checked + .slider:before {
            transform: translateX(16px);
        }

        .nav-btn-fullscreen {
            display: none;
            position: absolute;
            top: 50%;
            transform: translateY(-50%);
            background: transparent;
            border: none;
            color: #000000;
            font-size: 5rem;
            font-weight: 300;
            cursor: pointer;
            user-select: none;
            z-index: 100001;
            opacity: 0.15;
            transition: opacity 0.2s, transform 0.2s;
            padding: 2rem 1.5rem;
            outline: none;
            font-family: monospace;
        }

        .nav-btn-fullscreen:hover {
            opacity: 0.7;
            transform: translateY(-50%) scale(1.1);
        }

        .nav-btn-fullscreen:active {
            transform: translateY(-50%) scale(0.95);
        }

        #fullscreen-prev-btn {
            left: 1.5rem;
        }

        #fullscreen-next-btn {
            right: 1.5rem;
        }

        body.txt-manual-mode .nav-btn-fullscreen {
            display: block;
        }
    </style>"""

    if old_styles in content:
        content = content.replace(old_styles, new_styles)
        changed = True
        print("Patched styles.")

    # 2. HTML overlay
    old_overlay = """    <!-- Overlay de pantalla completa -->
    <div id="fullscreen-overlay">
        <div id="fullscreen-text"></div>
        <div class="exit-hint">Haz clic o presiona ESC para salir</div>
    </div>"""
    new_overlay = """    <!-- Overlay de pantalla completa -->
    <div id="fullscreen-overlay">
        <button id="fullscreen-prev-btn" class="nav-btn-fullscreen">&lt;</button>
        <div id="fullscreen-text"></div>
        <button id="fullscreen-next-btn" class="nav-btn-fullscreen">&gt;</button>
        <div class="exit-hint">Haz clic o presiona ESC para salir</div>
    </div>"""

    if old_overlay in content:
        content = content.replace(old_overlay, new_overlay)
        changed = True
        print("Patched HTML overlay.")

    # 3. Variables
    old_vars = """        let pdfDoc = null,
            pageNum = initialPage,
            pageRendering = false,
            pageNumPending = null,
            scale = 1.5,
            canvasContainer = document.getElementById('pdf-viewer'),
            lastPageNum = null;"""
    new_vars = """        let pdfDoc = null,
            pageNum = initialPage,
            pageRendering = false,
            pageNumPending = null,
            scale = 1.5,
            canvasContainer = document.getElementById('pdf-viewer'),
            lastPageNum = null,
            manualPagePreferLast = false;"""

    if old_vars in content:
        content = content.replace(old_vars, new_vars)
        changed = True
        print("Patched variables.")

    # 4. RenderPage ending
    old_render_end = """            if (document.body.classList.contains('txt-mode')) {
                speakCurrentPage();
            }
        }"""
    new_render_end = """            if (document.body.classList.contains('txt-mode')) {
                speakCurrentPage();
            } else if (document.body.classList.contains('txt-manual-mode')) {
                showManualCurrentPage(manualPagePreferLast);
                manualPagePreferLast = false;
            }
        }"""

    if old_render_end in content:
        content = content.replace(old_render_end, new_render_end)
        changed = True
        print("Patched renderPage end.")

    # 5. Keydown listener
    old_keydown = """        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowRight' || e.key === 'PageDown') onNextPage();
            if (e.key === 'ArrowLeft' || e.key === 'PageUp') onPrevPage();
        });"""
    new_keydown = """        document.addEventListener('keydown', (e) => {
            if (document.body.classList.contains('txt-manual-mode')) {
                if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'Spacebar') {
                    e.preventDefault();
                    onNextManualChunk();
                    return;
                }
                if (e.key === 'ArrowLeft') {
                    e.preventDefault();
                    onPrevManualChunk();
                    return;
                }
            }
            if (e.key === 'ArrowRight' || e.key === 'PageDown') onNextPage();
            if (e.key === 'ArrowLeft' || e.key === 'PageUp') onPrevPage();
        });"""

    if old_keydown in content:
        content = content.replace(old_keydown, new_keydown)
        changed = True
        print("Patched keydown listener.")

    # 6. exitTxtMode function start
    old_exit_start = """        function exitTxtMode() {
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
            const globalPlayBtn = document.getElementById('global-play-btn');"""
    
    new_exit_start = """        function exitTxtMode() {
            isReading = false;
            if (typeof speechSynthesis !== 'undefined' && speechSynthesis.speaking) {
                speechSynthesis.cancel();
            }
            const overlay = document.getElementById('fullscreen-overlay');
            if (overlay) overlay.style.display = 'none';
            document.body.classList.remove('txt-mode');
            document.body.classList.remove('txt-manual-mode');
            const sanoBtnText = document.getElementById('sano-btn-text');
            if (sanoBtnText) {
                sanoBtnText.textContent = 'o-o';
            }
            const globalPlayBtn = document.getElementById('global-play-btn');"""

    if old_exit_start in content:
        content = content.replace(old_exit_start, new_exit_start)
        changed = True
        print("Patched exitTxtMode start.")

    # 7. Navigation functions in exitTxtMode end
    old_exit_end = """            // Restaurar visualización de showHeaderBtn según visibilidad del header
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

    new_exit_end = """            // Restaurar visualización de showHeaderBtn según visibilidad del header
            const headerEl = document.querySelector('header');
            const showHeaderBtn = document.getElementById('show-header-btn');
            if (headerEl && showHeaderBtn) {
                if (headerEl.style.display === 'none') {
                    showHeaderBtn.style.display = 'block';
                } else {
                    showHeaderBtn.style.display = 'none';
                }
            }
        }

        function showCurrentManualChunk() {
            if (!currentChunks || currentChunks.length === 0) {
                fitText("Página sin texto");
                return;
            }
            if (currentChunkIndex < 0) {
                currentChunkIndex = 0;
            }
            if (currentChunkIndex >= currentChunks.length) {
                currentChunkIndex = currentChunks.length - 1;
            }
            fitText(currentChunks[currentChunkIndex]);
        }

        function onNextManualChunk() {
            if (!document.body.classList.contains('txt-manual-mode')) return;
            if (currentChunkIndex < currentChunks.length - 1) {
                currentChunkIndex++;
                showCurrentManualChunk();
            } else {
                if (pageNum < pdfDoc.numPages) {
                    pageNum++;
                    const pageNumEl = pipWindow ? pipWindow.document.getElementById('page-num') : document.getElementById('page-num');
                    if (pageNumEl) pageNumEl.value = pageNum;
                    const showHeaderBtn = document.getElementById('show-header-btn');
                    if (showHeaderBtn && pdfDoc) {
                        showHeaderBtn.textContent = '↓ ' + pageNum + '/' + pdfDoc.numPages;
                    }
                    queueRenderPage(pageNum);
                } else {
                    exitTxtMode();
                }
            }
        }

        function onPrevManualChunk() {
            if (!document.body.classList.contains('txt-manual-mode')) return;
            if (currentChunkIndex > 0) {
                currentChunkIndex--;
                showCurrentManualChunk();
            } else {
                if (pageNum > 1) {
                    pageNum--;
                    const pageNumEl = pipWindow ? pipWindow.document.getElementById('page-num') : document.getElementById('page-num');
                    if (pageNumEl) pageNumEl.value = pageNum;
                    const showHeaderBtn = document.getElementById('show-header-btn');
                    if (showHeaderBtn && pdfDoc) {
                        showHeaderBtn.textContent = '↓ ' + pageNum + '/' + pdfDoc.numPages;
                    }
                    manualPagePreferLast = true;
                    queueRenderPage(pageNum);
                }
            }
        }

        function showManualCurrentPage(preferLastChunk = false) {
            if (typeof speechSynthesis !== 'undefined') {
                speechSynthesis.cancel();
            }
            isReading = false;
            if (!pdfDoc) return;
            
            const overlay = document.getElementById('fullscreen-overlay');
            if (overlay) overlay.style.display = 'flex';
            
            const onTextReady = (text) => {
                const chunks = parseChunks(text);
                currentChunks = chunks;
                if (preferLastChunk && chunks.length > 0) {
                    currentChunkIndex = chunks.length - 1;
                } else {
                    currentChunkIndex = 0;
                }
                showCurrentManualChunk();
            };

            if (typeof textMap !== 'undefined' && textMap[pageNum]) {
                let useLang = 'es';
                if (typeof activeLang !== 'undefined' && activeLang && textMap[pageNum][activeLang]) {
                    useLang = activeLang;
                } else if (typeof fallbackChain !== 'undefined' && fallbackChain) {
                    for (let i = 0; i < fallbackChain.length; i++) {
                        const l = fallbackChain[i];
                        if (textMap[pageNum][l] && textMap[pageNum][l].trim()) {
                            useLang = l;
                            break;
                        }
                    }
                } else {
                    let lang = 'es';
                    const lowerName = (fileName || "").toLowerCase();
                    if (lowerName.includes('-en-') || lowerName.includes('_en_') || lowerName.includes('.en.')) {
                        lang = 'en';
                    } else if (lowerName.includes('-de-') || lowerName.includes('_de_') || lowerName.includes('.de.')) {
                        lang = 'de';
                    }
                    if (textMap[pageNum][lang] && textMap[pageNum][lang].trim()) {
                        useLang = lang;
                    } else {
                        for (const l of ['es', 'en', 'de']) {
                            if (textMap[pageNum][l] && textMap[pageNum][l].trim()) {
                                useLang = l;
                                break;
                            }
                        }
                    }
                }
                const pageText = textMap[pageNum][useLang] || "";
                onTextReady(pageText);
            } else {
                pdfDoc.getPage(pageNum).then(page => {
                    return page.getTextContent();
                }).then(textContent => {
                    const text = textContent.items.map(item => item.str).join(' ');
                    onTextReady(text);
                }).catch(err => {
                    console.error("Error reading page text:", err);
                    fitText("Error al cargar texto");
                });
            }
        }"""

    if old_exit_end in content:
        content = content.replace(old_exit_end, new_exit_end)
        changed = True
        print("Patched manual navigation functions.")

    # 8. Sano-btn listener transitions
    old_transitions = """                } else if (currentVal === 'U_U') {
                    // Transition to txt (Text/Vociferar)
                    sanoBtnText.textContent = 'txt';
                    document.body.classList.remove('sano-mode');
                    document.body.classList.add('txt-mode');
                    const overlay = document.getElementById('fullscreen-overlay');
                    if (overlay) overlay.style.display = 'flex';
                    
                    // En modo texto grande, queremos ver el indicador de página (show-header-btn) siempre
                    if (showHeaderBtn) showHeaderBtn.style.display = 'block';
                    
                    speakCurrentPage();
                } else {
                    // Transition back to o-o (Lentecitos)
                    sanoBtnText.textContent = 'o-o';
                    document.body.classList.remove('sano-mode');
                    document.body.classList.remove('txt-mode');
                    const overlay = document.getElementById('fullscreen-overlay');
                    if (overlay) overlay.style.display = 'none';
                    isReading = false;
                    if (typeof speechSynthesis !== 'undefined') speechSynthesis.cancel();
                }"""

    new_transitions = """                } else if (currentVal === 'U_U') {
                    // Transition to txt (Text/Vociferar)
                    sanoBtnText.textContent = 'txt';
                    document.body.classList.remove('sano-mode');
                    document.body.classList.add('txt-mode');
                    const overlay = document.getElementById('fullscreen-overlay');
                    if (overlay) overlay.style.display = 'flex';
                    
                    // En modo texto grande, queremos ver el indicador de página (show-header-btn) siempre
                    if (showHeaderBtn) showHeaderBtn.style.display = 'block';
                    
                    speakCurrentPage();
                } else if (currentVal === 'txt') {
                    // Transition to txt > (Text/Vociferar - manual)
                    sanoBtnText.textContent = 'txt >';
                    document.body.classList.remove('sano-mode');
                    document.body.classList.remove('txt-mode');
                    document.body.classList.add('txt-manual-mode');
                    const overlay = document.getElementById('fullscreen-overlay');
                    if (overlay) overlay.style.display = 'flex';
                    
                    if (showHeaderBtn) showHeaderBtn.style.display = 'block';
                    
                    showManualCurrentPage(false);
                } else {
                    // Transition back to o-o (Lentecitos)
                    sanoBtnText.textContent = 'o-o';
                    document.body.classList.remove('sano-mode');
                    document.body.classList.remove('txt-mode');
                    document.body.classList.remove('txt-manual-mode');
                    const overlay = document.getElementById('fullscreen-overlay');
                    if (overlay) overlay.style.display = 'none';
                    isReading = false;
                    if (typeof speechSynthesis !== 'undefined') speechSynthesis.cancel();
                    
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

    if old_transitions in content:
        content = content.replace(old_transitions, new_transitions)
        changed = True
        print("Patched sano-btn transitions.")

    # 9. Overlay click and prev/next listeners
    old_overlay_click = """        const fullscreenOverlay = document.getElementById('fullscreen-overlay');
        if (fullscreenOverlay) {
            fullscreenOverlay.addEventListener('click', exitTxtMode);
        }"""
    
    new_overlay_click = """        const fullscreenOverlay = document.getElementById('fullscreen-overlay');
        if (fullscreenOverlay) {
            fullscreenOverlay.addEventListener('click', exitTxtMode);
        }

        const prevBtn = document.getElementById('fullscreen-prev-btn');
        if (prevBtn) {
            prevBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (document.body.classList.contains('txt-manual-mode')) {
                    onPrevManualChunk();
                }
            });
        }
        const nextBtn = document.getElementById('fullscreen-next-btn');
        if (nextBtn) {
            nextBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                if (document.body.classList.contains('txt-manual-mode')) {
                    onNextManualChunk();
                }
            });
        }"""

    if old_overlay_click in content:
        content = content.replace(old_overlay_click, new_overlay_click)
        changed = True
        print("Patched overlay click/navigation listeners.")

    if changed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Successfully patched {file_path}")
            return True
        except Exception as e:
            print(f"Error writing file {file_path}: {e}")
    else:
        print(f"No changes made to {file_path}")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python patch_new_mode.py <file_to_patch>")
        sys.exit(1)
    patch_file(sys.argv[1])
