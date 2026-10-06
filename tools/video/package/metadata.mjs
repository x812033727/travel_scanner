// What goes into YouTube's fields, per locale: title, the composed description (the Mokaair
// article, body, chapters, sources, picture credits, hashtags) and tags, each checked against
// YouTube's limits.
import { chapterTitle, descriptionWithinBudget, episodeNumbers, isCompilation } from "../core/compilation.mjs";
import { articleUrl, checkYoutubeFields, composeDescription, creditBytes, LABELS, tagsLength, TAGS_MAX_CHARS } from "../core/metadata.mjs";
import { narrationLocale } from "../core/schema.mjs";
import { chapterList, formatClock } from "../core/timeline.mjs";

/** Current names on the measured timeline: title-only edits need not re-encode a cardless cut. */
export function compilationChapterTitles(doc) {
  const numbers = episodeNumbers(doc.compilation);
  return Object.fromEntries(doc.compilation.episodes.map((slug, index) => [slug, chapterTitle(numbers[index], doc.compilation.titles?.[slug])]));
}

/**
 * Lint composes the description without the picture credits (lint.mjs reads no assets), so a
 * description that passed lint and passes the byte limit only here says what tipped it over.
 */
function withCreditHint(problem, assets, locale) {
  const bytes = creditBytes(assets, locale);
  if (!bytes || !/bytes once composed/.test(problem)) return problem;
  const label = (LABELS[locale] ?? LABELS.en).pictures;
  return `${problem} (the ${label} credits of assets[] add ${bytes} bytes that lint does not count: shorten youtube.description or use fewer stock photos)`;
}

/**
 * Metadata for the narration locale and the localized locales: the ones the owner chose titles
 * and descriptions for (`locales`, docs/videos/LANGUAGES.md), else every locale with a
 * translation file. A chosen locale whose title or description is not translated yet is a
 * problem. A locale's translation supplies { title, description, tags?, chapters?: { sceneId:
 * title } }; the article link uses that locale when the source article has it, the narration
 * locale otherwise. Every locale's description credits the stock photos in assets[] (docs/videos/
 * ILLUSTRATED.md §圖庫照片). A compilation's chapters key on its episode slugs, and when every
 * title would pass YouTube's description limit they fall back to 「第 N 集」 (docs/videos/BINGE.md),
 * in the chapter list the upload card shows as well.
 */
