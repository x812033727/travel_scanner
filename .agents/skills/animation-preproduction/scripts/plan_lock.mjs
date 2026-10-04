#!/usr/bin/env node
// 開拍鎖定與變更單：站主在花錢之前確認一次開拍鎖定包之後，把當下的劇本、每鏡的畫面與台詞、路線與設定、買幾秒、
// 定稿正文和預算寫成 <workdir>/plan/lock.json；之後任何改動先用 --check 對照鎖定，印出變更單（哪幾鏡改了、哪個雜湊
// 動了、會重畫重買什麼、要再 judge 幾次、哪個核准失效、哪些外部片段要重匯），讓站主決定再改；--ready 查備料清單裡
// 程式查得到的部分：鎖定之前跑一次放進鎖定包，送出第一支之前再跑一次。
//
//   node .agents/skills/animation-preproduction/scripts/plan_lock.mjs --slug <SLUG> | --file <video.json> --workdir <dir>
//     --write [--note "<站主怎麼說>"] [--assist on|off] [--force] | --check | --ready
//     [shot_plan.mjs 的規劃旗標：--route --plan --hailuo-model --model --resolution --handle --clip-takes
//      --expected-takes --pilot --production --timeline] [--root <repo>] [--json]
//
// --slug 時 --workdir 是放所有影片的目錄（VIDEO_WORKDIR 規則，同 tools/video）；給 --file 時 --workdir 是這支影片
// 自己的工作目錄。規劃旗標跟 shot_plan.mjs 同一組（PLAN_FLAGS），鎖的就是那一份計畫；--check、--ready、--write --force
// 沒給旗標就沿用鎖定檔裡的設定，給了就拿來跟鎖定比（換路線、換解析度也是變更）。--assist 記網頁的 AI 潤飾
// （Hailuo 的 AI Polish、Kling 的 AI Prompter）開或關。
// 離線、不花錢、不碰伺服器。結束碼：0；--check 有變更、--ready 有沒過的項目、--write 的計畫有做不進產線的問題是 1；
// 讀不到、鎖定檔壞了或版本不對、參數錯是 2。
import { createHash } from "node:crypto";
import { appendFileSync, existsSync, mkdirSync, renameSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { approvalState } from "../../../../tools/video/core/approvals.mjs";
import { isSourced, lookHash, resolveLook, shotCast } from "../../../../tools/video/core/drama.mjs";
import { atomicWrite, readJson } from "../../../../tools/video/core/paths.mjs";
import { screenplay } from "../../../../tools/video/core/screenplay.mjs";
import { speechHash, visualHash } from "../../../../tools/video/core/timeline.mjs";
import { shotPrompt } from "../../../../tools/video/media/keyframes.mjs";
import { PRICES } from "../../animation-production/scripts/episode_estimate.mjs";
import { loadInputs, PLAN_FLAGS, PLAN_USAGE, planEpisode, planOptions } from "./shot_plan.mjs";

export const LOCK_FILE = path.join("plan", "lock.json");
export const LOCK_VERSION = 2;
export const CHANGE_LOG = "changes.jsonl";
const GATES = ["script", "look", "audio", "storyboard"];
const sha = (value) => createHash("sha256").update(typeof value === "string" ? value : JSON.stringify(value)).digest("hex").slice(0, 16);

/**
 * 一鏡的三個指紋。畫面與台詞的欄位跟 tools/video/core/timeline.mjs 的 visualHash／speechHash 每鏡那一段相同：
 * 畫面 ＝ id、template、chapter、data、句子 id 與 reveal；台詞 ＝ 每句的文字、停頓、speaker、emotion、audio_ref 與
 * action_seconds。關鍵影格 ＝ keyframes.mjs 真的拿去問圖片模型與 judge 的東西（shotPrompt 的全文、characters、末格）：
 * #1193 起畫面請求與 judge 題目都沒變的鏡頭留著原來的圖與判定，所以只改 motion 不會重畫也不會重 judge 關鍵影格。
 */
export function shotPrints(scene, doc = null) {
  const lines = Array.isArray(scene.lines) ? scene.lines : [];
  const prints = {
    visual: sha([scene.id, scene.template, scene.chapter ?? null, scene.data ?? null, lines.map((line) => [line.id, line.reveal ?? 0])]),
    speech: sha([lines.map((line) => [line.id, line.text, line.pause_after_ms ?? null, line.speaker ?? "narrator", line.emotion ?? null, line.audio_ref ?? null]), scene.action_seconds ?? null]),
  };
  if (doc && scene.template === "shot") {
    prints.keyframe = isSourced(scene) ? null : sha([shotPrompt(scene, resolveLook(doc.look), shotCast(doc, scene)), scene.data?.characters ?? [], scene.data?.end_frame?.prompt ?? null]);
  }
  return prints;
}

/** 鎖定檔的內容（不含 created_at 與 note）。settings 是重建同一份計畫要的全部選項。 */
export function lockOf(doc, lexicon, plan, settings = {}) {
  const shots = {};
  const sceneById = new Map(doc.scenes.map((scene) => [scene.id, scene]));
  for (const shot of plan.shots) {
    shots[shot.id] = {
      ...shotPrints(sceneById.get(shot.id), doc),
      chapter: shot.chapter,
      setup: shot.setup,
      visual_kind: shot.visual,
      lines: shot.lines.length,
      source: shot.source,
      buy_s: shot.buy_s,
      risk: shot.risk.grade,
      risk_reasons: shot.risk.reasons.map((reason) => reason.id),
      cost: shot.cost,
      first_frame: shot.first_frame,
      end_frame: shot.end_frame,
      prompt: shot.prompt ? { text: shot.prompt.text, sha256: shot.prompt.sha256 } : null,
    };
  }
  let speech = null;
  try {
    speech = speechHash(doc, lexicon);
  } catch {
    speech = null;
  }
  const negative = plan.shots.find((shot) => shot.prompt?.negative)?.prompt.negative ?? null;
  return {
    version: LOCK_VERSION,
    route: plan.route,
    plan: plan.plan?.id ?? null,
    hailuo_model: plan.route === "hailuo" ? settings.hailuoModel ?? "h3" : null,
    model: plan.model,
    resolution: plan.resolution,
    handle_s: plan.handle_s,
    clip_takes: plan.clip_takes,
    expected_takes: plan.expected_takes,
    pilot: plan.batches[0]?.name === "小樣" ? plan.batches[0].shots : [],
    production: Boolean(settings.production),
    web_assist: settings.assist ?? null,
    negative: negative ? { text: negative, sha256: sha(negative), entry: "只貼進網頁真的有的負面欄；沒有就不貼" } : null,
    hashes: { look: lookHash(doc), visual: visualHash(doc), speech, script: sha(screenplay(doc)), document: sha(doc) },
    order: doc.scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id),
    shots,
    totals: plan.totals,
    batches: plan.batches.map(({ name, shots: members, buys }) => ({ name, shots: members, buys })),
    counts: plan.counts,
  };
}

