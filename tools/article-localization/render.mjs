/** Render staged SVGs, measure their text, and emit explicit layout-review receipts. */
import { chromium } from '@playwright/test';
import { createHash } from 'node:crypto';
import { readFile, writeFile, mkdir } from 'node:fs/promises';
import path from 'node:path';
import process from 'node:process';
import sharp from 'sharp';
import { fileURLToPath } from 'node:url';
import { loadBoundJob, finishRenderBinding } from './artifact-integrity.mjs';

const args = process.argv.slice(2);
if (args.length !== 2 || args[0] !== '--job') throw new Error('Usage: node tools/article-localization/render.mjs --job <staged job directory>');
const directory = path.resolve(args[1]);
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..');
const bound = await loadBoundJob(directory, root);
const { job, assets } = bound;
const browser = await chromium.launch({ headless: true });
const results = [];

function safeDimensions(source) {
  const viewBox = source.match(/\bviewBox=["']\s*([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)\s*["']/);
  const width = Number(source.match(/\bwidth=["']([\d.]+)["']/)?.[1] ?? viewBox?.[3]);
  const height = Number(source.match(/\bheight=["']([\d.]+)["']/)?.[1] ?? viewBox?.[4]);
  if (!(width >= 1 && width <= 4000 && height >= 1 && height <= 4000)) throw new Error('SVG dimensions must be between 1 and 4000 pixels');
  return { width: Math.ceil(width), height: Math.ceil(height) };
}

async function load(page, source, size) {
  if (/<script\b|\son\w+\s*=|<foreignObject\b/i.test(source)) throw new Error('Active SVG content is not supported');
  await page.setViewportSize(size);
  await page.setContent(`<meta charset="utf-8"><meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; img-src data:"><style>html,body{margin:0;padding:0}svg{display:block;width:${size.width}px;height:${size.height}px}</style>${source}`);
  await page.evaluate(() => document.fonts.ready);
  return page.locator('svg').evaluate(svg => {
    const box = node => { const r = node.getBoundingClientRect(); return { left: r.left, top: r.top, right: r.right, bottom: r.bottom, width: r.width, height: r.height }; };
    return {
      text: [...svg.querySelectorAll('text')].filter(node => node.textContent.trim()).map(node => ({ value: node.textContent, box: box(node), font: getComputedStyle(node).fontFamily, size: Number.parseFloat(getComputedStyle(node).fontSize) })),
      rectangles: [...svg.querySelectorAll('rect,circle,ellipse')].map(box),
    };
  });
}

const contains = (outer, inner, tolerance = 1) => inner.left >= outer.left - tolerance && inner.top >= outer.top - tolerance && inner.right <= outer.right + tolerance && inner.bottom <= outer.bottom + tolerance;
const overlaps = (a, b) => Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 && Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2;
const containerFor = (original, text) => original.rectangles.filter(rect => {
  const center = { x: (text.box.left + text.box.right) / 2, y: (text.box.top + text.box.bottom) / 2 };
  return rect.width > 0 && rect.height > 0 && center.x >= rect.left && center.x <= rect.right && center.y >= rect.top && center.y <= rect.bottom && text.box.width <= rect.width * 1.1 && text.box.height <= rect.height * 1.1;
}).sort((a, b) => a.width * a.height - b.width * b.height)[0];

try {
  const page = await browser.newPage();
  await page.route('**/*', route => route.abort());
  for (let index = 0; index < assets.length; index++) {
    const asset = assets[index];
    const svgPath = path.resolve(asset.svg);
    const relative = path.relative(directory, svgPath);
    if (relative.startsWith('..') || path.isAbsolute(relative)) throw new Error('Staged asset escaped job directory');
    let source = await readFile(svgPath, 'utf8');
    const size = safeDimensions(source);
    const original = await load(page, job.assets[index].source_svg, size);
    let localized = await load(page, source, size);
    const fontAdjustments = [];
    // Change only font size, retaining text, diagram shapes, anchors and coordinates.
    // Small badge labels such as "Three" need this even when body translation is exact.
    for (let pass = 0; pass < 4; pass++) {
      const adjustments = [];
      localized.text.forEach((text, textIndex) => {
        const originalText = original.text[textIndex];
        if (!originalText) return;
        const container = containerFor(original, originalText) ?? { left: 0, top: 0, right: size.width, bottom: size.height, width: size.width, height: size.height };
        if (contains(container, text.box)) return;
        const horizontalRoom = Math.max(1, container.right - container.left - 12);
        const verticalRoom = Math.max(1, container.bottom - container.top - 8);
        const ratio = Math.min(horizontalRoom / text.box.width, verticalRoom / text.box.height, 0.9);
        const fontSize = Math.max(14, Math.floor(text.size * ratio));
        if (fontSize < text.size) adjustments.push({ textIndex, before: text.size, after: fontSize });
      });
      if (!adjustments.length) break;
      await page.locator('svg').evaluate((svg, changes) => {
        const text = [...svg.querySelectorAll('text')].filter(node => node.textContent.trim());
        for (const change of changes) {
          text[change.textIndex].setAttribute('font-size', String(change.after));
          text[change.textIndex].style.fontSize = `${change.after}px`;
        }
      }, adjustments);
      fontAdjustments.push(...adjustments);
      source = await page.locator('svg').evaluate(svg => svg.outerHTML);
      localized = await load(page, source, size);
    }
    if (fontAdjustments.length) await writeFile(svgPath, source + '\n');
    const issues = [];
    if (original.text.length !== localized.text.length) issues.push({ reason: 'visible text node count changed' });
    localized.text.forEach((text, textIndex) => {
      const originalText = original.text[textIndex];
      const canvas = { left: 0, top: 0, right: size.width, bottom: size.height };
      if (!contains(canvas, text.box)) issues.push({ textIndex, text: text.value, reason: 'outside SVG canvas' });
      if (originalText) {
        const container = containerFor(original, originalText);
        if (container && !contains(container, text.box)) issues.push({ textIndex, text: text.value, reason: 'outside original containing shape' });
      }
      for (let other = 0; other < textIndex; other++) {
        if (overlaps(text.box, localized.text[other].box) && originalText && original.text[other] && !overlaps(originalText.box, original.text[other].box)) issues.push({ textIndex, other, reason: 'new text overlap' });
      }
    });
    const preview = svgPath.replace(/\.svg$/, '-preview.png');
    await page.screenshot({ path: preview, type: 'png' });
    const rendered = [];
    // An overflowing raster must never become a candidate for publication.
    if (!issues.length) {
      for (const target of asset.targets) {
        if (target.endsWith('.svg')) continue;
        const relativeTarget = target.replace(/^\//, '');
        const output = path.resolve(directory, 'assets', relativeTarget);
        if (path.relative(directory, output).startsWith('..')) throw new Error('Raster output escaped job directory');
        await mkdir(path.dirname(output), { recursive: true });
        if (target.endsWith('.webp')) {
          const png = await page.screenshot({ type: 'png' });
          await sharp(png).webp({ quality: 90 }).toFile(output);
        } else {
          await page.screenshot({ path: output, type: target.endsWith('.jpg') ? 'jpeg' : 'png', ...(target.endsWith('.jpg') ? { quality: 90 } : {}) });
        }
        rendered.push({ target, sha256: createHash('sha256').update(await readFile(output)).digest('hex') });
      }
    }
    results.push({ source: asset.public_svg, sha256: createHash('sha256').update(await readFile(svgPath)).digest('hex'), size, visibleTextNodes: localized.text.length, fontAdjustments, layoutIssues: issues, preview, rendered, visualReviewRequired: true, glyphReviewRequired: true });
  }
} finally { await browser.close(); }

const passed = results.every(result => result.layoutIssues.length === 0);
await finishRenderBinding(bound, { renderedAt: new Date().toISOString(), automatedLayoutPassed: passed, visualReviewComplete: false, glyphReviewComplete: false, results }, passed);
process.stdout.write(JSON.stringify({ slug: job.slug, locale: job.locale, automatedLayoutPassed: passed, assets: results.length, issues: results.flatMap(result => result.layoutIssues) }) + '\n');
if (!passed) process.exitCode = 1;
