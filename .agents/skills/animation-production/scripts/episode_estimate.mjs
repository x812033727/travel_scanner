#!/usr/bin/env node
// 一集 AI 漫劇在付任何一毛錢之前值多少：每個鏡頭會買幾秒片段、畫幾張圖、叫幾次 judge，一次 take 和
// 最壞情況（keyframe 3 take、clip 2 take、look 2 輪）各多少，同一集改走 Hailuo 網頁方案或 Kling 會用掉
// 多少 credits，以及哪些鏡頭可以改成剪接（data.source）、靜圖（visual "still"）或合併來省錢。
//
//   node .agents/skills/animation-production/scripts/episode_estimate.mjs <video.json>
//     [--tier clips|hybrid|stills] [--model <clip model id>] [--resolution <r>]
//     [--plan hailuo:standard|pro|master|max | kling:standard|pro|premier|ultra]
//     [--image-price N] [--price-per-second N] [--credits-per-video N] [--minutes-per-clip N]
//     [--keyframe-takes N] [--clip-takes N] [--cap N] [--month-clip-seconds N]
//     [--production] [--strict] [--json]
//
// 長度照 lint 的估法（tools/video/core/timeline.mjs estimateTimeline：一個字 0.24 s、一句停 0.3 s、
// 一鏡間隔 0.7 s），和 clips 階段讀 timeline.json 的方式一樣；錄好的 timeline 才是真的，這裡是事前估。
// 買的秒數照 tools/video/media/clips.mjs clipSeconds 的規則（本檔 secondsBought 重寫一份，
// tools/animation-production.test.mjs 盯著兩邊一致）。價目都在 PRICES 與 PLANS 兩張表，鍵是模型 id
// 或方案 id，每一筆寫明來源與讀取日期；旗標可以蓋過。離線、不碰伺服器：伺服器實際選的模型、每影片上限、
// 每月額度要看 `node tools/video/cli.mjs media-status`。
// --plan 把同一集的片段換算成方案的 credits、月額度占比、兩種美元（月費攤／頁面價），並和伺服器路線並列、印損益
// 平衡秒數（月費 ÷ 伺服器每秒價）；--resolution 給伺服器模型的解析度，--plan hailuo:* 時也選 768p 或 2k 的檔位。
// 結束碼：0；--strict 且裁定不過（超過 --cap、超過 --month-clip-seconds、超出 tier、production 下的長鏡頭、既有
// data.source 超出來源實際買到的秒數）是 1；讀不到檔或參數錯是 2。
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { isLookOnly, normalize, shotSize, TARGETS } from "../../../../tools/video/core/craft.mjs";
import { DEFAULT_LOOK_CANDIDATES, hasCast, MAX_SOURCE_CLIP_SECONDS, resolveLook, resolveMusic, TIER_CLIP_SHARE_MAX, VISUAL_TIERS } from "../../../../tools/video/core/drama.mjs";
import { estimateTimeline, FPS } from "../../../../tools/video/core/timeline.mjs";

export const CATALOG = "apps/api/app/video_media/catalog.py";
export const CATALOG_READ_ON = "2026-09-26";
export const PLANS_READ_ON = "2026-10-03";
// 實測：站主的帳號上量到的（Hailuo 一支 H3 2K 5 秒的文生影片；Kling CLI 的 who_am_i 與 account）。
export const PLANS_MEASURED_ON = "2026-10-04";
// 工具規定：tools/video/media/keyframes.mjs MAX_KEYFRAME_TAKES、clips.mjs MAX_CLIP_TAKES / MIN_CLIP_SECONDS /
// MAX_CLIP_SECONDS、look.mjs MAX_LOOK_ROUNDS（測試盯著一致）。
export const MAX_KEYFRAME_TAKES = 3;
export const MAX_CLIP_TAKES = 2;
export const MAX_LOOK_ROUNDS = 2;
export const MIN_CLIP_SECONDS = 4;
export const MAX_CLIP_SECONDS = 10;
// 站上的預設（apps/api/app/video_automation/models.py 設定列的預設值）；實際值看 media-status。
export const DEFAULT_CAP_USD = 200;
export const DEFAULT_MONTH_CLIP_SECONDS = 3000;
export const DEFAULT_CLIP_MODEL = "gemini-omni-1.1-flash";
export const DEFAULT_IMAGE_MODEL = "gemini-3-pro-image";
export const DEFAULT_MUSIC_MODEL = "lyria-3.5";
// 未驗證：第三方 2026 年整理的 Kling 3.0 Omni standard 5 s 約 35–45 credits、professional 約 70。
// 官方 CLI 的 who_am_i 不給 credits 價，2026-10-04 授權進來的帳號是 NORMAL、0 credits，一支都沒生成；
// 報價前先在站主帳號裡生成一支、記前後差額。
export const DEFAULT_KLING_CREDITS_PER_VIDEO = 40;
// 估價的單位，不是 Kling 的限制：kling-video-v3_0 可以要 3–15 秒整數（實測 2026-10-04），
// 但 5、10 秒以外扣幾 credits 沒有任何來源，所以仍以第三方的「一支 5 秒」計。
export const KLING_VIDEO_SECONDS = 5;
// 假設：方案佇列裡一支片段從送出到拿到要幾分鐘；只用來把「幾支片段」換算成「幾小時」。量過的只有一支：
// Hailuo H3 2K 5 秒、沒有別的在排隊，約 4 分 40 秒（實測 2026-10-04）；有排隊、較長的片段與 Kling 都沒量。
export const DEFAULT_MINUTES_PER_CLIP = 6;
// 工具規定：production profile 一鏡最多 8 秒（tools/video/core/lint.mjs productionShotProblems）。
export const PRODUCTION_SHOT_SECONDS = 8;
// 兩個 prompt 的字集 Jaccard：切鏡候選只比鏡位（camera 行加 prompt 第一子句），畫面像不像要人看；相似度低就標出來。
const words = (text) => new Set(String(text ?? "").toLowerCase().split(/[^a-z0-9一-鿿]+/).filter((each) => each.length > 1));
export function promptSimilarity(a, b) {
  const x = words(a);
  const y = words(b);
  if (!x.size && !y.size) return 1;
  let both = 0;
  for (const word of x) if (y.has(word)) both += 1;
  return both / (x.size + y.size - both);
}
export const PICTURE_SIMILARITY_MIN = 0.5;

const SECONDS_4_TO_10 = [4, 5, 6, 7, 8, 9, 10];
const catalogSource = (field) => `${CATALOG} ${field}（${CATALOG_READ_ON} 讀）`;

/**
 * 伺服器 API 路線的價目，鍵是 catalog.py 的模型 id，值照目錄抄（tools/animation-production.test.mjs
 * 用正則比對目錄，改了目錄就會紅）。`judge` 是一次評審的價（JUDGE_USD_PER_CALL）。
 */
