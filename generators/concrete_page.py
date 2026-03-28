from core.render import render_template


def build_concrete_page():
    content = """
    <div class="container">
      <div class="breadcrumbs"><a href="/">Home</a> / <a href="/calculators/">Calculators</a> / Concrete calculator</div>
    </div>

    <section class="section">
      <div class="container">
        <div class="card calc-shell">
          <div class="section-head">
            <h1>Concrete Calculator</h1>
            <p class="small">Estimate concrete volume for slabs, strip footings and post holes with mobile-first controls and a clear breakdown.</p>
          </div>

          <div class="calc-intro-bar">
            <span class="calc-pill">Slabs</span>
            <span class="calc-pill">Post holes</span>
            <span class="calc-pill">Footings</span>
          </div>

          <div class="calc-grid">
            <div>
              <div class="toggle-row">
                <button type="button" class="active" data-concrete-mode="slab">Slab</button>
                <button type="button" data-concrete-mode="footing">Footing</button>
                <button type="button" data-concrete-mode="post">Post holes</button>
              </div>
              <input type="hidden" id="concrete-mode" value="slab">

              <div class="field">
                <label for="unit">Units</label>
                <select id="unit">
                  <option value="metric">Metric (m, m³)</option>
                  <option value="imperial">Imperial (ft, yd³)</option>
                </select>
              </div>

              <div class="field">
                <label for="length">Length</label>
                <input id="length" type="number" value="5" step="0.1">
              </div>

              <div class="field">
                <label for="width">Width</label>
                <input id="width" type="number" value="3" step="0.1">
                <p class="field-note" id="width-note">For slabs, use the full slab width. For footings, use the trench width. For post holes, use the hole diameter.</p>
              </div>

              <div class="field">
                <label for="depth">Depth / thickness</label>
                <input id="depth" type="number" value="0.1" step="0.01">
              </div>

              <div class="field" id="count-field" style="display:none;">
                <label for="count">Number of holes</label>
                <input id="count" type="number" value="8" step="1">
              </div>

              <div class="field">
                <label for="waste">Waste allowance (%)</label>
                <input id="waste" type="number" value="10" step="1">
                <p class="field-note" id="mode-note">Slab preset: a modest waste allowance for over-ordering, spillage and uneven sub-base conditions.</p>
              </div>
            </div>

            <aside class="card result-card">
              <p class="small">Estimated result</p>
              <p id="result-main" class="result-big">0 m³</p>
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
          <h2>Why concrete pages need their own support logic</h2>
          <p>Concrete estimation is driven by volume, form type, trench geometry, hole count and pour tolerance. That gives this page a genuinely different intent profile from decorating or tile quantity pages.</p>
        </article>
        <article class="card tool-card">
          <h2>What the waste allowance covers</h2>
          <p>Concrete waste can come from uneven excavation, overfill, spillage, pump residue and slight variation in hole or trench dimensions. A cautious allowance helps avoid running short mid-pour.</p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="container grid-2">
        <article class="card faq-item">
          <h3>How much concrete do I need for a slab?</h3>
          <p>Multiply slab length by width by thickness to get the base volume, then add your waste allowance. This calculator handles the conversion for metric and imperial units automatically.</p>
        </article>
        <article class="card faq-item">
          <h3>How do post hole calculations work?</h3>
          <p>Post holes are treated as cylinders. The tool uses the hole diameter, hole depth and the number of holes to estimate the total concrete volume, then adds waste.</p>
        </article>
      </div>
    </section>
    """
    return render_template("base.html", {
        "title": "Concrete Calculator | BuildCostLab",
        "description": "Calculate concrete volume for slabs, strip footings and post holes with metric or imperial inputs.",
        "canonical": "https://buildcostlab.com/calculators/concrete-calculator/",
        "content": content,
        "script_path": "/assets/js/concrete.js",
    })
