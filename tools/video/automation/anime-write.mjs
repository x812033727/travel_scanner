// Bounded, durable screenplay generation. A successful act is committed before the next
// model call; replay only uses checkpoints bound to this exact source and operation.
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync } from "node:fs";
import path from "node:path";

import { requireAnimePolicy } from "../core/anime-policy.mjs";
import { atomicWrite } from "../core/paths.mjs";
import { LINE_ID } from "../core/schema.mjs";
import { estimateTimeline, frameToSeconds } from "../core/timeline.mjs";
import { AutomationError, OUTPUT_INVALID } from "./client.mjs";

export const ANIME_ACT_OUTPUT_TOKENS = 32_000;
export const ANIME_ACT_MAX_SECONDS = 300;
const MAX_ACT_BYTES = 180_000;
const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);
const fail = (message) => { throw new AutomationError(message, { code: OUTPUT_INVALID }); };
const canonical = (value) => Array.isArray(value) ? value.map(canonical) : object(value) ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, canonical(value[key])])) : value;
export const animeSourceHash = (value) => createHash("sha256").update(JSON.stringify(canonical(value))).digest("hex");
const save = (file, value) => atomicWrite(file, `${JSON.stringify(value, null, 2)}\n`);
const load = (file) => JSON.parse(readFileSync(file, "utf8"));

function allocatedIds(ids, count, taken) {
  if (!Array.isArray(ids) || ids.length !== count || ids.some((id) => !LINE_ID.test(id) || taken.has(id)) || new Set(ids).size !== ids.length) fail("anime act line ids must be unique, new and valid");
  ids.forEach((id) => taken.add(id));
  return ids;
}

/** Four or more acts; existing shots are assigned once, in order, using their natural timing. */
export function animeActPlan(source, existingVideo = null) {
  const runtime = requireAnimePolicy(source.series ?? source);
  const count = Math.max(4, Math.ceil(runtime.body_target_seconds / ANIME_ACT_MAX_SECONDS));
  const target = runtime.body_target_seconds / count;
  const acts = Array.from({ length: count }, (_, index) => ({ id: `act-${String(index + 1).padStart(2, "0")}`, index: index + 1, count, target_seconds: target, scene_prefix: `a${String(index + 1).padStart(2, "0")}-`, scenes: [] }));
  if (existingVideo) {
    const timeline = estimateTimeline(existingVideo);
    const durations = new Map(timeline.scenes.map((scene) => [scene.id, frameToSeconds(scene.end_frame - scene.start_frame)]));
    let elapsed = 0;
    for (const scene of existingVideo.scenes ?? []) {
      const index = Math.min(count - 1, Math.floor(elapsed / target));
      acts[index].scenes.push(scene);
      elapsed += durations.get(scene.id) ?? 0;
    }
    // A short rejected draft still gets four bounded repair units, rather than one giant act.
    if (acts.some((act) => !act.scenes.length) && (existingVideo.scenes?.length ?? 0) >= count) {
      acts.forEach((act) => { act.scenes = []; });
      existingVideo.scenes.forEach((scene, index) => acts[Math.min(count - 1, Math.floor(index * count / existingVideo.scenes.length))].scenes.push(scene));
    }
  }
  return acts;
}

export function animeActProblem(answer, act, { fresh = false } = {}) {
  if (!object(answer) || answer.act_id !== act.id || !object(answer.video) || !Array.isArray(answer.video.scenes) || !answer.video.scenes.length) return `${act.id}: expected matching act_id and nonempty video.scenes`;
  if (Buffer.byteLength(JSON.stringify(answer)) > MAX_ACT_BYTES) return `${act.id}: output exceeds the bounded act size`;
  if (answer.video.characters !== undefined && (!Array.isArray(answer.video.characters) || answer.video.characters.some((character) => !object(character) || typeof character.id !== "string"))) return `${act.id}: characters must be a valid cast list`;
  if (answer.video.scenes.length > 180) return `${act.id}: too many scenes for one bounded act`;
  const allowed = new Set(act.line_ids);
  const oldScenes = new Set(act.scenes.map((scene) => scene.id));
  const sceneIds = new Set();
  const lineIds = new Set();
  for (const scene of answer.video.scenes) {
    if (!object(scene) || typeof scene.id !== "string" || !Array.isArray(scene.lines)) return `${act.id}: malformed scene`;
    if ((!oldScenes.has(scene.id) && !scene.id.startsWith(act.scene_prefix)) || (fresh && !scene.id.startsWith(act.scene_prefix))) return `${act.id}: scene ${scene.id} belongs to another act`;
    if (sceneIds.has(scene.id)) return `${act.id}: duplicate scene ${scene.id}`;
    sceneIds.add(scene.id);
    for (const line of scene.lines) {
      if (!object(line) || !allowed.has(line.id) || lineIds.has(line.id)) return `${act.id}: missing, duplicate or foreign line id ${line?.id ?? ""}`;
      lineIds.add(line.id);
    }
  }
  return null;
}

