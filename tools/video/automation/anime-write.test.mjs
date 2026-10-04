import assert from "node:assert/strict";
import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { dramaFixture, tempDir } from "../core/fixtures/load.mjs";
import { animeActPlan, animeActProblem, animeSourceHash, mergeAnimeActs, writeAnimeActs } from "./anime-write.mjs";

const SERIES = { slug: "borrowed-dawn", kind: "series", genre: "custom", lead: "ensemble", category: "anime", style_preset: "anime-2d", target_minutes: 22, planned_episodes: 120, open_ended: false, hands_off: false, compilation: false, production_policy: "long-anime-v1", runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 } };
const source = () => ({ series: structuredClone(SERIES), beats: { hook: "原作鉤子", consequence: "不可抹掉的代價", state: { knowledge: "不知道答案" } } });
const directory = () => tempDir("anime-acts-test-");
function ids() { let count = 0; return (size, taken = new Set()) => { const result = []; while (result.length < size) { const id = (++count).toString(36).padStart(6, "0"); if (!taken.has(id)) result.push(id); } return result; }; }
function answer(payload) {
  const scene = { id: `${payload.act.scene_prefix}shot`, chapter: "故事", template: "shot", data: { prompt: "A girl pulls a bronze lever beside a broken pipe", camera: "medium", motion: "the girl pulls the lever", characters: [] }, lines: [{ id: payload.line_ids[0], text: "村爐還在漏氣。", speaker: "narrator" }] };
  return { act_id: payload.act.id, video: { ...dramaFixture(), scenes: [scene] } };
}

test("long anime uses at least four bounded acts and cannot activate from anime style alone", () => {
  const plan = animeActPlan(source());
  assert.equal(plan.length, 5);
  assert.equal(plan.reduce((sum, act) => sum + act.target_seconds, 0), 1320);
  assert.ok(plan.every((act) => act.target_seconds <= 300));
  const short = source(); short.series.runtime_spec = { body_target_seconds: 540, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1020, slot_reserve_seconds: 300 }; short.series.target_minutes = 9;
  assert.equal(animeActPlan(short).length, 4);
  const implicit = source(); delete implicit.series.production_policy; delete implicit.series.runtime_spec;
  assert.throws(() => animeActPlan(implicit), /production_policy/);
  const invalid = source(); invalid.series.runtime_spec.slot_reserve_seconds = 301;
  assert.throws(() => animeActPlan(invalid), /sum exactly/);
});

test("completed acts survive interruption and replay makes no calls for committed results", async () => {
  const workdir = directory();
  const freshIds = ids();
  const requests = [];
  let interrupted = false;
  const stage = async (payload, max) => {
    requests.push(payload.act.id); assert.equal(max, 32000);
    assert.equal(payload.beats.consequence, "不可抹掉的代價");
    assert.ok(payload.line_ids.length >= 100, "capacity is allocated per act, not one 140-id whole-script pool");
    if (payload.act.index === 2 && !interrupted) { interrupted = true; throw new Error("provider unavailable"); }
    return answer(payload);
  };
  await assert.rejects(writeAnimeActs({ workdir, source: source(), stage, freshIds }), /provider unavailable/);
  const result = await writeAnimeActs({ workdir, source: source(), stage, freshIds: () => { throw new Error("resume must reuse durable allocated ids"); } });
  assert.equal(result.video.scenes.length, 5);
  assert.deepEqual(requests, ["act-01", "act-02", "act-02", "act-03", "act-04", "act-05"]);
  const replay = await writeAnimeActs({ workdir, source: { ...source(), today: "2026-10-03" }, stage: () => { throw new Error("completed replay cannot call provider"); }, freshIds });
  assert.deepEqual(replay, result);
});

test("source/runtime/operation changes cannot reuse prior acts; source hash is canonical", async () => {
  const workdir = directory(); let calls = 0; const freshIds = ids();
  const stage = async (payload) => { calls++; return answer(payload); };
  await writeAnimeActs({ workdir, source: source(), stage, freshIds });
  const changed = source(); changed.beats.state.knowledge = "學到新的事實";
  await writeAnimeActs({ workdir, source: changed, stage, freshIds });
  await writeAnimeActs({ workdir, source: changed, stage, freshIds, operation: "repair" });
  assert.equal(calls, 15);
  assert.equal(animeSourceHash({ a: 1, b: [2, 3] }), animeSourceHash({ b: [2, 3], a: 1 }));
});

