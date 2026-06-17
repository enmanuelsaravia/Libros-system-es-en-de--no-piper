#!/bin/bash
export PORTABLE_MODE=1
export PORTABLE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$PORTABLE_ROOT/scripting/find-piper.sh"
echo "PIPER_EXE is: $PIPER_EXE"
if [ -n "$PIPER_EXE" ]; then
    ls -l "$PIPER_EXE"
    cat "$PIPER_EXE"
    "$PIPER_EXE" --version
fi
