BUILD MATE CALCULATORS - BATCH 10

This batch fixes the broken calculator routing introduced in Batch 9.

What happened:
- Batch 9's build.py only rebuilt the homepage, calculators index and gravel calculator.
- The older calculator pages were not being regenerated, so the homepage linked to URLs that no longer existed.

What this batch does:
1. Fixes build.py so it rebuilds any existing calculator generator modules it can find:
   - paint_calculator.py
   - tile_calculator.py
   - flooring_calculator.py
   - concrete_calculator.py
   - gravel_calculator.py
2. Keeps the homepage text rewrite and new homepage layout.
3. Updates the calculators index copy to feel less templated.
4. Adds a reusable pricing UI pattern file for the next calculator pass.
5. Updates the gravel calculator to include price-per-unit and estimated cost.

Replace these files in your project, then rebuild:
- scripts/build.py
- generators/homepage.py
- generators/calculators_index.py
- generators/gravel_calculator.py
- assets/js/gravel-calculator.js
- assets/css/styles.css
- assets/js/cost-pattern.js
- data/site_content.py
