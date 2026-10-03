import assert from "node:assert/strict";
import test from "node:test";
import { hasAnimePolicy, isClosedAnimeFinale, isLongAnime, LONG_ANIME_POLICY, runtimePolicyHash, validateAnimePolicy, validateAnimeRuntime } from "./anime-policy.mjs";

const runtime = () => ({ body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 });
const series = () => ({ production_policy: LONG_ANIME_POLICY, runtime_spec: runtime(), kind: "series", category: "anime", style_preset: "anime-2d", genre: "custom", lead: "ensemble", target_minutes: 22, planned_episodes: 120, open_ended: false });
const video = () => ({ production_policy: LONG_ANIME_POLICY, runtime_spec: runtime(), format: "drama", category: "anime", look: { preset: "anime-2d" }, target_minutes: [22, 22], series: { kind: "series", genre: "custom", lead: "ensemble", planned_episodes: 120, open_ended: false } });

test("explicit long-anime series and its video projection preserve the 22/3/5/30-minute specification", () => {
  assert.deepEqual(validateAnimePolicy(series()), []);
  assert.deepEqual(validateAnimePolicy(video()), []);
  assert.equal(isLongAnime(series()), true);
  assert.equal(runtimePolicyHash(series()), runtimePolicyHash(video()), "the series and episode use the same policy receipt");
  assert.deepEqual(validateAnimePolicy({ category: "anime", style_preset: "anime-2d", target_minutes: 3 }), []);
  assert.equal(hasAnimePolicy({ production_policy: null, runtime_spec: null }), false);
  assert.equal(runtimePolicyHash({ category: "anime" }), null);
});

test("a partial, unknown or malformed policy fails closed rather than using a short-drama fallback", () => {
  for (const change of [
    { production_policy: undefined }, { production_policy: "long-anime-v2" }, { production_policy: false }, { runtime_spec: undefined },
    { category: "story" }, { kind: "story" }, { style_preset: "flat-explainer" }, { genre: "xianxia-bonds" }, { lead: "male" },
    { target_minutes: 3 }, { compilation: true },
  ]) assert.ok(validateAnimePolicy({ ...series(), ...change }).length, JSON.stringify(change));
  for (const change of [{ format: "shorts" }, { target_minutes: [21, 23] }, { series: { kind: "series", genre: "custom" } }]) assert.ok(validateAnimePolicy({ ...video(), ...change }).length);
  assert.throws(() => runtimePolicyHash({ ...series(), runtime_spec: null }), RangeError);
});

test("runtime integers, whole-minute bounds and the exact slot budget are validated without coercion", () => {
  for (const minutes of [9, 22, 30]) assert.deepEqual(validateAnimeRuntime({ ...runtime(), body_target_seconds: minutes * 60, broadcast_slot_seconds: minutes * 60 + 480 }), []);
  for (const body of [480, 1860, 1320.5, "1320", true, Infinity, NaN]) assert.ok(validateAnimeRuntime({ ...runtime(), body_target_seconds: body }).length);
  for (const change of [{ op_ed_budget_seconds: -1 }, { op_ed_budget_seconds: 301 }, { slot_reserve_seconds: 901 }, { broadcast_slot_seconds: 3601 }, { broadcast_slot_seconds: 1799 }, { op_ed_budget_seconds: "180" }, { injected: 1 }]) assert.ok(validateAnimeRuntime({ ...runtime(), ...change }).length);
});

test("the policy hash is stable across key order and changes when actual duration requirements change", () => {
  const original = series();
  const reordered = { ...original, runtime_spec: Object.fromEntries(Object.entries(original.runtime_spec).reverse()) };
  assert.equal(runtimePolicyHash(original), runtimePolicyHash(reordered));
  const changed = { ...original, runtime_spec: { ...runtime(), op_ed_budget_seconds: 120, slot_reserve_seconds: 360 } };
  assert.notEqual(runtimePolicyHash(original), runtimePolicyHash(changed));
  for (const context of [{ slug: "another-series" }, { episode: 120 }, { chapter: 10 }, { planned_episodes: 121 }, { open_ended: true }, { closed_ending: true }]) {
    assert.notEqual(runtimePolicyHash({ ...original, ...context }), runtimePolicyHash(original), "a stale series/finale context invalidates duration evidence");
  }
});

test("quiet closure belongs only to the declared last episode of a closed explicit-policy series", () => {
  const closed = { ...series(), episode: 120, closed_ending: true };
  assert.equal(isClosedAnimeFinale(closed), true);
  assert.equal(isClosedAnimeFinale(closed, 120, { closed_ending: true }), true);
  for (const change of [{ episode: 119 }, { open_ended: true }, { planned_episodes: "120" }, { production_policy: undefined }, { closed_ending: false }]) assert.equal(isClosedAnimeFinale({ ...closed, ...change }), false);
  assert.equal(isClosedAnimeFinale(closed, 120, { closed_ending: false }), false);
});
