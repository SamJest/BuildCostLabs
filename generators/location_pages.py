from html import escape

from components.publishing import (
    render_ad_slot,
    render_breadcrumb_schema,
    render_breadcrumbs,
    render_layout,
    render_section_cards,
)
from data.locations import (
    get_all_locations,
    get_calculators_for_location,
    get_clusters_for_location,
    get_location_groups,
    get_location_index_content,
    get_related_locations,
)
from data.publisher import SITE


def render_location_quality_strip(kind: str) -> str:
    title = "Regional planning note" if kind == "region" else "City planning note"
    return (
        '<section class="quality-strip" aria-label="Freshness and methodology">'
        f'<article class="content-card quality-card"><div class="quality-kicker">Last checked</div><h2>{escape(SITE["updated_label"])}</h2><p>We checked the calculator links, local planning notes, and related tool-set routing on this page.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">How to use it</div><h2>{escape(title)}</h2><p>Start with the right calculator for the job, then use this location page to sense-check access, delivery, labour context, and the local conditions around the site.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Why trust it</div><h2>See how the site is maintained</h2><p>Read the <a href="{escape(SITE["methodology_path"])}">calculator methodology</a> and <a href="{escape(SITE["editorial_policy_path"])}">editorial policy</a> for the standards behind these pages.</p></article>'
        '</section>'
    )



def _location_local_checks(location: dict) -> list[tuple[str, str]]:
    base = [
        ('Access and delivery', 'Confirm where materials can be unloaded, how close the drop point is to the job, and whether staged deliveries are more realistic than one large load.'),
        ('Quote comparison', 'Send merchants or installers the same measured scope, finish assumption, and exclusions so the local price spread is easier to trust.'),
        ('Order timing', 'Check lead times, access windows, and whether weather or sequencing with other work could force the order to be split.'),
    ]
    if location['kind'] == 'city':
        base[0] = ('Urban access check', 'Parking, loading space, neighbours, and smaller delivery windows can move cost and practicality faster in city jobs than the raw material quantity does.')
    else:
        base[0] = ('Regional spread check', 'Travel time, merchant coverage, and whether the job sits in a dense urban pocket or a more spread-out area can change labour and delivery assumptions.')
    return base



def _location_project_fit(location: dict) -> list[tuple[str, str]]:
    return [
        ('Best jobs to start here', 'Use the calculators first for the material or task you actually need, then use this location page to pressure-test the estimate against local delivery, access, labour, and weather context.'),
        ('What to tell suppliers', 'Share the measured dimensions, the preferred material route, any access limits, the timing window, and whether you want materials only or labour included.'),
        ('What to recheck locally', 'Confirm waste removal, unloading, parking, storage space, and whether the site can realistically take the buying format you first planned.'),
    ]


