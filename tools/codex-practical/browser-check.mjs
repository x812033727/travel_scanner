#!/usr/bin/env node
// Actual learner-site observations, never native Codex App evidence.
import assert from 'node:assert/strict';
import { createServer } from 'node:http';
import { readFileSync, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { pathToFileURL } from 'node:url';
import { chromium } from '@playwright/test';

const { values } = parseArgs({ options: { run: { type:'string' } } });
if (!values.run) throw new Error('Use --run external lesson-01-cli directory');
const run = path.resolve(values.run);
const out = path.join(run, 'browser');
mkdirSync(out, { recursive:true });
const checks = [];
const contentTypes = { '.html':'text/html', '.js':'text/javascript', '.mjs':'text/javascript', '.css':'text/css' };
const server = createServer((req, res) => {
  try {
    const parts = new URL(req.url, 'http://localhost').pathname.split('/').filter(Boolean);
    if (!['start','reference'].includes(parts[0]) || parts.some(p => p === '..')) throw new Error('path');
    const file = path.resolve(run, ...parts, ...(parts.length === 1 ? ['index.html'] : []));
    if (!file.startsWith(run + path.sep)) throw new Error('path');
    res.setHeader('Content-Type', contentTypes[path.extname(file)] ?? 'application/octet-stream');
    res.end(readFileSync(file));
  } catch { res.writeHead(404); res.end('Not found'); }
});
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
const browser = await chromium.launch({ channel:'msedge', headless:true });
const base = `http://127.0.0.1:${server.address().port}`;
try {
  const fileContext = await browser.newContext();
  const filePage = await fileContext.newPage();
  const fileErrors = [];
  filePage.on('console', message => { if (message.type() === 'error') fileErrors.push(message.text()); });
  filePage.on('pageerror', error => fileErrors.push(error.message));
  await filePage.goto(pathToFileURL(path.join(run, 'start/index.html')).href);
  await filePage.waitForLoadState('networkidle');
  const fileMode = { variant:'start', name:'file-url-module-loading', error_count:fileErrors.length,
    cors_observed:fileErrors.some(error => /CORS|cross origin/i.test(error)),
    classification:fileErrors.length ? 'observed-startup-failure; use-local-HTTP' : 'no-failure-observed' };
  checks.push(fileMode);
  await fileContext.close();
  for (const variant of ['start','reference']) {
    const context = await browser.newContext({ viewport:{ width:390, height:844 } });
    const page = await context.newPage();
    const errors = [];
    page.on('pageerror', error => errors.push(error.message));
    await page.goto(`${base}/${variant}/`);
    const add = async title => {
      await page.locator('#task-title').fill(title);
      await page.locator('#task-form button[type=submit]').click();
    };
    await add('Read'); await add('Build');
    await page.locator('#tasks input').first().check();
    await page.locator('#filter').selectOption('active');
    const active = await page.locator('#tasks li').count();
    assert.equal(active, variant === 'start' ? 2 : 1);
    checks.push({ variant, name:'active-filter', observed:active,
      classification:variant === 'start' ? 'intentional-unimplemented-filter' : 'pass' });
    await page.locator('#filter').selectOption('completed');
    assert.equal(await page.locator('#tasks li').count(), variant === 'start' ? 2 : 1);
    await page.screenshot({ path:path.join(out, `${variant}-filter.png`), fullPage:true });
    await page.reload();
    assert.equal(await page.locator('#tasks li').count(), 2);
    assert.equal(await page.locator('#tasks input:checked').count(), 1);
    checks.push({ variant, name:'reload-preserves-all-tasks-and-completion', classification:'pass' });
    await add('Read');
    await page.locator('#tasks button').last().click();
    assert.equal(await page.locator('#tasks li').count(), 2);
    assert.equal(await page.locator('#tasks input:checked').count(), 1);
    checks.push({ variant, name:'same-title-delete-targets-selected-identity', classification:'pass' });
    await add('<img src=x>');
    assert.equal(await page.locator('#tasks img').count(), 0);
    assert.equal(await page.locator('#tasks span').last().textContent(), '<img src=x>');
    checks.push({ variant, name:'markup-is-literal-text', classification:'pass' });
    assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
    checks.push({ variant, name:'390px-no-horizontal-overflow', classification:'pass' });
    await page.evaluate(() => {
      localStorage.setItem('mokaair-codex-todo-v1', '{bad-json');
      localStorage.setItem('unrelated-example', 'preserve-me');
    });
    await page.reload();
    assert.match(await page.locator('#message').textContent(), /cannot be read/);
    await add('Temporary');
    assert.equal(await page.evaluate(() => localStorage.getItem('mokaair-codex-todo-v1')), '{bad-json');
    await page.locator('details summary').click();
    await page.locator('#reset').click();
    assert.equal(await page.evaluate(() => localStorage.getItem('unrelated-example')), 'preserve-me');
    checks.push({ variant, name:'damaged-storage-preserved-and-reset-scoped', classification:'pass' });
    assert.deepEqual(errors, []);
    await context.close();
  }
  const receipt = { schema_version:1, checked_on:new Date().toISOString(),
    evidence_kind:'actual-Edge-learner-website; not-native-Codex-App', browser_version:browser.version(),
    node_version:process.version, checks };
  writeFileSync(path.join(out, 'receipt.json'), JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify({ checks:checks.length, result:'pass', evidence_kind:receipt.evidence_kind }));
} finally { await browser.close(); await new Promise(resolve => server.close(resolve)); }
