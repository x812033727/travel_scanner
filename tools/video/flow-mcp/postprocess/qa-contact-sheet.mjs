/**
 * Zero-dependency interactive HTML QA galleries and manifest writer for
 * generated Flow stills and multi-take clips.
 *
 * Phase 2 upgrades:
 *   - Interactive Approve/Reject checkboxes + one-click Copy button emitting a
 *     ready-to-paste `flow_approve_stills` JSON payload for Claude/Codex/Antigravity
 *   - Toggleable 9:16 UI safe-zone red frame overlay (`drama-9x16` / `shorts`)
 *   - Multi-take clip cards displaying Take 1/2 history, PSNR, mid-clip hard-cut
 *     recommendations, and optional raw-audio sidecar preview player
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
 * Writes an interactive local HTML gallery (`stills/qa-gallery.html`) with
 * one-click `flow_approve_stills` JSON export and optional 9:16 safe-zone guide.
 */
export function writeStillsQaGallery({
  galleryFile,
  slug,
  series,
  items = [],
  safeZoneOverlay = false,
}) {
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
      const checkedApprove = item.qaStatus === "approved" ? "checked" : "";
      const checkedReject = item.qaStatus === "rejected" ? "checked" : "";
      return `<article class="card ${statusClass}" data-shot="${escapeHtml(item.shotId)}">
  <header>
    <strong>${escapeHtml(item.shotId)}</strong>
    <span class="badge">${escapeHtml(item.track || "scenery")}</span>
    <span class="badge">${escapeHtml(dimLabel)}</span>
    <span class="badge status">${escapeHtml(item.qaStatus || "pending")}</span>
  </header>
  <div class="frame-wrap">
    ${relImg ? `<img src="${escapeHtml(relImg)}" alt="${escapeHtml(item.shotId)}" loading="lazy" />` : `<div class="missing">Missing file</div>`}
    ${safeZoneOverlay ? `<div class="safe-zone" title="9:16 Safe Zone"></div>` : ""}
  </div>
  <div class="qa-controls">
    <label><input type="radio" name="qa_${escapeHtml(item.shotId)}" value="approved" ${checkedApprove} /> 通過</label>
    <label><input type="radio" name="qa_${escapeHtml(item.shotId)}" value="rejected" ${checkedReject} /> 退回</label>
    <input type="text" class="qa-note" placeholder="備註／退回原因" value="${escapeHtml(item.note || "")}" />
  </div>
  <p class="prompt">${escapeHtml(item.prompt || "")}</p>
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
  .toolbar { display: flex; gap: 10px; flex-wrap: wrap; align-items: center; margin-bottom: 16px; padding: 12px; background: #1a1e26; border-radius: 10px; border: 1px solid #2b3240; }
  button { background: #3b82f6; color: #fff; border: 0; border-radius: 6px; padding: 7px 12px; cursor: pointer; font-size: 13px; }
  button.secondary { background: #334155; }
  button:hover { opacity: 0.92; }
  .meta { color: #9aa4b2; font-size: 13px; margin-bottom: 14px; }
  .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(340px, 1fr)); gap: 16px; }
  .card { background: #1a1e26; border: 2px solid #2b3240; border-radius: 10px; overflow: hidden; padding: 12px; }
  .card.ok { border-color: #2e8b57; }
  .card.bad { border-color: #d64545; }
  .card header { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; margin-bottom: 8px; }
  .badge { font-size: 11px; padding: 2px 7px; border-radius: 999px; background: #293142; color: #d8dee9; }
  .card.ok .status { background: #1f5c3a; }
  .card.bad .status { background: #7f2323; }
  .frame-wrap { position: relative; }
  img { width: 100%; height: auto; display: block; border-radius: 6px; background: #000; }
  .safe-zone { position: absolute; top: 14%; bottom: 20%; left: 6%; right: 16%; border: 2px dashed rgba(239, 68, 68, 0.85); pointer-events: none; border-radius: 4px; }
  body.hide-safe .safe-zone { display: none; }
  .qa-controls { display: flex; gap: 10px; align-items: center; margin-top: 8px; font-size: 12px; }
  .qa-note { flex: 1; background: #0f131a; border: 1px solid #334155; color: #e2e8f0; border-radius: 5px; padding: 4px 8px; font-size: 12px; }
  .prompt { font-size: 12px; color: #b8c2d1; margin: 8px 0 0; line-height: 1.45; }
  .missing { padding: 48px 12px; text-align: center; background: #261a1a; color: #f28b82; border-radius: 6px; }
  #exportBox { width: 100%; min-height: 72px; margin-top: 10px; background: #0b0e14; color: #93c5fd; border: 1px solid #334155; border-radius: 6px; padding: 8px; font-family: monospace; font-size: 12px; display: none; }
</style>
</head>
<body>
  <h1>Flow 0 點數靜圖 QA — ${escapeHtml(slug)} (${escapeHtml(series)})</h1>
  <div class="meta">共 ${items.length} 張 · 勾選各鏡通過／退回後，點下方按鈕複製 JSON 貼回給 Claude / Codex / Antigravity 執行 <code>flow_approve_stills</code>。</div>
  <div class="toolbar">
    <button type="button" onclick="markAllApproved()">全部標記通過</button>
    <button type="button" onclick="copyApprovePayload()">複製 flow_approve_stills JSON</button>
    ${safeZoneOverlay ? `<button type="button" class="secondary" onclick="document.body.classList.toggle('hide-safe')">開關 9:16 安全區紅框</button>` : ""}
    <span id="copyMsg" style="font-size:12px;color:#86efac;"></span>
  </div>
  <textarea id="exportBox" readonly></textarea>
  <section class="grid">
${cards}
  </section>
<script>
const SLUG = ${JSON.stringify(slug)};
const SERIES = ${JSON.stringify(series)};
function markAllApproved() {
  document.querySelectorAll('.card').forEach(card => {
    const r = card.querySelector('input[value="approved"]');
    if (r) r.checked = true;
  });
}
function buildPayload() {
  const approved = [];
  const rejected = [];
  document.querySelectorAll('.card').forEach(card => {
    const shotId = card.dataset.shot;
    const sel = card.querySelector('input[type="radio"]:checked');
    const note = (card.querySelector('.qa-note')?.value || '').trim();
    if (!sel) return;
    if (sel.value === 'approved') approved.push(note ? { shotId, note } : shotId);
    if (sel.value === 'rejected') rejected.push(note ? { shotId, note } : { shotId, note: 'QA rejected' });
  });
  return { tool: 'flow_approve_stills', arguments: { slug: SLUG, series: SERIES, approved, rejected } };
}
async function copyApprovePayload() {
  const txt = JSON.stringify(buildPayload(), null, 2);
  const box = document.getElementById('exportBox');
  box.style.display = 'block';
  box.value = txt;
  try {
    await navigator.clipboard.writeText(txt);
    document.getElementById('copyMsg').textContent = '已複製到剪貼簿，可直接貼給 Agent！';
  } catch {
    box.select();
    document.getElementById('copyMsg').textContent = '請從上方文字框全選複製。';
  }
}
</script>
</body>
</html>
`;
  fs.writeFileSync(galleryFile, html, "utf8");
  return galleryFile;
}

