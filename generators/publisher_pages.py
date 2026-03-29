from html import escape

from components.publishing import (
    family_lookup,
    get_all_calculator_entries,
    render_ad_slot,
    render_breadcrumb_schema,
    render_breadcrumbs,
    render_faq_schema,
    render_layout,
    render_section_cards,
    render_software_application_schema,
)
from data.catalog import get_all_calculators, get_cluster_hub_content, get_cluster_intro
from data.publisher import PROJECT_HUB_LABEL, PROJECT_HUBS_LABEL, SITE, TRUST_PAGES


# ---------- Shared shells ----------

def render_cost_intelligence_shell() -> str:
    return (
        '<div class="result-intelligence">'
        '<section class="intelligence-panel">'
        '<div class="result-kicker">Estimate range</div>'
        '<h3>Low, mid, and high view</h3>'
        '<div class="scenario-grid" id="estimate-range"><div class="scenario-card"><strong>Waiting for inputs</strong><span>Complete the calculator to see a range.</span></div></div>'
        '<p class="intelligence-copy" id="estimate-drivers">The biggest cost drivers and uncertainty notes will appear here.</p>'
        '<p class="intelligence-copy intelligence-confidence" id="confidence-note">Confidence guidance updates once the calculator has a live result.</p>'
        '</section>'
        '<section class="intelligence-panel">'
        '<div class="result-kicker">Cost breakdown</div>'
        '<h3>What the total usually includes</h3>'
        '<div class="detail-list" id="cost-intelligence-breakdown"><div class="break-row"><span>Materials</span><strong>Waiting for inputs</strong></div></div>'
        '</section>'
        '<section class="intelligence-panel">'
        '<div class="result-kicker">Compare options</div>'
        '<h3>Budget, standard, and higher-spec routes</h3>'
        '<div class="compare-grid" id="comparison-output"><div class="compare-card"><strong>Waiting for inputs</strong><span>Option comparisons appear after a calculation.</span></div></div>'
        '</section>'
        '<section class="intelligence-panel">'
        '<div class="result-kicker">Typical timeline</div>'
        '<h3>Prep, install, and finish</h3>'
        '<div class="detail-list" id="timeline-output"><div class="break-row"><span>Timeline</span><strong>Waiting for inputs</strong></div></div>'
        '</section>'
        '<section class="intelligence-panel">'
        '<div class="result-kicker">Reality check</div>'
        '<h3>Real-world costs people miss</h3>'
        '<ul class="reality-list" id="reality-output"><li>Complete the calculator to see the extra items that commonly catch budgets out.</li></ul>'
        '</section>'
        '</div>'
    )


def render_calculator_jump_nav() -> str:
    return (
        '<nav class="section-jump-nav" aria-label="On this page">'
        '<a class="jump-chip" href="#calculator">Calculator</a>'
        '<a class="jump-chip" href="#quote-brief">Quote brief</a>'
        '<a class="jump-chip" href="#buying-checks">Buying checks</a>'
        '<a class="jump-chip" href="#next-guides">Next-step guides</a>'
        '<a class="jump-chip" href="#faqs">FAQs</a>'
        '</nav>'
    )


def render_quality_strip(page_type: str) -> str:
    page_name = page_type if page_type not in {"project hub", "guide", "calculator"} else page_type
    return (
        '<section class="quality-strip" aria-label="Freshness and methodology">'
        f'<article class="content-card quality-card"><div class="quality-kicker">Last checked</div><h2>{escape(SITE["updated_label"])}</h2><p>We checked the page logic, support notes, and related links on this page.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">How to use it</div><h2>Planning before buying</h2><p>Use this {escape(page_name)} for a planning check, then confirm the final order or quote against live product data and site conditions.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Why trust it</div><h2>See how the site is maintained</h2><p>Read the <a href="{escape(SITE["methodology_path"])}">calculator methodology</a> and <a href="{escape(SITE["editorial_policy_path"])}">editorial policy</a> for the standards behind these pages.</p></article>'
        '</section>'
    )


# ---------- Trust center helpers ----------

def _trust_summary_html(page: dict) -> str:
    cards = page.get("summary_cards", [])
    if not cards:
        return ""
    inner = "".join(
        f'<article class="content-card quality-card"><div class="quality-kicker">Overview</div><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
        for title, body in cards
    )
    return f'<section class="quality-strip" aria-label="Trust page summary">{inner}</section>'


def _trust_notice_html(page: dict) -> str:
    if not page.get("notice_title") or not page.get("notice_body"):
        return ""
    return f'<section class="content-card prose-card"><h2>{escape(page["notice_title"])}</h2><p>{escape(page["notice_body"])}</p></section>'


def _trust_links_html(page: dict) -> str:
    links = page.get("related_links", [])
    if not links:
        return ""
    actions = "".join(f'<a class="btn" href="{escape(href)}">{escape(label)}</a>' for label, href in links)
    return (
        '<section class="conversion-panel">'
        '<div class="section-head"><h2>Related trust pages</h2><p>Use these pages together when you want to understand how estimates are built, reviewed, and meant to be used.</p></div>'
        f'<div class="conversion-actions">{actions}</div>'
        '</section>'
    )


# ---------- Calculator helpers ----------

def _calculator_summary_cards(family: dict) -> list[tuple[str, str]]:
    formula = family.get("formula")
    quick = {
        "coverage": "Best for turning a measured area into a safer buying quantity before you compare pack sizes or place an order.",
        "volume": "Best for converting dimensions and depth into a delivered quantity before you choose bagged, bulk, or loose supply.",
        "linear": "Best for turning a clean run into a stock-length order with a more realistic allowance for cuts and joins.",
        "project_cost": "Best for early planning, option comparison, and quote preparation before the live contractor scope is fully locked down.",
    }
    return [
        ("Quick answer", quick.get(formula, family["support"]["use_case"])),
        ("Watch most", family["support"]["mistakes"]),
        ("Best next move", family["support"].get("estimate_tip", family["support"]["final_check"])),
    ]


