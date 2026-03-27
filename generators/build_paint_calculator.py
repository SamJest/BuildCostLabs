from __future__ import annotations

import json
from html import escape

from components.layout import build_breadcrumbs, build_footer, build_header
from core.config import DATA_DIR, OUTPUT_DIR, SITE_CONFIG
from core.io import ensure_dir, write_text


def render_mode_tabs(modes: list[dict], default_mode: str) -> str:
    buttons: list[str] = []
    panels: list[str] = []
    for mode in modes:
        selected = "true" if mode["id"] == default_mode else "false"
        active_class = " is-active" if mode["id"] == default_mode else ""
        hidden_attr = "" if mode["id"] == default_mode else " hidden"
        buttons.append(
            f"<button class=\"mode-tab{active_class}\" type=\"button\" data-mode-tab=\"{escape(mode['id'])}\" aria-pressed=\"{selected}\">{escape(mode['label'])}</button>"
        )
        panels.append(
            f"<div class=\"mode-panel{active_class}\" data-mode-panel=\"{escape(mode['id'])}\"{hidden_attr}><p>{escape(mode['description'])}</p></div>"
        )
    return (
        '<div class="mode-tabs" role="tablist" aria-label="Calculator modes">' + ''.join(buttons) + '</div>'
        + '<div class="mode-panel-wrap">' + ''.join(panels) + '</div>'
    )


def render_unique_sections(sections: list[dict]) -> str:
    blocks: list[str] = []
    for section in sections:
        paragraphs = ''.join(f"<p>{escape(text)}</p>" for text in section.get("paragraphs", []))
        bullets = ""
        if section.get("bullets"):
            bullets = '<ul class="content-list">' + ''.join(f"<li>{escape(item)}</li>" for item in section["bullets"]) + '</ul>'
        blocks.append(
            f"<section class=\"content-card\"><h2>{escape(section['heading'])}</h2>{paragraphs}{bullets}</section>"
        )
    return ''.join(blocks)


def render_faq(items: list[dict]) -> str:
    parts: list[str] = []
    for item in items:
        parts.append(
            f"<details class=\"faq-item\"><summary>{escape(item['question'])}</summary><p>{escape(item['answer'])}</p></details>"
        )
    return '<section class="content-card"><h2>Paint calculator FAQs</h2><div class="faq-list">' + ''.join(parts) + '</div></section>'


def render_related(items: list[dict]) -> str:
    cards: list[str] = []
    for item in items:
        cards.append(
            f"<article class=\"related-card\"><h3><a href=\"{escape(item['href'])}\">{escape(item['label'])}</a></h3><p>{escape(item['description'])}</p></article>"
        )
    return '<section class="content-card"><h2>Related calculators</h2><div class="related-grid">' + ''.join(cards) + '</div></section>'


