import sys
import shutil
import importlib
import json
import re
from pathlib import Path

CURRENT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = CURRENT_DIR.parent

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from core.config import ASSETS_DIR, OUTPUT_DIR
from generators.homepage import build_homepage
from generators.calculators_index import build_calculator_cards, build_calculators_index
from generators.publisher_pages import (
    build_cluster_pages,
    build_clusters_index,
    build_guide_pages,
    build_guides_index,
    build_trust_pages,
    build_compare_index,
)
from generators.scale_calculators import build_additional_calculator_pages
from data.catalog import get_all_calculators
from data.publisher import SITE, TRUST_PAGES

CALCULATOR_TARGETS = [
    ("paint_calculator", "paint-calculator", "paint"),
    ("tile_calculator", "tile-calculator", "tile"),
    ("flooring_calculator", "flooring-calculator", "flooring"),
    ("concrete_calculator", "concrete-calculator", "concrete"),
    ("gravel_calculator", "gravel-calculator", "gravel"),
    ("decking_calculator", "decking-calculator", "decking"),
    ("paving_calculator", "paving-calculator", "paving"),
    ("fence_calculator", "fence-calculator", "fence"),
]

def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")

def clean_output() -> None:
    if OUTPUT_DIR.exists():
        shutil.rmtree(OUTPUT_DIR)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def copy_assets() -> None:
    if ASSETS_DIR.exists():
        shutil.copytree(ASSETS_DIR, OUTPUT_DIR / "assets", dirs_exist_ok=True)

def get_candidate_function_names(base_key: str):
    return [
        f"build_{base_key}_calculator_page",
        f"build_{base_key}_page",
        f"generate_{base_key}_calculator_page",
        f"generate_{base_key}_page",
        f"render_{base_key}_calculator_page",
        f"render_{base_key}_page",
        f"build_{base_key}_calculator",
        f"generate_{base_key}_calculator",
        f"render_{base_key}_calculator",
        f"build_{base_key}",
        f"generate_{base_key}",
        f"render_{base_key}",
    ]

def find_builder(module, base_key: str):
    for function_name in get_candidate_function_names(base_key):
        builder = getattr(module, function_name, None)
        if callable(builder):
            return function_name, builder
    return None, None

def build_dynamic_calculators():
    for module_name, slug, base_key in CALCULATOR_TARGETS:
        full_module_name = f"generators.{module_name}"
        try:
            module = importlib.import_module(full_module_name)
        except ModuleNotFoundError:
            print(f"Skipped missing module: {full_module_name}")
            continue
        except Exception as exc:
            print(f"Failed importing {full_module_name}: {exc}")
            continue
        function_name, builder = find_builder(module, base_key)
        if builder is None:
            print(f"Skipped {full_module_name}: no matching builder function found for key '{base_key}'")
            continue
        try:
            html = builder()
            if not isinstance(html, str) or not html.strip():
                print(f"Skipped {full_module_name}.{function_name}: builder returned no HTML")
                continue
            write_file(OUTPUT_DIR / "calculators" / slug / "index.html", html)
            print(f"Built: /calculators/{slug}/ using {full_module_name}.{function_name}")
        except Exception as exc:
            print(f"Failed building {full_module_name}.{function_name}: {exc}")

