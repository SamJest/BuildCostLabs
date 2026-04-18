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


def render_calculator_hero_badges(formula: str) -> str:
    badges = {
        "coverage": ["Area + buying units", "Waste-aware result", "Buying checks"],
        "volume": ["Volume + tonnes + units", "Waste-aware result", "Buying checks"],
        "linear": ["Run + stock lengths", "Rounding buffer", "Buying checks"],
        "project_cost": ["Estimate range", "Cost breakdown", "Quote prep"],
    }.get(formula, ["Fast estimate", "Buying checks", "Quote prep"])
    return '<div class="hero-badges">' + "".join(
        f'<span class="hero-badge">{escape(label)}</span>' for label in badges
    ) + '</div>'


def render_quality_strip(page_type: str) -> str:
    page_name = page_type if page_type not in {"project hub", "guide", "calculator"} else page_type
    return (
        '<section class="quality-strip" aria-label="Freshness and methodology">'
        f'<article class="content-card quality-card"><div class="quality-kicker">Last checked</div><h2>{escape(SITE["updated_label"])}</h2><p>We checked the page logic, support notes, and related links on this page.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">How to use it</div><h2>Planning before buying</h2><p>Use this {escape(page_name)} for a planning check, then confirm the final order or quote against live product data and site conditions.</p></article>'
        f'<article class="content-card quality-card"><div class="quality-kicker">Why trust it</div><h2>See how the site is maintained</h2><p>Read the <a href="{escape(SITE["methodology_path"])}">calculator methodology</a> and <a href="{escape(SITE["editorial_policy_path"])}">editorial policy</a> for the standards behind these pages.</p></article>'
        '</section>'
    )


def _dedupe_slug_items(items: list[dict]) -> list[dict]:
    seen: set[str] = set()
    deduped: list[dict] = []
    for item in items:
        slug = item.get("slug")
        if not slug or slug in seen:
            continue
        seen.add(slug)
        deduped.append(item)
    return deduped


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
        f'<div class="section-head"><h2>{escape(page.get("related_links_title", "Related trust pages"))}</h2><p>{escape(page.get("related_links_intro", "Use these pages together when you want to understand how estimates are built, reviewed, and meant to be used."))}</p></div>'
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
    if slug == "flooring-calculator":
        return "Example: a 4.4m by 3.6m room gives 15.84m2 before waste. Add 8 percent and the planning quantity becomes 17.11m2. If the flooring pack covers 1.84m2, the safer buying total is 10 packs rather than 9.3 on paper, especially if you want one cleaner spare-pack margin."
    if slug == "laminate-flooring-calculator":
        return "Example: a 4.4m by 3.6m room gives 15.84m2 before waste. Add 10 percent and the planning quantity becomes 17.42m2. If the laminate pack covers 2.22m2, the safer order is 8 packs rather than 7.85 on paper, especially once doorway cuts and spare-board thinking are included."
    if slug == "hardcore-calculator":
        return "Example: a 5m by 3m base at 100mm depth gives 1.5m3 before waste. Add 10 percent and the planning quantity becomes 1.65m3. At roughly 1.7 tonnes per m3, that is about 2.8 tonnes, which is close to four 0.85-tonne bulk bags."
    if slug == "sub-base-calculator":
        return "Example: a 6m by 3m patio base at 120mm depth gives 2.16m3 before waste. Add 10 percent and the planning quantity becomes 2.376m3. At roughly 1.8 tonnes per m3, that is about 4.28 tonnes, so five 0.85-tonne bulk bags is the safer planning order."
    if slug == "mot-type-1-calculator":
        return "Example: a 6m by 3m driveway base at 120mm compacted depth gives 2.16m3 before waste. Add 10 percent and the planning quantity becomes 2.376m3. At roughly 1.8 tonnes per m3, that is about 4.28 tonnes, so five 0.85-tonne bulk bags is the safer planning order."
    if slug == "drainage-pipe-calculator":
        return "Example: a 24m run with 8 percent waste becomes 25.92m of planned pipe coverage. If the pipe is sold in 3m lengths, the safer order is 9 lengths rather than 8.64 on paper, especially once bends, branches, and one modest spare are considered."
    if slug == "french-drain-gravel-calculator":
        return "Example: a 12m trench at 350mm width and 450mm gravel depth gives 1.89m3 before waste. Add 10 percent and the planning quantity becomes 2.079m3. At roughly 1.6 tonnes per m3, that is about 3.33 tonnes, so four 0.85-tonne bulk bags is the safer planning order."
    if slug == "geotextile-membrane-calculator":
        return "Example: a 15m by 2m covered area gives 30m2 before waste. Add 12 percent and the planning quantity becomes 33.6m2. If the effective roll coverage after overlaps is 45m2, one roll covers the job, but a second roll may still be worth checking on more awkward layouts."
    if slug == "coving-calculator":
        return "Example: a 14m ceiling perimeter with 12 percent waste becomes 15.68m of planned coverage. If the profile is sold in 2m lengths, the safer order is 8 lengths rather than 7.84 on paper, especially once mitres and short return pieces are involved."
    if slug == "skirting-board-calculator":
        return "Example: a room with 15.2m of wall run after doorway deductions becomes 16.72m once 10 percent waste is added. If the skirting is sold in 4.2m boards, the safer buying total is 4 boards rather than 3.98 on paper."
    if slug == "pipe-bedding-calculator":
        return "Example: a 15m drainage run with a 300mm bedding width and 100mm bedding depth gives 0.45m3 before waste. Add 10 percent and the planning quantity becomes 0.495m3. At roughly 1.6 tonnes per m3, that is about 0.79 tonnes, which is close to one 0.85-tonne bulk bag."
    if "paint" in slug and "cost" not in slug:
        return "Example: 12m2 of wall area with a paint coverage rate of 10m2 per tin and 10 percent waste becomes 13.2m2 of planned coverage. That is 1.32 tins on paper, so the safer buying decision is 2 tins."
    if "concrete" in slug and formula != "project_cost":
        return "Example: a 4m by 3m slab at 100mm depth gives 1.2m3 before waste. Add 10 percent and the planning quantity becomes 1.32m3, which is the number to compare against bagged or ready-mix buying routes."
    if "gravel" in slug or "sub-base" in slug or "mot-type-1" in slug:
        return "Example: a 5m by 3m area at 50mm depth gives 0.75m3 before waste. Add 10 percent and the planning quantity becomes 0.825m3. From there you can compare bulk bags, loose loads, or tonnage-based supply."
    if "deck" in slug:
        return "Example: an 18m2 deck with 10 percent waste becomes 19.8m2 of buying allowance. The board count is only part of the job, so check screws, joists, trims, and awkward cuts before you treat the first total as final."
    if "floor" in slug and formula == "coverage":
        return "Example: a 14m2 room with 8 percent waste becomes 15.12m2 of buying coverage. If the product is sold by pack, compare that figure against the pack yield and round up to the next full pack."
    if "tile" in slug and formula == "coverage":
        return "Example: 9m2 of tiled area with 12 percent waste becomes 10.08m2 of planned coverage. That is the safer figure to use when you compare tile boxes, adhesive bags, and grout allowances."
    if "fence" in slug:
        return "Example: a 15m run with 1.8m panels does not only need a panel count. It also needs a sensible allowance for posts, gravel boards, concrete, and any shorter end section that changes the final buying list."
    if formula == "coverage":
        return "Example: 12m2 of measured coverage with 10 percent waste becomes 13.2m2 of planned coverage. Divide by the real pack or unit yield, then round up to the next full buying unit."
    if formula == "volume":
        return "Example: 4m by 3m by 50mm gives 0.6m3 before waste. Add 10 percent and the planning quantity becomes 0.66m3. Then compare that number against the way the product is actually sold."
    if formula == "linear":
        return "Example: an 18m run with 8 percent waste becomes 19.44m of planned coverage. If lengths are sold in 2.4m pieces, the safer order is 9 lengths rather than 8.1 on paper."
    return "Example: a 20m2 job at GBP60 per m2 for materials, GBP45 per m2 for labour, and GBP12 per m2 for extras creates a baseline planning rate of GBP117 per m2 before complexity and contingency are added."


