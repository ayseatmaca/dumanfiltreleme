import sys

file_path = "c:\\Users\\muham\\OneDrive\\Masaüstü\\duman\\fitre.html"
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update fonts and :root variables
old_fonts = '''  <link
    href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;500;700;800&display=swap"
    rel="stylesheet">
  <style>
    :root {
      --bg: #080b0f;
      --surface: #0d1117;
      --panel: #111820;
      --border: #1e2d3d;
      --border-hi: #2a4060;
      --accent: #00d4ff;
      --accent2: #7c3aed;
      --accent3: #10b981;
      --warn: #f59e0b;
      --text: #e2eaf4;
      --text-muted: #5a7a99;
      --text-dim: #2d4a66;
      --mono: 'Space Mono', monospace;
      --sans: 'Syne', sans-serif;
    }'''
new_fonts = '''  <link
    href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600;700;800&display=swap"
    rel="stylesheet">
  <style>
    :root {
      --bg: #102B53;
      --surface: rgba(80, 105, 189, 0.2);
      --panel: rgba(16, 43, 83, 0.5);
      --border: #4E7AB1;
      --border-hi: #5069BD;
      --accent: #CEB5D4;
      --accent2: #4E7AB1;
      --accent3: #7D9FC0;
      --warn: #CEB5D4;
      --text: #ffffff;
      --text-muted: #CEB5D4;
      --text-dim: #7D9FC0;
      --mono: 'Space Mono', monospace;
      --sans: 'Inter', sans-serif;
    }'''

html = html.replace(old_fonts, new_fonts)

# Add glassmorphism CSS overrides at the end of the style block
style_end = '''    @media (max-width: 900px) {'''
glass_css = '''
    /* Glassmorphism Overrides */
    .panel, .canvas-wrap {
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      border-radius: 12px;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
    }
    .log-bar, .pipeline-display, .upload-zone, .cw-body {
      border-radius: 8px;
    }
    .btn-run, .btn-ghost, .fi-header {
      border-radius: 6px;
    }
    .panel-header, .cw-header {
      border-top-left-radius: 12px;
      border-top-right-radius: 12px;
    }
    canvas {
      border-radius: 8px;
    }
    '''
html = html.replace(style_end, glass_css + style_end)

# Add new HTML filter items
filter_scroll_start = '''<div class="filter-scroll">'''
new_filters_html = '''
              <div class="filter-item" id="fi-tophat">
                <div class="fi-header" onclick="toggleFilter('tophat')">
                  <div class="fi-check"><svg viewBox="0 0 8 8" fill="none">
                      <polyline points="1,4 3,6 7,2" stroke-width="1.5" stroke-linecap="round"
                        stroke-linejoin="round" />
                    </svg></div>
                  <span class="fi-name">MORFOLOJİK TOP-HAT</span>
                  <span class="fi-badge badge-noise">DUMAN ÇİZGİSİ</span>
                </div>
                <div class="fi-body">
                  <div class="fi-desc">Geniş yansımaları/parlamaları yoksayarak yalnızca ince akış çizgilerini (aydınlık bölgeleri) ortaya çıkarır.</div>
                  <div class="srow"><label>Yarıçap</label><input type="range" id="sl-tophat" min="1" max="15" step="1"
                      value="6"><span id="vl-tophat">6</span></div>
                </div>
              </div>

              <div class="filter-item" id="fi-hlsuppress">
                <div class="fi-header" onclick="toggleFilter('hlsuppress')">
                  <div class="fi-check"><svg viewBox="0 0 8 8" fill="none">
                      <polyline points="1,4 3,6 7,2" stroke-width="1.5" stroke-linecap="round"
                        stroke-linejoin="round" />
                    </svg></div>
                  <span class="fi-name">YANSIMA BASKILAMA</span>
                  <span class="fi-badge badge-warn">MASKELEME</span>
                </div>
                <div class="fi-body">
                  <div class="fi-desc">Aşırı parlak noktaları tespit eder (ışık yansıması) ve bu noktaları belirli bir eşiğe göre karartır.</div>
                  <div class="srow"><label>Eşik (Threshold)</label><input type="range" id="sl-hl-t" min="100" max="255" step="5"
                      value="200"><span id="vl-hl-t">200</span></div>
                  <div class="srow"><label>Baskılama Gücü</label><input type="range" id="sl-hl-a" min="0.1" max="1.0" step="0.1"
                      value="0.8"><span id="vl-hl-a">0.8</span></div>
                </div>
              </div>

              <div class="filter-item" id="fi-gamma">
                <div class="fi-header" onclick="toggleFilter('gamma')">
                  <div class="fi-check"><svg viewBox="0 0 8 8" fill="none">
                      <polyline points="1,4 3,6 7,2" stroke-width="1.5" stroke-linecap="round"
                        stroke-linejoin="round" />
                    </svg></div>
                  <span class="fi-name">GAMA DÜZELTMESİ</span>
                  <span class="fi-badge badge-flow">KONTRAST</span>
                </div>
                <div class="fi-body">
                  <div class="fi-desc">Karanlık detayları (dumanı) görünür kılarken yüksek parlamaları minimal seviyede artırır. Orta tonları güçlendirir.</div>
                  <div class="srow"><label>Gama Değeri</label><input type="range" id="sl-gamma" min="0.2" max="3.0" step="0.1"
                      value="1.4"><span id="vl-gamma">1.4</span></div>
                </div>
              </div>
'''
html = html.replace(filter_scroll_start, filter_scroll_start + "\n" + new_filters_html)

