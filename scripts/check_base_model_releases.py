"""Fetch read-only first-party evidence for an Atlas release-watch run.

Input: vault release_watch.json and the preceding evidence directory.
Output: dated HF inventories, collections and official-page snapshots plus a
manifest; it never edits notes, sets all-team success, or publishes the site.
Repository creation dates are candidate signals, not model release dates.

Example:
  python3 scripts/check_base_model_releases.py --previous \
    /Users/omegalin/Documents/github/BrainHao/Topics/13_base_model/src/release_watch_evidence/2026-10-13/evening
"""
import argparse
import concurrent.futures
import hashlib
import gzip
import json
import urllib.parse
import urllib.request
from datetime import datetime, timedelta
from html.parser import HTMLParser
from pathlib import Path
from zoneinfo import ZoneInfo

TOPIC = Path('/Users/omegalin/Documents/github/BrainHao/Topics/13_base_model')
OFFICIAL_PAGES = {
    'deepseek': 'https://api-docs.deepseek.com/updates/',
    'zhipu': 'https://z.ai/blog',
    'kimi': 'https://www.kimi.com/en/blog/',
    'qwen': 'https://qwen.ai/research',
    'seed': 'https://seed.bytedance.com/zh/research',
    'minimax': 'https://www.minimax.io/news',
    'mimo': 'https://mimo.mi.com/docs/en-US/updates/model',
    'longcat': 'https://longcat.chat/platform/docs/zh/ChangeLog.html',
    'stepfun': 'https://www.stepfun.com/news',
    'baidu': 'https://yiyan.baidu.com/blog',
    'hunyuan': 'https://hunyuan.tencent.com/research',
    'ernie_extra': 'https://www.miromind.ai/blog',
    'openai': 'https://openai.com/news/research/',
    'anthropic': 'https://www.anthropic.com/news',
    'google': 'https://deepmind.google/models/model-cards/',
    'meta': 'https://ai.meta.com/blog/',
    'xai': 'https://x.ai/news',
    'mistral': 'https://mistral.ai/news/',
    'microsoft': 'https://www.microsoft.com/en-us/research/blog/',
    'amazon': 'https://www.amazon.science/blog',
    'nvidia': 'https://research.nvidia.com/publications',
    'cohere': 'https://cohere.com/blog',
    'ibm': 'https://www.ibm.com/granite/docs/changelog',
}

# HF inventories miss closed-source releases, and legacy entry pages can lag
# behind a team's current research or service-release channel. Snapshot these
# additional first-party directories; a human still verifies first-release dates
# and excludes provider onboarding, API changes, and repeated family SKUs.
ADDITIONAL_PAGES = {
    'meta-current': ('meta', 'https://research.meta.ai/'),
    'zhipu-autoclaw': ('zhipu', 'https://autoclaw.z.ai/blog/'),
    'qwen-model-studio': ('qwen', 'https://help.aliyun.com/zh/model-studio/newly-released-models'),
}


class VisibleText(HTMLParser):
    """Extract static text without executing downloaded scripts."""
    def __init__(self):
        super().__init__()
        self.hidden = 0
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag in {'script', 'style'}:
            self.hidden += 1

    def handle_endtag(self, tag):
        if tag in {'script', 'style'}:
            self.hidden = max(0, self.hidden - 1)

    def handle_data(self, data):
        if not self.hidden and data.strip():
            self.parts.append(data.strip())


def fetch_job(job, output, previous, window_start):
    key, url, suffix, kind, team = job
    result = {'key': key, 'team': team, 'kind': kind, 'url': url,
              'checkedAt': datetime.now(ZoneInfo('Asia/Shanghai')).isoformat(timespec='seconds')}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Atlas release evidence'})
        with urllib.request.urlopen(request, timeout=25) as response:
            content_type = response.headers.get('Content-Type', '')
            if 'pdf' in content_type.lower():
                raise ValueError('PDF response is link-only; not downloaded')
            data = response.read()
            if data.startswith(b'\x1f\x8b'):
                data = gzip.decompress(data)
            result.update(status='fetched', finalUrl=response.geturl(), contentType=content_type,
                          bytes=len(data), sha256=hashlib.sha256(data).hexdigest())
        (output / (key + suffix)).write_bytes(data)
        prior = previous / (key + suffix)
        if kind == 'inventory':
            rows = json.loads(data)
            old = json.loads(prior.read_text()) if prior.exists() else []
            old_ids = {row['id'] for row in old}
            result['newRepositories'] = [row['id'] for row in rows if row['id'] not in old_ids]
            result['recentCandidates'] = [row['id'] for row in rows if row.get('createdAt', '') >= window_start]
        elif kind == 'page':
            parser = VisibleText()
            parser.feed(data.decode(errors='replace'))
            visible = '\n'.join(parser.parts)
            (output / (key + '.txt')).write_text(visible)
            result['staticTextCharacters'] = len(visible)
            if prior.exists():
                old_parser = VisibleText()
                old_parser.feed(prior.read_text(errors='replace'))
                result['staticTextChanged'] = parser.parts != old_parser.parts
        return result
    except Exception as error:
        result.update(status='failed', error=str(error))
        return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--previous', type=Path, required=True)
    args = parser.parse_args()
    now = datetime.now(ZoneInfo('Asia/Shanghai'))
    state = json.loads((TOPIC / 'src/release_watch.json').read_text())
    start = (now.date() - timedelta(days=29)).isoformat()
    output = TOPIC / 'src/release_watch_evidence' / now.strftime('%Y-%m-%d') / now.strftime('%H%M')
    output.mkdir(parents=True, exist_ok=False)
    jobs = []
    for team in state['checkedTeams']:
        org = team['hfOrg']
        query = urllib.parse.urlencode({'author': org, 'sort': 'createdAt', 'direction': -1, 'limit': 100})
        jobs.append((org, 'https://huggingface.co/api/models?' + query, '.json', 'inventory', team['team']))
        jobs.append(('collections-' + org, 'https://huggingface.co/api/collections?' + urllib.parse.urlencode({'owner': org}),
                     '.json', 'collections', team['team']))
        jobs.append(('blog-' + team['team'], OFFICIAL_PAGES[team['team']], '.html', 'page', team['team']))
    for key, (team, url) in ADDITIONAL_PAGES.items():
        jobs.append(('blog-' + key, url, '.html', 'page', team))
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda job: fetch_job(job, output, args.previous, start), jobs))
    manifest = {'windowStart': start, 'windowEnd': now.date().isoformat(), 'previous': str(args.previous),
                'checkedAt': now.isoformat(timespec='seconds'), 'results': results}
    (output / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'evidence': str(output), 'newRepositories': {row['team']: row.get('newRepositories')
        for row in results if row.get('newRepositories')}, 'pageChanges': [row['team'] for row in results
        if row.get('staticTextChanged')], 'failures': [{'key':row['key'],'error':row['error']}
        for row in results if row['status'] == 'failed']}, ensure_ascii=False))


if __name__ == '__main__':
    main()