/** 鎖定檔裡的設定 → planEpisode 的選項（--check、--ready、--write --force 沒給旗標時用它重建同一份計畫）。 */
export function settingsOf(lock) {
  return {
    route: lock.route,
    ...(lock.plan ? { plan: lock.plan } : {}),
    ...(lock.hailuo_model ? { hailuoModel: lock.hailuo_model } : {}),
    ...(lock.route === "server" && lock.model ? { model: lock.model } : {}),
    ...(lock.resolution ? { resolution: lock.resolution } : {}),
    ...(lock.route !== "server" && Number.isFinite(lock.handle_s) ? { handle: lock.handle_s } : {}),
    ...(Number.isFinite(lock.clip_takes) ? { clipTakes: lock.clip_takes } : {}),
    ...(lock.expected_takes ? { expectedTakes: lock.expected_takes } : {}),
    ...(Array.isArray(lock.pilot) && lock.pilot.length ? { pilot: lock.pilot } : {}),
    ...(lock.production ? { production: true } : {}),
  };
}

/** 讀得懂的鎖定檔才拿來比；舊版或壞掉的回原因。 */
export function lockProblem(lock) {
  if (!lock || typeof lock !== "object") return "not a JSON object";
  if (lock.version !== LOCK_VERSION) return `version ${lock.version ?? "missing"}, this script writes version ${LOCK_VERSION}: lock again with --write --force after checking the plan by hand`;
  for (const key of ["route", "hashes", "shots", "order", "totals"]) if (!lock[key]) return `missing ${key}`;
  return null;
}

const SETTING_KEYS = ["route", "plan", "hailuo_model", "model", "resolution", "handle_s", "clip_takes"];

