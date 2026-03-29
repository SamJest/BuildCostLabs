from html import escape

from components.publishing import (
    family_lookup,
    render_ad_slot,
    render_breadcrumb_schema,
    render_breadcrumbs,
    render_faq_schema,
    render_item_list_schema,
    render_layout,
    render_section_cards,
)
from data.catalog import get_all_calculators, get_cluster_hub_content, get_cluster_intro
from data.publisher import SITE, TRUST_PAGES
from data.uk_regions import FEATURED_REGION_SLUGS, UK_REGION_PROFILES


def render_authority_panel(page_type: str) -> str:
    label = "calculator" if page_type == "calculator" else page_type
    return (
        '<section class="authority-panel content-card" aria-label="Authority and estimate notes">'
        '<div class="section-head"><h2>Planning estimate notes</h2><p>Use the page for early budgeting and ordering checks, then confirm the final decision against live product information and site conditions.</p></div>'
        '<div class="authority-grid">'
        f'<article class="authority-card"><div class="quality-kicker">Reviewed by</div><h3>{escape(SITE["review_team"])}</h3><p>{escape(SITE["coverage_note"])}</p></article>'
        f'<article class="authority-card"><div class="quality-kicker">Last checked</div><h3>{escape(SITE["updated_label"])}</h3><p>We revisited the formula logic, support guidance, and internal routing for this {escape(label)}.</p></article>'
        f'<article class="authority-card"><div class="quality-kicker">Best for</div><h3>Early planning</h3><p>This page is strongest when you want a fast rough estimate before requesting quotes or placing an order.</p></article>'
        '</div></section>'
    )


def render_methodology_steps(family: dict) -> str:
    steps = [
        ("Measure the job", family["support"].get("measure_step", "Start with the real dimensions, count, depth, or coverage area that drives the job.")),
        ("Apply practical estimating logic", family["support"].get("assumptions", "The page uses estimating assumptions that are intended to be closer to a buying decision than a bare formula.")),
        ("Add waste and buying reality", family["support"].get("mistakes", "The result should be checked against waste, cuts, overlaps, pack sizes, and the way the product is actually sold.")),
        ("Sense-check the order", family["support"].get("final_check", "Before buying, compare the result with product coverage, supplier constraints, delivery minimums, and whether one extra unit is safer than running short.")),
    ]
    items = ''.join(
        f'<article class="method-step"><div class="method-step-number">{index + 1}</div><div><h3>{escape(title)}</h3><p>{escape(body)}</p></div></article>'
        for index, (title, body) in enumerate(steps)
    )
    return f'<section class="content-card methodology-card"><div class="section-head"><h2>How we estimate this</h2><p>These pages combine basic geometry with more practical buying assumptions so the result is more useful for real jobs.</p></div><div class="methodology-steps">{items}</div></section>'


def render_estimate_limits(family: dict) -> str:
    cards = [
        ("Estimate strength", family["support"].get("use_case", "Best for first-pass planning, quick material checks, and comparing likely buying routes.")),
        ("What can change the total", family["support"].get("estimate_tip", "Dimensions, waste, coverage assumptions, site access, and product choice usually move the total the most.")),
        ("When to remeasure", family["support"].get("remeasure_tip", "Remeasure when the layout is irregular, the substrate is poor, or the supplier pack size does not match the default assumptions.")),
    ]
    return '<section class="stack-grid">' + ''.join(
        f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
        for title, body in cards
    ) + '</section>'


def render_assumption_checklist(family: dict) -> str:
    items = [
        family["support"].get("assumptions", "Check the core estimating assumption before you order."),
        family["support"].get("buyer_tip", "Compare pack sizes, coverage, and waste before choosing the cheapest-looking product."),
        family["support"].get("market_note", "Supplier wording, pack sizes, and sales units can vary by market and merchant."),
        family["support"].get("final_check", "Make one final sense-check before the order is placed."),
    ]
    li = ''.join(f'<li>{escape(item)}</li>' for item in items)
    return f'<section class="content-card prose-card"><h2>Before you rely on this estimate</h2><ul class="checklist">{li}</ul></section>'




def classify_guide(item: dict) -> str:
    title = item["title"].lower()
    slug = item["slug"]
    if "labour-vs-materials" in slug:
        return "labour_split"
    if " vs " in title or "-vs-" in slug or "bags-vs-bulk" in slug:
        return "comparison"
    if "cost per" in title or "cost-per" in slug:
        return "cost_per"
    if "budget planning" in title or "budget" in slug:
        return "budget"
    if "cost drivers" in title or "cost-drivers" in slug:
        return "drivers"
    return "general"


def build_item_list_entries(items: list[dict], prefix: str, name_key: str = "title") -> list[dict]:
    return [{"name": item[name_key], "url": f"{prefix}{item['slug']}/"} for item in items]


def gather_all_guides() -> list[tuple[dict, dict]]:
    pairs = []
    for family in get_all_calculators():
        for item in family["intent_pages"] + family["guide_pages"]:
            pairs.append((family, item))
    return pairs


