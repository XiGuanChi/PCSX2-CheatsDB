#!/usr/bin/env python3
import os
import re
import sys

# Target folders to process
TARGET_DIRS = [f"cheats-v{i}" for i in range(1, 7)]

def contains_patch(content):
    """Return True if content contains 'patch=' (case-insensitive)."""
    return re.search(r'patch\s*=', content, re.IGNORECASE) is not None

def process_file(filepath):
    """Read file, apply fixes, and write back."""
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
        new_line = line  # default: keep unchanged

        # 1. Handle existing comment lines: //...
        comment_match = re.match(r'^\s*//(.*?)\s*$', stripped)
        if comment_match:
            content = comment_match.group(1).strip()
            if contains_patch(content):
                # Do NOT convert comments containing "patch=" to brackets
                new_line = line  # keep as is
            else:
                new_line = f"[{content}]\n"
            if new_line != line:
                modified = True
            new_lines.append(new_line)
            continue

        # 2. Handle bracket lines that might have been wrongly created: [patch=...]
        bracket_match = re.match(r'^\s*\[(.*?)\]\s*$', stripped)
        if bracket_match:
            content = bracket_match.group(1).strip()
            if contains_patch(content):
                # Convert back to a comment (remove brackets, add //)
                new_line = f"//{content}\n"
                if new_line != line:
                    modified = True
                new_lines.append(new_line)
                continue

        # 3. All other lines: keep unchanged
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
