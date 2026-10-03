// The channel's Mandarin, as a Gemini voice style says it (docs/videos/README.md §頻道規格).
//
// Gemini has no Taiwan accent to pick (docs/videos/DESIGN.md), so the accent is words in the
// style. Until 2026-10-03 those words were 「台灣國語」 and "a natural Taiwanese accent": in Taiwan
// 「台灣國語」 names the heavy Hokkien-coloured accent, the model played it that way, and the owner
// found the narration too accented. The channel's wording is CHANNEL_ACCENT; channelAccent() puts
// it in place of the retired wording wherever a style still carries it (the settings row, a
// series' setting book, a video.json written before the change), so no stored document has to be
// rewritten and none of their hashes move.

/** What a zh-TW voice style says about the accent: standard, clearly articulated, no persona. */
export const CHANNEL_ACCENT = "標準國語，咬字清楚，台北人平常說話的語調";
/** The same in an English style; reads after "in". */
export const CHANNEL_ACCENT_EN = "standard Mandarin with clear, precise articulation";

// Mirrors STYLE_MAX in drama.mjs and the server's limit on `style`.
const STYLE_MAX = 400;
// The wording, then what is left of it when a style has no room: the last is never longer than
// the wording it replaces, so a style that fitted still fits.
const WORDINGS = [
  { zh: CHANNEL_ACCENT, en: CHANNEL_ACCENT_EN },
  { zh: "標準國語", en: "standard Mandarin" },
  { zh: "國語", en: "Mandarin" },
];

// A style that asks for no accent (「不帶台灣腔」) already says what the channel wants.
const NEGATED = "(?<!(?:不要|不帶|不用|沒有|避免|去掉|別帶)(?:任何|太重的?|明顯的?|很重的?|自然的?)?)";
const RETIRED = new RegExp(
  [
    // 「台灣國語」 alone or with its usual company: 「台灣國語，自然台灣口音」「台灣國語、台灣腔」.
    `${NEGATED}(?:自然的?)?台灣國語(?:[，、,]\\s*(?:自然的?)?台灣(?:口音|腔))?`,
    `${NEGATED}(?:自然的?)?台灣(?:口音|腔)`,
    "(?<en>Taiwan(?:ese)? Mandarin(?:,? with an? (?:natural |light |slight )?Taiwan(?:ese)? accent)?|(?<bare>with an? (?:natural |light |slight )?Taiwan(?:ese)? accent))",
  ].join("|"),
  "giu",
);
const SEPARATOR = /^[，、；;,]\s*/u;
const BOUNDARY = /^[\s，、；。！？,.;:!?）)」』]/u;

function rewrite(style, words) {
  let out = "";
  let last = 0;
  let replaced = false;
  for (const match of style.matchAll(RETIRED)) {
    out += style.slice(last, match.index);
    last = match.index + match[0].length;
    if (replaced) {
      // Said once is enough: a second mention goes, with the separator that followed it.
      last += style.slice(last).match(SEPARATOR)?.[0].length ?? 0;
      continue;
    }
    replaced = true;
    const english = match.groups.en !== undefined;
    // "with a natural Taiwanese accent" on its own keeps its sentence: "in standard Mandarin…".
    out += english ? `${match.groups.bare ? "in " : ""}${words.en}` : words.zh;
    // 「台灣國語說書人」: the accent ends its own sentence instead of running into the next word.
    if (last < style.length && !BOUNDARY.test(style.slice(last))) out += english ? " " : "。";
  }
  return out + style.slice(last);
}

/**
 * A Gemini voice style with the retired accent wording replaced by the channel's, once; a style
 * without it comes back as it is, so a dub's English or Japanese style and a style that never
 * named an accent are untouched. A style within `max` stays within it: the wording shortens
 * before anything else in the style would have to be cut.
 */
export function channelAccent(style, max = STYLE_MAX) {
  if (typeof style !== "string" || !style) return style;
  // search() neither reads nor moves the pattern's lastIndex, which matchAll() starts from.
  if (style.search(RETIRED) === -1) return style;
  const room = Math.max(max, style.length);
  let rewritten = style;
  for (const words of WORDINGS) {
    rewritten = rewrite(style, words).trim();
    if (rewritten.length <= room) break;
  }
  return rewritten;
}
