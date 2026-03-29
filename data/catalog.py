from data.calculator_scale import ADDITIONAL_CALCULATORS
from data.publisher import CALCULATOR_FAMILIES


FORMULA_SUPPORT = {
    "coverage": {
        "assumptions": "Coverage-based calculators assume the product is bought by a stated coverage rate or yield, then rounded to whole buying units after waste is added.",
        "mistakes": "The usual mistakes are using the wrong coverage or yield rate, ignoring trimming losses, and comparing pack prices without checking what each unit really covers.",
        "use_case": "Works best for materials sold by pack, roll, sheet, board, bag, or tin, where the real task is turning a measured area into a whole-unit order.",
        "estimate_tip": "Start with clean geometry, add realistic waste, then check the product sheet because quoted coverage can vary by substrate and install method.",
        "buyer_tip": "If the result is close to the next full unit, most buyers round up to avoid delays, especially where colour, batch, or finish matching matters.",
        "final_check": "Before placing an order, compare product yield, pack size, delivery cost, and whether buying one extra unit is safer than risking a shortfall.",
    },
    "volume": {
        "assumptions": "Volume calculators assume the job can be reduced to length, width, depth, and a practical density or buying-unit conversion.",
        "mistakes": "Depth mistakes are the biggest problem, followed by using the wrong density and forgetting that loose and compacted materials do not behave identically.",
        "use_case": "Best for aggregates, soils, screeds, and fill materials where the order usually starts with volume, then converts into tonnes, bags, or bulk units.",
        "estimate_tip": "Check whether the depth entered is the installed depth or the loose-delivered depth, because the difference can materially change the order.",
        "buyer_tip": "Bag and bulk pricing can diverge quickly once the quantity grows, so use the output to compare the real delivered buying route, not just a headline unit cost.",
        "final_check": "Before placing an order, compare the assumed depth, density, buying-unit size, delivery access, and whether bulk supply is more realistic than bagged buying.",
    },
    "linear": {
        "assumptions": "Linear calculators assume materials are bought in stock lengths and the job can be reduced to a total run with a reasonable cut allowance.",
        "mistakes": "Common misses include forgetting joints, corners, mitres, end conditions, and the waste created when standard stock lengths do not divide neatly into the run.",
        "use_case": "Best for trim, drainage, roofline, pipework, and edging products where the real order is based on whole stock lengths.",
        "estimate_tip": "Measure the full run, add realistic waste for cuts and joints, then check whether fittings and corners need to be costed separately.",
        "buyer_tip": "A slightly higher stock-length overage is often cheaper than losing time to a short final piece or making an extra delivery run.",
        "final_check": "Before placing an order, compare stock lengths, join requirements, fittings, delivery charges, and whether one extra length is safer than running short on site.",
    },
    "project_cost": {
        "assumptions": "Project cost calculators assume a known area or job size, a realistic material allowance, a labour rate per square metre, and a contingency for prep, access, or finish complexity.",
        "mistakes": "The common misses are underestimating prep work, using a finish level that is too optimistic, and forgetting that awkward access or demolition can add cost before the visible install even starts.",
        "use_case": "Best for early project budgeting when you want a realistic low-mid-high planning range before you ask for trade quotes or start pricing the supporting materials in detail.",
        "estimate_tip": "Use a realistic finish level and contingency first, then drill into the supporting material calculators for the parts of the job that still feel uncertain.",
        "buyer_tip": "Treat the result as a planning range, not a fixed quote. Most buyers keep a contingency because labour, prep, and delivery conditions can move quickly once the job is opened up.",
        "final_check": "Before committing, compare labour assumptions, waste, access constraints, disposal, and whether the supporting materials have been checked with their own calculators.",
    },
}

