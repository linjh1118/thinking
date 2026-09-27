#!/usr/bin/env python3
"""Import the self-contained Jev Atlas and migrate its linked paper posters.

The original report is built from BrainHao Markdown. This import keeps its
content and interactive UI intact, replaces intranet routes with public local
paths, and copies the 13 linked posters without changing unrelated site pages.
"""
import argparse
import concurrent.futures
import re
from pathlib import Path
from urllib.request import ProxyHandler, build_opener

ROOT = Path(__file__).resolve().parents[1]
PAPERS = [
    '1706_Calibration_Modern_Neural_Networks',
    '2102_Calibrate_Before_Use', '2104_Surface_Form_Competition',
    '2309_Batch_Calibration', '2309_Robust_Multiple_Choice_Selectors',
    '2609_Type_Safe_Not_Error_Free', '2609_Same_Scores_Different_Decisions',
    '2609_JEV_as_a_Judge', '2609_JEV_vs_LLM_Rubric_Judges',
    '2609_Jev_Scientific_Decisions', '2609_Jev_Mobile',
    '2609_Jev_Edge_Orchestration',
    '2609_Calibrated_Decision_Models_Pentest',
]
PUBLIC = 'https://linjh1118.github.io/thinking/jev_atlas.html'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--poster-origin', required=True)
    args = parser.parse_args()
    origin = args.poster_origin.rstrip('/') + '/'
    content = args.source.read_text(encoding='utf-8')
    content = content.replace(origin, 'jev-papers/')
    content = content.replace('http://21.91.144.35:9448/jev-atlas.html', PUBLIC)
    content = '<!-- index: Jev Atlas · 决策模型研究手册 | 2026-09-27 | 八个项目的模型结构、训练数据与 Benchmark 精读，附全文搜索、概率实验室和 13 篇论文海报。 -->\n' + content
    (ROOT / 'jev_atlas.html').write_text(content, encoding='utf-8')

    def import_poster(name):
        opener = build_opener(ProxyHandler({}))
        html = opener.open(origin + name + '/index.html', timeout=30).read().decode('utf-8')
        html = html.replace('href="../index.html"', 'href="../../jev_atlas.html#home/papers"')
        html = html.replace("href='../index.html'", "href='../../jev_atlas.html#home/papers'")
        html = re.sub(r'[ \t]+$', '', html, flags=re.M)
        dest = ROOT / 'jev-papers' / name / 'index.html'
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(html, encoding='utf-8')
        return name, len(html.encode())

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        for name, size in pool.map(import_poster, PAPERS):
            print('{}: {} bytes'.format(name, size))
    print('Imported Jev Atlas and {} posters.'.format(len(PAPERS)))


if __name__ == '__main__':
    main()
