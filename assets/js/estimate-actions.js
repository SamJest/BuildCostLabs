(function () {
  function textBySelector(selector) {
    var node = document.querySelector(selector);
    return node ? node.textContent.trim() : "";
  }

  function buildSummary() {
    var title = (document.querySelector("h1") || {}).textContent || document.title || "Estimate";
    title = title.trim();
    var main = textBySelector(".result-main") || "Run the calculator to generate a live result.";
    var sub = textBySelector(".result-sub");
    var lines = [title, window.location.href, "", "Main result: " + main];
    if (sub) {
      lines.push(sub);
    }
    var rows = Array.prototype.slice.call(document.querySelectorAll(".result-breakdown .break-row"));
    if (rows.length) {
      lines.push("", "Breakdown:");
      rows.forEach(function (row) {
        var cells = row.querySelectorAll("span, strong");
        if (cells.length >= 2) {
          lines.push("- " + cells[0].textContent.trim() + ": " + cells[1].textContent.trim());
        }
      });
    }
    lines.push("", "Built with BuildCostLab. Use as a planning estimate and compare against live quotes and supplier data.");
    return lines.join("\n");
  }

  function updateStatus(message) {
    var node = document.getElementById("estimate-action-status");
    if (node) {
      node.textContent = message;
    }
  }

  function track(action) {
    if (typeof window.gtag === "function") {
      window.gtag("event", "estimate_action_click", {
        action_name: action,
        page_type: document.querySelector('meta[name="page-type"]')?.content || "unknown"
      });
    }
  }

  function copySummary(summary) {
    if (navigator.clipboard && navigator.clipboard.writeText) {
      return navigator.clipboard.writeText(summary);
    }
    var area = document.createElement("textarea");
    area.value = summary;
    area.setAttribute("readonly", "readonly");
    area.style.position = "absolute";
    area.style.left = "-9999px";
    document.body.appendChild(area);
    area.select();
    try {
      document.execCommand("copy");
      document.body.removeChild(area);
      return Promise.resolve();
    } catch (error) {
      document.body.removeChild(area);
      return Promise.reject(error);
    }
  }

  document.querySelectorAll("[data-estimate-action]").forEach(function (button) {
    button.addEventListener("click", function () {
      var action = button.getAttribute("data-estimate-action");
      var summary = buildSummary();
      if (action === "copy") {
        copySummary(summary).then(function () {
          updateStatus("Estimate summary copied. Paste it into notes, email, or a quote request.");
        }).catch(function () {
          updateStatus("Copy failed on this device. Use print or email instead.");
        });
        track("copy");
        return;
      }
      if (action === "email") {
        var email = button.getAttribute("data-email") || "";
        var subject = encodeURIComponent("Estimate from BuildCostLab: " + ((document.querySelector("h1") || {}).textContent || document.title || "Calculator"));
        var body = encodeURIComponent(summary);
        window.location.href = "mailto:" + email + "?subject=" + subject + "&body=" + body;
        updateStatus("Your email app should open with the estimate summary prefilled.");
        track("email");
        return;
      }
      if (action === "print") {
        window.print();
        updateStatus("Print dialog opened. Save as PDF if you want a shareable quote brief.");
        track("print");
      }
    });
  });
})();
