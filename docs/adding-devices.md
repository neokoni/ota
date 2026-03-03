# 添加设备与 ROM 版本

本文档介绍如何向站点添加新设备、新 ROM 系统或新版本，以及如何更新现有版本的更新日志。

## 数据结构概览

每台设备对应 `src/ota/` 目录下的一个 JSON 文件，格式如下：

```jsonc
{
  "codename": "设备代号",        // 设备代号（全小写，与文件名一致）
  "name": "设备显示名称",
  "systems": [
    {
      "name": "ROM名称",          // 例如 "AviumUI"
      "description": "简介",     // 可选
      "versions": [
        {
          "version": "版本标识",  // 例如 "avium-16"
          "label": "版本显示名", // 例如 "类原生 AviumUI 16"
          "otaUrl": "/AviumUI/avium-16/设备代号/ota.json", // 可选，OTA JSON 路径
          "releases": [
            {
              "date": "YYYY-MM-DD",
              "version": "可选，具体版本号",
              "changes": [
                "更新内容条目1",
                "更新内容条目2（支持 HTML，如 <a> <code> <s> 标签）"
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

> **注意**：`releases` 数组的排序无关紧要，站点会在展示时按日期降序自动排列（最新日期显示在最前）。

## 添加新设备

### 第一步：创建设备 JSON 文件

在 `src/ota/` 目录下新建一个以设备代号命名的 JSON 文件，例如 `src/ota/lisa.json`：

```json
{
  "codename": "lisa",
  "name": "Xiaomi 11 Lite 5G NE",
  "systems": [
    {
      "name": "AviumUI",
      "versions": [
        {
          "version": "avium-16",
          "label": "类原生 AviumUI 16",
          "otaUrl": "/AviumUI/avium-16/lisa/ota.json",
          "releases": [
            {
              "date": "2026-03-01",
              "changes": [
                "初始构建版本"
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

新文件会被 `src/config/devices.ts` 中的 `import.meta.glob` 自动加载，**无需修改任何其他文件**。

### 第二步（可选）：添加 OTA JSON 文件

如果刷机工具需要读取 OTA 信息，在 `public/` 目录下创建对应路径的 `ota.json`：

```
public/AviumUI/avium-16/lisa/ota.json
```

文件格式详见 [OTA JSON 格式](./ota-json-format.md)。可以使用 `scripts/generate_ota_json.py` 脚本自动生成，详见[生成 OTA JSON](./generate-ota-json.md)。

## 添加新 ROM 系统

在现有设备的 JSON 文件中，向 `systems` 数组追加一个新对象即可：

```json
{
  "codename": "nabu",
  "name": "Xiaomi Pad 5",
  "systems": [
    {
      "name": "AviumUI",
      "versions": [ ... ]
    },
    {
      "name": "LineageOS",
      "versions": [
        {
          "version": "lineage-22",
          "label": "LineageOS 22.1",
          "releases": [
            {
              "date": "2026-03-01",
              "changes": ["初始构建"]
            }
          ]
        }
      ]
    }
  ]
}
```

## 添加新版本

在对应系统的 `versions` 数组中追加一个新版本对象：

```json
{
  "version": "avium-17",
  "label": "类原生 AviumUI 17",
  "otaUrl": "/AviumUI/avium-17/nabu/ota.json",
  "releases": [
    {
      "date": "2026-06-01",
      "changes": ["升级至 Android 17 基础版本"]
    }
  ]
}
```

## 更新现有版本的更新日志

直接向对应版本的 `releases` 数组中追加一条新记录即可，例如：

```json
{
  "date": "2026-03-10",
  "changes": [
    "上游代码:",
    "1. 更新安全补丁",
    "内核:",
    "1. 修复已知崩溃问题"
  ]
}
```

> **技巧**：`changes` 字段支持 HTML 内联标签，例如：
> - `<a href="..." target="_blank">链接文字</a>`
> - `<code>代码片段</code>`
> - `<s>删除线文字</s>`

## 验证

修改完成后，运行开发服务器检查展示效果：

```bash
npm run dev
```

访问对应设备路径，确认更新日志正常显示。如需检查类型，也可运行：

```bash
npm run type-check
```
