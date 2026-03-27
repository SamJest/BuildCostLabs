from data.calculator_scale import ADDITIONAL_CALCULATORS
from data.publisher import CALCULATOR_FAMILIES


FORMULA_SUPPORT = {
    "coverage": {
        "assumptions": "Coverage-based calculators assume the material is bought by usable area per unit, then rounded to whole buying units after waste is added.",
        "mistakes": "The usual mistakes are using the wrong product coverage rate, ignoring trimming losses, and comparing pack prices without checking true covered area.",
        "use_case": "Best for sheets, rolls, packs, boards, and bagged products where the real buying decision is coverage per unit.",
        "estimate_tip": "Start with clean geometry, add realistic waste, then check the product sheet because quoted coverage can vary by substrate and install method.",
        "buyer_tip": "If the result is close to the next full unit, most buyers round up to avoid delays, especially where colour, batch, or finish matching matters.",
    },
    "volume": {
        "assumptions": "Volume calculators assume the job can be reduced to length, width, depth, and a practical density or buying-unit conversion.",
        "mistakes": "Depth mistakes are the biggest problem, followed by using the wrong density and forgetting that loose and compacted materials do not behave identically.",
        "use_case": "Best for aggregates, soils, screeds, and fill materials where the order usually starts with volume, then converts into tonnes, bags, or bulk units.",
        "estimate_tip": "Check whether the depth entered is the installed depth or the loose-delivered depth, because the difference can materially change the order.",
        "buyer_tip": "Bag and bulk pricing can diverge quickly once the quantity grows, so use the output to compare the real delivered buying route, not just a headline unit cost.",
    },
    "linear": {
        "assumptions": "Linear calculators assume materials are bought in stock lengths and the job can be reduced to a total run with a reasonable cut allowance.",
        "mistakes": "Common misses include forgetting joints, corners, mitres, end conditions, and the waste created when standard stock lengths do not divide neatly into the run.",
        "use_case": "Best for trim, drainage, roofline, pipework, and edging products where the real order is based on whole stock lengths.",
        "estimate_tip": "Measure the full run, add realistic waste for cuts and joints, then check whether fittings and corners need to be costed separately.",
        "buyer_tip": "A slightly higher stock-length overage is often cheaper than losing time to a short final piece or making an extra delivery run.",
    },
}

