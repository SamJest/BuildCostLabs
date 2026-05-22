import json
from html import escape

from components.publishing import (
    absolute_url,
    family_lookup,
    render_ad_slot,
    render_breadcrumb_schema,
    render_breadcrumbs,
    render_faq_schema,
    render_layout,
)
from data.catalog import get_all_calculators
from data.workflows import get_all_workflows, workflow_lookup
from generators.publisher_pages import render_quality_strip


def _guide_lookup() -> dict[str, dict]:
    guides = {}
    for family in get_all_calculators():
        for guide in family.get("intent_pages", []) + family.get("guide_pages", []):
            guides[guide["slug"]] = guide | {"family": family}
    return guides


def _workflow_card(workflow: dict, *, label: str = "Workflow") -> str:
    return (
        f'<article class="tool-card workflow-card" data-workflow-card="{escape(workflow["slug"])}">'
        f'<div class="card-chip-row"><span class="card-chip card-chip-featured">{escape(label)}</span>'
        f'<span class="card-chip card-chip-soft">{len(workflow.get("calculator_slugs", []))} calculators</span></div>'
        f'<h3><a href="/workflows/{escape(workflow["slug"])}/" data-workflow-card-link>{escape(workflow["title"])}</a></h3>'
        f'<p>{escape(workflow["intro"])}</p>'
        '<div class="tool-card-actions">'
        f'<a class="text-link" href="/workflows/{escape(workflow["slug"])}/" data-workflow-card-link>Plan this job</a>'
        '</div>'
        '</article>'
    )


def _calculator_cards(workflow: dict, calculators: dict[str, dict]) -> str:
    cards = []
    for index, slug in enumerate(workflow.get("calculator_slugs", []), start=1):
        calculator = calculators.get(slug)
        if not calculator:
            continue
        cards.append(
            f'<article class="tool-card workflow-step-card">'
            f'<div class="card-chip-row"><span class="card-chip">Step {index}</span><span class="card-chip card-chip-soft">{escape(calculator["category"])}</span></div>'
            f'<h3><a href="/calculators/{escape(slug)}/" data-workflow-step-calculator>{escape(calculator["name"])}</a></h3>'
            f'<p>{escape(calculator["intro"])}</p>'
            f'<a class="text-link" href="/calculators/{escape(slug)}/" data-workflow-step-calculator>Open calculator</a>'
            '</article>'
        )
    return "".join(cards)


def _guide_cards(workflow: dict, guides: dict[str, dict]) -> str:
    cards = []
    for slug in workflow.get("guide_slugs", []):
        guide = guides.get(slug)
        if not guide:
            continue
        cards.append(
            f'<article class="tool-card"><div class="card-chip-row"><span class="card-chip">Guide</span></div>'
            f'<h3><a href="/guides/{escape(slug)}/">{escape(guide["title"])}</a></h3>'
            f'<p>{escape(guide["description"])}</p></article>'
        )
    return "".join(cards)


def _ordered_steps(workflow: dict, calculators: dict[str, dict]) -> str:
    items = []
    for index, step in enumerate(workflow.get("steps", []), start=1):
        calculator = calculators.get(step.get("calculator_slug", ""))
        calculator_link = ""
        if calculator:
            calculator_link = (
                f'<a class="text-link" href="/calculators/{escape(calculator["slug"])}/" '
                f'data-workflow-step-calculator>Open {escape(calculator["name"])}</a>'
            )
        items.append(
            f'<article class="content-card prose-card workflow-step">'
            f'<div class="quality-kicker">Step {index}</div>'
            f'<h2>{escape(step["title"])}</h2>'
            f'<p>{escape(step["body"])}</p>'
            f'{calculator_link}'
            '</article>'
        )
    return "".join(items)


