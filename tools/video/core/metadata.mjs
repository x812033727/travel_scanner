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

// Section labels of the composed description, per locale.
export const LABELS = {
  "zh-TW": { chapters: "章節", article: "完整文章", sources: "參考資料", colon: "：" },
  "zh-CN": { chapters: "章节", article: "完整文章", sources: "参考资料", colon: "：" },
  en: { chapters: "Chapters", article: "Full article", sources: "Sources", colon: ": " },
  ja: { chapters: "チャプター", article: "記事全文", sources: "参考資料", colon: "：" },
  ko: { chapters: "챕터", article: "전체 글", sources: "참고 자료", colon: ": " },
};

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
 * The Mokaair page for a content pack, with the campaign tag that separates video traffic in
 * analytics. Same URL shapes as the recorded route's video_kit.py: life articles under /life,
 * everything else under /guides/<kind>.
 */
export function articleUrl(pack, locale, campaign) {
  if (!pack?.slug) return null;
  const path = pack.kind === "life" ? `/life/${pack.slug}` : `/guides/${pack.kind}/${pack.slug}`;
  return `${SITE}/${locale}${path}?utm_source=youtube&utm_medium=video&utm_campaign=${encodeURIComponent(campaign)}`;
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
 * "more"; then the body, the chapters, the sources, and the hashtags last, the layout the channels
 * we learn from use (2026-09-26, the owner's reference video).
 */
export function composeDescription({ body, timeline, chapterTitles = {}, article, sources = [], locale, tags = [] }) {
  const labels = LABELS[locale] ?? LABELS.en;
  const parts = [];
  if (article) parts.push(`🔗 ${labels.article}${labels.colon}${article}`);
  parts.push(body.trim());
  if (timeline) parts.push(`📌 ${labels.chapters}\n${chapterText(timeline, chapterTitles)}`);
  if (sources.length) parts.push(`📚 ${labels.sources}\n${sources.map((source) => `${source.title}${labels.colon}${source.url}`).join("\n")}`);
  const hashtags = hashtagsFrom(tags);
  if (hashtags.length) parts.push(hashtags.join(" "));
  return parts.join("\n\n");
}
