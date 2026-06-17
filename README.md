# Requirements

- **System utilities**: `pdfinfo`, `pdftotext`, `tesseract`, `qpdf`, `exiftool`
- **Python**: Version **3.6.x** (already present as `python3`)
- **Tesseract language packs** (Fedora/CentOS):
  ```bash
  # Install core OCR engine (includes English)
  sudo dnf install tesseract

  # Install additional language packs (Spanish, German)
  sudo dnf install tesseract-langpack-spa tesseract-langpack-deu
  ```

## Python dependencies

The scripts rely on the `translate` library, which works with Python 3.6.
Install it globally or inside a virtual environment:

```bash
# Option 1: global install (may require sudo)
python3 -m pip install --user translate

# Option 2: create a local virtual environment
python3 -m venv $HOME/translate/venv
source $HOME/translate/venv/bin/activate
pip install translate
# The `translate` package installs a CLI entry‑point called `translate`. After activation it is available as `translate` in the venv.
# To expose it system‑wide you can symlink it:
#   sudo ln -s $HOME/translate/venv/bin/translate /usr/local/bin/translate
```

If you use the virtual environment, the scripts will automatically detect it (they look for `$HOME/googletrans/venv`, you can symlink it):

```bash
mkdir -p $HOME/googletrans
ln -s $HOME/translate/venv $HOME/googletrans/venv
```

## Additional setup

1. Ensure poppler utilities are installed (provides `pdfinfo` and `pdftotext`). On Fedora/CentOS:
   ```bash
   sudo dnf install poppler-utils
   ```
2. Install Tesseract OCR for scanned PDFs:
   ```bash
   sudo dnf install tesseract
   ```
3. Install `qpdf` for PDF manipulation:
   ```bash
   sudo dnf install qpdf
   ```

## Notas específicas para Rocky Linux 8

Dado que Rocky Linux 8 cuenta con una versión antigua de `glibc` (v2.28), los binarios portables de **Piper TTS** incluidos podrían fallar con el error de `version 'GLIBC_2.29' not found`. Para garantizar el funcionamiento correcto en este entorno, es necesario instalar herramientas vía DNF y compilar algunas de forma manual.

### 1. Instalación con dnf
Asegúrate de instalar Python 3.11, las herramientas de manipulación de PDF / OCR, y los reemplazos nativos para las herramientas de la carpeta `portable-bin-PATH` que fallan por GLIBC:
```bash
sudo dnf install epel-release
sudo dnf install python3.11 qpdf poppler-utils tesseract \
                 tesseract-langpack-eng tesseract-langpack-spa tesseract-langpack-deu \
                 ImageMagick xosd xclip xdotool xournalpp xorg-x11-server-utils jdupes perl-Image-ExifTool
```

### 2. Dependencias de Python (Pip)
El script de generación de audios requiere dependencias adicionales como `deep_translator`:
```bash
python3.11 -m pip install --user deep_translator pdf2image
```

### 3. Compilación manual de dependencias faltantes
Para evitar problemas dinámicos de librerías, es obligatorio contar con instalaciones nativas de las siguientes herramientas, ya que los binarios portables provistos fallan en Rocky Linux 8 por requerir GLIBC >= 2.34 (mientras que Rocky usa 2.28):

**A. Piper TTS:**
El wrapper (`find-piper.sh`) dará prioridad a tu compilación local:
```bash
# 1. Instalar dependencias de compilación
sudo dnf install gcc-c++ cmake git

# 2. Compilar Piper (instrucciones oficiales de rhasspy/piper)
git clone https://github.com/rhasspy/piper.git ~/piper
cd ~/piper
# Seguir las instrucciones del repositorio para compilar usando CMake
```
> [!IMPORTANT]  
> Asegúrate de que el binario de piper compilado termine en `~/piper/install/piper` o `~/piper/piper`. Nuestro script lo buscará automáticamente en esas ubicaciones.

**B. Apertium y Lexical Tools (`lttoolbox`):**
Actualmente, estas herramientas no están disponibles en los repositorios estándar de Rocky Linux 8 (`dnf`), y sus binarios portables fallan. Si necesitas utilizarlas para traducciones offline (nuestro script principal usa Google Translate remoto, por lo que no es estrictamente obligatorio para el HTML con audio), debes clonarlas desde su repositorio de GitHub y compilarlas desde cero.

https://github.com/apertium/apertium-anaphora/releases/download/v1.1.1/apertium-anaphora-1.1.1.tar.bz2
https://github.com/apertium/apertium-eng-spa/releases/download/v0.8.1/apertium-eng-spa-0.8.1.tar.bz2
https://github.com/apertium/apertium-lex-tools/releases/download/v0.5.0/apertium-lex-tools-0.5.0.tar.bz2
https://github.com/apertium/apertium/releases/download/v3.9.12/apertium-3.9.12.tar.bz2
https://github.com/apertium/lttoolbox/releases/download/v3.8.2/lttoolbox-3.8.2.tar.bz2

**C. Feh (Visor de imágenes):**
`feh` tampoco fue encontrado en los repositorios de DNF, por lo que su binario portable fallará si el script intenta invocarlo. De ser necesario su uso, deberá compilarse desde el código fuente oficial.

https://feh.finalrewind.org/feh-3.10.3.tar.bz2

## Running the workflow

```bash
bash init.sh
```

The script will guide you through selecting the PDF, page range, and target languages. Audio files will be generated in the `personal/htm-pags` directory.