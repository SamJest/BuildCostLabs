from data.catalog import get_all_calculators

REGION_PAGES = [
    {
        "slug": "london",
        "name": "London",
        "kind": "region",
        "headline": "London building material and job-planning calculators",
        "description": "Use BuildCostLab calculators and guides to plan paint, paving, concrete, flooring, fencing, and other common jobs in London.",
        "intro": "London jobs often feel expensive because labour, access, delivery windows, parking, and waste removal stack up quickly. Use these calculators to get the material side right first, then sense-check the practical extras that commonly matter more in denser urban jobs.",
        "featured_calculators": ["paint-calculator", "concrete-calculator", "paving-calculator", "flooring-calculator", "tile-calculator", "fence-calculator"],
        "featured_clusters": ["paint-estimating", "concrete-estimating", "paving-and-patio-estimating", "flooring-estimating"],
        "factors": [
            ("What usually moves the budget", "Access limits, labour rates, delivery constraints, parking, and skip or waste handling often change the final project cost faster in London than the raw material quantity does."),
            ("Where estimates go wrong", "People often price the visible finish but forget the effect of restricted access, extra labour time, and phased deliveries on smaller or tighter London jobs."),
            ("How to use these calculators locally", "Start with the material quantity, then add a realistic buffer for delivery, handling, and labour complexity before comparing quotes."),
        ],
        "related_locations": ["south-east-england", "birmingham", "bristol"],
    },
    {
        "slug": "south-east-england",
        "name": "South East England",
        "kind": "region",
        "headline": "South East England calculators for materials, quantities, and buying checks",
        "description": "Plan common building and garden jobs in South East England with practical calculators and supporting buying guides.",
        "intro": "South East jobs can swing between suburban access, premium labour areas, and easier merchant supply routes. These pages help you estimate the main quantities first so you can judge whether quote differences come from the work itself or the local conditions around it.",
        "featured_calculators": ["paint-calculator", "gravel-calculator", "paving-calculator", "decking-calculator", "fence-calculator", "topsoil-calculator"],
        "featured_clusters": ["paving-and-patio-estimating", "decking-estimating", "fence-estimating", "soil-and-landscaping-estimating"],
        "factors": [
            ("Common local pressure points", "Finish level, labour pricing, delivery access, and whether the job sits in a dense town, commuter belt, or more accessible suburban area can all move the final cost."),
            ("Best use for these pages", "These pages work well for comparing the same job across a few buying routes before you ask merchants or contractors for firm prices."),
            ("Before you compare quotes", "Make sure waste, delivery, prep work, and any disposal or removal costs are treated consistently across every quote."),
        ],
        "related_locations": ["london", "south-west-england", "bristol"],
    },
    {
        "slug": "south-west-england",
        "name": "South West England",
        "kind": "region",
        "headline": "South West England calculators for renovation, garden, and outdoor project planning",
        "description": "Estimate materials and common job quantities for South West England using calculators, guides, and grouped project hubs.",
        "intro": "South West projects often mix straightforward domestic jobs with longer delivery routes, weather exposure, and outdoor work where waste and timing matter. Start with the quantity estimate, then sense-check the buying format and practical conditions around the site.",
        "featured_calculators": ["paint-calculator", "paving-calculator", "decking-calculator", "gravel-calculator", "fence-calculator", "roofing-shingle-calculator"],
        "featured_clusters": ["paving-and-patio-estimating", "decking-estimating", "gravel-and-aggregate-estimating", "roofing-estimating"],
        "factors": [
            ("What matters most", "Outdoor exposure, delivery logistics, timing, and whether the job is coastal, urban, or rural can all change the real buying plan."),
            ("What people miss", "Garden and surfacing jobs are often priced by the visible finish first, with base layers, edge details, and delivery setup left too vague."),
            ("How to use the estimate", "Treat the calculator result as the clean quantity baseline, then add sensible allowances for access, weather delays, and staged deliveries where needed."),
        ],
        "related_locations": ["south-east-england", "wales", "bristol"],
    },
    {
        "slug": "midlands",
        "name": "The Midlands",
        "kind": "region",
        "headline": "Midlands building calculators for material takeoffs and early budget checks",
        "description": "Use BuildCostLab calculators to estimate common building, landscaping, flooring, and fencing jobs across the Midlands.",
        "intro": "Midlands projects often sit in the sweet spot where merchant access is decent, labour pricing varies by town and city, and comparing supplier routes can make a real difference. These pages help you isolate the quantity and buying questions before you price the labour side.",
        "featured_calculators": ["concrete-calculator", "brick-calculator", "flooring-calculator", "tile-calculator", "gravel-calculator", "fence-calculator"],
        "featured_clusters": ["concrete-estimating", "masonry-estimating", "flooring-estimating", "fence-estimating"],
        "factors": [
            ("What usually changes costs", "Ground conditions, labour availability, merchant choice, and whether materials are bought in bags, pallets, or bulk can all shift the final price."),
            ("Best jobs for these tools", "Extensions, refits, garden hardscaping, and routine domestic upgrade jobs tend to benefit most from a quick quantity-first planning pass."),
            ("Good quote discipline", "Ask each contractor or supplier to price the same spec, waste assumption, and delivery route so the comparison stays useful."),
        ],
        "related_locations": ["birmingham", "north-of-england", "wales"],
    },
    {
        "slug": "north-of-england",
        "name": "North of England",
        "kind": "region",
        "headline": "North of England project calculators for materials, garden jobs, and refits",
        "description": "Estimate materials, quantities, and practical buying routes for common jobs across the North of England.",
        "intro": "Northern jobs can still vary a lot by city, weather exposure, property type, and supplier route. The value of these calculators is that they let you keep the core quantity logic stable while you compare how labour, access, and buying choices change locally.",
        "featured_calculators": ["paint-calculator", "concrete-calculator", "gravel-calculator", "decking-calculator", "insulation-board-calculator", "fence-calculator"],
        "featured_clusters": ["paint-estimating", "concrete-estimating", "decking-estimating", "insulation-estimating"],
        "factors": [
            ("Where planning pays off", "Groundwork, external jobs, and thermal-upgrade work usually benefit from checking quantities, waste, and buying units before labour quotes arrive."),
            ("Common oversight", "People often compare headline material prices but forget to compare delivery minimums, bulk routes, and small extras that change the real order value."),
            ("How to use the pages", "Use the calculators to standardise the scope first, then compare local contractor and merchant prices against the same baseline."),
        ],
        "related_locations": ["manchester", "leeds", "scotland"],
    },
    {
        "slug": "scotland",
        "name": "Scotland",
        "kind": "region",
        "headline": "Scotland calculators for material quantities, weather-exposed jobs, and buying checks",
        "description": "Plan common renovation, flooring, surfacing, insulation, and fencing jobs in Scotland with practical calculators and guides.",
        "intro": "Scottish jobs often need sensible allowances for weather exposure, insulation expectations, transport, and outdoor-install timing. These pages help you separate the hard quantity answer from the softer planning variables that often drive the real quote.",
        "featured_calculators": ["insulation-board-calculator", "concrete-calculator", "gravel-calculator", "roofing-shingle-calculator", "flooring-calculator", "fence-calculator"],
        "featured_clusters": ["insulation-estimating", "roofing-estimating", "concrete-estimating", "flooring-estimating"],
        "factors": [
            ("Main local variables", "Transport, weather windows, thermal-spec expectations, and exposed-site detailing often change the real cost much more than the base quantity does."),
            ("What these calculators are good for", "They are strong for early budgeting, merchant comparisons, and checking whether a quote feels aligned with the actual material quantities involved."),
            ("Before you buy", "Check whether local weather, lead times, and site access mean you need a more conservative waste or spare-stock allowance."),
        ],
        "related_locations": ["edinburgh", "glasgow", "north-of-england"],
    },
    {
        "slug": "wales",
        "name": "Wales",
        "kind": "region",
        "headline": "Wales calculators for outdoor works, renovation jobs, and quantity planning",
        "description": "Estimate common project quantities in Wales with practical calculators for concrete, gravel, paint, fencing, decking, and more.",
        "intro": "Welsh projects often combine routine domestic work with weather exposure, delivery planning, and varied site access between towns, valleys, and rural areas. Start with the material quantity, then use the supporting notes to sense-check the practical buying route.",
        "featured_calculators": ["paint-calculator", "gravel-calculator", "paving-calculator", "decking-calculator", "fence-calculator", "topsoil-calculator"],
        "featured_clusters": ["gravel-and-aggregate-estimating", "paving-and-patio-estimating", "decking-estimating", "soil-and-landscaping-estimating"],
        "factors": [
            ("Where the cost shifts happen", "Delivery distance, exposure, labour availability, and whether the work is phased around weather can all change the buying plan."),
            ("Useful jobs for this section", "Garden hardscaping, repainting, surfacing, fencing, and domestic upgrade projects are strong fits for these tools."),
            ("How to compare options well", "Use the same assumptions for waste, prep, and extras across every quote or buying route before deciding which option is actually cheaper."),
        ],
        "related_locations": ["cardiff", "south-west-england", "midlands"],
    },
]