GENERIC_INTENT_TEMPLATES = {
    "coverage": [
        {
            "slug_suffix": "calculator-by-area",
            "title": "{name} Calculator by Area",
            "description": "Work out how much {name} you need from the measured area and a realistic waste allowance.",
            "headline": "Use area and product coverage to work out {name}",
            "intro": "If you already know the area, this page helps turn it into a buying quantity with product yield and waste in mind.",
        },
        {
            "slug_suffix": "how-much-do-i-need",
            "title": "{name} Buying Guide",
            "description": "Work out a sensible buying quantity for {name} before you order.",
            "headline": "{name}: how much should you buy?",
            "intro": "Use this guide to sense-check the calculator result, allow for spare material, and turn the covered area into a more practical order.",
        },
    ],
    "volume": [
        {
            "slug_suffix": "calculator-by-volume",
            "title": "{name} Calculator by Volume",
            "description": "Work out how much {name} you need from length, width, depth, and a realistic waste allowance.",
            "headline": "Use volume to work out {name} with more confidence",
            "intro": "Volume-first estimating is usually the quickest route into a usable buying quantity for loose, bagged, or bulk materials.",
        },
        {
            "slug_suffix": "how-much-do-i-need",
            "title": "{name} Quantity Guide",
            "description": "Use the job dimensions to build a sensible order quantity for {name}.",
            "headline": "{name}: how much should you order?",
            "intro": "Use this guide to sense-check the calculator result, compare buying formats, and move from raw volume into a more reliable order.",
        },
    ],
    "linear": [
        {
            "slug_suffix": "length-calculator",
            "title": "{name} Length Calculator",
            "description": "Work out how much {name} you need from total run length, stock size, and a practical cut allowance.",
            "headline": "Use total run length to work out {name} with less waste",
            "intro": "Length-based materials are usually bought in stock sizes, so the clean run length is only the starting point.",
        },
        {
            "slug_suffix": "how-much-do-i-need",
            "title": "{name} Buying Guide",
            "description": "Turn the measured run into a sensible order for {name} before you buy stock lengths.",
            "headline": "{name}: how much should you buy?",
            "intro": "Use this guide to sense-check the calculator result, compare stock lengths, and allow for the cutting waste that affects real buying totals.",
        },
    ],
    "project_cost": [
        {
            "slug_suffix": "cost-per-m2-guide",
            "title": "{name} Cost per m2 Guide",
            "description": "See how area, finish level, labour, and contingency affect {name} cost per square metre.",
            "headline": "Use cost per m2 as a planning shortcut, not a blind answer",
            "intro": "Cost per square metre is useful for early budgeting, but it only works when the prep, finish level, and extras are honest.",
        },
        {
            "slug_suffix": "budget-planning-guide",
            "title": "{name} Budget Planning Guide",
            "description": "Plan a more realistic budget for {name} using materials, labour, extras, and contingency.",
            "headline": "Build the budget around the job, not just the visible finish",
            "intro": "The visible area matters, but labour, prep, delivery, and snagging are often what separate a neat spreadsheet number from a usable budget.",
        },
    ],
}

