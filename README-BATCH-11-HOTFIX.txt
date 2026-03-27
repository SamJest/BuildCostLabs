BUILD MATE CALCULATORS - BATCH 11 HOTFIX

This is a targeted hotfix for the import error:

ImportError: cannot import name 'TEMPLATES_DIR' from 'core.config'

What happened:
- Earlier calculator generator files still expect older config names.
- Batch 10's config no longer exposed all of those constants.

What this hotfix does:
- Restores the older config constants while keeping the current project setup.
- Makes the newer build.py compatible with the older generator modules.

Replace:
- core/config.py

Then rebuild:
python scripts/build.py
