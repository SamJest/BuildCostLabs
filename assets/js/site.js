(function () {
  function track(eventName, payload) {
    if (typeof window.gtag === "function") {
      window.gtag("event", eventName, payload || {});
    }
  }

  function normalize(value) {
    return String(value || "").trim().toLowerCase();
  }

  document.querySelectorAll("[data-ad-slot]").forEach(function (slot) {
    track("ad_slot_visible", {
      slot_name: slot.getAttribute("data-ad-slot"),
      page_type: document.querySelector('meta[name="page-type"]')?.content || "unknown"
    });
  });

  document.querySelectorAll(".mini-tool-card, .text-link, .tool-card a, .jump-chip, .hero-quick-link").forEach(function (link) {
    link.addEventListener("click", function () {
      track("internal_link_click", {
        href: link.getAttribute("href") || "",
        page_type: document.querySelector('meta[name="page-type"]')?.content || "unknown"
      });
    });
  });

  document.querySelectorAll(".calculator-form").forEach(function (form) {
    form.addEventListener("submit", function () {
      track("calculator_submit", {
        form_id: form.getAttribute("id") || "calculator-form"
      });
    });
  });

  document.querySelectorAll("[data-estimate-action]").forEach(function (button) {
    button.addEventListener("click", function () {
      track("estimate_action_click", {
        action: button.getAttribute("data-estimate-action") || "unknown",
        page_type: document.querySelector('meta[name="page-type"]')?.content || "unknown"
      });
    });
  });

  document.querySelectorAll("[data-conversion-link]").forEach(function (link) {
    link.addEventListener("click", function () {
      track("conversion_link_click", {
        target: link.getAttribute("data-conversion-link") || "unknown",
        page_type: document.querySelector('meta[name="page-type"]')?.content || "unknown"
      });
    });
  });

  document.querySelectorAll("[data-directory-root]").forEach(function (root) {
    var searchInput = root.querySelector("[data-directory-search]");
    var resetButton = root.querySelector("[data-directory-reset]");
    var countNode = root.querySelector("[data-directory-count]");
    var emptyNode = root.querySelector("[data-directory-empty]");
    var cards = Array.prototype.slice.call(root.querySelectorAll("[data-directory-card]"));
    var filters = Array.prototype.slice.call(root.querySelectorAll("[data-filter-value]"));
    var activeFilter = "all";

    function applyDirectoryFilter() {
      var query = normalize(searchInput && searchInput.value);
      var visibleCount = 0;

      cards.forEach(function (card) {
        var category = normalize(card.getAttribute("data-category"));
        var haystack = normalize(card.getAttribute("data-search"));
        var matchesQuery = !query || haystack.indexOf(query) !== -1;
        var matchesFilter = activeFilter === "all" || category === normalize(activeFilter);
        var isVisible = matchesQuery && matchesFilter;
        card.hidden = !isVisible;
        if (isVisible) visibleCount += 1;
      });

      if (countNode) {
        if (visibleCount === cards.length) {
          countNode.textContent = "Showing all " + cards.length + " calculators.";
        } else {
          countNode.textContent = "Showing " + visibleCount + " of " + cards.length + " calculators.";
        }
      }

      if (emptyNode) {
        emptyNode.hidden = visibleCount !== 0;
      }
    }

    filters.forEach(function (button) {
      button.addEventListener("click", function () {
        activeFilter = button.getAttribute("data-filter-value") || "all";
        filters.forEach(function (item) {
          item.classList.toggle("is-active", item === button);
        });
        track("directory_filter_use", {
          filter_value: activeFilter,
          page_type: document.querySelector('meta[name="page-type"]')?.content || "unknown"
        });
        applyDirectoryFilter();
      });
    });

    if (searchInput) {
      searchInput.addEventListener("input", applyDirectoryFilter);
    }

    if (resetButton) {
      resetButton.addEventListener("click", function () {
        if (searchInput) searchInput.value = "";
        activeFilter = "all";
        filters.forEach(function (item) {
          item.classList.toggle("is-active", (item.getAttribute("data-filter-value") || "all") === "all");
        });
        applyDirectoryFilter();
      });
    }

    applyDirectoryFilter();
  });
})();