def _list_section(title: str, intro: str, items: list[str]) -> str:
    if not items:
        return ""
    item_html = "".join(f'<li>{escape(item)}</li>' for item in items)
    return (
        '<section class="conversion-panel workflow-list-panel">'
        f'<div class="section-head"><h2>{escape(title)}</h2><p>{escape(intro)}</p></div>'
        f'<ul class="conversion-list">{item_html}</ul>'
        '</section>'
    )


def _howto_schema(workflow: dict) -> str:
    steps = []
    for index, step in enumerate(workflow.get("steps", []), start=1):
        calculator_slug = step.get("calculator_slug")
        step_url = absolute_url(f'/workflows/{workflow["slug"]}/#step-{index}')
        if calculator_slug:
            step_url = absolute_url(f"/calculators/{calculator_slug}/")
        steps.append(
            {
                "@type": "HowToStep",
                "position": index,
                "name": step["title"],
                "text": step["body"],
                "url": step_url,
            }
        )
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "HowTo",
            "name": workflow["title"],
            "description": workflow["meta_description"],
            "step": steps,
        }
    )


def _item_list_schema(workflow: dict, calculators: dict[str, dict], guides: dict[str, dict]) -> str:
    items = []
    position = 1
    for slug in workflow.get("calculator_slugs", []):
        calculator = calculators.get(slug)
        if not calculator:
            continue
        items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": calculator["name"],
                "url": absolute_url(f"/calculators/{slug}/"),
            }
        )
        position += 1
    for slug in workflow.get("guide_slugs", []):
        guide = guides.get(slug)
        if not guide:
            continue
        items.append(
            {
                "@type": "ListItem",
                "position": position,
                "name": guide["title"],
                "url": absolute_url(f"/guides/{slug}/"),
            }
        )
        position += 1
    return json.dumps(
        {
            "@context": "https://schema.org",
            "@type": "ItemList",
            "name": f'{workflow["title"]} calculators and guides',
            "itemListElement": items,
        }
    )


