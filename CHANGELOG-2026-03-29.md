# BuildCostLab changelog — 2026-03-29

## What changed
- Removed internal audit-style wording and competitor/comparison language from shared generators, navigation copy, listing pages, and reusable content.
- Renamed the user-facing "Tool Sets" IA label to **Project Hubs** across navigation, cards, breadcrumbs, footer links, helper text, and generated page copy while preserving the existing `/clusters/` URLs.
- Reworked the shared publishing layer so core trust signals now appear more consistently across page types.
- Upgraded homepage and calculator index messaging around the main workflow: estimate, sense-check, compare, and prepare a quote brief.

## Trust improvements
- Expanded the trust center content for:
  - About
  - Calculator Methodology
  - Editorial Policy
  - Contact
- Added stronger, honest planning-aid disclaimers and clearer guidance on how estimates should be used.
- Added clearer trust/navigation links in the footer and more explicit methodology/editorial references in shared page templates.

## Content depth improvements
- Enhanced calculator-page support sections with:
  - quick summaries
  - scope and exclusions
  - assumptions
  - worked examples
  - cost/quantity drivers
  - practical buying checks
  - quote-ready checklist panels
  - stronger guide and hub linking
- Enhanced guide-page templates with:
  - clearer direct answers
  - trade-off framing
  - scenario/example panels
  - practical checklists
  - stronger next-step linking
- Upgraded project hub pages to work more clearly as grouped decision-support destinations.
- Upgraded location pages with more useful structured local planning notes covering access, delivery, weather, site constraints, quote comparison, and local question prompts.

## Compatibility and routing
- Kept existing `/clusters/` URLs in place for backward compatibility.
- No redirect layer was required because the IA rename was handled at the label/copy layer rather than by changing paths.

## Build and validation
- Rebuilt the site successfully with `python scripts/build.py`.
- Generated deployable output in `output/`.
- Verified there are no broken internal links in the generated site.
- Verified the generated output no longer contains banned internal wording or the old "Tool Sets" label.