ITEM_INTENT_TEMPLATES = {
    "mot-type-1-calculator": [
        {
            "slug": "mot-type-1-calculator-for-driveway",
            "title": "MOT Type 1 Calculator for Driveway",
            "description": "Estimate MOT Type 1 for driveway sub-base depth, tonnage, and practical delivery quantities.",
            "headline": "Estimate MOT Type 1 for a driveway before you book aggregate",
            "intro": "Driveway builds usually rise or fall on the base. This page focuses on converting driveway dimensions into a more realistic Type 1 order.",
        },
    ],
    "sharp-sand-calculator": [
        {
            "slug": "sharp-sand-calculator-for-patio",
            "title": "Sharp Sand Calculator for Patio",
            "description": "Estimate sharp sand for patio bedding and paving prep with practical depth assumptions.",
            "headline": "Work out sharp sand for patio bedding before you order",
            "intro": "Patio bedding depths are easy to misjudge, so this page focuses on turning slab area into a more practical sharp sand order.",
        },
    ],
    "tile-adhesive-calculator": [
        {
            "slug": "bathroom-tile-adhesive-calculator",
            "title": "Bathroom Tile Adhesive Calculator",
            "description": "Estimate bathroom tile adhesive bags for walls, floors, and common domestic tiling layouts.",
            "headline": "Estimate bathroom tile adhesive with fewer bag-count surprises",
            "intro": "Bathroom jobs often mix wall and floor coverage with awkward cuts, so this page focuses on turning the tiled area into a safer adhesive order.",
        },
        {
            "slug": "floor-tile-adhesive-calculator",
            "title": "Floor Tile Adhesive Calculator",
            "description": "Estimate floor tile adhesive quantities from tiled area and practical waste assumptions.",
            "headline": "Use floor area to estimate tile adhesive more realistically",
            "intro": "Floor tile adhesive demand is strongly shaped by the tiled area, product yield, and how much waste the room layout creates.",
        },
    ],
    "tile-grout-calculator": [
        {
            "slug": "bathroom-tile-grout-calculator",
            "title": "Bathroom Tile Grout Calculator",
            "description": "Estimate bathroom tile grout quantities before you buy tubs, bags, or cartons.",
            "headline": "Estimate bathroom tile grout before the final buying list is locked in",
            "intro": "Bathroom tiling often combines wall areas, floor areas, and awkward cuts, so this page helps turn a rough area figure into a more practical grout order.",
        },
    ],
    "tile-backer-board-calculator": [
        {
            "slug": "bathroom-backer-board-calculator",
            "title": "Bathroom Backer Board Calculator",
            "description": "Estimate backer board sheets for bathroom walls and floors before tiling starts.",
            "headline": "Estimate bathroom backer board before the prep stage begins",
            "intro": "Backer board is often bought alongside tiles and adhesive, but it needs its own coverage check before the job starts.",
        },
        {
            "slug": "tile-backer-board-calculator-for-floor",
            "title": "Tile Backer Board Calculator for Floor",
            "description": "Estimate tile backer board sheets or packs from floor area and waste allowance.",
            "headline": "Use floor area to estimate tile backer board with less waste",
            "intro": "Floor prep boards are usually bought by sheet or pack coverage, so this page focuses on converting the floor area into a practical buying total.",
        },
    ],
    "primer-calculator": [
        {
            "slug": "primer-calculator-for-new-plaster",
            "title": "Primer Calculator for New Plaster",
            "description": "Estimate primer or mist-coat quantities for new plaster before painting starts.",
            "headline": "Estimate primer for new plaster before you open the first tin",
            "intro": "New plaster surfaces can absorb far more than a smooth repaint, so this page focuses on a more cautious primer estimate.",
        },
    ],
    "wallpaper-calculator": [
        {
            "slug": "how-many-wallpaper-rolls-do-i-need",
            "title": "How Many Wallpaper Rolls Do I Need?",
            "description": "Estimate wallpaper rolls for a room with repeat, trimming, and spare-roll logic in mind.",
            "headline": "Estimate wallpaper rolls before pattern matching pushes the order up",
            "intro": "Wallpaper jobs often look simple on area alone, but repeat matching and trimming can move the roll count quickly.",
        },
    ],
    "weed-membrane-calculator": [
        {
            "slug": "weed-membrane-calculator-for-gravel",
            "title": "Weed Membrane Calculator for Gravel",
            "description": "Estimate weed membrane coverage for gravel paths, beds, and decorative stone areas.",
            "headline": "Estimate weed membrane for gravel before the aggregate order is placed",
            "intro": "Membrane usually gets ordered alongside gravel or stone, so this page helps turn the covered area into a more practical roll count.",
        },
    ],
    "plasterboard-calculator": [
        {
            "slug": "plasterboard-calculator-for-ceiling",
            "title": "Plasterboard Calculator for Ceiling",
            "description": "Estimate plasterboard sheets for ceiling coverage with a more practical waste allowance.",
            "headline": "Estimate ceiling plasterboard before you order sheets",
            "intro": "Ceiling boarding creates different cutting and handling waste from straight wall work, so this page focuses on that buying pattern.",
        },
    ],
    "plasterboard-adhesive-calculator": [
        {
            "slug": "dot-and-dab-adhesive-calculator",
            "title": "Dot and Dab Adhesive Calculator",
            "description": "Estimate dot-and-dab adhesive bags for plasterboard wall installs and drylining prep.",
            "headline": "Estimate dot-and-dab adhesive before the drylining order is placed",
            "intro": "Drylining jobs can look like simple board coverage, but the adhesive needs a separate buying check before work starts.",
        },
    ],
    "cladding-calculator": [
        {
            "slug": "shed-cladding-calculator",
            "title": "Shed Cladding Calculator",
            "description": "Estimate cladding boards for sheds, garden rooms, and simple outbuildings.",
            "headline": "Estimate shed cladding before you compare board lengths",
            "intro": "Small outbuildings often have lots of cuts and openings, so this page focuses on turning the wall area into a more practical cladding order.",
        },
    ],
    "wood-stain-calculator": [
        {
            "slug": "decking-stain-calculator",
            "title": "Decking Stain Calculator",
            "description": "Estimate decking stain quantities from covered area and coat count assumptions.",
            "headline": "Estimate decking stain before you choose tin sizes",
            "intro": "Exterior timber finishes often need more than one coat, so this page focuses on converting covered area into a more practical stain order.",
        },
    ],
    "paving-sand-calculator": [
        {
            "slug": "paving-sand-calculator-for-patio",
            "title": "Paving Sand Calculator for Patio",
            "description": "Estimate paving sand for patio bedding layers with more practical depth assumptions.",
            "headline": "Estimate patio bedding sand before you price the base and slabs together",
            "intro": "Patio builds often combine several layers, so this page helps isolate the bedding sand quantity before the rest of the order is finalised.",
        },
    ],
    "paving-jointing-compound-calculator": [
        {
            "slug": "patio-jointing-compound-calculator",
            "title": "Patio Jointing Compound Calculator",
            "description": "Estimate patio jointing compound quantities from paved area and a cautious waste margin.",
            "headline": "Estimate patio jointing compound before you buy tubs or bags",
            "intro": "Jointing products are easy to leave until last, so this page helps turn the paved area into a more practical finishing-material order.",
        },
    ],
    "pea-gravel-calculator": [
        {
            "slug": "pea-gravel-calculator-for-garden",
            "title": "Pea Gravel Calculator for Garden",
            "description": "Estimate pea gravel quantities for garden paths, borders, and decorative surface areas.",
            "headline": "Estimate pea gravel for garden areas before you compare bag and bulk delivery",
            "intro": "Decorative gravel jobs are usually bought differently from structural aggregate, so this page focuses on the practical buying quantity for smaller surface areas.",
        },
    ],
    "shed-felt-calculator": [
        {
            "slug": "shed-roof-felt-calculator",
            "title": "Shed Roof Felt Calculator",
            "description": "Estimate shed roof felt rolls for sheds, workshops, and garden buildings.",
            "headline": "Estimate shed roof felt before overlap and waste catch you out",
            "intro": "Small outbuilding roofs often look simple, but roll coverage still depends on laps, edges, and a sensible waste margin.",
        },
    ],
}

