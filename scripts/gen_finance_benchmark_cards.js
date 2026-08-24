#!/usr/bin/env node

const fs = require('fs');
const path = require('path');

const input = process.argv[2];
const output = process.argv[3] || 'finance_economy_benchmark_atlas.html';
if (!input) {
  console.error('Usage: node scripts/gen_finance_benchmark_cards.js <benchmark_papers.md> [output.html]');
  process.exit(1);
}

const resources = {
  1: ['HF Dataset Preview', 'https://huggingface.co/datasets/BUPT-Reasoning-Lab/FinMMDocR', 'hf'],
  2: ['Repo Preview', 'https://github.com/ant-research/FinMathBench', 'repo'],
  3: ['HF Dataset Preview', 'https://huggingface.co/datasets/jinsong8/FinRpt', 'hf'],
  4: ['Repo Preview', 'https://github.com/HuuuNan/TaxReasoning', 'repo'],
  7: ['Repo Preview', 'https://github.com/hedyHe/FinED-Bench', 'repo'],
  9: ['Repo Preview', 'https://github.com/sarmistha-D/FIND_FinVQA', 'repo'],
  10: ['HF Dataset Preview', 'https://huggingface.co/datasets/AI-TAX/factual-state-discovery-benchmark', 'hf'],
  12: ['Repo Preview', 'https://github.com/mbzuai-nlp/finchain', 'repo'],
  13: ['HF Dataset Preview', 'https://huggingface.co/datasets/Tizzzzy/FinChart-Bench', 'hf'],
  14: ['Repo Preview', 'https://github.com/ujin0415/FinHarmBench', 'repo'],
  15: ['Repo Preview', 'https://github.com/sqyangit/FinMRAGBench', 'repo'],
  17: ['Repo Preview', 'https://github.com/sustech-nlp/FinSafetyBench', 'repo'],
  19: ['Repo Preview', 'https://github.com/FinWorkBench/Finch', 'repo'],
  23: ['HF Dataset Preview', 'https://huggingface.co/datasets/TheFinAI/MultiFinBen_OCR_Task', 'hf'],
  24: ['Repo Preview', 'https://github.com/insait-institute/RealFin', 'repo'],
  25: ['HF Dataset Preview', 'https://huggingface.co/datasets/SahmBenchmark/Islamic_Finance_QnA_eval', 'hf'],
  27: ['Repo Preview', 'https://github.com/Yating-Chen/TaxPraBen', 'repo'],
  29: ['HF Dataset Preview', 'https://huggingface.co/datasets/SakanaAI/EDINET-Bench', 'hf'],
  30: ['HF Dataset Preview', 'https://huggingface.co/datasets/ByteSeedXpert/FinSearchComp', 'hf'],
  32: ['HF Dataset Preview', 'https://huggingface.co/datasets/HiThink-Research/BizFinBench.v2', 'hf'],
  35: ['HF Dataset Preview', 'https://huggingface.co/datasets/HYU-NLP/FCMR', 'hf'],
  36: ['HF Dataset Preview', 'https://huggingface.co/datasets/BUPT-Reasoning-Lab/FinanceReasoning', 'hf'],
  37: ['Repo Preview', 'https://github.com/JaeyoungChoe/LOFin-bench-HiREC', 'repo'],
  40: ['HF Dataset Preview', 'https://huggingface.co/datasets/Zhihan/XFinBench', 'hf'],
  41: ['HF Dataset Preview', 'https://huggingface.co/datasets/Dragongon/FinLFQA', 'hf'],
  42: ['HF Dataset Preview', 'https://huggingface.co/datasets/bowang0911/FinMTEBFinQAChunkRetrieval', 'hf'],
  43: ['HF Dataset Preview', 'https://huggingface.co/datasets/zhaosuifeng/FinRAGBench-V', 'hf'],
  44: ['HF Dataset Preview', 'https://huggingface.co/datasets/HughieHu/FinTrust', 'hf'],
  45: ['HF Dataset Preview', 'https://huggingface.co/datasets/IDEA-FinAI/Golden-Touchstone', 'hf'],
  47: ['HF Dataset Preview', 'https://huggingface.co/datasets/SUFE-AIFLM-Lab/VisFinEval', 'hf'],
  48: ['HF Dataset Preview', 'https://huggingface.co/datasets/BUPT-Reasoning-Lab/FinMMR', 'hf'],
  49: ['HF Dataset Preview', 'https://huggingface.co/datasets/FDU-INS/INS-MMBench', 'hf'],
  50: ['Repo Preview', 'https://github.com/peernagy/lob_bench', 'repo'],
  52: ['HF Dataset Preview', 'https://huggingface.co/datasets/SUFE-AIFLM-Lab/FinEval', 'hf'],
  55: ['HF Dataset Preview', 'https://huggingface.co/datasets/TobyYang7/UCFE', 'hf'],
  56: ['Repo Preview', 'https://github.com/aliyun/cflue', 'repo'],
  57: ['HF Dataset Preview', 'https://huggingface.co/datasets/kensho/bizbench', 'hf'],
  58: ['Repo Preview', 'https://github.com/UBC-NLP/fintral', 'repo'],
  60: ['HF Dataset Preview', 'https://huggingface.co/datasets/yinzhu-quan/econ_logic_qa', 'hf']
};

