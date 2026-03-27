from html import escape

from data.catalog import get_all_calculators


def build_related_tools(current_slug: str = "") -> str:
    cards = []
    for item in get_all_calculators():
        if item["slug"] == current_slug:
            continue
        cards.append(
            f'<a class="mini-tool-card" href="/calculators/{escape(item["slug"])}/">{escape(item["name"])}</a>'
        )
    return (
        '<section class="related-tools"><div class="section-head"><h2>Related calculators</h2>'
        '<p>Open another tool for the next part of the job.</p></div>'
        f'<div class="mini-tool-grid">{"".join(cards)}</div></section>'
    )
