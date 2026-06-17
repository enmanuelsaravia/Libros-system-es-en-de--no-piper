#!/bin/bash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"


# Directorio donde están los WAVs y donde saldrán los MP3
WAV_DIR="$PROJECT_ROOT/personal"
OUT_DIR="$PROJECT_ROOT/personal"

# Obtener prefijos únicos de los archivos WAV
# Busca archivos que tengan el formato: nombre_del_libro__0000.wav
mapfile -t prefixes < <(ls -1 "$WAV_DIR"/*.wav 2>/dev/null | sed 's/.*\///;s/__.*//' | sort | uniq)

if [ ${#prefixes[@]} -eq 0 ]; then
    echo "Error: No se encontraron archivos WAV en $WAV_DIR"
    exit 1
fi

echo "--- Generador de MP3 por Partes ---"
echo "Libros disponibles en audio:"
for i in "${!prefixes[@]}"; do
    echo "  $i) ${prefixes[$i]}"
done
echo "-----------------------------------"

read -p "Seleccione el número del libro (0-$((${#prefixes[@]}-1))): " choice

if [[ ! "$choice" =~ ^[0-9]+$ ]] || [ "$choice" -ge "${#prefixes[@]}" ]; then
    echo "Selección inválida."
    exit 1
fi

selected_prefix="${prefixes[$choice]}"
echo ""
echo ">>> Procesando: $selected_prefix"

# Archivo WAV temporal para la unión (evita problemas de cabeceras al concatenar)
temp_wav="$WAV_DIR/joined_temp.wav"

# Unir archivos WAV usando sox
echo ">>> Uniendo archivos WAV (esto puede tardar un momento)..."
# Usamos sort para asegurar el orden correcto de las partes
files_to_join=$(ls -1 "$WAV_DIR"/"$selected_prefix"__*.wav | sort)
sox $files_to_join "$temp_wav"

if [ $? -ne 0 ]; then
    echo "Error al unir los archivos con sox."
    exit 1
fi

# Calcular duración total en segundos
duration=$(soxi -D "$temp_wav" | cut -d. -f1)
# 5400 segundos = 1.5 horas. A 128kbps mono, esto son unos 83MB.
# (Bien por debajo del límite de 100MB solicitado)
segment_time=5400

echo ">>> Duración total estimada: $((duration / 60)) minutos."
echo ">>> Convirtiendo a MP3 en partes jugables..."

# Bucle para extraer cada parte y convertirla a MP3
for (( i=0, start=0; start < duration; i++, start+=segment_time )); do
    part_num=$(printf "%02d" $((i+1)))
    out_file="$OUT_DIR/${selected_prefix}.part${part_num}.mp3"
    
    echo "    Generando parte $part_num: $(basename "$out_file")..."
    
    # Extraemos el fragmento como WAV y lo pasamos por tubería a lame
    # -y sobreescribe si ya existe
    ffmpeg -y -ss $start -t $segment_time -i "$temp_wav" -f wav - 2>/dev/null | lame -b 128 - "$out_file" > /dev/null 2>&1
done

# Limpieza del archivo temporal
rm "$temp_wav"

echo ""
echo "¡Proceso completado!"
echo "Los archivos MP3 resultantes están en: $OUT_DIR"
echo ""