def build_site() -> None:
    cards_html = build_calculator_cards()
    write_file(OUTPUT_DIR / "index.html", build_homepage(cards_html))
    write_file(OUTPUT_DIR / "calculators" / "index.html", build_calculators_index(cards_html))
    build_dynamic_calculators()
    for slug, html in build_additional_calculator_pages():
        write_file(OUTPUT_DIR / "calculators" / slug / "index.html", html)
    for path, html in build_trust_pages():
        write_file(OUTPUT_DIR / path.strip("/") / "index.html", html)
    for path, html in build_cluster_pages():
        write_file(OUTPUT_DIR / path.strip("/") / "index.html", html)
    for path, html in build_guide_pages():
        write_file(OUTPUT_DIR / path.strip("/") / "index.html", html)
    guide_index_path, guide_index_html = build_guides_index()
    write_file(OUTPUT_DIR / guide_index_path.strip("/") / "index.html", guide_index_html)
    compare_index_path, compare_index_html = build_compare_index()
    write_file(OUTPUT_DIR / compare_index_path.strip("/") / "index.html", compare_index_html)
    cluster_index_path, cluster_index_html = build_clusters_index()
    write_file(OUTPUT_DIR / cluster_index_path.strip("/") / "index.html", cluster_index_html)
    write_file(OUTPUT_DIR / "robots.txt", build_robots())
    write_file(OUTPUT_DIR / "sitemap.xml", build_sitemap())
    write_file(OUTPUT_DIR / "page-inventory.json", build_page_inventory())
    write_file(OUTPUT_DIR / "seo-report.json", build_seo_report())
    write_file(OUTPUT_DIR / "launch-readiness-report.json", build_launch_readiness_report())
    write_file(OUTPUT_DIR / "CNAME", build_cname())
    write_file(OUTPUT_DIR / ".nojekyll", "")


def build_robots() -> str:
    return f"User-agent: *\nAllow: /\nSitemap: {SITE['base_url']}/sitemap.xml\n"


def build_cname() -> str:
    return f"{SITE['domain']}\n"


def build_sitemap() -> str:
    pages = ["/", "/calculators/", "/clusters/", "/guides/", "/compare/"]
    pages.extend(f"/{page['slug']}/" for page in TRUST_PAGES)
    calculators = get_all_calculators()
    pages.extend(f"/calculators/{item['slug']}/" for item in calculators)
    seen_clusters = set()
    for item in calculators:
        if item["cluster_slug"] not in seen_clusters:
            pages.append(f"/clusters/{item['cluster_slug']}/")
            seen_clusters.add(item["cluster_slug"])
        pages.extend(f"/guides/{guide['slug']}/" for guide in item["intent_pages"] + item["guide_pages"])
    urls = "".join(f"<url><loc>{SITE['base_url']}{path}</loc></url>" for path in pages)
    return f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>'


def build_page_inventory() -> str:
    pages = [{"path": "/compare/", "type": "compare-index"}]
    pages.extend({"path": f"/{page['slug']}/", "type": "trust"} for page in TRUST_PAGES)
    calculators = get_all_calculators()
    pages.extend({"path": f"/calculators/{item['slug']}/", "type": "calculator", "cluster": item["cluster_slug"]} for item in calculators)
    seen_clusters = set()
    for item in calculators:
        if item["cluster_slug"] not in seen_clusters:
            pages.append({"path": f"/clusters/{item['cluster_slug']}/", "type": "cluster"})
            seen_clusters.add(item["cluster_slug"])
        pages.extend({"path": f"/guides/{guide['slug']}/", "type": "guide", "cluster": item["cluster_slug"]} for guide in item["intent_pages"] + item["guide_pages"])
    return json.dumps({"site": SITE["name"], "count": len(pages), "pages": pages}, indent=2)