# Add to JS arrays
js_filter_ids = "const filterIds = ['gray', 'bgsub', 'tophat', 'hlsuppress', 'gamma', 'median', 'bilateral', 'gauss', 'clahe', 'heq', 'unsharp', 'contrast', 'sobel', 'thresh', 'invert'];"
html = html.replace("const filterIds = ['gray', 'bgsub', 'median', 'bilateral', 'gauss', 'clahe', 'heq', 'unsharp', 'contrast', 'sobel', 'thresh', 'invert'];", js_filter_ids)

js_names = "const names = { gray: 'GRİ TON', bgsub: 'BG ÇIKARMA', tophat: 'TOP-HAT', hlsuppress: 'YANSIMA ÖNLE', gamma: 'GAMA', median: 'MEDİAN', bilateral: 'BİLATERAL', gauss: 'GAUSS', clahe: 'CLAHE', heq: 'HİST.EQ.', unsharp: 'UNSHARP', contrast: 'KONTRAST', sobel: 'SOBEL', thresh: 'EŞİKLEME', invert: 'TERS' };"
html = html.replace("const names = { gray: 'GRİ TON', bgsub: 'BG ÇIKARMA', median: 'MEDİAN', bilateral: 'BİLATERAL', gauss: 'GAUSS', clahe: 'CLAHE', heq: 'HİST.EQ.', unsharp: 'UNSHARP', contrast: 'KONTRAST', sobel: 'SOBEL', thresh: 'EŞİKLEME', invert: 'TERS' };", js_names)

sliderdefs_old = "['sl-bgsub', 'vl-bgsub', v => parseFloat(v).toFixed(1)],"
sliderdefs_new = sliderdefs_old + '''
      ['sl-tophat', 'vl-tophat', v => v],
      ['sl-hl-t', 'vl-hl-t', v => v],
      ['sl-hl-a', 'vl-hl-a', v => parseFloat(v).toFixed(1)],
      ['sl-gamma', 'vl-gamma', v => parseFloat(v).toFixed(1)],'''
html = html.replace(sliderdefs_old, sliderdefs_new)

