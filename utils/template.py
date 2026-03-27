from pathlib import Path
import re


def render_template(template_path: Path, context: dict) -> str:
    html = template_path.read_text(encoding="utf-8")

    def handle_if(match):
        key = match.group(1).strip()
        inner = match.group(2)
        return inner if context.get(key) else ''

    html = re.sub(r"\{% if ([^%]+?) %\}(.*?)\{% endif %\}", handle_if, html, flags=re.DOTALL)

    for key, value in context.items():
        html = html.replace('{{ ' + key + ' }}', str(value))

    return html
