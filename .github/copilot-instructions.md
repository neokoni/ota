# Copilot Instructions — neokoni/ota

## 项目概述

**ota_site** 是一个自托管的 OTA（空中升级）信息站点，展示 Neokoni ROM 构建的更新记录。
- 线上地址：`https://ota.neokoni.ink`
- 面向用户：ROM 用户查看更新日志；刷机工具（如 Avium）读取 OTA JSON

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.5.x | 前端框架（Composition API + `<script setup>`） |
| TypeScript | ~5.9 | 类型系统 |
| Vite | ^7.x | 构建工具与开发服务器 |
| Vue Router 4 | ^4.6 | 客户端路由（HTML5 History 模式） |
| @material/web | ^2.4.1 | Material Web Components（Google 官方 Material Design 3 Web 组件） |

## 目录结构

```
ota/
├── public/AviumUI/avium-16/{codename}/ota.json   # 供刷机工具读取的 OTA JSON
├── scripts/generate_ota_json.py                  # 自动生成 ota.json 的 Python 脚本
├── src/
│   ├── assets/main.css         # 全局样式（CSS 变量、字体、基础覆盖）
│   ├── config/
│   │   ├── devices.ts          # 类型定义 + import.meta.glob 加载所有 ota/*.json
│   │   └── site.ts             # ICP 备案信息 (siteConfig) + 壁纸 API (wallpaperConfig)
│   ├── ota/
│   │   ├── nabu.json           # 小米平板5 (Xiaomi Pad 5) 更新日志
│   │   └── lemonades.json      # 一加9R (OnePlus 9R) 更新日志
│   ├── router/index.ts         # 路由定义
│   ├── views/
│   │   ├── HomeView.vue             # 首页
│   │   ├── DeviceSelectionView.vue  # 设备列表页
│   │   ├── DeviceView.vue           # 设备详情页（ROM 系统列表）
│   │   ├── SystemView.vue           # 系统版本列表页
│   │   ├── ChangelogView.vue        # 版本更新日志页
│   │   └── NotFoundView.vue         # 404 页面
│   ├── App.vue                 # 根组件：顶栏、侧边抽屉导航、主题切换、动态配色
│   └── main.ts                 # 应用入口
├── docs/                       # 详细技术文档（中文）
├── vite.config.ts              # Vite 配置，含两个自定义插件（纯文本日志接口）
└── .github/workflows/deployment.yml  # CI/CD：push main → npm build → SCP 上传服务器
```

## 路由结构

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | `HomeView` | 首页 |
| `/devices` | `DeviceSelectionView` | 设备列表 |
| `/device/:codename` | `DeviceView` | 设备 ROM 系统列表 |
| `/device/:codename/:system` | `SystemView` | 系统版本列表 |
| `/device/:codename/:system/:version` | `ChangelogView` | 版本更新日志 |
| `/:pathMatch(.*)` | `NotFoundView` | 404 |

## 数据流

```
src/ota/*.json
  └─ import.meta.glob (devices.ts)
       ├─ devices[]          → DeviceSelectionView, App.vue 侧边导航
       ├─ getDevice()        → DeviceView, ChangelogView
       └─ getSystem()        → SystemView, ChangelogView
```

`src/ota/` 下新增 JSON 文件后**无需修改任何其他文件**，会被自动加载。

## OTA JSON 数据格式（src/ota/*.json）

```jsonc
{
  "codename": "nabu",          // 设备代号（全小写，与文件名一致）
  "name": "Xiaomi Pad 5",
  "systems": [{
    "name": "AviumUI",
    "versions": [{
      "version": "avium-16",           // 版本标识（用于路由和 URL）
      "label": "类原生 AviumUI 16",    // 显示名称
      "otaUrl": "/AviumUI/avium-16/nabu/ota.json",  // 可选，指向 public/ 下的 ota.json
      "releases": [{                   // 按日期降序自动排列（ChangelogView 中排序）
        "date": "2026-02-26",
        "changes": ["更新内容（支持 HTML 内联标签：<a> <code> <s>）"]
      }]
    }]
  }]
}
```

## UI 设计惯例（CSS 规范）

- **悬停效果**：仅使用 `background-color` 过渡，禁止使用 `box-shadow` 或 `transform: translateY`
  ```css
  /* 正确 */
  transition: background-color 200ms ease;
  .item:hover { background-color: var(--md-sys-color-surface-variant); }
  /* 禁止 */
  /* box-shadow、transform: translateY 不用于 hover 状态 */
  ```
- **卡片盒模型**：包含 `padding` 的卡片/容器必须设置 `box-sizing: border-box`，防止移动端溢出
- **移动端适配**：`@media (max-width: 600px)` 减少容器和卡片的 `padding`
- **颜色系统**：使用 `var(--md-sys-color-*)` CSS 变量（@material/web / Material Design 3 token），在 `main.css` 中有静态回退值，运行时由 `applyTheme()` 动态覆盖
- **焦点样式**：使用 `:focus-visible { outline: 3px solid var(--md-sys-color-primary); }` 键盘导航可访问性

## App.vue 核心功能

- **顶部栏**：品牌 logo + 名称（点击返回首页）、菜单按钮、主题切换按钮
- **侧边抽屉**：首页入口 + 所有设备快捷链接（从 `devices` 配置自动生成）；移动端使用半透明遮罩 + push 布局
- **主题模式**：`auto` / `light` / `dark`，偏好存入 `localStorage`
- **动态配色**：从必应壁纸 API（`wallpaperConfig.api`）提取主色调，调用 `applyTheme()` 换肤

## Vite 自定义插件（vite.config.ts）

面向刷机工具提供纯文本更新日志：

| 插件 | 路径 | 说明 |
|------|------|------|
| `bpPlainTextMiddleware` | `/device/:codename/AviumUI/avium-16` | User-Agent 含 `Build/BP` 时返回纯文本日志 |
| `alwaysPlainTextPagePlugin` | `/plain/device/:codename/AviumUI/avium-16` | 开发时动态返回；构建时生成 `dist/plain/.../index.txt` |

## 常用命令

```bash
npm run dev          # 启动开发服务器（http://localhost:5173）
npm run build        # 类型检查 + 构建生产版本（输出 dist/）
npm run type-check   # 仅 TypeScript 类型检查
npm run preview      # 预览生产构建（http://localhost:4173）
```

## 部署

- **自动**：push 到 `main` 分支触发 GitHub Actions，构建后 SCP 上传到 `/opt/1panel/www/sites/ota.neokoni.ink/index/`
- **所需 Secrets**：`SERVER_HOST`、`SERVER_USERNAME`、`SERVER_PASSWORD`
- 服务器 Nginx 需配置 `try_files $uri $uri/ /index.html`（HTML5 History 模式）

## 如何添加新设备

1. 在 `src/ota/` 下新建 `{codename}.json`（格式见上方数据格式）
2. 可选：在 `public/AviumUI/avium-16/{codename}/ota.json` 添加供刷机工具使用的 OTA JSON
   - 使用 `python3 scripts/generate_ota_json.py <zip> <build.prop>` 自动生成

## 变更历史摘要

| PR | 内容 |
|----|------|
| #5 | 移除所有 hover `box-shadow` 和 `transform`，仅保留 `background-color` 过渡；为 `.device-card`/`.system-card` 添加 `box-sizing: border-box` 修复移动端溢出；减少 `≤600px` 下的内边距 |
