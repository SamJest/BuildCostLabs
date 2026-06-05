(function () {
  const root = document.querySelector("[data-calculator-actions]");
  if (!root) return;

  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  const status = document.getElementById("calculator-action-status");
  const formulaList = document.querySelector("[data-calculator-formula-steps]");
  const shoppingList = document.querySelector("[data-shopping-list]");
  const vatBreakdown = document.querySelector("[data-vat-breakdown]");
  const formula = root.getAttribute("data-calculator-formula") || "coverage";
  const calculatorName = root.getAttribute("data-calculator-name") || "BuildCostLab calculator";
  const storageKey = "bcl_custom_estimate_" + (window.location.pathname || "/");

  function setStatus(message) {
    if (status) status.textContent = message || "";
  }

  function defaultFormulaSteps() {
    if (formula === "volume") {
      return [
        "Measure the area or run the calculator asks for.",
        "Convert depth into a volume where needed.",
        "Add the waste or delivery allowance.",
        "Convert into tonnes, bags, cubic metres, or whole buying units."
      ];
    }
    if (formula === "linear") {
      return [
        "Start with the measured run length.",
        "Adjust for openings, corners, joins, and practical cutting waste.",
        "Divide by stock length or spacing.",
        "Round up to whole pieces and check fittings separately."
      ];
    }
    if (formula === "project_cost") {
      return [
        "Measure the project scope.",
        "Apply material, labour, extras, and contingency assumptions.",
        "Compare low, standard, and higher-spec routes.",
        "Use the result as a planning brief, not a fixed quote."
      ];
    }
    return [
      "Measure the covered area.",
      "Apply product coverage, pack size, or unit dimensions.",
      "Add waste for cuts, joins, breakage, or layout loss.",
      "Round up to whole packs, boxes, slabs, tins, rolls, or boards."
    ];
  }

  function renderFormulaSteps() {
    if (!formulaList) return;
    formulaList.innerHTML = "";
    defaultFormulaSteps().forEach(function (step) {
      const li = document.createElement("li");
      li.textContent = step;
      formulaList.appendChild(li);
    });
  }

  function breakdownRows() {
    if (!resultBreakdown) return [];
    return Array.from(resultBreakdown.querySelectorAll(".break-row")).map(function (row) {
      const cells = Array.from(row.children).map(function (cell) {
        return cell.textContent.trim();
      }).filter(Boolean);
      return {
        label: cells[0] || "",
        value: cells.slice(1).join(": ") || ""
      };
    }).filter(function (row) {
      return row.label || row.value;
    });
  }

  function moneyValue(text) {
    const match = String(text || "").replace(/,/g, "").match(/([£$€])\s*([0-9]+(?:\.[0-9]+)?)/);
    if (!match) return null;
    return {
      symbol: match[1],
      value: Number(match[2])
    };
  }

  function likelyShoppingRows(rows) {
    const skip = /cost|price|area|volume|measured|single unit|coverage|layout|room size|floor area|buffer/i;
    return rows.filter(function (row) {
      return row.value && !skip.test(row.label);
    }).slice(0, 6);
  }

  function renderShoppingList() {
    if (!shoppingList) return;
    const rows = likelyShoppingRows(breakdownRows());
    shoppingList.innerHTML = "";
    if (!rows.length) {
      shoppingList.innerHTML = '<div class="break-row"><span>Materials</span><strong>Run the calculator to build a buying checklist</strong></div>';
      return;
    }
    rows.forEach(function (row) {
      const div = document.createElement("div");
      div.className = "break-row";
      div.innerHTML = `<span>${row.label}</span><strong>${row.value}</strong>`;
      shoppingList.appendChild(div);
    });
    const note = document.createElement("div");
    note.className = "calc-note";
    note.textContent = "Before ordering, check accessories, delivery, waste removal, VAT, and whether one spare unit is safer than running short.";
    shoppingList.appendChild(note);
  }

  function renderVat() {
    if (!vatBreakdown) return;
    const costRow = breakdownRows().find(function (row) {
      return /estimated|material|total|cost/i.test(row.label) && moneyValue(row.value);
    });
    vatBreakdown.innerHTML = "";
    if (!costRow) {
      vatBreakdown.innerHTML = '<div class="break-row"><span>VAT view</span><strong>Run the calculator to see cost with and without VAT</strong></div>';
      return;
    }
    const parsed = moneyValue(costRow.value);
    const exVat = parsed.value / 1.2;
    const vat = parsed.value - exVat;
    vatBreakdown.innerHTML =
      `<div class="break-row"><span>Displayed total</span><strong>${parsed.symbol}${parsed.value.toFixed(2)}</strong></div>` +
      `<div class="break-row"><span>If total includes 20% VAT</span><strong>${parsed.symbol}${exVat.toFixed(2)} ex VAT + ${parsed.symbol}${vat.toFixed(2)} VAT</strong></div>` +
      `<div class="break-row"><span>If total excludes VAT</span><strong>${parsed.symbol}${(parsed.value * 1.2).toFixed(2)} incl VAT</strong></div>`;
  }

  function summaryText() {
    const lines = [
      calculatorName,
      window.location.href,
      "",
      "Result: " + (resultMain ? resultMain.textContent.trim() : ""),
      resultSub ? resultSub.textContent.trim() : "",
      ""
    ];
    const rows = breakdownRows();
    if (rows.length) {
      lines.push("Breakdown:");
      rows.forEach(function (row) {
        lines.push("- " + row.label + ": " + row.value);
      });
      lines.push("");
    }
    lines.push("Quote checks:");
    lines.push("- Confirm whether prices include VAT, delivery, waste removal, accessories, and labour.");
    lines.push("- Compare suppliers or installers against the same measurements and assumptions.");
    return lines.join("\n");
  }

  function saveSnapshot() {
    try {
      window.localStorage.setItem(storageKey, JSON.stringify({
        savedAt: new Date().toISOString(),
        result: resultMain ? resultMain.textContent.trim() : "",
        text: summaryText()
      }));
      setStatus("Estimate snapshot saved on this device.");
    } catch (error) {
      setStatus("This browser could not save the snapshot. Copy or print the result instead.");
    }
  }

  function refreshPanels() {
    renderShoppingList();
    renderVat();
  }

  root.addEventListener("click", function (event) {
    const button = event.target.closest("[data-calculator-action]");
    if (!button) return;
    const action = button.getAttribute("data-calculator-action");
    if (action === "copy") {
      navigator.clipboard.writeText(summaryText()).then(function () {
        setStatus("Estimate copied. Paste it into a quote request or notes.");
      }).catch(function () {
        setStatus("Copy failed in this browser. Try save or print instead.");
      });
      return;
    }
    if (action === "save") {
      saveSnapshot();
      return;
    }
    if (action === "print") {
      window.print();
      setStatus("Use the browser print dialog to save a PDF if needed.");
    }
  });

  if (resultBreakdown) {
    new MutationObserver(refreshPanels).observe(resultBreakdown, { childList: true, subtree: true });
  }

  renderFormulaSteps();
  refreshPanels();
})();
