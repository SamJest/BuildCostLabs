from html import escape

from data.catalog import get_all_calculators


def _score_related(current: dict, candidate: dict) -> int:
    score = 0
    if current["cluster_slug"] == candidate["cluster_slug"]:
        score += 100
    if current.get("category") == candidate.get("category"):
        score += 30
    current_tokens = set(current["slug"].replace("-calculator", "").split("-")) | set(current["name"].lower().replace("calculator", "").split())
    candidate_tokens = set(candidate["slug"].replace("-calculator", "").split("-")) | set(candidate["name"].lower().replace("calculator", "").split())
    score += len(current_tokens & candidate_tokens) * 8
    return score


def build_related_tools(current_slug: str = "", limit: int = 6) -> str:
    all_items = get_all_calculators()
    current = next((item for item in all_items if item["slug"] == current_slug), None)
    if current is None:
        candidates = all_items[:limit]
    else:
        candidates = sorted(
            (item for item in all_items if item["slug"] != current_slug),
            key=lambda item: (-_score_related(current, item), item["name"]),
        )[:limit]
    cards = []
    for item in candidates:
        label = "Same project hub" if current and item["cluster_slug"] == current["cluster_slug"] else item["category"]
        cards.append(
            '<a class="mini-tool-card mini-tool-card-rich" href="/calculators/{slug}/">'
            '<span class="mini-tool-label">{label}</span>'
            '<strong>{name}</strong>'
            '<span>{intro}</span>'
            '</a>'.format(
                slug=escape(item["slug"]),
                label=escape(label),
                name=escape(item["name"]),
                intro=escape(item["intro"]),
            )
        )
    return (
        '<section class="related-tools"><div class="section-head"><h2>Related calculators</h2>'
        '<p>Open the closest tool for the next part of the same job.</p></div>'
        f'<div class="mini-tool-grid mini-tool-grid-rich">{"".join(cards)}</div></section>'
    )