def _calculator_methodology_cards(family: dict) -> list[tuple[str, str]]:
    formula = family.get("formula")
    method_text = {
        "coverage": "We multiply length by width, add the waste allowance, then convert the adjusted area into whole buying units using the stated coverage per pack, roll, sheet, bag, or tin.",
        "volume": "We multiply length by width by depth, add the waste allowance, then convert the adjusted volume into tonnes or whole buying units using the stated density and delivery format.",
        "linear": "We measure the total run, add the waste allowance, then convert the adjusted run into whole stock lengths using the selected piece length.",
        "project_cost": "We measure the scope first, add complexity, then build a planning total from materials, labour, extras, regional weighting, and contingency rather than from one flat rate.",
    }
    rounding_text = {
        "coverage": "Because most products are bought in full packs, rolls, sheets, or tins, the final answer rounds up to a real ordering total rather than stopping at the theoretical minimum.",
        "volume": "Because bulk materials are bought by bag, bulk bag, tonne, or loose load, the final answer rounds to a real buying quantity rather than stopping at the theoretical trench or base volume.",
        "linear": "Because trims, pipes, and stock lengths are bought in whole pieces, the final answer rounds up to a real ordering total and shows the buffer created by that rounding.",
        "project_cost": "Because real budgets need room for uncertainty, the final answer is shown as a planning total with scenario range support rather than one overconfident exact quote.",
    }
    return [
        ("How this estimate is worked out", method_text.get(formula, family["support"]["assumptions"])),
        ("What assumptions sit underneath it", family["support"]["assumptions"]),
        ("How rounding is handled", rounding_text.get(formula, family["support"]["final_check"])),
    ]


def _calculator_driver_cards(family: dict) -> list[tuple[str, str]]:
    if family["slug"] == "flooring-calculator":
        return [
            ("What changes the result most", "Room shape, pack coverage, board direction, visible cut-heavy edges, and whether you keep a same-batch spare pack usually move the flooring order fastest."),
            ("Where people under-order", "Neat room area maths often misses hall links, bay details, thresholds, and the spare-pack margin many buyers wish they had kept."),
            ("Practical buying checks", "Check underlay, trims, thresholds, skirting clearance, and whether subfloor prep still needs its own quantity or budget check."),
        ]
    if family["slug"] == "laminate-flooring-calculator":
        return [
            ("What changes the result most", "Pack coverage, room shape, board direction, and the decision to keep same-batch spare boards usually move laminate totals fastest."),
            ("Where people under-order", "The neat room area often misses doorway cuts, linked spaces, angled walls, and the extra spare that protects future repair matching."),
            ("Practical buying checks", "Check underlay, trims, thresholds, moisture control layers, and whether one extra pack is cheaper than a mismatch or delayed top-up order."),
        ]
    if family["slug"] == "hardcore-calculator":
        return [
            ("What changes the result most", "Compacted depth, density, level corrections, and whether the site suits bags, bulk bags, or loose tonnes usually move the hardcore order fastest."),
            ("Where people under-order", "The neat footprint often misses soft spots, uneven formation, and the extra material needed when the site does not hold a perfect constant depth."),
            ("Practical buying checks", "Compare bulk bags against loose tonnes, check if compaction changes the delivered quantity, and confirm whether membrane or top layers still need separate material checks."),
        ]
    if family["slug"] == "sub-base-calculator":
        return [
            ("What changes the result most", "Compacted depth, density, the final paved footprint, and any level correction in the formation usually move the sub-base order fastest."),
            ("Where people under-order", "Base layers often rise above the paper total once weak spots, edge thickening, and level corrections are added back into the build-up."),
            ("Practical buying checks", "Compare MOT Type 1, hardcore, and other graded routes, then check whether bulk bags or loose tonnes fit the site access and spreading plan best."),
        ]
    if family["slug"] == "mot-type-1-calculator":
        return [
            ("What changes the result most", "Compacted depth, density, edge thickening, and whether the area needs level correction usually move the Type 1 order fastest."),
            ("Where people under-order", "Drive edges, weak spots, and turning areas often use more Type 1 than the neat footprint suggests once the real build-up is checked."),
            ("Practical buying checks", "Compare bulk bags against loose tonnes, confirm the specified Type 1 grade, and check whether membrane, bedding, and drainage layers are being priced separately."),
        ]
    if family["slug"] == "drainage-pipe-calculator":
        return [
            ("What changes the result most", "Full run length, stock length, fitting count, chamber positions, and whether one spare pipe length is worth carrying usually move the pipe order fastest."),
            ("Where people under-order", "Straight-run maths often misses bends, chamber entries, branches, and the offcuts that stop a neat paper result from matching the real trench route."),
            ("Practical buying checks", "Confirm the pipe diameter, stock length, fittings, and chamber list, then check whether bedding, surround, and membrane are being estimated alongside the pipe order."),
        ]
    if family["slug"] == "french-drain-gravel-calculator":
        return [
            ("What changes the result most", "Trench width, gravel depth, outlet details, widened sections, and whether the supplier prices by bulk bag or loose tonne usually move the order fastest."),
            ("Where people under-order", "French drains often rise above the neat trench total once corners, outlets, soakaway ties, and overbreak are added back into the real gravel envelope."),
            ("Practical buying checks", "Check whether the gravel order covers the washed aggregate only, then confirm membrane wrap, pipe bedding, and reinstatement materials separately."),
        ]
    if family["slug"] == "geotextile-membrane-calculator":
        return [
            ("What changes the result most", "Overlap allowance, effective roll coverage, awkward edges, and the membrane grade usually move the final roll count fastest."),
            ("Where people under-order", "Clean rectangle maths often misses turn-ups, trench edges, joints, and trimming around curves or drainage details."),
            ("Practical buying checks", "Check the roll width, overlap requirement, and membrane grade, then make sure the aggregate layers above and below are being estimated alongside it."),
        ]
    if family["slug"] == "pipe-bedding-calculator":
        return [
            ("What changes the result most", "Bedding width, bedding depth below the pipe, widened trench sections at chambers or fittings, and the choice between sand, gravel, bags, or loose delivery usually move the order fastest."),
            ("Where people under-order", "Straight trench maths often misses the extra material used around bends, connections, inspection chambers, and any gravel surround that sits above or beside the base bedding."),
            ("Practical buying checks", "Confirm whether the merchant quote covers the bedding layer only or the full trench aggregate build-up, then compare bulk bags, tonne pricing, and whether access makes one route easier than another."),
        ]
    if family["slug"] == "coving-calculator":
        return [
            ("What changes the result most", "Corner count, chimney breasts, bay returns, piece length, and how brittle or ornate the profile is usually what moves the coving order fastest."),
            ("Where people under-order", "Clean perimeter maths often misses short return pieces, damaged ends after mitres, and the extra spare that decorative or plaster coving can need."),
            ("Practical buying checks", "Compare 2m and 3m lengths, check whether corners or adhesives are priced separately, and decide whether a spare length is worth carrying for breakage or later repairs."),
        ]
    if family["slug"] == "skirting-board-calculator":
        return [
            ("What changes the result most", "Doorway deductions, alcoves, long visible walls, board length, and the number of scribes or mitres usually move the skirting order fastest."),
            ("Where people under-order", "Straight perimeter maths often ignores return pieces, damaged ends, awkward joints on visible walls, and the spare board many buyers wish they had kept."),
            ("Practical buying checks", "Compare 3m and 4.2m boards, decide whether MDF, pine, or finished boards suit the room best, and check whether adhesive, pins, caulk, and filler are being priced separately."),
        ]
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
    if family["slug"] == "flooring-calculator":
        items_map["coverage"] = [
            "State the room dimensions, chosen flooring route, pack coverage, and the waste allowance you want priced against.",
            "Ask whether underlay, trims, thresholds, and subfloor prep are included or need separate quantities.",
            "Check whether a same-batch spare pack is worth carrying before the order is treated as final.",
        ]
    if family["slug"] == "laminate-flooring-calculator":
        items_map["coverage"] = [
            "State the room size, laminate pack coverage, waste allowance, and whether you want a same-batch spare pack included.",
            "Ask whether underlay, trims, door bars, and moisture-control layers are included or need separate quantities.",
            "Check whether room shape, hall links, or visible cut-heavy edges justify a more cautious pack total.",
        ]
    items_html = "".join(f'<li>{escape(item)}</li>' for item in items_map.get(formula, []))
    return (
        '<section class="conversion-panel">'
        '<div class="section-head"><h2>Quote-ready checklist</h2><p>Use these prompts when you want to turn the estimate into a clearer builder, installer, or merchant request.</p></div>'
        f'<ul class="conversion-list">{items_html}</ul>'
        '</section>'
    )


