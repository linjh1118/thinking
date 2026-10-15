"""Regression tests for nested inline Markdown in archived model cards.

Run: python3 -m unittest discover -s scripts -p test_atlas_markdown.py
"""
import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

import build_base_model_atlas as atlas
from build_base_model_atlas import render_inline_md


class InlineMarkdownTests(unittest.TestCase):
    def test_poster_keeps_generated_note_and_vault_backlink(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / 'source'
            root.mkdir()
            (root / 'Note.md').write_text('# Model note')
            poster = root / 'poster.html'
            poster.write_text('<a href="Note.html">渲染笔记</a><a href="obsidian://open?vault=BrainHao">源笔记</a><a href="missing.html">Legacy missing</a>')
            destination = Path(directory) / 'published/poster.html'
            atlas.copy_file_with_refs(poster, destination, root)
            rendered = destination.read_text()
            self.assertIn('href="Note.html"', rendered)
            self.assertIn('href="obsidian://open?vault=BrainHao"', rendered)
            self.assertIn('href="#">Legacy missing', rendered)

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
