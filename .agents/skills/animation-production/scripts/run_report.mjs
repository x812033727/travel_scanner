#!/usr/bin/env node
// 一集跑完（或跑到一半）的帳：錢花在哪一類、哪一階段，每鏡幾個 take、幾個過，買的秒數用掉幾成
// （needed_s ÷ 買的秒數：工具自己還沒記這個數），剪接省下多少，哪些片段不是這條線買的，judge 叫了幾次，
// 五種「完成」各算幾個（任務 ready、QC 過、judge 過、needs_review、站主核准），哪個關卡的核准過期了，
// 每階段跑了多久。--markdown 印成 .agents/skills/animation-production/references/post-mortem.md 的表，
// 數字填好、每個退回的 take 一列；填不出來的欄印 not_available，人要補的段留空。
//
//   node .agents/skills/animation-production/scripts/run_report.mjs --slug <SLUG> [--workdir <work base>]
//     [--root <repository root>] [--markdown] [--json]
//
// 讀 media/ledger.json（readLedger / totalsOf / savedTotals / importedTotals）、characters、keyframes 與 clips 的 manifest、
// timeline.json、state.json、approvals.json；不碰伺服器（本月剩餘額度要看 media-status）。有 plan/lock.json（animation-
// preproduction 的開拍鎖定）時再列每鏡的承諾（類型、買幾秒、路線、fit）對交付（clips manifest）與花的（ledger），以及
// 省下／多花的差；答應的 clip 變成 still／切／fit freeze 而 changes.jsonl 沒有站主點頭的變更單就標「沒簽」。
// 結束碼：0；讀不到專案或參數錯 2。
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { approvalState } from "../../../../tools/video/core/approvals.mjs";
import { drawnShotScenes, isDrama } from "../../../../tools/video/core/drama.mjs";
import { readJson, resolveWorkdir, UsageError } from "../../../../tools/video/core/paths.mjs";
import { ARTIFACTS, loadProject } from "../../../../tools/video/core/state.mjs";
import { FPS } from "../../../../tools/video/core/timeline.mjs";
import { importedTotals, readLedger, savedTotals, totalsOf } from "../../../../tools/video/media/ledger.mjs";
import { coveringOrder, LOCK_FILE, lockProblem, promiseBreak, readChangeOrders } from "../../animation-preproduction/scripts/plan_lock.mjs";
import { visualKindOf } from "../../animation-preproduction/scripts/shot_plan.mjs";

export const KINDS = ["image", "clip", "music", "judge"];
export const STATUS_COLUMNS = ["job_ready", "qc_ok", "judge_passed", "needs_review", "owner_accepted"];
export const STATUS_LABELS = { job_ready: "job ready", qc_ok: "QC ok（ffmpeg）", judge_passed: "judge passed", needs_review: "needs_review", owner_accepted: "站主 accepted（關卡）" };
export const NOT_AVAILABLE = "not_available";
const round4 = (value) => Math.round(value * 10_000) / 10_000;
const ratio = (needed, bought) => (bought > 0 ? round4(needed / bought) : null);
const usd = (value) => `US$${Number(value ?? 0).toFixed(2)}`;
const percent = (value) => (value === null || value === undefined ? NOT_AVAILABLE : `${Math.round(value * 100)}%`);
const cell = (value) => (value === null || value === undefined ? "—" : String(value));

/**
 * { slug, workdir, totals, saved, imported, spend, bought, takes, retakes, utilisation, cuts, external, judge,
 *   status, gates, stale, wallclock, needs_review, promises }。promises 沒有鎖定檔是 null，否則
 * { lock, route, unit, shots: [{ id, promised, now, delivered, spent, kept, change, signed, delta, delta_s }], totals, orders, note }。
 */