def build_paint_calculator() -> None:
    data = json.loads((DATA_DIR / 'calculator_pages' / 'paint-calculator.json').read_text(encoding='utf-8'))
    breadcrumbs = build_breadcrumbs([
        {"label": "Home", "href": "/"},
        {"label": "Calculators", "href": "/calculators/"},
        {"label": data['heading'], "href": f"/calculators/{data['slug']}/"},
    ])

    html = f'''<!doctype html>
<html lang="{SITE_CONFIG['locale']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(data['title'])}</title>
  <meta name="description" content="{escape(data['meta_description'])}">
  <link rel="canonical" href="{SITE_CONFIG['site_url']}/calculators/{data['slug']}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(data['title'])}">
  <meta property="og:description" content="{escape(data['meta_description'])}">
  <meta property="og:url" content="{SITE_CONFIG['site_url']}/calculators/{data['slug']}/">
  <meta property="og:image" content="{SITE_CONFIG['site_url']}/assets/images/og-default.png">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  {build_header(SITE_CONFIG)}
  <main>
    <section class="page-hero">
      <div class="container">
        {breadcrumbs}
        <p class="eyebrow">{escape(data['eyebrow'])}</p>
        <h1>{escape(data['heading'])}</h1>
        <p class="page-intro">{escape(data['intro'])}</p>
      </div>
    </section>

    <section class="section">
      <div class="container calculator-layout">
        <div class="calculator-shell">
          <div class="calculator-shell-head">
            <div>
              <p class="eyebrow">Live calculator</p>
              <h2>Estimate paint in litres, gallons and tins</h2>
            </div>
            <p class="calculator-shell-text">{escape(data['result_summary'])}</p>
          </div>
          {render_mode_tabs(data['calculator']['modes'], data['calculator']['default_mode'])}
          <form class="tool-card" id="paint-calculator-form" data-calculator="paint">
            <div class="field-grid field-grid-compact">
              <div class="field-group field-group-inline">
                <span class="field-label">Units</span>
                <label><input type="radio" name="unitSystem" value="metric" checked> Metric</label>
                <label><input type="radio" name="unitSystem" value="imperial"> Imperial</label>
              </div>
              <div class="field-group field-group-inline">
                <span class="field-label">Mode</span>
                <label><input type="radio" name="mode" value="walls" checked> Walls + room</label>
                <label><input type="radio" name="mode" value="ceiling"> Ceiling only</label>
                <label><input type="radio" name="mode" value="single"> Single surface</label>
              </div>
            </div>
            <div class="field-grid">
              <label class="field-group" data-visibility="walls ceiling">
                <span class="field-label">Room length</span>
                <input type="number" name="roomLength" min="0" step="0.01" value="4.2">
                <span class="field-hint" data-unit-label="length">metres</span>
              </label>
              <label class="field-group" data-visibility="walls ceiling">
                <span class="field-label">Room width</span>
                <input type="number" name="roomWidth" min="0" step="0.01" value="3.6">
                <span class="field-hint" data-unit-label="length">metres</span>
              </label>
              <label class="field-group" data-visibility="walls">
                <span class="field-label">Wall height</span>
                <input type="number" name="wallHeight" min="0" step="0.01" value="2.4">
                <span class="field-hint" data-unit-label="length">metres</span>
              </label>
              <label class="field-group" data-visibility="single">
                <span class="field-label">Surface width</span>
                <input type="number" name="surfaceWidth" min="0" step="0.01" value="3.0">
                <span class="field-hint" data-unit-label="length">metres</span>
              </label>
              <label class="field-group" data-visibility="single">
                <span class="field-label">Surface height</span>
                <input type="number" name="surfaceHeight" min="0" step="0.01" value="2.4">
                <span class="field-hint" data-unit-label="length">metres</span>
              </label>
              <label class="field-group" data-visibility="walls single">
                <span class="field-label">Doors to subtract</span>
                <input type="number" name="doors" min="0" step="1" value="1">
                <span class="field-hint">Approx. 1.9 m² / 21 ft² each</span>
              </label>
              <label class="field-group" data-visibility="walls single">
                <span class="field-label">Windows to subtract</span>
                <input type="number" name="windows" min="0" step="1" value="1">
                <span class="field-hint">Approx. 1.5 m² / 16 ft² each</span>
              </label>
              <label class="field-group">
                <span class="field-label">Coats</span>
                <input type="number" name="coats" min="1" step="1" value="2">
                <span class="field-hint">Usually 2 coats for planning</span>
              </label>
              <label class="field-group">
                <span class="field-label">Coverage per litre</span>
                <input type="number" name="coveragePerLitre" min="0.1" step="0.1" value="10">
                <span class="field-hint">m² per litre per coat</span>
              </label>
              <label class="field-group">
                <span class="field-label">Extra wastage</span>
                <input type="number" name="wastagePercent" min="0" step="1" value="10">
                <span class="field-hint">For cutting-in, loss and touch-ups</span>
              </label>
            </div>
            <div class="tool-actions">
              <button class="button button-primary" type="submit">Calculate paint</button>
              <button class="button button-secondary" type="reset">Reset</button>
            </div>
          </form>
        </div>
        <aside class="results-shell" id="paint-results" aria-live="polite">
          <div class="result-card result-card-accent">
            <p class="eyebrow">Estimated paint needed</p>
            <p class="result-value" data-result-litres>0.0 L</p>
            <p class="result-subvalue" data-result-gallons>0.00 gal</p>
            <p class="result-support">Rounded buying estimate including the wastage allowance.</p>
          </div>
          <div class="result-card">
            <h2>Breakdown</h2>
            <ul class="result-list">
              <li><span>Paint area</span><strong data-result-area>0.0 m²</strong></li>
              <li><span>Coverage needed</span><strong data-result-coverage>0.0 litre-coats</strong></li>
              <li><span>Base litres</span><strong data-result-base>0.0 L</strong></li>
              <li><span>After wastage</span><strong data-result-total>0.0 L</strong></li>
            </ul>
          </div>
          <div class="result-card">
            <h2>Suggested tins</h2>
            <p class="result-note" data-result-tins>Enter your measurements to see suggested tin combinations.</p>
          </div>
          <div class="result-card">
            <h2>How it was calculated</h2>
            <ol class="result-steps" data-result-steps>
              <li>Choose a mode and enter your measurements.</li>
              <li>The calculator works out the paintable area.</li>
              <li>It applies coats, coverage and wastage to estimate total paint needed.</li>
            </ol>
          </div>
        </aside>
      </div>
    </section>

    <section class="section section-alt">
      <div class="container content-stack">
        {render_unique_sections(data['unique_sections'])}
        {render_faq(data['faq'])}
        {render_related(data['related_calculators'])}
      </div>
    </section>
  </main>
  {build_footer(SITE_CONFIG)}
  <script src="/assets/js/site.js"></script>
</body>
</html>'''

    output_dir = OUTPUT_DIR / 'calculators' / data['slug']
    ensure_dir(output_dir)
    write_text(output_dir / 'index.html', html)


if __name__ == '__main__':
    build_paint_calculator()