/**
 * Writes an HTML gallery for upscaled 1080p30 clips, multi-take history,
 * PSNR / hard-cut QC metrics, and optional raw-audio sidecar player.
 */
export function writeClipsQaGallery({ galleryFile, slug, series, clips = [] }) {
  const dir = path.dirname(galleryFile);
  fs.mkdirSync(dir, { recursive: true });

  const cards = clips
    .map((clip) => {
      const relQa4 = toRelativePosix(dir, clip.qa4Path);
      const relMp4 = toRelativePosix(dir, clip.upscaledPath || clip.rawPath);
      const relAudio = toRelativePosix(dir, clip.rawAudioPath);
      const psnrText = clip.qc?.frame0Psnr != null ? `PSNR ${clip.qc.frame0Psnr.toFixed(1)}dB` : null;
      const cutWarning =
        Array.isArray(clip.qc?.hardCutTimes) && clip.qc.hardCutTimes.length > 0
          ? `偵測中途硬切 @ ${clip.qc.hardCutTimes.join(", ")}s（建議剪點 dur=${clip.qc.recommendedTrim?.durSec}s）`
          : null;
      const takesCount = Array.isArray(clip.takes) ? clip.takes.length : 1;

      return `<article class="card ${clip.qc?.psnrOk === false ? "warn" : ""}">
  <header>
    <strong>${escapeHtml(clip.shotId)}</strong>
    <span class="badge">${escapeHtml(clip.model || "omni-1.2-flash")}</span>
    <span class="badge">Take ${escapeHtml(clip.selectedTake ?? takesCount)}/${escapeHtml(takesCount)}</span>
    <span class="badge">${escapeHtml(clip.credits ?? 12)} credits</span>
    ${psnrText ? `<span class="badge">${escapeHtml(psnrText)}</span>` : ""}
  </header>
  ${relQa4 ? `<img src="${escapeHtml(relQa4)}" alt="${escapeHtml(clip.shotId)} 4-frame QA" loading="lazy" />` : ""}
  ${relMp4 ? `<video controls preload="metadata" src="${escapeHtml(relMp4)}"></video>` : ""}
  ${relAudio ? `<div class="audio-row"><span>原聲側錄試聽：</span><audio controls preload="none" src="${escapeHtml(relAudio)}"></audio></div>` : ""}
  ${cutWarning ? `<p class="cut-warn">${escapeHtml(cutWarning)}</p>` : ""}
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
  .card { background: #1a1e26; border: 2px solid #2b3240; border-radius: 10px; padding: 12px; }
  .card.warn { border-color: #d97706; }
  .card header { display: flex; gap: 6px; flex-wrap: wrap; align-items: center; margin-bottom: 8px; }
  .badge { font-size: 11px; padding: 2px 7px; border-radius: 999px; background: #293142; color: #d8dee9; }
  img, video { width: 100%; border-radius: 6px; margin-bottom: 8px; background: #000; display: block; }
  .audio-row { display: flex; align-items: center; gap: 8px; font-size: 12px; color: #93c5fd; margin-bottom: 8px; }
  .audio-row audio { flex: 1; height: 28px; }
  .cut-warn { font-size: 12px; color: #fbbf24; margin: 4px 0 6px; }
  .prompt { font-size: 12px; color: #b8c2d1; margin: 0; line-height: 1.45; }
</style>
</head>
<body>
  <h1>Flow 1080p30 動態鏡頭 QA — ${escapeHtml(slug)} (${escapeHtml(series)})</h1>
  <div class="meta">共 ${clips.length} 支片段（720p 原檔免費下載 → Lanczos 1080p30 / bt709 / tv / -an；歷史 Take 保留於 <code>flow-clips/takes/</code>）。</div>
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
    schemaVersion: 2,
    updatedAt: new Date().toISOString(),
    ...manifest,
  });
  return manifestFile;
}
