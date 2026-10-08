// Title, description and tags as YouTube will accept them (developers.google.com/youtube/v3/docs/videos).
//
// The description limit is 5,000 bytes, not characters: a Chinese character is three bytes in
// UTF-8, so a zh-TW description holds about 1,666 characters, chapters and links included. The
// check therefore runs on the composed description, not on the body the writer typed.
//
// Beside YouTube's hard limits (errors, checkYoutubeFields) the channel review of 2026-10-07
// (docs/videos/channel-review-20261007/README.md §2.2 D06, D13; DECISIONS.md 2026-10-08) left the
// channel's own rules, all of them warnings (youtubeWarnings): a title at most TITLE_WARN_WIDTH
// full-width characters wide with the series name as a suffix and no episode number, and a
// description that opens on the hook, names its audience, links the article once with UTM and
// closes on the series hashtag.
import { chapterText } from "./timeline.mjs";

export const SITE = "https://mokaair.com";
export const TITLE_MAX_CHARS = 100;
export const DESCRIPTION_MAX_BYTES = 5000;
export const TAGS_MAX_CHARS = 500;

// Section labels of the composed description, per locale; `parens` wrap a picture's licence.
export const LABELS = {
  "zh-TW": { chapters: "章節", article: "完整文章", sources: "參考資料", pictures: "圖片來源", colon: "：", parens: ["（", "）"] },
  "zh-CN": { chapters: "章节", article: "完整文章", sources: "参考资料", pictures: "图片来源", colon: "：", parens: ["（", "）"] },
  en: { chapters: "Chapters", article: "Full article", sources: "Sources", pictures: "Image credits", colon: ": ", parens: [" (", ")"] },
  ja: { chapters: "チャプター", article: "記事全文", sources: "参考資料", pictures: "画像の出典", colon: "：", parens: ["（", "）"] },
  ko: { chapters: "챕터", article: "전체 글", sources: "참고 자료", pictures: "이미지 출처", colon: ": ", parens: [" (", ")"] },
};

/**
 * One entry of video.json's assets[]: the three fields the schema requires (path, source,
 * license) and the two `stock fetch` adds (tools/video/media/stock.mjs). `source` is the credit
 * line as the vendor words it ("Photo by … on Pexels", "Image by … from Pixabay"), `author` the
 * photographer's name alone, `url` the photo's own page, which a credit links back to.
 */
export const ASSET_FIELDS = ["path", "source", "license", "author", "url"];

/**
 * The assets the description credits: those that name an author or link to a page, which is
 * what a stock photo's entry carries. Mokaair's own diagrams, listed with a source and licence
 * alone, need no credit line, so the descriptions of the videos that list them do not move.
 * One entry per path, in assets[] order.
 */
export function creditedAssets(assets = []) {
  const seen = new Set();
  const credited = [];
  for (const asset of Array.isArray(assets) ? assets : []) {
    if (!asset || typeof asset !== "object" || typeof asset.source !== "string" || !(asset.author || asset.url)) continue;
    if (seen.has(asset.path)) continue;
    seen.add(asset.path);
    credited.push(asset);
  }
  return credited;
}

/** One picture's line: the vendor's credit, the licence in parentheses, then the photo's page. */
export function creditLine(asset, locale) {
  const labels = LABELS[locale] ?? LABELS.en;
  const [open, close] = labels.parens;
  const licence = typeof asset.license === "string" && asset.license.trim() ? `${open}${asset.license.trim()}${close}` : "";
  const head = `${asset.source.trim()}${licence}`;
  return asset.url ? `${head}${labels.colon}${asset.url}` : head;
}

/** The 「圖片來源」 section of the description (docs/videos/ILLUSTRATED.md §圖庫照片), or "" when nothing is credited. */
export function pictureCredits(assets, locale) {
  const credited = creditedAssets(assets);
  if (!credited.length) return "";
  const labels = LABELS[locale] ?? LABELS.en;
  return `📷 ${labels.pictures}\n${credited.map((asset) => creditLine(asset, locale)).join("\n")}`;
}

/** What the credits add to the composed description, in bytes: lint composes without them, package with. */
export function creditBytes(assets, locale) {
  const credits = pictureCredits(assets, locale);
  return credits ? Buffer.byteLength(`\n\n${credits}`, "utf8") : 0;
}

const characters = (text) => [...text].length;

