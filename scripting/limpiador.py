import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import sys
import os
import re

def limpiar_texto(ruta_entrada):
    # Definimos los caracteres permitidos según tu lista
    # usa este cuando te sientas seguro que no hay exeso de numeros
    # permitidos = "0123456789abcdefghijklmnñopqrstuvwxyzüáéíóúABCDEFGHIJKLMNÑOPQRSTUVWXYZÜÁÉÍÓÚ.,:; "
    permitidos = "0123456789abcdefghijklmnñopqrstuvwxyzäöüáéíóúßABCDEFGHIJKLMNÑOPQRSTUVWXYZÄÖÜÁÉÍÓÚ!?.,:;ʼ”“()- "
    # permitidos = "abcdefghijklmnñopqrstuvwxyzäöüáéíóúßABCDEFGHIJKLMNÑOPQRSTUVWXYZÄÖÜÁÉÍÓÚ!?.,:;ʼ”“()- "
    set_permitidos = set(permitidos)
    signos_puntuacion = "!?.,:;ʼ”“()-"

    nombre_base = os.path.splitext(ruta_entrada)[0]
    ruta_salida = f"{nombre_base}.txt"

    try:
        with open(ruta_entrada, 'r', encoding='utf-8') as f:
            contenido = f.read()

        # 1. Filtrar caracteres: lo no permitido se convierte en espacio
        texto = "".join(c if c in set_permitidos else " " for c in contenido)

        # 2. Colapsar todos los espacios y saltos de línea en uno solo
        texto = re.sub(r'\s+', ' ', texto)

        # 3. Regla de puntuación:
        for signo in signos_puntuacion:
            # Quita espacio antes: " . " -> "."
            texto = texto.replace(f" {signo}", signo)
            # Asegura espacio después: "." -> ". "
            texto = texto.replace(signo, f"{signo} ")

        # 4. Limpieza final de espacios dobles y bordes
        texto_final = re.sub(r'\s+', ' ', texto).strip()

        with open(ruta_salida, 'w', encoding='utf-8') as f:
            f.write(texto_final)
            
        print(f"Hecho: '{ruta_entrada}' -> '{ruta_salida}'")

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo '{ruta_entrada}'")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python3 limpiador.py archivo.txt")
    else:
        limpiar_texto(sys.argv[1])