/**
 * 現在的劇本與計畫對鎖定檔：{ changed, look, hashes, settings, added, removed, reordered, shots, impact, lines }。
 * keyframes 與 clips 的 manifest 決定「已畫」「已買」「已匯入」；approved 是現在 approved 的關卡（null＝不知道，全列）。
 */
export function compareLock(lock, current, { keyframes = null, clips = null, approved = null } = {}) {
  const moved = (key) => (lock.hashes?.[key] ?? null) !== (current.hashes?.[key] ?? null);
  const changes = {
    look: moved("look"),
    hashes: { look: moved("look"), visual: moved("visual"), speech: moved("speech"), script: moved("script") },
    settings: SETTING_KEYS.filter((key) => JSON.stringify(lock[key] ?? null) !== JSON.stringify(current[key] ?? null)),
    added: [],
    removed: [],
    reordered: false,
    shots: [],
  };
  const lockedIds = Object.keys(lock.shots);
  const currentIds = Object.keys(current.shots);
  changes.added = currentIds.filter((id) => !lock.shots[id]);
  changes.removed = lockedIds.filter((id) => !current.shots[id]);
  const common = lock.order.filter((id) => current.shots[id]);
  changes.reordered = common.join("|") !== current.order.filter((id) => lock.shots[id]).join("|");
  for (const id of common) {
    const before = lock.shots[id];
    const after = current.shots[id];
    const entry = {
      id,
      visual: before.visual !== after.visual,
      keyframe: (before.keyframe ?? before.visual) !== (after.keyframe ?? after.visual),
      speech: before.speech !== after.speech,
      prompt: (before.prompt?.sha256 ?? null) !== (after.prompt?.sha256 ?? null),
      buy: before.buy_s !== after.buy_s ? [before.buy_s, after.buy_s] : null,
      kind: before.visual_kind !== after.visual_kind ? [before.visual_kind, after.visual_kind] : null,
      spoken: (after.lines ?? 0) > 0 || (before.lines ?? 0) > 0,
    };
    if (entry.visual || entry.speech || entry.prompt || entry.buy || entry.kind) changes.shots.push(entry);
  }
  const drawn = (id) => Boolean(keyframes?.shots?.[id]?.file);
  const boughtEntry = (id) => { const shot = clips?.shots?.[id]; return shot?.file && !shot.source && !shot.still ? shot : null; };
  const anyVisual = changes.look || changes.hashes.visual || changes.added.length > 0 || changes.removed.length > 0 || changes.reordered || changes.shots.some((shot) => shot.visual || shot.kind);
  const anySpeech = changes.hashes.speech || changes.added.length > 0 || changes.removed.length > 0 || changes.reordered || changes.shots.some((shot) => shot.speech);
  const rebuy = [];
  const lines = [];
  if (changes.look) {
    rebuy.push("全部：設定圖、每一張關鍵影格、每一支素材（look 在 lookHash 裡，快取鍵也含 negative 與參考圖）");
    lines.push("look（或角色 appearance、sheet_prompt）改了");
  }
  for (const shot of changes.shots) {
    const what = [
      shot.visual && (shot.keyframe ? "畫面欄位（prompt／camera／characters／末格…）" : "畫面欄位（motion、source、chapter 這類不進關鍵影格請求的）"),
      shot.speech && "台詞或動作秒數",
      shot.prompt && "要貼的定稿正文",
      shot.buy && `買的秒數 ${shot.buy[0]} → ${shot.buy[1]}`,
      shot.kind && `類型 ${shot.kind[0]} → ${shot.kind[1]}`,
    ].filter(Boolean).join("、");
    lines.push(`${shot.id}：${what}`);
    if (!changes.look) {
      const redo = [];
      if (shot.keyframe && drawn(shot.id)) redo.push("關鍵影格（已畫，重畫並 judge）");
      if ((shot.visual || shot.prompt || shot.buy || shot.kind) && boughtEntry(shot.id)) redo.push(boughtEntry(shot.id).imported_at ? "外部片段（已匯入，要重做）" : "素材（已買）");
      if (shot.speech) redo.push(shot.spoken ? "那幾句的 TTS" : "動作秒數變了：時間軸重排");
      if (redo.length) rebuy.push(`${shot.id}：${redo.join("、")}`);
    }
  }
  const explainedVisual = changes.look || changes.added.length || changes.removed.length || changes.reordered || changes.shots.some((shot) => shot.visual || shot.kind);
  const explainedSpeech = changes.added.length || changes.removed.length || changes.reordered || changes.shots.some((shot) => shot.speech);
  if (changes.hashes.visual && !explainedVisual) lines.push(`visualHash ${lock.hashes.visual} → ${current.hashes.visual}：縮圖、角色命名造型的外觀或卡片場景改了`);
  if (changes.hashes.speech && !explainedSpeech) {
    lines.push(`speechHash ${lock.hashes.speech} → ${current.hashes.speech}：旁白或角色的聲音、詞庫用到的條目、發音提示改了`);
    rebuy.push("受影響的台詞全部重錄 TTS（聲音或詞庫是整集共用的）");
  }
  if (changes.hashes.script && !changes.shots.some((shot) => shot.speech) && !explainedVisual && !changes.hashes.speech) lines.push("劇本（script.md 的內容：角色名字、聲音、章節）改了");
  for (const id of changes.added) lines.push(`${id}：新增的鏡頭`);
  for (const id of changes.removed) lines.push(`${id}：鎖定後刪掉的鏡頭${boughtEntry(id) ? "（素材已買，錢花了）" : ""}`);
  if (changes.reordered) lines.push("鏡頭順序變了");
  if (changes.settings.length) lines.push(`路線或設定變了：${changes.settings.map((key) => `${key} ${JSON.stringify(lock[key] ?? null)} → ${JSON.stringify(current[key] ?? null)}`).join("、")}`);

  const stale = [];
  if (changes.hashes.script) stale.push("script");
  if (changes.look) stale.push("look");
  if (anyVisual || changes.look) stale.push("storyboard");
  if (anySpeech) stale.push("audio");
  const approvals = [...new Set(stale)].filter((gate) => approved === null || approved.includes(gate));
  // 關鍵影格：look 改了全部重畫重 judge；否則只有關鍵影格指紋變了、已經畫過的那幾鏡，加上新增的鏡頭。
  const keyframeCalls = changes.look ? Object.values(keyframes?.shots ?? {}).filter((shot) => shot?.file).length : changes.shots.filter((shot) => shot.keyframe && drawn(shot.id)).length + changes.added.length;
  // 伺服器買的素材：clips manifest 綁 speech／visual／look 雜湊，任何一個變了就重建，每一支從快取拿回但再 judge 一次。
  const serverClips = Object.values(clips?.shots ?? {}).filter((shot) => shot?.file && !shot.source && !shot.still && !shot.imported_at).length;
  const clipCalls = anyVisual || anySpeech ? serverClips : 0;
  const judgeCalls = keyframeCalls + clipCalls;
  return {
    changed: lines.length > 0,
    ...changes,
    impact: {
      rebuy,
      approvals,
      approvals_if_approved: [...new Set(stale)],
      judge_calls: judgeCalls,
      judge_keyframes: keyframeCalls,
      judge_clips: clipCalls,
      judge_usd: Math.round(judgeCalls * PRICES.judge.usd_per_call * 100) / 100,
      imported_need_reimport: anyVisual || anySpeech ? Object.entries(clips?.shots ?? {}).filter(([, shot]) => shot?.imported_at).map(([id]) => id) : [],
    },
    lines,
  };
}

