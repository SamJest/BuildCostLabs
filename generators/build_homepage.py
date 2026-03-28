from __future__ import annotations

import json
from html import escape

from components.layout import build_footer, build_header
from core.config import DATA_DIR, OUTPUT_DIR, SITE_CONFIG
from core.io import ensure_dir, write_text


def build_feature_cards(cards: list[dict]) -> str:
    items = []
    for card in cards:
        items.append(
            f'''
            <article class="feature-card">
              <p class="eyebrow">{escape(card['eyebrow'])}</p>
              <h2>{escape(card['title'])}</h2>
              <p>{escape(card['text'])}</p>
            </article>'''
        )
    return '<div class="feature-grid">' + ''.join(items) + '</div>'



def build_category_cards(categories: list[dict]) -> str:
    items = []
    for category in categories:
        items.append(
            f'''
            <article class="category-card">
              <p class="category-kicker">{escape(category['kicker'])}</p>
              <h3>{escape(category['title'])}</h3>
              <p>{escape(category['text'])}</p>
              <ul>
                {''.join(f'<li>{escape(item)}</li>' for item in category['examples'])}
              </ul>
            </article>'''
        )
    return '<div class="category-grid">' + ''.join(items) + '</div>'



def build_calculator_cards(calculators: list[dict]) -> str:
    items = []
    for calculator in calculators:
        status = calculator.get('status_label', 'Planned')
        items.append(
            f'''
            <article class="calculator-card">
              <div class="calculator-card-top">
                <p class="eyebrow">{escape(calculator['category'])}</p>
                <span class="status-pill">{escape(status)}</span>
              </div>
              <h3>{escape(calculator['name'])}</h3>
              <p>{escape(calculator['summary'])}</p>
              <a class="text-link" href="/calculators/{escape(calculator['slug'])}/">View planned URL</a>
            </article>'''
        )
    return '<div class="calculator-grid">' + ''.join(items) + '</div>'



def build_homepage() -> None:
    homepage_path = DATA_DIR / 'pages' / 'homepage.json'
    calculators_path = DATA_DIR / 'calculators' / 'calculators.json'

    homepage_data = json.loads(homepage_path.read_text(encoding='utf-8'))
    calculators = json.loads(calculators_path.read_text(encoding='utf-8'))

    html = f'''<!doctype html>
<html lang="{SITE_CONFIG['locale']}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(homepage_data['title'])}</title>
  <meta name="description" content="{escape(homepage_data['meta_description'])}">
  <link rel="canonical" href="{SITE_CONFIG['site_url']}/">
  <meta property="og:type" content="website">
  <meta property="og:title" content="{escape(homepage_data['title'])}">
  <meta property="og:description" content="{escape(homepage_data['meta_description'])}">
  <meta property="og:url" content="{SITE_CONFIG['site_url']}/">
  <meta property="og:image" content="{SITE_CONFIG['site_url']}/assets/images/og-default.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(homepage_data['title'])}">
  <meta name="twitter:description" content="{escape(homepage_data['meta_description'])}">
  <link rel="stylesheet" href="/assets/css/site.css">
</head>
<body>
  {build_header(SITE_CONFIG)}
  <main>
    <section class="hero-section">
      <div class="container hero-grid">
        <div>
          <p class="eyebrow">{escape(homepage_data['hero_eyebrow'])}</p>
          <h1>{escape(homepage_data['hero_heading'])}</h1>
          <p class="hero-text">{escape(homepage_data['hero_text'])}</p>
          <div class="hero-actions">
            <a class="button button-primary" href="{escape(homepage_data['primary_cta_href'])}">{escape(homepage_data['primary_cta_label'])}</a>
            <a class="button button-secondary" href="{escape(homepage_data['secondary_cta_href'])}">{escape(homepage_data['secondary_cta_label'])}</a>
          </div>
          <ul class="hero-points">
            {''.join(f'<li>{escape(point)}</li>' for point in homepage_data['hero_points'])}
          </ul>
        </div>
        <aside class="hero-panel">
          <p class="hero-panel-label">Best first tool set</p>
          <h2>{escape(homepage_data['hero_panel_title'])}</h2>
          <p>{escape(homepage_data['hero_panel_text'])}</p>
          <ul>
            {''.join(f'<li>{escape(item)}</li>' for item in homepage_data['hero_panel_list'])}
          </ul>
        </aside>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">Fastest path to traffic</p>
          <h2>{escape(homepage_data['features_heading'])}</h2>
          <p>{escape(homepage_data['features_text'])}</p>
        </div>
        {build_feature_cards(homepage_data['feature_cards'])}
      </div>
    </section>

    <section class="section section-alt">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">Search-led structure</p>
          <h2>{escape(homepage_data['categories_heading'])}</h2>
          <p>{escape(homepage_data['categories_text'])}</p>
        </div>
        {build_category_cards(homepage_data['category_cards'])}
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-heading">
          <p class="eyebrow">Planned calculators</p>
          <h2>{escape(homepage_data['calculators_heading'])}</h2>
          <p>{escape(homepage_data['calculators_text'])}</p>
        </div>
        {build_calculator_cards(calculators)}
      </div>
    </section>
  </main>
  {build_footer(SITE_CONFIG)}
  <script src="/assets/js/site.js"></script>
</body>
</html>'''

    ensure_dir(OUTPUT_DIR)
    write_text(OUTPUT_DIR / 'index.html', html)


if __name__ == '__main__':
    build_homepage()
