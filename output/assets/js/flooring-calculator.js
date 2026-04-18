(function () {
  const form = document.getElementById("flooring-form");
  if (!form) return;

  const modeButtons = Array.from(document.querySelectorAll(".mode-toggle"));
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const currencyButtons = Array.from(document.querySelectorAll(".currency-pill"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  const resultContext = document.getElementById("result-context");
  const roomLengthLabel = document.getElementById("room-length-label");
  const roomWidthLabel = document.getElementById("room-width-label");
  const intelligence = window.BuildCostLabCostIntel;

  const currencyMap = {
    GBP: { symbol: "\u00A3", code: "GBP" },
    USD: { symbol: "$", code: "USD" },
    EUR: { symbol: "\u20AC", code: "EUR" }
  };

  let mode = "laminate";
  let unit = "metric";
  let currency = "GBP";

  const presets = {
    laminate: { waste: 8, packCoverage: 1.84, pricePerPack: 29.99, plankWidth: 192, plankLength: 1285 },
    wood: { waste: 10, packCoverage: 1.6, pricePerPack: 54.0, plankWidth: 150, plankLength: 1900 },
    vinyl: { waste: 6, packCoverage: 2.2, pricePerPack: 39.99, plankWidth: 180, plankLength: 1220 }
  };

  function money(value) {
    const info = currencyMap[currency] || currencyMap.GBP;
    return `${info.symbol}${Number(value).toFixed(2)} ${info.code}`;
  }

  function formatArea(value) {
    const squareFeet = value * 10.7639;
    return `${value.toFixed(2)} m2 (${squareFeet.toFixed(1)} sq ft)`;
  }

  function formatLength(valueMetres) {
    const feet = valueMetres * 3.28084;
    return `${valueMetres.toFixed(2)} m (${feet.toFixed(1)} ft)`;
  }

  function setActive(buttons, key, value) {
    buttons.forEach(function (button) {
      button.classList.toggle("is-active", button.dataset[key] === value);
    });
  }

  function getNumber(id) {
    const field = document.getElementById(id);
    const value = field ? parseFloat(field.value) : 0;
    return Number.isFinite(value) ? value : 0;
  }

  function lengthInMetres(rawLength) {
    return unit === "metric" ? rawLength : rawLength * 0.3048;
  }

  function flooringTimeline(area) {
    if (area < 20) {
      return [
        { stage: "Prep and acclimatise", duration: "Half day" },
        { stage: "Lay boards or planks", duration: "Half day to 1 day" },
        { stage: "Trims and snagging", duration: "Half day" }
      ];
    }
    if (area < 50) {
      return [
        { stage: "Prep and acclimatise", duration: "Half day to 1 day" },
        { stage: "Lay boards or planks", duration: "1 to 2 days" },
        { stage: "Trims and snagging", duration: "Half day to 1 day" }
      ];
    }
    return [
      { stage: "Prep and acclimatise", duration: "1 day" },
      { stage: "Lay boards or planks", duration: "2 to 3 days" },
      { stage: "Trims and snagging", duration: "1 day" }
    ];
  }

  function applyPreset() {
    const preset = presets[mode];
    document.getElementById("waste").value = preset.waste;
    document.getElementById("pack-coverage").value = preset.packCoverage;
    document.getElementById("price-per-pack").value = preset.pricePerPack;
    document.getElementById("plank-width").value = preset.plankWidth;
    document.getElementById("plank-length").value = preset.plankLength;
  }

  function modeLabel() {
    if (mode === "wood") return "wood flooring";
    if (mode === "vinyl") return "vinyl plank flooring";
    return "laminate flooring";
  }

  function updateUnitLabels() {
    const lengthUnit = unit === "metric" ? "m" : "ft";
    if (roomLengthLabel) roomLengthLabel.textContent = `Room length (${lengthUnit})`;
    if (roomWidthLabel) roomWidthLabel.textContent = `Room width (${lengthUnit})`;
  }

  function modeContext() {
    if (mode === "wood") {
      return {
        driverText: "Board width, room width, visible joins, waste allowance, and the decision to keep matching boards are the main levers on wood flooring estimates.",
        confidenceText: "Use the higher estimate when the room has several openings, you want cleaner long-board runs, or the subfloor still needs more prep than expected.",
        comparisonProfiles: [
          { label: "Budget wood route", note: "Entry engineered boards and leaner extras.", material: 0.88, labour: 0.95, extras: 0.94, fees: 0.98 },
          { label: "Standard wood route", note: "Typical domestic engineered-wood spec.", material: 1, labour: 1, extras: 1, fees: 1 },
          { label: "Higher-spec wood route", note: "Better finish boards, added prep, and safer spare stock.", material: 1.28, labour: 1.08, extras: 1.1, fees: 1.03 }
        ],
        realityItems: [
          "Underlay, vapour control, thresholds, and trims often sit outside the first wood pack total.",
          "Longer boards can reduce joins, but they can also increase visible waste in awkward rooms.",
          "Subfloor flatness and acclimatisation rules can shift the real job cost more than one extra pack.",
          "Matching boards later can be difficult, so spare stock is often worth budgeting for up front."
        ]
      };
    }
    if (mode === "vinyl") {
      return {
        driverText: "Room shape, plank direction, waste around thresholds, and underlay or acoustic-layer choice are the main levers on vinyl plank estimates.",
        confidenceText: "Use the higher estimate when the room has several doorways, linked spaces, or you need extra planks for tricky cuts and future repairs.",
        comparisonProfiles: [
          { label: "Budget vinyl route", note: "Lower-cost click or glue-down pack route.", material: 0.87, labour: 0.93, extras: 0.93, fees: 0.97 },
          { label: "Standard vinyl route", note: "Typical domestic vinyl plank install.", material: 1, labour: 1, extras: 1, fees: 1 },
          { label: "Higher-spec vinyl route", note: "Better wear layer, extras, and a safer spare-plank allowance.", material: 1.22, labour: 1.04, extras: 1.08, fees: 1.02 }
        ],
        realityItems: [
          "Thresholds, edge trims, and acoustic or moisture layers can sit outside the first vinyl pack total.",
          "Linked room layouts can create more waste than one simple rectangle suggests.",
          "Some vinyl routes still need prep or smoothing work before the visible finish is laid.",
          "A same-batch spare pack is often easier to justify than trying to match planks later."
        ]
      };
    }
    return {
      driverText: "Room shape, board direction, cut-heavy edges, pack coverage, and whether you keep a same-batch spare pack are the main levers on laminate estimates.",
      confidenceText: "Use the higher estimate when the room links into a hall, has angled walls or alcoves, or you want a same-batch spare for later repairs.",
      comparisonProfiles: [
        { label: "Budget laminate", note: "Entry-level boards and a simpler fitting allowance.", material: 0.85, labour: 0.9, extras: 0.9, fees: 0.9 },
        { label: "Standard laminate", note: "Typical domestic flooring spec.", material: 1, labour: 1, extras: 1, fees: 1 },
        { label: "Higher-spec laminate", note: "Better wear layer, extra prep, and more cautious spares.", material: 1.24, labour: 1.05, extras: 1.08, fees: 1.02 }
      ],
      realityItems: [
        "Underlay, trims, thresholds, and matching scotia are often missed from the first laminate basket.",
        "Visible cut-heavy rooms often need more spare than the neat area suggests, especially near bays, hearths, or hall links.",
        "A same-batch spare pack can be easier to justify than trying to match the floor later.",
        "Subfloor levelling and door clearance adjustments can shift the real job cost more than one extra pack."
      ]
    };
  }

  function renderDefaultState() {
    resultMain.textContent = "Enter your measurements";
    resultSub.textContent = "You will see the room area, pack count, approximate board count, and wider buying guidance here.";
    resultBreakdown.innerHTML = "";
    if (resultContext) {
      resultContext.textContent = "";
    }
    if (intelligence) intelligence.clear();
  }

  function calculate(event) {
    if (event) event.preventDefault();

    const roomLength = lengthInMetres(getNumber("room-length"));
    const roomWidth = lengthInMetres(getNumber("room-width"));
    const area = roomLength * roomWidth;
    const waste = Math.max(getNumber("waste"), 0) / 100;
    const packCoverage = Math.max(getNumber("pack-coverage"), 0.01);
    const pricePerPack = Math.max(getNumber("price-per-pack"), 0);
    const plankWidth = Math.max(getNumber("plank-width"), 1) / 1000;
    const plankLength = Math.max(getNumber("plank-length"), 1) / 1000;

    const totalArea = area * (1 + waste);
    const boardArea = plankWidth * plankLength;
    const approximateBoards = Math.ceil(totalArea / boardArea);
    const rows = Math.max(1, Math.ceil(roomWidth / plankWidth));
    const boardsPerRow = Math.max(1, Math.ceil(roomLength / plankLength));
    const packs = Math.ceil(totalArea / packCoverage);
    const estimatedCost = packs * pricePerPack;

    if (!(packs > 0)) {
      renderDefaultState();
      return;
    }

    resultMain.textContent = `${packs} packs of ${modeLabel()}`;
    resultSub.textContent = `That covers about ${formatArea(totalArea)} including waste and roughly ${money(estimatedCost)} in ${modeLabel()} cost.`;
    resultBreakdown.innerHTML =
      `<div class="break-row"><span>Room size</span><strong>${formatLength(roomLength)} x ${formatLength(roomWidth)}</strong></div>` +
      `<div class="break-row"><span>Floor area</span><strong>${formatArea(area)}</strong></div>` +
      `<div class="break-row"><span>Area incl. waste</span><strong>${formatArea(totalArea)}</strong></div>` +
      `<div class="break-row"><span>Approx. board area</span><strong>${boardArea.toFixed(3)} m2</strong></div>` +
      `<div class="break-row"><span>Approx. boards or planks</span><strong>${approximateBoards}</strong></div>` +
      `<div class="break-row"><span>Approx. layout check</span><strong>${rows} rows x ${boardsPerRow} boards</strong></div>` +
      `<div class="break-row"><span>Coverage per pack</span><strong>${packCoverage.toFixed(2)} m2</strong></div>` +
      `<div class="break-row"><span>Packs needed</span><strong>${packs}</strong></div>` +
      `<div class="break-row"><span>Price per pack</span><strong>${money(pricePerPack)}</strong></div>` +
      `<div class="break-row"><span>Estimated material cost</span><strong>${money(estimatedCost)}</strong></div>` +
      `<div class="calc-note">Calculation: room length x width, then waste is added and rounded up to full packs. Board count is an approximate sense-check, not a cutting plan.</div>`;
    if (resultContext) {
      resultContext.textContent = "Check pack coverage against the exact board format, add a sensible spare-pack allowance for future repairs, and review underlay, trims, thresholds, and room transitions before treating the first total as your full order.";
    }

    if (intelligence) {
      const context = modeContext();
      intelligence.render({
        formula: "coverage",
        materialCost: estimatedCost,
        quantity: packs,
        quantitySuffix: "packs",
        quantityDecimals: 0,
        scopeValue: totalArea,
        driverText: context.driverText,
        confidenceText: context.confidenceText,
        comparisonProfiles: context.comparisonProfiles,
        costModel: { labour: 0.48, extras: 0.16, fees: 0.04 },
        realityItems: context.realityItems,
        timelineSteps: flooringTimeline(totalArea),
        money: money,
        formatQuantity: function (value) {
          return `${Math.max(1, Math.round(value))}`;
        }
      });
    }
  }

  modeButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      mode = button.dataset.mode || "laminate";
      setActive(modeButtons, "mode", mode);
      applyPreset();
      calculate();
    });
  });

  unitButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      unit = button.dataset.unit || "metric";
      setActive(unitButtons, "unit", unit);
      updateUnitLabels();
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

  updateUnitLabels();
  applyPreset();
  calculate();
})();
