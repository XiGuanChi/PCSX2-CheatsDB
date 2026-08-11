import os
import yaml
import glob
import subprocess

def process_file(filepath, data):
    """
    This function is called for each YAML file.
    Parameters:
      - filepath: the full path to the file
      - data: the loaded YAML content (dictionary/list)
    """
    print(f"\n📄 Processing: {filepath}")
    
    # --- Example 1: Display the YAML structure ---
    print("YAML content:")
    print(yaml.dump(data, default_flow_style=False, allow_unicode=True))
    
    # --- Example 2: Run a command if the key 'script' or 'commands' exists ---
    if isinstance(data, dict):
        # If there is a 'script' field (string) – run it as a shell command
        if 'script' in data:
            cmd = data['script']
            print(f"🚀 Running script: {cmd}")
            subprocess.run(cmd, shell=True, check=False)
        
        # If there is a 'commands' field (list) – run each command
        if 'commands' in data and isinstance(data['commands'], list):
            for idx, cmd in enumerate(data['commands'], 1):
                print(f"🔹 Command #{idx}: {cmd}")
                subprocess.run(cmd, shell=True, check=False)
    
    # --- Example 3: Merge with other files (if needed) ---
    # (add your own logic here)

def main():
    # Find all files matching the pattern
    pattern = "mirror-patches-part*.yml"
    files = sorted(glob.glob(pattern))
    
    if not files:
        print("⚠️  No files found matching the pattern 'mirror-patches-part*.yml'")
        return
    
    print(f"🔍 Found {len(files)} files:")
    for f in files:
        print(f"   - {f}")
    
    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            process_file(filepath, data)
        except Exception as e:
            print(f"❌ Failed to process {filepath}: {e}")

if __name__ == "__main__":
    main()
