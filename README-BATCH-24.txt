BUILD COST LAB - BATCH 24 RESTORE

This fixes the regression from Batch 23.

What happened:
- Batch 23 replaced the stylesheet with a tiny placeholder file
- that removed the whole premium card layout and left plain text output

This batch restores:
- the light premium stylesheet
- the proper homepage structure
- the clean text logo (without the dark logo block)

Replace:
- assets/css/styles.css
- generators/homepage.py

Then rebuild:
python scripts/build.py
