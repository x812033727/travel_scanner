// Burned-in subtitles for a drama: one transparent 1920x260 PNG strip per distinct cue text,
// which the assemble stage lays over the clips (docs/videos/DRAMA.md).
//
// The cues are the zh-TW captions' (tools/video/core/captions.mjs): what is burned in and what
// the CC track says are cut and timed alike. The strips are drawn by the same headless browser
// with the bundled font, not by libass: the bundled fonts are woff2, which fontconfig cannot see,
// so libass would quietly fall back to whatever each machine has installed and Windows, CI and
// the worker would draw three different videos. A strip's key is its HTML, so a cue is redrawn
// exactly when its words, its speaker prefix or the style below change.
import { createHash } from "node:crypto";

import { buildCues } from "../core/captions.mjs";
import { characterOf, resolveSubtitles } from "../core/drama.mjs";
import { eachLine, NARRATION_LOCALE } from "../core/schema.mjs";
import { FPS } from "../core/timeline.mjs";
import { escapeHtml, ORIGIN } from "../templates/templates.mjs";

export const STRIP_SIZE = { width: 1920, height: 260 };
export const STRIP_LOCALE = NARRATION_LOCALE;
// Relative to the work directory, with forward slashes, like the slide frames.
export const BLANK_STRIP = "frames/sub-blank.png";
export const stripFile = (key) => `frames/sub-${key}.png`;

const hash = (text) => createHash("sha256").update(text).digest("hex").slice(0, 16);

const BASE_CSS = [
  "* { box-sizing: border-box; }",
  "html, body { margin: 0; padding: 0; background: transparent; }",
  `body { width: ${STRIP_SIZE.width}px; height: ${STRIP_SIZE.height}px; overflow: hidden; font-family: "Noto Sans TC Variable", sans-serif; -webkit-font-smoothing: antialiased; text-rendering: geometricPrecision; line-break: strict; }`,
  // The text sits on the bottom edge of the strip, 56 px up: about 14% of a 1080 p frame, where
  // the reference dramas put theirs and clear of YouTube's own controls when they are not shown.
  ".content { position: absolute; left: 0; right: 0; bottom: 56px; height: 204px; display: flex; justify-content: center; align-items: flex-end; overflow: hidden; }",
  ".strip { max-width: 1700px; text-align: center; white-space: pre-line; }",
].join("");

// Two looks: `drama` is the outlined white text of the reference videos, readable on any frame;
// `plain` is the boxed caption of a talking-head video. The line height is 1.5: Noto Sans TC's
// glyph box is about 1.45 em tall, and a tighter line would overflow the strip by a few pixels,
// which the renderer rightly reports as a layout problem.
export const STRIP_STYLES = {
  drama: [
    ".strip { font-size: 56px; font-weight: 600; line-height: 1.5; letter-spacing: 0.02em; color: #f7f1e8; paint-order: stroke fill; -webkit-text-stroke: 5px #000; text-shadow: 0 2px 8px rgba(0, 0, 0, 0.55); }",
    ".strip .speaker { color: #f0a04b; }",
  ].join(""),
  plain: [
    ".strip { font-size: 48px; font-weight: 500; line-height: 1.5; color: #fff; background: rgba(0, 0, 0, 0.62); padding: 4px 24px; border-radius: 6px; }",
    ".strip .speaker { color: #f0a04b; }",
  ].join(""),
};

function stripPage(body, style) {
  return [
    '<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8">',
    `<link rel="stylesheet" href="${ORIGIN}/fonts/noto-sans-tc/index.css">`,
    `<style>${BASE_CSS}${STRIP_STYLES[style] ?? STRIP_STYLES.drama}</style>`,
    `</head><body>${body}</body></html>`,
  ].join("");
}

/** One cue as a complete page: the text, with the speaker's name before it when asked for. */
export function stripHtml(text, style = "drama", speaker = null) {
  const prefix = speaker ? `<span class="speaker">【${escapeHtml(speaker)}】</span>` : "";
  return stripPage(`<main class="content"><div class="strip">${prefix}${escapeHtml(text)}</div></main>`, style);
}

/** The strip shown while nobody speaks: nothing at all, on a transparent ground. */
export const blankStripHtml = () => stripPage("", "drama");
// The renderer serves a page under a hex key; the blank strip's is its HTML's hash like the others'.
export const blankStripKey = () => hash(blankStripHtml());

/** The speaker's name for a character's line, or null for the narrator. */
function speakerName(doc, line) {
  return characterOf(doc, line)?.name ?? null;
}

const clamp = (value, low, high) => Math.min(high, Math.max(low, value));

/**
 * Every strip to draw and every cue to show, from the narration's timeline.
 * Returns { style, strips: [{ key, html, text }], cues: [{ line, key, start_frame, end_frame, text }] }.
 * A strip is shared by every cue with the same words, so a repeated line costs one drawing; the
 * speaker prefix goes on a character's first cue only, as the reference dramas do.
 */
export function subtitlePlan(doc, timeline) {
  const settings = resolveSubtitles(doc);
  const texts = {};
  const speakers = {};
  for (const { line } of eachLine(doc)) {
    texts[line.id] = line.text;
    speakers[line.id] = speakerName(doc, line);
  }
  const { cues, missing } = buildCues(timeline, texts, STRIP_LOCALE);
  if (missing.length) throw new Error(`no subtitle text for lines ${missing.join(", ")}`);
  const placed = new Map(timeline.lines.map((line) => [line.id, line]));
  const strips = new Map();
  const shown = [];
  let previousLine = null;
  for (const cue of cues) {
    const line = placed.get(cue.line);
    const first = cue.line !== previousLine;
    previousLine = cue.line;
    const speaker = settings.speaker_prefix && first ? speakers[cue.line] : null;
    const html = stripHtml(cue.text, settings.style, speaker);
    const key = hash(html);
    const text = `${speaker ? `【${speaker}】` : ""}${cue.text}`;
    if (!strips.has(key)) strips.set(key, { key, html, text });
    // Cues are timed in milliseconds off the frame grid; the overlay works in whole frames.
    const startFrame = clamp(Math.round((cue.start_ms * FPS) / 1000), line.start_frame, line.end_frame - 1);
    const endFrame = clamp(Math.round((cue.end_ms * FPS) / 1000), startFrame + 1, line.end_frame);
    shown.push({ line: cue.line, key, start_frame: startFrame, end_frame: endFrame, text });
  }
  return { style: settings.style, strips: [...strips.values()], cues: shown };
}