def build_launch_readiness_report() -> str:
    inventory = json.loads(build_page_inventory())
    seo = json.loads(build_seo_report())
    calculators = [item for item in inventory["pages"] if item.get("type") == "calculator"]
    guides = [item for item in inventory["pages"] if item.get("type") == "guide"]
    clusters = [item for item in inventory["pages"] if item.get("type") == "cluster"]
    trust_pages = [item for item in inventory["pages"] if item.get("type") == "trust"]
    compare_pages = [item for item in inventory["pages"] if item.get("type") == "compare-index"]
    html_pages = list(OUTPUT_DIR.rglob("index.html"))
    schema_counts = {"faq": 0, "item_list": 0, "software_application": 0, "breadcrumb": 0}
    for html_path in html_pages:
        content = html_path.read_text(encoding="utf-8")
        if '"@type": "FAQPage"' in content:
            schema_counts["faq"] += 1
        if '"@type": "ItemList"' in content:
            schema_counts["item_list"] += 1
        if '"@type": "SoftwareApplication"' in content:
            schema_counts["software_application"] += 1
        if '"@type": "BreadcrumbList"' in content:
            schema_counts["breadcrumb"] += 1

    required_paths = [
        "/",
        "/calculators/",
        "/guides/",
        "/clusters/",
        "/compare/",
        SITE.get("methodology_path", "/calculator-methodology/"),
        SITE.get("editorial_policy_path", "/editorial-policy/"),
        SITE.get("quote_contact_path", "/contact/"),
    ]
    existing_paths = {page["path"] for page in inventory["pages"]}
    existing_paths.add("/")
    existing_paths.add("/calculators/")
    existing_paths.add("/guides/")
    existing_paths.add("/clusters/")
    missing_required = [path for path in required_paths if path not in existing_paths]

    project_cost_count = sum(1 for item in get_all_calculators() if item.get("formula") == "project_cost")

    readiness_checks = {
        "required_pages_present": not missing_required,
        "seo_report_clean": len(seo.get("issues", [])) == 0,
        "calculators_present": len(calculators) >= 10,
        "guides_present": len(guides) >= 20,
        "clusters_present": len(clusters) >= 5,
        "trust_pages_present": len(trust_pages) >= 5,
        "compare_hub_present": len(compare_pages) == 1,
        "project_cost_family_present": project_cost_count >= 4,
        "calculator_schema_present": schema_counts["software_application"] >= project_cost_count,
    }

    return json.dumps(
        {
            "site": SITE["name"],
            "generated_on": SITE.get("updated_iso", "2026-03-29"),
            "counts": {
                "pages": inventory["count"],
                "calculators": len(calculators),
                "guides": len(guides),
                "clusters": len(clusters),
                "trust_pages": len(trust_pages),
                "project_cost_calculators": project_cost_count,
            },
            "schema_counts": schema_counts,
            "missing_required_paths": missing_required,
            "readiness_checks": readiness_checks,
            "seo_summary": {
                "issues": len(seo.get("issues", [])),
                "duplicate_titles": len(seo.get("duplicate_titles", {})),
                "duplicate_descriptions": len(seo.get("duplicate_descriptions", {})),
            },
        },
        indent=2,
    )


def build_seo_report() -> str:
    title_pattern = re.compile(r"<title>(.*?)</title>", re.IGNORECASE | re.DOTALL)
    description_pattern = re.compile(r'<meta name="description" content="(.*?)">', re.IGNORECASE)
    canonical_pattern = re.compile(r'<link rel="canonical" href="(.*?)">', re.IGNORECASE)

    pages = []
    title_map = {}
    description_map = {}
    issues = []

    for html_path in OUTPUT_DIR.rglob("index.html"):
        content = html_path.read_text(encoding="utf-8")
        rel_path = "/" + html_path.relative_to(OUTPUT_DIR).as_posix().removesuffix("index.html")
        title_match = title_pattern.search(content)
        description_match = description_pattern.search(content)
        canonical_match = canonical_pattern.search(content)

        title = title_match.group(1).strip() if title_match else ""
        description = description_match.group(1).strip() if description_match else ""
        canonical = canonical_match.group(1).strip() if canonical_match else ""

        pages.append({"path": rel_path, "title": title, "description": description, "canonical": canonical})
        if title:
            title_map.setdefault(title, []).append(rel_path)
        else:
            issues.append({"path": rel_path, "issue": "missing_title"})
        if description:
            description_map.setdefault(description, []).append(rel_path)
        else:
            issues.append({"path": rel_path, "issue": "missing_description"})
        if not canonical:
            issues.append({"path": rel_path, "issue": "missing_canonical"})

    duplicate_titles = {key: value for key, value in title_map.items() if len(value) > 1}
    duplicate_descriptions = {key: value for key, value in description_map.items() if len(value) > 1}

    return json.dumps(
        {
            "page_count": len(pages),
            "issues": issues,
            "duplicate_titles": duplicate_titles,
            "duplicate_descriptions": duplicate_descriptions,
        },
        indent=2,
    )

def main():
    print("=== BUILD START ===")
    clean_output()
    copy_assets()
    build_site()
    print("=== BUILD COMPLETE ===")

if __name__ == "__main__":
    main()
