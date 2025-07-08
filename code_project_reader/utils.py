import os
import fnmatch

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
    #".sql", ".sql.gz", ".sql.xz", ".sql.bz2", ".sql.zst", ".sql.lz4", ".sql.lzo", ".sql.xz",
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

def parse_gitignore(root_path):
    """解析.gitignore文件并返回匹配函数"""
    gitignore_path = os.path.join(root_path, '.gitignore')
    if not os.path.isfile(gitignore_path):
        return lambda path: False
    
    patterns = []
    with open(gitignore_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # 处理目录规则（以/结尾）
            if line.endswith('/'):
                line = line[:-1]
                
            patterns.append(line)
    
    def match(path):
        """检查路径是否匹配.gitignore规则"""
        # 强制忽略.gitignore文件自身
        if path == '.gitignore':
            return True
            
        # 标准化路径格式
        unix_path = path.replace(os.sep, '/')
        
        # 检查是否匹配任何模式
        for pattern in patterns:
            # 目录匹配（递归匹配）
            if unix_path.startswith(pattern + '/'):
                return True
                
            # 精确匹配
            if unix_path == pattern:
                return True
                
            # 通配符匹配
            if fnmatch.fnmatch(unix_path, pattern):
                return True
                
            # 文件名匹配
            if '/' not in pattern and fnmatch.fnmatch(os.path.basename(unix_path), pattern):
                return True
                
        return False
    
    return match