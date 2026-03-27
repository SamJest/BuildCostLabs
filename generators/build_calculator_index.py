from __future__ import annotations

import json
from html import escape

from components.layout import build_breadcrumbs, build_footer, build_header
from core.config import DATA_DIR, OUTPUT_DIR, SITE_CONFIG
from core.io import ensure_dir, write_text


def build_index_cards(calculators: list[dict]) -> str:
    items: list[str] = []
    for calculator in calculators:
        items.append(
            f'''
            <article class="directory-card">
              <div class="directory-card-top">
                <p class="eyebrow">{escape(calculator['category'])}</p>
                <span class="status-pill">{escape(calculator.get('status_label', 'Planned'))}</span>
              </div>
              <h2><a href="/calculators/{escape(calculator['slug'])}/">{escape(calculator['name'])}</a></h2>
              <p>{escape(calculator['summary'])}</p>
            </article>'''
        )
    return '<div class="directory-grid">' + ''.join(items) + '</div>'


def build_calculator_index() -> None:
    calculators = json.loads((DATA_DIR / 'calculators' / 'calculators.json').read_text(encoding='utf-8'))
    breadcrumbs = build_breadcrumbs([
        {"label": "Home", "href": "/"},
        {"label": "Calculators", "href": "/calculators/"},
    ])
    html = f'''<!doctype html>
<html lang="{SITE_CONFIG['locale']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>All Calculators | {escape(SITE_CONFIG['brand_name'])}</title>
  <meta name="description" content="Browse practical project calculators for paint, tiles, flooring, concrete, gravel, decking, paving and more.">
  <link rel="canonical" href="{SITE_CONFIG['site_url']}/calculators/">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  {build_header(SITE_CONFIG)}
  <main>
    <section class="page-hero">
      <div class="container">
        {breadcrumbs}
        <p class="eyebrow">Calculator index</p>
        <h1>All calculators</h1>
        <p class="page-intro">Browse the growing BuildMate library of material and project estimators. Each page is designed around a distinct job intent so the site can scale without becoming a wall of duplicated copy.</p>
      </div>
    </section>
    <section class="section">
      <div class="container">
        {build_index_cards(calculators)}
      </div>
    </section>
  </main>
  {build_footer(SITE_CONFIG)}
</body>
</html>'''
    output_dir = OUTPUT_DIR / 'calculators'
    ensure_dir(output_dir)
    write_text(output_dir / 'index.html', html)


if __name__ == '__main__':
    build_calculator_index()
