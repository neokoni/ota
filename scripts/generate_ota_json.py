import os
import sys
import json
import hashlib
import re
import argparse
import zipfile

# Default Configuration
DEFAULT_BASE_URL = "https://pan.neokoni.ink/d/NeoBuilds"

def get_sha(sha_algo, file_path):
    if sha_algo.upper() == "SHA1":
        algo = hashlib.sha1()
    elif sha_algo.upper() == "SHA256":
        algo = hashlib.sha256()
    else:
        raise ValueError(f"Unsupported SHA algorithm: {sha_algo}")
    with open(file_path, 'rb') as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            algo.update(data)
    return algo.hexdigest()

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

def truncate_version_at_dot(version_str):
    """Truncate version string at first dot (e.g. '16.2.0' -> '16')"""
    match = re.match(r'^([^.]+)', version_str)
    return match.group(1) if match else version_str

def exit_with_error(msg):
    if msg:
        print(f"Error: {msg}")
    sys.exit(1)

def get_streaming_properties(zip_path):
    try:
        ota_zip = zipfile.ZipFile(zip_path, 'r')
        metadata = ota_zip.read('META-INF/com/android/metadata').decode('utf-8')
        for line in metadata.splitlines():
            k,v = line.split('=', 1)
            if k == "ota-property-files":
                return v.strip()
        return None
    except Exception:
        return None

def main():
    parser = argparse.ArgumentParser(description="Generate OTA JSON from zip and prop files.")
    parser.add_argument("files", nargs='+', help="Path to .zip and .prop files")
    parser.add_argument("--version", help="Override version (e.g. version-17)")
    parser.add_argument("--os-version", help="Override OS version (e.g. 1.2.3)")
    parser.add_argument("--os", help="Override OS name (e.g. ExampleUI)")
    parser.add_argument("--device", help="Override device codename (e.g. lemonades)")
    parser.add_argument("--date", help="Override date (e.g. 2026-02-26)")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL, help="Override base URL")
    parser.add_argument("--format", default="2", help="OTA format data version (default: 2), from Android 17, use 2 for new format")
    parser.add_argument("--no-stream", action="store_true", help="Disable try to add streaming install properties")
    parser.add_argument("-y", "--yes", action="store_true", help="Skip confirmation and save directly")
    parser.add_argument("-n", "--no", action="store_true", help="Skip saving, only generate preview")
    parser.add_argument("-t", "--type", default="UNOFFICIAL", help="OTA type (default: UNOFFICIAL)")
    
    args = parser.parse_args()

    if len(args.files) != 2:
        print("Usage: python3 generate_ota_json.py <file1> <file2> [options]")
        exit_with_error("One must be a .zip file, the other a build.prop file")

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
        exit_with_error("Could not identify zip and prop files. Ensure one ends with .zip and the other is a .prop file.")

    # Handle relative paths
    zip_path = os.path.abspath(zip_path)
    prop_path = os.path.abspath(prop_path)

    if not os.path.exists(zip_path):
        exit_with_error(f"Zip file not found: {zip_path}")
    if not os.path.exists(prop_path):
        exit_with_error(f"Prop file not found: {prop_path}")
    print(f"Processing Zip: {zip_path}")
    print(f"Processing Prop: {prop_path}")

    # 1. Get timestamp from build.prop
    print("Step 1: Reading build.prop...")
    props = parse_prop(prop_path)
    utc_time = props.get('ro.system.build.date.utc')
    if args.format == "2":
        security_path = props.get('ro.build.version.security_patch')
        sdk = props.get('ro.build.version.sdk')
    if not utc_time:
        exit_with_error("Error: ro.system.build.date.utc not found in build.prop")
    print(f"  Found timestamp: {utc_time}")

    # 2. Get file info (size and SHA1)
    print("Step 2: Analyzing Zip file...")
    file_size = os.path.getsize(zip_path)
    print(f"  File size: {file_size} bytes")

    if args.format == "2":
        sha_algo = "SHA256"
    elif args.format == "1":
        sha_algo = "SHA1"
    else:
        exit_with_error(f"Unsupported OTA version: {args.format}")
    
    print(f"  Calculating {sha_algo} (this may take a moment)...")
    file_id = get_sha(sha_algo, zip_path)
    print(f"  {sha_algo}: {file_id}")

    # 3. Parse filename
    print("Step 3: Parsing filename...")
    zip_filename = os.path.basename(zip_path)
    filename_no_ext = os.path.splitext(zip_filename)[0]
    
    # Expected format: Name-Ver-Device-Date-Tags.zip
    # Example: ExampleUI-lemonades-20251208-Unofficial-GMS.zip
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
        exit_with_error("Date (YYYYMMDD) not found in filename and no --date argument provided.")
    elif args.date:
        # If date provided via args, handle it
        # Assuming args.date is YYYY-MM-DD or YYYYMMDD
        date_str = args.date.replace('-', '')
        # If we didn't find it in filename, we can't easily deduce index for version/device split
        # but we can try to proceed if we have overrides or if we found it but want to override

    # URL Construction
    # https://pan.neokoni.ink/d/NeoBuilds/lemonades/ExampleUI/version-17/2025-12-08/ExampleUI-16-lemonades-20251208-Unofficial-GMS.zip
    
    # Format date: 20251208 -> 2025-12-08
    if len(date_str) == 8:
        date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    else:
        date_formatted = date_str # assume already formatted or handle error?

    # Re-evaluate device codename if needed (not passed in args currently, maybe add?)
    # User didn't ask for device override, so keep from filename
    # Apply version truncation to path_ver_part as well (will be set in next block)
    
    url = f"{args.base_url}/{args.device}/{args.os}/{args.version}/{date_formatted}/{zip_filename}"
    
    print(f"  Parsed Device: {args.device}")
    print(f"  Parsed Version: {args.version}")
    print(f"  Generated URL: {url}")

    # 4. Build JSON
    if args.format == "1":
        ota_data = {
            "response": [
                {
                    "datetime": int(utc_time),
                    "filename": zip_filename, # Full filename with extension
                    "id": file_id,
                    "size": file_size,
                    "url": url,
                    "version": args.version
                }
            ]
        }
    elif args.format == "2" :
        ota_data = [
            {
                "datetime": int(utc_time),
                "type": args.type,
                "version": args.os_version if args.os_version else args.version,
                "files": [
                    {
                       "filename": zip_filename,
                       "size": file_size,
                       "sha256": file_id,
                       "url": url,
                       "os_sdk_level": sdk,
                       "os_patch_level": security_path
                    }
                ]
            }
        ]
    else:
        exit_with_error(f"Unsupported OTA version: {args.format}")

     # Project root is parent of script dir
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(script_dir)
    
    output_rel_path = os.path.join("public", args.os, args.version, args.device, "ota.json")
    output_abs_path = os.path.join(project_root, output_rel_path)

    if not args.no_stream:
        if args.format == "2":
            streaming_properties = get_streaming_properties(zip_path)
            if streaming_properties:
                ota_data[0]["files"][0]["ota_property_files"] = streaming_properties



    print("\n" + "="*30)
    print("JSON Content Preview:")
    print(json.dumps(ota_data, indent=2))
    print("="*30)
    print(f"Target File: {output_abs_path}")
    
    # Determine action based on flags or user input
    if args.no:
        print("\nPreview only (-n flag set). File not saved.")
    elif args.yes:
        confirm = 'y'
        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)
        with open(output_abs_path, 'w') as f:
            json.dump(ota_data, f, indent=2)
        print("File saved successfully.")
    else:
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