def parse_comparison_labels(item: dict, guide_type: str) -> tuple[str, str]:
    title = item["title"]
    cleaned = title
    for suffix in (" Guide", " Costs", " Cost Guide", " Buying Guide", " Budget Planning Guide", " Cost Drivers Guide", " Cost per m2 Guide"):
        if cleaned.endswith(suffix):
            cleaned = cleaned[: -len(suffix)]
    if guide_type == "labour_split":
        return ("Labour pressure", "Material pressure")
    if guide_type == "cost_per":
        return ("Headline price", "Real cost per covered area")
    if guide_type == "budget":
        return ("Visible finish", "Full working budget")
    if guide_type == "drivers":
        return ("Stable inputs", "Budget movers")
    if " vs " in cleaned:
        left, right = cleaned.split(" vs ", 1)
        return left.strip(), right.strip()
    if "Bags vs Bulk" in cleaned:
        return ("Bags", "Bulk")
    return ("Option A", "Option B")


def render_comparison_matrix(family: dict, item: dict) -> str:
    guide_type = classify_guide(item)
    if guide_type == "general":
        return ""
    left, right = parse_comparison_labels(item, guide_type)
    next_target = f'/calculators/{family["slug"]}/'
    next_copy = f'Run the {family["name"]} to pressure-test the route that looks strongest once you have real dimensions or quantities.'
    if infer_family_formula(family) == "project_cost":
        next_copy = f'Use the {family["name"]} to test finish level, labour, extras, and contingency after you compare the routes on this page.'
    body_map = {
        "comparison": [
            (f"Choose {left} when", f"It matches the job shape, waste pattern, and supporting-material logic better than the alternative. {family['support'].get('buyer_tip', '')}"),
            (f"Choose {right} when", f"It reduces labour, ordering friction, or long-term compromise enough to justify the higher-looking line item or different buying format."),
            ("What swings the result", "Coverage, accessory materials, waste, and labour can change the winning option faster than the visible sticker price."),
            ("Best next move", next_copy),
        ],
        "labour_split": [
            (left, "Labour climbs when prep, access, awkward cuts, or slower install methods are doing most of the work."),
            (right, "Material pressure dominates when the finish itself is expensive, coverage is poor, or the supporting products are costly."),
            ("What to isolate", "Keep labour, materials, extras, and contingency separate so one moving part does not hide another."),
            ("Best next move", next_copy),
        ],
        "cost_per": [
            (left, "Headline pack, bag, or box prices only help when the coverage assumptions are genuinely equivalent."),
            (right, "Compare on covered area after waste and supporting products so the cheaper-looking sticker price does not mislead you."),
            ("What people miss", "Waste, overlaps, pack rounding, and accessory products often destroy a simple price-per-unit comparison."),
            ("Best next move", next_copy),
        ],
        "budget": [
            (left, "The visible finish is only one layer of the number. It is useful, but not enough for a usable plan."),
            (right, "A working budget keeps materials, labour, extras, access, and contingency visible so the total can be stress-tested."),
            ("What usually gets missed", family['support'].get('mistakes', 'Prep work, accessories, and contingency are commonly left until too late.')),
            ("Best next move", next_copy),
        ],
        "drivers": [
            (left, "Hold the stable assumptions in one group so you can see which parts of the estimate are not changing much."),
            (right, "Focus on the inputs that move fastest: labour rate, access, finish spec, waste, groundwork, and supporting items."),
            ("What to test first", family['support'].get('estimate_tip', 'Test the assumption that feels least certain before asking for quotes.')),
            ("Best next move", next_copy),
        ],
    }
    cards = ''.join(
        f'<article class="content-card prose-card compare-insight-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
        for title, body in body_map.get(guide_type, body_map["comparison"])
    )
    heading_map = {
        "comparison": f"{left} vs {right}: the practical trade-offs",
        "labour_split": "Split labour from materials before you trust the budget",
        "cost_per": "Compare the rate, not just the price tag",
        "budget": "Turn a rough number into a working budget",
        "drivers": "Focus on what actually moves the total",
    }
    intro_map = {
        "comparison": "The cheapest-looking route is not always the best value once waste, supporting products, labour, and delivery are included.",
        "labour_split": "A clearer budget starts when labour and material pressure stop being mixed into one vague number.",
        "cost_per": "Normalise the comparison first so one expensive-looking unit does not hide better real coverage.",
        "budget": "Make the money usable by keeping the layers of the budget separate and visible.",
        "drivers": "Use the page to find the unstable assumptions before they become expensive surprises.",
    }
    return (
        f'<section class="content-card prose-card compare-insight-panel"><h2>{escape(heading_map.get(guide_type, heading_map["comparison"]))}</h2><p>{escape(intro_map.get(guide_type, intro_map["comparison"]))}</p></section>'
        f'<section class="stack-grid compare-insight-grid">{cards}</section>'
    )


def infer_family_formula(family: dict) -> str:
    if family.get("formula"):
        return family["formula"]
    slug = family.get("slug", "")
    cluster = family.get("cluster_slug", "")
    if cluster == "project-cost-estimating" or "-cost-calculator" in slug:
        return "project_cost"
    if any(token in slug for token in ("concrete", "gravel", "topsoil", "mulch", "compost", "bark", "sand", "mortar", "screed", "plaster", "render", "sub-base", "subbase", "mot-type-1")):
        return "volume"
    if any(token in slug for token in ("fence", "pipe", "gutter", "fascia", "architrave", "skirting", "sleepers", "cladding", "bead", "batten")):
        return "linear"
    return "coverage"


