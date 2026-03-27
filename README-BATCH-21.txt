BUILD COST LAB - BATCH 21 VISUAL FIX

This batch fixes the regression from the previous rebrand batch.

What it restores:
- premium card layout
- lighter futuristic look
- modern gradients / glow / panels
- homepage card grid
- better calculator/result card styling

What it keeps:
- BuildCostLab branding
- dark/futuristic direction (but much lighter than the last batch)
- compatibility with your existing build.py expecting build_homepage(cards_html)

Replace:
- assets/css/styles.css
- generators/homepage.py

Then rebuild:
python scripts/build.py
