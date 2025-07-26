import os
import fnmatch
import sys

TEXT_FILE_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".yaml", ".yml", ".xml", ".html", ".css", ".js", ".csv",
    ".java", ".sh",  ".kt", ".kts", ".cs", ".log", ".ini", ".properties", ".bat", ".bkp",
    ".dockerfile", ".jsx", ".ts", ".tsx", ".javadoc", ".groovy", ".pgsql", ".patch", ".gradle",
    "",  # 无扩展名的文件
    ".config", ".webapp", ".gml", ".svg", ".map", ".rb", ".scss", ".vm", ".geojson", ".mf",
    ".jrxml", ".xsl", ".hbm", ".sessionfactorybuilderfactory", ".toolprovider", ".hbs", ".mjs",
    ".sample", ".pot", ".po", ".vue", ".less", ".styl", ".stylus", ".coffee", ".pug", ".jade",
    ".ejs", ".handlebars", ".mustache", ".sass", ".htm", ".markdown", ".cfg", ".cmd", ".php",
    ".pl", ".cgi", ".asp", ".aspx", ".cshtml", ".jsp", ".jspx", ".h2", ".hsql",
}

TEXT_FILE_NAMES = {
    "Dockerfile", "Makefile", ".gitignore", "README", "README.md",
    "factories", "conf", "data", "lst", "dat", "jrxml", "ftl"
}

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

def _find_library_root():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def _find_caller_project_root():
    # 尝试从调用栈中找到site-packages外的最近一级（或sys.argv[0]目录）
    import inspect
    import site
    site_paths = set(site.getsitepackages() + [site.getusersitepackages()])
    site_paths = set(os.path.abspath(p) for p in site_paths)

    # 查找最近的非本包调用方文件
    frames = inspect.stack()
    for frame_info in frames:
        filename = frame_info.filename
        abspath = os.path.abspath(filename)
        # 跳过本库代码
        if abspath.startswith(_find_library_root()):
            continue
        # 跳过site-packages下的代码
        skip = False
        for s in site_paths:
            if abspath.startswith(s):
                skip = True
        if skip:
            continue
        # 返回其所在目录
        return os.path.dirname(abspath)
    # 退回命令行入口
    main_mod = sys.modules.get("__main__")
    if hasattr(main_mod, "__file__"):
        return os.path.dirname(os.path.abspath(main_mod.__file__))
    # fallback
    return os.getcwd()

def parse_gitignore(_project_root_path_ignored=None):
    """
    优先检测调用方项目根目录下的 .gitignore，若无则退回本库根目录 .gitignore
    """
    # 检查调用方项目根目录
    caller_project_root = _find_caller_project_root()
    caller_gitignore = os.path.join(caller_project_root, ".gitignore")
    if os.path.isfile(caller_gitignore):
        gitignore_path = caller_gitignore
    else:
        gitignore_path = os.path.join(_find_library_root(), ".gitignore")
    if not os.path.isfile(gitignore_path):
        return lambda path: False

    patterns = []
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            patterns.append(line)

    def match(path):
        if path == '.gitignore':
            return True
        unix_path = path.replace(os.sep, '/')
        for pattern in patterns:
            is_dir_pattern = pattern.endswith('/')
            norm_pattern = pattern.rstrip('/') if is_dir_pattern else pattern
            if is_dir_pattern:
                parts = unix_path.split('/')
                if norm_pattern in parts:
                    return True
                if unix_path.startswith(norm_pattern + '/'):
                    return True
                for part in parts:
                    if fnmatch.fnmatch(part, norm_pattern):
                        return True
            else:
                if unix_path == norm_pattern:
                    return True
                if fnmatch.fnmatch(unix_path, norm_pattern):
                    return True
                if '/' not in norm_pattern and fnmatch.fnmatch(os.path.basename(unix_path), norm_pattern):
                    return True
        return False

    return match