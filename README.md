# BuildCostLab

Calculator-first static publishing site for building material quantities, rough project costs, and supporting search-intent guides.

## Current build
- Homepage, calculator index, cluster hubs, guide library, and trust pages
- 50+ calculator pages with structured support content
- Metric + imperial calculator support
- GBP, USD, and EUR result handling
- SEO metadata, sitemap, robots, schema, favicon, and social image output
- GitHub Pages-friendly build output including `CNAME` and `.nojekyll`

## Important content rule
This site should not scale by cloning the same support copy onto every calculator page. Each calculator needs its own:
- assumptions
- mistakes
- use cases
- FAQs
- related links
- intent-specific copy

The publishing pipeline is designed around calculator families, cluster hubs, supporting guides, and repeatable SEO structure rather than thin duplicate pages.

## Build
```bash
python scripts/build.py
```
