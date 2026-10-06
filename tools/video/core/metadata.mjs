// Title, description and tags as YouTube will accept them (developers.google.com/youtube/v3/docs/videos).
//
// The description limit is 5,000 bytes, not characters: a Chinese character is three bytes in
// UTF-8, so a zh-TW description holds about 1,666 characters, chapters and links included. The
// check therefore runs on the composed description, not on the body the writer typed.
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

/**
 * Where a content pack's article is read, after the locale: life articles under /life, everything
 * else under /guides/<kind> (the routes in apps/web/app/(ads-public)/[locale]). /guides/<slug> on
 * its own is a kind's list page and answers 404 for an article.
 */
export function articlePath(pack) {
  return pack.kind === "life" ? `/life/${pack.slug}` : `/guides/${pack.kind}/${pack.slug}`;
}

/**
 * The Mokaair page for a content pack, with the campaign tag that separates video traffic in
 * analytics. Same URL shapes as the recorded route's video_kit.py.
 */
export function articleUrl(pack, locale, campaign) {
  if (!pack?.slug) return null;
  return `${SITE}/${locale}${articlePath(pack)}?utm_source=youtube&utm_medium=video&utm_campaign=${encodeURIComponent(campaign)}`;
}

export const HASHTAG_COUNT = 3;

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
 * The description as it is uploaded. The article link goes first, where YouTube shows it before
 * "more"; then the body, the chapters, the sources, the picture credits (`assets`, the stock
 * photos' authors, vendors and licences: never burnt into the video, always here), and the
 * hashtags last, the layout the channels we learn from use (2026-09-26, the owner's reference video).
 */
export function composeDescription({ body, timeline, chapterTitles = {}, article, sources = [], assets = [], locale, tags = [] }) {
  const labels = LABELS[locale] ?? LABELS.en;
  const parts = [];
  if (article) parts.push(`🔗 ${labels.article}${labels.colon}${article}`);
  parts.push(body.trim());
  if (timeline) parts.push(`📌 ${labels.chapters}\n${chapterText(timeline, chapterTitles)}`);
  if (sources.length) parts.push(`📚 ${labels.sources}\n${sources.map((source) => `${source.title}${labels.colon}${source.url}`).join("\n")}`);
  const credits = pictureCredits(assets, locale);
  if (credits) parts.push(credits);
  const hashtags = hashtagsFrom(tags);
  if (hashtags.length) parts.push(hashtags.join(" "));
  return parts.join("\n\n");
}
