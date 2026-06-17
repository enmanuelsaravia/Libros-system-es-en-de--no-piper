#!/bin/bash
PROJECT=$1
ROOT='/home/user/Personal'
LIBROS="Libros-${PROJECT}"
if [ -d $ROOT/$LIBROS ]; then
    echo "El proyecto $ROOT/$LIBROS ya existe"
    exit 0
else
    mkdir -p /home/user/Personal/$LIBROS
    ln -svf /home/user/Libros-system-es-en-de--no-piper/init.sh /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/init-validate-all-portable-binaries.sh /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/patch_htm_files.py /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/patch-init-python.py /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/portable-bin-for-gentoo-2026-PATH /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/portable-bin-for-rocky-linux-8-PATH /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/README.md /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/scripting /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/server-init.sh /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/test-piper.sh /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/test.sh /home/user/Personal/$LIBROS/
    ln -svf /home/user/Libros-system-es-en-de--no-piper/var /home/user/Personal/$LIBROS/
    WAV="${ROOT}/Processed_WAV_files-${PROJECT}"
    HTM="${ROOT}/Processed_htms-${PROJECT}"
    HTMAUDIO="${ROOT}/Processed_htm_audios-${PROJECT}"
    PDFS="${ROOT}/pdfs-${PROJECT}"
    mkdir -p "$HTM"
    mkdir -p "$HTMAUDIO"
    mkdir -p "$WAV"
    mkdir -p "$PDFS"
    ln -svf "$HTM" "${ROOT}/${LIBROS}/htm"
    ln -svf "$HTMAUDIO" "${ROOT}/${LIBROS}/htm+audio"
    ln -svf "$WAV" "${ROOT}/${LIBROS}/personal"
    ln -svf "$PDFS" "${ROOT}/${LIBROS}/pdfs"
fi