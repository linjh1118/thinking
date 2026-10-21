"""Check per-repository links for multi-card archived model families."""
import json
import tempfile
import unittest
from pathlib import Path

import build_base_model_atlas as atlas


class ManifestLinkTests(unittest.TestCase):
    def test_sibling_card_uses_its_own_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'Sibling.md'
            source.write_text('# Sibling\n\n[License](LICENSE)\n\n![Chart](assets/chart.png)\n')
            documents = {
                'hf_model_card.md': {'url': 'https://huggingface.co/org/Main/resolve/main/README.md'},
                'Sibling.md': {'url': 'https://huggingface.co/org/Sibling/resolve/main/README.md'},
            }
            (root / 'retrieval_manifest.json').write_text(json.dumps({'documents': documents}))
            output = root / 'Sibling.html'
            atlas.render_markdown(source, output, {})
            rendered = output.read_text()
            self.assertIn('https://huggingface.co/org/Sibling/blob/main/LICENSE', rendered)
            self.assertIn('https://huggingface.co/org/Sibling/resolve/main/assets/chart.png', rendered)
            self.assertNotIn('https://huggingface.co/org/Main/', rendered)

    def test_non_card_does_not_inherit_primary_repository(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / 'Local.md'
            source.write_text('# Local\n\n[Other note](Other.md)\n')
            (root / 'retrieval_manifest.json').write_text(json.dumps({'documents': {
                'hf_model_card.md': {'url': 'https://huggingface.co/org/Main/raw/main/README.md'},
            }}))
            output = root / 'Local.html'
            atlas.render_markdown(source, output, {})
            self.assertIn('href="Other.md.html"', output.read_text())
            self.assertNotIn('https://huggingface.co/org/Main/', output.read_text())


if __name__ == '__main__':
    unittest.main()
