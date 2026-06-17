SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$SCRIPT_DIR"

# Ejecutar esto directamente en la terminal de la otra computadora:
mv portable-bin-PATH/lib/libacl.so.1 portable-bin-PATH/lib/libacl.so.1.bak
mv portable-bin-PATH/lib/libpcre2-8.so.0 portable-bin-PATH/lib/libpcre2-8.so.0.bak
mv portable-bin-PATH/lib/libz.so.1 portable-bin-PATH/lib/libz.so.1.bak
mv portable-bin-PATH/lib/libm.so.6 portable-bin-PATH/lib/libm.so.6.bak
mv portable-bin-PATH/lib/libstdc++.so.6 portable-bin-PATH/lib/libstdc++.so.6.bak