export function renderChangeOrder(result, lockMeta) {
  const out = [];
  if (!result.changed) {
    out.push(`和鎖定（${lockMeta.created_at}${lockMeta.note ? `，${lockMeta.note}` : ""}）一樣：照鎖定包做`);
    return out.join("\n");
  }
  out.push(`變更單：對照 ${lockMeta.created_at} 的開拍鎖定${lockMeta.note ? `（${lockMeta.note}）` : ""}`);
  const hashes = Object.entries(result.hashes).filter(([, value]) => value).map(([key]) => key);
  if (hashes.length) out.push(`動到的雜湊：${hashes.join("、")}`);
  out.push("");
  out.push("改了什麼：");
  for (const line of result.lines) out.push(`- ${line}`);
  out.push("");
  out.push("會重畫、重買或重做：");
  if (result.impact.rebuy.length) for (const line of result.impact.rebuy) out.push(`- ${line}`);
  else out.push("- 還沒畫也還沒買的鏡頭：改劇本不花錢，但要重鎖");
  if (result.impact.judge_calls) out.push(`- judge 再付 ${result.impact.judge_calls} 次（約 US$${result.impact.judge_usd.toFixed(2)}）：關鍵影格 ${result.impact.judge_keyframes} 張、伺服器素材 ${result.impact.judge_clips} 支（從快取拿回不付素材錢）`);
  if (result.impact.imported_need_reimport.length) out.push(`- 已經 clips import 的外部片段要重新匯入（clips manifest 從空的重建）：${result.impact.imported_need_reimport.join("、")}`);
  if (result.impact.approvals.length) out.push(`失效的核准：${result.impact.approvals.join("、")}（要再送審）`);
  else if (result.impact.approvals_if_approved.length) out.push(`核准：${result.impact.approvals_if_approved.join("、")} 還沒核准過，改了不用重審，但送審的是改過的版本`);
  out.push("");
  out.push("下一步：把這次要改的攢齊、讓站主看這張變更單點頭，一次改完再 --write --force 重鎖；批次進行中不要為單鏡改字。");
  return out.join("\n");
}

