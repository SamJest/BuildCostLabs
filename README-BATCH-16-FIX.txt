BUILD MATE CALCULATORS - BATCH 16 FIX

This fixes the import-path issue in Batch 16.

Problem:
- scripts/build.py was using project imports without adding the project root to sys.path

Fix:
- restores proper project-root import handling
- keeps the existing multi-calculator build flow
- adds fence-calculator to the builder target list instead of replacing the whole build system

Replace:
- scripts/build.py
- generators/fence_calculator.py
- assets/js/fence.js

Then run:
python scripts/build.py