def render_guide_summary_strip(family: dict, item: dict) -> str:
    guide_type = classify_guide(item)
    summary_map = {
        "comparison": [("Decision type", "Compare the job fit first"), ("Watch most", "Coverage, extras, and labour"), ("Best next move", "Run the linked calculator")],
        "labour_split": [("Decision type", "Split labour from materials"), ("Watch most", "Access, prep, and finish level"), ("Best next move", "Test a mid-range budget")],
        "cost_per": [("Decision type", "Compare on covered area"), ("Watch most", "Waste and pack coverage"), ("Best next move", "Use price per m², not sticker price")],
        "budget": [("Decision type", "Build a layered budget"), ("Watch most", "Contingency and supporting materials"), ("Best next move", "Turn the total into a quote brief")],
        "drivers": [("Decision type", "Find the biggest cost levers"), ("Watch most", "Area, access, and finish spec"), ("Best next move", "Lock down the uncertain inputs")],
        "general": [("Decision type", "Use this as a sense-check"), ("Watch most", "Waste and buying units"), ("Best next move", "Jump back into the live calculator")],
    }
    cards = ''.join(
        f'<article class="content-card quality-card"><div class="quality-kicker">{escape(label)}</div><h2>{escape(value)}</h2><p>{escape(family["support"].get("use_case", "Use this page to support a real buying decision."))}</p></article>'
        for label, value in summary_map.get(guide_type, summary_map["general"])
    )
    return f'<section class="quality-strip guide-summary-strip">{cards}</section>'


def render_region_cost_overview(family: dict) -> str:
    if infer_family_formula(family) != "project_cost":
        return ""
    selected = [profile for profile in UK_REGION_PROFILES if profile["slug"] in FEATURED_REGION_SLUGS]
    cards = ''.join(
        f'<article class="authority-card"><div class="quality-kicker">{escape(profile["label"])}</div><h3>{escape(profile["summary"])}</h3><p>{escape(profile["note"])}</p></article>'
        for profile in selected
    )
    return (
        '<section class="content-card prose-card"><h2>Regional cost pressure</h2><p>Use the UK region selector as a planning weight for labour, access, and extras. It is useful for early budgeting, but it is still not a trade quote.</p></section>'
        f'<section class="authority-grid region-cost-grid">{cards}</section>'
    )


def render_guide_examples(family: dict) -> str:
    examples_map = {
        "coverage": [("Single room", "Use the room dimensions, coats, and a realistic waste margin to avoid under-ordering on straightforward layouts."), ("Awkward cuts", "Add a little more when the layout includes niches, trims, or many offcuts that reduce effective coverage."), ("Buying check", "Round against the actual board, box, tin, or roll size rather than relying on the raw calculator figure.")],
        "volume": [("Shallow layer", "Decorative and bedding layers usually move most when the installed depth drifts above the original plan."), ("Structural pour", "Concrete and dense fill jobs become expensive quickly when depth or trench width changes on site."), ("Delivery route", "Use the result to compare bagged and bulk buying only after access and unloading are clear.")],
        "linear": [("Straight run", "Simple runs are easiest to price when the stock length and join pattern are known up front."), ("Corners and returns", "Linear products often need more spare once corners, mitres, posts, or end details appear."), ("Site handling", "Long lengths can create extra waste if storage, transport, or handling on site is awkward.")],
        "project_cost": [("Budget route", "Use the lower range only when site prep is simple, access is clean, and finish expectations are basic."), ("Typical route", "Most jobs land in the middle once normal labour, materials, and a realistic contingency are included."), ("Higher-spec route", "Premium finishes, harder access, or more detailed prep can push the same footprint into a much higher total.")],
    }
    cards = ''.join(
        f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
        for title, body in examples_map.get(infer_family_formula(family), examples_map["coverage"])
    )
    return f'<section class="stack-grid guide-example-grid">{cards}</section>'


def render_guide_decision_cards(family: dict, item: dict) -> str:
    guide_type = classify_guide(item)
    card_map = {
        "comparison": [("Usually cheaper when", "The layout is simple, waste is low, and the lower-spec option still fits the job without extra supporting products."), ("Worth paying more when", "The upgraded option removes labour, lasts longer, or cuts the risk of ordering the wrong supporting materials."), ("Do not compare blindly", "Two products can look close on price while creating very different waste, fitting, and labour patterns.")],
        "labour_split": [("Materials-heavy jobs", "Simple installs with expensive surface materials usually swing more with product choice than labour."), ("Labour-heavy jobs", "Prep, access, detailing, and awkward geometry often matter more than the headline material cost."), ("Quote prep", "Split the estimate into labour, materials, and extras before comparing contractors or merchants.")],
        "cost_per": [("Like-for-like basis", "Compare by covered area, thickness, or usable yield rather than by pack or bag price on its own."), ("Include add-ons", "Adhesive, underlay, fixings, edging, and waste can completely change which option is actually cheaper."), ("Use range thinking", "A low cost per m² can still become a poor buy once breakage, cuts, and supporting products are counted.")],
        "budget": [("Build in layers", "Keep the main material, labour, supporting items, and contingency separate so the estimate stays readable."), ("Protect the budget", "The fastest way to blow the number is to ignore groundwork, prep, or accessory materials until late."), ("Best next action", "Use the linked calculator pages to test the parts of the budget that feel weakest before asking for quotes.")],
        "drivers": [("Primary drivers", "Area, finish level, access, and labour rate usually move the result first."), ("Secondary drivers", "Waste, pack rounding, disposal, and small extras often matter after the main scope is fixed."), ("What to lock down", "Measure the uncertain dimensions and assumptions first so the estimate range narrows faster.")],
        "general": [("Quick answer", "Use this guide to understand the calculator output, not to replace a live estimate."), ("What to check", "Confirm the real product coverage, depth, or stock length before the order feels locked in."), ("What next", "Jump to the tool set or budget calculator if the job needs a broader answer than a raw quantity.")],
    }
    cards = ''.join(
        f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
        for title, body in card_map.get(guide_type, card_map["general"])
    )
    heading_map = {
        "comparison": "How to compare the options properly",
        "labour_split": "What the split usually looks like",
        "cost_per": "How to compare the rate properly",
        "budget": "How to make the budget more usable",
        "drivers": "Where the estimate usually moves most",
        "general": "Use this guide to make the estimate better",
    }
    return f'<section class="content-card prose-card guide-decision-panel"><h2>{escape(heading_map.get(guide_type, heading_map["general"]))}</h2><p>Use these checks to move from a rough answer into a cleaner buying or budgeting decision.</p></section><section class="stack-grid guide-decision-grid">{cards}</section>'


