import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { createHash } from 'node:crypto';
import { chromium } from '@playwright/test';

const dir = path.dirname(fileURLToPath(import.meta.url));
const poolDir = path.resolve(dir, '../..');
const browser = await chromium.launch({ headless: true });
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
  const errors = [];
  page.on('pageerror', error => errors.push(error.message));
  await page.goto(pathToFileURL(path.join(dir, 'demo.html')).href);
  const work = [];
  for (const mode of ['idle', 'main', 'worker']) work.push(await page.evaluate(mode => window.runWork(mode), mode));
  assert.ok(work[1].timer_elapsed_ms >= 650, 'main-thread timer did not wait for the simulated work');
  assert.ok(work[0].timer_elapsed_ms < 400 && work[2].timer_elapsed_ms < 400, 'control or worker timer delayed: repeat under recorded conditions before using this demo');
  assert.deepEqual(work[2].event_order, ['started', 'timer', 'done']);
  assert.equal(work[2].worker_evidence.timer_before_done, true);
  assert.ok(work[2].worker_evidence.work_elapsed_ms >= 650);
  assert.ok(work[2].worker_evidence.done_message_elapsed_ms > work[2].timer_elapsed_ms);
  const images = await page.evaluate(() => window.runImages());
  assert.ok(images.unreserved_delta_px > 50);
  assert.ok(Math.abs(images.reserved_delta_px) < 1);
  await page.screenshot({ path: path.join(poolDir, '.cache/wave4-g37-desktop.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  const mobileImages = await page.evaluate(() => window.runImages());
  assert.ok(Math.abs(mobileImages.reserved_delta_px) < 1);
  assert.equal(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth), true);
  await page.screenshot({ path: path.join(poolDir, '.cache/wave4-g37-mobile.png'), fullPage: true });
  assert.deepEqual(errors, []);
  const receipt = {
    status: 'PASS_CONTROLLED_DEMO_NOT_VIDEO_OR_AUDIENCE_TEST',
    tested_on: new Date().toISOString(),
    browser: await browser.version(), node: process.version,
    source_sha256: createHash('sha256').update(fs.readFileSync(path.join(dir, 'demo.html'))).digest('hex'),
    verifier_sha256: createHash('sha256').update(fs.readFileSync(fileURLToPath(import.meta.url))).digest('hex'),
    work, images, mobile_images: mobileImages,
    scope: 'Single run per condition, headless Chromium, local file, synthetic busy loop, timer callback latency; no input latency, INP, network-speed or population estimate. Positions are relative to each card.',
    screenshots: ['.cache/wave4-g37-desktop.png', '.cache/wave4-g37-mobile.png'],
    visual_inspection: 'PENDING', production_ready: false,
  };
  fs.writeFileSync(path.join(poolDir, 'reviews/wave4-g37-demo.json'), JSON.stringify(receipt, null, 2) + '\n');
  console.log(JSON.stringify(receipt));
} finally { await browser.close(); }
