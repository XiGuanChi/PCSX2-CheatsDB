#!/usr/bin/env python3
import os
import re
import sys

# Target folders to process
TARGET_DIRS = [
    "patches-team",
    "patcheats-v1",
    "patches-v1",
    "patches-v2",
    "patches-v3",
    "patches-v4",
    "patches-v5",
    "patches-v6"
]

def process_file(filepath):
    """Read file, replace comment lines with [Content] except those containing 'patch'."""
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
        # Match lines that consist only of a comment (optional surrounding whitespace)
        match = re.match(r'^\s*//(.*?)\s*$', stripped)
        if match:
            content = match.group(1).strip()
            # If the comment contains the word "patch", leave it untouched
            if "patch" in content:
                new_lines.append(line)   # keep original
            else:
                # Convert to [content]
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
