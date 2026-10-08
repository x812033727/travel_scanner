// Slide templates: scene data in, HTML out, as pure functions so they are tested without a browser.
//
// A scene's `lines[].reveal` counts apply to the last N elements of its template: a bullets slide
// with three items and three reveals starts empty and gains one item per reveal; with no reveals
// every item is there from the start. Elements that appear in a state get the `enter` class, and
// the renderer freezes that entrance animation frame by frame (tools/video/render/browser.mjs).
import { LOCALE_FONTS, SLIDE_FAMILY } from "../render/fonts.mjs";
import { TERMINAL_CSS, TERMINAL_SPEC, terminalBody } from "./terminal/terminal.mjs";

export const ORIGIN = "https://video.local";
export const SIZE = { width: 1920, height: 1080 };
export const THUMB_SIZE = { width: 1280, height: 720 };
export const BRAND = "MOKAAIR";
export const SITE_LABEL = "mokaair.com";

const isText = (value) => typeof value === "string" && value.trim().length > 0;
const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const isTextList = (value, min, max) => Array.isArray(value) && value.length >= min && value.length <= max && value.every(isText);
const isPercent = (value) => typeof value === "number" && value >= 0 && value <= 100;
const visibleLength = (value) => [...value.replace(/\*\*/g, "")].length;

