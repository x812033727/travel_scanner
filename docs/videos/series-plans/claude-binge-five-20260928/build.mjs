// Turns each work's `source.mjs` (the one file an author edits) into the documents the drama
// pipeline files for a binge series (docs/videos/BINGE.md, docs/videos/SERIES.md): the
// SeriesIn request, the setting book, the whole-run outline and the four chapter outlines, each
// as {body_md, body_json} the way `POST /video/automation/series/<slug>/docs` takes them, plus
// the readable Markdown, a continuity ledger, the packaging copy and a manifest of hashes.
// Nothing here talks to the site or spends a cent; see README.md for how the files are used.
import fs from "node:fs/promises";
import path from "node:path";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";

export const ROOT = path.dirname(fileURLToPath(import.meta.url));
export const SLUGS = [
  "reload-first-day",
  "before-the-hammer",
  "three-needles",
  "taste-of-the-throne",
  "ghost-at-his-side",
];
// The one-button form's values every one of the five shares (docs/videos/BINGE.md): 120 minutes
// of 3-minute episodes is 40 episodes in four chapters of ten (`binge_shape`); hybrid visuals;
// one long video at the end; a closed first part. `hands_off` stays false so that creating the
// series never starts an unattended run by accident; the owner flips it on the series page.
export const COMMON = {
  total_minutes: 120,
  target_minutes: 3,
  planned_episodes: 40,
  episodes_per_chapter: 10,
  compilation: true,
  open_ended: false,
  visual_tier: "hybrid",
  style_preset: "cinematic-3d",
  hands_off: false,
};
export const CHAPTERS = COMMON.planned_episodes / COMMON.episodes_per_chapter;

export const hash = (value) =>
  createHash("sha256").update(typeof value === "string" ? value : JSON.stringify(value)).digest("hex");

const pad = (n) => String(n).padStart(2, "0");
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const cell = (value) => String(value ?? "").replaceAll("|", "／").replaceAll("\n", "<br>");
const bullets = (items) => items.map((item) => `- ${item}`).join("\n");
const table = (heads, rows) =>
  [`| ${heads.join(" | ")} |`, `| ${heads.map(() => "---").join(" | ")} |`, ...rows.map((row) => `| ${row.map(cell).join(" | ")} |`)].join("\n");
const list = (items) => (items && items.length ? items.join("、") : "—");
const chapterOf = (episode) => Math.ceil(episode / COMMON.episodes_per_chapter);
const minutes = (chapter) => `${(chapter - 1) * 30}–${chapter * 30} 分`;

export const CLIFF_LABELS = { danger: "危機", reveal: "揭露", choice: "抉擇", reversal: "反轉", emotion: "情感" };
export const HOOK_LABELS = { question: "問題", danger: "危險", image: "畫面", line: "台詞", reversal: "反轉" };
export const ARC_LABELS = { wins: "贏", suffers: "挨打", mixed: "有輸有贏" };
export const BEAT_LABELS = { opening: "開場", first_half: "前半", midpoint: "中段", second_half: "後半", ending: "結尾" };
export const SATISFACTION_LABELS = {
  face_slap: "打臉",
  identity_reveal: "身份揭露",
  counter_kill: "反殺",
  level_up: "升級",
  first_clear: "首殺／首通",
  betrayer_punished: "背叛者遭報",
  villain_humbled: "反派低頭",
  hidden_power: "藏拙露鋒",
  public_vindication: "當眾平反",
  rescue: "及時救場",
  reversal: "反轉",
};

export async function loadSource(slug) {
  if (!SLUGS.includes(slug)) throw new Error(`unknown work: ${slug}`);
  return (await import(new URL(`./${slug}/source.mjs`, import.meta.url))).default;
}

