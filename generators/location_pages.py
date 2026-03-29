from html import escape

from components.publishing import render_ad_slot, render_breadcrumb_schema, render_breadcrumbs, render_layout, render_section_cards
from data.locations import (
    get_all_locations,
    get_calculators_for_location,
    get_clusters_for_location,
    get_location_groups,
    get_location_index_content,
    get_related_locations,
)
from data.publisher import PROJECT_HUB_LABEL, PROJECT_HUBS_LABEL, SITE


def render_location_quality_strip(kind: str) -> str:
    area_label = "Regional planning" if kind == "region" else "City planning"
    return (
        '<section class="quality-strip" aria-label="Freshness and methodology">'
        f'<article class="content-card quality-card"><div class="quality-kicker">Last checked</div><h2>{escape(SITE["updated_label"])}</h2><p>We reviewed the links, planning prompts, and local guidance structure on this page.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Scope</div><h2>{escape(area_label)}</h2><p>These pages explain what can vary locally without pretending to know every live price or contractor rate in the area.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Methodology</div><h2>Use the estimate first</h2><p>Start with the calculator, then use the local notes to check access, delivery, labour context, weather, and quote readiness.</p></article>'
        '</section>'
    )


def _location_local_checks(location: dict) -> list[tuple[str, str]]:
    access_title = 'Urban access and parking' if location['kind'] == 'city' else 'Travel and delivery spread'
    access_body = (
        'Check where materials can be unloaded, how long vehicles can stay, whether permits or restricted loading windows apply, and how far items still need to be moved by hand.'
        if location['kind'] == 'city'
        else 'Check delivery distance, travel time, merchant coverage, and whether the job is close to main supply routes or likely to need staged deliveries.'
    )
    return [
        (access_title, access_body),
        ('Weather and timing', 'Outdoor work often changes once weather windows, storage conditions, ground moisture, or sequencing with other trades are considered. Build that into the budget and timing discussion early.'),
        ('Property-type and site constraints', 'Older properties, tight gardens, shared drives, basements, upper floors, and uneven ground can all add labour time or change the buying format that is most practical.'),
    ]


def _location_budget_checks(location: dict) -> list[tuple[str, str]]:
    return [
        ('Buying and access checks', 'Confirm access, unloading distance, waste removal, storage space, and whether the site can realistically handle the pack size, pallet, bulk bag, or ready-mix route you first planned.'),
        ('How to compare local quotes', 'Send every contractor or supplier the same measurements, inclusions, exclusions, finish level, and timing notes so the quote spread reflects the work rather than mixed assumptions.'),
        ('When to allow more contingency', 'Add a little more contingency where ground conditions, hidden prep, access, awkward layouts, or weather-sensitive sequencing are still uncertain.'),
    ]


def _location_questions(location: dict) -> list[str]:
    name = location['name']
    return [
        f'Can you price this job for {name} on the same measured scope, including any access or delivery limits you can already see?',
        'What is included in your price for materials, labour, waste removal, delivery, and setup?',
        'Are there local access, parking, unloading, or timing issues that could change the total after the first visit?',
        'Which assumptions would you want confirmed before you treat the estimate as a working quote?',
    ]


def _location_quote_prompt(location: dict) -> str:
    prompt = (
        f'Example brief starter: "I am planning a job in {location["name"]}. The measured scope is ready, I have a BuildCostLab estimate, and I want the quote to show materials, labour, extras, lead time, and any access-related exclusions separately."'
    )
    return (
        '<section class="conversion-panel">'
        '<div class="section-head">'
        f'<h2>Local quote-prep prompt for {escape(location["name"])}</h2>'
        '<p>Use this wording as a starting point when you want local suppliers or installers to price the same scope more clearly.</p>'
        '</div>'
        f'<p class="conversion-note">{escape(prompt)}</p>'
        '<div class="conversion-actions">'
        '<a class="btn btn-primary" href="/quote-checklist/">Open quote checklist</a>'
        '<a class="btn" href="/contact/">Contact BuildCostLab</a>'
        '</div>'
        '</section>'
    )


def _questions_panel(location: dict) -> str:
    items = ''.join(f'<li>{escape(item)}</li>' for item in _location_questions(location))
    return (
        '<section class="conversion-panel">'
        '<div class="section-head">'
        f'<h2>Questions to ask suppliers or contractors in {escape(location["name"])}</h2>'
        '<p>These questions help expose the local assumptions that often sit behind the first headline price.</p>'
        '</div>'
        f'<ul class="conversion-list">{items}</ul>'
        '</section>'
    )