def render_related_guide_cards(family: dict, current_slug: str) -> str:
    related = [item for item in family["intent_pages"] + family["guide_pages"] if item["slug"] != current_slug]
    related.sort(key=lambda entry: (classify_guide(entry) == "general", entry["title"]))
    selected = related[:4]
    if not selected:
        return ""
    return render_conversion_cards(
        [{"eyebrow": classify_guide(entry).replace('_', ' '), "title": entry["title"], "href": f'/guides/{entry["slug"]}/', "text": entry["description"]} for entry in selected],
        heading="Related decision pages",
        intro="These pages cover the next comparison, cost, or buying angle people usually check after the first estimate.",
        variant="guide-related",
    )


def render_cluster_decision_section(intent_pages: list[dict], guide_pages: list[dict]) -> str:
    decision_items = [item for item in intent_pages + guide_pages if classify_guide(item) != "general"]
    if not decision_items:
        return ""
    cards = ''.join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p></article>'
        for item in decision_items[:6]
    )
    return ('<section class="content-card prose-card"><h2>Comparison and budget pages</h2>'
            '<p>Use these pages when the job has moved beyond a raw quantity and you need a clearer choice between buying routes, cost rates, or budget structure.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section>')


def get_project_cost_calculators() -> list[dict]:
    return [item for item in get_all_calculators() if item.get("formula") == "project_cost"]


def find_budget_calculator(family: dict) -> dict | None:
    slug = family["slug"]
    keyword_map = [
        (("paint", "primer", "wallpaper", "filler"), "room-painting-cost-calculator"),
        (("driveway", "pea-gravel", "french-drain"), "driveway-cost-calculator"),
        (("gravel", "sub-base", "mot-type-1", "hardcore"), "driveway-cost-calculator"),
        (("paving", "patio", "sand", "jointing", "edging", "kerb", "weed-membrane"), "patio-cost-calculator"),
        (("deck", "sleepers", "wood-stain"), "decking-cost-calculator"),
        (("fence", "post", "gravel-board"), "fence-cost-calculator"),
        (("plaster", "render", "plasterboard", "drywall", "joint-compound", "bead"), "plastering-cost-calculator"),
    ]
    target_slug = None
    for keywords, candidate in keyword_map:
        if any(keyword in slug for keyword in keywords):
            target_slug = candidate
            break
    if not target_slug:
        return None
    for item in get_project_cost_calculators():
        if item["slug"] == target_slug:
            return item
    return None


def render_conversion_cards(cards: list[dict], *, heading: str, intro: str, variant: str = "conversion") -> str:
    if not cards:
        return ""
    items = "".join(
        f'<article class="content-card conversion-card"><div class="quality-kicker">{escape(card.get("eyebrow", "Next step"))}</div><h3><a href="{escape(card["href"])}">{escape(card["title"])}</a></h3><p>{escape(card["text"])}</p></article>'
        for card in cards
    )
    return (
        f'<section class="content-card conversion-panel {escape(variant)}-panel">'
        f'<div class="section-head"><h2>{escape(heading)}</h2><p>{escape(intro)}</p></div>'
        f'<div class="conversion-grid">{items}</div></section>'
    )


def render_quote_actions(family: dict) -> str:
    checklist_items = [
        family["support"].get("assumptions", "Confirm the assumption behind the main estimate."),
        family["support"].get("estimate_tip", "Check the part of the job most likely to move the total."),
        family["support"].get("buyer_tip", "Round for real buying units and keep a small safety margin."),
    ]
    li = ''.join(f'<li>{escape(item)}</li>' for item in checklist_items)
    return (
        '<section class="content-card estimate-actions-panel">'
        '<div class="section-head"><h2>Turn this estimate into a buying plan</h2><p>Copy the live result, email it, or print the page so you can compare merchants, quotes, and supporting material layers without starting from scratch.</p></div>'
        '<div class="estimate-action-grid">'
        '<button class="btn btn-primary estimate-action" type="button" data-estimate-action="copy">Copy estimate summary</button>'
        f'<button class="btn btn-secondary estimate-action" type="button" data-estimate-action="email" data-email="{escape(SITE["quote_email"])}">Email estimate summary</button>'
        '<button class="btn btn-secondary estimate-action" type="button" data-estimate-action="print">Print this page</button>'
        '</div>'
        '<p class="estimate-action-note" id="estimate-action-status">Run the calculator first, then use these actions to move the result into your next step.</p>'
        '<div class="quote-checklist"><h3>Quote-ready checklist</h3>'
        f'<ul class="checklist">{li}</ul></div>'
        '</section>'
    )