export const PRICES = {
  "gemini-3-pro-image": {
    kind: "image",
    label: "Gemini 3 Pro Image（Nano Banana Pro）",
    usd_per_image: 0.134,
    usd_per_image_2k: 0.134,
    source: `${CATALOG} usd_per_image / usd_per_image_2k（Google 價目頁 2026-09-28 讀）`,
    note: "漫劇的 keyframe 以 1K 畫（它是片段的首格）；只有投影片插圖用 2K，兩者同價",
  },
  "gemini-omni-1.1-flash": {
    kind: "clip",
    label: "Gemini Omni 1.1 Flash",
    usd_per_second: 0.15,
    durations: SECONDS_4_TO_10,
    resolutions: ["720p", "1080p"],
    default_resolution: "1080p",
    source: catalogSource("usd_per_second"),
  },
  "veo-3.1-lite-generate-preview": {
    kind: "clip",
    label: "Veo 3.1 Lite",
    usd_per_second: 0.08,
    durations: [4, 6, 8],
    resolutions: ["720p", "1080p"],
    default_resolution: "1080p",
    fixed_at_1080p: 8,
    source: catalogSource("usd_per_second"),
    note: "1080p 一律買 8 秒，不管鏡頭需要幾秒（tools/video/media/clips.mjs clipSeconds）；720p 才會貼著需求選 4/6/8",
  },
  "veo-3.1-generate-001": {
    kind: "clip",
    label: "Veo 3.1",
    usd_per_second: 0.40,
    durations: [4, 6, 8],
    resolutions: ["720p", "1080p"],
    default_resolution: "1080p",
    fixed_at_1080p: 8,
    source: catalogSource("usd_per_second"),
  },
  "veo-3.1-fast-generate-001": {
    kind: "clip",
    label: "Veo 3.1 Fast",
    usd_per_second: 0.12,
    durations: [4, 6, 8],
    resolutions: ["720p", "1080p"],
    default_resolution: "1080p",
    fixed_at_1080p: 8,
    source: catalogSource("usd_per_second"),
  },
  "MiniMax-H3": {
    kind: "clip",
    label: "MiniMax H3（Hailuo 3.0）",
    usd_per_second: 0.13,
    durations: SECONDS_4_TO_10,
    resolutions: ["768p", "2k"],
    default_resolution: "2k",
    vendor_seconds: [4, 15],
    source: catalogSource("usd_per_second"),
    note: "目錄只開 4–10 秒；MiniMax 官方把 H3 賣到 4–15 秒整數（platform.minimax.io，2026-10-03 讀）。計價表每秒一價，768P 也照 2K 的 US$0.13 算（apps/api/app/video_media/meter.py 不分解析度）",
  },
  "lyria-3.5": {
    kind: "music",
    label: "Lyria 3.5",
    usd_per_track: 0.08,
    source: catalogSource("usd_per_track"),
  },
  judge: {
    kind: "judge",
    label: "judge（Gemini 看圖或看片）",
    usd_per_call: 0.01,
    source: `${CATALOG} JUDGE_USD_PER_CALL；tools/video/media/stages.mjs JUDGE_USD_PER_CALL`,
  },
};

const HAILUO_CREDITS_PER_SECOND = { "2k": 12, "768p": 7 };
// 2K 的 12 是實測（站主的 Max 帳號，H3 2K 5 秒：「創建」旁顯示 60，餘額 27,150 → 27,090）；768P 的 7 沒有量。
export const HAILUO_CREDITS_BASIS = { "2k": `實測 ${PLANS_MEASURED_ON}`, "768p": "推算" };
const HAILUO_NOTE = `H3 2K 12 credits/s 是實測（${PLANS_MEASURED_ON}：5 秒一支扣 60）；768P 的 7 credits/s 仍推算自訂閱頁的每月秒數（Pro 4,500 credits ≈ 643 s 的 768P、≈ 375 s 的 2K；Standard 1,000 ≈ 143 / 84 s），每級一樣；頁面標的每秒美元是以年繳月價算的`;
const HAILUO_OUTPUT_NOTE = `H3 2K 的輸出是 2560×1440、24 fps、帶 AAC 音軌（實測 ${PLANS_MEASURED_ON}）：不是原生 1920×1080，production profile 不收；音軌成片不用。下載走「全部下載 → 無水印下載」，結果卡 <video> 的 src 是有浮水印的版本，clips import 的 ffmpeg 檢查抓不到`;
const KLING_NOTE = `每支影片的 credits 未驗證：40 是第三方 2026 年的整理（standard 5 s 約 35–45）；官方 CLI 的 who_am_i 不給 credits 價，${PLANS_MEASURED_ON} 授權進來的帳號是 NORMAL、0 credits，沒有生成過。用 --credits-per-video 蓋過`;

/**
 * 訂閱方案（價目：hailuoai.video 訂閱頁與 kling.ai 會員頁，2026-10-03 在應用內瀏覽器讀；Hailuo H3 2K 的
 * credits/s 是 2026-10-04 實測；三條路線的比較、操作步驟與權利在
 * .agents/skills/animation-production/references/providers-and-plans.md）。
 * Hailuo 的 credits 以秒計，Kling 以「一支 5 秒影片」計（估價單位，見 KLING_VIDEO_SECONDS）。
 */
export const PLANS = {
  "hailuo:standard": { vendor: "hailuo", label: "Hailuo Standard", fee_usd: 14.99, fee_annual_monthly_usd: 8.40, credits: 1000, running: 1, queued: 8, credits_per_second: HAILUO_CREDITS_PER_SECOND, page_usd_per_second: { "2k": 0.101, "768p": 0.059 }, default_resolution: "2k", clip_seconds: [4, 15], images: "每張圖都扣 credits（單價未抄）", note: HAILUO_NOTE },
  "hailuo:pro": { vendor: "hailuo", label: "Hailuo Pro", fee_usd: 54.99, fee_annual_monthly_usd: 30.40, credits: 4500, running: 2, queued: 8, credits_per_second: HAILUO_CREDITS_PER_SECOND, page_usd_per_second: { "2k": 0.081, "768p": 0.047 }, default_resolution: "2k", clip_seconds: [4, 15], images: "圖片無限（1K）", note: HAILUO_NOTE },
  "hailuo:master": { vendor: "hailuo", label: "Hailuo Master", fee_usd: 119.99, fee_annual_monthly_usd: 71.20, credits: 10500, running: 2, queued: 12, credits_per_second: HAILUO_CREDITS_PER_SECOND, page_usd_per_second: { "2k": 0.081, "768p": 0.047 }, default_resolution: "2k", clip_seconds: [4, 15], images: "圖片無限（2K）", note: HAILUO_NOTE },
  "hailuo:max": { vendor: "hailuo", label: "Hailuo Max", fee_usd: 199.99, fee_annual_monthly_usd: 184.00, credits: 27000, running: 2, queued: 12, credits_per_second: HAILUO_CREDITS_PER_SECOND, page_usd_per_second: { "2k": 0.081, "768p": 0.047 }, default_resolution: "2k", clip_seconds: [4, 15], images: "圖片無限（4K）", unlimited: "credits 用完後 Hailuo 2.0/2.3（1080p 6 s、10 s）進 relax 佇列無限生成，H3 不在內", note: HAILUO_NOTE },
  "kling:standard": { vendor: "kling", label: "Kling Standard", fee_usd: 10, first_month_usd: 6.99, credits: 660, running: null, queued: "unlimited", video_seconds: KLING_VIDEO_SECONDS, credits_per_video: DEFAULT_KLING_CREDITS_PER_VIDEO, note: KLING_NOTE },
  "kling:pro": { vendor: "kling", label: "Kling Pro", fee_usd: 37, first_month_usd: 25.99, credits: 3000, running: null, queued: "unlimited", video_seconds: KLING_VIDEO_SECONDS, credits_per_video: DEFAULT_KLING_CREDITS_PER_VIDEO, note: KLING_NOTE },
  "kling:premier": { vendor: "kling", label: "Kling Premier", fee_usd: 92, first_month_usd: 64.99, credits: 8000, running: null, queued: "unlimited", video_seconds: KLING_VIDEO_SECONDS, credits_per_video: DEFAULT_KLING_CREDITS_PER_VIDEO, note: KLING_NOTE },
  "kling:ultra": { vendor: "kling", label: "Kling Ultra", fee_usd: 180, first_month_usd: 127.99, credits: 26000, running: null, queued: "unlimited", video_seconds: KLING_VIDEO_SECONDS, credits_per_video: DEFAULT_KLING_CREDITS_PER_VIDEO, note: KLING_NOTE },
};

