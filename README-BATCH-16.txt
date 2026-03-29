BuildCostLab Batch 16

Theme: UK location landing pages

Included in this batch:
- New source data for UK region and city landing pages
- New generator for /locations/ index and individual location pages
- Build-script wiring so location pages are included in the site build, sitemap, and page inventory
- Navigation update to add Locations sitewide
- Homepage update to surface location pages
- Fully regenerated output/ so the new nav and locations section are already reflected in the built site

New published paths:
- /locations/
- /locations/london/
- /locations/south-east-england/
- /locations/south-west-england/
- /locations/midlands/
- /locations/north-of-england/
- /locations/scotland/
- /locations/wales/
- /locations/manchester/
- /locations/birmingham/
- /locations/leeds/
- /locations/bristol/
- /locations/edinburgh/
- /locations/glasgow/
- /locations/cardiff/

Files changed in source:
- data/locations.py (new)
- data/publisher.py
- generators/location_pages.py (new)
- generators/homepage.py
- scripts/build.py

Paste/merge the contents of this batch into your project root.
If you rebuild locally, run:
  python scripts/build.py
