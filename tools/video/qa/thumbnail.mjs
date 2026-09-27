// The thumbnail check: YouTube's size limits, and a headline that still reads on a phone.
//
// The size and the byte count are read from the JPEG or PNG header, so the check needs neither a
// browser nor an image library. The headline's height is estimated from the thumb template's
// numbers (tools/video/templates/theme.css) and the renderer's fitting rule
// (tools/video/render/browser.mjs fitText): render does not record the size it settled on, so
// the estimate repeats its greedy shrink on a model of the layout. A test pins the numbers to
// theme.css, so a theme change fails here until they are updated.
import { THUMB_SIZE } from "../templates/templates.mjs";

// Same as tools/video/render/cli.mjs THUMBNAIL_MAX_BYTES: YouTube's limit for custom thumbnails.
export const MAX_BYTES = 2 * 1024 * 1024;
// The width the phone check scales to: the skill's publish checklist reads the thumbnail "at 320
// wide", a phone feed thumbnail at 1x, a quarter of the 1280 px frame.
export const PHONE_WIDTH = 320;
/**
 * The smallest headline glyph height, in pixels at PHONE_WIDTH, that passes. How it was chosen:
 * theme.css sets the headline at 136 px (34 px at 320 wide), and the renderer lets a `.fit`
 * element shrink to 60% (82 px, 20 px at 320) before it reports overflow. 24 px sits between
 * them: a 96 px headline in the frame, about 70% of the theme's size, which is what a headline
 * of three full lines settles at. A CJK glyph 24 px tall on a 320 px wide picture is roughly
 * the height of a phone app's title text, and leaves room for JPEG softness and the smaller
 * tiles of a tablet grid. Revisit after the first hands-off batch if a thumbnail the owner
 * would have accepted fails here.
 */
export const MIN_HEADLINE_PX_AT_PHONE = 24;

// The thumb template's headline, as theme.css sets it (`.thumb` and `.thumb h1`).
export const HEADLINE = {
  fontSize: 136, // .thumb h1 font-size
  lineHeight: 1.1, // .thumb h1 line-height
  maxHeight: 460, // .thumb h1 max-height
  width: THUMB_SIZE.width - 72 - 340, // the frame less .thumb's left padding (72) and right padding (340)
  minScale: 0.6, // fitText stops shrinking at 60% of the start size
  step: 2, // fitText shrinks 2 px at a time
  tolerance: 0.4, // fitText counts vertical overflow only past 0.4 em
};

/** Width, height and format from a JPEG or PNG header, or null when it is neither. */
export function imageSize(bytes) {
  const buffer = Buffer.from(bytes);
  if (buffer.length >= 24 && buffer.subarray(0, 8).equals(Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a])) && buffer.subarray(12, 16).toString("latin1") === "IHDR") {
    return { format: "png", width: buffer.readUInt32BE(16), height: buffer.readUInt32BE(20) };
  }
  if (buffer.length < 4 || buffer[0] !== 0xff || buffer[1] !== 0xd8) return null;
  let offset = 2;
  while (offset + 4 <= buffer.length) {
    if (buffer[offset] !== 0xff) return null;
    const marker = buffer[offset + 1];
    if (marker === 0xff) {
      offset += 1; // fill bytes before a marker
      continue;
    }
    // Start-of-frame markers carry the frame's dimensions (C4, C8 and CC are not frames).
    if (marker >= 0xc0 && marker <= 0xcf && marker !== 0xc4 && marker !== 0xc8 && marker !== 0xcc) {
      if (offset + 9 > buffer.length) return null;
      return { format: "jpeg", height: buffer.readUInt16BE(offset + 5), width: buffer.readUInt16BE(offset + 7) };
    }
    if (marker === 0xd8 || marker === 0x01 || (marker >= 0xd0 && marker <= 0xd7)) {
      offset += 2; // standalone markers have no length
      continue;
    }
    if (marker === 0xd9 || marker === 0xda) return null; // end of image, or scan data before any frame
    offset += 2 + buffer.readUInt16BE(offset + 2);
  }
  return null;
}

// Glyph widths in em, as Noto Sans TC draws them: a CJK glyph fills the em; Latin letters and
// digits take about six tenths of it in the heavy weight; a space a third; ASCII punctuation less.
const CJK = /[぀-ヿ㐀-鿿豈-﫿가-힯＀-｠]/u;
function glyphWidth(char) {
  if (CJK.test(char)) return 1;
  if (/\s/.test(char)) return 0.3;
  if (/[A-Za-z0-9]/.test(char)) return 0.6;
  return 0.4;
}