/** 片段模型會買的秒數，照 tools/video/media/clips.mjs clipSeconds：Veo 3.1 在 1080p 固定 8 秒，否則需求夾在 4–10 秒再往上貼到模型賣的長度。 */
export function secondsBought(frames, model = DEFAULT_CLIP_MODEL, resolution = null) {
  if (/^veo-?3\.1/.test(model) && resolution === "1080p") return 8;
  const need = Math.max(MIN_CLIP_SECONDS, Math.min(MAX_CLIP_SECONDS, Math.ceil(frames / FPS)));
  const allowed = [...(PRICES[model]?.durations ?? [])].filter((each) => Number.isInteger(each)).sort((a, b) => a - b);
  if (!allowed.length) return need;
  return allowed.find((each) => each >= need) ?? allowed.at(-1);
}

/** Hailuo 網頁的 H3：整數秒，4 到 15（platform.minimax.io 與 hailuoai.video，2026-10-03 讀；設定面板 2026-10-04 實測同樣是 4–15 秒整數）。 */
export const hailuoSeconds = (frames) => Math.min(15, Math.max(4, Math.ceil(frames / FPS)));
/** Kling：一支 5 秒影片為一單位，需要幾支（估價單位；kling-video-v3_0 本身收 3–15 秒整數）。 */
export const klingVideos = (frames) => Math.max(1, Math.ceil(frames / FPS / KLING_VIDEO_SECONDS));

// 同一個機位：camera 行加 prompt 第一個子句，和 tools/video/core/craft.mjs 的 setupKey 一樣。
const setupKey = (data) => `${String(data?.camera ?? "").trim().toLowerCase()}|${String(data?.prompt ?? "").split(/[,.;]/)[0].trim().toLowerCase()}`;
const castKey = (data) => String([...(Array.isArray(data?.characters) ? data.characters : [])].sort());
const round2 = (value) => Math.round(value * 100) / 100;
const round4 = (value) => Math.round(value * 10_000) / 10_000;
const sum = (items, key) => items.reduce((total, item) => total + (item[key] ?? 0), 0);
const usd = (value) => `US$${value.toFixed(2)}`;
// A unit price keeps its third decimal (US$0.134 a picture, US$0.081 a second), a total two.
const unit = (value) => `US$${value.toFixed(3).replace(/0$/, "")}`;

/**
 * 整集的估算：{ basis, model, prices, shots, counts, stages, totals, plan, levers, verdict }。
 * 只讀 video.json；一個有 `shots[]` 的量測剪接檔不在這裡（drama_craft_check 讀得了，但沒有 look 和角色）。
 */