def _calculator_scope_cards(family: dict) -> list[tuple[str, str]]:
    formula = family.get("formula")
    includes = {
        "coverage": "The measured coverage area, stated product yield or pack coverage, waste allowance, whole-unit rounding, and a rough material spend when a price is entered.",
        "volume": "The measured volume, waste-adjusted buying quantity, density or unit-size conversion, and a rough material spend when a price is entered.",
        "linear": "The total run, waste or cutting allowance, whole stock-length rounding, and a rough material spend when a price is entered.",
        "project_cost": "The measured project size, planning allowances for materials, labour, extras, contingency, and a comparison-friendly budget range.",
    }
    excludes = {
        "coverage": "Live product instructions, substrate preparation, delivery charges, labour, and installation details that depend on the specific product system.",
        "volume": "Unexpected excavation differences, compaction behaviour, haulage constraints, and local delivery charges unless you add them separately.",
        "linear": "Corners, fittings, trims, labour, and awkward site details that may need their own count outside the clean run length.",
        "project_cost": "Fixed contractor pricing, hidden defects, structural changes, surveys, permits, and any local rate that needs a real quote to confirm.",
    }
    return [
        ("What this estimate includes", includes.get(formula, family["support"]["use_case"])),
        ("What it may not include", excludes.get(formula, family["support"]["final_check"])),
        ("Key assumptions", family["support"]["assumptions"]),
    ]


def _calculator_worked_example_text(family: dict) -> str:
    slug = family["slug"]
    formula = family.get("formula")
    if "paint" in slug and "cost" not in slug:
        return "Example: 12m² of wall area with a paint coverage rate of 10m² per tin and 10 percent waste becomes 13.2m² of planned coverage. That is 1.32 tins on paper, so the safer buying decision is 2 tins."
    if "concrete" in slug and formula != "project_cost":
        return "Example: a 4m by 3m slab at 100mm depth gives 1.2m³ before waste. Add 10 percent and the planning quantity becomes 1.32m³, which is the number to compare against bagged or ready-mix buying routes."
    if "gravel" in slug or "sub-base" in slug or "mot-type-1" in slug:
        return "Example: a 5m by 3m area at 50mm depth gives 0.75m³ before waste. Add 10 percent and the planning quantity becomes 0.825m³. From there you can compare bulk bags, loose loads, or tonnage-based supply."
    if "deck" in slug:
        return "Example: an 18m² deck with 10 percent waste becomes 19.8m² of buying allowance. The board count is only part of the job, so check screws, joists, trims, and awkward cuts before you treat the first total as final."
    if "floor" in slug and formula == "coverage":
        return "Example: a 14m² room with 8 percent waste becomes 15.12m² of buying coverage. If the product is sold by pack, compare that figure against the pack yield and round up to the next full pack."
    if "tile" in slug and formula == "coverage":
        return "Example: 9m² of tiled area with 12 percent waste becomes 10.08m² of planned coverage. That is the safer figure to use when you compare tile boxes, adhesive bags, and grout allowances."
    if "fence" in slug:
        return "Example: a 15m run with 1.8m panels does not only need a panel count. It also needs a sensible allowance for posts, gravel boards, concrete, and any shorter end section that changes the final buying list."
    if formula == "coverage":
        return "Example: 12m² of measured coverage with 10 percent waste becomes 13.2m² of planned coverage. Divide by the real pack or unit yield, then round up to the next full buying unit."
    if formula == "volume":
        return "Example: 4m by 3m by 50mm gives 0.6m³ before waste. Add 10 percent and the planning quantity becomes 0.66m³. Then compare that number against the way the product is actually sold."
    if formula == "linear":
        return "Example: an 18m run with 8 percent waste becomes 19.44m of planned coverage. If lengths are sold in 2.4m pieces, the safer order is 9 lengths rather than 8.1 on paper."
    return "Example: a 20m² job at £60 per m² for materials, £45 per m² for labour, and £12 per m² for extras creates a baseline planning rate of £117 per m² before complexity and contingency are added."


def _calculator_driver_cards(family: dict) -> list[tuple[str, str]]:
    formula = family.get("formula")
    cards = {
        "coverage": [
            ("What changes the result most", "Real product yield, waste, awkward cuts, surface condition, and whole-pack rounding usually move the final order more than people expect."),
            ("When this estimate breaks", "Remeasure when the product coverage is uncertain, the layout is heavily cut up, or the supplier sells in pack sizes that do not match the default assumptions."),
            ("Practical buying checks", "Check batch matching, spare stock, delivery timing, and whether running short would be more expensive than buying one extra unit."),
        ],
        "volume": [
            ("What changes the result most", "Installed depth, loose-versus-compacted behaviour, density assumptions, and buying format usually move the real order fastest."),
            ("When this estimate breaks", "Remeasure when excavation depth changes across the job, the substrate is uneven, or the supplier grades the material differently from your assumption."),
            ("Practical buying checks", "Compare bags, bulk bags, loose loads, minimum order quantities, access for delivery vehicles, and whether the site can store the chosen route."),
        ],
        "linear": [
            ("What changes the result most", "Corners, joints, fittings, waste from stock lengths, and awkward end conditions often change the final order more than the clean run length."),
            ("When this estimate breaks", "Check again when the run includes mitres, several branches, unusual fittings, or hidden details that are not covered by a single straight-line measurement."),
            ("Practical buying checks", "Confirm stock lengths, accessory counts, fixing method, and whether one extra length is cheaper than a return trip or delayed install."),
        ],
        "project_cost": [
            ("What changes the cost most", "Labour rate, prep scope, finish level, access, complexity, and contingency usually matter more than the measured area alone."),
            ("When this estimate breaks", "Get a real quote when the site may hide defects, access is restricted, structural work is involved, or the finish specification is still moving."),
            ("Practical labour checks", "Ask builders to separate labour, materials, extras, lead time, and exclusions so the quote spread is easier to understand and challenge."),
        ],
    }
    return cards.get(formula, [])


