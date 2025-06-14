import os
from code_project_reader.utils import is_text_file, safe_read_file
from code_project_reader.tree_builder import build_tree

def generate_project_document(root_path: str) -> str:
    if not os.path.isdir(root_path):
        raise ValueError(f"Invalid directory: {root_path}")

    project_name = os.path.basename(os.path.abspath(root_path))

    # Project Structure
    tree_lines = [project_name + "/"] + build_tree(root_path)
    tree_structure = "\n".join(tree_lines)

    # File Contents
    file_contents = []
    for dirpath, _, filenames in os.walk(root_path):
        for filename in filenames:
            full_path = os.path.join(dirpath, filename)
            if not is_text_file(full_path):
                continue

            rel_path = os.path.relpath(full_path, root_path)
            content = safe_read_file(full_path)
            if content is None:
                continue

            file_contents.append(
                f"File 1: {rel_path}\n---\n{content}\n---"
            )

    return (
        f"Project Name: {project_name}\n\n"
        f"Project Structure:\n{tree_structure}\n\n"
        f"File Contents:\n\n" + "\n\n".join(file_contents)
    )