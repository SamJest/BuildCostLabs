from core.render import render_template

def build_tile_page():
    content = """
    <div class="container">
      <div class="breadcrumbs"><a href="/">Home</a> / <a href="/calculators/">Calculators</a> / Tile calculator</div>
    </div>

    <section class="section">
      <div class="container">
        <div class="card calc-shell">
          <div class="section-head">
            <h1>Tile Calculator</h1>
            <p class="small">Estimate tile quantities, waste allowance and boxes needed using room area and tile size in metric or imperial units.</p>
          </div>

          <div class="calc-grid">
            <div>
              <div class="field">
                <label for="unit">Units</label>
                <select id="unit">
                  <option value="metric">Metric (m², mm)</option>
                  <option value="imperial">Imperial (sq ft, inches)</option>
                </select>
              </div>

              <div class="field">
                <label for="room-area">Area to tile</label>
                <input id="room-area" type="number" value="18" step="0.1">
              </div>

              <div class="field">
                <label for="tile-width">Tile width</label>
                <input id="tile-width" type="number" value="600" step="0.1">
              </div>

              <div class="field">
                <label for="tile-height">Tile height</label>
                <input id="tile-height" type="number" value="300" step="0.1">
              </div>

              <div class="field">
                <label for="tiles-per-box">Tiles per box</label>
                <input id="tiles-per-box" type="number" value="8" step="1">
              </div>

              <div class="field">
                <label for="waste">Waste allowance (%)</label>
                <input id="waste" type="number" value="12" step="1">
              </div>
            </div>

            <aside class="card result-card">
              <p class="small">Estimated result</p>
              <p id="result-main" class="result-big">0 tiles / 0 boxes</p>
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
          <h2>Why tile pages need different copy</h2>
          <p>Unlike paint, tile calculations depend on tile face size, layout cuts, spare stock and supplier box sizes. This page is structured around those variables so it stays distinct.</p>
        </article>
        <article class="card tool-card">
          <h2>Typical waste guidance</h2>
          <p>Straight lay floors often need less waste than diagonal layouts or tight rooms with many perimeter cuts. Matching discontinued batches later can be difficult, so many users keep a few spare tiles.</p>
        </article>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <div class="section-head">
          <h2>Tile calculator FAQs</h2>
        </div>
        <div class="grid-2">
          <article class="card faq-item">
            <h3>How many boxes of tiles do I need?</h3>
            <p>First estimate the total tiles required including waste, then divide by tiles per box and round up to the next whole box. This calculator handles that automatically.</p>
          </article>
          <article class="card faq-item">
            <h3>How much waste should I allow for tiles?</h3>
            <p>That depends on the layout, tile size, room shape and how many cuts are needed. A basic straight layout usually needs less spare than a pattern with more offcuts.</p>
          </article>
        </div>
      </div>
    </section>
    """
    return render_template("base.html", {
        "title": "Tile Calculator | BuildMate Calculators",
        "description": "Calculate tile quantities, waste and boxes needed using room area and tile size.",
        "canonical": "https://example.com/calculators/tile-calculator/",
        "content": content,
        "script_path": "/assets/js/tile.js",
    })