/** The SeriesIn body the owner would send to create the series (apps/api schemas.SeriesIn). */
export function seriesRequest(source) {
  const s = source.series;
  return {
    slug: s.slug,
    title: s.title,
    premise: s.premise,
    aspects: s.aspects ?? [],
    tone: s.tone,
    style_preset: COMMON.style_preset,
    target_minutes: COMMON.target_minutes,
    planned_episodes: COMMON.planned_episodes,
    episodes_per_chapter: COMMON.episodes_per_chapter,
    open_ended: COMMON.open_ended,
    note: s.note,
    genre: s.genre,
    lead: s.lead,
    hands_off: COMMON.hands_off,
    compilation: COMMON.compilation,
    visual_tier: COMMON.visual_tier,
    total_minutes: COMMON.total_minutes,
  };
}

/** The series as the worker's `documentProblem` job carries it. */
export function jobSeries(source) {
  return { ...seriesRequest(source), chapters: CHAPTERS };
}

function characterBlock(c) {
  return [
    `### ${c.name}（\`${c.id}\`，${c.role === "lead" ? "主角" : c.role === "antagonist" ? "反派" : "配角"}）`,
    "",
    table(
      ["項目", "設定"],
      [
        ["年齡與身分", c.age],
        ["性格", c.personality],
        ["想要", c.want],
        ["害怕", c.fear],
        ["秘密", c.secret],
        ["說話習慣", c.speech],
        ["聲音（擬定，未試聽）", `${c.voice.provider} / ${c.voice.name} / ${c.voice.style}`],
        ["外觀提示詞（每集逐字沿用）", c.appearance],
      ],
    ),
    "",
    table(["對象", "關係"], c.relationships.map((r) => [r.with, r.kind])),
  ].join("\n");
}

function settingDocument(source) {
  const s = source.series;
  const st = source.setting;
  const mysteries = st.mysteries.map((m) => ({
    id: m.id,
    question: m.question,
    answer: m.answer,
    planted: m.planted,
    advanced: m.advanced,
    revealed: m.revealed,
    planted_chapter: chapterOf(m.planted),
    reveal_chapter: m.revealed ? chapterOf(m.revealed) : null,
    reserved: Boolean(m.reserved),
  }));
  const body_json = {
    title: s.title,
    logline: s.logline,
    characters: st.characters,
    world: st.world,
    rules: st.rules,
    mysteries,
    tone: st.tone,
    imagery: st.imagery,
    naming: st.naming,
    never: st.never,
    lexicon: st.lexicon,
    ending: st.ending,
    cold_open: st.cold_open,
  };
  const body_md = [
    `# ${s.title}｜設定集`,
    "",
    `> ${s.logline}`,
    "",
    "> 製作企劃，尚未生成任何圖片、聲音或影片；聲音是擬定的 casting，開拍前先試聽。",
    "",
    "## 世界觀",
    "",
    st.world.era,
    "",
    table(["地點（id）", "名稱", "固定辨識"], st.world.places.map((p) => [p.id, p.name, p.description])),
    "",
    table(["勢力", "想要什麼", "隱瞞什麼"], st.world.factions.map((f) => [f.name, f.wants, f.hides])),
    "",
    "## 規則與代價",
    "",
    bullets(st.rules),
    "",
    "## 人物",
    "",
    st.characters.map(characterBlock).join("\n\n"),
    "",
    "## 長線謎團",
    "",
    table(
      ["id", "問題", "確定答案", "埋下（集）", "推進（集）", "揭曉（集）"],
      mysteries.map((m) => [m.id, m.question, m.answer, m.planted, list(m.advanced), m.revealed ?? "保留"]),
    ),
    "",
    "## 語氣與畫面",
    "",
    st.tone,
    "",
    st.imagery,
    "",
    "## 開場三十秒（第 1 集）",
    "",
    table(["秒", "畫面", "聲音"], st.cold_open.map((b) => [b.seconds, b.picture, b.audio])),
    "",
    "## 命名規則",
    "",
    bullets(st.naming),
    "",
    "## 不做的事",
    "",
    bullets(st.never),
    "",
    "## 發音表",
    "",
    table(["詞", "讀法"], Object.entries(st.lexicon).map(([k, v]) => [k, v ?? "照字面"])),
    "",
    "## 確定的結局",
    "",
    st.ending,
    "",
  ].join("\n");
  return { body_md, body_json };
}

