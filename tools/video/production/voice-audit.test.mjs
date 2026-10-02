import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { loadDesigns } from "./cli.mjs";
import { buildAuditionPlan, CALIBRATION_SAMPLES } from "./voice-audit.mjs";
import { designHash, productionSetting } from "./design.mjs";
import { castFrom } from "../automation/series.mjs";
import { voiceFor } from "../core/drama.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
const { works, profile } = await loadDesigns(root);
const named = (slug) => works.find((work) => work.slug === slug);
const needles = named("three-needles");
const reload = named("reload-first-day");
const resolved = (work) => productionSetting(JSON.parse(work.files["documents.json"]).documents.find((document) => document.kind === "setting"), work.design, profile).body_json;

test("all ten audition plans preserve calibration, source bindings and not-synthesized boundaries without mutation", () => {
  for (const work of works) {
    const before = designHash(work);
    const plan = buildAuditionPlan(work, profile);
    assert.equal(designHash(work), before);
    assert.equal(plan.status, "samples-prepared-not-synthesized");
    assert.equal(plan.generation_performed, false);
    assert.equal(plan.audition_performed, false);
    assert.equal(plan.approval_granted, false);
    for (const id of [...work.design.characters.map((character) => character.id), "narrator"]) {
      for (const sample of CALIBRATION_SAMPLES) {
        const entry = plan.entries.find((entry) => entry.id === `${id}-${sample.id}`);
        assert.ok(entry, `${work.slug}/${id}/${sample.id}`);
        assert.equal(entry.delivery_scope, "offscreen-calibration-not-story");
        assert.ok(entry.audition_style.includes(sample.direction));
      }
    }
    for (const entry of [...plan.entries, ...plan.scenes, ...plan.cues]) {
      assert.equal(entry.status, "not-synthesized");
      assert.equal(entry.source_binding.source_sha256, designHash(work.source));
      assert.ok(entry.source_refs.length);
    }
  }
});

test("each distinct credited episode voice state uses the same resolved cast as production", () => {
  for (const work of works) {
    const plan = buildAuditionPlan(work, profile);
    const setting = resolved(work);
    for (const episode of work.source.chapters.flatMap((chapter) => chapter.episodes)) {
      for (const actor of castFrom(setting, episode.number).filter((actor) => episode.characters.includes(actor.id))) {
        const entries = plan.entries.filter((entry) => entry.kind === "effective-voice-state" && entry.character === actor.id && entry.episodes.includes(episode.number));
        assert.equal(entries.length, 1);
        assert.equal(entries[0].voice, actor.voice.name);
        assert.equal(entries[0].effective_style, actor.voice.style ?? "");
      }
    }
  }
  const suxing = buildAuditionPlan(reload, profile).entries.filter((entry) => entry.kind === "effective-voice-state" && entry.character === "suxing");
  assert.ok(suxing.length >= 2, "source own-voice override must not disappear into base calibration");
  assert.notEqual(suxing.find((entry) => entry.episodes.includes(35)).effective_style, suxing.find((entry) => entry.episodes.includes(38)).effective_style);
});

test("canonical aliases and clue terms have independent pronunciation samples instead of relying on selected story lines", () => {
  for (const [slug, term] of [["three-needles", "安歲散"], ["before-the-hammer", "青釐盞"], ["reload-first-day", "阿嬤"]]) {
    const work = named(slug);
    const entry = buildAuditionPlan(work, profile).entries.find((entry) => entry.kind === "pronunciation-term" && entry.transcript.trim() === `${term}。`);
    assert.ok(entry, `${slug}/${term}`);
    assert.equal(entry.character, "narrator");
    assert.ok(entry.audition_style.includes(resolved(work).lexicon[term]));
    assert.equal(entry.delivery_scope, "offscreen-calibration-not-story");
    assert.equal(entry.status, "not-synthesized");
  }
});

