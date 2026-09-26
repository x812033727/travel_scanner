// Slide templates: scene data in, HTML out, as pure functions so they are tested without a browser.
//
// A scene's `lines[].reveal` counts apply to the last N elements of its template: a bullets slide
// with three items and three reveals starts empty and gains one item per reveal; with no reveals
// every item is there from the start. Elements that appear in a state get the `enter` class, and
// the renderer freezes that entrance animation frame by frame (tools/video/render/browser.mjs).
export const ORIGIN = "https://video.local";
export const SIZE = { width: 1920, height: 1080 };
export const THUMB_SIZE = { width: 1280, height: 720 };
export const BRAND = "MOKAAIR";
export const SITE_LABEL = "mokaair.com";

const isText = (value) => typeof value === "string" && value.trim().length > 0;
const isTextList = (value, min, max) => Array.isArray(value) && value.length >= min && value.length <= max && value.every(isText);
const isPercent = (value) => typeof value === "number" && value >= 0 && value <= 100;

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
      !isAssetPath(data.image, /\.(png|jpe?g|webp)$/i) && `image must be a repository path under ${ASSET_ROOTS.join(" or ")}`,
      data.highlight !== undefined && !(data.highlight && ["x", "y", "w", "h"].every((key) => isPercent(data.highlight[key]))) && "highlight must be { x, y, w, h } in percent",
      data.caption !== undefined && !isText(data.caption) && "caption must be text",
    ],
    capacity: (data) => (data.highlight ? 1 : 0),
  },
  // The next four came from a reference video (2026-09-26): concrete little artefacts instead of
  // one slide of text left up for half a minute.
  chat: {
    check: (data) => [
      data.title !== undefined && !isText(data.title) && "title must be text",
      !(Array.isArray(data.messages) && data.messages.length >= 1 && data.messages.length <= 5 &&
        data.messages.every((message) => message && ["left", "right"].includes(message.side) && isText(message.text) && (message.name === undefined || isText(message.name)))) &&
        "messages must be 1 to 5 of { side: left|right, name?, text }",
    ],
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
    return `${heading(data, state.first)}<div class="frame"><div ${enterClass(state.first, "shot", 1)}><img src="${assetUrl(data.image)}" alt="">${box}</div></div>${data.caption ? `<div class="caption-line">${richText(data.caption)}</div>` : ""}`;
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

function page(body, size, extraCss = "") {
  return [
    "<!doctype html>",
    '<html lang="zh-Hant"><head><meta charset="utf-8">',
    `<link rel="stylesheet" href="${ORIGIN}/fonts/noto-sans-tc/index.css">`,
    `<link rel="stylesheet" href="${ORIGIN}/fonts/jetbrains-mono/index.css">`,
    `<link rel="stylesheet" href="${ORIGIN}/theme.css">`,
    `<style>:root{--width:${size.width}px;--height:${size.height}px}${extraCss}</style>`,
    `</head><body>${body}</body></html>`,
  ].join("");
}

/**
 * Where the viewer is: a bar across the top with one segment per chapter, the ones seen and the
 * current one marked, and "02 / 06 chapter" in the corner. The owner asked for both after a
 * reference video on 2026-09-26. The title card opens the video and carries neither.
 */
function chrome(scene, state) {
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
  return page(`${chrome(scene, state)}<main class="content t-${scene.template}">${renderer(scene.data, context)}</main>`, SIZE);
}

export function thumbnailProblems(thumbnail) {
  if (!thumbnail) return [];
  const data = thumbnail.data ?? {};
  return [!isText(data.headline) && "thumbnail.data.headline is required", data.tag !== undefined && !isText(data.tag) && "thumbnail.data.tag must be text", data.sub !== undefined && !isText(data.sub) && "thumbnail.data.sub must be text"].filter(Boolean);
}

// A drama's thumbnail sits on a keyframe: the picture fills the frame under a scrim that keeps
// the headline readable, in place of the decorative ring. The CSS lives here rather than in the
// theme so that adding it changed no slides video's frame keys.
const THUMB_BACKGROUND_CSS =
  ".thumb-bg{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}" +
  ".thumb-scrim{position:absolute;inset:0;background:linear-gradient(90deg,rgba(14,38,39,.94) 0%,rgba(14,38,39,.72) 48%,rgba(14,38,39,.12) 100%)}";

/**
 * The thumbnail as a page. `background` is the URL of a picture to fill it with (a drama's
 * keyframe, served from the work directory); without one the theme's ring decorates it.
 */
export function thumbnailHtml(thumbnail, { background = null } = {}) {
  const data = thumbnail.data;
  const body = [
    background ? `<img class="thumb-bg" src="${escapeHtml(background)}" alt=""><div class="thumb-scrim"></div>` : '<div class="thumb-art"></div>',
    '<div class="thumb">',
    data.tag ? `<div class="tag">${richText(data.tag)}</div>` : "",
    `<h1 class="fit">${richText(data.headline)}</h1>`,
    data.sub ? `<div class="sub fit">${richText(data.sub)}</div>` : "",
    `<div class="brand">${BRAND}</div>`,
    "</div>",
  ].join("");
  return page(body, THUMB_SIZE, background ? THUMB_BACKGROUND_CSS : "");
}

/** The characters a slide will draw, for the font coverage check. */
export function visibleText(html) {
  return html
    .replace(/<head>[\s\S]*?<\/head>/, "")
    .replace(/<[^>]+>/g, "")
    .replace(/&(amp|lt|gt|quot|#39);/g, (_, name) => ({ amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'" })[name]);
}
