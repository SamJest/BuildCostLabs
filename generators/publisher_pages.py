from html import escape

from components.publishing import (
    family_lookup,
    render_ad_slot,
    render_breadcrumb_schema,
    render_breadcrumbs,
    render_faq_schema,
    render_layout,
    render_section_cards,
)
from data.catalog import get_all_calculators, get_cluster_intro
from data.publisher import SITE, TRUST_PAGES


def build_trust_pages():
    pages = []
    for page in TRUST_PAGES:
        path = f'/{page["slug"]}/'
        crumbs = [("Home", "/"), (page["title"], path)]
        sections = render_section_cards([(item["title"], item["body"]) for item in page["sections"]])
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">Publisher information</div><h1>{escape(page["headline"])}</h1>'
            f'<p class="hero-copy">{escape(page["intro"])}</p></section>'
            f'{render_ad_slot("trust-top")}{sections}</div>'
        )
        html = render_layout(
            title=page["title"],
            description=page["description"],
            path=path,
            content=content,
            schema=[render_breadcrumb_schema(crumbs)],
            page_type="trust",
        )
        pages.append((path, html))
    return pages


def build_cluster_pages():
    pages = []
    clusters = {}
    for item in get_all_calculators():
        clusters.setdefault(item["cluster_slug"], []).append(item)
    for cluster_slug, items in clusters.items():
        family = items[0]
        key = family["key"]
        path = f'/clusters/{cluster_slug}/'
        crumbs = [("Home", "/"), ("Clusters", "/clusters/"), (family["cluster_name"], path)]
        cluster_guides = []
        for calculator in items:
            cluster_guides.extend(calculator["intent_pages"] + calculator["guide_pages"])
        intent_links = "".join(
            f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p></article>'
            for item in cluster_guides
        )
        calculator_cards = "".join(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
            for item in items
        )
        intent_section = ""
        if intent_links:
            intent_section = f'<section class="calculator-grid-section"><div class="calculator-grid">{intent_links}</div></section>'
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">Cluster hub</div><h1>{escape(family["cluster_name"])}</h1>'
            f'<p class="hero-copy">{escape(get_cluster_intro(cluster_slug, family["intro"]))}</p>'
            f'<div class="hero-badges"><span class="hero-badge">{escape(family["category"])}</span><span class="hero-badge">{len(items)} calculators</span><span class="hero-badge">Ad-ready templates</span></div></section>'
            f'{render_ad_slot(f"{key}-hub-top")}'
            f'<section class="content-card prose-card"><h2>Core calculators in this cluster</h2><p>Use this hub to move between closely related calculators in the same topic family. The goal is to keep the estimating journey connected instead of forcing one page to do every job.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{calculator_cards}</div></section>'
            f'{render_section_cards([("How to use this cluster", "Start with the calculator that matches the material or buying format you actually need, then move sideways into related tools if the job expands."), ("What affects estimates most", "Dimensions, depth or coverage assumptions, waste allowance, and pack or stock-length rounding are usually the biggest drivers of the final buying number."), ("How this helps SEO", "These cluster hubs create clear internal-link pathways between calculators, supporting guides, and next-step commercial intent without duplicating one generic explanation everywhere.")])}'
            f'{intent_section}</div>'
        )
        html = render_layout(
            title=f'{family["cluster_name"]} | {SITE["name"]}',
            description=f'Browse {family["cluster_name"].lower()} calculators and supporting guides on {SITE["name"]}.',
            path=path,
            content=content,
            schema=[render_breadcrumb_schema(crumbs)],
            page_type="cluster",
        )
        pages.append((path, html))
    return pages


def build_guide_pages():
    pages = []
    for family in get_all_calculators():
        key = family["key"]
        related = family["intent_pages"] + family["guide_pages"]
        for item in related:
            path = f'/guides/{item["slug"]}/'
            crumbs = [("Home", "/"), ("Guides", "/guides/"), (item["title"], path)]
            supporting_cards = [
                ("Why this page exists", family["support"]["use_case"]),
                ("Core assumption", family["support"]["assumptions"]),
                ("Common mistake", family["support"]["mistakes"]),
            ]
            content = (
                f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
                f'<div class="eyebrow">{escape(family["cluster_name"])}</div><h1>{escape(item["headline"])}</h1>'
                f'<p class="hero-copy">{escape(item["intro"])}</p></section>'
                f'{render_ad_slot(f"{key}-guide-top")}'
                f'{render_quality_strip("guide")}'
                f'<section class="content-card prose-card"><h2>Use the calculator first</h2><p>The quickest path is to start with <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>, then use this guide to sense-check the result and decide what to buy next.</p></section>'
                f'{render_section_cards(supporting_cards)}'
                f'<section class="content-card prose-card"><h2>Next step links</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} cluster</a> or go straight to the <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>.</p></section></div>'
            )
            html = render_layout(
                title=f'{item["title"]} | {SITE["name"]}',
                description=item["description"],
                path=path,
                content=content,
                schema=[render_breadcrumb_schema(crumbs)],
                page_type="guide",
            )
            pages.append((path, html))
    return pages


