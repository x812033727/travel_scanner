// The brand story's flow (docs/videos/STORY.md, automation/story.mjs), with stand-ins for the
// site, the model, the pages and the media commands: no network, no model, no media vendor. The
// story here is invented (a folding umbrella and a maker that never existed); it is not one of
// the planned hundred.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, unlinkSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { readApprovals } from "../core/approvals.mjs";
import { clipsHash, drawnShotScenes, EXPLAINER_PRESET, hasCast, isExplainer, lookHash, mixHash, shotScenes, subtitlesHash } from "../core/drama.mjs";
import { explainerFixture, sandbox, storyFixture, storySeries, writeAudioFixture } from "../core/fixtures/load.mjs";
import { validateLexicon } from "../core/lexicon.mjs";
import { reviseStoryLexicon, videoLexicon } from "../core/lexicon-store.mjs";
import { BRIEF_SECTIONS_DRAMA, briefSectionsFor } from "../core/lint.mjs";
import { NARRATIVE_PANEL, PANEL_RULES_SHA256 } from "../core/narrative.mjs";
import { scriptCheckBinding } from "../core/script-check.mjs";
import { isStory } from "../core/story.mjs";
import { readJson } from "../core/paths.mjs";
import { eachLine } from "../core/schema.mjs";
import { pipelineStatus } from "../core/state.mjs";
import { buildTimeline, estimatedSamples, estimateTimeline, speechHash, visualHash } from "../core/timeline.mjs";
import { automationClient } from "./client.mjs";
import { MAX_PAGE_CHARS, pageReader } from "./fetch.mjs";
import { Automation, automatedVideos, MAX_STAGE_FAILURES } from "./flow.mjs";
import { instructionsFor } from "./prompts.mjs";
import { isExplainerOneOff, startEpisode } from "./series.mjs";
import { STORY_INSTRUCTIONS } from "./story-prompts.mjs";
import {
  advanceStory,
  anchorsFor,
  applyPatch,
  CHAPTER_KEYS,
  chapterBudgets,
  composeStory,
  effectiveStoryLengthBand,
  effectiveStoryMinutes,
  factChapters,
  figuresIn,
  lengthBand,
  LENGTH_FIX_ROUNDS,
  OUTLINE_NOTE,
  passagesOf,
  PILOT_SCRIPT_REFERENCES,
  PILOT_SCRIPT_REVIEW_FILE,
  pilotScriptReviewEvidence,
  pilotScriptReviewProblem,
  readChapter,
  readChapterAnswer,
  SCRIPT_NOTE,
  STORY_CHAPTERS_DIR,
  storyCast,
  storyBrief,
  cuteStoryVisualProblems,
  storyLineIds,
  storySeriesFile,
  yearForms,
} from "./story.mjs";

const TOKEN = `mkv_${"u".repeat(43)}`;
const SITE = "https://site.test";
const SLUG = "story-folding-umbrella";
const sha = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");

// --- the invented story --------------------------------------------------------------------------

const LONG_PAGE = "https://museum.example/folding-umbrellas";
const FILLER = "Folding umbrellas have a long history in the city, and the collection keeps many of them. ";
// The figure stands past the 40,000 characters the worker's reader keeps of a page.
const MUSEUM = `<html><head><title>Umbrella Museum</title></head><body><p>${FILLER.repeat(560)}</p><p>In 1954 the factory sold its 1,000,000th folding umbrella, a record for the trade.</p><p>${FILLER.repeat(120)}</p></body></html>`;
const PAGES = {
  "https://patents.example/umbrella-1928": `<html><head><title>Patent</title></head><body><p>Telescopic umbrella frame. Filed 1928 by H. Marrow, London. The frame folds in three sections so the umbrella fits a coat pocket.</p><p>${"The claims describe a sliding runner and a locking notch. ".repeat(12)}</p></body></html>`,
  [LONG_PAGE]: MUSEUM,
  "https://news.example/marrow-train": `<html><head><title>Daily Example</title></head><body><p>Marrow recalled that the idea came to him on a rainy train ride, with a long umbrella dripping on his shoes.</p><p>${"He told the paper the story many times over the years. ".repeat(10)}</p></body></html>`,
};
const PDFS = new Set(["https://brellco.example/catalogue-1954.pdf", "https://brellco.example/annual-2025.pdf"]);

const POINTS = {
  hook: "雨傘用了三千年，能折起來放進口袋卻要等到 1928 年。先拋出這個時間差，再說這支影片要回答的事：一副會伸縮的傘骨，怎麼變成一門生意。",
  origin: "1928 年，倫敦的發明家 Hollis Marrow 申請了伸縮傘骨的專利。照 Marrow 自己的回憶，點子來自一趟被雨淋濕的火車旅行。",
  idea: "關鍵在傘骨分三段、用滑扣鎖住，收起來只有原本的三分之一長，可以放進大衣口袋；這讓傘從要拿在手上的東西，變成隨身帶著的東西。",
  engine: "Brellco 把專利做成工廠的生意：1954 年賣出第 100 萬把折疊傘。便宜的零件、統一的尺寸，讓百貨公司願意大量進貨。",
  turn: "折疊傘好帶，卻容易壞：傘骨多了關節，就多了會斷的地方。便宜的仿製品湧進市場，讓原本的工廠得在品質與價格之間選一邊。",
  now: "Brellco 的年報寫，2025 年折疊傘佔營收 62%。收尾回到開場的問題：點子不缺，缺的是讓它變得必要的生活方式。",
};
const PLAN = {
  id: "A90",
  category: "everyday",
  region: "global",
  subject: "折疊傘",
  question: "雨傘用了三千年，為什麼要等到 1928 年才折得進口袋？",
  chapters: CHAPTER_KEYS.map((key) => ({ key, point: POINTS[key] })),
  takeaway: "東西變小，常常不是技術突破，而是生活先變了。",
  must_verify: [
    { claim: "Hollis Marrow 在 1928 年申請伸縮傘骨的專利", sources: [0], core: true },
    { claim: "Brellco 在 1954 年賣出第 100 萬把折疊傘", sources: [1, 3] },
    { claim: "照 Marrow 的回憶，點子來自一趟被雨淋濕的火車旅行", sources: [2], attributed: true },
    { claim: "Brellco 的年報寫，2025 年折疊傘佔營收 62%", sources: [4], reviewer_only: true },
  ],
  sources: [
    { url: "https://patents.example/umbrella-1928", publisher: "Patent Office", kind: "official", supports: "Marrow 1928 年申請的伸縮傘骨專利", checked: "2026-09-28" },
    { url: LONG_PAGE, publisher: "Umbrella Museum", kind: "archive", supports: "1954 年第 100 萬把折疊傘", checked: "2026-09-28" },
    { url: "https://news.example/marrow-train", publisher: "Daily Example", kind: "news", supports: "Marrow 回憶火車上的靈感", checked: "2026-09-28" },
    { url: "https://brellco.example/catalogue-1954.pdf", publisher: "Brellco", kind: "official", supports: "1954 年的型錄：第 100 萬把折疊傘出廠", checked: "2026-09-28" },
    { url: "https://brellco.example/annual-2025.pdf", publisher: "Brellco", kind: "official", supports: "2025 年年報：折疊傘佔營收 62%", checked: "2026-09-28" },
  ],
  names: ["Hollis Marrow", "Marrow", "Brellco"],
  cast: [],
  image_notes: "畫 1920 年代的倫敦街頭、火車車廂、工廠與百貨公司；傘上不畫任何商標或字樣。",
  sensitivity: "none",
  related_guide: null,
  thumbnail: { headline: "傘為什麼會折", idea: "左邊一把長傘，右邊一把收進口袋的折疊傘" },
  caveats: "Marrow 是否在世未能確認，不提家人與健康。1954 年的一百萬把只有博物館與型錄兩個來源，要說是博物館的說法時照實交代。",
  publish: { day: 1, slot: "12:00" },
};
const LOOK = {
  style: "flat 2D cartoon illustration for an explainer video, clean bold outlines, warm muted palette with teal and orange accents, empty space in the bottom fifth of the frame",
  negative: "text, letters, numbers, watermark, logo, brand mark, photorealistic, real person likeness, extra fingers",
  motion: "slow steady camera move, no morphing",
};
const SERIES = {
  id: "5e1a2b3c-0000-4000-8000-00000000abcd", slug: "brand-stories", kind: "story", title: "品牌故事：日常背後的生意", premise: "每一集講一個品牌或日用品背後的生意。",
  aspects: [], tone: "no-romance", style_preset: "custom", target_minutes: 13, planned_episodes: 100, episodes_per_chapter: 10, chapters: 1, open_ended: false,
  status: "active", note: "企劃清單在 docs/videos/story-plans", requested_chapter: null, force_next: false, episodes_done: 0, episodes_started: 0, episodes_ready: 1, docs_pending: 0,
  media_usd: 0, clip_seconds: 0, genre: "xianxia-bonds", lead: "dual-male", hands_off: true, compilation: false, visual_tier: "stills", total_minutes: null,
  episodes_per_day: 2, image_model: "gemini-3.1-flash-image", look: LOOK, quota: null, created_at: "2026-09-28T00:00:00Z", updated_at: "2026-09-28T00:00:00Z",
};
const EPISODE = { number: 1, chapter_number: 1, title: "折疊傘等了三千年", logline: "雨傘用了三千年，折得進口袋卻是 1928 年的事：一副伸縮傘骨怎麼變成一門生意。", beats: PLAN, status: "ready", slug: SLUG, recap: null, started_at: null, finished_at: null, video: null };

// What the stand-in writer says in each chapter: two shots of two lines (the last chapter ends with the outro card).
const TEXT = {
  hook: [["雨傘用了三千年。", "為什麼到 1928 年才折得進口袋？"], ["這一集從一趟淋雨的火車講起。", "看一副傘骨怎麼變成一門生意。"]],
  origin: [["1928 年，Hollis Marrow 申請了專利。", "他設計的是一副會伸縮的傘骨。"], ["照 Marrow 的回憶，", "點子來自一趟淋濕的火車旅行。"]],
  idea: [["傘骨分成三段，用滑扣鎖住。", "收起來只剩原本的三分之一長。"], ["傘從拿在手上的東西，", "變成放進口袋的東西。"]],
  engine: [["照博物館的說法，", "Brellco 在 1954 年賣出第 100 萬把。"], ["便宜的零件和統一的尺寸，", "讓百貨公司願意大量進貨。"]],
  turn: [["多了關節，就多了會斷的地方。", "便宜的仿製品也跟著出現。"], ["工廠只好在品質與價格之間，", "選一邊站。"]],
  now: [["照 Brellco 的年報，", "2025 年折疊傘佔營收 62%。"], ["點子從來不缺，", "缺的是讓它變得必要的生活。"]],
};
const PROMPTS = {
  hook: ["a rainy 1920s London street, people holding long black umbrellas, wide shot, soft grey light", "a folded umbrella peeking out of a coat pocket on a train seat, close up, warm light"],
  origin: ["a 1920s inventor at a cluttered workbench sketching a folding frame, medium shot, lamp light", "a steam train compartment in the rain, a man with a dripping long umbrella, wide shot"],
  idea: ["a three-part umbrella frame laid flat on a drafting table, top view, clean light", "a hand slipping a small folded umbrella into a coat pocket, close up"],
  engine: ["a busy 1950s factory floor with rows of umbrella frames, wide shot", "a department store counter stacked with boxed umbrellas, shoppers browsing, medium shot"],
  turn: ["a broken umbrella rib bent in the wind on a city corner, close up", "two umbrellas on a scale, a cheap one and a sturdy one, still life"],
  now: ["a modern commuter train with passengers holding compact umbrellas, wide shot", "a person on a rainy street opening a small umbrella under a lamp, medium shot"],
};
const TITLES = { hook: "雨傘三千年的謎", origin: "倫敦的伸縮傘骨", idea: "折起來的點子", engine: "一百萬把傘的生意", turn: "好帶卻容易壞", now: "折疊傘的現在" };
const CLAIMS = {
  hook: [{ claim: "折疊傘到 1928 年才出現", scene: "hook-01", source: 0, fact: 0 }],
  origin: [{ claim: "1928 年 Hollis Marrow 申請專利", scene: "origin-01", source: 0, fact: 0 }, { claim: "照 Marrow 的回憶，點子來自淋濕的火車旅行", scene: "origin-02", source: 2, fact: 2 }],
  idea: [{ claim: "傘骨分三段，收起來剩三分之一長", scene: "idea-01", source: 0, fact: null }],
  engine: [{ claim: "Brellco 在 1954 年賣出第 100 萬把", scene: "engine-01", source: 1, fact: 1 }],
  turn: [],
  now: [{ claim: "2025 年折疊傘佔營收 62%", scene: "now-01", source: null, fact: 3 }],
};

/** The stand-in writer's answer for a chapter, from the ids it was handed. */
function chapterAnswer(key, payload, { nameInPrompt = false, extraShot = false } = {}) {
  const ids = [...payload.line_ids, ...(payload.current ? payload.current.scenes.flatMap((scene) => scene.lines.map((line) => line.id)) : [])];
  const take = () => ids.shift();
  const shots = TEXT[key].map((lines, index) => ({
    id: `${key}-${String(index + 1).padStart(2, "0")}`,
    template: "shot",
    data: { prompt: `${PROMPTS[key][index]}${nameInPrompt && index === 0 ? ", a Brellco shop sign above the door" : ""}`, camera: "slow push in", visual: "still" },
    lines: lines.map((text) => ({ id: take(), text })),
  }));
  if (extraShot) shots.push({ id: `${key}-03`, template: "shot", data: { prompt: "a quiet workshop at night, tools hanging on the wall, wide shot", camera: "drift", visual: "still" }, lines: [{ id: take(), text: "工坊裡還掛著當年的工具。" }] });
  if (key === "now") shots.push({ id: "now-outro", template: "outro", data: { title: "傘能折，是因為生活變了", cta: "參考資料在說明欄" }, lines: [{ id: take(), text: "所以折疊傘晚到，是在等生活追上它。" }] });
  return { title: TITLES[key], scenes: shots, claims: CLAIMS[key], lexicon_additions: { Hollis: null, Marrow: null, Brellco: null }, ...(key === "hook" ? { thumbnail_shot: "hook-02" } : {}) };
}

/** The stand-in checker: every row gets a verdict; the origin's attributed line is made more plainly Marrow's. */
function checkAnswer(payload) {
  const patch = {};
  for (const scene of payload.scenes) for (const line of scene.lines) if (line.text === "照 Marrow 的回憶，") patch[line.id] = "照 Marrow 自己的回憶，";
  const verdict = (row) => (row.fact === 3 ? "PLAN" : row.fact === 2 ? "ATTRIBUTED" : "CONFIRMED");
  return { patch, drop: [], claims: payload.claims.map((row) => ({ ...row, verdict: verdict(row), note: "段落裡有" })), report: `第 ${payload.chapter.number} 章逐條對過。` };
}

