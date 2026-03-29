# BuildCostLab

Calculator-first static publishing site for building material quantities, rough project costs, and supporting search-intent guides.

## Current build
- Homepage, calculator index, project hubs, guide library, location pages, and trust pages
- Calculator support content built around estimate -> sense-check -> compare -> quote brief
- Metric + imperial calculator support
- GBP, USD, and EUR result handling
- SEO metadata, sitemap, robots, schema, favicon, and social image output
- GitHub Pages-friendly output including `CNAME` and `.nojekyll`

## Important content rule
This site should not scale by cloning the same support copy onto every calculator page. Each important page needs its own:
- assumptions
- worked examples or scenario checks
- trade-offs
- practical buying or quoting guidance
- related links
- intent-specific copy

The publishing pipeline is designed around calculator families, project hubs, supporting guides, location planning pages, and repeatable SEO structure rather than thin duplicate pages.

## Build
```bash
python scripts/build.py
```

By default the site is built into `docs/` so GitHub Pages can publish directly from the `main` branch.

## Deploy from main branch
1. In GitHub Pages settings, choose **Deploy from a branch**.
2. Select **main** as the branch.
3. Select **/docs** as the folder.
4. Build locally with `python scripts/build.py`.
5. Commit the updated `docs/` output and push to `main`.

This repo does not need GitHub Actions or a `gh-pages` branch for publishing.
