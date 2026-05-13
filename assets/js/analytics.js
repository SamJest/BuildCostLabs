(function () {
  const recentKey = "bcl_recent_calculators";
  const maxRecent = 6;

  function pageType() {
    const meta = document.querySelector('meta[name="page-type"]');
    return meta ? meta.content || "unknown" : "unknown";
  }

  function calculatorSlugFromPath(pathname) {
    const match = String(pathname || "").match(/\/calculators\/([^/]+)\//);
    return match ? match[1] : "";
  }

  function track(eventName, payload) {
    const data = Object.assign(
      {
        page_type: pageType(),
        path: window.location.pathname || "/",
        calculator_slug: calculatorSlugFromPath(window.location.pathname)
      },
      payload || {}
    );
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, data);
    }
  }

  function readRecent() {
    try {
      return JSON.parse(window.localStorage.getItem(recentKey) || "[]").filter(Boolean);
    } catch (error) {
      return [];
    }
  }

  function writeRecent(items) {
    try {
      window.localStorage.setItem(recentKey, JSON.stringify(items.slice(0, maxRecent)));
    } catch (error) {
      // ignore storage failures
    }
  }

  function markCalculatorVisit() {
    const slug = calculatorSlugFromPath(window.location.pathname);
    if (!slug) return;
    const titleNode = document.querySelector("h1");
    const title = titleNode ? titleNode.textContent.trim() : slug.replace(/-/g, " ");
    const current = { slug: slug, title: title, href: "/calculators/" + slug + "/", ts: Date.now() };
    const existing = readRecent().filter(function (item) {
      return item.slug !== slug;
    });
    writeRecent([current].concat(existing));
  }

  function renderRecentTools() {
    const panels = Array.from(document.querySelectorAll("[data-recent-tools]"));
    if (!panels.length) return;
    const currentSlug = calculatorSlugFromPath(window.location.pathname);
    const items = readRecent().filter(function (item) {
      return item.slug && item.slug !== currentSlug;
    }).slice(0, 4);
    panels.forEach(function (panel) {
      const list = panel.querySelector("[data-recent-tools-list]");
      if (!list || !items.length) return;
      list.innerHTML = items.map(function (item) {
        return '<a class="mini-tool-card" href="' + item.href + '" data-recent-tool-link>' + item.title + "</a>";
      }).join("");
      panel.hidden = false;
    });
  }

  window.BuildCostLabAnalytics = {
    track: track,
    markCalculatorVisit: markCalculatorVisit,
    renderRecentTools: renderRecentTools,
    readRecent: readRecent
  };
})();