export async function runReport({ slug, root, workdir: workdirFlag, env = process.env, home }) {
  const project = loadProject({ slug, root });
  const { doc } = project;
  if (!isDrama(doc)) throw new UsageError(`${slug} is not a drama (format "${doc.format}")`);
  const workdir = resolveWorkdir({ flag: workdirFlag, env, slug: doc.slug, root, home });
  const read = (name) => readJson(path.join(workdir, name), null);
  const ledger = readLedger(workdir);
  const entries = ledger.entries ?? [];
  const totals = totalsOf(entries);
  const saved = savedTotals(entries);
  // What `clips import` booked: clips made on a plan elsewhere, kept apart from what this line bought.
  const imported = importedTotals(entries);
  const characters = read(ARTIFACTS.characters);
  const keyframes = read(ARTIFACTS.keyframes);
  const clips = read(ARTIFACTS.clips);
  const timeline = read(ARTIFACTS.timeline);
  const state = read(ARTIFACTS.state) ?? { runs: [] };
  const framesOf = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, scene.end_frame - scene.start_frame]));
  const gates = {};
  for (const gate of ["script", "look", "storyboard", "audio", "final"]) gates[gate] = (await approvalState({ gate, docDir: project.dir, workdir })).status;

  // The money: by kind and by stage, from the ledger alone (a cut is a saving, never a spend; an imported clip is counted on its own).
  const spend = { by_kind: {}, by_stage: {}, failed: { count: 0, usd: 0 } };
  for (const kind of KINDS) spend.by_kind[kind] = { count: 0, usd: 0, seconds: 0 };
  for (const entry of entries) {
    if (entry.status === "cut" || entry.status === "imported") continue;
    const kind = spend.by_kind[entry.kind] ?? (spend.by_kind[entry.kind] = { count: 0, usd: 0, seconds: 0 });
    kind.count += 1;
    kind.usd = round4(kind.usd + Number(entry.cost_usd || 0));
    if (entry.kind === "clip") kind.seconds += Number(entry.seconds || 0);
    const stage = spend.by_stage[entry.stage ?? "?"] ?? (spend.by_stage[entry.stage ?? "?"] = { count: 0, usd: 0, judge_calls: 0, images: 0, clips: 0, clip_seconds: 0 });
    stage.count += 1;
    stage.usd = round4(stage.usd + Number(entry.cost_usd || 0));
    if (entry.kind === "judge") stage.judge_calls += 1;
    if (entry.kind === "image") stage.images += 1;
    if (entry.kind === "clip") {
      stage.clips += 1;
      stage.clip_seconds += Number(entry.seconds || 0);
    }
    if (entry.status === "failed") {
      spend.failed.count += 1;
      spend.failed.usd = round4(spend.failed.usd + Number(entry.cost_usd || 0));
    }
  }
  const lookImages = entries.filter((entry) => entry.kind === "image" && entry.stage === "look" && entry.status !== "cut");
  const keyframeImages = entries.filter((entry) => entry.kind === "image" && entry.stage === "keyframes" && entry.status !== "cut");
  const clipJobs = entries.filter((entry) => entry.kind === "clip" && entry.status !== "cut" && entry.status !== "imported");
  const musicJobs = entries.filter((entry) => entry.kind === "music");
  const judgeJobs = entries.filter((entry) => entry.kind === "judge");
  const usdOf = (list) => round4(list.reduce((total, entry) => total + Number(entry.cost_usd || 0), 0));
  const bought = {
    sheets: { count: lookImages.length, usd: usdOf(lookImages) },
    keyframes: { count: keyframeImages.length, end_frames: keyframeImages.filter((entry) => /\/end$/.test(String(entry.id))).length, usd: usdOf(keyframeImages) },
    clips: { count: clipJobs.length, seconds: clipJobs.reduce((total, entry) => total + Number(entry.seconds || 0), 0), usd: usdOf(clipJobs) },
    music: { count: musicJobs.length, usd: usdOf(musicJobs) },
    judge: { count: judgeJobs.length, usd: usdOf(judgeJobs) },
  };

  // Takes per shot, from the manifests: a keyframe take passes on the judge, a clip take on ffmpeg's QC (which folds the judge in).
  const takes = [];
  const retakes = [];
  const keyframeShots = Object.entries(keyframes?.shots ?? {});
  for (const [id, shot] of keyframeShots) {
    const list = Array.isArray(shot.takes) ? shot.takes : shot.file ? [{ seed: shot.seed, judge: shot.judge }] : [];
    takes.push({ stage: "keyframes", id, takes: list.length, passed: list.filter((take) => take.judge?.passed).length, judge: shot.judge?.overall ?? null, needs_review: Boolean(shot.needs_review), problems: shot.problems ?? [] });
    list.forEach((take, index) => { if (!take.judge?.passed) retakes.push({ stage: "keyframes", id, take: take.seed ?? index + 1, judge: take.judge?.overall ?? null, problems: take.judge?.problems ?? [] }); });
  }
  const clipEntries = Object.entries(clips?.shots ?? {});
  const generated = clipEntries.filter(([, shot]) => shot.file && !shot.still && !shot.source);
  for (const [id, shot] of generated) {
    const list = Array.isArray(shot.takes) ? shot.takes : shot.file ? [{ seed: shot.seed, qc: shot.qc, judge: shot.judge }] : [];
    takes.push({ stage: "clips", id, takes: list.length, passed: list.filter((take) => take.qc?.ok).length, judge: shot.judge?.overall ?? null, needs_review: Boolean(shot.needs_review), problems: shot.problems ?? [] });
    list.forEach((take, index) => { if (!take.qc?.ok) retakes.push({ stage: "clips", id, take: take.seed ?? index + 1, judge: take.judge?.overall ?? null, problems: take.qc?.problems ?? take.judge?.problems ?? [] }); });
  }
  for (const take of takes.filter((each) => each.needs_review && each.takes === 0)) retakes.push({ stage: take.stage, id: take.id, take: "-", judge: null, problems: take.problems });

  // Clips this line did not buy: brought in by `clips import` (imported_at, with its route, plan and credits),
  // or put there by hand before that command existed (provider "external", or no job in the ledger).
  const ledgerClipIds = new Set(clipJobs.map((entry) => entry.id));
  const external = generated.filter(([id, shot]) => shot.imported_at || shot.provider === "external" || !ledgerClipIds.has(id)).map(([id, shot]) => ({ id, file: shot.file, seconds: shot.seconds ?? null, provider: shot.provider ?? null, route: shot.external?.route ?? (shot.imported_at ? shot.provider : null), plan: shot.plan ?? shot.external?.plan ?? null, credits: shot.credits ?? shot.external?.credits ?? null, imported: Boolean(shot.imported_at) }));
  const perShot = generated.map(([id, shot]) => {
    const needed = Number.isFinite(shot.needed_s) ? shot.needed_s : framesOf.has(id) ? framesOf.get(id) / FPS : null;
    const seconds = Number(shot.seconds || 0);
    return { id, needed_s: needed === null ? null : round4(needed), bought_s: seconds, utilisation: needed === null ? null : ratio(needed, seconds), external: external.some((each) => each.id === id) };
  });
  const measured = perShot.filter((shot) => shot.needed_s !== null && shot.bought_s > 0);
  const booked = measured.filter((shot) => !shot.external);
  const neededTotal = measured.reduce((total, shot) => total + shot.needed_s, 0);
  const adoptedTotal = measured.reduce((total, shot) => total + shot.bought_s, 0);
  const neededBooked = booked.reduce((total, shot) => total + shot.needed_s, 0);
  const utilisation = {
    shots: perShot,
    needed_s: round4(neededTotal),
    adopted_s: adoptedTotal,
    needed_booked_s: round4(neededBooked),
    adopted_booked_s: booked.reduce((total, shot) => total + shot.bought_s, 0),
    ledger_s: bought.clips.seconds,
    overall_adopted: ratio(neededTotal, adoptedTotal),
    // Against everything the ledger bought, retakes included; an external clip is outside the ledger, so it is outside this ratio too.
    overall_bought: ratio(neededBooked, bought.clips.seconds),
    note: "needed_s ÷ 買的秒數；adopted 只算採用的 take（外部片段也算），bought 算 ledger 裡買到的全部秒數（重拍也算，外部片段不在裡面）；工具自己還沒記這個數，這裡是從 manifest 和 ledger 算回來的",
  };
  // What was bought and then not used: the ledger's images and clip seconds against the manifests' adopted entries.
  const readyImageIds = new Set(entries.filter((entry) => entry.kind === "image" && entry.status === "ready").map((entry) => String(entry.id).replace(/\/end$/, "")));
  const adoptedImages = [...Object.entries(characters?.characters ?? {}).filter(([id, entry]) => readyImageIds.has(id) && !entry.needs_review), ...Object.entries(keyframes?.shots ?? {}).filter(([id, shot]) => readyImageIds.has(id) && shot.file && !shot.needs_review)].length;
  const waste = { images_bought: totals.images, images_used: adoptedImages, clip_seconds_bought: bought.clips.seconds, clip_seconds_used: utilisation.adopted_booked_s };
  const cuts = { ...saved, shots: entries.filter((entry) => entry.status === "cut").map((entry) => ({ id: entry.id, source: entry.source ?? null, saved_seconds: entry.saved_seconds ?? 0, saved_usd: entry.saved_usd ?? 0 })) };
  const judge = { calls: totals.judge_calls, usd: bought.judge.usd, by_stage: Object.fromEntries(Object.entries(spend.by_stage).filter(([, each]) => each.judge_calls > 0).map(([stage, each]) => [stage, each.judge_calls])) };

  // 承諾 vs 交付（plan/lock.json，animation-preproduction 的開拍鎖定）：每鏡答應的類型、秒數、路線與一次的價，對 clips manifest
  // 交了什麼、ledger 花了什麼；答應的 clip 變成 still／切／fit freeze 而 changes.jsonl 沒有站主點頭的變更單就標「沒簽」。
  const lock = read(LOCK_FILE);
  let promises = null;
  if (lock && !lockProblem(lock)) {
    const orders = readChangeOrders(workdir);
    const unit = lock.totals?.clip?.unit ?? (lock.route === "server" ? "usd" : "credits");
    const sceneById = new Map(doc.scenes.map((scene) => [scene.id, scene]));
    const shots = (lock.order ?? Object.keys(lock.shots ?? {})).filter((id) => lock.shots?.[id]).map((id) => {
      const locked = lock.shots[id];
      const promised = { kind: locked.promise?.visual_kind ?? locked.visual_kind, buy_s: locked.promise?.buy_s ?? locked.buy_s ?? 0, route: locked.promise?.route ?? lock.route, fit: locked.promise?.fit ?? "auto", cost_one: locked.cost?.one ?? 0 };
      const scene = sceneById.get(id);
      const now = scene ? { kind: visualKindOf(scene), fit: scene.data?.fit ?? "auto" } : { kind: "removed", fit: "auto" };
      const entry = clips?.shots?.[id];
      const deliveredKind = entry?.file ? (entry.source ? "cut" : entry.still ? "still" : "clip") : null;
      const delivered = deliveredKind ? { kind: deliveredKind, seconds: Number(entry.seconds || 0), external: deliveredKind === "clip" && Boolean(entry.imported_at || entry.provider === "external" || !ledgerClipIds.has(id)) } : null;
      const booked = entries.filter((each) => each.kind === "clip" && each.id === id && each.status !== "cut");
      const spent = { jobs: booked.length, seconds: booked.reduce((total, each) => total + Number(each.seconds || 0), 0), usd: round4(booked.reduce((total, each) => total + Number(each.cost_usd || 0), 0)), credits: booked.reduce((total, each) => total + Number(each.credits || 0), 0) };
      const amount = unit === "usd" ? spent.usd : spent.credits;
      const outcome = delivered?.kind ?? now.kind;
      const downgrade = promiseBreak({ visual_kind: promised.kind, fit: promised.fit }, { kind: outcome, fit: now.fit });
      const order = downgrade ? coveringOrder(orders, lock, id, downgrade) : null;
      return {
        id,
        promised,
        now,
        delivered,
        spent: { ...spent, unit, amount },
        kept: outcome === promised.kind && !downgrade,
        change: downgrade ? "downgrade" : outcome === promised.kind ? null : "upgrade",
        signed: downgrade ? Boolean(order) : null,
        delta: round4(amount - promised.cost_one),
        delta_s: (delivered?.seconds ?? 0) - promised.buy_s,
      };
    });
    const sumOf = (pick) => round4(shots.reduce((total, shot) => total + (pick(shot) ?? 0), 0));
    const totals = {
      shots: shots.length,
      kept: shots.filter((shot) => shot.kept).length,
      downgraded: shots.filter((shot) => shot.change === "downgrade").length,
      unsigned: shots.filter((shot) => shot.change === "downgrade" && !shot.signed).length,
      upgraded: shots.filter((shot) => shot.change === "upgrade").length,
      pending: shots.filter((shot) => !shot.delivered).length,
      promised_s: sumOf((shot) => shot.promised.buy_s),
      delivered_s: sumOf((shot) => shot.delivered?.seconds),
      promised_one: sumOf((shot) => shot.promised.cost_one),
      expected: lock.totals?.clip?.expected ?? null,
      spent: sumOf((shot) => shot.spent.amount),
    };
    totals.delta = round4(totals.spent - totals.promised_one);
    promises = {
      lock: lock.created_at ?? null,
      route: lock.route,
      unit,
      shots,
      totals,
      orders: { accepted: orders.filter((order) => order?.previous_lock === lock.created_at && order.status === "accepted").length, settled: orders.filter((order) => (order?.status ?? "settled") === "settled").length },
      note: "承諾是鎖定時每鏡答應的類型、買幾秒、路線與一次的價（plan/lock.json）；交付看 clips/manifest.json，花的看 ledger（伺服器 US$、網頁路線的點數）；差 ＝ 花的 − 承諾一次的價，負是省",
    };
  }

  // Five counts that are five different things: the server delivered, ffmpeg passed, the judge passed, nothing passed, the owner approved the gate.
  const readySheets = new Set(lookImages.filter((entry) => entry.status === "ready").map((entry) => entry.id));
  const readyImages = new Set(keyframeImages.filter((entry) => entry.status === "ready").map((entry) => String(entry.id).replace(/\/end$/, "")));
  const readyClips = new Set(clipJobs.filter((entry) => entry.status === "ready").map((entry) => entry.id));
  const drawn = drawnShotScenes(doc).map((scene) => scene.id);
  const characterEntries = Object.entries(characters?.characters ?? {});
  const status = {
    characters: {
      shots: characterEntries.length,
      job_ready: characterEntries.filter(([id]) => readySheets.has(id)).length,
      qc_ok: null,
      judge_passed: characterEntries.filter(([, entry]) => (entry.candidates ?? []).some((candidate) => candidate.judge?.passed)).length,
      needs_review: characterEntries.filter(([, entry]) => entry.needs_review).length,
      owner_accepted: gates.look === "approved" ? characterEntries.length : 0,
    },
    keyframes: {
      shots: keyframeShots.length,
      job_ready: keyframeShots.filter(([id]) => readyImages.has(id)).length,
      qc_ok: null,
      judge_passed: keyframeShots.filter(([, shot]) => shot.judge?.passed).length,
      needs_review: keyframeShots.filter(([, shot]) => shot.needs_review).length,
      owner_accepted: gates.storyboard === "approved" ? keyframeShots.filter(([id]) => drawn.includes(id)).length : 0,
    },
    clips: {
      shots: generated.length,
      job_ready: generated.filter(([id]) => readyClips.has(id)).length,
      qc_ok: generated.filter(([, shot]) => shot.qc?.ok).length,
      judge_passed: generated.filter(([, shot]) => shot.judge?.passed).length,
      needs_review: generated.filter(([, shot]) => shot.needs_review).length,
      owner_accepted: gates.final === "approved" ? generated.length : 0,
    },
    note: "五個數各算各的：ready 是伺服器交了檔（ledger），QC 是 ffmpeg 的 freeze/black/cut/PSNR（clips 的 qc.ok），judge 是 Gemini 的分數，needs_review 是沒有 take 同時過前兩項，站主核准是 look／storyboard／final 關卡現在是 approved",
  };
  const stale = Object.entries(gates).filter(([, each]) => each === "stale").map(([gate]) => gate);

  const wallclock = {};
  for (const run of state.runs ?? []) {
    const entry = wallclock[run.stage] ?? (wallclock[run.stage] = { runs: 0, seconds: 0, first_at: run.at ?? null, last_at: run.at ?? null, generated: 0 });
    entry.runs += 1;
    entry.seconds += Number(run.seconds || 0);
    entry.generated += Number(run.generated || 0);
    entry.last_at = run.at ?? entry.last_at;
  }
  const needsReview = takes.filter((take) => take.needs_review);
  return { slug: doc.slug, workdir, totals, saved, imported, spend, bought, takes, retakes, utilisation, waste, cuts, external, judge, status, gates, stale, wallclock, needs_review: needsReview, promises };
}

