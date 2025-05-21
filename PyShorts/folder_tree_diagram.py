import os

def print_tree(startpath, indent=''):
    if not os.path.exists(startpath):
        print(f"Path does not exist: {startpath}")
        return

    items = sorted(os.listdir(startpath))
    for i, item in enumerate(items):
        path = os.path.join(startpath, item)
        is_last = (i == len(items) - 1)
        prefix = '└── ' if is_last else '├── '
        print(indent + prefix + item)
        if os.path.isdir(path):
            extension = '    ' if is_last else '│   '
            print_tree(path, indent + extension)

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Print directory tree structure.")
    parser.add_argument("folder", help="Path to the folder.")
    args = parser.parse_args()

    print(args.folder)
    print_tree(args.folder)


