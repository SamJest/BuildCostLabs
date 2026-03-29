import json
from html import escape

from data.calculator_scale import ADDITIONAL_CALCULATORS
from data.calculator_ui import CALCULATOR_UI
from data.uk_regions import UK_REGION_PROFILES
from generators.publisher_pages import render_calculator_page


def _config_for(item):
    item_name = item["name"].replace(" Calculator", "")
    if item["formula"] == "volume":
        default_intro = f"You will see the material volume, buying quantity, rough material cost, and wider estimate view for {item_name} here."
    elif item["formula"] == "linear":
        default_intro = f"You will see the required lengths, buying quantity, rough material cost, and wider estimate view for {item_name} here."
    else:
        default_intro = f"You will see the buying quantity, rough material cost, and wider estimate view for {item_name} here."
    return {
        "length_label": "Length",
        "width_label": "Width",
        "depth_label": "Depth",
        "coverage_label": "Coverage per unit (m2)",
        "coverage_mode": "area_per_unit",
        "density_label": "Density / tonnes per m3",
        "unit_size_label": "Unit size (tonnes or m3)",
        "piece_length_label": "Stock length",
        "price_label": "Price per unit",
        "material_rate_label": "Material cost per m2",
        "labour_rate_label": "Labour cost per m2",
        "extra_rate_label": "Extra costs per m2",
        "contingency_label": "Contingency (%)",
        "unit_name_singular": "unit",
        "unit_name_plural": "units",
        "result_intro": default_intro,
        "defaults": {},
        "calculator_note": "",
    } | CALCULATOR_UI.get(item["slug"], {})


def _field(cfg, label: str, field_id: str, value: str, step: str) -> str:
    default_value = cfg.get("defaults", {}).get(field_id, value)
    return f'<label><span>{escape(label)}</span><input id="{escape(field_id)}" type="number" min="0" step="{escape(step)}" value="{escape(default_value)}"></label>'


def _select_field(label: str, field_id: str, options: list[tuple[str, str]], default_value: str) -> str:
    options_html = "".join(
        f'<option value="{escape(value)}"{" selected" if value == default_value else ""}>{escape(title)}</option>'
        for value, title in options
    )
    return f'<label><span>{escape(label)}</span><select id="{escape(field_id)}">{options_html}</select></label>'


def _coverage_form(cfg) -> str:
    note_html = f'<p class="form-note">{escape(cfg["calculator_note"])}</p>' if cfg.get("calculator_note") else ""
    return (
        '<div class="toggle-row units-row" role="tablist" aria-label="Units"><button class="unit-toggle is-active" data-unit="metric" type="button">Metric</button><button class="unit-toggle" data-unit="imperial" type="button">Imperial</button></div>'
        '<form class="calculator-form generic-calculator-form" data-formula="coverage"><div class="field-grid">'
        f'{_field(cfg, cfg["length_label"], "length", "4", "0.01")}'
        f'{_field(cfg, cfg["width_label"], "width", "3", "0.01")}'
        f'{_field(cfg, cfg["coverage_label"], "coverage-per-unit", "5", "0.01")}'
        f'{_field(cfg, "Waste allowance (%)", "waste", "10", "1")}'
        f'{_field(cfg, cfg["price_label"], "price-per-unit", "20", "0.01")}'
        f'</div>{note_html}<button class="btn btn-primary btn-block" type="submit">Calculate quantity</button></form>'
    )


def _volume_form(cfg) -> str:
    note_html = f'<p class="form-note">{escape(cfg["calculator_note"])}</p>' if cfg.get("calculator_note") else ""
    return (
        '<div class="toggle-row units-row" role="tablist" aria-label="Units"><button class="unit-toggle is-active" data-unit="metric" type="button">Metric</button><button class="unit-toggle" data-unit="imperial" type="button">Imperial</button></div>'
        '<form class="calculator-form generic-calculator-form" data-formula="volume"><div class="field-grid">'
        f'{_field(cfg, cfg["length_label"], "length", "4", "0.01")}'
        f'{_field(cfg, cfg["width_label"], "width", "3", "0.01")}'
        f'{_field(cfg, cfg["depth_label"], "depth", "0.05", "0.01")}'
        f'{_field(cfg, cfg["density_label"], "density", "1.6", "0.01")}'
        f'{_field(cfg, cfg["unit_size_label"], "unit-size", "0.85", "0.01")}'
        f'{_field(cfg, "Waste allowance (%)", "waste", "10", "1")}'
        f'{_field(cfg, cfg["price_label"], "price-per-unit", "65", "0.01")}'
        f'</div>{note_html}<button class="btn btn-primary btn-block" type="submit">Calculate quantity</button></form>'
    )