export function estimateEpisode(doc, options = {}) {
  if (!Array.isArray(doc?.scenes)) throw new Error("not a video.json: no scenes[]");
  const model = options.model ?? DEFAULT_CLIP_MODEL;
  const entry = PRICES[model];
  const pricePerSecond = Number.isFinite(options.pricePerSecond) ? options.pricePerSecond : entry?.kind === "clip" ? entry.usd_per_second : null;
  if (pricePerSecond === null) throw new Error(`unknown clip model "${model}": PRICES knows ${Object.keys(PRICES).filter((id) => PRICES[id].kind === "clip").join(", ")}; or give --price-per-second`);
  const tier = options.tier ?? null;
  if (tier !== null && !VISUAL_TIERS.includes(tier)) throw new Error(`--tier must be one of ${VISUAL_TIERS.join(", ")}`);
  const planId = options.plan ?? null;
  const plan = planId ? PLANS[planId] : null;
  if (planId && !plan) throw new Error(`unknown plan "${planId}": one of ${Object.keys(PLANS).join(", ")}`);
  // --resolution reaches the server model only when that model offers it (768p and 2k are Hailuo's
  // H3 tiers, which --plan hailuo:* reads from the raw flag below); otherwise the model's default.
  const wantedResolution = options.resolution ? String(options.resolution).toLowerCase() : null;
  const resolution = entry ? (entry.resolutions?.includes(wantedResolution) ? wantedResolution : entry.default_resolution ?? null) : wantedResolution;
  const production = Boolean(options.production);
  const imagePrice = Number.isFinite(options.imagePrice) ? options.imagePrice : PRICES[DEFAULT_IMAGE_MODEL].usd_per_image;
  const judgePrice = PRICES.judge.usd_per_call;
  const keyframeTakes = options.keyframeTakes ?? MAX_KEYFRAME_TAKES;
  const clipTakes = options.clipTakes ?? MAX_CLIP_TAKES;
  const cap = options.cap ?? DEFAULT_CAP_USD;
  const monthClipSeconds = options.monthClipSeconds ?? DEFAULT_MONTH_CLIP_SECONDS;
  const minutesPerClip = options.minutesPerClip ?? DEFAULT_MINUTES_PER_CLIP;

  let timeline = null;
  try {
    timeline = estimateTimeline(doc);
  } catch {
    timeline = null;
  }
  const { shots: rows, cast } = normalize(doc, { timeline });
  const framesOf = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, scene.end_frame - scene.start_frame]));
  const cutLimit = production ? PRODUCTION_SHOT_SECONDS : MAX_SOURCE_CLIP_SECONDS;

  const shots = rows.filter((row) => !row.card).map((row, index) => {
    const data = row.data ?? {};
    const frames = framesOf.get(row.id) ?? Math.round(row.seconds * FPS);
    const visual = data.source ? "cut" : data.visual === "still" ? "still" : "clip";
    const endFrame = visual === "clip" && Boolean(data.end_frame?.prompt);
    const bought = visual === "clip" ? secondsBought(frames, model, resolution) : 0;
    const imagesOne = visual === "cut" ? 0 : 1 + (endFrame ? 1 : 0);
    const imagesCap = visual === "cut" ? 0 : keyframeTakes + (endFrame ? 1 : 0);
    const judgeOne = visual === "cut" ? 0 : 1 + (visual === "clip" ? 1 : 0);
    const judgeCap = visual === "cut" ? 0 : keyframeTakes + (visual === "clip" ? clipTakes : 0);
    const clipOne = bought * pricePerSecond;
    return {
      index,
      id: row.id,
      seconds: round2(row.seconds),
      frames,
      visual,
      bought_s: bought,
      end_frame: endFrame,
      images_one: imagesOne,
      images_cap: imagesCap,
      judge_one: judgeOne,
      judge_cap: judgeCap,
      usd_one: round4(imagesOne * imagePrice + judgeOne * judgePrice + clipOne),
      usd_cap: round4(imagesCap * imagePrice + judgeCap * judgePrice + (visual === "clip" ? clipTakes : 0) * clipOne),
      size: shotSize(data),
      look_only: isLookOnly(data),
      setup: setupKey(data),
      cast: castKey(data),
      silent: row.silent,
      source: data.source ?? null,
      lines: row.lines.length,
    };
  });

  // An existing data.source cut is checked against the seconds its source actually buys under this
  // model (clips.mjs marks it needs_review only after the source was paid for): from_s plus the cut's
  // own length must fit inside min(bought, the lint or profile limit).
  const byId = new Map(shots.map((shot) => [shot.id, shot]));
  const promptOf = new Map(rows.map((row) => [row.id, row.data?.prompt ?? ""]));
  for (const shot of shots) {
    if (!shot.source) continue;
    const origin = byId.get(shot.source.shot) ?? null;
    const room = origin?.visual === "clip" ? Math.min(origin.bought_s, cutLimit) : null;
    shot.source_room_s = room;
    shot.source_fits = room !== null && Number(shot.source.from_s ?? 0) + shot.frames / FPS <= room + 1e-9;
  }

  const clipShots = shots.filter((shot) => shot.visual === "clip");
  const stillShots = shots.filter((shot) => shot.visual === "still");
  const cutShots = shots.filter((shot) => shot.visual === "cut");
  const drawnShots = shots.filter((shot) => shot.visual !== "cut");
  const characters = cast ? doc.characters.length : 0;
  const look = resolveLook(doc.look);
  const candidates = look.candidates ?? DEFAULT_LOOK_CANDIDATES;
  const sheets = characters * candidates;
  const music = resolveMusic(doc);
  const clipSecondsOne = sum(clipShots, "bought_s");
  const stages = {
    look: {
      images_one: sheets,
      images_cap: sheets * MAX_LOOK_ROUNDS,
      judge_one: sheets,
      judge_cap: sheets * MAX_LOOK_ROUNDS,
      usd_one: round4(sheets * imagePrice),
      usd_cap: round4(sheets * MAX_LOOK_ROUNDS * imagePrice),
      note: cast ? `${characters} 角色 × ${candidates} 張候選（look.candidates，預設 ${DEFAULT_LOOK_CANDIDATES}）；最壞 ${MAX_LOOK_ROUNDS} 輪` : "沒有角色：不畫人設表，也沒有 look 關卡",
    },
    keyframes: {
      images_one: sum(drawnShots, "images_one"),
      images_cap: sum(drawnShots, "images_cap"),
      end_frames: drawnShots.filter((shot) => shot.end_frame).length,
      judge_one: drawnShots.length,
      judge_cap: drawnShots.length * keyframeTakes,
      usd_one: round4(sum(drawnShots, "images_one") * imagePrice),
      usd_cap: round4(sum(drawnShots, "images_cap") * imagePrice),
      note: `${drawnShots.length} 鏡各一張 keyframe（cut 的鏡頭不畫），end_frame 另畫一張、不評審（keyframes --dry-run 會多算它一次 judge）`,
    },
    clips: {
      shots: clipShots.length,
      clip_seconds_one: clipSecondsOne,
      clip_seconds_cap: clipSecondsOne * clipTakes,
      judge_one: clipShots.length,
      judge_cap: clipShots.length * clipTakes,
      usd_one: round4(clipSecondsOne * pricePerSecond),
      usd_cap: round4(clipSecondsOne * clipTakes * pricePerSecond),
      note: `${model} ${resolution ?? ""} ${unit(pricePerSecond)}/s；still 和 cut 的鏡頭不買片段`,
    },
    music: {
      tracks: music?.prompt ? 1 : 0,
      usd: music?.prompt ? PRICES[DEFAULT_MUSIC_MODEL].usd_per_track : 0,
      note: music?.prompt ? `${DEFAULT_MUSIC_MODEL} 一首 ${unit(PRICES[DEFAULT_MUSIC_MODEL].usd_per_track)}` : music?.track ? "站主自己的音軌：不花錢" : "沒有音樂",
    },
  };
  stages.judge = {
    calls_one: stages.look.judge_one + stages.keyframes.judge_one + stages.clips.judge_one,
    calls_cap: stages.look.judge_cap + stages.keyframes.judge_cap + stages.clips.judge_cap,
    note: `每次 ${unit(judgePrice)}（${PRICES.judge.source}）`,
  };
  stages.judge.usd_one = round4(stages.judge.calls_one * judgePrice);
  stages.judge.usd_cap = round4(stages.judge.calls_cap * judgePrice);
  const totals = {
    usd_one: round4(stages.look.usd_one + stages.keyframes.usd_one + stages.clips.usd_one + stages.judge.usd_one + stages.music.usd),
    usd_cap: round4(stages.look.usd_cap + stages.keyframes.usd_cap + stages.clips.usd_cap + stages.judge.usd_cap + stages.music.usd),
    seconds: round2(sum(shots, "seconds")),
  };

  let planView = null;
  if (plan && plan.vendor === "hailuo") {
    const res = wantedResolution && Object.hasOwn(plan.credits_per_second, wantedResolution) ? wantedResolution : plan.default_resolution;
    const perShot = clipShots.map((shot) => {
      const seconds = hailuoSeconds(shot.frames);
      const credits = seconds * plan.credits_per_second[res];
      return { id: shot.id, seconds, credits, usd_page: round4(seconds * plan.page_usd_per_second[res]), usd_fee: round4((credits * plan.fee_usd) / plan.credits) };
    });
    const creditsOne = sum(perShot, "credits");
    const secondsOne = sum(perShot, "seconds");
    const feeOne = (creditsOne * plan.fee_usd) / plan.credits;
    const roundsOne = Math.ceil(clipShots.length / plan.running);
    const roundsCap = Math.ceil((clipShots.length * clipTakes) / plan.running);
    planView = {
      id: planId,
      vendor: plan.vendor,
      label: plan.label,
      fee_usd: plan.fee_usd,
      fee_annual_monthly_usd: plan.fee_annual_monthly_usd,
      credits: plan.credits,
      resolution: res,
      credits_per_second: plan.credits_per_second[res],
      credits_basis: HAILUO_CREDITS_BASIS[res],
      page_usd_per_second: plan.page_usd_per_second[res],
      shots: perShot,
      seconds_one: secondsOne,
      credits_one: creditsOne,
      credits_cap: creditsOne * clipTakes,
      usd_page_one: round4(secondsOne * plan.page_usd_per_second[res]),
      usd_page_cap: round4(secondsOne * clipTakes * plan.page_usd_per_second[res]),
      usd_fee_one: round4(feeOne),
      usd_fee_cap: round4(feeOne * clipTakes),
      share_one: round4(creditsOne / plan.credits),
      share_cap: round4((creditsOne * clipTakes) / plan.credits),
      running: plan.running,
      queued: plan.queued,
      rounds_one: roundsOne,
      rounds_cap: roundsCap,
      minutes_per_clip: minutesPerClip,
      hours_one: round2((roundsOne * minutesPerClip) / 60),
      hours_cap: round2((roundsCap * minutesPerClip) / 60),
      images: plan.images,
      // The same clips on the server route, and the seconds a month the plan must really be used
      // for to beat it (the fee divided by the server's price a second; unused credits expire).
      server_model: model,
      server_usd_per_second: pricePerSecond,
      server_clip_usd_one: stages.clips.usd_one,
      plan_seconds_per_month: Math.floor(plan.credits / plan.credits_per_second[res]),
      breakeven_seconds_monthly: Math.ceil(plan.fee_usd / pricePerSecond),
      breakeven_seconds_annual: Math.ceil(plan.fee_annual_monthly_usd / pricePerSecond),
      unverified: false,
      notes: [
        plan.note,
        `網頁的 H3 一支 4–15 秒整數，所以這裡每鏡買 ceil(需要的秒數)（最少 4）而不是 API 路線的貼模型長度；--resolution 768p|2k 選檔位（2K 輸出 2560×1440、768P 低於 1080p，哪個該選未驗）`,
        HAILUO_OUTPUT_NOTE,
        `keyframes、人設表、音樂、judge 仍走伺服器 API（上面的 US$）；${plan.images}`,
        `方案做出的片段用 clips import 帶進產線（references/stage-preconditions.md 最後一節）：跟買來的 take 過同一組 ffmpeg 檢查，帳本記點數；美元要自己用 --usd 給，judge 要帶 --judge 才問`,
        `「幾小時」用每支 ${minutesPerClip} 分鐘（--minutes-per-clip）的假設算；量過的只有一支：H3 2K 5 秒、沒有排隊約 4 分 40 秒（實測 ${PLANS_MEASURED_ON}）；同時跑 ${plan.running}、排隊 ${plan.queued}`,
        ...(plan.unlimited ? [plan.unlimited] : []),
      ],
    };
  } else if (plan && plan.vendor === "kling") {
    const creditsPerVideo = options.creditsPerVideo ?? plan.credits_per_video;
    const perShot = clipShots.map((shot) => {
      const videos = klingVideos(shot.frames);
      const credits = videos * creditsPerVideo;
      return { id: shot.id, videos, seconds: videos * plan.video_seconds, credits, usd_fee: round4((credits * plan.fee_usd) / plan.credits) };
    });
    const creditsOne = sum(perShot, "credits");
    const feeOne = (creditsOne * plan.fee_usd) / plan.credits;
    planView = {
      id: planId,
      vendor: plan.vendor,
      label: plan.label,
      fee_usd: plan.fee_usd,
      first_month_usd: plan.first_month_usd,
      credits: plan.credits,
      credits_per_video: creditsPerVideo,
      video_seconds: plan.video_seconds,
      shots: perShot,
      videos_one: sum(perShot, "videos"),
      credits_one: creditsOne,
      credits_cap: creditsOne * clipTakes,
      usd_fee_one: round4(feeOne),
      usd_fee_cap: round4(feeOne * clipTakes),
      share_one: round4(creditsOne / plan.credits),
      share_cap: round4((creditsOne * clipTakes) / plan.credits),
      running: plan.running,
      queued: plan.queued,
      rounds_one: clipShots.length,
      rounds_cap: clipShots.length * clipTakes,
      minutes_per_clip: minutesPerClip,
      hours_one: round2((clipShots.length * minutesPerClip) / 60),
      hours_cap: round2((clipShots.length * clipTakes * minutesPerClip) / 60),
      server_model: model,
      server_usd_per_second: pricePerSecond,
      server_clip_usd_one: stages.clips.usd_one,
      plan_seconds_per_month: Math.floor(plan.credits / creditsPerVideo) * plan.video_seconds,
      breakeven_seconds_monthly: Math.ceil(plan.fee_usd / pricePerSecond),
      breakeven_seconds_first_month: Math.ceil(plan.first_month_usd / pricePerSecond),
      unverified: true,
      notes: [
        plan.note,
        `一鏡需要幾支 ${plan.video_seconds} 秒影片 = ceil(需要的秒數 ÷ ${plan.video_seconds})；這是估價單位：kling-video-v3_0 可以直接要 3–15 秒整數（實測 ${PLANS_MEASURED_ON}），${plan.video_seconds}、10 秒以外的 credits 沒有來源`,
        `官方 CLI（npm @klingai/cli-global，站主 ${PLANS_MEASURED_ON} 選的）與官方 MCP（kling.ai/mcp）都用 Kling 帳號登入；kling account 回 membershipType 與 availableRemainCredits，讀起來是會員 credits，沒有用付費生成確認。社群 MCP（github.com/199-mcp/mcp-kling）用開發者 API 金鑰，扣的是資源包，不是會員 credits`,
        `image_to_video 要傳 enable_audio false 與 prefer_multi_shots false（兩個預設都是 true；一鏡是一個連續鏡頭）；NORMAL 帳號列的模型都只有 720p，付費方案在 CLI 上有沒有 1080p 未驗`,
        "同時幾支沒寫明（「無限排隊」）：這裡的「幾小時」把片段當一支接一支算，未驗證",
        "keyframes、人設表、音樂、judge 仍走伺服器 API（上面的 US$）；今天沒有 Kling adapter，做出的片段用 clips import 帶進產線",
      ],
    };
  }

  const levers = { cuts: [], stills: null, long: [], merges: [] };
  for (const shot of clipShots) {
    if (shot.setup === "|") continue;
    const earlier = clipShots.filter((other) => other.index < shot.index && other.setup === shot.setup);
    for (const origin of earlier) {
      const room = Math.min(origin.bought_s, cutLimit);
      const need = shot.frames / FPS;
      let from = Math.ceil(origin.frames / FPS);
      let repeats = false;
      if (from + need > room) {
        if (need > room) continue;
        from = 0;
        repeats = true;
      }
      const similarity = round2(promptSimilarity(promptOf.get(shot.id), promptOf.get(origin.id)));
      levers.cuts.push({ shot: shot.id, from_shot: origin.id, from_s: from, needed_s: round2(need), room_s: room, repeats_frames: repeats, prompt_similarity: similarity, picture_differs: similarity < PICTURE_SIMILARITY_MIN, saving_usd: shot.usd_one, saving_cap_usd: shot.usd_cap });
      break;
    }
  }
  if (tier && production) {
    levers.stills = { tier, note: "production profile 不准靜圖（tools/video/core/lint.mjs productionShotProblems）：tier 在這裡沒有槓桿" };
  } else if (tier) {
    const allowed = Math.ceil(TIER_CLIP_SHARE_MAX[tier] * shots.length);
    const over = Math.max(0, clipShots.length - allowed);
    const ranked = [...clipShots].sort((a, b) => Number(b.look_only) - Number(a.look_only) || a.frames - b.frames);
    const chosen = ranked.slice(0, over);
    const savingOf = (shot) => shot.bought_s * pricePerSecond + judgePrice;
    levers.stills = {
      tier,
      allowed_clips: allowed,
      clip_shots: clipShots.length,
      still_shots: stillShots.length,
      over_by: over,
      look_only_available: clipShots.filter((shot) => shot.look_only).length,
      candidates: chosen.map((shot) => ({ id: shot.id, look_only: shot.look_only, seconds: shot.seconds, saving_usd: round4(savingOf(shot)) })),
      saving_usd: round4(chosen.reduce((total, shot) => total + savingOf(shot), 0)),
      saving_cap_usd: round4(chosen.reduce((total, shot) => total + clipTakes * savingOf(shot), 0)),
      total_one_tiered: round4(totals.usd_one - chosen.reduce((total, shot) => total + savingOf(shot), 0)),
    };
  }
  for (const shot of shots) {
    if (shot.seconds > TARGETS.longestShotSeconds) levers.long.push({ id: shot.id, seconds: shot.seconds, visual: shot.visual, over_production: shot.seconds > PRODUCTION_SHOT_SECONDS, over_clip: shot.seconds > MAX_CLIP_SECONDS });
  }
  for (let at = 0; at + 1 < shots.length; at++) {
    const a = shots[at];
    const b = shots[at + 1];
    if (a.visual !== "clip" || b.visual !== "clip" || a.setup === "|" || a.setup !== b.setup || a.cast !== b.cast) continue;
    const need = (a.frames + b.frames) / FPS;
    if (need > PRODUCTION_SHOT_SECONDS) continue;
    const merged = secondsBought(a.frames + b.frames, model, resolution);
    levers.merges.push({ shots: [a.id, b.id], seconds: round2(need), bought_separately_s: a.bought_s + b.bought_s, bought_merged_s: merged, saving_usd: round4((a.bought_s + b.bought_s - merged) * pricePerSecond + imagePrice + 2 * judgePrice) });
  }

  const problems = [];
  for (const shot of cutShots.filter((each) => !each.source_fits)) {
    const origin = byId.get(shot.source.shot);
    problems.push(origin?.visual === "clip"
      ? `${shot.id} 從 ${shot.source.shot} 的 ${shot.source.from_s} s 切、需要 ${round2(shot.frames / FPS)} s，但 ${shot.source.shot} 在 ${model} 下只買 ${shot.source_room_s} s（clips 會在來源買下之後才把它標 needs_review）：from_s 提早、來源鏡頭寫長（多買秒數），或換成自己的片段`
      : `${shot.id} 的 data.source 指向 ${shot.source.shot}，它不是 clip 鏡（不在這份 video.json、是 still 或本身是切鏡），沒有素材可切`);
  }
  if (totals.usd_cap > cap) problems.push(`最壞情況 ${usd(totals.usd_cap)} 超過每影片上限 ${usd(cap)}（--cap；站上 max_usd_per_video，預設 ${DEFAULT_CAP_USD}）：先用槓桿把它壓到上限內，否則 clips 跑到一半會停在 video_media_cap`);
  if (stages.clips.clip_seconds_cap > monthClipSeconds) problems.push(`最壞情況要買 ${stages.clips.clip_seconds_cap} 秒片段，超過每月額度 ${monthClipSeconds} 秒（--month-clip-seconds；站上 monthly_clip_seconds_budget，預設 ${DEFAULT_MONTH_CLIP_SECONDS}）`);
  if (levers.stills?.over_by > 0) problems.push(`${tier} tier 最多 ${levers.stills.allowed_clips} 支片段，劇本有 ${clipShots.length} 支：lint 會擋（tools/video/core/drama.mjs visualTierProblems）；把 ${levers.stills.candidates.map((shot) => shot.id).join(", ")} 改成 visual "still"`);
  if (production) {
    for (const shot of levers.long.filter((each) => each.over_production)) problems.push(`${shot.id} 約 ${shot.seconds} 秒：production profile 一鏡最多 ${PRODUCTION_SHOT_SECONDS} 秒（lint 錯誤），拆鏡或縮台詞`);
    for (const shot of stillShots) problems.push(`${shot.id} 是 still：production profile 不准靜圖（lint 錯誤）`);
  }

  return {
    basis: timeline ? "lint 的估法（tools/video/core/timeline.mjs estimateTimeline）：一個字 0.24 s、一句停 0.3 s、一鏡間隔 0.7 s" : "estimateTimeline 讀不了這份檔，改用 craft.normalize 的估法（同樣的常數）",
    model,
    resolution,
    production,
    prices: {
      clip: { model, usd_per_second: pricePerSecond, source: Number.isFinite(options.pricePerSecond) ? "--price-per-second" : PRICES[model].source, note: PRICES[model]?.note ?? null },
      image: { model: DEFAULT_IMAGE_MODEL, usd_per_image: imagePrice, source: Number.isFinite(options.imagePrice) ? "--image-price" : PRICES[DEFAULT_IMAGE_MODEL].source },
      judge: { usd_per_call: judgePrice, source: PRICES.judge.source },
      music: { model: DEFAULT_MUSIC_MODEL, usd_per_track: PRICES[DEFAULT_MUSIC_MODEL].usd_per_track, source: PRICES[DEFAULT_MUSIC_MODEL].source },
    },
    takes: { keyframes: keyframeTakes, clips: clipTakes, look_rounds: MAX_LOOK_ROUNDS },
    shots,
    counts: { shots: shots.length, clips: clipShots.length, stills: stillShots.length, cuts: cutShots.length, characters, silent: shots.filter((shot) => shot.silent).length },
    stages,
    totals,
    plan: planView,
    levers,
    verdict: { ok: problems.length === 0, cap, month_clip_seconds: monthClipSeconds, usd_one: totals.usd_one, usd_cap: totals.usd_cap, clip_seconds_one: stages.clips.clip_seconds_one, clip_seconds_cap: stages.clips.clip_seconds_cap, problems },
  };
}

