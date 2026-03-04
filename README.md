# Neokoni's OTA Center

自托管的 OTA（空中升级）信息站点，展示 Neokoni ROM 构建的更新记录。

🔗 线上地址：**https://ota.neokoni.ink**

## 技术栈

- [Vue 3](https://vuejs.org/) + TypeScript（Composition API + `<script setup>`）
- [Vite](https://vite.dev/) 构建工具
- [@material/web 2](https://github.com/material-components/material-web)（Google 官方 Material Design 3 Web 组件）
- [Vue Router 4](https://router.vuejs.org/)（HTML5 History 模式）

## 快速开始

```sh
npm install
npm run dev
```

浏览器访问 `http://localhost:5173`。

## 可用命令

| 命令 | 说明 |
|------|------|
| `npm run dev` | 启动本地开发服务器（支持热重载） |
| `npm run build` | 类型检查 + 构建生产版本（输出到 `dist/`） |
| `npm run type-check` | 仅运行 TypeScript 类型检查 |
| `npm run preview` | 预览生产构建结果 |

## 文档

详细文档请参阅 [`docs/`](./docs/) 目录：

- [快速入门](./docs/getting-started.md)
- [项目架构](./docs/architecture.md)
- [添加设备](./docs/adding-devices.md)
- [OTA JSON 格式](./docs/ota-json-format.md)
- [生成 OTA JSON](./docs/generate-ota-json.md)
- [部署](./docs/deployment.md)

