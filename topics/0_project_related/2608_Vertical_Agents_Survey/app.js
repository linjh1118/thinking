(() => {
  "use strict";

  const header = document.querySelector("[data-header]");
  const menuButton = document.querySelector(".menu-button");
  const menu = document.querySelector("#site-menu");
  const navLinks = [...document.querySelectorAll(".nav-links a")];

  function setupCursorComet() {
    const canvas = document.querySelector(".cursor-comet");
    if (!canvas?.getContext || !window.matchMedia) return;

    const finePointer = window.matchMedia("(hover: hover) and (pointer: fine)");
    const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)");
    const context = canvas.getContext("2d");
    const activeSelector = "a, button, [role='button'], article, figure, details, .audit-callout, .benchmark-ladder, .factory-flow";
    const maxTrail = 34;
    const maxSparks = 90;
    let currentX = 0;
    let currentY = 0;
    let targetX = 0;
    let targetY = 0;
    let viewportWidth = 0;
    let viewportHeight = 0;
    let frame = 0;
    let burstTick = 0;
    let started = false;
    let inside = false;
    let active = false;
    let enabled = false;
    let trail = [];
    let sparks = [];

    const eligible = () => finePointer.matches && !reducedMotion.matches;

    function resizeCanvas() {
      const ratio = Math.min(window.devicePixelRatio || 1, 2);
      viewportWidth = window.innerWidth;
      viewportHeight = window.innerHeight;
      canvas.width = Math.round(viewportWidth * ratio);
      canvas.height = Math.round(viewportHeight * ratio);
      canvas.style.width = `${viewportWidth}px`;
      canvas.style.height = `${viewportHeight}px`;
      context.setTransform(ratio, 0, 0, ratio, 0, 0);
      trail = [];
      sparks = [];
    }

    function glow(x, y, radius, core, halo) {
      const gradient = context.createRadialGradient(x, y, 0, x, y, radius);
      gradient.addColorStop(0, core);
      gradient.addColorStop(0.3, halo);
      gradient.addColorStop(1, "rgba(47, 95, 224, 0)");
      context.fillStyle = gradient;
      context.beginPath();
      context.arc(x, y, radius, 0, Math.PI * 2);
      context.fill();
    }

    function requestDraw() {
      if (enabled && !frame) frame = window.requestAnimationFrame(drawComet);
    }

    function drawComet() {
      frame = 0;
      if (!enabled) return;
      const dx = targetX - currentX;
      const dy = targetY - currentY;
      const speed = Math.hypot(dx, dy);
      const moving = speed > 0.18;
      currentX += dx * 0.24;
      currentY += dy * 0.24;

      if (inside && moving) {
        trail.unshift({ x: currentX, y: currentY, life: 1, size: 2.2 + Math.random() * 2.4, wobble: (Math.random() - 0.5) * 5 });
        if (trail.length > maxTrail) trail.length = maxTrail;
        burstTick += 1;
        if (speed > 7 && burstTick % 3 === 0) {
          const direction = Math.atan2(dy, dx) + Math.PI;
          const amount = Math.min(7, 3 + Math.floor(speed / 22));
          for (let index = 0; index < amount; index += 1) {
            const angle = direction + (Math.random() - 0.5) * 2.2;
            const force = 1.2 + Math.random() * Math.min(5.5, 1.8 + speed * 0.045);
            sparks.push({
              x: currentX - dx * 0.025 + (Math.random() - 0.5) * 6,
              y: currentY - dy * 0.025 + (Math.random() - 0.5) * 6,
              vx: Math.cos(angle) * force,
              vy: Math.sin(angle) * force,
              life: 0.72 + Math.random() * 0.28,
              size: 1.1 + Math.random() * 2.2
            });
          }
          if (sparks.length > maxSparks) sparks.splice(0, sparks.length - maxSparks);
        }
      }

      trail.forEach(point => {
        point.life *= moving ? 0.955 : 0.91;
        point.y += point.wobble * 0.018;
        point.size *= 0.994;
      });
      trail = trail.filter((point, index) => point.life > 0.035 && index < maxTrail);
      sparks.forEach(spark => {
        spark.x += spark.vx;
        spark.y += spark.vy;
        spark.vx *= 0.94;
        spark.vy *= 0.94;
        spark.life *= 0.89;
        spark.size *= 0.985;
      });
      sparks = sparks.filter(spark => spark.life > 0.035);

      context.clearRect(0, 0, viewportWidth, viewportHeight);
      context.save();
      context.globalCompositeOperation = "lighter";
      if (trail.length > 1) {
        const tail = trail[trail.length - 1];
        const streak = context.createLinearGradient(currentX, currentY, tail.x + 0.01, tail.y + 0.01);
        streak.addColorStop(0, "rgba(91, 141, 239, 0.72)");
        streak.addColorStop(0.45, "rgba(47, 95, 224, 0.28)");
        streak.addColorStop(1, "rgba(30, 58, 138, 0)");
        context.strokeStyle = streak;
        context.lineWidth = active ? 5 : 3.5;
        context.lineCap = "round";
        context.lineJoin = "round";
        context.beginPath();
        context.moveTo(currentX, currentY);
        trail.forEach((point, index) => { if (index % 2 === 0) context.lineTo(point.x, point.y); });
        context.stroke();
      }
      trail.forEach((point, index) => {
        context.globalAlpha = point.life * (1 - index / Math.max(trail.length, 1)) * 0.72;
        glow(point.x, point.y, point.size * 3, "rgba(138, 181, 255, 0.85)", "rgba(47, 95, 224, 0.24)");
      });
      sparks.forEach(spark => {
        context.globalAlpha = spark.life * 0.9;
        glow(spark.x, spark.y, spark.size * 3.8, "rgba(255, 255, 255, 0.96)", "rgba(91, 141, 239, 0.34)");
      });
      context.globalAlpha = inside ? 1 : 0.45;
      glow(currentX, currentY, active ? 25 : 20, "rgba(255,255,255,0.98)", "rgba(91,141,239,0.48)");
      glow(currentX, currentY, active ? 10 : 8, "rgba(255,255,255,1)", "rgba(47,95,224,0.88)");
      context.restore();
      if (moving || trail.length > 1 || sparks.length) requestDraw();
    }

    function handlePointerMove(event) {
      if (!enabled || event.pointerType === "touch") return;
      targetX = event.clientX;
      targetY = event.clientY;
      if (!started) { currentX = targetX; currentY = targetY; started = true; }
      inside = true;
      canvas.classList.add("visible");
      requestDraw();
    }
    function handlePointerOver(event) {
      if (!enabled || !(event.target instanceof Element)) return;
      active = Boolean(event.target.closest(activeSelector));
      requestDraw();
    }
    function hide(clearParticles = false) {
      inside = false;
      active = false;
      canvas.classList.remove("visible");
      if (clearParticles) {
        trail = [];
        sparks = [];
        if (frame) window.cancelAnimationFrame(frame);
        frame = 0;
        context.clearRect(0, 0, viewportWidth, viewportHeight);
      }
    }
    function handleLeave() { hide(false); requestDraw(); }
    function handlePageExit() { hide(true); }
    function enable() {
      if (enabled || !eligible()) return;
      enabled = true;
      resizeCanvas();
      document.addEventListener("pointermove", handlePointerMove, { passive: true });
      document.addEventListener("pointerover", handlePointerOver, { passive: true });
      document.documentElement.addEventListener("mouseleave", handleLeave);
      window.addEventListener("blur", handlePageExit);
      window.addEventListener("resize", resizeCanvas, { passive: true });
    }
    function disable() {
      if (!enabled) return;
      hide(true);
      enabled = false;
      started = false;
      document.removeEventListener("pointermove", handlePointerMove);
      document.removeEventListener("pointerover", handlePointerOver);
      document.documentElement.removeEventListener("mouseleave", handleLeave);
      window.removeEventListener("blur", handlePageExit);
      window.removeEventListener("resize", resizeCanvas);
    }
    function updatePolicy() { eligible() ? enable() : disable(); }
    finePointer.addEventListener?.("change", updatePolicy);
    reducedMotion.addEventListener?.("change", updatePolicy);
    updatePolicy();
  }

  setupCursorComet();

  function closeMenu() {
    if (!menuButton || !menu) return;
    menuButton.setAttribute("aria-expanded", "false");
    menu.classList.remove("open");
    document.body.classList.remove("menu-open");
  }

  if (menuButton && menu) {
    menuButton.addEventListener("click", () => {
      const open = menuButton.getAttribute("aria-expanded") === "true";
      menuButton.setAttribute("aria-expanded", String(!open));
      menu.classList.toggle("open", !open);
      document.body.classList.toggle("menu-open", !open);
    });
    navLinks.forEach(link => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", event => {
      if (event.key === "Escape" && menuButton.getAttribute("aria-expanded") === "true") {
        closeMenu();
        menuButton.focus();
      }
    });
    window.addEventListener("resize", () => { if (window.innerWidth > 900) closeMenu(); }, { passive: true });
  }

  function updateHeader() { header?.classList.toggle("scrolled", window.scrollY > 18); }
  updateHeader();
  window.addEventListener("scroll", updateHeader, { passive: true });

  const revealItems = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const revealObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.08, rootMargin: "0px 0px -40px" });
    revealItems.forEach(item => revealObserver.observe(item));

    const activeObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (!entry.isIntersecting) return;
        navLinks.forEach(link => {
          const activeLink = link.getAttribute("href") === `#${entry.target.id}`;
          link.classList.toggle("active", activeLink);
          activeLink ? link.setAttribute("aria-current", "location") : link.removeAttribute("aria-current");
        });
      });
    }, { threshold: 0.12, rootMargin: "-20% 0px -65%" });
    document.querySelectorAll("main section[id]").forEach(section => activeObserver.observe(section));
  } else {
    revealItems.forEach(item => item.classList.add("visible"));
  }

  const lightbox = document.querySelector("#figure-lightbox");
  const lightboxImage = lightbox?.querySelector("img");
  let lightboxTrigger = null;
  function closeLightbox() {
    if (!lightbox) return;
    typeof lightbox.close === "function" ? lightbox.close() : lightbox.removeAttribute("open");
    lightboxTrigger?.focus();
  }
  document.querySelectorAll("[data-lightbox]").forEach(trigger => {
    trigger.addEventListener("click", () => {
      if (!lightbox || !lightboxImage) return;
      lightboxTrigger = trigger;
      const source = trigger.getAttribute("data-lightbox");
      const figureImage = trigger.closest("figure")?.querySelector("img");
      lightboxImage.src = source;
      lightboxImage.alt = figureImage?.alt || "Expanded survey figure";
      typeof lightbox.showModal === "function" ? lightbox.showModal() : lightbox.setAttribute("open", "");
    });
  });
  lightbox?.querySelector(".lightbox-close")?.addEventListener("click", closeLightbox);
  lightbox?.addEventListener("click", event => { if (event.target === lightbox) closeLightbox(); });
  lightbox?.addEventListener("close", () => { lightboxTrigger = null; });

  const copyButton = document.querySelector("#copy-bibtex");
  const bibtex = document.querySelector("#bibtex");
  const copyStatus = document.querySelector("#copy-status");
  copyButton?.addEventListener("click", async () => {
    if (!bibtex || !copyStatus) return;
    try {
      await navigator.clipboard.writeText(bibtex.textContent);
      copyStatus.textContent = "Copied to clipboard.";
    } catch (_) {
      copyStatus.textContent = "Select the BibTeX block to copy.";
    }
    window.setTimeout(() => { copyStatus.textContent = ""; }, 2200);
  });

  const sources = [
    { type: "benchmark", label: "Benchmark", path: "data/benchmarks.csv" },
    { type: "dataset", label: "Data & Synthesis", path: "data/datasets.csv" },
    { type: "harness", label: "Harness", path: "data/harnesses.csv" }
  ];
  const pageSize = 18;
  const state = { resources: [], filtered: [], currentType: "all", visibleLimit: pageSize };
  const collator = new Intl.Collator("en", { numeric: true, sensitivity: "base" });
  const elements = {
    search: document.querySelector("#search"),
    domain: document.querySelector("#domain-filter"),
    scope: document.querySelector("#scope-filter"),
    evidence: document.querySelector("#evidence-filter"),
    reset: document.querySelector("#reset-filters"),
    list: document.querySelector("#resource-list"),
    summary: document.querySelector("#results-summary"),
    loadMore: document.querySelector("#load-more"),
    advancedToggle: document.querySelector("#advanced-toggle"),
    advancedPanel: document.querySelector("#advanced-filters"),
    typeButtons: [...document.querySelectorAll("[data-type-filter]")]
  };

  function parseCSV(text) {
    const rows = [];
    let row = [];
    let field = "";
    let quoted = false;
    for (let index = 0; index < text.length; index += 1) {
      const character = text[index];
      const next = text[index + 1];
      if (quoted) {
        if (character === '"' && next === '"') { field += '"'; index += 1; }
        else if (character === '"') quoted = false;
        else field += character;
      } else if (character === '"') quoted = true;
      else if (character === ",") { row.push(field); field = ""; }
      else if (character === "\n") {
        row.push(field.replace(/\r$/, ""));
        if (row.some(cell => cell !== "")) rows.push(row);
        row = [];
        field = "";
      } else field += character;
    }
    if (field !== "" || row.length) {
      row.push(field.replace(/\r$/, ""));
      if (row.some(cell => cell !== "")) rows.push(row);
    }
    const [headers = [], ...body] = rows;
    return body.map(cells => Object.fromEntries(headers.map((headerName, index) => [headerName, cells[index] || ""])));
  }

  function inferHarnessDomain(row) {
    const value = `${row.name} ${row.harness_role} ${row.primary_layer}`;
    const rules = [
      [/SWE-bench/i, "Software engineering"], [/CyberGym/i, "Cybersecurity"], [/PaperBench/i, "AI research reproduction"],
      [/MLE-bench|MLGym/i, "Machine learning engineering"], [/WorkArena/i, "Enterprise knowledge work"],
      [/AppWorld/i, "Cross-application workflows"], [/τ-bench|tau/i, "Customer service and transactions"],
      [/BrowserGym|AgentLab/i, "Browser interaction"], [/OSWorld/i, "Desktop interaction"],
      [/InterCode|Terminal/i, "Terminal and code execution"], [/MCP|OpenTelemetry|Inspect AI|Harbor/i, "Cross-domain infrastructure"]
    ];
    return rules.find(([pattern]) => pattern.test(value))?.[1] || "Cross-domain infrastructure";
  }

  function normalize(row, source) {
    const resource = {
      ...row,
      type: source.type,
      typeLabel: source.label,
      domain: row.domain || inferHarnessDomain(row),
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
    return String(value).replace(/[&<>'"]/g, character => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;" })[character]);
  }
  function safeURL(value) {
    try {
      const url = new URL(value, window.location.href);
      return ["http:", "https:"].includes(url.protocol) ? url.href : "#";
    } catch (_) { return "#"; }
  }
  function scopeClassName(scope) {
    return ({ "Industry vertical": "scope-true", "Functional vertical": "scope-role", "Interface domain": "scope-interface", "Horizontal substrate": "scope-base", "Boundary evidence": "scope-boundary" })[scope] || "";
  }
  function detailItem(label, value, className = "") {
    if (!value || value === "—") return "";
    return `<div class="detail-item ${className}"><dt>${escapeHTML(label)}</dt><dd>${escapeHTML(value)}</dd></div>`;
  }

  function resourceCard(resource) {
    const evidencePill = resource.evidence_level !== "Not coded" ? `<span class="pill">${escapeHTML(resource.evidence_level)}</span>` : "";
    const processItem = resource.type === "dataset" ? detailItem("Synthesis / collection", resource.processLabel, "full") : resource.type === "harness" ? detailItem("Primary layer", resource.processLabel) : "";
    const observationItem = resource.type === "harness" ? detailItem("Observability", resource.observabilityLabel) : "";
    return `<details class="resource-card">
      <summary>
        <div class="resource-meta"><span class="resource-group">${escapeHTML(resource.typeLabel)}</span><span>${escapeHTML(resource.year)}</span></div>
        <h3>${escapeHTML(resource.name)}</h3>
        <p class="resource-role">${escapeHTML(resource.roleLabel)}</p>
        <p class="resource-preview">${escapeHTML(resource.environmentLabel)}</p>
        <div class="resource-pills"><span class="pill">${escapeHTML(resource.domain)}</span><span class="pill ${scopeClassName(resource.scope_class)}">${escapeHTML(resource.scope_class)}</span>${evidencePill}</div>
        <span class="expand-icon" aria-hidden="true"></span>
      </summary>
      <dl class="resource-details">
        ${detailItem(resource.type === "dataset" ? "Source unit" : "Environment / runtime", resource.environmentLabel)}
        ${detailItem("Verifier", resource.verifierLabel)}${processItem}${observationItem}
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

  function renderResources() {
    elements.list.setAttribute("aria-busy", "false");
    const visible = state.filtered.slice(0, state.visibleLimit);
    const shown = visible.length;
    const matched = state.filtered.length;
    elements.summary.innerHTML = matched ? `Showing <strong>${shown}</strong> of <strong>${matched}</strong> matched resources` : "No matching resources";
    if (!matched) {
      elements.list.innerHTML = `<div class="empty-state"><h3>No matching resources</h3><p>Clear the search term or broaden the domain, scope, and evidence filters.</p></div>`;
      elements.loadMore.hidden = true;
      return;
    }
    elements.list.innerHTML = visible.map(resourceCard).join("");
    elements.loadMore.hidden = shown >= matched;
    elements.loadMore.textContent = `Load ${Math.min(pageSize, matched - shown)} more resources`;
  }

  function applyFilters({ resetLimit = true } = {}) {
    if (resetLimit) state.visibleLimit = pageSize;
    const query = elements.search.value.trim().toLocaleLowerCase("en");
    const domain = elements.domain.value;
    const scope = elements.scope.value;
    const evidence = elements.evidence.value;
    state.filtered = state.resources.filter(resource => (
      (!query || resource.searchText.includes(query)) &&
      (state.currentType === "all" || resource.type === state.currentType) &&
      (domain === "all" || resource.domain === domain) &&
      (scope === "all" || resource.scope_class === scope) &&
      (evidence === "all" || resource.evidence_level === evidence)
    ));
    renderResources();
  }

  function resetFilters() {
    elements.search.value = "";
    elements.domain.value = "all";
    elements.scope.value = "all";
    elements.evidence.value = "all";
    state.currentType = "all";
    elements.typeButtons.forEach(button => {
      const activeButton = button.dataset.typeFilter === "all";
      button.classList.toggle("active", activeButton);
      button.setAttribute("aria-pressed", String(activeButton));
    });
    applyFilters();
    elements.search.focus();
  }

  function bindResourceEvents() {
    let searchTimer;
    elements.search.addEventListener("input", () => {
      window.clearTimeout(searchTimer);
      searchTimer = window.setTimeout(() => applyFilters(), 120);
    });
    [elements.domain, elements.scope, elements.evidence].forEach(element => element.addEventListener("change", () => applyFilters()));
    elements.typeButtons.forEach(button => button.addEventListener("click", () => {
      state.currentType = button.dataset.typeFilter || "all";
      elements.typeButtons.forEach(item => {
        const activeButton = item === button;
        item.classList.toggle("active", activeButton);
        item.setAttribute("aria-pressed", String(activeButton));
      });
      applyFilters();
    }));
    elements.reset.addEventListener("click", resetFilters);
    elements.loadMore.addEventListener("click", () => {
      state.visibleLimit += pageSize;
      renderResources();
    });
    elements.advancedToggle.addEventListener("click", () => {
      const expanded = elements.advancedToggle.getAttribute("aria-expanded") === "true";
      elements.advancedToggle.setAttribute("aria-expanded", String(!expanded));
      elements.advancedPanel.hidden = expanded;
    });
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
      bindResourceEvents();
      renderResources();
    } catch (error) {
      elements.list.setAttribute("aria-busy", "false");
      elements.summary.textContent = "Resource inventory unavailable";
      elements.list.innerHTML = `<div class="error-state"><strong>The CSV inventories could not be loaded.</strong><br>Open this page through a static web server.</div>`;
      console.error(error);
    }
  }

  loadResources();
})();
