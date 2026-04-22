import sys

file_path = "c:\\Users\\muham\\OneDrive\\Masaüstü\\duman\\fitre.html"
with open(file_path, 'r', encoding='utf-8') as f:
    html = f.read()

start_idx = html.find('<script>')
end_idx = html.find('</script>') + len('</script>')

new_script = """<script>
    const MAX_DIM = 960; // Slightly reduced for performance
    let W = 480, H = 360;
    let mainData = null, bgData = null;
    let isProcessing = false;

    const canvasOrig = document.getElementById('c-orig');
    const canvasOut = document.getElementById('c-out');
    const ctxO = canvasOrig.getContext('2d');
    const ctxOut = canvasOut.getContext('2d');

    function log(msg) { document.getElementById('log-text').textContent = msg; }

    function showCanvas(id, show) {
      document.getElementById(id).style.display = show ? 'block' : 'none';
      const ph = id === 'c-orig' ? 'orig-placeholder' : 'out-placeholder';
      document.getElementById(ph).style.display = show ? 'none' : 'flex';
    }

    function loadImg(file, isBg) {
      if (isBg && !mainData) { log('Lütfen arka plan yüklemeden önce ANA GÖRÜNTÜYÜ yükleyin!'); return; }
      const r = new FileReader();
      r.onload = ev => {
        const img = new Image();
        img.onload = () => {
          if (!isBg) {
            const sc = Math.min(1, MAX_DIM / Math.max(img.width, img.height));
            W = Math.round(img.width * sc);
            H = Math.round(img.height * sc);
            canvasOrig.width = W; canvasOrig.height = H;
            canvasOut.width = W; canvasOut.height = H;
          }
          if (isBg) {
            const tmp = document.createElement('canvas'); tmp.width = W; tmp.height = H;
            const tc = tmp.getContext('2d'); tc.clearRect(0, 0, W, H); tc.drawImage(img, 0, 0, W, H);
            bgData = tc.getImageData(0, 0, W, H);
            const el = document.getElementById('uz-bg'); el.classList.add('loaded');
            document.getElementById('uz-bg-lbl').textContent = 'ARKA PLAN ✓';
            log('Arka plan görüntüsü yüklendi. Arka plan çıkarma filtresi aktifleştirildi.');
          } else {
            ctxO.clearRect(0, 0, W, H); ctxO.drawImage(img, 0, 0, W, H);
            mainData = ctxO.getImageData(0, 0, W, H);
            showCanvas('c-orig', true);
            const el = document.getElementById('uz-main'); el.classList.add('loaded');
            document.getElementById('uz-main-lbl').textContent = 'ANA GÖRÜNTÜ ✓';
            document.getElementById('orig-info').textContent = img.width + '×' + img.height + ' (' + W + 'x' + H + ' işleniyor)';
            log('Ana görüntü yüklendi (' + img.width + '×' + img.height + '). Filtre zincirini oluşturun ve uygulayın.');
          }
        }; img.src = ev.target.result;
      }; r.readAsDataURL(file);
    }

    document.getElementById('fi-main').onchange = e => e.target.files[0] && loadImg(e.target.files[0], false);
    document.getElementById('fi-bg').onchange = e => e.target.files[0] && loadImg(e.target.files[0], true);

    const filterIds = ['gray', 'bgsub', 'tophat', 'hlsuppress', 'gamma', 'median', 'bilateral', 'gauss', 'clahe', 'heq', 'unsharp', 'contrast', 'sobel', 'thresh', 'invert'];
    const filterState = {};
    filterIds.forEach(id => { filterState[id] = id === 'gray'; });

    function toggleFilter(id) {
      filterState[id] = !filterState[id];
      const el = document.getElementById('fi-' + id);
      el.classList.toggle('on', filterState[id]);
      updatePipeline();
    }

    function updatePipeline() {
      const steps = document.getElementById('pipeline-steps');
      const names = { gray: 'GRİ TON', bgsub: 'BG ÇIKARMA', tophat: 'TOP-HAT', hlsuppress: 'YANSIMA ÖNLE', gamma: 'GAMA', median: 'MEDİAN', bilateral: 'BİLATERAL', gauss: 'GAUSS', clahe: 'CLAHE', heq: 'HİST.EQ.', unsharp: 'UNSHARP', contrast: 'KONTRAST', sobel: 'SOBEL', thresh: 'EŞİKLEME', invert: 'TERS' };
      const active = filterIds.filter(id => filterState[id]);
      if (!active.length) { steps.innerHTML = '<span style="font-family:var(--mono);font-size:9px;color:var(--text-dim);">Filtre seçilmedi</span>'; return; }
      steps.innerHTML = active.map((id, i) => `<span class="pd-step active">${names[id]}</span>${i < active.length - 1 ? '<span class="pd-arrow">›</span>' : ''}`).join('');
    }

    function setOn(id, val) {
      filterState[id] = val;
      document.getElementById('fi-' + id).classList.toggle('on', val);
    }

    const sliderDefs = [
      ['sl-bgsub', 'vl-bgsub', v => parseFloat(v).toFixed(1)],
      ['sl-tophat', 'vl-tophat', v => v],
      ['sl-hl-t', 'vl-hl-t', v => v],
      ['sl-hl-a', 'vl-hl-a', v => parseFloat(v).toFixed(1)],
      ['sl-gamma', 'vl-gamma', v => parseFloat(v).toFixed(1)],
      ['sl-bil-s', 'vl-bil-s', v => v],
      ['sl-bil-r', 'vl-bil-r', v => v],
      ['sl-gauss', 'vl-gauss', v => v],
      ['sl-clahe', 'vl-clahe', v => parseFloat(v).toFixed(1)],
      ['sl-unsharp', 'vl-unsharp', v => parseFloat(v).toFixed(1)],
      ['sl-unsharp-r', 'vl-unsharp-r', v => v],
      ['sl-con', 'vl-con', v => parseFloat(v).toFixed(2)],
      ['sl-bri', 'vl-bri', v => v],
      ['sl-sobel', 'vl-sobel', v => v],
      ['sl-thresh', 'vl-thresh', v => v],
    ];
    sliderDefs.forEach(([s, v, f]) => {
      const el = document.getElementById(s), ov = document.getElementById(v);
      if (el && ov) el.addEventListener('input', () => { ov.textContent = f(el.value); });
    });

    document.getElementById('fi-gray').classList.add('on');
    updatePipeline();

    function clamp(v) { return Math.max(0, Math.min(255, Math.round(v))); }

    function gaussKernel(r) {
      const sz = r * 2 + 1, sig = r / 2.5, k = []; let s = 0;
      for (let i = 0; i < sz; i++) { const x = i - r, v = Math.exp(-(x * x) / (2 * sig * sig)); k.push(v); s += v; }
      return k.map(v => v / s);
    }
    function blurPass(d, w, h, r, ch) {
      const k = gaussKernel(r), tmp = new Float32Array(w * h);
      for (let y = 0; y < h; y++)for (let x = 0; x < w; x++) { let s = 0; for (let i = -r; i <= r; i++) { const xx = Math.max(0, Math.min(w - 1, x + i)); s += d[(y * w + xx) * 4 + ch] * k[i + r]; } tmp[y * w + x] = s; }
      for (let y = 0; y < h; y++)for (let x = 0; x < w; x++) { let s = 0; for (let i = -r; i <= r; i++) { const yy = Math.max(0, Math.min(h - 1, y + i)); s += tmp[yy * w + x] * k[i + r]; } d[(y * w + x) * 4 + ch] = clamp(s); }
    }
    function blurAll(d, w, h, r) { blurPass(d, w, h, r, 0); blurPass(d, w, h, r, 1); blurPass(d, w, h, r, 2); }

    function medianFilter(d, w, h, sz) {
      const half = Math.floor(sz / 2), out = new Uint8ClampedArray(d);
      for (let y = 0; y < h; y++)for (let x = 0; x < w; x++) {
        const vals = [];
        for (let ky = -half; ky <= half; ky++)for (let kx = -half; kx <= half; kx++) {
          const yy = Math.max(0, Math.min(h - 1, y + ky)), xx = Math.max(0, Math.min(w - 1, x + kx));
          vals.push(d[(yy * w + xx) * 4]);
        }
        vals.sort((a, b) => a - b);
        const mid = vals[Math.floor(vals.length / 2)];
        const i = (y * w + x) * 4; out[i] = out[i + 1] = out[i + 2] = mid;
      }
      for (let i = 0; i < d.length; i++)d[i] = out[i];
    }

    function bilateralFilter(d, w, h, sigS, sigR) {
      const r = Math.ceil(sigS * 2), out = new Uint8ClampedArray(d);
      for (let y = 0; y < h; y++)for (let x = 0; x < w; x++) {
        let wSum = 0, vSum = 0; const cI = d[(y * w + x) * 4];
        for (let ky = -r; ky <= r; ky++)for (let kx = -r; kx <= r; kx++) {
          const yy = Math.max(0, Math.min(h - 1, y + ky)), xx = Math.max(0, Math.min(w - 1, x + kx));
          const nI = d[(yy * w + xx) * 4];
          const w2 = Math.exp(-(kx * kx + ky * ky) / (2 * sigS * sigS)) * Math.exp(-Math.pow(nI - cI, 2) / (2 * sigR * sigR));
          wSum += w2; vSum += nI * w2;
        }
        const v = clamp(vSum / wSum); const i = (y * w + x) * 4; out[i] = out[i + 1] = out[i + 2] = v;
      }
      for (let i = 0; i < d.length; i++)d[i] = out[i];
    }

    function doClahe(d, w, h, clip, grid) {
      const tw = Math.floor(w / grid), th = Math.floor(h / grid);
      for (let ty = 0; ty < grid; ty++)for (let tx = 0; tx < grid; tx++) {
        const x0 = tx * tw, y0 = ty * th, x1 = Math.min(x0 + tw, w), y1 = Math.min(y0 + th, h);
        const hist = new Int32Array(256);
        for (let y = y0; y < y1; y++)for (let x = x0; x < x1; x++)hist[d[(y * w + x) * 4]]++;
        const lim = Math.round((tw * th) / (256 / clip));
        let ex = 0; for (let v = 0; v < 256; v++)if (hist[v] > lim) { ex += hist[v] - lim; hist[v] = lim; }
        const rd = Math.floor(ex / 256); for (let v = 0; v < 256; v++)hist[v] += rd;
        const cdf = new Int32Array(256); cdf[0] = hist[0]; for (let v = 1; v < 256; v++)cdf[v] = cdf[v - 1] + hist[v];
        const tot = (x1 - x0) * (y1 - y0), cMin = cdf[0];
        const lut = new Uint8Array(256); for (let v = 0; v < 256; v++)lut[v] = clamp((cdf[v] - cMin) / (tot - cMin) * 255);
        for (let y = y0; y < y1; y++)for (let x = x0; x < x1; x++) { const i = (y * w + x) * 4; d[i] = d[i + 1] = d[i + 2] = lut[d[i]]; }
      }
    }

    function histEq(d, w, h) {
      const hist = new Int32Array(256);
      for (let i = 0; i < w * h; i++)hist[d[i * 4]]++;
      const cdf = new Int32Array(256); cdf[0] = hist[0]; for (let v = 1; v < 256; v++)cdf[v] = cdf[v - 1] + hist[v];
      const mn = cdf.find(v => v > 0), tot = w * h;
      const lut = new Uint8Array(256); for (let v = 0; v < 256; v++)lut[v] = clamp((cdf[v] - mn) / (tot - mn) * 255);
      for (let i = 0; i < w * h; i++) { const p = i * 4; d[p] = d[p + 1] = d[p + 2] = lut[d[p]]; }
    }

    function otsuThresh(d, w, h) {
      const hist = new Array(256).fill(0);
      for (let i = 0; i < w * h; i++)hist[d[i * 4]]++;
      const tot = w * h; let sum = 0; for (let v = 0; v < 256; v++)sum += v * hist[v];
      let sumB = 0, wB = 0, best = 0, t = 0;
      for (let v = 0; v < 256; v++) {
        wB += hist[v]; if (!wB) continue; const wF = tot - wB; if (!wF) break;
        sumB += v * hist[v]; const mB = sumB / wB, mF = (sum - sumB) / wF;
        const between = wB * wF * (mB - mF) * (mB - mF); if (between > best) { best = between; t = v; }
      }
      return t;
    }

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
        // use intensity of the pixel assuming grayscale or max of RGB
        let v = Math.max(d[i], d[i+1], d[i+2]);
        if (v > thr) {
          let newV = thr + (v - thr) * (1 - amt);
          let ratio = newV / v;
          d[i] = clamp(d[i] * ratio);
          d[i+1] = clamp(d[i+1] * ratio);
          d[i+2] = clamp(d[i+2] * ratio);
        }
      }
    }

    const delay = ms => new Promise(r => setTimeout(r, ms));

    async function run() {
      if (!mainData) { log('HATA: Önce ana görüntü yükleyin.'); return; }
      if (isProcessing) { log('Devam eden işlem var, lütfen bekleyin...'); return; }
      
      const btn = document.querySelector('.btn-run');
      btn.style.opacity = '0.5';
      btn.textContent = 'İŞLENİYOR...';
      isProcessing = true;
      
      try {
        const d = new Uint8ClampedArray(mainData.data);
        const applied = [];

        log('Uygulanıyor: Hazırlık...');
        await delay(20);

        if (filterState.gray) {
          applied.push('Gri ton');
          for (let i = 0; i < d.length; i += 4) { const g = clamp(0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2]); d[i] = d[i + 1] = d[i + 2] = g; }
          await delay(10);
        }
        if (filterState.bgsub) {
          const amp = parseFloat(document.getElementById('sl-bgsub').value);
          applied.push('BG çıkarma ×' + amp.toFixed(1));
          if (bgData) {
            for (let i = 0; i < d.length; i += 4) { const diff = Math.abs(d[i] - bgData.data[i]); const v = clamp(diff * amp); d[i] = d[i + 1] = d[i + 2] = v; }
          } else {
            const tmp = new Uint8ClampedArray(d); blurAll(tmp, W, H, 15);
            for (let i = 0; i < d.length; i += 4) { const diff = Math.abs(d[i] - tmp[i]); const v = clamp(diff * amp); d[i] = d[i + 1] = d[i + 2] = v; }
          }
          await delay(10);
        }
        if (filterState.tophat) {
          const r = parseInt(document.getElementById('sl-tophat').value);
          applied.push('Top-Hat r=' + r);
          log('Uygulanıyor: Morfolojik Top-Hat...');
          await delay(20);
          doTopHat(d, W, H, r);
        }
        if (filterState.hlsuppress) {
          const thr = parseInt(document.getElementById('sl-hl-t').value);
          const amt = parseFloat(document.getElementById('sl-hl-a').value);
          applied.push('Yans.Bask. t=' + thr);
          log('Uygulanıyor: Yansıma Baskılama...');
          suppressHL(d, W, H, thr, amt);
          await delay(10);
        }
        if (filterState.gamma) {
          const g = parseFloat(document.getElementById('sl-gamma').value);
          applied.push('Gama = ' + g.toFixed(1));
          log('Uygulanıyor: Gama Düzeltmesi...');
          doGamma(d, W, H, g);
          await delay(10);
        }
        if (filterState.median) {
          const sz = parseInt(document.getElementById('sl-median').value);
          applied.push('Median ' + sz + '×' + sz); 
          log('Uygulanıyor: Median...');
          await delay(20);
          medianFilter(d, W, H, sz);
        }
        if (filterState.bilateral) {
          const sS = parseInt(document.getElementById('sl-bil-s').value), sR = parseInt(document.getElementById('sl-bil-r').value);
          applied.push('Bilateral σs=' + sS); 
          log('Uygulanıyor: Bilateral...');
          await delay(20);
          bilateralFilter(d, W, H, sS, sR);
        }
        if (filterState.gauss) {
          const r = parseInt(document.getElementById('sl-gauss').value);
          applied.push('Gauss r=' + r); 
          log('Uygulanıyor: Gauss Blur...');
          await delay(20);
          blurAll(d, W, H, r);
        }
        if (filterState.clahe) {
          const clip = parseFloat(document.getElementById('sl-clahe').value);
          const grid = parseInt(document.getElementById('sl-clahe-grid').value);
          applied.push('CLAHE ' + clip.toFixed(1) + '/' + grid + '×' + grid); 
          log('Uygulanıyor: CLAHE...');
          await delay(20);
          doClahe(d, W, H, clip, grid);
        }
        if (filterState.heq) { applied.push('Hist.eq.'); histEq(d, W, H); await delay(10); }
        if (filterState.unsharp) {
          const amt = parseFloat(document.getElementById('sl-unsharp').value);
          const r = parseInt(document.getElementById('sl-unsharp-r').value);
          applied.push('Unsharp ×' + amt.toFixed(1));
          log('Uygulanıyor: Unsharp Mask...');
          await delay(20);
          const orig2 = new Uint8ClampedArray(d), blr = new Uint8ClampedArray(d); blurAll(blr, W, H, r);
          for (let i = 0; i < d.length; i += 4) { d[i] = clamp(orig2[i] + amt * (orig2[i] - blr[i])); d[i + 1] = clamp(orig2[i + 1] + amt * (orig2[i + 1] - blr[i + 1])); d[i + 2] = clamp(orig2[i + 2] + amt * (orig2[i + 2] - blr[i + 2])); }
        }
        if (filterState.contrast) {
          const c = parseFloat(document.getElementById('sl-con').value), b = parseInt(document.getElementById('sl-bri').value);
          applied.push('Kontrast ×' + c.toFixed(2));
          log('Uygulanıyor: Kontrast/Parlaklık...');
          for (let i = 0; i < d.length; i += 4) { d[i] = clamp((d[i] - 128) * c + 128 + b); d[i + 1] = clamp((d[i + 1] - 128) * c + 128 + b); d[i + 2] = clamp((d[i + 2] - 128) * c + 128 + b); }
          await delay(10);
        }
        if (filterState.sobel) {
          const thr = parseInt(document.getElementById('sl-sobel').value);
          const mod = document.getElementById('sel-sobel').value;
          applied.push('Sobel[' + mod + ']');
          log('Uygulanıyor: Sobel...');
          await delay(20);
          const gray = new Uint8Array(W * H); for (let i = 0; i < W * H; i++)gray[i] = d[i * 4];
          const gx = new Float32Array(W * H), gy = new Float32Array(W * H);
          for (let y = 1; y < H - 1; y++)for (let x = 1; x < W - 1; x++) {
            gx[y * W + x] = -gray[(y - 1) * W + (x - 1)] - 2 * gray[y * W + (x - 1)] - gray[(y + 1) * W + (x - 1)] + gray[(y - 1) * W + (x + 1)] + 2 * gray[y * W + (x + 1)] + gray[(y + 1) * W + (x + 1)];
            gy[y * W + x] = -gray[(y - 1) * W + (x - 1)] - 2 * gray[(y - 1) * W + x] - gray[(y - 1) * W + (x + 1)] + gray[(y + 1) * W + (x - 1)] + 2 * gray[(y + 1) * W + x] + gray[(y + 1) * W + (x + 1)];
          }
          for (let i = 0; i < W * H; i++) {
            const mag = Math.sqrt(gx[i] * gx[i] + gy[i] * gy[i]);
            let v;
            if (mod === 'mag') v = clamp(mag);
            else if (mod === 'bin') v = mag > thr ? 255 : 0;
            else { const angle = (Math.atan2(gy[i], gx[i]) + Math.PI) / (2 * Math.PI) * 255; v = mag > thr ? clamp(angle) : 0; }
            d[i * 4] = d[i * 4 + 1] = d[i * 4 + 2] = v;
          }
        }
        if (filterState.thresh) {
          const mod = document.getElementById('sel-thresh').value;
          let t = parseInt(document.getElementById('sl-thresh').value);
          if (mod === 'adapt') t = otsuThresh(d, W, H);
          applied.push('Eşik t=' + t + (mod === 'adapt' ? ' [Otsu]' : mod === 'inv' ? ' [ters]' : ''));
          for (let i = 0; i < W * H; i++) { const p = i * 4; const v = mod === 'inv' ? (d[p] < t ? 255 : 0) : (d[p] > t ? 255 : 0); d[p] = d[p + 1] = d[p + 2] = v; }
          await delay(10);
        }
        if (filterState.invert) {
          applied.push('Ters çevirme');
          for (let i = 0; i < d.length; i += 4) { d[i] = 255 - d[i]; d[i + 1] = 255 - d[i + 1]; d[i + 2] = 255 - d[i + 2]; }
        }

        ctxOut.putImageData(new ImageData(d, W, H), 0, 0);
        showCanvas('c-out', true);
        document.getElementById('out-info').textContent = applied.length + ' filtre';
        log('Tamamlandı: ' + applied.join(' → '));
      } catch (err) {
        log('Bir hata oluştu: ' + err.message);
      } finally {
        isProcessing = false;
        btn.style.opacity = '1';
        btn.textContent = '▶ FİLTRELERİ UYGULA';
      }
    }

    function dl() {
      const a = document.createElement('a'); a.download = 'smoke_flow_processed.png';
      a.href = document.getElementById('c-out').toDataURL('image/png'); a.click();
    }

    function setPreset(name) {
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      document.getElementById('pr-' + name)?.classList.add('active');
      const presets = {
        flow: {
          gray: true, bgsub: false, tophat: true, hlsuppress: true, gamma: true, median: false, bilateral: true, gauss: false, clahe: true, heq: false, unsharp: true, contrast: true, sobel: false, thresh: false, invert: false,
          vals: { 'sl-tophat': 8, 'sl-hl-t': 220, 'sl-hl-a': 0.8, 'sl-gamma': 1.6, 'sl-bil-s': 4, 'sl-bil-r': 30, 'sl-clahe': 2.0, 'sl-unsharp': 1.5, 'sl-unsharp-r': 2, 'sl-con': 1.1, 'sl-bri': 0 }
        },
        smoke: {
          gray: true, bgsub: false, tophat: false, hlsuppress: false, gamma: false, median: true, bilateral: false, gauss: true, clahe: true, heq: false, unsharp: true, contrast: true, sobel: false, thresh: false, invert: false,
          vals: { 'sl-median': 3, 'sl-gauss': 2, 'sl-clahe': 3, 'sl-unsharp': 2, 'sl-unsharp-r': 2, 'sl-con': 2, 'sl-bri': 10 }
        },
        edge: {
          gray: true, bgsub: false, tophat: false, hlsuppress: false, gamma: false, median: false, bilateral: false, gauss: true, clahe: false, heq: false, unsharp: false, contrast: false, sobel: true, thresh: false, invert: false,
          vals: { 'sl-gauss': 2, 'sl-sobel': 25 }
        },
        binary: {
          gray: true, bgsub: true, tophat: false, hlsuppress: false, gamma: false, median: true, bilateral: false, gauss: true, clahe: true, heq: false, unsharp: false, contrast: false, sobel: false, thresh: true, invert: false,
          vals: { 'sl-bgsub': 4, 'sl-median': 3, 'sl-gauss': 2, 'sl-clahe': 2, 'sl-thresh': 80 }
        },
        clean: {
          gray: true, bgsub: false, tophat: false, hlsuppress: false, gamma: false, median: true, bilateral: true, gauss: false, clahe: true, heq: false, unsharp: false, contrast: true, sobel: false, thresh: false, invert: false,
          vals: { 'sl-median': 5, 'sl-bil-s': 5, 'sl-bil-r': 40, 'sl-clahe': 2, 'sl-con': 1.4, 'sl-bri': 0 }
        },
      };
      const p = presets[name]; if (!p) return;
      filterIds.forEach(id => setOn(id, p[id] || false));
      if (p.vals) Object.entries(p.vals).forEach(([k, v]) => { const el = document.getElementById(k); if (el) el.value = v; });
      sliderDefs.forEach(([s, v, f]) => { const el = document.getElementById(s), ov = document.getElementById(v); if (el && ov) ov.textContent = f(el.value); });
      updatePipeline();
      const names = { flow: 'Akış Çizgileri', smoke: 'Duman Netliği', edge: 'Kenar Analizi', binary: 'İkili Görüntü', clean: 'Temiz Filtre' };
      log('Ön ayar yüklendi: ' + names[name] + '. Görüntü yükleyip "Filtreleri Uygula"ya basın.');
    }

    function resetUI() {
      filterIds.forEach(id => setOn(id, id === 'gray'));
      ctxOut.clearRect(0, 0, W, H);
      showCanvas('c-out', false);
      document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
      updatePipeline();
      log('Sıfırlandı. Tüm filtreler temizlendi.');
    }
  </script>"""

html = html[:start_idx] + new_script + html[end_idx:]

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("done")
