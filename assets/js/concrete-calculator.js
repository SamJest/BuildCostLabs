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
  }const form = document.getElementById("concrete-form");
  if (!form) return;
  const modeButtons = Array.from(document.querySelectorAll(".mode-toggle"));
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  let mode = "slab";
  let unit = "metric";
  const presets = { slab: { depthMetric: 0.1, depthImperial: 4, waste: 10, price: 140 }, footing: { depthMetric: 0.3, depthImperial: 12, waste: 10, price: 145 }, post: { depthMetric: 0.6, depthImperial: 24, waste: 12, price: 150 } };
  function setActive(buttons, value) { buttons.forEach((btn) => btn.classList.toggle("is-active", btn.dataset.mode === value || btn.dataset.unit === value)); }
  function applyPreset() { const p = presets[mode]; document.getElementById("depth").value = unit === "metric" ? p.depthMetric : p.depthImperial; document.getElementById("waste").value = p.waste; document.getElementById("price-per-m3").value = p.price; }
  function getNumber(id) { const v = parseFloat(document.getElementById(id).value); return Number.isFinite(v) ? v : 0; }
  function toMetricLength(v) { return unit === "metric" ? v : v * 0.3048; }
  function toMetricDepth(v) { return unit === "metric" ? v : v * 0.0254; }
  modeButtons.forEach((btn) => btn.addEventListener("click", function () { mode = btn.dataset.mode; setActive(modeButtons, mode); applyPreset(); }));
  unitButtons.forEach((btn) => btn.addEventListener("click", function () { unit = btn.dataset.unit; setActive(unitButtons, unit); applyPreset(); }));
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const length = toMetricLength(getNumber("length"));
    const width = toMetricLength(getNumber("width"));
    const depth = toMetricDepth(getNumber("depth"));
    const count = getNumber("count");
    const waste = getNumber("waste") / 100;
    const pricePerM3 = getNumber("price-per-m3");
    let volume = mode === "post" ? length * width * depth * count : length * width * depth;
    const totalVolume = volume * (1 + waste);
    const estimatedCost = totalVolume * pricePerM3;
    resultMain.textContent = totalVolume > 0 ? `${totalVolume.toFixed(3)} m³ of concrete` : "Enter your measurements";
    resultSub.textContent = totalVolume > 0 ? `That is the estimated pour volume including waste, with a rough material cost of ${money(estimatedCost)}.` : "You will see the concrete volume and rough material cost here.";
    resultBreakdown.innerHTML = totalVolume > 0 ? `
      <div class="break-row"><span>Base volume</span><strong>${volume.toFixed(3)} m³</strong></div>
      <div class="break-row"><span>Volume incl. waste</span><strong>${totalVolume.toFixed(3)} m³</strong></div>
      <div class="break-row"><span>Price per m³</span><strong>${money(pricePerM3)}</strong></div>
      <div class="break-row"><span>Estimated material cost</span><strong>${money(estimatedCost)}</strong></div>
      <div class="calc-note">Calculation: length × width × depth, then waste added. Post hole mode multiplies by the number of holes.</div>
    ` : "";
  });
  applyPreset();
})();