def _score_related_calculator(current: dict, candidate: dict) -> int:
    score = 0
    if current["cluster_slug"] == candidate["cluster_slug"]:
        score += 100
    if current.get("formula") == candidate.get("formula"):
        score += 40
    if current.get("category") == candidate.get("category"):
        score += 20
    current_tokens = set(current["slug"].replace("-calculator", "").split("-")) | set(
        current["name"].lower().replace("calculator", "").split()
    )
    candidate_tokens = set(candidate["slug"].replace("-calculator", "").split("-")) | set(
        candidate["name"].lower().replace("calculator", "").split()
    )
    score += len(current_tokens & candidate_tokens) * 6
    return score


def _calculator_related_calculators(family: dict) -> str:
    lookup = family_lookup()
    slugs = family.get("related_calculator_slugs", [])
    explicit_links = bool(slugs)
    if not slugs:
        candidates = sorted(
            (
                item
                for item in lookup.values()
                if item["slug"] != family["slug"] and item["cluster_slug"] == family["cluster_slug"]
            ),
            key=lambda item: (-_score_related_calculator(family, item), item["name"]),
        )
        slugs = [item["slug"] for item in candidates[:4]]
    cards = []
    for slug in slugs:
        entry = lookup.get(slug)
        if not entry or slug == family["slug"]:
            continue
        cards.append(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(entry["slug"])}/">{escape(entry["name"])}</a></h3><p>{escape(entry["intro"])}</p></article>'
        )
    if not cards:
        return ""
    if family["slug"] == "pipe-bedding-calculator":
        title = "Related calculators for the same drainage or base build-up"
        intro = "Use these linked tools when the trench estimate needs pipe length, membrane coverage, gravel surround, or supporting base-material quantities rather than one isolated number."
    elif not explicit_links:
        title = "Related calculators in the same project hub"
        intro = f'Use these linked tools when the estimate crosses into another calculator in the {family["cluster_name"]} cluster rather than stopping at one isolated material number.'
    else:
        title = family.get("related_calculator_title", "Related calculators for the same job")
        intro = family.get("related_calculator_intro", "Use these linked tools when the estimate depends on more than one material, layer, room finish, or buying format.")
    return (
        f'<section class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(intro)}</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(cards)}</div></section>'
    )


def _cluster_workflow_section(hub_content: dict) -> str:
    workflow_cards = hub_content.get("workflow_cards", [])
    if not workflow_cards:
        return ""
    title = hub_content.get("workflow_title", "How to use this project hub")
    intro = hub_content.get("workflow_intro", "Follow this route to move from first estimate into a cleaner buying or quote-prep decision.")
    cards_html = "".join(
        f'<article class="content-card prose-card"><h2>{escape(card_title)}</h2><p>{escape(card_body)}</p></article>'
        for card_title, card_body in workflow_cards
    )
    return (
        f'<section class="content-card prose-card"><div class="section-head"><h2>{escape(title)}</h2><p>{escape(intro)}</p></div></section>'
        f'<section class="stack-grid workflow-grid">{cards_html}</section>'
    )