function outlineDocument(source) {
  const s = source.series;
  const chapters = source.chapters;
  const schedule = source.setting.mysteries.map((m) => ({
    mystery: m.id,
    planted: chapterOf(m.planted),
    advanced: [...new Set(m.advanced.map(chapterOf))],
    revealed: m.revealed ? chapterOf(m.revealed) : null,
    planted_episode: m.planted,
    advanced_episodes: m.advanced,
    revealed_episode: m.revealed,
  }));
  const body_json = {
    chapters: chapters.map((c) => ({
      number: c.number,
      title: c.title,
      theme: c.theme,
      start_state: c.start_state,
      end_state: c.end_state,
      turn: c.turn,
      episodes: c.episodes.map((e) => ({ number: e.number, title: e.title, logline: e.logline, timeline: e.timeline })),
    })),
    tension_map: chapters.map((c) => ({ chapter: c.number, stakes: c.stakes, question: c.question, turn: c.turn })),
    reveal_schedule: schedule,
    world_flip_episode: chapters.flatMap((c) => c.episodes).find((e) => e.world_flip)?.number ?? null,
  };
  const body_md = [
    `# ${s.title}｜四篇四十集總綱`,
    "",
    s.premise,
    "",
    "每集目標三分鐘；分鐘數是規劃，不是量測。",
    "",
    "## 全季張力地圖",
    "",
    table(["篇", "時間", "賭注", "核心問題", "篇末轉折"], chapters.map((c) => [c.number, minutes(c.number), c.stakes, c.question, c.turn])),
    "",
    ...chapters.flatMap((c) => [
      `## 第 ${c.number} 篇：${c.title}`,
      "",
      c.theme,
      "",
      `- 起點：${c.start_state}`,
      `- 終點：${c.end_state}`,
      `- 篇末轉折：${c.turn}`,
      "",
      table(
        ["集", "標題", "一句話（回答一個問題、丟出更大的問題）", "時間線"],
        c.episodes.map((e) => [pad(e.number), e.title + (e.world_flip ? "（翻轉世界觀）" : ""), e.logline, e.timeline === "past" ? "過去" : "現在"]),
      ),
      "",
    ]),
    "## 謎團揭曉排程",
    "",
    table(
      ["謎團", "埋下", "推進", "揭曉"],
      schedule.map((m) => [m.mystery, `第 ${m.planted_episode} 集`, m.advanced_episodes.length ? m.advanced_episodes.map((n) => `第 ${n} 集`).join("、") : "—", m.revealed_episode ? `第 ${m.revealed_episode} 集` : "保留"]),
    ),
    "",
  ].join("\n");
  return { body_md, body_json };
}

function episodeBlock(e, isLast) {
  const sats = e.satisfaction.map((b) => `${BEAT_LABELS[b.beat]}／${SATISFACTION_LABELS[b.type] ?? b.type}：${b.text}`);
  return [
    `### 第 ${e.number} 集：${e.title}${e.world_flip ? "（翻轉世界觀）" : ""}`,
    "",
    `**一句話**　${e.logline}`,
    "",
    table(
      ["節拍", "內容"],
      [
        [`開場鉤子（${HOOK_LABELS[e.hook_type] ?? e.hook_type}）`, `「${e.hook}」`],
        ["主要衝突", e.conflict],
        ["中段轉折", e.turn],
        ["爽點", sats.join("<br>")],
        [isLast ? `收束（${CLIFF_LABELS[e.cliffhanger.type]}）` : `結尾懸念（${CLIFF_LABELS[e.cliffhanger.type]}）`, e.cliffhanger.text],
        ["埋下 / 回收", `${list(e.setups)} / ${list(e.payoffs)}`],
        ["張力曲線", e.tension.join(" → ")],
        ["主角走向", ARC_LABELS[e.lead_arc] ?? e.lead_arc],
        ["出場角色", list(e.characters)],
        ["場景", list(e.locations)],
        ["主題句", e.theme],
        ["下一集承接", e.carry],
      ],
    ),
  ].join("\n");
}

