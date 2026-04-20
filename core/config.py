import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Main paths
ASSETS_DIR = PROJECT_ROOT / "assets"
OUTPUT_DIR = Path(os.environ.get("BUILD_OUTPUT_DIR", str(PROJECT_ROOT / "docs")))
TEMPLATES_DIR = PROJECT_ROOT / "templates"
DATA_DIR = PROJECT_ROOT / "data"
GENERATORS_DIR = PROJECT_ROOT / "generators"
CORE_DIR = PROJECT_ROOT / "core"
UTILS_DIR = PROJECT_ROOT / "utils"
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# Common aliases for older modules
ROOT_DIR = PROJECT_ROOT
BASE_DIR = PROJECT_ROOT
STATIC_DIR = ASSETS_DIR

# Site config
SITE_NAME = "BuildCostLab"
SITE_TAGLINE = "Calculator-first guides for materials, quantities, and rough project costs"
BASE_URL = "https://buildcostlab.com"

# Basic helper values older modules may expect
SITE_URL = BASE_URL
OUTPUT_PATH = OUTPUT_DIR
TEMPLATES_PATH = TEMPLATES_DIR
ASSETS_PATH = ASSETS_DIR
