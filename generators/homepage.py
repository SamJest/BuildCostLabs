from html import escape

from components.publishing import get_all_calculator_entries, render_ad_slot, render_layout
from data.catalog import get_all_calculators
from data.locations import get_all_locations
from data.publisher import PROJECT_HUBS_LABEL, SITE
from generators.calculators_index import calculator_directory_categories, calculator_directory_stats, render_directory_section, render_search_opportunity_section


def build_homepage(cards_html: str = ""):
    calculators = get_all_calculator_entries()
    stats = calculator_directory_stats()
    location_count = len(get_all_locations())
    featured_slugs = {
        "paint-calculator",
        "concrete-calculator",
        "paving-calculator",
        "decking-calculator",
        "flooring-calculator",
        "driveway-cost-calculator",
        "mot-type-1-calculator",
        "hardcore-calculator",
    }
    featured = "".join(
        f'<article class="tool-card"><h3><a href="/clusters/{escape(item["cluster_slug"])}/">{escape(item["cluster_name"])}</a></h3><p>{escape(item["intro"])}</p><a class="text-link" href="/clusters/{escape(item["cluster_slug"])}/">Open {escape(PROJECT_HUBS_LABEL[:-1])}</a></article>'
        for item in calculators
        if item["slug"] in featured_slugs
    )
    popular_cards = "".join(
        f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p><a class="text-link" href="/guides/{escape((item["intent_pages"] + item["guide_pages"])[0]["slug"] if (item["intent_pages"] + item["guide_pages"]) else item["slug"] )}/">Sense-check the estimate</a></article>'
        for item in calculators
        if item["slug"] in {"paving-calculator", "flooring-calculator", "mot-type-1-calculator", "skirting-board-calculator", "pea-gravel-calculator", "laminate-flooring-calculator"}
    )
    quick_links = "".join(
        f'<a class="hero-quick-link" href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a>'
        for item in calculators
        if item["slug"] in {"paving-calculator", "flooring-calculator", "mot-type-1-calculator", "skirting-board-calculator", "hardcore-calculator", "pea-gravel-calculator"}
    )
    guide_count = sum(len(item["intent_pages"]) + len(item["guide_pages"]) for item in get_all_calculators())
    content = f'''
  <div class="site-shell">
    <section class="hero hero-home">
      <div class="hero-brand-row">
        <img class="hero-logo" src="/assets/logo.svg" alt="{escape(SITE["name"])}">
        <div class="eyebrow">buildcostlab.com</div>
      </div>
      <h1>Estimate smarter, then prepare a better quote request</h1>
      <p class="hero-copy">{escape(SITE["description"])} Start with the right calculator, check the assumptions that usually move the number, compare options clearly, and turn the result into something a supplier or installer can price properly.</p>
      <div class="hero-actions">
        <a class="btn btn-primary" href="/calculators/">Browse calculators</a>
        <a class="btn btn-secondary" href="/quote-checklist/">Open quote prep</a>
      </div>
      <div class="hero-badges">
        <span class="hero-badge">Estimate → sense-check → compare → brief</span>
        <span class="hero-badge">Metric and imperial support</span>
        <span class="hero-badge">Planning aids with practical next steps</span>
      </div>
      <div class="hero-quick-links">
        <span class="hero-quick-label">Quick starts</span>
        {quick_links}
      </div>
    </section>

    <section class="stats-strip" aria-label="Library scale">
      <article class="content-card metric-card"><strong>{stats["calculator_count"]}</strong><span>calculators</span></article>
      <article class="content-card metric-card"><strong>{stats["cluster_count"]}</strong><span>{escape(PROJECT_HUBS_LABEL.lower())}</span></article>
      <article class="content-card metric-card"><strong>{guide_count}</strong><span>support guides</span></article>
      <article class="content-card metric-card"><strong>{location_count}</strong><span>location pages</span></article>
    </section>

    {render_ad_slot("home-top")}

    {render_search_opportunity_section(calculators, title="Start with pages people are already searching for", intro="Recent search-demand signals point to paving, flooring, MOT Type 1, skirting, pea gravel, laminate, hardcore, plasterboard, turf, loft insulation, and gutter estimates. These quick links give those searches a cleaner path from the homepage.")}

    {render_directory_section(title="Find the right calculator faster", intro="Search by job, material, or buying task, then filter the library so you can start with the right estimate instead of scrolling through an endless list.", cards_html=cards_html, categories=calculator_directory_categories(), count_text=f'Showing all {stats["calculator_count"]} calculators.')}

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>How BuildCostLab helps you plan the job</h2>
        <p>The site is designed around the practical workflow people actually need: estimate the quantity or budget, pressure-test the weak assumptions, compare routes where necessary, and package the result into a cleaner brief.</p>
      </div>
    </section>

    <section class="stack-grid workflow-grid">
      <article class="content-card prose-card"><h2>1. Start with a usable estimate</h2><p>Pick the calculator that matches the real material or project question so the starting number is already in the right format for buying or budgeting.</p></article>
      <article class="content-card prose-card"><h2>2. Check what could change it</h2><p>Use the guide links, support notes, and range logic to see where waste, labour, access, pack size, or finish level could move the real total.</p></article>
      <article class="content-card prose-card"><h2>3. Brief suppliers more clearly</h2><p>Use the quote-ready tools and checklist so every builder or merchant is pricing the same scope, assumptions, and exclusions.</p></article>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Popular starting points</h2>
        <p>These are some of the most useful pages for early planning, whether you are buying materials, checking a budget, or preparing a quote brief.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {popular_cards}
      </div>
    </section>

    <section class="content-card intro-card">
      <div class="section-head">
        <h2>Browse by project type</h2>
        <p>Open a {escape(PROJECT_HUBS_LABEL[:-1].lower())} when the job includes linked materials, supporting guides, and a wider quote-prep path rather than one single calculation.</p>
      </div>
    </section>

    <section class="calculator-grid-section">
      <div class="calculator-grid">
        {featured}
      </div>
    </section>

    <section class="quality-strip" aria-label="Trust signals">
      <article class="content-card quality-card"><div class="quality-kicker">Methodology</div><h2>See how estimates are built</h2><p>Read the <a href="/calculator-methodology/">calculator methodology</a> for formulas, waste logic, conversions, and why planning ranges matter.</p></article>
      <article class="content-card quality-card"><div class="quality-kicker">Editorial standards</div><h2>Understand how pages are reviewed</h2><p>The <a href="/editorial-policy/">editorial policy</a> explains source hierarchy, update standards, and how corrections are handled.</p></article>
      <article class="content-card quality-card"><div class="quality-kicker">Planning use</div><h2>Use estimates as planning aids</h2><p>BuildCostLab is designed for planning and quote preparation, not fixed promises. Always confirm live prices, measurements, and site conditions.</p></article>
    </section>

    <section class="conversion-panel conversion-panel-prominent">
      <div class="section-head">
        <h2>Move from estimate to quote-ready brief</h2>
        <p>Use the calculator result as your starting number, then turn it into a cleaner builder or supplier request with the quote checklist and contact page.</p>
      </div>
      <div class="conversion-actions">
        <a class="btn btn-primary" href="/quote-checklist/" data-conversion-link="quote-checklist">Open quote checklist</a>
        <a class="btn btn-secondary" href="/contact/" data-conversion-link="contact">Contact BuildCostLab</a>
      </div>
    </section>
  </div>'''
    return render_layout(
        title=f'{SITE["name"]} | Practical Building Material and Cost Calculators',
        description=SITE["description"],
        path="/",
        content=content,
        page_type="homepage",
    )
