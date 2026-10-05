#!/usr/bin/env node
// 離線預檢：下一個付費階段（look → keyframes → clips → music → assemble）跑下去，會先被什麼擋住
// （關卡沒核准或過期：exit 3；timeline 過期或 manifest 沒綁到現在的 hash：exit 2；lint 錯：exit 1），
// 又會白花什麼（judge 題目超過 400 字被站上拒收、
// 重跑把快取裡的 manifest 重寫而把核准作廢、production profile 的模型和存好的片段不合而整批重買）。
// 有開拍鎖定（plan/lock.json，animation-preproduction 的 plan_lock.mjs 寫的）時，每個階段再對照每鏡的承諾與連戲鎖：
// 鎖定時答應的 clip 變成 still、切或 fit freeze，或鎖住的道具／服裝／時刻字從 prompt 消失，而 plan/changes.jsonl 裡沒有
// 對照這把鎖、站主點頭的變更單，就以 lint 的碼（exit 1）擋下；有變更單只提醒。沒有鎖定檔的集不查。
// 只讀檔案：不碰伺服器、不要 token、不要 ffmpeg；伺服器實際選的模型得看 `media-status`，所以片段模型
// 從 series.json 的 production.profile.video、存好的 clips/manifest.json 或 --model 來。
//
//   node .agents/skills/animation-production/scripts/drama_preflight.mjs --slug <SLUG> [--workdir <work base>]
//     [--root <repository root>] [--stage look|keyframes|clips|music|assemble] [--model <clip model id>] [--json]
//
// 和各階段一樣，--workdir 是放所有影片的工作目錄（VIDEO_WORKDIR），影片自己的目錄是 <workdir>/<slug>/。
// 結束碼：0 沒有會被拒絕或白花的事；1 有（--json 時一樣）；2 讀不到專案或參數錯。
import { existsSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { approvalState } from "../../../../tools/video/core/approvals.mjs";
import { audioEvidenceProblems } from "../../../../tools/video/core/audio-evidence.mjs";
import { burnIn, clipShotScenes, drawnShotScenes, hasCast, isDrama, isSourced, lookHash, mixHash, resolveLook, resolveMusic, shotCast, shotScenes, sourcedShotScenes, stillShotScenes } from "../../../../tools/video/core/drama.mjs";
import { productionClipProblems, productionShotProblems } from "../../../../tools/video/core/lint.mjs";
import { readJson, resolveWorkBase, resolveWorkdir, stopRequested, UsageError } from "../../../../tools/video/core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, lookChosen, pipelineStatus } from "../../../../tools/video/core/state.mjs";
import { FPS, speechHash, visualHash } from "../../../../tools/video/core/timeline.mjs";
import { readLedger } from "../../../../tools/video/media/ledger.mjs";
import { continuityBreaks, coveringOrder, LOCK_FILE, lockProblem, promiseBreaks, readChangeOrders } from "../../animation-preproduction/scripts/plan_lock.mjs";
import { CONTINUITY_LABELS } from "../../animation-preproduction/scripts/shot_plan.mjs";
import { DEFAULT_IMAGE_MODEL, MAX_CLIP_TAKES, MAX_KEYFRAME_TAKES, MAX_LOOK_ROUNDS, PRICES, secondsBought } from "./episode_estimate.mjs";

// tools/video/cli.mjs EXIT（測試盯著一致）：各階段回的碼。
export const EXIT = { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5, incomplete: 6 };
export const STAGES = ["look", "keyframes", "clips", "music", "assemble"];
const STEP_OF = { look: "look generated", keyframes: "keyframes drawn", clips: "clips generated", music: "music generated", assemble: "video assembled" };
// 站上規定：judge 題目最長 400 字（apps/api/app/video_media/schemas.py JudgeCriterion.question）。
export const MAX_RUBRIC_QUESTION = 400;
// 站上預設：每月 judge 額度（apps/api/app/video_automation/models.py monthly_judge_calls_budget）。
export const JUDGE_MONTHLY_BUDGET = 3000;
// 站上規定：媒體路由每小時的 judge 次數（apps/api/app/video_media/admin_api.py JUDGES_PER_HOUR；
// 自動化路由另有自己的 60 次，不是這條線用的）。
export const JUDGE_CALLS_PER_HOUR = 360;
// tools/video/assemble/drama.mjs KEYFRAME_MIN_PSNR：片段第 0 格對 keyframe 的 PSNR 下限。
export const KEYFRAME_MIN_PSNR = 22;
const describe = { approved: "已核准", stale: "核准後檔案又變了（stale）", missing: "還沒核准", absent: "檔案還不存在" };
const usd = (value) => `US$${value.toFixed(2)}`;
const ids = (scenes) => scenes.map((scene) => scene.id).join(", ");

async function rubricBuilders() {
  try {
    const [keyframes, clips] = await Promise.all([import("../../../../tools/video/media/keyframes.mjs"), import("../../../../tools/video/media/clips.mjs")]);
    return { keyframeRubric: keyframes.keyframeRubric, clipRubric: clips.clipRubric, error: null };
  } catch (error) {
    return { keyframeRubric: null, clipRubric: null, error: error.message };
  }
}

/**
 * { slug, workdir, stage, next_paid, steps, gates, hashes, bindings, kept, needs_review, external, imported,
 *   stop, lock: null | { file, created_at, version, problem, broken: { promise, continuity }, signed: { promise, continuity } },
 *   findings: [{ stage, level: refuse|waste|note, exit, what, fix, usd?, judge_calls?, id? }], judge, exit_code }
 * findings 的 id 只有鎖定那幾條有：promise.broken、promise.signed、continuity.broken、continuity.signed。
 */
export async function preflight({ slug, root, workdir: workdirFlag, env = process.env, home, stage: wanted = null, model: modelFlag = null }) {
  if (wanted && !STAGES.includes(wanted)) throw new UsageError(`--stage must be one of ${STAGES.join(", ")}`);
  const project = loadProject({ slug, root });
  const { doc, lexicon, series } = project;
  if (!isDrama(doc)) throw new UsageError(`${slug} is not a drama (format "${doc.format}"); this preflight is for a drama's media stages`);
  const workdir = resolveWorkdir({ flag: workdirFlag, env, slug: doc.slug, root, home });
  const workBase = resolveWorkBase({ flag: workdirFlag, env, root, home });
  const lint = lintProject(project);
  const status = await pipelineStatus({ slug, root, workdir });
  const read = (name) => readJson(path.join(workdir, name), null);
  const timeline = read(ARTIFACTS.timeline);
  const characters = read(ARTIFACTS.characters);
  const choice = read(ARTIFACTS.characterChoice);
  const keyframes = read(ARTIFACTS.keyframes);
  const clips = read(ARTIFACTS.clips);
  const musicManifest = read(ARTIFACTS.music);
  const frames = read(ARTIFACTS.frames);
  const ledger = readLedger(workdir);
  const hashes = { look: lookHash(doc), visual: visualHash(doc), speech: speechHash(doc, lexicon), mix: mixHash(doc) };
  const gates = {};
  for (const gate of ["script", "look", "storyboard", "audio", "final"]) gates[gate] = await approvalState({ gate, docDir: project.dir, workdir });

  const cast = hasCast(doc);
  const look = resolveLook(doc.look);
  const chosen = cast ? lookChosen(characters, choice, hashes.look) : {};
  const profile = series?.production?.profile ?? null;
  const profileVideo = profile?.video ?? null;
  const clipModel = modelFlag ?? profileVideo?.model ?? clips?.clip?.model ?? null;
  const clipResolution = profileVideo?.resolution ?? clips?.clip?.resolution ?? PRICES[clipModel]?.default_resolution ?? null;
  const modelCurrent = !profile || ["provider", "model", "resolution"].every((key) => (clips?.clip?.[key] ?? null) === (profileVideo?.[key] ?? null));
  const bindings = {
    timeline: { file: ARTIFACTS.timeline, present: Boolean(timeline), bound: Boolean(timeline) && timeline.speech_hash === hashes.speech, binds: "speech_hash" },
    characters: { file: ARTIFACTS.characters, present: Boolean(characters), bound: Boolean(characters) && characters.look_hash === hashes.look, binds: "look_hash" },
    keyframes: { file: ARTIFACTS.keyframes, present: Boolean(keyframes), bound: Boolean(keyframes) && keyframes.look_hash === hashes.look && keyframes.visual_hash === hashes.visual, binds: "look_hash + visual_hash" },
    clips: { file: ARTIFACTS.clips, present: Boolean(clips), bound: Boolean(clips) && clips.speech_hash === hashes.speech && clips.visual_hash === hashes.visual && clips.look_hash === hashes.look, model_current: modelCurrent, binds: "speech_hash + visual_hash + look_hash（有 production profile 時再加 provider/model/resolution）" },
    frames: { file: ARTIFACTS.frames, present: Boolean(frames), bound: Boolean(frames) && frames.visual_hash === hashes.visual, binds: "visual_hash" },
    music: { file: ARTIFACTS.music, present: Boolean(musicManifest), bound: Boolean(musicManifest) && musicManifest.mix_hash === hashes.mix, binds: "mix_hash" },
  };

  const exists = (file) => Boolean(file) && existsSync(path.join(workdir, file));
  const drawn = drawnShotScenes(doc);
  const keptKeyframes = bindings.keyframes.bound ? drawn.filter((scene) => { const shot = keyframes.shots?.[scene.id]; return shot?.file && !shot.needs_review && exists(shot.file); }) : [];
  const newKeyframes = drawn.filter((scene) => !keptKeyframes.includes(scene));
  const clipShots = clipShotScenes(doc).filter((scene) => !isSourced(scene));
  const stills = stillShotScenes(doc);
  const cuts = sourcedShotScenes(doc);
  const keptClips = bindings.clips.bound && modelCurrent ? clipShots.filter((scene) => { const shot = clips.shots?.[scene.id]; return shot?.file && !shot.still && !shot.source && !shot.needs_review && exists(shot.file); }) : [];
  const newClips = clipShots.filter((scene) => !keptClips.includes(scene));
  const characterIds = cast ? doc.characters.map((character) => character.id) : [];
  const keptCharacters = bindings.characters.bound ? characterIds.filter((id) => { const entry = characters.characters?.[id]; return entry && !entry.needs_review && (entry.suggested !== null || chosen?.[id]); }) : [];
  const newCharacters = characterIds.filter((id) => !keptCharacters.includes(id));
  const needsReview = {
    characters: Object.entries(characters?.characters ?? {}).filter(([, entry]) => entry?.needs_review).map(([id]) => id),
    keyframes: Object.entries(keyframes?.shots ?? {}).filter(([, shot]) => shot?.needs_review).map(([id, shot]) => ({ id, problems: shot.problems ?? [] })),
    clips: Object.entries(clips?.shots ?? {}).filter(([, shot]) => shot?.needs_review).map(([id, shot]) => ({ id, problems: shot.problems ?? [] })),
  };
  const ledgerClipIds = new Set(ledger.entries.filter((entry) => entry.kind === "clip" && entry.status !== "cut" && entry.status !== "imported").map((entry) => entry.id));
  // Clips this line did not buy: `clips import` brought them in (imported_at) and checked them; the rest were put there by hand.
  const outside = Object.entries(clips?.shots ?? {}).filter(([id, shot]) => shot?.file && !shot.still && !shot.source && (shot.imported_at || shot.provider === "external" || !ledgerClipIds.has(id)));
  const external = outside.map(([id]) => id);
  const imported = outside.filter(([, shot]) => shot.imported_at).map(([id]) => id);
  const handPlaced = external.filter((id) => !imported.includes(id));
  const stop = stopRequested(workdir);
  const imagePrice = PRICES[DEFAULT_IMAGE_MODEL].usd_per_image;
  const judgePrice = PRICES.judge.usd_per_call;
  const clipPrice = PRICES[clipModel]?.usd_per_second ?? null;
  const framesOf = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, scene.end_frame - scene.start_frame]));
  const clipCost = (scenes) => (clipPrice === null ? null : scenes.reduce((total, scene) => total + secondsBought(framesOf.get(scene.id) ?? 0, clipModel, clipResolution) * clipPrice, 0));

  // The next paid stage is the earlier of what `status` says and what the manifests say: with
  // lint errors `status` marks every media step undone (its hashes are null), and a clips manifest
  // that covers only the shots of a `--shot` run counts as "clips generated" there while assemble
  // would still refuse the missing ones.
  const fromManifests = () => {
    if (cast && !(bindings.characters.bound && !newCharacters.length)) return "look";
    if (!(bindings.keyframes.bound && !newKeyframes.length)) return "keyframes";
    if (!(bindings.clips.bound && modelCurrent && !newClips.length && !needsReview.clips.length)) return "clips";
    if (doc.music && !bindings.music.bound) return "music";
    return "assemble";
  };
  const fromStatus = lint.errors.length ? null : STAGES.find((name) => {
    const step = status.steps.find((each) => each.id === STEP_OF[name]);
    return step && !step.done;
  }) ?? null;
  const nextPaid = [fromManifests(), fromStatus].filter(Boolean).sort((a, b) => STAGES.indexOf(a) - STAGES.indexOf(b))[0] ?? null;
  const stage = wanted ?? nextPaid;
  const findings = [];
  const add = (level, exit, what, fix, extra = {}) => findings.push({ stage, level, exit, what, fix, ...extra });
  const judge = { stage, calls_one: 0, calls_cap: 0 };
  const rubrics = await rubricBuilders();
  const longQuestions = (build, scenes) => (build ? scenes.flatMap((scene) => build(shotCast(doc, scene)).filter((criterion) => criterion.question.length > MAX_RUBRIC_QUESTION).map((criterion) => ({ shot: scene.id, key: criterion.key, length: criterion.question.length }))) : []);
  const reportLongQuestions = (long, what) => {
    if (!long.length) return;
    add("waste", EXIT.external, `${what} 的 judge 題目超過 ${MAX_RUBRIC_QUESTION} 字：${long.map((each) => `${each.shot}/${each.key} ${each.length} 字`).join("、")}（apps/api/app/video_media/schemas.py JudgeCriterion）`, "站上會以 422 拒收那次評審，而圖或片段已經買了、階段也會丟錯停下：先檢查這個階段實際產生的題目並修到 400 字內，再跑；keyframe 識別題仍直接帶 appearance，clip 識別題已改用有界文字與完整 context，不能把兩者當成相同限制");
  };
  const stopNote = () => { if (stop) add("note", null, "工作目錄（或它上一層）有 STOP 檔", "階段做完手上那一個單位就會退出；要整段跑完先刪掉 STOP"); };
  const lintRefuse = () => { if (lint.errors.length) add("refuse", EXIT.lint, `video.json 有 ${lint.errors.length} 個 lint 錯誤：${lint.errors.slice(0, 3).map((error) => `${error.path}: ${error.message}`).join("；")}${lint.errors.length > 3 ? "…" : ""}`, "先 `node tools/video/cli.mjs lint --slug <slug>` 修到 0 錯"); };
  const rateNote = () => { if (judge.calls_cap > JUDGE_CALLS_PER_HOUR) add("note", null, `這一跑最壞要 ${judge.calls_cap} 次 judge，超過站上每小時 ${JUDGE_CALLS_PER_HOUR} 次（apps/api/app/video_media/admin_api.py JUDGES_PER_HOUR）；每月額度 ${JUDGE_MONTHLY_BUDGET}（apps/api/app/video_automation/models.py 預設，剩多少看 media-status）`, "超過就會 429 等下一小時：用 --shot 分批跑，或先把 needs_review 的提示修好再跑"); };

  if (stage === "look") {
    lintRefuse();
    if (!cast) add("note", null, "沒有角色：look 階段沒東西畫，也沒有 look 關卡", "narrator-only 的漫劇直接跑 keyframes");
    else {
      const candidates = look.candidates;
      judge.calls_one = newCharacters.length * candidates;
      judge.calls_cap = newCharacters.length * candidates * MAX_LOOK_ROUNDS;
      if (bindings.characters.bound && !newCharacters.length) {
        if (gates.look.status === "approved") add("waste", null, `characters/manifest.json 已綁到現在的 look_hash（${hashes.look}），${characterIds.length} 個角色都有表，look 關卡已核准`, "再跑 look 會從快取取圖、不花錢，但會重寫 manifest，look 核准就作廢，站主要再核一次：沒有要改人設就不要跑");
        else add("note", null, `characters/manifest.json 已綁到現在的 look_hash，${characterIds.length} 個角色都有表；look 關卡${describe[gates.look.status]}`, "下一步是 review-push --gate look，不是再跑 look");
      } else {
        add("note", null, `要畫的角色：${newCharacters.join(", ") || "無"}（${candidates} 張候選各一次 judge；最壞 ${MAX_LOOK_ROUNDS} 輪）；留用：${keptCharacters.join(", ") || "無"}`, `約 ${usd(newCharacters.length * candidates * (imagePrice + judgePrice))} 一輪`, { usd: newCharacters.length * candidates * (imagePrice + judgePrice), judge_calls: judge.calls_one });
        if (bindings.characters.present && !bindings.characters.bound) add("note", null, "characters/manifest.json 是舊 look 畫的（look_hash 不同）：這次把每個角色重畫", "look.style / negative / motion、角色 appearance、sheet_prompt 任何一個改了都算新 look；改之前先想清楚");
      }
      if (needsReview.characters.length) add("note", null, `上次沒有候選過 judge 的角色：${needsReview.characters.join(", ")}`, "改 appearance 或 sheet_prompt 再跑；不改提示重跑只會得到同樣的圖");
    }
    stopNote();
    rateNote();
  } else if (stage === "keyframes") {
    lintRefuse();
    if (cast) {
      if (gates.look.status !== "approved") add("refuse", EXIT.owner, `look 關卡${describe[gates.look.status]}${gates.look.status === "absent" ? "（還沒跑 look）" : ""}`, gates.look.status === "absent" ? "先跑 look" : "review-push --gate look，等站主在 /admin/videos 選表，再 review-pull");
      else if (chosen === null) add("refuse", EXIT.owner, "look 已核准，但有角色沒有選定的人設表（choice.json 沒綁到現在的 look_hash，manifest 也沒有 suggested）", "review-pull，或 look --choose <id>=<n>");
    }
    judge.calls_one = newKeyframes.length;
    judge.calls_cap = newKeyframes.length * MAX_KEYFRAME_TAKES;
    const endFrames = newKeyframes.filter((scene) => scene.data.end_frame?.prompt).length;
    const oneTake = newKeyframes.length * (imagePrice + judgePrice) + endFrames * imagePrice;
    if (bindings.keyframes.bound && !newKeyframes.length) {
      if (gates.storyboard.status === "approved") add("waste", null, `keyframes/manifest.json 已綁到現在的 look_hash + visual_hash，${drawn.length} 鏡都留用，storyboard 關卡已核准`, "再跑 keyframes 從快取取圖、不花錢，但會重寫 manifest，storyboard 核准作廢：沒有要改分鏡就不要跑");
      else add("note", null, `keyframes/manifest.json 已綁到現在的 hash，${drawn.length} 鏡都留用；storyboard 關卡${describe[gates.storyboard.status]}`, "下一步是 review-push --gate storyboard");
    } else {
      add("note", null, `要畫：${ids(newKeyframes) || "無"}（${newKeyframes.length} 鏡，end_frame ${endFrames} 張）；留用：${ids(keptKeyframes) || "無"}`, `約 ${usd(oneTake)} 一 take，最壞 ${usd(newKeyframes.length * MAX_KEYFRAME_TAKES * (imagePrice + judgePrice) + endFrames * imagePrice)}（keyframe ${MAX_KEYFRAME_TAKES} take）`, { usd: oneTake, judge_calls: judge.calls_one });
      if (bindings.keyframes.present && !bindings.keyframes.bound) add("note", null, `keyframes/manifest.json 是舊劇本或舊 look 畫的（要 look_hash ${hashes.look} + visual_hash ${hashes.visual}）：上一次的修改把 ${drawn.length} 鏡全部重買`, "visual_hash 連 scenes 的 id、chapter、data、lines 的 id 都算：改一個鏡頭的 prompt 就是整本重畫（快取只省下提示沒變的那些）；改之前先 keyframes --dry-run 看會畫幾張");
      if (bindings.keyframes.bound && gates.storyboard.status === "approved") add("note", null, "storyboard 已核准，但這次要補畫鏡頭：跑完 manifest 會變、核准作廢", "補畫完要再 review-push --gate storyboard");
    }
    if (needsReview.keyframes.length) add("note", null, `上次沒有 take 過 judge 的鏡頭：${needsReview.keyframes.map((shot) => `${shot.id}（${shot.problems.join("; ") || "沒寫原因"}）`).join("、")}`, "先改 prompt 再跑；不改提示重跑只會再買同樣的 3 張");
    reportLongQuestions(longQuestions(rubrics.keyframeRubric && ((characters) => rubrics.keyframeRubric(characters, { subtitleBand: burnIn(doc), craft: false })), newKeyframes), "keyframe");
    if (rubrics.error) add("note", null, `讀不到 keyframes.mjs 的 rubric（${rubrics.error}）`, "judge 題目長度這一項沒檢查");
    stopNote();
    rateNote();
  } else if (stage === "clips") {
    lintRefuse();
    if (!bindings.timeline.bound) add("refuse", EXIT.usage, bindings.timeline.present ? "timeline.json 是舊劇本合成的（speech_hash 不同）" : "沒有 timeline.json", "先跑 tts（片段和台詞一樣長，沒有 timeline 就不知道買幾秒）");
    const timing = bindings.timeline.bound ? productionShotProblems(doc, series, timeline) : [];
    if (timing.length) add("refuse", EXIT.owner, `production profile 的時長規則：${timing.map((problem) => `${problem.path}: ${problem.message}`).join("；")}`, "拆鏡或縮台詞，再 tts");
    if (!bindings.keyframes.bound) add("refuse", EXIT.usage, bindings.keyframes.present ? "keyframes/manifest.json 是舊劇本或舊 look 畫的" : "沒有 keyframes/manifest.json", "先跑 keyframes，再 review-push --gate storyboard");
    else {
      const undrawn = [...clipShots, ...stills].filter((scene) => !keyframes.shots?.[scene.id]?.file || keyframes.shots[scene.id].needs_review);
      if (undrawn.length) add("refuse", EXIT.usage, `這些鏡頭沒有過 judge 的 keyframe：${ids(undrawn)}`, "修 prompt、跑 keyframes，再核 storyboard");
    }
    if (gates.storyboard.status !== "approved") add("refuse", EXIT.owner, `storyboard 關卡${describe[gates.storyboard.status]}`, "review-push --gate storyboard，等站主（或自動核准設定）在 /admin/videos 決定，再 review-pull");
    if (clipModel === null) add("note", null, "離線看不出伺服器會用哪個片段模型（series.json 沒有 production.profile.video，也沒有存過 clips/manifest.json）", "先 `clips --dry-run` 看 server 行，核對實際模型、解析度與預算");
    if (bindings.clips.present && bindings.clips.bound && !modelCurrent) add("waste", null, `clips/manifest.json 是 ${clips.clip?.provider ?? "?"} ${clips.clip?.model ?? "?"} ${clips.clip?.resolution ?? "?"} 做的，production profile 要 ${profileVideo?.provider ?? ""} ${profileVideo?.model} ${profileVideo?.resolution}`, `模型不同時整本 manifest 重建，${clipShots.length} 支片段全部重買：要換模型就要認這筆錢；不換就把 profile 改回去`);
    if (bindings.clips.present && bindings.clips.bound && modelCurrent && bindings.timeline.bound) {
      const cached = productionClipProblems(doc, series, timeline, clips).filter((problem) => problem.path.startsWith("clips."));
      for (const problem of cached) add("refuse", EXIT.owner, `存好的片段 ${problem.path.slice(6)}：${problem.message}`, "clips 會在這個鏡頭停下（cached clip … revise or explicitly regenerate）：修劇本、或刪掉它的 manifest 條目讓它重買");
    }
    judge.calls_one = newClips.length;
    judge.calls_cap = newClips.length * MAX_CLIP_TAKES;
    const cost = clipCost(newClips);
    if (!newClips.length && clipShots.length) add("note", null, `${clipShots.length} 支片段都留用（manifest 綁到現在的三個 hash）；還有 ${stills.length} 支 still、${cuts.length} 支 cut`, "clips 只會補 still 和 cut 的條目，不花錢");
    else add("note", null, `要買：${ids(newClips) || "無"}（${newClips.length} 支）；留用：${ids(keptClips) || "無"}；still ${stills.length}、cut ${cuts.length} 不買`, cost === null ? `模型 ${clipModel ?? "未知"} 不在 PRICES，算不出錢；用 clips --dry-run` : `約 ${usd(cost + newClips.length * judgePrice)} 一 take，最壞 ${usd(cost * MAX_CLIP_TAKES + newClips.length * MAX_CLIP_TAKES * judgePrice)}（clip ${MAX_CLIP_TAKES} take，${clipModel} ${clipResolution ?? ""}）`, { usd: cost === null ? null : cost + newClips.length * judgePrice, judge_calls: judge.calls_one });
    if (bindings.clips.present && !bindings.clips.bound) add("note", null, `clips/manifest.json 是舊劇本、舊台詞或舊 look 做的（要 speech ${hashes.speech}、visual ${hashes.visual}、look ${hashes.look}）：上一次的修改把 ${clipShots.length} 支片段全部重買`, "改台詞（speech_hash）、改任何鏡頭的 data（visual_hash）、改 look 都會：先算一下值不值");
    if (needsReview.clips.length) add("note", null, `上次沒有 take 過的鏡頭：${needsReview.clips.map((shot) => `${shot.id}（${shot.problems.join("; ") || "沒寫原因"}）`).join("、")}`, "先改 motion / camera 再跑；不改提示重跑只會再買兩個 take");
    reportLongQuestions(longQuestions(rubrics.clipRubric, newClips), "clip");
    if (rubrics.error) add("note", null, `讀不到 clips.mjs 的 rubric（${rubrics.error}）`, "judge 題目長度這一項沒檢查");
    if (imported.length) add("note", null, `clips import 匯入的片段：${imported.join(", ")}`, "它們過了跟買來的 take 同一組 ffmpeg 檢查，judge 只有匯入時帶 --judge 才問過；clips 會留用它們，clips --force 會把它們重買");
    if (handPlaced.length) add("note", null, `clips/manifest.json 裡有不是這條線買的片段（ledger 沒有它們的 job）：${handPlaced.join(", ")}`, `手放的外部素材沒有經過 clips 的 qc.mjs（黑格、freezedetect、模型自己切鏡），assemble 只驗格數、第 0 格對 keyframe 的 PSNR（≥ ${KEYFRAME_MIN_PSNR}）、fit 的停格 > 60 格與響度，ledger 和 run_report 的錢也不含它們：改用 clips import 重新帶進來（references/stage-preconditions.md 最後一節）`);
    stopNote();
    rateNote();
  } else if (stage === "music") {
    lintRefuse();
    const music = resolveMusic(doc);
    if (!music) add("note", null, "沒有 music：music 階段沒東西做（會丟 usage error，exit 2）", "不用跑；assemble 不會等它");
    else if (music.track) {
      const file = path.join(workBase, "_music", music.track);
      if (!existsSync(file)) add("refuse", EXIT.owner, `music.track ${music.track} 不在 ${path.join(workBase, "_music")}`, "把授權的檔放進去（名字要一樣）；music.sha256 有填就要對得上");
      else add("note", null, `站主自己的音軌 ${music.track}：不花錢`, bindings.music.bound ? "manifest 已綁到現在的 mix_hash" : "跑 music 只是驗檔並寫 manifest");
    } else {
      if (!bindings.timeline.bound) add("refuse", EXIT.usage, bindings.timeline.present ? "timeline.json 是舊劇本合成的" : "沒有 timeline.json", "先跑 tts（曲子要和影片一樣長）");
      if (bindings.music.bound) add("note", null, "music/manifest.json 已綁到現在的 mix_hash", "再跑會從快取取（同提示同長度不會再付）");
      else add("note", null, `要生成一首（${usd(PRICES["lyria-3.5"].usd_per_track)}）`, "music.prompt 改了才會再買；gain/duck 只改混音不改曲");
    }
    stopNote();
  } else if (stage === "assemble") {
    lintRefuse();
    if (!bindings.timeline.bound) add("refuse", EXIT.usage, bindings.timeline.present ? "timeline.json 是舊劇本合成的" : "沒有 timeline.json", "先跑 tts");
    else {
      const audio = audioEvidenceProblems(timeline, workdir);
      if (audio.length) add("refuse", EXIT.usage, `narration 的音檔證據不齊：${audio.join("; ")}`, "再跑 tts");
    }
    if (!bindings.frames.bound) add("refuse", EXIT.usage, bindings.frames.present ? "frames/manifest.json 是舊劇本畫的" : "沒有 frames/manifest.json", "先跑 render（本機、免費）");
    else if (burnIn(doc) && (frames.speech_hash !== hashes.speech || !frames.subtitles)) add("refuse", EXIT.usage, "frames/manifest.json 沒有這份劇本的字幕條", "再跑 render");
    if (!bindings.clips.bound) add("refuse", EXIT.usage, bindings.clips.present ? "clips/manifest.json 是舊劇本或舊 look 做的" : "沒有 clips/manifest.json", "先跑 clips");
    else {
      const waiting = [...needsReview.keyframes.map((shot) => shot.id), ...needsReview.clips.map((shot) => shot.id)];
      if (waiting.length) add("refuse", null, `有鏡頭 needs_review：${waiting.join(", ")}`, "assemble 會丟 PlanError 停下：修提示、重跑 keyframes / clips");
      if (bindings.timeline.bound) {
        const problems = productionClipProblems(doc, series, timeline, clips);
        if (problems.length) add("refuse", EXIT.usage, `production clips need review：${problems.map((problem) => `${problem.path}: ${problem.message}`).join("；")}`, "重跑 clips 或改 profile");
      }
    }
    if (doc.music && !bindings.music.bound) add("refuse", EXIT.usage, bindings.music.present ? "music/manifest.json 是舊的（mix_hash 不同）" : "沒有 music/manifest.json", "先跑 music");
    if (handPlaced.length) add("note", null, `手放的外部片段 ${handPlaced.join(", ")} 在這裡只受第 0 格 PSNR（≥ ${KEYFRAME_MIN_PSNR}，對 keyframe）、fit 的停格 > 60 格與響度檢查；黑格、freezedetect、模型自己切鏡 assemble 不查（只有 clips 的 qc.mjs 查）`, "外部片段的第一格要就是這個鏡頭的 keyframe（image-to-video 用那張圖起手），不然 checks.json 會把它列成問題；用 clips import 重新帶進來，黑格／凍格／切鏡才查得到（references/stage-preconditions.md 最後一節）");
    add("note", null, "assemble 在本機跑 ffmpeg，不花錢；只有 branding 和 final 核准在後面", "跑完看 checks.json 的 problems");
    stopNote();
  } else {
    add("note", null, "付費階段都做完了（look、keyframes、clips、music、assemble 的步驟都是 done）", "下一步看 `status`：captions、final 核准、package");
  }
  for (const [gate, state] of Object.entries(gates)) {
    if (state.status === "stale") add("note", null, `${gate} 關卡的核准過期了（檔案在核准後變過）`, "要用到它的階段會以 exit 3 拒絕：再 review-push 那一關");
  }

  // 開拍鎖定的承諾與連戲鎖（plan/lock.json）：鎖定時答應的 clip 變成 still、切、刪掉或 fit freeze，或鎖住的連戲字從 prompt
  // 消失，而 changes.jsonl 沒有對照這把鎖、記了這一鏡這個改動的變更單，就以 lint 的碼擋；有變更單只提醒。每個階段都查：
  // 承諾是錢還沒花之前的事，但花過之後也不該靜靜改掉。沒有鎖定檔（沒走 animation-preproduction 的集）不查。
  const lockDoc = readJson(path.join(workdir, LOCK_FILE), null);
  const lock = lockDoc ? { file: LOCK_FILE, created_at: lockDoc.created_at ?? null, version: lockDoc.version ?? null, problem: lockProblem(lockDoc), broken: { promise: [], continuity: [] }, signed: { promise: [], continuity: [] } } : null;
  if (lock?.problem) add("note", null, `${LOCK_FILE}：${lock.problem}`, "承諾與連戲鎖這一項沒檢查；plan_lock.mjs 重鎖之後再跑");
  else if (lock) {
    const orders = readChangeOrders(workdir);
    const nowKind = { still: "是 still", cut: "是切素材（source）", removed: "不在 video.json 裡" };
    const signedBy = (order) => `有站主點頭的變更單（${order.at}${order.note ? `：${order.note}` : ""}）`;
    for (const broken of promiseBreaks(lockDoc, doc)) {
      const what = `${broken.id} 鎖定時答應的是 clip（買 ${broken.promise.buy_s} s，${broken.promise.route}），現在${broken.kind ? nowKind[broken.now.kind] ?? `是 ${broken.now.kind}` : ` fit 是 freeze（鎖定時 ${broken.promise.fit}）`}`;
      const order = coveringOrder(orders, lockDoc, broken.id, { kind: broken.kind, fit: broken.fit });
      if (order) {
        lock.signed.promise.push(broken.id);
        add("note", null, `${what}：${signedBy(order)}`, "照變更單做；一次改完再 plan_lock.mjs --write --force 重鎖", { id: "promise.signed" });
      } else {
        lock.broken.promise.push(broken.id);
        add("refuse", EXIT.lint, `${what}，沒有變更單`, "不是站主的意思就改回鎖定的樣子；是的話 plan_lock.mjs --check 印變更單，站主點頭後 --accept --note \"<站主的話>\"，或一次改完 --write --force 重鎖", { id: "promise.broken" });
      }
    }
    for (const broken of continuityBreaks(lockDoc, doc)) {
      const what = `${broken.id} 鎖住的連戲字不在 prompt 裡了：${broken.missing.map((item) => `${CONTINUITY_LABELS[item.category] ?? item.category}「${item.text}」`).join("、")}${broken.depends_on.length ? `（接 ${broken.depends_on.join("、")} 的字）` : ""}`;
      const order = coveringOrder(orders, lockDoc, broken.id, { continuity: broken });
      if (order) {
        lock.signed.continuity.push(broken.id);
        add("note", null, `${what}：${signedBy(order)}`, "照變更單做；關鍵影格要不要重畫看 plan_lock.mjs --check 的「會重畫、重買或重做」", { id: "continuity.signed" });
      } else {
        lock.broken.continuity.push(broken.id);
        add("refuse", EXIT.lint, `${what}，沒有變更單`, "把那個字寫回 prompt（每鏡的錨點寫一樣的字），或 plan_lock.mjs --check 看變更單、站主點頭後 --accept --note \"<站主的話>\"，或一次改完 --write --force 重鎖", { id: "continuity.broken" });
      }
    }
  }

  const refused = findings.filter((finding) => finding.level === "refuse");
  const wasted = findings.filter((finding) => finding.level === "waste");
  return {
    slug: doc.slug,
    workdir,
    stage,
    next_paid: nextPaid,
    steps: status.steps.map((step) => ({ id: step.id, done: step.done, note: step.note ?? null })),
    gates: Object.fromEntries(Object.entries(gates).map(([gate, state]) => [gate, state.status])),
    hashes,
    clip_model: clipModel,
    clip_resolution: clipResolution,
    bindings,
    kept: { characters: keptCharacters, keyframes: keptKeyframes.map((scene) => scene.id), clips: keptClips.map((scene) => scene.id) },
    new: { characters: newCharacters, keyframes: newKeyframes.map((scene) => scene.id), clips: newClips.map((scene) => scene.id) },
    needs_review: needsReview,
    external,
    imported,
    stop,
    lock,
    lint: { errors: lint.errors.length, warnings: lint.warnings.length },
    judge: { ...judge, per_hour: JUDGE_CALLS_PER_HOUR, monthly: JUDGE_MONTHLY_BUDGET },
    findings,
    exit_code: refused.length || wasted.length ? 1 : 0,
  };
}