/**
 * The stand-in listener: in the hook, one line reworded and one whose year it changes (refused);
 * with the owner's note, the turn's closing line said more plainly.
 */
function listenAnswer(payload) {
  const lines = payload.scenes.flatMap((scene) => scene.lines);
  if (payload.owner_note) {
    const plain = lines.find((line) => line.text === "選一邊站。");
    return plain ? { patch: { [plain.id]: "只能選一邊站。" }, drop: [], edits: [] } : { patch: {}, drop: [], edits: [] };
  }
  if (payload.chapter.key !== "hook") return { patch: {}, drop: [], edits: [] };
  const first = lines.find((line) => line.text === "雨傘用了三千年。");
  const second = lines.find((line) => line.text.includes("1928"));
  return { patch: { ...(first ? { [first.id]: "雨傘已經用了三千年。" } : {}), ...(second ? { [second.id]: second.text.replace("1928", "1929") } : {}) }, drop: [], edits: [] };
}

// --- the site ------------------------------------------------------------------------------------

function storySite({ answers = {}, jobs = null, settings = {}, raw = {}, paused = () => false, series = SERIES, plannedEpisode = EPISODE, held = null } = {}) {
  const calls = { run: [], episodes: [], reports: [], pages: [], answers: [] };
  const projects = new Map();
  const stageJobs = new Map();
  const reviewsOf = (slug) => projects.get(slug) ?? projects.set(slug, []).get(slug);
  const queue = jobs ?? [{ kind: "episode", series, chapter_number: null, episode: plannedEpisode, previous: null, rewrites_left: 0, context: { series, setting: null, outline: null, chapter: null, chapter_number: null, episode: plannedEpisode, episodes: [{ ...plannedEpisode, beats: {} }], recaps: [], mysteries: [] } }];
  const current = {
    enabled: true, draft_interval_hours: 72, topics_per_run: 1, max_waiting_drafts: 3, topic_scope: ["AI"], topic_avoid: [], topic_from_site: true, topic_from_search: false,
    stage_models: {}, voice: { provider: "gemini", name: "Sulafat", style: "溫和的說書人語氣", model: null, rate: "+0%" }, target_minutes_min: 8, target_minutes_max: 12, caption_locales: [],
    max_drafts_per_month: 8, monthly_token_budget_millions: 20, max_verify_rounds: 3, max_retake_rounds: 2, auto_approve_audio: true, channel_stance: "",
    drama: { drama_enabled: true, style_preset: "cinematic-3d", subtitle_burn_in: true, music_enabled: false, character_voice_pool: [], series_script_gate: true }, ...settings,
  };
  const json = (body, status = 200) => Response.json(body, { status });
  const fetchImpl = async (url, init = {}) => {
    if (!url.startsWith(SITE)) {
      calls.pages.push(url);
      if (PDFS.has(url)) return new Response("%PDF-1.7", { status: 200, headers: { "content-type": "application/pdf" } });
      if (PAGES[url]) return new Response(PAGES[url], { status: 200, headers: { "content-type": "text/html; charset=utf-8" } });
      return new Response("gone", { status: 404, headers: { "content-type": "text/html" } });
    }
    const { pathname } = new URL(url);
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    const body = init.body ? JSON.parse(init.body) : null;
    if (pathname === "/api/video/automation/settings") return json(current);
    if (pathname === "/api/video/automation/videos") return json([]);
    if (pathname === "/api/video/automation/drama-requests/next") return json({ request: null });
    if (pathname === "/api/video/automation/series/messages/next") return json({ job: null });
    const answered = /^\/api\/video\/automation\/series\/messages\/([^/]+)\/answer$/.exec(pathname);
    if (answered) {
      calls.answers.push({ id: answered[1], ...body });
      return json({ reply: { id: "m2", body_md: body.reply_md }, revision: null });
    }
    if (pathname === "/api/video/automation/series/next") return json({ job: queue.shift() ?? null });
    const episode = /^\/api\/video\/automation\/series\/([a-z0-9-]+)\/episodes\/(\d+)\/(start|recap|done)$/.exec(pathname);
    if (episode) {
      calls.episodes.push({ series: episode[1], number: Number(episode[2]), action: episode[3], ...(body ?? {}) });
      if (episode[3] !== "start") return json({ number: Number(episode[2]), status: episode[3] === "done" ? "done" : "started" });
      // The server's contract (apps/api/app/video_automation/series.py start_episode): a story starts under its planned slug.
      if (body.slug !== plannedEpisode.slug) return json({ code: "video_series_story_slug", detail: `這個故事的影片代號是 ${plannedEpisode.slug}，不是 ${body.slug}` }, 409);
      // A limit that took hold after next advertised the story (#918): the start is refused.
      if (held) return json({ code: "video_series_story_held", detail: held }, 409);
      const started = { ...plannedEpisode, status: "started" };
      return json({ request: { id: "b0c1d2e3-0000-4000-8000-000000000001", premise: `品牌故事 第 1 集：${plannedEpisode.title}\n${plannedEpisode.logline}\nquestion: ${PLAN.question}`, title: `品牌故事 第 1 集 ${plannedEpisode.title}`, source_guide: null, style_preset: "custom", target_minutes: series.target_minutes, note: series.note, status: "started", slug: body.slug, series_slug: series.slug, episode_number: 1 }, episode: started, context: { series, setting: null, outline: null, chapter: null, chapter_number: null, chapter_range: null, episode: started, episodes: [{ ...started, beats: {} }], recaps: [], mysteries: [] } });
    }
    if (pathname === "/api/video/automation/run" || pathname === "/api/video/automation/run/jobs") {
      calls.run.push(body);
      if (paused(body)) return json({ code: "video_ai_subscription_paused", detail: "every Claude account is at its cap" }, 429);
      const key = body.variant ? `${body.stage}:${body.variant}` : body.stage;
      const answer = answers[key]?.(body);
      const text = raw[key]?.(body) ?? JSON.stringify(answer ?? {});
      const result = { text, provider: "anthropic", model: "claude-sonnet-5", input_tokens: 10, output_tokens: 5, usage: { tokens: 15, token_budget: 20_000_000, drafts: 0, draft_budget: 8, calls: 1, failed_calls: 0 } };
      if (pathname === "/api/video/automation/run") return json(result);
      // Pilot chapters use the production saved-job transport. Return its receipt shape so
      // the integration fixture exercises the same durable path without a paid provider.
      const id = `00000000-0000-4000-8000-${String(stageJobs.size + 1).padStart(12, "0")}`;
      const job = { id, request_key: body.request_key, request_hash: "a".repeat(64), input_hash: "b".repeat(64),
        provider: result.provider, model: result.model, status: "succeeded", result,
        error_code: null, error_detail: null, error_status: null, retry_after: null };
      stageJobs.set(id, job);
      return json(job);
    }
    const stageJob = /^\/api\/video\/automation\/run\/jobs\/([a-f0-9-]+)$/.exec(pathname);
    if (stageJob) return stageJobs.has(stageJob[1]) ? json(stageJobs.get(stageJob[1])) : json({ code: "not_found", detail: pathname }, 404);
    const match = /^\/api\/video\/reviews\/([a-z0-9-]+)(\/reviews)?$/.exec(pathname);
    if (match) {
      const [, slug, sub] = match;
      if (init.method === "PUT") {
        calls.reports.push({ slug, ...body });
        return json({ slug, reviews: reviewsOf(slug) });
      }
      if (sub && init.method === "POST") {
        const review = { id: `r${reviewsOf(slug).length + 1}`, status: "pending", choice: null, note: null, decided_at: null, created_at: new Date().toISOString(), ...body };
        reviewsOf(slug).unshift(review);
        return json(review);
      }
      return json({ slug, title: slug, stage: "x", checklist: [], youtube_video_id: null, reviews: reviewsOf(slug) });
    }
    return json({ code: "not_found", detail: pathname }, 404);
  };
  return { calls, fetchImpl, reviewsOf, settings: current };
}

function context(box, fetchImpl) {
  const clock = { now: Date.parse("2026-09-28T02:00:00Z") };
  const out = { stdout: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE },
      home: box.base,
      fetch: fetchImpl,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stdout += text) },
      now: () => new Date(clock.now),
      sleep: async (ms) => {
        clock.now += ms;
      },
      EXIT: { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 },
    },
  };
}

const smallRefs = { script_writing: "一句一個意思，唸得出來。", formats: "", channel: "Mokaair", showcase: { scenes: [] }, minimal: {}, drama: "the drama route", drama_example: {}, drama_brief: "# brief", series: "the series route" };

/** The storytelling panel's answer (core/narrative.mjs): every question yes unless `no` names one. */
const panelAnswer = (no = []) => ({ answers: NARRATIVE_PANEL.map((question) => ({ id: question.id, yes: !no.includes(question.id), evidence: "[h1] 一把傘。" })) });

const standardAnswers = (overrides = {}) => ({
  "writer:story": (body) => chapterAnswer(body.payload.chapter.key, body.payload),
  "verifier:story": (body) => checkAnswer(body.payload),
  "listener:story": (body) => listenAnswer(body.payload),
  // The merged story is read blind by the panel before the narration is recorded.
  "verifier:narrative": () => panelAnswer(),
  ...overrides,
});

/** A story's world: the site, the automation, the media stand-ins (tts writes a timeline of `seconds()` when set). */
function storyWorld({ answers = standardAnswers(), raw = {}, seconds = null, settings = {}, paused, jobs = null, series, episode = EPISODE, held = null, decide = () => ({ status: "approved" }) } = {}) {
  const box = sandbox();
  const site = storySite({ answers, raw, settings, paused, jobs, series, plannedEpisode: episode, held });
  const { ctx, out } = context(box, site.fetchImpl);
  const dir = path.join(box.root, "docs", "videos", episode.slug);
  const workdir = path.join(box.work, episode.slug);
  const runs = [];
  const lexicon = () => existsSync(path.join(dir, "story-lexicon", "current.json"))
    ? videoLexicon({ root: box.root, slug: episode.slug, workdir }).lexicon
    : readJson(path.join(box.root, "docs", "videos", "lexicon.json"));
  const video = () => readJson(path.join(dir, "video.json"));
  // The site decides these gates on arrival for a hands-off story, and what it approved is what review-pull records.
  const GATE_FILES = { audio: "timeline.json", storyboard: path.join("keyframes", "manifest.json"), final: "final.mp4", publish: path.join("upload", "metadata.json") };
  const write = (file, data) => {
    mkdirSync(path.dirname(path.join(workdir, file)), { recursive: true });
    writeFileSync(path.join(workdir, file), typeof data === "string" ? data : JSON.stringify(data));
  };
  ctx.runCommand = async (command) => {
    runs.push(command.join(" "));
    const [name] = command;
    const doc = existsSync(path.join(dir, "video.json")) ? video() : null;
    if (name === "tts") {
      if (seconds) writeTimeline(doc, lexicon(), workdir, seconds());
      else writeSyntheticNarration(doc, lexicon(), workdir);
      return { code: 0, out: "narration" };
    }
    if (name === "check-audio") return { code: 0, out: "every line passed" };
    if (name === "keyframes") {
      const picture = (id) => {
        const file = `keyframes/${id}-1.png`;
        write(file, `synthetic selected picture: ${id}`);
        return { file, sha256: sha(path.join(workdir, file)) };
      };
      const shots = Object.fromEntries(drawnShotScenes(doc).map((scene) => [scene.id, {
        ...picture(scene.id), needs_review: false, judge: { overall: 8, passed: true, problems: [] },
        ...(scene.data.end_frame?.prompt ? { end_frame: picture(`${scene.id}-end`) } : {}),
      }]));
      write(path.join("keyframes", "manifest.json"), { look_hash: lookHash(doc), visual_hash: visualHash(doc), shots });
      return { code: 0, out: `${Object.keys(shots).length} keyframes` };
    }
    if (name === "render") {
      write(path.join("frames", "manifest.json"), { visual_hash: visualHash(doc), speech_hash: speechHash(doc, lexicon()), subtitles_hash: subtitlesHash(doc), theme_hash: "t", scenes: [], subtitles: { style: "drama", blank: "frames/sub-blank.png", cues: [] }, thumbnail: null });
      return { code: 0, out: "rendered" };
    }
    if (name === "clips") {
      // Stills only: the manifest names each keyframe, and nothing is bought (media/clips.mjs).
      const keyframes = readJson(path.join(workdir, "keyframes", "manifest.json"));
      const shots = shotScenes(doc).map((scene) => ({ id: scene.id, ...keyframes.shots[scene.id] }));
      write(path.join("clips", "manifest.json"), { speech_hash: speechHash(doc, lexicon()), visual_hash: visualHash(doc), look_hash: lookHash(doc), clips_hash: clipsHash(shots), shots: Object.fromEntries(shots.map((shot) => [shot.id, { still: true, file: shot.file, sha256: shot.sha256 }])) });
      return { code: 0, out: "0 clips bought; every shot is a still" };
    }
    if (name === "assemble") {
      write("final.mp4", "final cut");
      const clips = readJson(path.join(workdir, "clips", "manifest.json"));
      write("checks.json", { ok: true, speech_hash: speechHash(doc, lexicon()), narration_sha256: readJson(path.join(workdir, "timeline.json")).audio_evidence.narration_sha256, visual_hash: visualHash(doc), look_hash: lookHash(doc), clips_hash: clips.clips_hash, subtitles_hash: subtitlesHash(doc), mix_hash: mixHash(doc), problems: [] });
      return { code: 0, out: "assembled" };
    }
    if (name === "captions") {
      write(path.join("captions", "manifest.json"), { speech_hash: speechHash(doc, lexicon()), locales: { "zh-TW": { file: "captions/zh-TW.srt" } } });
      return { code: 0, out: "captions written" };
    }
    if (name === "package") {
      write(path.join("upload", "metadata.json"), { final_sha256: sha(path.join(workdir, "final.mp4")), title: doc.youtube.title });
      return { code: 0, out: "package written" };
    }
    if (name === "review-push") {
      const gate = command[command.indexOf("--gate") + 1];
      if (GATE_FILES[gate]) site.reviewsOf(episode.slug).unshift({ id: `${gate}-${site.reviewsOf(episode.slug).length}`, gate, choice: null, note: `${gate}：依設定自動核准`, decided_at: "2026-09-28T03:00:00Z", content_sha256: sha(path.join(workdir, GATE_FILES[gate])), payload: {}, ...decide(gate) });
      return { code: 0, out: `${gate} submitted` };
    }
    if (name === "review-pull") {
      const { approve } = await import("../core/approvals.mjs");
      for (const review of site.reviewsOf(episode.slug).filter((each) => each.status === "approved" && GATE_FILES[each.gate])) {
        const file = path.join(workdir, GATE_FILES[review.gate]);
        if (existsSync(file) && sha(file) === review.content_sha256 && !readApprovals(workdir).approvals.some((entry) => entry.gate === review.gate && entry.sha256 === review.content_sha256)) await approve({ gate: review.gate, docDir: dir, workdir, note: review.note });
      }
      return { code: 0, out: "pulled" };
    }
    return { code: 0, out: `${name} stood in` };
  };
  const automation = new Automation(ctx, automationClient(ctx), site.settings);
  automation.refs = smallRefs;
  const state = () => automatedVideos(box.work).find((each) => each.slug === episode.slug);
  return { box, site, ctx, out, automation, runs, dir, workdir, state, video, lexicon };
}