/** How YouTube counts the tag limit: commas between tags count, and a tag with a space is quoted. */
export function tagsLength(tags) {
  return tags.reduce((sum, tag) => sum + characters(tag) + (/\s/.test(tag) ? 2 : 0), 0) + Math.max(0, tags.length - 1);
}

export function checkYoutubeFields({ title, description, tags }, where = "youtube") {
  const problems = [];
  if (characters(title) > TITLE_MAX_CHARS) problems.push(`${where}.title: ${characters(title)} characters, at most ${TITLE_MAX_CHARS}`);
  if (/[<>]/.test(title)) problems.push(`${where}.title: YouTube rejects < and >`);
  const bytes = Buffer.byteLength(description, "utf8");
  if (bytes > DESCRIPTION_MAX_BYTES) problems.push(`${where}.description: ${bytes} bytes once composed, at most ${DESCRIPTION_MAX_BYTES}`);
  if (/[<>]/.test(description)) problems.push(`${where}.description: YouTube rejects < and >`);
  if (tagsLength(tags) > TAGS_MAX_CHARS) problems.push(`${where}.tags: ${tagsLength(tags)} characters counted YouTube's way, at most ${TAGS_MAX_CHARS}`);
  return problems;
}

// The title rules (D06; DECISIONS.md: the series name is a suffix, episodes are not numbered).
// The phone list cuts a title after about 40 full-width characters and nobody has measured
// where exactly, so 36 is the conservative width; the suffix counts, since the phone shows it.
export const TITLE_WARN_WIDTH = 36;
export const TITLE_QUESTION_MARKS = 1;
export const TITLE_LIST_ITEMS = 3;
// The media-literacy sentence shapes six of the first eighteen titles shared and no reference
// channel's title did (D06). A hit is a warning for the writer, never an error.
export const TITLE_BANNED = ["是誰說的", "是誰測的", "怎麼讀", "怎麼看", "先分清", "先問"];
// The series suffix the owner chose over a number: 「…｜AI 名詞十分鐘」.
export const SERIES_SEPARATOR = "｜";
const EPISODE_NUMBER = /第\s*[0-9０-９一二三四五六七八九十百零〇]+\s*集|\bEP\.?\s*[0-9]+|#[0-9]+/iu;
// East Asian wide and full-width code points (CJK, kana, hangul, full-width forms, emoji) take a
// full cell of the list; everything else, Latin letters, digits and spaces, about half of one.
const WIDE = /[ᄀ-ᅟ⺀-꓏가-힣豈-﫿︰-﹏＀-｠￠-￦\u{1F000}-\u{1FAFF}\u{20000}-\u{3FFFD}]/u;

/** A title's width in full-width characters: CJK and other wide characters 1, ASCII 0.5. */
export function titleWidth(text) {
  let width = 0;
  for (const character of String(text ?? "")) width += WIDE.test(character) ? 1 : 0.5;
  return width;
}

// How many tags the upload keeps (uploadTags): the zh-TW terms and the English product names
// video.json lists first; the translated locales' tags stay with their translations.
export const TAGS_MAX_COUNT = 10;

/**
 * The channel's own rules on the YouTube fields, as warnings in checkYoutubeFields' shape
 * (`<where>.title: …`), for lint to report beside the errors. `numbered` allows an episode
 * number in the title (a drama series counts its episodes; the narrated series do not).
 */
export function youtubeWarnings({ title = "", tags = [] }, where = "youtube", { numbered = false } = {}) {
  const warnings = [];
  const width = titleWidth(title);
  if (width > TITLE_WARN_WIDTH) warnings.push(`${where}.title: ${width} full-width characters wide (CJK 1, ASCII 0.5; the ${SERIES_SEPARATOR}series suffix counts), at most ${TITLE_WARN_WIDTH} before the phone list cuts it`);
  const questions = (title.match(/[？?]/g) ?? []).length;
  if (questions > TITLE_QUESTION_MARKS) warnings.push(`${where}.title: ${questions} question marks; ask at most ${TITLE_QUESTION_MARKS} question and answer it in the video`);
  const banned = TITLE_BANNED.filter((phrase) => title.includes(phrase));
  if (banned.length) warnings.push(`${where}.title: 「${banned.join("」「")}」 is the media-literacy shape no reference channel titles with; name the product and the number instead`);
  const listed = (title.match(/、/g) ?? []).length + 1;
  if (listed >= TITLE_LIST_ITEMS) warnings.push(`${where}.title: lists ${listed} items with 、; a title carries one subject, the list goes in the description`);
  const episode = EPISODE_NUMBER.exec(title);
  if (episode && !numbered) warnings.push(`${where}.title: 「${episode[0]}」 numbers the episode; the series is named as a suffix (${SERIES_SEPARATOR}series name) and not counted`);
  if (Array.isArray(tags) && tags.length > TAGS_MAX_COUNT) warnings.push(`${where}.tags: ${tags.length} tags; package keeps the first ${TAGS_MAX_COUNT}, so put the zh-TW terms and the English product names first`);
  return warnings;
}