def build_workflow_pages():
    calculators = family_lookup()
    guides = _guide_lookup()
    lookup = workflow_lookup()
    pages = []
    for workflow in get_all_workflows():
        path = f'/workflows/{workflow["slug"]}/'
        crumbs = [("Home", "/"), ("Workflows", "/workflows/"), (workflow["title"], path)]
        calculator_cards = _calculator_cards(workflow, calculators)
        guide_cards = _guide_cards(workflow, guides)
        related_cards = "".join(
            _workflow_card(lookup[slug], label="Related workflow")
            for slug in workflow.get("related_workflow_slugs", [])
            if slug in lookup
        )
        query_chips = "".join(
            f'<span class="card-chip card-chip-soft">{escape(query)}</span>'
            for query in workflow.get("primary_queries", [])
        )
        slot_name = f'workflow-{workflow["slug"]}-top'
        faq_html = "".join(
            f'<article class="content-card prose-card"><h2>{escape(item["q"])}</h2><p>{escape(item["a"])}</p></article>'
            for item in workflow.get("faqs", [])
        )
        content = (
            f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
            '<div class="eyebrow">Project planner</div>'
            f'<h1>{escape(workflow["headline"])}</h1>'
            f'<p class="hero-copy">{escape(workflow["intro"])}</p>'
            f'<div class="hero-badges"><span class="hero-badge">{len(workflow.get("calculator_slugs", []))} linked calculators</span><span class="hero-badge">Scope checklist</span><span class="hero-badge">Project sequence</span></div>'
            f'<div class="card-chip-row workflow-query-row">{query_chips}</div>'
            '</section>'
            f'{render_ad_slot(slot_name)}'
            f'{render_quality_strip("workflow")}'
            f'{_list_section("Measure first", "Take these measurements once, then reuse them through the calculators so the order, budget, and quote request stay aligned.", workflow.get("measure_first", []))}'
            '<section class="content-card prose-card"><h2>Planning order</h2><p>Work through the job in this order so the visible finish, hidden layers, accessories, and cost checks are not priced as separate guesses.</p></section>'
            f'<section class="stack-grid workflow-step-grid">{_ordered_steps(workflow, calculators)}</section>'
            '<section class="content-card prose-card"><h2>Calculators in this plan</h2><p>Each calculator covers one decision in the job: quantity, coverage, depth, fixings, accessories, or budget. Keep the outputs together when you build the buying list.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{calculator_cards}</div></section>'
            f'{_list_section("Material checklist", "Treat this as the first pass at the buying list. Add product names, sizes, grades, and exclusions before sending it for a price.", workflow.get("material_checklist", []))}'
            f'{_list_section("Common mistakes", "These are the places where tidy measurement maths often breaks once products, delivery, site access, and labour are involved.", workflow.get("common_mistakes", []))}'
            '<section class="conversion-panel conversion-panel-prominent">'
            '<div class="section-head"><h2>Brief to send for pricing</h2>'
            f'<p>{escape(workflow["quote_prompt"])}</p></div>'
            '<div class="conversion-actions"><a class="btn btn-primary" href="/quote-checklist/" data-workflow-quote-cta>Open quote checklist</a></div>'
            '</section>'
            f'<section class="content-card prose-card"><h2>Guides worth checking</h2><p>These pages cover the details that usually decide whether the calculator output is safe to order against.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{guide_cards}</div></section>'
            '<section class="content-card prose-card"><h2>Related project plans</h2><p>Open one of these when the job touches another surface, base layer, finish, or outdoor area.</p></section>'
            f'<section class="calculator-grid-section"><div class="calculator-grid">{related_cards}</div></section>'
            '<section class="content-card prose-card"><h2>Practical answers</h2><p>Short answers for the decisions that usually come up before ordering materials or sending a quote request.</p></section>'
            f'<section class="stack-grid">{faq_html}</section>'
            '</div>'
        )
        html = render_layout(
            title=workflow["meta_title"],
            description=workflow["meta_description"],
            path=path,
            content=content,
            schema=[
                render_breadcrumb_schema(crumbs),
                render_faq_schema(workflow.get("faqs", [])),
                _howto_schema(workflow),
                _item_list_schema(workflow, calculators, guides),
            ],
            page_type="workflow",
        )
        pages.append((path, html))
    return pages


def build_workflows_index() -> tuple[str, str]:
    workflows = get_all_workflows()
    path = "/workflows/"
    crumbs = [("Home", "/"), ("Workflows", path)]
    cards = "".join(_workflow_card(workflow, label="Project workflow") for workflow in workflows)
    content = (
        f'<div class="site-shell"><section class="hero hero-compact">{render_breadcrumbs(crumbs)}'
        '<div class="eyebrow">Planner library</div>'
        '<h1>Project planners for jobs that need more than one calculator</h1>'
        '<p class="hero-copy">Start here when a job has layers: a surface, a base, fixings, trims, prep, waste, and a quote to compare. Each planner keeps the related calculators and buying checks in one place.</p>'
        f'<div class="hero-badges"><span class="hero-badge">{len(workflows)} project planners</span><span class="hero-badge">Measured scope first</span><span class="hero-badge">Built for quote checks</span></div>'
        '</section>'
        f'{render_ad_slot("workflows-index-top")}'
        f'{render_quality_strip("workflow index")}'
        '<section class="content-card prose-card"><h2>Choose the closest job</h2><p>Pick the planner that matches the work, then adjust the measurements, products, and quote notes to fit the actual site.</p></section>'
        f'<section class="calculator-grid-section"><div class="calculator-grid">{cards}</div></section>'
        '</div>'
    )
    return path, render_layout(
        title=f'Project Workflows | BuildCostLab',
        description="Browse BuildCostLab workflows that connect calculators, guides, material checklists, and quote-prep steps for common building and home projects.",
        path=path,
        content=content,
        schema=[render_breadcrumb_schema(crumbs)],
        page_type="workflow-index",
    )