/** timeline.json for `doc` whose narration runs about `seconds`, as tts would write it. */
function writeTimeline(doc, lexicon, workdir, seconds) {
  const estimated = estimatedSamples(doc);
  const first = buildTimeline(doc, estimated);
  // The pauses between lines stay as they are; the speech stretches to make up the rest.
  const speech = Object.values(estimated).reduce((sum, samples) => sum + samples, 0) / 1600;
  const factor = (seconds * 30 - (first.total_frames - speech)) / speech;
  const scaled = Object.fromEntries(Object.entries(estimated).map(([id, samples]) => [id, Math.max(1600, Math.round(samples * factor))]));
  mkdirSync(workdir, { recursive: true });
  writeAudioFixture({ ...buildTimeline(doc, scaled), speech_hash: speechHash(doc, lexicon) }, workdir);
}

async function steps(automation, count) {
  const lines = [];
  for (let index = 0; index < count; index++) lines.push(await automation.step());
  return lines;
}

// --- the numbers ----------------------------------------------------------------------------------

test("a 13-minute story is 3,250 characters over about 90 shots, the hook a 30 to 60 second condensation and engine the longest; the narration may run 11:30 to 15:30", () => {
  const budgets = chapterBudgets(13);
  assert.deepEqual(budgets.map((budget) => budget.key), CHAPTER_KEYS);
  assert.equal(budgets.reduce((sum, budget) => sum + budget.seconds, 0), 13 * 60, "the seconds add up to the target");
  assert.equal(budgets.reduce((sum, budget) => sum + budget.chars, 0), 3_250, "250 characters a minute");
  const shots = budgets.reduce((sum, budget) => sum + budget.shots, 0);
  assert.ok(shots >= 85 && shots <= 100, `about 90 shots (${shots})`);
  assert.equal(budgets[0].seconds, 45, "the hook is given the middle of the condensation's 30 to 60 seconds");
  assert.equal(budgets.reduce((best, budget) => (budget.seconds > best.seconds ? budget : best)).key, "engine");
  for (const budget of budgets) assert.ok(budget.seconds / budget.shots >= 6 && budget.seconds / budget.shots <= 12, `${budget.key}: a shot holds 6 to 12 seconds`);
  assert.deepEqual(lengthBand(13), [11 * 60 + 30, 15 * 60 + 30]);
  for (const minutes of [12, 14, 15]) assert.equal(chapterBudgets(minutes).reduce((sum, budget) => sum + budget.chars, 0), minutes * 250);
});

test("every story stage has its own prompt: the writer is told the length comes from the passages, the checker holds the script to the plan and converts calendars, the listener answers a patch", () => {
  assert.deepEqual(Object.keys(STORY_INSTRUCTIONS).sort(), ["listener:story", "verifier:story", "writer:story", "writer:story-fix"]);
  const writer = instructionsFor("writer", "drama", "", "story");
  assert.match(writer, /ONE chapter/);
  assert.match(writer, /beyond the plan is told from a passage you were\s+given, and the checker will look for it there/);
  assert.match(writer, /never\s+pad with generalities, never add what you remember/);
  assert.match(writer, /"caveats" are the plan's fact checker's orders/);
  assert.match(writer, /an official page, or on two independent reliable sources/);
  assert.match(writer, /no name of "names"\s+in any prompt/);
  assert.match(writer, /"no_more": true/);
  assert.doesNotMatch(writer, /No real living people, no real brands/, "a story is not the drama's fiction");
  const checker = instructionsFor("verifier", "drama", "", "story");
  assert.match(checker, /facts"\) are established/);
  assert.match(checker, /reviewer_only[\s\S]*do not look for it in\s+"sources"/);
  assert.match(checker, /昭和[\s\S]*民國 N 年 = 1911 \+ N[\s\S]*200 billion/);
  assert.match(checker, /"read" is "plan"/);
  assert.match(checker, /"patch"[\s\S]*"claims"/);
  assert.doesNotMatch(checker, /"video": <corrected video\.json/, "never the whole script");
  const listener = instructionsFor("listener", "drama", "", "story");
  assert.match(listener, /Return \{"patch"/);
  assert.match(instructionsFor("writer", "drama", "", "story-fix"), /PICTURES of a few shots/);
  assert.match(instructionsFor("writer", "drama", "", "story-fix"), /When\s+a target in "fix.targets" carries "prompt_budget_chars", that shot's prompt must be at most that\s+many characters/);
  assert.match(instructionsFor("writer", "drama", "講慢一點", "story"), /standing instructions[\s\S]*講慢一點$/, "the owner's standing drama instructions still end the prompt");
  assert.match(instructionsFor("writer", "drama"), /"format": "drama"/, "a drama without a variant is written as before");
});

// --- pages and passages -----------------------------------------------------------------------------

test("the worker's reader answers its other callers as before, and hands the whole page only to a caller that asks", async () => {
  const long = `<p>${"字".repeat(50_000)}</p><p>the figure is 1972</p>`;
  const fetchImpl = async () => new Response(long, { status: 200, headers: { "content-type": "text/html" } });
  const plain = await pageReader({ fetchImpl, sleep: async () => {} })("https://a.example/p");
  assert.deepEqual(Object.keys(plain).sort(), ["final_url", "ok", "status", "text", "title", "truncated", "url"]);
  assert.equal(plain.text.length, MAX_PAGE_CHARS);
  assert.equal(plain.truncated, true);
  assert.doesNotMatch(plain.text, /1972/);
  const whole = await pageReader({ fetchImpl, sleep: async () => {}, whole: true })("https://a.example/p");
  assert.equal(whole.text, plain.text, "the head is the same");
  assert.match(whole.whole, /the figure is 1972$/);
});

test("a fact's figure past the 40,000th character is found in the page's whole text, a year is found in its Japanese or Republic form, and a page with nothing found gives its head", () => {
  assert.deepEqual([...figuresIn("1,000,000 把、1954 年、US$3、２０２５年、62.5%")], ["1000000", "1954", "2025", "62.5"]);
  assert.ok(yearForms(1957).includes("昭和32年"));
  assert.ok(yearForms(1989).includes("平成元年") && yearForms(1989).includes("昭和64年"));
  assert.ok(yearForms(2025).includes("民國114年") && yearForms(2025).includes("114年"));
  const page = `${"x".repeat(45_000)} In 1954 the factory sold its 1,000,000th umbrella. ${"y".repeat(20_000)}`;
  const anchors = anchorsFor(["Brellco 在 1954 年賣出第 100 萬把"], ["Brellco"]);
  const cut = passagesOf(page, anchors);
  assert.equal(cut.passages.length, 1);
  assert.ok(cut.passages[0].at > 40_000, "the passage is where the figure is, not the head");
  assert.match(cut.passages[0].text, /In 1954 the factory sold its 1,000,000th umbrella/);
  assert.ok(cut.passages[0].text.length < 1_200);
  const japanese = passagesOf(`${"あ".repeat(10_000)}昭和29年に100万本目を販売した。${"い".repeat(10_000)}`, anchorsFor(["1954 年"]));
  assert.match(japanese.passages[0].text, /昭和29年に100万本目/);
  const nothing = passagesOf("z".repeat(20_000), anchorsFor(["1954 年"]));
  assert.equal(nothing.head, true);
  assert.equal(nothing.passages[0].at, 0);
  assert.equal(passagesOf("short page 1954", anchors).whole, true);
  assert.deepEqual(factChapters(PLAN), [["origin"], ["engine"], ["origin"], ["now"]], "each fact goes with the chapter whose point shares its figures and names");
});

test("a writer's chapter is made the worker's: stills only, narrator lines, handed-out ids, rows pointing at its scenes", () => {
  const ids = ["aa11", "bb22", "cc33", "dd44", "ee55"];
  const answer = {
    title: "起點",
    scenes: [
      { id: "x", template: "shot", data: { prompt: "a workshop", visual: "clip", characters: ["nobody"], end_frame: { prompt: "y" } }, lines: [{ id: "aa11", text: "一句。", speaker: "someone" }, { id: "zzzz", text: "兩句。" }] },
      { id: "origin-07", template: "shot", data: { prompt: "a train" }, lines: [{ id: "aa11", text: "三句。" }] },
    ],
    claims: [{ claim: "一件事", scene: "x", source: 9, fact: 1 }],
  };
  const read = readChapterAnswer(answer, { key: "origin", ids, sources: 3, facts: 2 });
  assert.equal(read.problem, undefined);
  const [first, second] = read.chapter.scenes;
  assert.equal(first.id, "origin-01", "a scene id that is not the chapter's is given one");
  assert.equal(second.id, "origin-07", "a scene id the writer gave in the chapter's form is kept");
  assert.deepEqual(first.data, { prompt: "a workshop", camera: "slow drift", visual: "still" });
  assert.deepEqual(first.lines.map((line) => line.id), ["aa11", "bb22"], "an id that was not handed out takes the next unused one");
  assert.equal(second.lines[0].id, "cc33", "a repeated id takes the next unused one");
  assert.equal("speaker" in first.lines[0], false);
  assert.deepEqual(read.chapter.claims, [{ claim: "一件事", scene: "origin-01", source: null, fact: 1 }]);
  assert.match(readChapterAnswer({ title: "t", scenes: [{ template: "title", lines: [] }] }, { key: "hook", ids }).problem, /a story's scene is a shot/);
  assert.match(readChapterAnswer({ title: "t", scenes: [{ template: "outro", data: {}, lines: [{ text: "x" }] }] }, { key: "idea", ids }).problem, /only the last chapter ends with an outro/);
  assert.deepEqual(readChapterAnswer({ no_more: true, reason: "段落沒有更多" }, { key: "idea", ids }), { noMore: "段落沒有更多" });
  const chapter = { key: "idea", scenes: [{ id: "idea-01", template: "shot", data: {}, lines: [{ id: "aa11", text: "有 1928 年。" }, { id: "bb22", text: "沒有數字。" }] }] };
  const patched = applyPatch(chapter, { patch: { aa11: "有 1929 年。", zz99: "外面的" }, drop: ["bb22"] }, { guard: (before, after) => (before.match(/\d+/g)?.join() === after.match(/\d+/g)?.join() ? [] : ["number changed"]) });
  assert.deepEqual([patched.changed, patched.dropped], [[], ["bb22"]]);
  assert.equal(patched.refused.length, 2);
  assert.match(applyPatch(chapter, { drop: ["aa11", "bb22"] }).refused.at(-1), /without a shot/, "a patch may not empty the chapter");
});

// --- the flow -------------------------------------------------------------------------------------------

test("the five-film and v2 pilot visual gate counts body illustrations and cards at exact scene paths", () => {
  const shot = (id) => ({ id, template: "shot" });
  const card = (id) => ({ id, template: "stat" });
  const bookend = (id, template) => ({ id, template });
  const slug = "story-five-lego-legoland";
  const look = { preset: "cute-mystery" };
  const sevenShots = Array.from({ length: 7 }, (_, index) => shot(`s${index}`));
  const sixShots = sevenShots.slice(0, 6);
  const boundary = [bookend("title", "title"), ...sevenShots, card("c1"), card("c2"), bookend("chapter", "chapter"), card("c3"), bookend("outro", "outro")];
  assert.deepEqual(cuteStoryVisualProblems({ slug, look, scenes: boundary }), [], "7/10 shots and three cards pass; chapter cards are excluded from the body");

  const failing = [bookend("title", "title"), ...sixShots, card("c1"), card("c2"), card("c3"), bookend("chapter", "chapter"), card("c4"), bookend("outro", "outro")];
  const problems = cuteStoryVisualProblems({ slug, look, scenes: failing });
  assert.deepEqual(problems.map((problem) => problem.path), ["scenes[11]", "scenes[11]"], "both errors name the offending card's original scene index");
  assert.match(problems[0].message, /6 of 10 body scenes.*60%.*at least 70%/);
  assert.match(problems[1].message, /4 cards in a row \(c1 → c2 → c3 → c4\)/, "a chapter card does not break the card run");
  assert.deepEqual(cuteStoryVisualProblems({ slug, look, scenes: [bookend("outro", "outro")] }).map((problem) => problem.path), ["scenes[0]"], "the body cannot be empty");
  assert.deepEqual(cuteStoryVisualProblems({ slug, look: { ...look, negative: "photorealistic" }, scenes: boundary }).map((problem) => problem.path), ["look"], "a look override blocks the five-story route");
  assert.deepEqual(cuteStoryVisualProblems({ slug, look: { preset: "custom", style: "cute" }, scenes: boundary }).map((problem) => problem.path), ["look"]);
  for (const pilot of ["story-rolling-suitcase-v2", "story-conveyor-belt-sushi-v2"]) {
    assert.deepEqual(cuteStoryVisualProblems({ slug: pilot, look, scenes: boundary }), [], `${pilot}: the boundary passes`);
    assert.deepEqual(cuteStoryVisualProblems({ slug: pilot, look, scenes: failing }).map((problem) => problem.path), ["scenes[11]", "scenes[11]"], `${pilot}: the preimage gate blocks bad visual pacing`);
    assert.deepEqual(cuteStoryVisualProblems({ slug: pilot, look: { ...look, style: "custom" }, scenes: boundary }).map((problem) => problem.path), ["look"]);
  }
  for (const legacy of [SLUG, "story-rolling-suitcase", "story-conveyor-belt-sushi"]) {
    assert.deepEqual(cuteStoryVisualProblems({ slug: legacy, scenes: failing }), [], `${legacy}: the original custom story route keeps its own rules`);
  }
});

test("a complete cute pilot script sends visual failures to the chapter before drawing keyframes", async () => {
  const series = { ...SERIES, slug: "brand-stories-curio-pilot-v2", target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const episode = { ...EPISODE, slug: "story-rolling-suitcase-v2" };
  const answers = standardAnswers({ "writer:story": (body) => {
    const chapter = chapterAnswer(body.payload.chapter.key, body.payload);
    chapter.scenes.forEach((scene, index) => { if (scene.template === "shot") scene.data.camera = index % 2 ? "slow pan left" : "slow push in"; });
    return chapter;
  } });
  const world = storyWorld({ series, episode, answers });
  await world.automation.step();
  const written = await steps(world.automation, 6);
  assert.match(written.at(-1), /six are merged into video\.json/, written.join("\n"));
  assert.equal(world.state().story.chapters.idea.lint, null, "the six unedited chapters pass");

  // Simulate a later saved-chapter edit. The writer currently writes only shots, but the merged
  // script must still refuse a card-heavy chapter before the paid keyframes stage.
  for (const key of ["origin", "idea"]) {
    const file = path.join(world.workdir, STORY_CHAPTERS_DIR, `${key}.json`);
    const chapter = readJson(file);
    for (const scene of chapter.scenes) scene.template = "stat";
    writeFileSync(file, JSON.stringify(chapter));
  }
  const result = await advanceStory(world.automation, world.state(), "script passes lint");
  assert.match(result, /merged story fails lint in/);
  const errors = world.state().story.chapters.idea.lint.join("\n");
  assert.match(errors, /scenes\[5\]: 8 of 12 body scenes are illustrated shots \(66%\)/);
  assert.match(errors, /scenes\[5\]: 4 cards in a row \(origin-01 → origin-02 → idea-01 → idea-02\)/);
  assert.equal(world.runs.some((command) => command.startsWith("keyframes ")), false);
});

test("the two pilot editorial reference hashes still match their independently PASS-reviewed Markdown", () => {
  for (const [slug, id] of [["story-rolling-suitcase-v2", "A01"], ["story-conveyor-belt-sushi-v2", "B18"]]) {
    const script = fileURLToPath(new URL(`../../../docs/videos/brand-stories-pilot-v2-20261015/scripts/${id}.md`, import.meta.url));
    const review = fileURLToPath(new URL(`../../../docs/videos/brand-stories-pilot-v2-20261015/scripts/reviews/${id}.md`, import.meta.url));
    const hash = sha(script);
    assert.equal(hash, PILOT_SCRIPT_REFERENCES[slug]);
    assert.match(readFileSync(review, "utf8"), new RegExp(`SHA-256 .${hash}.`));
    assert.match(readFileSync(review, "utf8"), /文字事實與敘事 PASS|逐字稿文字事實與敘事 PASS/);
  }
});

const pilotAnswers = () => standardAnswers({ "writer:story": (body) => {
  const chapter = chapterAnswer(body.payload.chapter.key, body.payload);
  chapter.scenes.forEach((scene, index) => { if (scene.template === "shot") scene.data.camera = index % 2 ? "slow pan left" : "slow push in"; });
  return chapter;
} });

test("a v2 pilot holds before TTS until an independent review binds the actual six chapters and reference", async () => {
  const slug = "story-rolling-suitcase-v2";
  const series = { ...SERIES, slug: "brand-stories-curio-pilot-v2", target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const episode = { ...EPISODE, slug };
  const world = storyWorld({ series, episode, answers: pilotAnswers() });
  const { automation, workdir } = world;
  const progress = [];
  for (let index = 0; index < 1 + 6 + 6 + 6; index++) {
    try { progress.push(await automation.step()); }
    catch (error) { throw new Error(`pilot step ${index + 1}: ${progress.join(" | ")}`, { cause: error }); }
  }
  assert.match(await automation.step(), /STOPPED_HOLD: .*script-review\.json is missing/);
  assert.equal(world.state().status, "blocked");
  assert.equal(world.state().blocked_kind, "pilot_script_review");
  assert.equal(readApprovals(workdir).approvals.some((entry) => entry.gate === "script"), false);
  assert.equal(world.runs.some((command) => command.startsWith("tts ")), false);

  const places = { slug, root: world.box.root, workdir };
  const receipt = {
    schema_version: 1,
    ...pilotScriptReviewEvidence(places),
    status: "PASS",
    reviewer_id: "editorial-reader-a01",
    independent: true,
    reviewed_at: "2026-10-15T00:00:00.000Z",
    checks: { reference_alignment: "PASS", factual_claims: "PASS", narrative: "PASS" },
  };
  const receiptFile = path.join(workdir, PILOT_SCRIPT_REVIEW_FILE);
  mkdirSync(path.dirname(receiptFile), { recursive: true });
  const saveReceipt = () => writeFileSync(receiptFile, JSON.stringify(receipt));
  assert.match(pilotScriptReviewProblem(places), /missing/);
  receipt.slug = "story-conveyor-belt-sushi-v2";
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /matching slug/);
  receipt.slug = slug;
  receipt.reviewer_id = "worker:story";
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /independent reviewer/);
  receipt.reviewer_id = "editorial-reader-a01";
  receipt.reference_script_sha256 = "0".repeat(64);
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /frozen independently reviewed Markdown/);
  receipt.reference_script_sha256 = PILOT_SCRIPT_REFERENCES[slug];
  receipt.files["script.md"] = "0".repeat(64);
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /script\.md is missing or changed/);
  receipt.files["script.md"] = sha(path.join(world.dir, "script.md"));
  saveReceipt();
  assert.equal(pilotScriptReviewProblem(places), null);

  // A newly signed script-review file cannot bless an old panel PASS under obsolete questions.
  const narrativeFile = path.join(workdir, "review", "narrative.json");
  const currentPanel = readFileSync(narrativeFile, "utf8");
  const legacyPanel = JSON.parse(currentPanel);
  delete legacyPanel.panel_rules_sha256;
  writeFileSync(narrativeFile, JSON.stringify(legacyPanel));
  receipt.narrative_review_sha256 = sha(narrativeFile);
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /stale under the current questions/);
  writeFileSync(narrativeFile, currentPanel);
  receipt.narrative_review_sha256 = sha(narrativeFile);
  saveReceipt();
  assert.equal(pilotScriptReviewProblem(places), null);

  const scriptFile = path.join(world.dir, "script.md");
  const originalScript = readFileSync(scriptFile, "utf8");
  writeFileSync(scriptFile, `${originalScript}\n手動加上的旁白。`);
  receipt.files["script.md"] = sha(scriptFile);
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /script\.md no longer matches the narration in video\.json/, "a reviewer cannot attest a detached text file as the worker's script");
  writeFileSync(scriptFile, originalScript);
  receipt.files["script.md"] = sha(scriptFile);
  saveReceipt();
  assert.equal(pilotScriptReviewProblem(places), null);

  // A second reader's new hashes cannot bless a detached chapter: the spoken text in the
  // chapter files must be the text that was actually merged into the video and screenplay.
  const hookFile = path.join(workdir, STORY_CHAPTERS_DIR, "hook.json");
  const originalHook = readFileSync(hookFile, "utf8");
  const changedHook = JSON.parse(originalHook);
  changedHook.scenes[0].lines[0].text = "審過章稿後才改掉的旁白。";
  writeFileSync(hookFile, JSON.stringify(changedHook));
  receipt.chapters.hook = sha(hookFile);
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /video\.json scenes no longer match the six reviewed chapter files/);
  changedHook.scenes[0].lines[0].text = JSON.parse(originalHook).scenes[0].lines[0].text;
  changedHook.scenes[0].data.prompt = "a different image prompt after the merged scene was reviewed";
  writeFileSync(hookFile, JSON.stringify(changedHook));
  receipt.chapters.hook = sha(hookFile);
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /video\.json scenes no longer match the six reviewed chapter files/);
  writeFileSync(hookFile, originalHook);
  receipt.chapters.hook = sha(hookFile);
  saveReceipt();
  assert.equal(pilotScriptReviewProblem(places), null);

  // A fresh receipt cannot approve a video that still publishes uncited plan research.
  const videoFile = path.join(world.dir, "video.json");
  const originalVideo = readFileSync(videoFile, "utf8");
  const videoWithExtraSource = JSON.parse(originalVideo);
  videoWithExtraSource.sources.push({ title: "Unused research", url: "https://example.test/uncited", checked_on: "2026-10-19" });
  writeFileSync(videoFile, JSON.stringify(videoWithExtraSource));
  receipt.files["video.json"] = sha(videoFile);
  saveReceipt();
  assert.match(pilotScriptReviewProblem(places), /A01 video\.json sources no longer match the effective claims/);
  writeFileSync(videoFile, originalVideo);
  receipt.files["video.json"] = sha(videoFile);
  saveReceipt();
  assert.equal(pilotScriptReviewProblem(places), null);

  // Normal non-scene metadata may be updated without changing the reviewed narration or shots.
  const videoWithId = JSON.parse(originalVideo);
  videoWithId.youtube.video_id = "test-video-id";
  writeFileSync(videoFile, JSON.stringify(videoWithId));
  receipt.files["video.json"] = sha(videoFile);
  saveReceipt();
  assert.equal(pilotScriptReviewProblem(places), null);
  writeFileSync(videoFile, originalVideo);
  receipt.files["video.json"] = sha(videoFile);
  saveReceipt();

  // The owner retries only after the second reader has signed the current worker artifact.
  const state = world.state();
  state.status = "active";
  delete state.blocked;
  delete state.blocked_kind;
  automation.persist(state);
  assert.match(await automation.step(), /screenplay is approved here/);
  assert.equal(world.runs.some((command) => command.startsWith("tts ")), false);
  assert.match(await automation.step(), /narration synthesized/);
  assert.equal(world.runs.filter((command) => command.startsWith("tts ")).length, 1);
});

