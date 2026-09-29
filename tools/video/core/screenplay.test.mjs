import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { dramaFixture, fixtureLexicon, sandbox } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";
import { validateVideo } from "./schema.mjs";
import { narrativeHash, screenplay, scriptScenes, writeScreenplay } from "./screenplay.mjs";
import { loadProject, pipelineStatus } from "./state.mjs";

const episode = () => ({ ...dramaFixture(), series: { slug: "xianxia", episode: 3, chapter: 1 } });

test("the screenplay hash follows the narrative, not the shot prompts", () => {
  const doc = episode();
  const before = narrativeHash(doc);
  const shot = doc.scenes.find((scene) => scene.template === "shot");
  shot.data.prompt = `${shot.data.prompt} at dusk`;
  assert.equal(narrativeHash(doc), before, "a prompt fix leaves an approved script approved");
  assert.equal(screenplay(doc), screenplay(episode()), "and the file the gate is bound to");
  shot.lines[0].text = `${shot.lines[0].text}！`;
  assert.notEqual(narrativeHash(doc), before, "a changed line needs a new reading");
  const spoken = episode();
  spoken.scenes.find((scene) => scene.template === "shot").lines[0].emotion = "冷靜";
  assert.notEqual(narrativeHash(spoken), before, "so does a changed emotion");
  for (const field of ["say", "pause_after_ms"]) {
    const timed = episode();
    const line = timed.scenes[0].lines[0];
    line[field] = field === "say" ? "她已改變了選擇。" : 900;
    assert.notEqual(screenplay(timed), screenplay(episode()), "spoken words and timing need renewed approval too");
  }
});

test("the screenplay names every speaker and never a prompt; the review scenes carry the prompts", () => {
  const doc = episode();
  const text = screenplay(doc);
  assert.match(text, /^# /);
  assert.match(text, /作品 xianxia · 第 3 集（第 1 篇）/);
  assert.match(text, /## 角色/);
  assert.match(text, /【精衛】/);
  assert.match(text, /旁白：/);
  for (const scene of doc.scenes) if (scene.template === "shot") assert.ok(!text.includes(scene.data.prompt), "prompts stay out of the file");
  const scenes = scriptScenes(doc);
  assert.equal(scenes.length, doc.scenes.length);
  const shot = scenes.find((scene) => scene.prompt);
  assert.ok(shot && shot.lines.every((line) => typeof line.speaker === "string"));
  assert.ok(scenes.some((scene) => scene.lines.some((line) => line.name === "精衛")));
});

test("an episode names its series, lists its cast in order, and matches the setting book", () => {
  const doc = episode();
  assert.deepEqual(validateVideo(doc), []);
  const wrong = { ...doc, series: { slug: "Bad Slug", episode: 0, chapter: 1, extra: true } };
  const problems = validateVideo(wrong).map((problem) => problem.path);
  assert.ok(problems.includes("series.slug") && problems.includes("series.episode") && problems.includes("series.extra"));
  const slides = { ...doc, format: "slides" };
  delete slides.characters;
  delete slides.look;
  assert.ok(validateVideo(slides).some((problem) => problem.path === "series"), "only a drama has a series");
  const unsorted = { ...doc, characters: [...doc.characters].reverse() };
  assert.ok(validateVideo(unsorted).some((problem) => problem.path === "characters"), "the cast is listed by id");
  assert.deepEqual(validateVideo({ ...doc, characters: [...doc.characters].sort((a, b) => (a.id < b.id ? -1 : 1)) }), []);

  const sorted = { ...doc, characters: [...doc.characters].sort((a, b) => (a.id < b.id ? -1 : 1)) };
  const context = { brief: undefined, lexicon: fixtureLexicon() };
  const nothing = lintVideo(sorted, { ...context, series: null });
  assert.ok(nothing.warnings.some((warning) => warning.path === "series"), "no series.json yet is a warning");
  const book = { slug: "xianxia", episode: 3, characters: sorted.characters.map((character) => ({ ...character })) };
  assert.equal(lintVideo(sorted, { ...context, series: book }).errors.filter((error) => error.path.startsWith("characters")).length, 0);
  const drifted = { ...book, characters: book.characters.map((character, index) => (index === 0 ? { ...character, appearance: `${character.appearance}, taller` } : character)) };
  assert.ok(lintVideo(sorted, { ...context, series: drifted }).errors.some((error) => error.path === "characters[0].appearance"));
  const stranger = { ...book, characters: book.characters.slice(1) };
  assert.ok(lintVideo(sorted, { ...context, series: stranger }).errors.some((error) => error.path === "characters[0]"));
  const other = { ...book, episode: 4 };
  assert.ok(lintVideo(sorted, { ...context, series: other }).errors.some((error) => error.path === "series"));
});

test("a series episode's status waits for the script gate between the check and the sheets", async () => {
  const box = sandbox("fixture-drama", "drama");
  const doc = { ...dramaFixture(), series: { slug: "xianxia", episode: 1, chapter: 1 } };
  doc.characters = [...doc.characters].sort((a, b) => (a.id < b.id ? -1 : 1));
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  writeFileSync(path.join(box.dir, "series.json"), JSON.stringify({ slug: "xianxia", episode: 1, characters: doc.characters, beats: { hook: "h" } }));
  mkdirSync(box.workdir, { recursive: true });
  const status = () => pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.ok((await status()).steps.some((step) => step.id === "script approved"));
  const { approve } = await import("./approvals.mjs");
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir });
  writeFileSync(path.join(box.dir, "verify-1.md"), "# ok\n");
  const waiting = await status();
  assert.equal(waiting.next.id, "script approved");
  assert.match(waiting.next.todo, /script --slug/);
  const project = loadProject({ slug: box.slug, root: box.root });
  assert.equal(project.series.beats.hook, "h");
  const file = writeScreenplay(box.dir, project.doc);
  assert.equal(readFileSync(file, "utf8"), screenplay(project.doc));
  assert.equal((await status()).next.id, "script approved", "written, not yet approved");
  await approve({ gate: "script", docDir: box.dir, workdir: box.workdir });
  assert.equal((await status()).next.id, "look generated");
  const shot = project.doc.scenes.find((scene) => scene.template === "shot");
  shot.data.prompt = `${shot.data.prompt}, moonlight`;
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(project.doc));
  writeScreenplay(box.dir, project.doc);
  assert.equal((await status()).next.id, "look generated", "a prompt fix keeps the approval");
  shot.lines[0].pause_after_ms = 900;
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(project.doc));
  writeScreenplay(box.dir, project.doc);
  assert.equal((await status()).next.id, "script approved", "new timing cannot reuse the previous script approval after rechecking");
});
