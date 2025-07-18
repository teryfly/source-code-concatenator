# source-code-concatenator
concatenate source code into one file

## 程序B调用方式（示例）
```python
from code_project_reader.api import get_project_document

# 调用A的功能获取项目文档
try:
    project_path = "/path/to/your/project"
    result = get_project_document(project_path, save_output=False)
    
    # 获取拼接后的文档内容
    document_content = result["content"]
    
    # 获取元数据
    print(f"项目名称: {result['metadata']['project_name']}")
    print(f"总行数: {result['metadata']['total_lines']}")
    
    # 使用文档内容做进一步处理...
    # with open("custom_output.txt", "w") as f:
    #     f.write(document_content)
    
except Exception as e:
    print(f"处理失败: {e}")
```
### 调用注意事项
1、 安装依赖：

```bash
# 在程序B的环境中安装A
pip install /path/to/source-code-concatenator
```
2、确保传递给 get_project_document() 的是绝对路径
3、跨平台路径处理：使用 os.path.abspath(project_path)