test("a v2 pilot rechecks its review before downstream stages and holds when a chapter changes", async () => {
  const slug = "story-conveyor-belt-sushi-v2";
  const series = { ...SERIES, slug: "brand-stories-curio-pilot-v2", target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const world = storyWorld({ series, episode: { ...EPISODE, slug }, answers: pilotAnswers() });
  const progress = [];
  for (let index = 0; index < 1 + 6 + 6 + 6; index++) {
    try { progress.push(await world.automation.step()); }
    catch (error) { throw new Error(`pilot step ${index + 1}: ${progress.join(" | ")}`, { cause: error }); }
  }
  assert.match(await world.automation.step(), /STOPPED_HOLD/);
  const receipt = {
    schema_version: 1,
    ...pilotScriptReviewEvidence({ slug, root: world.box.root, workdir: world.workdir }),
    status: "PASS",
    reviewer_id: "independent-reader-b18",
    independent: true,
    reviewed_at: "2026-10-15T00:00:00.000Z",
    checks: { reference_alignment: "PASS", factual_claims: "PASS", narrative: "PASS" },
  };
  const file = path.join(world.workdir, PILOT_SCRIPT_REVIEW_FILE);
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, JSON.stringify(receipt));
  const state = world.state();
  state.status = "active";
  delete state.blocked;
  delete state.blocked_kind;
  world.automation.persist(state);
  assert.match(await world.automation.step(), /screenplay is approved here/);
  const chapterFile = path.join(world.workdir, STORY_CHAPTERS_DIR, "origin.json");
  writeFileSync(chapterFile, `${readFileSync(chapterFile, "utf8")} `);
  assert.match(await world.automation.step(), /STOPPED_HOLD: chapter origin is missing or changed/);
  assert.equal(world.runs.some((command) => command.startsWith("tts ")), false);
});

