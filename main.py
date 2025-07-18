import sys
from code_project_reader.api import get_project_document

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <project_root_path>")
        sys.exit(1)
    
    try:
        result = get_project_document(sys.argv[1],True)
        metadata = result["metadata"]
        
        print(f"\nProject Documentation Summary:")
        print(f"Total lines: {metadata['total_lines']:,}")
        print(f"Estimated tokens: {metadata['total_tokens']:,}")
        print(f"File saved to: {metadata['output_path']}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)