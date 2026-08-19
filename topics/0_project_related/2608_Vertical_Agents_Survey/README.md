# Vertical Agents Survey: Interactive Companion

This is a dependency-free static companion to the survey. The browser reads the three CSV inventories in `data/` and exposes full-text search, type chips, advanced domain/scope/evidence filters, expandable source cards, and progressive loading.

## Local preview

Serve the directory through any static web server so the browser can load the CSV files:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. Opening `index.html` directly through the `file://` protocol may cause browsers to block CSV loading.

## Publishing contract

- Copy the final paper to `vertical_agents_survey.pdf` in this directory to activate the download links.
- Keep the four shared research figures in `assets/overview.png`, `assets/mindmap.png`, `assets/synthesis.png`, and `assets/harness.png`; each figure supports zoom and direct download.
- Keep `assets/og.png` at 1731×909 for Open Graph and X link previews.
- The page uses no CDN, third-party font, external JavaScript, or external CSS dependency.
- When the survey inventory changes, update `data/benchmarks.csv`, `data/datasets.csv`, and `data/harnesses.csv` together.
- All public-facing content is English; the separate Feishu interpretation document is the only Chinese artifact.
