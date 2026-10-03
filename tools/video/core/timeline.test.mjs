import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "./fixtures/load.mjs";
import { buildCues } from "./captions.mjs";
import { LONG_ANIME_POLICY, runtimePolicyHash } from "./anime-policy.mjs";
import {
  buildTimeline,
  chapterList,
  chapterText,
  checkChapters,
  DEFAULT_PAUSE_MS,
  estimatedSamples,
  estimateTimeline,
  formatClock,
  framesFor,
  msToSamples,
  SAMPLES_PER_FRAME,
  SCENE_GAP_MS,
  speechHash,
  spokenUnits,
  TAIL_MS,
  visualHash,
} from "./timeline.mjs";

test("one frame is exactly 1,600 samples at 48 kHz and 30 fps", () => {
  assert.equal(SAMPLES_PER_FRAME, 1600);
  assert.equal(framesFor(1600), 1);
  assert.equal(framesFor(1601), 2);
});

test("spokenUnits counts a CJK character once and a Latin word or number twice, like video_kit.py", () => {
  assert.equal(spokenUnits("排行榜"), 3);
  assert.equal(spokenUnits("GPT-5 很強"), 4);
  assert.equal(spokenUnits("2026 年，好。"), 4);
});

test("every line starts on a frame and gets its clip plus pause, padded to whole frames", () => {
  const doc = fixture();
  const samples = { k7p2: 100_000, m4qa: 48_001, x9fe: 1, b3tn: 1600, r8wd: 77_777, h2cz: 50_000, p5vs: 60_000 };
  const timeline = buildTimeline(doc, samples);
  let frame = 0;
  for (const line of timeline.lines) {
    assert.equal(line.start_frame, frame);
    const scene = doc.scenes.find((each) => each.id === line.scene);
    const isLast = scene.lines.at(-1).id === line.id;
    const extra = isLast ? (scene === doc.scenes.at(-1) ? TAIL_MS : SCENE_GAP_MS) : 0;
    assert.equal(line.end_frame - line.start_frame, framesFor(samples[line.id] + msToSamples(DEFAULT_PAUSE_MS + extra)));
    frame = line.end_frame;
  }
  assert.equal(timeline.total_frames, frame);
});

test("two thousand lines of arbitrary length accumulate no drift between audio and frames", () => {
  let seed = 7;
  const random = () => (seed = (seed * 48271) % 2147483647) / 2147483647;
  const lines = Array.from({ length: 2000 }, (_, index) => ({ id: `l${String(index).padStart(4, "0")}`, text: "一句話", pause_after_ms: Math.floor(random() * 900) }));
  const doc = { ...fixture(), scenes: [{ id: "all", chapter: "全部", template: "big", data: {}, lines }] };
  const samples = Object.fromEntries(lines.map((line) => [line.id, 1 + Math.floor(random() * 400_000)]));
  const pauses = Object.fromEntries(lines.map((line) => [line.id, line.pause_after_ms]));
  const timeline = buildTimeline(doc, samples);
  // Building narration.wav means: each clip, then silence up to its end frame. The clip of every
  // line must then begin at exactly start_frame * 1600 samples.
  let cursor = 0;
  for (const line of timeline.lines) {
    assert.equal(cursor, line.start_frame * SAMPLES_PER_FRAME);
    const silence = (line.end_frame - line.start_frame) * SAMPLES_PER_FRAME - line.audio_samples;
    assert.ok(silence >= 0 && silence < msToSamples(pauses[line.id] + TAIL_MS) + SAMPLES_PER_FRAME);
    cursor += line.audio_samples + silence;
  }
  assert.equal(cursor, timeline.total_frames * SAMPLES_PER_FRAME);
});

test("reveals become slide states; a reveal on a scene's first line changes the opening state", () => {
  const doc = fixture();
  const timeline = estimateTimeline(doc);
  const bullets = timeline.scenes.find((scene) => scene.id === "questions");
  assert.deepEqual(bullets.states.map((state) => state.reveal), [1, 2, 3]);
  assert.equal(bullets.states[0].start_frame, bullets.start_frame);
  assert.equal(bullets.states.at(-1).end_frame, bullets.end_frame);
  for (let index = 1; index < bullets.states.length; index++) assert.equal(bullets.states[index - 1].end_frame, bullets.states[index].start_frame);
  const hook = timeline.scenes.find((scene) => scene.id === "hook");
  assert.deepEqual(hook.states.map((state) => state.reveal), [0]);
});

