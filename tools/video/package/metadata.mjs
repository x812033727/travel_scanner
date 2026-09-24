// What goes into YouTube's fields, per locale: title, the composed description (body, chapters,
// the Mokaair article, sources) and tags, each checked against YouTube's limits.
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

export function uploadChecklist({ metadata, captions, thumbnail }) {
  const captionLines = captions.length ? captions.map((file) => `   - \`${file}\``).join("\n") : "   - （還沒有字幕檔：先跑 captions）";
  return `# 上傳檢查表：${metadata.title}

這個資料夾就是要上傳的全部內容。公開前的每一步都由站主自己在 YouTube Studio 操作。

## 1. 上傳（Studio → 建立 → 上傳影片）

1. 上傳 \`final.mp4\`。**瀏覽權限先選「私人」**。
2. 標題：\`description.zh-TW.txt\` 的第一行。
3. 說明：\`description.zh-TW.txt\` 第三行以後的全部內容（章節時間戳已經在裡面）。
4. 縮圖：${thumbnail ? "上傳 `thumbnail.jpg`（帳號需完成手機驗證）" : "這次沒有縮圖，Studio 會自動挑一格"}。
5. 目標觀眾：選「否，這不是為兒童打造的內容」${metadata.made_for_kids ? "（注意：video.json 標為兒童內容，請確認）" : ""}。
6. 標籤：貼上 \`metadata.json\` 的 \`tags\`。類別：科學與技術（${metadata.category_id}）。影片語言：中文（台灣）。

## 2. 字幕

${captionLines}

在「字幕」分頁新增語言並上傳對應的檔案；或上傳完成後，把影片 ID 交回，用 \`node tools/video/cli.mjs youtube-sync\` 一次補上字幕與其他語言的標題說明。

## 3. 上架前自我檢查

- [ ] **AI 使用揭露**（Studio「變造或合成內容」）：只有擬真到會被誤認為真人、真實事件或真實場景時才要勾。用一般 TTS 聲音唸投影片，依 YouTube 說明推論不需要；如果用了複製真人（不是自己）的聲音，一定要勾。
- [ ] **非原創內容政策**：這支有站主自己的觀點（brief.md 的「站主觀點」）、至少一段實際示範或實算，而不是套版型念重點。
- [ ] **付費宣傳**：影片裡有業配或聯盟連結就勾選，說明欄也要寫明。
- [ ] 說明欄的連結都點過，文章頁會開。
- [ ] 縮圖縮到手機大小還看得懂。

## 4. 公開

確認都沒問題之後，才把瀏覽權限改成「公開」或設定排程。影片網址交回後會寫進 \`video.json\`。
`;
}
