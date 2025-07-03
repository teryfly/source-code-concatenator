import os

TEXT_FILE_EXTENSIONS = {
    ".py", ".txt", ".md", ".json", ".yaml", ".yml", ".xml", ".html", ".css", ".js", ".csv",
    ".java", ".sh", ".sql", ".kt", ".kts", ".cs", ".log", ".ini", ".properties", ".bat", ".bkp",
    ".dockerfile", ".jsx", ".ts", ".tsx", ".javadoc", ".groovy", ".pgsql", ".patch", ".gradle",
    "",  # 无扩展名的文件
    ".config", ".webapp", ".gml", ".svg", ".map", ".rb", ".scss", ".vm", ".geojson", ".mf",
    ".jrxml", ".xsl", ".hbm", ".sessionfactorybuilderfactory", ".toolprovider", ".hbs", ".mjs",
    ".sample", ".pot", ".po", ".vue", ".less", ".styl", ".stylus", ".coffee", ".pug", ".jade",
    ".ejs", ".handlebars", ".mustache", ".sass", ".htm", ".markdown", ".cfg", ".cmd", ".php",
    ".pl", ".cgi", ".asp", ".aspx", ".cshtml", ".jsp", ".jspx", ".h2", ".hsql"
}

TEXT_FILE_NAMES = {
    # 原始文件名
    "Dockerfile", "Makefile", ".gitignore", "README", "README.md",
    # 新增文件名
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