/**
 * The headline's tokens, each { width in em, breakable? }: a CJK glyph may break from its
 * neighbours; a Latin word or number never breaks inside; an emphasised run (**...**) stays on
 * one line (theme.css sets `.thumb em` to nowrap). Explicit line breaks come back as null.
 */
export function headlineTokens(headline) {
  const tokens = [];
  const lines = String(headline).split("\n");
  lines.forEach((line, index) => {
    if (index) tokens.push(null);
    for (const [, emphasis, plain] of line.matchAll(/\*\*(.+?)\*\*|([^*]+|\*)/g)) {
      if (emphasis !== undefined) {
        tokens.push({ width: [...emphasis].reduce((sum, char) => sum + glyphWidth(char), 0) });
        continue;
      }
      for (const run of plain.match(/[A-Za-z0-9][A-Za-z0-9.'%+-]*|\s+|./gsu) ?? []) {
        tokens.push({ width: [...run].reduce((sum, char) => sum + glyphWidth(char), 0), space: /^\s+$/.test(run) });
      }
    }
  });
  return tokens;
}

/** How many lines the headline takes at a font size, and whether a token is wider than the box. */
export function headlineLayout(tokens, fontSize, width = HEADLINE.width) {
  let lines = 1;
  let used = 0;
  let tooWide = false;
  for (const token of tokens) {
    if (token === null) {
      lines += 1;
      used = 0;
      continue;
    }
    const px = token.width * fontSize;
    if (px > width) tooWide = true;
    if (used > 0 && used + px > width) {
      lines += 1;
      used = token.space ? 0 : px;
    } else {
      used += px;
    }
  }
  return { lines, tooWide };
}

/**
 * The font size the renderer's fitText settles on for the headline, in pixels of the 1280 px
 * frame: the theme's size, shrunk in steps while the text overflows its box, never below the
 * renderer's floor. A headline that still overflows at the floor comes back at the floor; the
 * render item reports that overflow from the renderer's own check.
 */
export function headlineSizeEstimate(headline, rule = HEADLINE) {
  const tokens = headlineTokens(headline);
  const overflows = (size) => {
    const { lines, tooWide } = headlineLayout(tokens, size, rule.width);
    return tooWide || lines * rule.lineHeight * size - rule.maxHeight > rule.tolerance * size;
  };
  let size = rule.fontSize;
  while (overflows(size) && size - rule.step > rule.fontSize * rule.minScale) size -= rule.step;
  return size;
}

/** A glyph height in the frame, scaled to PHONE_WIDTH. */
export const atPhoneWidth = (px) => Math.round((px * PHONE_WIDTH) / THUMB_SIZE.width);

/**
 * The thumbnail item's verdict from the file's bytes and the headline video.json asked for:
 * { ok, detail, warnings }.
 */
export function thumbnailChecks({ bytes, headline }) {
  const problems = [];
  const size = imageSize(bytes);
  if (!size) problems.push("the file is not a JPEG or PNG");
  else if (size.width !== THUMB_SIZE.width || size.height !== THUMB_SIZE.height) problems.push(`${size.width}x${size.height}; YouTube wants ${THUMB_SIZE.width}x${THUMB_SIZE.height}`);
  if (bytes.length > MAX_BYTES) problems.push(`${bytes.length} bytes; YouTube's limit is 2 MB`);
  const headlinePx = typeof headline === "string" && headline.trim() ? atPhoneWidth(headlineSizeEstimate(headline)) : null;
  if (headlinePx !== null && headlinePx < MIN_HEADLINE_PX_AT_PHONE) {
    problems.push(`the headline shrinks to about ${headlinePx} px at ${PHONE_WIDTH} px wide; at least ${MIN_HEADLINE_PX_AT_PHONE} px reads on a phone, so shorten it`);
  }
  const kb = Math.round(bytes.length / 1024);
  const described = size ? `${size.width}x${size.height} ${size.format.toUpperCase()}, ${kb} KB` : `${kb} KB`;
  const glyphs = headlinePx === null ? "" : `; the headline is about ${headlinePx} px tall at ${PHONE_WIDTH} px wide`;
  return { ok: problems.length === 0, detail: problems.length ? problems.join("; ") : `${described}${glyphs}`, warnings: [] };
}
