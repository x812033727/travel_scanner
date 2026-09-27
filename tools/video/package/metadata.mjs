// What goes into YouTube's fields, per locale: title, the composed description (the Mokaair
// article, body, chapters, sources, hashtags) and tags, each checked against YouTube's limits.
import { articleUrl, checkYoutubeFields, composeDescription, tagsLength, TAGS_MAX_CHARS } from "../core/metadata.mjs";
import { NARRATION_LOCALE } from "../core/schema.mjs";
import { chapterList, formatClock } from "../core/timeline.mjs";

/**
 * Metadata for zh-TW and the localized locales: the ones the owner chose titles and descriptions
 * for (`locales`, docs/videos/LANGUAGES.md), else every locale with a translation file. A chosen
 * locale whose title or description is not translated yet is a problem. A locale's translation
 * supplies { title, description, tags?, chapters?: { sceneId: title } }; the article link uses
 * that locale when the source article has it, zh-TW otherwise.
 */
export function composeMetadata({ doc, timeline, translations = {}, pack = null, locales: wanted = null }) {
  const translated = (locale) => Boolean(translations[locale]?.title && translations[locale]?.description);
  const asked = wanted ?? Object.keys(translations).filter(translated);
  const problems = asked.filter((locale) => locale !== NARRATION_LOCALE && !translated(locale)).map((locale) => `${locale}: the title and description are not translated yet (i18n-sheet --locale ${locale} --parts metadata, then i18n-merge)`);
  const locales = [NARRATION_LOCALE, ...asked.filter((locale) => locale !== NARRATION_LOCALE && translated(locale))];
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
 * The Studio steps for the dub tracks (docs/videos/DUBS.md), or where to ask for some. Tracks
 * can be added before or after the video is public; YouTube's own auto dub of a language has to
 * be deleted before the owner's track for it goes up.
 */
export function dubSteps(dubs = [], skippedDubs = {}) {
  const lines = [];
  if (dubs.length) {
    lines.push("要上傳的音軌：", "");
    for (const dub of dubs) lines.push(`- \`${dub.file}\`（${dub.locale}${dub.tempo_max > 1 ? `，最快處 ${dub.tempo_max} 倍速` : ""}）`);
    lines.push(
      "",
      "每個語系做一次：Studio 左選單「語言」→ 這支影片 →「新增語言」→ 選語言 →「配音」旁的「新增」→「選取檔案」→ 選對應的檔案 →「發布」。上架前或上架後都可以加。",
      "",
      "- 頻道要有「進階功能」（設定 → 頻道 → 功能使用資格）。",
      "- YouTube 已經替這個語言自動配音的話，要先在同一頁刪掉自動配音，才傳得上去；建議在設定 → 頻道 → 進階設定取消「允許自動配音」。",
      "- 傳完到影片頁的「語言」卡片按「已在 Studio 上傳配音」；標題說明與字幕由網站的 API 送上，不用手動。",
    );
  } else {
    lines.push("這支沒有配音音軌。要加，在 `/admin/videos` 這支影片的頁面勾那個語言的「配音」，工人做好會再送一張「語言」卡片。");
  }
  const skipped = Object.entries(skippedDubs);
  if (skipped.length) {
    lines.push("", "做不出來的語系（不用等）：");
    for (const [locale, reason] of skipped) lines.push(`- ${locale}：${reason || "沒有寫原因"}`);
  }
  return lines.join("\n");
}

/**
 * UPLOAD.md: only the operating steps in YouTube Studio. The checks that used to be a list here
 * (facts, links, thumbnail legibility, the owner's viewpoint, the disclosure) are the automatic
 * quality check and the package check now (docs/videos/HANDS-OFF.md); the disclosure answer is
 * in metadata.json and this page only says how to tick it. The dub tracks (docs/videos/DUBS.md)
 * keep their own section: which file goes where in Studio's 「語言」.
 */
export function uploadChecklist({ metadata, captions, thumbnail, drama = false, disclosure = null, dubs = [], skippedDubs = {} }) {
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

## 3. 配音音軌（多語言音訊）

${dubSteps(dubs, skippedDubs)}

## 4. 上傳之後

回到 /admin/videos 這支影片的「可以上架」卡片貼上 YouTube 網址，並選上架時間；影片 ID 會寫進 \`video.json\`，影片就算完成。不要自己按公開：公開由站主選的時間決定。
`;
}
