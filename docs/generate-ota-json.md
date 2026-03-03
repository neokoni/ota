# 生成 OTA JSON

`scripts/generate_ota_json.py` 脚本用于从 ROM ZIP 包和 `build.prop` 文件自动生成 `ota.json`，无需手动填写构建时间戳、文件大小和 SHA-1 哈希。

## 前置要求

- Python 3.x（无需额外依赖）
- ROM ZIP 包（例如 `AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip`）
- 从 ROM ZIP 包中提取的 `build.prop` 文件（位于 `system/build.prop`）

## 基本用法

```bash
python3 scripts/generate_ota_json.py <zip文件> <build.prop文件> [选项]
```

示例：

```bash
python3 scripts/generate_ota_json.py \
  AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip \
  build.prop
```

脚本会：
1. 从 `build.prop` 读取 `ro.system.build.date.utc` 时间戳
2. 计算 ZIP 文件的大小和 SHA-1 哈希
3. 从文件名解析设备代号、ROM 名称和版本信息
4. 根据解析结果构造下载 URL
5. 预览生成的 JSON 内容，并询问是否保存

## 命令行参数

| 参数 | 说明 | 示例 |
|------|------|------|
| `files` | （必填）ZIP 文件和 build.prop 文件路径，顺序不限 | `rom.zip build.prop` |
| `--version` | 覆盖版本标识（用于 URL 和 JSON 中） | `--version=avium16` |
| `--os` | 覆盖 ROM 名称 | `--os=AviumUI` |
| `--date` | 覆盖日期（YYYY-MM-DD 或 YYYYMMDD 格式） | `--date=2026-02-26` |
| `--base-url` | 覆盖下载基础 URL（默认：`https://pan.neokoni.ink/d/OneDrive-Public`） | `--base-url=https://example.com/dl` |

## 文件名解析规则

脚本期望 ZIP 文件名遵循以下格式：

```
{ROM名称}-{版本号}-{设备代号}-{日期(YYYYMMDD)}-{标签...}.zip
```

脚本会自动识别 8 位数字日期（如 `20260226`），并以此为分隔点解析：
- **日期之前**：ROM 名称和版本信息
- **日期前一位**：设备代号
- **日期之后**：附加标签（忽略）

## 输出路径

生成的 `ota.json` 将保存至：

```
public/{ROM名称}/{版本标识}/{设备代号}/ota.json
```

例如，处理 `AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip` 时，输出路径为：

```
public/AviumUI/AviumUI-16.2.0-nabu/nabu/ota.json
```

> **提示**：如果输出路径与预期不符，可使用 `--version` 参数手动指定版本标识以控制路径。

## 交互式确认

脚本在保存文件前会显示 JSON 预览并询问确认：

```
==============================
JSON Content Preview:
{
  "response": [
    {
      "datetime": 1772097425,
      "filename": "AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip",
      "id": "618bedfd390a3031da6bd063ac21d6d68b2e2faf",
      "size": 2590263421,
      "url": "https://pan.neokoni.ink/d/OneDrive-Public/nabu/avium16/2026-02-26/...",
      "version": "AviumUI-16.2.0-nabu"
    }
  ]
}
==============================
Target File: /path/to/public/AviumUI/AviumUI-16.2.0-nabu/nabu/ota.json

Save to file? (y/n):
```

输入 `y` 确认保存，输入其他任意内容或按 `Ctrl+C` 取消操作。

## OTA JSON 格式详情

生成的 JSON 结构详见 [OTA JSON 格式](./ota-json-format.md)。