ITEM_SUPPORT_OVERRIDES = {
    "brick-calculator": {
        "final_check": "Before placing an order, compare the brick size, openings, pack or pallet breaks, delivery damage risk, and whether a small spare is safer than a short final count.",
    },
    "block-calculator": {
        "final_check": "Before placing an order, compare the block size, openings, pack or pallet breaks, delivery handling, and whether a small spare is safer than a short final count.",
    },
    "mortar-calculator": {
        "assumptions": "Mortar estimates depend on joint thickness, unit type, wall detail, and whether the job is being supplied in bags, tubs, or bulk volume.",
        "mistakes": "The common misses are using the wrong joint-depth assumption, underestimating handling waste, and forgetting that different unit sizes can change mortar demand noticeably.",
        "use_case": "Best for brick and block laying jobs where the buyer wants a rough mortar quantity before comparing bagged and bulk buying routes.",
        "estimate_tip": "Sense-check the assumed joint thickness and wall type first, because those two inputs move the mortar quantity more than many buyers expect.",
        "buyer_tip": "For small jobs, a spare bag is usually safer than landing exactly on the theoretical minimum and risking a part-finished wall.",
        "market_note": "Bag sizes, mix naming, and site mixing habits vary between markets, but yield, joint thickness, and waste are still the main drivers.",
        "final_check": "Before placing an order, compare the assumed joint thickness, bag or bulk yield, weather exposure, and whether the job needs a small contingency for handling loss.",
    },
    "plaster-bead-calculator": {
        "assumptions": "Plaster bead estimates depend on the total run length, profile type, corner details, and how standard stock lengths break across the job.",
        "mistakes": "The common misses are forgetting stop beads, reveals, mitres, and the offcuts created when corners and openings do not divide neatly into stock lengths.",
        "use_case": "Best for corners, reveals, stop ends, and trim lines where the buyer needs a practical stock-length estimate rather than a neat measured run.",
        "estimate_tip": "Measure corners, reveals, and stop runs separately first, then combine them into a total length with a sensible allowance for mitres and offcuts.",
        "buyer_tip": "A spare length is often worth having because damaged ends, awkward cuts, and last-minute reveal changes can quickly use up the final piece.",
        "market_note": "Profile sizes and stock lengths differ between suppliers, but the estimating logic still starts with total run length, profile choice, and cut waste.",
        "final_check": "Before placing an order, compare stock lengths, profile type, corner details, and whether an extra bead length is safer than a return trip for one missing piece.",
    },
    "roof-batten-calculator": {
        "assumptions": "Roof batten estimates depend on the total measured run, batten gauge, roof detail, and how the available stock lengths break across the courses.",
        "mistakes": "The common misses are forgetting extra batten at edges and details, underestimating joins, and assuming the full roof size matters more than the measured batten runs.",
        "use_case": "Best for roofs where the total batten run is already known and the next decision is how many stock lengths to order with a realistic cut allowance.",
        "estimate_tip": "Check the measured batten run against the roof detail, because eaves, ridges, openings, and repairs can all create extra lengths or wastage.",
        "buyer_tip": "Ordering one or two extra battens is often cheaper than stopping a roof job because the final course or detail runs short.",
        "market_note": "Batten sizes and roofing terminology vary, but stock length, roof detail, and cut waste remain the main estimate drivers.",
        "final_check": "Before placing an order, compare batten gauge, stock length, joins, detail runs, and whether a small spare is worth carrying for damaged or unusable pieces.",
    },
}

