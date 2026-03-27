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
  }const form = document.getElementById("flooring-form");
  if (!form) return;
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  let unit = "metric";
  function setActive(buttons, value) { buttons.forEach((btn) => btn.classList.toggle("is-active", btn.dataset.unit === value)); }
  function getNumber(id) { const v = parseFloat(document.getElementById(id).value); return Number.isFinite(v) ? v : 0; }
  function toMetricLength(v) { return unit === "metric" ? v : v * 0.3048; }
  unitButtons.forEach((btn) => btn.addEventListener("click", function () { unit = btn.dataset.unit; setActive(unitButtons, unit); }));
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const roomAreaInput = getNumber("room-area");
    const waste = getNumber("waste") / 100;
    const packCoverage = getNumber("pack-coverage");
    const pricePerPack = getNumber("price-per-pack");
    const area = unit === "metric" ? roomAreaInput : roomAreaInput * 0.092903;
    const totalArea = area * (1 + waste);
    const packs = packCoverage > 0 ? Math.ceil(totalArea / packCoverage) : 0;
    const estimatedCost = packs * pricePerPack;
    resultMain.textContent = packs > 0 ? `${packs} packs of flooring` : "Enter your measurements";
    resultSub.textContent = packs > 0 ? `That covers about ${totalArea.toFixed(2)} m² including waste and roughly ${money(estimatedCost)} in flooring cost.` : "You will see the floor area, packs needed and rough material cost here.";
    resultBreakdown.innerHTML = packs > 0 ? `
      <div class="break-row"><span>Floor area</span><strong>${area.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Area incl. waste</span><strong>${totalArea.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Coverage per pack</span><strong>${packCoverage.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Packs needed</span><strong>${packs}</strong></div>
      <div class="break-row"><span>Price per pack</span><strong>${money(pricePerPack)}</strong></div>
      <div class="break-row"><span>Estimated material cost</span><strong>${money(estimatedCost)}</strong></div>
      <div class="calc-note">Calculation: room area plus waste allowance, then rounded up to full packs.</div>
    ` : "";
  });
})();