def _cluster_quote_support_section(items: list[dict], hub_content: dict) -> str:
    calculator_slugs = hub_content.get("quote_support_calculator_slugs", [])
    guide_slugs = hub_content.get("quote_support_guide_slugs", [])
    if not calculator_slugs and not guide_slugs:
        return ""
    calculator_lookup = family_lookup()
    guide_lookup = {}
    for item in items:
        for guide in _dedupe_slug_items(item["intent_pages"] + item["guide_pages"]):
            guide_lookup[guide["slug"]] = guide
    cards = []
    for slug in calculator_slugs:
        entry = calculator_lookup.get(slug)
        if not entry:
            continue
        cards.append(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(entry["slug"])}/">{escape(entry["name"])}</a></h3><p>Calculator: {escape(entry["intro"])}</p></article>'
        )
    for slug in guide_slugs:
        entry = guide_lookup.get(slug)
        if not entry:
            continue
        cards.append(
            f'<article class="tool-card"><h3><a href="/guides/{escape(entry["slug"])}/">{escape(entry["title"])}</a></h3><p>Guide: {escape(entry["description"])}</p></article>'
        )
    if not cards:
        return ""
    title = hub_content.get("quote_support_title", "Best pages to include in the brief")
    intro = hub_content.get("quote_support_intro", "Use these linked pages when the request depends on more than one calculation or one final buying check.")
    return (
        f'<section class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(intro)}</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{"".join(cards)}</div></section>'
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
            title=page.get("meta_title", page["title"]),
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
        intent_pages = _dedupe_slug_items(intent_pages)
        guide_pages = _dedupe_slug_items(guide_pages)

        featured_slugs = hub_content.get("featured_slugs", [item["slug"] for item in items[:3]])
        featured_order = {slug: index for index, slug in enumerate(featured_slugs)}
        featured_items = sorted(
            [item for item in items if item["slug"] in featured_slugs],
            key=lambda item: featured_order.get(item["slug"], 999),
        )
        remaining_items = [item for item in items if item["slug"] not in featured_slugs]
        primary_family = featured_items[0] if featured_items else family

        featured_cards = "".join(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
            for item in featured_items
        )
        calculator_cards = "".join(
            f'<article class="tool-card"><h3><a href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a></h3><p>{escape(item["intro"])}</p></article>'
            for item in remaining_items
        )
        cross_cluster_cards = ""
        cross_cluster_slugs = hub_content.get("cross_cluster_slugs", [])
        if cross_cluster_slugs:
            lookup = family_lookup()
            cross_cluster_cards = "".join(
                f'<article class="tool-card"><h3><a href="/calculators/{escape(lookup[slug]["slug"])}/">{escape(lookup[slug]["name"])}</a></h3><p>{escape(lookup[slug]["intro"])}</p></article>'
                for slug in cross_cluster_slugs
                if slug in lookup
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
        workflow_section = _cluster_workflow_section(hub_content)
        calculator_section = ""
        if calculator_cards:
            calculator_section = (
                '<section class="content-card prose-card"><h2>More calculators in this hub</h2>'
                '<p>Use these related pages when the same project includes extra materials, linked layers, or a different buying format.</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{calculator_cards}</div></section>'
            )
        cross_cluster_section = ""
        if cross_cluster_cards:
            cross_cluster_section = (
                f'<section class="content-card prose-card"><h2>{escape(hub_content.get("cross_cluster_title", "Related calculators outside this hub"))}</h2>'
                f'<p>{escape(hub_content.get("cross_cluster_intro", "Use these linked calculators when the same estimate crosses into a connected material or build-up."))}</p></section>'
                f'<section class="calculator-grid-section"><div class="calculator-grid">{cross_cluster_cards}</div></section>'
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
        quote_support_section = _cluster_quote_support_section(items, hub_content)

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
            f'{workflow_section}'
            f'{calculator_section}'
            f'{cross_cluster_section}'
            f'{render_section_cards(hub_content.get("notes", default_notes))}'
            f'{intent_section}'
            f'{guide_section}'
            f'{quote_support_section}'
            f'{render_quote_prep_panel(primary_family, "cluster", hub_content)}'
            '</div>'
        )
        html = render_layout(
            title=hub_content.get("meta_title", f'{family["cluster_name"]} | {SITE["name"]}'),
            description=hub_content.get("meta_description", f'Browse {family["cluster_name"].lower()} calculators, guides, and next-step planning content on {SITE["name"]}.'),
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
    if 'cost-per' in text or 'per-m2' in text or 'costs' in text:
        return 'cost-per'
    if any(token in text for token in ('waste', 'coverage', 'overlap', 'yield', 'fit', 'depth')):
        return 'waste'
    if any(token in text for token in ('length', 'boxes', 'packs', 'rolls', 'how-much', 'calculator-by-area', 'calculator-by-volume')):
        return 'quantity'
    return 'general'


def _guide_role(item: dict) -> str:
    text = f"{item['slug']} {item['title']}".lower()
    if any(token in text for token in ('calculator-by-area', 'calculator by area', 'calculator-by-volume', 'calculator by volume', 'length-calculator', 'length calculator', 'packs-calculator', 'boxes-calculator', 'rolls-calculator')):
        return 'measurement'
    if 'how-much-do-i-need' in text or 'buying guide' in text or 'quantity guide' in text:
        return 'buying'
    mode = _guide_mode(item)
    if mode == 'waste':
        return 'assumptions'
    if mode == 'compare':
        return 'comparison'
    if mode in {'budget', 'cost-drivers', 'cost-per', 'labour-materials'}:
        return 'cost'
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
    return f"{description.rstrip('.')}." + endings[_guide_mode(item)]


def _guide_support_cards(item: dict, family: dict) -> list[tuple[str, str]]:
    role = _guide_role(item)
    if role == 'measurement':
        return [
            ('What this page isolates', 'It strips the job back to the measured area, volume, or run so you can check the core quantity logic before supplier format, pack rounding, or quote wording changes the answer.'),
            ('Measurement assumption to keep straight', family['support']['assumptions']),
            ('Where the measurement usually drifts', family['support']['mistakes']),
        ]
    if role == 'buying':
        return [
            ('What this page adds after the maths', 'It moves from the neat measured result into the real buying decision: pack size, stock length, spare allowance, linked materials, and what should still be checked before ordering.'),
            ('Buying assumption to keep straight', family['support']['assumptions']),
            ('Common buying miss', family['support']['mistakes']),
        ]
    if role == 'assumptions':
        return [
            ('What this page isolates', 'It focuses on the assumption behind the result rather than repeating the first quantity. Use it to test whether the allowance, overlap, coverage, or yield still looks believable.'),
            ('Assumption under pressure', family['support']['assumptions']),
            ('When the assumption usually breaks', family['support']['mistakes']),
        ]
    if role == 'comparison':
        return [
            ('What this page isolates', 'It separates two routes that often get compared too loosely so you can test them on the same measured scope.'),
            ('Like-for-like assumption', family['support']['assumptions']),
            ('Common comparison mistake', family['support']['mistakes']),
        ]
    if role == 'cost':
        return [
            ('What this page isolates', 'It helps turn a headline rate or planning number into a more usable budget or quote-comparison check.'),
            ('Budget assumption to keep straight', family['support']['assumptions']),
            ('Common budgeting miss', family['support']['mistakes']),
        ]
    return [
        ('What this page isolates', family['support']['use_case']),
        ('Key assumption', family['support']['assumptions']),
        ('Common mistake to avoid', family['support']['mistakes']),
    ]


def _guide_use_calculator_panel(item: dict, family: dict) -> str:
    role = _guide_role(item)
    if role == 'measurement':
        body = f'The fastest route is to use this page to isolate the core area, volume, or run measurement, then confirm the rounded buying total in the <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>.'
    elif role == 'buying':
        body = f'Start with <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a> for the first number, then use this page to pressure-test pack sizes, spare stock, linked materials, and the parts of the order that usually get missed.'
    elif role == 'assumptions':
        body = f'Start with <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>, then use this page to challenge the waste, overlap, or coverage assumption that usually decides whether the result still feels safe.'
    elif role == 'comparison':
        body = f'Run <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a> first so both routes are compared against the same measured scope rather than two different assumptions.'
    elif role == 'cost':
        body = f'Use <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a> as the planning baseline, then use this page to test the cost assumptions before you compare live quotes.'
    else:
        body = f'The quickest path is to start with <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>, then use this guide to sense-check the result and decide what to buy or ask for next.'
    return f'<section class="content-card prose-card"><h2>Use the calculator first</h2><p>{body}</p></section>'


def _guide_section_copy(item: dict) -> dict:
    role = _guide_role(item)
    if role == 'measurement':
        return {
            'tradeoff_title': 'Measurement rules that change the answer',
            'tradeoff_intro': 'These are the checks that usually move the clean area, volume, or run figure before it turns into a real order.',
            'example_title': 'Where the neat measurement usually moves',
            'example_intro': 'Use these examples to see when the first measured number stops being enough on its own.',
        }
    if role == 'buying':
        return {
            'tradeoff_title': 'Buying decisions after the maths',
            'tradeoff_intro': 'These are the choices that usually change the real order once the first quantity is roughly right.',
            'example_title': 'Where buying totals usually move',
            'example_intro': 'Use these examples to see where pack size, spare stock, or linked materials push the final order.',
        }
    if role == 'assumptions':
        return {
            'tradeoff_title': 'Assumptions that change the result',
            'tradeoff_intro': 'These are the places where one allowance or coverage assumption often matters more than the neat first number.',
            'example_title': 'Where the assumption usually breaks',
            'example_intro': 'Use these examples to see when the default allowance stops matching the real job.',
        }
    if role == 'comparison':
        return {
            'tradeoff_title': 'Trade-offs to compare',
            'tradeoff_intro': 'These are the route choices that usually matter more than a neat headline difference.',
            'example_title': 'Where the better option changes',
            'example_intro': 'Use these examples to see when one route starts to outperform the other on the same scope.',
        }
    if role == 'cost':
        return {
            'tradeoff_title': 'Cost checks that move the budget',
            'tradeoff_intro': 'These are the cost layers that usually matter more than the neat headline benchmark.',
            'example_title': 'Where planning budgets usually change',
            'example_intro': 'Use these examples to see when the first budget check needs a stronger allowance.',
        }
    return {
        'tradeoff_title': 'Trade-offs to compare',
        'tradeoff_intro': 'These are the practical choices that usually matter more than a neat headline answer.',
        'example_title': 'Worked examples and scenario checks',
        'example_intro': 'Use these examples to see where the simple answer often needs a second look.',
    }


def _guide_focus_cards(item: dict, family: dict) -> list[tuple[str, str]]:
    mode = _guide_mode(item)
    if family["slug"] == "flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn room size and pack coverage into a safer flooring order once waste, spare packs, and room shape matter more than the neat area alone."),
            ("Watch most", "Pack coverage, board direction, hall links, and the choice to keep matching spare stock usually move the final flooring order most."),
            ("Best next move", "Check the room layout and linked extras first, then compare pack rounding, underlay, and trim decisions before you buy."),
        ]
    if family["slug"] == "laminate-flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn laminate room area into a safer pack order once doorway cuts, spare boards, and same-batch buying matter more than the neat rectangle."),
            ("Watch most", "Pack coverage, room shape, visible cut-heavy edges, and the decision to keep spare laminate boards usually move the final order most."),
            ("Best next move", "Check doorway cuts, hall links, and underlay needs first, then compare whether one extra pack is safer than a top-up order later."),
        ]
    if family["slug"] == "hardcore-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn base dimensions and compacted depth into a safer hardcore order once tonnes, bulk bags, and loose delivery start to matter more than the neat footprint."),
            ("Watch most", "Compacted depth, density, uneven formation, and delivery format usually move the final hardcore order most."),
            ("Best next move", "Check the compacted depth first, then compare whether bulk bags or loose tonnes make more sense for the site access and size of the job."),
        ]
    if family["slug"] == "sub-base-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn the paved footprint and compacted layer depth into a safer sub-base order before the merchant quantity is locked in."),
            ("Watch most", "Compacted depth, density, edge thickening, and formation corrections usually move the final sub-base order most."),
            ("Best next move", "Pressure-test the compacted build-up first, then compare whether MOT Type 1, hardcore, bulk bags, or loose tonnes suit the job best."),
        ]
    if family["slug"] == "mot-type-1-calculator":
        return [
            ("When this guide helps", "Turn the driveway or patio footprint and compacted sub-base depth into a safer Type 1 order before the merchant quantity is locked in."),
            ("Watch most", "Compacted depth, density, edge thickening, and level corrections usually move the final Type 1 order most."),
            ("Best next move", "Pressure-test the compacted build-up first, then compare whether Type 1, hardcore, bulk bags, or loose tonnes suit the job and access best."),
        ]
    if family["slug"] == "drainage-pipe-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn the full trench run into a safer drainage pipe order once stock lengths, fittings, and spare pieces matter more than the neat line on the plan."),
            ("Watch most", "Stock length, fitting count, chamber entries, and offcuts usually move the final pipe order more than people expect."),
            ("Best next move", "Measure the full run and branch points first, then compare stock lengths, fittings, and whether one spare pipe length is worth carrying."),
        ]
    if family["slug"] == "french-drain-gravel-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn trench geometry into a safer washed-gravel order once widened sections, outlets, and delivery format matter more than the neat rectangle."),
            ("Watch most", "Trench width, gravel depth, outlet details, and whether the gravel is being bought in bags, bulk bags, or loose tonnes usually move the result most."),
            ("Best next move", "Pressure-test the trench envelope first, then compare whether bulk bags or loose tonnes suit the access, storage, and unloading plan best."),
        ]
    if family["slug"] == "geotextile-membrane-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn covered area into a safer membrane order once overlaps, roll width, and awkward edges matter more than the neat rectangle."),
            ("Watch most", "Overlap allowance, roll coverage after trimming, curves, and trench edge detail usually move the membrane order most."),
            ("Best next move", "Check the effective roll coverage after overlaps first, then compare whether the selected membrane grade still suits the job."),
        ]
    if family["slug"] == "coving-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn ceiling perimeter into a safer coving order once corners, mitres, and the real piece length start to matter more than the clean room shape."),
            ("Watch most", "Corner count, chimney breasts, bay returns, and whether the profile comes in 2m or 3m lengths usually move the final order most."),
            ("Best next move", "Measure each ceiling run separately, count the corners, and compare whether longer lengths reduce joins enough to justify the higher piece price."),
        ]
    if family["slug"] == "skirting-board-calculator" and mode in {"quantity", "waste"}:
        return [
            ("When this guide helps", "Turn room perimeter into a safer skirting order once doorway deductions, board length, and visible joints matter more than the first wall measurement."),
            ("Watch most", "Door openings, alcoves, corners, long visible walls, and whether 3m or 4.2m boards fit the room best usually move the order most."),
            ("Best next move", "Measure each wall separately, subtract only the openings that definitely need no skirting, then place the longest boards on the most visible walls before ordering."),
        ]
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
        if family.get('formula') == 'volume':
            return [
                ('When this guide helps', 'Turn trench, base, or fill dimensions into a safer order quantity for cubic metres, tonnes, bags, bulk bags, or loose supply.'),
                ('Watch most', 'Installed depth, density, widened sections, and the real buying route usually move the final order more than people expect.'),
                ('Best next move', 'Run the calculator, then compare whether bagged supply, bulk bags, or a tonne-based delivery makes the most sense for the site.'),
            ]
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
    if family["slug"] == "flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Exact pack count vs safer spare", "A neat pack total can look efficient, but one extra same-batch pack is often cheaper than a shortfall or a repair mismatch later."),
            ("Cheaper pack vs better coverage", "A lower sticker price can still lose once the real pack coverage, wear layer, and linked extras are compared properly."),
            ("Clean room maths vs awkward layout", "Straight area maths is useful, but hall links, hearths, bays, and thresholds often justify a more cautious buying total."),
        ]
    if family["slug"] == "laminate-flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Lower pack price vs safer spare", "The cheaper laminate route can still lose once spare-board matching and later repair risk are taken seriously."),
            ("Tighter waste vs easier fitting", "A lean waste allowance can look efficient, but awkward cuts and visible room edges often justify a more conservative pack total."),
            ("Laminate route vs vinyl route", "Laminate can look cheaper on paper until underlay, moisture risk, and long-term replacement flexibility are compared on the same basis."),
        ]
    if family["slug"] == "hardcore-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Bulk bag route vs loose route", "The cheapest unit price is not always the best route once site access, unloading, spreading effort, and spoil handling are taken seriously."),
            ("Exact depth vs safer overage", "A neat design depth is useful, but uneven formation and compaction can justify a modest spare on many groundwork jobs."),
            ("Recycled route vs graded route", "Lower-cost recycled hardcore can still change handling, compaction, and how the next layer behaves if the grade differs from the plan."),
        ]
    if family["slug"] == "sub-base-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Type 1 route vs general fill route", "A cheaper fill layer is not always the right choice once load, compaction, and the final paved surface are taken seriously."),
            ("Bulk bag route vs loose route", "Bulk bags can simplify domestic access, while loose tonnes can make more sense once the footprint grows and spreading is straightforward."),
            ("Tight maths vs corrected formation", "Straight footprint maths is useful, but weak spots and level corrections often justify a more conservative order."),
        ]
    if family["slug"] == "mot-type-1-calculator":
        return [
            ("Bulk bag route vs loose tonnes", "Bulk bags can suit many domestic jobs, but larger drives often look better value once loose delivery and spreading access are compared properly."),
            ("Neat footprint vs real base build-up", "A clean footprint can still understate the true Type 1 order if edge thickening, turning areas, or weak spots need extra depth."),
            ("Type 1 route vs deeper fill route", "A named sub-base layer only solves part of the build-up if deeper fill, hardcore, or membrane separation still need separate quantities."),
        ]
    if family["slug"] == "drainage-pipe-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Tight stock use vs safer spare", "The lowest piece count can look efficient, but one spare pipe length is often cheaper than a damaged piece or delayed top-up order."),
            ("Straight run vs fitting-heavy run", "A neat straight-run total can understate the real order once bends, branches, and chamber entries are priced honestly."),
            ("Pipe order vs full trench order", "Pipe length is only one part of the drainage build-up once bedding, gravel surround, and membrane are checked properly."),
        ]
    if family["slug"] == "french-drain-gravel-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Bulk bag route vs loose tonnes", "Bulk bags can suit smaller gardens and tighter access, but longer drains often look better value once loose-tonne delivery is priced properly."),
            ("Washed gravel only vs full trench build-up", "A gravel quantity can look complete on paper while pipe bedding, membrane wrap, and reinstatement materials still sit outside the order."),
            ("Tight trench maths vs safer overage", "Straight trench geometry is useful, but outlets, corners, and overbreak often justify a more conservative gravel order."),
        ]
    if family["slug"] == "geotextile-membrane-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Nominal roll coverage vs effective coverage", "The label coverage can look generous until overlaps, turn-ups, and trimming reduce the real installed area."),
            ("Lighter membrane vs tougher membrane", "A cheaper roll can still lose if puncture resistance, stability, or drainage performance are wrong for the job."),
            ("Exact roll count vs safer spare", "A spare roll can be easier to justify than a shortfall once the trench or driveway layout is more awkward than expected."),
        ]
    if family["slug"] == "coving-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Longer lengths vs easier handling", "Longer coving pieces can reduce joins, but they can also be harder to transport, cut cleanly, and fit safely in smaller rooms."),
            ("Lightweight profile vs sharper finish", "Lower-cost foam routes can fit quickly, while denser polymer or plaster profiles often change both waste and fitting time."),
            ("Exact count vs safer spare", "A neat piece count can look efficient, but one extra length is often cheaper than running short after a bad mitre or damaged end."),
        ]
    if family["slug"] == "skirting-board-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Longer boards vs less waste", "Longer skirting boards can reduce visible joins, but they may be harder to transport, carry upstairs, and fit in tighter spaces."),
            ("Lower board price vs better finish", "Cheaper board routes can still lose once extra prep, filling, sorting, or repainting are taken seriously."),
            ("Exact count vs future spare", "A spare board can be valuable for damage, last-minute changes, or matching repairs later, even when the paper total looks exact."),
        ]
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
    if mode == 'quantity' and family.get('formula') == 'volume':
        return [
            ('Bagged route vs bulk route', 'The cheapest unit price is not always the best buying route once access, unloading, storage, and labour are taken seriously.'),
            ('Base bedding vs full surround', 'Some estimates only cover the bedding under the pipe, while others quietly drift into the wider trench fill around the run.'),
            ('Tight maths vs safe overage', 'Straight trench geometry is useful, but fittings, chambers, and uneven excavation often justify a more conservative order.'),
        ]
    return [
        ('Lower waste vs easier install', 'The most efficient buying route is not always the easiest route to install or live with on site.'),
        ('Small overbuy vs shortfall risk', 'A modest spare allowance can be cheaper than a delayed job, second delivery, or hard-to-match top-up order.'),
        ('Clean maths vs supplier reality', 'Always compare the neat result against live pack sizes, stock lengths, and merchant terms before you treat it as final.'),
    ]