def render_quote_brief_panel(family: dict) -> str:
    if infer_family_formula(family) != "project_cost":
        return ""
    items = [
        family["support"].get("measure_step", "A measured area, length, or footprint for the real job."),
        family["support"].get("estimate_tip", "The finish level, prep, or access assumption most likely to move the total."),
        family["support"].get("buyer_tip", "The main materials or supporting items that should be visible before comparing prices."),
        family["support"].get("final_check", "A last check on access, waste, and contingency before the quote brief goes out."),
    ]
    bullets = ''.join(f'<li>{escape(item)}</li>' for item in items)
    return (
        '<section class="content-card quote-brief-panel">'
        '<div class="section-head"><h2>Build a cleaner quote brief</h2><p>Project-cost pages work best when the assumptions are written down before you compare contractors, merchants, or buying routes.</p></div>'
        '<div class="quote-brief-grid">'
        '<article class="content-card prose-card quote-brief-card"><h3>Have these details ready</h3>'
        f'<ul class="checklist">{bullets}</ul></article>'
        '<article class="content-card prose-card quote-brief-card"><h3>Use the result properly</h3><p>Keep the calculator total, the selected UK region, the finish level, and any uncertainty notes together. That makes the estimate easier to pressure-test against real quotes.</p><p><a class="text-link" href="/contact/">Open the contact path</a> or review the <a class="text-link" href="/calculator-methodology/">methodology page</a> before sharing the brief.</p></article>'
        '</div></section>'
    )


def render_conversion_path(family: dict, *, page_type: str) -> str:
    budget_calc = find_budget_calculator(family)
    cards = []
    if page_type != "calculator":
        cards.append({
            "eyebrow": "Live estimate",
            "title": family["name"],
            "href": f'/calculators/{family["slug"]}/',
            "text": "Run the calculator first so the guide or cluster notes have a real number to work from.",
        })
    if budget_calc:
        cards.append({
            "eyebrow": "Budget next",
            "title": budget_calc["name"],
            "href": f'/calculators/{budget_calc["slug"]}/',
            "text": "Use the rough quantity result as the input for a wider materials-plus-labour planning range.",
        })
    cards.append({
        "eyebrow": "Tool set",
        "title": family["cluster_name"],
        "href": f'/clusters/{family["cluster_slug"]}/',
        "text": "Open the full tool set to check the supporting materials, waste, and ordering logic around this estimate.",
    })
    cards.append({
        "eyebrow": "Need a tighter number?",
        "title": "Contact BuildCostLab",
        "href": SITE["quote_contact_path"],
        "text": SITE["quote_cta_copy"],
    })
    heading_map = {"calculator": "Use this result on the next step", "guide": "Move from guide to action", "cluster": "Move from tool set to budget", "trust": "Next step"}
    intro_map = {"calculator": "These are the fastest routes from a rough estimate into a budget, order check, or quote brief without leaving the site flow.", "guide": "Use the guide as a sense-check, then jump straight back into a live estimate or the wider budget path.", "cluster": "Start with the tool that fits the job, then move into a broader budget or contact path when the estimate needs more context.", "trust": "Use the next-step links to move into a live estimate or budget page."}
    heading = heading_map.get(page_type, "Next step")
    intro = intro_map.get(page_type, intro_map["guide"])
    return render_conversion_cards(cards[:4], heading=heading, intro=intro, variant=page_type)


def render_home_conversion_cards() -> str:
    cards = []
    for item in get_project_cost_calculators()[:4]:
        cards.append({
            "eyebrow": "Project budget",
            "title": item["name"],
            "href": f'/calculators/{item["slug"]}/',
            "text": item["intro"],
        })
    cards.append({
        "eyebrow": "Contact",
        "title": "Need a tighter estimate path?",
        "href": SITE["quote_contact_path"],
        "text": "Use the contact page for calculator feedback, commercial conversations, or to start shaping a cleaner quote brief.",
    })
    return render_conversion_cards(cards, heading="Budget-first tools", intro="Start here when you need more than a material count and want a rough materials-plus-labour planning range.", variant="home")

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


def build_trust_pages():
    pages = []
    for page in TRUST_PAGES:
        path = f'/{page["slug"]}/'
        crumbs = [("Home", "/"), (page["title"], path)]
        sections = render_section_cards([(item["title"], item["body"]) for item in page["sections"]])
        standards = render_section_cards([
            ("Reviewed by", f"{SITE['review_team']} reviews the wording, estimate framing, and trust notes used across the site."),
            ("Research and maintenance", f"{SITE['research_team']} checks formulas, internal links, and page support blocks when key pages are refreshed."),
            ("Planning-use reminder", "The site is designed for planning decisions and early budgeting, not fixed quotes or engineering sign-off."),
        ])
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">Publisher information</div><h1>{escape(page["headline"])}</h1>'
            f'<p class="hero-copy">{escape(page["intro"])}</p></section>'
            f'{render_authority_panel("trust")}'
            f'{render_ad_slot("trust-top")}'
            f'{sections}'
            f'{standards}'
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


