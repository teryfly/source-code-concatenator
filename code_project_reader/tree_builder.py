import os

def build_tree(path, prefix=""):
    entries = []
    try:
        # 忽略以点开头的文件夹（隐藏文件夹）
        entries = sorted(
            [e for e in os.listdir(path) 
             if (not e.startswith(".") or e in (".gitignore",)) 
             and not os.path.isdir(os.path.join(path, e)) or not e.startswith(".")],
            key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())
        )
    except PermissionError:
        return []

    lines = []
    for idx, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        # 跳过隐藏文件夹
        if entry.startswith(".") and os.path.isdir(full_path):
            continue
            
        connector = "└── " if idx == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry)

        if os.path.isdir(full_path):
            extension = "    " if idx == len(entries) - 1 else "│   "
            lines.extend(build_tree(full_path, prefix + extension))

    return lines