CITY_PAGES = [
    {
        "slug": "manchester",
        "name": "Manchester",
        "kind": "city",
        "headline": "Manchester calculators for flooring, paint, concrete, and outdoor jobs",
        "description": "Use BuildCostLab calculators and guides to plan common renovation and landscaping jobs in Manchester.",
        "intro": "Manchester jobs often combine city access considerations with a broad mix of domestic refits, flooring work, external upgrades, and landscaping. These pages help you fix the quantity baseline before you compare labour and delivery routes.",
        "featured_calculators": ["paint-calculator", "flooring-calculator", "concrete-calculator", "decking-calculator", "fence-calculator", "gravel-calculator"],
        "featured_clusters": ["flooring-estimating", "paint-estimating", "concrete-estimating", "decking-estimating"],
        "factors": [
            ("What usually matters locally", "Access, parking, phased work, labour availability, and the choice between small-load and bulk deliveries can all move the quote."),
            ("Strong jobs for these tools", "Room refits, flooring upgrades, patios, fencing, and small concrete works are all good fits for a quantity-first planning pass."),
            ("How to use them", "Start with the calculator result, then ask merchants or contractors to price against the same scope so the comparison is fair."),
        ],
        "related_locations": ["north-of-england", "leeds", "liverpool"],
    },
    {
        "slug": "birmingham",
        "name": "Birmingham",
        "kind": "city",
        "headline": "Birmingham project calculators for materials, surfacing, and common home upgrades",
        "description": "Estimate common renovation and outdoor project quantities in Birmingham with BuildCostLab calculators and guides.",
        "intro": "Birmingham projects often benefit from comparing multiple merchant routes and installation options. These pages help you lock in the quantities first so you can tell whether a quote difference is genuine or just a change in assumptions.",
        "featured_calculators": ["concrete-calculator", "brick-calculator", "paint-calculator", "paving-calculator", "tile-calculator", "fence-calculator"],
        "featured_clusters": ["concrete-estimating", "masonry-estimating", "paint-estimating", "paving-and-patio-estimating"],
        "factors": [
            ("Where budgets move", "Delivery setup, labour pace, prep work, and spec differences between quotes often matter more than people expect."),
            ("Best use case", "These pages work well for domestic upgrades, landscaping, and straightforward extension-related material planning."),
            ("Quote comparison tip", "Keep the same waste setting, base depth, and finish assumptions across every option before deciding what is best value."),
        ],
        "related_locations": ["midlands", "london", "bristol"],
    },
    {
        "slug": "leeds",
        "name": "Leeds",
        "kind": "city",
        "headline": "Leeds calculators for paint, flooring, insulation, and garden jobs",
        "description": "Plan common Leeds renovation and garden jobs with practical calculators for materials, quantities, and buying checks.",
        "intro": "Leeds projects often span routine domestic upgrades, external works, and energy-related refits where the material quantity is only one part of the decision. Use these tools to fix the quantity first, then price the practical extras around it.",
        "featured_calculators": ["paint-calculator", "flooring-calculator", "insulation-board-calculator", "gravel-calculator", "decking-calculator", "fence-calculator"],
        "featured_clusters": ["paint-estimating", "flooring-estimating", "insulation-estimating", "decking-estimating"],
        "factors": [
            ("What changes real cost", "Labour availability, waste allowances, access, and whether the job uses bagged, packed, or bulk supply can all change the total."),
            ("Good fit projects", "Internal redecoration, flooring replacement, insulation upgrades, and small outdoor jobs all work well with these tools."),
            ("How to compare routes", "Use the same measured area and waste assumptions when comparing merchants, brands, and contractor quotes."),
        ],
        "related_locations": ["north-of-england", "manchester", "scotland"],
    },
    {
        "slug": "bristol",
        "name": "Bristol",
        "kind": "city",
        "headline": "Bristol calculators for paint, paving, decking, and landscaping jobs",
        "description": "Estimate common Bristol material quantities for renovation, hardscaping, and garden projects with BuildCostLab.",
        "intro": "Bristol jobs often mix urban access constraints with garden and extension-led work where the material baseline matters. These pages help you sense-check quantities before comparing quotes or planning delivery.",
        "featured_calculators": ["paint-calculator", "paving-calculator", "decking-calculator", "gravel-calculator", "topsoil-calculator", "fence-calculator"],
        "featured_clusters": ["paving-and-patio-estimating", "decking-estimating", "soil-and-landscaping-estimating", "paint-estimating"],
        "factors": [
            ("Key planning variables", "Access, parking, delivery timing, and the knock-on effect of staged outdoor works often change the buying route."),
            ("Where people under-plan", "Patio and garden jobs are often priced from the finish surface only, with base layers, waste, and extras under-scoped."),
            ("How to use the pages", "Lock in the quantities first, then use the cluster pages and guides to check the buying format and likely missing extras."),
        ],
        "related_locations": ["south-west-england", "london", "cardiff"],
    },
    {
        "slug": "edinburgh",
        "name": "Edinburgh",
        "kind": "city",
        "headline": "Edinburgh calculators for refits, insulation, flooring, and outdoor works",
        "description": "Use BuildCostLab calculators to estimate common Edinburgh project quantities for interiors, insulation, and outdoor jobs.",
        "intro": "Edinburgh projects often bring together older building stock, access quirks, and weather-aware planning. Use the calculators to answer the quantity question cleanly, then adapt the buying plan to the conditions around the job.",
        "featured_calculators": ["insulation-board-calculator", "flooring-calculator", "paint-calculator", "concrete-calculator", "gravel-calculator", "roofing-shingle-calculator"],
        "featured_clusters": ["insulation-estimating", "flooring-estimating", "paint-estimating", "roofing-estimating"],
        "factors": [
            ("What usually moves the quote", "Access, weather windows, thermal-upgrade scope, and waste allowances can change the real budget quickly."),
            ("Best use case", "These pages are useful for early planning, merchant checks, and bringing more consistency to contractor comparisons."),
            ("Buying tip", "Be realistic about spare stock and weather-sensitive timing on exposed or phased jobs."),
        ],
        "related_locations": ["scotland", "glasgow", "leeds"],
    },
    {
        "slug": "glasgow",
        "name": "Glasgow",
        "kind": "city",
        "headline": "Glasgow calculators for paint, concrete, insulation, and garden projects",
        "description": "Estimate common Glasgow project quantities with practical calculators for materials, waste, and buying checks.",
        "intro": "Glasgow projects can range from straightforward domestic work to more access-sensitive refurbishments and exposed outdoor jobs. These pages help you standardise the quantity side before you compare labour and supply options.",
        "featured_calculators": ["paint-calculator", "concrete-calculator", "insulation-board-calculator", "gravel-calculator", "decking-calculator", "fence-calculator"],
        "featured_clusters": ["paint-estimating", "concrete-estimating", "insulation-estimating", "decking-estimating"],
        "factors": [
            ("What matters most", "Weather exposure, transport, site access, and whether materials arrive as small loads or bulk supply can all change the total."),
            ("What these tools solve", "They are best for clarifying scope, sense-checking merchant totals, and making labour quotes easier to compare."),
            ("Before you compare options", "Keep the same prep assumptions, waste, and buying units across every contractor or merchant route."),
        ],
        "related_locations": ["scotland", "edinburgh", "north-of-england"],
    },
    {
        "slug": "cardiff",
        "name": "Cardiff",
        "kind": "city",
        "headline": "Cardiff calculators for surfacing, fencing, paint, and renovation jobs",
        "description": "Plan common Cardiff material quantities with calculators and guides for paint, paving, fencing, gravel, and more.",
        "intro": "Cardiff jobs often benefit from a clean material baseline because small differences in access, delivery, and weather can make quotes look more different than the core scope really is. Use these tools to pin down the quantity answer first.",
        "featured_calculators": ["paint-calculator", "paving-calculator", "gravel-calculator", "decking-calculator", "fence-calculator", "topsoil-calculator"],
        "featured_clusters": ["paint-estimating", "paving-and-patio-estimating", "gravel-and-aggregate-estimating", "decking-estimating"],
        "factors": [
            ("Where the real cost changes", "Delivery setup, exposure, access, and the small extras around external work often move the total more than the base quantity."),
            ("Best fit", "These tools are strong for domestic outdoor work, repainting, landscaping, and practical upgrade jobs."),
            ("How to use the output", "Treat the calculator result as your clean starting point, then use the related guides to think through waste, pack size, and delivery format."),
        ],
        "related_locations": ["wales", "bristol", "south-west-england"],
    },
]


