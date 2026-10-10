import fs from 'node:fs';
import path from 'node:path';
import http from 'node:http';
import crypto from 'node:crypto';
import os from 'node:os';
import assert from 'node:assert/strict';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';

// Run after build-final-gallery.mjs has written the final gallery and index.
// Usage: node verify-final-gallery.mjs <episode-media-directory>
// This verifies the gallery, not artwork acceptance or animation readiness.
const scriptPath = fileURLToPath(import.meta.url);
const scriptDir = path.dirname(scriptPath);
if (process.argv.includes('--help') || !process.argv[2]) {
  console.log('Usage: node verify-final-gallery.mjs <episode-media-directory>');
  console.log('Writes gallery-verification-20261009.json beside this script and screenshots under final-art/20261009/qa/.');
  process.exit(process.argv.includes('--help') ? 0 : 1);
}

const media = fs.realpathSync(path.resolve(process.argv[2]));
const galleryDir = path.join(media, 'final-art/20261009');
const galleryPath = path.join(galleryDir, 'gallery.html');
const indexPath = path.join(galleryDir, 'gallery-index.json');
const qaDir = path.join(galleryDir, 'qa');
const reportPath = path.join(scriptDir, 'gallery-verification-20261009.json');
const portableRoots = [
  [media, '<VIDEO_WORKDIR>/ou-de-jianghu-e001'],
  [path.resolve(scriptDir, '../../../../../..'), '<REPO>'],
  [os.homedir(), '<USER_HOME>'],
].map(([root, token]) => [root.replaceAll('\\', '/'), token]);
// Normalize only serialized evidence; filesystem operations keep their real paths.
const portable = value => {
  if (typeof value === 'string') {
    let result = value.replaceAll('\\', '/');
    for (const [root, token] of portableRoots) {
      result = result.replaceAll('file:///' + root, token).replaceAll(root, token);
    }
    return result.replace(/http:\/\/127\.0\.0\.1:\d+/g, '<LOCAL_MEDIA_SERVER>');
  }
  if (Array.isArray(value)) return value.map(portable);
  if (value && typeof value === 'object') return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, portable(item)]));
  return value;
};
const sha = value => crypto.createHash('sha256').update(value).digest('hex');
const within = (root, file) => {
  const relative = path.relative(root, file);
  return relative !== '..' && !relative.startsWith('..' + path.sep) && !path.isAbsolute(relative);
};
const read = file => fs.readFileSync(file);
const counts = (rows, field) => Object.fromEntries(
  [...new Set(rows.map(row => row[field]))].sort().map(key => [key, rows.filter(row => row[field] === key).length]),
);
const expectedCategories = { concept: 9, portrait: 27, reference: 82, scene: 28 };
const expectedCharacters = {
  'bao-sanqian': 13, ensemble: 2, 'ji-wen': 13, 'ji-wushuang': 13,
  'luo-qingyan': 13, 'nie-gutie': 13, scene: 28, 'shen-guihe': 13,
  'xuanmen-elder': 13, 'yan-hui': 13, 'yin-wusheng': 12,
};
const { chromium } = createRequire(import.meta.url)('playwright');
const report = {
  schema_version: 1,
  started_at_utc: new Date().toISOString(),
  status: 'running',
  engine: 'Microsoft Edge via Playwright, headless, local HTTP only',
  scope: 'Local gallery bytes, image decoding, filtering, dialog, mobile layout and navigation. Does not accept artwork, approve a look or plan, verify lip-sync, or accept animation.',
  artwork_accepted: false,
  animation_accepted: false,
  production_approved: false,
  visual_review: { status: 'pending_manual_view_image', screenshots: [] },
  page_errors: [], request_failures: [],
};
let server;
let browser;