export function escapeHtml(text) {
  return String(text).replace(/[&<>"']/g, (char) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[char]);
}

/**
 * Escaped text where **this** becomes the accent colour, the one emphasis a slide may use, and a
 * newline is a line break the writer chose.
 */
export function richText(text) {
  return escapeHtml(text).replace(/\*\*(.+?)\*\*/g, "<em>$1</em>").replace(/\n/g, "<br>");
}

/** Where a slide may load an image from: files in the repository, by repository path. */
export const assetUrl = (repoPath) => `${ORIGIN}/repo/${repoPath.split("/").map(encodeURIComponent).join("/")}`;
export const ASSET_ROOTS = ["apps/web/public/", "docs/videos/"];
const isAssetPath = (value, extensions) =>
  isText(value) && ASSET_ROOTS.some((root) => value.startsWith(root)) && !value.includes("..") && extensions.test(value);
/**
 * The other place a screenshot slide may load its picture from: a stock photo `stock fetch`
 * (tools/video/media/stock.mjs) put in the work directory as stock/<sha256>.<ext>, named by its
 * bytes, with its credit in video.json's assets[] (docs/videos/ILLUSTRATED.md §圖庫照片). The
 * renderer's fake origin serves the work directory under /work/, as it does the keyframes.
 */
export const STOCK_PATH = /^stock\/[0-9a-f]{64}\.(?:png|jpg|webp)$/;
export const isStockPath = (value) => typeof value === "string" && STOCK_PATH.test(value);
export const workUrl = (file) => `${ORIGIN}/work/${file.split("/").map(encodeURIComponent).join("/")}`;
// A credit drawn on the slide is a short line in the picture's corner; the description carries it in full.
export const CREDIT_MAX_CHARS = 60;

// Per template: which data it needs, and how many elements lines may reveal.
export const TEMPLATE_SPECS = {
  title: {
    check: (data) => [!isText(data.title) && "title is required", data.subtitle !== undefined && !isText(data.subtitle) && "subtitle must be text", data.tag !== undefined && !isText(data.tag) && "tag must be text"],
    capacity: () => 0,
  },
  chapter: {
    check: (data) => [!isText(data.title) && "title is required", data.number !== undefined && !/^\d{1,2}$/.test(String(data.number)) && "number must be one or two digits"],
    capacity: () => 0,
  },
  bullets: {
    check: (data) => [data.title !== undefined && !isText(data.title) && "title must be text", !isTextList(data.items, 1, 6) && "items must be 1 to 6 strings"],
    capacity: (data) => data.items.length,
  },
  compare: {
    check: (data) => {
      const side = (value) => value && isText(value.heading) && isTextList(value.points, 1, 5);
      return [data.title !== undefined && !isText(data.title) && "title must be text", !side(data.left) && "left needs heading and 1 to 5 points", !side(data.right) && "right needs heading and 1 to 5 points"];
    },
    capacity: () => 2,
  },
  steps: {
    check: (data) => [
      data.title !== undefined && !isText(data.title) && "title must be text",
      !(Array.isArray(data.steps) && data.steps.length >= 2 && data.steps.length <= 5 && data.steps.every((step) => step && isText(step.title) && (step.detail === undefined || isText(step.detail)))) &&
        "steps must be 2 to 5 of { title, detail? }",
    ],
    capacity: (data) => data.steps.length,
  },
  table: {
    check: (data) => {
      const columns = isTextList(data.columns, 2, 5);
      const rows = Array.isArray(data.rows) && data.rows.length >= 1 && data.rows.length <= 8 && data.rows.every((row) => Array.isArray(row) && columns && row.length === data.columns.length && row.every((cell) => typeof cell === "string"));
      return [
        data.title !== undefined && !isText(data.title) && "title must be text",
        !columns && "columns must be 2 to 5 strings",
        !rows && "rows must be 1 to 8 arrays as long as columns",
        data.highlight !== undefined && !(Number.isInteger(data.highlight) && rows && data.highlight >= 0 && data.highlight < data.rows.length) && "highlight must be a row index",
      ];
    },
    capacity: (data) => data.rows.length,
  },
  code: {
    check: (data) => {
      const lines = typeof data.code === "string" ? data.code.replace(/\n$/, "").split("\n") : [];
      return [
        !isText(data.code) && "code is required",
        lines.length > 16 && `code has ${lines.length} lines; at most 16 fit`,
        lines.some((line) => line.length > 64) && "a code line is longer than 64 characters",
        data.highlight !== undefined && !(Array.isArray(data.highlight) && data.highlight.every((n) => Number.isInteger(n) && n >= 1 && n <= lines.length)) && "highlight must list line numbers",
        data.caption !== undefined && !isText(data.caption) && "caption must be text",
      ];
    },
    capacity: () => 0,
  },
  big: {
    check: (data) => [!isText(data.text) && "text is required", data.kicker !== undefined && !isText(data.kicker) && "kicker must be text", data.sub !== undefined && !isText(data.sub) && "sub must be text"],
    capacity: () => 0,
  },
  diagram: {
    check: (data) => [!isAssetPath(data.svg, /\.svg$/) && `svg must be a repository path under ${ASSET_ROOTS.join(" or ")}`, data.caption !== undefined && !isText(data.caption) && "caption must be text"],
    capacity: () => 0,
  },
  screenshot: {
    check: (data) => [
      !(isAssetPath(data.image, /\.(png|jpe?g|webp)$/i) || isStockPath(data.image)) &&
        `image must be a repository path under ${ASSET_ROOTS.join(" or ")}, or a stock photo fetched into the work directory (stock/<sha256>.png|jpg|webp)`,
      data.highlight !== undefined && !(data.highlight && ["x", "y", "w", "h"].every((key) => isPercent(data.highlight[key]))) && "highlight must be { x, y, w, h } in percent",
      data.caption !== undefined && !isText(data.caption) && "caption must be text",
      // Optional, and the description credits the picture whether or not the slide does (the
      // owner burns no text in by default): one short line in the picture's corner.
      data.credit !== undefined && !(isText(data.credit) && !data.credit.includes("\n") && visibleLength(data.credit) <= CREDIT_MAX_CHARS) &&
        `credit must be one line of text (at most ${CREDIT_MAX_CHARS} characters)`,
    ],
    capacity: (data) => (data.highlight ? 1 : 0),
  },
  // The next four came from a reference video (2026-09-26): concrete little artefacts instead of
  // one slide of text left up for half a minute.
  chat: {
    check: (data) => {
      const messages = data.messages;
      const valid = Array.isArray(messages) && messages.length >= 1 && messages.length <= 3 &&
        messages.every((message) => message && ["left", "right"].includes(message.side) && isText(message.text) && (message.name === undefined || isText(message.name)));
      // Hidden bubbles retain their height. Two named, two-line bubbles or three unnamed ones
      // fit below a one-line heading at 1080p; a fourth named bubble does not.
      return [
        data.title !== undefined && !isText(data.title) && "title must be text",
        isText(data.title) && (visibleLength(data.title) > 20 || data.title.includes("\n")) && "chat title must fit on one line (at most 20 characters)",
        !valid && "messages must be 1 to 3 of { side: left|right, name?, text }",
        valid && messages.length > 2 && messages.some((message) => message.name !== undefined) && "named chat messages are limited to 2",
        valid && messages.some((message) => visibleLength(message.text) > 44 || message.text.includes("\n")) && "chat message text must fit in two lines (at most 44 characters)",
        valid && messages.some((message) => message.name !== undefined && (visibleLength(message.name) > 10 || message.name.includes("\n"))) && "chat message names must fit on one line (at most 10 characters)",
      ];
    },
    capacity: (data) => data.messages.length,
  },
  quote: {
    check: (data) => [
      !isText(data.quote) && "quote is required",
      !isText(data.source) && "source is required: where the words come from",
      data.kicker !== undefined && !isText(data.kicker) && "kicker must be text",
      data.translation !== undefined && !isText(data.translation) && "translation must be text",
    ],
    capacity: (data) => (data.translation ? 1 : 0),
  },
  stats: {
    check: (data) => [
      data.title !== undefined && !isText(data.title) && "title must be text",
      !(Array.isArray(data.stats) && data.stats.length >= 1 && data.stats.length <= 4 &&
        data.stats.every((stat) => stat && isText(stat.value) && isText(stat.label) && (stat.note === undefined || isText(stat.note)))) &&
        "stats must be 1 to 4 of { value, label, note? }",
      data.source !== undefined && !isText(data.source) && "source must be text",
    ],
    capacity: (data) => data.stats.length,
  },
  // A command and what it printed, from a real run with its date and version (terminal/terminal.mjs).
  terminal: TERMINAL_SPEC,
  cta: {
    check: (data) => [!isText(data.title) && "title is required", data.kicker !== undefined && !isText(data.kicker) && "kicker must be text", data.sub !== undefined && !isText(data.sub) && "sub must be text"],
    capacity: () => 0,
  },
  outro: {
    check: (data) => [!isText(data.title) && "title is required", data.cta !== undefined && !isText(data.cta) && "cta must be text", data.lines !== undefined && !isTextList(data.lines, 1, 4) && "lines must be 1 to 4 strings"],
    capacity: () => 0,
  },
};

/**
 * An SVG file's markup made fit to inline: prolog and doctype dropped, the root's fixed size
 * removed so the slide sizes it. Article diagrams already pass check_svg; this is for anything else.
 */
export function inlineSvg(markup) {
  return String(markup)
    .replace(/^﻿/, "")
    .replace(/<\?xml[\s\S]*?\?>/, "")
    .replace(/<!DOCTYPE[\s\S]*?>/i, "")
    .replace(/<svg\b([^>]*)>/, (_, attributes) => `<svg${attributes.replace(/\s(width|height)="[^"]*"/g, "")}>`)
    .trim();
}

export function svgProblems(markup) {
  const text = String(markup);
  const problems = [];
  if (!/<svg\b/.test(text)) problems.push("the file is not an SVG");
  if (/<script\b|<foreignObject\b|\son[a-z]+\s*=|javascript:/i.test(text)) problems.push("the SVG contains script, an event handler or foreignObject");
  if (/(?:href|src)\s*=\s*["']https?:|url\(\s*["']?https?:|@import/i.test(text)) problems.push("the SVG loads something from the network");
  return problems;
}

/** Everything wrong with a scene's data for its template, reveals included. */
export function sceneProblems(scene) {
  const spec = TEMPLATE_SPECS[scene.template];
  if (!spec) return [`unknown template ${scene.template}`];
  const problems = spec.check(scene.data ?? {}).filter(Boolean);
  if (problems.length) return problems;
  const reveals = scene.lines.reduce((sum, line) => sum + (line.reveal ?? 0), 0);
  const capacity = spec.capacity(scene.data);
  if (reveals > capacity) problems.push(`reveals ${reveals} elements but the ${scene.template} slide has ${capacity}`);
  return problems;
}

/** Which of `count` elements are shown, and which of those enter now, at a given reveal state. */
export function visibility(count, totalReveals, reveal, previousReveal, first) {
  const shown = count - totalReveals + reveal;
  const before = first ? 0 : count - totalReveals + previousReveal;
  // order staggers elements entering together; one that enters alone starts at once.
  return (index) => ({ shown: index < shown, entering: index < shown && index >= before, order: Math.max(0, index - before) });
}

function attrs({ shown, entering, order }, className = "", style = "") {
  const classes = [className, entering ? "enter" : ""].filter(Boolean).join(" ");
  return `${classes ? ` class="${classes}"` : ""}${shown ? "" : " data-hidden"} style="--i:${order}${style ? `;${style}` : ""}"`;
}

function enterClass(first, extra = "", index = 0) {
  return `class="${[extra, first ? "enter" : ""].filter(Boolean).join(" ")}" style="--i:${index}"`;
}

const heading = (data, first) => (data.title ? `<h2 ${enterClass(first, "heading fit")}>${richText(data.title)}</h2>` : "");
const pad = (number) => String(number).padStart(2, "0");
const knowsChapters = (state) => (state.chapterCount ?? 0) >= 2 && (state.chapterNumber ?? 0) >= 1;

// A stock photo's credit, in the picture's corner over the highlight's scrim: a dark pill with
// one short line, cut with an ellipsis rather than wrapped should the lint cap ever be passed.
const CREDIT_CSS =
  ".t-screenshot .credit{position:absolute;right:16px;bottom:14px;max-width:80%;padding:6px 16px;border-radius:999px;" +
  "background:rgba(8,24,25,.62);color:rgba(255,255,255,.88);font-size:22px;line-height:1.3;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}";

// CSS a template carries in its own page instead of the theme, so that adding the template moved
// no other video's frame keys. A function takes the scene's data: a screenshot slide carries the
// credit CSS only when it draws a credit, so every other screenshot page is byte for byte what it was.
const TEMPLATE_CSS = { terminal: TERMINAL_CSS, screenshot: (data) => (data.credit ? CREDIT_CSS : "") };
const templateCss = (scene) => {
  const own = TEMPLATE_CSS[scene.template];
  return typeof own === "function" ? own(scene.data ?? {}) : own ?? "";
};

const RENDERERS = {
  title(data, state) {
    const parts = [];
    if (data.tag) parts.push(`<div ${enterClass(state.first, "tag", 0)}>${richText(data.tag)}</div>`);
    parts.push(`<h1 ${enterClass(state.first, "fit", 1)}>${richText(data.title)}</h1>`);
    parts.push(`<div ${enterClass(state.first, "rule", 2)}></div>`);
    if (data.subtitle) parts.push(`<div ${enterClass(state.first, "subtitle fit", 3)}>${richText(data.subtitle)}</div>`);
    return parts.join("");
  },
  chapter(data, state) {
    const number = data.number ?? state.chapterNumber;
    const of = number && knowsChapters(state) ? `<span class="of">/ ${pad(state.chapterCount)}</span>` : "";
    return [
      number ? `<div ${enterClass(state.first, "number", 0)}>${escapeHtml(pad(number))}${of}</div>` : "",
      `<h2 ${enterClass(state.first, "fit", 1)}>${richText(data.title)}</h2>`,
      data.subtitle ? `<div ${enterClass(state.first, "subtitle fit", 2)}>${richText(data.subtitle)}</div>` : "",
    ].join("");
  },
  bullets(data, state) {
    const show = state.visible(data.items.length);
    const items = data.items.map((item, index) => `<li${attrs(show(index))}><span class="n">${index + 1}</span><span class="fit">${richText(item)}</span></li>`);
    return `${heading(data, state.first)}<ol>${items.join("")}</ol>${data.note ? `<div class="note">${richText(data.note)}</div>` : ""}`;
  },
  compare(data, state) {
    const show = state.visible(2);
    const card = (side, index, name) =>
      `<div${attrs(show(index), `card ${name}`)}><h3>${richText(side.heading)}</h3><ul>${side.points.map((point) => `<li>${richText(point)}</li>`).join("")}</ul></div>`;
    return `${heading(data, state.first)}<div class="cards">${card(data.left, 0, "left")}${card(data.right, 1, "right")}</div>${data.verdict ? `<div class="verdict">${richText(data.verdict)}</div>` : ""}`;
  },
  steps(data, state) {
    const show = state.visible(data.steps.length);
    const parts = data.steps.map((step, index) => {
      const card = `<div${attrs(show(index), "step")}><div class="num">STEP ${index + 1}</div><h3>${richText(step.title)}</h3>${step.detail ? `<p>${richText(step.detail)}</p>` : ""}</div>`;
      const arrow = index ? `<div${attrs(show(index), "arrow")}>→</div>` : "";
      return arrow + card;
    });
    return `${heading(data, state.first)}<div class="flow">${parts.join("")}</div>`;
  },
  table(data, state) {
    const show = state.visible(data.rows.length);
    const head = `<tr>${data.columns.map((column) => `<th>${richText(column)}</th>`).join("")}</tr>`;
    const rows = data.rows.map((row, index) => `<tr${attrs(show(index), index === data.highlight ? "hot" : "")}>${row.map((cell) => `<td>${richText(cell)}</td>`).join("")}</tr>`);
    return `${heading(data, state.first)}<table><thead>${head}</thead><tbody>${rows.join("")}</tbody></table>`;
  },
  code(data, state) {
    const hot = new Set(data.highlight ?? []);
    const lines = data.code.replace(/\n$/, "").split("\n").map((line, index) => `<span class="ln${hot.has(index + 1) ? " hot" : ""}" data-n="${index + 1}">${escapeHtml(line) || " "}</span>`);
    const label = data.language ? `<div class="label">${escapeHtml(data.language)}</div>` : "";
    return `${heading(data, state.first)}<div ${enterClass(state.first, "panel", 1)}>${label}<pre>${lines.join("")}</pre></div>${data.caption ? `<div class="caption">${richText(data.caption)}</div>` : ""}`;
  },
  big(data, state) {
    return [
      data.kicker ? `<div ${enterClass(state.first, "kicker", 0)}>${richText(data.kicker)}</div>` : "",
      `<div ${enterClass(state.first, "word fit", 1)}>${richText(data.text)}</div>`,
      data.sub ? `<div ${enterClass(state.first, "sub fit", 2)}>${richText(data.sub)}</div>` : "",
    ].join("");
  },
  diagram(data, state) {
    // Inline, so the SVG's text is set in the bundled font like the rest of the slide; an <img>
    // would use whatever fonts the machine has, and CI has none for Chinese.
    const art = state.svg ? inlineSvg(state.svg) : `<img src="${assetUrl(data.svg)}" alt="">`;
    return `${heading(data, state.first)}<div class="frame"><div ${enterClass(state.first, "paper", 1)}>${art}</div></div>${data.caption ? `<div class="caption-line">${richText(data.caption)}</div>` : ""}`;
  },
  screenshot(data, state) {
    const box = data.highlight
      ? `<div${attrs(state.visible(1)(0), "box mark", `left:${data.highlight.x}%;top:${data.highlight.y}%;width:${data.highlight.w}%;height:${data.highlight.h}%`)}></div>`
      : "";
    // A stock photo is served from the work directory; a repository picture from the repository.
    const src = isStockPath(data.image) ? workUrl(data.image) : assetUrl(data.image);
    const credit = data.credit ? `<div class="credit">${richText(data.credit)}</div>` : "";
    return `${heading(data, state.first)}<div class="frame"><div ${enterClass(state.first, "shot", 1)}><img src="${src}" alt="">${box}${credit}</div></div>${data.caption ? `<div class="caption-line">${richText(data.caption)}</div>` : ""}`;
  },
  chat(data, state) {
    const show = state.visible(data.messages.length);
    const messages = data.messages.map(
      (message, index) => `<div${attrs(show(index), `msg ${message.side}`)}>${message.name ? `<div class="who">${richText(message.name)}</div>` : ""}<div class="bubble fit">${richText(message.text)}</div></div>`,
    );
    return `${heading(data, state.first)}<div class="thread">${messages.join("")}</div>`;
  },
  quote(data, state) {
    // A reveal brings in the translation after the original words have been heard.
    const translation = data.translation ? `<div${attrs(state.visible(1)(0), "translation fit")}>${richText(data.translation)}</div>` : "";
    return [
      data.kicker ? `<div ${enterClass(state.first, "kicker", 0)}>${richText(data.kicker)}</div>` : "",
      `<blockquote ${enterClass(state.first, "fit", 1)}>${richText(data.quote)}</blockquote>`,
      translation,
      `<div ${enterClass(state.first, "source", 2)}>${richText(data.source)}</div>`,
    ].join("");
  },
  stats(data, state) {
    const show = state.visible(data.stats.length);
    const cards = data.stats.map(
      (stat, index) => `<div${attrs(show(index), "stat")}><div class="value fit">${richText(stat.value)}</div><div class="label">${richText(stat.label)}</div>${stat.note ? `<div class="note">${richText(stat.note)}</div>` : ""}</div>`,
    );
    return `${heading(data, state.first)}<div class="grid" style="--n:${data.stats.length}">${cards.join("")}</div>${data.source ? `<div class="caption-line">${richText(data.source)}</div>` : ""}`;
  },
  terminal(data, state) {
    return terminalBody(data, state, heading(data, state.first));
  },
  cta(data, state) {
    return `<div ${enterClass(state.first, "cta-card", 0)}>${data.kicker ? `<div class="kicker">${richText(data.kicker)}</div>` : ""}<h2 class="fit">${richText(data.title)}</h2>${data.sub ? `<div class="sub fit">${richText(data.sub)}</div>` : ""}<div class="site">${SITE_LABEL}</div></div>`;
  },
  outro(data, state) {
    return [
      `<h2 ${enterClass(state.first, "fit", 0)}>${richText(data.title)}</h2>`,
      data.cta ? `<div ${enterClass(state.first, "cta fit", 1)}>${richText(data.cta)}</div>` : "",
      data.lines ? `<ul ${enterClass(state.first, "", 2)}>${data.lines.map((line) => `<li>${richText(line)}</li>`).join("")}</ul>` : "",
      `<div ${enterClass(state.first, "site", 3)}>${SITE_LABEL}</div>`,
    ].join("");
  },
};

// Exported for the screencast template (tools/video/screencast/scene.mjs), which draws its own body.
// `locale` is a caption locale's thumbnail set in a font of its own (fonts.mjs LOCALE_FONTS): that
// font is loaded and put first, before the slide font. Every other page is byte for byte what it
// was, so no frame key of an existing video moves.
export function page(body, size, extraCss = "", { locale = null } = {}) {
  const own = LOCALE_FONTS[locale] ?? null;
  return [
    "<!doctype html>",
    `<html lang="${own ? own.lang : "zh-Hant"}"><head><meta charset="utf-8">`,
    own ? `<link rel="stylesheet" href="${ORIGIN}/fonts/${own.font}/index.css">` : "",
    `<link rel="stylesheet" href="${ORIGIN}/fonts/noto-sans-tc/index.css">`,
    `<link rel="stylesheet" href="${ORIGIN}/fonts/jetbrains-mono/index.css">`,
    `<link rel="stylesheet" href="${ORIGIN}/theme.css">`,
    `<style>:root{--width:${size.width}px;--height:${size.height}px${own ? `;--font:"${own.family}","${SLIDE_FAMILY}",sans-serif` : ""}}${extraCss}</style>`,
    `</head><body>${body}</body></html>`,
  ].join("");
}

/**
 * Where the viewer is: a bar across the top with one segment per chapter, the ones seen and the
 * current one marked, and "02 / 06 chapter" in the corner. The owner asked for both after a
 * reference video on 2026-09-26. The title card opens the video and carries neither.
 */
export function chrome(scene, state) {
  const bar = knowsChapters(state) && scene.template !== "title"
    ? `<div class="chrome-progress">${Array.from({ length: state.chapterCount }, (_, index) => {
      const place = index + 1 < state.chapterNumber ? ' class="done"' : index + 1 === state.chapterNumber ? ' class="now"' : "";
      return `<span${place}></span>`;
    }).join("")}</div>`
    : "";
  const index = knowsChapters(state) ? `<span class="index">${pad(state.chapterNumber)} / ${pad(state.chapterCount)}</span>` : "";
  const label = state.chapter ? `<div class="chrome-chapter">${index}${escapeHtml(state.chapter)}</div>` : "";
  return `${bar}${label}<div class="chrome-brand">${BRAND}</div>`;
}

/**
 * One slide state as a complete HTML page.
 * state: { reveal, previousReveal, first, totalReveals, chapter (label to show), chapterNumber, chapterCount }
 */
export function slideHtml(scene, state) {
  const renderer = RENDERERS[scene.template];
  if (!renderer) throw new Error(`unknown template ${scene.template}`);
  const context = {
    ...state,
    visible: (count) => visibility(count, state.totalReveals, state.reveal, state.previousReveal, state.first),
  };
  return page(`${chrome(scene, state)}<main class="content t-${scene.template}">${renderer(scene.data, context)}</main>`, SIZE, templateCss(scene));
}

/**
 * A series' own thumbnail (docs/videos/so-thats-why/thumbnails.md): its palette, its name in place
 * of the channel's, a red stamp, the tag coloured by the episode's pillar, and a shorter headline.
 * The render plan picks it from the video (the flat-explainer look is So That's Why).
 */
export const THUMB_SERIES = {
  sothatswhy: { brand: "原來如此事務所", stamp: ["原來", "如此"], headlineMax: 10, headlineLines: 2 },
};
export const THUMB_PILLARS = ["business", "science", "travel", "tech"];
/** A series' thumbnail keeps the full-width text column and may mirror it (the stamp follows). */
export const THUMB_SERIES_LAYOUTS = ["left", "right"];
/**
 * The channel's thumbnail (docs/videos/README.md §版型, the owner's 2026-10-08 decision): the text
 * column is the left 40%, the subject the right 60%, in one of three layouts the slug rotates
 * through unless `data.layout` names one: a) the subject on a card inset in its area, b) the
 * subject filling the frame under a scrim on the text side, c) a hard split with the text column
 * on a solid tone. Without a picture the subject area is a flat tone, one of THUMB_TONES by the
 * slug, in place of the ring and dot the theme used to draw for all eleven of the first batch.
 */
export const THUMB_LAYOUTS = ["a", "b", "c"];
export const THUMB_TONES = ["teal", "plum", "navy", "forest"];
/** The subject's sources, in the order render prefers them (render/plan.mjs drawThumbnail). */
export const THUMB_SUBJECTS = ["capture", "shot"];
/**
 * The channel's headline: at most six characters of the kind a phone shows at a glance (a CJK
 * glyph counts one, a Latin word or a number counts one, and at most two of those), on one or two
 * lines. The limit is the visuals reference's (.agents/skills/youtube-video/references/visuals.md
 * §縮圖); the 40% column holds three CJK glyphs a line at the theme's size, so six is two lines.
 * The qa stage holds a thumbnail to it (tools/video/qa/thumbnail.mjs); render draws any length.
 */
export const THUMB_HEADLINE_MAX = 6;
export const THUMB_HEADLINE_WORDS_MAX = 2;
const CJK_GLYPH = /[぀-ヿ㐀-鿿豈-﫿가-힯]/u;
/**
 * A Latin word or a number in a headline, for the count here and the line model of the qa stage
 * (tools/video/qa/thumbnail.mjs headlineTokens): letters and digits with the marks a word or a
 * number carries inside (v2.0, 16x, 1,000, don't, 50%), after an optional currency sign, so
 * 「NT$270」, 「$50」 and 「1,000」 each count one. A comma at its end is the sentence's, not the
 * word's: the count drops it, the line model keeps it with the word as the browser does.
 */
export const HEADLINE_WORD = /(?:NT\$|US\$|[$€¥£￥])?[A-Za-z0-9][A-Za-z0-9.,'%+-]*/g;
/** The headline's count: { cjk, words: [the Latin words and numbers], count: cjk + words }. */
export function headlineCount(headline) {
  const plain = String(headline).replace(/\*\*/g, "");
  const words = (plain.match(HEADLINE_WORD) ?? []).map((word) => word.replace(/,+$/, ""));
  const cjk = [...plain].filter((char) => CJK_GLYPH.test(char)).length;
  return { cjk, words, count: cjk + words.length };
}
const headlineShape = (headline) => {
  const lines = headline.replace(/\*\*/g, "").split("\n");
  return { lines: lines.length, chars: Math.max(...lines.map((line) => [...line.replace(/\s/g, "")].length)) };
};
/**
 * The layout and tone a slug rotates to, the same hash as the slides look (core/drama.mjs
 * slidesPresetFor) so a video always gets the same one; `offset` moves the B and C variants of
 * YouTube's test one step on, so the three differ in more than their words. Two videos in a row
 * share a tone one time in four: `data.tone` names another when the owner sees it happen.
 */
export function thumbnailRotation(slug, offset = 0) {
  let hash = 2166136261;
  for (const char of String(slug ?? "")) hash = Math.imul(hash ^ char.charCodeAt(0), 16777619) >>> 0;
  return { layout: THUMB_LAYOUTS[(hash + offset) % THUMB_LAYOUTS.length], tone: THUMB_TONES[(Math.floor(hash / THUMB_LAYOUTS.length) + offset) % THUMB_TONES.length] };
}
/**
 * `data.capture` names a screencast scene whose still is the subject, as "<scene id>" (its first
 * capture) or "<scene id>#<n>" (its n-th, from 1). Returns { scene, index } (index from 0) or null.
 */
export function captureRef(value) {
  const match = typeof value === "string" ? /^([a-z0-9]+(?:-[a-z0-9]+)*)(?:#([1-9]\d*))?$/.exec(value) : null;
  return match ? { scene: match[1], index: match[2] ? Number(match[2]) - 1 : 0 } : null;
}

/**
 * YouTube's "Test & compare" takes up to three thumbnails (docs/videos/so-thats-why/thumbnails.md,
 * A/B): `thumbnail` itself is A, and `thumbnail.variants` holds B and C, each `{ data }` laid over
 * A's data (so B may change only the headline). Returns [{ id: "b", thumbnail }, ...].
 */
export const THUMB_VARIANT_IDS = ["b", "c"];
export function thumbnailVariants(thumbnail) {
  const variants = Array.isArray(thumbnail?.variants) ? thumbnail.variants : [];
  return variants.slice(0, THUMB_VARIANT_IDS.length).map((variant, index) => ({
    id: THUMB_VARIANT_IDS[index],
    thumbnail: { template: thumbnail.template, data: { ...thumbnail.data, ...(variant?.data ?? {}) } },
  }));
}

export function thumbnailProblems(thumbnail, { series = null } = {}) {
  if (!thumbnail) return [];
  const problems = ownThumbnailProblems(thumbnail, series);
  if (thumbnail.variants === undefined) return problems;
  const variants = thumbnail.variants;
  if (!Array.isArray(variants) || !variants.length || variants.length > THUMB_VARIANT_IDS.length || !variants.every((variant) => isObject(variant) && isObject(variant.data))) {
    return [...problems, `thumbnail.variants must be 1 to ${THUMB_VARIANT_IDS.length} of { data: {...} } (A is the thumbnail itself; YouTube tests up to three)`];
  }
  for (const { id, thumbnail: variant } of thumbnailVariants(thumbnail)) {
    for (const message of ownThumbnailProblems(variant, series)) problems.push(`variant ${id}: ${message}`);
  }
  return problems;
}

function ownThumbnailProblems(thumbnail, series) {
  const data = thumbnail.data ?? {};
  const problems = [!isText(data.headline) && "thumbnail.data.headline is required", data.tag !== undefined && !isText(data.tag) && "thumbnail.data.tag must be text", data.sub !== undefined && !isText(data.sub) && "thumbnail.data.sub must be text"];
  const own = THUMB_SERIES[series];
  const layouts = own ? THUMB_SERIES_LAYOUTS : THUMB_LAYOUTS;
  if (data.layout !== undefined && !layouts.includes(data.layout)) problems.push(`thumbnail.data.layout must be one of ${layouts.join(", ")}`);
  if (data.tone !== undefined && !THUMB_TONES.includes(data.tone)) problems.push(`thumbnail.data.tone must be one of ${THUMB_TONES.join(", ")}`);
  if (data.pillar !== undefined && !THUMB_PILLARS.includes(data.pillar)) problems.push(`thumbnail.data.pillar must be one of ${THUMB_PILLARS.join(", ")}`);
  if (data.capture !== undefined && !captureRef(data.capture)) problems.push('thumbnail.data.capture must name a screencast scene, "<scene id>" or "<scene id>#<n>" for its n-th capture');
  if (data.shot !== undefined && !isText(data.shot)) problems.push("thumbnail.data.shot must be a shot's id");
  // The channel's headline length (THUMB_HEADLINE_MAX) is the qa stage's business
  // (tools/video/qa/thumbnail.mjs), where it fails the thumbnail item: the fixtures and the
  // first batch's scripts carry longer headlines, and render still draws those.
  if (own && isText(data.headline)) {
    const shape = headlineShape(data.headline);
    if (shape.lines > own.headlineLines) problems.push(`thumbnail.data.headline has ${shape.lines} lines; this series takes at most ${own.headlineLines}`);
    if (shape.chars > own.headlineMax) problems.push(`thumbnail.data.headline has a line of ${shape.chars} characters; this series takes at most ${own.headlineMax} a line, readable at phone size`);
  }
  return problems.filter(Boolean);
}

// A series' thumbnail sits on a keyframe: the picture fills the frame under a scrim that keeps
// the headline readable. The CSS lives here rather than in the theme so that adding it changed
// no slides video's frame keys.
const THUMB_BACKGROUND_CSS =
  ".thumb-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}" +
  ".thumb-scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,38,39,.94) 0%,rgba(14,38,39,.72) 48%,rgba(14,38,39,.12) 100%)}";

// So That's Why (docs/videos/so-thats-why/look.md): cream, ink navy, stamp red, mustard. Inline
// for the same reason as the keyframe CSS: no other video's thumbnail key moves.
const THUMB_SERIES_CSS = {
  sothatswhy:
    ".thumb-scrim{background:linear-gradient(90deg,rgba(31,42,68,.94) 0%,rgba(31,42,68,.7) 48%,rgba(31,42,68,.1) 100%)}" +
    ".thumb h1{color:#f6efe3}.thumb em{color:#e8b64c}.thumb .sub{color:#e9dfcd}" +
    ".thumb .brand{color:#e8b64c;letter-spacing:.12em}" +
    ".thumb .tag{background:#e8b64c;color:#1f2a44}" +
    ".thumb .tag.pillar-science{background:#f6efe3;color:#1f2a44}" +
    ".thumb .tag.pillar-travel{background:#1f2a44;color:#e8b64c;box-shadow:inset 0 0 0 3px #e8b64c}" +
    ".thumb .tag.pillar-tech{background:#1f2a44;color:#f6efe3;box-shadow:inset 0 0 0 3px #f6efe3}" +
    ".thumb-stamp{position:absolute;left:785px;top:75px;width:150px;height:150px;transform:rotate(-8deg);border:9px solid #d8452f;border-radius:10px;" +
    "color:#d8452f;opacity:.9;display:grid;grid-template-rows:1fr 1fr;place-items:center;font-size:52px;font-weight:900;line-height:1;letter-spacing:.04em}" +
    ".thumb.layout-right~.thumb-stamp{left:auto;right:785px}",
};
// The text column on the right and the scrim mirrored, for a picture whose subject is on the left.
const THUMB_RIGHT_CSS =
  ".thumb.layout-right{padding-right:72px;padding-left:340px;align-items:flex-end;text-align:right}" +
  ".thumb.layout-right .tag{align-self:flex-end}.thumb.layout-right .brand{left:auto;right:72px}" +
  ".thumb-scrim.layout-right{transform:scaleX(-1)}";

/**
 * The thumbnail as a page. `background` is the URL of the subject's picture (a screencast still
 * or a shot's keyframe, served from the work directory) and `subject` which of THUMB_SUBJECTS it
 * is: a page still is cropped to its top left corner, where the product's name and interface
 * are; a keyframe to its right side, where the writer left the subject. Without a picture the
 * subject area is a flat tone. `series` names a series' own look (THUMB_SERIES), which keeps
 * the full-width column, the scrim and the mirrored layout of docs/videos/so-thats-why/thumbnails.md.
 * `slug` and `offset` pick the channel's layout and tone (thumbnailRotation) when `data.layout`
 * and `data.tone` do not. `locale` is the caption locale a translated thumbnail is for: Korean,
 * Simplified Chinese and Japanese are set in their own font (page).
 */
export function thumbnailHtml(thumbnail, { background = null, subject = null, series = null, locale = null, slug = null, offset = 0 } = {}) {
  const data = thumbnail.data;
  const own = THUMB_SERIES[series] ?? null;
  if (own) return page(seriesThumbnailBody(data, own, background), THUMB_SIZE, [background ? THUMB_BACKGROUND_CSS : "", data.layout === "right" ? THUMB_RIGHT_CSS : "", THUMB_SERIES_CSS[series]].join(""), { locale });
  const rotation = thumbnailRotation(slug, offset);
  const layout = THUMB_LAYOUTS.includes(data.layout) ? data.layout : rotation.layout;
  const tone = THUMB_TONES.includes(data.tone) ? data.tone : rotation.tone;
  const classes = `layout-${layout} tone-${tone}`;
  const kind = THUMB_SUBJECTS.includes(subject) ? subject : THUMB_SUBJECTS[1];
  const body = [
    `<div class="thumb-subject ${classes}${background ? ` from-${kind}` : ""}">${background ? `<img src="${escapeHtml(background)}" alt="">` : ""}</div>`,
    `<div class="thumb column ${classes}">`,
    data.tag ? `<div class="tag">${richText(data.tag)}</div>` : "",
    `<h1 class="fit">${richText(data.headline)}</h1>`,
    data.sub ? `<div class="sub fit">${richText(data.sub)}</div>` : "",
    `<div class="brand">${BRAND}</div>`,
    "</div>",
  ].join("");
  return page(body, THUMB_SIZE, "", { locale });
}

// A series' page as it always was, less the ring a series thumbnail without its keyframe used to show.
function seriesThumbnailBody(data, own, background) {
  const layout = data.layout === "right" ? " layout-right" : "";
  const pillar = THUMB_PILLARS.includes(data.pillar) ? ` pillar-${data.pillar}` : "";
  return [
    background ? `<img class="thumb-bg" src="${escapeHtml(background)}" alt=""><div class="thumb-scrim${layout}"></div>` : "",
    `<div class="thumb series${layout}">`,
    data.tag ? `<div class="tag${pillar}">${richText(data.tag)}</div>` : "",
    `<h1 class="fit">${richText(data.headline)}</h1>`,
    data.sub ? `<div class="sub fit">${richText(data.sub)}</div>` : "",
    `<div class="brand">${escapeHtml(own.brand)}</div>`,
    "</div>",
    `<div class="thumb-stamp" aria-hidden="true">${own.stamp.map((row) => `<span>${escapeHtml(row)}</span>`).join("")}</div>`,
  ].join("");
}

/** The characters a slide will draw, for the font coverage check. */
export function visibleText(html) {
  return html
    .replace(/<head>[\s\S]*?<\/head>/, "")
    .replace(/<[^>]+>/g, "")
    .replace(/&(amp|lt|gt|quot|#39);/g, (_, name) => ({ amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'" })[name]);
}