def build_cluster_pages():
    pages = []
    clusters = {}
    for item in get_all_calculators():
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
        decision_section = render_cluster_decision_section(intent_pages, guide_pages)
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            f'<div class="eyebrow">Tool set</div><h1>{escape(family["cluster_name"])}</h1>'
            f'<p class="hero-copy">{escape(get_cluster_intro(cluster_slug, family["intro"]))}</p>'
            f'<div class="hero-badges"><span class="hero-badge">{escape(family["category"])}</span><span class="hero-badge">{len(items)} calculators</span><span class="hero-badge">Related guides included</span></div></section>'
            f'{render_ad_slot(f"{key}-hub-top")}'
            f'{featured_section}'
            f'{calculator_section}'
            f'{render_conversion_path(family, page_type="cluster")}'
            f'{render_region_cost_overview(family)}'
            f'{render_quote_brief_panel(family)}'
            f'{render_section_cards(hub_content.get("notes", [("How to use this tool set", "Start with the calculator that matches the material or buying format you actually need, then move into the related guides if you need more detail before buying."), ("What affects estimates most", "Dimensions, depth or coverage assumptions, waste allowance, and pack or stock-length rounding are usually the biggest drivers of the final buying number."), ("Why these guides are useful", "The extra guides in each tool set help explain common mistakes, waste allowances, and buying choices that a simple quantity figure cannot cover on its own.")]))}'
            f'{decision_section}'
            f'{intent_section}'
            f'{guide_section}</div>'
        )
        cluster_schema_items = build_item_list_entries(items, '/calculators/', name_key='name') + build_item_list_entries((intent_pages + guide_pages)[:6], '/guides/')
        html = render_layout(
            title=f'{family["cluster_name"]} | {SITE["name"]}',
            description=f'Browse {family["cluster_name"].lower()} calculators and supporting guides on {SITE["name"]}.',
            path=path,
            content=content,
            schema=[render_breadcrumb_schema(crumbs), render_item_list_schema(f'{family["cluster_name"]} pages', cluster_schema_items)],
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
            guide_type = classify_guide(item)
            quick_answer = {
                "comparison": "Use this page to compare the main trade-offs before deciding which route deserves a live estimate.",
                "labour_split": "Use this page to separate labour pressure from material pressure so the budget is easier to test.",
                "cost_per": "Use this page to compare the real cost rate, not just the sticker price of a box, bag, or pack.",
                "budget": "Use this page to turn a rough total into a more practical planning budget with clearer layers.",
                "drivers": "Use this page to find the assumptions most likely to move the budget before you ask for quotes.",
                "general": "Use this page to sense-check the main estimate and avoid the ordering mistakes people make most often.",
            }
            faq_section = '<section class="stack-grid">' + ''.join(
                f'<article class="content-card prose-card"><h2>{escape(entry["q"])}</h2><p>{escape(entry["a"])}</p></article>'
                for entry in family["faqs"]
            ) + '</section>'
            content = (
                f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
                f'<div class="eyebrow">{escape(family["cluster_name"])}</div><h1>{escape(item["headline"])}</h1>'
                f'<p class="hero-copy">{escape(item["intro"])}</p></section>'
                f'{render_authority_panel("guide")}'
                f'{render_ad_slot(f"{key}-guide-top")}'
                f'{render_quality_strip("guide")}'
                f'{render_guide_summary_strip(family, item)}'
                f'<section class="content-card prose-card"><h2>Quick answer</h2><p>{escape(quick_answer.get(guide_type, quick_answer["general"]))}</p></section>'
                f'<section class="content-card prose-card"><h2>Use the calculator first</h2><p>The quickest path is to start with <a href="/calculators/{escape(family["slug"])}">{escape(family["name"])}</a>, then use this guide to sense-check the result and decide what to buy next.</p></section>'
                f'{render_methodology_steps(family)}'
                f'{render_comparison_matrix(family, item)}'
                f'{render_guide_decision_cards(family, item)}'
                f'{render_guide_examples(family)}'
                f'{render_region_cost_overview(family)}'
                f'{render_quote_brief_panel(family)}'
                f'{render_conversion_path(family, page_type="guide")}'
                f'{render_related_guide_cards(family, item["slug"])}'
                f'{render_section_cards(supporting_cards)}'
                f'{render_estimate_limits(family)}'
                f'{faq_section}'
                f'<section class="content-card prose-card"><h2>Next step links</h2><p><a href="/clusters/{escape(family["cluster_slug"])}">Open the full {escape(family["cluster_name"])} tool set</a> or go straight to the <a href="/calculators/{escape(family["slug"])}">{escape(family["name"])}</a>.</p></section>'
                '</div>'
            )
            html = render_layout(
                title=f'{item["title"]} | {SITE["name"]}',
                description=item["description"],
                path=path,
                content=content,
                schema=[render_breadcrumb_schema(crumbs), render_faq_schema(family["faqs"])],
                page_type="guide",
            )
            pages.append((path, html))
    return pages


def render_quality_strip(page_type: str) -> str:
    return (
        '<section class="quality-strip" aria-label="Freshness and methodology">'
        f'<article class="content-card quality-card"><div class="quality-kicker">Last checked</div><h2>{escape(SITE["updated_label"])}</h2><p>We checked the calculator logic, page notes, and related links on this page.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Estimate use</div><h2>Planning before buying</h2><p>Use this {escape(page_type)} for early buying and budget checks, then confirm the final order against product data, access, and site conditions.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Trust layer</div><h2>{escape(SITE["review_team"])}</h2><p>Read the <a href="{escape(SITE["methodology_path"])}">calculator methodology</a> and <a href="{escape(SITE["editorial_policy_path"])}">editorial policy</a> for the standards behind these pages.</p></article>'
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
        next_step_section = f'<section class="related-tools"><div class="section-head"><h2>Next-step guides</h2><p>Use these guides to sense-check the estimate, avoid common mistakes, and choose the right buying format.</p></div><div class="mini-tool-grid">{next_links}</div></section>'
    compare_links = "".join(
        f'<a class="mini-tool-card" href="/guides/{escape(item["slug"])}">{escape(item["title"])}</a>'
        for item in family["intent_pages"] + family["guide_pages"]
        if classify_guide(item) != "general"
    )
    compare_section = ""
    if compare_links:
        compare_section = f'<section class="related-tools compare-link-panel"><div class="section-head"><h2>Comparison and budget guides</h2><p>Use these pages when the job has moved beyond a raw quantity and you need to compare routes, cost rates, or labour pressure.</p></div><div class="mini-tool-grid">{compare_links}</div></section>'
    return (
        f'{render_authority_panel("calculator")}'
        f'{render_quote_actions(family)}'
        f'{render_region_cost_overview(family)}'
        f'{render_quote_brief_panel(family)}'
        f'{render_conversion_path(family, page_type="calculator")}'
        f'{render_ad_slot(f"{key}-mid")}'
        f'{render_methodology_steps(family)}'
        f'{render_section_cards([("Assumptions", family["support"]["assumptions"]), ("Common mistakes", family["support"]["mistakes"]), ("Best use cases", family["support"]["use_case"]), ("How to get a better estimate", family["support"].get("estimate_tip", "Measure carefully, apply realistic waste, and sense-check the result against how the product is actually sold.")), ("Before you buy", family["support"].get("buyer_tip", "Round to whole buying units and compare product coverage before buying solely on sticker price.")), ("UK and US note", family["support"].get("market_note", "Unit wording and supplier pack conventions differ between markets, but the estimating logic still starts with geometry, waste, and whole-unit ordering.")), ("Final buying check", family["support"].get("final_check", "Before placing an order, compare product coverage, pack size, delivery cost, and whether buying one extra unit is safer than risking a shortfall."))])}'
        f'{render_estimate_limits(family)}'
        f'{render_assumption_checklist(family)}'
        f'<section class="content-card prose-card"><h2>Explore this tool set</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} tool set</a> to move from quick estimate to deeper guidance.</p></section>'
        f'{next_step_section}'
        f'{compare_section}'
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
        f'<p class="hero-copy">{escape(intro)}</p>'
        '<div class="hero-badges"><span class="hero-badge">Estimate range</span><span class="hero-badge">Cost breakdown</span><span class="hero-badge">Compare options</span></div></section>'
        f'{render_ad_slot(f"{key}-top")}'
        f'{render_quality_strip("calculator")}'
        f'<section class="calculator-layout"><div class="content-card calculator-card">{form_html}</div><aside class="content-card result-card">{result_html}{render_cost_intelligence_shell()}</aside></section>'
        f'{build_calculator_support(slug)}</div><script src="/assets/js/global-calculator.js"></script><script src="/assets/js/cost-intelligence.js"></script><script src="/assets/js/estimate-actions.js"></script><script src="/assets/js/{escape(script_name)}"></script>'
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
    comparison_cards = []
    cost_cards = []
    for family in get_all_calculators():
        for item in family["intent_pages"] + family["guide_pages"]:
            card = f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p></article>'
            cards.append(card)
            guide_type = classify_guide(item)
            if guide_type in {"comparison", "labour_split"}:
                comparison_cards.append(card)
            if guide_type in {"cost_per", "budget", "drivers"}:
                cost_cards.append(card)
    path = "/guides/"
    crumbs = [("Home", "/"), ("Guides", path)]
    guide_items = []
    for family in get_all_calculators():
        for item in family["intent_pages"] + family["guide_pages"]:
            guide_items.append({"name": item["title"], "url": f'/guides/{item["slug"]}/'})
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Guide library</div><h1>Supporting guides built around calculator intent</h1>'
        '<p class="hero-copy">These pages are written to support real estimating and buying decisions, then route users back into the right calculator or tool set.</p></section>'
        f'{render_ad_slot("guides-index-top")}'
        '<section class="quality-strip guide-summary-strip">'
        '<article class="content-card quality-card"><div class="quality-kicker">Best for</div><h2>Buying checks</h2><p>Use the guides when the raw quantity is not enough and you need more confidence before ordering.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">Compare</div><h2>Rates and options</h2><p>Comparison, cost-per-area, and labour-vs-material pages help users make a cleaner decision.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">Next move</div><h2>Jump back into the tool</h2><p>Each guide is designed to route back into the right calculator or cluster once the decision is clearer.</p></article>'
        '</section>'
        '<section class="content-card prose-card"><h2>Comparison guides</h2><p>Use these when you need to choose between materials, buying formats, or labour-vs-material pressure points.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(comparison_cards[:9])}</div></section>'
        '<section class="content-card prose-card"><h2>Cost and budget guides</h2><p>These pages help with cost per m², budget planning, and understanding what usually moves the estimate most.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(cost_cards[:9])}</div></section>'
        '<section class="content-card prose-card"><h2>All guide pages</h2><p>Browse the full guide library by estimating intent, then move back into the calculator that fits the job.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(cards)}</div></section></div>'
    )
    return path, render_layout(
        title=f'Guides | {SITE["name"]}',
        description="Browse BuildCostLab guides covering material quantities, waste, and rough cost decisions.",
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs), render_item_list_schema('BuildCostLab guides', guide_items[:80])],
        page_type="guide-index",
    )