def _guide_example_cards(item: dict, family: dict) -> list[tuple[str, str]]:
    mode = _guide_mode(item)
    if family["slug"] == "flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Simple bedroom or lounge", "Straight rooms usually give the cleanest flooring pack estimate, especially if the board direction and pack coverage are already clear."),
            ("Hall link or awkward edges", "Doorways, hall links, bays, and hearth details can create more cut loss and spare-pack pressure than the neat area suggests."),
            ("Linked buying check", "Underlay, trims, thresholds, and skirting adjustments can matter just as much as the visible pack total on the first pass."),
        ]
    if family["slug"] == "laminate-flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Straight rectangular room", "Simple bedrooms and lounges usually behave closest to the base laminate waste allowance."),
            ("Room with alcoves or linked spaces", "Hall links, alcoves, and several doorway cuts can push laminate waste and spare-board planning up quickly."),
            ("Future repair check", "A same-batch spare pack can be easier to justify than trying to match laminate later after the product line changes."),
        ]
    if family["slug"] == "hardcore-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Small patio or shed base", "Simple rectangular bases usually give the cleanest hardcore estimate, but the compacted depth still needs checking against the real formation."),
            ("Soft spot or uneven base", "One low patch or weak section can use more hardcore than the neat rectangle suggests once the base is levelled properly."),
            ("Delivery check", "Compare bulk bags, loose tonnes, and unloading effort before the order feels fixed, especially on smaller domestic sites."),
        ]
    if family["slug"] == "sub-base-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Simple patio or path", "Straight footprints usually give the cleanest sub-base estimate, but the compacted depth and edge detail still need checking."),
            ("Driveway or heavy-use base", "Larger, deeper builds can move quickly once the footprint, compaction, and chosen grade are pressure-tested together."),
            ("Build-up check", "Sub-base often sits alongside membrane, bedding sand, and edging, so the base quantity is rarely the only material decision in play."),
        ]
    if family["slug"] == "mot-type-1-calculator":
        return [
            ("Simple driveway or patio base", "Straight footprints usually give the cleanest Type 1 estimate, but the compacted depth and edge build-up still need checking."),
            ("Weak spots or edge thickening", "Low patches, turning zones, and edges can quickly add more Type 1 than the neat footprint suggests."),
            ("Delivery route check", "Comparing bulk bags, loose tonnes, and access is often the step that turns the first estimate into a realistic order."),
        ]
    if family["slug"] == "drainage-pipe-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Straight trench run", "A clean run gives the best starting estimate, but even simple drainage work still needs a decision on stock length, bends, and one modest spare."),
            ("Branches or chamber entries", "Junctions, bends, and chamber connections can use more pipe and more awkward offcuts than the neat run length suggests."),
            ("Linked trench-material check", "Pipe length is only one part of the order once bedding, gravel surround, and membrane are checked on the same trench run."),
        ]
    if family["slug"] == "french-drain-gravel-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Straight trench run", "A clean run gives the best starting estimate, but even simple french drains still need a decision on trench width, gravel depth, and outlet detail."),
            ("Corners, outlets, or soakaway links", "Corners, turns, and outlet ties can widen the trench and use more gravel than the neat straight run suggests."),
            ("Delivery check", "Compare bags, bulk bags, and loose supply against access, storage, and whether a small spare is safer than a second delivery."),
        ]
    if family["slug"] == "geotextile-membrane-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Simple rectangular area", "Straight rectangles usually behave closest to the base overlap allowance, especially if the roll width suits the layout well."),
            ("Trench, curve, or stepped level", "Curves, trench edges, and stepped ground can create more trimming and overlap waste than the neat area suggests."),
            ("Coverage check", "Use the effective roll coverage after overlaps rather than the label headline before you finalise the roll count."),
        ]
    if family["slug"] == "coving-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Simple square room", "Straight rooms usually give the cleanest coving count, but they still need enough waste for each mitre and the final short return."),
            ("Bay or chimney breast", "Extra corners and short sections can push the number of cuts and damaged ends up much faster than the perimeter alone suggests."),
            ("Accessory check", "Adhesive, filler, caulk, and any preformed corners can be easier to miss than the main coving lengths."),
        ]
    if family["slug"] == "skirting-board-calculator" and mode in {"quantity", "waste"}:
        return [
            ("Simple bedroom or box room", "Straight walls and one doorway usually give the cleanest skirting estimate, especially if the board length fits the main walls well."),
            ("Room with alcoves or several openings", "Extra corners, returns, and doorway changes can make the real board plan quite different from the neat room perimeter."),
            ("Accessory check", "Adhesive, pins, filler, caulk, and matching corner blocks can all sit outside the first board count if they are not checked early."),
        ]
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
        if family.get('formula') == 'volume':
            return [
                ('Straight trench run', 'A clean run gives the best starting estimate, but even simple drainage work still needs a decision on width, depth, and waste.'),
                ('Fittings and widened sections', 'Junctions, chambers, and bends can widen the trench and use more bedding or gravel surround than the neat run length suggests.'),
                ('Delivery check', 'Compare bags, bulk bags, and loose supply against access, storage, and whether a small spare is safer than a second delivery.'),
            ]
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
    if family["slug"] == "flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Flooring Calculator to pressure-test pack coverage, waste, spare packs, and the linked underlay or trim decisions before you buy.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Room shape, pack coverage, board direction, hall links, and whether you keep same-batch spare stock usually move the final flooring order most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Whole-pack rounding and one safer spare pack are often cheaper than a delayed top-up order or a mismatch later.'},
        ]
    if family["slug"] == "laminate-flooring-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Laminate Flooring Calculator to pressure-test pack coverage, waste, spare-board thinking, and the linked underlay decisions before you order.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Pack coverage, room shape, doorway cuts, and whether you keep same-batch spare laminate boards usually move the final order most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Laminate jobs often benefit from a safer whole-pack total, especially where future repair matching matters.'},
        ]
    if family["slug"] == "hardcore-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Hardcore Calculator to pressure-test the base depth, density, and whether bulk bags or loose tonnes suit the site best.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Compacted depth, density, uneven formation, and delivery format usually move the final hardcore order most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Compaction, level corrections, and merchant minimums often justify a modest overage rather than landing exactly on the paper total.'},
        ]
    if family["slug"] == "sub-base-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Sub-Base Calculator to pressure-test the compacted build-up, density, and merchant delivery route before you order.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Compacted depth, density, formation corrections, and whether the supplier prices by bulk bag or loose tonne usually move the result most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Weak spots, edge thickening, and delivery minimums can justify a modest spare rather than landing exactly on the theoretical total.'},
        ]
    if family["slug"] == "mot-type-1-calculator":
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the MOT Type 1 Calculator to pressure-test the compacted build-up, edge detail, and merchant delivery route before you order.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Compacted depth, density, edge thickening, and whether the supplier prices by bulk bag or loose tonne usually move the result most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Weak spots, compaction, and delivery minimums can justify a modest spare rather than landing exactly on the paper total.'},
        ]
    if family["slug"] == "drainage-pipe-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Drainage Pipe Calculator to pressure-test the full run, stock length, fitting count, and whether one spare pipe length is worth carrying.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Stock length, fitting count, chamber entries, and offcuts usually move the final drainage pipe order more than people expect.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. One spare pipe length is often cheaper than a damaged piece, a missed final connection, or a delayed top-up order.'},
        ]
    if family["slug"] == "french-drain-gravel-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the French Drain Gravel Calculator to pressure-test trench width, gravel depth, outlet detail, and the real buying format before you place an order.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Trench width, gravel depth, widened sections, and whether the material is being bought in bags, bulk bags, or loose tonnes usually move the result most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Outlets, corners, overbreak, and delivery minimums often justify a modest overage rather than landing exactly on the theoretical trench volume.'},
        ]
    if family["slug"] == "geotextile-membrane-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Geotextile Membrane Calculator to pressure-test overlap waste, effective roll coverage, and whether the selected grade fits the job.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Overlap allowance, effective roll coverage, awkward edges, and the membrane grade usually move the final roll count most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Overlaps, trimming, and trench details can use more membrane than the neat covered area suggests, so a spare roll is often safer.'},
        ]
    if family["slug"] == "coving-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Coving Calculator to pressure-test the ceiling run, piece length, corner count, and how much spare the profile is likely to need.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Corner count, bay returns, piece length, and how fragile or ornate the coving profile is usually move the final order most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Coving waste often shows up in bad mitres, damaged ends, and awkward short returns rather than in the neat ceiling perimeter alone.'},
        ]
    if family["slug"] == "skirting-board-calculator" and mode in {"quantity", "waste"}:
        return [
            {'q': f'How should I use {subject}?', 'a': 'Use it with the Skirting Board Calculator to pressure-test doorway deductions, board length, visible joints, and the spare allowance before you buy.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Door openings, alcoves, corner count, board length, and the need to keep the longest boards on the most visible walls usually move the order most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. A spare board is often cheaper than a delay, a bad colour match later, or a visible wall that runs short after cutting.'},
        ]
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
    if mode == 'quantity' and family.get('formula') == 'volume':
        return [
            {'q': f'How should I use {subject}?', 'a': f'Use it with the {family["name"]} to pressure-test trench width, depth, density, and the real buying format before you place an order.'},
            {'q': f'What usually changes the {subject} answer most?', 'a': 'Installed depth, density, widened sections, and whether the material is being bought in bags, bulk bags, or loose tonnes usually move the result most.'},
            {'q': 'Should I round up the result?', 'a': 'Usually yes. Chambers, fittings, overbreak, and delivery minimums often justify a modest overage rather than landing exactly on the theoretical trench volume.'},
        ]
    return [
        {'q': f'How should I use {subject}?', 'a': f'Use it with the {family["name"]} as a buying and planning sense-check, then confirm the final order against live supplier information and the site conditions.'},
        {'q': f'What usually changes the {subject} answer most?', 'a': 'Coverage or stock assumptions, waste, awkward cuts, and whole-unit rounding usually move the final order more than people expect.'},
        {'q': 'Should I round up the result?', 'a': 'Usually yes. A small spare allowance is often cheaper than a shortfall, a second delivery, or a delayed job.'},
    ]


