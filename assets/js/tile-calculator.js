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
  }const form = document.getElementById("tile-form");
  if (!form) return;
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  let unit = "metric";
  function setActive(buttons, value) { buttons.forEach((btn) => btn.classList.toggle("is-active", btn.dataset.unit === value)); }
  function getNumber(id) { const v = parseFloat(document.getElementById(id).value); return Number.isFinite(v) ? v : 0; }
  function toMetricLength(v) { return unit === "metric" ? v : v * 0.3048; }
  function tileDimensionToMetres(v) { return unit === "metric" ? v / 1000 : v * 0.0254; }
  unitButtons.forEach((btn) => btn.addEventListener("click", function () { unit = btn.dataset.unit; setActive(unitButtons, unit); }));
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const length = toMetricLength(getNumber("length"));
    const width = toMetricLength(getNumber("width"));
    const tileLength = tileDimensionToMetres(getNumber("tile-length"));
    const tileWidth = tileDimensionToMetres(getNumber("tile-width"));
    const tilesPerBox = getNumber("tiles-per-box");
    const waste = getNumber("waste") / 100;
    const pricePerBox = getNumber("price-per-box");
    const area = length * width;
    const tileArea = tileLength * tileWidth;
    const tileCount = tileArea > 0 ? Math.ceil((area / tileArea) * (1 + waste)) : 0;
    const boxes = tilesPerBox > 0 ? Math.ceil(tileCount / tilesPerBox) : 0;
    const estimatedCost = boxes * pricePerBox;
    resultMain.textContent = tileCount > 0 ? `${tileCount} tiles needed` : "Enter your measurements";
    resultSub.textContent = tileCount > 0 ? `That works out to about ${boxes} boxes and roughly ${money(estimatedCost)} in tile cost.` : "You will see the tiled area, tile count, boxes needed and rough material cost here.";
    resultBreakdown.innerHTML = tileCount > 0 ? `
      <div class="break-row"><span>Tiled area</span><strong>${area.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Tile face area</span><strong>${tileArea.toFixed(3)} m²</strong></div>
      <div class="break-row"><span>Tiles needed</span><strong>${tileCount}</strong></div>
      <div class="break-row"><span>Boxes needed</span><strong>${boxes}</strong></div>
      <div class="break-row"><span>Price per box</span><strong>${money(pricePerBox)}</strong></div>
      <div class="break-row"><span>Estimated material cost</span><strong>${money(estimatedCost)}</strong></div>
      <div class="calc-note">Calculation: area ÷ single tile area, then waste added and rounded to full boxes.</div>
    ` : "";
  });
})();