def build_compare_index() -> tuple[str, str]:
    pairs = gather_all_guides()
    compare_pairs = [(family, item) for family, item in pairs if classify_guide(item) in {"comparison", "labour_split"}]
    budget_pairs = [(family, item) for family, item in pairs if classify_guide(item) in {"cost_per", "budget", "drivers"}]
    compare_cards = "".join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p><p class="tool-card-meta">{escape(family["cluster_name"])}</p></article>'
        for family, item in compare_pairs[:18]
    )
    budget_cards = "".join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(item["slug"])}">{escape(item["title"])}</a></h3><p>{escape(item["description"])}</p><p class="tool-card-meta">{escape(family["cluster_name"])}</p></article>'
        for family, item in budget_pairs[:18]
    )
    calc_cards = "".join(
        f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
        for item in get_project_cost_calculators()[:6]
    )
    crumbs = [("Home", "/"), ("Compare", "/compare/")]
    list_items = [{"name": item["title"], "url": f'/guides/{item["slug"]}/'} for _, item in (compare_pairs + budget_pairs)[:80]]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Comparison hub</div><h1>Compare materials, buying routes, and budget logic</h1>'
        '<p class="hero-copy">Use this hub when a raw quantity is not enough and you need to decide between products, buying formats, labour-heavy routes, or wider budget assumptions.</p></section>'
        f'{render_ad_slot("compare-index-top")}'
        '<section class="quality-strip guide-summary-strip">'
        '<article class="content-card quality-card"><div class="quality-kicker">Best for</div><h2>Choice pages</h2><p>Open these when the real question is not how much, but which route is the better fit for the job.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">Budget logic</div><h2>Rates and pressure points</h2><p>Cost-per-area, labour-vs-material, and driver pages help turn fuzzy numbers into cleaner decisions.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">Next step</div><h2>Pressure-test with calculators</h2><p>After comparing routes, jump back into the live calculators to test the winner with real measurements.</p></article>'
        '</section>'
        '<section class="content-card prose-card"><h2>Material and buying-format comparisons</h2><p>These pages compare one route against another so you can see the practical trade-offs before the order feels locked in.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{compare_cards}</div></section>'
        '<section class="content-card prose-card"><h2>Cost, labour, and budget pages</h2><p>Use these when the comparison is really about cost rate, labour pressure, contingency, or the assumptions most likely to move the total.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{budget_cards}</div></section>'
        '<section class="content-card prose-card"><h2>Need a live number first?</h2><p>These project-cost calculators are a strong next move after reading a comparison page because they combine materials, labour, extras, and contingency.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{calc_cards}</div></section>'
        '<section class="content-card prose-card"><h2>Before you compare quotes</h2><p>Keep the area, finish level, region, waste assumptions, and the main extras visible in the same note. That makes builder or merchant comparisons much easier to pressure-test.</p><p><a class="text-link" href="/contact/">Use the contact path</a> if you want a cleaner feedback route after running the calculators.</p></section></div>'
    )
    return '/compare/', render_layout(
        title=f'Compare Building Options | {SITE["name"]}',
        description='Compare materials, buying routes, labour pressure, and budget assumptions across BuildCostLab guides.',
        path='/compare/',
        content=content,
        schema=[render_breadcrumb_schema(crumbs), render_item_list_schema('BuildCostLab comparison guides', list_items)],
        page_type='compare-index',
    )




