"""Regression tests for nested inline Markdown in archived model cards.

Run: python3 -m unittest discover -s scripts -p test_atlas_markdown.py
"""
import unittest
import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import build_base_model_atlas as atlas
from build_base_model_atlas import render_inline_md


class InlineMarkdownTests(unittest.TestCase):
    def test_native_card_tables_keep_merged_cells_and_strip_executable_html(self):
        raw = '<table onclick="bad()"><tr><th colspan="2">Result</th></tr><tr><td rowspan="2" style="color:red">9.49</td><td><b>Offline</b><script>alert(1)</script></td></tr></table>'
        clean = atlas.sanitize_card_table(raw)
        self.assertIn('colspan="2"', clean)
        self.assertIn('rowspan="2"', clean)
        self.assertIn('<b>Offline</b>', clean)
        for unsafe in ['onclick', 'style=', 'alert(1)', '<script']:
            self.assertNotIn(unsafe, clean)
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / 'card.md'
            destination = Path(directory) / 'card.html'
            source.write_text('# Card\n\nIntro\n' + raw + '\n\n```html\n<table><tr><td>Literal</td></tr></table>\n```\n')
            atlas.render_markdown(source, destination, {})
            rendered = destination.read_text()
            self.assertIn('<div class="table-wrap"><table>', rendered)
            self.assertIn('&lt;table&gt;&lt;tr&gt;&lt;td&gt;Literal', rendered)

    def test_hf_html_headings_code_links_and_video_are_readable(self):
        raw = ('<h1 align="center">Model Title</h1>\n'
               '<p>BF16 · <code>Pipeline</code></p>\n'
               '<a href="https://example.com/report"><img alt="Report" src="badge.png"/></a>\n'
               '<video src="https://example.com/demo.mp4" controls></video>')
        normalized = atlas.normalize_card_html(raw)
        self.assertIn('# Model Title', normalized)
        self.assertIn('`Pipeline`', normalized)
        self.assertIn('[Report](https://example.com/report)', normalized)
        self.assertIn('[▶ 官方演示视频](https://example.com/demo.mp4)', normalized)
        self.assertNotIn('<video', normalized)

    def test_hf_html_normalization_preserves_fenced_code(self):
        code = '```html\n<h1>Literal heading</h1>\n<code>literal</code>\n```'
        self.assertEqual(atlas.normalize_card_html(code), code)

    def test_hf_mailto_does_not_become_a_repository_file(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'hf_model_card.md'
            source.write_text('[Contact](mailto:team@example.com)\n')
            (root / 'retrieval_manifest.json').write_text(json.dumps({'documents': {
                source.name: {'url': 'https://huggingface.co/org/Model/resolve/main/README.md'}
            }}))
            published = root / 'card.html'
            atlas.render_markdown(source, published, {})
            self.assertIn('href="mailto:team@example.com"', published.read_text())
            self.assertNotIn('/blob/main/mailto:', published.read_text())

    def test_family_update_keeps_first_release_and_stable_leaf(self):
        record = {'slug':'family','date':'2026-09-10','name':'Family','releaseUpdates':[
            {'slug':'family','date':'2026-10-17','name':'Family-1017','summary':'Minor update'}
        ]}
        rows = atlas.recent_release_rows([record])
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]['date'], '2026-09-10')
        self.assertEqual(rows[1]['slug'], 'family')
        self.assertEqual(rows[1]['date'], '2026-10-17')
        self.assertIn('非新正代', rows[1]['lineageLabel'])
        self.assertEqual(record['date'], '2026-09-10')

    def test_family_updates_are_deduplicated_and_hidden_families_stay_hidden(self):
        update = {'date':'2026-10-17','name':'Family-1017'}
        record = {'slug':'family','date':'2026-09-10','releaseUpdates':[update, update]}
        self.assertEqual(len(atlas.recent_release_rows([record])), 2)
        record['timelineVisible'] = False
        self.assertEqual(atlas.recent_release_rows([record]), [])

    def test_archived_card_preserves_renderer_navigation(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'vault/Model/src/card.md'
            source.parent.mkdir(parents=True)
            source.write_text('Original README')
            published_root = root / 'atlas'
            published = published_root / 'library/team/model/src/card.md.html'
            published.parent.mkdir(parents=True)
            (published_root / 'library.html').write_text('Library')
            published.write_text('<a href="../../../../library.html">← 资料馆</a><a href="LICENSE">License</a>')
            with patch.object(atlas, 'ATLAS', published_root):
                atlas.resolve_archived_card_links(source, published, 'https://huggingface.co/org/Model/resolve/main/README.md')
            rendered = published.read_text()
            self.assertIn('href="../../../../library.html"', rendered)
            self.assertIn('https://huggingface.co/org/Model/blob/main/LICENSE', rendered)
            self.assertNotIn('https://huggingface.co/library.html', rendered)

    def test_note_display_math_loads_renderer_only_when_needed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'Note.md'
            destination = root / 'Note.html'
            source.write_text('# Note\n\n$$P(t)=1.$$\n')
            atlas.render_markdown(source, destination, {})
            self.assertIn('tex-svg.js', destination.read_text())
            self.assertIn('$$P(t)=1.$$', destination.read_text())
            source.write_text('# Note\n\nNo formula.\n')
            atlas.render_markdown(source, destination, {})
            self.assertNotIn('tex-svg.js', destination.read_text())

    def test_repository_readme_fragment_points_to_original_markdown(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'card.md'
            source.write_text('Unmodified README')
            published = root / 'card.md.html'
            published.write_text('<a href="docs/TRAINING.md.html#fine-tuning">Train</a>')
            atlas.resolve_archived_card_links(
                source, published, 'https://raw.githubusercontent.com/NVlabs/GEM-X/main/README.md')
            self.assertIn('https://github.com/NVlabs/GEM-X/blob/main/docs/TRAINING.md#fine-tuning',
                          published.read_text())
            self.assertNotIn('.md.html#', published.read_text())
            self.assertEqual(source.read_text(), 'Unmodified README')

    def test_github_archive_resolves_remote_links_without_changing_raw(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'official-repository.md'
            source.write_text('Original README')
            published = root / 'official-repository.md.html'
            published.write_text('<img src="assets/demo.png"><a href="CHANGELOG.md.html">Changes</a><a href="LICENSE">License</a>')
            atlas.resolve_archived_card_links(source, published, 'https://raw.githubusercontent.com/nv-tlabs/kimodo/main/README.md')
            rendered = published.read_text()
            self.assertIn('https://raw.githubusercontent.com/nv-tlabs/kimodo/main/assets/demo.png', rendered)
            self.assertIn('https://github.com/nv-tlabs/kimodo/blob/main/CHANGELOG.md', rendered)
            self.assertIn('https://github.com/nv-tlabs/kimodo/blob/main/LICENSE', rendered)
            self.assertEqual(source.read_text(), 'Original README')

    def test_model_local_source_wikilink_resolves_to_rendered_card(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); (root/'src').mkdir()
            (root/'src/Model-card.md.html').write_text('Card')
            rendered=render_inline_md('[[src/Model-card|原始MD]]',root/'Note.html',{})
            self.assertIn('href="src/Model-card.md.html"',rendered)

    def test_archived_card_links_keep_raw_card_but_resolve_repository_base(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            source=root/'Model-model-card.md'; source.write_text('Original README')
            (root/'assets').mkdir(); (root/'assets/chart.png').write_bytes(b'image')
            published=root/'Model-model-card.md.html'
            published.write_text('<img src="figures/chart.png"><a href="Guide.md.html">Guide</a>')
            atlas.resolve_archived_card_links(source,published,'https://huggingface.co/org/Model/resolve/main/README.md')
            result=published.read_text()
            self.assertIn('src="assets/chart.png"',result)
            self.assertIn('https://huggingface.co/org/Model/blob/main/Guide.md',result)
            self.assertEqual(source.read_text(),'Original README')

    def test_poster_keeps_generated_note_and_vault_backlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            root.mkdir()
            (root / 'Note.md').write_text('# Model note')
            poster = root / 'poster.html'
            poster.write_text('<a href="Note.html">渲染笔记</a><a href="obsidian://open?vault=BrainHao">源笔记</a><a href="missing.html">Legacy missing</a>')
            os.utime(poster, (1, 1))
            destination = Path(directory) / 'published/poster.html'
            atlas.copy_file_with_refs(poster, destination, root)
            rendered = destination.read_text()
            self.assertIn('href="Note.html"', rendered)
            self.assertIn('href="obsidian://open?vault=BrainHao"', rendered)
            self.assertIn('href="#">Legacy missing', rendered)
            self.assertGreater(destination.stat().st_mtime, poster.stat().st_mtime)

    def test_shorter_authored_poster_replaces_previous_version(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            root.mkdir()
            poster = root / 'poster.html'
            poster.write_text('<h1>Updated, concise poster</h1>')
            library = Path(directory) / 'library'
            destination = library / 'test/test-model/poster.html'
            destination.parent.mkdir(parents=True)
            destination.write_text('<h1>Old authored poster with much longer obsolete content</h1>')
            record = {'team': 'test', 'slug': 'test-model', '_assets': {'dir': root, 'posters': [poster]}}
            with patch.object(atlas, 'LIBRARY', library), patch.object(atlas, 'ATLAS', Path(directory)):
                atlas.sync_library([record], {})
            self.assertEqual(destination.read_text(), poster.read_text())

    def test_fallback_does_not_replace_authored_poster(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            root.mkdir()
            poster = root / 'poster.html'
            poster.write_text('Base Model Atlas 补齐页')
            library = Path(directory) / 'library'
            destination = library / 'test/test-model/poster.html'
            destination.parent.mkdir(parents=True)
            destination.write_text('<h1>Authored poster</h1>')
            record = {'team': 'test', 'slug': 'test-model', '_assets': {'dir': root, 'posters': [poster]}}
            with patch.object(atlas, 'LIBRARY', library), patch.object(atlas, 'ATLAS', Path(directory)):
                atlas.sync_library([record], {})
            self.assertEqual(destination.read_text(), '<h1>Authored poster</h1>')

    def test_explicit_release_slug_preserves_plus_generation(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory)
            (source / 'src').mkdir()
            release = {
                'team': 'cohere', 'name': 'Command A+',
                'slug': 'cohere-command-a-plus', 'folder': 'Cohere/260520_A_Plus',
                'date': '2026-05-20', 'lineageType': 'mainline',
                'label': '主干正代', 'summary': 'Distinct generation',
                'sources': [{'label': 'Tech Blog', 'url': 'https://cohere.com/blog/command-a-plus'}],
            }
            (source / 'src/verified_releases.json').write_text(json.dumps([release]))
            team = {
                'id': 'cohere', 'name': 'Cohere', 'dir': 'Cohere',
                'region': '海外', 'color': '#abc', 'thesis': 'Enterprise',
                'models': [('2503', 'Command A', 'Original', 'https://cohere.com/')],
            }
            with patch.object(atlas, 'SOURCE', source), patch.object(atlas, 'TEAMS', [team]), patch.object(atlas, 'PINNED_TIMELINE_VARIANTS', {}), patch.object(atlas, 'BRANCH_MODEL_NODES', {}):
                _, records = atlas.build_records()
            self.assertEqual({r['slug'] for r in records}, {'cohere-command-a', 'cohere-command-a-plus'})

    def test_inline_code_in_external_link(self):
        rendered = render_inline_md(
            '[`model-name`](https://huggingface.co/org/model)', Path('/tmp/note.html'), {}
        )
        self.assertIn('<code>model-name</code></a>', rendered)
        self.assertNotIn('\x00', rendered)

    def test_inline_code_in_local_link(self):
        rendered = render_inline_md('[`README`](src/card.md)', Path('/tmp/note.html'), {})
        self.assertEqual(rendered, '<a href="src/card.md.html"><code>README</code></a>')

    def test_code_does_not_turn_into_markdown(self):
        rendered = render_inline_md('`**literal**` and **bold**', Path('/tmp/note.html'), {})
        self.assertEqual(rendered, '<code>**literal**</code> and <strong>bold</strong>')

    def test_published_poster_wikilink_uses_library_not_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            vault = Path(directory) / 'vault'
            source = vault / 'Topics/13_base_model'
            model = source / 'Team/2610_Model'
            model.mkdir(parents=True)
            (model / 'model_poster_zh.html').write_text('<html></html>')
            published = Path(directory) / 'atlas'
            poster = published / 'library/team/model/model_poster_zh.html'
            poster.parent.mkdir(parents=True)
            poster.write_text('<html></html>')
            (published / 'models.json').write_text(json.dumps([{
                'posters': ['library/team/model/model_poster_zh.html']
            }]))
            with patch.object(atlas, 'SOURCE', source), patch.object(atlas, 'BRAINHAO', vault), patch.object(atlas, 'ATLAS', published):
                targets = atlas.note_targets()
            key = 'Topics/13_base_model/Team/2610_Model/model_poster_zh.html'
            self.assertEqual(targets[key], poster)


if __name__ == '__main__':
    unittest.main()