CLUSTER_OVERRIDES = {
    "soil-and-landscaping-estimating": {
        "cluster_intro": "Estimate topsoil, mulch, compost, and bark quantities with a focus on installed depth, delivery format, and whether the job is better served by bags or bulk supply.",
        "support": {
            "assumptions": "Landscaping fill calculators depend heavily on finished depth, whether the material settles after laying, and whether the supplier sells in loose volume, tonnes, or bagged units.",
            "mistakes": "The common misses are underestimating settled depth, ignoring irregular bed shapes, and forgetting that decorative coverage and soil-conditioning depth are not the same thing.",
            "use_case": "Best for beds, borders, levelling work, and decorative coverings where the buyer needs a practical delivered quantity rather than a neat geometric answer.",
            "estimate_tip": "Measure the finished spread area, decide the true installed depth, and then sense-check whether bagged delivery or loose bulk supply is more realistic for the quantity.",
            "buyer_tip": "On small domestic jobs, bags can be easier to handle; on larger jobs, the delivered loose option often gives a better effective price and fewer packaging headaches.",
            "market_note": "UK buyers often think in bulk bags and tonnes, while US buyers may lean more on cubic yards and bagged landscaping products, so keep the buying format in mind as well as the geometry.",
        },
        "guides_by_formula": {
            "volume": [
                {"slug_suffix": "depth-guide", "title": "{name} Depth Guide", "description": "See how installed depth changes the final buying quantity.", "headline": "Depth is the main reason landscaping orders swing", "intro": "A small change in depth can turn a manageable order into a shortfall or an expensive overbuy."},
                {"slug_suffix": "bags-vs-bulk-guide", "title": "{name} Bags vs Bulk Guide", "description": "Compare bagged and bulk buying routes for this material.", "headline": "Choose the buying format before the order feels locked in", "intro": "The best buying route depends on quantity, access, labour, and how much packaging or loose handling the site can tolerate."},
            ],
        },
    },
    "insulation-estimating": {
        "cluster_intro": "Estimate insulation boards, rolls, and acoustic products with pack coverage, thickness, fit losses, and whole-pack buying logic treated as first-order concerns.",
        "support": {
            "assumptions": "Insulation estimates usually depend on covered area, product thickness, and the fact that boards and rolls are bought to pack coverage, not to neat geometry alone.",
            "mistakes": "The biggest mistakes are confusing thermal thickness with coverage, ignoring cut loss around framing or rafters, and overlooking staggered joints or offcuts.",
            "use_case": "Best for early thermal upgrade planning, material comparisons, and checking how many packs or rolls a room, floor, roof, or partition is likely to need.",
            "estimate_tip": "Choose the exact product format first, then check the pack coverage and thickness because two seemingly similar insulation products can create different buying quantities.",
            "buyer_tip": "A spare pack is often worth having when cuts are awkward or when the same thickness may be needed for a later phase of the job.",
            "market_note": "Terminology differs between UK and US buyers, but the practical buying logic still comes down to coverage per pack, thickness, and cut loss.",
        },
        "guides_by_formula": {
            "coverage": [
                {"slug_suffix": "coverage-guide", "title": "{name} Coverage Guide", "description": "Understand how insulation pack or roll coverage turns into a real order quantity.", "headline": "Coverage numbers only help if the product format is clear", "intro": "Pack coverage is the bridge between room size and the real number of packs or rolls you need to buy."},
                {"slug_suffix": "waste-and-fit-guide", "title": "{name} Waste and Fit Guide", "description": "See when insulation waste should be low, standard, or higher.", "headline": "Cutting and fitting losses are where insulation orders go wrong", "intro": "Joists, studs, rafters, and awkward edges often push the real buying total above the clean area figure."},
            ],
        },
    },
    "plaster-and-render-estimating": {
        "cluster_intro": "Estimate skim plaster and render with more realistic attention to thickness, yield, suction, and how background condition changes the real bag count.",
        "support": {
            "assumptions": "Plaster and render estimates depend on product yield, finished thickness, and substrate condition more than many buyers expect at first glance.",
            "mistakes": "Common misses include ignoring suction on thirsty backgrounds, using the wrong thickness assumption, and forgetting that repair work and full coverage jobs behave very differently.",
            "use_case": "Best for walls and ceilings where the buyer wants to move from area into realistic bag quantities and rough spend before choosing the exact system.",
            "estimate_tip": "Confirm the intended thickness and substrate condition first, because those two assumptions change the bag count faster than the visible wall area alone suggests.",
            "buyer_tip": "If the background is rough or absorbent, a slightly more conservative order is usually safer than trying to land exactly on the theoretical coverage figure.",
            "market_note": "Product naming and bag formats vary between markets, but yield, thickness, suction, and waste are still the main levers in the estimate.",
        },
        "guides_by_formula": {
            "coverage": [
                {"slug_suffix": "coverage-guide", "title": "{name} Coverage Guide", "description": "Learn how yield and thickness change bag quantities for this finish.", "headline": "Yield is only meaningful when thickness is honest", "intro": "Published coverage figures usually assume a specific thickness and a cooperative substrate, so real jobs need a more grounded view."},
                {"slug_suffix": "substrate-and-waste-guide", "title": "{name} Substrate and Waste Guide", "description": "Understand how suction, uneven backgrounds, and waste alter the final quantity.", "headline": "Background condition can move the order more than the wall size", "intro": "A clean board surface and an uneven masonry wall do not consume finish in the same way, even when the area is identical."},
            ],
        },
    },
    "brick-and-block-estimating": {
        "cluster_intro": "Estimate bricks, blocks, and mortar with wall area, openings, waste, and whole-unit ordering treated as the core of the masonry buying decision.",
        "support": {
            "assumptions": "Masonry estimates depend on wall area, unit size, joint pattern, openings, and whether the buyer is ordering by piece count, pack, or pallet.",
            "mistakes": "The most common problems are forgetting openings, using the wrong unit coverage rate, and overlooking mortar, cuts, and breakage at corners or reveals.",
            "use_case": "Best for wall-building jobs where the goal is to move from area into a sensible piece count, waste margin, and supporting mortar logic.",
            "estimate_tip": "Check the actual brick or block size being priced, then confirm how much wall is lost to openings before trusting the final count.",
            "buyer_tip": "If the result is close to the next pack or pallet break, most buyers round up to protect against cuts, breakages, and unavoidable site losses.",
            "market_note": "Metric and imperial naming can differ, but the core estimate still depends on unit size, wall area, openings, and realistic waste.",
        },
        "guides_by_formula": {
            "coverage": [
                {"slug_suffix": "count-per-area-guide", "title": "{name} Count per Area Guide", "description": "Understand how wall area turns into a practical unit count.", "headline": "The count starts with area, but the buying logic does not end there", "intro": "Wall area is only the first step. Openings, unit size, and waste all affect what should actually be ordered."},
                {"slug_suffix": "waste-and-openings-guide", "title": "{name} Waste and Openings Guide", "description": "See how openings, cuts, and breakage affect the final masonry order.", "headline": "Waste and openings separate clean estimates from real orders", "intro": "Doors, windows, corners, and small returns can change the count enough to matter before the first pallet is ordered."},
            ],
            "volume": [
                {"slug_suffix": "yield-guide", "title": "{name} Yield Guide", "description": "Understand how joint size and wall type change mortar demand.", "headline": "Mortar yield depends on the wall as much as the mix", "intro": "The same volume of mortar behaves differently depending on joint thickness, unit type, and how much wastage the wall detail creates."},
                {"slug_suffix": "waste-guide", "title": "{name} Waste Guide", "description": "See how handling loss and wall details affect the final mortar quantity.", "headline": "Mortar waste is small until the wall detail says otherwise", "intro": "Joint style, weather, handling losses, and the speed of work can all move the final mortar requirement above the theoretical minimum."},
            ],
        },
    },
    "roofing-estimating": {
        "cluster_intro": "Estimate shingles, felt, and battens with overlaps, laps, pitch effects, and edge waste treated as real buying factors instead of afterthoughts.",
        "support": {
            "assumptions": "Roofing estimates rely on covered area, lap or overlap allowances, and the fact that roof shape and pitch often increase the real material take-off above a simple plan area.",
            "mistakes": "Common issues include ignoring overlap, failing to allow for cuts at edges and ridges, and treating every roof as if it behaves like a simple rectangle.",
            "use_case": "Best for sheds, garages, simple roofs, and early roofing material checks where the buyer needs a fast but practical order estimate.",
            "estimate_tip": "Check whether the product is sold by effective coverage after laps or by nominal pack size, because that changes the buying count immediately.",
            "buyer_tip": "Roofing jobs rarely reward under-ordering. A small overage is usually cheaper than the disruption caused by a short finish course or delayed extra delivery.",
            "market_note": "Terms vary between roofing systems and markets, but overlaps, pitch, edge waste, and actual covered area remain the critical estimate drivers.",
        },
        "guides_by_formula": {
            "coverage": [
                {"slug_suffix": "coverage-guide", "title": "{name} Coverage Guide", "description": "Understand how effective roof coverage changes the final order quantity.", "headline": "Nominal coverage and effective coverage are not the same thing", "intro": "The label on the pack is only useful once laps, overlaps, and real roof geometry are accounted for."},
                {"slug_suffix": "waste-and-overlap-guide", "title": "{name} Waste and Overlap Guide", "description": "See how edges, overlaps, and cuts affect roofing quantities.", "headline": "Overlap is not optional and waste is not random", "intro": "Edges, ridges, verge details, and overlap rules can quietly add more material than a flat-area estimate suggests."},
            ],
            "linear": [
                {"slug_suffix": "length-guide", "title": "{name} Length Guide", "description": "Understand how stock lengths and roof geometry change the final order.", "headline": "Stock length logic matters more than raw roof size", "intro": "Battens and similar roofing lengths are bought in stock sizes, so the cutting pattern affects the total as much as the roof dimensions do."},
                {"slug_suffix": "waste-and-joins-guide", "title": "{name} Waste and Joins Guide", "description": "See how joins, trimming, and roof detail affect length-based roofing materials.", "headline": "Joins and details quietly create the waste", "intro": "Valleys, edges, staggered joints, and stock-length joins often create more loss than the clean run length first suggests."},
            ],
        },
    },
}


