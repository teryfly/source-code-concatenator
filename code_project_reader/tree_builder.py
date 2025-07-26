import os

def build_tree(path, base_path, prefix="", ignore_func=None, debug=None):
    """构建目录树，支持忽略规则"""
    if ignore_func is None:
        ignore_func = lambda rel_path: False

    if debug is None:
        def debug(msg): pass

    rel_path = os.path.relpath(path, base_path)
    if rel_path == '.':
        rel_path = ''

    ignored = rel_path and ignore_func(rel_path)
    debug(f"TREE CHECK DIR: {rel_path or '.'} IGNORED={ignored}")
    if rel_path and ignored:
        return []

    try:
        all_entries = os.listdir(path)
    except PermissionError:
        return []

    filtered_dirs = []
    filtered_files = []

    for entry in all_entries:
        entry_path = os.path.join(path, entry)
        entry_rel = os.path.join(rel_path, entry) if rel_path else entry
        ignored = ignore_func(entry_rel)
        debug(f"TREE ENTRY: {entry_rel} IGNORED={ignored}")
        if ignored:
            continue
        if os.path.isdir(entry_path):
            filtered_dirs.append(entry)
        else:
            filtered_files.append(entry)

    entries = sorted(filtered_dirs, key=lambda x: x.lower()) + sorted(filtered_files, key=lambda x: x.lower())

    lines = []
    total = len(entries)
    for idx, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = "└── " if idx == total - 1 else "├── "
        lines.append(prefix + connector + entry)
        if os.path.isdir(full_path):
            extension = "    " if idx == total - 1 else "│   "
            child_rel = os.path.join(rel_path, entry) if rel_path else entry
            lines.extend(build_tree(full_path, base_path, prefix + extension, ignore_func, debug))

    return lines