def _project_fit_cards(location: dict) -> list[tuple[str, str]]:
    return [
        ('Start with the main quantity question', 'Use the calculator that matches the actual material, layer, or project budget you need first. The local page is there to help you pressure-test that result, not replace it.'),
        ('Check what changes locally', 'After the first estimate, use the local notes to think through labour availability, access, delivery route, weather exposure, and property constraints before you treat the number as settled.'),
        ('Use the brief tools at the end', 'Once the quantity and local caveats feel realistic, move into the quote checklist or calculator export tools so the next conversation starts from a clearer scope.'),
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
            f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p><a class="text-link" href="/clusters/{escape(item["cluster_slug"])}/">Open {escape(PROJECT_HUB_LABEL.lower())}</a></article>'
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
            f'<article class="tool-card"><h3><a href="/locations/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>Compare planning notes, local checks, and starting calculators for {escape(item["name"])}.</p></article>'
            for item in related_locations
        )

        local_checks_html = ''.join(
            f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
            for title, body in _location_local_checks(location)
        )
        project_fit_html = ''.join(
            f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
            for title, body in _project_fit_cards(location)
        )

        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">{escape("Regional planning" if location["kind"] == "region" else "City planning")}</div>'
            f'<h1>{escape(location["headline"])}</h1>'
            f'<p class="hero-copy">{escape(location["intro"])}</p>'
            f'<div class="hero-badges"><span class="hero-badge">{len(calculators)} featured calculators</span><span class="hero-badge">{len(clusters)} {escape(PROJECT_HUBS_LABEL.lower())}</span><span class="hero-badge">Local planning checks included</span></div></section>'
            f'{render_ad_slot(f"{location["slug"]}-location-top")}'
            f'{render_location_quality_strip(location["kind"])}'
            '<section class="content-card prose-card"><h2>Start with the quantity, then check the local variables</h2><p>These location pages are here to make your estimate more useful locally. They explain what can vary in practice, such as labour pressure, delivery access, parking, weather exposure, property type, and how the job is likely to be supplied.</p></section>'
            f'<section class="stack-grid">{project_fit_html}</section>'
            '<section class="content-card prose-card"><h2>Best calculators to open first</h2><p>Use these pages to answer the main quantity or budget question before you start adjusting for local conditions.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{calculator_cards}</div></section>'
            '<section class="content-card prose-card"><h2>What can vary in this area</h2><p>These notes focus on the local issues that commonly move real buying decisions and quote comparisons.</p></section>'
            f'{render_section_cards(location["factors"])}'
            '<section class="content-card prose-card"><h2>What to check locally before budgeting</h2><p>Use these checks to turn a clean estimate into a more realistic plan for buying, booking, and comparing local quotes.</p></section>'
            f'<section class="stack-grid">{local_checks_html}</section>'
            f'{render_section_cards(_location_budget_checks(location))}'
            f'{_questions_panel(location)}'
            '<section class="content-card prose-card"><h2>Browse grouped project hubs</h2><p>Use these project hubs when the job includes linked materials, multiple buying formats, or several related calculators and guides.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{cluster_cards}</div></section>'
            '<section class="content-card prose-card"><h2>Helpful next-step guides</h2><p>Once the main quantity is clear, these guide pages help with waste, buying format, pack sizing, and the practical decisions that usually follow the first estimate.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{guide_cards}</div></section>'
            f'{_location_quote_prompt(location)}'
        )
        if related_cards:
            content += (
                '<section class="content-card prose-card"><h2>Compare nearby location pages</h2><p>These related pages make it easier to compare the same kind of job across nearby areas without changing the estimating logic.</p></section>'
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
        '<section class="content-card prose-card"><h2>UK regions</h2><p>Start here if you want broader planning notes for a wider area before moving into calculators and project hubs.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{region_cards}</div></section>'
        '<section class="content-card prose-card"><h2>Major cities</h2><p>Use the city pages for tighter checks around access, delivery, weather exposure, property constraints, and local quote preparation.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{city_cards}</div></section>'
        '<section class="quality-strip" aria-label="How to use this section">'
        '<article class="content-card quality-card"><div class="quality-kicker">1</div><h2>Choose the area</h2><p>Pick the city or region that best matches the job location.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">2</div><h2>Open the right calculator</h2><p>Start with the material or cost page that answers the first quantity question clearly.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">3</div><h2>Pressure-test locally</h2><p>Use the location notes to check labour, delivery, access, weather, and quote-readiness before you commit.</p></article>'
        '</section>'
        '</div>'
    )
    return path, render_layout(
        title=f'Locations | {SITE["name"]}',
        description='Browse BuildCostLab location pages for UK regions and cities, then jump into the right calculators and project hubs.',
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="location-index",
    )
