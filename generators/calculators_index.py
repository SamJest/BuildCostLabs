from html import escape

from components.publishing import render_ad_slot, render_breadcrumb_schema, render_breadcrumbs, render_layout
from data.catalog import get_all_calculators
from data.publisher import SITE


def build_calculator_cards() -> str:
    parts = []
    for item in get_all_calculators():
        parts.append(
            f'''
        <article class="tool-card">
          <div class="tool-card-glow"></div>
          <h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3>
          <p>{escape(item["intro"])}</p>
          <a class="text-link" href="/clusters/{escape(item["cluster_slug"])}/">Open cluster</a>
        </article>
        '''
        )
    return "".join(parts)


def build_calculators_index(cards_html: str) -> str:
    crumbs = [("Home", "/"), ("Calculators", "/calculators/")]
    content = f'''
  <div class="site-shell">
    <section class="hero hero-compact">
      {render_breadcrumbs(crumbs)}
      <div class="eyebrow">Calculator directory</div>
      <h1>Choose the tool you need</h1>
      <p class="hero-copy">Start with a working calculator, then move into the linked cluster guides if you need buying help, assumptions, or next-step material decisions.</p>
    </section>
    {render_ad_slot("calculators-index-top")}
    <section class="calculator-grid-section"><div class="calculator-grid">{cards_html}</div></section>
  </div>'''
    return render_layout(
        title=f'Calculators | {SITE["name"]}',
        description='Browse practical material calculators for building, decorating, and outdoor jobs.',
        path="/calculators/",
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="calculator-index",
    )
