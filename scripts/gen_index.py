#!/usr/bin/env python3
"""
自动扫描当前目录下的所有 HTML 文件，生成 index.html。
每个 HTML 文件需要包含 <!-- index: title, date, description --> 注释头。
"""
import os
import re
import html
from pathlib import Path
from datetime import datetime

EXPERIMENTS_DIR = Path(".")
OUTPUT_FILE = Path("index.html")
SKIP_FILES = {"index.html", "gen_index.py", ".nojekyll", "README.md"}
SKIP_DIRS = {".git", ".github", "scripts", "node_modules"}


def parse_html_metadata(filepath: Path) -> dict:
    """从 HTML 文件头提取 title, date, description"""
    meta = {"title": filepath.stem, "date": "", "description": ""}
    try:
        content = filepath.read_text(encoding="utf-8")
        # 尝试从 <title> 标签提取
        title_match = re.search(r"<title[^>]*>([^<]+)</title>", content, re.IGNORECASE)
        if title_match:
            meta["title"] = title_match.group(1).strip()

        # 尝试从 <meta name="description"> 提取
        desc_match = re.search(
            r'<meta\s+name=["\']description["\']\s+content=["\']([^"\']+)["\']',
            content, re.IGNORECASE
        )
        if desc_match:
            meta["description"] = desc_match.group(1).strip()

        # 尝试从注释头提取: <!-- index: Title | 2024-01-01 | Description -->
        comment_match = re.search(
            r'<!--\s*index:\s*([^|]+)\|([^|]+)\|?([^>]*)-->',
            content, re.IGNORECASE
        )
        if comment_match:
            meta["title"] = html.unescape(comment_match.group(1).strip())
            meta["date"] = comment_match.group(2).strip()
            meta["description"] = html.unescape(comment_match.group(3).strip())
    except Exception as e:
        print(f"Warning: Failed to parse {filepath}: {e}")
    return meta


def generate_index() -> str:
    """生成 index.html"""
    html_files = sorted(
        EXPERIMENTS_DIR.glob("*.html"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )

    items_html = ""
    for f in html_files:
        if f.name in SKIP_FILES:
            continue
        meta = parse_html_metadata(f)
        # 格式化日期
        try:
            dt = datetime.fromtimestamp(f.stat().st_mtime)
            date_str = meta["date"] or dt.strftime("%Y-%m-%d")
        except:
            date_str = meta["date"] or "Unknown"

        items_html += f"""
        <li class="item">
            <a href="{f.name}" class="item-link">
                <span class="item-title">{html.escape(meta['title'])}</span>
                <span class="item-date">{date_str}</span>
            </a>
            <p class="item-desc">{html.escape(meta['description'])}</p>
        </li>"""

    total_count = len([f for f in html_files if f.name not in SKIP_FILES])

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="实验 HTML 存档索引">
    <title>Experiments Index</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
               background: #f5f5f5; color: #333; line-height: 1.6; padding: 2rem; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        h1 {{ font-size: 1.8rem; margin-bottom: 0.5rem; color: #1a1a1a; }}
        .subtitle {{ color: #666; margin-bottom: 2rem; }}
        .count {{ background: #e0e0e0; padding: 0.2rem 0.6rem; border-radius: 4px;
                 font-size: 0.85rem; }}
        ul {{ list-style: none; }}
        .item {{ background: white; border-radius: 8px; padding: 1rem 1.2rem; margin-bottom: 0.8rem;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .item-link {{ display: flex; justify-content: space-between; align-items: center;
                    text-decoration: none; color: inherit; }}
        .item-link:hover .item-title {{ color: #0066cc; }}
        .item-title {{ font-weight: 600; color: #333; }}
        .item-date {{ color: #999; font-size: 0.85rem; }}
        .item-desc {{ color: #666; font-size: 0.9rem; margin-top: 0.3rem; padding-left: 0.5rem;
                     border-left: 2px solid #e0e0e0; }}
        .footer {{ text-align: center; color: #999; font-size: 0.8rem; margin-top: 2rem; }}
        .nojekyll {{ display: none; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Experiments Archive <span class="count">{total_count} 个实验</span></h1>
        <p class="subtitle">自动生成的索引页面 · 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <ul>{items_html if items_html else '<li class="item"><p class="item-desc">暂无实验记录</p></li>'}
        </ul>
        <div class="footer">由 gen_index.py 自动生成</div>
    </div>
</body>
</html>"""


if __name__ == "__main__":
    # 确保 _experiments 目录存在
    EXPERIMENTS_DIR.mkdir(exist_ok=True)

    # 生成 index.html
    index_content = generate_index()
    OUTPUT_FILE.write_text(index_content, encoding="utf-8")
    print(f"Generated {OUTPUT_FILE} with index of HTML files in {EXPERIMENTS_DIR}/")
