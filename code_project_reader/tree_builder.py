import os

def build_tree(path, base_path, prefix="", ignore_func=None):
    """构建目录树，支持忽略规则"""
    if ignore_func is None:
        ignore_func = lambda rel_path: False

    # 计算当前路径的相对路径
    rel_path = os.path.relpath(path, base_path)
    if rel_path == '.':
        rel_path = ''
    
    # 检查当前目录本身是否被忽略
    if rel_path and ignore_func(rel_path):
        return []

    entries = []
    try:
        # 获取并过滤条目
        all_entries = os.listdir(path)
        filtered_entries = []
        for entry in all_entries:
            # 计算条目的相对路径
            entry_rel = os.path.join(rel_path, entry) if rel_path else entry
            
            # 检查条目是否被忽略
            if ignore_func(entry_rel):
                continue
                
            filtered_entries.append(entry)
        
        # 排序：目录在前，文件在后，按字母顺序
        entries = sorted(
            filtered_entries,
            key=lambda x: (not os.path.isdir(os.path.join(path, x)), x.lower())
        )
    except PermissionError:
        return []

    lines = []
    for idx, entry in enumerate(entries):
        full_path = os.path.join(path, entry)
        connector = "└── " if idx == len(entries) - 1 else "├── "
        lines.append(prefix + connector + entry)

        if os.path.isdir(full_path):
            extension = "    " if idx == len(entries) - 1 else "│   "
            child_rel = os.path.join(rel_path, entry) if rel_path else entry
            
            # 递归构建子树（仅当目录未被忽略）
            if not ignore_func(child_rel):
                lines.extend(build_tree(full_path, base_path, prefix + extension, ignore_func))

    return lines