import json
from html import escape

from data.calculator_scale import ADDITIONAL_CALCULATORS
from data.catalog import get_all_calculators
from data.publisher import NAV_LINKS, SITE


def _default_support(item: dict) -> dict:
    if item.get("formula") == "project_cost":
        return {
            "assumptions": "This tool is designed for rough early-stage budgeting. Regional pricing, scope changes, finish level, access, and contractor availability can move the live quote significantly.",
            "mistakes": "Common mistakes include treating a planning figure as a fixed quote, missing prep or disposal items, and comparing contractor prices that do not cover the same scope.",
            "use_case": "Best used for budget planning, comparing finish routes, and preparing a cleaner quote request before asking suppliers or installers to price the job.",
            "estimate_tip": "Keep the measured area realistic, state any extras clearly, and compare at least two finish routes before relying on one total.",
            "buyer_tip": "Ask whether labour, prep, waste removal, delivery, and snagging are included before comparing headline totals.",
            "market_note": "Regional labour pressure, access, and spec choice can change project-cost pages more than the raw area alone.",
            "final_check": "Before making a decision, compare the calculator output against live local quotes, product data, and the actual site condition.",
        }
    return {
        "assumptions": "This tool uses common estimating logic, practical waste allowances, and buyer-friendly rounding rather than a bare formula-only result.",
        "mistakes": "Common mistakes include using unrealistic coverage or depth inputs, rounding down too aggressively, and ignoring the buying format the supplier actually sells.",
        "use_case": "Best for early planning, quick merchant checks, and turning rough dimensions into a more realistic ordering or budgeting starting point.",
        "estimate_tip": "Measure carefully, sense-check the result against supplier pack sizes, and add a practical allowance for cuts, breakage, or site variation.",
        "buyer_tip": "Compare real delivered coverage, stock size, or bag count rather than relying on the headline price alone.",
        "market_note": "Names, pack sizes, and unit wording can change by supplier or market, but the estimating logic still starts with geometry, waste, and whole-unit buying.",
        "final_check": "Before placing an order, compare coverage, pack size, delivery cost, and whether carrying one extra unit is safer than risking a shortfall.",
    }


def _default_faqs(item: dict) -> list[dict]:
    subject = item["name"].replace(" Calculator", "")
    if item.get("formula") == "project_cost":
        return [
            {"q": f"How accurate is the {subject} estimate?", "a": "Treat it as a planning figure. Real quotes still depend on scope detail, local labour, access, finish level, and what is included or excluded."},
            {"q": f"What should I compare after using the {subject} tool?", "a": "Compare materials, labour, extras, lead time, and exclusions on the same scope before choosing between quotes."},
        ]
    return [
        {"q": f"How should I use the {subject} result?", "a": "Use it as a planning and buying starting point, then compare it against supplier pack sizes, product sheets, and site conditions before ordering."},
        {"q": f"Should I round up the {subject} estimate?", "a": "Most jobs are safer with a practical allowance for waste, cuts, handling loss, or small coverage differences between products."},
    ]


def get_all_calculator_entries() -> list[dict]:
    items = list(get_all_calculators())
    existing_slugs = {item["slug"] for item in items}
    for item in ADDITIONAL_CALCULATORS:
        if item["slug"] in existing_slugs:
            continue
        synthetic = {
            "key": item["slug"].removesuffix("-calculator").replace("-", "_"),
            "slug": item["slug"],
            "name": item["name"],
            "cluster_slug": item["cluster_slug"],
            "cluster_name": item["cluster_name"],
            "category": item["category"],
            "intro": item["intro"],
            "meta_description": item.get("meta_description", item["intro"]),
            "hero_eyebrow": item.get("hero_eyebrow", "Calculator"),
            "support": _default_support(item),
            "faqs": _default_faqs(item),
            "intent_pages": [],
            "guide_pages": [],
            "formula": item.get("formula"),
        }
        items.append(synthetic)
    return items


def family_lookup():
    return {item["slug"]: item for item in get_all_calculator_entries()}


def absolute_url(path: str) -> str:
    return f"{SITE['base_url']}{path}"


def render_nav() -> str:
    links = "".join(
        f'<a href="{escape(item["href"])}">{escape(item["label"])}</a>' for item in NAV_LINKS
    )
    return f'<header class="site-header"><div class="site-shell header-shell"><a class="brand" href="/" aria-label="{escape(SITE["name"])} home"><img src="/assets/logo.svg" alt="{escape(SITE["name"])}"></a><nav class="site-nav">{links}</nav></div></header>'