CLUSTER_OVERRIDES = {
    "project-cost-estimating": {
        "cluster_intro": "Estimate patio, driveway, decking, fencing, painting, and plastering budgets with materials, labour, extras, and contingency combined into a more realistic early planning range.",
        "support": {
            "assumptions": "Project cost pages assume a measured job size, realistic material and labour allowances, and an honest contingency for prep, access, or finish complexity.",
            "mistakes": "The usual mistakes are copying a headline cost-per-m2 number without checking prep work, underestimating extras, and treating a planning budget as if it were a fixed quote.",
            "use_case": "Best for homeowners and planners who want a fast budget range before asking for quotes or breaking the job into the supporting material take-offs.",
            "estimate_tip": "Use the finish and contingency settings to match the real job, then use the linked material calculators to pressure-test the parts of the budget that matter most.",
            "buyer_tip": "A useful budget usually includes contingency. Labour, site prep, delivery, disposal, and snagging can all move after the first quote or opening-up work begins.",
            "market_note": "UK and US labour markets differ, but the planning logic still comes down to scope, material quality, labour rate, prep, and contingency.",
            "final_check": "Before committing, compare the planning range against at least one real quote and sense-check the linked material layers separately where the job feels most uncertain.",
        },
        "guides_by_formula": {
            "project_cost": [
                {"slug_suffix": "cost-drivers-guide", "title": "{name} Cost Drivers Guide", "description": "See what moves {name} the most before you lock in a budget.", "headline": "The biggest budget swings usually happen before the visible finish goes in", "intro": "Area matters, but labour, prep, access, waste, and finish level are usually what move a project budget fastest."},
                {"slug_suffix": "labour-vs-materials-guide", "title": "{name} Labour vs Materials Guide", "description": "Compare labour and material pressure points inside a {name} budget.", "headline": "A cheap material choice does not always create a cheap project", "intro": "Some jobs are material-heavy, some are labour-heavy, and the balance changes with access, finish level, and complexity."},
            ],
        },
    },
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
                {"slug_suffix": "depth-guide", "title": "{name} Depth Guide", "description": "See how installed depth changes the final buying quantity for {name}.", "headline": "Depth is the main reason landscaping orders swing", "intro": "A small change in depth can turn a manageable order into a shortfall or an expensive overbuy."},
                {"slug_suffix": "bags-vs-bulk-guide", "title": "{name} Bags vs Bulk Guide", "description": "Compare bagged and bulk buying routes for {name}.", "headline": "Choose the buying format before the order feels locked in", "intro": "The best buying route depends on quantity, access, labour, and how much packaging or loose handling the site can tolerate."},
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
                {"slug_suffix": "coverage-guide", "title": "{name} Coverage Guide", "description": "Understand how {name} pack or roll coverage turns into a real order quantity.", "headline": "Coverage numbers only help if the product format is clear", "intro": "Pack coverage is the bridge between room size and the real number of packs or rolls you need to buy."},
                {"slug_suffix": "waste-and-fit-guide", "title": "{name} Waste and Fit Guide", "description": "See when {name} waste should be low, standard, or higher.", "headline": "Cutting and fitting losses are where insulation orders go wrong", "intro": "Joists, studs, rafters, and awkward edges often push the real buying total above the clean area figure."},
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
                {"slug_suffix": "coverage-guide", "title": "{name} Coverage Guide", "description": "Learn how yield and thickness change {name} bag quantities.", "headline": "Yield is only meaningful when thickness is honest", "intro": "Published coverage figures usually assume a specific thickness and a cooperative substrate, so real jobs need a more grounded view."},
                {"slug_suffix": "substrate-and-waste-guide", "title": "{name} Substrate and Waste Guide", "description": "Understand how suction, uneven backgrounds, and waste alter the final quantity for {name}.", "headline": "Background condition can move the order more than the wall size", "intro": "A clean board surface and an uneven masonry wall do not consume finish in the same way, even when the area is identical."},
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
                {"slug_suffix": "count-per-area-guide", "title": "{name} Count per Area Guide", "description": "Understand how wall area turns into a practical {name} count.", "headline": "The count starts with area, but the buying logic does not end there", "intro": "Wall area is only the first step. Openings, unit size, and waste all affect what should actually be ordered."},
                {"slug_suffix": "waste-and-openings-guide", "title": "{name} Waste and Openings Guide", "description": "See how openings, cuts, and breakage affect the final {name} order.", "headline": "Waste and openings separate clean estimates from real orders", "intro": "Doors, windows, corners, and small returns can change the count enough to matter before the first pallet is ordered."},
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
                {"slug_suffix": "coverage-guide", "title": "{name} Coverage Guide", "description": "Understand how effective {name} coverage changes the final order quantity.", "headline": "Nominal coverage and effective coverage are not the same thing", "intro": "The label on the pack is only useful once laps, overlaps, and real roof geometry are accounted for."},
                {"slug_suffix": "waste-and-overlap-guide", "title": "{name} Waste and Overlap Guide", "description": "See how edges, overlaps, and cuts affect {name} quantities.", "headline": "Overlap is not optional and waste is not random", "intro": "Edges, ridges, verge details, and overlap rules can quietly add more material than a flat-area estimate suggests."},
            ],
            "linear": [
                {"slug_suffix": "length-guide", "title": "{name} Length Guide", "description": "Understand how stock lengths and roof geometry change the final order.", "headline": "Stock length logic matters more than raw roof size", "intro": "Battens and similar roofing lengths are bought in stock sizes, so the cutting pattern affects the total as much as the roof dimensions do."},
                {"slug_suffix": "waste-and-joins-guide", "title": "{name} Waste and Joins Guide", "description": "See how joins, trimming, and roof detail affect length-based roofing materials.", "headline": "Joins and details quietly create the waste", "intro": "Valleys, edges, staggered joints, and stock-length joins often create more loss than the clean run length first suggests."},
            ],
        },
    },
}