const promisedCell = (shot) => `${shot.promised.kind}${shot.promised.buy_s ? ` ${shot.promised.buy_s} s` : ""}${shot.promised.fit !== "auto" ? ` fit ${shot.promised.fit}` : ""}`;
const deliveredCell = (shot) => (shot.delivered ? `${shot.delivered.kind}${shot.delivered.seconds ? ` ${shot.delivered.seconds} s` : ""}${shot.delivered.external ? "（外部）" : ""}` : `還沒做（現在 ${shot.now.kind}${shot.now.fit !== "auto" ? ` fit ${shot.now.fit}` : ""}）`);
const keptCell = (shot) => (shot.kept ? "守住" : shot.change === "downgrade" ? `改小${shot.signed ? "（有變更單）" : "（沒簽變更單）"}` : "升級");
const signed = (value) => `${value >= 0 ? "+" : ""}${value}`;

export function renderReport(report) {
  const out = [];
  out.push(`${report.slug}（${report.workdir}）：共 ${usd(report.totals.usd)}；圖 ${report.totals.images} 張、片段 ${report.totals.clip_seconds} s${report.imported.clips ? `（其中匯入 ${report.imported.clip_seconds} s）` : ""}、音樂 ${report.totals.music} 首、judge ${report.totals.judge_calls} 次${report.spend.failed.count ? `；失敗但入帳 ${report.spend.failed.count} 筆 ${usd(report.spend.failed.usd)}` : ""}`);
  out.push("花在哪一類：" + KINDS.map((kind) => `${kind} ${report.spend.by_kind[kind].count} 筆 ${usd(report.spend.by_kind[kind].usd)}`).join("；"));
  out.push("花在哪一階段：" + (Object.entries(report.spend.by_stage).map(([stage, each]) => `${stage} ${usd(each.usd)}（judge ${each.judge_calls} 次）`).join("；") || "ledger 是空的"));
  out.push("");
  out.push("每鏡 take：");
  if (report.takes.length) for (const take of report.takes) out.push(`  ${take.stage.padEnd(9)} ${take.id.padEnd(12)} ${String(take.takes).padStart(2)} take，${take.passed} 過${take.judge !== null ? `，judge ${take.judge}/10` : ""}${take.needs_review ? `，needs_review：${take.problems.join("; ") || "沒寫原因"}` : ""}`);
  else out.push("  （還沒有 manifest）");
  out.push("");
  out.push(`秒數利用率（${report.utilisation.note}）：`);
  for (const shot of report.utilisation.shots) out.push(`  ${shot.id.padEnd(12)} 需要 ${shot.needed_s ?? "?"} s，買 ${shot.bought_s} s，${percent(shot.utilisation)}${shot.external ? "（外部）" : ""}`);
  out.push(`  整集：採用的 take ${percent(report.utilisation.overall_adopted)}（${report.utilisation.needed_s} ÷ ${report.utilisation.adopted_s} s）；全部買到的 ${percent(report.utilisation.overall_bought)}（${report.utilisation.needed_booked_s} ÷ ledger 的 ${report.utilisation.ledger_s} s，不含外部）`);
  out.push(`買了沒用的：圖 ${report.waste.images_bought} 買、${report.waste.images_used} 用；片段 ${report.waste.clip_seconds_bought} s 買、${report.waste.clip_seconds_used} s 採用`);
  out.push(`剪接：${report.cuts.cuts} 鏡從別鏡的片段切，省 ${report.cuts.clip_seconds} s、${usd(report.cuts.usd)}${report.cuts.shots.length ? `：${report.cuts.shots.map((cut) => `${cut.id} ← ${cut.source?.shot ?? "?"} @ ${cut.source?.from_s ?? "?"} s`).join("、")}` : ""}`);
  out.push(`外部片段（clips import 匯入的，或手放、ledger 沒有它的 job）：${report.external.length ? report.external.map((each) => `${each.id}（${each.file}，${each.seconds ?? "?"} s${each.route ? `，${each.route}` : ""}${each.credits !== null ? `，${each.credits} credits ${each.plan ?? ""}` : ""}${each.imported ? "" : "，手放"}）`).join("、") : "無"}${report.imported.clips ? `；帳本記的匯入：${report.imported.clips} 筆 ${report.imported.clip_seconds} s、${report.imported.credits} credits、${usd(report.imported.usd)}` : ""}`);
  out.push(`judge：${report.judge.calls} 次 ${usd(report.judge.usd)}（${Object.entries(report.judge.by_stage).map(([stage, calls]) => `${stage} ${calls}`).join("、") || "無"}）`);
  if (report.promises) {
    const { totals: sums } = report.promises;
    out.push("");
    out.push(`承諾 vs 交付（plan/lock.json 鎖定 ${report.promises.lock ?? "?"}，${report.promises.route}，${report.promises.unit}）：`);
    for (const shot of report.promises.shots) out.push(`  ${shot.id.padEnd(12)} 承諾 ${promisedCell(shot)} → ${deliveredCell(shot)}；花 ${shot.spent.amount}（${shot.spent.jobs} 筆），差 ${signed(shot.delta)}；${keptCell(shot)}`);
    out.push(`  整集：守住 ${sums.kept}／${sums.shots}，改小 ${sums.downgraded}（沒簽 ${sums.unsigned}），升級 ${sums.upgraded}，還沒做 ${sums.pending}；承諾 ${sums.promised_s} s、一次 ${sums.promised_one}${sums.expected !== null ? `、期望 ${sums.expected}` : ""}；交付 ${sums.delivered_s} s、花 ${sums.spent}；差 ${signed(sums.delta)} ${report.promises.unit}（負是省）；變更單：點頭未重鎖 ${report.promises.orders.accepted}、已重鎖 ${report.promises.orders.settled}`);
  }
  out.push("");
  out.push("五種狀態（各算各的）：    " + STATUS_COLUMNS.map((column) => STATUS_LABELS[column]).join("  "));
  for (const stage of ["characters", "keyframes", "clips"]) out.push(`  ${stage.padEnd(10)} ${String(report.status[stage].shots).padStart(3)}  ` + STATUS_COLUMNS.map((column) => cell(report.status[stage][column]).padStart(10)).join("  "));
  out.push(`過期的核准：${report.stale.length ? report.stale.join(", ") : "無"}（${Object.entries(report.gates).map(([gate, each]) => `${gate} ${each}`).join("、")}）`);
  out.push("每階段時間（state.json 的 runs）：" + (Object.entries(report.wallclock).map(([stage, each]) => `${stage} ${each.runs} 次 ${each.seconds} s（生成 ${each.generated}）`).join("；") || "沒有紀錄"));
  if (report.needs_review.length) {
    out.push("");
    out.push("待修：");
    for (const take of report.needs_review) out.push(`  ${take.stage} ${take.id}：${take.problems.join("; ") || "沒寫原因"}`);
  }
  return out.join("\n");
}

