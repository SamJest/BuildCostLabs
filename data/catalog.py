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

GENERIC_INTENT_TEMPLATES = {
    "coverage": [
        {
            "slug_suffix": "calculator-by-area",
            "title": "{name} Calculator by Area",
            "description": "Estimate {name_lower} from the area to be covered and a realistic waste allowance.",
            "headline": "Use covered area to estimate {name_lower} more accurately",
            "intro": "If you already know the area, you can turn it into a practical buying quantity once coverage per unit and waste are clear.",
        },
        {
            "slug_suffix": "how-much-do-i-need",
            "title": "How Much {name} Do I Need?",
            "description": "Work out how much {name_lower} to buy before you order materials.",
            "headline": "Work out how much {name_lower} to buy before you order",
            "intro": "This page explains the main checks to make before turning a simple coverage figure into a real order quantity.",
        },
    ],
    "volume": [
        {
            "slug_suffix": "calculator-by-volume",
            "title": "{name} Calculator by Volume",
            "description": "Estimate {name_lower} from length, width, depth, and a realistic waste allowance.",
            "headline": "Use volume to estimate {name_lower} more confidently",
            "intro": "Volume-first estimating is usually the quickest route into a usable buying quantity for loose, bagged, or bulk materials.",
        },
        {
            "slug_suffix": "how-much-do-i-need",
            "title": "How Much {name} Do I Need?",
            "description": "Work out how much {name_lower} to order for your job without relying on rough guesswork.",
            "headline": "Turn the job dimensions into a sensible {name_lower} order",
            "intro": "A rough length, width, and depth can usually be turned into a much safer material order once waste and buying format are taken into account.",
        },
    ],
    "linear": [
        {
            "slug_suffix": "length-calculator",
            "title": "{name} Length Calculator",
            "description": "Estimate {name_lower} from total run length, stock size, and a practical cut allowance.",
            "headline": "Use total run length to estimate {name_lower} with less waste",
            "intro": "Length-based materials are usually bought in stock sizes, so the clean run length is only the starting point.",
        },
        {
            "slug_suffix": "how-much-do-i-need",
            "title": "How Much {name} Do I Need?",
            "description": "Work out how much {name_lower} to buy for your run, perimeter, or edge detail.",
            "headline": "Work out how much {name_lower} to buy before you order stock lengths",
            "intro": "A good buying number for length-based materials depends on the run, the stock size, and how much cutting waste the job will create.",
        },
    ],
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

CLUSTER_HUB_CONTENT = {
    "tile-estimating": {
        "start_here_title": "Start with the right tiling question",
        "start_here_intro": "Most tiling jobs begin with one of three questions: how many tiles, how much adhesive, and how much grout. Start with the part of the job you are buying first, then use the guides to check waste and box or bag rounding.",
        "featured_slugs": ["tile-calculator", "tile-adhesive-calculator", "tile-grout-calculator"],
        "question_heading": "Popular tiling questions",
        "question_intro": "Use these pages when you already know the room or wall area and want a quicker route into tile, adhesive, or grout quantities.",
        "guide_heading": "Tiling guides and buying checks",
        "guide_intro": "These guides help with waste, box counts, and the practical differences between common tiling products.",
        "notes": [
            ("What changes a tile order most", "Tile size, layout pattern, breakage risk, and whether the job needs separate adhesive and grout calculations are usually the biggest drivers of the final order."),
            ("When to increase waste", "Increase the waste allowance for diagonal layouts, feature borders, awkward cuts, or jobs where future matching tiles may be difficult."),
            ("Before you order", "Check tile box coverage, adhesive coverage, grout yield, and whether trims, movement joints, and backer boards need to be bought separately."),
        ],
    },
    "aggregate-and-base-estimating": {
        "start_here_title": "Choose the aggregate or base material first",
        "start_here_intro": "This cluster works best once you know whether the job needs bedding sand, compacted sub-base, MOT Type 1, ballast, or another bulk material. The calculators here help turn trench, patio, path, and driveway dimensions into a real delivered quantity.",
        "featured_slugs": ["mot-type-1-calculator", "sub-base-calculator", "sharp-sand-calculator", "ballast-calculator"],
        "question_heading": "Quick quantity pages",
        "question_intro": "Start here if you mainly want to know how much bulk material to order from the dimensions of the job.",
        "guide_heading": "Guides for delivery and depth decisions",
        "guide_intro": "These pages help with the parts of aggregate ordering that usually cause mistakes: depth, compaction, and whether bags or bulk delivery make more sense.",
        "notes": [
            ("What changes these estimates most", "Installed depth, compaction, density, and the difference between finished depth and loose-delivered depth can move the order significantly."),
            ("Why buying format matters", "A small domestic job may be easier with bags or mini bulk bags, while a larger driveway or patio base can look very different once loose delivery is priced."),
            ("Before you order", "Check whether the supplier sells by tonne, cubic metre, or bag size, and confirm if the quoted quantity is loose, compacted, or effective coverage."),
        ],
    },
    "drainage-estimating": {
        "start_here_title": "Plan the trench and the material together",
        "start_here_intro": "Drainage work usually needs more than one material at once. You may need pipe length, trench gravel, bedding material, and membrane coverage, so this hub is designed to help you move through those linked decisions without missing a part of the order.",
        "featured_slugs": ["drainage-pipe-calculator", "french-drain-gravel-calculator", "pipe-bedding-calculator", "geotextile-membrane-calculator"],
        "question_heading": "Common drainage quantity checks",
        "question_intro": "Use these pages to estimate the main trench materials before you compare fittings, pipe sizes, and supplier pack options.",
        "guide_heading": "Drainage planning guides",
        "guide_intro": "These guides support the main calculators by helping with coverage, trench fill, and how much material is usually tied to each part of the run.",
        "notes": [
            ("What changes drainage quantities most", "Trench width, bedding depth, gravel surround, and the total run length are usually more important than the pipe diameter alone."),
            ("Where people under-order", "Pipe runs are often estimated without enough bedding or gravel surround, especially where trench width grows around fittings or inspection points."),
            ("Before you order", "Check whether fittings, chambers, connectors, and fabric overlaps need to be costed separately from the core trench materials."),
        ],
    },
    "decorating-estimating": {
        "start_here_title": "Pick the finish you are actually buying",
        "start_here_intro": "Decorating estimates change depending on whether you are buying paint, wallpaper, or primer. Start with the finish layer that matches the job, then use the related pages to check waste, coverage, and how many tins or rolls you are likely to need.",
        "featured_slugs": ["paint-calculator", "primer-calculator", "wallpaper-calculator"],
        "question_heading": "Popular decorating questions",
        "question_intro": "These pages are useful when you already know the walls, ceilings, or surface area and want a quick buying number.",
        "guide_heading": "Coverage and waste guides",
        "guide_intro": "The decorating guides help explain when a simple area figure needs a more cautious coverage or waste assumption.",
        "notes": [
            ("What changes these estimates most", "Coat count, surface texture, repeat patterns, and how much cut-in or trimming the job involves are the biggest reasons decorating orders change."),
            ("When a quick estimate is enough", "A straightforward repaint or simple wallpaper layout can usually be planned quickly, but textured walls and pattern matching need more caution."),
            ("Before you order", "Check product spread rates, roll yield, surface prep needs, and whether primer or sealer coats need to be bought separately from the finish coat."),
        ],
    },
    "garden-surface-estimating": {
        "start_here_title": "Match the surface to the way it is sold",
        "start_here_intro": "Garden-surface materials are sold in very different ways. Turf often comes by roll, seed by pack coverage, artificial grass by roll width, and membrane by roll area, so this cluster helps you start with the right buying format for the job.",
        "featured_slugs": ["turf-calculator", "grass-seed-calculator", "artificial-grass-calculator", "weed-membrane-calculator"],
        "question_heading": "Quick lawn and surface calculators",
        "question_intro": "Use these pages when you already know the lawn or surface area and want the quickest route into rolls, packs, or membrane coverage.",
        "guide_heading": "Surface prep and buying guides",
        "guide_intro": "These pages help explain which product format suits the job and where waste or extra prep materials often get missed.",
        "notes": [
            ("What changes these estimates most", "Surface area is the starting point, but overlaps, trimming, offcuts, and patching or edging waste can all push the real order higher."),
            ("When the buying format matters most", "Roll goods and seeded areas behave very differently on awkward shapes, narrow strips, and borders with lots of trimming."),
            ("Before you order", "Check roll sizes, pack coverage, overlaps, and whether topsoil, sub-base, or fixing accessories need to be ordered alongside the surface product itself."),
        ],
    },
    "roofline-estimating": {
        "start_here_title": "Break the roofline into the parts you are buying",
        "start_here_intro": "Roofline jobs usually involve several linked products rather than one single quantity. Use this cluster to split the job into fascia, soffit, guttering, and downpipes so each part can be measured and ordered in a more practical way.",
        "featured_slugs": ["fascia-calculator", "soffit-calculator", "gutter-calculator", "downpipe-calculator"],
        "question_heading": "Quick roofline quantity pages",
        "question_intro": "Use these pages when you already know the run lengths and want a fast route into boards, gutters, or downpipe quantities.",
        "guide_heading": "Roof edge and drainage guides",
        "guide_intro": "These pages help with joins, stock lengths, waste, and the parts of roofline work that often get underestimated on first pass.",
        "notes": [
            ("What changes a roofline order most", "Corners, joints, stop ends, outlets, and how the stock lengths break across the run usually matter as much as the total measured length."),
            ("Where people under-order", "It is common to count the straight runs but forget outlets, brackets, trims, and the extra pieces created by corners or changes in level."),
            ("Before you order", "Check stock lengths, fittings, corner pieces, and whether fixings or joint trims need to be bought separately from the main boards or gutters."),
        ],
    },
    "trim-and-joinery-estimating": {
        "start_here_title": "Start with the trim run you can actually measure",
        "start_here_intro": "Joinery trims are usually bought in stock lengths, so the clean perimeter or opening size is only the starting point. This cluster groups together the main room trims so you can estimate skirting, architrave, and coving without treating them as interchangeable.",
        "featured_slugs": ["skirting-board-calculator", "architrave-calculator", "coving-calculator"],
        "question_heading": "Quick trim quantity pages",
        "question_intro": "These pages are useful when you already know the room perimeter or door and ceiling runs and want a quick stock-length estimate.",
        "guide_heading": "Trim buying and waste guides",
        "guide_intro": "These pages help with mitres, offcuts, and why the final buying number often ends up above the clean measured run.",
        "notes": [
            ("What changes these estimates most", "Stock length choices, mitres, waste at corners, and whether the room or opening sizes divide neatly into the available lengths all affect the final order."),
            ("When to add more waste", "Increase the allowance where there are lots of corners, detailed profiles, damaged walls, or a need for cleaner grain or finish matching."),
            ("Before you order", "Check profile size, stock lengths, corner waste, and whether adhesive, pins, sealant, or caulk should be planned alongside the trim itself."),
        ],
    },
    "floor-prep-estimating": {
        "start_here_title": "Choose the floor prep layer before you calculate",
        "start_here_intro": "Floor preparation often involves several materials that do different jobs: membranes for moisture control, underlay for comfort or noise, and compounds or screeds for levelling. Use this cluster to start with the prep layer that actually matches the job.",
        "featured_slugs": ["screed-calculator", "self-levelling-compound-calculator", "underlay-calculator", "dpm-calculator"],
        "question_heading": "Common floor prep questions",
        "question_intro": "Use these pages when you want a fast estimate for the layer you need before comparing product options or installation methods.",
        "guide_heading": "Floor prep guides and buying checks",
        "guide_intro": "These pages help with the parts of floor prep that often cause mistakes: depth, substrate condition, and product coverage differences.",
        "notes": [
            ("What changes floor prep quantities most", "Substrate condition, finished depth, overlap rules, and the difference between nominal product coverage and real site yield are the usual drivers."),
            ("Where people under-order", "Levelling products and membranes are often estimated from room size alone without allowing for overlap, irregular areas, or extra depth in low spots."),
            ("Before you order", "Check the intended layer thickness, substrate condition, overlap requirements, and whether primer, tape, edge strip, or moisture control products need to be bought as well."),
        ],
    },
    "drywall-and-finish-estimating": {
        "start_here_title": "Treat boards, screws, and compound as separate buying decisions",
        "start_here_intro": "Drywall work is easy to under-estimate if you only count the boards. This cluster helps separate the sheet coverage, screw quantity, and finishing material so you can build a more realistic order for boarding and jointing work.",
        "featured_slugs": ["plasterboard-calculator", "drywall-screws-calculator", "joint-compound-calculator"],
        "question_heading": "Quick drywall quantity pages",
        "question_intro": "Use these pages when you already know the wall or ceiling area and want a quick route into sheets, screws, or finishing material.",
        "guide_heading": "Boarding and finishing guides",
        "guide_intro": "These guides help with sheet coverage, cut loss, fixings, and the finishing materials that are easy to miss on first calculation.",
        "notes": [
            ("What changes these estimates most", "Board size, framing layout, offcut waste, fixing patterns, and whether the job includes more corners, cut-outs, or awkward ceiling work all affect the total."),
            ("Where people under-order", "It is common to estimate sheet count reasonably well but forget how much screws, compound, tape, and trim details add to the final buying list."),
            ("Before you order", "Check board dimensions, framing centres, fixing rules, and whether tape, beads, jointing materials, or vapour-control layers need their own quantities."),
        ],
    },
    "exterior-finish-estimating": {
        "start_here_title": "Pick the exterior finish before you estimate the order",
        "start_here_intro": "Exterior finishes can behave very differently depending on whether the job uses cladding boards, sealers, or another protective layer. This cluster helps keep those buying routes separate so the estimate matches the product system you are actually using.",
        "featured_slugs": ["cladding-calculator", "masonry-sealer-calculator"],
        "question_heading": "Quick exterior-finish calculators",
        "question_intro": "Use these pages when you already know the wall area and want a faster route into boards, coverage products, or protective coatings.",
        "guide_heading": "Exterior-finish guides",
        "guide_intro": "These pages help with coverage, overlap, and the buying checks that tend to matter most on outside surfaces.",
        "notes": [
            ("What changes these estimates most", "Overlap, exposed edge detail, surface texture, and the difference between nominal product coverage and real installed coverage can all shift the order."),
            ("When to be more cautious", "Increase the allowance on weathered or uneven walls, detailed elevations, and jobs where extra finish coats or cut-heavy layouts are likely."),
            ("Before you order", "Check coverage per pack or board, fixing systems, trims, overlap rules, and whether primers, battens, or membranes need their own quantities."),
        ],
    },
    "concrete-reinforcement-estimating": {
        "start_here_title": "Estimate the reinforcement in the form it is actually bought",
        "start_here_intro": "Reinforcement is usually ordered either as mesh sheets or individual rebar lengths, and those two buying routes behave differently. This cluster keeps them separate so you can move from slab or footing size into a more practical reinforcement order.",
        "featured_slugs": ["mesh-calculator", "rebar-calculator"],
        "question_heading": "Quick reinforcement pages",
        "question_intro": "Use these pages when you already know the slab area or total run length and want a fast starting estimate for mesh or rebar.",
        "guide_heading": "Reinforcement checks and next steps",
        "guide_intro": "These pages help with sheet overlap, stock lengths, and the extra details that often sit outside the first quantity estimate.",
        "notes": [
            ("What changes these estimates most", "Sheet overlap, lap lengths, stock-bar sizes, spacing assumptions, and whether the reinforcement needs extra detailing around openings or edges are the main levers."),
            ("Where people under-order", "A simple area estimate can miss laps, edge conditions, chairs, tying wire, and the extra lengths needed around corners or penetrations."),
            ("Before you order", "Check engineer or supplier requirements for bar size, mesh type, laps, spacers, and whether extra reinforcement is needed in specific parts of the slab or footing."),
        ],
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


def build_intent_pages(item):
    item_name = item["name"].replace(" Calculator", "")
    item_name_lower = item_name.lower()
    templates = GENERIC_INTENT_TEMPLATES.get(item["formula"], [])
    return [
        {
            "slug": item["slug"].replace("-calculator", f"-{page['slug_suffix']}"),
            "title": page["title"].format(name=item_name),
            "description": page["description"].format(name_lower=item_name_lower),
            "headline": page["headline"].format(name_lower=item_name_lower),
            "intro": page["intro"],
        }
        for page in templates
    ]


def get_cluster_intro(cluster_slug: str, fallback: str) -> str:
    override = CLUSTER_OVERRIDES.get(cluster_slug)
    if override:
        return override.get("cluster_intro", fallback)
    return fallback


def get_cluster_hub_content(cluster_slug: str) -> dict:
    return CLUSTER_HUB_CONTENT.get(cluster_slug, {})


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
                "intent_pages": build_intent_pages(item),
                "guide_pages": build_guides(item),
            }
        )
    return calculators
