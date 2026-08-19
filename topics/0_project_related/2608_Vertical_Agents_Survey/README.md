# Vertical Agents Survey: Interactive Companion

This is a dependency-free static companion to the survey. The browser reads the three CSV inventories in `data/` and exposes full-text search plus filters for resource type, domain, scope class, and evidence level.

## Local preview

Serve the directory through any static web server so the browser can load the CSV files:

```bash
python3 -m http.server 8000
```

Then open `http://localhost:8000/`. Opening `index.html` directly through the `file://` protocol may cause browsers to block CSV loading.

## Publishing contract

- Copy the final paper to `vertical_agents_survey.pdf` in this directory to activate the download links.
- The page uses no CDN, third-party font, external JavaScript, or external CSS dependency.
- When the survey inventory changes, update `data/benchmarks.csv`, `data/datasets.csv`, and `data/harnesses.csv` together.
- All public-facing content is English; the separate Feishu interpretation document is the only Chinese artifact.
