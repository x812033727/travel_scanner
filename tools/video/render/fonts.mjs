// The two fonts slides are drawn with, and which characters they cover.
//
// A character no bundled font has would silently fall back to whatever the machine has installed,
// so the same video would render differently on Windows and in CI, and a Simplified form or an
// emoji could slip into a Traditional Chinese slide unnoticed. Render refuses such a slide.
// Coverage comes from the fontsource CSS: each @font-face subset declares its unicode-range.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

export const FONT_PACKAGES = {
  "noto-sans-tc": "@fontsource-variable/noto-sans-tc",
  "jetbrains-mono": "@fontsource-variable/jetbrains-mono",
};

const require = createRequire(import.meta.url);

/** The installed directory of a font package, or a clear error telling you to install it. */
export function fontDir(name) {
  const pkg = FONT_PACKAGES[name];
  try {
    return path.dirname(require.resolve(`${pkg}/package.json`));
  } catch {
    throw new Error(`${pkg} is not installed; run npm ci in this checkout`);
  }
}

/** [start, end] code point pairs from every unicode-range in a stylesheet. */
export function parseUnicodeRanges(css) {
  const ranges = [];
  for (const [, list] of css.matchAll(/unicode-range:\s*([^;]+);/g)) {
    for (const part of list.split(",")) {
      const token = part.trim().replace(/^U\+/i, "");
      if (!token) continue;
      if (token.includes("?")) {
        ranges.push([parseInt(token.replace(/\?/g, "0"), 16), parseInt(token.replace(/\?/g, "F"), 16)]);
      } else if (token.includes("-")) {
        const [start, end] = token.split("-").map((value) => parseInt(value, 16));
        ranges.push([start, end]);
      } else {
        const point = parseInt(token, 16);
        ranges.push([point, point]);
      }
    }
  }
  return mergeRanges(ranges);
}

export function mergeRanges(ranges) {
  const sorted = ranges.filter(([start, end]) => Number.isFinite(start) && Number.isFinite(end)).sort((a, b) => a[0] - b[0]);
  const merged = [];
  for (const [start, end] of sorted) {
    const last = merged.at(-1);
    if (last && start <= last[1] + 1) last[1] = Math.max(last[1], end);
    else merged.push([start, end]);
  }
  return merged;
}

export function covers(ranges, point) {
  let low = 0;
  let high = ranges.length - 1;
  while (low <= high) {
    const middle = (low + high) >> 1;
    const [start, end] = ranges[middle];
    if (point < start) high = middle - 1;
    else if (point > end) low = middle + 1;
    else return true;
  }
  return false;
}

/** Characters in `text` that no range covers, whitespace and control characters aside. */
export function uncovered(text, ranges) {
  const missing = new Set();
  for (const char of text) {
    const point = char.codePointAt(0);
    if (point < 0x21 || /\s/u.test(char)) continue;
    if (!covers(ranges, point)) missing.add(char);
  }
  return [...missing];
}

let cached = null;
/** The union of what the bundled fonts cover. */
export function bundledCoverage() {
  if (!cached) {
    const css = Object.keys(FONT_PACKAGES).map((name) => readFileSync(path.join(fontDir(name), "index.css"), "utf8"));
    cached = mergeRanges(css.flatMap((sheet) => parseUnicodeRanges(sheet)));
  }
  return cached;
}