export function composeMetadata({ doc, timeline, translations = {}, pack = null, locales: wanted = null }) {
  const narration = narrationLocale(doc);
  const translated = (locale) => Boolean(translations[locale]?.title && translations[locale]?.description);
  const asked = wanted ?? Object.keys(translations).filter(translated);
  const problems = asked.filter((locale) => locale !== narration && !translated(locale)).map((locale) => `${locale}: the title and description are not translated yet (i18n-sheet --locale ${locale} --parts metadata, then i18n-merge)`);
  const locales = [narration, ...asked.filter((locale) => locale !== narration && translated(locale))];
  const compilation = isCompilation(doc);
  const perLocale = {};
  let zhChapters = {};
  for (const locale of locales) {
    const translation = locale === narration ? null : translations[locale];
    const title = translation ? translation.title : doc.youtube.title;
    const body = translation ? translation.description : doc.youtube.description;
    const articleLocale = pack?.locales?.[locale] ? locale : narration;
    const fields = {
      body,
      timeline,
      chapterTitles: compilation ? { ...compilationChapterTitles(doc), ...(translation?.chapters ?? {}) } : translation?.chapters ?? {},
      article: pack ? articleUrl(pack, articleLocale, doc.slug) : null,
      sources: doc.sources ?? [],
      assets: doc.assets ?? [],
      locale,
      tags: translation?.tags?.length ? translation.tags : doc.youtube.tags,
    };
    let description;
    if (compilation) {
      const budget = descriptionWithinBudget(body, timeline, fields.chapterTitles, { locale, sources: fields.sources, tags: fields.tags, article: fields.article });
      description = budget.description;
      if (locale === narration) zhChapters = budget.titles;
    } else description = composeDescription(fields);
    problems.push(...checkYoutubeFields({ title, description, tags: [] }, `${locale}`).map((problem) => withCreditHint(problem, fields.assets, locale)));
    perLocale[locale] = { title, description };
  }
  // Tags are one list per video, not per locale: the narration's first, then translated ones.
  const tags = [];
  for (const tag of [...doc.youtube.tags, ...locales.flatMap((locale) => translations[locale]?.tags ?? [])]) {
    if (!tags.includes(tag) && tagsLength([...tags, tag]) <= TAGS_MAX_CHARS) tags.push(tag);
  }
  const chapters = chapterList(timeline, zhChapters).map((chapter) => ({ at: formatClock(chapter.start), title: chapter.title }));
  return {
    problems,
    metadata: {
      slug: doc.slug,
      default_language: narration,
      category_id: doc.youtube.category_id,
      made_for_kids: doc.youtube.made_for_kids,
      privacy_status: "private",
      title: perLocale[narration].title,
      description: perLocale[narration].description,
      tags,
      localizations: Object.fromEntries(Object.entries(perLocale).filter(([locale]) => locale !== narration)),
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
 * The Studio steps for each language's own thumbnail, as YouTube Help "Add Multi-language
 * features to your videos" (support.google.com/youtube/answer/13338784, read 2026-10-01) gives
 * them under 「Manage localized thumbnails」: long-form videos only, on a channel with access to
 * advanced features, the video's own thumbnail first, then Studio's 「語言」 page, the language's
 * name, 「新增」 beside 「縮圖」. The page names no API for it, so the owner uploads them by hand.
 */
export function localizedThumbnailSteps(thumbnails = {}, skipped = {}) {
  const lines = [];
  const files = Object.entries(thumbnails);
  if (files.length) {
    lines.push("要上傳的縮圖（每個語言一張，字換成該語言，畫面與版型同 `thumbnail.jpg`）：", "");
    for (const [locale, file] of files) lines.push(`- \`${file}\`（${locale}）`);
    lines.push(
      "",
      "先照第 1 節傳好 `thumbnail.jpg`。每個語言做一次：Studio 左選單「語言」→ 這支影片 → 點那個語言的名稱 →「縮圖」旁的「新增」→ 選對應的檔案 →「更新」。要點的是語言名稱，所以那個語言要先列在這支影片的「語言」頁：第 2、3 節的字幕、配音或標題說明傳上去後就會列出。",
      "",
      "- YouTube 說明頁寫的條件：只適用長片（不含 Shorts），頻道要能使用「進階功能」。",
      "- 觀眾看到的是符合他語言設定的縮圖；沒有自己縮圖的語言看到 `thumbnail.jpg`。",
      "- 說明頁只寫了 Studio 的做法、沒提到 API，網站也不送它：只能在 Studio 手動傳。",
    );
  }
  const left = Object.entries(skipped);
  if (left.length) {
    if (lines.length) lines.push("");
    lines.push("沒有自己縮圖的語言（用 `thumbnail.jpg`，不用等）：");
    for (const [locale, reason] of left) lines.push(`- ${locale}：${reason}`);
  }
  return lines.join("\n");
}

/**
 * Step 1.4, the thumbnail. With variants B and C (docs/videos/so-thats-why/thumbnails.md §A/B 測試)
 * all three go to Studio's 「測試與比較」 thumbnail test, which takes up to three images, and the
 * title stays as it is while the test runs, or the result cannot be told apart from the title's.
 */
export function thumbnailStep(thumbnail, variants = []) {
  if (!thumbnail) return "這次沒有縮圖，Studio 會自動挑一格";
  if (!variants.length) return "上傳 `thumbnail.jpg`（帳號需完成手機驗證）";
  const letter = (file) => /^thumbnail-([a-z])\.jpg$/.exec(file)?.[1]?.toUpperCase() ?? file;
  const files = ["`thumbnail.jpg`（A）", ...variants.map((file) => `\`${file}\`（${letter(file)}）`)].join("、");
  return `在「縮圖」點「測試與比較」，選縮圖測試，${files}全部上傳（一支影片最多三張；帳號需完成手機驗證）。**測試期間不要改標題**，否則分不出是哪張縮圖的效果；測試結束後把勝出的那張記在這集的 \`brief.md\``;
}

/**
 * The 合集 section of a compilation's UPLOAD.md (docs/videos/BINGE.md): the 1080p file is too
 * big for the review store, so the owner downloads it from the site's 「可以上架」 card; the
 * chapters, one per episode, are already in the description.
 */
export function compilationSection(metadata, { episodes = 0, size_bytes: sizeBytes = 0 } = {}) {
  const gb = (sizeBytes / 1024 ** 3).toFixed(2);
  return `## 合集

- 這支是 ${episodes} 集的合集：每集一章，章節時間戳已經在說明欄裡（\`metadata.json\` 的 \`chapters\` 有 ${(metadata.chapters ?? []).length} 章）。
- 1080p 的 \`final.mp4\` 約 ${gb} GB，不走審核檔案區：到 /admin/videos 這支的「可以上架」卡片下載（\`${metadata.download ?? "upload/final.mp4"}\`），再照第 1 節在 Studio 上傳，瀏覽權限一樣先選「私人」。
- 各集已經各自上架；合集不重跑字幕與旁白，字幕是各集字幕依時間接起來的。`;
}

/**
 * UPLOAD.md: only the operating steps in YouTube Studio. The checks that used to be a list here
 * (facts, links, thumbnail legibility, the owner's viewpoint, the disclosure) are the automatic
 * quality check and the package check now (docs/videos/HANDS-OFF.md); the disclosure answer is
 * in metadata.json and this page only says how to tick it. The dub tracks (docs/videos/DUBS.md)
 * keep their own section: which file goes where in Studio's 「語言」.
 */
export function uploadChecklist({ metadata, captions, thumbnail, drama = false, disclosure = null, dubs = [], skippedDubs = {}, thumbnails = {}, skippedThumbnails = {}, variants = [], compilation = null }) {
  const captionLines = captions.length ? captions.map((file) => `   - \`${file}\``).join("\n") : "   - （還沒有字幕檔：先跑 captions）";
  // Each language's own thumbnail gets a section of its own when there is one or a note about one.
  const languageThumbnails = thumbnail ? localizedThumbnailSteps(thumbnails, skippedThumbnails) : "";
  const thumbnailSection = languageThumbnails ? `## 4. 各語言的縮圖\n\n${languageThumbnails}\n\n` : "";
  const synthetic = typeof disclosure?.synthetic === "boolean" ? disclosure.synthetic : typeof metadata.contains_synthetic_media === "boolean" ? metadata.contains_synthetic_media : drama;
  const reason = disclosure?.reason ?? metadata.disclosure_reason ?? (drama ? "AI-generated shots and voices" : "slides read by a synthesized narration");
  return `# 上傳步驟：${metadata.title}

這個資料夾就是要上傳的全部內容。自動品管與上傳包檢查已經做過；這裡只剩站主自己在 YouTube Studio 的操作，公開的時間也由站主決定。
${compilation ? `\n${compilationSection(metadata, compilation)}\n` : ""}
## 1. 上傳（Studio → 建立 → 上傳影片）

1. 上傳 \`final.mp4\`。**瀏覽權限先選「私人」**。
2. 標題：\`description.zh-TW.txt\` 的第一行。
3. 說明：\`description.zh-TW.txt\` 第三行以後的全部內容（章節時間戳已經在裡面）。
4. 縮圖：${thumbnailStep(thumbnail, variants)}。
5. 目標觀眾：選「否，這不是為兒童打造的內容」${metadata.made_for_kids ? "（注意：video.json 標為兒童內容，請確認）" : ""}。
6. 標籤：貼上 \`metadata.json\` 的 \`tags\`。類別：科學與技術（${metadata.category_id}）。影片語言：中文（台灣）。
7. 「變造或合成內容」：${synthetic ? "勾「是」" : "不用勾"}。\`metadata.json\` 的 \`contains_synthetic_media\` 是 \`${synthetic}\`（${reason}）。

## 2. 字幕

${captionLines}

在「字幕」分頁新增語言並上傳對應的檔案；其他語系的標題與說明在 \`description.<語系>.txt\`。

## 3. 配音音軌（多語言音訊）

${dubSteps(dubs, skippedDubs)}

${thumbnailSection}## ${thumbnailSection ? 5 : 4}. 上傳之後

回到 /admin/videos 這支影片的「可以上架」卡片貼上 YouTube 網址，並選上架時間；影片 ID 會寫進 \`video.json\`，影片就算完成。不要自己按公開：公開由站主選的時間決定。
`;
}
