import os
from core.config import TEMPLATES_DIR

def load_template(name: str) -> str:
    path = os.path.join(TEMPLATES_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def render_template(name: str, context: dict) -> str:
    html = load_template(name)
    # handle simple optional script placeholder
    script_tag = ""
    script_path = context.get("script_path", "").strip()
    if script_path:
        script_tag = f'<script src="{script_path}"></script>'
    html = html.replace("{{SCRIPT_TAG}}", script_tag)

    for key, value in context.items():
        if key == "script_path":
            continue
        html = html.replace(f"{{{{{key}}}}}", str(value))
    return html
