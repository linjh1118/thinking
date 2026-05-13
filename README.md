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
