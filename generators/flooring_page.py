from core.render import render_template

def build_flooring_page():
    content = """
    <div class="container">
      <div class="breadcrumbs"><a href="/">Home</a> / <a href="/calculators/">Calculators</a> / Flooring calculator</div>
    </div>

    <section class="section">
      <div class="container">
        <div class="card calc-shell">
          <div class="section-head">
            <h1>Flooring Calculator</h1>
            <p class="small">Estimate flooring packs, board counts and waste allowance for laminate, wood or vinyl plank installs in metric or imperial units.</p>
          </div>

          <div class="calc-grid">
            <div>
              <div class="toggle-row">
                <button type="button" class="active" data-flooring-mode="laminate">Laminate</button>
                <button type="button" data-flooring-mode="wood">Wood</button>
                <button type="button" data-flooring-mode="vinyl">Vinyl plank</button>
              </div>
              <input type="hidden" id="flooring-mode" value="laminate">

              <div class="field">
                <label for="unit">Units</label>
                <select id="unit">
                  <option value="metric">Metric (m², mm)</option>
                  <option value="imperial">Imperial (sq ft, inches)</option>
                </select>
              </div>

              <div class="field">
                <label for="room-area">Floor area</label>
                <input id="room-area" type="number" value="18" step="0.1">
                <p class="field-note">Enter the finished floor area, not the wall perimeter. Use the waste setting for cuts, offcuts and spare stock.</p>
              </div>

              <div class="field">
                <label for="plank-width">Board / plank width</label>
                <input id="plank-width" type="number" value="192" step="0.1">
              </div>

              <div class="field">
                <label for="plank-length">Board / plank length</label>
                <input id="plank-length" type="number" value="1285" step="0.1">
              </div>

              <div class="field">
                <label for="pack-coverage">Pack coverage (m² per pack)</label>
                <input id="pack-coverage" type="number" value="1.84" step="0.01">
              </div>

              <div class="field">
                <label for="waste">Waste allowance (%)</label>
                <input id="waste" type="number" value="8" step="1">
                <p class="field-note" id="mode-note">Laminate preset: lighter waste for straighter runs and cleaner board consistency.</p>
              </div>
            </div>

            <aside class="card result-card">
              <p class="small">Estimated result</p>
              <p id="result-main" class="result-big">0 pack(s)</p>
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
          <h2>Why flooring pages need different support copy</h2>
          <p>Flooring estimates depend on board dimensions, pack coverage, staggered cuts and spare stock. That is a different decision pattern from paint litres or tile boxes, so the supporting content is purpose-built for flooring intent.</p>
        </article>
        <article class="card tool-card">
          <h2>Where flooring waste comes from</h2>
          <p>Waste usually comes from end cuts, awkward room shapes, door thresholds, pattern direction and keeping spare boards from the same batch for future repairs.</p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <h2>Flooring calculator FAQs</h2>
        </div>
        <div class="grid-2">
          <article class="card faq-item">
            <h3>How many packs of flooring do I need?</h3>
            <p>Work out the room area, add waste, then divide by the pack coverage shown by the manufacturer. This calculator rounds the result up to whole packs.</p>
          </article>
          <article class="card faq-item">
            <h3>Should I buy extra flooring?</h3>
            <p>Most people do. Spare boards from the same batch can help later if a section gets damaged or if the product line changes.</p>
          </article>
        </div>
      </div>
    </section>
    """
    return render_template("base.html", {
        "title": "Flooring Calculator | BuildMate Calculators",
        "description": "Calculate flooring packs, board counts and waste allowance for laminate, wood and vinyl plank installs.",
        "canonical": "https://example.com/calculators/flooring-calculator/",
        "content": content,
        "script_path": "/assets/js/flooring.js",
    })