function chapterDocument(source, chapter) {
  const s = source.series;
  const episodes = chapter.episodes.map((e) => ({
    number: e.number,
    title: e.title,
    logline: e.logline,
    timeline: e.timeline,
    hook: e.hook,
    hook_type: e.hook_type,
    conflict: e.conflict,
    turn: e.turn,
    cliffhanger: { type: e.cliffhanger.type, text: e.cliffhanger.text },
    satisfaction: e.satisfaction.map((b) => ({ beat: b.beat, type: b.type, text: b.text })),
    lead_arc: e.lead_arc,
    setups: e.setups,
    payoffs: e.payoffs,
    tension: e.tension,
    characters: e.characters,
    locations: e.locations,
    theme: e.theme,
    carry: e.carry,
    ...(e.world_flip ? { world_flip: true } : {}),
  }));
  const body_json = { chapter: chapter.number, title: chapter.title, episodes };
  const last = chapter.number === CHAPTERS;
  const body_md = [
    `# ${s.title}｜第 ${chapter.number} 篇：${chapter.title}`,
    "",
    "## 本篇",
    "",
    chapter.theme,
    "",
    `- 賭注：${chapter.stakes}`,
    `- 核心問題：${chapter.question}`,
    `- 起點：${chapter.start_state}`,
    `- 終點：${chapter.end_state}`,
    `- 篇末轉折：${chapter.turn}`,
    `- 規劃時段：${minutes(chapter.number)}；秒數與鏡數由劇本與 TTS 決定。`,
    "",
    chapter.episodes.map((e) => episodeBlock(e, last && e.number === COMMON.planned_episodes)).join("\n\n"),
    "",
  ].join("\n");
  return { body_md, body_json };
}

function packagingFiles(source) {
  const s = source.series;
  const p = source.packaging;
  const episodes = source.chapters.flatMap((c) => c.episodes);
  const packaging = {
    ...p,
    status: "planning-only",
    category_id: "24",
    default_language: "zh-TW",
    caption_languages: ["zh-TW", "en", "ja", "ko", "zh-CN"],
    chapter_titles: episodes.map((e) => ({ episode: e.number, title: e.title })),
    compilation: { chapter_cards: false, outro: false },
    made_for_kids: false,
    disclosure: { synthetic_content: true },
    publish_state: "not-uploaded",
  };
  const md = [
    `# ${s.title}｜標題、縮圖與上架文案`,
    "",
    "> 文案與構圖規格；縮圖圖片、字幕、章節時間碼與成片尚未製作。",
    "",
    "## 為什麼有機會破百萬",
    "",
    bullets(p.why_million),
    "",
    "## 觀眾",
    "",
    p.audience,
    "",
    "## 三組標題（A/B 測試用）",
    "",
    p.titles.map((t, i) => `${i + 1}. ${t}`).join("\n"),
    "",
    "## 三組縮圖",
    "",
    p.thumbnails
      .map((t) => `### ${t.id}：${t.headline}${t.tag ? `（角標：${t.tag}）` : ""}\n\n- 構圖：${t.composition}\n- 素材：第 ${t.episode} 集，${t.scene}\n- 必須兌現：${t.promise}`)
      .join("\n\n"),
    "",
    "## 說明欄本文",
    "",
    p.description,
    "",
    "## 標籤",
    "",
    p.tags.join("、"),
    "",
    "## 視覺與音樂",
    "",
    p.visual_identity,
    "",
    p.music,
    "",
    "## 置頂留言",
    "",
    p.pinned_comment,
    "",
    "## 合集交接",
    "",
    "- 合集 `video.json` 的 `compilation` 設 `chapter_cards: false`、`outro: false`，一口氣看到底；YouTube 章節照實際 `timeline.json` 的時間碼。",
    "- 每集冷開場：第一句就是鉤子，沒有片頭卡、沒有前情、最後一句就是懸念。",
    "- 分類 24（娛樂）、非兒童向、合成內容揭露一律勾；五語 CC 由產線在成片後產出。",
    "",
  ].join("\n");
  return { "packaging.json": json(packaging), "packaging.md": md };
}

