from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

DIRECTORIES = [
    "assets",
    "assets/css",
    "assets/js",
    "assets/images",
    "components",
    "components/__pycache__",
    "core",
    "data",
    "data/calculators",
    "data/pages",
    "data/site",
    "generators",
    "output",
    "output/calculators",
    "output/assets",
    "output/assets/css",
    "output/assets/js",
    "output/assets/images",
    "scripts",
    "templates",
    "utils",
]

FILES = {
    ".gitignore": """# Python\n__pycache__/\n*.pyc\n\n# Build output\noutput/\n\n# OS files\n.DS_Store\nThumbs.db\n""",
    "README.md": """# Calculator Site Scaffold\n\nThis project is a Python-based static site generator scaffold for an evergreen calculator / estimator pSEO site.\n\n## Current structure\n- `assets/` static frontend files\n- `components/` reusable HTML section builders\n- `core/` site-wide config + build helpers\n- `data/` calculator datasets and site metadata\n- `generators/` page generation modules\n- `templates/` HTML templates\n- `utils/` helper utilities\n- `output/` generated static site\n- `scripts/` setup / utility scripts\n\n## First run\n```bash\npython scripts/generate_scaffold.py\n```\n""",
    "assets/css/site.css": """/* Base stylesheet placeholder */\n:root {\n  --bg: #0b1020;\n  --panel: #121933;\n  --text: #f5f7ff;\n  --muted: #aab3d1;\n  --accent: #f2c14e;\n}\n\nhtml, body {\n  margin: 0;\n  padding: 0;\n  font-family: Arial, sans-serif;\n  background: var(--bg);\n  color: var(--text);\n}\n""",
    "assets/js/site.js": """// Base JS placeholder\nconsole.log('site.js loaded');\n""",
    "components/__init__.py": "",
    "components/layout.py": """from __future__ import annotations\n\n\ndef build_header(site_name: str) -> str:\n    return f'<header class="site-header"><div class="container"><a href="/">{site_name}</a></div></header>'\n\n\ndef build_footer(site_name: str) -> str:\n    return f'<footer class="site-footer"><div class="container">&copy; {site_name}</div></footer>'\n""",
    "core/__init__.py": "",
    "core/config.py": """from __future__ import annotations\n\nfrom pathlib import Path\n\nROOT_DIR = Path(__file__).resolve().parent.parent\nASSETS_DIR = ROOT_DIR / 'assets'\nDATA_DIR = ROOT_DIR / 'data'\nOUTPUT_DIR = ROOT_DIR / 'output'\nTEMPLATES_DIR = ROOT_DIR / 'templates'\n\nSITE_CONFIG = {\n    'site_name': 'Project Calculator',\n    'site_url': 'https://example.com',\n    'site_description': 'Evergreen calculators and estimators.',\n    'brand_name': 'Project Calculator',\n    'locale': 'en-GB',\n}\n""",
    "core/io.py": """from __future__ import annotations\n\nfrom pathlib import Path\n\n\ndef ensure_dir(path: Path) -> None:\n    path.mkdir(parents=True, exist_ok=True)\n\n\ndef write_text(path: Path, content: str) -> None:\n    path.parent.mkdir(parents=True, exist_ok=True)\n    path.write_text(content, encoding='utf-8')\n""",
    "data/site/site.json": json.dumps({
        "site_name": "Project Calculator",
        "site_url": "https://example.com",
        "site_description": "Evergreen calculators and estimators.",
        "locale": "en-GB"
    }, indent=2),
    "data/calculators/calculators.json": json.dumps([
        {
            "slug": "brick-calculator",
            "name": "Brick Calculator",
            "category": "building",
            "status": "planned"
        },
        {
            "slug": "paint-calculator",
            "name": "Paint Calculator",
            "category": "decorating",
            "status": "planned"
        }
    ], indent=2),
    "data/pages/homepage.json": json.dumps({
        "title": "Project Calculator",
        "hero_heading": "Simple calculators for real projects",
        "hero_text": "Estimate materials, costs, and quantities in seconds."
    }, indent=2),
    "generators/__init__.py": "",
    "generators/build_homepage.py": """from __future__ import annotations\n\nimport json\nfrom pathlib import Path\n\nfrom components.layout import build_footer, build_header\nfrom core.config import DATA_DIR, OUTPUT_DIR, SITE_CONFIG\nfrom core.io import ensure_dir, write_text\n\n\ndef build_homepage() -> None:\n    homepage_path = DATA_DIR / 'pages' / 'homepage.json'\n    homepage_data = json.loads(homepage_path.read_text(encoding='utf-8'))\n\n    html = f'''<!doctype html>\n<html lang="en-GB">\n<head>\n  <meta charset="utf-8">\n  <meta name="viewport" content="width=device-width, initial-scale=1">\n  <title>{homepage_data['title']}</title>\n  <meta name="description" content="{SITE_CONFIG['site_description']}">\n  <link rel="stylesheet" href="/assets/css/site.css">\n</head>\n<body>\n  {build_header(SITE_CONFIG['site_name'])}\n  <main>\n    <section class="hero">\n      <div class="container">\n        <h1>{homepage_data['hero_heading']}</h1>\n        <p>{homepage_data['hero_text']}</p>\n      </div>\n    </section>\n  </main>\n  {build_footer(SITE_CONFIG['site_name'])}\n  <script src="/assets/js/site.js"></script>\n</body>\n</html>'''\n\n    ensure_dir(OUTPUT_DIR)\n    write_text(OUTPUT_DIR / 'index.html', html)\n\n\nif __name__ == '__main__':\n    build_homepage()\n""",
    "scripts/build.py": """from __future__ import annotations\n\nimport shutil\nfrom pathlib import Path\n\nfrom core.config import ASSETS_DIR, OUTPUT_DIR\nfrom core.io import ensure_dir\nfrom generators.build_homepage import build_homepage\n\n\ndef copy_assets() -> None:\n    target = OUTPUT_DIR / 'assets'\n    if target.exists():\n        shutil.rmtree(target)\n    shutil.copytree(ASSETS_DIR, target)\n\n\ndef build_site() -> None:\n    ensure_dir(OUTPUT_DIR)\n    build_homepage()\n    copy_assets()\n    print('Build complete.')\n\n\nif __name__ == '__main__':\n    build_site()\n""",
    "templates/base.html": """<!doctype html>\n<html lang=\"en-GB\">\n<head>\n  <meta charset=\"utf-8\">\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n  <title>{{ title }}</title>\n</head>\n<body>\n  {{ body }}\n</body>\n</html>\n""",
    "utils/__init__.py": "",
    "utils/slugify.py": """from __future__ import annotations\n\nimport re\n\n\ndef slugify(value: str) -> str:\n    value = value.strip().lower()\n    value = re.sub(r'[^a-z0-9]+', '-', value)\n    return value.strip('-')\n""",
}

PLACEHOLDER_INIT_DIRS = [
    "components",
    "core",
    "generators",
    "utils",
]


def create_directories() -> None:
    for rel_path in DIRECTORIES:
        if rel_path.endswith("__pycache__"):
            continue
        (ROOT / rel_path).mkdir(parents=True, exist_ok=True)


def create_files() -> None:
    for rel_path, content in FILES.items():
        path = ROOT / rel_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content if isinstance(content, str) else str(content), encoding="utf-8")


def main() -> None:
    create_directories()
    create_files()
    print(f"Scaffold created at: {ROOT}")


if __name__ == "__main__":
    main()
