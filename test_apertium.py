import subprocess
import re

title = "Patterns of Enterprise Application Architecture"
try:
    res = subprocess.run(
        ["/home/user/Libros-system-es-en-de/portable-bin-for-gentoo-2026-PATH/bin/apertium", "eng-spa"],
        input=title.encode('utf-8'),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
        env={"LD_LIBRARY_PATH": "/home/user/Libros-system-es-en-de/portable-bin-for-gentoo-2026-PATH/lib", "APERTIUM_DATADIR": "/home/user/Libros-system-es-en-de/portable-bin-for-gentoo-2026-PATH/share/apertium"}
    )
    print("ES:", res.stdout.decode('utf-8').strip())
except Exception as e:
    print(e)
