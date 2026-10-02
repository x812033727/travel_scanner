// The fonts pages are drawn with, and which characters they cover.
//
// A character no bundled font has would silently fall back to whatever the machine has installed,
// so the same video would render differently on Windows and in CI, and a Simplified form or an
// emoji could slip into a Traditional Chinese slide unnoticed. Render refuses such a slide.
// Coverage comes from the fontsource CSS: each @font-face subset declares its unicode-range.
//
// Slides and the video's own thumbnail are Traditional Chinese, set in Noto Sans TC with
// JetBrains Mono for code. A caption locale whose script that font lacks or draws in another
// font's weight gets its own font, first in the stack, on its own thumbnail only (LOCALE_FONTS):
// Korean (Hangul), Simplified Chinese, and Japanese, whose kanji the TC font draws in their
// Traditional Chinese forms (直, 骨, 写 differ in stroke from the Japanese standard). Coverage is
// judged per language, so a Traditional Chinese slide still refuses the Simplified forms only the
// SC font has.
import { readFileSync } from "node:fs";
import { createRequire } from "node:module";
import path from "node:path";

export const FONT_PACKAGES = {
  "noto-sans-tc": "@fontsource-variable/noto-sans-tc",
  "jetbrains-mono": "@fontsource-variable/jetbrains-mono",
  "noto-sans-kr": "@fontsource-variable/noto-sans-kr",
  "noto-sans-sc": "@fontsource-variable/noto-sans-sc",
  "noto-sans-jp": "@fontsource-variable/noto-sans-jp",
};

/** The fonts every page loads: the slide font and the code font. */
export const SLIDE_FONTS = ["noto-sans-tc", "jetbrains-mono"];
export const SLIDE_FAMILY = "Noto Sans TC Variable";

/** Caption locales whose thumbnail is set in a font of its own, with the page's lang attribute. */
export const LOCALE_FONTS = {
  ko: { font: "noto-sans-kr", family: "Noto Sans KR Variable", lang: "ko" },
  "zh-CN": { font: "noto-sans-sc", family: "Noto Sans SC Variable", lang: "zh-Hans" },
  ja: { font: "noto-sans-jp", family: "Noto Sans JP Variable", lang: "ja" },
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

/** The fonts a page in `locale` is set in; without a locale of its own, the slide fonts. */
export function pageFonts(locale = null) {
  const own = LOCALE_FONTS[locale]?.font;
  return own ? [own, ...SLIDE_FONTS] : SLIDE_FONTS;
}

const cached = new Map();
/**
 * The union of what a page's fonts cover: the slide fonts by default (slides, the video's own
 * thumbnail), plus the locale's own font for a caption locale's thumbnail.
 */
export function bundledCoverage(locale = null) {
  const fonts = pageFonts(locale);
  const key = fonts.join(",");
  if (!cached.has(key)) {
    const css = fonts.map((name) => readFileSync(path.join(fontDir(name), "index.css"), "utf8"));
    cached.set(key, mergeRanges(css.flatMap((sheet) => parseUnicodeRanges(sheet))));
  }
  return cached.get(key);
}
