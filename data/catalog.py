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
        "assumptions": "Project-cost calculators combine covered area with material, labour, extras, contingency, and regional weighting to create a planning number rather than a contract quote.",
        "mistakes": "The common misses are underestimating prep, using labour rates that are too optimistic, forgetting waste or complexity, and treating a planning calculator like a fixed quote.",
        "use_case": "Best for early budget planning, quote preparation, and comparing finish levels before the exact contractor scope is locked in.",
        "estimate_tip": "Start with a realistic job area, then pressure-test the assumptions that move fastest: labour, prep, access, finish level, and contingency.",
        "buyer_tip": "If the total is close to the top of your comfort range, use the higher scenario and write down the scope assumptions before comparing quotes.",
        "final_check": "Before relying on the total, separate materials, labour, extras, and contingency, then check whether access, removals, and finish detail need their own allowance.",
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
    "project_cost": [
        {
            "slug_suffix": "budget-planning-guide",
            "title": "{name} Budget Planning Guide",
            "description": "Build a more usable early budget for {name} before you request quotes.",
            "headline": "Turn a rough {name} number into a working budget",
            "intro": "Use this guide when the estimate needs to become something you can compare, question, and take into a quote conversation.",
        },
        {
            "slug_suffix": "quote-brief-guide",
            "title": "{name} Quote Brief Guide",
            "description": "Use the {name} estimate to prepare a clearer quote brief and scope summary.",
            "headline": "Use the estimate as a cleaner quote brief",
            "intro": "These pages help move from a planning total into a quote-ready brief with fewer hidden assumptions.",
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
}

ITEM_INTENT_TEMPLATES = {
    "hardcore-calculator": [
        {
            "slug": "hardcore-calculator-by-volume",
            "title": "Hardcore Calculator by Volume",
            "meta_title": "Hardcore Calculator by Volume for Base Layers | BuildCostLab",
            "description": "Work out hardcore volume for patios, paths, shed bases, and general fill before you order bags, bulk bags, or loose tonnes.",
            "headline": "Use base dimensions and depth to estimate hardcore before you order aggregate",
            "intro": "Hardcore orders rise or fall on the real base depth and the way the supplier sells the material. Use this page to pressure-test volume, compaction, and buying format before you commit.",
        },
        {
            "slug": "hardcore-how-much-do-i-need",
            "title": "Hardcore Quantity Guide",
            "meta_title": "How Much Hardcore Do I Need? | BuildCostLab",
            "description": "Work out how much hardcore you need, then sense-check tonnes, compaction, and bag versus loose delivery.",
            "headline": "How much hardcore should you order for a base layer?",
            "intro": "A better hardcore order starts with the real area and compacted depth, then checks how that volume turns into tonnes, bulk bags, or loose delivery on site.",
        },
    ],
    "sub-base-calculator": [
        {
            "slug": "sub-base-calculator-by-volume",
            "title": "Sub-Base Calculator by Volume",
            "meta_title": "Sub-Base Calculator by Volume for Patios and Drives | BuildCostLab",
            "description": "Work out sub-base volume for patios, paths, and driveways before you order tonnes, bulk bags, or loose aggregate.",
            "headline": "Use footprint and depth to estimate sub-base before you order",
            "intro": "Sub-base buying gets expensive when the compacted depth, footprint, or supply route is wrong. Use this page to turn the planned build-up into a safer delivered quantity.",
        },
        {
            "slug": "sub-base-how-much-do-i-need",
            "title": "Sub-Base Quantity Guide",
            "meta_title": "How Much Sub-Base Do I Need? | BuildCostLab",
            "description": "Work out how much sub-base you need, then sense-check tonnes, compaction, and merchant delivery options.",
            "headline": "How much sub-base should you order for a patio, path, or drive?",
            "intro": "A better sub-base order starts with the real paved footprint and compacted depth, then checks whether bulk bags or loose tonnes make more sense for the site.",
        },
    ],
    "geotextile-membrane-calculator": [
        {
            "slug": "geotextile-membrane-calculator-by-area",
            "title": "Geotextile Membrane Calculator by Area",
            "meta_title": "Geotextile Membrane Calculator by Area | BuildCostLab",
            "description": "Work out geotextile membrane rolls from covered area, effective roll coverage, and practical overlap waste.",
            "headline": "Use covered area and overlap allowance to estimate geotextile membrane",
            "intro": "Membrane orders usually fail on overlap waste, awkward edges, and optimistic roll coverage. Use this page to turn the measured area into a safer roll count before you buy.",
        },
        {
            "slug": "geotextile-membrane-how-much-do-i-need",
            "title": "Geotextile Membrane Buying Guide",
            "meta_title": "How Much Geotextile Membrane Do I Need? | BuildCostLab",
            "description": "Work out how much geotextile membrane you need, then sense-check overlaps, roll coverage, and groundwork use cases.",
            "headline": "How much geotextile membrane should you order?",
            "intro": "A better membrane order starts with the real covered area, then checks overlap allowances, roll size, and whether the job is separating base layers, lining a trench, or supporting drainage build-up.",
        },
    ],
    "laminate-flooring-calculator": [
        {
            "slug": "laminate-flooring-calculator-by-area",
            "title": "Laminate Flooring Calculator by Area",
            "meta_title": "Laminate Flooring Calculator by Area for Packs and Waste | BuildCostLab",
            "description": "Work out laminate flooring packs from room area, pack coverage, waste allowance, and spare-pack thinking.",
            "headline": "Use room area and pack coverage to estimate laminate flooring with less guesswork",
            "intro": "Laminate orders usually fail on cuts, room shape, and spare-pack decisions rather than the neat area alone. Use this page to turn the measured room into a safer buying total.",
        },
        {
            "slug": "laminate-flooring-how-much-do-i-need",
            "title": "Laminate Flooring Buying Guide",
            "meta_title": "How Much Laminate Flooring Do I Need? | BuildCostLab",
            "description": "Work out how much laminate flooring you need, then sense-check waste, spare packs, and room-fit buying decisions.",
            "headline": "How much laminate flooring should you order for a room?",
            "intro": "A better laminate order starts with the real room shape, then checks pack coverage, waste, spare stock, and the extra materials that often sit outside the first pack count.",
        },
    ],
    "coving-calculator": [
        {
            "slug": "coving-length-calculator",
            "title": "Coving Length Calculator",
            "meta_title": "Coving Length Calculator for Ceiling Perimeter | BuildCostLab",
            "description": "Work out coving lengths from ceiling perimeter, stock size, and realistic corner waste before you order.",
            "headline": "Use ceiling perimeter to estimate coving lengths with less corner waste",
            "intro": "Coving orders usually fail on corners and short return pieces, not on the clean perimeter alone. Use this page to turn the measured ceiling run into a safer buying total.",
        },
        {
            "slug": "coving-how-much-do-i-need",
            "title": "Coving Quantity Guide",
            "meta_title": "How Much Coving Do I Need? | BuildCostLab",
            "description": "Work out how much coving you need for a room, then sense-check piece lengths, mitres, and spare allowance.",
            "headline": "How much coving should you order for a room?",
            "intro": "A better coving order starts with the real ceiling runs, then checks corners, mitres, profile choice, and whether 2m or 3m lengths reduce waste best.",
        },
    ],
    "skirting-board-calculator": [
        {
            "slug": "skirting-board-length-calculator",
            "title": "Skirting Board Length Calculator",
            "meta_title": "Skirting Board Length Calculator for Room Perimeter | BuildCostLab",
            "description": "Work out skirting board lengths from room perimeter, board size, and realistic cut waste before you order.",
            "headline": "Use room perimeter to estimate skirting board lengths with less waste",
            "intro": "Skirting is bought in full board lengths, so the clean room perimeter is only the start. Use this page to pressure-test openings, joints, corners, and board size before you buy.",
        },
        {
            "slug": "skirting-board-how-much-do-i-need",
            "title": "Skirting Board Quantity Guide",
            "meta_title": "How Much Skirting Board Do I Need? | BuildCostLab",
            "description": "Work out how much skirting board you need, then sense-check board lengths, doorway deductions, and spare allowance.",
            "headline": "How much skirting board should you order for a room?",
            "intro": "A better skirting order starts with the real wall runs, then checks door openings, alcoves, corners, and how the chosen board length breaks across the room.",
        },
    ],
    "pipe-bedding-calculator": [
        {
            "slug": "pipe-bedding-calculator-by-volume",
            "title": "Pipe Bedding Calculator by Volume",
            "meta_title": "Pipe Bedding Calculator by Volume for Drainage Trenches | BuildCostLab",
            "description": "Estimate pipe bedding volume for drainage trenches, including practical depth, tonnes, and bulk-bag thinking.",
            "headline": "Use trench volume to estimate pipe bedding before you order sand or gravel",
            "intro": "Pipe bedding is usually ordered from the bedding zone around the pipe, not from a vague trench guess. Use this page to sense-check trench length, bedding width, depth, and buying format before you commit.",
        },
        {
            "slug": "pipe-bedding-how-much-do-i-need",
            "title": "Pipe Bedding Quantity Guide",
            "meta_title": "How Much Pipe Bedding Do I Need? | BuildCostLab",
            "description": "Work out how much pipe bedding you need for a drainage trench, then sense-check tonnes, bulk bags, and surround assumptions.",
            "headline": "Pipe bedding: how much should you order for a drainage trench?",
            "intro": "A better pipe bedding estimate starts with the real trench geometry around the pipe, then checks whether you are pricing the bedding layer only or the wider gravel surround as well.",
        },
    ],
    "drainage-pipe-calculator": [
        {
            "slug": "drainage-pipe-length-calculator",
            "title": "Drainage Pipe Length Calculator",
            "meta_title": "Drainage Pipe Length Calculator for Stock Pieces | BuildCostLab",
            "description": "Work out drainage pipe lengths from trench run, stock size, and a realistic allowance for bends, cuts, and spare pipe.",
            "headline": "Use trench run length to estimate drainage pipe stock lengths with less waste",
            "intro": "Drainage pipe orders usually fail on fittings, chambers, and offcuts rather than the neat straight run. Use this page to turn the measured run into a safer stock-length total before you order.",
        },
        {
            "slug": "drainage-pipe-how-much-do-i-need",
            "title": "Drainage Pipe Buying Guide",
            "meta_title": "How Much Drainage Pipe Do I Need? | BuildCostLab",
            "description": "Work out how much drainage pipe you need, then sense-check stock lengths, fittings, chambers, and spare allowance.",
            "headline": "How much drainage pipe should you order for a trench run?",
            "intro": "A better drainage pipe order starts with the full run and fall, then checks stock lengths, bends, branches, chambers, and whether one spare pipe length is worth carrying.",
        },
    ],
    "french-drain-gravel-calculator": [
        {
            "slug": "french-drain-gravel-calculator-by-volume",
            "title": "French Drain Gravel Calculator by Volume",
            "meta_title": "French Drain Gravel Calculator by Volume | BuildCostLab",
            "description": "Work out french drain gravel volume from trench length, width, depth, and realistic trench overage before you order.",
            "headline": "Use trench dimensions to estimate french drain gravel before you order",
            "intro": "French drain gravel orders usually fail on widened trench sections, outlet details, and the real gravel envelope around the pipe. Use this page to pressure-test the trench volume before you commit.",
        },
        {
            "slug": "french-drain-gravel-how-much-do-i-need",
            "title": "French Drain Gravel Quantity Guide",
            "meta_title": "How Much French Drain Gravel Do I Need? | BuildCostLab",
            "description": "Work out how much french drain gravel you need, then sense-check trench width, gravel depth, delivery route, and spare allowance.",
            "headline": "How much french drain gravel should you order for the trench?",
            "intro": "A better french drain gravel order starts with the real trench build-up, then checks washed gravel depth, widened sections, outlet details, and whether bags or loose tonnes suit the site best.",
        },
    ],
    "mot-type-1-calculator": [
        {
            "slug": "mot-type-1-calculator-for-driveway",
            "title": "MOT Type 1 Calculator for Driveway",
            "meta_title": "MOT Type 1 Calculator for Driveway and Sub-Base | BuildCostLab",
            "description": "Estimate MOT Type 1 for driveway and patio sub-base depth, tonnage, bulk bags, and practical delivery quantities.",
            "headline": "Estimate MOT Type 1 for a driveway or patio base before you book aggregate",
            "intro": "Driveway and patio builds usually rise or fall on the base. This page focuses on converting the footprint and compacted build-up into a more realistic Type 1 order.",
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
    "laminate-flooring-calculator": {
        "assumptions": "Laminate estimates work best when the room footprint, pack coverage, fitting pattern, and any same-batch spare policy are clear before you buy.",
        "mistakes": "The common misses are trusting the neat area, underestimating cuts around doorways or awkward walls, and forgetting spare packs or linked underlay quantities.",
        "use_case": "Best for bedrooms, lounges, hall links, and refresh projects where the buyer needs a practical laminate pack total before ordering.",
        "estimate_tip": "Check the room shape and board direction early, because visible cut-heavy edges and hall links usually move laminate waste faster than people expect.",
    },
    "hardcore-calculator": {
        "assumptions": "Hardcore estimates work best when the base footprint, compacted depth, and the likely loose-delivered buying route are all clear before ordering.",
        "mistakes": "The common misses are using an average depth on an uneven formation, forgetting compaction, and assuming a bulk bag or tonne quote matches the installed layer without checking density.",
        "use_case": "Best for patio bases, shed bases, paths, and general fill where the buyer needs a practical hardcore order before comparing bags, bulk bags, and loose tonnes.",
        "estimate_tip": "Pressure-test the compacted design depth first, because a small change in depth usually moves the hardcore order more than people expect.",
        "buyer_tip": "Bagged supply can suit repairs and tight access, but larger bases often work out better once you compare loose delivery, unloading effort, and spoil handling.",
        "market_note": "Hardcore can cover crushed concrete, recycled aggregate, and other fill routes, but the estimating logic still comes down to footprint, depth, density, compaction, and supply format.",
        "final_check": "Before placing an order, confirm the base dimensions, compacted depth, density assumption, delivery route, and whether membrane or top layers still need separate quantity checks.",
    },
    "sub-base-calculator": {
        "assumptions": "Sub-base estimates work best when the footprint, compacted layer depth, and the intended base specification are clear before the order is placed.",
        "mistakes": "The common misses are underestimating the depth needed for the build, ignoring soft spots or level corrections, and confusing loose-delivered tonnage with the compacted finished layer.",
        "use_case": "Best for patios, paths, and driveways where the buyer needs a practical sub-base quantity before comparing MOT Type 1, hardcore, and merchant delivery routes.",
        "estimate_tip": "Check the compacted target depth against the actual build-up first, because level corrections and weak formation can use more sub-base than the neat footprint suggests.",
        "buyer_tip": "Bulk bags work well for many domestic jobs, but once the area is larger, loose tonnes can be better value if the site can receive and spread them efficiently.",
        "market_note": "Sub-base may be supplied as Type 1, crushed stone, or another graded route, but the estimate still depends mainly on footprint, compacted depth, density, and supply format.",
        "final_check": "Before placing an order, confirm the footprint, compacted depth, chosen material grade, access for delivery, and whether membrane, edging, and bedding layers are being checked separately.",
    },
    "geotextile-membrane-calculator": {
        "assumptions": "Geotextile membrane estimates work best when the covered area, effective roll coverage after overlaps, and the membrane role in the build-up are all clear before buying.",
        "mistakes": "The common misses are ignoring overlap waste, using the nominal roll coverage instead of the effective installed coverage, and forgetting turn-ups, trench edges, or awkward cuts.",
        "use_case": "Best for driveways, french drains, groundwork separation layers, and trench jobs where the buyer needs a safer membrane roll count before ordering.",
        "estimate_tip": "Start with the real covered area, then reduce the roll coverage to account for overlaps and trimming instead of trusting the label coverage at face value.",
        "buyer_tip": "A heavier membrane can change both the roll cost and the effective coverage, so compare grade, overlap requirement, and puncture resistance before deciding on the cheapest roll.",
        "market_note": "Membrane terminology varies between separator, weed-control, non-woven, and geotextile products, but the estimate still turns on effective coverage, overlap waste, and the job type.",
        "final_check": "Before placing an order, confirm effective roll coverage, overlap allowance, membrane grade, edge details, and whether the aggregate or drainage layers above and below still need their own checks.",
    },
    "coving-calculator": {
        "assumptions": "Coving estimates work best when the ceiling run is measured wall by wall, the profile style is known, and the waste allowance reflects mitres, corners, and fragile cuts.",
        "mistakes": "The common misses are forgetting chimney breasts, bay returns, uneven corners, and the extra waste created when short coving lengths force more joins.",
        "use_case": "Best for room refreshes and decorating jobs where you need a practical coving order before comparing profile types, adhesives, and finishing extras.",
        "estimate_tip": "Measure each ceiling run separately, count the corners, and compare whether longer lengths reduce joins enough to justify the higher piece price.",
        "buyer_tip": "Lightweight coving can cut faster and waste less on simple rooms, while plaster or ornate profiles usually need more spare and more fitting care.",
        "market_note": "Merchants describe coving by profile, drop, projection, and material, but the estimate still comes down to ceiling run, length format, corner count, and breakage risk.",
        "final_check": "Before placing an order, confirm profile size, piece length, number of corners, adhesive and filler needs, and whether a spare length is worth carrying for breakage or future repairs.",
    },
    "skirting-board-calculator": {
        "assumptions": "Skirting estimates work best when the wall run is measured room by room, door openings are handled consistently, and the chosen board length matches the real buying format.",
        "mistakes": "The common misses are forgetting doorway deductions or returns, underestimating waste at scribes and mitres, and assuming every wall can be joined without affecting the visible finish.",
        "use_case": "Best for room-by-room trim planning where you need a practical board order before choosing MDF, pine, primed, or prefinished skirting.",
        "estimate_tip": "Measure each wall separately, subtract only the openings that definitely need no skirting, then place the longest boards on the most visible walls before you finalise the order.",
        "buyer_tip": "A slightly longer board can reduce visible joins, but it can also be harder to transport and fit in tight stairwells or smaller rooms.",
        "market_note": "Board height, profile, finish, and stock length change by supplier, but the estimate still depends mainly on the real wall run, opening deductions, joints, and waste.",
        "final_check": "Before placing an order, confirm board length, doorway deductions, corner count, adhesive or pin-fixing method, and whether you want one spare board for damage, late changes, or future repairs.",
    },
    "pipe-bedding-calculator": {
        "assumptions": "Pipe bedding estimates work best when the drain run, bedding width, bedding depth, pipe size, and whether you are estimating the bed only or the bed plus surround are all clear.",
        "mistakes": "The common misses are using the full trench width instead of the actual bedding zone, forgetting the gravel surround around fittings or chambers, and mixing installed depth with the loose-delivered quantity.",
        "use_case": "Best for drainage trenches where you need a practical order for bedding sand or pea gravel before comparing pipe, membrane, gravel surround, and base-material quantities.",
        "estimate_tip": "Measure the pipe run first, then decide whether the quantity should cover the bedding under the pipe only or the wider trench envelope around the run.",
        "buyer_tip": "Small trenches may suit bags or mini bulk bags, but longer runs usually make more sense when you compare tonnes, loose delivery, and the handling effort on site.",
        "market_note": "Pipe bedding is described differently by merchants, but the estimating logic still comes down to run length, bedding width, bedding depth, density, and buying format.",
        "final_check": "Before placing an order, confirm the pipe size, trench width, bedding depth, surround detail, delivery access, and whether the quote covers bedding only or the full drainage aggregate build-up.",
    },
    "drainage-pipe-calculator": {
        "assumptions": "Drainage pipe estimates work best when the full run, stock length, fitting count, chamber positions, and the likely spare allowance are all broadly clear before buying.",
        "mistakes": "The common misses are measuring only the straight run, forgetting bends or chambers, and assuming short offcuts will always be reusable later in the trench.",
        "use_case": "Best for foul and surface-water runs where the buyer needs a practical pipe-length order before pricing bends, connectors, bedding, and trench materials around it.",
        "estimate_tip": "Measure the full run first, then pressure-test stock lengths against bends, chamber entries, branch connections, and whether one spare pipe length is worth carrying.",
        "buyer_tip": "A slightly higher pipe-length order can be cheaper than stalling the install because one damaged or badly cut piece leaves the trench unfinished.",
        "market_note": "Drainage pipe is sold in several diameters, materials, and coupling systems, but the estimate still depends mainly on full run length, stock size, fittings, and spare policy.",
        "final_check": "Before placing an order, confirm pipe diameter, stock length, fitting and chamber count, trench route, and whether bedding, surround, and membrane are being checked separately.",
    },
    "french-drain-gravel-calculator": {
        "assumptions": "French drain gravel estimates work best when the trench run, gravel depth, trench width, outlet detail, and the chosen washed aggregate route are all clear before ordering.",
        "mistakes": "The common misses are using the neat trench width only, forgetting outlets or widened sections, and mixing the gravel envelope with separate bedding or topsoil reinstatement allowances.",
        "use_case": "Best for french drains, interceptor trenches, and perimeter drains where the buyer needs a practical washed-gravel order before comparing membrane, pipe, and outlet details.",
        "estimate_tip": "Measure the full trench envelope first, then decide whether the quantity should cover the gravel surround only or the wider aggregate build-up around outlets and inspection points.",
        "buyer_tip": "Short runs may suit bulk bags, but longer trenches can look very different once loose-tonne delivery, unloading effort, and storage space are compared properly.",
        "market_note": "French drain gravel may be described as washed stone, pea gravel, or drainage aggregate, but the estimate still comes down to trench geometry, gravel depth, density, and buying route.",
        "final_check": "Before placing an order, confirm trench width, gravel depth, outlet details, delivery access, and whether membrane wrap, bedding, or reinstatement materials still need their own checks.",
    },
    "mot-type-1-calculator": {
        "assumptions": "MOT Type 1 estimates work best when the footprint, compacted depth, edge detail, and the intended sub-base build-up are clear before the order is placed.",
        "mistakes": "The common misses are underestimating compacted depth, forgetting edge thickening or levelling corrections, and assuming the loose-delivered quantity matches the installed layer without checking compaction.",
        "use_case": "Best for driveways, patios, and path bases where the buyer needs a practical Type 1 order before comparing bulk bags, loose tonnes, and the layers around the sub-base.",
        "estimate_tip": "Check the compacted target depth against the actual build-up first, because edge thickening, turning areas, and weak formation can use more Type 1 than the neat footprint suggests.",
        "buyer_tip": "Bulk bags can suit smaller domestic jobs, but larger drives and wider bases often work out better once loose-tonne delivery and spreading access are priced properly.",
        "market_note": "Suppliers may sell Type 1 under different stone and recycled routes, but the estimate still depends mainly on footprint, compacted depth, density, and delivery format.",
        "final_check": "Before placing an order, confirm the footprint, compacted depth, material grade, access for delivery, and whether membrane, edging, bedding, or drainage layers are being priced separately.",
    },
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

ITEM_FAQ_OVERRIDES = {
    "laminate-flooring-calculator": [
        {
            "q": "How do I use the Laminate Flooring Calculator?",
            "a": "Measure the room, enter the pack coverage, add a realistic waste allowance, and compare the rounded pack total before you order laminate.",
        },
        {
            "q": "What changes the Laminate Flooring Calculator estimate most?",
            "a": "Room shape, board direction, cut-heavy edges, spare-pack policy, and the true pack coverage after trimming usually move the final laminate order most.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Most laminate jobs benefit from a safer whole-pack total, especially where you want same-batch spare boards for later repairs.",
        },
    ],
    "hardcore-calculator": [
        {
            "q": "How do I use the Hardcore Calculator?",
            "a": "Enter the base dimensions, the installed hardcore depth, and a realistic waste allowance, then compare the result as cubic metres, tonnes, and buying units before you order.",
        },
        {
            "q": "What changes the Hardcore Calculator estimate most?",
            "a": "The biggest drivers are compacted depth, density, and whether the supplier is pricing by bag, bulk bag, or loose tonne rather than by a neat installed layer.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Uneven formation, compaction, and delivery minimums often justify a modest overage rather than landing exactly on the theoretical volume.",
        },
    ],
    "sub-base-calculator": [
        {
            "q": "How do I use the Sub-Base Calculator?",
            "a": "Enter the footprint, compacted sub-base depth, and a realistic waste allowance, then compare the result as cubic metres, tonnes, and buying units before you order.",
        },
        {
            "q": "What changes the Sub-Base Calculator estimate most?",
            "a": "The biggest drivers are compacted depth, density, weak spots or level corrections in the formation, and whether the supplier is pricing by bulk bag or loose tonne.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Small level corrections, compaction, and merchant minimums often justify a modest overage rather than landing exactly on the paper total.",
        },
    ],
    "geotextile-membrane-calculator": [
        {
            "q": "How do I use the Geotextile Membrane Calculator?",
            "a": "Enter the covered area dimensions, use an effective roll coverage that already reflects overlaps, and compare the rounded roll count before you order.",
        },
        {
            "q": "What changes the Geotextile Membrane Calculator estimate most?",
            "a": "The biggest drivers are overlap allowance, the true effective roll coverage, awkward edges or trench details, and the membrane grade chosen for the job.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Overlaps, turn-ups, and trimming can use more membrane than the neat rectangle suggests, so a spare roll is often safer than a shortfall on site.",
        },
    ],
    "coving-calculator": [
        {
            "q": "How do I use the Coving Calculator?",
            "a": "Enter the ceiling run or room perimeter, the coving length you plan to buy, and a realistic waste allowance, then compare the rounded piece count before you order.",
        },
        {
            "q": "What changes the Coving Calculator estimate most?",
            "a": "The biggest drivers are the number of corners, whether the room has bays or chimney breasts, the piece length you can buy, and how much spare you want for brittle cuts or breakage.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Coving cuts, mitres, and damaged ends can use more material than the clean ceiling perimeter suggests, so a modest spare is often safer than landing exactly on the paper total.",
        },
    ],
    "skirting-board-calculator": [
        {
            "q": "How do I use the Skirting Board Calculator?",
            "a": "Enter the wall run that actually needs skirting, the board length you plan to buy, and a realistic waste allowance, then compare the rounded board count before you order.",
        },
        {
            "q": "What changes the Skirting Board Calculator estimate most?",
            "a": "The biggest drivers are doorway deductions, alcoves or chimney breasts, board length, and the extra waste created by corners, scribes, mitres, and visible-joint planning.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. A spare board is often cheaper than running short on a visible wall, making a second trip, or trying to match the profile and finish later.",
        },
    ],
    "pipe-bedding-calculator": [
        {
            "q": "How do I use the Pipe Bedding Calculator?",
            "a": "Enter the drain run, the bedding width, the bedding depth, and a realistic waste allowance, then compare the result as cubic metres, tonnes, and buying units before you order.",
        },
        {
            "q": "What changes the Pipe Bedding Calculator estimate most?",
            "a": "The biggest drivers are the bedding width around the pipe, the assumed depth below and around the run, and whether the supplier prices the material by bag, bulk bag, tonne, or loose load.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Chambers, fittings, overbreak, and awkward trench sections can use more material than the clean trench rectangle suggests, so a modest overage is safer than running short.",
        },
    ],
    "drainage-pipe-calculator": [
        {
            "q": "How do I use the Drainage Pipe Calculator?",
            "a": "Enter the full drain run, the stock length you plan to buy, and a realistic waste allowance, then compare the rounded piece count before you order pipe.",
        },
        {
            "q": "What changes the Drainage Pipe Calculator estimate most?",
            "a": "The biggest drivers are the full trench run, stock length, bends, chambers, and the extra waste created when cuts and offcuts do not divide neatly into the route.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. One spare pipe length is often cheaper than a damaged piece, a missed final connection, or a second merchant run part way through the install.",
        },
    ],
    "french-drain-gravel-calculator": [
        {
            "q": "How do I use the French Drain Gravel Calculator?",
            "a": "Enter the trench length, width, gravel depth, and a realistic waste allowance, then compare the result as cubic metres, tonnes, and buying units before you order.",
        },
        {
            "q": "What changes the French Drain Gravel Calculator estimate most?",
            "a": "The biggest drivers are trench width, gravel depth, widened sections around outlets or corners, and whether the supplier prices by bag, bulk bag, or loose tonne.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Overbreak, widened trench sections, and delivery minimums often justify a modest overage rather than landing exactly on the theoretical trench volume.",
        },
    ],
    "mot-type-1-calculator": [
        {
            "q": "How do I use the MOT Type 1 Calculator?",
            "a": "Enter the footprint, compacted Type 1 depth, and a realistic waste allowance, then compare the result as cubic metres, tonnes, and buying units before you order.",
        },
        {
            "q": "What changes the MOT Type 1 Calculator estimate most?",
            "a": "The biggest drivers are compacted depth, density, edge thickening, level corrections, and whether the supplier prices by bulk bag or loose tonne.",
        },
        {
            "q": "Should I round the result up?",
            "a": "Usually yes. Compaction, weak spots, and merchant minimums often justify a modest overage rather than landing exactly on the paper total.",
        },
    ],
}

CLUSTER_OVERRIDES = {
    "project-cost-estimating": {
        "cluster_intro": "Estimate whole-job planning costs with materials, labour, extras, contingency, and regional weighting kept visible from the start.",
        "support": {
            "assumptions": "Project-cost pages use area-based planning rates rather than a contractor bill of quantities, so they are strongest when the goal is early budgeting and quote preparation.",
            "mistakes": "People often focus on the finish price and forget prep, disposal, access, trims, removals, edge details, or regional labour pressure.",
            "use_case": "Best for first-pass project budgeting, comparing finish routes, and turning a rough job idea into a clearer quote brief.",
            "estimate_tip": "Keep material, labour, extras, and contingency separate so you can see what changed when the estimate moves.",
            "buyer_tip": "When scope is still loose, most planners compare a budget, standard, and higher-spec route rather than treating one total as fixed.",
            "market_note": "Regional labour pressure, access, and buying conventions change by area, but the planning logic still starts with measured scope and separated cost layers.",
        },
        "guides_by_formula": {
            "project_cost": [
                {"slug_suffix": "per-m2-guide", "title": "{name} per m2 Guide", "description": "Use a rough per-m2 view to sense-check the {name} estimate before comparing quotes.", "headline": "Use the rate to stress-test the total", "intro": "A square-metre rate is only useful when the job scope and finish level are clear enough to compare like with like."},
                {"slug_suffix": "budget-planning-guide", "title": "{name} Budget Planning Guide", "description": "Turn the {name} estimate into a more usable early budget.", "headline": "Separate the working budget into clearer layers", "intro": "Keep materials, labour, extras, and contingency visible so the number stays useful when you start comparing routes."},
                {"slug_suffix": "labour-vs-materials-guide", "title": "{name} Labour vs Materials Guide", "description": "See whether labour or materials are more likely to move the {name} total.", "headline": "Find the part of the budget doing the real work", "intro": "A cleaner project budget starts when labour pressure stops hiding inside one vague total."},
                {"slug_suffix": "cost-drivers-guide", "title": "{name} Cost Drivers Guide", "description": "See what usually moves the {name} estimate most.", "headline": "Focus on the assumptions that move first", "intro": "The fastest route to a better estimate is isolating the unstable assumptions before asking for quotes."},
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
        "start_here_title": "Start with the project budget question that matters",
        "start_here_intro": "These pages are for jobs that have moved beyond material counts and into materials, labour, extras, contingency, and regional pressure.",
        "featured_slugs": ["patio-cost-calculator", "driveway-cost-calculator", "roofing-cost-calculator", "tiling-cost-calculator"],
        "question_heading": "Popular project-cost calculators",
        "question_intro": "Use these pages when you need a planning total, not just a quantity list.",
        "guide_heading": "Budget, labour, and quote-prep guides",
        "guide_intro": "These guides help you separate cost layers, compare finish routes, and prepare clearer quote conversations.",
        "notes": [
            ("What moves project budgets most", "Labour, prep, removals, access, finish level, and contingency usually move faster than the measured scope alone."),
            ("Where people under-budget", "Extras, disposal, edge details, and regional labour pressure are commonly missed on early plans."),
            ("Before you compare quotes", "Write down the measured scope, finish assumptions, and what is excluded so contractor totals are being compared on the same basis."),
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
        "meta_title": "Aggregate and Base Estimating Hub for Hardcore, Sub-Base, MOT Type 1, and Pipe Bedding | BuildCostLab",
        "meta_description": "Plan hardcore, sub-base, MOT Type 1, and pipe bedding quantities with linked drainage checks and quote-prep guidance.",
        "start_here_title": "Choose the aggregate or base material first",
        "start_here_intro": "This project hub works best once you know whether the job needs pipe bedding, compacted sub-base, MOT Type 1, hardcore, or another bulk material. The calculators here help turn trench, patio, path, and driveway dimensions into a real delivered quantity, then link into the nearest drainage pages when the base build-up overlaps a trench run.",
        "featured_slugs": ["hardcore-calculator", "sub-base-calculator", "mot-type-1-calculator", "pipe-bedding-calculator"],
        "workflow_title": "Best route through an aggregate or base-material brief",
        "workflow_intro": "Use the hub like a build-up check so the final request covers the right base depth, buying route, and any linked drainage materials.",
        "workflow_cards": [
            ("1. Pick the layer you are actually buying", "Start with hardcore, sub-base, MOT Type 1, or pipe bedding based on the real layer in the build-up rather than using one aggregate page as a rough proxy for all of them."),
            ("2. Check how the material will be supplied", "Sense-check compacted depth, density, tonne conversion, and whether the merchant quote should price bags, bulk bags, or loose delivery."),
            ("3. Send one joined-up base brief", "When the base overlaps a trench or drainage run, package the linked quantities together so the supplier is pricing the whole build-up instead of one isolated tonnage line."),
        ],
        "cross_cluster_title": "Related trench and drainage calculators",
        "cross_cluster_intro": "Use these linked tools when the aggregate order also depends on drainage pipe lengths, pipe bedding, trench gravel, or membrane coverage around the run.",
        "cross_cluster_slugs": ["pipe-bedding-calculator", "drainage-pipe-calculator", "french-drain-gravel-calculator", "geotextile-membrane-calculator"],
        "question_heading": "Quick quantity pages",
        "question_intro": "Start here if you mainly want to know how much bulk material to order from the dimensions of the job and the compacted build-up you are trying to achieve.",
        "guide_heading": "Guides for delivery and depth decisions",
        "guide_intro": "These pages help with the parts of aggregate ordering that usually cause mistakes: compacted depth, delivery format, and whether the base layer is really separate from nearby drainage materials.",
        "quote_support_title": "Best pages to attach before you request aggregate prices",
        "quote_support_intro": "Use these pages together when the merchant or groundworker needs the base layer, supporting trench material, and the nearest delivery-format checks in one place.",
        "quote_support_calculator_slugs": ["hardcore-calculator", "sub-base-calculator", "mot-type-1-calculator", "pipe-bedding-calculator"],
        "quote_support_guide_slugs": ["hardcore-how-much-do-i-need", "sub-base-how-much-do-i-need", "mot-type-1-calculator-for-driveway"],
        "quote_primary_slug": "hardcore-calculator",
        "quote_panel_title": "Turn the base estimate into a cleaner merchant or groundworker brief",
        "quote_panel_intro": "Send one request that covers the real base layer, the target depth, and the delivery route you want priced, especially if the job also touches trench or drainage materials.",
        "quote_panel_items": [
            "State the footprint, target compacted depth, and whether the quoted quantity should reflect loose delivery or finished build-up depth.",
            "Separate hardcore, Type 1, sub-base, bedding, membrane, and any drainage crossover so nothing is missed or priced twice.",
            "Flag access limits, storage space, and whether you want bags, bulk bags, mini loads, or loose tonnes compared in the same reply.",
        ],
        "notes": [
            ("What changes these estimates most", "Installed depth, compaction, density, edge thickening, and the difference between finished depth and loose-delivered depth can move the order significantly."),
            ("Why buying format matters", "A small domestic job may be easier with bags or mini bulk bags, while a larger driveway, patio base, or trench crossover can look very different once loose delivery is priced."),
            ("Before you order", "Check whether the supplier sells by tonne, cubic metre, or bag size, confirm if the quoted quantity is loose or compacted, and make sure linked trench materials are not being priced twice or missed completely."),
        ],
    },
    "drainage-estimating": {
        "meta_title": "Drainage Estimating Hub for Pipe Bedding, Drainage Pipe, Gravel, and Membrane | BuildCostLab",
        "meta_description": "Plan drainage trench materials in one place, including pipe bedding, drainage pipe, gravel surround, membrane, and linked base layers.",
        "start_here_title": "Plan the trench build-up in the order you buy it",
        "start_here_intro": "Drainage work usually needs more than one material at once. You may need pipe length, bedding material, gravel surround, and membrane coverage, so this hub is designed to help you move through those linked trench decisions without missing a part of the order.",
        "featured_slugs": ["pipe-bedding-calculator", "drainage-pipe-calculator", "french-drain-gravel-calculator", "geotextile-membrane-calculator"],
        "workflow_title": "Best route through a drainage trench brief",
        "workflow_intro": "Use the hub like a trench checklist so pipe, bedding, surround, and membrane all make it into the same supplier or installer request.",
        "workflow_cards": [
            ("1. Measure the trench route first", "Start with the full run, likely chamber points, widened sections, and the pipe length so the rest of the trench materials have the right baseline."),
            ("2. Split the trench into buying layers", "Estimate pipe bedding, gravel surround, and membrane separately rather than letting one bulk-material total hide what each layer actually needs."),
            ("3. Send one joined-up drainage request", "Package the trench layers, fittings, and access notes together so the supplier or installer is pricing one drainage build-up rather than several disconnected numbers."),
        ],
        "cross_cluster_title": "Related base-layer calculators",
        "cross_cluster_intro": "Use these linked tools when the drainage estimate also depends on hardcore, sub-base, or Type 1 below and around the trench build-up.",
        "cross_cluster_slugs": ["hardcore-calculator", "sub-base-calculator", "mot-type-1-calculator"],
        "question_heading": "Common drainage quantity checks",
        "question_intro": "Use these pages to estimate the main trench materials before you compare pipe sizes, fittings, outlets, and supplier pack options.",
        "guide_heading": "Drainage planning guides",
        "guide_intro": "These guides support the main calculators by helping with stock lengths, trench fill, washed aggregate quantities, and the parts of the run that usually get missed on first pass.",
        "quote_support_title": "Best pages to include in a drainage quote request",
        "quote_support_intro": "These are the pages most worth attaching when you want one cleaner trench brief instead of separate notes for pipe, bedding, and surround.",
        "quote_support_calculator_slugs": ["pipe-bedding-calculator", "drainage-pipe-calculator", "french-drain-gravel-calculator", "geotextile-membrane-calculator"],
        "quote_support_guide_slugs": ["pipe-bedding-how-much-do-i-need", "drainage-pipe-how-much-do-i-need", "french-drain-gravel-how-much-do-i-need"],
        "quote_primary_slug": "pipe-bedding-calculator",
        "quote_panel_title": "Turn the trench estimate into one cleaner drainage brief",
        "quote_panel_intro": "Send one request that covers the trench route, the pipe run, and the supporting bedding, surround, and membrane layers so the reply is easier to compare and harder to misread.",
        "quote_panel_items": [
            "State the trench run, pipe diameter, stock length, and whether fittings, chambers, or branch connections should be included.",
            "Separate bedding, gravel surround, membrane coverage, and any linked base layer so the quote does not bury missing trench materials inside one vague aggregate line.",
            "Flag access, delivery limits, outlet details, and whether you want loose tonnes, bulk bags, or merchant stock lengths priced side by side.",
        ],
        "notes": [
            ("What changes drainage quantities most", "Trench width, bedding depth, gravel surround, fittings, and the total run length usually matter more than the pipe diameter alone."),
            ("Where people under-order", "Pipe runs are often estimated without enough bedding, gravel surround, or spare pipe, especially where trench width grows around chambers, corners, and outlet points."),
            ("Before you order", "Check whether fittings, chambers, connectors, membrane overlaps, and the base layers around the trench need to be costed separately from the core trench materials."),
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
        "start_here_intro": "Garden-surface materials are sold in very different ways. Turf often comes by roll, seed by pack coverage, artificial grass by roll width, and membrane by roll area, so this project hub helps you start with the right buying format for the job.",
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
        "start_here_intro": "Roofline jobs usually involve several linked products rather than one single quantity. Use this project hub to split the job into fascia, soffit, guttering, and downpipes so each part can be measured and ordered in a more practical way.",
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
        "meta_title": "Trim and Joinery Estimating Hub for Skirting, Coving, and Room Trims | BuildCostLab",
        "meta_description": "Plan skirting, coving, and room-trim quantities with linked flooring and decorating checks plus clearer quote-prep guidance.",
        "start_here_title": "Start with the trim run you can actually measure",
        "start_here_intro": "Joinery trims are usually bought in stock lengths, so the clean perimeter or opening size is only the starting point. This project hub groups together the main room trims so you can estimate skirting, architrave, and coving without treating them as interchangeable.",
        "featured_slugs": ["skirting-board-calculator", "architrave-calculator", "coving-calculator"],
        "workflow_title": "Best route through a room-trim brief",
        "workflow_intro": "Use the hub to split the room into the trim lines you can really measure, then turn those lengths into one clearer joinery or decorating request.",
        "workflow_cards": [
            ("1. Measure the visible trim runs properly", "Start with doorway deductions, alcoves, returns, and ceiling corners so the trim length reflects the room you are actually fitting."),
            ("2. Match the stock length to the finish standard", "Sense-check board or coving lengths, mitre waste, and whether one spare length is worth carrying for cleaner visible walls or future repairs."),
            ("3. Send one room-finish brief", "If the trim order also depends on flooring, decorating, or adhesives, package those linked room-finish decisions together instead of requesting trim in isolation."),
        ],
        "cross_cluster_title": "Related room finish calculators",
        "cross_cluster_intro": "Use these linked tools when the trim order also depends on flooring packs, ceiling paint, or wider room decorating costs.",
        "cross_cluster_slugs": ["flooring-calculator", "laminate-flooring-calculator", "ceiling-paint-calculator", "room-painting-cost-calculator"],
        "question_heading": "Quick trim quantity pages",
        "question_intro": "These pages are useful when you already know the room perimeter or door and ceiling runs and want a quick stock-length estimate.",
        "guide_heading": "Trim buying and waste guides",
        "guide_intro": "These pages help with mitres, offcuts, and why the final buying number often ends up above the clean measured run.",
        "quote_support_title": "Best pages to include in a trim or room-finish brief",
        "quote_support_intro": "Use these pages together when you want a fitter, joiner, or supplier to price the room trims and the nearest linked finish decisions on the same scope.",
        "quote_support_calculator_slugs": ["skirting-board-calculator", "coving-calculator", "flooring-calculator"],
        "quote_support_guide_slugs": ["skirting-board-how-much-do-i-need", "coving-how-much-do-i-need"],
        "quote_primary_slug": "skirting-board-calculator",
        "quote_panel_title": "Turn the trim estimate into a cleaner room-finish brief",
        "quote_panel_intro": "Send one request that covers the measured trim runs, stock-length assumptions, and the linked flooring or decorating checks that affect the final finish standard.",
        "quote_panel_items": [
            "State the room perimeter or ceiling run, any doorway deductions, and whether the price should include mitres, returns, adhesives, pins, caulk, or filler.",
            "Separate skirting, coving, architrave, and any linked flooring or decorating work so visible-room finishes are being priced on the same basis.",
            "Flag profile choice, board length preference, finish standard, and whether you want one spare length allowed for breakage or later repairs.",
        ],
        "notes": [
            ("What changes these estimates most", "Stock length choices, mitres, waste at corners, and whether the room or opening sizes divide neatly into the available lengths all affect the final order."),
            ("When to add more waste", "Increase the allowance where there are lots of corners, detailed profiles, damaged walls, or a need for cleaner grain or finish matching."),
            ("Before you order", "Check profile size, stock lengths, corner waste, and whether adhesive, pins, sealant, or caulk should be planned alongside the trim itself."),
        ],
    },
    "flooring-estimating": {
        "meta_title": "Flooring Estimating Hub for Flooring Packs, Laminate, Underlay, and Room Prep | BuildCostLab",
        "meta_description": "Plan flooring packs, laminate buying totals, underlay, and room-edge checks with clearer quote-prep guidance for interior finish jobs.",
        "start_here_title": "Start with the flooring buying route, not just the room area",
        "start_here_intro": "Flooring jobs are rarely just a neat square-metre question. Use this project hub to move from room size into pack buying, laminate versus vinyl decisions, and the linked underlay or trim checks that often get missed on first pass.",
        "featured_slugs": ["flooring-calculator", "laminate-flooring-calculator", "vinyl-plank-flooring-calculator"],
        "workflow_title": "Best route through a flooring brief",
        "workflow_intro": "Use the hub to move from room size into packs, underlay, and room-edge details so the final flooring request reflects the real install rather than one neat area figure.",
        "workflow_cards": [
            ("1. Start with the floor covering you are actually buying", "Choose flooring, laminate, or vinyl plank first so the pack logic matches the real product route rather than forcing one pack total across different systems."),
            ("2. Check the room-edge extras before you stop", "Sense-check underlay, thresholds, skirting, and spare-pack thinking because those are often the details that move the real room order."),
            ("3. Send one room-by-room flooring brief", "Package the room size, pack assumptions, linked prep layers, and trim notes together so installers and suppliers are pricing the same finish route."),
        ],
        "cross_cluster_title": "Related floor prep and room-edge calculators",
        "cross_cluster_intro": "Use these linked tools when the flooring estimate also depends on underlay, moisture control, screed prep, or skirting quantities around the room perimeter.",
        "cross_cluster_slugs": ["underlay-calculator", "dpm-calculator", "self-levelling-compound-calculator", "skirting-board-calculator"],
        "question_heading": "Popular flooring quantity pages",
        "question_intro": "Use these pages when you already know the room size and want a faster route into packs, waste, or product-choice checks.",
        "guide_heading": "Flooring buying and waste guides",
        "guide_intro": "These pages help with spare packs, product comparisons, and the parts of room flooring that often create the biggest surprises after the first estimate.",
        "quote_support_title": "Best pages to include in a flooring quote request",
        "quote_support_intro": "Use these pages together when the supplier or installer needs the room pack total, the product route, and the prep or edge details priced on the same basis.",
        "quote_support_calculator_slugs": ["flooring-calculator", "laminate-flooring-calculator", "underlay-calculator", "skirting-board-calculator"],
        "quote_support_guide_slugs": ["flooring-packs-calculator", "laminate-flooring-how-much-do-i-need", "laminate-flooring-waste-guide"],
        "quote_primary_slug": "flooring-calculator",
        "quote_panel_title": "Turn the room estimate into a cleaner flooring brief",
        "quote_panel_intro": "Send one request that covers room size, pack assumptions, prep layers, and visible edge details so the install quote is easier to compare and less likely to hide missing extras.",
        "quote_panel_items": [
            "State the room sizes, flooring route, pack coverage, waste allowance, and whether you want a same-batch spare pack included.",
            "Separate underlay, DPM, floor prep, trims, thresholds, and skirting so the room-finish quote does not hide those items in one vague install total.",
            "Flag subfloor condition, door clearances, furniture moves, and whether labour, materials, or both should be priced.",
        ],
        "notes": [
            ("What changes flooring orders most", "Room shape, pack coverage, board direction, visible cut-heavy edges, and the choice to keep a same-batch spare pack usually move the final order most."),
            ("Where people under-order", "Straight room maths often ignores hall links, bay details, thresholds, underlay, and the extra spare many buyers wish they had kept."),
            ("Before you order", "Check pack coverage, waste assumptions, underlay, trims, door bars, and whether subfloor prep or door clearances still need their own allowance."),
        ],
    },
    "floor-prep-estimating": {
        "start_here_title": "Choose the floor prep layer before you calculate",
        "start_here_intro": "Floor preparation often involves several materials that do different jobs: membranes for moisture control, underlay for comfort or noise, and compounds or screeds for levelling. Use this project hub to start with the prep layer that actually matches the job.",
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
        "start_here_intro": "Drywall work is easy to under-estimate if you only count the boards. This project hub helps separate the sheet coverage, screw quantity, and finishing material so you can build a more realistic order for boarding and jointing work.",
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
        "start_here_intro": "Exterior finishes can behave very differently depending on whether the job uses cladding boards, sealers, or another protective layer. This project hub helps keep those buying routes separate so the estimate matches the product system you are actually using.",
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
        "start_here_intro": "Reinforcement is usually ordered either as mesh sheets or individual rebar lengths, and those two buying routes behave differently. This project hub keeps them separate so you can move from slab or footing size into a more practical reinforcement order.",
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
        "start_here_intro": "Decking materials are often under-estimated because the board count gets attention before the fixings and layout waste do. This project hub keeps the main timber quantity and the screw order separate so the buying list is more practical.",
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
        "start_here_intro": "Paving jobs usually need slabs or pavers, bedding material, and jointing products rather than one single material order. This project hub helps separate those layers so the estimate matches the way patios are actually bought and built.",
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
        "start_here_intro": "Roofing quantities often change once overlaps, laps, ridge details, and smaller outbuilding layouts are considered. This project hub separates shingles, felt, and battens so you can estimate the roofing layer that actually matches the job.",
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
    item_override = ITEM_FAQ_OVERRIDES.get(item["slug"])
    if item_override:
        return item_override
    support = build_support(item)
    name = item["name"]
    how_to_answers = {
        "coverage": "Enter the covered dimensions, choose a realistic waste setting, and use this calculator to turn the measured area into a practical buying quantity.",
        "volume": "Enter the measured dimensions and depth, choose a realistic waste setting, and use this calculator to compare the likely buying quantity before you choose bags, bulk, or tonnage-based supply.",
        "linear": "Enter the total run, stock length, and a realistic waste setting, then use this calculator to plan the buying quantity before you check joins, fittings, and extra detail pieces.",
        "project_cost": "Enter the measured scope, choose a UK region, and pressure-test the material, labour, extras, and contingency assumptions until the total looks realistic for planning.",
    }
    result_drivers = {
        "coverage": "The biggest drivers are the measured area, the waste allowance, and the coverage rate or unit count used to turn that area into a buying quantity.",
        "volume": "The biggest drivers are the measured depth, the density or yield assumption, and whether the material is being bought loose, bulk, or bagged.",
        "linear": "The biggest drivers are the measured run, the stock length, and the extra waste created by cuts, corners, joints, and awkward end details.",
        "project_cost": "The biggest drivers are labour, finish level, regional pressure, prep scope, extras, and contingency rather than the measured area alone.",
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
            **({"meta_title": page["meta_title"].format(name=item_name)} if page.get("meta_title") else {}),
        }
        for page in templates
    ]
    pages.extend(ITEM_INTENT_TEMPLATES.get(item["slug"], []))
    deduped_by_slug = {}
    for page in pages:
        deduped_by_slug[page["slug"]] = page
    return list(deduped_by_slug.values())


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