test("a corrupt checkpoint is rejected before any new provider call", async () => {
  const workdir = directory(); const freshIds = ids();
  await writeAnimeActs({ workdir, source: source(), stage: async (payload) => answer(payload), freshIds });
  const subdir = path.join(workdir, "anime-acts", readdirSync(path.join(workdir, "anime-acts"))[0]);
  const file = path.join(subdir, "act-03.json"); const saved = JSON.parse(readFileSync(file, "utf8")); saved.answer.video.scenes[0].lines[0].text = "漂移"; writeFileSync(file, JSON.stringify(saved));
  await assert.rejects(writeAnimeActs({ workdir, source: source(), stage: () => { throw new Error("no call allowed"); }, freshIds }), /corrupt or stale checkpoint/);
});

test("act and final merge reject missing/duplicate acts, foreign scenes and duplicate line ids", () => {
  const plan = animeActPlan(source()).map((act, index) => ({ ...act, line_ids: [String(index + 1).padStart(6, "0")] }));
  const answers = plan.map((act) => answer({ act, line_ids: act.line_ids }));
  assert.equal(mergeAnimeActs(plan, answers).video.scenes.length, 5);
  assert.throws(() => mergeAnimeActs(plan, answers.slice(1)), /each planned act/);
  const duplicate = structuredClone(answers); duplicate[1].act_id = duplicate[0].act_id;
  assert.throws(() => mergeAnimeActs(plan, duplicate), /each planned act/);
  const foreign = structuredClone(answers[0]); foreign.video.scenes[0].id = "a02-shot";
  assert.match(animeActProblem(foreign, plan[0], { fresh: true }), /belongs to another act/);
  const duplicateLine = structuredClone(answers[0]); duplicateLine.video.scenes[0].lines.push(duplicateLine.video.scenes[0].lines[0]);
  assert.match(animeActProblem(duplicateLine, plan[0]), /duplicate or foreign line id/);
});

test("repairs send only their act's scenes and merge preserves authoritative metadata", async () => {
  const video = dramaFixture();
  video.scenes = Array.from({ length: 10 }, (_, index) => ({ ...video.scenes[1], id: `existing-${index}`, lines: [{ ...video.scenes[1].lines[0], id: index.toString(36).padStart(6, "0") }] }));
  const seen = [];
  const result = await writeAnimeActs({ workdir: directory(), source: source(), existingVideo: video, operation: "owner-repair", freshIds: ids(), stage: async (payload) => {
    seen.push(...payload.video.scenes.map((scene) => scene.id));
    assert.ok(payload.video.scenes.length <= 2);
    assert.equal(payload.act.count, 5);
    return { act_id: payload.act.id, video: { ...payload.video, category: "other", scenes: payload.video.scenes } };
  } });
  assert.deepEqual(seen, video.scenes.map((scene) => scene.id));
  assert.deepEqual(result.video, video, "act models cannot replace whole-video authority or unscoped scenes");
});


test("bounded repairs can fix shared first-act metadata without changing production authority", () => {
  const video = { ...dramaFixture(), category: "anime", target_minutes: [22, 22], production_policy: SERIES.production_policy, runtime_spec: SERIES.runtime_spec, series: { slug: SERIES.slug, episode: 1, chapter: 1 } };
  const plan = animeActPlan(source()).map((act, index) => ({ ...act, line_ids: [String(index + 1).padStart(6, "0")] }));
  const answers = plan.map((act) => answer({ act, line_ids: act.line_ids }));
  answers[0].video.youtube.title = "修復後的標題";
  answers[0].video.runtime_spec = {};
  answers[1].video.youtube.title = "後幕無權替換";
  const merged = mergeAnimeActs(plan, answers, video).video;
  assert.equal(merged.youtube.title, "修復後的標題");
  assert.deepEqual(merged.runtime_spec, SERIES.runtime_spec);
  assert.deepEqual(merged.target_minutes, [22, 22]);
  assert.equal(merged.category, "anime");
});
