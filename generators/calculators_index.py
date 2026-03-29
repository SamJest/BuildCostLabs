from collections import Counter
from html import escape

from components.publishing import get_all_calculator_entries, render_ad_slot, render_breadcrumb_schema, render_breadcrumbs, render_layout
from data.catalog import get_all_calculators
from data.publisher import SITE


DEFAULT_FEATURED_SLUGS = {
    "paint-calculator",
    "concrete-calculator",
    "flooring-calculator",
    "tile-calculator",
    "gravel-calculator",
    "decking-calculator",
    "paving-calculator",
    "fence-calculator",
    "driveway-cost-calculator",
    "patio-cost-calculator",
}


def calculator_directory_categories(limit: int = 8) -> list[str]:
    counts = Counter(item["category"] for item in get_all_calculator_entries())
    preferred = [
        "Project costs",
        "Decorating",
        "Aggregates",
        "Concrete and aggregates",
        "Flooring",
        "Tiles and finishes",
        "Roofing",
        "Landscaping",
        "Drainage",
        "Interior finishes",
    ]
    ordered = [label for label in preferred if label in counts]
    ordered.extend(label for label, _ in counts.most_common() if label not in ordered)
    return ordered[:limit]


def calculator_directory_stats() -> dict:
    calculators = get_all_calculator_entries()
    guide_count = sum(len(item["intent_pages"]) + len(item["guide_pages"]) for item in get_all_calculators())
    return {
        "calculator_count": len(calculators),
        "cluster_count": len({item["cluster_slug"] for item in calculators}),
        "guide_count": guide_count,
    }


def _card_search_text(item: dict) -> str:
    guide_titles = " ".join(entry["title"] for entry in item["intent_pages"] + item["guide_pages"])
    return " ".join(
        part
        for part in [
            item["name"],
            item["intro"],
            item["category"],
            item["cluster_name"],
            item.get("meta_description", ""),
            guide_titles,
        ]
        if part
    ).lower()


def build_calculator_cards(featured_slugs: set[str] | None = None) -> str:
    featured_slugs = set(featured_slugs or DEFAULT_FEATURED_SLUGS)
    parts = []
    for item in get_all_calculator_entries():
        guide_count = len(item["intent_pages"]) + len(item["guide_pages"])
        workflow_label = "Cost planning" if item.get("formula") == "project_cost" else "Materials"
        featured_badge = '<span class="card-chip card-chip-featured">Popular</span>' if item["slug"] in featured_slugs else ""
        parts.append(
            f'''
        <article class="tool-card directory-card" data-directory-card data-category="{escape(item["category"])}" data-search="{escape(_card_search_text(item))}">
          <div class="tool-card-top">
            <div class="card-chip-row">
              {featured_badge}
              <span class="card-chip">{escape(item["category"])}</span>
              <span class="card-chip card-chip-soft">{guide_count} guides</span>
            </div>
            <span class="card-meta-label">{escape(workflow_label)}</span>
          </div>
          <h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3>
          <p>{escape(item["intro"])}</p>
          <div class="card-meta-list">
            <span>{escape(item["cluster_name"])}</span>
            <span>Estimate • compare • brief</span>
          </div>
          <div class="tool-card-actions">
            <a class="text-link" href="/calculators/{escape(item["slug"])}/">Open calculator</a>
            <a class="text-link text-link-secondary" href="/clusters/{escape(item["cluster_slug"])}/">Open tool set</a>
          </div>
        </article>
        '''
        )
    return "".join(parts)


def render_directory_section(*, title: str, intro: str, cards_html: str, categories: list[str], count_text: str) -> str:
    filter_buttons = [
        '<button class="filter-chip is-active" type="button" data-filter-value="all">All calculators</button>'
    ]
    filter_buttons.extend(
        f'<button class="filter-chip" type="button" data-filter-value="{escape(category)}">{escape(category)}</button>'
        for category in categories
    )
    return f'''
    <section class="directory-section" data-directory-root>
      <div class="content-card directory-shell">
        <div class="section-head">
          <h2>{escape(title)}</h2>
          <p>{escape(intro)}</p>
        </div>
        <div class="directory-toolbar" role="search" aria-label="Calculator directory search">
          <label class="directory-search">
            <span class="sr-only">Search calculators</span>
            <input type="search" data-directory-search placeholder="Search paint, driveway cost, insulation, fence posts, packs, drainage...">
          </label>
          <button class="btn directory-reset" type="button" data-directory-reset>Reset</button>
        </div>
        <div class="directory-filter-row" data-directory-filters>
          {''.join(filter_buttons)}
        </div>
        <p class="directory-count" data-directory-count>{escape(count_text)}</p>
      </div>
      <div class="calculator-grid directory-grid" data-directory-grid>
        {cards_html}
      </div>
      <section class="content-card directory-empty" hidden data-directory-empty>
        <h3>No exact match yet</h3>
        <p>Try a broader material, project type, or buying term. Searching for words like packs, driveway, plasterboard, paint, or quote usually works well.</p>
      </section>
    </section>'''


def build_calculators_index(cards_html: str) -> str:
    crumbs = [("Home", "/"), ("Calculators", "/calculators/")]
    stats = calculator_directory_stats()
    categories = calculator_directory_categories()
    content = f'''
  <div class="site-shell">
    <section class="hero hero-compact">
      {render_breadcrumbs(crumbs)}
      <div class="eyebrow">Calculator directory</div>
      <h1>Choose the tool you need faster</h1>
      <p class="hero-copy">Search the library by job, material, or buying task, then open the matching calculator and its linked tool set for the next step.</p>
      <div class="hero-badges">
        <span class="hero-badge">{stats["calculator_count"]} calculators</span>
        <span class="hero-badge">{stats["cluster_count"]} tool sets</span>
        <span class="hero-badge">{stats["guide_count"]} support guides</span>
      </div>
    </section>
    {render_ad_slot("calculators-index-top")}
    {render_directory_section(title="Search the calculator library", intro="The strongest competitors make discovery easy. This directory now lets visitors filter by major job type and search the exact task they are trying to price or buy for.", cards_html=cards_html, categories=categories, count_text=f'Showing all {stats["calculator_count"]} calculators.')}
  </div>'''
    return render_layout(
        title=f'Calculators | {SITE["name"]}',
        description='Browse practical material calculators for building, decorating, outdoor projects, and early quote-planning decisions.',
        path="/calculators/",
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="calculator-index",
    )
