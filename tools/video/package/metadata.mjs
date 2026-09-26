// What goes into YouTube's fields, per locale: title, the composed description (the Mokaair
// article, body, chapters, sources, hashtags) and tags, each checked against YouTube's limits.
import { articleUrl, checkYoutubeFields, composeDescription, tagsLength, TAGS_MAX_CHARS } from "../core/metadata.mjs";
import { NARRATION_LOCALE } from "../core/schema.mjs";
import { chapterList, formatClock } from "../core/timeline.mjs";

/**
 * Metadata for zh-TW and every locale with a translation file. A locale's translation supplies
 * { title, description, tags?, chapters?: { sceneId: title } }; the article link uses that
 * locale when the source article has it, zh-TW otherwise.
 */
export function composeMetadata({ doc, timeline, translations = {}, pack = null }) {
  const locales = [NARRATION_LOCALE, ...Object.keys(translations).filter((locale) => translations[locale]?.title && translations[locale]?.description)];
  const problems = [];
  const perLocale = {};
  for (const locale of locales) {
    const translation = locale === NARRATION_LOCALE ? null : translations[locale];
    const title = translation ? translation.title : doc.youtube.title;
    const body = translation ? translation.description : doc.youtube.description;
    const articleLocale = pack?.locales?.[locale] ? locale : NARRATION_LOCALE;
    const description = composeDescription({
      body,
      timeline,
      chapterTitles: translation?.chapters ?? {},
      article: pack ? articleUrl(pack, articleLocale, doc.slug) : null,
      sources: doc.sources ?? [],
      locale,
      tags: translation?.tags?.length ? translation.tags : doc.youtube.tags,
    });
    problems.push(...checkYoutubeFields({ title, description, tags: [] }, `${locale}`));
    perLocale[locale] = { title, description };
  }
  // Tags are one list per video, not per locale: the zh-TW ones first, then translated ones.
  const tags = [];
  for (const tag of [...doc.youtube.tags, ...locales.flatMap((locale) => translations[locale]?.tags ?? [])]) {
    if (!tags.includes(tag) && tagsLength([...tags, tag]) <= TAGS_MAX_CHARS) tags.push(tag);
  }
  const chapters = chapterList(timeline).map((chapter) => ({ at: formatClock(chapter.start), title: chapter.title }));
  return {
    problems,
    metadata: {
      slug: doc.slug,
      default_language: NARRATION_LOCALE,
      category_id: doc.youtube.category_id,
      made_for_kids: doc.youtube.made_for_kids,
      privacy_status: "private",
      title: perLocale[NARRATION_LOCALE].title,
      description: perLocale[NARRATION_LOCALE].description,
      tags,
      localizations: Object.fromEntries(Object.entries(perLocale).filter(([locale]) => locale !== NARRATION_LOCALE)),
      chapters,
    },
  };
}

/**
 * UPLOAD.md: only the operating steps in YouTube Studio. The checks that used to be a list here
 * (facts, links, thumbnail legibility, the owner's viewpoint, the disclosure) are the automatic
 * quality check and the package check now (docs/videos/HANDS-OFF.md); the disclosure answer is
 * in metadata.json and this page only says how to tick it.
 */
export function uploadChecklist({ metadata, captions, thumbnail, drama = false, disclosure = null }) {
  const captionLines = captions.length ? captions.map((file) => `   - \`${file}\``).join("\n") : "   - （還沒有字幕檔：先跑 captions）";
  const synthetic = typeof disclosure?.synthetic === "boolean" ? disclosure.synthetic : typeof metadata.contains_synthetic_media === "boolean" ? metadata.contains_synthetic_media : drama;
  const reason = disclosure?.reason ?? metadata.disclosure_reason ?? (drama ? "AI-generated shots and voices" : "slides read by a synthesized narration");
  return `# 上傳步驟：${metadata.title}

這個資料夾就是要上傳的全部內容。自動品管與上傳包檢查已經做過；這裡只剩站主自己在 YouTube Studio 的操作，公開的時間也由站主決定。

## 1. 上傳（Studio → 建立 → 上傳影片）

1. 上傳 \`final.mp4\`。**瀏覽權限先選「私人」**。
2. 標題：\`description.zh-TW.txt\` 的第一行。
3. 說明：\`description.zh-TW.txt\` 第三行以後的全部內容（章節時間戳已經在裡面）。
4. 縮圖：${thumbnail ? "上傳 `thumbnail.jpg`（帳號需完成手機驗證）" : "這次沒有縮圖，Studio 會自動挑一格"}。
5. 目標觀眾：選「否，這不是為兒童打造的內容」${metadata.made_for_kids ? "（注意：video.json 標為兒童內容，請確認）" : ""}。
6. 標籤：貼上 \`metadata.json\` 的 \`tags\`。類別：科學與技術（${metadata.category_id}）。影片語言：中文（台灣）。
7. 「變造或合成內容」：${synthetic ? "勾「是」" : "不用勾"}。\`metadata.json\` 的 \`contains_synthetic_media\` 是 \`${synthetic}\`（${reason}）。

## 2. 字幕

${captionLines}

在「字幕」分頁新增語言並上傳對應的檔案；其他語系的標題與說明在 \`description.<語系>.txt\`。

## 3. 上傳之後

回到 /admin/videos 這支影片的「可以上架」卡片貼上 YouTube 網址，並選上架時間；影片 ID 會寫進 \`video.json\`，影片就算完成。不要自己按公開：公開由站主選的時間決定。
`;
}
