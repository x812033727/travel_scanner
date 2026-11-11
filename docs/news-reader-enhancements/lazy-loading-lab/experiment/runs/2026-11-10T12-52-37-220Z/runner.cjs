'use strict';
const fs = require('node:fs');
const path = require('node:path');
const http = require('node:http');
const crypto = require('node:crypto');
const os = require('node:os');
const { performance } = require('node:perf_hooks');

const root = __dirname;
const fixtures = path.join(root, 'fixtures');
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const writeJson = (file, value) => fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n');
function buildFixtures() {
  fs.mkdirSync(path.join(fixtures, 'images'), { recursive: true });
  for (let n = 1; n <= 20; n++) {
    const hue = (n * 29) % 360;
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="675" viewBox="0 0 1200 675"><rect width="1200" height="675" fill="hsl(${hue} 65% 25%)"/><circle cx="950" cy="250" r="180" fill="hsl(${hue} 70% 45%)"/><path d="M0 600 L400 250 L780 675 H0" fill="hsl(${hue} 60% 35%)"/><text x="70" y="150" fill="white" font-family="sans-serif" font-size="54">MOKAAIR LOCAL LAB</text><text x="70" y="330" fill="white" font-family="sans-serif" font-size="120">IMAGE ${String(n).padStart(2, '0')}</text><text x="70" y="545" fill="white" font-family="sans-serif" font-size="36">1200 x 675 / original synthetic fixture</text></svg>`;
    fs.writeFileSync(path.join(fixtures, 'images', `${String(n).padStart(2, '0')}.svg`), svg);
  }
  for (const mode of ['eager', 'lazy']) {
    const sections = Array.from({ length: 20 }, (_, i) => {
      const n = i + 1;
      const before = n === 2 ? '<div class="near-gap">Near-viewport gap: 600 CSS px</div>' : n === 3 ? '<div class="far-gap">Far-image gap: 6000 CSS px</div>' : n > 3 ? '<div class="tail-gap"></div>' : '';
      return `${before}<section id="section-${n}"><h2>Image ${String(n).padStart(2, '0')}</h2><img id="image-${n}" src="/images/${String(n).padStart(2, '0')}.svg" width="1200" height="675" loading="${mode === 'lazy' && n > 1 ? 'lazy' : 'eager'}" alt="Original local test image ${n}"><p>Fixed dimensions. Same image and position in both variants.</p></section>`;
    }).join('\n');
    const html = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Mokaair image-loading lab — ${mode}</title><link rel="icon" href="data:,"><style>*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:#f4f6f8;color:#122033;font-family:Arial,sans-serif}main{width:min(calc(100% - 32px),900px);margin:0 auto;padding:24px 0}header{margin-bottom:24px}h1{font-size:clamp(24px,3vw,36px);line-height:1.16;margin:0 0 12px}h2{font-size:20px;margin:0 0 12px}p{font-size:16px;line-height:1.5;margin:10px 0}section{background:white;padding:16px;border:1px solid #b9c6d2;border-radius:12px}img{display:block;width:100%;height:auto;background:#d9e2eb;aspect-ratio:1200/675}code{background:#e2eaf1;padding:2px 4px}.near-gap{height:600px;padding-top:24px}.far-gap{height:6000px;padding-top:24px;background:repeating-linear-gradient(180deg,transparent 0,transparent 199px,#dce5ec 200px)}.tail-gap{height:600px}</style></head><body data-page-script="not-run"><main><header><h1>Native image loading: ${mode}</h1><p>20 local images. First image stays eager. No analytics or external assets.</p><p>Compare requests before scrolling and after scrolling.</p></header>${sections}<footer><p>End of local lab. No performance score is calculated.</p></footer></main><script>document.body.dataset.pageScript='enabled';</script></body></html>`;
    fs.writeFileSync(path.join(fixtures, `${mode}.html`), html);
  }
  const files = ['eager.html', 'lazy.html', ...Array.from({ length: 20 }, (_, i) => `images/${String(i + 1).padStart(2, '0')}.svg`)];
  const manifest = files.map(file => ({ file, sha256: sha(fs.readFileSync(path.join(fixtures, file))), bytes: fs.statSync(path.join(fixtures, file)).size }));
  writeJson(path.join(root, 'fixture-manifest.json'), manifest);
  return manifest;
}
function createServer(serverLog, phaseRef) {
  const started = performance.now();
  return http.createServer((req, res) => {
    const url = new URL(req.url, 'http://127.0.0.1');
    const relative = url.pathname.slice(1);
    const safe = /^(eager\.html|lazy\.html|images\/(0[1-9]|1[0-9]|20)\.svg)$/.test(relative);
    const file = safe ? path.join(fixtures, relative) : null;
    const body = file && fs.existsSync(file) ? fs.readFileSync(file) : Buffer.from('Not found');
    const status = file && fs.existsSync(file) ? 200 : 404;
    const row = { at: new Date().toISOString(), sinceServerStartMs: +(performance.now() - started).toFixed(3), caseId: req.headers['x-lab-case'] || null, phase: phaseRef.value, method: req.method, pathname: url.pathname, status, bodyBytes: body.length };
    serverLog.push(row);
    res.writeHead(status, { 'Content-Type': relative.endsWith('.svg') ? 'image/svg+xml' : 'text/html; charset=utf-8', 'Cache-Control': 'no-store', 'Content-Length': body.length, 'Content-Security-Policy': "default-src 'self'; img-src 'self' data:; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'; frame-src 'none'" });
    res.end(body);
  });
}
async function main() {
  const command = process.argv[2] || 'generate';
  const manifest = buildFixtures();
  if (command === 'generate') { console.log(JSON.stringify({ fixtures: manifest.length, path: fixtures })); return; }
  const serverLog = [], phaseRef = { value: 'idle' };
  const server = createServer(serverLog, phaseRef);
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = `http://127.0.0.1:${server.address().port}`;
  if (command === 'serve') { console.log(`${origin}/lazy.html`); console.log(`${origin}/eager.html`); return; }
  if (command !== 'run') { server.close(); throw new Error('Use generate, serve, or run'); }
  // Public derivative: only dependency resolution was made portable; see PUBLICATION-REBIND.md.
  const pwRoot = process.env.MOKAAIR_PLAYWRIGHT_ROOT || path.dirname(require.resolve('playwright/package.json', { paths: [root, process.cwd()] }));
  const { chromium } = require(pwRoot);
  const pwPackage = require(path.join(pwRoot, 'package.json'));
  const runId = new Date().toISOString().replaceAll(':', '-').replaceAll('.', '-');
  const out = path.join(root, 'runs', runId);
  fs.mkdirSync(out, { recursive: true });
  fs.mkdirSync(path.join(out, 'screenshots'));
  const env = { startedAt: new Date().toISOString(), platform: os.platform(), release: os.release(), arch: os.arch(), node: process.version, playwright: pwPackage.version, browser: 'Microsoft Edge', headless: true, origin, deviceScaleFactor: 1, mobileEmulation: false, cache: 'new context; CDP disabled; HTTP no-store', network: 'localhost; no throttle', pageNetworkPolicy: 'block non-local origin; service workers blocked; not an OS telemetry audit', planSha256: sha(fs.readFileSync(path.join(root, 'experiment-plan.md'))), runnerSha256: sha(fs.readFileSync(__filename)), fixtureManifestSha256: sha(fs.readFileSync(path.join(root, 'fixture-manifest.json'))) };
  const results = [], browserLog = [], blocked = [], errors = [];
  let browser, failure;
  try {
    browser = await chromium.launch({ channel: 'msedge', headless: true });
    env.browserVersion = browser.version();
    writeJson(path.join(out, 'environment.json'), env);
    fs.copyFileSync(path.join(root, 'experiment-plan.md'), path.join(out, 'experiment-plan.md'));
    fs.copyFileSync(path.join(root, 'fixture-manifest.json'), path.join(out, 'fixture-manifest.json'));
    fs.copyFileSync(__filename, path.join(out, 'runner.cjs'));
    for (const viewport of [{ name: 'desktop', width: 1440, height: 900 }, { name: 'narrow', width: 390, height: 844 }]) {
      for (let repetition = 1; repetition <= 3; repetition++) {
        for (const scenario of [{ name: 'eager-js', mode: 'eager', js: true }, { name: 'lazy-js', mode: 'lazy', js: true }, { name: 'lazy-nojs', mode: 'lazy', js: false }]) {
          const caseId = `${viewport.name}-${scenario.name}-r${repetition}`;
          phaseRef.value = `${caseId}:initial`;
          const context = await browser.newContext({ viewport: { width: viewport.width, height: viewport.height }, deviceScaleFactor: 1, javaScriptEnabled: scenario.js, serviceWorkers: 'block', extraHTTPHeaders: { 'X-Lab-Case': caseId } });
          await context.route('**/*', route => {
            const url = new URL(route.request().url());
            if (url.origin === origin) return route.continue();
            blocked.push({ caseId, url: url.href, phase: phaseRef.value });
            return route.abort('blockedbyclient');
          });
          const page = await context.newPage();
          page.on('request', req => browserLog.push({ caseId, at: new Date().toISOString(), phase: phaseRef.value, url: req.url(), method: req.method(), type: req.resourceType() }));
          page.on('pageerror', error => errors.push({ caseId, message: error.message }));
          const cdp = await context.newCDPSession(page);
          await cdp.send('Network.enable');
          await cdp.send('Network.setCacheDisabled', { cacheDisabled: true });
          const snapshot = async phase => {
            const dom = await page.evaluate(() => ({ pageScript: document.body.dataset.pageScript, scrollY, innerWidth, innerHeight, devicePixelRatio, scrollHeight: document.documentElement.scrollHeight, images: [...document.images].map(img => { const r = img.getBoundingClientRect(); return { id: img.id, loading: img.loading, complete: img.complete, naturalWidth: img.naturalWidth, loaded: img.complete && img.naturalWidth > 0, top: r.top, bottom: r.bottom, documentTop: r.top + scrollY, width: r.width, height: r.height, intersectsViewport: r.bottom > 0 && r.top < innerHeight }; }) }));
            const requests = serverLog.filter(r => r.caseId === caseId && r.pathname.endsWith('.svg'));
            const entry = { phase, recordedAt: new Date().toISOString(), uniqueImagesRequested: new Set(requests.map(r => r.pathname)).size, requestedImagePaths: [...new Set(requests.map(r => r.pathname))], imageBodyBytesServed: requests.reduce((sum, r) => sum + r.bodyBytes, 0), loadedCount: dom.images.filter(img => img.loaded).length, ...dom };
            if (repetition === 1) { entry.screenshot = `screenshots/${caseId}-${phase}.png`; await page.screenshot({ path: path.join(out, entry.screenshot), fullPage: false }); }
            return entry;
          };
          try {
            await page.goto(`${origin}/${scenario.mode}.html`, { waitUntil: 'domcontentloaded' });
            await page.waitForTimeout(3000);
            const initial = await snapshot('initial');
            phaseRef.value = `${caseId}:after-end`;
            await page.keyboard.press('End');
            await page.waitForTimeout(1000);
            const afterEnd = await snapshot('after-end');
            phaseRef.value = `${caseId}:full-traversal`;
            await page.keyboard.press('Control+Home');
            await page.waitForTimeout(100);
            let steps = 0;
            for (; steps < 200; steps++) {
              const atBottom = await page.evaluate(() => scrollY >= document.documentElement.scrollHeight - innerHeight - 2);
              if (atBottom) break;
              await page.mouse.wheel(0, 700);
              await page.waitForTimeout(80);
            }
            await page.waitForTimeout(1000);
            const afterTraversal = await snapshot('after-traversal');
            const checks = {
              pageScriptMatchesCondition: initial.pageScript === (scenario.js ? 'enabled' : 'not-run'),
              noInitialScroll: initial.scrollY === 0,
              farImageOutsideViewport: initial.images[2].top > initial.innerHeight,
              firstImageLoaded: initial.images[0].loaded,
              eagerOrNoJsAllInitialLoaded: scenario.name === 'lazy-js' || initial.loadedCount === 20,
              lazyFarImageDeferred: scenario.name !== 'lazy-js' || (!initial.images[2].loaded && !initial.requestedImagePaths.includes('/images/03.svg')),
              finalImageLoadedAfterEnd: afterEnd.images[19].loaded,
              reachedBottomAfterEnd: afterEnd.scrollY >= afterEnd.scrollHeight - afterEnd.innerHeight - 2,
              allImagesLoadedAfterTraversal: afterTraversal.loadedCount === 20,
              traversalWithinBound: steps < 200
            };
            results.push({ caseId, viewport, scenario, repetition, steps, initial, afterEnd, afterTraversal, checks, pass: Object.values(checks).every(Boolean) });
            writeJson(path.join(out, 'results.json'), results);
            console.log(JSON.stringify({ caseId, initial: initial.loadedCount, afterEnd: afterEnd.loadedCount, afterTraversal: afterTraversal.loadedCount, pass: Object.values(checks).every(Boolean) }));
          } finally { await context.close(); }
        }
      }
    }
  } catch (error) { failure = error.stack || String(error); }
  finally {
    if (browser) await browser.close();
    await new Promise(resolve => server.close(resolve));
    writeJson(path.join(out, 'server-requests.json'), serverLog);
    writeJson(path.join(out, 'browser-requests.json'), browserLog);
    writeJson(path.join(out, 'blocked-external-requests.json'), blocked);
    writeJson(path.join(out, 'page-errors.json'), errors);
    writeJson(path.join(out, 'results.json'), results);
    const pass = !failure && results.length === 18 && results.every(r => r.pass) && errors.length === 0 && blocked.length === 0;
    writeJson(path.join(out, 'receipt.json'), { status: pass ? 'PASS' : 'FAILED', runId, startedAt: env.startedAt, completedAt: new Date().toISOString(), cases: results.length, passCases: results.filter(r => r.pass).length, pageErrors: errors.length, blockedExternalRequests: blocked.length, failure: failure || null, environmentSha256: sha(fs.readFileSync(path.join(out, 'environment.json'))), resultsSha256: sha(fs.readFileSync(path.join(out, 'results.json'))), serverRequestsSha256: sha(fs.readFileSync(path.join(out, 'server-requests.json'))), browserRequestsSha256: sha(fs.readFileSync(path.join(out, 'browser-requests.json'))), limitations: ['one Edge build on one Windows machine', 'headless and CSS viewports, not physical phone tests', 'synthetic SVG and localhost; no internet performance or SEO claim', 'page requests checked; OS/browser telemetry not audited'] });
    console.log(JSON.stringify({ output: out, status: pass ? 'PASS' : 'FAILED', failure }));
    if (!pass) process.exitCode = 1;
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