test("a flagged v2 pilot audio take waits for owner review instead of rewriting and paying TTS for unreviewed words", async () => {
  const slug = "story-rolling-suitcase-v2";
  const series = { ...SERIES, slug: "brand-stories-curio-pilot-v2", target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const world = storyWorld({
    series,
    episode: { ...EPISODE, slug },
    answers: pilotAnswers(),
    seconds: () => 450,
    settings: { max_retake_rounds: 1 },
    decide: (gate) => ({ status: gate === "audio" ? "pending" : "approved" }),
  });
  await steps(world.automation, 1 + 6 + 6 + 6);
  assert.match(await world.automation.step(), /STOPPED_HOLD/);
  const receipt = {
    schema_version: 1,
    ...pilotScriptReviewEvidence({ slug, root: world.box.root, workdir: world.workdir }),
    status: "PASS",
    reviewer_id: "independent-reader-a01",
    independent: true,
    reviewed_at: "2026-10-15T00:00:00.000Z",
    checks: { reference_alignment: "PASS", factual_claims: "PASS", narrative: "PASS" },
  };
  const receiptFile = path.join(world.workdir, PILOT_SCRIPT_REVIEW_FILE);
  mkdirSync(path.dirname(receiptFile), { recursive: true });
  writeFileSync(receiptFile, JSON.stringify(receipt));
  const state = world.state();
  state.status = "active";
  delete state.blocked;
  delete state.blocked_kind;
  world.automation.persist(state);
  assert.match(await world.automation.step(), /screenplay is approved here/);
  assert.match(await world.automation.step(), /narration synthesized/);

  const originalRun = world.ctx.runCommand;
  const flaggedId = world.video().scenes[0].lines[0].id;
  world.ctx.runCommand = async (command) => {
    const result = await originalRun(command);
    if (command[0] !== "check-audio") return result;
    const timeline = readJson(path.join(world.workdir, "timeline.json"));
    const entries = Object.fromEntries(timeline.lines.map((line) => [line.id, {
      match: line.id !== flaggedId,
      match_kind: line.id === flaggedId ? null : "exact",
      intended: "已審旁白",
      heard: line.id === flaggedId ? "Jev 聽成另一句" : "已審旁白",
      noul: line.id === flaggedId ? 0.2 : null,
      clip: line.audio_sha256.slice(0, 16),
    }]));
    mkdirSync(path.join(world.workdir, "review"), { recursive: true });
    writeFileSync(path.join(world.workdir, "review", "check.json"), JSON.stringify({ lines: entries }));
    writeFileSync(path.join(world.workdir, "review", "check-flags.json"), JSON.stringify({ slug, speech_hash: timeline.speech_hash, flags: [flaggedId], notes: { [flaggedId]: "Jev 仍標記" } }));
    return { code: 1, out: "one line still flagged" };
  };

  const checked = await world.automation.step();
  assert.match(checked, /narration checked \(some lines flagged\) and sent for review; pilot audio waits for owner review/);
  assert.equal(world.runs.filter((run) => run.startsWith("tts ") && run.includes("--redo")).length, 1, "only the same-script retake is paid");
  assert.equal(world.site.calls.run.filter((call) => call.stage === "listener" && call.variant === "rewrite").length, 0);
  assert.equal(world.site.reviewsOf(slug).find((review) => review.gate === "audio")?.status, "pending");
  assert.equal(pilotScriptReviewProblem({ slug, root: world.box.root, workdir: world.workdir }), null, "the approved script remains the spoken script");
  assert.equal(await world.automation.advance(world.state()), null, "the worker waits for the owner to judge the flagged take");

  const audioReview = world.site.reviewsOf(slug).find((review) => review.gate === "audio");
  audioReview.status = "rejected";
  audioReview.note = "這句改自然一點";
  assert.match(await world.automation.advance(world.state()), /the owner sent the narration back .*listener goes over the six chapters/);
  for (let index = 0; index < 6; index++) await world.automation.advance(world.state());
  assert.match(await world.automation.advance(world.state()), /STOPPED_HOLD: .*changed since the pilot script review/, "a chapter listener edit needs a new independent script receipt before TTS");
  assert.equal(world.runs.filter((run) => run.startsWith("tts ") && !run.includes("--redo")).length, 1);

  // The hold has a finite recovery: independently review the newly merged script, write its
  // current hashes, and explicitly retry. Only then may the new words reach TTS.
  Object.assign(receipt, pilotScriptReviewEvidence({ slug, root: world.box.root, workdir: world.workdir }));
  writeFileSync(receiptFile, JSON.stringify(receipt));
  const retry = world.state();
  retry.status = "active";
  delete retry.blocked;
  delete retry.blocked_kind;
  world.automation.persist(retry);
  assert.match(await world.automation.advance(world.state()), /screenplay is approved here/);
  assert.match(await world.automation.advance(world.state()), /narration synthesized/);
  assert.equal(world.runs.filter((run) => run.startsWith("tts ") && !run.includes("--redo")).length, 2);
});

test("A01 publishes only effective cited sources in plan order across partial and repeated merges", () => {
  const sources = Array.from({ length: 25 }, (_, index) => ({
    url: `https://source.example/${index}`, publisher: `Publisher ${index}`, checked: "2026-10-19",
  }));
  const plan = { ...PLAN, sources };
  const info = storySeriesFile({ series: SERIES, episode: EPISODE, plan, cast: [] });
  const cited = [0, 1, 2, 5, 6, 8, 11, 12, 13, 15, 16, 17, 18, 19, 21, 22, 23, 24];
  const chapters = Object.fromEntries(CHAPTER_KEYS.map((key, chapterIndex) => {
    const id = `${key}-01`;
    return [key, {
      key, title: key,
      scenes: [{ id, template: "shot", data: { prompt: "a suitcase in an airport" }, lines: [] }],
      claims: cited.filter((_, index) => index % CHAPTER_KEYS.length === chapterIndex)
        .map((source, index) => ({ id: `${key}${index}`, scene: id, source, verdict: "PENDING" })),
    }];
  }));
  chapters.hook.claims.push(
    { id: "not-found", scene: "hook-01", source: 3, verdict: "NOT FOUND" },
    { id: "orphan", scene: "hook-missing", source: 4, verdict: "CONFIRMED" },
    ...[null, -1, 1.5, "7", 25].map((source, index) => ({ id: `invalid-${index}`, scene: "hook-01", source, verdict: "PENDING" })),
  );
  const compose = (slug, current) => composeStory({ slug, info, chapters: current, voice: SERIES.voice, root: "." });
  const expected = cited.map((index) => ({ title: sources[index].publisher, url: sources[index].url, checked_on: sources[index].checked }));

  assert.deepEqual(compose("story-rolling-suitcase-v2", { hook: chapters.hook }).sources,
    chapters.hook.claims.slice(0, 3).map((row) => row.source).sort((a, b) => a - b).map((index) => expected[cited.indexOf(index)]),
    "a partial merge includes only its written chapter's effective citations");
  assert.deepEqual(compose("story-rolling-suitcase-v2", chapters).sources, expected, "the A01 25-source plan publishes its 18 cited entries");
  assert.deepEqual(compose("story-rolling-suitcase-v2", chapters).sources, expected, "repeating the merge cannot restore unused URLs");

  const revised = structuredClone(chapters);
  const removed = revised.now.claims.shift().source;
  assert.deepEqual(compose("story-rolling-suitcase-v2", revised).sources,
    expected.filter((source) => source.url !== sources[removed].url), "a rewritten chapter removes a citation that no current scene uses");
  assert.equal(compose("story-rolling-suitcase-v2", {}).sources.length, 0, "an unwritten A01 chapter cites nothing");
  assert.equal(compose("story-conveyor-belt-sushi-v2", chapters).sources.length, sources.length, "B18 keeps its existing source behavior");
  assert.equal(compose(SLUG, chapters).sources.length, sources.length, "ordinary stories keep their existing source behavior");
});

test("a plan's thumbnail.brand reaches the thumbnail in place of the tag, and leaves the pictures' hash alone", () => {
  const hook = { title: "開場", scenes: [{ id: "hook-01", template: "shot", data: { prompt: "a watch on a desk" }, lines: [] }], claims: [] };
  const compose = (thumbnail) => {
    const info = storySeriesFile({ series: SERIES, episode: EPISODE, plan: { ...PLAN, thumbnail }, cast: [] });
    return composeStory({ slug: SLUG, info, chapters: { hook }, voice: SERIES.voice, root: "." });
  };
  const plain = compose({ headline: "比車貴的錶", idea: "a watch" });
  assert.deepEqual(plain.thumbnail.data, { headline: "比車貴的錶", tag: "品牌故事", shot: "hook-01" }, "a plan without a brand keeps the tag alone");
  const branded = compose({ headline: "比車貴的錶", idea: "a watch", brand: " SEIKO " });
  assert.deepEqual(branded.thumbnail.data, { headline: "比車貴的錶", tag: "品牌故事", brand: "SEIKO", shot: "hook-01" });
  // The brand is drawn on thumbnail.jpg alone: adding it to a story already shot must not make
  // its keyframes, clips and assembly stale (they are bound to visualHash).
  assert.equal(visualHash(branded), visualHash(plain));
  assert.notEqual(visualHash(compose({ headline: "比電腦貴", idea: "a watch" })), visualHash(plain), "the headline still counts");
});

test("an existing A01 ten-minute merged script holds before TTS without rewriting reviewed files", async () => {
  const slug = "story-rolling-suitcase-v2";
  const series = { ...SERIES, slug: "brand-stories-curio-pilot-v2", target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const world = storyWorld({ series, episode: { ...EPISODE, slug }, answers: pilotAnswers(), seconds: () => 450 });
  await steps(world.automation, 1 + 6 + 6 + 6);
  const videoFile = path.join(world.dir, "video.json");
  const oldVideo = { ...world.video(), target_minutes: [9, 11] };
  writeFileSync(videoFile, JSON.stringify(oldVideo));
  const originalVideo = readFileSync(videoFile);
  const chapterFiles = CHAPTER_KEYS.map((key) => path.join(world.workdir, STORY_CHAPTERS_DIR, `${key}.json`));
  const originalChapters = chapterFiles.map((file) => readFileSync(file));
  const receipt = {
    schema_version: 1,
    ...pilotScriptReviewEvidence({ slug, root: world.box.root, workdir: world.workdir }),
    status: "PASS", reviewer_id: "independent-reader-a01", independent: true,
    reviewed_at: "2026-10-15T00:00:00.000Z",
    checks: { reference_alignment: "PASS", factual_claims: "PASS", narrative: "PASS" },
  };
  const receiptFile = path.join(world.workdir, PILOT_SCRIPT_REVIEW_FILE);
  mkdirSync(path.dirname(receiptFile), { recursive: true });
  writeFileSync(receiptFile, JSON.stringify(receipt));
  assert.match(pilotScriptReviewProblem({ slug, root: world.box.root, workdir: world.workdir }), /legacy duration target/);
  const state = world.state();
  state.story.chapters.origin.lint = ["the old chapter needs a fix"];
  world.automation.persist(state);
  const writerCalls = world.site.calls.run.filter((call) => call.stage === "writer").length;
  assert.match(await world.automation.step(), /STOPPED_HOLD: A01's existing video.json has a legacy or unreadable duration target/);
  assert.equal(world.site.calls.run.filter((call) => call.stage === "writer").length, writerCalls,
    "a legacy merged script holds before even a pending chapter lint fix calls the model");
  assert.deepEqual(readFileSync(videoFile), originalVideo, "ordinary retry preserves the old merged script");
  chapterFiles.forEach((file, index) => assert.deepEqual(readFileSync(file), originalChapters[index], `${file} is preserved`));
  assert.equal(world.runs.some((run) => run.startsWith("tts ")), false);

  unlinkSync(chapterFiles.at(-1));
  const incomplete = world.state();
  incomplete.status = "active";
  delete incomplete.blocked;
  delete incomplete.blocked_kind;
  world.automation.persist(incomplete);
  assert.match(await world.automation.step(), /STOPPED_HOLD: A01 has an existing video.json but chapter files are missing \(now\)/);
  assert.equal(world.site.calls.run.filter((call) => call.stage === "writer").length, writerCalls,
    "a missing chapter cannot trigger a writer call while the old merged script exists");
  assert.deepEqual(readFileSync(videoFile), originalVideo);
  chapterFiles.slice(0, -1).forEach((file, index) => assert.deepEqual(readFileSync(file), originalChapters[index]));

  writeFileSync(videoFile, JSON.stringify({ ...oldVideo, target_minutes: [7, 8] }));
  const compactButIncomplete = readFileSync(videoFile);
  const next = world.state();
  next.status = "active";
  delete next.blocked;
  delete next.blocked_kind;
  world.automation.persist(next);
  assert.match(await world.automation.step(), /STOPPED_HOLD: A01 has an existing video.json but chapter files are missing \(now\)/);
  assert.equal(world.site.calls.run.filter((call) => call.stage === "writer").length, writerCalls,
    "a current target cannot auto-recreate a missing reviewed chapter either");
  assert.deepEqual(readFileSync(videoFile), compactButIncomplete);
});

test("the ten-minute preset is preserved by the story file and video composer", () => {
  const cute = { ...SERIES, target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const info = storySeriesFile({ series: cute, episode: EPISODE, plan: PLAN, cast: [] });
  assert.deepEqual(info.look, { preset: "cute-mystery" });
  assert.equal(info.image_model, "image-01");
  assert.match(storyBrief({ episode: EPISODE, plan: PLAN, cast: [], look: info.look }), /## 問題\n[^\n]+\n\n## 一句答案\n[^\n]+/);
  assert.doesNotMatch(storyBrief({ episode: EPISODE, plan: PLAN, cast: [], look: LOOK }), /## 問題\n|## 一句答案\n/, "the original custom brief keeps its drama sections");
  const cuteBudgets = chapterBudgets(10, info.look);
  assert.equal(cuteBudgets.reduce((seconds, chapter) => seconds + chapter.seconds, 0), 600);
  assert.equal(cuteBudgets.reduce((shots, chapter) => shots + chapter.shots, 0), 80, "7.5 seconds per picture gives 75–120 illustrations");
  assert.equal(chapterBudgets(13).reduce((shots, chapter) => shots + chapter.shots, 0), 90, "the original 13-minute route keeps its pace");
  assert.deepEqual(lengthBand(10, info.look), [540, 660]);
  assert.deepEqual(lengthBand(13), [690, 930]);
  const video = composeStory({ slug: SLUG, info, chapters: {}, voice: SERIES.voice, root: "." });
  assert.deepEqual(video.look, { preset: "cute-mystery" });
  assert.deepEqual(video.target_minutes, [9, 11]);
  assert.deepEqual(video.subtitles, { burn_in: false, style: "drama" }, "new brand stories use switchable zh-TW CC");
});

test("only A01 writes to an eight-minute budget while the shared pilot series stays ten", async () => {
  const series = { ...SERIES, slug: "brand-stories-curio-pilot-v2", target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const episode = { ...EPISODE, slug: "story-rolling-suitcase-v2" };
  const info = storySeriesFile({ series, episode, plan: PLAN, cast: [] });
  assert.equal(info.target_minutes, 10, "the series snapshot keeps the other episodes at ten minutes");
  assert.equal(effectiveStoryMinutes(episode.slug, info), 8);
  assert.deepEqual(effectiveStoryLengthBand(episode.slug, info), [420, 480]);
  const compact = chapterBudgets(8, info.look, { compactA01: true });
  assert.equal(compact.reduce((sum, chapter) => sum + chapter.seconds, 0), 480);
  assert.equal(compact.reduce((sum, chapter) => sum + chapter.chars, 0), 8 * 250);
  assert.equal(compact.reduce((sum, chapter) => sum + chapter.shots, 0), 64,
    "A01 keeps the cute story's 7.5-second illustration pace");
  assert.deepEqual(composeStory({ slug: episode.slug, info, chapters: {}, voice: SERIES.voice, root: "." }).target_minutes, [7, 8]);

  for (const other of [
    { slug: "story-conveyor-belt-sushi-v2", info: { ...info, episode: 2 } },
    { slug: episode.slug, info: { ...info, slug: "brand-stories-five-v2" } },
    { slug: episode.slug, info: { ...info, look: { preset: "custom" } } },
  ]) {
    assert.equal(effectiveStoryMinutes(other.slug, other.info), 10);
    assert.deepEqual(effectiveStoryLengthBand(other.slug, other.info),
      other.info.look.preset === "cute-mystery" ? [540, 660] : [510, 750]);
    assert.deepEqual(composeStory({ slug: other.slug, info: other.info, chapters: {}, voice: SERIES.voice, root: "." }).target_minutes,
      other.info.look.preset === "cute-mystery" ? [9, 11] : [9, 12]);
  }

  const world = storyWorld({ series, episode, answers: pilotAnswers() });
  assert.match(await world.automation.step(), /^story brand-stories-curio-pilot-v2:/);
  assert.equal(readJson(path.join(world.dir, "series.json")).target_minutes, 10);
  assert.equal(world.state().target_minutes, 8);
  await steps(world.automation, 2);
  const origin = world.site.calls.run.find((call) => call.stage === "writer" && call.payload.chapter.key === "origin");
  assert.equal(origin.payload.target_minutes, 8,
    "the writer payload explicitly overrides the generic cute-story ten-minute prompt");
  assert.deepEqual(origin.payload.episode_length.measured_narration_seconds, [420, 480]);
  assert.match(origin.payload.episode_length.owner_decision, /in place of the generic cute-mystery ten-minute example/);
  assert.deepEqual(origin.payload.chapter.budget, {
    seconds: compact[1].seconds, chars: compact[1].chars, shots: compact[1].shots,
  });
  const written = await steps(world.automation, 4);
  assert.match(written.at(-1), /six are merged into video\.json/, written.join("\n"));
  assert.deepEqual(world.video().target_minutes, [7, 8],
    "a fresh A01 with no pre-existing merged script reaches the compact six-chapter output");
});

test("a ten-minute story carries the exact MiniMax cute look from series to video", async () => {
  const cute = { ...SERIES, target_minutes: 10, image_model: "image-01", look: { preset: "cute-mystery" } };
  const answers = standardAnswers({ "writer:story": (body) => {
    const chapter = chapterAnswer(body.payload.chapter.key, body.payload);
    chapter.scenes.forEach((scene, index) => { if (scene.template === "shot") scene.data.camera = index % 2 ? "slow pan left" : "slow push in"; });
    return chapter;
  } });
  const world = storyWorld({ series: cute, answers });
  assert.match(await world.automation.step(), /^story brand-stories:/);
  const info = readJson(path.join(world.dir, "series.json"));
  assert.equal(info.target_minutes, 10);
  assert.equal(info.image_model, "image-01");
  assert.deepEqual(info.look, { preset: "cute-mystery" });
  const brief = readFileSync(path.join(world.dir, "brief.md"), "utf8");
  assert.match(brief, /## 問題\n[^\n]+\n\n## 一句答案\n[^\n]+/);
  assert.equal(world.state().style_preset, "custom", "the six-chapter story writer stays in use");
  assert.equal(world.state().target_minutes, 10);
  const written = await steps(world.automation, 6);
  assert.match(written.at(-1), /six are merged into video\.json/, written.join("\n"));
  const video = world.video();
  assert.deepEqual(video.look, { preset: "cute-mystery" });
  assert.deepEqual(video.target_minutes, [9, 11]);
  assert.equal(video.category, "story");
  assert.equal(video.subtitles.burn_in, false, "the merged script keeps zh-TW captions switchable");
  assert.equal(world.site.calls.run.filter((call) => call.stage === "writer").length, 6);
});

test("a story goes from the site's job to its first media step: started from its plan, written, checked and heard a chapter a call, the script gate approved here, then tts", async () => {
  const world = storyWorld();
  const { automation, site, dir, workdir, state } = world;

  // Started: the planned slug, series.json as lint wants it for a story, brief.md, the outline approved here.
  assert.match(await automation.step(), /^story brand-stories: story-folding-umbrella \(A90\) started from its plan/);
  assert.deepEqual(site.calls.episodes, [{ series: "brand-stories", number: 1, action: "start", slug: SLUG }], "the video slug is the plan's, not <series>-e001");
  const info = readJson(path.join(dir, "series.json"));
  assert.equal(info.kind, "story");
  assert.deepEqual(info.names, PLAN.names);
  assert.deepEqual([info.slug, info.episode, info.chapter, info.visual_tier, info.compilation], ["brand-stories", 1, 1, "stills", false]);
  assert.deepEqual(info.characters, []);
  assert.deepEqual(info.look, LOOK);
  assert.equal(info.image_model, "gemini-3.1-flash-image");
  assert.equal(info.plan.id, "A90");
  const brief = readFileSync(path.join(dir, "brief.md"), "utf8");
  assert.match(brief, /## 故事前提[\s\S]*## 角色\n沒有反覆出場的角色[\s\S]*## 站主觀點[\s\S]*## 大綱\n\n### 選項 A：折疊傘等了三千年/);
  assert.match(brief, /## 查核者的注意事項\nMarrow 是否在世未能確認/);
  assert.equal(readApprovals(workdir).approvals.find((entry) => entry.gate === "outline").note, OUTLINE_NOTE);
  assert.deepEqual(state().series, { slug: "brand-stories", episode: 1, chapter: 1, kind: "story", visual_tier: "stills", compilation: false, hands_off: true });
  assert.equal(state().category, "story", "a brand story is filed as one on /admin/videos");
  assert.equal(site.calls.reports[0].category, "story", "the very first report files it, before video.json exists");
  assert.equal(site.calls.reports.at(-1).series_slug, "brand-stories");
  assert.equal(site.calls.run.length, 0, "starting costs no model call");

  // Written a chapter a call; the sixth merges the script and lint passes.
  const written = await steps(automation, 6);
  written.slice(0, 5).forEach((line, index) => assert.match(line, new RegExp(`chapter ${index + 1}/6 \\(${CHAPTER_KEYS[index]}\\) written: 2 shots`)));
  assert.match(written[5], /chapter 6\/6 \(now\) written: 2 shots.*the six are merged into video\.json and claims\.md and the script passes lint/);
  const writers = site.calls.run.filter((call) => call.stage === "writer");
  assert.equal(writers.length, 6);
  const hook = writers[0].payload;
  assert.equal(hook.chapter.key, "hook");
  assert.equal(hook.chapter.point, POINTS.hook);
  assert.deepEqual(hook.chapter.budget, { seconds: 45, chars: 188, shots: 5 });
  assert.equal(hook.plan.chapters.length, 6, "every point, for context");
  assert.deepEqual(hook.facts.map((fact) => [fact.index, fact.attributed ?? false, fact.reviewer_only ?? false]), [[0, false, false], [1, false, false], [2, true, false], [3, false, true]]);
  assert.equal(hook.caveats, PLAN.caveats);
  assert.deepEqual(hook.look, LOOK);
  assert.deepEqual(hook.names, PLAN.names);
  assert.ok(hook.story_rules.some((rule) => rule.id === "names"));
  assert.deepEqual(hook.previous_lines, []);
  assert.ok(hook.line_ids.length >= 12);
  const origin = writers[1].payload;
  assert.deepEqual(origin.previous_lines, ["雨傘用了三千年。", "為什麼到 1928 年才折得進口袋？", "這一集從一趟淋雨的火車講起。", "看一副傘骨怎麼變成一門生意。"], "the last sentences of the chapter before");
  const engine = writers[3].payload;
  const museum = engine.sources.find((source) => source.url === LONG_PAGE);
  assert.ok(museum.passages.some((passage) => passage.at > 40_000 && /1954 the factory sold its 1,000,000th/.test(passage.text)), "the writer gets the passage past the reader's first 40,000 characters");
  assert.equal(engine.sources.find((source) => source.index === 3).read, "plan", "a PDF is the plan's supports line");
  const video = world.video();
  assert.equal(video.format, "drama");
  assert.deepEqual(video.series, { slug: "brand-stories", episode: 1, chapter: 1 });
  assert.deepEqual(video.characters, []);
  assert.ok(video.scenes.filter((scene) => scene.template === "shot").every((scene) => scene.data.visual === "still"));
  assert.deepEqual(video.scenes.filter((scene) => scene.chapter).map((scene) => scene.chapter), CHAPTER_KEYS.map((key) => TITLES[key]));
  assert.equal(video.scenes.at(-1).id, "now-outro");
  assert.equal(video.thumbnail.data.shot, "hook-02");
  assert.equal(video.look.preset, "custom");
  assert.equal(video.look.style, LOOK.style);
  assert.equal(video.youtube.category_id, 27);
  assert.equal(video.youtube.title, EPISODE.title);
  assert.deepEqual(video.sources.map((source) => source.url), PLAN.sources.map((source) => source.url));
  assert.equal(new Set(storyLineIds(Object.fromEntries(CHAPTER_KEYS.map((key) => [key, readChapter(automation, state(), key)])))).size, [...eachLine(video)].length, "no line id repeats across the chapters");
  assert.ok(existsSync(path.join(dir, "claims.md")));
  let status = await pipelineStatus({ slug: SLUG, root: world.box.root, workdir });
  assert.equal(status.next.id, "fact-checked");
  assert.equal(status.lint.errors.length, 0);

  // Checked a chapter a call, by a fresh session: the passage past 40,000 characters, a PDF as its supports line, a reviewer_only fact with no page.
  const checked = await steps(automation, 6);
  checked.forEach((line, index) => assert.match(line, new RegExp(`chapter ${CHAPTER_KEYS[index]} checked \\(round 1\\)`)));
  assert.match(checked[5], /every chapter is checked \(verify-1\.md\)/);
  const checkers = site.calls.run.filter((call) => call.stage === "verifier");
  assert.equal(checkers.length, 6);
  const engineCheck = checkers[3].payload;
  assert.deepEqual(engineCheck.scenes.map((scene) => scene.id), ["engine-01", "engine-02"]);
  assert.ok(!("prompt" in engineCheck.scenes[0]), "the checker reads the lines, not the pictures");
  const page = engineCheck.sources.find((source) => source.url === LONG_PAGE);
  assert.equal(page.read, "now");
  assert.ok(page.passages.some((passage) => passage.at > 40_000 && /In 1954 the factory sold its 1,000,000th folding umbrella/.test(passage.text)), "the checker gets the passage around the fact's figures");
  assert.ok(page.passages.every((passage) => passage.text.length < 2_000), "the passage, not the page");
  const pdf = engineCheck.sources.find((source) => source.index === 3);
  assert.equal(pdf.read, "plan");
  assert.equal(pdf.supports, PLAN.sources[3].supports);
  assert.match(pdf.note, /不是這次讀的/);
  assert.equal(pdf.passages, undefined);
  const nowCheck = checkers[5].payload;
  const planOnly = nowCheck.facts.find((fact) => fact.index === 3);
  assert.equal(planOnly.reviewer_only, true);
  assert.match(planOnly.note, /照企劃的寫法核對/);
  assert.equal(nowCheck.sources.some((source) => source.index === 4), false, "a reviewer_only fact reaches the checker with no page");
  assert.ok(existsSync(path.join(dir, "verify-1.md")));
  assert.match(readFileSync(path.join(dir, "verify-1.md"), "utf8"), /\| n1 \| 2025 年折疊傘佔營收 62% \| now-01 \|  \| PLAN \|/);
  assert.match(readChapter(automation, state(), "origin").scenes[1].lines[0].text, /照 Marrow 自己的回憶/, "the checker's patch is applied to the line it names");
  assert.equal(state().verified, true);

  // Heard a chapter a call: a patch; a change of a year is refused.
  const heard = await steps(automation, 6);
  assert.match(heard[0], /chapter hook heard: 1 lines reworded, 0 dropped, 1 edits refused/);
  assert.equal(readChapter(automation, state(), "hook").scenes[0].lines[0].text, "雨傘已經用了三千年。");
  assert.match(readChapter(automation, state(), "hook").scenes[0].lines[1].text, /1928/);
  assert.ok(state().notes.some((note) => /listener's edit of hook dropped: .*number/.test(note)));
  assert.equal(state().listener_done, true);

  // An old PASS bound to these very words cannot waive the current blind panel questions.
  const panelFile = path.join(workdir, "review", "narrative.json");
  mkdirSync(path.dirname(panelFile), { recursive: true });
  writeFileSync(panelFile, JSON.stringify({
    ...scriptCheckBinding(world.video()), round: 0, passed: true,
    answers: [], failed: [], advisory: [],
  }));

  // No script gate for a story: approved here with the reason; nothing went to the owner.
  assert.match(await automation.step(), /a story has no script gate; the screenplay is approved here/);
  assert.equal(readJson(panelFile).panel_rules_sha256, PANEL_RULES_SHA256);
  assert.equal(readApprovals(workdir).approvals.find((entry) => entry.gate === "script").note, SCRIPT_NOTE);
  assert.ok(existsSync(path.join(dir, "script.md")));
  assert.equal(world.runs.length, 0, "no media command and no review before the script is approved");

  // The first media step: a narrator-only story has no look to draw, so tts.
  assert.match(await automation.step(), /narration synthesized/);
  assert.deepEqual(world.runs, [`tts --slug ${SLUG}`]);
  status = await pipelineStatus({ slug: SLUG, root: world.box.root, workdir });
  assert.equal(status.steps.some((step) => step.id === "look generated"), false);

  // Twenty model calls, each under its own variant (never counted as a draft): six a chapter for
  // the writer, the checker and the listener, then the storytelling panel's two readers on the merged story.
  assert.equal(site.calls.run.length, 20);
  assert.deepEqual(site.calls.run.map((call) => `${call.stage}:${call.variant}`), [...Array(6).fill("writer:story"), ...Array(6).fill("verifier:story"), ...Array(6).fill("listener:story"), "verifier:narrative", "verifier:narrative"]);
  for (const call of site.calls.run) {
    assert.equal(call.format, "drama");
    assert.ok(call.max_output_tokens <= 32_000);
    assert.ok(call.instructions.length <= 60_000);
    assert.ok(JSON.stringify(call.payload).length < 100_000, `a ${call.stage} payload fits the relay`);
  }
  assert.equal(site.calls.run.some((call) => call.variant === "recap"), false);
});

test("past the script, a story takes the drama's own steps to the upload: Jev's check, keyframes, the storyboard the site decides, stills for clips, no recap, and the episode reported done", async () => {
  const world = storyWorld({ seconds: () => 780 });
  const { automation, site, state, runs } = world;
  await steps(automation, 1 + 6 + 6 + 6 + 1);
  assert.match(await automation.step(), /narration synthesized/);
  assert.match(await automation.step(), /narration checked \(Jev passed every line\) and sent for review/);
  assert.equal(state().story.length.seconds, 780, "the length was measured before Jev was asked");
  assert.match(await automation.step(), /keyframes done/);
  assert.match(await automation.step(), /storyboard sent to \/admin\/videos/);
  assert.match(await automation.step(), /approved the storyboard/);
  assert.match(await automation.step(), /frames rendered/);
  assert.match(await automation.step(), /clips done/);
  assert.match(await automation.step(), /video assembled/);
  assert.match(await automation.step(), /captions written/);
  assert.match(await automation.step(), /final sent to \/admin\/videos/);
  assert.match(await automation.step(), /the final is approved/);
  assert.match(await automation.step(), /upload package written/);
  assert.match(await automation.step(), /publish confirmation sent to \/admin\/videos/);
  assert.match(await automation.step(), /the upload is confirmed/);
  assert.equal(state().status, "done");
  assert.deepEqual(site.calls.episodes.map((each) => each.action), ["start", "done"], "the site hears the story is cleared for upload");
  assert.equal(site.calls.run.some((call) => call.variant === "recap" || !call.variant), false, "no recap, and every model call a story's own");
  assert.equal(runs.some((run) => run.startsWith("look ")), false, "no cast, no character sheets");
  assert.equal(runs.some((run) => run.startsWith("music ")), false, "music is off on the settings tab");
  assert.equal(site.reviewsOf(SLUG).some((review) => review.gate === "script" || review.gate === "outline"), false, "neither the outline nor the script went to the owner");

  const panelFile = path.join(world.workdir, "review", "narrative.json");
  const oldPanel = readJson(panelFile);
  delete oldPanel.panel_rules_sha256;
  writeFileSync(panelFile, JSON.stringify(oldPanel));
  const before = [runs.length, site.calls.run.length];
  await automation.move(state(), new Map());
  assert.equal(state().status, "done");
  assert.deepEqual([runs.length, site.calls.run.length], before, "a finished upload is not restarted or charged after panel rules move");
});

test("a loop one chapter plants and a later one pays off survives into the merged script", async () => {
  // A story is written a chapter a call, so the chapter that plants a hook cannot write its payoff
  // and the chapter that pays it does not own the setup line. Both halves used to be thrown away —
  // the planting chapter's for having no payoff, the paying chapter's for a setup that is not one
  // of its own lines — so every cross-chapter loop vanished from video.json and lint then warned
  // that the story had none (PR #1478 review, 2026-10-13). A loop inside one chapter is the weak
  // kind; these are the ones the rules ask for.
  let planted = null;
  let open = null;
  const world = storyWorld({
    answers: standardAnswers({
      "writer:story": (body) => {
        const answer = chapterAnswer(body.payload.chapter.key, body.payload);
        if (body.payload.chapter.key === "hook") {
          planted = answer.scenes[0].lines[0].id;
          return { ...answer, loops: [{ setup: planted, what: "那把傘為什麼等了三千年" }] };
        }
        if (body.payload.chapter.key === "now") {
          // The writer learns what is still hanging from its payload, not from the test.
          open = body.payload.loops_open;
          const hanging = open[0];
          const last = answer.scenes.at(-1).lines.at(-1).id;
          return { ...answer, loops: [{ setup: hanging.setup, payoff: last, what: hanging.what }] };
        }
        return answer;
      },
    }),
  });
  const { automation, video } = world;
  await steps(automation, 20);
  const doc = video();
  assert.ok(doc, "the script was merged");
  assert.deepEqual(open, [{ setup: planted, what: "那把傘為什麼等了三千年", chapter: "hook" }], "the later chapter was told the hook was still hanging");
  assert.equal(doc.loops.length, 1, "one loop, not two halves and not none");
  const [loop] = doc.loops;
  assert.equal(loop.setup, planted, "the setup is the line the hook planted");
  assert.equal(loop.what, "那把傘為什麼等了三千年");
  const order = new Map(doc.scenes.flatMap((scene) => scene.lines).map((line, index) => [line.id, index]));
  assert.ok(order.get(loop.payoff) > order.get(loop.setup), "and the payoff is spoken after it");
  assert.ok(order.get(loop.setup) < 5, "the setup is in the opening chapter");
});

test("a story's storytelling panel asks two readers: a question fails only when both say no, a yes with no line quoted is no yes, and a reader that fails keeps nothing", async () => {
  // Reader 1 fails no_spoiler and payoffs, reader 2 no_spoiler alone; in round 2 reader 2 passes it.
  let round = 0;
  const readers = (body) => {
    if (body.payload.reader === 1) round += 1;
    if (body.payload.reader === 1) return panelAnswer(["no_spoiler", "payoffs"]);
    return panelAnswer(round === 1 ? ["no_spoiler"] : []);
  };
  const world = storyWorld({ answers: standardAnswers({ "verifier:narrative": readers }) });
  const { automation, site, state, workdir } = world;
  await steps(automation, 1 + 6 + 6 + 6);
  assert.match(await automation.step(), /the storytelling panel sent the narration back \(round 1: no_spoiler\); the listener goes over the six chapters/);
  const [first, second] = site.calls.run.slice(-2);
  assert.deepEqual([first, second].map((call) => [`${call.stage}:${call.variant}`, call.payload.reader]), [["verifier:narrative", 1], ["verifier:narrative", 2]]);
  assert.equal(second.payload.narration, first.payload.narration, "both readers read the same script");
  assert.deepEqual(second.payload.questions, first.payload.questions);
  assert.equal(second.instructions, first.instructions);
  const panelFile = path.join(workdir, "review", "narrative.json");
  let record = readJson(panelFile);
  assert.deepEqual([record.passed, record.round, record.failed], [false, 1, ["no_spoiler"]]);
  assert.deepEqual(record.readers.map((reader) => reader.failed), [["no_spoiler", "payoffs"], ["no_spoiler"]]);
  assert.equal(record.answers.find((answer) => answer.id === "payoffs").yes, true, "one reader's cited yes meets the question");
  assert.match(state().story.owner_note, /^說故事檢查沒過：no_spoiler：.*讀者一：\[h1\] 一把傘。；讀者二：\[h1\] 一把傘。/);
  assert.doesNotMatch(state().story.owner_note, /payoffs/, "the listener is sent only what both readers failed");

  // The listener goes over the six chapters; in round 2 reader 2 says yes with a line quoted, and it passes.
  await steps(automation, 6);
  assert.match(await automation.step(), /a story has no script gate/);
  record = readJson(panelFile);
  assert.deepEqual([record.passed, record.round, record.failed], [true, 2, []]);
  assert.deepEqual(record.readers.map((reader) => reader.passed), [false, true]);
  assert.ok(state().notes.includes("storytelling panel passed (round 2)"));

  // A "yes" with no line id quoted does not outvote the other reader's "no".
  const uncited = storyWorld({ answers: standardAnswers({ "verifier:narrative": (body) => (body.payload.reader === 1
    ? panelAnswer(["no_spoiler"])
    : { answers: NARRATIVE_PANEL.map(({ id }) => ({ id, yes: true, evidence: id === "no_spoiler" ? "開場沒有劇透" : "[h1] 一把傘。" })) }) }) });
  await steps(uncited.automation, 1 + 6 + 6 + 6);
  assert.match(await uncited.automation.step(), /sent the narration back \(round 1: no_spoiler\)/);
  assert.match(uncited.state().story.owner_note, /讀者二：no line id quoted: 開場沒有劇透/);

  // The second reader's answer is unusable: the round fails as one reader's would, and nothing is
  // kept, so the first reader's answer is never taken for two.
  const broken = storyWorld({ raw: { "verifier:narrative": (body) => (body.payload.reader === 2 ? "sorry, no JSON here" : undefined) } });
  await steps(broken.automation, 1 + 6 + 6 + 6);
  assert.match(await broken.automation.step(), /verifier gave nothing usable \(verifier answered something that is not JSON/);
  assert.equal(existsSync(path.join(broken.workdir, "review", "narrative.json")), false);
  assert.equal(broken.state().story.narrative, undefined);
  assert.deepEqual(broken.site.calls.run.slice(-2).map((call) => call.payload.reader), [1, 2]);
});

test("a tutorial or drama's storytelling panel still asks one reader (flow.mjs): only a brand story asks two", async () => {
  let asked = 0;
  const world = storyWorld({ answers: standardAnswers({ "verifier:narrative": () => (asked += 1, panelAnswer()) }) });
  const slug = "thunder-one-reader";
  const doc = explainerFixture();
  doc.target_minutes = [10, 12];
  for (let n = 0; estimateTimeline(doc).total_frames / 30 / 60 < 8.5; n++) {
    doc.scenes.splice(doc.scenes.length - 1, 0, { id: `pan-${n}`, template: "shot", data: { prompt: "A wide shot of a village square at noon, one farmer counting on his fingers beside a wooden fence.", camera: "drift", visual: "still" }, lines: [{ id: `pan${n.toString(36).padStart(4, "0")}`, text: "這一句只是把範例拉長到一集的長度。" }] });
  }
  mkdirSync(path.join(world.box.root, "docs", "videos", slug), { recursive: true });
  writeFileSync(path.join(world.box.root, "docs", "videos", slug, "video.json"), JSON.stringify(doc));
  world.automation.persist({ slug, title: "雷聲", format: "drama", style_preset: EXPLAINER_PRESET, target_minutes: 10, source_urls: [], notes: [], status: "active", verified: true, listener_done: true });
  const state = readJson(path.join(world.box.work, slug, "auto.json"));
  assert.match(await world.automation.narrativeGate(state), /the storytelling panel passed \(round 1\)/);
  assert.equal(asked, 1);
  assert.deepEqual(Object.keys(world.site.calls.run.at(-1).payload), ["narration", "questions"], "no reader number");
  assert.equal("readers" in readJson(path.join(world.box.work, slug, "review", "narrative.json")), false);
});

test("a chapter the writer answers badly is asked for again once, then the video is blocked", async () => {
  let asked = 0;
  const world = storyWorld({
    answers: standardAnswers({ "writer:story": (body) => (body.payload.chapter.key === "idea" ? { title: "點子", scenes: [] } : chapterAnswer(body.payload.chapter.key, body.payload)) }),
    raw: { "writer:story": (body) => (body.payload.chapter.key === "idea" && asked++ === 0 ? "sorry, no JSON here" : undefined) },
  });
  const { automation, state } = world;
  await steps(automation, 3);
  const first = await automation.step();
  assert.match(first, /writer gave nothing usable \(writer answered something that is not JSON.*the next run tries once more/);
  assert.equal(automation.halted, true);
  assert.ok(automation.skipped.has(state().slug), "no other lane asks the writer for it again in this run");
  // The next run.
  automation.halted = false;
  automation.skipped.clear();
  const second = await automation.step();
  assert.match(second, /blocked — writer failed 2 times in a row: chapter idea: scenes is missing or empty/);
  assert.equal(MAX_STAGE_FAILURES, 2);
  assert.equal(state().status, "blocked");
  assert.match(world.site.calls.reports.at(-1).checklist[0].label, /^卡住，需要人處理：writer failed 2 times/);
  assert.ok(existsSync(path.join(world.workdir, "answers")), "what the model said is kept for a person");
});

test("a story saves a writer's pronunciation proposal and chapter without changing shared or pinned words, then requires a reviewed revision", async () => {
  const world = storyWorld({
    answers: standardAnswers({
      "writer:story": (body) => {
        const { key } = body.payload.chapter;
        const answer = chapterAnswer(key, body.payload);
        if (key === "hook") Object.assign(answer.lexicon_additions, { "8B": null, "6abc": null, Ai2: null });
        return answer;
      },
    }),
  });
  const { automation, site, state, lexicon, box, workdir } = world;
  const sharedFile = path.join(box.root, "docs", "videos", "lexicon.json");
  const sharedBefore = readFileSync(sharedFile);
  await steps(automation, 2);
  assert.deepEqual(readFileSync(sharedFile), sharedBefore);
  assert.equal(state().status, "blocked");
  assert.deepEqual(state().story.lexicon_pending, ["Ai2"]);
  assert.equal(state().story.chapters.hook.written, 1);
  assert.ok(readChapter(automation, state(), "hook"), "successful writer output is retained");
  assert.equal(Object.hasOwn(lexicon().terms, "Ai2"), false);
  assert.deepEqual(validateLexicon(lexicon()), []);
  assert.equal(Object.hasOwn(lexicon().terms, "8B"), false);
  const calls = site.calls.run.length;
  await advanceStory(automation, state(), "script passes lint");
  assert.equal(site.calls.run.length, calls, "the blocked project makes no second model request");
  const next = structuredClone(lexicon());
  next.terms.Ai2 = null;
  reviseStoryLexicon({ root: box.root, slug: SLUG, workdir, nextBytes: Buffer.from(JSON.stringify(next)), reviewSha256: createHash("sha256").update("independent fixture review").digest("hex") });
  const saved = state();
  saved.story.chapters.hook.checked = true;
  saved.story.chapters.hook.listened = true;
  saved.story.chapters.hook.check_rounds = 2;
  assert.match(await advanceStory(automation, saved, "script passes lint"), /pronunciation input changed/);
  assert.equal(saved.story.chapters.hook.checked, false);
  assert.equal(saved.story.chapters.hook.listened, false);
  assert.equal(saved.story.chapters.hook.check_rounds, 2, "review ceilings are not reset");
  assert.deepEqual(readFileSync(sharedFile), sharedBefore);
});

test("a name of the story in a picture prompt is refused before anything is drawn: the chapter goes back to the writer, and a prompt fix that names it is not kept", async () => {
  let named = 0;
  const world = storyWorld({
    answers: standardAnswers({
      "writer:story": (body) => chapterAnswer(body.payload.chapter.key, body.payload, { nameInPrompt: body.payload.chapter.key === "idea" && !body.payload.lint_errors && named++ === 0 }),
      "writer:story-fix": (body) => ({ shots: body.payload.shots.map((shot) => ({ id: shot.id, prompt: `${shot.prompt}, the Brellco logo on the wall`, camera: "static" })) }),
    }),
  });
  const { automation, site, state } = world;
  await steps(automation, 3);
  assert.match(await automation.step(), /chapter 3\/6 \(idea\) written: 2 shots, \d+ characters; 1 lint errors in it go back to the writer/);
  assert.match(state().story.chapters.idea.lint[0], /data\.prompt: names "Brellco"/);
  assert.match(await automation.step(), /chapter idea fixed for 1 lint errors \(round 1\)/);
  const fix = site.calls.run.at(-1);
  assert.equal(fix.variant, "story");
  assert.match(fix.payload.lint_errors[0], /Brellco/);
  assert.equal(fix.payload.current.key, "idea", "the fix gets its own chapter, not the script");
  assert.doesNotMatch(readChapter(automation, state(), "idea").scenes[0].data.prompt, /Brellco/);
  assert.equal(world.runs.length, 0, "nothing was drawn");
  await steps(automation, 3 + 6 + 6 + 1);
  assert.equal((await pipelineStatus({ slug: SLUG, root: world.box.root, workdir: world.workdir })).next.id, "narration synthesized");

  // A keyframe that failed its check: a patch of that shot alone; one that names the brand is refused and not kept.
  const before = readChapter(automation, state(), "engine");
  const other = structuredClone(readChapter(automation, state(), "turn"));
  const done = await automation.fixPrompts(state(), "keyframes", { targets: [{ id: "engine-02", problems: ["the frame is crowded"] }] });
  assert.match(done, /engine-02 fix fails lint|gave nothing usable \(the keyframes fix fails lint/);
  assert.deepEqual(readChapter(automation, state(), "engine"), before, "the refused patch left the chapter as it was");
  const call = site.calls.run.at(-1);
  assert.equal(call.variant, "story-fix");
  assert.deepEqual(call.payload.shots.map((shot) => shot.id), ["engine-02"], "only the named shot goes to the writer");
  assert.deepEqual(call.payload.fix.targets, [{ id: "engine-02", problems: ["the frame is crowded"] }]);
  assert.deepEqual(readChapter(automation, state(), "turn"), other);
});

test("a keyframe fix patches the named shot alone, and after the rounds the video waits for a person", async () => {
  const world = storyWorld({
    answers: standardAnswers({ "writer:story-fix": (body) => ({ shots: body.payload.shots.map((shot) => ({ id: shot.id, prompt: "a calm department store counter with a few boxed umbrellas, medium shot", camera: "slow pan left" })) }) }),
  });
  const { automation, state } = world;
  await steps(automation, 1 + 6 + 6 + 6 + 1);
  const before = readChapter(automation, state(), "engine");
  assert.match(await automation.fixPrompts(state(), "keyframes", { targets: [{ id: "engine-02", problems: ["the frame is crowded"] }] }), /keyframes prompts fixed \(round 1\) for engine-02; keyframes runs again next/);
  const after = readChapter(automation, state(), "engine");
  assert.equal(after.scenes[1].data.prompt, "a calm department store counter with a few boxed umbrellas, medium shot");
  assert.equal(after.scenes[1].data.camera, "slow pan left");
  assert.deepEqual(after.scenes[0], before.scenes[0], "the shot that passed is untouched");
  assert.deepEqual(after.scenes[1].lines, before.scenes[1].lines, "no line changes");
  assert.equal(world.video().scenes.find((scene) => scene.id === "engine-02").data.camera, "slow pan left", "video.json is merged again");
  assert.equal(state().prompt_fixes.keyframes, 1);
  // A shot the image model's budget refused tells the writer its number, for the shot and for the fix as a whole.
  await automation.fixPrompts(state(), "keyframes", { targets: [{ id: "engine-02", problems: ["still crowded"], prompt_budget_chars: 420 }, { id: "engine-01", problems: ["too long"], prompt_budget_chars: 480 }] });
  const budgeted = world.site.calls.run.at(-1).payload.fix;
  assert.equal(budgeted.prompt_budget_chars, 420, "the tightest among the targets");
  assert.deepEqual(budgeted.targets.map((target) => target.prompt_budget_chars), [420, 480]);
  assert.match(await automation.fixPrompts(state(), "keyframes", { targets: [{ id: "engine-02", problems: ["still crowded"] }] }), /blocked — keyframes still fails after 2 prompt fixes/);
});

test("a narration too long after tts: the writer cuts the longest chapter, which is checked and heard again, and the next length passes", async () => {
  const lengths = [1000, 780];
  const world = storyWorld({
    answers: standardAnswers({ "writer:story": (body) => chapterAnswer(body.payload.chapter.key, body.payload, { extraShot: body.payload.chapter.key === "engine" && !body.payload.resize }) }),
    seconds: () => lengths.shift() ?? 780,
  });
  const { automation, site, state } = world;
  await steps(automation, 1 + 6 + 6 + 6 + 1);
  assert.match(await automation.step(), /narration synthesized/);
  const cut = await automation.step();
  assert.match(cut, /the narration measures 16:[34]\d, over 15:30; the writer cut engine \(about \d+ s, round 1\); it is checked and heard again/);
  const resize = site.calls.run.at(-1);
  assert.equal(resize.variant, "story");
  assert.equal(resize.payload.chapter.key, "engine", "the longest chapter");
  assert.ok(resize.payload.resize.seconds < 0);
  assert.equal(resize.payload.current.scenes.length, 3);
  assert.equal(readChapter(automation, state(), "engine").scenes.length, 2);
  assert.match(await automation.step(), /chapter engine checked \(round 1\)/);
  assert.match(await automation.step(), /chapter engine heard/);
  assert.match(await automation.step(), /a story has no script gate/);
  assert.match(await automation.step(), /narration synthesized/);
  assert.match(await automation.step(), /narration checked \(Jev passed every line\) and sent for review/);
  assert.equal(state().story.length.seconds, 780);
  assert.equal(state().story.resizes, 1);
  assert.deepEqual(world.runs.filter((run) => run.startsWith("tts")).length, 2);
});

test("a narration too short whose passages hold no more waits for the owner, and one still too long after two fixes is blocked with its length", async () => {
  const short = storyWorld({
    answers: standardAnswers({ "writer:story": (body) => (body.payload.resize ? { no_more: true, reason: "段落只講到 1954 年的數字" } : chapterAnswer(body.payload.chapter.key, body.payload)) }),
    seconds: () => 600,
  });
  await steps(short.automation, 1 + 6 + 6 + 6 + 1 + 1);
  const blocked = await short.automation.step();
  assert.match(blocked, /blocked — the narration measures (09:5\d|10:0\d), under 11:30, and the passages hold nothing more to tell in \w+ \(段落只講到 1954 年的數字\): the owner decides, a shorter video or another story/);
  const resize = short.site.calls.run.at(-1);
  assert.ok(resize.payload.resize.seconds > 0, "adding, never padding");
  assert.notEqual(resize.payload.chapter.key, "hook", "the hook keeps its 30 seconds");
  assert.equal(short.state().status, "blocked");

  const long = storyWorld({ seconds: () => 1000 });
  const { automation } = long;
  await steps(automation, 1 + 6 + 6 + 6 + 1 + 1);
  for (let round = 1; round <= LENGTH_FIX_ROUNDS; round++) {
    assert.match(await automation.step(), new RegExp(`the narration measures 16:[34]\\d, over 15:30; the writer cut \\w+ .*round ${round}`));
    await steps(automation, 3);
    assert.match(await automation.step(), /narration synthesized/);
  }
  assert.match(await automation.step(), /blocked — the narration measures 16:[34]\d, over 15:30 after 2 length fixes; a story runs 11:30 to 15:30: the owner decides/);
  assert.equal(long.runs.filter((run) => run.startsWith("check-audio")).length, 0, "Jev is not paid for a narration that must change");
});

test("the owner who sends the narration back has the listener go over the six chapters with the note; a note that changes nothing leaves the video for a person", async () => {
  let pushed = 0;
  const world = storyWorld({ seconds: () => 780, decide: (gate) => (gate === "audio" && pushed++ === 0 ? { status: "rejected", note: "結尾那句太硬" } : { status: "approved" }) });
  const { automation, site, state } = world;
  await steps(automation, 1 + 6 + 6 + 6 + 1 + 1);
  assert.match(await automation.step(), /narration checked .* and sent for review/);
  assert.match(await automation.step(), /the owner sent the narration back \(結尾那句太硬\); the listener goes over the six chapters with the note/);
  const heard = await steps(automation, 6);
  heard.forEach((line, index) => assert.match(line, new RegExp(`chapter ${CHAPTER_KEYS[index]} heard`)));
  const pass = site.calls.run.slice(-6);
  assert.ok(pass.every((call) => call.variant === "story" && call.stage === "listener" && call.payload.owner_note === "結尾那句太硬"));
  assert.equal(readChapter(automation, state(), "turn").scenes[1].lines[1].text, "只能選一邊站。");
  assert.match(await automation.step(), /a story has no script gate/, "a changed line voids the local approval of the script");
  assert.match(await automation.step(), /narration synthesized/);
  assert.match(await automation.step(), /narration checked .* and sent for review/);
  assert.match(await automation.step(), /keyframes done/);
  assert.ok(state().notes.includes("narration sent back: 結尾那句太硬"));

  const still = storyWorld({ seconds: () => 780, decide: (gate) => (gate === "audio" ? { status: "rejected", note: "再自然一點" } : { status: "approved" }), answers: standardAnswers({ "listener:story": (body) => (body.payload.owner_note ? { patch: {}, drop: [] } : listenAnswer(body.payload)) }) });
  await steps(still.automation, 1 + 6 + 6 + 6 + 1 + 1 + 1 + 1 + 6);
  assert.match(await still.automation.step(), /blocked — the owner sent the narration back \(再自然一點\) and the listener's pass changed nothing/);
});

test("the owner's storyboard note with no failed shot offers the writer every shot, and only the shot the note is about changes", async () => {
  const world = storyWorld({
    answers: standardAnswers({ "writer:story-fix": (body) => ({ shots: [{ id: "turn-01", prompt: "a broken umbrella rib under a bright street lamp, close up", camera: "slow push in" }] }) }),
  });
  const { automation, site, state } = world;
  await steps(automation, 1 + 6 + 6 + 6 + 1);
  const before = Object.fromEntries(CHAPTER_KEYS.map((key) => [key, readChapter(automation, state(), key)]));
  assert.match(await automation.fixPrompts(state(), "keyframes", { targets: [], ownerNote: "轉折第一個畫面太暗" }), /keyframes prompts fixed \(round 1\) for turn-01/);
  const call = site.calls.run.at(-1);
  assert.equal(call.variant, "story-fix");
  assert.equal(call.payload.shots.length, 12, "every shot is offered when the note names none");
  assert.equal(call.payload.fix.owner_note, "轉折第一個畫面太暗");
  assert.equal(readChapter(automation, state(), "turn").scenes[0].data.prompt, "a broken umbrella rib under a bright street lamp, close up");
  for (const key of CHAPTER_KEYS.filter((each) => each !== "turn")) assert.deepEqual(readChapter(automation, state(), key), before[key]);
  assert.ok(state().notes.includes("keyframes sent back: 轉折第一個畫面太暗"));
});

test("a paused subscription ends the round without counting a failure, a start the site holds back writes nothing, a series with no shared look is refused at the start, and a thread on a story's screenplay is answered without a rewrite", async () => {
  const held = storyWorld({ held: "今天已經開始 2 支故事，每日上限 2 支" });
  assert.match(await held.automation.step(), /the site refused to start story 1 \(story-folding-umbrella\): 今天已經開始 2 支故事/);
  assert.equal(held.automation.halted, true, "the round ends; the next one asks the site again");
  assert.equal(held.state(), undefined, "nothing was written for a story that did not start");
  assert.equal(existsSync(held.dir), false);

  const paused = storyWorld({ paused: (body) => body.stage === "writer" });
  await paused.automation.step();
  await assert.rejects(paused.automation.step(), (error) => error.code === "video_ai_subscription_paused");
  assert.equal(paused.state().status, "active");
  assert.equal(paused.state().failures, undefined, "a paused subscription is no failure of the story");
  assert.equal(readChapter(paused.automation, paused.state(), "hook"), null);

  const bare = { ...SERIES, look: null };
  const lookless = storyWorld({ series: bare, jobs: [{ kind: "episode", series: bare, chapter_number: null, episode: EPISODE, previous: null, rewrites_left: 0, context: { series: bare, setting: null, outline: null, chapter: null, chapter_number: null, chapter_range: null, episode: EPISODE, episodes: [], recaps: [], mysteries: [] } }] });
  assert.match(await lookless.automation.step(), /blocked — the story cannot be written: the story series has no shared look/);

  const world = storyWorld();
  await steps(world.automation, 1 + 6);
  const { answerScript, STORY_THREAD_REPLY } = await import("./discuss.mjs");
  const calls = world.site.calls.run.length;
  const job = { series: SERIES, subject: "script:1", target: "script", message: { id: "m1", body_md: "開場改短一點" }, thread: [], episode: { ...EPISODE, slug: SLUG }, context: {} };
  assert.match(await answerScript(world.automation, job), /a story's screenplay is not rewritten from a thread/);
  assert.deepEqual(world.site.calls.answers, [{ id: "m1", reply_md: STORY_THREAD_REPLY, revised: null }]);
  assert.equal(world.site.calls.run.length, calls, "no model call");
});

test("a story is never taken for an explainer (#904), nor an explainer for a story", async () => {
  // The story's own files: the custom look, the drama's brief sections, series.json of kind "story".
  const world = storyWorld();
  await steps(world.automation, 1 + 6);
  const video = world.video();
  assert.equal(video.look.preset, "custom");
  assert.notEqual(video.look.preset, EXPLAINER_PRESET);
  assert.equal(isExplainer(video), false);
  assert.equal(hasCast(video), false, "a narrator-only story has no look gate, as #904's hasCast and #897's narratorOnly both read it");
  assert.deepEqual(briefSectionsFor(video.format, video.look.preset), BRIEF_SECTIONS_DRAMA);
  assert.equal(isStory(readJson(path.join(world.dir, "series.json"))), true);
  assert.equal(isExplainerOneOff(SERIES), false, "a story series is no one-off");
  assert.equal(world.automation.variantOf(world.state()), null, "the explainer's variants never reach a story");
  assert.ok(world.site.calls.run.every((call) => call.variant === "story"));
  assert.equal(isExplainer(storyFixture()), false);
  assert.equal(isStory(storySeries()), true);
  // The explainer: its video is no story, and a one-off in the flat-explainer preset is started
  // under <series>-e001 and drafted by the drama's flow; the story's steps leave it alone.
  assert.equal(isExplainer(explainerFixture()), true);
  assert.equal(isStory({ slug: "one-off-7a1b2c3d", episode: 1, chapter: 1, characters: [] }), false, "a one-off's series.json names no kind");
  const started = [];
  const drama = {
    api: { episodeStart: async (series, number, slug) => (started.push(slug), { request: { slug }, context: {}, episode: { number } }) },
    draftEpisode: async (request) => `drafted ${request.slug} as a drama`,
  };
  const oneOff = { ...SERIES, slug: "one-off-7a1b2c3d", kind: "one-off", style_preset: EXPLAINER_PRESET, look: null };
  assert.equal(isExplainerOneOff(oneOff), true);
  assert.equal(await startEpisode(drama, { kind: "episode", series: oneOff, episode: { number: 1, slug: null, beats: {} } }), "drafted one-off-7a1b2c3d-e001 as a drama");
  assert.deepEqual(started, ["one-off-7a1b2c3d-e001"]);
  const explainerState = { slug: "one-off-7a1b2c3d-e001", status: "active", format: "drama", style_preset: EXPLAINER_PRESET, series: { slug: "one-off-7a1b2c3d", episode: 1, chapter: 1, kind: "one-off" } };
  assert.equal(await advanceStory(world.automation, explainerState, "script passes lint"), undefined);
  assert.equal(world.automation.variantOf(explainerState), "explainer");
});

test("a story's cast is generic: its figures carry no name of the story, speak with the narrator's voice, and bring the look step back", () => {
  const plan = { ...PLAN, cast: [{ id: "brellco-founder", role: "創立 Brellco 的發明家", appearance: "a man in his forties in a 1920s tweed suit, round glasses, carrying a folded umbrella" }, { id: "clerk", role: "店員", appearance: "a young woman in a 1950s shop uniform" }] };
  const voice = { provider: "gemini", name: "Sulafat" };
  const cast = storyCast(plan, voice);
  assert.deepEqual(cast.map((figure) => [figure.id, figure.name]), [["brellco-founder", "founder"], ["clerk", "clerk"]]);
  assert.ok(cast.every((figure) => figure.voice === voice));
});