def _calculator_checklist_panel(family: dict) -> str:
    formula = family.get("formula")
    items_map = {
        "coverage": [
            "State the measured area, product choice, waste allowance, and how the material is sold.",
            "Ask the supplier or installer to confirm real coverage and whether substrate condition changes the quantity.",
            "Check whether one spare unit is sensible for matching, touch-ups, awkward cuts, or batch consistency.",
        ],
        "volume": [
            "State the measured area, target depth, and whether the depth is compacted or loose-delivered.",
            "Ask how the material will be supplied: bags, bulk bags, loose load, or ready-mix route where relevant.",
            "Flag any access, storage, delivery, or waste-removal limits before the first quote is treated as final.",
        ],
        "linear": [
            "Share the total run, the number of corners or fittings, and the preferred stock length if you know it.",
            "Ask whether fixings, trims, connectors, and waste from offcuts are included.",
            "Confirm whether the job needs one clean install or a small spare allowance for mistakes and future repairs.",
        ],
        "project_cost": [
            "Share the measured scope, preferred finish, timing, and whether the price should include materials, labour, or both.",
            "Ask for labour, materials, extras, and exclusions to be shown separately.",
            "State any access, parking, disposal, delivery, or phasing constraints up front so they do not appear as surprises later.",
        ],
    }
    items_html = "".join(f'<li>{escape(item)}</li>' for item in items_map.get(formula, []))
    return (
        '<section class="conversion-panel">'
        '<div class="section-head"><h2>Quote-ready checklist</h2><p>Use these prompts when you want to turn the estimate into a clearer builder, installer, or merchant request.</p></div>'
        f'<ul class="conversion-list">{items_html}</ul>'
        '</section>'
    )


# ---------- Trust center ----------

def build_trust_pages():
    pages = []
    for page in TRUST_PAGES:
        path = f'/{page["slug"]}/'
        crumbs = [("Home", "/"), (page["title"], path)]
        sections = render_section_cards([(item["title"], item["body"]) for item in page["sections"]])
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">Trust center</div><h1>{escape(page["headline"])}</h1>'
            f'<p class="hero-copy">{escape(page["intro"])}</p></section>'
            f'{render_ad_slot("trust-top")}'
            f'{_trust_summary_html(page)}'
            f'{_trust_notice_html(page)}'
            f'{sections}'
            f'{_trust_links_html(page)}'
            '</div>'
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


# ---------- Project hubs ----------

def build_cluster_pages():
    pages = []
    clusters = {}
    for item in get_all_calculator_entries():
        clusters.setdefault(item["cluster_slug"], []).append(item)
    for cluster_slug, items in clusters.items():
        family = items[0]
        hub_content = get_cluster_hub_content(cluster_slug)
        key = family["key"]
        path = f'/clusters/{cluster_slug}/'
        crumbs = [("Home", "/"), (PROJECT_HUBS_LABEL, "/clusters/"), (family["cluster_name"], path)]
        intent_pages = []
        guide_pages = []
        for calculator in items:
            intent_pages.extend(calculator["intent_pages"])
            guide_pages.extend(calculator["guide_pages"])

        featured_slugs = hub_content.get("featured_slugs", [item["slug"] for item in items[:3]])
        featured_items = [item for item in items if item["slug"] in featured_slugs]
        remaining_items = [item for item in items if item["slug"] not in featured_slugs]

        featured_cards = "".join(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
            for item in featured_items
        )
        calculator_cards = "".join(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
            for item in remaining_items
        )
        intent_links = "".join(
            f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p></article>'
            for item in intent_pages
        )
        guide_links = "".join(
            f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p></article>'
            for item in guide_pages
        )

        featured_section = ""
        if featured_cards:
            featured_section = (
                f'<section class="content-card prose-card"><h2>{escape(hub_content.get("start_here_title", "Start here"))}</h2>'
                f'<p>{escape(hub_content.get("start_here_intro", "Start with the calculator that best matches the main material or buying format for the job."))}</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{featured_cards}</div></section>'
            )
        calculator_section = ""
        if calculator_cards:
            calculator_section = (
                '<section class="content-card prose-card"><h2>More calculators in this hub</h2>'
                '<p>Use these related pages when the same project includes extra materials, linked layers, or a different buying format.</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{calculator_cards}</div></section>'
            )
        intent_section = ""
        if intent_links:
            intent_section = (
                f'<section class="content-card prose-card"><h2>{escape(hub_content.get("question_heading", "Popular question pages"))}</h2>'
                f'<p>{escape(hub_content.get("question_intro", "Use these pages for faster answers when you already know the basic dimensions of the job."))}</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{intent_links}</div></section>'
            )
        guide_section = ""
        if guide_links:
            guide_section = (
                f'<section class="content-card prose-card"><h2>{escape(hub_content.get("guide_heading", "Guides and next steps"))}</h2>'
                f'<p>{escape(hub_content.get("guide_intro", "These guides help explain waste, product choice, and buying format once the first estimate is clear."))}</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{guide_links}</div></section>'
            )

        default_notes = [
            ("How to use this project hub", "Start with the calculator that matches the material or buying format you actually need, then move into the related guides if you need more detail before buying or requesting quotes."),
            ("What affects estimates most", "Dimensions, depth or coverage assumptions, waste allowance, and pack or stock-length rounding are usually the biggest drivers of the final buying number."),
            ("Why the linked guides matter", "The extra guides in each hub explain common mistakes, trade-offs, and buying choices that a simple quantity figure cannot cover on its own."),
        ]
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">{escape(PROJECT_HUB_LABEL)}</div><h1>{escape(family["cluster_name"])}</h1>'
            f'<p class="hero-copy">{escape(get_cluster_intro(cluster_slug, family["intro"]))}</p>'
            f'<div class="hero-badges"><span class="hero-badge">{escape(family["category"])}</span><span class="hero-badge">{len(items)} calculators</span><span class="hero-badge">Guides and quote prep included</span></div></section>'
            f'{render_ad_slot(f"{key}-hub-top")}'
            f'{render_quality_strip("project hub")}'
            f'{featured_section}'
            f'{calculator_section}'
            f'{render_section_cards(hub_content.get("notes", default_notes))}'
            f'{intent_section}'
            f'{guide_section}'
            f'{render_quote_prep_panel(family, "cluster")}'
            '</div>'
        )
        html = render_layout(
            title=f'{family["cluster_name"]} | {SITE["name"]}',
            description=f'Browse {family["cluster_name"].lower()} calculators, guides, and next-step planning content on {SITE["name"]}.',
            path=path,
            content=content,
            schema=[render_breadcrumb_schema(crumbs)],
            page_type="cluster",
        )
        pages.append((path, html))
    return pages


