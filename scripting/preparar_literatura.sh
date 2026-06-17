#!/bin/dash
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

sed -i 's/^[[:space:]]*//' "$1"
sleep 0.1
sed -i 's/[[:space:]]*$//' "$1"
sleep 0.1
sed -i '/^[[:space:]]*$/d' "$1"
sleep 0.1
sed -i ':a;N;$!ba;s/\n/ /g' "$1"
sleep 0.1
sed -i 's/\.[[:space:]]/\.\n/g' "$1"
sleep 0.1
sed -i 's/\![[:space:]]/\.\n/g' "$1"
sleep 0.1
sed -i 's/\?[[:space:]]/\.\n/g' "$1"
sleep 0.1
sed -i 's/\;[[:space:]]/\.\n/g' "$1"
sleep 0.1
sed -i 's/\:[[:space:]]/\.\n/g' "$1"
sleep 0.1
sed -i 's/\,[[:space:]]/\,\n/g' "$1"
sleep 0.1
sed -i 's/^[[:space:]]*//' "$1"
sleep 0.1
sed -i 's/ :/:/g' "$1"
sleep 0.1
echo listo