/** 文字版：一鏡一行，再來各階段小計、方案、槓桿、裁定。 */
export function renderEstimate(report, file) {
  const out = [];
  const { counts, stages, totals, prices } = report;
  out.push(`${file}：${counts.shots} 鏡（clip ${counts.clips}、still ${counts.stills}、cut ${counts.cuts}）、${counts.characters} 角色，約 ${totals.seconds.toFixed(1)} s（${report.basis}）`);
  out.push(`價目：片段 ${prices.clip.model} ${report.resolution ?? ""} ${unit(prices.clip.usd_per_second)}/s（${prices.clip.source}）；圖片 ${prices.image.model} ${unit(prices.image.usd_per_image)}/張（${prices.image.source}）；judge ${unit(prices.judge.usd_per_call)}/次；take 上限 keyframe ${report.takes.keyframes}、clip ${report.takes.clips}、look ${report.takes.look_rounds} 輪${report.production ? "；production profile（一鏡 ≤ 8 s、不准 still）" : ""}`);
  if (prices.clip.note) out.push(`  ${prices.clip.note}`);
  out.push("");
  out.push("鏡頭        需要   形式   買秒  圖(1/上限)  judge(1/上限)  US$(1 take)  US$(上限)  尺寸     只有看");
  for (const shot of report.shots) {
    out.push(`${shot.id.padEnd(11)} ${String(shot.seconds.toFixed(1)).padStart(5)}  ${shot.visual.padEnd(5)}  ${String(shot.bought_s || "-").padStart(4)}  ${`${shot.images_one}/${shot.images_cap}`.padStart(9)}  ${`${shot.judge_one}/${shot.judge_cap}`.padStart(12)}  ${shot.usd_one.toFixed(2).padStart(10)}  ${shot.usd_cap.toFixed(2).padStart(9)}  ${String(shot.size ?? "?").padEnd(7)}  ${shot.look_only ? "yes" : "-"}${shot.source ? `  cut from ${shot.source.shot} @ ${shot.source.from_s} s（來源買 ${shot.source_room_s ?? "?"} s${shot.source_fits ? "" : "：超出"}）` : ""}${shot.silent ? "  （沒有台詞也沒有 action_seconds：lint 會拒絕）" : ""}`);
  }
  out.push("");
  out.push("階段小計（1 take → 上限）：");
  out.push(`  look       圖 ${stages.look.images_one} → ${stages.look.images_cap}，${usd(stages.look.usd_one)} → ${usd(stages.look.usd_cap)}；${stages.look.note}`);
  out.push(`  keyframes  圖 ${stages.keyframes.images_one} → ${stages.keyframes.images_cap}（end_frame ${stages.keyframes.end_frames}），${usd(stages.keyframes.usd_one)} → ${usd(stages.keyframes.usd_cap)}；${stages.keyframes.note}`);
  out.push(`  clips      ${stages.clips.shots} 支、${stages.clips.clip_seconds_one} s → ${stages.clips.clip_seconds_cap} s，${usd(stages.clips.usd_one)} → ${usd(stages.clips.usd_cap)}；${stages.clips.note}`);
  out.push(`  judge      ${stages.judge.calls_one} 次 → ${stages.judge.calls_cap} 次，${usd(stages.judge.usd_one)} → ${usd(stages.judge.usd_cap)}；${stages.judge.note}`);
  out.push(`  music      ${stages.music.tracks} 首，${usd(stages.music.usd)}；${stages.music.note}`);
  out.push(`一集：1 take ${usd(totals.usd_one)}；最壞 ${usd(totals.usd_cap)}`);
  if (report.plan) {
    const plan = report.plan;
    out.push("");
    if (plan.vendor === "hailuo") {
      out.push(`方案 ${plan.id}（${plan.label}，月費 ${usd(plan.fee_usd)}、年繳折合 ${usd(plan.fee_annual_monthly_usd)}/月，${plan.credits} credits/月；hailuoai.video 訂閱頁 ${PLANS_READ_ON} 讀）：H3 ${plan.resolution} ${plan.credits_per_second} credits/s（${plan.credits_basis}），頁面標 ${unit(plan.page_usd_per_second)}/s`);
      for (const shot of plan.shots) out.push(`  ${shot.id.padEnd(11)} ${String(shot.seconds).padStart(2)} s  ${String(shot.credits).padStart(4)} credits  ≈ ${usd(shot.usd_page)}（頁面價）/ ${usd(shot.usd_fee)}（月費攤）`);
      out.push(`  片段合計 ${plan.seconds_one} s：${plan.credits_one} credits（1 take）→ ${plan.credits_cap}（上限），佔月額 ${(plan.share_one * 100).toFixed(0)}% → ${(plan.share_cap * 100).toFixed(0)}%；≈ ${usd(plan.usd_page_one)} → ${usd(plan.usd_page_cap)}（頁面價）、${usd(plan.usd_fee_one)} → ${usd(plan.usd_fee_cap)}（月費攤）`);
      out.push(`  佇列：同時 ${plan.running} 支、排隊 ${plan.queued}；${plan.rounds_one} 輪 → ${plan.rounds_cap} 輪，約 ${plan.hours_one} → ${plan.hours_cap} 小時（每支 ${plan.minutes_per_clip} 分鐘的假設）`);
      out.push(`  對照伺服器 ${plan.server_model}：片段 ${usd(plan.server_clip_usd_one)}（1 take，不含 judge）vs 方案 ${usd(plan.usd_fee_one)}（月費攤）／${usd(plan.usd_page_one)}（頁面價＝年繳）；損益平衡：月繳要這個月真的用掉 ≥ ${plan.breakeven_seconds_monthly} s、年繳 ≥ ${plan.breakeven_seconds_annual} s（月費 ÷ 伺服器 ${unit(plan.server_usd_per_second)}/s；沒用完的 credits 月底歸零），而方案一個月只有 ${plan.plan_seconds_per_month} s 的 ${plan.resolution}${plan.breakeven_seconds_annual > plan.plan_seconds_per_month ? "：靠 credits 贏不了這個模型" : ""}`);
    } else {
      out.push(`方案 ${plan.id}（${plan.label}，月費 ${usd(plan.fee_usd)}、首月 ${usd(plan.first_month_usd)}，${plan.credits} credits/月；kling.ai 會員頁 ${PLANS_READ_ON} 讀）：每支 ${plan.video_seconds} s 影片 ${plan.credits_per_video} credits【未驗證】`);
      for (const shot of plan.shots) out.push(`  ${shot.id.padEnd(11)} ${shot.videos} 支  ${String(shot.credits).padStart(4)} credits  ≈ ${usd(shot.usd_fee)}（月費攤）`);
      out.push(`  片段合計 ${plan.videos_one} 支：${plan.credits_one} credits（1 take）→ ${plan.credits_cap}（上限），佔月額 ${(plan.share_one * 100).toFixed(0)}% → ${(plan.share_cap * 100).toFixed(0)}%；≈ ${usd(plan.usd_fee_one)} → ${usd(plan.usd_fee_cap)}`);
      out.push(`  佇列：同時幾支未知（無限排隊）；一支接一支約 ${plan.hours_one} → ${plan.hours_cap} 小時（每支 ${plan.minutes_per_clip} 分鐘的假設）`);
      out.push(`  對照伺服器 ${plan.server_model}：片段 ${usd(plan.server_clip_usd_one)}（1 take，不含 judge）vs 方案 ${usd(plan.usd_fee_one)}（月費攤，credits 未驗）；損益平衡：月繳要這個月真的用掉 ≥ ${plan.breakeven_seconds_monthly} s、首月價 ≥ ${plan.breakeven_seconds_first_month} s（月費 ÷ 伺服器 ${unit(plan.server_usd_per_second)}/s），方案一個月約 ${plan.plan_seconds_per_month} s（${plan.credits} ÷ ${plan.credits_per_video} 支 × ${plan.video_seconds} s）`);
    }
    for (const note of plan.notes) out.push(`  註：${note}`);
  }
  const { levers } = report;
  out.push("");
  out.push("槓桿：");
  if (levers.cuts.length) for (const cut of levers.cuts) out.push(`  cut   ${cut.shot} 可以從 ${cut.from_shot} 的片段 ${cut.from_s} s 切（需要 ${cut.needed_s} s，片段在這個模型下有 ${cut.room_s} s${cut.repeats_frames ? "；會重播它的開頭" : ""}）：data.source: { shot: "${cut.from_shot}", from_s: ${cut.from_s} }，省 ${usd(cut.saving_usd)}（上限 ${usd(cut.saving_cap_usd)}）${cut.picture_differs ? `；同鏡位、畫面不同（prompt 相似度 ${Math.round(cut.prompt_similarity * 100)}%）：要人看，不算省` : ""}`);
  else out.push("  cut   沒有：沒有後面的 clip 鏡頭重複前面某一鏡的 camera 行加 prompt 第一子句，或塞不進它的片段（候選只比鏡位，畫面要人看）");
  if (levers.stills?.candidates) {
    const stills = levers.stills;
    out.push(`  still ${stills.tier} tier 最多 ${stills.allowed_clips} 支片段（${(TIER_CLIP_SHARE_MAX[stills.tier] * 100).toFixed(0)}%，docs/videos/BINGE.md），劇本 clip ${stills.clip_shots}、still ${stills.still_shots}${stills.over_by ? `：多 ${stills.over_by} 支，先改 ${stills.candidates.map((shot) => `${shot.id}${shot.look_only ? "（只有看）" : ""}`).join(", ")}，省 ${usd(stills.saving_usd)}（上限 ${usd(stills.saving_cap_usd)}）→ 一集 ${usd(stills.total_one_tiered)}` : "：在 tier 內"}；只有看的鏡頭 ${stills.look_only_available} 支最適合當 still`);
  } else if (levers.stills?.note) out.push(`  still ${levers.stills.note}`);
  else out.push(`  still 沒給 --tier：劇本自己標了 ${report.counts.stills} 支 still；一支 still 省掉它的片段和一次 judge，只剩一張圖`);
  if (levers.long.length) for (const shot of levers.long) out.push(`  long  ${shot.id} 約 ${shot.seconds} s：超過 ${TARGETS.longestShotSeconds} s 的 craft 目標${shot.over_production ? "、production 的 8 s 上限" : ""}${shot.over_clip ? "、模型的 10 s" : ""}；拆成兩鏡或縮台詞`);
  else out.push(`  long  沒有超過 ${TARGETS.longestShotSeconds} s 的鏡頭`);
  if (levers.merges.length) for (const merge of levers.merges) out.push(`  merge ${merge.shots.join(" + ")}（同機位同人，合計 ${merge.seconds} s）：分開買 ${merge.bought_separately_s} s、合併買 ${merge.bought_merged_s} s，省 ${usd(merge.saving_usd)}`);
  else out.push("  merge 沒有相鄰、同機位同人、合計 8 s 內的兩鏡");
  out.push("");
  out.push(`裁定：${report.verdict.ok ? `過：最壞 ${usd(totals.usd_cap)} ≤ 上限 ${usd(report.verdict.cap)}，最壞 ${report.verdict.clip_seconds_cap} s ≤ 月額 ${report.verdict.month_clip_seconds} s` : "不過"}`);
  for (const problem of report.verdict.problems) out.push(`  ✗ ${problem}`);
  return out.join("\n");
}

