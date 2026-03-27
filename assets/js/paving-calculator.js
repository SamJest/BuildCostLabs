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
    currencyButtons.forEach((btn) => btn.classList.toggle("is-active", btn.dataset.currency === next));
  }
  currencyButtons.forEach((btn) => btn.addEventListener("click", function () {
    setCurrency(btn.dataset.currency);
  }));
  function money(value) {
    const info = currencyMap[currency] || currencyMap.GBP;
    return `${info.symbol}${Number(value).toFixed(2)} ${info.code}`;
  }const form = document.getElementById("paving-form");
  if (!form) return;
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  let unit = "metric";

  function setActive(buttons, value) {
    buttons.forEach((btn) => btn.classList.toggle("is-active", btn.dataset.unit === value));
  }
  function getNumber(id) {
    const v = parseFloat(document.getElementById(id).value);
    return Number.isFinite(v) ? v : 0;
  }
  function toMetricLength(v) {
    return unit === "metric" ? v : v * 0.3048;
  }
  function slabDimensionToMetres(v) {
    return unit === "metric" ? v / 1000 : v * 0.0254;
  }

  unitButtons.forEach((btn) => btn.addEventListener("click", function () {
    unit = btn.dataset.unit;
    setActive(unitButtons, unit);
  }));

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const length = toMetricLength(getNumber("length"));
    const width = toMetricLength(getNumber("width"));
    const slabLength = slabDimensionToMetres(getNumber("slab-length"));
    const slabWidth = slabDimensionToMetres(getNumber("slab-width"));
    const slabsPerPack = getNumber("slabs-per-pack");
    const waste = getNumber("waste") / 100;
    const pricePerSlab = getNumber("price-per-slab");

    const area = length * width;
    const slabArea = slabLength * slabWidth;
    const slabCount = slabArea > 0 ? Math.ceil((area / slabArea) * (1 + waste)) : 0;
    const packs = slabsPerPack > 0 ? Math.ceil(slabCount / slabsPerPack) : 0;
    const estimatedCost = slabCount * pricePerSlab;

    resultMain.textContent = slabCount > 0 ? `${slabCount} paving slabs` : "Enter your measurements";
    resultSub.textContent = slabCount > 0
      ? `That works out to about ${packs} packs and roughly ${money(estimatedCost)} in slab cost.`
      : "You will see the paved area, slab count, packs needed and rough material cost here.";

    resultBreakdown.innerHTML = slabCount > 0 ? `
      <div class="break-row"><span>Paved area</span><strong>${area.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Single slab area</span><strong>${slabArea.toFixed(3)} m²</strong></div>
      <div class="break-row"><span>Slabs needed</span><strong>${slabCount}</strong></div>
      <div class="break-row"><span>Packs needed</span><strong>${packs}</strong></div>
      <div class="break-row"><span>Price per slab</span><strong>${money(pricePerSlab)}</strong></div>
      <div class="break-row"><span>Estimated material cost</span><strong>${money(estimatedCost)}</strong></div>
      <div class="calc-note">Calculation: area ÷ single slab area, then waste added and rounded to full slabs and packs.</div>
    ` : "";
  });
})();
