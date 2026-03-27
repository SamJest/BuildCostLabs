BUILD MATE CALCULATORS - BATCH 13 RESTORE

What your build report showed:
- paint module exists, but its builder returned no HTML
- tile / flooring / concrete generator modules do not exist
- gravel works

What this batch does:
1. Replaces generators/paint_calculator.py with a working HTML page builder.
2. Adds missing generators:
   - generators/tile_calculator.py
   - generators/flooring_calculator.py
   - generators/concrete_calculator.py
3. Adds matching JS files:
   - assets/js/paint-calculator.js
   - assets/js/tile-calculator.js
   - assets/js/flooring-calculator.js
   - assets/js/concrete-calculator.js
4. Every calculator in this batch includes:
   - result
   - breakdown
   - calculation notes
   - price per unit field
   - estimated material cost

Replace these files in your project, then rebuild:
python scripts/build.py
