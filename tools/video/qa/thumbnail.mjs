// The thumbnail check: YouTube's size limits, and a headline that still reads on a phone, says
// one thing in at most six characters, breaks between words and does not repeat the title.
//
// The size and the byte count are read from the JPEG or PNG header, so the check needs neither a
// browser nor an image library. The headline's height is estimated from the thumb template's
// numbers (tools/video/templates/theme.css) and the renderer's fitting rule
// (tools/video/render/browser.mjs fitText): render does not record the size it settled on, so
// the estimate repeats its greedy shrink on a model of the layout. A test pins the numbers to
// theme.css, so a theme change fails here until they are updated. The same model says where the
// browser breaks the headline's lines, and Intl.Segmenter (zh) says whether a break falls inside
// a word; the writer moves it with a `\n`.
import { HEADLINE_WORD, headlineCount, THUMB_HEADLINE_MAX, THUMB_HEADLINE_WORDS_MAX, THUMB_SERIES, THUMB_SIZE } from "../templates/templates.mjs";

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
 * of two full lines in the channel's column settles at. A CJK glyph 24 px tall on a 320 px wide
 * picture is roughly the height of a phone app's title text, and leaves room for JPEG softness
 * and the smaller tiles of a tablet grid. Revisit after the first hands-off batch if a thumbnail
 * the owner would have accepted fails here.
 */
export const MIN_HEADLINE_PX_AT_PHONE = 24;
// How much of the headline may be found verbatim in the title's first characters before the
// thumbnail is only the title again (docs/videos/channel-review-20261007/README.md D05).
export const TITLE_HEAD_CHARS = 10;
export const TITLE_OVERLAP_MAX = 0.5;

// The channel's thumb template headline, as theme.css sets it (`.thumb h1` and `.thumb.column`):
// the text column is the left 40% of the frame.
export const HEADLINE = {
  fontSize: 136, // .thumb h1 font-size
  lineHeight: 1.1, // .thumb h1 line-height
  maxHeight: 300, // .thumb.column h1 max-height: two lines
  width: THUMB_SIZE.width * 0.4 - 56 - 24, // the column (40%) less .thumb.column's left padding (56) and right padding (24)
  minScale: 0.6, // fitText stops shrinking at 60% of the start size
  step: 2, // fitText shrinks 2 px at a time
  tolerance: 0.4, // fitText counts vertical overflow only past 0.4 em
};
// A series' thumbnail (templates.mjs THUMB_SERIES) keeps the full-width column: `.thumb` less
// its left padding (72) and `.thumb.series`'s right padding (340), three lines high.
export const HEADLINE_SERIES = { ...HEADLINE, maxHeight: 460, width: THUMB_SIZE.width - 72 - 340 };
export const headlineRule = (series = null) => (series && Object.hasOwn(THUMB_SERIES, series) ? HEADLINE_SERIES : HEADLINE);

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

// A run of the headline: a Latin word or number (templates.mjs HEADLINE_WORD, so 「NT$270」 is
// one run and never breaks between the sign and the digits), a run of spaces, or one character.
const HEADLINE_RUN = new RegExp(`${HEADLINE_WORD.source}|\\s+|.`, "gsu");
/**
 * The headline's tokens, each { width in em, breakable?, text }: a CJK glyph may break from its
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
        tokens.push({ width: [...emphasis].reduce((sum, char) => sum + glyphWidth(char), 0), text: emphasis });
        continue;
      }
      for (const run of plain.match(HEADLINE_RUN) ?? []) {
        tokens.push({ width: [...run].reduce((sum, char) => sum + glyphWidth(char), 0), space: /^\s+$/.test(run), text: run });
      }
    }
  });
  return tokens;
}

/**
 * How many lines the headline takes at a font size, whether a token is wider than the box, and
 * where the lines break: `breaks` holds, for every line after the first, the offset into the
 * headline's text (markup removed, a chosen break one space) of the character that starts it,
 * and whether the writer chose it (`chosen`) or the browser wraps there.
 */
