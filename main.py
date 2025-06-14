from code_project_reader.reader import generate_project_document

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python main.py <project_root_path>")
        sys.exit(1)
    
    root = sys.argv[1]
    document = generate_project_document(root)
    
    with open("output.txt", "w") as f:
        for line in document.split("\n"):
            print(line)
            f.write(line + "\n")