/** The form in references/post-mortem.md with the numbers filled; the human sections stay blank. */
export function renderMarkdown(report, now = new Date()) {
  const date = now.toISOString().slice(0, 10);
  const na = NOT_AVAILABLE;
  const column = (key) => ["characters", "keyframes", "clips"].map((stage) => cell(report.status[stage][key])).join(" | ");
  const externalSeconds = report.external.reduce((total, each) => total + Number(each.seconds || 0), 0);
  const externalCredits = report.external.some((each) => each.credits !== null) ? report.external.reduce((total, each) => total + Number(each.credits || 0), 0) : null;
  const externalPlans = [...new Set(report.external.map((each) => each.plan).filter(Boolean))];
  const out = [];
  out.push(`# ${report.slug} post-mortem（${date}）`);
  out.push("");
  out.push(`run_report.mjs 於 ${now.toISOString()} 從 ${report.workdir} 的 media/ledger.json、characters、keyframes、clips 的 manifest、timeline.json、state.json、approvals.json 算出；US$ 是 ledger 記的站上估價（apps/api/app/video_media/catalog.py），不是帳單。`);
  out.push("");
  out.push("## 範圍");
  out.push(`- 哪幾集、哪幾鏡、跑到哪一步、誰跑的：（人填；\`status\` 的 next）`);
  out.push(`- 路線：（人填）伺服器 API 的 provider／model 看 clips/manifest.json 的 clip 欄；外部片段 ${report.external.length} 支${externalPlans.length ? `（方案 ${externalPlans.join("、")}）` : ""}`);
  out.push("");
  out.push("## 買了什麼（帳本）");
  out.push("| 種類 | 筆數 | 單位 | US$（帳本） | 預留（站上） | 實際帳單 |");
  out.push("| --- | ---: | --- | ---: | --- | --- |");
  out.push(`| 設定圖 | ${report.bought.sheets.count} | 張 | ${report.bought.sheets.usd.toFixed(2)} | ${na} | ${na} |`);
  out.push(`| 關鍵影格 | ${report.bought.keyframes.count} | 張（含 end_frame ${report.bought.keyframes.end_frames}） | ${report.bought.keyframes.usd.toFixed(2)} | ${na} | ${na} |`);
  out.push(`| 素材 | ${report.bought.clips.count} | ${report.bought.clips.seconds} 秒 | ${report.bought.clips.usd.toFixed(2)} | ${na} | ${na} |`);
  out.push(`| 音樂 | ${report.bought.music.count} | 首 | ${report.bought.music.usd.toFixed(2)} | ${na} | ${na} |`);
  out.push(`| judge | ${report.bought.judge.count} | 次 | 0.01 × ${report.bought.judge.count} = ${report.bought.judge.usd.toFixed(2)} | ${na} | ${na} |`);
  out.push(`| 外部片段 | ${report.external.length} | ${report.external.length} 支／${externalSeconds} 秒 | ${report.imported.usd.toFixed(2)}（方案點數：${externalCredits === null ? na : `${externalCredits} 點`}，方案 ${externalPlans.join("、") || na}） | — | — |`);
  out.push(`| 合計 | ${report.bought.sheets.count + report.bought.keyframes.count + report.bought.clips.count + report.bought.music.count + report.bought.judge.count} | | ${report.totals.usd.toFixed(2)} | ${na} | ${na} |`);
  out.push(`- 本月剩餘（\`media-status\`）：${na}（離線）；失敗但入帳 ${report.spend.failed.count} 筆 ${usd(report.spend.failed.usd)}`);
  out.push("");
  out.push("## 接受了什麼（五個數字分開）");
  out.push("| | 設定圖 | 關鍵影格 | 素材 |");
  out.push("| --- | ---: | ---: | ---: |");
  out.push(`| 共 | ${column("shots")} |`);
  for (const key of STATUS_COLUMNS.slice(0, 4)) out.push(`| ${STATUS_LABELS[key]} | ${column(key)} |`);
  out.push(`| ${STATUS_LABELS.owner_accepted} | look: ${report.gates.look} ${report.status.characters.owner_accepted} | storyboard: ${report.gates.storyboard} ${report.status.keyframes.owner_accepted} | final: ${report.gates.final} ${report.status.clips.owner_accepted} |`);
  out.push(`- ${report.status.note}`);
  out.push("");
  out.push("## 浪費了什麼");
  out.push(`- 買了沒用的：圖 ${report.waste.images_bought} 買、${report.waste.images_used} 用；素材 ${report.waste.clip_seconds_bought} 秒買、${report.waste.clip_seconds_used} 秒採用（分母是「買了什麼」，匯入與手放的外部片段不算）`);
  out.push(`- 利用率（素材）：每鏡 ${report.utilisation.shots.map((shot) => `${shot.id} ${percent(shot.utilisation)}${shot.external ? "（外部）" : ""}`).join("、") || na}；整集 ${percent(report.utilisation.overall_adopted)}（採用的 take）／${percent(report.utilisation.overall_bought)}（全部買到，不含外部）；切鏡省下 ${report.cuts.clip_seconds} 秒／${usd(report.cuts.usd)}`);
  out.push(`- 白跑的輪：結束碼 2 ${na} 次、3 ${na} 次（state.json 不記結束碼；看 shell 紀錄）`);
  out.push("");
  if (report.promises) {
    const { totals: sums } = report.promises;
    out.push("## 承諾與交付（plan/lock.json）");
    out.push(`鎖定 ${report.promises.lock ?? na}，${report.promises.route}，單位 ${report.promises.unit}；守住 ${sums.kept}／${sums.shots}，改小 ${sums.downgraded}（沒簽變更單 ${sums.unsigned}），升級 ${sums.upgraded}，還沒做 ${sums.pending}；承諾一次 ${sums.promised_one}${sums.expected !== null ? `、期望 ${sums.expected}` : ""}，花 ${sums.spent}，差 ${signed(sums.delta)}（負是省）；變更單：點頭未重鎖 ${report.promises.orders.accepted}、已重鎖 ${report.promises.orders.settled}`);
    out.push("");
    out.push("| 鏡 | 承諾 | 交付 | 花 | 差 | 守住？ |");
    out.push("| --- | --- | --- | ---: | ---: | --- |");
    for (const shot of report.promises.shots) out.push(`| ${shot.id} | ${promisedCell(shot)}（${shot.promised.route}） | ${deliveredCell(shot)} | ${shot.spent.amount} | ${signed(shot.delta)} | ${keptCell(shot)} |`);
    out.push("");
  }
  out.push("## 重拍的原因分類（每個 needs_review 或退回的 take 一列）");
  out.push("| 鏡 | take | 退回的話（judge problems 或人看的） | 類別：內容／隨機／判讀／QC／工具 | 這次怎麼修 | 修了有沒有收斂 |");
  out.push("| --- | --- | --- | --- | --- | --- |");
  if (report.retakes.length) for (const retake of report.retakes) out.push(`| ${retake.stage}/${retake.id} | ${retake.take} | ${retake.problems.join("; ") || (retake.judge !== null ? `judge ${retake.judge}/10` : "沒寫原因")} | | | |`);
  else out.push("| （沒有退回的 take） | | | | | |");
  out.push("");
  out.push("## 路線與方案");
  out.push(`- 伺服器：每小時送出 ${na} 次、最長等待 ${na}（state.json 不記）；failed 的 job ${report.spend.failed.count} 筆`);
  out.push(`- Hailuo／Kling：匯入 ${report.external.length} 支${report.external.length ? `（${report.external.map((each) => `${each.id}${each.route ? ` ${each.route}` : ""}${each.credits !== null ? ` ${each.credits} 點` : ""}`).join("、")}）` : ""}；方案、排隊、assemble 過幾支：（人填）`);
  out.push("");
  out.push("## 核准");
  out.push("| 關卡 | 狀態（approved／stale／missing／absent） | stale 的原因（哪個改動） |");
  out.push("| --- | --- | --- |");
  for (const [gate, each] of Object.entries(report.gates)) out.push(`| ${gate} | ${each} | ${each === "stale" ? "（人填：核准後改了什麼）" : ""} |`);
  out.push("");
  out.push("## 時間");
  out.push("| 階段 | 跑了幾次 | 合計秒數（state.json runs） | 等站主多久 |");
  out.push("| --- | ---: | ---: | --- |");
  if (Object.keys(report.wallclock).length) for (const [stage, each] of Object.entries(report.wallclock)) out.push(`| ${stage} | ${each.runs} | ${each.seconds} | ${na} |`);
  else out.push(`| 全部 | — | ${na} | ${na} |`);
  out.push("");
  out.push("## 站主的反應");
  out.push("- 原話、日期、對哪一版（SHA-256）；接受／退回／沒看：（人填）");
  out.push("");
  out.push("## 下次改什麼（可驗證的，一條一個變數）");
  out.push("- 分鏡：");
  out.push("- prompt／camera／motion：");
  out.push("- 路線或模型：");
  out.push("- 流程（哪個檢查要提前、哪個腳本要補）：");
  out.push("- 不改的（為什麼）：");
  if (report.needs_review.length) {
    out.push("");
    out.push("## 附：needs_review 的鏡頭");
    for (const take of report.needs_review) out.push(`- ${take.stage} ${take.id}（${take.takes} take）：${take.problems.join("; ") || "沒寫原因"}`);
  }
  return out.join("\n");
}

export async function main(argv, stdout = process.stdout, stderr = process.stderr) {
  let values;
  try {
    ({ values } = parseArgs({ args: argv, options: { slug: { type: "string" }, workdir: { type: "string" }, root: { type: "string" }, markdown: { type: "boolean" }, json: { type: "boolean" } }, strict: true }));
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  if (!values.slug) {
    stderr.write("usage: run_report.mjs --slug <SLUG> [--workdir <work base>] [--root <repository root>] [--markdown] [--json]\n");
    return 2;
  }
  let report;
  try {
    report = await runReport({ slug: values.slug, root: values.root ? path.resolve(values.root) : undefined, workdir: values.workdir });
  } catch (error) {
    stderr.write(`${values.slug}: ${error.message}\n`);
    return 2;
  }
  stdout.write(`${values.json ? JSON.stringify(report, null, 2) : values.markdown ? renderMarkdown(report) : renderReport(report)}\n`);
  return 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