# ---------- Guides ----------

def _guide_mode(item: dict) -> str:
    text = f"{item['slug']} {item['title']} {item.get('headline', '')}".lower()
    if any(token in text for token in (' vs ', '-vs-', 'versus', 'compare')):
        return 'compare'
    if 'labour-vs-materials' in text:
        return 'labour-materials'
    if 'budget' in text:
        return 'budget'
    if 'cost-driver' in text or 'cost-drivers' in text:
        return 'cost-drivers'
    if 'cost-per' in text or 'per-m2' in text or 'per-m²' in text or 'costs' in text:
        return 'cost-per'
    if any(token in text for token in ('waste', 'coverage', 'overlap', 'yield', 'fit', 'depth')):
        return 'waste'
    if any(token in text for token in ('length', 'boxes', 'packs', 'rolls', 'how-much', 'calculator-by-area', 'calculator-by-volume')):
        return 'quantity'
    return 'general'


def _guide_description(item: dict, family: dict) -> str:
    description = item['description'].strip()
    if len(description) >= 95:
        return description
    endings = {
        'compare': f" Use it with the {family['name']} and the wider {family['cluster_name']} {PROJECT_HUB_LABEL.lower()} to compare routes on the same scope.",
        'labour-materials': f" Use it with the {family['name']} to separate labour pressure from materials before you compare quotes.",
        'budget': f" Use it with the {family['name']} to turn an early estimate into a more realistic planning budget.",
        'cost-drivers': f" Use it with the {family['name']} to isolate the assumptions most likely to move the final number.",
        'cost-per': f" Use it with the {family['name']} to turn headline rates into a more practical cost check.",
        'waste': f" Use it with the {family['name']} to sense-check waste, coverage, and buying-unit rounding before you order.",
        'quantity': f" Use it with the {family['name']} to turn a neat quantity into a safer buying decision.",
        'general': f" Use it with the {family['name']} and related guides to pressure-test the estimate before you buy or request quotes.",
    }
    return f"{description.rstrip('.')}" + endings[_guide_mode(item)]


def _guide_focus_cards(item: dict, family: dict) -> list[tuple[str, str]]:
    mode = _guide_mode(item)
    if mode == 'compare':
        return [
            ('When this guide helps', 'Compare two routes on the same measured job before price, convenience, or supplier preference blur the decision.'),
            ('Watch most', 'Coverage, waste, fixing extras, lifespan, and labour time often matter more than the first sticker price.'),
            ('Best next move', f"Run the {family['name']} first, then compare both options against the same scope and finish level."),
        ]
    if mode == 'labour-materials':
        return [
            ('When this guide helps', 'Split labour from materials so quote differences are easier to understand and challenge.'),
            ('Watch most', 'Prep, access, cutting, disposal, and finish complexity often shift labour faster than the material line.'),
            ('Best next move', 'Ask every installer to price the same inclusions, exclusions, and contingency assumptions.'),
        ]
    if mode == 'budget':
        return [
            ('When this guide helps', 'Turn a rough quantity into a more realistic planning budget before you request formal quotes.'),
            ('Watch most', 'Contingency, prep work, delivery, waste, and secondary materials usually explain why real totals exceed the first estimate.'),
            ('Best next move', 'Lock down the uncertain scope first, then compare budget, standard, and higher-spec routes.'),
        ]
    if mode in {'cost-drivers', 'cost-per'}:
        return [
            ('When this guide helps', 'Sense-check headline rates before treating them as a working budget or quote benchmark.'),
            ('Watch most', 'Scope gaps, access, finish level, labour pressure, and extras can move the total more than the visible headline rate.'),
            ('Best next move', 'Pressure-test the weak assumptions before comparing contractor or merchant prices.'),
        ]
    if mode == 'waste':
        return [
            ('When this guide helps', 'Use this when the order depends on waste, overlap, pack rounding, or awkward cuts rather than simple geometry alone.'),
            ('Watch most', 'Layout complexity, offcuts, breakage, and the real product coverage usually decide whether the order feels safe.'),
            ('Best next move', 'Confirm the supplier unit size and round against the buying format you can actually order.'),
        ]
    if mode == 'quantity':
        return [
            ('When this guide helps', 'Turn measured dimensions into a safer order quantity for packs, sheets, rolls, bags, or linear products.'),
            ('Watch most', 'Coverage assumptions, minimum order units, stock lengths, and handling loss usually move the final order.'),
            ('Best next move', 'Run the calculator, then round against live pack sizes and the awkward parts of the job.'),
        ]
    return [
        ('When this guide helps', family['support']['use_case']),
        ('Watch most', family['support']['mistakes']),
        ('Best next move', family['support'].get('estimate_tip', 'Measure carefully, sense-check the result, and compare buying routes before you commit.')),
    ]


