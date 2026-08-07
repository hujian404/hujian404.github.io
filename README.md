# Veritas | Personal Blog

基于 HTML/CSS/JS 模板搭建的个人博客，使用 **GitHub Pages** 免费托管。

## 目录结构

```
.
├── index.html          # 博客首页（Home / About / Resume / Services / Works / Blog / Contact）
├── blog-single.html    # 博客文章详情页
├── css/                # 样式文件
├── js/                 # 脚本文件
├── fonts/              # 字体图标
└── images/             # 图片资源
```

> 所有资源引用均使用**相对路径**，因此无论部署在用户主页（`<username>.github.io`）还是项目子路径下都能正常加载。

## 本地预览

直接用浏览器打开 `index.html` 即可。若希望以本地服务器方式预览：

```bash
# Python 3
python -m http.server 8000
# 然后访问 http://localhost:8000
```

## 部署到 GitHub Pages

1. 将代码推送到 GitHub 仓库的 `main` 分支根目录。
2. （用户主页站点）将仓库重命名为 `<username>.github.io`，例如 `hujian404.github.io`。
3. 进入仓库 **Settings → Pages**，Source 选择 `main` 分支、`/ (root)` 目录，保存。
4. 等待 1~2 分钟，访问 `https://<username>.github.io` 即可。

## 个性化修改指南

需要替换的位置集中在 `index.html` 与 `blog-single.html`：

- **作者名称 / 标语**：搜索 `Veritas`、`blogger` / `developer` / `lifelong learner`。
- **联系方式**：搜索 `3194446884@qq.com`、`hujian404`。
- **社交链接**：搜索 `github.com/hujian404`、`mailto:`。
- **博客文章**：在 `index.html` 的 `<!-- card item --> ... id="blog"` 区块新增/修改 `news-block`，并在 `blog-single.html` 中编辑正文。
- **联系表单**：当前使用 `mailto:` 在纯静态环境下打开邮件客户端。如需更完善的表单，可接入 [Formspree](https://formspree.io/) 等第三方服务，替换 `<form>` 的 `action`。

## 备注

- 地图组件依赖 Google Maps API Key；如未配置有效 Key，地图区域不会显示，不影响其它功能。
