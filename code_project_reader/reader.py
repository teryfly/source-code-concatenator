import os
from code_project_reader.utils import is_text_file, safe_read_file, parse_gitignore
from code_project_reader.tree_builder import build_tree

def debug_print(msg):
    try:
        if os.environ.get("CODE_PROJECT_DEBUG") == "1":
            print("[DEBUG]", msg)
    except Exception:
        pass

def generate_project_document(root_path: str) -> str:
    if not os.path.isdir(root_path):
        raise ValueError(f"Invalid directory: {root_path}")

    project_name = os.path.basename(os.path.abspath(root_path))
    ignore_func = parse_gitignore()  # 自动检测调用方项目.gitignore或本库.gitignore

    tree_lines = [project_name + "/"] + build_tree(root_path, root_path, "", ignore_func, debug=debug_print)
    tree_structure = "\n".join(tree_lines)

    file_contents = []
    for dirpath, dirnames, filenames in os.walk(root_path):
        abs_dirnames = []
        for d in dirnames:
            rel = os.path.relpath(os.path.join(dirpath, d), root_path)
            ignored = ignore_func(rel)
            debug_print(f"DIR CHECK: {rel} IGNORED={ignored}")
            if not ignored:
                abs_dirnames.append(d)
        dirnames[:] = abs_dirnames

        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            rel_path = os.path.relpath(full_path, root_path)
            ignored = ignore_func(rel_path)
            debug_print(f"FILE CHECK: {rel_path} IGNORED={ignored}")
            if ignored or not is_text_file(full_path):
                continue
            content = safe_read_file(full_path)
            if content is not None:
                file_contents.append(f"File: {rel_path}\n---\n{content}\n---")

    return (
        f"Project Name: {project_name}\n\n"
        f"Project Structure:\n{tree_structure}\n\n"
        f"File Contents:\n\n" + "\n\n".join(file_contents)
    )