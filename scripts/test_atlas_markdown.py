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
