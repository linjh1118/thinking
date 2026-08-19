(() => {
  "use strict";

  const sources = [
    { type: "benchmark", label: "Benchmark", icon: "B", path: "data/benchmarks.csv" },
    { type: "dataset", label: "Dataset", icon: "D", path: "data/datasets.csv" },
    { type: "harness", label: "Harness", icon: "H", path: "data/harnesses.csv" }
  ];

  const state = { resources: [], filtered: [] };
  const collator = new Intl.Collator("en", { numeric: true, sensitivity: "base" });

  const elements = {
    search: document.querySelector("#search"),
    type: document.querySelector("#type-filter"),
    domain: document.querySelector("#domain-filter"),
    scope: document.querySelector("#scope-filter"),
    evidence: document.querySelector("#evidence-filter"),
    reset: document.querySelector("#reset-filters"),
    list: document.querySelector("#resource-list"),
    summary: document.querySelector("#results-summary")
  };

  function parseCSV(text) {
    const rows = [];
    let row = [];
    let field = "";
    let quoted = false;

    for (let index = 0; index < text.length; index += 1) {
      const char = text[index];
      const next = text[index + 1];
      if (quoted) {
        if (char === '"' && next === '"') {
          field += '"';
          index += 1;
        } else if (char === '"') {
          quoted = false;
        } else {
          field += char;
        }
      } else if (char === '"') {
        quoted = true;
      } else if (char === ",") {
        row.push(field);
        field = "";
      } else if (char === "\n") {
        row.push(field.replace(/\r$/, ""));
        if (row.some(cell => cell !== "")) rows.push(row);
        row = [];
        field = "";
      } else {
        field += char;
      }
    }

    if (field !== "" || row.length) {
      row.push(field.replace(/\r$/, ""));
      if (row.some(cell => cell !== "")) rows.push(row);
    }

    const [headers = [], ...body] = rows;
    return body.map(cells => Object.fromEntries(headers.map((header, index) => [header, cells[index] || ""])));
  }

  function inferHarnessDomain(row) {
    const value = `${row.name} ${row.harness_role} ${row.primary_layer}`;
    const rules = [
      [/SWE-bench/i, "Software engineering"],
      [/CyberGym/i, "Cybersecurity"],
      [/PaperBench/i, "AI research reproduction"],
      [/MLE-bench|MLGym/i, "Machine learning engineering"],
      [/WorkArena/i, "Enterprise knowledge work"],
      [/AppWorld/i, "Cross-application workflows"],
      [/τ-bench|tau/i, "Customer service and transactions"],
      [/BrowserGym|AgentLab/i, "Browser interaction"],
      [/OSWorld/i, "Desktop interaction"],
      [/InterCode|Terminal/i, "Terminal and code execution"],
      [/MCP|OpenTelemetry|Inspect AI|Harbor/i, "Cross-domain infrastructure"]
    ];
    return rules.find(([pattern]) => pattern.test(value))?.[1] || "Cross-domain infrastructure";
  }

  function normalize(row, source) {
    const domain = row.domain || inferHarnessDomain(row);
    const resource = {
      ...row,
      type: source.type,
      typeLabel: source.label,
      icon: source.icon,
      domain,
      evidence_level: row.evidence_level || "Not coded",
      roleLabel: row.role || row.harness_role || "—",
      environmentLabel: row.environment || row.source_unit || row.environment_or_runtime || "—",
      processLabel: row.synthesis_or_collection || row.primary_layer || "—",
      verifierLabel: row.verifier || row.verifier_support || "—",
      observabilityLabel: row.observability || "—"
    };
    resource.searchText = Object.values(resource).join(" ").toLocaleLowerCase("en");
    return resource;
  }

  function escapeHTML(value = "") {
    return String(value).replace(/[&<>'"]/g, character => ({
      "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;"
    })[character]);
  }

  function safeURL(value) {
    try {
      const url = new URL(value, window.location.href);
      return ["http:", "https:"].includes(url.protocol) ? url.href : "#";
    } catch (_) {
      return "#";
    }
  }

  function scopeClassName(scope) {
    return ({
      "Industry vertical": "scope-true",
      "Functional vertical": "scope-role",
      "Interface domain": "scope-interface",
      "Horizontal substrate": "scope-base",
      "Boundary evidence": "scope-boundary"
    })[scope] || "";
  }

  function detailItem(label, value, className = "") {
    if (!value || value === "—") return "";
    return `<div class="detail-item ${className}"><dt>${escapeHTML(label)}</dt><dd>${escapeHTML(value)}</dd></div>`;
  }

  function resourceCard(resource) {
    const evidencePill = resource.evidence_level !== "Not coded"
      ? `<span class="pill">${escapeHTML(resource.evidence_level)}</span>`
      : "";
    const processItem = resource.type === "dataset"
      ? detailItem("Synthesis / collection", resource.processLabel, "full")
      : resource.type === "harness"
        ? detailItem("Primary layer", resource.processLabel)
        : "";
    const observationItem = resource.type === "harness"
      ? detailItem("Observability", resource.observabilityLabel)
      : "";

    return `
      <details class="resource-card">
        <summary>
          <span class="type-icon type-${escapeHTML(resource.type)}" aria-hidden="true">${escapeHTML(resource.icon)}</span>
          <span class="resource-name"><strong>${escapeHTML(resource.name)}</strong><small>${escapeHTML(resource.roleLabel)} · ${escapeHTML(resource.year)}</small></span>
          <span class="resource-pills">
            <span class="pill">${escapeHTML(resource.typeLabel)}</span>
            <span class="pill">${escapeHTML(resource.domain)}</span>
            <span class="pill ${scopeClassName(resource.scope_class)}">${escapeHTML(resource.scope_class)}</span>
            ${evidencePill}
          </span>
          <span class="expand-icon" aria-hidden="true"></span>
        </summary>
        <dl class="resource-details">
          ${detailItem(resource.type === "dataset" ? "Source unit" : "Environment / runtime", resource.environmentLabel)}
          ${detailItem("Verifier", resource.verifierLabel)}
          ${processItem}
          ${observationItem}
          ${detailItem("Key limitation", resource.main_limit, "full limit-item")}
          <div class="detail-item full"><dt>Primary source</dt><dd><a class="source-link" href="${safeURL(resource.primary_url)}" target="_blank" rel="noreferrer">Open primary source <span aria-hidden="true">↗</span></a></dd></div>
        </dl>
      </details>`;
  }

  function updateStats(resources) {
    const counts = resources.reduce((accumulator, resource) => {
      accumulator[resource.type] = (accumulator[resource.type] || 0) + 1;
      return accumulator;
    }, {});
    document.querySelector("#stat-total").textContent = resources.length;
    document.querySelector("#stat-bench").textContent = counts.benchmark || 0;
    document.querySelector("#stat-data").textContent = counts.dataset || 0;
    document.querySelector("#stat-harness").textContent = counts.harness || 0;
    document.querySelector("#hero-bench-count").textContent = counts.benchmark || 0;
    document.querySelector("#hero-data-count").textContent = counts.dataset || 0;
    document.querySelector("#hero-harness-count").textContent = counts.harness || 0;
  }

  function populateDomains(resources) {
    const domains = [...new Set(resources.map(resource => resource.domain))].sort(collator.compare);
    elements.domain.insertAdjacentHTML("beforeend", domains.map(domain => `<option value="${escapeHTML(domain)}">${escapeHTML(domain)}</option>`).join(""));
  }

  function applyFilters() {
    const query = elements.search.value.trim().toLocaleLowerCase("en");
    const type = elements.type.value;
    const domain = elements.domain.value;
    const scope = elements.scope.value;
    const evidence = elements.evidence.value;

    state.filtered = state.resources.filter(resource => (
      (!query || resource.searchText.includes(query)) &&
      (type === "all" || resource.type === type) &&
      (domain === "all" || resource.domain === domain) &&
      (scope === "all" || resource.scope_class === scope) &&
      (evidence === "all" || resource.evidence_level === evidence)
    ));
    renderResources();
  }

  function renderResources() {
    elements.list.setAttribute("aria-busy", "false");
    elements.summary.innerHTML = `Showing <strong>${state.filtered.length}</strong> of ${state.resources.length} resources`;
    if (!state.filtered.length) {
      elements.list.innerHTML = `<div class="empty-state"><h3>No matching resources</h3><p>Clear the search term or broaden the domain, scope class, and evidence filters.</p></div>`;
      return;
    }
    elements.list.innerHTML = state.filtered.map(resourceCard).join("");
  }

  function resetFilters() {
    elements.search.value = "";
    elements.type.value = "all";
    elements.domain.value = "all";
    elements.scope.value = "all";
    elements.evidence.value = "all";
    applyFilters();
    elements.search.focus();
  }

  function bindEvents() {
    let searchTimer;
    elements.search.addEventListener("input", () => {
      window.clearTimeout(searchTimer);
      searchTimer = window.setTimeout(applyFilters, 120);
    });
    [elements.type, elements.domain, elements.scope, elements.evidence].forEach(element => element.addEventListener("change", applyFilters));
    elements.reset.addEventListener("click", resetFilters);
  }

  async function loadResources() {
    try {
      const groups = await Promise.all(sources.map(async source => {
        const response = await fetch(source.path);
        if (!response.ok) throw new Error(`${source.path}: HTTP ${response.status}`);
        return parseCSV(await response.text()).map(row => normalize(row, source));
      }));

      state.resources = groups.flat().sort((left, right) => {
        const typeOrder = { benchmark: 0, dataset: 1, harness: 2 };
        return typeOrder[left.type] - typeOrder[right.type] || Number(right.year) - Number(left.year) || collator.compare(left.name, right.name);
      });
      state.filtered = [...state.resources];
      populateDomains(state.resources);
      updateStats(state.resources);
      bindEvents();
      renderResources();
    } catch (error) {
      elements.list.setAttribute("aria-busy", "false");
      elements.summary.textContent = "Resource inventory unavailable";
      elements.list.innerHTML = `<div class="error-state"><strong>The CSV inventories could not be loaded.</strong><br>Open this page through a static web server; browsers may block data loading when the file is opened directly.</div>`;
      console.error(error);
    }
  }

  loadResources();
})();
