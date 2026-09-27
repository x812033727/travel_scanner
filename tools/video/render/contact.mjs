// The contact sheet: every distinct slide state on one image, so a person or a multimodal agent can
// look over the whole video's pictures before anything is assembled.
import { escapeHtml, ORIGIN } from "../templates/templates.mjs";

export const SHEET_WIDTH = 1920;
const COLUMNS = 4;

/** HTML for the sheet; frame paths are relative to the work directory, served under /work/. */
export function contactSheetHtml(title, tiles) {
  const cells = tiles
    .map((tile) => `<figure><img src="${ORIGIN}/work/${tile.file}" alt=""><figcaption>${escapeHtml(tile.label)}</figcaption></figure>`)
    .join("");
  return [
    '<!doctype html><html><head><meta charset="utf-8">',
    `<link rel="stylesheet" href="${ORIGIN}/fonts/noto-sans-tc/index.css">`,
    "<style>",
    "body{margin:0;padding:40px;background:#081819;color:#f7f1e8;font-family:'Noto Sans TC Variable',sans-serif;width:1840px}",
    "h1{margin:0 0 28px;font-size:36px}",
    `.grid{display:grid;grid-template-columns:repeat(${COLUMNS},1fr);gap:24px}`,
    "figure{margin:0}img{width:100%;display:block;border-radius:8px;border:1px solid rgba(247,241,232,.2)}",
    "figcaption{margin-top:8px;font-size:20px;color:#a8bcb8}",
    "</style></head><body>",
    `<h1>${escapeHtml(title)}</h1><div class="grid">${cells}</div>`,
    "</body></html>",
  ].join("");
}