def _guide_related_cards(family: dict, current_slug: str) -> str:
    related_pool = _dedupe_slug_items(family['intent_pages'] + family['guide_pages'])
    current = next(
        (entry for entry in related_pool if entry['slug'] == current_slug),
        None,
    )
    role = _guide_role(current) if current else 'general'
    related_items = [
        entry for entry in related_pool if entry['slug'] != current_slug
    ]
    if role == 'measurement':
        related_items = sorted(
            related_items,
            key=lambda entry: (0 if _guide_role(entry) == 'buying' else 1, entry['title']),
        )
        title = 'Next buying guide to open'
        intro = 'Once the measurement looks right, use the buying guide to pressure-test pack sizes, spare stock, and the real ordering decision.'
    elif role == 'buying':
        related_items = sorted(
            related_items,
            key=lambda entry: (0 if _guide_role(entry) == 'measurement' else 1, entry['title']),
        )
        title = 'If you want to pressure-test the maths'
        intro = 'Open the paired measurement guide when you want to check the core area, volume, or run before you change the buying decision.'
    else:
        related_items = sorted(related_items, key=lambda entry: entry['title'])
        title = 'Related decision pages'
        intro = 'Use these pages to pressure-test the next buying, waste, or cost question that usually follows the first estimate.'
    related_items = related_items[:3]
    if not related_items:
        return ''
    cards = ''.join(
        f'<article class="tool-card"><h3><a href="/guides/{escape(entry["slug"])}/">{escape(entry["title"])}</a></h3><p>{escape(entry["description"])}</p></article>'
        for entry in related_items
    )
    return (
        f'<section class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(intro)}</p></section>'
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
    elif family["slug"] == "flooring-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the room dimensions, chosen flooring route, pack coverage, and the waste allowance you want to price against.',
            'Check whether underlay, trims, thresholds, and any skirting or door-clearance work need their own quantity or cost line.',
            'Decide whether one same-batch spare pack is worth carrying before the order is treated as final.',
        ]
    elif family["slug"] == "laminate-flooring-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the room shape, laminate pack coverage, waste allowance, and whether you want same-batch spare boards included.',
            'Check doorways, hall links, bays, and visible cut-heavy edges before trusting the neat room area alone.',
            'Pressure-test underlay, trims, thresholds, and moisture-control layers before you finalise the laminate order.',
        ]
    elif family["slug"] == "hardcore-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the base dimensions, compacted depth, density assumption, and whether the supplier prices by bag, bulk bag, or loose tonne.',
            'Check whether the formation has low spots, level corrections, or membrane layers that change the real hardcore quantity.',
            'Pressure-test delivery access, unloading effort, and whether a modest spare is safer than a mid-job shortfall.',
        ]
    elif family["slug"] == "sub-base-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the footprint, compacted sub-base depth, and the actual base material or grade being specified.',
            'Check whether soft spots, edge thickening, or level corrections change the neat rectangular volume.',
            'Compare bulk bags, loose tonnes, and whether membrane or bedding layers still need separate quantity checks.',
        ]
    elif family["slug"] == "mot-type-1-calculator":
        items = [
            'Confirm the footprint, compacted Type 1 depth, and whether the design needs edge thickening, turning areas, or level correction.',
            'Check the actual Type 1 grade, density assumption, and whether the supplier prices by bulk bag or loose tonne.',
            'Compare delivery access, unloading, and whether membrane, bedding, or nearby trench layers still need separate checks.',
        ]
    elif family["slug"] == "drainage-pipe-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the full pipe run, stock length, pipe diameter, and whether bends, branches, or chambers have been counted properly.',
            'Check whether short offcuts are genuinely reusable before trusting the neat piece count alone.',
            'Pressure-test bedding, gravel surround, membrane, and fitting counts alongside the pipe-length order so the trench build-up stays complete.',
        ]
    elif family["slug"] == "french-drain-gravel-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the trench width, gravel depth, outlet detail, and whether the quantity covers only the washed gravel envelope or the wider trench build-up.',
            'Check the real density, bag size, bulk bag size, or tonne pricing against the drainage aggregate your supplier actually sells.',
            'Pressure-test delivery access, unloading effort, membrane wrap, and whether a modest overage is safer than a shortfall on site.',
        ]
    elif family["slug"] == "geotextile-membrane-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the effective roll coverage after overlaps, the membrane grade, and whether the roll width suits the layout.',
            'Check edges, turn-ups, trench details, and awkward cuts before trusting the neat covered area alone.',
            'Pressure-test whether the membrane order also needs pins, tape, and linked aggregate quantities above or below it.',
        ]
    elif family["slug"] == "coving-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the real coving piece length, profile material, and whether corners or adhesives are sold separately.',
            'Count internal and external corners, bay returns, chimney breasts, and any short sections that can increase mitre waste.',
            'Decide whether one spare length is worth carrying for breakage, damage, or future repair matching before you place the order.',
        ]
    elif family["slug"] == "skirting-board-calculator" and mode in {"quantity", "waste"}:
        items = [
            'Confirm the real board length, profile, finish route, and whether doorway deductions have been handled consistently.',
            'Check corners, returns, visible joint positions, and whether the longest walls need full boards rather than short patched sections.',
            'Pressure-test adhesive, pins, filler, caulk, and whether one spare board is worth having for damage or later repairs.',
        ]
    elif family.get('formula') == 'volume':
        items = [
            'Confirm whether the quantity covers the base layer only, the full trench surround, or the wider fill around fittings and chambers.',
            'Check the real density, bag size, bulk bag size, or tonne pricing against the product your supplier actually sells.',
            'Pressure-test delivery access, unloading effort, and whether a small overage is safer than a shortfall on site.',
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
        related = _dedupe_slug_items(family['intent_pages'] + family['guide_pages'])
        for item in related:
            path = f"/guides/{item['slug']}/"
            crumbs = [('Home', '/'), ('Guides', '/guides/'), (item['title'], path)]
            focus_cards = _guide_focus_cards(item, family)
            support_cards = _guide_support_cards(item, family)
            tradeoff_cards = _guide_tradeoff_cards(item, family)
            example_cards = _guide_example_cards(item, family)
            faqs = _guide_faqs(item, family)
            related_cards = _guide_related_cards(family, item['slug'])
            description = _guide_description(item, family)
            section_copy = _guide_section_copy(item)

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
                f'{_guide_use_calculator_panel(item, family)}'
                f'{render_section_cards(support_cards)}'
                f'<section class="content-card prose-card"><h2>{escape(section_copy["tradeoff_title"])}</h2><p>{escape(section_copy["tradeoff_intro"])}</p></section>'
                f'<section class="stack-grid">{tradeoff_html}</section>'
                f'<section class="content-card prose-card"><h2>{escape(section_copy["example_title"])}</h2><p>{escape(section_copy["example_intro"])}</p></section>'
                f'<section class="stack-grid">{example_html}</section>'
                f'{_guide_checklist_panel(item, family)}'
                f'{related_cards}'
                f'<section class="content-card prose-card"><h2>Next step links</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} {escape(PROJECT_HUB_LABEL.lower())}</a> or go straight to the <a href="/calculators/{escape(family["slug"])}/">{escape(family["name"])}</a>.</p></section>'
                f'{render_quote_prep_panel(family, "guide")}'
                f'<section class="stack-grid">{faq_html}</section></div>'
            )
            html = render_layout(
                title=item.get('meta_title', f"{item['title']} | {SITE['name']}"),
                description=description,
                path=path,
                content=content,
                schema=[render_breadcrumb_schema(crumbs), render_faq_schema(faqs)],
                page_type='guide',
            )
            pages.append((path, html))
    return pages