def build_support(item):
    override = CLUSTER_OVERRIDES.get(item["cluster_slug"])
    if override:
        return override["support"]
    formula_support = FORMULA_SUPPORT[item["formula"]]
    material_label = item["name"].replace(" Calculator", "").lower()
    return {
        "assumptions": formula_support["assumptions"],
        "mistakes": formula_support["mistakes"],
        "use_case": f"{formula_support['use_case']} This one is tuned for {material_label} jobs.",
        "estimate_tip": formula_support["estimate_tip"],
        "buyer_tip": formula_support["buyer_tip"],
        "market_note": "UK and US buyers often use different unit language and pack conventions, but the geometry, waste, and whole-unit rounding logic are still the foundation.",
    }


def build_faqs(item):
    override = CLUSTER_OVERRIDES.get(item["cluster_slug"])
    if override:
        label = item["name"].lower()
        return [
            {"q": f"How do I use the {label}?", "a": f"Enter the job dimensions, choose a realistic waste setting, and use the {label} to get a planning quantity before checking product-specific coverage or pack rules."},
            {"q": f"What most affects the {label} result?", "a": override["support"]["mistakes"]},
            {"q": "Should I round the result up?", "a": override["support"]["buyer_tip"]},
        ]
    label = item["name"].lower()
    return [
        {"q": f"How do I use the {label}?", "a": f"Enter the job dimensions, choose a sensible waste setting, and use the {label} as a buying guide rather than an exact order."},
        {"q": f"What most affects the {label} result?", "a": "Usually the job dimensions, waste allowance, and the product coverage or stock-length assumption used to convert geometry into whole buying units."},
        {"q": "Should I round the result up?", "a": "Usually yes, because most materials are bought in whole units and small site losses are common."},
    ]


def build_guides(item):
    item_name = item["name"].replace(" Calculator", "")
    override = CLUSTER_OVERRIDES.get(item["cluster_slug"], {})
    templates = override.get("guides_by_formula", {}).get(item["formula"], [])
    return [
        {
            "slug": item["slug"].replace("-calculator", f"-{guide['slug_suffix']}"),
            "title": guide["title"].format(name=item_name),
            "description": f"{item_name}: {guide['description'][0].lower()}{guide['description'][1:]}",
            "headline": guide["headline"],
            "intro": guide["intro"],
        }
        for guide in templates
    ]


def get_cluster_intro(cluster_slug: str, fallback: str) -> str:
    override = CLUSTER_OVERRIDES.get(cluster_slug)
    if override:
        return override.get("cluster_intro", fallback)
    return fallback


def get_all_calculators():
    calculators = []
    calculators.extend(CALCULATOR_FAMILIES)
    for item in ADDITIONAL_CALCULATORS:
        calculators.append(
            {
                **item,
                "key": item["slug"].replace("-calculator", "").replace("-", "_"),
                "support": build_support(item),
                "faqs": build_faqs(item),
                "intent_pages": [],
                "guide_pages": build_guides(item),
            }
        )
    return calculators