/** 備料清單：程式查得到的項目 { id, ok, what }，加上要人打勾的 manual。lock 可以是 null（鎖定之前跑）。 */
export async function readiness({ inputs, lock, current, docDir, workdir }) {
  const checks = [];
  const info = [];
  const add = (id, ok, what) => checks.push({ id, ok, what });
  if (lock) {
    const comparison = compareLock(lock, current);
    add("lock.current", !comparison.changed, comparison.changed ? `劇本或路線跟鎖定不同（${comparison.lines.length} 項）：先跑 --check、走變更單` : "劇本與路線跟鎖定一樣");
  } else {
    info.push("還沒有鎖定檔：站主確認開拍鎖定包之後 --write，送出第一支之前再跑一次 --ready");
  }
  const docDirOk = docDir && workdir;
  if (docDirOk) {
    for (const gate of GATES) {
      const state = await approvalState({ gate, docDir, workdir });
      const needed = gate !== "look" || (inputs.doc.characters ?? []).length > 0;
      if (needed) add(`gate.${gate}`, state.status === "approved", `${gate} 關卡：${state.status}`);
    }
  }
  const timeline = workdir ? readJson(path.join(workdir, "timeline.json"), null) : null;
  let speech = null;
  try {
    speech = speechHash(inputs.doc, inputs.lexicon);
  } catch {
    speech = null;
  }
  add("timeline.bound", Boolean(timeline) && timeline.speech_hash === speech, timeline ? (timeline.speech_hash === speech ? "配音 timeline 綁著現在的台詞（買幾秒照實測）" : "timeline.json 是舊台詞錄的：重跑 tts") : "還沒有錄好的 timeline.json：買幾秒是估的，先 tts");
  const manifest = inputs.manifest;
  const bound = Boolean(manifest) && manifest.look_hash === lookHash(inputs.doc) && manifest.visual_hash === visualHash(inputs.doc);
  add("keyframes.bound", bound, manifest ? (bound ? "keyframes manifest 綁著現在的 look 與畫面" : "keyframes manifest 過期：look 或畫面欄位在畫完之後改過") : "還沒畫關鍵影格");
  // 首格與末格只查要買素材的鏡頭；still 的圖由 storyboard 關卡管。
  for (const [id, shot] of Object.entries(current.shots)) {
    if (shot.visual_kind !== "clip") continue;
    const entry = manifest?.shots?.[id];
    const file = entry?.file ? path.join(workdir ?? "", entry.file) : null;
    const ok = Boolean(entry?.file) && !entry.needs_review && Boolean(workdir) && existsSync(file);
    if (!ok) add(`first_frame.${id}`, false, `${id} 的首格${entry?.file ? (entry.needs_review ? "被 judge 標 needs_review" : "檔案不在工作目錄") : "還沒畫"}`);
    if (shot.end_frame?.planned) {
      const end = entry?.end_frame?.file;
      if (!end || !existsSync(path.join(workdir ?? "", end))) add(`end_frame.${id}`, false, `${id} 計畫要末格，但還沒畫`);
    }
  }
  if (current.route !== "server") add("import.profile", !inputs.series?.production?.profile, inputs.series?.production?.profile ? "有 production profile：clips import 會以 3 拒收外部片段" : "沒有 production profile：clips import 收得進來");
  const plan = lock ?? current;
  const assist = plan.web_assist ? `AI 潤飾（Hailuo 的 AI Polish、Kling 的 AI Prompter）照鎖定：${plan.web_assist}` : "AI 潤飾（Hailuo 的 AI Polish、Kling 的 AI Prompter）開或關要寫進鎖定包（--assist on|off）";
  const manual = current.route === "server"
    ? ["`media-status`：供應商、模型、解析度與本月剩餘對得上鎖定包", "`drama_preflight.mjs --stage clips` 沒有 refuse／waste", "第一鏡單獨跑（主機地區）"]
    : [
        `${current.route === "hailuo" ? "hailuoai.video" : "kling.ai"} 是站主的帳號、方案對（${plan.plan ?? "—"}），餘額 ≥ 期望 ${plan.totals.clip.expected} 點＋一成預留`,
        "首格上傳的路：照當次瀏覽器工具的文件確認（2026-10-04 Claude 桌面版內建瀏覽器傳不了本機圖，當時的替代是站主同意後用 Claude in Chrome 的 file_upload，或站主手動）",
        current.route === "kling" ? `生成頁：VIDEO 3.0、${plan.resolution}、輸出數 1、原生音訊關、Multi-Shot 關、比例跟首格（16:9）` : `生成頁：${plan.hailuo_model === "2.3" ? "Hailuo 2.3" : "H3"}、${plan.resolution}、16:9（設定面板預設 21:9）、秒數照鎖定、單鏡`,
        assist,
        `負面欄：網頁真的有才貼 look.negative；沒有就不貼，也不寫進正文`,
        current.route === "hailuo" ? "下載：全部下載 → 無水印下載（結果卡的 <video> 是有浮水印的版本）" : "下載：會員的無浮水印下載",
        "收據檔（每支一筆：首格 sha256、正文 sha256 要等於鎖定檔、送出前後餘額、job id）與停損規則備好",
        "`drama_preflight.mjs --stage clips` 沒有 refuse（clips import 的前提同 clips：timeline、keyframes manifest、storyboard 核准、沒有 profile）",
      ];
  return { checks, info, ok: checks.every((check) => check.ok), manual };
}

