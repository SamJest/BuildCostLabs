BUILD MATE CALCULATORS - BATCH 12 ROUTE FIX

Problem fixed in this batch:
- The site built successfully, but only gravel existed in /output/calculators/
- Older calculator generator modules were present, but the new build script only knew one exact
  builder function name per file.
- Your older generator files use different function names, so they were being skipped silently.

What this batch does:
1. Replaces scripts/build.py with a compatibility-first builder.
2. It tries multiple common builder function names for each calculator module:
   - build_paint_calculator_page
   - build_paint_page
   - generate_paint_calculator_page
   - generate_paint_page
   - render_paint_calculator_page
   - render_paint_page
   - and similar patterns for tile / flooring / concrete / gravel
3. Prints exactly which pages were built and which modules were skipped.
4. Writes a route report into output/_build_report.txt so you can see what happened.

Replace:
- scripts/build.py

Then rebuild:
python scripts/build.py
