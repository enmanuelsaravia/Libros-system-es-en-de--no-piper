import os
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.environ.get('PORTABLE_ROOT', os.path.dirname(SCRIPT_DIR) if os.path.basename(SCRIPT_DIR) == 'scripting' else SCRIPT_DIR)
import sys
import re

def is_garbled(filepath, lang):
    try:
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            text = f.read()
    except Exception:
        return True # Trigger OCR on error
        
    # If empty or only whitespace, it's empty, so return True to trigger OCR
    if not text.strip():
        return True

    # Word sets for common words
    common_de = {'und', 'die', 'der', 'das', 'ist', 'in', 'zu', 'von', 'mit', 'den', 'dem', 'des', 'ein', 'eine', 'auf', 'für', 'sich', 'nicht', 'es', 'sie', 'er', 'wir', 'ihr', 'vor', 'nach', 'aus', 'bei', 'wie', 'oder', 'aber', 'so', 'als', 'an', 'am', 'im', 'um', 'zur', 'zum'}
    common_en = {'the', 'and', 'of', 'to', 'in', 'is', 'that', 'it', 'he', 'was', 'for', 'on', 'are', 'as', 'with', 'his', 'they', 'at', 'be', 'this', 'have', 'from', 'or', 'had', 'by', 'but', 'not', 'what', 'all', 'were', 'we', 'when', 'your', 'can', 'said', 'there', 'use', 'an', 'each', 'which'}
    common_es = {'de', 'la', 'que', 'el', 'en', 'y', 'a', 'los', 'del', 'se', 'las', 'por', 'un', 'para', 'con', 'no', 'una', 'su', 'al', 'lo', 'como', 'más', 'o', 'pero', 'sus', 'este', 'esta', 'entre', 'cuando', 'muy', 'sin', 'sobre', 'también', 'me', 'había', 'era', 'ser', 'sino'}
    
    if lang == 'de':
        common = common_de
    elif lang == 'en':
        common = common_en
    else:
        common = common_es

    # Find all alphabetic words
    words = re.findall(r'\b[a-zA-ZáéíóúüñäöüßñÑáéíóúüñÑíóüñÑíóüñ]+\b', text.lower())
    total_words = len(words)
    
    # If there are extremely few words but the text length is significant, it's garbled
    if total_words < 3 and len(text.strip()) > 30:
        return True
        
    if total_words == 0:
        return True

    # Calculate common word ratio
    common_words_found = [w for w in words if w in common]
    common_ratio = len(common_words_found) / total_words

    # Calculate garbage character ratio
    allowed_pattern = r'[a-zA-Z0-9\s.,;:!?\(\)\[\]\'\"\-äöüßÄÖÜáéíóúüñÑ]'
    non_allowed = re.sub(allowed_pattern, '', text)
    garbage_ratio = len(non_allowed) / len(text) if len(text) > 0 else 0

    # Rules for garbled text detection:
    # 1. High garbage character ratio (e.g. > 1.5% and total garbage chars > 3)
    if garbage_ratio > 0.015 and len(non_allowed) >= 3:
        return True
        
    # 2. Extremely low common word ratio (e.g. < 15%) for text with a reasonable number of words
    if total_words >= 10 and common_ratio < 0.15:
        return True
        
    # 3. Many weird characters in words (e.g. sequences like 'rometf)eu' or 'rftc§')
    # If we find symbols like §, @, ^, |, *, \ inside words or adjacent to letters
    weird_connectors = re.findall(r'[a-zA-Z][§@\^\|\\\*#§][a-zA-Z]|[a-zA-Z]\)|[a-zA-Z]\(', text)
    if len(weird_connectors) >= 2:
        return True

    return False

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 check_garbled.py <filepath> [lang]")
        sys.exit(0)
    filepath = sys.argv[1]
    lang = sys.argv[2] if len(sys.argv) > 2 else 'de'
    if is_garbled(filepath, lang):
        sys.exit(1) # Garbled/Needs OCR
    else:
        sys.exit(0) # OK