export function compile(source) {
  const s = source.series;
  const episodes = source.chapters.flatMap((c) => c.episodes);
  const files = {};
  files["series-request.json"] = json(seriesRequest(source));
  const setting = settingDocument(source);
  files["setting.md"] = setting.body_md;
  files["setting.json"] = json(setting);
  const outline = outlineDocument(source);
  files["outline.md"] = outline.body_md;
  files["outline.json"] = json(outline);
  const chapterDocs = [];
  for (const chapter of source.chapters) {
    const doc = chapterDocument(source, chapter);
    files[`chapter-${pad(chapter.number)}.md`] = doc.body_md;
    files[`chapter-${pad(chapter.number)}.json`] = json(doc);
    chapterDocs.push({ kind: "chapter", chapter_number: chapter.number, ...doc });
  }
  files["documents.json"] = json({
    slug: s.slug,
    status: "prepared-not-submitted",
    documents: [{ kind: "setting", chapter_number: 0, ...setting }, { kind: "outline", chapter_number: 0, ...outline }, ...chapterDocs],
  });
  files["continuity.md"] = [
    `# ${s.title}｜連貫性表`,
    "",
    bullets(source.continuity_notes),
    "",
    table(["集", "標題", "出場", "場景", "埋下", "回收", "下一集承接"], episodes.map((e) => [e.number, e.title, list(e.characters), list(e.locations), list(e.setups), list(e.payoffs), e.carry])),
    "",
  ].join("\n");
  Object.assign(files, packagingFiles(source));
  files["README.md"] = [
    `# ${s.title}`,
    "",
    `> ${s.logline}`,
    "",
    s.premise,
    "",
    `題材 \`${s.genre}\`｜主角 \`${s.lead}\`｜情感線 \`${s.tone}\`｜120 分鐘、四篇四十集、hybrid 畫面。狀態：**製作企劃**，沒有建立後台作品、沒有生成媒體、沒有上架。`,
    "",
    "- [設定集](setting.md)：世界、規則、人物（外觀提示詞與聲音）、謎團與答案、開場三十秒、結局。",
    "- [四十集總綱](outline.md)：張力地圖、每集一句話、謎團排程。",
    "- [第 1 篇](chapter-01.md) · [第 2 篇](chapter-02.md) · [第 3 篇](chapter-03.md) · [第 4 篇](chapter-04.md)：每集的鉤子、衝突、轉折、爽點、懸念、張力曲線與承接。",
    "- [連貫性表](continuity.md) · [標題縮圖與上架文案](packaging.md)。",
    "- [後台建立資料](series-request.json)：`SeriesIn` 欄位；[待送件文件](documents.json)：設定集、總綱、四篇細綱的 `body_md`／`body_json`。",
    "",
  ].join("\n");
  files["manifest.json"] = json({
    schema_version: 1,
    slug: s.slug,
    title: s.title,
    genre: s.genre,
    lead: s.lead,
    source_sha256: hash(source),
    stage: "production-plan",
    episode_count: episodes.length,
    chapter_count: source.chapters.length,
    media_generated: false,
    admin_series_created: false,
    published: false,
    files: Object.fromEntries(Object.entries(files).map(([name, data]) => [name, hash(data)])),
  });
  return files;
}

export async function writeWork(slug) {
  const files = compile(await loadSource(slug));
  for (const [name, body] of Object.entries(files)) await fs.writeFile(path.join(ROOT, slug, name), body, "utf8");
  return Object.keys(files).length;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const slugs = process.argv.slice(2);
  for (const slug of slugs.length ? slugs : SLUGS) {
    const count = await writeWork(slug);
    process.stdout.write(`${slug}: ${count} files built\n`);
  }
}
