from html import escape

from components.publishing import get_all_calculator_entries, render_ad_slot, render_layout
from data.catalog import get_all_calculators
from data.locations import get_all_locations
from data.publisher import SITE
from generators.calculators_index import calculator_directory_categories, calculator_directory_stats, render_directory_section


def build_homepage(cards_html: str = ""):
    calculators = get_all_calculator_entries()
    stats = calculator_directory_stats()
    location_count = len(get_all_locations())
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
    quick_links = "".join(
        f'<a class="hero-quick-link" href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a>'
        for item in calculators
        if item["slug"] in {"paint-calculator", "concrete-calculator", "flooring-calculator", "gravel-calculator"}
    )
    guide_count = sum(len(item["intent_pages"]) + len(item["guide_pages"]) for item in get_all_calculators())
    content = f'''
  <div class="site-shell">
    <section class="hero hero-home">
      <div class="hero-brand-row">
        <img class="hero-logo" src="/assets/logo.svg" alt="{escape(SITE["name"])}">
        <div class="eyebrow">buildcostlab.com</div>
      </div>
      <h1>Material calculators built for real building jobs</h1>
      <p class="hero-copy">{escape(SITE["description"])} Start with a calculator, pressure-test the result with the linked guides, then turn it into a cleaner quote brief before you buy.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/calculators/">Browse calculators</a>
        <a class="btn btn-secondary" href="/quote-checklist/">Open quote prep</a>
      </div>
      <div class="hero-badges">
        <span class="hero-badge">Practical quantity tools</span>
        <span class="hero-badge">Metric and imperial support</span>
        <span class="hero-badge">Quote-ready workflow</span>
      </div>
      <div class="hero-quick-links">
        <span class="hero-quick-label">Quick starts</span>
        {quick_links}
      </div>
    </section>

    <section class="stats-strip" aria-label="Library scale">
      <article class="content-card metric-card"><strong>{stats["calculator_count"]}</strong><span>calculators</span></article>
      <article class="content-card metric-card"><strong>{stats["cluster_count"]}</strong><span>tool sets</span></article>
      <article class="content-card metric-card"><strong>{guide_count}</strong><span>support guides</span></article>
      <article class="content-card metric-card"><strong>{location_count}</strong><span>location pages</span></article>
    </section>

    {render_ad_slot("home-top")}

    {render_directory_section(title="Find the right calculator faster", intro="One clear gap against stronger competitors is discoverability. Instead of forcing visitors through a long flat list, this front page now lets them search by task and filter by major project type immediately.", cards_html=cards_html, categories=calculator_directory_categories(), count_text=f'Showing all {stats["calculator_count"]} calculators.')}

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Plan the full job, not just the maths</h2>
        <p>BuildCostLab is strongest when it behaves like a workflow: find the right calculator, sense-check the result, then package the estimate into something a builder or supplier can actually quote from.</p>
      </div>
    </section>

    <section class="stack-grid workflow-grid">
      <article class="content-card prose-card"><h2>1. Find the right estimator</h2><p>Search by material, job, or buying term so people land on the right calculator faster than they would in a generic directory.</p></article>
      <article class="content-card prose-card"><h2>2. Pressure-test the number</h2><p>Use the built-in estimate range, cost breakdown, comparison view, and linked guides to spot the assumptions most likely to move the final order.</p></article>
      <article class="content-card prose-card"><h2>3. Turn it into a brief</h2><p>Use the quote-ready tools to copy, export, or email a cleaner project summary instead of relying on a rough mental note or screenshot.</p></article>
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
        <p>Each topic area brings related calculators and guides together so users can move from a quick estimate to a more confident buying decision.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {featured}
      </div>
    </section>

    <section class="conversion-panel conversion-panel-prominent">
      <div class="section-head">
        <h2>Move from estimate to quote-ready brief</h2>
        <p>Use the calculator result as your starting number, then turn it into a cleaner builder or supplier request with the quote-prep checklist and contact guidance page.</p>
      </div>
      <div class="conversion-actions">
        <a class="btn btn-primary" href="/quote-checklist/" data-conversion-link="quote-checklist">Open quote checklist</a>
        <a class="btn btn-secondary" href="/contact/" data-conversion-link="contact">Contact BuildCostLab</a>
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