def render_footer() -> str:
    return (
        '<footer class="site-footer"><div class="site-shell footer-grid">'
        f'<p><strong>{escape(SITE["name"])}</strong> publishes calculators and guides for estimating materials, quantities, and rough costs.</p>'
        '<p class="footer-note"><a href="/about/">About</a> <a href="/editorial-policy/">Editorial policy</a> <a href="/calculator-methodology/">Methodology</a> <a href="/quote-checklist/">Quote prep</a> <a href="/advertiser-disclosure/">Advertiser disclosure</a> <a href="/privacy-policy/">Privacy</a> <a href="/terms/">Terms</a> <a href="/contact/">Contact</a></p>'
        '</div></footer>'
    )


def render_breadcrumbs(items: list[tuple[str, str]]) -> str:
    parts = ['<nav class="breadcrumbs" aria-label="Breadcrumbs">']
    for index, (label, href) in enumerate(items):
        if index:
            parts.append('<span>/</span>')
        parts.append(f'<a href="{escape(href)}">{escape(label)}</a>')
    parts.append("</nav>")
    return "".join(parts)


def render_ad_slot(slot_name: str, label: str = "Advertisement") -> str:
    return ""


def render_faq_schema(faqs: list[dict]) -> str:
    if not faqs:
        return ""
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
            }
            for item in faqs
        ],
    }
    return json.dumps(data)


def render_site_schema() -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "WebSite",
            "name": SITE["name"],
            "url": SITE["base_url"],
            "description": SITE["description"],
        }
    )


def render_org_schema() -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "Organization",
            "name": SITE["name"],
            "url": SITE["base_url"],
            "logo": absolute_url("/assets/logo.svg"),
            "contactPoint": [
                {
                    "@type": "ContactPoint",
                    "contactType": "customer support",
                    "email": SITE["contact_email"],
                }
            ],
        }
    )




def render_software_application_schema(*, name: str, description: str, path: str, category: str = "Estimator") -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "SoftwareApplication",
            "name": name,
            "applicationCategory": category,
            "operatingSystem": "Web",
            "description": description,
            "url": absolute_url(path),
        }
    )


def render_breadcrumb_schema(items: list[tuple[str, str]]) -> str:
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "BreadcrumbList",
            "itemListElement": [
                {
                    "@type": "ListItem",
                    "position": index + 1,
                    "name": label,
                    "item": absolute_url(href),
                }
                for index, (label, href) in enumerate(items)
            ],
        }
    )


def render_layout(*, title: str, description: str, path: str, content: str, schema: list[str] | None = None, page_type: str = "content") -> str:
    canonical = absolute_url(path)
    schema_blocks = [
        render_site_schema(),
        render_org_schema(),
        json.dumps(
            {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": title,
                "url": canonical,
                "description": description,
            }
        ),
    ]
    if schema:
        schema_blocks.extend(item for item in schema if item)
    scripts = "".join(
        f'<script type="application/ld+json">{block}</script>' for block in schema_blocks
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(title)}</title>
  <meta name="description" content="{escape(description)}">
  <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
  <meta name="theme-color" content="#4f8fff">
  <meta name="google-site-verification" content="sqiSiIkXZHkd3G7PHNW6VYudbyt0SPyvvmI2vvdlb_Q">
  <link rel="icon" type="image/svg+xml" href="/assets/favicon.svg">
  <link rel="shortcut icon" href="/assets/favicon.svg">
  <link rel="canonical" href="{escape(canonical)}">
  <link rel="alternate" hreflang="en-GB" href="{escape(canonical)}">
  <link rel="alternate" hreflang="en-US" href="{escape(canonical)}">
  <link rel="alternate" hreflang="x-default" href="{escape(canonical)}">
  <meta property="og:title" content="{escape(title)}">
  <meta property="og:description" content="{escape(description)}">
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{escape(SITE['name'])}">
  <meta property="og:locale" content="en_GB">
  <meta property="og:url" content="{escape(canonical)}">
  <meta property="og:image" content="{escape(absolute_url(SITE['default_image']))}">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{escape(title)}">
  <meta name="twitter:description" content="{escape(description)}">
  <meta name="twitter:image" content="{escape(absolute_url(SITE['default_image']))}">
  <meta name="page-type" content="{escape(page_type)}">
  <link rel="stylesheet" href="/assets/css/styles.css">
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-VZKLRBJ5JK"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){{dataLayer.push(arguments);}}
    gtag('js', new Date());
    gtag('config', 'G-VZKLRBJ5JK');
  </script>
  <script defer src="/assets/js/site.js"></script>
  {scripts}
</head>
<body class="lab-surface">
  {render_nav()}
  <main>{content}</main>
  {render_footer()}
</body>
</html>"""


def render_section_cards(items: list[tuple[str, str]]) -> str:
    cards = "".join(
        f'<article class="content-card prose-card"><h2>{escape(title)}</h2><p>{escape(body)}</p></article>'
        for title, body in items
    )
    return f'<section class="stack-grid">{cards}</section>'