def build_location_pages():
    pages = []
    for location in get_all_locations():
        path = f'/locations/{location["slug"]}/'
        crumbs = [("Home", "/"), ("Locations", "/locations/"), (location["name"], path)]
        calculators = get_calculators_for_location(location)
        clusters = get_clusters_for_location(location)
        related_locations = get_related_locations(location)

        calculator_cards = "".join(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p><a class="text-link" href="/clusters/{escape(item["cluster_slug"])}/">Open {escape(item["cluster_name"])} </a></article>'
            for item in calculators
        )
        cluster_cards = "".join(
            f'<article class="tool-card"><h3><a href="/clusters/{escape(item["cluster_slug"])}/">{escape(item["cluster_name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
            for item in clusters
        )
        guide_cards = "".join(
            f'<article class="tool-card"><h3><a href="/guides/{escape(calc["intent_pages"][0]["slug"] if calc["intent_pages"] else calc["guide_pages"][0]["slug"])}' \
            f'/">{escape(calc["intent_pages"][0]["title"] if calc["intent_pages"] else calc["guide_pages"][0]["title"])}</a></h3>'
            f'<p>{escape(calc["intent_pages"][0]["description"] if calc["intent_pages"] else calc["guide_pages"][0]["description"])}</p></article>'
            for calc in calculators[:4]
            if calc.get("intent_pages") or calc.get("guide_pages")
        )
        related_cards = "".join(
            f'<article class="tool-card"><h3><a href="/locations/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>Compare local planning notes, tool sets, and starting calculators for {escape(item["name"])}.</p></article>'
            for item in related_locations
        )

        local_checks_html = ''.join(
            f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
            for title, body in _location_local_checks(location)
        )
        project_fit_html = ''.join(
            f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
            for title, body in _location_project_fit(location)
        )

        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">{escape("Regional planning" if location["kind"] == "region" else "City planning")}</div>'
            f'<h1>{escape(location["headline"])}</h1>'
            f'<p class="hero-copy">{escape(location["intro"])}</p>'
            f'<div class="hero-badges"><span class="hero-badge">{len(calculators)} featured calculators</span><span class="hero-badge">{len(clusters)} grouped tool sets</span><span class="hero-badge">UK-focused planning notes</span></div></section>'
            f'{render_ad_slot(f"{location["slug"]}-location-top")}'
            f'{render_location_quality_strip(location["kind"])}'
            '<section class="content-card prose-card"><h2>Start with the quantity, then check the local variables</h2><p>These location pages are not here to replace the calculators. They exist to help you use the right calculator first, then sense-check the estimate against common local variables such as access, delivery, labour context, waste handling, and weather exposure.</p></section>'
            f'<section class="stack-grid">{project_fit_html}</section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{calculator_cards}</div></section>'
            f'{render_section_cards(location["factors"])}'
            '<section class="content-card prose-card"><h2>Local planning checks before you request quotes</h2><p>Use these prompts to turn a clean quantity estimate into a more realistic local buying or quote-comparison brief.</p></section>'
            f'<section class="stack-grid">{local_checks_html}</section>'
            '<section class="content-card prose-card"><h2>Browse grouped tool sets</h2><p>Use these tool sets when the job includes linked materials, multiple buying formats, or a mix of calculators and supporting guides.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{cluster_cards}</div></section>'
            '<section class="content-card prose-card"><h2>Helpful next-step guides</h2><p>Once the main quantity is clear, these guide pages help with waste, buying format, pack sizing, and the practical decisions that usually follow the first estimate.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{guide_cards}</div></section>'
        )
        if related_cards:
            content += (
                '<section class="content-card prose-card"><h2>Compare nearby location pages</h2><p>These related pages make it easier to compare the same type of job across different areas without changing the estimating logic.</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{related_cards}</div></section>'
            )
        content += '</div>'


        html = render_layout(
            title=f'{location["name"]} Building Cost and Material Calculators | {SITE["name"]}',
            description=location["description"],
            path=path,
            content=content,
            schema=[render_breadcrumb_schema(crumbs)],
            page_type="location",
        )
        pages.append((path, html))
    return pages



def build_locations_index() -> tuple[str, str]:
    content_meta = get_location_index_content()
    groups = get_location_groups()
    region_cards = "".join(
        f'<article class="tool-card"><h3><a href="/locations/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
        for item in groups["regions"]
    )
    city_cards = "".join(
        f'<article class="tool-card"><h3><a href="/locations/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
        for item in groups["cities"]
    )
    path = "/locations/"
    crumbs = [("Home", "/"), ("Locations", path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Location library</div>'
        f'<h1>{escape(content_meta["headline"])}</h1>'
        f'<p class="hero-copy">{escape(content_meta["intro"])}</p></section>'
        f'{render_ad_slot("locations-index-top")}'
        '<section class="content-card prose-card"><h2>UK regions</h2><p>Start here if you want broad planning notes for a larger area before moving into calculators and tool sets.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{region_cards}</div></section>'
        '<section class="content-card prose-card"><h2>Major cities</h2><p>Use the city pages for tighter planning notes, quote-checking context, and links into the strongest calculator families for that area.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{city_cards}</div></section>'
        '<section class="content-card prose-card"><h2>How to use this section</h2><p>Pick the area that best matches the job, start with the calculator that fits the material or task, then use the location notes to think through access, delivery, labour context, weather, and buying route before you request quotes.</p></section>'
        '</div>'
    )
    return path, render_layout(
        title=f'Locations | {SITE["name"]}',
        description='Browse BuildCostLab location pages for UK regions and cities, then jump into the right calculators and grouped tool sets.',
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="location-index",
    )