def render_quality_strip(page_type: str) -> str:
    return (
        '<section class="quality-strip" aria-label="Freshness and methodology">'
        f'<article class="content-card quality-card"><div class="quality-kicker">Updated</div><h2>{escape(SITE["updated_label"])}</h2><p>Reviewed against the current calculator logic, structured content, and internal linking used on BuildCostLabs.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Methodology</div><h2>Planning-first estimate</h2><p>Use this {escape(page_type)} to build a quick order or budget estimate, then confirm against product coverage data, site conditions, and supplier pack sizes.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Trust</div><h2>How we publish</h2><p>See the <a href="{escape(SITE["methodology_path"])}">calculator methodology</a> and <a href="{escape(SITE["editorial_policy_path"])}">editorial policy</a> for the standards behind these pages.</p></article>'
        '</section>'
    )


def build_calculator_support(slug: str) -> str:
    family = family_lookup()[slug]
    key = family["key"]
    faq_html = "".join(
        f'<article class="content-card prose-card"><h2>{escape(item["q"])}</h2><p>{escape(item["a"])}</p></article>'
        for item in family["faqs"]
    )
    next_links = "".join(
        f'<a class="mini-tool-card" href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a>'
        for item in family["intent_pages"] + family["guide_pages"]
    )
    next_step_section = ""
    if next_links:
        next_step_section = f'<section class="related-tools"><div class="section-head"><h2>Next-step guides</h2><p>Keep users moving through the cluster instead of bouncing after one result.</p></div><div class="mini-tool-grid">{next_links}</div></section>'
    return (
        f'{render_ad_slot(f"{key}-mid")}'
        f'{render_section_cards([("Assumptions", family["support"]["assumptions"]), ("Common mistakes", family["support"]["mistakes"]), ("Best use cases", family["support"]["use_case"]), ("How to get a better estimate", family["support"].get("estimate_tip", "Measure carefully, apply realistic waste, and sense-check the result against how the product is actually sold.")), ("Buyer note", family["support"].get("buyer_tip", "Round to whole buying units and compare product coverage before buying solely on sticker price.")), ("UK and US note", family["support"].get("market_note", "Unit wording and supplier pack conventions differ between markets, but the estimating logic still starts with geometry, waste, and whole-unit ordering.")), ("Commercial next step", "After checking quantity, compare product coverage, pack size, delivery cost, and whether buying an extra unit reduces the risk of a stalled job.")])}'
        f'<section class="content-card prose-card"><h2>Explore this topic cluster</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} hub</a> to move from quick estimate to deeper guidance.</p></section>'
        f'{next_step_section}'
        f'<section class="stack-grid">{faq_html}</section>'
    )


def render_calculator_page(*, slug: str, title: str, description: str, intro: str, form_html: str, result_html: str, script_name: str) -> str:
    family = family_lookup()[slug]
    key = family["key"]
    path = f"/calculators/{slug}/"
    crumbs = [("Home", "/"), ("Calculators", "/calculators/"), (title, path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        f'<div class="eyebrow">{escape(family["hero_eyebrow"])}</div><h1>{escape(title)}</h1>'
        f'<p class="hero-copy">{escape(intro)}</p></section>'
        f'{render_ad_slot(f"{key}-top")}'
        f'{render_quality_strip("calculator")}'
        f'<section class="calculator-layout"><div class="content-card calculator-card">{form_html}</div><aside class="content-card result-card">{result_html}</aside></section>'
        f'{build_calculator_support(slug)}</div><script src="/assets/js/global-calculator.js"></script><script src="/assets/js/{escape(script_name)}"></script>'
    )
    return render_layout(
        title=f"{title} | {SITE['name']}",
        description=description,
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs), render_faq_schema(family["faqs"])],
        page_type="calculator",
    )


def build_guides_index() -> tuple[str, str]:
    cards = []
    for family in get_all_calculators():
        for item in family["intent_pages"] + family["guide_pages"]:
            cards.append(
                f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p></article>'
            )
    path = "/guides/"
    crumbs = [("Home", "/"), ("Guides", path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Guide library</div><h1>Supporting guides built around calculator intent</h1>'
        '<p class="hero-copy">These pages are written to support real estimating and buying decisions, then route users back into the right calculator or cluster.</p></section>'
        f'{render_ad_slot("guides-index-top")}'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(cards)}</div></section></div>'
    )
    return path, render_layout(
        title=f'Guides | {SITE["name"]}',
        description="Browse BuildCostLabs guides covering material quantities, waste, and rough cost decisions.",
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="guide-index",
    )


def build_clusters_index() -> tuple[str, str]:
    seen = set()
    parts = []
    for item in get_all_calculators():
        if item["cluster_slug"] in seen:
            continue
        seen.add(item["cluster_slug"])
        parts.append(
            f'<article class="tool-card"><h3><a href="/clusters/{escape(item["cluster_slug"])}/">{escape(item["cluster_name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
        )
    cards = "".join(parts)
    path = "/clusters/"
    crumbs = [("Home", "/"), ("Clusters", path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Topic hubs</div><h1>Calculator clusters built for search intent</h1>'
        '<p class="hero-copy">Each cluster combines a core calculator, next-step guides, and internal links designed to keep users moving through the topic.</p></section>'
        f'{render_ad_slot("clusters-index-top")}'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section></div>'
    )
    return path, render_layout(
        title=f'Clusters | {SITE["name"]}',
        description="Browse BuildCostLabs topic clusters for calculators, guides, and next-step buying content.",
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="cluster-index",
    )
