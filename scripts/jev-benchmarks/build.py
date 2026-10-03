#!/usr/bin/env python3
"""Build the offline Jev benchmark dashboard from reviewed public result data.

Input: jev-benchmark-data/data.json and this directory's template.html.
Output: repository-root jev_benchmarks.html.
Usage: python3 scripts/jev-benchmarks/build.py
No network requests, model calls, or publishing are performed.
"""
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
data = json.loads((ROOT / 'jev-benchmark-data/data.json').read_text())
assert len({b['id'] for b in data['boards']}) == len(data['boards'])
assert all(b['rows'] for b in data['boards'])
source_ids = {s['id'] for s in data['sources']}
boards_by_id = {board['id']: board for board in data['boards']}
for catalog in data['catalog']:
    assert catalog['source'] in source_ids, catalog['id']
    for board_id in catalog['boards']:
        assert boards_by_id[board_id]['source'] == catalog['source'], board_id
for board in data['boards']:
    assert board['source'] in source_ids, board['id']
    keys = {metric['key'] for metric in board['metrics']}
    assert len(keys) == len(board['metrics']), board['id']
    assert len({row['model'] for row in board['rows']}) == len(board['rows']), board['id']
    assert all(metric['direction'] in ('asc', 'desc') for metric in board['metrics'])
    for row in board['rows']:
        assert keys.issubset(row['metrics']), (board['id'], row['model'])
        assert all(value is None or (type(value) in (int, float) and math.isfinite(value))
                   for value in row['metrics'].values())
serialized = json.dumps(data, ensure_ascii=False, separators=(',', ':'), allow_nan=False)
serialized = serialized.replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
template = Path(__file__).with_name('template.html').read_text()
assert template.count('__DASHBOARD_DATA__') == 1
out = template.replace('__DASHBOARD_DATA__', serialized)
(ROOT / 'jev_benchmarks.html').write_text(out)
print(f"Built {len(data['boards'])} boards / {sum(len(b['rows']) for b in data['boards'])} rows; {len(out.encode()):,} bytes")
