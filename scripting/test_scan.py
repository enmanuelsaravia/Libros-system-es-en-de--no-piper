import os

def get_langs_from_htm(filepath):
    langs = []
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            chunk = f.read(65536)
            if 'id="play-es"' in chunk: langs.append('es')
            if 'id="play-en"' in chunk: langs.append('en')
            if 'id="play-de"' in chunk: langs.append('de')
    except:
        pass
    return langs

print(get_langs_from_htm('/home/user/Libros-system-es-en-de/var/Michael-Feathers--Working-Effectively-With-Legacy-Code.en-part_0001.htm'))
