#!/usr/bin/env node
// Optional local-media browser smoke check; not part of tools-only CI.
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { chromium } from 'playwright';

const output = path.resolve(process.argv[2] || '/workspace/elementary-season01-output');
const requested = (process.argv[3] || 'ep01').split(',');
const report = { checked_at: new Date().toISOString(), passed: false,
  engine: 'Real headless Chromium, local file URL, actual H.264/AAC playback; no media mocks',
  episodes: requested, checks: [], voice_samples: [], browser_errors: [] };
let browser;
try {
  browser = await chromium.launch({ executablePath: process.env.CHROMIUM_BIN || '/usr/bin/chromium',
    headless: true, args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  report.browser_version = browser.version();
  const page = await browser.newPage({ viewport: { width: 1365, height: 1100 } });
  await page.route(/^https?:/, route => route.abort());
  page.on('pageerror', error => report.browser_errors.push(error.message));
  await page.goto(pathToFileURL(path.join(output, 'index.html')).href);
  assert.equal(await page.locator('.episode-card').count(), 12);
  assert.equal(await page.locator('#voice option').count(), 5);
  assert.equal(await page.locator('#cc option[value=en]').count(), 0);
  await page.waitForFunction(() => document.querySelector('#video').readyState >= 2 && document.querySelector('#audio').readyState >= 2);
  await page.locator('#start-play').click();
  await page.waitForFunction(() => document.querySelector('#video').currentTime > .6 && document.querySelector('#audio').currentTime > .5);
  for (const locale of ['zh-TW', 'en', 'zh-CN', 'ja', 'ko']) {
    await page.selectOption('#voice', locale);
    await page.waitForFunction(locale => {
      const a = document.querySelector('#audio'), v = document.querySelector('#video');
      return a.src.endsWith(`/${locale}.m4a`) && !a.paused && !v.paused && a.readyState >= 2 && !a.error && !v.error;
    }, locale);
    const before = await page.locator('#video').evaluate(v => v.currentTime);
    await page.waitForFunction(before => document.querySelector('#video').currentTime > before + .5, before);
    const sample = await page.evaluate(() => ({
      voice: document.querySelector('#voice').value,
      video_time: document.querySelector('#video').currentTime,
      audio_time: document.querySelector('#audio').currentTime,
      muted_video: document.querySelector('#video').muted,
      audio_muted: document.querySelector('#audio').muted,
    }));
    assert.ok(Math.abs(sample.video_time - sample.audio_time) < .6, JSON.stringify(sample));
    assert.equal(sample.muted_video, true);
    assert.equal(sample.audio_muted, false);
    report.voice_samples.push(sample);
  }
  report.checks.push('All five real AAC sidecars play while the muted H.264 film advances, with audio/video clocks within 0.6 seconds');
  await page.locator('#play').click();
  await page.selectOption('#cc', 'ja');
  const cue = await page.evaluate(() => JSON.parse(document.querySelector('#episode-data').textContent)[0].captions.ja[0]);
  async function seek(time) {
    await page.locator('#seek').evaluate((slider, time) => { slider.value = String(time); slider.dispatchEvent(new Event('input', { bubbles: true })); }, time);
    await page.waitForFunction(time => {
      const v = document.querySelector('#video'), a = document.querySelector('#audio');
      return !v.seeking && Math.abs(v.currentTime-time) < .15 && Math.abs(a.currentTime-time) < .15;
    }, time);
  }
  await seek((cue.start + cue.end)/2);
  assert.equal(await page.locator('#caption-text').textContent(), cue.text);
  assert.equal(await page.locator('#voice').inputValue(), 'ko');
  const resolved = JSON.parse(await fs.readFile(path.join(output, 'lessons.resolved.json'), 'utf8'));
  const quiz = resolved.episodes[0].scenes.find(s => s.mode === 'quiz');
  await seek(quiz.start + quiz.demo_end + .5);
  assert.equal(await page.locator('#caption-text').textContent(), '');
  await seek(quiz.start + quiz.reveal_at + .25);
  assert.equal(await page.locator('#caption-text').textContent(), quiz.demo_translation.ja);
  await page.selectOption('#cc', 'off');
  assert.equal(await page.locator('#caption-text').textContent(), '');
  report.checks.push('Japanese CC is independent of Korean audio; actual seek synchronizes both elements; quiz wait hides CC and reveal shows its translation; CC off hides text');
  for (const eid of requested) {
    await page.locator(`.episode-card[data-id=${eid}]`).click();
    await page.waitForFunction(eid => {
      const v = document.querySelector('#video'), a = document.querySelector('#audio');
      return v.src.endsWith(`/${eid}/final.mp4`) && a.src.includes(`/${eid}/audio/`) && v.readyState >= 2 && a.readyState >= 2 && !v.error && !a.error;
    }, eid);
    await page.locator('#start-play').click();
    await page.waitForFunction(() => document.querySelector('#video').currentTime > .2 && document.querySelector('#audio').currentTime > .1);
    await page.locator('#play').click();
  }
  report.checks.push('Requested episode files load and begin real playback after selection');
  await page.screenshot({ path: path.join(output, 'player-desktop.png'), fullPage: true });
  await page.setViewportSize({ width: 390, height: 844 });
  const layout = await page.evaluate(() => ({ viewport: innerWidth, page: document.documentElement.scrollWidth }));
  assert.ok(layout.page <= layout.viewport, JSON.stringify(layout));
  await page.screenshot({ path: path.join(output, 'player-mobile.png'), fullPage: true });
  report.checks.push('390px mobile layout has no horizontal overflow');
  assert.deepEqual(report.browser_errors, []);
  report.passed = true;
} catch (error) {
  report.error = String(error?.stack || error);
  process.exitCode = 1;
} finally {
  if (browser) await browser.close();
  await fs.writeFile(path.join(output, 'browser-checks.json'), JSON.stringify(report, null, 2)+'\n');
  console.log(JSON.stringify(report, null, 2));
}
