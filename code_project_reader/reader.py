import os
from code_project_reader.utils import is_text_file, safe_read_file, parse_gitignore
from code_project_reader.tree_builder import build_tree

def generate_project_document(root_path: str) -> str:
    if not os.path.isdir(root_path):
        raise ValueError(f"Invalid directory: {root_path}")

    project_name = os.path.basename(os.path.abspath(root_path))
    ignore_func = parse_gitignore(root_path)

    # 项目结构（应用忽略规则）
    tree_lines = [project_name + "/"] + build_tree(root_path, root_path, "", ignore_func)
    tree_structure = "\n".join(tree_lines)

    # 文件内容（应用忽略规则）
    file_contents = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        # 动态过滤被忽略的目录
        dirnames[:] = [
            d for d in dirnames 
            if not ignore_func(os.path.relpath(os.path.join(dirpath, d), root_path))
        ]
        
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_path)
            
            # 跳过被忽略的文件或非文本文件
            if ignore_func(rel_path) or not is_text_file(full_path):
                continue

            content = safe_read_file(full_path)
            if content is not None:
                file_contents.append(f"File: {rel_path}\n---\n{content}\n---")

    return (
        f"Project Name: {project_name}\n\n"
        f"Project Structure:\n{tree_structure}\n\n"
        f"File Contents:\n\n" + "\n\n".join(file_contents)
    )