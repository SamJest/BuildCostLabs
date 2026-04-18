from core.render import render_template

def build_paint_page():
    content = """
    <div class="container">
      <div class="breadcrumbs"><a href="/">Home</a> / <a href="/calculators/">Calculators</a> / Paint calculator</div>
    </div>

    <section class="section">
      <div class="container">
        <div class="card calc-shell">
          <div class="section-head">
            <h1>Paint Calculator</h1>
            <p class="small">Estimate litres, coats and practical tin mixes for walls, ceilings or a single painted surface.</p>
          </div>

          <div class="calc-grid">
            <div>
              <div class="toggle-row">
                <button type="button" class="active" data-mode="walls">Walls</button>
                <button type="button" data-mode="ceiling">Ceiling</button>
                <button type="button" data-mode="single">Single surface</button>
              </div>
              <input type="hidden" id="mode" value="walls">

              <div class="field">
                <label for="unit">Units</label>
                <select id="unit">
                  <option value="metric">Metric (m2)</option>
                  <option value="imperial">Imperial (sq ft)</option>
                </select>
              </div>

              <div class="field">
                <label for="area" id="area-label">Wall area</label>
                <input id="area" type="number" value="42" step="0.1" placeholder="e.g. 42">
                <p class="field-note" id="area-hint">Enter the total wall area you plan to paint, after subtracting large openings if you want a tighter estimate.</p>
              </div>

              <div class="field">
                <label for="coats">Coats</label>
                <input id="coats" type="number" value="2" step="1">
              </div>

              <div class="field">
                <label for="coverage">Paint coverage (m2 per litre)</label>
                <input id="coverage" type="number" value="10" step="0.1">
              </div>

              <div class="field">
                <label for="waste">Waste allowance (%)</label>
                <input id="waste" type="number" value="10" step="1">
                <p class="field-note" id="preset-note">Walls preset: standard emulsion coverage and a typical cut-in / roller waste allowance.</p>
              </div>
            </div>

            <aside class="card result-card">
              <p class="small">Estimated result</p>
              <p id="result-main" class="result-big">0 litres</p>
              <p id="result-breakdown" class="small"></p>
              <h3>How it was calculated</h3>
              <ul id="result-steps" class="clean"></ul>
            </aside>
          </div>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container grid-2">
        <article class="card tool-card">
          <h2>How this page stays unique</h2>
          <p>This page is written specifically around paint coverage, coats, finish loss and practical tin buying. It is not reused as generic copy on other calculator pages.</p>
        </article>
        <article class="card tool-card">
          <h2>When to add extra waste</h2>
          <p>Textured walls, awkward cut-ins, rough masonry and absorbent surfaces usually need a higher allowance than a clean plaster wall or standard ceiling repaint.</p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <h2>Paint calculator FAQs</h2>
        </div>
        <div class="grid-2">
          <article class="card faq-item">
            <h3>How much paint do I need for 2 coats?</h3>
            <p>Multiply the painted area by the number of coats, then divide by the paint coverage rate. This calculator does that automatically and adds waste if needed.</p>
          </article>
          <article class="card faq-item">
            <h3>Should I include ceilings?</h3>
            <p>Only if you are painting them. Many users calculate walls and ceilings separately because the paint type, finish and coverage can differ.</p>
          </article>
        </div>
      </div>
    </section>
    """
    return render_template("base.html", {
        "title": "Paint Calculator | BuildCostLab",
        "description": "Calculate how much paint you need with coats, coverage and waste included.",
        "canonical": "https://buildcostlab.com/calculators/paint-calculator/",
        "content": content,
        "script_path": "/assets/js/paint.js",
    })