def _guide_tradeoff_cards(item: dict, family: dict) -> list[tuple[str, str]]:
    mode = _guide_mode(item)
    if mode == 'compare':
        return [
            ('Cheaper now vs cheaper overall', 'A lower sticker price can still lose once waste, add-ons, labour time, lifespan, or replacement risk are considered.'),
            ('Convenience vs control', 'Pre-packed or faster-install options can reduce hassle, but they may also limit choice or change the total coverage cost.'),
            ('Simple answer vs better fit', 'The right route is usually the one that fits the real scope, not the one with the neatest headline number.'),
        ]
    if family.get('formula') == 'project_cost' or mode in {'budget', 'cost-drivers', 'cost-per', 'labour-materials'}:
        return [
            ('Lower budget vs safer budget', 'A lean early number can be useful, but a budget that ignores prep, access, extras, or contingency often fails once quotes arrive.'),
            ('Materials first vs labour first', 'Some jobs look material-heavy until cutting, prep, disposal, and finish detail push labour far higher than expected.'),
            ('Fast benchmark vs local reality', 'Headline rates are useful for orientation, but local labour pressure, site difficulty, and finish expectations still need checking.'),
        ]
    return [
        ('Lower waste vs easier install', 'The most efficient buying route is not always the easiest route to install or live with on site.'),
        ('Small overbuy vs shortfall risk', 'A modest spare allowance can be cheaper than a delayed job, second delivery, or hard-to-match top-up order.'),
        ('Clean maths vs supplier reality', 'Always compare the neat result against live pack sizes, stock lengths, and merchant terms before you treat it as final.'),
    ]


def _guide_example_cards(item: dict, family: dict) -> list[tuple[str, str]]:
    mode = _guide_mode(item)
    if family.get('formula') == 'project_cost':
        return [
            ('Scope driver', 'Area, spec, and whether the existing surface needs preparation often move the budget before finishing touches are considered.'),
            ('Site driver', 'Access, waste removal, delivery setup, and sequencing with other trades can change the real total quickly.'),
            ('Buying driver', 'A cleaner quote brief usually comes from checking materials, labour, and extras as separate lines first.'),
        ]
    if mode == 'compare':
        return [
            ('Material route', 'One route may look cheaper until waste, coverage, or extra accessories are priced on the same basis.'),
            ('Installation route', 'A faster or cleaner install route can offset a higher material cost when labour is tight.'),
            ('Replacement route', 'Think about rework, maintenance, and spare stock when the cheaper option may be harder to match later.'),
        ]
    if mode == 'waste':
        return [
            ('Simple layout', 'Rectangles and straightforward runs usually behave closest to the base waste assumption.'),
            ('Awkward layout', 'Niches, cuts, borders, curves, or lots of penetrations usually justify a higher allowance.'),
            ('Buying check', 'Use the live pack or roll size before finalising the order so the rounding matches supplier reality.'),
        ]
    if mode == 'quantity':
        return [
            ('Single room or run', 'Straightforward rooms or runs usually make the cleanest first-pass estimate.'),
            ('Linked extras', 'Adhesives, fixings, trims, and underlayers are often missed when people focus only on the headline unit count.'),
            ('Delivery check', 'Round with enough spare to avoid paying for a second delivery or stalling the job.'),
        ]
    return [
        ('Measurement check', 'Remeasure the parts of the job that feel least certain before you rely on the first estimate.'),
        ('Supplier check', 'Compare live pack sizes, product sheets, and merchant wording against the assumptions used here.'),
        ('Decision check', 'Treat the calculator and guide together as a planning baseline, not a substitute for a real quote.'),
    ]


def _guide_faqs(item: dict, family: dict) -> list[dict]:
    subject = item['title']
    mode = _guide_mode(item)
    if mode == 'compare':
        return [
            {'q': f'How should I compare options in {subject}?', 'a': f'Start with the same measured scope, waste allowance, and finish level, then compare materials, labour, and extras side by side using the {family["name"]}.'},
            {'q': f'What usually changes the result in {subject}?', 'a': 'Coverage, waste, accessory items, labour time, and replacement risk usually matter more than the headline sticker price alone.'},
            {'q': f'When should I stop comparing and ask for quotes?', 'a': 'Once the dimensions, finish route, and scope are stable, ask merchants or installers to price the same assumptions so the quote spread is easier to trust.'},
        ]
    if mode in {'budget', 'cost-drivers', 'cost-per', 'labour-materials'} or family.get('formula') == 'project_cost':
        return [
            {'q': f'How accurate is {subject}?', 'a': 'Treat it as a planning page, not a fixed quote. Scope, access, labour rate, finish level, and the included extras still need checking locally.'},
            {'q': f'What should I compare after using {subject}?', 'a': 'Compare materials, labour, prep, waste removal, delivery, and exclusions on the same scope before you decide which route is best value.'},
            {'q': 'Should I add contingency?', 'a': 'Yes. A realistic contingency is usually the difference between a useful planning budget and a number that falls apart once the site conditions are clearer.'},
        ]
    return [
        {'q': f'How should I use {subject}?', 'a': f'Use it with the {family["name"]} as a buying and planning sense-check, then confirm the final order against live supplier information and the site conditions.'},
        {'q': f'What usually changes the {subject} answer most?', 'a': 'Coverage or stock assumptions, waste, awkward cuts, and whole-unit rounding usually move the final order more than people expect.'},
        {'q': 'Should I round up the result?', 'a': 'Usually yes. A small spare allowance is often cheaper than a shortfall, a second delivery, or a delayed job.'},
    ]


