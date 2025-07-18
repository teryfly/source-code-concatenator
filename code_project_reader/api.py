from .reader import generate_project_document
from datetime import datetime
import os

def get_project_document(root_path: str, save_output: bool = False) -> dict:
    """
    获取项目文档内容及元数据
    
    :param root_path: 项目根目录路径
    :param save_output: 是否保存输出文件（默认False）
    :return: 包含文档内容和元数据的字典
    """
    # 创建输出目录
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    # 生成文档内容
    document = generate_project_document(root_path)
    
    # 准备元数据
    last_dir = os.path.basename(os.path.normpath(root_path))
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    output_filename = f"{last_dir}({timestamp}).txt"
    output_path = os.path.join(output_dir, output_filename)
    
    # 计算统计信息
    lines = document.split("\n")
    total_lines = len(lines)
    total_tokens = max(1, len(document) // 4)  # 1 token ≈ 4 chars
    
    # 可选：保存输出文件
    if save_output:
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(document)
        except UnicodeEncodeError as e:
            raise RuntimeError(f"文件写入失败: {e}")
    
    return {
        "content": document,
        "metadata": {
            "project_name": last_dir,
            "output_path": output_path,
            "total_lines": total_lines,
            "total_tokens": total_tokens
        }
    }