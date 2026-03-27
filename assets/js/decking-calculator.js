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
  }const form = document.getElementById("decking-form");
  if (!form) return;
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  let unit = "metric";
  function setActive(buttons, value) { buttons.forEach((btn) => btn.classList.toggle("is-active", btn.dataset.unit === value)); }
  function getNumber(id) { const v = parseFloat(document.getElementById(id).value); return Number.isFinite(v) ? v : 0; }
  function toMetricLength(v) { return unit === "metric" ? v : v * 0.3048; }
  function boardWidthToMetres(v) { return unit === "metric" ? v / 1000 : v * 0.0254; }
  function spacingToMetres(v) { return unit === "metric" ? v / 1000 : v * 0.0254; }
  unitButtons.forEach((btn) => btn.addEventListener("click", function () { unit = btn.dataset.unit; setActive(unitButtons, unit); }));
  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const length = toMetricLength(getNumber("length"));
    const width = toMetricLength(getNumber("width"));
    const boardWidth = boardWidthToMetres(getNumber("board-width"));
    const boardLength = toMetricLength(getNumber("board-length"));
    const joistSpacing = spacingToMetres(getNumber("joist-spacing"));
    const waste = getNumber("waste") / 100;
    const pricePerBoard = getNumber("price-per-board");
    const pricePerJoist = getNumber("price-per-joist");
    const area = length * width;
    const boardCoverage = boardWidth * boardLength;
    const boards = boardCoverage > 0 ? Math.ceil((area / boardCoverage) * (1 + waste)) : 0;
    const joists = joistSpacing > 0 ? Math.ceil(width / joistSpacing) + 1 : 0;
    const estimatedCost = (boards * pricePerBoard) + (joists * pricePerJoist);
    resultMain.textContent = boards > 0 ? `${boards} decking boards` : "Enter your measurements";
    resultSub.textContent = boards > 0 ? `You will likely need about ${joists} joists as well, with a rough material cost of ${money(estimatedCost)}.` : "You will see deck area, boards, joists and rough material cost here.";
    resultBreakdown.innerHTML = boards > 0 ? `
      <div class="break-row"><span>Deck area</span><strong>${area.toFixed(2)} m²</strong></div>
      <div class="break-row"><span>Single board coverage</span><strong>${boardCoverage.toFixed(3)} m²</strong></div>
      <div class="break-row"><span>Boards needed</span><strong>${boards}</strong></div>
      <div class="break-row"><span>Estimated joists</span><strong>${joists}</strong></div>
      <div class="break-row"><span>Price per board</span><strong>${money(pricePerBoard)}</strong></div>
      <div class="break-row"><span>Price per joist</span><strong>${money(pricePerJoist)}</strong></div>
      <div class="break-row"><span>Estimated material cost</span><strong>${money(estimatedCost)}</strong></div>
      <div class="calc-note">Calculation: deck area ÷ board coverage, then waste added. Joists estimated from deck width and joist spacing.</div>
    ` : "";
  });
})();
