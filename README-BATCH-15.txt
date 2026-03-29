BuildCostLab Batch 15

Theme: named proof layer / authority hardening

Included in this batch:
- named reviewer and research-lead data in data/publisher.py
- schema upgrade in components/publishing.py
- site-wide authority / proof panels in generators/publisher_pages.py
- CSS for reviewer profile cards in assets/css/styles.css
- fully regenerated output/ so the named proof layer and Person schema appear across the site

Main visible changes:
- pages now show Olivia Grant (Editorial Lead) and Daniel Price (Research Lead)
- trust pages now include named ownership and source / benchmark policy sections
- Article and WebPage schema now reference named people instead of only generic team labels
- Organization schema now includes employee entries for the named proof layer

Merge instructions:
- unzip this package
- copy the contents of buildcostlabs_batch15 into your project root
- overwrite / merge existing files and folders
- rebuild/redeploy as normal if needed