test("audition request style includes only matched pronunciation plus this sample's direction", () => {
  const plan = buildAuditionPlan(needles, profile);
  const entry = plan.entries.find((entry) => entry.id === "yiwei-name");
  const setting = resolved(needles);
  const actor = castFrom(setting).find((actor) => actor.id === "yiwei");
  const voice = voiceFor({ pronunciation_hints: setting.lexicon, characters: [actor], voice: actor.voice },
    { id: entry.id, speaker: actor.id, text: entry.transcript.trim(), emotion: entry.direction });
  assert.equal(entry.audition_style, voice.style);
  assert.match(entry.audition_style, /ㄨㄟˊ/);
  const a = plan.entries.find((entry) => entry.id === "yiwei-controlled");
  const b = plan.entries.find((entry) => entry.id === "yiwei-quiet");
  assert.notEqual(a.audition_style, b.audition_style);
  assert.equal(a.effective_style, b.effective_style);
  assert.ok(plan.entries.filter((entry) => entry.character === "narrator").every((entry) => /台灣國語/.test(entry.effective_style)));
});

test("every proposed acting state gets a separate sample, while silent writing never becomes invented TTS", () => {
  const plan = buildAuditionPlan(needles, profile);
  const silent = plan.entries.find((entry) => entry.id === "heting-performance-silent-writing");
  assert.equal(silent.kind, "nonverbal-performance-check");
  assert.equal(silent.transcript, null);
  assert.equal(silent.synthesis_allowed, false);
  assert.equal(silent.audition_style, null);
  for (const work of works) {
    const entries = buildAuditionPlan(work, profile).entries;
    for (const character of work.design.characters) for (const state of character.performance_states ?? []) {
      const entry = entries.find((entry) => entry.id === `${character.id}-performance-${state.id}`);
      assert.ok(entry, `${work.slug}/${state.id}`);
      assert.equal(entry.context.performance_state.id, state.id);
      if (state.speech_mode !== "nonverbal") assert.ok(entry.audition_style.includes(state.cue));
    }
  }
});

test("Codex acting samples use the performance direction after the prose guard", () => {
  const work = named("wedding-reckoning");
  const actor = work.design.characters.find((entry) => entry.id === "zhixia");
  const state = actor.performance_states.find((entry) => entry.id === "zhixia-smoke-radio");
  const entry = buildAuditionPlan(work, profile).entries.find((entry) => entry.id === `zhixia-performance-${state.id}`);
  assert.ok(entry.audition_style.includes("咳聲放句外"));
  assert.ok(!entry.direction.includes("source_excerpt"));
  assert.equal(entry.context.performance_state.instructions[0], state.instructions[0]);
});

test("story excerpts are explicit verbatim attributed samples, never prose, palm writing or automatic narrator lines", () => {
  const plan = buildAuditionPlan(needles, profile);
  const scene = plan.scenes.find((scene) => scene.id === "two-speaking-elders");
  assert.ok(scene.voices.some((voice) => voice.character === "heting"));
  assert.ok(scene.entry_ids.every((id) => plan.entries.find((entry) => entry.id === id).character !== "heting"));
  assert.ok(plan.entries.filter((entry) => entry.kind === "story-excerpt").every((entry) => entry.character !== "narrator"));
  const contextOnly = structuredClone(needles);
  delete contextOnly.design.audio_plan.audition_scenes[0].line_samples;
  const contextScene = buildAuditionPlan(contextOnly, profile).scenes[0];
  assert.equal(contextScene.material_kind, "context-only-no-story-transcript");
  assert.deepEqual(contextScene.entry_ids, []);
});

test("stale source, uncredited speaker, invented dialogue and narrator misattribution fail closed", () => {
  const stale = structuredClone(needles);
  stale.source.series.title += " changed";
  assert.throws(() => buildAuditionPlan(stale, profile), /source binding/);
  for (const mutate of [
    (scene) => { scene.line_samples[0].text = "這句原作不存在。"; },
    (scene) => { scene.line_samples[0].speaker = "narrator"; },
    (scene) => { scene.line_samples[0].source_kind = "message-read"; },
    (scene) => { scene.speaker_ids.push("not-in-this-story"); },
  ]) {
    const invalid = structuredClone(needles);
    mutate(invalid.design.audio_plan.audition_scenes[0]);
    assert.throws(() => buildAuditionPlan(invalid, profile));
  }
});

test("overlong directions reject instead of silently dropping acting or required readings", () => {
  const invalid = structuredClone(needles);
  invalid.design.characters[0].performance = "聲".repeat(400);
  assert.throws(() => buildAuditionPlan(invalid, profile), /400 characters/);
});
