# 快速入门

本文档介绍如何在本地搭建开发环境并运行 ota_site 项目。

## 前置要求

| 工具 | 最低版本 | 推荐安装方式 |
|------|----------|-------------|
| Node.js | 20.19.0 或 ≥ 22.12.0 | [nodejs.org](https://nodejs.org/) |
| npm | 随 Node.js 附带 | — |
| Git | 任意版本 | [git-scm.com](https://git-scm.com/) |

## 克隆仓库

```bash
git clone https://github.com/neokoni/ota.git
cd ota
```

## 安装依赖

```bash
npm install
```

## 启动开发服务器

```bash
npm run dev
```

启动后，在浏览器中访问 `http://localhost:5173`（端口号以终端输出为准）。

## 可用命令

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动本地开发服务器，支持热重载 |
| `npm run build` | 类型检查 + 构建生产版本（输出到 `dist/`） |
| `npm run build-only` | 仅构建，跳过类型检查 |
| `npm run type-check` | 运行 TypeScript 类型检查（`vue-tsc`） |
| `npm run preview` | 在本地预览生产构建结果 |

## 推荐开发工具

- **IDE**：[Visual Studio Code](https://code.visualstudio.com/)
  - 扩展：[Vue - Official (Volar)](https://marketplace.visualstudio.com/items?itemName=Vue.volar)（请禁用 Vetur）
- **浏览器 DevTools 插件**：
  - Chrome/Edge/Brave：[Vue.js devtools](https://chromewebstore.google.com/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)
  - Firefox：[Vue.js devtools](https://addons.mozilla.org/en-US/firefox/addon/vue-js-devtools/)

## 目录结构速览

```
ota/
├── public/            # 静态资源（OTA JSON 等）
├── scripts/           # 辅助脚本（generate_ota_json.py）
├── src/
│   ├── assets/        # 全局样式
│   ├── config/        # 设备配置与站点配置
│   ├── ota/           # 各设备更新日志 JSON
│   ├── router/        # Vue Router 路由配置
│   └── views/         # 页面组件
├── docs/              # 项目文档（当前目录）
├── index.html         # HTML 入口
├── vite.config.ts     # Vite 配置
├── package.json
└── tsconfig.json
```

更多细节请参阅[项目架构](./architecture.md)文档。
