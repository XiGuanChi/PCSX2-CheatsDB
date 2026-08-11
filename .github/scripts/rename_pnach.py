import os
import sys

def process_file(filepath):
    """
    Read the file, replace lines that exactly contain '//Name' with '[Name]',
    then write back if any changes were made.
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    modified = False
    new_lines = []
    for line in lines:
        stripped = line.strip()
        if stripped == "//Name":
            new_lines.append("[Name]\n")
            modified = True
        else:
            new_lines.append(line)

    if modified:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        print(f"Modified: {filepath}")

    return modified

def main():
    target_dirs = ['cheats-v1', 'cheats-v2', 'cheats-v3', 'cheats-v4', 'cheats-v5', 'cheats-v6']
    root = os.getcwd()
    total_modified = 0

    for dir_name in target_dirs:
        dir_path = os.path.join(root, dir_name)
        if not os.path.isdir(dir_path):
            print(f"Directory not found, skipping: {dir_path}")
            continue

        for current_root, _, files in os.walk(dir_path):
            for file in files:
                if file.endswith('.pnach'):
                    filepath = os.path.join(current_root, file)
                    if process_file(filepath):
                        total_modified += 1

    print(f"Total files modified: {total_modified}")

if __name__ == "__main__":
    main()
