BUILD MATE CALCULATORS - BATCH 16 FIX 2

This fixes the homepage import error:

ImportError: cannot import name 'HOME_SECTIONS' from 'data.site_content'

Problem:
- Batch 15/16 replaced data/site_content.py with a smaller version
- generators/homepage.py still expects HOME_HERO and HOME_SECTIONS

Fix:
- restores HOME_SECTIONS
- keeps the newer calculator intro entries, including fence
- keeps homepage copy compatible with your current homepage generator

Replace:
- data/site_content.py

Then run:
python scripts/build.py
