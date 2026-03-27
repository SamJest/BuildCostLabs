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
        <div class="logo-text">BuildCost<span>Labs</span></div>
        <div class="eyebrow">buildcostlabs.com</div>
      </div>
      <h1>Structured cost tools for real building jobs</h1>
      <p class="hero-copy">{escape(SITE["description"])}</p>
      <div class="hero-badges">
        <span class="hero-badge">Calculator-led publishing</span>
        <span class="hero-badge">UK and US intent</span>
        <span class="hero-badge">Ad-ready page templates</span>
      </div>
    </section>

    {render_ad_slot("home-top")}

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Calculator library</h2>
        <p>Start with a working calculator, then move into supporting guides, cost explainers, and next-step pages built around the same job intent. The site now supports a much larger inventory model so clusters can scale without losing structure.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {cards_html}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Launch-ready traffic candidates</h2>
        <p>These are the strongest early pages for combining practical utility, ad-friendly time on page, and obvious next-step cluster expansion.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {launch_cards}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Topic clusters built to compound traffic</h2>
        <p>Each cluster combines a core calculator, sub-intent pages, and support guides so visitors can keep moving through the topic instead of bouncing after one answer.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {featured}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>High-intent buying journeys</h2>
        <p>The strongest revenue paths start with a quantity question, then move into waste, pack size, delivery format, and product comparison. The site architecture is now built to support that journey.</p>
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