const escapeHtml = (value = '') => String(value)
  .replaceAll('&', '&amp;').replaceAll('<', '&lt;').replaceAll('>', '&gt;')
  .replaceAll('"', '&quot;').replaceAll("'", '&#039;');

const cleanInline = (value = '') => value
  .replace(/\*\*(.*?)\*\*/g, '$1')
  .replace(/`(.*?)`/g, '$1')
  .replace(/\\textbf\{([^}]+)\}/g, '$1')
  .replace(/\s+/g, ' ')
  .trim();

const raw = fs.readFileSync(input, 'utf8');
const entries = [];
for (const section of raw.split(/\n---\n/)) {
  const heading = section.match(/^## (\d+)\. (.+)$/m);
  if (!heading) continue;
  const number = Number(heading[1]);
  const title = cleanInline(heading[2]);
  const body = section.slice(heading.index + heading[0].length);
  const get = (label) => cleanInline((body.match(new RegExp(`^- \\*\\*${label}\\*\\*：(.+)$`, 'm')) || [,''])[1]);
  const ym = get('年份 / 会议').match(/^(\d{4})\s*\/\s*(.+)$/);
  const paperMatch = body.match(/^- \*\*论文链接\*\*：\[([^\]]+)\]\(([^)]+)\)/m);
  const tldr = cleanInline((body.match(/^\*\*TL;DR\*\*：([\s\S]+)$/m) || [,''])[1]);
  const r = resources[number];
  entries.push({
    number, title,
    year: ym ? ym[1] : '',
    venue: ym ? ym[2] : '',
    domain: get('领域'),
    reason: get('收录原因'),
    benchmark: get('Benchmark 判定'),
    verification: get('链接验证'),
    paperLabel: paperMatch ? paperMatch[1] : '论文',
    paperUrl: paperMatch ? paperMatch[2] : '#',
    tldr,
    resource: r ? {label: r[0], url: r[1], type: r[2]} : null
  });
}

const venues = [...new Set(entries.map(e => e.venue))].sort();
const years = [...new Set(entries.map(e => e.year))].sort((a, b) => b.localeCompare(a));
const resourceCount = entries.filter(e => e.resource).length;
const hfCount = entries.filter(e => e.resource?.type === 'hf').length;
const repoCount = entries.filter(e => e.resource?.type === 'repo').length;

const cards = entries.map(e => {
  const searchable = escapeHtml([e.number, e.title, e.year, e.venue, e.domain, e.benchmark, e.tldr].join(' ').toLowerCase());
  const resource = e.resource
    ? `<a class="action resource ${e.resource.type}" href="${escapeHtml(e.resource.url)}" target="_blank" rel="noopener noreferrer"><span>${e.resource.type === 'hf' ? '🤗' : '⌘'}</span>${escapeHtml(e.resource.label)}<span aria-hidden="true">↗</span></a>`
    : `<span class="action unavailable" title="未检索到可核验的公开数据或代码入口">暂无公开 Preview</span>`;
  return `
    <article class="bench-card" id="bench-${e.number}" data-year="${e.year}" data-venue="${escapeHtml(e.venue)}" data-domain="${escapeHtml(e.domain)}" data-resource="${e.resource ? 'yes' : 'no'}" data-search="${searchable}">
      <div class="card-topline">
        <span class="index">${String(e.number).padStart(2, '0')}</span>
        <div class="badges"><span class="badge domain-${e.domain.toLowerCase()}">${escapeHtml(e.domain)}</span><span class="badge">${e.year}</span><span class="badge venue">${escapeHtml(e.venue)}</span></div>
      </div>
      <h2>${escapeHtml(e.title)}</h2>
      <p class="tldr">${escapeHtml(e.tldr)}</p>
      <details>
        <summary>为什么它算 benchmark</summary>
        <p>${escapeHtml(e.benchmark)}</p>
        <p class="reason">${escapeHtml(e.reason)}</p>
      </details>
      <div class="card-actions">
        <a class="action paper" href="${escapeHtml(e.paperUrl)}" target="_blank" rel="noopener noreferrer">论文 · ${escapeHtml(e.paperLabel)}<span aria-hidden="true">↗</span></a>
        ${resource}
      </div>
    </article>`;
}).join('');

