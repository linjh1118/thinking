"""Export frozen public benchmark records into browsable subset files.

Input: an exp7 step1_prepare_data directory containing only public suites.
Output: jev-benchmark-data/questions/*.json; no predictions or private data.
Run: python3 scripts/jev-benchmarks/prepare_questions.py /path/to/step1_prepare_data
"""
import hashlib
import json
import sys
from collections import defaultdict
from pathlib import Path

root = Path(__file__).resolve().parents[2]
source = Path(sys.argv[1])
output = root / 'jev-benchmark-data/questions'
output.mkdir(exist_ok=True)
manifest = {'updated': '2026-10-07', 'benchmarks': []}
configs = [
 ('jevbench', 'JevBench', '公开原题；仅 public231，不含封存评测题。', 'https://github.com/fstandhartinger/jevbench/tree/bb05a335bc809e61b20c0f745d25499a82b326fc'),
 ('jevals', 'Jevals', 'suite 0.1.0 固定公开题。Choice、Noul、Score 各300题；不重复展示5次推理。Jevals Contributors / CC-BY-4.0；底层数据许可见 task。', 'https://github.com/Jevals/jevals-data/tree/21bb47b72814cf661539b313844d2d2e26166e54'),
 ('nimble', 'Nimble', '固定公共评测集的13个子集，展示官方转换后的原始评测输入与人工标签。', 'https://github.com/bespokelabsai/nimble/tree/dcfdbd9a64f0d869f658d7a72f1beaee32737773'),
 ('eikos', 'Eikos 评测套件', '公开 builder 生成或从公开数据转换的评测题；不是四十二套独立原创数据。保留42任务，排除重复的JevBench副本。', 'https://github.com/caiovicentino/eikos/tree/8902fbe9e06e10da50d3ed5d27bb52fcf8ddd900')]
for bench, title, note, url in configs:
    groups = defaultdict(list)
    hashes = {}
    if bench == 'jevals':
        for path in sorted((source/bench).glob('*.json')):
            d = json.loads(path.read_text())
            task = d['task']
            for item in d['items']:
                groups[path.stem].append({'id':item['item_id'], 'state':item['state'], 'question':task, 'gold':item['target'], 'raw':item})
            hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    else:
        paths = sorted((source/bench).glob('*/all.jsonl')) if bench == 'nimble' else sorted((source/bench).glob('*.jsonl'))
        for path in paths:
            if path.stem == 'suite_jb_public':
                continue
            hashes[str(path.relative_to(source/bench))] = hashlib.sha256(path.read_bytes()).hexdigest()
            for line in path.read_text().splitlines():
                d = json.loads(line)
                if bench == 'nimble':
                    subset = path.parent.name
                    state, question, gold = d['input']['state'], d['input']['questions'], d['reference']
                else:
                    subset = d.get('task') or d['id'].split('-')[0]
                    state, question, gold = d['state'], d['question'], d['expected']
                groups[subset].append({'id':d['id'], 'state':state, 'question':question, 'gold':gold, 'raw':d})
    info = {'id':bench, 'name':title, 'note':note, 'source':url, 'subsets':[], 'source_sha256':hashes}
    for subset, rows in sorted(groups.items()):
        assert len({r['id'] for r in rows}) == len(rows)
        # Raw records retain the complete original fields; the viewer derives columns.
        records = [r['raw'] for r in rows]
        payload = {'benchmark':bench, 'subset':subset, 'rows':records}
        if bench == 'jevals':
            payload['task'] = rows[0]['question']
        filename = f'{bench}--{subset}.json'
        (output/filename).write_text(json.dumps(payload, ensure_ascii=False, separators=(',',':')))
        info['subsets'].append({'id':subset, 'count':len(rows), 'file':filename})
    if bench == 'eikos':
        info['upstream_manifest'] = json.loads((source/bench/'manifest.json').read_text())
    info['count'] = sum(s['count'] for s in info['subsets'])
    manifest['benchmarks'].append(info)
(output/'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
print([(b['name'], b['count'], len(b['subsets'])) for b in manifest['benchmarks']])
