(function () {
  const currencyMap = {
    GBP: { symbol: "£", code: "GBP" },
    USD: { symbol: "$", code: "USD" },
    EUR: { symbol: "€", code: "EUR" },
    AUD: { symbol: "$", code: "AUD" },
    CAD: { symbol: "$", code: "CAD" }
  };
  let currency = "GBP";
  const currencyButtons = Array.from(document.querySelectorAll(".currency-pill"));
  function setCurrency(next) {
    currency = next;
    currencyButtons.forEach((btn) => {
      btn.classList.toggle("is-active", btn.dataset.currency === next);
    });
  }
  currencyButtons.forEach((btn) => btn.addEventListener("click", function () {
    setCurrency(btn.dataset.currency);
  }));
  function money(value) {
    const info = currencyMap[currency] || currencyMap.GBP;
    return `${info.symbol}${Number(value).toFixed(2)} ${info.code}`;
  }const form = document.getElementById("gravel-form");
  if (!form) return;
  const modeButtons = Array.from(document.querySelectorAll(".mode-toggle"));
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  let mode = "driveway";
  let unit = "metric";
  const presets = { driveway: { depthMetric: 50, depthImperial: 2, waste: 10, density: 1.7, price: 65 }, base: { depthMetric: 100, depthImperial: 4, waste: 12, density: 1.8, price: 55 }, decorative: { depthMetric: 40, depthImperial: 1.5, waste: 8, density: 1.6, price: 75 } };
  function setActive(buttons, value) { buttons.forEach((btn) => btn.classList.toggle("is-active", btn.dataset.mode === value || btn.dataset.unit === value)); }
  function applyPreset() { const p = presets[mode]; document.getElementById("depth").value = unit === "metric" ? p.depthMetric : p.depthImperial; document.getElementById("waste").value = p.waste; document.getElementById("density").value = p.density; document.getElementById("price-per-tonne").value = p.price; }
  function getNumber(id) { const v = parseFloat(document.getElementById(id).value); return Number.isFinite(v) ? v : 0; }
  function toMetricLength(v) { return unit === "metric" ? v : v * 0.3048; }
  function toMetricDepth(v) { return unit === "metric" ? v / 1000 : v * 0.0254; }
  function labelForMode() { if (mode === "base") return "base layer"; if (mode === "decorative") return "decorative gravel"; return "driveway or path gravel"; }
  modeButtons.forEach((btn) => btn.addEventListener("click", function () { mode = btn.dataset.mode; setActive(modeButtons, mode); applyPreset(); }));
  unitButtons.forEach((btn) => btn.addEventListener("click", function () { unit = btn.dataset.unit; setActive(unitButtons, unit); applyPreset(); }));
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const length = toMetricLength(getNumber("length"));
    const width = toMetricLength(getNumber("width"));
    const depth = toMetricDepth(getNumber("depth"));
    const waste = getNumber("waste") / 100;
    const density = getNumber("density");
    const bagSize = getNumber("bag-size");
    const pricePerTonne = getNumber("price-per-tonne");
    const area = length * width;
    const volume = area * depth;
    const totalVolume = volume * (1 + waste);
    const tonnes = totalVolume * density;
    const bags = bagSize > 0 ? tonnes / bagSize : 0;
    const estimatedCost = tonnes * pricePerTonne;
    resultMain.textContent = tonnes > 0 ? `${tonnes.toFixed(2)} tonnes of ${labelForMode()}` : "Enter your measurements";
    resultSub.textContent = tonnes > 0 ? `That is about ${bags.toFixed(1)} bulk bags and roughly ${money(estimatedCost)} in material cost.` : "You will see the area, volume, tonnage, bulk bag estimate and rough cost here.";
    resultBreakdown.innerHTML = tonnes > 0 ? `
      <div class="break-row"><span>Area</span><strong>${area.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Loose volume</span><strong>${volume.toFixed(3)} m³</strong></div>
      <div class="break-row"><span>Volume incl. waste</span><strong>${totalVolume.toFixed(3)} m³</strong></div>
      <div class="break-row"><span>Estimated weight</span><strong>${tonnes.toFixed(2)} tonnes</strong></div>
      <div class="break-row"><span>Bulk bags</span><strong>${bags.toFixed(1)}</strong></div>
      <div class="break-row"><span>Price per tonne</span><strong>${money(pricePerTonne)}</strong></div>
      <div class="break-row"><span>Estimated material cost</span><strong>${money(estimatedCost)}</strong></div>
      <div class="calc-note">Calculation: length × width × depth, then waste allowance and density applied.</div>
    ` : "";
  });
  applyPreset();
})();
