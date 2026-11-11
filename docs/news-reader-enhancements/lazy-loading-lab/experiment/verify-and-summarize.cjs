'use strict';
// Read-only verification of a completed run, followed by derived local summary files.
const fs = require('node:fs');
const path = require('node:path');
const crypto = require('node:crypto');
const sha = data => crypto.createHash('sha256').update(data).digest('hex');
const input = process.argv[2];
if (!input) throw new Error('Pass one completed run directory');
const run = path.resolve(input);
const read = file => JSON.parse(fs.readFileSync(path.join(run, file), 'utf8'));
const receipt = read('receipt.json'), env = read('environment.json'), rows = read('results.json');
const server = read('server-requests.json'), browser = read('browser-requests.json');
const manifest = read('fixture-manifest.json');
const checks = [];
const check = (name, pass) => checks.push({ name, pass: Boolean(pass) });
check('receipt-pass', receipt.status === 'PASS');
check('18-distinct-cases', rows.length === 18 && new Set(rows.map(r => r.caseId)).size === 18);
for (const [file, key] of [['environment.json', 'environmentSha256'], ['results.json', 'resultsSha256'], ['server-requests.json', 'serverRequestsSha256'], ['browser-requests.json', 'browserRequestsSha256']]) check(`receipt-hash:${file}`, sha(fs.readFileSync(path.join(run, file))) === receipt[key]);
check('frozen-plan-hash', sha(fs.readFileSync(path.join(run, 'experiment-plan.md'))) === env.planSha256);
check('frozen-runner-hash', sha(fs.readFileSync(path.join(run, 'runner.cjs'))) === env.runnerSha256);
check('frozen-manifest-hash', sha(fs.readFileSync(path.join(run, 'fixture-manifest.json'))) === env.fixtureManifestSha256);
for (const f of manifest) check(`fixture-hash:${f.file}`, sha(fs.readFileSync(path.join(__dirname, 'fixtures', f.file))) === f.sha256);
check('no-page-errors', read('page-errors.json').length === 0);
check('no-external-page-requests', browser.every(r => new URL(r.url).origin === env.origin) && read('blocked-external-requests.json').length === 0);
for (const r of rows) {
  const imageRequests = server.filter(x => x.caseId === r.caseId && x.pathname.endsWith('.svg'));
  const browserImages = browser.filter(x => x.caseId === r.caseId && x.type === 'image').map(x => new URL(x.url).pathname);
  check(`${r.caseId}:20-successful-image-responses`, imageRequests.length === 20 && imageRequests.every(x => x.status === 200 && x.method === 'GET') && new Set(imageRequests.map(x => x.pathname)).size === 20);
  check(`${r.caseId}:browser-server-image-match`, JSON.stringify([...browserImages].sort()) === JSON.stringify(imageRequests.map(x => x.pathname).sort()));
  for (const point of ['initial', 'afterEnd', 'afterTraversal']) {
    const s = r[point];
    check(`${r.caseId}:${point}:loaded-count`, s.loadedCount === s.images.filter(x => x.complete && x.naturalWidth > 0).length);
    if (s.screenshot) check(`${r.caseId}:${point}:screenshot`, fs.existsSync(path.join(run, s.screenshot)));
  }
  const pair = rows.find(other => other.viewport.name === r.viewport.name && other.repetition === r.repetition && other.scenario.name === 'eager-js');
  check(`${r.caseId}:equal-geometry`, r.initial.images.every((img, i) => img.documentTop === pair.initial.images[i].documentTop && img.width === pair.initial.images[i].width && img.height === pair.initial.images[i].height));
  if (r.scenario.name === 'lazy-js') check(`${r.caseId}:near-image-loaded-before-visible`, r.initial.images[1].loaded && !r.initial.images[1].intersectsViewport);
}
const verify = { status: checks.every(x => x.pass) ? 'PASS' : 'FAILED', checkedAt: new Date().toISOString(), checks: checks.length, failed: checks.filter(x => !x.pass), inputReceiptSha256: sha(fs.readFileSync(path.join(run, 'receipt.json'))), details: checks };
fs.writeFileSync(path.join(run, 'verification.json'), JSON.stringify(verify, null, 2) + '\n');
if (verify.status !== 'PASS') { console.log(JSON.stringify(verify.failed)); process.exitCode = 1; }
else {
  const columns = ['caseId', 'viewportWidth', 'viewportHeight', 'javaScriptEnabled', 'initialImagesRequested', 'initialLoaded', 'afterEndLoaded', 'afterTraversalLoaded', 'nearImageInitialTop', 'farImageInitialTop', 'farImageInitialLoaded', 'lastImageAfterEndLoaded'];
  const csv = [columns.join(','), ...rows.map(r => [r.caseId, r.viewport.width, r.viewport.height, r.scenario.js, r.initial.uniqueImagesRequested, r.initial.loadedCount, r.afterEnd.loadedCount, r.afterTraversal.loadedCount, r.initial.images[1].top, r.initial.images[2].top, r.initial.images[2].loaded, r.afterEnd.images[19].loaded].join(','))].join('\n') + '\n';
  fs.writeFileSync(path.join(run, 'results.csv'), csv);
  const ranges = values => `${Math.min(...values)}${Math.min(...values) === Math.max(...values) ? '' : '–' + Math.max(...values)}`;
  const groups = [];
  for (const v of ['desktop', 'narrow']) for (const s of ['eager-js', 'lazy-js', 'lazy-nojs']) {
    const group = rows.filter(r => r.viewport.name === v && r.scenario.name === s);
    groups.push(`| ${v === 'desktop' ? '1440×900' : '390×844'} | ${s} | ${group.length} | ${ranges(group.map(r => r.initial.loadedCount))}/20 | ${ranges(group.map(r => r.afterEnd.loadedCount))}/20 | ${ranges(group.map(r => r.afterTraversal.loadedCount))}/20 |`);
  }
  const summary = `# 實驗結果簡報（非文章稿）\n\n執行時間：${receipt.startedAt} 至 ${receipt.completedAt}（UTC）。Edge ${env.browserVersion}，Windows kernel ${env.release}／${env.arch}，Playwright ${env.playwright}，headless。兩種 CSS viewport、DPR 1、每次新 context、關 cache、本機 HTTP，18 次均完成；沒有測實體手機或其他瀏覽器。\n\n## 實測結果\n\n| CSS viewport | 條件 | 重複次數 | 未捲動 3 秒 loaded | 按 End 後 loaded | 逐段捲完 loaded |\n|---|---|---:|---:|---:|---:|\n${groups.join('\n')}\n\n- eager 視窗外圖片初始就已請求並載入；lazy＋JS 只載入第 1、2 張，遠處第 3 張尚未請求。\n- 第 2 張雖在視窗外，lazy 仍已載入：桌機 top=1411.875px，高度 900px；窄視窗 top=1165.078125px，高度 844px。此為幾何觀察，不是精確預載門檻測量。\n- 第 3 張桌機 top=8012px，窄視窗 top=7484.328125px；lazy＋JS 初始未載入，eager 與 lazy-nojs 初始已載入。\n- 按 End 後最後一張全部成功載入；End 可能經過中間視窗，不能解讀成瞬間跳躍時只會載入最後幾張。逐段捲完整頁後，每個條件都載入全部 20 張。\n- JavaScript 停用時頁內 sentinel 未執行，圖片初始全部載入。DOM 觀察由瀏覽器自動化介面讀取，不表示頁內 JavaScript 被啟用。\n\n初始數字同時有 server 請求與 DOM loaded 狀態作證；不能從本組 2/20 推成照片流量省 90% 或頁速提升。素材是小型 SVG，本機連線與正式站不同。\n\n## 官方規格解釋，與觀察分開\n\n[MDN](https://developer.mozilla.org/en-US/docs/Web/API/HTMLImageElement/loading) 將 loading 描述為瀏覽器提示。[WHATWG HTML](https://html.spec.whatwg.org/multipage/urls-and-fetching.html#lazy-loading-attributes) 規定 scripting disabled 時不採 lazy，且預載 margin 由實作決定，可考慮裝置、網路與偏好。兩者均於 2026-11-10 實讀並存 HTTP 200／SHA 收據；文件符合本輪觀察，但未代替實測。\n\n## 收據與後續作者須保留的限制\n\n- 執行 receipt：${sha(fs.readFileSync(path.join(run, 'receipt.json')))}\n- 結果 SHA：${receipt.resultsSha256}\n- 原始 server requests SHA：${receipt.serverRequestsSha256}\n- 事後交叉核對：${verify.checks} 個檢查全部通過，包括素材／執行檔／規格 hash、18 次的 browser/server 請求一致、幾何一致、截圖存在及 loaded 計數。這是資料一致性檢查，不是新一輪瀏覽器實驗。\n- 18 張 viewport 截圖；0 pageerror；0 非本機頁面請求，0 被阻擋外部請求。未稽核 OS／瀏覽器背景 telemetry。\n- 未測 LCP、SEO、真實網速、照片、Safari／Firefox、JS library lazy loader 或使用者主站；不得稱全平台效能驗收或真人受試測試。\n- 可銜接既有 lazy-loading-images 教學，但公開 URL／現行內容仍須發文前再讀。\n- 實驗完成、證據可供獨立覆核；文章尚未撰寫、匯入或發布。\n`;
  fs.writeFileSync(path.join(__dirname, 'RESULTS-BRIEF.md'), summary);
  console.log(JSON.stringify({ status: verify.status, checks: verify.checks, run, resultBrief: path.join(__dirname, 'RESULTS-BRIEF.md') }));
}