def _linear_form(cfg) -> str:
    note_html = f'<p class="form-note">{escape(cfg["calculator_note"])}</p>' if cfg.get("calculator_note") else ""
    return (
        '<div class="toggle-row units-row" role="tablist" aria-label="Units"><button class="unit-toggle is-active" data-unit="metric" type="button">Metric</button><button class="unit-toggle" data-unit="imperial" type="button">Imperial</button></div>'
        '<form class="calculator-form generic-calculator-form" data-formula="linear"><div class="field-grid">'
        f'{_field(cfg, cfg["length_label"], "length", "12", "0.01")}'
        f'{_field(cfg, cfg["piece_length_label"], "piece-length", "2.4", "0.01")}'
        f'{_field(cfg, "Waste allowance (%)", "waste", "8", "1")}'
        f'{_field(cfg, cfg["price_label"], "price-per-unit", "15", "0.01")}'
        f'</div>{note_html}<button class="btn btn-primary btn-block" type="submit">Calculate quantity</button></form>'
    )


def _project_cost_form(cfg) -> str:
    note_html = f'<p class="form-note">{escape(cfg["calculator_note"])}</p>' if cfg.get("calculator_note") else ""
    region_options = [(profile["slug"], profile["label"]) for profile in UK_REGION_PROFILES]
    default_region = cfg.get("defaults", {}).get("region", "national-average")
    return (
        '<div class="toggle-row units-row" role="tablist" aria-label="Units"><button class="unit-toggle is-active" data-unit="metric" type="button">Metric</button><button class="unit-toggle" data-unit="imperial" type="button">Imperial</button></div>'
        '<form class="calculator-form generic-calculator-form" data-formula="project_cost"><div class="field-grid">'
        f'{_field(cfg, cfg["length_label"], "length", "5", "0.01")}'
        f'{_field(cfg, cfg["width_label"], "width", "4", "0.01")}'
        f'{_select_field("UK region", "region", region_options, default_region)}'
        f'{_field(cfg, "Waste or complexity (%)", "waste", "10", "1")}'
        f'{_field(cfg, cfg["material_rate_label"], "material-rate", "60", "0.01")}'
        f'{_field(cfg, cfg["labour_rate_label"], "labour-rate", "45", "0.01")}'
        f'{_field(cfg, cfg["extra_rate_label"], "extra-rate", "12", "0.01")}'
        f'{_field(cfg, cfg["contingency_label"], "contingency", "10", "1")}'
        f'</div>{note_html}<button class="btn btn-primary btn-block" type="submit">Calculate project cost</button></form>'
    )


def _result_panel(cfg) -> str:
    return f"""<div class="result-kicker">Estimated result</div><h2 class="result-main">Enter your measurements</h2><p class="result-sub">{escape(cfg["result_intro"])}</p><div class="currency-pills" role="tablist" aria-label="Currency"><button class="currency-pill is-active" data-currency="GBP" type="button">GBP</button><button class="currency-pill" data-currency="USD" type="button">USD</button><button class="currency-pill" data-currency="EUR" type="button">EUR</button></div><div class="result-breakdown" id="result-breakdown"></div><p class="result-context" id="result-context"></p>"""


def build_additional_calculator_pages():
    pages = []
    for item in ADDITIONAL_CALCULATORS:
        cfg = _config_for(item)
        formula = item["formula"]
        if formula == "coverage":
            form_html = _coverage_form(cfg)
        elif formula == "volume":
            form_html = _volume_form(cfg)
        elif formula == "project_cost":
            form_html = _project_cost_form(cfg)
        else:
            form_html = _linear_form(cfg)
        result_html = _result_panel(cfg)
        calculator_config = {
            "formula": formula,
            "name": item["name"],
            "category": item["category"],
            "clusterName": item["cluster_name"],
            "unitNameSingular": cfg["unit_name_singular"],
            "unitNamePlural": cfg["unit_name_plural"],
            "resultIntro": cfg["result_intro"],
            "coverageLabel": cfg["coverage_label"],
            "coverageMode": cfg["coverage_mode"],
            "driverText": cfg.get("driver_text", ""),
            "confidenceText": cfg.get("confidence_text", ""),
            "comparisonProfiles": cfg.get("comparison_profiles", []),
            "realityItems": cfg.get("reality_items", []),
            "costModel": cfg.get("cost_model", None),
            "timelineSteps": cfg.get("timeline_steps", []),
            "costModel": cfg.get("cost_model", None),
            "regionProfiles": UK_REGION_PROFILES if formula == "project_cost" else [],
            "defaultRegion": cfg.get("defaults", {}).get("region", "national-average"),
        }
        html = render_calculator_page(
            slug=item["slug"],
            title=item["name"],
            description=item["meta_description"],
            intro=item["intro"],
            form_html=form_html,
            result_html=result_html,
            script_name="generic-material-calculator.js",
        ).replace(
            '<script src="/assets/js/generic-material-calculator.js"></script>',
            f'<script>window.__calculatorConfig = {json.dumps(calculator_config)};</script><script src="/assets/js/generic-material-calculator.js"></script>',
        )
        pages.append((item["slug"], html))
    return pages
