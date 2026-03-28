(function () {
  const form = document.getElementById("paint-form");
  if (!form) return;

  const modeButtons = Array.from(document.querySelectorAll(".mode-toggle"));
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const currencyButtons = Array.from(document.querySelectorAll(".currency-pill"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");

  const currencyMap = {
    GBP: { symbol: "GBP £", rate: 1 },
    USD: { symbol: "USD $", rate: 1.27 },
    EUR: { symbol: "EUR €", rate: 1.17 },
  };

  let mode = "walls";
  let unit = "metric";
  let currency = "GBP";

  function getNumber(id) {
    const field = document.getElementById(id);
    const value = field ? parseFloat(field.value) : 0;
    return Number.isFinite(value) ? value : 0;
  }

  function formatMoney(value) {
    const info = currencyMap[currency] || currencyMap.GBP;
    return `${info.symbol} ${(value * info.rate).toFixed(2)}`;
  }

  function setActive(buttons, key, value) {
    buttons.forEach(function (button) {
      button.classList.toggle("is-active", button.dataset[key] === value);
    });
  }

  function toMetricLength(value) {
    return unit === "metric" ? value : value * 0.3048;
  }

  function currentArea(length, width, height) {
    if (mode === "ceiling") {
      return length * width;
    }
    if (mode === "single") {
      return length * height;
    }
    return (2 * (length + width)) * height;
  }

  function modeLabel() {
    if (mode === "ceiling") return "ceiling area";
    if (mode === "single") return "single surface";
    return "wall area";
  }

  function calculate(event) {
    if (event) event.preventDefault();

    const length = toMetricLength(getNumber("length"));
    const width = toMetricLength(getNumber("width"));
    const height = toMetricLength(getNumber("height"));
    const coats = Math.max(getNumber("coats"), 1);
    const coverage = Math.max(getNumber("coverage"), 0.1);
    const waste = Math.max(getNumber("waste"), 0);
    const pricePerLitre = Math.max(getNumber("price-per-litre"), 0);

    const baseArea = currentArea(length, width, height);
    const adjustedArea = baseArea * coats * (1 + waste / 100);
    const litres = adjustedArea / coverage;
    const estimatedCost = litres * pricePerLitre;

    if (!(litres > 0)) {
      resultMain.textContent = "Enter your measurements";
      resultSub.textContent = "You will see the painted area, litres, tin suggestion and rough material cost here.";
      resultBreakdown.innerHTML = "";
      return;
    }

    const tenLitreTins = Math.floor(litres / 10);
    const remainderAfterTen = litres - (tenLitreTins * 10);
    const fiveLitreTins = Math.floor(remainderAfterTen / 5);
    const topUpLitres = Math.max(remainderAfterTen - (fiveLitreTins * 5), 0);

    resultMain.textContent = `${litres.toFixed(2)} litres of paint`;
    resultSub.textContent = `That covers about ${adjustedArea.toFixed(2)} m² across ${coats} coat(s), with a rough material cost of ${formatMoney(estimatedCost)}.`;
    resultBreakdown.innerHTML = `
      <div class="break-row"><span>Estimated ${modeLabel()}</span><strong>${baseArea.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Area incl. coats and waste</span><strong>${adjustedArea.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Coverage per litre</span><strong>${coverage.toFixed(2)} m²/L</strong></div>
      <div class="break-row"><span>Paint needed</span><strong>${litres.toFixed(2)} litres</strong></div>
      <div class="break-row"><span>Price per litre</span><strong>${formatMoney(pricePerLitre)}</strong></div>
      <div class="break-row"><span>Estimated material cost</span><strong>${formatMoney(estimatedCost)}</strong></div>
      <div class="calc-note">Suggested buying mix: ${tenLitreTins ? `${tenLitreTins} × 10L` : "0 × 10L"}${fiveLitreTins ? `, ${fiveLitreTins} × 5L` : ""}${topUpLitres > 0.05 ? `, plus a small top-up tin` : ""}.</div>
    `;
  }

  modeButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      mode = button.dataset.mode || "walls";
      setActive(modeButtons, "mode", mode);
      calculate();
    });
  });

  unitButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      unit = button.dataset.unit || "metric";
      setActive(unitButtons, "unit", unit);
      calculate();
    });
  });

  currencyButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      currency = button.dataset.currency || "GBP";
      setActive(currencyButtons, "currency", currency);
      calculate();
    });
  });

  form.addEventListener("submit", calculate);
  form.querySelectorAll("input").forEach(function (input) {
    input.addEventListener("input", calculate);
  });

  calculate();
})();