/** The tags the upload carries: video.json's order, repeats dropped, the first TAGS_MAX_COUNT within YouTube's length. */
export function uploadTags(tags = []) {
  const kept = [];
  for (const tag of tags) {
    if (kept.length === TAGS_MAX_COUNT) break;
    if (!kept.includes(tag) && tagsLength([...kept, tag]) <= TAGS_MAX_CHARS) kept.push(tag);
  }
  return kept;
}

/**
 * Where a content pack's article is read, after the locale: life articles under /life, everything
 * else under /guides/<kind> (the routes in apps/web/app/(ads-public)/[locale]). /guides/<slug> on
 * its own is a kind's list page and answers 404 for an article.
 */
export function articlePath(pack) {
  return pack.kind === "life" ? `/life/${pack.slug}` : `/guides/${pack.kind}/${pack.slug}`;
}

/** The campaign tag that separates video traffic in analytics; the campaign is the video's slug. */
export function utmQuery(campaign) {
  return `utm_source=youtube&utm_medium=video${campaign ? `&utm_campaign=${encodeURIComponent(campaign)}` : ""}`;
}

/**
 * The Mokaair page for a content pack, with the campaign tag that separates video traffic in
 * analytics. Same URL shapes as the recorded route's video_kit.py.
 */
export function articleUrl(pack, locale, campaign) {
  if (!pack?.slug) return null;
  return `${SITE}/${locale}${articlePath(pack)}?${utmQuery(campaign)}`;
}