export function renderPreflight(result) {
  const out = [];
  out.push(`${result.slug}（${result.workdir}）：下一個付費階段 ${result.next_paid ?? "無"}${result.stage !== result.next_paid ? `；檢查的是 --stage ${result.stage}` : ""}`);
  out.push(`關卡：${Object.entries(result.gates).map(([gate, state]) => `${gate} ${describe[state]}`).join("；")}`);
  out.push(`現在的 hash：look ${result.hashes.look}、visual ${result.hashes.visual}、speech ${result.hashes.speech}、mix ${result.hashes.mix}`);
  for (const [name, binding] of Object.entries(result.bindings)) out.push(`  ${name.padEnd(10)} ${binding.present ? (binding.bound ? "綁到現在的 " + binding.binds : "有，但是舊的（" + binding.binds + " 不同）") : "沒有"}${binding.model_current === false ? "；模型和 production profile 不合" : ""}`);
  out.push(`留用／要買：角色 ${result.kept.characters.length}／${result.new.characters.length}，keyframe ${result.kept.keyframes.length}／${result.new.keyframes.length}，clip ${result.kept.clips.length}／${result.new.clips.length}`);
  if (result.clip_model) out.push(`片段模型（離線推斷）：${result.clip_model} ${result.clip_resolution ?? ""}`);
  if (result.lock) out.push(`開拍鎖定 ${result.lock.created_at ?? "?"}：${result.lock.problem ? result.lock.problem : `承諾改小 沒變更單 ${result.lock.broken.promise.length}／有 ${result.lock.signed.promise.length}；連戲字少了 沒變更單 ${result.lock.broken.continuity.length}／有 ${result.lock.signed.continuity.length}`}`);
  if (result.stop) out.push("STOP 檔在");
  out.push("");
  out.push(`階段 ${result.stage ?? "-"}：`);
  const mark = { refuse: "拒絕", waste: "白花", note: "提醒" };
  for (const finding of result.findings) {
    out.push(`  [${mark[finding.level]}${finding.exit !== null && finding.exit !== undefined ? ` exit ${finding.exit}` : ""}] ${finding.what}`);
    out.push(`      → ${finding.fix}`);
  }
  out.push(`judge：這一跑 ${result.judge.calls_one} 次，最壞 ${result.judge.calls_cap} 次（每小時 ${result.judge.per_hour}、每月 ${result.judge.monthly}）`);
  out.push(result.exit_code ? "結論：有會被拒絕或白花的事，先處理再花錢。" : "結論：沒有會被拒絕或白花的事。");
  return out.join("\n");
}

export async function main(argv, stdout = process.stdout, stderr = process.stderr) {
  let values;
  try {
    ({ values } = parseArgs({ args: argv, options: { slug: { type: "string" }, workdir: { type: "string" }, root: { type: "string" }, stage: { type: "string" }, model: { type: "string" }, json: { type: "boolean" } }, strict: true }));
  } catch (error) {
    stderr.write(`${error.message}\n`);
    return 2;
  }
  if (!values.slug) {
    stderr.write("usage: drama_preflight.mjs --slug <SLUG> [--workdir <work base>] [--root <repository root>] [--stage look|keyframes|clips|music|assemble] [--model <clip model id>] [--json]\n");
    return 2;
  }
  let result;
  try {
    result = await preflight({ slug: values.slug, root: values.root ? path.resolve(values.root) : undefined, workdir: values.workdir, stage: values.stage ?? null, model: values.model ?? null });
  } catch (error) {
    stderr.write(`${values.slug}: ${error.message}\n`);
    return 2;
  }
  stdout.write(`${values.json ? JSON.stringify(result, null, 2) : renderPreflight(result)}\n`);
  return result.exit_code;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) main(process.argv.slice(2)).then((code) => { process.exitCode = code; });