test("a line without an audio length is a hard error, not a silent zero", () => {
  const samples = estimatedSamples(fixture());
  delete samples.x9fe;
  assert.throws(() => buildTimeline(fixture(), samples), /no audio length for line x9fe/);
});

test("chapters follow YouTube's rules: at least three, first at 00:00, ten seconds each", () => {
  const timeline = estimateTimeline(fixture());
  assert.deepEqual(checkChapters(timeline), []);
  assert.equal(chapterText(timeline).split("\n")[0], "00:00 開場");
  const two = fixture();
  delete two.scenes[2].chapter;
  assert.match(checkChapters(estimateTimeline(two))[0], /2 chapters/);
  const short = fixture();
  short.scenes[2].lines = [{ id: "zzzz", text: "再見。" }];
  assert.match(checkChapters(estimateTimeline(short)).join("\n"), /chapter "結論" lasts/);
});

test("chapter titles can be swapped for a translation by scene id", () => {
  const titles = chapterList(estimateTimeline(fixture()), { hook: "Intro" }).map((chapter) => chapter.title);
  assert.deepEqual(titles, ["Intro", "三個問題", "結論"]);
});

test("formatClock writes mm:ss, or h:mm:ss past an hour", () => {
  assert.equal(formatClock(0), "00:00");
  assert.equal(formatClock(65.9), "01:05");
  assert.equal(formatClock(3725), "1:02:05");
});

test("speechHash follows the audio's inputs and nothing else", () => {
  const doc = fixture();
  const lexicon = { schema_version: 1, terms: { AI: null } };
  const base = speechHash(doc, lexicon);
  const text = fixture();
  text.scenes[0].lines[0].text = "改一個字。";
  const pause = fixture();
  pause.scenes[0].lines[0].pause_after_ms = 900;
  const voice = fixture();
  voice.voice.name = "zh-TW-YunJheNeural";
  const picture = fixture();
  picture.scenes[0].data.title = "新標題";
  assert.notEqual(speechHash(text, lexicon), base);
  assert.notEqual(speechHash(pause, lexicon), base);
  assert.notEqual(speechHash(voice, lexicon), base);
  assert.notEqual(speechHash(doc, { schema_version: 1, terms: { AI: "A I" } }), base);
  assert.equal(speechHash(picture, lexicon), base);
});

test("a dictionary term no line says leaves speechHash alone; one a line says changes it", () => {
  const doc = fixture();
  const lexicon = { schema_version: 1, terms: { AI: "A I" } };
  const base = speechHash(doc, lexicon);
  // Added for another video: this script never says them.
  assert.equal(speechHash(doc, { schema_version: 1, terms: { ...lexicon.terms, LLM: "L L M", "RTX Spark": "R T X Spark", GB: "G B" } }), base);
  // Inside a longer word it is not a match either, like the speech request.
  const inside = fixture();
  for (const scene of inside.scenes) for (const line of scene.lines) line.text = line.text.replace(/AI/g, "AIs");
  assert.equal(speechHash(inside, lexicon), speechHash(inside, { schema_version: 1, terms: {} }));
  // A line that starts saying one of them changes it.
  const says = fixture();
  says.scenes[0].lines[0].text = "每次有新 LLM 出來，排行榜就換一次第一名。";
  assert.notEqual(speechHash(says, { schema_version: 1, terms: { ...lexicon.terms, LLM: "L L M" } }), speechHash(says, lexicon));
});

test("visualHash follows the pictures' inputs and nothing else", () => {
  const base = visualHash(fixture());
  const picture = fixture();
  picture.scenes[1].data.items[0] = "別的";
  const reveal = fixture();
  delete reveal.scenes[1].lines[2].reveal;
  const text = fixture();
  text.scenes[0].lines[0].text = "改一個字。";
  assert.notEqual(visualHash(picture), base);
  assert.notEqual(visualHash(reveal), base);
  assert.equal(visualHash(text), base);
});