// A Mokaair link as it appears in prose: the URL ends at whitespace or at the punctuation
// (ASCII and full-width) that closes a sentence or a bracket around it, as qa/links.mjs reads it.
const MOKAAIR_LINK = /https?:\/\/(?:www\.)?mokaair\.com[^\s｜|<>"'）)\]，。、；：！？「」『』】〉》]*/g;
const TRAILING_PUNCTUATION = /[.,;:!?]+$/;

/** A URL with the video's UTM tags when it is a Mokaair page without any; any other URL as it is. */
export function withUtm(url, campaign) {
  let host;
  try {
    host = new URL(url).hostname.toLowerCase();
  } catch {
    return url;
  }
  if (host !== "mokaair.com" && host !== "www.mokaair.com") return url;
  if (/[?&]utm_source=/.test(url)) return url;
  const [base, hash] = url.split("#");
  return `${base}${base.includes("?") ? "&" : "?"}${utmQuery(campaign)}${hash === undefined ? "" : `#${hash}`}`;
}

/** Every Mokaair link in a text tagged with the video's UTM (withUtm); the sentence's own punctuation stays outside the URL. */
export function tagMokaairLinks(text, campaign) {
  return String(text ?? "").replace(MOKAAIR_LINK, (url) => {
    const trailing = TRAILING_PUNCTUATION.exec(url)?.[0] ?? "";
    return `${withUtm(url.slice(0, url.length - trailing.length), campaign)}${trailing}`;
  });
}

const UTM_PARAM = /^utm_/i;

/**
 * What makes two links the same page: scheme, host, path and query, without the UTM parameters,
 * the fragment or a trailing slash. The rest of the query stays, since many sites page by it
 * alone (ntm.gov.tw/cp.aspx?n=5444 and ?n=5445 are two pages); only the tags this tool adds
 * (utm_*) say nothing about which page it is.
 */
export function urlKey(url) {
  try {
    const parsed = new URL(url);
    for (const name of [...parsed.searchParams.keys()]) if (UTM_PARAM.test(name)) parsed.searchParams.delete(name);
    const query = parsed.searchParams.toString();
    return `${parsed.protocol}//${parsed.hostname.toLowerCase()}${parsed.pathname.replace(/\/+$/, "")}${query ? `?${query}` : ""}`;
  } catch {
    const [path, query = ""] = String(url).replace(/#.*$/, "").split("?");
    const kept = query.split("&").filter((pair) => pair && !UTM_PARAM.test(pair));
    return `${path.replace(/\/+$/, "")}${kept.length ? `?${kept.join("&")}` : ""}`;
  }
}

const ANY_LINK = /https?:\/\/[^\s｜|<>"'）)\]，。、；：！？「」『』】〉》]+/g;
// A line that is only a link, with at most a short label before it (「完整文章：https://…」, 「🔗 https://…」).
const LABEL_ONLY = /^[^\p{L}\p{N}]*(?:[\p{L}\p{N}\s]{0,16}[：:]\s*)?[^\p{L}\p{N}]*$/u;

/**
 * The body without the lines that only repeat a link the description carries elsewhere: the
 * article's own line (composeDescription adds it after the body) and a bare link to a page
 * another line of the body links too, before or after it. Fifteen of the first eighteen
 * descriptions opened on a bare URL and three showed the same URL three times (D13). Returns
 * { body, mentioned }: `mentioned` says the article is still linked inside a sentence, so the
 * article line would be its second appearance.
 */
export function dedupeLinks(body, article = null) {
  const articleKey = article ? urlKey(article) : null;
  const lines = String(body ?? "").split(/\r?\n/).map((line) => {
    const links = line.match(ANY_LINK) ?? [];
    const keys = links.map((link) => urlKey(link.replace(TRAILING_PUNCTUATION, "")));
    return { line, keys, bare: keys.length > 0 && LABEL_ONLY.test(line.replace(ANY_LINK, "")) };
  });
  const kept = new Set();
  let mentioned = false;
  const out = [];
  lines.forEach((entry, index) => {
    // A page is linked elsewhere when the article is it, a kept line links it, or a sentence
    // below does; of two bare lines to one page the first, with its label, is the one kept.
    const elsewhere = (key) => key === articleKey || kept.has(key) || lines.slice(index + 1).some((later) => !later.bare && later.keys.includes(key));
    if (entry.bare && entry.keys.every(elsewhere)) return;
    if (articleKey && entry.keys.includes(articleKey)) mentioned = true;
    for (const key of entry.keys) kept.add(key);
    out.push(entry.line);
  });
  return { body: out.join("\n").replace(/^\n+/, "").replace(/\n{3,}/g, "\n\n").trim(), mentioned };
}

// Where the first sentence ends: a CJK terminator, or a Latin one followed by a space or the end
// (so "2.5%" and "Omni 1.1" stay whole), and the quote or bracket that closes it.
const SENTENCE_END = /[。！？]|[.!?](?=\s|$)/u;
const CLOSERS = /^[」』）)\]"']/u;

/** A paragraph's first sentence and the rest of it: ["Token 是什麼？", "這集回答…"]. */
export function splitFirstSentence(text) {
  const match = SENTENCE_END.exec(text);
  if (!match) return [text.trim(), ""];
  let end = match.index + match[0].length;
  while (end < text.length && CLOSERS.test(text[end])) end += 1;
  return [text.slice(0, end).trim(), text.slice(end).trim()];
}

/**
 * The body's three parts in the order the description shows them (D13; publish.md §說明欄):
 * line 1 the hook, the body's first sentence; line 2 who the video is for, the body's second
 * line (the writer's 「給…的人」); from line 3 the rest, the remainder of the first paragraph
 * first, then the paragraphs that follow, as the writer broke them.
 */
export function bodyLayout(body) {
  const text = String(body ?? "").trim();
  if (!text) return { hook: "", audience: "", rest: "" };
  const lines = text.split(/\r?\n/);
  const first = lines.findIndex((line) => line.trim());
  const [hook, leftover] = splitFirstSentence(lines[first]);
  let next = lines.findIndex((line, index) => index > first && line.trim());
  let audience = "";
  let rest;
  if (next === -1) {
    audience = leftover;
    rest = "";
  } else {
    audience = lines[next].trim();
    rest = lines.slice(next + 1).join("\n").trim();
    if (leftover) rest = rest ? `${leftover}\n\n${rest}` : leftover;
  }
  return { hook, audience, rest };
}

export const HASHTAG_COUNT = 3;
// The series hashtag that closes a description (D13: the first eighteen carried topic words only
// and no series), by the video's category (schema.mjs VIDEO_CATEGORIES) or its series slug. A
// category without a row gets no series hashtag.
export const SERIES_HASHTAGS = {
  "ai-terms": "#AI名詞十分鐘",
  tutorial: "#AI工具教學",
  "ai-news": "#AI新聞拆解",
};

/** The series hashtag for a video: its series' slug first (a drama), then its category; null without a row. */
export function seriesHashtag({ category = null, series = null } = {}) {
  const slug = typeof series === "string" ? series : series?.slug;
  return (slug && SERIES_HASHTAGS[slug]) ?? (category && SERIES_HASHTAGS[category]) ?? null;
}

/**
 * Hashtags from the first tags: YouTube shows the description's first three above the title.
 * A hashtag cannot hold spaces or punctuation, so "ChatGPT Go" becomes #ChatGPTGo.
 */
export function hashtagsFrom(tags = [], count = HASHTAG_COUNT) {
  const hashtags = [];
  for (const tag of tags) {
    const word = String(tag).replace(/[^\p{L}\p{N}_]/gu, "");
    // YouTube treats #ChatGPTGo and #chatgptgo as one hashtag.
    if (word && !hashtags.some((hashtag) => hashtag.toLowerCase() === `#${word}`.toLowerCase())) hashtags.push(`#${word}`);
    if (hashtags.length === count) break;
  }
  return hashtags;
}

/**
 * The description's last line: two topic hashtags from the first tags, then the series hashtag
 * (seriesHashtag) as the third. Without a series row there are two; a tag that already spells
 * the series does not take a topic slot.
 */
export function descriptionHashtags({ tags = [], category = null, series = null } = {}) {
  const suffix = seriesHashtag({ category, series });
  const topics = hashtagsFrom(tags, HASHTAG_COUNT).filter((hashtag) => hashtag.toLowerCase() !== suffix?.toLowerCase()).slice(0, HASHTAG_COUNT - 1);
  return suffix ? [...topics, suffix] : topics;
}

/** The campaign a composed article link carries, for the body's other Mokaair links. */
function campaignOf(article) {
  try {
    return article ? new URL(article).searchParams.get("utm_campaign") : null;
  } catch {
    return null;
  }
}

/**
 * The sources the 📚 section lists: those whose page the description does not link already,
 * as the article (a pack's sources end on the article itself: ai-term-embedding) or inside
 * the body, and each page once. `linked` holds the urlKey of every page linked above.
 */
export function unlinkedSources(sources = [], linked = new Set()) {
  const seen = new Set(linked);
  const kept = [];
  for (const source of sources) {
    const key = urlKey(source.url);
    if (seen.has(key)) continue;
    seen.add(key);
    kept.push(source);
  }
  return kept;
}

/**
 * The description as it is uploaded (DECISIONS.md 2026-10-08; publish.md §說明欄): the hook, who
 * it is for, the rest of the body (bodyLayout); then the article link, once (dedupeLinks), where
 * the body's links are tagged with the video's UTM (tagMokaairLinks); the chapters, the sources
 * not linked above (unlinkedSources), the picture credits (`assets`, the stock photos' authors,
 * vendors and licences: never burnt into the video, always here) and last the hashtags, two
 * topic words and the series (descriptionHashtags). `campaign` is the video's slug; without it
 * the article link's is used.
 */
export function composeDescription({ body, timeline, chapterTitles = {}, article, sources = [], assets = [], locale, tags = [], category = null, series = null, campaign = null }) {
  const labels = LABELS[locale] ?? LABELS.en;
  const utm = campaign ?? campaignOf(article);
  const parts = [];
  const deduped = dedupeLinks(body, article);
  const { hook, audience, rest } = bodyLayout(deduped.body);
  const head = [hook, audience].filter(Boolean).join("\n");
  parts.push(tagMokaairLinks(rest ? `${head}\n\n${rest}` : head, utm));
  if (article && !deduped.mentioned) parts.push(`🔗 ${labels.article}${labels.colon}${article}`);
  if (timeline) parts.push(`📌 ${labels.chapters}\n${chapterText(timeline, chapterTitles)}`);
  // A page the body or the article line links is not listed again (one page, one link).
  const linked = new Set([...(article ? [article] : []), ...(deduped.body.match(ANY_LINK) ?? [])].map((link) => urlKey(link.replace(TRAILING_PUNCTUATION, ""))));
  const listed = unlinkedSources(sources, linked);
  if (listed.length) parts.push(`📚 ${labels.sources}\n${listed.map((source) => `${source.title}${labels.colon}${tagMokaairLinks(source.url, utm)}`).join("\n")}`);
  const credits = pictureCredits(assets, locale);
  if (credits) parts.push(credits);
  const hashtags = descriptionHashtags({ tags, category, series });
  if (hashtags.length) parts.push(hashtags.join(" "));
  return parts.join("\n\n");
}
