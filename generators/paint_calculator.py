from data.publisher import CALCULATOR_FAMILIES
from generators.publisher_pages import render_calculator_page


def build_paint_calculator_page() -> str:
    family = next(item for item in CALCULATOR_FAMILIES if item["slug"] == "paint-calculator")
    form_html = """<div class="toggle-row" role="tablist" aria-label="Paint mode"><button class="mode-toggle is-active" data-mode="walls" type="button">Walls</button><button class="mode-toggle" data-mode="ceiling" type="button">Ceiling</button><button class="mode-toggle" data-mode="single" type="button">Single surface</button></div><div class="toggle-row units-row" role="tablist" aria-label="Units"><button class="unit-toggle is-active" data-unit="metric" type="button">Metric</button><button class="unit-toggle" data-unit="imperial" type="button">Imperial</button></div><form id="paint-form" class="calculator-form"><div class="field-grid"><label><span>Length</span><input id="length" type="number" min="0" step="0.01" value="4"></label><label><span>Width</span><input id="width" type="number" min="0" step="0.01" value="3"></label><label><span>Height</span><input id="height" type="number" min="0" step="0.01" value="2.4"></label><label><span>Coats</span><input id="coats" type="number" min="1" step="1" value="2"></label><label><span>Coverage per litre (m²)</span><input id="coverage" type="number" min="0" step="0.1" value="12"></label><label><span>Waste allowance (%)</span><input id="waste" type="number" min="0" step="1" value="10"></label><label><span>Price per litre</span><input id="price-per-litre" type="number" min="0" step="0.01" value="8.50"></label></div><button class="btn btn-primary btn-block" type="submit">Calculate paint</button></form>"""
    result_html = """<div class="result-kicker">Estimated result</div><h2 class="result-main">Enter your measurements</h2><p class="result-sub">You will see the painted area, litres, tin suggestion and rough material cost here.</p><div class="currency-pills" role="tablist" aria-label="Currency"><button class="currency-pill is-active" data-currency="GBP" type="button">GBP £</button><button class="currency-pill" data-currency="USD" type="button">USD $</button><button class="currency-pill" data-currency="EUR" type="button">EUR €</button></div><div class="result-breakdown" id="result-breakdown"></div>"""
    return render_calculator_page(
        slug=family["slug"],
        title=family["name"],
        description=family["meta_description"],
        intro=family["intro"],
        form_html=form_html,
        result_html=result_html,
        script_name="paint-calculator.js",
    )
