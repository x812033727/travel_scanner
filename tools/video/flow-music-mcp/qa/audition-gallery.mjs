/**
 * Generates a zero-dependency interactive HTML audition & sign-off gallery
 * (`qa-gallery.html`) for Flow Music collections (`bed` / `cue` / `sfx` / cuts).
 *
 * The owner double-clicks `qa-gallery.html` in any browser to listen to every
 * track, inspect LUFS / True Peak / silence warnings, enter reject reasons
 * (e.g. "有人聲", "有爆點", "搶旁白"), and click one button to copy the exact
 * `music_approve` JSON payload.
 */

import fs from "node:fs";
import path from "node:path";

function escapeHtml(str) {
  return String(str ?? "")
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;");
}

function toRelativeSrc(galleryFile, targetPath) {
  if (!targetPath) return "";
  const rel = path.relative(path.dirname(galleryFile), targetPath).replace(/\\/g, "/");
  return rel.startsWith(".") ? rel : `./${rel}`;
}

export function writeMusicQaGallery({
  galleryFile,
  collection,
  series = "curio",
  files = [],
} = {}) {
  fs.mkdirSync(path.dirname(galleryFile), { recursive: true });

  const cards = files
    .map((entry) => {
      const id = entry.file || entry.cue || "unknown";
      const kind = entry.kind || "bed";
      const status = entry.qa_status || "pending";
      const src = toRelativeSrc(galleryFile, entry.filePath || path.join(path.dirname(galleryFile), entry.file || ""));
      const lufs = entry.lufs_i != null ? `${entry.lufs_i} LUFS` : "unmeasured";
      const peak = entry.peak_dbtp != null ? `${entry.peak_dbtp} dBTP` : "—";
      const dur = entry.seconds != null ? `${Number(entry.seconds).toFixed(1)}s` : "—";
      const nearSilent = entry.lufs_i != null && entry.lufs_i < -38;
      const clipping = entry.peak_dbtp != null && entry.peak_dbtp > 0;
      const slices = Array.isArray(entry.slices) ? entry.slices : [];
      const sliceSummary =
        slices.length > 0
          ? `<div class="slices">Detected slices (${slices.length}): ${slices
              .slice(0, 8)
              .map((s) => `${s.startSec}–${s.endSec}s`)
              .join(", ")}${slices.length > 8 ? " …" : ""}</div>`
          : "";

      return `
      <div class="card" data-id="${escapeHtml(id)}" data-kind="${escapeHtml(kind)}" data-status="${escapeHtml(status)}">
        <div class="card-head">
          <span class="badge kind-${escapeHtml(kind)}">${escapeHtml(kind.toUpperCase())}</span>
          <strong class="title">${escapeHtml(id)}</strong>
          <span class="status-pill status-${escapeHtml(status)}">${escapeHtml(status)}</span>
        </div>
        <div class="metrics">
          <span>⏱ ${escapeHtml(dur)}</span>
          <span class="${nearSilent ? "warn" : ""}">🔊 ${escapeHtml(lufs)}${nearSilent ? " ⚠ 近靜音" : ""}</span>
          <span class="${clipping ? "warn" : ""}">📈 ${escapeHtml(peak)}${clipping ? " ⚠ 削波" : ""}</span>
          <span>🔇 靜音段: ${escapeHtml(entry.silences ?? "—")}</span>
        </div>
        <audio controls preload="none" src="${escapeHtml(src)}"></audio>
        ${sliceSummary}
        <div class="prompt">${escapeHtml(entry.sound_prompt || entry.prompt || "")}</div>
        <div class="controls">
          <label><input type="radio" name="qa_${escapeHtml(id)}" value="approved" ${status === "approved" ? "checked" : ""}> ✅ 可用</label>
          <label><input type="radio" name="qa_${escapeHtml(id)}" value="rejected" ${status === "rejected" ? "checked" : ""}> ❌ 不用</label>
          <label><input type="radio" name="qa_${escapeHtml(id)}" value="pending" ${status === "pending" ? "checked" : ""}> ⏳ 待聽</label>
          <input type="text" class="reason" placeholder="備註／退件理由（例如：有人聲、有爆點、搶旁白、剪 2.1–8.5s）" value="${escapeHtml(entry.qa_reason || "")}">
        </div>
      </div>`;
    })
    .join("\n");

  const html = `<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8" />
  <title>Flow Music 試聽簽核 — ${escapeHtml(collection)}</title>
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: #111318; color: #e8ecf1; margin: 0; padding: 20px; }
    header { position: sticky; top: 0; z-index: 10; background: #191d26; border: 1px solid #2b3240; border-radius: 10px; padding: 14px 18px; margin-bottom: 18px; display: flex; flex-wrap: wrap; align-items: center; gap: 12px; justify-content: space-between; }
    h1 { margin: 0; font-size: 18px; }
    .toolbar { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
    button { background: #2d6cdf; color: #fff; border: 0; border-radius: 6px; padding: 8px 14px; font-weight: 600; cursor: pointer; }
    button.secondary { background: #2a3140; color: #d5dce6; }
    button:hover { filter: brightness(1.1); }
    .grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(420px, 1fr)); gap: 14px; }
    .card { background: #181c24; border: 1px solid #2a3140; border-radius: 10px; padding: 14px; display: flex; flex-direction: column; gap: 8px; }
    .card-head { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
    .title { font-size: 14px; word-break: break-all; }
    .badge { font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 99px; }
    .kind-bed { background: #1e3a5f; color: #90caf9; }
    .kind-cue { background: #4a2c5a; color: #e1bee7; }
    .kind-sfx { background: #5a3a1e; color: #ffcc80; }
    .status-pill { margin-left: auto; font-size: 11px; padding: 2px 8px; border-radius: 99px; background: #2a3140; }
    .status-approved { background: #1b4d32; color: #81c784; }
    .status-rejected { background: #5c1e24; color: #ef9a9a; }
    .metrics { display: flex; flex-wrap: wrap; gap: 10px; font-size: 12px; color: #a7b3c4; }
    .metrics .warn { color: #ffab40; font-weight: 700; }
    audio { width: 100%; height: 34px; }
    .slices { font-size: 12px; color: #80cbc4; }
    .prompt { font-size: 12px; color: #8c98a8; line-height: 1.4; max-height: 60px; overflow: auto; }
    .controls { display: flex; flex-wrap: wrap; gap: 10px; align-items: center; font-size: 13px; border-top: 1px solid #252c38; padding-top: 8px; }
    .reason { flex: 1 1 220px; background: #101319; color: #e8ecf1; border: 1px solid #313949; border-radius: 6px; padding: 5px 8px; font-size: 12px; }
    .hidden { display: none !important; }
    #copyToast { font-size: 12px; color: #81c784; }
  </style>
</head>
<body>
  <header>
    <div>
      <h1>Flow Music 試聽簽核 — ${escapeHtml(collection)} (${escapeHtml(series)})</h1>
      <div style="font-size:12px;color:#9aa7b8;margin-top:4px;">共 ${files.length} 首・AI 生成音樂（Lyria 3.5）・審核完點右側按鈕複製 JSON 貼回 <code>music_approve</code></div>
    </div>
    <div class="toolbar">
      <button class="secondary" onclick="filterKind('all')">全部</button>
      <button class="secondary" onclick="filterKind('bed')">底樂 BED</button>
      <button class="secondary" onclick="filterKind('cue')">短音樂 CUE</button>
      <button class="secondary" onclick="filterKind('sfx')">音效 SFX</button>
      <button onclick="copyApprovePayload()">📋 複製 music_approve JSON</button>
      <span id="copyToast"></span>
    </div>
  </header>
  <div class="grid" id="grid">
${cards}
  </div>
  <script>
    function filterKind(kind) {
      document.querySelectorAll('.card').forEach((card) => {
        card.classList.toggle('hidden', kind !== 'all' && card.dataset.kind !== kind);
      });
    }
    function buildApprovePayload() {
      const approved = [];
      const rejected = [];
      const reasons = {};
      document.querySelectorAll('.card').forEach((card) => {
        const id = card.dataset.id;
        const checked = card.querySelector('input[type="radio"]:checked');
        const reason = (card.querySelector('.reason')?.value || '').trim();
        if (reason) reasons[id] = reason;
        if (checked?.value === 'approved') approved.push(id);
        else if (checked?.value === 'rejected') rejected.push(id);
      });
      return { collection: ${JSON.stringify(collection)}, approved, rejected, reasons };
    }
    async function copyApprovePayload() {
      const text = JSON.stringify(buildApprovePayload(), null, 2);
      try {
        await navigator.clipboard.writeText(text);
        document.getElementById('copyToast').textContent = '已複製！請貼回對話執行 music_approve';
      } catch {
        prompt('複製以下 JSON 貼回 music_approve:', text);
      }
    }
  </script>
</body>
</html>
`;

  fs.writeFileSync(galleryFile, html, "utf8");
  return galleryFile;
}