export function renderReadiness(result) {
  const out = ["備料清單（程式查的）："];
  for (const check of result.checks) out.push(`  ${check.ok ? "ok  " : "沒過"} ${check.id}：${check.what}`);
  for (const line of result.info) out.push(`  註   ${line}`);
  out.push("人工確認：");
  for (const item of result.manual) out.push(`  [ ] ${item}`);
  out.push(result.ok ? "程式查得到的都過了；人工項目逐條打勾後開拍" : "有沒過的項目：鎖定之前放進鎖定包的「還要做的事」；送出第一支之前要全過");
  return out.join("\n");
}

const flagsGiven = (values) => Object.keys(PLAN_FLAGS).some((key) => values[key] !== undefined && key !== "timeline");

export async function main(argv, stdout = process.stdout, stderr = process.stderr, now = () => new Date().toISOString()) {
  let values;
  try {
    ({ values } = parseArgs({
      args: argv,
      options: {
        ...PLAN_FLAGS,
        slug: { type: "string" },
        file: { type: "string" },
        workdir: { type: "string" },
        root: { type: "string" },
        write: { type: "boolean" },
        check: { type: "boolean" },
        ready: { type: "boolean" },
        force: { type: "boolean" },
        note: { type: "string" },
        assist: { type: "string" },
        json: { type: "boolean" },
      },
      strict: true,
    }));
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  const modes = ["write", "check", "ready"].filter((mode) => values[mode]);
  if ((!values.slug && !values.file) || modes.length !== 1 || (values.file && !values.workdir) || (values.assist !== undefined && !["on", "off"].includes(values.assist))) {
    stderr.write(`usage: plan_lock.mjs --slug <SLUG> | --file <video.json> --workdir <dir>  --write [--note ...] [--assist on|off] [--force] | --check | --ready  ${PLAN_USAGE} [--json]\n`);
    return 2;
  }
  let inputs;
  try {
    inputs = loadInputs({ file: values.file, slug: values.slug, workdir: values.workdir, root: values.root, timeline: values.timeline });
  } catch (error) {
    stderr.write(`${values.slug ?? values.file}: ${error.message}\n`);
    return 2;
  }
  const lockPath = path.join(inputs.workdir, LOCK_FILE);
  const existing = readJson(lockPath, null);
  if (existing) {
    const problem = lockProblem(existing);
    if (problem && !(values.write && values.force)) {
      stderr.write(`${lockPath}: ${problem}\n`);
      return 2;
    }
  }
  const usable = existing && !lockProblem(existing) ? existing : null;
  let options;
  try {
    options = flagsGiven(values) || !usable ? planOptions(values) : settingsOf(usable);
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  let plan;
  try {
    plan = planEpisode(inputs.doc, { ...options, timeline: inputs.timeline, manifest: inputs.manifest, series: inputs.series, timelineStale: inputs.timeline_stale });
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  const assist = values.assist ?? usable?.web_assist ?? null;
  const current = lockOf(inputs.doc, inputs.lexicon, plan, { ...options, assist });
  const approvedGates = async () => {
    const out = [];
    for (const gate of GATES) if ((await approvalState({ gate, docDir: inputs.dir, workdir: inputs.workdir })).status === "approved") out.push(gate);
    return out;
  };

  if (values.write) {
    if (existing && !values.force) {
      stderr.write(`${lockPath} already holds the lock of ${existing.created_at}; check it first (--check) and pass --force to lock again (the old one is kept beside it)\n`);
      return 2;
    }
    const refused = plan.problems.filter((problem) => problem.level === "refuse");
    if (refused.length) {
      stderr.write(`這份計畫有做不進產線的問題，不鎖：\n${refused.map((problem) => `- ${problem.shot ? `${problem.shot}：` : ""}${problem.what}`).join("\n")}\n`);
      return 1;
    }
    mkdirSync(path.dirname(lockPath), { recursive: true });
    const createdAt = now();
    if (existing) {
      if (usable) {
        // 這次重鎖結掉的變更單，一筆一行：改了什麼、重買什麼、誰點頭。
        const settled = compareLock(usable, current, { keyframes: inputs.manifest, clips: readJson(path.join(inputs.workdir, "clips", "manifest.json"), null), approved: await approvedGates() });
        appendFileSync(path.join(path.dirname(lockPath), CHANGE_LOG), `${JSON.stringify({ at: createdAt, previous_lock: usable.created_at, note: values.note ?? null, changes: settled.lines, rebuy: settled.impact.rebuy, approvals: settled.impact.approvals, judge_calls: settled.impact.judge_calls })}\n`);
      }
      renameSync(lockPath, path.join(path.dirname(lockPath), `lock-${String(existing.created_at ?? createdAt).replace(/[:.]/g, "-")}.json`));
    }
    const lock = { ...current, created_at: createdAt, note: values.note ?? null };
    atomicWrite(lockPath, `${JSON.stringify(lock, null, 2)}\n`);
    const warned = plan.problems.filter((problem) => problem.level !== "refuse");
    if (warned.length) stderr.write(`鎖了，但計畫還有 ${warned.length} 個問題（shot_plan.mjs 的「問題與註記」）：\n${warned.map((problem) => `- ${problem.shot ? `${problem.shot}：` : ""}${problem.what}`).join("\n")}\n`);
    stdout.write(values.json ? `${JSON.stringify({ lock: lockPath, ...lock }, null, 2)}\n` : `鎖定 ${Object.keys(lock.shots).length} 鏡（${lock.route}${lock.plan ? ` ${lock.plan}` : ""}${lock.hailuo_model ? ` ${lock.hailuo_model}` : ""} ${lock.resolution ?? ""}，片段期望 ${lock.totals.clip.expected}、上限 ${lock.totals.clip.cap}；小樣 ${lock.pilot.join(", ") || "—"}）寫進 ${lockPath}\n`);
    return 0;
  }
  if (values.check) {
    if (!usable) {
      stderr.write(`no lock at ${lockPath}: write one with --write after the owner confirms the lock package\n`);
      return 2;
    }
    const result = compareLock(usable, current, { keyframes: inputs.manifest, clips: readJson(path.join(inputs.workdir, "clips", "manifest.json"), null), approved: await approvedGates() });
    stdout.write(values.json ? `${JSON.stringify(result, null, 2)}\n` : `${renderChangeOrder(result, usable)}\n`);
    return result.changed ? 1 : 0;
  }
  const result = await readiness({ inputs, lock: usable, current, docDir: inputs.dir, workdir: inputs.workdir });
  stdout.write(values.json ? `${JSON.stringify(result, null, 2)}\n` : `${renderReadiness(result)}\n`);
  return result.ok ? 0 : 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
