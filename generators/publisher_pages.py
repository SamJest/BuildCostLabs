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
from data.publisher import SITE, TRUST_PAGES


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
    for item in get_all_calculator_entries():
        clusters.setdefault(item["cluster_slug"], []).append(item)
    for cluster_slug, items in clusters.items():
        family = items[0]
        hub_content = get_cluster_hub_content(cluster_slug)
        key = family["key"]
        path = f'/clusters/{cluster_slug}/'
        crumbs = [("Home", "/"), ("Tool Sets", "/clusters/"), (family["cluster_name"], path)]
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
                '<section class="content-card prose-card"><h2>More tools in this set</h2>'
                '<p>These related tools help when the job involves extra materials, linked quantities, or a different buying format.</p></section>'
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
                f'<p>{escape(hub_content.get("guide_intro", "These guides help explain waste, product choice, and buying format once the first quantity estimate is clear."))}</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{guide_links}</div></section>'
            )
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">Tool set</div><h1>{escape(family["cluster_name"])}</h1>'
            f'<p class="hero-copy">{escape(get_cluster_intro(cluster_slug, family["intro"]))}</p>'
            f'<div class="hero-badges"><span class="hero-badge">{escape(family["category"])}</span><span class="hero-badge">{len(items)} calculators</span><span class="hero-badge">Related guides included</span></div></section>'
            f'{render_ad_slot(f"{key}-hub-top")}'
            f'{featured_section}'
            f'{calculator_section}'
            f'{render_section_cards(hub_content.get("notes", [("How to use this tool set", "Start with the calculator that matches the material or buying format you actually need, then move into the related guides if you need more detail before buying."), ("What affects estimates most", "Dimensions, depth or coverage assumptions, waste allowance, and pack or stock-length rounding are usually the biggest drivers of the final buying number."), ("Why these guides are useful", "The extra guides in each tool set help explain common mistakes, waste allowances, and buying choices that a simple quantity figure cannot cover on its own.")]))}'
            f'{intent_section}'
            f'{guide_section}'
            f'{render_quote_prep_panel(family, "cluster")}</div>'
        )
        html = render_layout(
            title=f'{family["cluster_name"]} | {SITE["name"]}',
            description=f'Browse {family["cluster_name"].lower()} calculators, supporting guides, and next-step buying content on {SITE["name"]}.',
            path=path,
            content=content,
            schema=[render_breadcrumb_schema(crumbs)],
            page_type="cluster",
        )
        pages.append((path, html))
    return pages


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
        'compare': f" Use it with the {family['name']} and the wider {family['cluster_name']} tool set to compare routes on the same scope.",
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
            ('Best use', 'Compare two routes on the same measured job before price, convenience, or supplier preference start to blur the decision.'),
            ('Watch most', 'Coverage, waste, fixing extras, lifespan, and labour time often matter more than the first sticker price.'),
            ('Best next move', f"Run the {family['name']} first, then compare both options against the same scope and finish level."),
        ]
    if mode == 'labour-materials':
        return [
            ('Best use', 'Split labour from materials so quote differences are easier to understand and challenge.'),
            ('Watch most', 'Prep, access, cutting, disposal, and finish complexity often shift labour faster than the material line.'),
            ('Best next move', 'Ask every installer to price the same inclusions, exclusions, and contingency assumptions.'),
        ]
    if mode == 'budget':
        return [
            ('Best use', 'Turn a rough quantity into a more realistic planning budget before you request formal quotes.'),
            ('Watch most', 'Contingency, prep work, delivery, waste, and secondary materials usually explain why real totals exceed the first estimate.'),
            ('Best next move', 'Lock down the uncertain scope first, then compare budget, standard, and higher-spec routes.'),
        ]
    if mode in {'cost-drivers', 'cost-per'}:
        return [
            ('Best use', 'Sense-check headline rates before treating them as a working budget or quote benchmark.'),
            ('Watch most', 'Scope gaps, access, finish level, labour pressure, and extras can move the total more than the visible headline rate.'),
            ('Best next move', 'Pressure-test the weak assumptions before comparing contractor or merchant prices.'),
        ]
    if mode == 'waste':
        return [
            ('Best use', 'Use this when the order depends on waste, overlap, pack rounding, or awkward cuts rather than simple geometry alone.'),
            ('Watch most', 'Layout complexity, offcuts, breakage, and the real product coverage usually decide whether the order feels safe.'),
            ('Best next move', 'Confirm the supplier unit size and round against the buying format you can actually order.'),
        ]
    if mode == 'quantity':
        return [
            ('Best use', 'Turn measured dimensions into a safer order quantity for packs, sheets, rolls, bags, or linear products.'),
            ('Watch most', 'Coverage assumptions, minimum order units, stock lengths, and handling loss usually move the final order.'),
            ('Best next move', 'Run the calculator, then round against live pack sizes and the awkward parts of the job.'),
        ]
    return [
        ('Best use', family['support']['use_case']),
        ('Watch most', family['support']['mistakes']),
        ('Best next move', family['support'].get('estimate_tip', 'Measure carefully, sense-check the result, and compare buying routes before you commit.')),
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
            ('Single room', 'Straightforward rooms or runs usually make the cleanest first-pass estimate.'),
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
            {'q': f'What should I compare after using {subject}?', 'a': f'Compare materials, labour, prep, waste removal, delivery, and exclusions on the same scope before you decide which route is best value.'},
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
        f'<article class="tool-card"><h3><a href="/guides/{escape(entry["slug"] )}/">{escape(entry["title"])}</a></h3><p>{escape(entry["description"])}</p></article>'
        for entry in related_items
    )
    return (
        '<section class="content-card prose-card"><h2>Related decision pages</h2><p>Use these pages to pressure-test the next buying, waste, or cost question that usually follows the first estimate.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section>'
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
                ('Why this page exists', family['support']['use_case']),
                ('Core assumption', family['support']['assumptions']),
                ('Common mistake', family['support']['mistakes']),
            ]
            example_cards = _guide_example_cards(item, family)
            faqs = _guide_faqs(item, family)
            related_cards = _guide_related_cards(family, item['slug'])
            description = _guide_description(item, family)
            focus_html = ''.join(
                f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
                for title, body in focus_cards
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
                f'<section class="content-card prose-card"><h2>Use the calculator first</h2><p>The quickest path is to start with <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>, then use this guide to sense-check the result and decide what to buy next.</p></section>'
                f'{render_section_cards(support_cards)}'
                f'<section class="content-card prose-card"><h2>Practical checks before you buy or brief</h2><p>Use these prompts to move from a neat estimate into a more realistic buying, budgeting, or quote-comparison decision.</p></section>'
                f'<section class="stack-grid">{example_html}</section>'
                f'{related_cards}'
                f'<section class="content-card prose-card"><h2>Next step links</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} tool set</a> or go straight to the <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>.</p></section>'
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

def render_quote_prep_panel(family: dict, context: str) -> str:
    calculator_path = f'/calculators/{family["slug"]}/'
    cluster_path = f'/clusters/{family["cluster_slug"]}/'
    label = {
        "calculator": "Use this estimate in a quote request",
        "guide": "Ready to turn this guide into a quote request?",
        "cluster": "Use this tool set to brief suppliers or installers",
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
        f'<p class="conversion-note">You can also open the wider <a href="{escape(cluster_path)}">{escape(family["cluster_name"])}</a> tool set if the quote depends on more than one material.</p>'
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


def render_quality_strip(page_type: str) -> str:
    return (
        '<section class="quality-strip" aria-label="Freshness and methodology">'
        f'<article class="content-card quality-card"><div class="quality-kicker">Last checked</div><h2>{escape(SITE["updated_label"])}</h2><p>We checked the calculator logic, page notes, and related links on this page.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">How to use it</div><h2>Use it to plan the job</h2><p>Use this {escape(page_type)} for an early buying and budget check, then confirm the final order against product data and site conditions.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Why trust it</div><h2>See how the site is maintained</h2><p>Read the <a href="{escape(SITE["methodology_path"])}">calculator methodology</a> and <a href="{escape(SITE["editorial_policy_path"])}">editorial policy</a> for the standards behind these pages.</p></article>'
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
        next_step_section = f'<section class="related-tools" id="next-guides"><div class="section-head"><h2>Next-step guides</h2><p>Use these guides to sense-check the estimate, avoid common mistakes, and choose the right buying format.</p></div><div class="mini-tool-grid">{next_links}</div></section>'
    support_cards = render_section_cards([("Assumptions", family["support"]["assumptions"]), ("Common mistakes", family["support"]["mistakes"]), ("Best use cases", family["support"]["use_case"]), ("How to get a better estimate", family["support"].get("estimate_tip", "Measure carefully, apply realistic waste, and sense-check the result against how the product is actually sold.")), ("Before you buy", family["support"].get("buyer_tip", "Round to whole buying units and compare product coverage before buying solely on sticker price.")), ("UK and US note", family["support"].get("market_note", "Unit wording and supplier pack conventions differ between markets, but the estimating logic still starts with geometry, waste, and whole-unit ordering.")), ("Final buying check", family["support"].get("final_check", "Before placing an order, compare product coverage, pack size, delivery cost, and whether buying one extra unit is safer than risking a shortfall."))])
    return (
        f'{render_ad_slot(f"{key}-mid")}'
        '<section id="buying-checks" class="content-card prose-card section-anchor-card"><h2>Practical checks before you buy</h2><p>These notes are where BuildCostLab goes beyond a generic calculator result by surfacing the assumptions, buying traps, and next decisions that usually move the real order.</p></section>'
        f'{support_cards}'
        f'<section class="content-card prose-card"><h2>Explore this tool set</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} tool set</a> to move from quick estimate to deeper guidance.</p></section>'
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
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        f'<div class="eyebrow">{escape(family["hero_eyebrow"])}</div><h1>{escape(title)}</h1>'
        f'<p class="hero-copy">{escape(intro)}</p>'
        '<div class="hero-badges"><span class="hero-badge">Estimate range</span><span class="hero-badge">Cost breakdown</span><span class="hero-badge">Compare options</span></div></section>'
        f'{render_ad_slot(f"{key}-top")}'
        f'{render_quality_strip("calculator")}'
        f'{render_calculator_jump_nav()}'
        f'<section class="calculator-layout" id="calculator"><div class="content-card calculator-card">{form_html}</div><aside class="content-card result-card">{result_html}{render_cost_intelligence_shell()}</aside></section>'
        f'{render_quote_brief_shell(family)}'
        f'{build_calculator_support(slug)}'
        f'{render_quote_prep_panel(family, "calculator")}</div><script src="/assets/js/global-calculator.js"></script><script src="/assets/js/cost-intelligence.js"></script><script src="/assets/js/quote-brief.js"></script><script src="/assets/js/{escape(script_name)}"></script>'
    )
    return render_layout(
        title=f"{title} | {SITE['name']}",
        description=normalized_description,
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs), render_faq_schema(family["faqs"]), render_software_application_schema(name=title, description=normalized_description, path=path, category="Estimator")],
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
        '<p class="hero-copy">These pages are written to support real estimating and buying decisions, then route users back into the right calculator or tool set.</p></section>'
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
    crumbs = [("Home", "/"), ("Tool Sets", path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Project tool sets</div><h1>Tool sets by project type</h1>'
        '<p class="hero-copy">Browse grouped calculators and guides for painting, concrete, roofing, landscaping, flooring, and other common building jobs.</p></section>'
        f'{render_ad_slot("clusters-index-top")}'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section></div>'
    )
    return path, render_layout(
        title=f'Tool Sets | {SITE["name"]}',
        description="Browse BuildCostLab tool sets for calculators, guides, quote-prep steps, and next-step buying content.",
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
        f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p><a class="text-link" href="/clusters/{escape(item["family"]["cluster_slug"])}/">Open tool set</a></article>'
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
