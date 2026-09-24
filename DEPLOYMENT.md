# 《信任力》阅读站部署说明

本仓库以 `book/` 中的 Markdown 为唯一书稿源，VitePress负责把同一份内容生成静态阅读网站。正文不再手工复制到其他HTML仓库。

## 本地预览

需要Node.js 22。

```bash
npm ci
npm run docs:dev
```

本地构建检查：

```bash
npm run docs:build
npm run docs:preview
```

构建产物位于 `book/.vitepress/dist`，该目录是自动产物，不进入Git。

## EdgeOne Pages配置

| 配置项 | 值 |
|---|---|
| Git仓库 | `flyingpig707/PowerofTrust` |
| 生产分支 | `main` |
| Node.js | `22` |
| 安装命令 | `npm ci` |
| 构建命令 | `npm run docs:build` |
| 输出目录 | `book/.vitepress/dist` |

建议设置环境变量：

```text
VITEPRESS_SITE_URL=https://trust.learn-together.cn
VITEPRESS_EDIT_BRANCH=main
```

生产域名建议使用 `trust.learn-together.cn`。V0.2改版期间，非生产分支由EdgeOne生成预览部署；确认十二章完整后再合并到 `main`。

## 发布原则

- `main`继续承载当前正式可读版本。
- `book/v0.2-three-part-structure`承载V0.2完整改版和分支预览。
- 每完成一章，独立提交并推送。
- 内容审阅与网页预览均通过后，再合并正式版本。
- 旧的手工HTML阅读页在新站正式接管前继续保留，接管后只保留跳转或历史版本入口。