def build_clusters_index() -> tuple[str, str]:
    seen = set()
    parts = []
    cluster_items = []
    cost_parts = []
    for item in get_all_calculators():
        if item["cluster_slug"] in seen:
            continue
        seen.add(item["cluster_slug"])
        card = f'<article class="tool-card"><h3><a href="/clusters/{escape(item["cluster_slug"])}/">{escape(item["cluster_name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
        parts.append(card)
        cluster_items.append({"name": item["cluster_name"], "url": f'/clusters/{item["cluster_slug"]}/'})
        if item.get("formula") == "project_cost" or item["cluster_slug"] == "project-cost-estimating":
            cost_parts.append(card)
    cards = "".join(parts)
    path = "/clusters/"
    crumbs = [("Home", "/"), ("Tool Sets", path)]
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Project tool sets</div><h1>Tool sets by project type</h1>'
        '<p class="hero-copy">Browse grouped calculators and guides for painting, concrete, roofing, landscaping, flooring, and other common building jobs.</p></section>'
        f'{render_ad_slot("clusters-index-top")}'
        '<section class="quality-strip guide-summary-strip">'
        '<article class="content-card quality-card"><div class="quality-kicker">Start here</div><h2>Pick the right job family</h2><p>Clusters group the calculators and guides that usually belong together in a real project flow.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">Best for</div><h2>Next-step routing</h2><p>Use a cluster when you need more than one calculator or want to compare material and cost pages side by side.</p></article>'
        '<article class="content-card quality-card"><div class="quality-kicker">Commercial intent</div><h2>Project cost planning</h2><p>The project cost cluster is the fastest route from material estimating into broader budget thinking.</p></article>'
        '</section>'
        '<section class="content-card prose-card"><h2>Project cost and budget hub</h2><p>Use the project-cost path when the job has moved beyond materials-only planning and you need a rough materials-plus-labour view.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(cost_parts[:3])}</div></section>'
        '<section class="content-card prose-card"><h2>All tool sets</h2><p>Browse every grouped calculator family and its supporting guides.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section></div>'
    )
    return path, render_layout(
        title=f'Tool Sets | {SITE["name"]}',
        description="Browse BuildCostLab tool sets for calculators, guides, and next-step buying content.",
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs), render_item_list_schema('BuildCostLab tool sets', cluster_items)],
        page_type="cluster-index",
    )
