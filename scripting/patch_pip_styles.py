import os
import glob

def patch_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return

    changed = False

    # 1. Update .pagination-group border
    old_pag = """        .pagination-group {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            background: #ffffff !important;
            border-radius: 8px;
            padding: 4px 12px;
            border: 1px solid var(--border-color);
        }"""
    new_pag = """        .pagination-group {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 1rem;
            background: #ffffff !important;
            border-radius: 8px;
            padding: 4px 12px;
            border: none;
        }"""
    if old_pag in content:
        content = content.replace(old_pag, new_pag)
        changed = True

    # 2. Update #hide-header-btn border
    old_hide = """        #hide-header-btn {
            width: auto;
            min-width: 44px;
            height: 24px;
            justify-content: center;
            font-weight: bold;
            border: 1px solid var(--border-color);
            border-radius: 4px;
            background: #ffffff !important;
            color: var(--text-color);
            padding: 2px 10px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 0.5rem;
            display: inline-flex;
            align-items: center;
        }"""
    new_hide = """        #hide-header-btn {
            width: auto;
            min-width: 44px;
            height: 24px;
            justify-content: center;
            font-weight: bold;
            border: none;
            border-radius: 4px;
            background: #ffffff !important;
            color: var(--text-color);
            padding: 2px 10px;
            cursor: pointer;
            font-size: 1rem;
            margin-top: 0.5rem;
            display: inline-flex;
            align-items: center;
        }"""
    if old_hide in content:
        content = content.replace(old_hide, new_hide)
        changed = True

    # 3. Update #pip-btn border and background
    old_pip = """        #pip-btn {
            width: 100%;
            justify-content: center;
            font-weight: bold;
            text-transform: uppercase;
            border: 2px solid var(--border-color);
            padding: 10px 16px;
            border-radius: 8px;
            background: transparent;
            color: var(--text-color);
            font-size: 1rem;
        }"""
    new_pip = """        #pip-btn {
            width: 100%;
            justify-content: center;
            font-weight: bold;
            text-transform: uppercase;
            border: none;
            padding: 10px 16px;
            border-radius: 8px;
            background: #ffffff;
            color: var(--text-color);
            font-size: 1rem;
        }"""
    if old_pip in content:
        content = content.replace(old_pip, new_pip)
        changed = True

    # 4. Update auto-pip-toggle-container style
    old_line = '<div class="auto-pip-toggle-container" style="display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 6px 12px; font-size: 0.85rem; font-weight: bold; border: 2px solid var(--border-color); border-radius: 8px;">'
    new_line = '<div class="auto-pip-toggle-container" style="display: flex; align-items: center; justify-content: space-between; width: 100%; padding: 6px 12px; font-size: 0.85rem; font-weight: bold; background: #ffffff; border-radius: 8px;">'
    if old_line in content:
        content = content.replace(old_line, new_line)
        changed = True

    if changed:
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Patched: {file_path}")
            return True
        except Exception as e:
            print(f"Error writing to {file_path}: {e}")
    return False

def main():
    target_files = []

    # Find all htm.htm files
    for root, dirs, files in os.walk("/home/user"):
        # Skip hidden directories like .git
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        for file in files:
            if file == "htm.htm":
                target_files.append(os.path.join(root, file))
            elif file.endswith(".htm"):
                # Also include all generated htm files under Processed_htms- or Processed_htm_audios-
                if "Processed_" in root:
                    target_files.append(os.path.join(root, file))

    print(f"Found {len(target_files)} potential target files.")
    patched_count = 0
    for path in target_files:
        if patch_file(path):
            patched_count += 1

    print(f"Done. Patched {patched_count} files.")

if __name__ == "__main__":
    main()
