# 项目架构

## 目录结构

```
ota/
├── public/
│   └── AviumUI/
│       └── avium-16/
│           ├── nabu/
│           │   └── ota.json        # 小米平板5 OTA 信息（供刷机工具读取）
│           └── lemonades/
│               └── ota.json        # 一加9R OTA 信息（供刷机工具读取）
├── scripts/
│   └── generate_ota_json.py        # 自动生成 OTA JSON 的 Python 脚本
├── src/
│   ├── assets/
│   │   └── main.css                # 全局样式
│   ├── config/
│   │   ├── devices.ts              # 设备数据类型定义与加载逻辑
│   │   └── site.ts                 # 站点配置（ICP 备案、壁纸 API）
│   ├── ota/
│   │   ├── nabu.json               # 小米平板5 更新日志数据
│   │   └── lemonades.json          # 一加9R 更新日志数据
│   ├── router/
│   │   └── index.ts                # Vue Router 路由定义
│   ├── views/
│   │   ├── HomeView.vue            # 首页
│   │   ├── DeviceSelectionView.vue # 设备选择页
│   │   ├── DeviceView.vue          # 设备详情页（系统列表）
│   │   ├── SystemView.vue          # 系统版本列表页
│   │   ├── ChangelogView.vue       # 版本更新日志页
│   │   └── NotFoundView.vue        # 404 页面
│   ├── App.vue                     # 根组件（顶部栏、侧边导航、主题切换）
│   └── main.ts                     # 应用入口
├── docs/                           # 项目文档
├── .github/
│   └── workflows/
│       └── deployment.yml          # CI/CD 自动部署工作流
├── index.html                      # HTML 入口文件
├── vite.config.ts                  # Vite 配置（含自定义插件）
├── tsconfig.json                   # TypeScript 配置（根）
├── tsconfig.app.json               # TypeScript 配置（应用）
└── tsconfig.node.json              # TypeScript 配置（Node 环境）
```

## 技术栈

| 技术 | 版本 | 用途 |
|------|------|------|
| Vue 3 | 3.5.x | 前端框架（Composition API） |
| TypeScript | ~5.9 | 类型系统 |
| Vite | ^7.x | 构建工具与开发服务器 |
| Vue Router 4 | ^4.6 | 客户端路由 |
| MDUI 2 | ^2.1 | Material Design 3 UI 组件库 |
| Roboto / Noto Sans SC | — | 字体（中英文） |

## 路由结构

| 路径 | 组件 | 说明 |
|------|------|------|
| `/` | `HomeView` | 首页（品牌介绍 + 入口按钮） |
| `/devices` | `DeviceSelectionView` | 设备选择列表 |
| `/device/:codename` | `DeviceView` | 设备页（显示可用 ROM 系统） |
| `/device/:codename/:system` | `SystemView` | 系统页（显示可用版本） |
| `/device/:codename/:system/:version` | `ChangelogView` | 版本更新日志 |
| `/:pathMatch(.*)` | `NotFoundView` | 404 页面 |

## 数据流

```
src/ota/*.json
       │
       ▼
src/config/devices.ts   ← import.meta.glob 动态加载所有 JSON
       │
       ├─ devices[]      → DeviceSelectionView / App.vue 侧边导航
       ├─ getDevice()    → DeviceView / ChangelogView
       └─ getSystem()    → SystemView / ChangelogView
```

所有设备数据来源于 `src/ota/` 目录下的 JSON 文件，`devices.ts` 使用 Vite 的 `import.meta.glob` 在构建时自动加载所有文件，无需手动注册。

## App.vue 根组件功能

- **顶部应用栏**：品牌名称、菜单按钮、主题切换按钮
- **侧边抽屉导航**：首页入口 + 所有设备快捷链接（自动从 `devices` 配置生成）
- **主题模式**：支持 `auto` / `light` / `dark` 三档，偏好保存到 `localStorage`
- **动态配色**：通过必应壁纸 API 提取主色调，调用 MDUI 的 `setColorScheme` 动态换肤

## Vite 自定义插件

`vite.config.ts` 中包含两个自定义 Vite 插件，用于向刷机工具（如 Avium 内置 OTA 检查器）暴露纯文本格式的更新日志：

### `bpPlainTextMiddleware`

- **触发条件**：请求的 `User-Agent` 中包含 `Build/BP`
- **匹配路径**：`/device/:codename/AviumUI/avium-16`
- **响应**：以 `text/plain` 格式返回该设备 AviumUI avium-16 版本的所有更新日志，HTML 标签被自动剥离

### `alwaysPlainTextPagePlugin`

- **匹配路径**：`/plain/device/:codename/AviumUI/avium-16`
- **开发/预览模式**：动态返回纯文本更新日志
- **生产构建**：在 `dist/plain/device/:codename/AviumUI/avium-16/index.txt` 生成静态文本文件

纯文本格式示例：

```
2026-02-26
==================
上游代码:
1. 更新AviumUI 16.2版本(QPR2)
内核:
1. 更新KernelSU

2026-01-16
==================
...
```

## 站点配置

`src/config/site.ts` 导出两项配置：

- **`siteConfig`**：页脚 ICP 备案信息数组，每项包含 `icp`（备案号）和 `icpLink`（链接）
- **`wallpaperConfig`**：壁纸 API 地址，用于动态配色初始化

## UI / CSS 设计惯例

### 悬停效果

所有可交互元素（导航项、设备卡片、系统项、版本项）的悬停效果**仅使用 `background-color` 过渡**，禁止使用 `box-shadow` 或 `transform: translateY`：

```css
/* 正确 */
transition: background-color 200ms ease;
.item:hover { background-color: var(--md-sys-color-surface-variant); }

/* 禁止——不使用 box-shadow 或 transform 作为 hover 效果 */
```

### 卡片盒模型

包含 `padding` 的卡片和容器必须设置 `box-sizing: border-box`，防止宽度超出视口（尤其在移动端）：

```css
.device-card, .system-card {
  width: 100%;
  padding: 24px;
  box-sizing: border-box; /* 必须，否则 375px 视口会溢出 */
}
```

### 移动端适配

在 `@media (max-width: 600px)` 断点下，减少容器和卡片的内边距以充分利用屏幕空间：

```css
@media (max-width: 600px) {
  .view-container { padding: 12px; }
  .card { padding: 16px; }
}
```

### 焦点样式

键盘导航可访问性使用 `:focus-visible`：

```css
.item:focus-visible {
  outline: 3px solid var(--md-sys-color-primary);
  outline-offset: 2px;
}
```
