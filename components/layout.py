from __future__ import annotations

from html import escape


def build_header(site_config: dict) -> str:
    navigation = ''.join(
        f'<a href="{item["href"]}">{escape(item["label"])}' + '</a>'
        for item in site_config.get('header_navigation', [])
    )
    return f'''
<header class="site-header">
  <div class="container site-header-inner">
    <a class="site-brand" href="/">
      <span class="site-brand-mark">BM</span>
      <span class="site-brand-text-wrap">
        <span class="site-brand-text">{escape(site_config['brand_name'])}</span>
        <span class="site-brand-subtext">Project calculators for real jobs</span>
      </span>
    </a>
    <nav class="site-nav" aria-label="Primary navigation">
      {navigation}
    </nav>
  </div>
</header>'''


def build_footer(site_config: dict) -> str:
    footer_links = ''.join(
        f'<a href="{item["href"]}">{escape(item["label"])}' + '</a>'
        for item in site_config.get('footer_navigation', [])
    )
    return f'''
<footer class="site-footer">
  <div class="container site-footer-inner">
    <div>
      <strong>{escape(site_config['brand_name'])}</strong>
      <p>{escape(site_config['site_description'])}</p>
    </div>
    <div class="site-footer-links">{footer_links}</div>
  </div>
</footer>'''


def build_breadcrumbs(items: list[dict[str, str]]) -> str:
    rendered = []
    for index, item in enumerate(items):
        is_last = index == len(items) - 1
        if is_last:
            rendered.append(f'<span aria-current="page">{escape(item["label"])}' + '</span>')
        else:
            rendered.append(f'<a href="{item["href"]}">{escape(item["label"])}' + '</a>')
    return '<nav class="breadcrumbs" aria-label="Breadcrumbs">' + '<span class="breadcrumbs-sep">/</span>'.join(rendered) + '</nav>'
