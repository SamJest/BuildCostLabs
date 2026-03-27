(function () {
  const config = window.__calculatorConfig || { formula: "coverage", name: "Material" };
  const form = document.querySelector(".generic-calculator-form");
  if (!form) return;

  const currencyMap = {
    GBP: { symbol: "£", code: "GBP" },
    USD: { symbol: "$", code: "USD" },
    EUR: { symbol: "€", code: "EUR" }
  };
  let currency = "GBP";
  let unit = "metric";

  const currencyButtons = Array.from(document.querySelectorAll(".currency-pill"));
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");

  function materialLabel() {
    return (config.name || "material").replace(/\s+calculator$/i, "").toLowerCase();
  }

  function unitLabel(count) {
    if (count === 1) {
      return config.unitNameSingular || "unit";
    }
    return config.unitNamePlural || "units";
  }

  function money(value) {
    const info = currencyMap[currency] || currencyMap.GBP;
    return `${info.symbol}${Number(value).toFixed(2)} ${info.code}`;
  }

  function getNumber(id) {
    const el = document.getElementById(id);
    if (!el) return 0;
    const value = parseFloat(el.value);
    return Number.isFinite(value) ? value : 0;
  }

  function toMetricLength(value) {
    return unit === "metric" ? value : value * 0.3048;
  }

  function toMetricDepth(value) {
    return unit === "metric" ? value : value * 0.3048;
  }

  function setActive(buttons, matcher) {
    buttons.forEach((button) => button.classList.toggle("is-active", matcher(button)));
  }

  currencyButtons.forEach((button) => button.addEventListener("click", function () {
    currency = button.dataset.currency;
    setActive(currencyButtons, (item) => item.dataset.currency === currency);
  }));

  unitButtons.forEach((button) => button.addEventListener("click", function () {
    unit = button.dataset.unit;
    setActive(unitButtons, (item) => item.dataset.unit === unit);
  }));

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const wasteFactor = 1 + (getNumber("waste") / 100);
    const pricePerUnit = getNumber("price-per-unit");
    let units = 0;
    let note = "";

    if (config.formula === "coverage") {
      const area = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width"));
      const coveragePerUnit = getNumber("coverage-per-unit");
      const coveredArea = area * wasteFactor;
      units = coveragePerUnit > 0 ? Math.ceil(coveredArea / coveragePerUnit) : 0;
      note = "Calculation: area plus waste, then rounded to whole buying units by coverage.";
      resultMain.textContent = units > 0 ? `${units} ${unitLabel(units)} of ${materialLabel()}` : "Enter your measurements";
      resultSub.textContent = units > 0 ? `That covers about ${coveredArea.toFixed(2)} m2 after waste and roughly ${money(units * pricePerUnit)} in material cost.` : (config.resultIntro || `You will see the estimated quantity, whole-unit buying count, and rough material cost for ${materialLabel()} here.`);
      resultBreakdown.innerHTML = units > 0 ? `
        <div class="break-row"><span>Covered area incl. waste</span><strong>${coveredArea.toFixed(2)} m2</strong></div>
        <div class="break-row"><span>Coverage per unit</span><strong>${coveragePerUnit.toFixed(2)} m2</strong></div>
        <div class="break-row"><span>Buying total</span><strong>${units} ${unitLabel(units)}</strong></div>
        <div class="break-row"><span>Estimated cost</span><strong>${money(units * pricePerUnit)}</strong></div>
        <div class="calc-note">${note}</div>` : "";
      return;
    }

    if (config.formula === "volume") {
      const volume = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width")) * toMetricDepth(getNumber("depth"));
      const density = getNumber("density");
      const unitSize = getNumber("unit-size");
      const totalVolume = volume * wasteFactor;
      const tonnes = totalVolume * density;
      units = unitSize > 0 ? Math.ceil(tonnes / unitSize) : 0;
      note = "Calculation: length x width x depth, then waste, then density, then rounded to whole units.";
      resultMain.textContent = units > 0 ? `${units} ${unitLabel(units)} of ${materialLabel()}` : "Enter your measurements";
      resultSub.textContent = units > 0 ? `That works out to about ${totalVolume.toFixed(3)} m3, roughly ${tonnes.toFixed(2)} tonnes, and about ${money(units * pricePerUnit)} in material cost.` : (config.resultIntro || `You will see the estimated quantity, whole-unit buying count, and rough material cost for ${materialLabel()} here.`);
      resultBreakdown.innerHTML = units > 0 ? `
        <div class="break-row"><span>Volume incl. waste</span><strong>${totalVolume.toFixed(3)} m3</strong></div>
        <div class="break-row"><span>Tonnage</span><strong>${tonnes.toFixed(2)} t</strong></div>
        <div class="break-row"><span>Buying total</span><strong>${units} ${unitLabel(units)}</strong></div>
        <div class="break-row"><span>Estimated cost</span><strong>${money(units * pricePerUnit)}</strong></div>
        <div class="calc-note">${note}</div>` : "";
      return;
    }

    const run = toMetricLength(getNumber("length")) * wasteFactor;
    const pieceLength = toMetricLength(getNumber("piece-length"));
    units = pieceLength > 0 ? Math.ceil(run / pieceLength) : 0;
    note = "Calculation: total run plus waste, then rounded to whole-length buying pieces.";
    resultMain.textContent = units > 0 ? `${units} ${unitLabel(units)} of ${materialLabel()}` : "Enter your measurements";
    resultSub.textContent = units > 0 ? `That covers about ${run.toFixed(2)} linear metres after waste and roughly ${money(units * pricePerUnit)} in material cost.` : (config.resultIntro || `You will see the estimated quantity, whole-unit buying count, and rough material cost for ${materialLabel()} here.`);
    resultBreakdown.innerHTML = units > 0 ? `
      <div class="break-row"><span>Run incl. waste</span><strong>${run.toFixed(2)} m</strong></div>
      <div class="break-row"><span>Unit length</span><strong>${pieceLength.toFixed(2)} m</strong></div>
      <div class="break-row"><span>Buying total</span><strong>${units} ${unitLabel(units)}</strong></div>
      <div class="break-row"><span>Estimated cost</span><strong>${money(units * pricePerUnit)}</strong></div>
      <div class="calc-note">${note}</div>` : "";
  });
})();
