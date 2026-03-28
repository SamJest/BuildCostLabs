from html import escape

from components.publishing import render_ad_slot, render_layout
from data.catalog import get_all_calculators
from data.publisher import SITE


def build_homepage(cards_html: str = ""):
    calculators = get_all_calculators()
    launch_ready = [
        "paint-calculator",
        "concrete-calculator",
        "brick-calculator",
        "insulation-board-calculator",
        "roofing-shingle-calculator",
        "topsoil-calculator",
    ]
    featured = "".join(
        f'<article class="tool-card"><h3><a href="/clusters/{escape(item["cluster_slug"])}/">{escape(item["cluster_name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
        for item in calculators[:4]
    )
    launch_cards = "".join(
        f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p><a class="text-link" href="/clusters/{escape(item["cluster_slug"])}/">View cluster</a></article>'
        for item in calculators
        if item["slug"] in launch_ready
    )
    content = f'''
  <div class="site-shell">
    <section class="hero hero-home">
      <div class="hero-brand-row">
        <img class="hero-logo" src="/assets/logo.svg" alt="{escape(SITE["name"])}">
        <div class="eyebrow">buildcostlab.com</div>
      </div>
      <h1>Material calculators for real building jobs</h1>
      <p class="hero-copy">{escape(SITE["description"])}</p>
      <div class="hero-badges">
        <span class="hero-badge">Practical quantity tools</span>
        <span class="hero-badge">Metric and imperial support</span>
        <span class="hero-badge">Guides for common buying decisions</span>
      </div>
    </section>

    {render_ad_slot("home-top")}

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Calculator library</h2>
        <p>Start with the calculator that fits your job, then use the related guides to check waste, buying units, and rough material costs before you order.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {cards_html}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Popular starting points</h2>
        <p>These calculators cover some of the most common jobs people price and plan first, from paint and concrete to roofing and topsoil.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {launch_cards}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Browse by project type</h2>
        <p>Each topic area brings related calculators and guides together so you can move from a quick estimate to a more confident buying decision.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {featured}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Plan the job before you buy</h2>
        <p>A simple quantity result is only the start. The guides on this site help you think through waste, pack sizes, delivery format, and the practical differences between common product options.</p>
      </div>
    </section>
  </div>'''
    return render_layout(
        title=f'{SITE["name"]} | Building Material and Cost Calculators',
        description=SITE["description"],
        path="/",
        content=content,
        page_type="homepage",
    )
