from html import escape

from components.publishing import render_ad_slot, render_layout
from generators.publisher_pages import classify_guide, render_home_conversion_cards
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
        f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p><a class="text-link" href="/clusters/{escape(item["cluster_slug"])}/">View tool set</a></article>'
        for item in calculators
        if item["slug"] in launch_ready
    )
    project_cost_calculators = [item for item in calculators if item.get("formula") == "project_cost"]
    compare_guides = []
    for family in calculators:
        for item in family["intent_pages"] + family["guide_pages"]:
            if classify_guide(item) != "general":
                compare_guides.append(item)
    compare_cards = "".join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p></article>'
        for item in compare_guides[:6]
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
        <h2>Compare options and budget routes</h2>
        <p>Use the comparison and budget guides when you need more than a raw material count and want a faster route into product choices, cost rates, or labour-vs-material thinking.</p>
        <p><a class="text-link" href="/compare/">Open the comparison hub</a></p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {compare_cards}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Prepare for quote comparisons</h2>
        <p>When the job has moved beyond material counts, use the project-cost calculators to keep labour, extras, contingency, and regional pressure visible before you compare quotes.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {"".join(f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p><a class="text-link" href="/contact/">Use with quote brief</a></article>' for item in project_cost_calculators[:4])}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Plan the job before you buy</h2>
        <p>A simple quantity result is only the start. The guides on this site help you think through waste, pack sizes, delivery format, and the practical differences between common product options.</p>
        <p><a class="text-link" href="/calculator-methodology/">Review the methodology</a> or <a class="text-link" href="/contact/">open the contact path</a> before sending estimates around.</p>
      </div>
    </section>

    {render_home_conversion_cards()}
  </div>'''
    return render_layout(
        title=f'{SITE["name"]} | Building Material and Cost Calculators',
        description=SITE["description"],
        path="/",
        content=content,
        page_type="homepage",
    )