_CALCULATOR_LOOKUP = {item["slug"]: item for item in get_all_calculators()}
_CLUSTER_LOOKUP = {}
for item in get_all_calculators():
    _CLUSTER_LOOKUP.setdefault(item["cluster_slug"], {"cluster_slug": item["cluster_slug"], "cluster_name": item["cluster_name"], "intro": item["intro"]})



def get_location_index_content() -> dict:
    return {
        "headline": "UK location pages for practical estimating and buying decisions",
        "intro": "These pages are designed to help you start with the right calculator for your area, then pressure-test the result against common local planning variables such as access, delivery, labour context, and outdoor exposure.",
    }



def get_all_locations() -> list[dict]:
    return REGION_PAGES + CITY_PAGES



def get_location_groups() -> dict:
    return {"regions": REGION_PAGES, "cities": CITY_PAGES}



def get_location_by_slug(slug: str) -> dict | None:
    for item in get_all_locations():
        if item["slug"] == slug:
            return item
    return None



def get_calculators_for_location(location: dict) -> list[dict]:
    return [
        _CALCULATOR_LOOKUP[slug]
        for slug in location.get("featured_calculators", [])
        if slug in _CALCULATOR_LOOKUP
    ]



def get_clusters_for_location(location: dict) -> list[dict]:
    return [
        _CLUSTER_LOOKUP[slug]
        for slug in location.get("featured_clusters", [])
        if slug in _CLUSTER_LOOKUP
    ]



def get_related_locations(location: dict) -> list[dict]:
    return [
        get_location_by_slug(slug)
        for slug in location.get("related_locations", [])
        if get_location_by_slug(slug) is not None
    ]
