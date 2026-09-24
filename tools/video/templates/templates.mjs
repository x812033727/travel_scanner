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
  outro: {
    check: (data) => [!isText(data.title) && "title is required", data.cta !== undefined && !isText(data.cta) && "cta must be text", data.lines !== undefined && !isTextList(data.lines, 1, 4) && "lines must be 1 to 4 strings"],
    capacity: () => 0,
  },
};

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
    return [
      number ? `<div ${enterClass(state.first, "number", 0)}>${escapeHtml(String(number).padStart(2, "0"))}</div>` : "",
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
    return `${heading(data, state.first)}<div class="frame"><div ${enterClass(state.first, "paper", 1)}><img src="${assetUrl(data.svg)}" alt=""></div></div>${data.caption ? `<div class="caption-line">${richText(data.caption)}</div>` : ""}`;
  },
  screenshot(data, state) {
    const box = data.highlight
      ? `<div${attrs(state.visible(1)(0), "box mark", `left:${data.highlight.x}%;top:${data.highlight.y}%;width:${data.highlight.w}%;height:${data.highlight.h}%`)}></div>`
      : "";
    return `${heading(data, state.first)}<div class="frame"><div ${enterClass(state.first, "shot", 1)}><img src="${assetUrl(data.image)}" alt="">${box}</div></div>${data.caption ? `<div class="caption-line">${richText(data.caption)}</div>` : ""}`;
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

function page(body, size) {
  return [
    "<!doctype html>",
    '<html lang="zh-Hant"><head><meta charset="utf-8">',
    `<link rel="stylesheet" href="${ORIGIN}/fonts/noto-sans-tc/index.css">`,
    `<link rel="stylesheet" href="${ORIGIN}/fonts/jetbrains-mono/index.css">`,
    `<link rel="stylesheet" href="${ORIGIN}/theme.css">`,
    `<style>:root{--width:${size.width}px;--height:${size.height}px}</style>`,
    `</head><body>${body}</body></html>`,
  ].join("");
}

/**
 * One slide state as a complete HTML page.
 * state: { reveal, previousReveal, first, totalReveals, chapter (label to show), chapterNumber }
 */
export function slideHtml(scene, state) {
  const renderer = RENDERERS[scene.template];
  if (!renderer) throw new Error(`unknown template ${scene.template}`);
  const context = {
    ...state,
    visible: (count) => visibility(count, state.totalReveals, state.reveal, state.previousReveal, state.first),
  };
  const chrome = `${state.chapter ? `<div class="chrome-chapter">${escapeHtml(state.chapter)}</div>` : ""}<div class="chrome-brand">${BRAND}</div>`;
  return page(`${chrome}<main class="content t-${scene.template}">${renderer(scene.data, context)}</main>`, SIZE);
}

export function thumbnailProblems(thumbnail) {
  if (!thumbnail) return [];
  const data = thumbnail.data ?? {};
  return [!isText(data.headline) && "thumbnail.data.headline is required", data.tag !== undefined && !isText(data.tag) && "thumbnail.data.tag must be text", data.sub !== undefined && !isText(data.sub) && "thumbnail.data.sub must be text"].filter(Boolean);
}

export function thumbnailHtml(thumbnail) {
  const data = thumbnail.data;
  const body = [
    '<div class="thumb-art"></div>',
    '<div class="thumb">',
    data.tag ? `<div class="tag">${richText(data.tag)}</div>` : "",
    `<h1 class="fit">${richText(data.headline)}</h1>`,
    data.sub ? `<div class="sub fit">${richText(data.sub)}</div>` : "",
    `<div class="brand">${BRAND}</div>`,
    "</div>",
  ].join("");
  return page(body, THUMB_SIZE);
}

/** The characters a slide will draw, for the font coverage check. */
export function visibleText(html) {
  return html
    .replace(/<head>[\s\S]*?<\/head>/, "")
    .replace(/<[^>]+>/g, "")
    .replace(/&(amp|lt|gt|quot|#39);/g, (_, name) => ({ amp: "&", lt: "<", gt: ">", quot: '"', "#39": "'" })[name]);
}
