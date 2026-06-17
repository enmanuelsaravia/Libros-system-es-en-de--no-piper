#!/bin/bash
# Recorrer todos los directorios que coincidan con el patrón
for folder in "$HOME"/Personal/Libros-*; do
# Verificar que realmente sea un directorio
if [ -d "$folder" ]; then
echo "Procesando: $folder"
# Entrar al directorio
cd "$folder" || continue
# Ejecutar el comando
bash server-init.sh &
# Esperar un momento para evitar condiciones de carrera en puertos y en /tmp
sleep 2
# Opcional: regresar al directorio anterior (buena práctica)
cd - > /dev/null
fi
done