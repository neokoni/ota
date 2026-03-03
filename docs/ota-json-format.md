# OTA JSON 格式

`public/` 目录下的 `ota.json` 文件供刷机工具（如 AOSP/LineageOS 系 Updater App）读取，以实现自动检测和下载新版本。

## 文件路径约定

```
public/{ROM名称}/{版本标识}/{设备代号}/ota.json
```

示例：

```
public/AviumUI/avium-16/nabu/ota.json
public/AviumUI/avium-16/lemonades/ota.json
```

部署后，这些文件可通过以下 URL 访问：

```
https://ota.neokoni.ink/AviumUI/avium-16/nabu/ota.json
```

## 文件格式

```json
{
  "response": [
    {
      "datetime": 1772097425,
      "filename": "AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip",
      "id": "618bedfd390a3031da6bd063ac21d6d68b2e2faf",
      "size": 2590263421,
      "url": "https://pan.neokoni.ink/d/OneDrive-Public/nabu/avium16/2026-02-26/AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip",
      "version": "AviumUI-16.2.0-nabu"
    }
  ]
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `response` | 数组 | 固定键名，包含一个或多个版本条目（通常只含最新版本） |
| `datetime` | 整数 | 构建时间戳（UTC Unix 时间戳），从 ROM 的 `build.prop` 中的 `ro.system.build.date.utc` 字段读取 |
| `filename` | 字符串 | ZIP 包文件名（含扩展名），例如 `AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip` |
| `id` | 字符串 | ZIP 包的 SHA-1 哈希值，用于完整性校验 |
| `size` | 整数 | ZIP 包文件大小（字节） |
| `url` | 字符串 | ZIP 包的完整下载地址 |
| `version` | 字符串 | 版本标识字符串，格式通常为 `{ROM}-{版本号}-{设备代号}` |

## 文件名命名约定

ZIP 包文件名遵循以下格式：

```
{ROM名称}-{版本号}-{设备代号}-{日期(YYYYMMDD)}-{标签...}.zip
```

示例：

```
AviumUI-16.2.0-nabu-20260226-Unofficial-GMS.zip
```

| 片段 | 示例值 | 说明 |
|------|--------|------|
| ROM名称 | `AviumUI` | ROM 的名称 |
| 版本号 | `16.2.0` | ROM 版本号 |
| 设备代号 | `nabu` | 目标设备的代号 |
| 日期 | `20260226` | 构建日期（YYYYMMDD） |
| 标签 | `Unofficial-GMS` | 可选附加标签（如认证状态、GMS 包含情况） |

## 手动生成

可以手动创建 `ota.json`，也可以使用仓库提供的脚本自动生成。推荐使用脚本以减少人为错误，详见[生成 OTA JSON](./generate-ota-json.md)。

## 在网站中关联 OTA JSON

在对应设备的 `src/ota/*.json` 中，将 `otaUrl` 字段设置为 `ota.json` 的路径即可：

```json
{
  "version": "avium-16",
  "label": "类原生 AviumUI 16",
  "otaUrl": "/AviumUI/avium-16/nabu/ota.json",
  "releases": [ ... ]
}
```

站点会在更新日志页面展示"查看系统更新文件 (JSON)"链接，指向该 URL。