def _guide_related_cards(family: dict, current_slug: str) -> str:
    related_items = [
        entry for entry in (family['intent_pages'] + family['guide_pages']) if entry['slug'] != current_slug
    ][:3]
    if not related_items:
        return ''
    cards = ''.join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(entry["slug"])}/">{escape(entry["title"])}</a></h3><p>{escape(entry["description"])}</p></article>'
        for entry in related_items
    )
    return (
        '<section class="content-card prose-card"><h2>Related decision pages</h2><p>Use these pages to pressure-test the next buying, waste, or cost question that usually follows the first estimate.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section>'
    )


def _guide_checklist_panel(item: dict, family: dict) -> str:
    mode = _guide_mode(item)
    if family.get('formula') == 'project_cost' or mode in {'budget', 'cost-drivers', 'cost-per', 'labour-materials'}:
        items = [
            'Write down what the price should include: materials, labour, prep, waste removal, delivery, and extras.',
            'Keep the same scope and exclusions across every quote or comparison route.',
            'Use the guide to challenge weak assumptions, not to replace a live site visit or trade quote.',
        ]
    else:
        items = [
            'Confirm the real product yield, pack size, stock length, or buying format before you order.',
            'Check whether waste, awkward cuts, and spare stock justify rounding up further.',
            f'Use the linked calculator and {PROJECT_HUB_LABEL.lower()} together if the decision affects more than one material or layer.',
        ]
    items_html = ''.join(f'<li>{escape(item)}</li>' for item in items)
    return (
        '<section class="conversion-panel">'
        '<div class="section-head"><h2>Practical checks before you buy or brief</h2><p>Use these prompts to move from a neat guide answer into a cleaner real-world decision.</p></div>'
        f'<ul class="conversion-list">{items_html}</ul>'
        '</section>'
    )


def build_guide_pages():
    pages = []
    for family in get_all_calculators():
        key = family['key']
        related = family['intent_pages'] + family['guide_pages']
        for item in related:
            path = f"/guides/{item['slug']}/"
            crumbs = [('Home', '/'), ('Guides', '/guides/'), (item['title'], path)]
            focus_cards = _guide_focus_cards(item, family)
            support_cards = [
                ('When this guide helps', family['support']['use_case']),
                ('Key assumption', family['support']['assumptions']),
                ('Common mistake to avoid', family['support']['mistakes']),
            ]
            tradeoff_cards = _guide_tradeoff_cards(item, family)
            example_cards = _guide_example_cards(item, family)
            faqs = _guide_faqs(item, family)
            related_cards = _guide_related_cards(family, item['slug'])
            description = _guide_description(item, family)

            focus_html = ''.join(
                f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
                for title, body in focus_cards
            )
            tradeoff_html = ''.join(
                f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
                for title, body in tradeoff_cards
            )
            example_html = ''.join(
                f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
                for title, body in example_cards
            )
            faq_html = ''.join(
                f'<article class="content-card prose-card"><h2>{escape(entry["q"])}</h2><p>{escape(entry["a"])}</p></article>'
                for entry in faqs
            )
            content = (
                f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
                f'<div class="eyebrow">{escape(family["cluster_name"])}</div><h1>{escape(item["headline"])}</h1>'
                f'<p class="hero-copy">{escape(item["intro"])}</p></section>'
                f'{render_ad_slot(f"{key}-guide-top")}'
                f'{render_quality_strip("guide")}'
                f'<section class="content-card prose-card"><h2>Quick answer</h2><p>{escape(description)}</p></section>'
                f'<section class="stack-grid">{focus_html}</section>'
                f'<section class="content-card prose-card"><h2>Use the calculator first</h2><p>The quickest path is to start with <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>, then use this guide to sense-check the result and decide what to buy or ask for next.</p></section>'
                f'{render_section_cards(support_cards)}'
                '<section class="content-card prose-card"><h2>Trade-offs to compare</h2><p>These are the practical choices that usually matter more than a neat headline answer.</p></section>'
                f'<section class="stack-grid">{tradeoff_html}</section>'
                '<section class="content-card prose-card"><h2>Worked examples and scenario checks</h2><p>Use these examples to see where the simple answer often needs a second look.</p></section>'
                f'<section class="stack-grid">{example_html}</section>'
                f'{_guide_checklist_panel(item, family)}'
                f'{related_cards}'
                f'<section class="content-card prose-card"><h2>Next step links</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} {escape(PROJECT_HUB_LABEL.lower())}</a> or go straight to the <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>.</p></section>'
                f'{render_quote_prep_panel(family, "guide")}'
                f'<section class="stack-grid">{faq_html}</section></div>'
            )
            html = render_layout(
                title=f"{item['title']} | {SITE['name']}",
                description=description,
                path=path,
                content=content,
                schema=[render_breadcrumb_schema(crumbs), render_faq_schema(faqs)],
                page_type='guide',
            )
            pages.append((path, html))
    return pages


# ---------- Conversion panels ----------