# ---------- Conversion panels ----------

def render_quote_prep_panel(family: dict, context: str, panel_data: dict | None = None) -> str:
    panel_data = panel_data or {}
    target_family = family
    if context == "cluster" and panel_data.get("quote_primary_slug"):
        target_family = family_lookup().get(panel_data["quote_primary_slug"], family)
    calculator_path = f'/calculators/{target_family["slug"]}/'
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
    checklist_items = [
        "Confirm what the quote should include: materials only, labour only, or both.",
        "State access, finish level, timing, and any unknowns clearly.",
        "Ask each supplier or installer to price the same scope and exclusions.",
    ]
    label = panel_data.get("quote_panel_title", label)
    intro = panel_data.get("quote_panel_intro", intro)
    checklist_items = panel_data.get("quote_panel_items", checklist_items)
    actions = []
    if context != "calculator":
        actions.append(f'<a class="btn btn-primary" href="{escape(calculator_path)}" data-conversion-link="calculator">Open {escape(target_family["name"])}</a>')
    actions.append('<a class="btn" href="/quote-checklist/" data-conversion-link="quote-checklist">Open quote checklist</a>')
    actions.append('<a class="btn" href="/contact/" data-conversion-link="contact">Contact BuildCostLab</a>')
    items_html = "".join(f'<li>{escape(item)}</li>' for item in checklist_items)
    panel_class = "conversion-panel conversion-panel-prominent" if context == "cluster" else "conversion-panel"
    return (
        f'<section class="{panel_class}">'
        '<div class="section-head">'
        f'<h2>{escape(label)}</h2>'
        f'<p>{escape(intro)}</p>'
        '</div>'
        f'<ul class="conversion-list">{items_html}</ul>'
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
    guide_items = _dedupe_slug_items(family["intent_pages"] + family["guide_pages"])
    faq_html = "".join(
        f'<article class="content-card prose-card"><h2>{escape(item["q"])}</h2><p>{escape(item["a"])}</p></article>'
        for item in family["faqs"]
    )
    next_links = "".join(
        f'<a class="mini-tool-card" href="/guides/{escape(item["slug"])}/">{escape(item["title"])}</a>'
        for item in guide_items
    )
    next_step_section = ""
    if next_links:
        next_step_section = f'<section class="related-tools" id="next-guides"><div class="section-head"><h2>Next-step guides</h2><p>Use these guides to sense-check the estimate, avoid common mistakes, and choose the right buying format.</p></div><div class="mini-tool-grid">{next_links}</div></section>'
    scope_cards = render_section_cards(_calculator_scope_cards(family))
    methodology_cards = render_section_cards(_calculator_methodology_cards(family))
    driver_cards = render_section_cards(_calculator_driver_cards(family))
    worked_example = f'<section class="content-card prose-card"><h2>Worked example</h2><p>{escape(_calculator_worked_example_text(family))}</p></section>'
    return (
        f'{render_ad_slot(f"{key}-mid")}'
        '<section id="buying-checks" class="content-card prose-card section-anchor-card"><h2>Practical checks before you buy</h2><p>These notes are where BuildCostLab goes beyond a generic calculator result by surfacing the assumptions, buying traps, and next decisions that usually move the real order.</p></section>'
        f'{scope_cards}'
        f'{worked_example}'
        f'{methodology_cards}'
        f'{driver_cards}'
        f'{_calculator_checklist_panel(family)}'
        f'<section class="content-card prose-card"><h2>Explore this {escape(PROJECT_HUB_LABEL.lower())}</h2><p><a href="/clusters/{escape(family["cluster_slug"])}/">Open the full {escape(family["cluster_name"])} {escape(PROJECT_HUB_LABEL.lower())}</a> to move from quick estimate to deeper guidance.</p></section>'
        f'{_calculator_related_calculators(family)}'
        f'{next_step_section}'
        '<section id="faqs" class="content-card prose-card section-anchor-card"><h2>Quick answers</h2><p>These answers are designed to resolve the last practical buying questions people usually have after running the calculator.</p></section>'
        f'<section class="stack-grid">{faq_html}</section>'
    )


def render_calculator_page(*, slug: str, title: str, description: str, intro: str, form_html: str, result_html: str, script_name: str) -> str:
    family = family_lookup()[slug]
    normalized_description = description.strip()
    if len(normalized_description) < 90:
        normalized_description = f"{normalized_description.rstrip('.')} with practical quantity, waste, and rough cost outputs for planning."
    meta_title = family.get("meta_title", f"{title} | {SITE['name']}")
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
        f'{render_calculator_hero_badges(family.get("formula", ""))}</section>'
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
        title=meta_title,
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
    seen: set[str] = set()
    for family in get_all_calculators():
        for item in _dedupe_slug_items(family["guide_pages"]):
            if item["slug"] in seen:
                continue
            seen.add(item["slug"])
            records.append({
                "family": family,
                "slug": item["slug"],
                "title": item["title"],
                "description": item["description"],
            })
    return records


def build_compare_index() -> tuple[str, str]:
    compare_keywords = (" vs ", "-vs-", "versus", "cost per", "per m2", "costs")
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
        '<p class="hero-copy">Use these pages when you need to compare material routes, pressure-test a per-m2 rate, or make sure two buying options are being judged on the same assumptions.</p></section>'
        f'{render_ad_slot("compare-index-top")}'
        '<section class="content-card prose-card"><h2>How to use this section</h2><p>Start with the calculator if you need a fresh quantity first, then use these comparison pages to sense-check costs, buying formats, and option trade-offs before you request quotes.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section></div>'
    )
    return path, render_layout(
        title=f'Compare Materials and Costs | {SITE["name"]}',
        description='Browse BuildCostLab comparison guides for per-m2 rates, material trade-offs, and cost benchmarks.',
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

