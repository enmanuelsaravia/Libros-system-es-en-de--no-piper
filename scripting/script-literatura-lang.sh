#!/bin/dash

# Calcular el directorio portable y de scripts de forma dinamica
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORTABLE_ROOT="${PORTABLE_ROOT:-$(cd "$SCRIPT_DIR/.." && pwd)}"

if [ -z "$PORTABLE_MODE" ]; then
    MONOLITHS_DIR="$HOME/monoliths-llm"
    TRANS_DIR="$HOME/googletrans/dist"
else
    MONOLITHS_DIR="${MONOLITHS_DIR:-$SCRIPT_DIR}"
    TRANS_DIR="${TRANS_DIR:-$PORTABLE_ROOT/portable-bin-PATH/bin}"
fi

CONT="$1"

# TO SPANISH
if ! cat "$MONOLITHS_DIR/script-literatura-core.sh" | grep '#VERSION=' | grep -iq es_MX; then
    if [ -f "$TRANS_DIR/googletrans-es" ]; then
	CONT=$("$TRANS_DIR/googletrans-es" "$CONT")
    fi
fi

# TO SPANISH NOT INTERNET BUT LAN ASUS
if false; then
    CONT=$(printf '%s\n' "$CONT" \
	       | ssh -o LogLevel=ERROR $(cat ~/.asdf)@$(cat ~/.fdsa) "apertium eng-spa" \
	       | tr -d '*' | tr -d '#')
fi

# TO GERMAN
if ! cat "$MONOLITHS_DIR/script-literatura-core.sh" | grep '#VERSION=' | grep -iq de_DE; then
    if [ -f "$TRANS_DIR/googletrans-de" ]; then
	CONT=$("$TRANS_DIR/googletrans-de" "$CONT")
    fi
fi

echo -n "$CONT"