def render_quote_prep_panel(family: dict, context: str) -> str:
    calculator_path = f'/calculators/{family["slug"]}/'
    cluster_path = f'/clusters/{family["cluster_slug"]}/'
    label = {
        "calculator": "Use this estimate in a quote request",
        "guide": "Ready to turn this guide into a quote request?",
        "cluster": f"Use this {PROJECT_HUB_LABEL.lower()} to brief suppliers or installers",
    }.get(context, "Move from estimate to quote-ready scope")
    intro = {
        "calculator": "Copy the estimate, add your own notes, and send the same scope to each builder or supplier so the quotes are easier to compare.",
        "guide": "Once you understand the assumptions and buying choices, send builders or merchants the same measured scope so the prices are easier to compare fairly.",
        "cluster": "Work through the core calculator first, then use the linked guides and quote checklist to request cleaner, more comparable prices.",
    }.get(context, "Use the calculator and checklist together to request cleaner quotes.")
    actions = []
    if context != "calculator":
        actions.append(f'<a class="btn btn-primary" href="{escape(calculator_path)}" data-conversion-link="calculator">Open {escape(family["name"])}</a>')
    actions.append('<a class="btn" href="/quote-checklist/" data-conversion-link="quote-checklist">Open quote checklist</a>')
    actions.append('<a class="btn" href="/contact/" data-conversion-link="contact">Contact BuildCostLab</a>')
    return (
        '<section class="conversion-panel">'
        '<div class="section-head">'
        f'<h2>{escape(label)}</h2>'
        f'<p>{escape(intro)}</p>'
        '</div>'
        '<ul class="conversion-list">'
        '<li>Confirm what the quote should include: materials only, labour only, or both.</li>'
        '<li>State access, finish level, timing, and any unknowns clearly.</li>'
        '<li>Ask each supplier or installer to price the same scope and exclusions.</li>'
        '</ul>'
        f'<div class="conversion-actions">{"".join(actions)}</div>'
        f'<p class="conversion-note">You can also open the wider <a href="{escape(cluster_path)}">{escape(family["cluster_name"])}</a> {escape(PROJECT_HUB_LABEL.lower())} if the quote depends on more than one material.</p>'
        '</section>'
    )


def render_quote_brief_shell(family: dict) -> str:
    return (
        '<section id="quote-brief" class="quote-brief-shell content-card">'
        '<div class="section-head">'
        '<h2>Quote-ready brief</h2>'
        '<p>Use these actions to turn the live calculator result into a cleaner request for builders, suppliers, or merchants.</p>'
        '</div>'
        '<div class="quote-field-grid">'
        '<label><span>Project label</span><input id="quote-project-label" type="text" placeholder="Patio at rear garden, guest bedroom repaint, driveway refresh"></label>'
        '<label><span>Location or postcode area</span><input id="quote-location" type="text" placeholder="Leeds, LS12 or similar"></label>'
        '<label><span>Target timing</span><input id="quote-timing" type="text" placeholder="Next month, before summer, flexible"></label>'
        '<label><span>Email recipient (optional)</span><input id="quote-email" type="email" placeholder="builder@example.com"></label>'
        '<label class="quote-notes-field"><span>Notes or exclusions</span><textarea id="quote-notes" rows="4" placeholder="Access notes, product preference, labour/material split, exclusions, desired finish, or anything still uncertain."></textarea></label>'
        '</div>'
        '<div class="conversion-actions">'
        '<button class="btn btn-primary" type="button" data-estimate-action="copy">Copy quote brief</button>'
        '<button class="btn" type="button" data-estimate-action="email">Email quote brief</button>'
        '<button class="btn" type="button" data-estimate-action="txt">Download brief (.txt)</button>'
        '<button class="btn" type="button" data-estimate-action="csv">Download comparison sheet (.csv)</button>'
        '<button class="btn" type="button" data-estimate-action="print">Print / save PDF</button>'
        '</div>'
        '<p class="quote-status" id="quote-status">Run the calculator, then use these actions to prepare the estimate for a real quote request.</p>'
        f'<p class="conversion-note">Need help deciding what to ask for? Read the <a href="/quote-checklist/">quote checklist</a> or contact the team at <a href="mailto:{escape(SITE["contact_email"])}">{escape(SITE["contact_email"])}</a>.</p>'
        '</section>'
    )


# ---------- Calculator pages ----------

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
        next_step_section = f'<section class="related-tools" id="next-guides"><div class="section-head"><h2>Next-step guides</h2><p>Use these guides to sense-check the estimate, avoid common mistakes, and choose the right buying format.</p></div><div class="mini-tool-grid">{next_links}</div></section>'
    scope_cards = render_section_cards(_calculator_scope_cards(family))
    driver_cards = render_section_cards(_calculator_driver_cards(family))
    worked_example = f'<section class="content-card prose-card"><h2>Worked example</h2><p>{escape(_calculator_worked_example_text(family))}</p></section>'
    return (
        f'{render_ad_slot(f"{key}-mid")}'
        '<section id="buying-checks" class="content-card prose-card section-anchor-card"><h2>Practical checks before you buy</h2><p>These notes are where BuildCostLab goes beyond a generic calculator result by surfacing the assumptions, buying traps, and next decisions that usually move the real order.</p></section>'
        f'{scope_cards}'
        f'{worked_example}'
        f'{driver_cards}'
        f'{_calculator_checklist_panel(family)}'
        f'<section class="content-card prose-card"><h2>Explore this {escape(PROJECT_HUB_LABEL.lower())}</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} {escape(PROJECT_HUB_LABEL.lower())}</a> to move from quick estimate to deeper guidance.</p></section>'
        f'{next_step_section}'
        '<section id="faqs" class="content-card prose-card section-anchor-card"><h2>Quick answers</h2><p>These answers are designed to resolve the last practical buying questions people usually have after running the calculator.</p></section>'
        f'<section class="stack-grid">{faq_html}</section>'
    )


