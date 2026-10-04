#!/usr/bin/env node
// 開拍鎖定與變更單：站主一次確認開拍鎖定包之後，把當下的劇本、每鏡的畫面與台詞、路線、買幾秒、定稿正文和預算
// 寫成 <workdir>/plan/lock.json；之後任何改動先用 --check 對照鎖定，印出變更單（哪幾鏡改了、會重買什麼、哪個
// 核准失效、大約多少錢），讓站主決定再改；--ready 在送出第一支之前，查備料清單裡程式查得到的部分。
//
//   node .agents/skills/animation-preproduction/scripts/plan_lock.mjs --slug <SLUG> | --file <video.json> --workdir <dir>
//     --write [--note "<站主怎麼說>"] [--force] | --check | --ready
//     [--route server|hailuo|kling] [--plan hailuo:pro|kling:pro|...] [--model <id>] [--resolution <r>]
//     [--root <repo>] [--json]
//
// --slug 時 --workdir 是放所有影片的目錄（VIDEO_WORKDIR 規則，同 tools/video）；給 --file 時 --workdir 是這支影片
// 自己的工作目錄。--write 時路線旗標決定鎖什麼；--check、--ready 沿用鎖定檔裡的路線。
// 離線、不花錢、不碰伺服器。結束碼：0；--check 有變更或 --ready 有沒過的項目是 1；讀不到、沒有鎖定檔、參數錯是 2。
import { createHash } from "node:crypto";
import { appendFileSync, existsSync, mkdirSync, renameSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { approvalState } from "../../../../tools/video/core/approvals.mjs";
import { lookHash } from "../../../../tools/video/core/drama.mjs";
import { atomicWrite, readJson } from "../../../../tools/video/core/paths.mjs";
import { speechHash, visualHash } from "../../../../tools/video/core/timeline.mjs";
import { PRICES } from "../../animation-production/scripts/episode_estimate.mjs";
import { loadInputs, planEpisode } from "./shot_plan.mjs";

export const LOCK_FILE = path.join("plan", "lock.json");
export const LOCK_VERSION = 1;
export const CHANGE_LOG = "changes.jsonl";
const sha = (value) => createHash("sha256").update(typeof value === "string" ? value : JSON.stringify(value)).digest("hex").slice(0, 16);

/**
 * 一鏡的兩個指紋，欄位跟 tools/video/core/timeline.mjs 的 visualHash／speechHash 每鏡的那一段相同：
 * 畫面 ＝ id、template、chapter、data、句子 id 與 reveal；台詞 ＝ 每句的文字、停頓、speaker、emotion 與 action_seconds。
 */
export function shotPrints(scene) {
  const lines = Array.isArray(scene.lines) ? scene.lines : [];
  return {
    visual: sha([scene.id, scene.template, scene.chapter ?? null, scene.data ?? null, lines.map((line) => [line.id, line.reveal ?? 0])]),
    speech: sha([lines.map((line) => [line.id, line.text, line.pause_after_ms ?? null, line.speaker ?? "narrator", line.emotion ?? null]), scene.action_seconds ?? null]),
  };
}

/** 鎖定檔的內容（不含 created_at 與 note）。 */
export function lockOf(doc, lexicon, plan) {
  const shots = {};
  const sceneById = new Map(doc.scenes.map((scene) => [scene.id, scene]));
  for (const shot of plan.shots) {
    shots[shot.id] = {
      ...shotPrints(sceneById.get(shot.id)),
      chapter: shot.chapter,
      setup: shot.setup,
      visual_kind: shot.visual,
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
  return {
    version: LOCK_VERSION,
    route: plan.route,
    plan: plan.plan?.id ?? null,
    model: plan.model,
    resolution: plan.resolution,
    handle_s: plan.handle_s,
    hashes: { look: lookHash(doc), visual: visualHash(doc), speech, document: sha(doc) },
    order: doc.scenes.filter((scene) => scene.template === "shot").map((scene) => scene.id),
    shots,
    totals: plan.totals,
    batches: plan.batches.map(({ name, shots: members, buys }) => ({ name, shots: members, buys })),
    counts: plan.counts,
  };
}

/**
 * 現在的劇本對鎖定檔：{ changed, look, route, added, removed, reordered, shots: [{ id, visual, speech, prompt, buy }],
 * impact: { rebuy, approvals, judge_calls, cost_note }, lines }。clips 與 keyframes 的 manifest 決定「已買」與「已畫」。
 */
export function compareLock(lock, current, { keyframes = null, clips = null } = {}) {
  const changes = { look: lock.hashes.look !== current.hashes.look, route: ["route", "plan", "model", "resolution"].filter((key) => (lock[key] ?? null) !== (current[key] ?? null)), added: [], removed: [], reordered: false, shots: [] };
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
      speech: before.speech !== after.speech,
      prompt: (before.prompt?.sha256 ?? null) !== (after.prompt?.sha256 ?? null),
      buy: before.buy_s !== after.buy_s ? [before.buy_s, after.buy_s] : null,
      kind: before.visual_kind !== after.visual_kind ? [before.visual_kind, after.visual_kind] : null,
    };
    if (entry.visual || entry.speech || entry.prompt || entry.buy || entry.kind) changes.shots.push(entry);
  }
  const drawn = (id) => Boolean(keyframes?.shots?.[id]?.file);
  const bought = (id) => Boolean(clips?.shots?.[id]?.file) && !clips.shots[id].source && !clips.shots[id].still;
  const anyVisual = changes.look || changes.added.length > 0 || changes.removed.length > 0 || changes.reordered || changes.shots.some((shot) => shot.visual || shot.kind);
  const anySpeech = changes.shots.some((shot) => shot.speech) || changes.added.length > 0 || changes.removed.length > 0;
  const rebuy = [];
  const lines = [];
  if (changes.look) {
    rebuy.push("全部：設定圖、每一張關鍵影格、每一支素材（look 在 lookHash 裡，快取鍵也含 negative 與參考圖）");
    lines.push("look（或角色 appearance、sheet_prompt）改了");
  }
  for (const shot of changes.shots) {
    const what = [shot.visual && "畫面欄位（prompt／camera／motion／characters／source／chapter…）", shot.speech && "台詞或動作秒數", shot.prompt && "要貼的定稿正文", shot.buy && `買的秒數 ${shot.buy[0]} → ${shot.buy[1]}`, shot.kind && `類型 ${shot.kind[0]} → ${shot.kind[1]}`].filter(Boolean).join("、");
    lines.push(`${shot.id}：${what}`);
    if (!changes.look) {
      const redo = [];
      if (shot.visual && drawn(shot.id)) redo.push("關鍵影格（已畫）");
      if ((shot.visual || shot.prompt || shot.buy || shot.kind) && bought(shot.id)) redo.push("素材（已買）");
      if (shot.speech) redo.push("那幾句的 TTS");
      if (redo.length) rebuy.push(`${shot.id}：${redo.join("、")}`);
    }
  }
  for (const id of changes.added) lines.push(`${id}：新增的鏡頭`);
  for (const id of changes.removed) lines.push(`${id}：鎖定後刪掉的鏡頭${bought(id) ? "（素材已買，錢花了）" : ""}`);
  if (changes.reordered) lines.push("鏡頭順序變了");
  if (changes.route.length) lines.push(`路線設定變了：${changes.route.map((key) => `${key} ${lock[key] ?? "—"} → ${current[key] ?? "—"}`).join("、")}`);
  const approvals = [];
  if (changes.look) approvals.push("look", "storyboard");
  else if (anyVisual) approvals.push("storyboard");
  if (anySpeech) approvals.push("audio");
  const drawnCount = Object.values(keyframes?.shots ?? {}).filter((shot) => shot?.file).length;
  const boughtCount = Object.values(clips?.shots ?? {}).filter((shot) => shot?.file && !shot.source && !shot.still).length;
  // 任一鏡的畫面欄位變了，visualHash 就變：keyframes 與 clips 的 manifest 都重建，沒改的從快取拿回，但每一鏡再 judge 一次。
  const judgeCalls = anyVisual || anySpeech ? (anyVisual ? drawnCount : 0) + boughtCount : 0;
  return {
    changed: lines.length > 0,
    ...changes,
    impact: {
      rebuy,
      approvals: [...new Set(approvals)],
      judge_calls: judgeCalls,
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
  out.push("");
  out.push("改了什麼：");
  for (const line of result.lines) out.push(`- ${line}`);
  out.push("");
  out.push("會重買：");
  if (result.impact.rebuy.length) for (const line of result.impact.rebuy) out.push(`- ${line}`);
  else out.push("- 還沒畫也還沒買的鏡頭：改劇本不花錢，但要重鎖");
  if (result.impact.judge_calls) out.push(`- judge：manifest 綁的 hash 變了，已畫已買的 ${result.impact.judge_calls} 張／支都要再 judge 一次（約 US$${result.impact.judge_usd.toFixed(2)}；沒改的鏡頭從快取拿回不付圖錢）`);
  if (result.impact.imported_need_reimport.length) out.push(`- 已經 clips import 的外部片段要重新匯入（clips manifest 從空的重建）：${result.impact.imported_need_reimport.join("、")}`);
  if (result.impact.approvals.length) out.push(`失效的核准：${result.impact.approvals.join("、")}（要再送審）`);
  out.push("");
  out.push("下一步：把這次要改的攢齊、讓站主看這張變更單點頭，一次改完再 --write 重鎖；批次進行中不要為單鏡改字。");
  return out.join("\n");
}

/** 備料清單：程式查得到的項目 { id, ok, what }；查不到的交給人（manual）。 */
export async function readiness({ inputs, lock, current, docDir, workdir }) {
  const checks = [];
  const add = (id, ok, what) => checks.push({ id, ok, what });
  const comparison = compareLock(lock, current);
  add("lock.current", !comparison.changed, comparison.changed ? `劇本或路線跟鎖定不同（${comparison.lines.length} 項）：先跑 --check、走變更單` : "劇本與路線跟鎖定一樣");
  if (docDir && workdir) {
    for (const gate of ["script", "look", "audio", "storyboard"]) {
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
  for (const [id, shot] of Object.entries(current.shots)) {
    if (shot.visual_kind === "cut") continue;
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
  const manual = current.route === "server"
    ? ["`media-status`：供應商、模型、解析度與本月剩餘對得上鎖定包", "`drama_preflight.mjs --stage clips` 沒有 refuse／waste", "第一鏡單獨跑（主機地區）"]
    : [
        `${current.route === "hailuo" ? "hailuoai.video" : "kling.ai"} 是站主的帳號、方案對（${lock.plan ?? "—"}），餘額 ≥ 期望 ${lock.totals.clip.expected} 點＋預留`,
        "首格上傳的路：內建瀏覽器傳不了本機圖，用 Claude in Chrome 的 file_upload（站主同意、已登入）或站主手動",
        current.route === "kling" ? "生成頁：VIDEO 3.0、1080p、輸出數 1、原生音訊關、多鏡／智能分鏡關、16:9" : "生成頁：H3、解析度照鎖定、16:9（預設是 21:9）、秒數照鎖定、單鏡",
        current.route === "hailuo" ? "下載：全部下載 → 無水印下載（結果卡的 <video> 是有浮水印的版本）" : "下載：付費方案的無浮水印檔",
        "收據檔（每支一筆：首格 sha256、正文 sha256、送出前後餘額、job id）與 STOP 規則備好",
        "`drama_preflight.mjs --stage clips` 沒有 refuse（clips import 的前提同 clips：timeline、keyframes manifest、storyboard 核准、沒有 profile）",
      ];
  return { checks, ok: checks.every((check) => check.ok), manual };
}

export function renderReadiness(result) {
  const out = ["備料清單（程式查的）："];
  for (const check of result.checks) out.push(`  ${check.ok ? "ok  " : "沒過"} ${check.id}：${check.what}`);
  out.push("人工確認：");
  for (const item of result.manual) out.push(`  [ ] ${item}`);
  out.push(result.ok ? "程式查得到的都過了；人工項目逐條打勾後開拍" : "有沒過的項目：先補齊再送出第一支");
  return out.join("\n");
}

export async function main(argv, stdout = process.stdout, stderr = process.stderr, now = () => new Date().toISOString()) {
  let values;
  try {
    ({ values } = parseArgs({
      args: argv,
      options: {
        slug: { type: "string" },
        file: { type: "string" },
        workdir: { type: "string" },
        root: { type: "string" },
        write: { type: "boolean" },
        check: { type: "boolean" },
        ready: { type: "boolean" },
        force: { type: "boolean" },
        note: { type: "string" },
        route: { type: "string" },
        plan: { type: "string" },
        model: { type: "string" },
        resolution: { type: "string" },
        json: { type: "boolean" },
      },
      strict: true,
    }));
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  const modes = ["write", "check", "ready"].filter((mode) => values[mode]);
  if ((!values.slug && !values.file) || modes.length !== 1 || (values.file && !values.workdir)) {
    stderr.write("usage: plan_lock.mjs --slug <SLUG> | --file <video.json> --workdir <dir>  --write [--note ...] [--force] | --check | --ready  [--route server|hailuo|kling] [--plan ...] [--model ...] [--resolution ...] [--json]\n");
    return 2;
  }
  let inputs;
  try {
    inputs = loadInputs({ file: values.file, slug: values.slug, workdir: values.workdir, root: values.root });
  } catch (error) {
    stderr.write(`${values.slug ?? values.file}: ${error.message}\n`);
    return 2;
  }
  const lockPath = path.join(inputs.workdir, LOCK_FILE);
  const existing = readJson(lockPath, null);
  const routeOptions = values.write || !existing ? { route: values.route, plan: values.plan, model: values.model, resolution: values.resolution } : { route: existing.route, plan: existing.plan ?? undefined, model: existing.route === "server" ? existing.model ?? undefined : undefined, resolution: existing.resolution ?? undefined };
  let plan;
  try {
    plan = planEpisode(inputs.doc, { ...routeOptions, timeline: inputs.timeline, manifest: inputs.manifest, series: inputs.series, handle: existing && !values.write ? existing.handle_s : undefined });
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  const current = lockOf(inputs.doc, inputs.lexicon, plan);

  if (values.write) {
    if (existing && !values.force) {
      stderr.write(`${lockPath} already holds the lock of ${existing.created_at}; check it first (--check) and pass --force to lock again (the old one is kept beside it)\n`);
      return 2;
    }
    mkdirSync(path.dirname(lockPath), { recursive: true });
    const createdAt = now();
    if (existing) {
      // The change order this re-lock settles, one JSON line each: what changed, what it re-bought, who said yes.
      const settled = compareLock(existing, current, { keyframes: inputs.manifest, clips: readJson(path.join(inputs.workdir, "clips", "manifest.json"), null) });
      appendFileSync(path.join(path.dirname(lockPath), CHANGE_LOG), `${JSON.stringify({ at: createdAt, previous_lock: existing.created_at, note: values.note ?? null, changes: settled.lines, rebuy: settled.impact.rebuy, approvals: settled.impact.approvals, judge_calls: settled.impact.judge_calls })}\n`);
      renameSync(lockPath, path.join(path.dirname(lockPath), `lock-${String(existing.created_at).replace(/[:.]/g, "-")}.json`));
    }
    const lock = { ...current, created_at: createdAt, note: values.note ?? null };
    atomicWrite(lockPath, `${JSON.stringify(lock, null, 2)}\n`);
    stdout.write(values.json ? `${JSON.stringify({ lock: lockPath, ...lock }, null, 2)}\n` : `鎖定 ${Object.keys(lock.shots).length} 鏡（${lock.route}${lock.plan ? ` ${lock.plan}` : ""}，片段期望 ${lock.totals.clip.expected}、上限 ${lock.totals.clip.cap}）寫進 ${lockPath}\n`);
    return 0;
  }
  if (!existing) {
    stderr.write(`no lock at ${lockPath}: write one with --write after the owner confirms the lock package\n`);
    return 2;
  }
  if (values.check) {
    const result = compareLock(existing, current, { keyframes: inputs.manifest, clips: readJson(path.join(inputs.workdir, "clips", "manifest.json"), null) });
    stdout.write(values.json ? `${JSON.stringify(result, null, 2)}\n` : `${renderChangeOrder(result, existing)}\n`);
    return result.changed ? 1 : 0;
  }
  const result = await readiness({ inputs, lock: existing, current, docDir: inputs.dir, workdir: inputs.workdir });
  stdout.write(values.json ? `${JSON.stringify(result, null, 2)}\n` : `${renderReadiness(result)}\n`);
  return result.ok ? 0 : 1;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
