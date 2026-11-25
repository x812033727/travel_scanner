/**
 * Zero-dependency HTML QA gallery and manifest writer for generated Flow stills
 * and clips. Works on Windows by double-clicking `qa-gallery.html` in Explorer.
 */

import fs from "node:fs";
import path from "node:path";
import { atomicWriteJson } from "../guards/budget-guard.mjs";

function escapeHtml(value) {
  return String(value ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function toRelativePosix(fromDir, targetPath) {
  if (!targetPath) return "";
  return path.relative(fromDir, targetPath).split(path.sep).join("/");
}

/**
 * Writes an interactive local HTML gallery (`stills/qa-gallery.html`) for
 * zero-credit visual QA before unlocking paid video generation.
 */
export function writeStillsQaGallery({ galleryFile, slug, series, items = [] }) {
  const dir = path.dirname(galleryFile);
  fs.mkdirSync(dir, { recursive: true });

  const cards = items
    .map((item) => {
      const relImg = toRelativePosix(dir, item.filePath);
      const statusClass =
        item.qaStatus === "approved"
          ? "ok"
          : item.qaStatus === "rejected" || item.aspectOk === false
            ? "bad"
            : "pending";
      const dimLabel =
        item.width && item.height ? `${item.width}×${item.height}` : "unknown";
      return `<article class="card ${statusClass}">
  <header>
    <strong>${escapeHtml(item.shotId)}</strong>
    <span class="badge">${escapeHtml(item.track || "scenery")}</span>
    <span class="badge">${escapeHtml(dimLabel)}</span>
    <span class="badge status">${escapeHtml(item.qaStatus || "pending")}</span>
  </header>
  ${relImg ? `<img src="${escapeHtml(relImg)}" alt="${escapeHtml(item.shotId)}" loading="lazy" />` : `<div class="missing">Missing file</div>`}
  <p class="prompt">${escapeHtml(item.prompt || "")}</p>
  ${item.note ? `<p class="note">${escapeHtml(item.note)}</p>` : ""}
</article>`;
    })
    .join("\n");

  const html = `<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8" />
<title>Flow Stills QA — ${escapeHtml(slug)}</title>
<style>
  body { font-family: system-ui, -apple-system, sans-serif; background: #111318; color: #eceff4; margin: 24px; }
  h1 { font-size: 20px; margin: 0 0 8px; }
  .meta { color: #9aa4b2; font-size: 13px; margin-bottom: 20px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(360px, 1fr)); gap: 16px; }
  .card { background: #1a1e26; border: 2px solid #2b3240; border-radius: 10px; overflow: hidden; padding: 12px; }
  .card.ok { border-color: #2e8b57; }
  .card.bad { border-color: #d64545; }
  .card header { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 8px; }
  .badge { font-size: 11px; padding: 2px 7px; border-radius: 999px; background: #293142; color: #d8dee9; }
  .card.ok .status { background: #1f5c3a; }
  .card.bad .status { background: #7f2323; }
  img { width: 100%; height: auto; display: block; border-radius: 6px; background: #000; }
  .prompt { font-size: 12px; color: #b8c2d1; margin: 8px 0 0; line-height: 1.45; }
  .note { font-size: 12px; color: #f6b73c; margin: 6px 0 0; }
  .missing { padding: 48px 12px; text-align: center; background: #261a1a; color: #f28b82; border-radius: 6px; }
</style>
</head>
<body>
  <h1>Flow 0 點數靜圖 QA — ${escapeHtml(slug)} (${escapeHtml(series)})</h1>
  <div class="meta">共 ${items.length} 張 · 檢查重點：1376×768 寬銀幕、五指與角色設定、無亂碼招牌字、無現代穿越物。驗收後呼叫 <code>flow_approve_stills</code> 解鎖影片生成。</div>
  <section class="grid">
${cards}
  </section>
</body>
</html>
`;
  fs.writeFileSync(galleryFile, html, "utf8");
  return galleryFile;
}

/**
 * Writes an HTML gallery for upscaled 1080p30 clips + 4-frame QA sheets.
 */
export function writeClipsQaGallery({ galleryFile, slug, series, clips = [] }) {
  const dir = path.dirname(galleryFile);
  fs.mkdirSync(dir, { recursive: true });

  const cards = clips
    .map((clip) => {
      const relQa4 = toRelativePosix(dir, clip.qa4Path);
      const relMp4 = toRelativePosix(dir, clip.upscaledPath || clip.rawPath);
      return `<article class="card">
  <header>
    <strong>${escapeHtml(clip.shotId)}</strong>
    <span class="badge">${escapeHtml(clip.model || "omni-1.2-flash")}</span>
    <span class="badge">${escapeHtml(clip.credits ?? 12)} credits</span>
  </header>
  ${relQa4 ? `<img src="${escapeHtml(relQa4)}" alt="${escapeHtml(clip.shotId)} 4-frame QA" loading="lazy" />` : ""}
  ${relMp4 ? `<video controls preload="metadata" src="${escapeHtml(relMp4)}"></video>` : ""}
  <p class="prompt">${escapeHtml(clip.prompt || "")}</p>
</article>`;
    })
    .join("\n");

  const html = `<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8" />
<title>Flow Clips QA — ${escapeHtml(slug)}</title>
<style>
  body { font-family: system-ui, -apple-system, sans-serif; background: #111318; color: #eceff4; margin: 24px; }
  h1 { font-size: 20px; margin: 0 0 8px; }
  .meta { color: #9aa4b2; font-size: 13px; margin-bottom: 20px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 16px; }
  .card { background: #1a1e26; border: 1px solid #2b3240; border-radius: 10px; padding: 12px; }
  .card header { display: flex; gap: 8px; align-items: center; margin-bottom: 8px; }
  .badge { font-size: 11px; padding: 2px 7px; border-radius: 999px; background: #293142; color: #d8dee9; }
  img, video { width: 100%; border-radius: 6px; margin-bottom: 8px; background: #000; display: block; }
  .prompt { font-size: 12px; color: #b8c2d1; margin: 0; line-height: 1.45; }
</style>
</head>
<body>
  <h1>Flow 1080p30 動態鏡頭 QA — ${escapeHtml(slug)} (${escapeHtml(series)})</h1>
  <div class="meta">共 ${clips.length} 支片段（720p 原檔免費下載 → Lanczos 1080p30 / bt709 / tv / -an）。</div>
  <section class="grid">
${cards}
  </section>
</body>
</html>
`;
  fs.writeFileSync(galleryFile, html, "utf8");
  return galleryFile;
}

/**
 * Updates `flow-clips/manifest.json` atomically.
 */
export function saveClipsManifest(manifestFile, manifest) {
  atomicWriteJson(manifestFile, {
    schemaVersion: 1,
    updatedAt: new Date().toISOString(),
    ...manifest,
  });
  return manifestFile;
}