try {
  fs.mkdirSync(qaDir, { recursive: true });
  const galleryBytes = read(galleryPath);
  const indexBytes = read(indexPath);
  const { rows } = JSON.parse(indexBytes);
  assert.equal(rows.length, 146, 'gallery-index row count');
  assert.equal(new Set(rows.map(row => row.key)).size, 146, 'unique keys');
  assert.equal(new Set(rows.map(row => row.sha256)).size, 146, 'unique image hashes');
  assert.deepEqual(counts(rows, 'category'), expectedCategories, 'category cohorts');
  assert.deepEqual(counts(rows, 'character'), expectedCharacters, 'character cohorts');
  report.inputs = {
    gallery: { file: galleryPath, sha256: sha(galleryBytes) },
    index: { file: indexPath, sha256: sha(indexBytes) },
    verifier: { file: scriptPath, sha256: sha(read(scriptPath)) },
  };
  report.category_counts = counts(rows, 'category');
  report.character_counts = counts(rows, 'character');
  report.images = rows.map(row => {
    assert(!/^[a-z][a-z\d+.-]*:/i.test(row.src), 'source must be a local relative file');
    const file = fs.realpathSync(path.resolve(galleryDir, row.src));
    assert(within(media, file), 'image escaped episode media directory: ' + row.key);
    const bytes = read(file);
    assert.equal(sha(bytes), row.sha256, 'image SHA: ' + row.key);
    assert.equal(bytes.subarray(0, 8).toString('hex'), '89504e470d0a1a0a', 'PNG signature: ' + row.key);
    const width = bytes.readUInt32BE(16), height = bytes.readUInt32BE(20);
    assert.equal(width, row.width, 'PNG width: ' + row.key);
    assert.equal(height, row.height, 'PNG height: ' + row.key);
    return { key: row.key, character: row.character, category: row.category, src: row.src,
      sha256: row.sha256, width, height, bytes: bytes.length, sha_matches: true };
  });
  report.sha_verified_images = report.images.length;

  server = http.createServer((request, response) => {
    try {
      const requestPath = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
      const file = path.resolve(media, '.' + requestPath);
      if (!within(media, file)) { response.writeHead(403).end(); return; }
      if (!fs.existsSync(file) || !fs.statSync(file).isFile()) { response.writeHead(404).end(); return; }
      if (!within(media, fs.realpathSync(file))) { response.writeHead(403).end(); return; }
      const types = { '.html': 'text/html; charset=utf-8', '.png': 'image/png', '.svg': 'image/svg+xml', '.json': 'application/json' };
      response.setHeader('Content-Type', types[path.extname(file)] || 'application/octet-stream');
      response.setHeader('Cache-Control', 'no-store');
      response.end(read(file));
    } catch { response.writeHead(400).end(); }
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  const origin = 'http://127.0.0.1:' + server.address().port;
  browser = await chromium.launch({ channel: 'msedge', headless: true });
  report.browser_version = browser.version();
  const page = await browser.newPage({ viewport: { width: 1360, height: 1000 }, deviceScaleFactor: 1 });
  page.on('pageerror', error => report.page_errors.push(error.message));
  page.on('requestfailed', request => report.request_failures.push({ url: request.url(), error: request.failure()?.errorText }));
  const response = await page.goto(origin + '/final-art/20261009/gallery.html', { waitUntil: 'domcontentloaded' });
  assert.equal(response.status(), 200, 'gallery HTTP status');
  assert.equal(sha(await response.body()), report.inputs.gallery.sha256, 'served HTML SHA');
  const cardData = await page.locator('.card').evaluateAll(cards => cards.map(card => ({
    character: card.dataset.character, category: card.dataset.category,
    src: card.dataset.src, image_src: card.querySelector('img')?.getAttribute('src'),
  })));
  assert.deepEqual(cardData, rows.map(row => ({ character: row.character, category: row.category, src: row.src, image_src: row.src })), 'rendered cards match index');
  const decoded = await page.evaluate(async () => {
    const images = [...document.querySelectorAll('.card img')];
    images.forEach(image => { image.loading = 'eager'; });
    return await Promise.all(images.map(async image => {
      await image.decode();
      return { src: image.getAttribute('src'), complete: image.complete, width: image.naturalWidth, height: image.naturalHeight };
    }));
  });
  assert.equal(decoded.length, 146, 'decoded image count');
  for (let i = 0; i < rows.length; i++) {
    assert.deepEqual(decoded[i], { src: rows[i].src, complete: true, width: rows[i].width, height: rows[i].height }, 'decoded dimensions: ' + rows[i].key);
    report.images[i].browser_decode = true;
  }
  report.decoded_images = decoded.length;
  const settle = () => page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
  const shot = async (name, viewport) => {
    await settle();
    const file = path.join(qaDir, name + '.png');
    await page.screenshot({ path: file });
    const entry = { name, file, sha256: sha(read(file)), viewport };
    report.visual_review.screenshots.push(entry);
  };
  await shot('final-gallery-desktop', { width: 1360, height: 1000 });

  const characterOptions = await page.locator('#character option').evaluateAll(options => options.map(option => option.value));
  const categoryOptions = await page.locator('#category option').evaluateAll(options => options.map(option => option.value));
  assert.deepEqual([...characterOptions].sort(), ['all', ...Object.keys(expectedCharacters)].sort(), 'character filter options');
  assert.deepEqual([...categoryOptions].sort(), ['all', ...Object.keys(expectedCategories)].sort(), 'category filter options');
  report.filters = [];
  for (const character of characterOptions) {
    for (const category of categoryOptions) {
      await page.selectOption('#character', character);
      await page.selectOption('#category', category);
      const expected = rows.filter(row => (character === 'all' || row.character === character) && (category === 'all' || row.category === category)).length;
      assert.equal(await page.locator('.card:visible').count(), expected, 'visible filters: ' + character + '/' + category);
      assert.equal(await page.locator('#count').textContent(), expected + ' 張', 'filter count text');
      report.filters.push({ character, category, expected, actual: expected });
    }
  }
  report.filter_combinations = report.filters.length;

  await page.selectOption('#character', 'shen-guihe');
  await page.selectOption('#category', 'portrait');
  const modalRow = rows.find(row => row.character === 'shen-guihe' && row.category === 'portrait' && row.key.includes('full-body'));
  assert(modalRow, 'full-body portrait for modal');
  const modalCard = page.locator('.card').filter({ has: page.locator('img[src=' + JSON.stringify(modalRow.src) + ']') });
  await modalCard.click();
  assert(await page.locator('#viewer').isVisible(), 'modal opened');
  const large = await page.locator('#large').evaluate(async image => { await image.decode(); return { width: image.naturalWidth, height: image.naturalHeight, src: image.getAttribute('src') }; });
  assert.deepEqual(large, { width: modalRow.width, height: modalRow.height, src: modalRow.src }, 'modal image');
  await shot('final-gallery-modal', { width: 1360, height: 1000 });
  await page.keyboard.press('Escape');
  assert(!(await page.locator('#viewer').isVisible()), 'Escape closed modal');
  report.modal = { key: modalRow.key, decoded: true, opened: true, escape_closed: true };

  await page.setViewportSize({ width: 390, height: 844 });
  await page.selectOption('#character', 'all');
  await page.selectOption('#category', 'all');
  await page.evaluate(() => window.scrollTo(0, 0));
  await settle();
  const geometry = await page.evaluate(() => ({ inner_width: innerWidth, document_width: document.documentElement.scrollWidth, body_width: document.body.scrollWidth }));
  assert(geometry.document_width <= geometry.inner_width, 'mobile document overflow');
  assert(geometry.body_width <= geometry.inner_width, 'mobile body overflow');
  await shot('final-gallery-mobile', { width: 390, height: 844 });
  report.mobile = { ...geometry, overflow: false, viewport: { width: 390, height: 844 } };

  const links = await page.locator('nav a').evaluateAll(anchors => anchors.map(anchor => ({ label: anchor.textContent, href: anchor.href })));
  assert.equal(links.length, 3, 'navigation link count');
  report.navigation = [];
  for (const link of links) {
    assert.equal(new URL(link.href).origin, origin, 'navigation stays on local media server');
    const result = await page.request.get(link.href);
    assert.equal(result.status(), 200, 'navigation HTTP status: ' + link.label);
    report.navigation.push({ label: link.label, path: new URL(link.href).pathname, status: result.status(), sha256: sha(await result.body()) });
  }
  assert.deepEqual(report.page_errors, [], 'browser page errors');
  assert.deepEqual(report.request_failures, [], 'browser request failures');
  // Fail if the gallery or index changed during this run; rebuilds require a new verification.
  assert.equal(sha(read(galleryPath)), report.inputs.gallery.sha256, 'gallery changed during run');
  assert.equal(sha(read(indexPath)), report.inputs.index.sha256, 'index changed during run');
  report.status = 'automated_checks_passed_pending_visual_review';
  console.log(JSON.stringify(portable({ status: report.status, decoded_images: report.decoded_images, sha_verified_images: report.sha_verified_images, filter_combinations: report.filter_combinations, report: reportPath, screenshots: report.visual_review.screenshots.map(item => item.file) }), null, 2));
} catch (error) {
  report.status = 'failed';
  report.error = { message: error.message, stack: error.stack };
  console.error(portable(error.stack || error.message));
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  if (server?.listening) await new Promise(resolve => server.close(resolve));
  report.completed_at_utc = new Date().toISOString();
  fs.writeFileSync(reportPath, JSON.stringify(portable(report), null, 2) + '\n');
}
