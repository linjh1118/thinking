# GitHub Pages HTML 自动部署实验

## 目标
把 HTML 可视化结果自动发布到 `linjh1118.github.io`，并通过 `index.html` 自动索引所有实验。

## 当前结构
```
exp111_github_pages/
├── .github/workflows/deploy.yml   # GitHub Actions 配置
├── scripts/gen_index.py           # 自动生成 index.html
├── _experiments/                  # 存放 HTML 文件的目录
│   └── demo_experiment.html       # 示例 HTML
└── README.md
```

## 部署步骤

### 1. 初始化目标仓库（只需执行一次）

把以下文件复制到 `linjh1118.github.io` 仓库的根目录：
- `.github/workflows/deploy.yml`
- `scripts/gen_index.py`
- `.nojekyll`（创建空文件，防止 Jekyll 处理 HTML）

```bash
# 在 linjh1118.github.io 仓库中
touch .nojekyll
mkdir -p _experiments scripts
# 复制文件
cp /path/to/Agent-Factory-Med/work/exp111_github_pages/.github/workflows/deploy.yml .github/workflows/
cp /path/to/Agent-Factory-Med/work/exp111_github_pages/scripts/gen_index.py scripts/
```

### 2. 添加新的 HTML 实验

在 `linjh1118.github.io` 仓库的 `_experiments/` 目录下添加 HTML 文件：

```html
<!-- index: 实验标题 | 2026-05-13 | 实验描述 -->
<!DOCTYPE html>
<html>
<head>
    <title>实验标题</title>
    <meta name="description" content="实验描述">
</head>
<body>
    <!-- 你的 HTML 内容 -->
</body>
</html>
```

### 3. 推送后自动部署

每次 push 到 `main` 分支，GitHub Actions 会：
1. 运行 `gen_index.py` 生成 `index.html`
2. 上传所有文件到 GitHub Pages
3. 实验自动出现在 `linjh1118.github.io/index.html`

### 4. 手动触发（可选）

在 GitHub 仓库页面 → Actions → "Deploy Experiments to Pages" → Run workflow

## 本地测试

```bash
cd /path/to/linjh1118.github.io
python3 scripts/gen_index.py
# 然后用浏览器打开 index.html 查看效果
```

## 注意事项

1. HTML 文件头必须包含 `<!-- index: Title | Date | Description -->` 注释
2. 如果 HTML 文件没有这个注释，会从 `<title>` 和 `<meta description>` 标签提取
3. 部署需要目标仓库开启 GitHub Pages（Settings → Pages → Source: GitHub Actions）


## Jev Atlas

[打开 Jev 决策模型研究手册](https://linjh1118.github.io/thinking/jev_atlas.html)：八个项目的模型结构、训练数据与 Benchmark 精读，包含搜索、页内目录、公式/结构图、概率实验室与 13 篇论文海报。

- 入口：`jev_atlas.html`，首页部署时自动收录。
- 海报：`jev-papers/`，所有返回链接回到专题页，访问不依赖内网。
- 内容源：BrainHao 的 `Topics/22_Jev/projects/`；原页面生成器位于 `00.work/260927_jev_survey/src/`。
- 更新导入：`scripts/publish_jev_atlas.py --source <生成的 HTML> --poster-origin <海报服务器地址>`。

### Jev Atlas 轻量加载版

公网版的首页为静态 HTML，首屏约 100 KB；文章 JSON、搜索索引、数学字体与图表引擎按需加载。`jev-atlas-assets/` 必须与 `jev_atlas.html` 一起部署。

维护入口：`scripts/jev-site/`。`content.json` 保存导入内容，`shell.html` 为预渲染页面框架，`app.js` 提供交互，`style.css` 提供样式。

```bash
npm ci --prefix scripts/jev-site
npm run build --prefix scripts/jev-site
```

从新版单文件导出重新导入时，先运行 `publish_jev_atlas.py` 完成公网链接转换，再运行 `node scripts/jev-site/build.mjs --import jev_atlas.html`。导入预渲染需 Chromium；可通过 `CHROME_PATH` 指定浏览器可执行文件。日常仅重建无需浏览器。

## FinJev 方案讨论页

[打开 FinJev 方法与评测方案讨论](https://linjh1118.github.io/thinking/finjev-design-review.html)：模型、数据、RLCD、评测与方案选择的六章讨论稿。

入口为 `finjev-design-review.html`，部署时自动收录到首页。单文件页面无需外部资源；选择保存在当前浏览器，可复制讨论方案或下载 JSON。
