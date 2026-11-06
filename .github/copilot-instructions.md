# Copilot Instructions — neokoni/ota

## 项目概述

**ota_site** 是 NeoBuilds Changelog，展示 Neokoni ROM 的更新记录。
- 线上地址：`https://ota.neokoni.ink`
- 面向用户：ROM 用户查看更新日志；刷机工具（如 Avium）读取 OTA JSON

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.5.x | 前端框架（Composition API + `<script setup>`） |
| TypeScript | ~5.9 | 类型系统 |
| Vite | ^7.x | 构建工具与开发服务器 |
| Vue Router 4 | ^4.6 | 客户端路由（HTML5 History 模式） |
| @m3e/web | ^2.11 | Material 3 Expressive Web Components |
| @m3e/icons | ^1.0 | Material Symbols（SVG，按需注册） |

## 目录结构

```
ota/
├── public/AviumUI/avium-16/{codename}/ota.json   # 供刷机工具读取的 OTA JSON
├── scripts/generate_ota_json.py                  # 自动生成 ota.json 的 Python 脚本
├── src/
│   ├── assets/main.css         # 全局样式（CSS 变量、字体、基础覆盖）
│   ├── config/
│   │   ├── devices.ts          # 类型定义 + import.meta.glob 加载所有 ota/*.json
│   │   ├── site.ts             # ICP 备案信息 (siteConfig) + 壁纸 API (wallpaperConfig)
│   │   └── theme.ts            # 动态取色（每日缓存）+ auto/light/dark 主题模式
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
       ├─ devices[]          → DeviceSelectionView / DeviceView
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

- **组件库**：统一使用 `m3e-*` 自定义元素（`@m3e/web`），图标使用 `m3e-icon` + `@m3e/icons` 的 SVG 模块（`import "@m3e/icons/outlined/<name>"`）
- **悬停效果**：仅使用 state layer/背景色，禁止使用 `box-shadow` 或 `transform: translateY`；`main.css` 已将 `m3e-button` / `m3e-card` 的 hover/focus/pressed elevation token 置为 `0`
- **卡片盒模型**：包含 `padding` 的自定义容器必须设置 `box-sizing: border-box`，防止移动端溢出
- **移动端适配**：`@media (max-width: 600px)` 减少容器和卡片的 `padding`
- **颜色系统**：使用 `var(--md-sys-color-*)` token；`m3e-theme` 在运行时根据壁纸源色生成 Tonal Spot 动态方案，不要单独硬编码组件颜色（选中态等由主题 token 自动派生）
- **焦点样式**：`m3e-theme` 已启用 `strong-focus`；自定义元素沿用 `:focus-visible { outline: 3px solid var(--md-sys-color-primary); }`

## App.vue 核心功能

- **顶部栏**：`m3e-app-bar`，品牌 logo + 名称（点击返回首页）、抽屉开关、主题切换按钮
- **侧边导航**：`m3e-drawer-container` + `m3e-nav-rail`，仅「主页」与「设备列表」两个入口（设备列表 → `/devices`）；桌面端默认展开、导航后不收起，移动端为覆盖式抽屉
- **主题模式**：`auto` / `light` / `dark`，绑定 `m3e-theme` 的 `scheme`，偏好存入 `localStorage`
- **动态配色**：从必应壁纸 API（`wallpaperConfig.api`）提取源色，按本地日期每日缓存一次；`src/config/theme.ts` 负责取色与主题模式
- **页面过渡**：`router-view` 使用 `<transition mode="out-in">`，动画时长/缓动复用 `--md-sys-motion-spring-*` token，并尊重 `prefers-reduced-motion`

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