function directedAnime() {
  const shot = (id, seconds) => ({ id, template: "shot", action_seconds: seconds, data: { prompt: "A girl runs across falling stones", motion: "stones break beneath her feet" }, lines: [] });
  return {
    ...fixture(), format: "drama", category: "anime", look: { preset: "anime-2d" }, production_policy: LONG_ANIME_POLICY,
    target_minutes: [22, 22], runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { kind: "series", genre: "custom", lead: "ensemble" },
    scenes: [shot("opening-action", 2), { id: "voice-a", template: "shot", data: {}, lines: [{ id: "a", text: "快抓住我的手。" }] },
      { ...shot("bridge-action", 3), chapter: "崩落的橋" }, { id: "voice-b", template: "shot", data: {}, lines: [{ id: "b", text: "橋要塌下去了。" }] }, shot("closing-action", 1)],
  };
}

test("directed silent action occupies real scene frames and shifts speech, captions and chapters without fake TTS lines", () => {
  const doc = directedAnime();
  const timeline = buildTimeline(doc, { a: 96_000, b: 96_000 });
  assert.equal(timeline.timing_basis, "measured");
  assert.equal(timeline.runtime_policy_hash, runtimePolicyHash(doc));
  assert.deepEqual(timeline.lines.map((line) => [line.id, line.start_frame, line.end_frame]), [["a", 60, 150], ["b", 240, 330]]);
  assert.deepEqual(timeline.actions, [
    { scene: "opening-action", start_frame: 0, end_frame: 60 }, { scene: "bridge-action", start_frame: 150, end_frame: 240 }, { scene: "closing-action", start_frame: 330, end_frame: 360 },
  ]);
  assert.equal(timeline.total_frames, 360);
  assert.equal(timeline.scenes.length, 5);
  assert.ok(timeline.scenes.every((scene) => scene.states[0].start_frame === scene.start_frame && scene.states.at(-1).end_frame === scene.end_frame));
  assert.deepEqual(timeline.chapters, [{ title: "崩落的橋", scene: "bridge-action", start_frame: 150 }]);
  const captions = buildCues(timeline, { a: "快抓住我的手。", b: "橋要塌下去了。" }, "zh-TW").cues;
  assert.deepEqual(captions.map((cue) => [cue.line, cue.start_ms]), [["a", 2000], ["b", 8000]]);
  assert.equal(estimateTimeline(doc).timing_basis, "estimated", "planned action plus estimated words remains an estimate");
});

test("runtime budget changes reuse spoken audio while action timing changes rebuild narration", () => {
  const doc = directedAnime();
  const hash = speechHash(doc, { terms: {} });
  const budget = structuredClone(doc);
  budget.runtime_spec.op_ed_budget_seconds = 120;
  budget.runtime_spec.slot_reserve_seconds = 360;
  assert.equal(speechHash(budget, { terms: {} }), hash);
  assert.notEqual(runtimePolicyHash(budget), runtimePolicyHash(doc));
  const action = structuredClone(doc);
  action.scenes[0].action_seconds += 1;
  assert.notEqual(speechHash(action, { terms: {} }), hash);
  const moved = structuredClone(doc);
  moved.scenes.unshift(moved.scenes.splice(2, 1)[0]);
  assert.notEqual(speechHash(moved, { terms: {} }), hash, "moving the same silent shot changes the actual spoken offsets");
  assert.notEqual(buildTimeline(moved, { a: 96_000, b: 96_000 }).lines[0].start_frame, buildTimeline(doc, { a: 96_000, b: 96_000 }).lines[0].start_frame);
  assert.equal(estimateTimeline(fixture()).timing_basis, undefined, "ordinary timeline format stays unchanged");
});

test("silent action cannot extend an ordinary episode, spoken scene, slide or invalid duration", () => {
  for (const seconds of [0, 9, 1.5, "3"]) {
    const doc = directedAnime();
    doc.scenes[0].action_seconds = seconds;
    assert.throws(() => buildTimeline(doc, { a: 96_000, b: 96_000 }), /silent shot of a long anime or of a drama with a cast, lasting 1 to 8 seconds/);
  }
  for (const mutate of [(doc) => { delete doc.production_policy; delete doc.runtime_spec; }, (doc) => { doc.scenes[0].lines = [{ id: "fake", text: "假的旁白" }]; }, (doc) => { doc.scenes[0].template = "big"; }]) {
    const doc = directedAnime();
    mutate(doc);
    assert.throws(() => buildTimeline(doc, { a: 96_000, b: 96_000 }), /action_seconds/);
  }
});
