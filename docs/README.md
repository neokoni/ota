# Neokoni's OTA Center — 文档

本目录包含 **ota_site** 项目的完整技术文档。

## 文档目录

| 文档 | 描述 |
|------|------|
| [快速入门](./getting-started.md) | 本地开发环境搭建 |
| [项目架构](./architecture.md) | 项目结构与技术架构说明 |
| [添加设备](./adding-devices.md) | 如何添加新设备和 ROM 版本 |
| [OTA JSON 格式](./ota-json-format.md) | 面向刷机工具的 OTA JSON 文件格式说明 |
| [生成 OTA JSON](./generate-ota-json.md) | 使用 `generate_ota_json.py` 脚本生成 OTA JSON |
| [部署](./deployment.md) | CI/CD 与服务器部署说明 |

## 项目简介

**ota_site** 是一个自托管的 OTA（空中升级）信息站点，用于展示 Neokoni ROM 构建的更新记录。用户可以在此站点：

- 浏览所有受支持的设备列表
- 查看每台设备上可用的 ROM 系统及版本
- 阅读各版本的详细更新日志
- 获取 OTA 下载包的 JSON 链接（供刷机工具自动识别）

## 技术栈概览

- **前端框架**：[Vue 3](https://vuejs.org/) + TypeScript
- **构建工具**：[Vite](https://vite.dev/)
- **UI 组件库**：[@material/web 2](https://github.com/material-components/material-web)（Material Web Components，Google 官方 Material Design 3）
- **路由**：[Vue Router 4](https://router.vuejs.org/)
- **CI/CD**：GitHub Actions + SSH 部署
