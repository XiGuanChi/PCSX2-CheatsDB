#!/usr/bin/env python3
import os
import re
import sys

# Target folders to process
TARGET_DIRS = [f"cheats-v{i}" for i in range(1, 7)]

def process_file(filepath):
    """Read file, replace lines matching //Content with [Content], and write back."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Failed to read {filepath}: {e}", file=sys.stderr)
        return False

    modified = False
    new_lines = []
    for line in lines:
        stripped = line.rstrip('\n')
        # Match lines that contain only "//..." (with optional surrounding spaces)
        match = re.match(r'^\s*//(.*?)\s*$', stripped)
        if match:
            content = match.group(1).strip()
            new_line = f"[{content}]\n"
            if new_line != line:
                modified = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if modified:
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.writelines(new_lines)
            print(f"Updated: {filepath}")
        except Exception as e:
            print(f"Failed to write {filepath}: {e}", file=sys.stderr)
            return False
    return modified

def main():
    repo_root = os.getcwd()
    total_modified = 0
    for dir_name in TARGET_DIRS:
        target_dir = os.path.join(repo_root, dir_name)
        if not os.path.isdir(target_dir):
            print(f"Folder {target_dir} not found, skipping.", file=sys.stderr)
            continue
        for root, _, files in os.walk(target_dir):
            for file in files:
                if file.endswith('.pnach'):
                    full_path = os.path.join(root, file)
                    if process_file(full_path):
                        total_modified += 1

    print(f"Done. Total files modified: {total_modified}")

if __name__ == "__main__":
    main()