# Add JS functions before run()
new_funcs = '''
    function morphologyPass(src, dst, w, h, r, isErosion) {
      const tmp = new Uint8ClampedArray(src.length);
      for (let y = 0; y < h; y++) {
        for (let x = 0; x < w; x++) {
          let val = src[(y * w + x) * 4];
          for (let k = -r; k <= r; k++) {
            const xx = Math.max(0, Math.min(w - 1, x + k));
            const p = src[(y * w + xx) * 4];
            val = isErosion ? Math.min(val, p) : Math.max(val, p);
          }
          const i = (y * w + x) * 4;
          tmp[i] = tmp[i + 1] = tmp[i + 2] = val;
          tmp[i + 3] = 255;
        }
      }
      for (let x = 0; x < w; x++) {
        for (let y = 0; y < h; y++) {
          let val = tmp[(y * w + x) * 4];
          for (let k = -r; k <= r; k++) {
            const yy = Math.max(0, Math.min(h - 1, y + k));
            const p = tmp[(yy * w + x) * 4];
            val = isErosion ? Math.min(val, p) : Math.max(val, p);
          }
          const i = (y * w + x) * 4;
          dst[i] = dst[i + 1] = dst[i + 2] = val;
          dst[i + 3] = 255;
        }
      }
    }

    function doTopHat(d, w, h, r) {
      const orig = new Uint8ClampedArray(d);
      const opened = new Uint8ClampedArray(d);
      morphologyPass(orig, opened, w, h, r, true);
      const eroded = new Uint8ClampedArray(opened);
      morphologyPass(eroded, opened, w, h, r, false);
      for (let i = 0; i < d.length; i += 4) {
        d[i] = d[i + 1] = d[i + 2] = clamp(orig[i] - opened[i]);
      }
    }

    function doGamma(d, w, h, gamma) {
      const lut = new Uint8Array(256);
      for (let i = 0; i < 256; i++) lut[i] = clamp(Math.pow(i / 255, 1 / gamma) * 255);
      for (let i = 0; i < d.length; i += 4) {
        d[i] = lut[d[i]]; d[i + 1] = lut[d[i + 1]]; d[i + 2] = lut[d[i + 2]];
      }
    }

    function suppressHL(d, w, h, thr, amt) {
      for (let i = 0; i < d.length; i += 4) {
        let v = d[i];
        if (v > thr) {
          v = thr + (v - thr) * (1 - amt);
        }
        d[i] = d[i + 1] = d[i + 2] = clamp(v);
      }
    }
'''
html = html.replace('function run() {', new_funcs + '\n    function run() {')

# Inject execution logic inside run()
run_bgsub = '''      if (filterState.bgsub) {
        const amp = parseFloat(document.getElementById('sl-bgsub').value);
        applied.push('BG çıkarma ×' + amp.toFixed(1));
        if (bgData) {
          for (let i = 0; i < d.length; i += 4) { const diff = Math.abs(d[i] - bgData.data[i]); const v = clamp(diff * amp); d[i] = d[i + 1] = d[i + 2] = v; }
        } else {
          const tmp = new Uint8ClampedArray(d); blurAll(tmp, W, H, 15);
          for (let i = 0; i < d.length; i += 4) { const diff = Math.abs(d[i] - tmp[i]); const v = clamp(diff * amp); d[i] = d[i + 1] = d[i + 2] = v; }
        }
      }'''
run_new = run_bgsub + '''
      if (filterState.tophat) {
        const r = parseInt(document.getElementById('sl-tophat').value);
        applied.push('Top-Hat r=' + r);
        doTopHat(d, W, H, r);
      }
      if (filterState.hlsuppress) {
        const thr = parseInt(document.getElementById('sl-hl-t').value);
        const amt = parseFloat(document.getElementById('sl-hl-a').value);
        applied.push('Yans.Bask. t=' + thr);
        suppressHL(d, W, H, thr, amt);
      }
      if (filterState.gamma) {
        const g = parseFloat(document.getElementById('sl-gamma').value);
        applied.push('Gama = ' + g.toFixed(1));
        doGamma(d, W, H, g);
      }'''
html = html.replace(run_bgsub, run_new)

# Update Presets to include new filters
presets_old = '''        flow: {
          gray: true, bgsub: true, median: false, bilateral: true, gauss: false, clahe: true, heq: false, unsharp: true, contrast: true, sobel: false, thresh: false, invert: false,
          vals: { 'sl-bgsub': 3, 'sl-bil-s': 4, 'sl-bil-r': 30, 'sl-clahe': 2.5, 'sl-unsharp': 1.5, 'sl-unsharp-r': 2, 'sl-con': 1.8, 'sl-bri': 5 }
        },'''
presets_new = '''        flow: {
          gray: true, bgsub: false, tophat: true, hlsuppress: true, gamma: true, median: false, bilateral: true, gauss: false, clahe: true, heq: false, unsharp: true, contrast: true, sobel: false, thresh: false, invert: false,
          vals: { 'sl-tophat': 8, 'sl-hl-t': 220, 'sl-hl-a': 0.8, 'sl-gamma': 1.6, 'sl-bil-s': 4, 'sl-bil-r': 30, 'sl-clahe': 2.0, 'sl-unsharp': 1.5, 'sl-unsharp-r': 2, 'sl-con': 1.1, 'sl-bri': 0 }
        },'''
html = html.replace(presets_old, presets_new)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated successfully")
