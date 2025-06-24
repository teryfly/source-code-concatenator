from code_project_reader.reader import generate_project_document
from datetime import datetime
import os
import sys

def estimate_tokens(text):
    """Simple token estimation (approximate: 1 token ~= 4 characters)"""
    return max(1, len(text) // 4)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python main.py <project_root_path>")
        sys.exit(1)
    
    root = sys.argv[1]
    
    # Create output directory if it doesn't exist
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        document = generate_project_document(root)
    except UnicodeDecodeError as e:
        print(f"Error reading files: {e}")
        sys.exit(1)
    
    # Generate output filename with timestamp
    last_dir = os.path.basename(os.path.normpath(root))
    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    output_filename = f"{last_dir}({timestamp}).txt"
    output_path = os.path.join(output_dir, output_filename)
    
    # Calculate statistics
    lines = document.split("\n")
    total_lines = len(lines)
    total_tokens = estimate_tokens(document)
    
    try:
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(document)
        
        # Print statistics
        print(f"\nProject Documentation Summary:")
        print(f"Total lines: {total_lines:,}")
        print(f"Estimated tokens: {total_tokens:,}")
        print(f"File saved to: {output_path}")
        
    except UnicodeEncodeError as e:
        print(f"Error writing output file: {e}")
        sys.exit(1)