const number = (value, name) => {
  if (value === undefined) return undefined;
  const parsed = Number(value);
  if (!Number.isFinite(parsed) || parsed < 0) throw new Error(`${name} must be a number, not "${value}"`);
  return parsed;
};

export function main(argv, stdout = process.stdout, stderr = process.stderr) {
  let values;
  let positionals;
  try {
    ({ values, positionals } = parseArgs({
      args: argv,
      options: {
        tier: { type: "string" },
        model: { type: "string" },
        resolution: { type: "string" },
        plan: { type: "string" },
        "image-price": { type: "string" },
        "price-per-second": { type: "string" },
        "credits-per-video": { type: "string" },
        "minutes-per-clip": { type: "string" },
        "keyframe-takes": { type: "string" },
        "clip-takes": { type: "string" },
        cap: { type: "string" },
        "month-clip-seconds": { type: "string" },
        production: { type: "boolean" },
        strict: { type: "boolean" },
        json: { type: "boolean" },
      },
      allowPositionals: true,
      strict: true,
    }));
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  const file = positionals[0];
  if (!file) {
    stderr.write("usage: episode_estimate.mjs <video.json> [--tier clips|hybrid|stills] [--model <clip model id>] [--resolution 1080p|720p|768p|2k (the server model's; with --plan hailuo:* also the H3 tier)] [--plan hailuo:pro|kling:pro|...] [--image-price N] [--price-per-second N] [--credits-per-video N] [--keyframe-takes N] [--clip-takes N] [--cap N] [--month-clip-seconds N] [--production] [--strict] [--json]\n");
    return 2;
  }
  let report;
  try {
    const doc = JSON.parse(readFileSync(file, "utf8").replace(/^﻿/, ""));
    report = estimateEpisode(doc, {
      tier: values.tier,
      model: values.model,
      resolution: values.resolution,
      plan: values.plan,
      imagePrice: number(values["image-price"], "--image-price"),
      pricePerSecond: number(values["price-per-second"], "--price-per-second"),
      creditsPerVideo: number(values["credits-per-video"], "--credits-per-video"),
      minutesPerClip: number(values["minutes-per-clip"], "--minutes-per-clip"),
      keyframeTakes: number(values["keyframe-takes"], "--keyframe-takes"),
      clipTakes: number(values["clip-takes"], "--clip-takes"),
      cap: number(values.cap, "--cap"),
      monthClipSeconds: number(values["month-clip-seconds"], "--month-clip-seconds"),
      production: values.production,
    });
  } catch (error) {
    stderr.write(`${file}: ${error.message}\n`);
    return 2;
  }
  stdout.write(`${values.json ? JSON.stringify({ file, ...report }, null, 2) : renderEstimate(report, file)}\n`);
  return values.strict && !report.verdict.ok ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exitCode = main(process.argv.slice(2));
