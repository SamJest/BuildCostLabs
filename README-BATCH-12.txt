BuildCostLabs Batch 12 — Non-empty calculator landing states

What changed
- Replaced static “Waiting for inputs” calculator intelligence panels with useful benchmark content.
- Auto-runs the starter/default scenario on calculator load so pages open with a live estimate instead of an empty state.
- Added starter-state summary rows to generic calculator result panels.
- Fixed the tile calculator preset placement bug while updating the starter load behaviour.

Included source files
- assets/js/cost-intelligence.js
- assets/js/generic-material-calculator.js
- assets/js/concrete-calculator.js
- assets/js/decking-calculator.js
- assets/js/fence.js
- assets/js/flooring-calculator.js
- assets/js/gravel-calculator.js
- assets/js/paving-calculator.js
- assets/js/tile-calculator.js
- generators/publisher_pages.py

Included built output
- output/assets/js/* for the updated calculator scripts
- output/calculators/* regenerated so calculator pages now ship with benchmark placeholder content instead of empty “waiting” blocks

Merge notes
- Paste/merge into the project root.
- If you rebuild locally, these source changes will regenerate the same calculator behaviour.