CLUSTER_HUB_CONTENT = {
    "project-cost-estimating": {
        "start_here_title": "Start with the budget question that matches the job",
        "start_here_intro": "These project-cost calculators combine material, labour, extras, and contingency so you can build a planning budget before you start chasing trade quotes. Use them as parent budget tools, then drop into the supporting material calculators when you need deeper take-offs.",
        "featured_slugs": ["patio-cost-calculator", "driveway-cost-calculator", "decking-cost-calculator", "fence-cost-calculator", "room-painting-cost-calculator", "plastering-cost-calculator"],
        "question_heading": "High-intent budget pages",
        "question_intro": "Use these pages when you mainly want to know what the full job could cost, not just how much material to buy.",
        "guide_heading": "Budget-planning guides and next steps",
        "guide_intro": "These guides explain cost per m2, finish levels, contingency, and how to move from a planning budget into a better buying plan.",
        "notes": [
            ("What changes these budgets most", "Labour rate, prep or groundwork, access, finish level, and contingency usually move the total more than small changes in the visible area alone."),
            ("How to use them best", "Use the project-cost result as a parent budget, then open the linked material calculators for the layers of the job that still feel uncertain."),
            ("Before you commit", "Compare the planning range against local quotes, delivery constraints, disposal, and whether supporting materials such as sub-base, paint, screws, or sand have been priced separately."),
        ],
    },
    "tile-estimating": {
        "start_here_title": "Start with the right tiling question",
        "start_here_intro": "Most tiling jobs begin with one of three questions: how many tiles, how much adhesive, and how much grout. Start with the part of the job you are buying first, then use the guides to check waste and box or bag rounding.",
        "featured_slugs": ["tile-calculator", "tile-adhesive-calculator", "tile-grout-calculator", "tile-backer-board-calculator"],
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
        "start_here_intro": "This tool set works best once you know whether the job needs bedding sand, compacted sub-base, MOT Type 1, ballast, or another bulk material. The calculators here help turn trench, patio, path, and driveway dimensions into a real delivered quantity.",
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
        "start_here_intro": "Garden-surface materials are sold in very different ways. Turf often comes by roll, seed by pack coverage, artificial grass by roll width, and membrane by roll area, so this tool set helps you start with the right buying format for the job.",
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
        "start_here_intro": "Roofline jobs usually involve several linked products rather than one single quantity. Use this tool set to split the job into fascia, soffit, guttering, and downpipes so each part can be measured and ordered in a more practical way.",
        "featured_slugs": ["fascia-calculator", "soffit-calculator", "gutter-calculator", "gutter-guard-calculator", "downpipe-calculator"],
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
        "start_here_intro": "Joinery trims are usually bought in stock lengths, so the clean perimeter or opening size is only the starting point. This tool set groups together the main room trims so you can estimate skirting, architrave, and coving without treating them as interchangeable.",
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
        "start_here_intro": "Floor preparation often involves several materials that do different jobs: membranes for moisture control, underlay for comfort or noise, and compounds or screeds for levelling. Use this tool set to start with the prep layer that actually matches the job.",
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
        "start_here_intro": "Drywall work is easy to under-estimate if you only count the boards. This tool set helps separate the sheet coverage, screw quantity, and finishing material so you can build a more realistic order for boarding and jointing work.",
        "featured_slugs": ["plasterboard-calculator", "plasterboard-adhesive-calculator", "drywall-screws-calculator", "joint-compound-calculator"],
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
        "start_here_intro": "Exterior finishes can behave very differently depending on whether the job uses cladding boards, sealers, or another protective layer. This tool set helps keep those buying routes separate so the estimate matches the product system you are actually using.",
        "featured_slugs": ["cladding-calculator", "masonry-sealer-calculator", "wood-stain-calculator"],
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
        "start_here_intro": "Reinforcement is usually ordered either as mesh sheets or individual rebar lengths, and those two buying routes behave differently. This tool set keeps them separate so you can move from slab or footing size into a more practical reinforcement order.",
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
    "decking-estimating": {
        "start_here_title": "Break the decking job into boards and fixings",
        "start_here_intro": "Decking materials are often under-estimated because the board count gets attention before the fixings and layout waste do. This tool set keeps the main timber quantity and the screw order separate so the buying list is more practical.",
        "featured_slugs": ["decking-calculator", "deck-screws-calculator"],
        "question_heading": "Quick decking quantity pages",
        "question_intro": "Use these pages when you already know the deck area and want a fast route into boards, fixings, or common decking buying checks.",
        "guide_heading": "Decking guides and ordering checks",
        "guide_intro": "These pages help with joist spacing, waste, board layouts, and the supporting quantities that are easy to miss on first pass.",
        "notes": [
            ("What changes a decking order most", "Board width, deck shape, cut waste, and whether hidden details like fixings or support timbers are being estimated separately all affect the final order."),
            ("Where people under-order", "A deck can look simple on area alone, but edge cuts, picture framing, spare boards, and screw quantities often add more than expected."),
            ("Before you order", "Check board coverage, joist layout, fixing pattern, and whether fascia boards, subframe timber, weed control, or finish products need their own quantities."),
        ],
    },
    "paving-and-patio-estimating": {
        "start_here_title": "Treat the patio as a layered build-up, not one single quantity",
        "start_here_intro": "Paving jobs usually need slabs or pavers, bedding material, and jointing products rather than one single material order. This tool set helps separate those layers so the estimate matches the way patios are actually bought and built.",
        "featured_slugs": ["paving-calculator", "paving-sand-calculator", "paving-jointing-compound-calculator"],
        "question_heading": "Quick paving quantity pages",
        "question_intro": "Use these pages when you already know the paved area and want a quicker route into slabs, bedding sand, or jointing product quantities.",
        "guide_heading": "Patio guides and buying checks",
        "guide_intro": "These pages help with slab counts, bedding depth, jointing, and the practical differences between paving layouts and product systems.",
        "notes": [
            ("What changes these estimates most", "Unit size, bedding depth, joint width, and the number of cuts around edges or features usually move the final order most."),
            ("Where people under-order", "Patio jobs often budget for the paving units first, then discover the bedding layer and jointing products need a separate quantity check."),
            ("Before you order", "Check slab or paver coverage, bedding thickness, jointing yield, and whether edge restraints, base layers, or sealers need to be bought alongside the paving materials."),
        ],
    },
    "roofing-estimating": {
        "start_here_title": "Match the roof covering to the real roof shape",
        "start_here_intro": "Roofing quantities often change once overlaps, laps, ridge details, and smaller outbuilding layouts are considered. This tool set separates shingles, felt, and battens so you can estimate the roofing layer that actually matches the job.",
        "featured_slugs": ["roofing-shingle-calculator", "roof-felt-calculator", "shed-felt-calculator", "roof-batten-calculator"],
        "question_heading": "Quick roofing quantity pages",
        "question_intro": "Use these pages when you already know the roof area or total batten run and want a faster route into bundles, rolls, or stock lengths.",
        "guide_heading": "Roofing guides and buying checks",
        "guide_intro": "These pages help with overlap, effective coverage, stock lengths, and the parts of roofing work that usually create the most waste.",
        "notes": [
            ("What changes roofing orders most", "Overlaps, roof pitch, edge waste, verge details, and how the roof breaks into courses or stock lengths usually matter more than the clean plan area alone."),
            ("Where people under-order", "Small roofs often look simple, but laps, ridge details, edges, and extra rolls or bundles for awkward cuts can move the final order quickly."),
            ("Before you order", "Check effective product coverage, overlap rules, fixings, edge trims, and whether underlay, battens, or accessories need their own quantity check."),
        ],
    },
}


def build_support(item):
    formula_support = FORMULA_SUPPORT[item["formula"]]
    support = {
        "assumptions": formula_support["assumptions"],
        "mistakes": formula_support["mistakes"],
        "use_case": formula_support["use_case"],
        "estimate_tip": formula_support["estimate_tip"],
        "buyer_tip": formula_support["buyer_tip"],
        "market_note": "UK and US buyers often use different unit language and pack conventions, but the geometry, waste, and whole-unit rounding logic are still the foundation.",
        "final_check": formula_support["final_check"],
    }
    cluster_override = CLUSTER_OVERRIDES.get(item["cluster_slug"])
    if cluster_override:
        support |= cluster_override["support"]
    item_override = ITEM_SUPPORT_OVERRIDES.get(item["slug"])
    if item_override:
        support |= item_override
    return support


def build_faqs(item):
    support = build_support(item)
    name = item["name"]
    how_to_answers = {
        "coverage": "Enter the covered dimensions, choose a realistic waste setting, and use this calculator to turn the measured area into a practical buying quantity.",
        "volume": "Enter the measured dimensions and depth, choose a realistic waste setting, and use this calculator to compare the likely buying quantity before you choose bags, bulk, or tonnage-based supply.",
        "linear": "Enter the total run, stock length, and a realistic waste setting, then use this calculator to plan the buying quantity before you check joins, fittings, and extra detail pieces.",
        "project_cost": "Enter the project dimensions, material and labour assumptions, and contingency settings, then use this calculator to build a realistic planning range before you seek trade quotes.",
    }
    result_drivers = {
        "coverage": "The biggest drivers are the measured area, the waste allowance, and the coverage rate or unit count used to turn that area into a buying quantity.",
        "volume": "The biggest drivers are the measured depth, the density or yield assumption, and whether the material is being bought loose, bulk, or bagged.",
        "linear": "The biggest drivers are the measured run, the stock length, and the extra waste created by cuts, corners, joints, and awkward end details.",
        "project_cost": "The biggest drivers are the true job area, labour rate, prep or groundwork allowance, finish level, and the contingency used to cover uncertainty.",
    }
    return [
        {"q": f"How do I use the {name}?", "a": how_to_answers[item["formula"]]},
        {"q": f"What changes the {name} estimate most?", "a": result_drivers[item["formula"]]},
        {"q": "Should I round the result up?", "a": support["buyer_tip"]},
    ]


def build_guides(item):
    item_name = item["name"].replace(" Calculator", "")
    override = CLUSTER_OVERRIDES.get(item["cluster_slug"], {})
    templates = override.get("guides_by_formula", {}).get(item["formula"], [])
    return [
        {
            "slug": item["slug"].replace("-calculator", f"-{guide['slug_suffix']}"),
            "title": guide["title"].format(name=item_name),
            "description": guide["description"].format(name=item_name),
            "headline": guide["headline"],
            "intro": guide["intro"],
        }
        for guide in templates
    ]


def build_intent_pages(item):
    item_name = item["name"].replace(" Calculator", "")
    templates = GENERIC_INTENT_TEMPLATES.get(item["formula"], [])
    pages = [
        {
            "slug": item["slug"].replace("-calculator", f"-{page['slug_suffix']}"),
            "title": page["title"].format(name=item_name),
            "description": page["description"].format(name=item_name),
            "headline": page["headline"].format(name=item_name),
            "intro": page["intro"],
        }
        for page in templates
    ]
    pages.extend(ITEM_INTENT_TEMPLATES.get(item["slug"], []))
    deduped = []
    seen = set()
    for page in pages:
        if page["slug"] in seen:
            continue
        seen.add(page["slug"])
        deduped.append(page)
    return deduped


def get_cluster_intro(cluster_slug: str, fallback: str) -> str:
    override = CLUSTER_OVERRIDES.get(cluster_slug)
    if override:
        return override.get("cluster_intro", fallback)
    hub_content = CLUSTER_HUB_CONTENT.get(cluster_slug)
    if hub_content:
        return hub_content.get("start_here_intro", fallback)
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
