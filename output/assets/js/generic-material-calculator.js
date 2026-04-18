(function () {
  const config = window.__calculatorConfig || { formula: "coverage", name: "Material" };
  const form = document.querySelector(".generic-calculator-form");
  if (!form) return;

  const currencyMap = {
    GBP: { symbol: "\u00A3", code: "GBP" },
    USD: { symbol: "$", code: "USD" },
    EUR: { symbol: "\u20AC", code: "EUR" }
  };

  let currency = "GBP";
  let unit = "metric";

  const currencyButtons = Array.from(document.querySelectorAll(".currency-pill"));
  const unitButtons = Array.from(document.querySelectorAll(".unit-toggle"));
  const resultMain = document.querySelector(".result-main");
  const resultSub = document.querySelector(".result-sub");
  const resultBreakdown = document.getElementById("result-breakdown");
  const resultContext = document.getElementById("result-context");
  const intelligence = window.BuildCostLabCostIntel;

  function unitLabel(count) {
    return count === 1 ? (config.unitNameSingular || "unit") : (config.unitNamePlural || "units");
  }

  function money(value) {
    const info = currencyMap[currency] || currencyMap.GBP;
    return `${info.symbol}${Number(value).toFixed(2)} ${info.code}`;
  }

  function formatArea(value) {
    const squareFeet = value * 10.7639;
    return `${value.toFixed(2)} m2 (${squareFeet.toFixed(1)} sq ft)`;
  }

  function formatLength(value) {
    const feet = value * 3.28084;
    return `${value.toFixed(2)} m (${feet.toFixed(1)} ft)`;
  }

  function formatVolume(value) {
    const cubicFeet = value * 35.3147;
    return `${value.toFixed(3)} m3 (${cubicFeet.toFixed(1)} cu ft)`;
  }

  function formatWeightTonnes(value) {
    return `${value.toFixed(2)} t (${Math.round(value * 1000)} kg)`;
  }

  function getNumber(id) {
    const el = document.getElementById(id);
    if (!el) return 0;
    const value = parseFloat(el.value);
    return Number.isFinite(value) ? value : 0;
  }

  function getValue(id) {
    const el = document.getElementById(id);
    return el ? String(el.value || "") : "";
  }

  function toMetricLength(value) {
    return unit === "metric" ? value : value * 0.3048;
  }

  function setActive(buttons, matcher) {
    buttons.forEach(function (button) {
      button.classList.toggle("is-active", matcher(button));
    });
  }

  function getRegionProfile() {
    const profiles = Array.isArray(config.regionProfiles) ? config.regionProfiles : [];
    const selected = getValue("region") || config.defaultRegion || "national-average";
    const fallback = {
      slug: "national-average",
      label: "UK average",
      materials: 1,
      labour: 1,
      extras: 1,
      summary: "Neutral planning baseline",
      note: "Use this as a national-average planning range when the location is still fluid."
    };
    return profiles.find(function (profile) {
      return profile.slug === selected;
    }) || fallback;
  }

  function setContext(text) {
    if (!resultContext) return;
    resultContext.textContent = text || "";
  }

  function starterBreakdown() {
    if (config.formula === "project_cost") {
      const region = getRegionProfile();
      const area = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width"));
      return (
        `<div class="break-row"><span>Starter area</span><strong>${area.toFixed(2)} m2</strong></div>` +
        `<div class="break-row"><span>Region baseline</span><strong>${region.label}</strong></div>` +
        `<div class="break-row"><span>What this is for</span><strong>Fast budget benchmark before quote comparison</strong></div>`
      );
    }
    if (config.formula === "volume") {
      const volume = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width")) * toMetricLength(getNumber("depth"));
      return (
        `<div class="break-row"><span>Starter volume</span><strong>${formatVolume(volume)}</strong></div>` +
        `<div class="break-row"><span>Buying route</span><strong>${config.unitNamePlural || "units"} with waste already loaded</strong></div>` +
        `<div class="break-row"><span>What to change first</span><strong>Depth, density, and unit size</strong></div>`
      );
    }
    if (config.formula === "linear") {
      const run = toMetricLength(getNumber("length"));
      return (
        `<div class="break-row"><span>Starter run length</span><strong>${formatLength(run)}</strong></div>` +
        `<div class="break-row"><span>Buying route</span><strong>Whole stock lengths with waste already loaded</strong></div>` +
        `<div class="break-row"><span>What to change first</span><strong>Total run, piece length, and cut waste</strong></div>`
      );
    }
    const area = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width"));
    return (
      `<div class="break-row"><span>Starter area</span><strong>${formatArea(area)}</strong></div>` +
      `<div class="break-row"><span>Buying route</span><strong>${config.unitNamePlural || "units"} using the loaded coverage rate</strong></div>` +
      `<div class="break-row"><span>What to change first</span><strong>Coverage, waste, and price per unit</strong></div>`
    );
  }

  function renderDefaultState() {
    resultMain.textContent = "Starter scenario ready";
    resultSub.textContent = "The form is preloaded with a benchmark example. Adjust the inputs to match the real job or use the starter setup for a quick estimate.";
    resultBreakdown.innerHTML = starterBreakdown();
    setContext(config.formula === "project_cost" ? "Choose a UK region to apply a location-weighted planning range before you rely on the benchmark." : "Use the starter inputs as a benchmark, then update the numbers for the real site conditions.");
    if (intelligence) intelligence.clear({
      formula: config.formula,
      name: config.name,
      money: money,
      coverageMode: config.coverageMode,
      unitNameSingular: config.unitNameSingular,
      unitNamePlural: config.unitNamePlural,
      currentInputs: {
        length: getNumber("length"),
        width: getNumber("width"),
        depth: getNumber("depth"),
        density: getNumber("density"),
        unitSize: getNumber("unit-size"),
        waste: getNumber("waste"),
        pricePerUnit: getNumber("price-per-unit"),
        coveragePerUnit: getNumber("coverage-per-unit"),
        pieceLength: getNumber("piece-length"),
        materialRate: getNumber("material-rate"),
        labourRate: getNumber("labour-rate"),
        extraRate: getNumber("extra-rate"),
        contingency: getNumber("contingency"),
        regionLabel: getRegionProfile().label,
        regionNote: getRegionProfile().note,
        regionSummary: getRegionProfile().summary,
        regionMaterials: getRegionProfile().materials,
        regionLabour: getRegionProfile().labour,
        regionExtras: getRegionProfile().extras
      }
    });
  }

  function renderIntelligence(payload) {
    if (!intelligence) return;
    intelligence.render({
      formula: config.formula,
      materialCost: payload.materialCost,
      quantity: payload.quantity,
      quantitySuffix: payload.quantitySuffix,
      quantityDecimals: payload.quantityDecimals,
      scopeValue: payload.scopeValue,
      driverText: payload.driverText || config.driverText,
      confidenceText: payload.confidenceText || config.confidenceText,
      comparisonProfiles: payload.comparisonProfiles || (config.comparisonProfiles && config.comparisonProfiles.length ? config.comparisonProfiles : []),
      realityItems: payload.realityItems || (config.realityItems && config.realityItems.length ? config.realityItems : []),
      costModel: payload.costModel || config.costModel,
      timelineSteps: payload.timelineSteps || (config.timelineSteps && config.timelineSteps.length ? config.timelineSteps : []),
      money: money,
      formatQuantity: payload.formatQuantity
    });
  }

  function calculate() {
    const wasteFactor = 1 + (getNumber("waste") / 100);
    const pricePerUnit = getNumber("price-per-unit");
    let units = 0;

    if (config.formula === "coverage") {
      const area = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width"));
      const coveredArea = area * wasteFactor;
      const coverageRate = getNumber("coverage-per-unit");
      const coverageMode = config.coverageMode || "area_per_unit";
      const exactUnits = coverageRate > 0
        ? (
            coverageMode === "units_per_area"
              ? coveredArea * coverageRate
              : coveredArea / coverageRate
          )
        : 0;
      units = coverageRate > 0
        ? (
            coverageMode === "units_per_area"
              ? Math.ceil(coveredArea * coverageRate)
              : Math.ceil(coveredArea / coverageRate)
          )
        : 0;

      if (!(units > 0)) {
        renderDefaultState();
        return;
      }

      resultMain.textContent = `${units} ${unitLabel(units)}`;
      resultSub.textContent = coverageMode === "units_per_area"
        ? `That is based on about ${formatArea(coveredArea)} after waste and roughly ${money(units * pricePerUnit)} in material cost.`
        : `That covers about ${formatArea(coveredArea)} after waste and roughly ${money(units * pricePerUnit)} in material cost.`;
      const bufferText = coverageMode === "units_per_area"
        ? `${Math.max(0, units - exactUnits).toFixed(2)} ${unitLabel(units)} above the theoretical minimum`
        : formatArea(Math.max(0, (units * coverageRate) - coveredArea));
      resultBreakdown.innerHTML =
        `<div class="break-row"><span>Measured area</span><strong>${formatArea(area)}</strong></div>` +
        `<div class="break-row"><span>Area incl. waste</span><strong>${formatArea(coveredArea)}</strong></div>` +
        `<div class="break-row"><span>${config.coverageLabel || "Coverage per unit"}</span><strong>${coverageRate.toFixed(2)}${coverageMode === "units_per_area" ? "" : " m2"}</strong></div>` +
        `<div class="break-row"><span>Exact units before rounding</span><strong>${exactUnits.toFixed(2)} ${unitLabel(exactUnits)}</strong></div>` +
        `<div class="break-row"><span>Buying total</span><strong>${units} ${unitLabel(units)}</strong></div>` +
        `<div class="break-row"><span>Buffer after rounding</span><strong>${bufferText}</strong></div>` +
        `<div class="break-row"><span>Estimated cost</span><strong>${money(units * pricePerUnit)}</strong></div>` +
        `<div class="calc-note">${coverageMode === "units_per_area" ? "Calculation: area plus waste, then multiplied by the unit rate and rounded to whole buying units." : "Calculation: area plus waste, then rounded to whole buying units by coverage."}</div>`;
      setContext("Round to whole packs, rolls, tins, or sheets, then pressure-test the result against real pack coverage, overlaps, and awkward cuts before ordering.");

      renderIntelligence({
        materialCost: units * pricePerUnit,
        quantity: units,
        quantitySuffix: unitLabel(units),
        quantityDecimals: 0,
        scopeValue: coveredArea,
        driverText: config.driverText || (coverageMode === "units_per_area"
          ? "Unit rate per square metre, waste allowance, openings, and supplier pack breaks are the main levers on this estimate."
          : "Coverage rate, waste allowance, and whole-pack rounding usually change this estimate most."),
        formatQuantity: function (value) {
          return `${Math.max(1, Math.round(value))}`;
        }
      });
      return;
    }

    if (config.formula === "project_cost") {
      const area = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width"));
      const complexityFactor = 1 + (getNumber("waste") / 100);
      const region = getRegionProfile();
      const baseMaterialRate = getNumber("material-rate");
      const baseLabourRate = getNumber("labour-rate");
      const baseExtraRate = getNumber("extra-rate");
      const materialRate = baseMaterialRate * (region.materials || 1);
      const labourRate = baseLabourRate * (region.labour || 1);
      const extraRate = baseExtraRate * (region.extras || 1);
      const contingencyFactor = 1 + (getNumber("contingency") / 100);
      const effectiveArea = area * complexityFactor;

      const baseMaterialCost = effectiveArea * baseMaterialRate;
      const baseLabourCost = effectiveArea * baseLabourRate;
      const baseExtraCost = effectiveArea * baseExtraRate;
      const basePreContingency = baseMaterialCost + baseLabourCost + baseExtraCost;
      const baseTotal = basePreContingency * contingencyFactor;

      const materialCost = effectiveArea * materialRate;
      const labourCost = effectiveArea * labourRate;
      const extraCost = effectiveArea * extraRate;
      const preContingency = materialCost + labourCost + extraCost;
      const total = preContingency * contingencyFactor;
      const regionalDelta = total - baseTotal;
      const regionalDeltaLabel = regionalDelta >= 0 ? `+${money(regionalDelta)}` : `-${money(Math.abs(regionalDelta))}`;

      if (!(effectiveArea > 0) || !(total > 0)) {
        renderDefaultState();
        return;
      }

      resultMain.textContent = money(total);
      resultSub.textContent = `That is based on about ${effectiveArea.toFixed(2)} m2 after complexity in ${region.label}, with roughly ${money(materialCost)} materials, ${money(labourCost)} labour, and ${money(extraCost)} in extras before contingency.`;
      resultBreakdown.innerHTML =
        `<div class="break-row"><span>Estimated scope incl. complexity</span><strong>${effectiveArea.toFixed(2)} m2</strong></div>` +
        `<div class="break-row"><span>Region profile</span><strong>${region.label}</strong></div>` +
        `<div class="break-row"><span>Materials</span><strong>${money(materialCost)}</strong></div>` +
        `<div class="break-row"><span>Labour</span><strong>${money(labourCost)}</strong></div>` +
        `<div class="break-row"><span>Prep and extras</span><strong>${money(extraCost)}</strong></div>` +
        `<div class="break-row"><span>Regional change vs UK average</span><strong>${regionalDeltaLabel}</strong></div>` +
        `<div class="break-row"><span>Planning total incl. contingency</span><strong>${money(total)}</strong></div>` +
        `<div class="calc-note">Calculation: area x complexity, then region-weighted material, labour, and extra allowances, then contingency.</div>`;
      setContext(`${region.label}: ${region.summary}. ${region.note}`);

      const dynamicReality = (config.realityItems && config.realityItems.length ? config.realityItems.slice() : []).concat([region.note]);
      const dynamicTimeline = config.timelineSteps && config.timelineSteps.length ? config.timelineSteps : null;
      renderIntelligence({
        materialCost: materialCost,
        quantity: total,
        quantitySuffix: "planning total",
        quantityDecimals: 2,
        scopeValue: effectiveArea,
        driverText: `${config.driverText || "Labour rate, prep, finish level, waste, and contingency usually move project-cost estimates most."} Selected region: ${region.label}.`,
        confidenceText: `${config.confidenceText || "Use the higher estimate when the finish level, access, or prep scope is still uncertain."} Regional weighting is for planning, not quoting.`,
        costModel: {
          labour: materialCost > 0 ? labourCost / materialCost : 0.75,
          extras: materialCost > 0 ? extraCost / materialCost : 0.2,
          fees: materialCost > 0 ? Math.max(0, total - materialCost - labourCost - extraCost) / materialCost : 0.1
        },
        formatQuantity: function (value) {
          return money(value);
        },
        comparisonProfiles: config.comparisonProfiles,
        realityItems: dynamicReality,
        timelineSteps: dynamicTimeline
      });
      return;
    }

    if (config.formula === "volume") {
      const volume = toMetricLength(getNumber("length")) * toMetricLength(getNumber("width")) * toMetricLength(getNumber("depth"));
      const density = getNumber("density");
      const unitSize = getNumber("unit-size");
      const totalVolume = volume * wasteFactor;
      const tonnes = totalVolume * density;
      const exactUnits = unitSize > 0 ? tonnes / unitSize : 0;
      units = unitSize > 0 ? Math.ceil(tonnes / unitSize) : 0;

      if (!(units > 0)) {
        renderDefaultState();
        return;
      }

      resultMain.textContent = `${units} ${unitLabel(units)}`;
      resultSub.textContent = `That works out to about ${formatVolume(totalVolume)}, roughly ${formatWeightTonnes(tonnes)}, and about ${money(units * pricePerUnit)} in material cost.`;
      resultBreakdown.innerHTML =
        `<div class="break-row"><span>Measured volume</span><strong>${formatVolume(volume)}</strong></div>` +
        `<div class="break-row"><span>Volume incl. waste</span><strong>${formatVolume(totalVolume)}</strong></div>` +
        `<div class="break-row"><span>Tonnage</span><strong>${formatWeightTonnes(tonnes)}</strong></div>` +
        `<div class="break-row"><span>Exact units before rounding</span><strong>${exactUnits.toFixed(2)} ${unitLabel(exactUnits)}</strong></div>` +
        `<div class="break-row"><span>Buying total</span><strong>${units} ${unitLabel(units)}</strong></div>` +
        `<div class="break-row"><span>Buffer after rounding</span><strong>${formatWeightTonnes(Math.max(0, (units * unitSize) - tonnes))}</strong></div>` +
        `<div class="break-row"><span>Estimated cost</span><strong>${money(units * pricePerUnit)}</strong></div>` +
        `<div class="calc-note">Calculation: length x width x depth, then waste, then density, then rounded to whole units.</div>`;
      setContext("Check whether the supplier quotes loose fill, compacted depth, bulk bags, or tonne-based delivery, because that choice can move the real order more than the headline cubic-metre figure.");

      renderIntelligence({
        materialCost: units * pricePerUnit,
        quantity: tonnes,
        quantitySuffix: "tonnes",
        quantityDecimals: 2,
        scopeValue: totalVolume,
        driverText: config.driverText || "Installed depth, loose-vs-compacted assumptions, density, and delivery format are the biggest cost drivers here.",
        formatQuantity: function (value) {
          return Number(value).toFixed(2);
        }
      });
      return;
    }

    const run = toMetricLength(getNumber("length")) * wasteFactor;
    const pieceLength = toMetricLength(getNumber("piece-length"));
    const exactUnits = pieceLength > 0 ? run / pieceLength : 0;
    units = pieceLength > 0 ? Math.ceil(run / pieceLength) : 0;

    if (!(units > 0)) {
      renderDefaultState();
      return;
    }

    resultMain.textContent = `${units} ${unitLabel(units)}`;
    resultSub.textContent = `That covers about ${formatLength(run)} after waste and roughly ${money(units * pricePerUnit)} in material cost.`;
    resultBreakdown.innerHTML =
      `<div class="break-row"><span>Measured run</span><strong>${formatLength(toMetricLength(getNumber("length")))}</strong></div>` +
      `<div class="break-row"><span>Run incl. waste</span><strong>${formatLength(run)}</strong></div>` +
      `<div class="break-row"><span>Unit length</span><strong>${formatLength(pieceLength)}</strong></div>` +
      `<div class="break-row"><span>Exact pieces before rounding</span><strong>${exactUnits.toFixed(2)} ${unitLabel(exactUnits)}</strong></div>` +
      `<div class="break-row"><span>Buying total</span><strong>${units} ${unitLabel(units)}</strong></div>` +
      `<div class="break-row"><span>Buffer after rounding</span><strong>${formatLength(Math.max(0, (units * pieceLength) - run))}</strong></div>` +
      `<div class="break-row"><span>Estimated cost</span><strong>${money(units * pricePerUnit)}</strong></div>` +
      `<div class="calc-note">Calculation: total run plus waste, then rounded to whole-length buying pieces.</div>`;
    setContext("Use the clean run as the starting point, then sense-check corners, fittings, mitres, and any spare length you would rather buy now than chase later.");

    renderIntelligence({
      materialCost: units * pricePerUnit,
      quantity: units,
      quantitySuffix: unitLabel(units),
      quantityDecimals: 0,
      scopeValue: run,
      driverText: config.driverText || "Run length, stock size, waste from cuts, and accessory pieces usually change this estimate most.",
      formatQuantity: function (value) {
        return `${Math.max(1, Math.round(value))}`;
      }
    });
  }

  currencyButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      currency = button.dataset.currency;
      setActive(currencyButtons, function (item) {
        return item.dataset.currency === currency;
      });
      if (resultBreakdown.innerHTML.trim()) calculate();
    });
  });

  unitButtons.forEach(function (button) {
    button.addEventListener("click", function () {
      unit = button.dataset.unit;
      setActive(unitButtons, function (item) {
        return item.dataset.unit === unit;
      });
      if (resultBreakdown.innerHTML.trim()) calculate();
    });
  });

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    calculate();
  });

  form.querySelectorAll("input, select").forEach(function (field) {
    field.addEventListener("change", function () {
      if (resultBreakdown.innerHTML.trim()) calculate();
    });
  });

  calculate();
})();
