// 把企劃包變成站上作品要的三份文件：`node site-bundle.mjs > bundle.json`。
//
// 輸出 `{ series, docs }`：`series` 是「新的作品」的 SeriesIn（30 集、每篇 10 集、題材系統遊戲、
// 男主、anime-2d、3 分鐘、畫面做法 manga、先不免關卡、做合集）；`docs` 是設定集（kind setting）、
// 總綱（outline，三篇各十集）與第 1 篇細綱（chapter 1 ＝ 第 1–10 集）的 `{ body_md, body_json }`，
// 形狀照 apps/api/app/video_automation/series.py 的 doc_problem 與 tools/video/automation/series.mjs
// 的 documentProblem。站上的做法：作品建好後工人先寫出每份文件的第一版，站主在後台把那一版換成
// 這裡的版本並核准（PUT …/docs/<kind>[/<chapter>]，帶 body_json、approve: true），三份都換完再打開
// 免關卡與設定分頁的「自動開下一集」。票：tasks/open/2026-10-22-bug-30.md。
import { readFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const plan = path.dirname(fileURLToPath(import.meta.url));
const read = (name) => readFileSync(path.join(plan, name), "utf8");
const json = (name) => JSON.parse(read(name));
const setting = json("setting.json");
const outline = json("outline.json");
const season = json("season-01.json");
const settingMd = read("setting.md");
const outlineMd = read("outline.md");
const seasonMd = read("season-01.md");

export const SLUG = "xitong-shuo-wo-shi-bug";
export const PLANNED = 30;
export const PER_CHAPTER = 10;

// 工人的 castFrom 讀的是 voice: { provider, name, style }；企劃包寫的是 tts.voice "gemini:Charon"。
function character(c) {
  const entry = { id: c.id, name: c.name, role: c.role, appearance: c.appearance };
  if (c.age) entry.age = c.age;
  if (typeof c.voice === "string") entry.voice_note = c.voice;
  if (c.tts && typeof c.tts.voice === "string" && c.tts.voice.startsWith("gemini:")) {
    entry.voice = { provider: "gemini", name: c.tts.voice.slice("gemini:".length), ...(c.tts.style ? { style: String(c.tts.style).slice(0, 400) } : {}) };
  }
  if (c.arc) entry.arc = c.arc;
  return entry;
}

export function buildBundle() {
  const characters = [...setting.characters.map(character), ...season.guest_cast.map(character)];
  for (const c of characters) {
    if (!/^[a-z][a-z0-9-]{1,23}$/.test(c.id)) throw new Error(`bad character id ${c.id}`);
    if (c.appearance.length > 800) throw new Error(`appearance over 800 characters: ${c.id}`);
  }
  const settingDoc = {
    kind: "setting",
    chapter: 0,
    body_md: settingMd,
    body_json: {
      title: "系統說我是 BUG",
      short_title: setting.short_title,
      logline: setting.logline,
      premise: setting.premise,
      world: setting.world,
      characters,
      beasts: setting.beasts,
      mysteries: setting.mysteries,
      tones: setting.tones,
      advertiser_safety: setting.advertiser_safety,
      glamour: setting.glamour,
      visual_bible: setting.visual_bible,
      season_threads: season.threads,
    },
  };

  const s1 = outline.seasons[0];
  const byNumber = new Map(season.episodes.map((e) => [e.number, e]));
  const siteChapters = [];
  for (let c = 1; c <= PLANNED / PER_CHAPTER; c++) {
    const first = (c - 1) * PER_CHAPTER + 1;
    const last = c * PER_CHAPTER;
    const planChapters = s1.chapters.filter((pc) => pc.episodes[0] >= first && pc.episodes[1] <= last);
    siteChapters.push({
      number: c,
      title: `${planChapters.map((pc) => pc.title).join("・")}（第 ${first}–${last} 集）`,
      tones: [...new Set(planChapters.flatMap((pc) => pc.tones))],
      plan_chapters: planChapters,
      episodes: Array.from({ length: PER_CHAPTER }, (_, i) => {
        const e = byNumber.get(first + i);
        if (!e) throw new Error(`season-01.json has no episode ${first + i}`);
        return { number: e.number, title: e.title, logline: e.logline, youtube_title: e.youtube_title, duration_s: e.duration_s };
      }),
    });
  }
  const outlineDoc = {
    kind: "outline",
    chapter: 0,
    body_md: outlineMd,
    body_json: {
      arc: outline.arc,
      ending: outline.ending,
      season: { number: s1.number, title: s1.title, theme: s1.theme, start_state: s1.start_state, end_state: s1.end_state },
      chapters: siteChapters,
    },
  };

  const chapterDocs = siteChapters.slice(0, 1).map((chapter) => {
    const first = chapter.episodes[0].number;
    const last = chapter.episodes[chapter.episodes.length - 1].number;
    const next = s1.chapters.find((pc) => pc.episodes[0] === last + 1);
    const cut = next ? seasonMd.indexOf(`## 篇章 ${next.number}`) : seasonMd.length;
    if (cut < 0) throw new Error(`season-01.md: heading of chapter ${next.number} not found`);
    return {
      kind: "chapter",
      chapter: chapter.number,
      body_md: seasonMd.slice(0, cut).trimEnd() + "\n",
      body_json: {
        chapter: chapter.number,
        title: chapter.title,
        guest_cast: season.guest_cast,
        threads: season.threads.filter((t) => t.setup_episode <= last),
        episodes: season.episodes.filter((e) => e.number >= first && e.number <= last).map((e) => ({ ...e })),
      },
    };
  });

  const premise = read("site-premise.md").trim();
  const note = read("site-note.md").trim();
  if (premise.length > 4000) throw new Error(`premise ${premise.length} > 4000`);
  if (note.length > 2000) throw new Error(`note ${note.length} > 2000`);
  const series = {
    slug: SLUG,
    kind: "series",
    title: "系統說我是 BUG",
    premise,
    aspects: [],
    tone: "hetero-leads",
    style_preset: "anime-2d",
    target_minutes: 3,
    planned_episodes: PLANNED,
    episodes_per_chapter: PER_CHAPTER,
    open_ended: true,
    note,
    genre: "system-game",
    lead: "male",
    hands_off: false,
    compilation: true,
    visual_tier: "manga",
  };
  return { series, docs: [settingDoc, outlineDoc, ...chapterDocs] };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const bundle = buildBundle();
  process.stdout.write(JSON.stringify(bundle, null, 1));
  const sizes = bundle.docs.map((d) => `${d.kind}/${d.chapter}: md ${d.body_md.length}, json ${JSON.stringify(d.body_json).length}`).join("; ");
  process.stderr.write(`premise ${bundle.series.premise.length}, note ${bundle.series.note.length}; ${sizes}\n`);
}
