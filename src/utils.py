import os

TEXT_FILE_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".yaml", ".yml", ".xml", ".html", ".css", ".js", ".csv"
}
TEXT_FILE_NAMES = {"Dockerfile", "Makefile", ".gitignore", "README", "README.md"}

def is_text_file(file_path):
    _, ext = os.path.splitext(file_path)
    filename = os.path.basename(file_path)
    return ext in TEXT_FILE_EXTENSIONS or filename in TEXT_FILE_NAMES

def safe_read_file(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except (UnicodeDecodeError, PermissionError, IsADirectoryError):
        return None