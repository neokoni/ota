# 部署

## 自动部署（GitHub Actions）

项目使用 GitHub Actions 实现代码推送后的自动构建与部署。工作流文件位于 `.github/workflows/deployment.yml`。

### 触发条件

| 触发方式 | 说明 |
|----------|------|
| 推送到 `main` 分支 | 自动触发构建与部署 |
| 向 `main` 分支提交 Pull Request | 触发构建，用于验证 |
| 手动触发（`workflow_dispatch`） | 在 GitHub Actions 页面手动运行 |

### 工作流步骤

```
1. 检出代码（actions/checkout@v4）
2. 配置 Node.js 环境（actions/setup-node@v4，使用 latest 版本）
3. 安装依赖（npm install）
4. 构建项目（npm run build → 输出到 dist/）
5. 通过 SCP 将 dist/ 上传到服务器（appleboy/scp-action@v0.1.7）
```

### 服务器部署路径

构建产物会上传至：

```
/opt/1panel/www/sites/ota.neokoni.ink/index/
```

上传时 `dist/` 前缀会被去掉（`strip_components: 1`），并清除服务器上的旧文件（`rm: true`）。

### 配置 GitHub Secrets

自动部署需要在 GitHub 仓库的 **Settings → Secrets and variables → Actions** 中配置以下 Secrets：

| Secret 名称 | 说明 |
|-------------|------|
| `SERVER_HOST` | 服务器 IP 地址或域名 |
| `SERVER_USERNAME` | SSH 登录用户名 |
| `SERVER_PASSWORD` | SSH 登录密码 |

## 手动构建与部署

如需手动构建并部署：

```bash
# 1. 安装依赖
npm install

# 2. 构建生产版本
npm run build

# 3. 将 dist/ 目录内容上传至服务器
scp -r dist/* user@your-server:/opt/1panel/www/sites/ota.neokoni.ink/index/
```

## 本地预览生产构建

```bash
npm run build
npm run preview
```

访问终端输出的地址（默认 `http://localhost:4173`）预览生产版本效果。

## 静态文件说明

构建后，`dist/` 目录除了 Vue 应用的 HTML/JS/CSS 文件外，还包含：

- `public/` 目录下的所有静态资源（OTA JSON 文件等）
- `plain/device/:codename/AviumUI/avium-16/index.txt`：各设备的纯文本更新日志（由 Vite 插件在构建时自动生成）

## 服务器 Web 服务器配置建议

站点使用 Vue Router 的 HTML5 History 模式，因此 Web 服务器需要将所有非文件请求回退到 `index.html`。

**Nginx 配置示例：**

```nginx
location / {
    try_files $uri $uri/ /index.html;
}
```

**Apache `.htaccess` 示例：**

```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```