/** Reject a partial, duplicate or substituted act before creating the complete screenplay. */
export function mergeAnimeActs(acts, answers, existingVideo = null) {
  if (answers.length !== acts.length || new Set(answers.map((answer) => answer?.act_id)).size !== acts.length) fail("anime merge needs each planned act exactly once");
  const scenes = [];
  const sceneIds = new Set();
  const lineIds = new Set();
  for (let index = 0; index < acts.length; index++) {
    const problem = animeActProblem(answers[index], acts[index], { fresh: !existingVideo });
    if (problem) fail(problem);
    for (const scene of answers[index].video.scenes) {
      if (sceneIds.has(scene.id)) fail(`anime merge duplicates scene ${scene.id}`);
      sceneIds.add(scene.id);
      for (const line of scene.lines) {
        if (lineIds.has(line.id)) fail(`anime merge duplicates line ${line.id}`);
        lineIds.add(line.id);
      }
      scenes.push(scene);
    }
  }
  const metadata = existingVideo ? { ...existingVideo, ...answers[0].video } : { ...answers[0].video };
  // The first act may repair shared metadata (title, thumbnail or lexicon), while approved
  // production identity/runtime remain authoritative. Later acts never replace metadata.
  const cast = new Map((existingVideo?.characters ?? []).map((character) => [character.id, character]));
  for (const answer of answers) for (const character of answer.video.characters ?? []) {
    if (object(character) && typeof character.id === "string" && !cast.has(character.id)) cast.set(character.id, character);
  }
  if (cast.size) metadata.characters = [...cast.values()].sort((a, b) => a.id.localeCompare(b.id));
  if (existingVideo) for (const key of ["schema_version", "slug", "format", "category", "target_minutes", "production_policy", "runtime_spec", "series"]) {
    if (Object.hasOwn(existingVideo, key)) metadata[key] = existingVideo[key];
    else delete metadata[key];
  }
  return { video: { ...metadata, scenes }, edits: answers.flatMap((answer) => answer.edits ?? []), lexicon_additions: Object.assign({}, ...answers.map((answer) => object(answer.lexicon_additions) ? answer.lexicon_additions : {})), claims: answers.map((answer) => answer.claims).filter((claim) => typeof claim === "string").join("\n") };
}

/** stage(payload, maxTokens) is injectable; this module never calls a provider directly. */
export async function writeAnimeActs({ workdir, source, stage, freshIds, existingVideo = null, operation = "write" }) {
  requireAnimePolicy(source.series ?? source);
  const boundSource = { ...source };
  delete boundSource.today; // Wall-clock rollover cannot discard committed fictional acts.
  const source_hash = animeSourceHash({ source: boundSource, existingVideo, operation });
  const dir = path.join(workdir, "anime-acts", source_hash);
  mkdirSync(dir, { recursive: true });
  const file = path.join(dir, "plan.json");
  let plan;
  if (existsSync(file)) {
    plan = load(file);
    if (plan.schema_version !== 1 || plan.source_hash !== source_hash || plan.operation !== operation || !Array.isArray(plan.acts) || plan.plan_hash !== animeSourceHash(plan.acts)) fail("anime act checkpoint does not match its source or plan");
  } else {
    const taken = new Set((existingVideo?.scenes ?? []).flatMap((scene) => (scene.lines ?? []).map((line) => line.id)));
    const acts = animeActPlan(source, existingVideo).map((act) => {
      const count = Math.ceil(act.target_seconds / 3) + 20;
      const newIds = allocatedIds(freshIds(count, taken), count, taken);
      return { ...act, line_ids: [...act.scenes.flatMap((scene) => (scene.lines ?? []).map((line) => line.id)), ...newIds] };
    });
    plan = { schema_version: 1, source_hash, operation, acts, plan_hash: animeSourceHash(acts) };
    save(file, plan);
  }
  const expected = animeActPlan(source, existingVideo);
  if (plan.acts.length !== expected.length || plan.acts.some((act, index) => animeSourceHash({ ...act, line_ids: undefined }) !== animeSourceHash({ ...expected[index], line_ids: undefined }))) fail("anime act checkpoint assignments have drifted");
  const allocated = plan.acts.flatMap((act) => act.line_ids);
  if (new Set(allocated).size !== allocated.length || allocated.some((id) => !LINE_ID.test(id))) fail("anime act checkpoint has duplicate or invalid line ids");
  const answers = [];
  for (const act of plan.acts) {
    const checkpoint = path.join(dir, `${act.id}.json`);
    let answer;
    if (existsSync(checkpoint)) {
      const stored = load(checkpoint);
      if (stored.source_hash !== source_hash || stored.plan_hash !== plan.plan_hash || stored.answer_hash !== animeSourceHash(stored.answer)) fail(`${act.id}: corrupt or stale checkpoint`);
      answer = stored.answer;
    } else {
      const { scenes, ...details } = act;
      const previous = answers.map((item) => ({ act_id: item.act_id, last_scene: item.video.scenes.at(-1) }));
      answer = await stage({ ...source, act: details, line_ids: act.line_ids, ...(existingVideo ? { video: { ...existingVideo, scenes } } : {}), completed_acts: previous, source_hash }, ANIME_ACT_OUTPUT_TOKENS);
      const problem = animeActProblem(answer, act, { fresh: !existingVideo });
      if (problem) fail(problem);
      save(checkpoint, { source_hash, plan_hash: plan.plan_hash, answer_hash: animeSourceHash(answer), answer });
    }
    const problem = animeActProblem(answer, act, { fresh: !existingVideo });
    if (problem) fail(problem);
    answers.push(answer);
  }
  return mergeAnimeActs(plan.acts, answers, existingVideo);
}