export function headlineLayout(tokens, fontSize, width = HEADLINE.width) {
  let lines = 1;
  let used = 0;
  let offset = 0;
  let tooWide = false;
  const breaks = [];
  tokens.forEach((token, index) => {
    if (token === null) {
      // A chosen break between two Latin runs counts one character, the space plainHeadline
      // puts in its place; between CJK glyphs it is nothing, so a word broken in two stays one.
      lines += 1;
      used = 0;
      if (joinsLatin(tokens[index - 1]?.text, tokens[index + 1]?.text)) offset += 1;
      breaks.push({ at: offset, chosen: true });
      return;
    }
    const px = token.width * fontSize;
    if (px > width) tooWide = true;
    if (used > 0 && used + px > width) {
      lines += 1;
      used = token.space ? 0 : px;
      if (!token.space) breaks.push({ at: offset, chosen: false });
    } else {
      used += px;
    }
    offset += [...(token.text ?? "")].length;
  });
  return { lines, tooWide, breaks };
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

// Whether a chosen break sits between two Latin letters or digits, where it must count as a
// space so the segmenter does not read the two runs as one word (「Gem\n11月」 is not Gem11); a
// break between CJK glyphs is nothing, so 「攻\n擊」 is still the word 攻擊.
const LATIN = /[A-Za-z0-9]/;
const joinsLatin = (before, after) => Boolean(before && after && LATIN.test([...before].at(-1)) && LATIN.test([...after][0]));
// The headline as one line of text: markup out, each chosen break a space or nothing (joinsLatin).
const plainHeadline = (headline) => String(headline).replace(/\*\*/g, "").replace(/(.?)\n(.?)/gsu, (_, before, after) => `${before}${joinsLatin(before, after) ? " " : ""}${after}`);
const segmenter = new Intl.Segmenter("zh", { granularity: "word" });

/**
 * The words a line break of the headline falls inside, at the size the renderer settles on:
 * [{ word, chosen }] in text order, each word once. A word is what Intl.Segmenter (zh, word)
 * calls one of two or more characters; a break the writer chose with `\n` counts as much as
 * one the browser makes, so 「一半的攻／擊」 is flagged either way.
 */
export function headlineSplitWords(headline, rule = HEADLINE) {
  const text = plainHeadline(headline);
  const { breaks } = headlineLayout(headlineTokens(headline), headlineSizeEstimate(headline, rule), rule.width);
  if (!breaks.length) return [];
  const words = [];
  let start = 0;
  for (const { segment, isWordLike } of segmenter.segment(text)) {
    const end = start + [...segment].length;
    const inside = breaks.find((line) => line.at > start && line.at < end);
    if (inside && isWordLike && end - start >= 2) words.push({ word: segment, chosen: inside.chosen });
    start = end;
  }
  return words;
}

/** The longest run of characters the headline and the title's first TITLE_HEAD_CHARS share, spaces and markup aside. */
export function titleOverlap(headline, title) {
  const strip = (value) => [...String(value).replace(/\*\*/g, "").replace(/[\s\p{P}\p{S}]/gu, "")];
  const own = strip(headline);
  const head = strip(title).slice(0, TITLE_HEAD_CHARS);
  let best = "";
  for (let i = 0; i < own.length; i++) {
    for (let j = 0; j < head.length; j++) {
      let length = 0;
      while (i + length < own.length && j + length < head.length && own[i + length].toLowerCase() === head[j + length].toLowerCase()) length += 1;
      if (length > best.length) best = own.slice(i, i + length).join("");
    }
  }
  return { shared: best, ratio: own.length ? [...best].length / own.length : 0 };
}

// The locale whose headline the channel's rules are written for (six CJK characters, two Latin
// words, a zh word segmenter): the video's own, zh-TW. A locale's own thumbnail (render's
// thumbnail_locales) is in another language, where those rules say nothing useful (an English
// headline is seldom two words, a Japanese one needs more than six kana, Korean is not segmented
// by a zh segmenter), so it keeps only the size, bytes, phone height and title checks.
export const CHANNEL_RULES_LOCALE = "zh-TW";
/**
 * The thumbnail item's verdict from the file's bytes and the headline video.json asked for:
 * { ok, detail, warnings }. `title` is youtube.title when the caller has it: a headline that is
 * the title's first characters again warns. `series` names a series' own thumbnail
 * (templates.mjs THUMB_SERIES), whose wider column and own headline length apply; without it the
 * channel's rules do: at most six characters, two Latin words, no line break inside a word.
 * `locale` names a locale's own thumbnail (CHANNEL_RULES_LOCALE or null is the video's own).
 */
export function thumbnailChecks({ bytes, headline, title = null, series = null, locale = null }) {
  const problems = [];
  const warnings = [];
  const size = imageSize(bytes);
  if (!size) problems.push("the file is not a JPEG or PNG");
  else if (size.width !== THUMB_SIZE.width || size.height !== THUMB_SIZE.height) problems.push(`${size.width}x${size.height}; YouTube wants ${THUMB_SIZE.width}x${THUMB_SIZE.height}`);
  if (bytes.length > MAX_BYTES) problems.push(`${bytes.length} bytes; YouTube's limit is 2 MB`);
  const rule = headlineRule(series);
  const own = typeof headline === "string" && headline.trim() ? headline : null;
  const headlinePx = own ? atPhoneWidth(headlineSizeEstimate(own, rule)) : null;
  if (headlinePx !== null && headlinePx < MIN_HEADLINE_PX_AT_PHONE) {
    problems.push(`the headline shrinks to about ${headlinePx} px at ${PHONE_WIDTH} px wide; at least ${MIN_HEADLINE_PX_AT_PHONE} px reads on a phone, so shorten it`);
  }
  if (own && rule === HEADLINE && (locale === null || locale === CHANNEL_RULES_LOCALE)) {
    const { count, words } = headlineCount(own);
    if (count > THUMB_HEADLINE_MAX) problems.push(`the headline counts ${count} characters (a Latin word or a number counts one); at most ${THUMB_HEADLINE_MAX} read at a glance, so say one thing in six`);
    if (words.length > THUMB_HEADLINE_WORDS_MAX) problems.push(`the headline has ${words.length} Latin words or numbers (${words.join(", ")}); at most ${THUMB_HEADLINE_WORDS_MAX} fit the column`);
    const split = headlineSplitWords(own, rule);
    if (split.length) problems.push(`a line break falls inside the word ${split.map(({ word }) => `「${word}」`).join(", ")}; put \\n where a word ends`);
  }
  if (own && typeof title === "string" && title.trim()) {
    const { shared, ratio } = titleOverlap(own, title);
    if (ratio > TITLE_OVERLAP_MAX) warnings.push(`the headline repeats the title: 「${shared}」 is in the title's first ${TITLE_HEAD_CHARS} characters; say what the title does not`);
  }
  const kb = Math.round(bytes.length / 1024);
  const described = size ? `${size.width}x${size.height} ${size.format.toUpperCase()}, ${kb} KB` : `${kb} KB`;
  const glyphs = headlinePx === null ? "" : `; the headline is about ${headlinePx} px tall at ${PHONE_WIDTH} px wide`;
  return { ok: problems.length === 0, detail: problems.length ? problems.join("; ") : `${described}${glyphs}`, warnings };
}
