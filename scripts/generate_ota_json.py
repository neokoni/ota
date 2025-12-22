import os
import sys
import json
import hashlib
import re

# 配置部分
BASE_URL = "https://pan.neokoni.ink/d/OneDrive-Public"

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
    if len(sys.argv) != 3:
        print("用法: python3 generate_ota_json.py <文件1> <文件2>")
        print("其中一个必须是 .zip 文件，另一个必须是 build.prop 文件")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    zip_path = None
    prop_path = None

    # 根据扩展名识别文件
    if file1.endswith('.zip'):
        zip_path = file1
    elif file1.endswith('.prop') or 'build.prop' in file1:
        prop_path = file1
    
    if file2.endswith('.zip'):
        zip_path = file2
    elif file2.endswith('.prop') or 'build.prop' in file2:
        prop_path = file2

    if not zip_path or not prop_path:
        print("错误: 无法识别 zip 和 prop 文件。请确保一个以 .zip 结尾，另一个是 .prop 文件。")
        sys.exit(1)

    # 处理相对路径
    zip_path = os.path.abspath(zip_path)
    prop_path = os.path.abspath(prop_path)

    if not os.path.exists(zip_path):
        print(f"错误: 找不到 Zip 文件: {zip_path}")
        sys.exit(1)
    if not os.path.exists(prop_path):
        print(f"错误: 找不到 Prop 文件: {prop_path}")
        sys.exit(1)

    print(f"正在处理 Zip: {zip_path}")
    print(f"正在处理 Prop: {prop_path}")

    # 1. 从 build.prop 获取时间戳
    print("步骤 1: 读取 build.prop...")
    props = parse_prop(prop_path)
    utc_time = props.get('ro.system.build.date.utc')
    if not utc_time:
        print("错误: 在 build.prop 中未找到 ro.system.build.date.utc")
        sys.exit(1)
    print(f"  找到时间戳: {utc_time}")

    # 2. 获取文件信息 (大小和 SHA1)
    print("步骤 2: 分析 Zip 文件...")
    file_size = os.path.getsize(zip_path)
    print(f"  文件大小: {file_size} 字节")
    
    print("  正在计算 SHA1 (这可能需要一点时间)...")
    file_id = get_sha1(zip_path)
    print(f"  SHA1: {file_id}")

    # 3. 解析文件名
    print("步骤 3: 解析文件名...")
    zip_filename = os.path.basename(zip_path)
    filename_no_ext = os.path.splitext(zip_filename)[0]
    
    # 预期格式: Name-Ver-Device-Date-Tags.zip
    # 示例: AviumUI-16-lemonades-20251208-Unofficial-GMS.zip
    parts = filename_no_ext.split('-')
    
    # 查找日期部分 (8位数字)
    date_index = -1
    date_str = ""
    for i, part in enumerate(parts):
        if re.match(r'^\d{8}$', part):
            date_index = i
            date_str = part
            break
    
    if date_index == -1:
        print("错误: 在文件名中未找到日期 (YYYYMMDD)。")
        sys.exit(1)

    # 提取信息
    # 版本字符串: 日期之前的所有内容
    version_str = "-".join(parts[:date_index])
    
    # 设备代号: 日期前一部分
    device_codename = parts[date_index - 1]
    
    # ROM 名称和版本 (假设在开头)
    # AviumUI-16 -> Name=AviumUI, Ver=16
    rom_name = parts[0]
    rom_ver = parts[1] # 基于示例的简单假设
    
    # 规范化 ROM 名称 (例如 AviumUI -> avium)
    rom_name_normalized = rom_name.lower()
    if rom_name_normalized.endswith('ui'):
        rom_name_normalized = rom_name_normalized[:-2]

    # URL 构建
    # https://pan.neokoni.ink/d/OneDrive-Public/lemonades/avium16/2025-12-08/AviumUI-16-lemonades-20251208-Unofficial-GMS.zip
    
    # 格式化日期: 20251208 -> 2025-12-08
    date_formatted = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:]}"
    
    # URL 版本部分: avium16 (小写名称 + 版本)
    url_ver_part = f"{rom_name_normalized}{rom_ver}"
    
    url = f"{BASE_URL}/{device_codename}/{url_ver_part}/{date_formatted}/{zip_filename}"
    
    print(f"  解析到的设备: {device_codename}")
    print(f"  解析到的版本: {version_str}")
    print(f"  生成的 URL: {url}")

    # 4. 构建 JSON
    ota_data = {
        "response": [
            {
                "datetime": int(utc_time),
                "filename": zip_filename, # 使用包含扩展名的完整文件名
                "id": file_id,
                "size": file_size,
                "url": url,
                "version": version_str
            }
        ]
    }

    # 5. 确定输出路径
    # public/AviumUI/avium-16/lemonades/ota.json
    # 路径版本部分: avium-16 (小写名称 + - + 版本)
    path_ver_part = f"{rom_name_normalized}-{rom_ver}" # avium-16
    
    # 项目根目录是脚本目录的父目录
    script_dir = os.path.dirname(os.path.realpath(__file__))
    project_root = os.path.dirname(script_dir)
    
    output_rel_path = os.path.join("public", rom_name, path_ver_part, device_codename, "ota.json")
    output_abs_path = os.path.join(project_root, output_rel_path)

    print("\n" + "="*30)
    print("JSON 内容预览:")
    print(json.dumps(ota_data, indent=2))
    print("="*30)
    print(f"目标文件: {output_abs_path}")
    
    try:
        confirm = input("\n保存到文件? (y/n): ").lower()
    except KeyboardInterrupt:
        print("\n操作已取消。")
        sys.exit(0)

    if confirm == 'y':
        os.makedirs(os.path.dirname(output_abs_path), exist_ok=True)
        with open(output_abs_path, 'w') as f:
            json.dump(ota_data, f, indent=2)
        print("文件保存成功。")
    else:
        print("操作已取消。")

if __name__ == "__main__":
    main()
