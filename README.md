# BuildMate Calculators

Static calculator site scaffold for practical material and project estimators.

## Current build
- Homepage
- Calculator index page
- Live paint calculator page
- Metric + imperial support
- Mode toggles for walls, ceiling-only and single-surface estimates
- Result summary, breakdown, tin suggestions and calculation steps

## Important content rule
This site should not scale by cloning the same support copy onto every calculator page.
Each calculator needs its own:
- assumptions
- mistakes
- use cases
- FAQs
- related links
- intent-specific copy

The paint calculator generator is the reference pattern for that approach.

## Build
```bash
python scripts/build.py
```
