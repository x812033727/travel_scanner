import test from "node:test";
import assert from "node:assert/strict";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { readFileSync } from "node:fs";
import { designHash, designProblems, productionForEpisode, productionNarrator } from "./design.mjs";
import { buildBundle, loadDesigns } from "./cli.mjs";
import { storyboardHtml } from "./preview.mjs";
import { planRequests } from "../tts/requests.mjs";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
const { works, profile } = await loadDesigns(root);
const first = works[0];

test("ten source-bound plans cover all 400 episode contracts without granting media approval", () => {
  assert.equal(works.length, 10);
  assert.equal(works.reduce((sum, work) => sum + work.design.episodes.length, 0), 400);
  for (const work of works) assert.deepEqual(designProblems(work.design, work.source, profile), [], work.slug);
});

test("stale story revisions, missing episodes and mismatched cast cannot become review bundles", () => {
  const source = structuredClone(first.source);
  source.series.premise += " changed";
  assert.ok(designProblems(first.design, source, profile).some((error) => error.includes("source revision")));
  const missing = structuredClone(first.design);
  missing.episodes.pop();
  assert.ok(designProblems(missing, first.source, profile).some((error) => error.includes("every episode")));
  const cast = structuredClone(first.design);
  cast.episodes[0].characters = null;
  assert.ok(designProblems(cast, first.source, profile).some((error) => error.includes("cast")));
});

test("subtitle burning, premature localization, still delivery and a long opening shot are rejected", () => {
  for (const mutate of [
    (p) => { p.subtitles.burn_in = true; },
    (p) => { p.phases.localization.automatic_generation_now = true; },
    (p) => { p.visual_tier = "stills"; },
    (p) => { p.video.model = "veo-3.1-lite-generate-001"; },
  ]) {
    const invalid = structuredClone(profile);
    mutate(invalid);
    assert.ok(designProblems(first.design, first.source, invalid).length);
  }
  const opening = structuredClone(first.design);
  opening.opening_30s[0].out_s = 9;
  assert.ok(designProblems(opening, first.source, profile).some((error) => error.includes("eight seconds")));
});

test("malformed director, audio or look data produces lint errors before emitting rejected API data", () => {
  for (const mutate of [
    (d) => { d.characters[0].look_states[0].id = ["base"]; },
    (d) => { d.episodes[0] = null; },
    (d) => { d.opening_30s[0] = null; },
    (d) => { delete d.visual_direction; },
    (d) => { delete d.audio_plan; },
    (d) => { d.characters[0].look_states[0] = null; },
  ]) {
    const invalid = structuredClone(first.design);
    mutate(invalid);
    assert.ok(designProblems(invalid, first.source, profile).length);
  }
});

test("chosen voices belong to the API catalog and each narrator stays distinct from the cast", () => {
  const python = readFileSync(path.join(root, "apps/api/app/video_speech/gemini.py"), "utf8");
  const known = new Set([...python.split("PREBUILT_VOICES = (")[1].split(")")[0].matchAll(/"([A-Za-z]+)"/g)].map((match) => match[1]));
  for (const work of works) {
    const narrator = productionNarrator(work.source.setting, work.design);
    assert.ok(known.has(narrator.voice_name));
    assert.ok(work.design.characters.every((entry) => known.has(entry.voice_name)));
    assert.ok(!work.design.characters.some((entry) => entry.voice_name === narrator.voice_name));
  }
  const unknown = structuredClone(first.design);
  unknown.characters[0].voice_name = "invented";
  assert.ok(designProblems(unknown, first.source, profile).some((error) => error.includes("supported selected voice")));
});

test("review overlays preserve story chapters, historical artifacts and complete appearance catalogs", () => {
  for (const work of works) {
    const before = designHash(work.source);
    const original = JSON.parse(work.files["documents.json"]);
    const { bundle, request, manifest } = buildBundle(work, profile);
    assert.equal(bundle.documents.length, 6);
    assert.deepEqual(bundle.documents.slice(1), original.documents.slice(1));
    assert.equal(designHash(work.source), before);
    assert.equal(request.visual_tier, "clips");
    assert.equal(manifest.approval_granted, false);
    assert.equal(manifest.generation_performed, false);
    const setting = bundle.documents[0].body_json;
    for (const character of setting.characters) {
      const direction = work.design.characters.find((entry) => entry.id === character.id);
      assert.equal(character.voice.name, direction.voice_name);
      assert.match(character.voice.style, /^台灣國語/);
      assert.deepEqual(character.shot_looks, direction.look_states.map(({ id, appearance }) => ({ id, appearance })));
    }
    const later = productionForEpisode(setting, 40);
    assert.equal(later.episode.episode, 40);
    assert.deepEqual(later.opening_30s, []);
    assert.equal(later.narrator.voice_name, setting.production_design.narrator.voice_name);
    assert.equal(later.characters.length, work.design.episodes.at(-1).characters.length);
  }
});

test("dialogue requests use the fixed actor voices, while shot appearance changes need no new voice", () => {
  const { bundle } = buildBundle(first, profile);
  const characters = bundle.documents[0].body_json.characters;
  const actor = characters[0];
  const doc = { format: "drama", voice: { provider: "gemini", name: "Schedar" }, characters,
    scenes: [{ id: "speech", lines: [
      { id: "one", speaker: actor.id, text: "我聽清楚了。", pause_after_ms: 0 },
      { id: "two", speaker: characters[1].id, text: "把話說完。", pause_after_ms: 0 },
    ] }] };
  const requests = planRequests(doc, {});
  assert.equal(requests[0].body.voice, `gemini:${actor.voice.name}`);
  assert.equal(requests[1].body.voice, `gemini:${characters[1].voice.name}`);
  const changed = structuredClone(doc);
  changed.characters[0].shot_looks[0].appearance += " alternate coat";
  assert.deepEqual(planRequests(changed, {}), requests);
});

test("backend-readable appendices carry sound and CC direction, with episode-specific voice-state handoff", () => {
  for (const work of works) {
    const { bundle } = buildBundle(work, profile);
    const setting = bundle.documents[0];
    const episode = work.design.episodes[0];
    assert.ok(setting.body_md.includes(episode.hero_shot.sound));
    assert.ok(setting.body_md.includes(episode.voice_notes[0]));
    assert.ok(setting.body_md.includes(episode.cc_notes[0]));
    const production = productionForEpisode(setting.body_json, 1);
    assert.deepEqual(production.pronunciation_hints, setting.body_json.lexicon);
    assert.ok(production.tts_instructions.some((entry) => entry.includes("audio_ref")));
    for (const character of production.characters) {
      assert.ok((character.performance_states ?? []).every((state) => state.episodes.includes(1)));
    }
    assert.ok((production.audio_plan.audio_cues ?? []).every((cue) => cue.episodes.includes(1)));
  }
});

test("the local storyboard protects source text in both markup and embedded JSON", () => {
  const injected = structuredClone(first);
  injected.source.series.title = '</script><img src=x onerror="bad()">';
  const html = storyboardHtml([injected], profile);
  assert.ok(!html.includes(injected.source.series.title));
  assert.match(html, /&lt;\/script&gt;/);
  const script = html.match(/<script>([\s\S]*)<\/script>/)[1];
  assert.doesNotThrow(() => new Function(script));
  assert.ok(!html.includes("https://"), "the viewer must load without external network dependencies");
});