def render_calculator_page(*, slug: str, title: str, description: str, intro: str, form_html: str, result_html: str, script_name: str) -> str:
    family = family_lookup()[slug]
    normalized_description = description.strip()
    if len(normalized_description) < 90:
        normalized_description = f"{normalized_description.rstrip('.')} with practical quantity, waste, and rough cost outputs for planning."
    key = family["key"]
    path = f"/calculators/{slug}/"
    crumbs = [("Home", "/"), ("Calculators", "/calculators/"), (title, path)]
    summary_cards_html = ''.join(
        f'<article class="content-card quality-card"><div class="quality-kicker">Planning summary</div><h2>{escape(label)}</h2><p>{escape(body)}</p></article>'
        for label, body in _calculator_summary_cards(family)
    )
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        f'<div class="eyebrow">{escape(family["hero_eyebrow"])}</div><h1>{escape(title)}</h1>'
        f'<p class="hero-copy">{escape(intro)}</p>'
        '<div class="hero-badges"><span class="hero-badge">Estimate range</span><span class="hero-badge">Cost breakdown</span><span class="hero-badge">Compare options</span></div></section>'
        f'{render_ad_slot(f"{key}-top")}'
        f'{render_quality_strip("calculator")}'
        f'<section class="quality-strip" aria-label="Calculator summary">{summary_cards_html}</section>'
        f'{render_calculator_jump_nav()}'
        f'<section class="calculator-layout" id="calculator"><div class="content-card calculator-card">{form_html}</div><aside class="content-card result-card">{result_html}{render_cost_intelligence_shell()}</aside></section>'
        f'{render_quote_brief_shell(family)}'
        f'{build_calculator_support(slug)}'
        f'{render_quote_prep_panel(family, "calculator")}'
        '</div>'
        '<script src="/assets/js/global-calculator.js"></script>'
        '<script src="/assets/js/cost-intelligence.js"></script>'
        '<script src="/assets/js/quote-brief.js"></script>'
        f'<script src="/assets/js/{escape(script_name)}"></script>'
    )
    return render_layout(
        title=f"{title} | {SITE['name']}",
        description=normalized_description,
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs), render_faq_schema(family["faqs"]), render_software_application_schema(name=title, description=normalized_description, path=path, category="Estimator")],
        page_type="calculator",
    )


# ---------- Index pages ----------

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
        '<div class="eyebrow">Guide library</div><h1>Guides that make the estimate more usable</h1>'
        '<p class="hero-copy">These pages help you apply calculator results to real buying, comparison, and quote-prep decisions instead of stopping at the first number.</p></section>'
        f'{render_ad_slot("guides-index-top")}'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(cards)}</div></section></div>'
    )
    return path, render_layout(
        title=f'Guides | {SITE["name"]}',
        description="Browse BuildCostLab guides covering material quantities, waste allowances, buying checks, and rough cost decisions.",
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
    crumbs = [("Home", "/"), (PROJECT_HUBS_LABEL, path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        f'<div class="eyebrow">{escape(PROJECT_HUBS_LABEL)}</div><h1>{escape(PROJECT_HUBS_LABEL)} by project type</h1>'
        '<p class="hero-copy">Browse grouped calculators and guides for painting, concrete, roofing, landscaping, flooring, and other common building jobs.</p></section>'
        f'{render_ad_slot("clusters-index-top")}'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section></div>'
    )
    return path, render_layout(
        title=f'{PROJECT_HUBS_LABEL} | {SITE["name"]}',
        description="Browse BuildCostLab project hubs for calculators, guides, quote-prep steps, and next-step buying content.",
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="cluster-index",
    )


def _guide_records() -> list[dict]:
    records = []
    for family in get_all_calculators():
        for item in family["guide_pages"]:
            records.append({
                "family": family,
                "slug": item["slug"],
                "title": item["title"],
                "description": item["description"],
            })
    return records


def build_compare_index() -> tuple[str, str]:
    compare_keywords = (" vs ", "-vs-", "versus", "cost per", "per m²", "per m2", "costs")
    records = [
        item for item in _guide_records()
        if any(keyword in (item["title"] + " " + item["slug"]).lower() for keyword in compare_keywords)
    ]
    cards = "".join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p><a class="text-link" href="/clusters/{escape(item["family"]["cluster_slug"])}/">Open project hub</a></article>'
        for item in records
    )
    path = "/compare/"
    crumbs = [("Home", "/"), ("Compare", path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Comparison hub</div><h1>Comparison and cost-benchmark guides</h1>'
        '<p class="hero-copy">Use these pages when you need to compare material routes, pressure-test a per-m² rate, or make sure two buying options are being judged on the same assumptions.</p></section>'
        f'{render_ad_slot("compare-index-top")}'
        '<section class="content-card prose-card"><h2>How to use this section</h2><p>Start with the calculator if you need a fresh quantity first, then use these comparison pages to sense-check costs, buying formats, and option trade-offs before you request quotes.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section></div>'
    )
    return path, render_layout(
        title=f'Compare Materials and Costs | {SITE["name"]}',
        description='Browse BuildCostLab comparison guides for per-m² rates, material trade-offs, and cost benchmarks.',
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="compare-index",
    )


def build_buying_guides_index() -> tuple[str, str]:
    records = _guide_records()
    cards = "".join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p><a class="text-link" href="/calculators/{escape(item["family"]["slug"])}/">Open calculator</a></article>'
        for item in records
    )
    path = "/buying-guides/"
    crumbs = [("Home", "/"), ("Buying Guides", path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Buying guide hub</div><h1>Buying, waste, and pack-size guides</h1>'
        '<p class="hero-copy">These guides help you move from a raw quantity into a safer buying decision by checking waste, pack coverage, buying format, and the practical choices that affect real orders.</p></section>'
        f'{render_ad_slot("buying-guides-index-top")}'
        '<section class="content-card prose-card"><h2>How to use this section</h2><p>Open the main calculator first if you still need a quantity, then use these guides to check coverage, pack sizes, waste, and the buying route that best matches the job.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section></div>'
    )
    return path, render_layout(
        title=f'Buying Guides | {SITE["name"]}',
        description='Browse BuildCostLab buying guides covering waste, pack sizes, material comparisons, and ordering decisions.',
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="buying-guide-index",
    )
