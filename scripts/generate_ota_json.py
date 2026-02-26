import os
import sys
import json
import hashlib
import re
import argparse

# Default Configuration
DEFAULT_BASE_URL = "https://pan.neokoni.ink/d/OneDrive-Public"

def get_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            sha1.update(data)
    return sha1.hexdigest()

def parse_prop(prop_path):
    props = {}
    with open(prop_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            if '=' in line:
                key, value = line.split('=', 1)
                props[key.strip()] = value.strip()
    return props

def main():
    parser = argparse.ArgumentParser(description="Generate OTA JSON from zip and prop files.")
    parser.add_argument("files", nargs='+', help="Path to .zip and .prop files")
    parser.add_argument("--version", help="Override version (e.g. avium16)")
    parser.add_argument("--os", help="Override OS name (e.g. AviumUI)")
    parser.add_argument("--date", help="Override date (e.g. 2026-02-26)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Override base URL")
    
    args = parser.parse_args()

    if len(args.files) != 2:
        print("Usage: python3 generate_ota_json.py <file1> <file2> [options]")
        print("One must be a .zip file, the other a build.prop file")
        sys.exit(1)

    file1 = args.files[0]
    file2 = args.files[1]

    zip_path = None
    prop_path = None

    # Identify files by extension
    if file1.endswith('.zip'):
        zip_path = file1
    elif file1.endswith('.prop') or 'build.prop' in file1:
        prop_path = file1
    
    if file2.endswith('.zip'):
        zip_path = file2
    elif file2.endswith('.prop') or 'build.prop' in file2:
        prop_path = file2

    if not zip_path or not prop_path:
        print("Error: Could not identify zip and prop files. Ensure one ends with .zip and the other is a .prop file.")
        sys.exit(1)

    # Handle relative paths
    zip_path = os.path.abspath(zip_path)
    prop_path = os.path.abspath(prop_path)

    if not os.path.exists(zip_path):
        print(f"Error: Zip file not found: {zip_path}")
        sys.exit(1)
    if not os.path.exists(prop_path):
        print(f"Error: Prop file not found: {prop_path}")
        sys.exit(1)

    print(f"Processing Zip: {zip_path}")
    print(f"Processing Prop: {prop_path}")

    # 1. Get timestamp from build.prop
    print("Step 1: Reading build.prop...")
    props = parse_prop(prop_path)
    utc_time = props.get('ro.system.build.date.utc')
    if not utc_time:
        print("Error: ro.system.build.date.utc not found in build.prop")
        sys.exit(1)
    print(f"  Found timestamp: {utc_time}")

    # 2. Get file info (size and SHA1)
    print("Step 2: Analyzing Zip file...")
    file_size = os.path.getsize(zip_path)
    print(f"  File size: {file_size} bytes")
    
    print("  Calculating SHA1 (this may take a moment)...")
    file_id = get_sha1(zip_path)
    print(f"  SHA1: {file_id}")

    # 3. Parse filename
    print("Step 3: Parsing filename...")
    zip_filename = os.path.basename(zip_path)
    filename_no_ext = os.path.splitext(zip_filename)[0]
    
    # Expected format: Name-Ver-Device-Date-Tags.zip
    # Example: AviumUI-16-lemonades-20251208-Unofficial-GMS.zip
    parts = filename_no_ext.split('-')
    
    # Find date part (8 digits)
    date_index = -1
    date_str = ""
    for i, part in enumerate(parts):
        if re.match(r'^\d{8}$', part):
            date_index = i
            date_str = part
            break
    
    if date_index == -1 and not args.date:
        print("Error: Date (YYYYMMDD) not found in filename.")
        sys.exit(1)
    elif args.date:
        # If date provided via args, handle it
        # Assuming args.date is YYYY-MM-DD or YYYYMMDD
        date_str = args.date.replace('-', '')
        # If we didn't find it in filename, we can't easily deduce index for version/device split
        # but we can try to proceed if we have overrides or if we found it but want to override
    
    # Extract info
    # Version string: content before date
    if date_index != -1:
        version_str = "-".join(parts[:date_index])
        device_codename = parts[date_index - 1]
        rom_name = parts[0]
        try:
            rom_ver = parts[1] # Simple assumption based on example
        except IndexError:
             rom_ver = "unknown"
    else:
        # Fallback if date not in filename but passed via args
        # We need to guess or rely on args
        version_str = "Unknown"
        device_codename = "Unknown"
        rom_name = "Unknown"
        rom_ver = "Unknown"

    # Overrides
    if args.version:
        version_str = args.version
        # Try to update parts derived from version
        # If version is "avium16", we might want to split or just use it
        # The original code did: url_ver_part = f"{rom_name_normalized}{rom_ver}"
        # detailed parsing logic below needs adjustment to support overrides properly

    if args.os:
        rom_name = args.os

    # Recalculate derived values based on potential overrides
    
    # Normalize ROM name (e.g. AviumUI -> avium)
    rom_name_normalized = rom_name.lower()
    if rom_name_normalized.endswith('ui'):
        rom_name_normalized = rom_name_normalized[:-2]

    # URL Construction
    # https://pan.neokoni.ink/d/OneDrive-Public/lemonades/avium16/2025-12-08/AviumUI-16-lemonades-20251208-Unofficial-GMS.zip
    
    # Format date: 20251208 -> 2025-12-08
    if len(date_str) == 8:
        date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    else:
        date_formatted = date_str # assume already formatted or handle error?

    # URL Version part: avium16 (lowercase name + version)
    # If args.version is provided, use it directly? 
    # The user example was --version=avium16
    if args.version:
        url_ver_part = args.version
        # Update path_ver_part logic if possible or assume standard
        # Original: path_ver_part = f"{rom_name_normalized}-{rom_ver}"
        # If version arg is avium16, we might not know rom_ver distinct from rom_name
        # Let's assume user provides what they want for the URL segment
    else:
        url_ver_part = f"{rom_name_normalized}{rom_ver}"

    # Re-evaluate device codename if needed (not passed in args currently, maybe add?)
    # User didn't ask for device override, so keep from filename
    
    url = f"{args.base_url}/{device_codename}/{url_ver_part}/{date_formatted}/{zip_filename}"
    
    print(f"  Parsed Device: {device_codename}")
    print(f"  Parsed Version: {version_str}")
    print(f"  Generated URL: {url}")

    # 4. Build JSON
    ota_data = {
        "response": [
            {
                "datetime": int(utc_time),
                "filename": zip_filename, # Full filename with extension
                "id": file_id,
                "size": file_size,
                "url": url,
                "version": version_str
            }
        ]
    }

    # 5. Determine output path
    # public/AviumUI/avium-16/lemonades/ota.json
    # Path version part: avium-16 (lowercase name + - + version)
    
    if args.version:
         # Attempt to reconstruct "avium-16" from "avium16" or similar if possible
         # Or just use the override if it looks right. 
         # But the user example "avium16" lacks the hyphen.
         # Let's try to be smart or just use what we have.
         # If user gave --version=avium16, maybe we use that for directory too?
         # Existing structure uses "avium-16".
         path_ver_part = args.version
    else:
        path_ver_part = f"{rom_name_normalized}-{rom_ver}" # avium-16
    
    # Project root is parent of script dir
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(script_dir)
    
    output_rel_path = os.path.join("public", rom_name, path_ver_part, device_codename, "ota.json")
    output_abs_path = os.path.join(project_root, output_rel_path)

    print("\n" + "="*30)
    print("JSON Content Preview:")
    print(json.dumps(ota_data, indent=2))
    print("="*30)
    print(f"Target File: {output_abs_path}")
    
    try:
        confirm = input("\nSave to file? (y/n): ").lower()
    except KeyboardInterrupt:
        print("\nOperation cancelled.")
        sys.exit(0)

    if confirm == 'y':
        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)
        with open(output_abs_path, 'w') as f:
            json.dump(ota_data, f, indent=2)
        print("File saved successfully.")
    else:
        print("Operation cancelled.")

if __name__ == "__main__":
    main()