const options = (items) => items.map(x => `<option value="${escapeHtml(x)}">${escapeHtml(x)}</option>`).join('');
const generated = new Date().toISOString().slice(0, 10);

const html = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="62 个 Finance / Economy Benchmark 卡片图鉴，含论文、Hugging Face Dataset Preview 与代码仓库入口。">
  <meta name="color-scheme" content="light">
  <title>Finance × Economy Benchmark Atlas · 62 Cards</title>
  <!-- index: Finance × Economy Benchmark Atlas | ${generated} | 62 个金融与经济 benchmark 的可筛选卡片图鉴，直达论文、Hugging Face Dataset Preview 与代码仓库 -->
  <style>
    :root{--ink:#10241f;--muted:#60706a;--paper:#fffef8;--soft:#f4f2e9;--line:#d9dbcf;--green:#0d7c66;--green-2:#125e51;--lime:#dff06a;--orange:#ff8a52;--blue:#4a6ee0;--shadow:0 14px 36px rgba(21,47,40,.09);--radius:22px}
    *{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--soft);color:var(--ink);font-family:Inter,"SF Pro Display","PingFang SC","Microsoft YaHei",system-ui,sans-serif;line-height:1.55}
    a{color:inherit}.wrap{width:min(1240px,calc(100% - 36px));margin:auto}.hero{position:relative;overflow:hidden;background:var(--ink);color:#fff;padding:58px 0 50px;border-bottom:6px solid var(--lime)}
    .hero:before,.hero:after{content:"";position:absolute;border-radius:999px;filter:blur(2px);opacity:.9}.hero:before{width:360px;height:360px;right:-70px;top:-190px;background:var(--orange)}.hero:after{width:260px;height:260px;right:210px;bottom:-210px;background:var(--lime)}
    .hero-grid{position:relative;z-index:1;display:grid;grid-template-columns:minmax(0,1.55fr) minmax(280px,.75fr);gap:48px;align-items:end}.eyebrow{display:inline-flex;align-items:center;gap:9px;padding:7px 12px;border:1px solid rgba(255,255,255,.28);border-radius:999px;color:#e9f3ef;font-weight:750;font-size:13px;letter-spacing:.06em;text-transform:uppercase}
    h1{font-size:clamp(42px,7vw,82px);line-height:.95;letter-spacing:-.055em;margin:20px 0 18px;max-width:850px}.hero-copy{max-width:760px;margin:0;color:#c9d7d2;font-size:clamp(16px,1.7vw,20px)}.hero-copy strong{color:var(--lime)}
    .hero-note{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);border-radius:20px;padding:20px;backdrop-filter:blur(10px)}.hero-note p{margin:0 0 12px;color:#d5e2dd;font-size:14px}.hero-note .stamp{display:flex;justify-content:space-between;gap:15px;padding-top:12px;border-top:1px solid rgba(255,255,255,.15);font-size:12px;color:#aebfba}
    .stats{position:relative;z-index:2;margin-top:-1px;background:#fff;border-bottom:1px solid var(--line)}.stat-grid{display:grid;grid-template-columns:repeat(4,1fr)}.stat{padding:22px 20px;border-right:1px solid var(--line)}.stat:last-child{border:0}.stat b{display:block;font-size:30px;letter-spacing:-.04em}.stat span{font-size:13px;color:var(--muted)}
    .toolbar-shell{position:sticky;top:0;z-index:20;background:rgba(244,242,233,.9);backdrop-filter:blur(16px);border-bottom:1px solid rgba(217,219,207,.9)}.toolbar{display:grid;grid-template-columns:minmax(250px,1.5fr) repeat(4,minmax(130px,.55fr));gap:10px;padding:14px 0}.control{width:100%;min-height:46px;border:1px solid var(--line);background:#fffefb;border-radius:13px;padding:0 13px;color:var(--ink);font:inherit;font-size:14px;outline:none}.control:focus{border-color:var(--green);box-shadow:0 0 0 3px rgba(13,124,102,.12)}.search-wrap{position:relative}.search-wrap .control{padding-left:42px}.search-icon{position:absolute;left:15px;top:50%;transform:translateY(-50%);color:var(--muted)}
    main{padding:32px 0 76px}.result-line{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:18px}.result-line strong{font-size:18px}.result-line span{color:var(--muted);font-size:13px}.cards{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:17px;align-items:stretch}.bench-card{position:relative;display:flex;flex-direction:column;min-width:0;background:var(--paper);border:1px solid var(--line);border-radius:var(--radius);padding:20px;box-shadow:0 1px 0 rgba(16,36,31,.03);transition:transform .18s ease,box-shadow .18s ease,border-color .18s ease;scroll-margin-top:90px}.bench-card:hover{transform:translateY(-3px);box-shadow:var(--shadow);border-color:#bec7bd}.bench-card.hidden{display:none}
    .card-topline{display:flex;justify-content:space-between;align-items:flex-start;gap:12px}.index{display:grid;place-items:center;width:42px;height:42px;flex:0 0 auto;border-radius:13px;background:var(--ink);color:#fff;font-variant-numeric:tabular-nums;font-weight:850;letter-spacing:.04em}.badges{display:flex;justify-content:flex-end;flex-wrap:wrap;gap:6px}.badge{border:1px solid var(--line);border-radius:999px;padding:4px 8px;background:#f7f6ef;color:var(--muted);font-size:11px;font-weight:750}.domain-finance{color:#075d4c;background:#e3f6ef;border-color:#bfe5d7}.domain-economy{color:#8a431e;background:#fff0e7;border-color:#ffd0b8}.badge.venue{color:#314a9c;background:#edf1ff;border-color:#cfd8ff}
    .bench-card h2{font-size:20px;line-height:1.22;letter-spacing:-.025em;margin:17px 0 10px;overflow-wrap:anywhere}.tldr{margin:0 0 16px;color:#46564f;font-size:14px;display:-webkit-box;-webkit-line-clamp:5;-webkit-box-orient:vertical;overflow:hidden}.bench-card details{margin:auto 0 16px;border-top:1px solid var(--line);padding-top:12px;color:var(--muted);font-size:13px}.bench-card summary{cursor:pointer;color:var(--green-2);font-weight:800;list-style:none}.bench-card summary::-webkit-details-marker{display:none}.bench-card summary:after{content:"＋";float:right}.bench-card details[open] summary:after{content:"−"}.bench-card details p{margin:10px 0 0}.bench-card details .reason{padding:9px 10px;border-radius:10px;background:#f2f5ef;color:#66746d}
    .card-actions{display:flex;flex-wrap:wrap;gap:8px;margin-top:auto}.action{display:inline-flex;align-items:center;justify-content:center;gap:6px;min-height:39px;padding:8px 11px;border-radius:11px;text-decoration:none;font-size:12px;font-weight:820;border:1px solid var(--line);transition:.15s ease}.action:hover{transform:translateY(-1px)}.action.paper{background:#fff;color:var(--ink)}.action.resource{color:#fff;background:var(--green);border-color:var(--green)}.action.resource.hf{background:#ff9f1c;border-color:#ff9f1c;color:#2b1b00}.action.unavailable{cursor:not-allowed;background:#f0efe9;color:#9a9d96;border-style:dashed;font-weight:650}
    .empty{display:none;text-align:center;padding:72px 20px;background:#fff;border:1px dashed #b9beb6;border-radius:var(--radius)}.empty.show{display:block}.empty b{display:block;font-size:24px;margin-bottom:6px}.foot{border-top:1px solid var(--line);padding:24px 0 45px;color:var(--muted);font-size:13px}.foot-row{display:flex;justify-content:space-between;gap:24px}.foot a{color:var(--green-2);font-weight:750}
    @media(max-width:980px){.hero-grid{grid-template-columns:1fr}.hero-note{max-width:620px}.cards{grid-template-columns:repeat(2,minmax(0,1fr))}.toolbar{grid-template-columns:1.5fr repeat(2,1fr)}.toolbar .resource-filter,.toolbar .sort{display:none}}
    @media(max-width:640px){.wrap{width:min(100% - 24px,1240px)}.hero{padding:42px 0 38px}.hero-grid{gap:28px}.hero:before{width:250px;height:250px}.stat-grid{grid-template-columns:repeat(2,1fr)}.stat:nth-child(2){border-right:0}.stat:nth-child(-n+2){border-bottom:1px solid var(--line)}.toolbar{grid-template-columns:1fr 1fr;padding:10px 0}.search-wrap{grid-column:1/-1}.toolbar .venue-filter{display:none}.cards{grid-template-columns:1fr}.result-line{align-items:flex-start}.bench-card{padding:18px}.foot-row{display:block}.foot-row span{display:block;margin-bottom:8px}}
  </style>
</head>
<body>
  <header class="hero">
    <div class="wrap hero-grid">
      <div>
        <span class="eyebrow">NAACL 2026 Survey Asset · Curated Atlas</span>
        <h1>Finance × Economy<br>Benchmark Atlas</h1>
        <p class="hero-copy">把 <strong>${entries.length} 个 benchmark</strong> 从长列表变成可搜索、可筛选、可直达资源的研究卡片。每张卡保留论文依据；公开资源可一键进入 Hugging Face Dataset Preview 或代码仓库。</p>
      </div>
      <aside class="hero-note">
        <p>收录标准：标题或摘要明确声明提出、发布、构建或建立 benchmark。资源链接仅展示已核验的公开入口，没有公开入口的条目不会伪造。</p>
        <div class="stamp"><span>Coverage: 2024–2026</span><span>Updated ${generated}</span></div>
      </aside>
    </div>
  </header>
  <section class="stats" aria-label="数据概览"><div class="wrap stat-grid">
    <div class="stat"><b>${entries.length}</b><span>Benchmarks</span></div>
    <div class="stat"><b>${resourceCount}</b><span>公开资源 Preview</span></div>
    <div class="stat"><b>${hfCount}</b><span>Hugging Face datasets</span></div>
    <div class="stat"><b>${repoCount}</b><span>Code repositories</span></div>
  </div></section>
  <div class="toolbar-shell"><div class="wrap toolbar" role="search">
    <label class="search-wrap"><span class="search-icon">⌕</span><input id="search" class="control" type="search" placeholder="搜索 benchmark、任务、关键词…" autocomplete="off"></label>
    <select id="domain" class="control" aria-label="领域"><option value="">全部领域</option><option value="Finance">Finance</option><option value="Economy">Economy</option></select>
    <select id="year" class="control" aria-label="年份"><option value="">全部年份</option>${options(years)}</select>
    <select id="venue" class="control venue-filter" aria-label="会议"><option value="">全部会议</option>${options(venues)}</select>
    <select id="resource" class="control resource-filter" aria-label="资源状态"><option value="">全部资源状态</option><option value="yes">有公开 Preview</option><option value="no">暂无公开 Preview</option></select>
  </div></div>
  <main class="wrap">
    <div class="result-line"><strong><span id="count">${entries.length}</span> 张卡片</strong><span>点击“为什么它算 benchmark”可展开论文原始判定</span></div>
    <section id="cards" class="cards" aria-live="polite">${cards}</section>
    <div id="empty" class="empty"><b>没有匹配的卡片</b><span>换一个关键词或清除筛选条件试试。</span></div>
  </main>
  <footer class="foot"><div class="wrap foot-row"><span>Source: benchmark_papers.md · 页面数据以论文与公开资源仓库为准。</span><span><a href="#">回到顶部 ↑</a></span></div></footer>
  <script>
    const controls = ['search','domain','year','venue','resource'].map(id => document.getElementById(id));
    const cards = [...document.querySelectorAll('.bench-card')];
    const count = document.getElementById('count');
    const empty = document.getElementById('empty');
    function applyFilters(){
      const [search,domain,year,venue,resource] = controls.map(el => el.value.trim().toLowerCase());
      let visible = 0;
      cards.forEach(card => {
        const ok = (!search || card.dataset.search.includes(search)) && (!domain || card.dataset.domain.toLowerCase()===domain) && (!year || card.dataset.year===year) && (!venue || card.dataset.venue.toLowerCase()===venue) && (!resource || card.dataset.resource===resource);
        card.classList.toggle('hidden', !ok); if(ok) visible++;
      });
      count.textContent = visible; empty.classList.toggle('show', visible===0);
    }
    controls.forEach(el => el.addEventListener(el.tagName==='INPUT'?'input':'change', applyFilters));
    document.addEventListener('keydown', e => { if(e.key==='/' && document.activeElement!==controls[0]){e.preventDefault();controls[0].focus();} });
  </script>
</body>
</html>`;

fs.writeFileSync(output, html);
console.log(`Generated ${path.resolve(output)} with ${entries.length} cards and ${resourceCount} public previews.`);
