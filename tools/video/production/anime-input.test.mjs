import assert from "node:assert/strict";
import fs from "node:fs";
import { readFileSync, mkdtempSync, symlinkSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import { syncBuiltinESMExports } from "node:module";
import { test } from "node:test";
import { buildAnimeProductionInput, FILE_NAMES, main, parseSourceJson, readAnimeSourceFiles, sha256, sourceBundleHash, SOURCE, SOURCE_DIRECTORY, validateAnimeProductionInput, validateAnimeSourceFiles } from "./anime-input.mjs";
import { validateAnimePolicy } from "../core/anime-policy.mjs";
import { documentProblem } from "../automation/series.mjs";

const ROOT = fileURLToPath(new URL("../../../", import.meta.url));
const original = readAnimeSourceFiles();
const clone = () => structuredClone(original);
const updateJson = (files, filename, edit) => {
  const value = JSON.parse(files[filename]);
  edit(value);
  files[filename] = `${JSON.stringify(value, null, 2)}\n`;
};
const refreshReceipt = (files) => {
  updateJson(files, "manifest.json", (manifest) => {
    for (const group of ["source_files", "support_files", "generated_files"]) for (const name of Object.keys(manifest[group])) manifest[group][name] = sha256(files[name]);
  });
};
const temporary = (run) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), "anime-input-"));
  try { return run(directory); } finally { rmSync(directory, { recursive: true, force: true }); }
};

test("actual complete source pack converts to the native 22-minute paused draft", () => {
  const draft = buildAnimeProductionInput(original);
  assert.equal(validateAnimeProductionInput(draft, original), true);
  assert.deepEqual(validateAnimePolicy(draft.series_request), []);
  assert.equal(draft.series_request.slug, "borrowed-dawn-production");
  assert.equal(draft.series_request.kind, "series");
  assert.equal(draft.series_request.category, "anime");
  assert.equal(draft.series_request.style_preset, "anime-2d");
  assert.equal(draft.series_request.genre, "custom");
  assert.equal(draft.series_request.lead, "ensemble");
  assert.equal(draft.series_request.tone, "no-romance");
  assert.equal(draft.series_request.target_minutes, 22);
  assert.equal(draft.series_request.planned_episodes, 120);
  assert.equal(draft.series_request.episodes_per_chapter, 12);
  for (const field of ["open_ended", "hands_off", "compilation"]) assert.equal(draft.series_request[field], false);
  assert.deepEqual(draft.series_request.runtime_spec, { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 });
  assert.equal(draft.series_request.production_policy, "long-anime-v1");
  assert.equal(Object.hasOwn(draft.series_request, "status"), false);
  for (const field of ["planning_only", "planning_spec", "production_support", "runtime", "source_binding"]) assert.equal(Object.hasOwn(draft.series_request, field), false);
  assert.deepEqual(draft.documents, JSON.parse(original["documents.json"]).documents);
  assert.equal(draft.documents.length, 12);
  assert.equal(draft.episodes.length, 120);
  assert.equal(draft.episodes.flatMap((episode) => episode.high_tension).length, 240);
  assert.deepEqual(draft.episodes.map((episode) => episode.number), Array.from({ length: 120 }, (_, i) => i + 1));
  assert.equal(draft.episodes.filter((episode) => episode.closed_ending).length, 1);
  assert.equal(draft.episodes[119].number, 120);
  assert.equal(draft.episodes[119].closed_ending, true);
  assert.equal(draft.episodes[119].tension[4], 2);
  assert.ok(draft.episodes.slice(0, 119).every((episode) => episode.tension[4] >= 4));
  assert.ok(draft.episodes.every((episode) => !Object.hasOwn(episode, "satisfaction")));
  assert.equal(draft.source_metadata.original_tone, JSON.parse(original["plan.json"]).tone);
  assert.deepEqual(draft.source_metadata.original_production_support, JSON.parse(original["plan.json"]).production_support);
  assert.equal(draft.source_binding.source, SOURCE);
  assert.equal(draft.source_binding.source_slug, "borrowed-dawn");
  assert.equal(draft.source_binding.manifest_sha256, sha256(original["manifest.json"]));
  assert.equal(draft.source_binding.bundle_sha256, sourceBundleHash(draft.source_bundle));
  assert.deepEqual(Object.keys(draft.source_binding.file_sha256).sort(), FILE_NAMES);
  for (const name of FILE_NAMES) assert.equal(draft.source_binding.file_sha256[name], sha256(original[name]));
});

test("validated planning shape leaves every missing voice and production requirement pending", () => {
  const draft = buildAnimeProductionInput(original);
  for (const key of ["ready_for_import", "ready_for_production", "admin_series_created", "media_generated", "published", "approvals_recorded"]) assert.equal(draft[key], false);
  const requirements = draft.production_requirements;
  assert.equal(requirements.ready_for_production, false);
  assert.equal(requirements.measured_body_seconds, null);
  assert.equal(requirements.op_ed_media_seconds, null);
  assert.equal(requirements.slot_reserve_generated, false);
  const cast = draft.documents[0].body_json.characters;
  assert.equal(requirements.casting.length, cast.length);
  assert.deepEqual(requirements.casting.map((row) => row.character_id), cast.map((row) => row.id));
  for (const row of requirements.casting) {
    assert.equal(row.source_voice_present, false);
    assert.ok(row.missing.includes("provider and voice name"));
    assert.ok(row.missing.includes("source-bound audition and listening acceptance"));
  }
  assert.ok(cast.every((row) => !Object.hasOwn(row, "voice")));
  assert.ok(requirements.shared.some((row) => row.includes("narrator casting")));
  assert.ok(requirements.shared.some((row) => row.includes("120 complete 22-minute screenplays")));
  assert.ok(requirements.design.some((row) => row.includes("character designs")));
  assert.ok(requirements.design.some((row) => row.includes("provider capability")));
});

test("all twelve original documents pass native anime worker checks without fabricated satisfaction", () => {
  const draft = buildAnimeProductionInput(original);
  const series = { ...draft.series_request, chapters: 10 };
  for (const document of draft.documents) {
    const first = document.kind === "chapter" ? (document.chapter_number - 1) * 12 + 1 : 1;
    const previous = draft.episodes.filter((episode) => episode.number < first).slice(-3);
    assert.equal(documentProblem(document.kind, document, { series, chapter_number: document.chapter_number, context: { episodes: previous } }), null, `${document.kind} ${document.chapter_number ?? ""}`);
  }
});

test("all source, generated and support hashes are checked against actual file bytes", () => {
  for (const name of ["season-01.json", "setting.md", "review.md", "build.mjs", "validate.mjs", "validate.test.mjs"]) {
    const files = clone();
    files[name] += "\n";
    assert.throws(() => buildAnimeProductionInput(files), /雜湊不符|validation/);
  }
  const missing = clone();
  delete missing["review.md"];
  assert.throws(() => buildAnimeProductionInput(missing), /missing or unexpected/);
  const extra = clone();
  extra["../../payload.mjs"] = "throw new Error('never execute')";
  assert.throws(() => buildAnimeProductionInput(extra), /missing or unexpected/);
});

test("rehashed Markdown and embedded Markdown cannot drift together from source JSON", () => {
  const files = clone();
  files["setting.md"] += "A forged ending.\n";
  updateJson(files, "documents.json", (document) => { document.documents[0].body_md = files["setting.md"]; });
  refreshReceipt(files);
  assert.throws(() => buildAnimeProductionInput(files), /setting.md: rendered content differs from source/);
});

test("rehashed structured document and outline twins must be exact projections", () => {
  const files = clone();
  updateJson(files, "documents.json", (document) => { document.documents[2].body_json.episodes[0].state.knowledge = "Invented future knowledge"; });
  refreshReceipt(files);
  assert.throws(() => buildAnimeProductionInput(files), /body_json|來源/);
  const outline = clone();
  updateJson(outline, "outline.json", (document) => { document.chapters[0].production_approved = true; });
  updateJson(outline, "documents.json", (document) => { document.documents[1].body_json = JSON.parse(outline["outline.json"]); });
  refreshReceipt(outline);
  assert.throws(() => buildAnimeProductionInput(outline), /outline projection differs/);
});

test("rehashed continuity CSV/Markdown remain faithful to actual states and chronology", () => {
  for (const name of ["continuity.csv", "continuity.md"]) {
    const files = clone();
    files[name] += "tampered continuity\n";
    refreshReceipt(files);
    assert.throws(() => buildAnimeProductionInput(files), /rendered content differs/);
  }
});

test("rehashed source semantics reject early closed endings, missing high tension and runtime drift", () => {
  const cases = [
    ["season-01.json", (season) => { season.episodes[0].closed_ending = true; }, /closed_ending/],
    ["season-10.json", (season) => { season.episodes[11].tension[4] = 4; }, /E120|末段/],
    ["season-01.json", (season) => { season.episodes[0].high_tension.pop(); }, /high_tension/],
    ["plan.json", (plan) => { plan.runtime.op_ed_budget_minutes = 4; plan.runtime.broadcast_slot_reserve_minutes = 4; }, /source runtime/],
    ["setting.json", (setting) => { setting.chronology[0].seasons = [1, 1]; }, /chronology/],
  ];
  for (const [name, change, error] of cases) {
    const files = clone();
    updateJson(files, name, change);
    // Synchronize JSON twins so semantic errors are assessed independently.
    if (name === "setting.json" || name.startsWith("season-")) updateJson(files, "documents.json", (document) => {
      const row = name === "setting.json" ? document.documents[0] : document.documents[Number(name.slice(7, 9)) + 1];
      row.body_json = JSON.parse(files[name]);
    });
    refreshReceipt(files);
    assert.throws(() => buildAnimeProductionInput(files), error);
  }
});

test("strict JSON rejects duplicate decoded keys, nonfinite values and malformed notation", () => {
  assert.deepEqual(parseSourceJson('{"one":1,"nested":[true,false,null,{"s":"escaped \\\" word"}]}'), { one: 1, nested: [true, false, null, { s: 'escaped " word' }] });
  for (const raw of ['{"category":"anime","category":"story"}', '{"a":1,"\\u0061":2}', '{"n":1e999}', '{"schema_version":1.0}', '{"n":9007199254740993}', '{"a":01}', '{"a":true,}', '{"a":[1,]}']) assert.throws(() => parseSourceJson(raw), /JSON|json/i);
  const files = clone();
  files["plan.json"] = files["plan.json"].replace('"schema_version": 1,', '"schema_version": 1, "schema_version": 1,');
  refreshReceipt(files);
  assert.throws(() => buildAnimeProductionInput(files), /duplicate JSON key/);
});

test("source names and paths are fixed and symlink routes are refused", () => {
  assert.throws(() => validateAnimeSourceFiles(original, { source: "docs/videos/series-plans/another" }), /source path/);
  assert.throws(() => readAnimeSourceFiles("/tmp"), /checked-in/);
  temporary((directory) => {
    const alias = path.join(directory, "borrowed-dawn");
    symlinkSync(SOURCE_DIRECTORY, alias, process.platform === "win32" ? "junction" : "dir");
    assert.equal(fs.lstatSync(alias).isSymbolicLink(), true);
    assert.throws(() => readAnimeSourceFiles(alias), /checked-in/);
  });
  const files = clone();
  updateJson(files, "manifest.json", (manifest) => { manifest.source_files["../secret.json"] = manifest.source_files["plan.json"]; });
  assert.throws(() => buildAnimeProductionInput(files), /清單|validation/);
});

test("source support code is hashed as inert text and never executed", () => {
  const files = clone();
  files["build.mjs"] = 'throw new Error("source support JavaScript was executed");\n';
  files["validate.mjs"] = 'process.exit(77);\n';
  refreshReceipt(files);
  assert.equal(buildAnimeProductionInput(files).ready_for_production, false);
});

test("a symlink entry in the canonical source pack is rejected before opening it", () => {
  temporary((directory) => {
    const entry = path.join(SOURCE_DIRECTORY, "setting.json");
    const alias = path.join(directory, "setting.json");
    symlinkSync(process.platform === "win32" ? SOURCE_DIRECTORY : entry, alias, process.platform === "win32" ? "junction" : "file");
    assert.equal(fs.lstatSync(alias).isSymbolicLink(), true);
    // Supply the actual symlink metadata without mutating another PR's frozen pack.
    const saved = fs.lstatSync;
    fs.lstatSync = (filename, ...args) => saved(filename === entry ? alias : filename, ...args);
    syncBuiltinESMExports();
    try { assert.throws(() => readAnimeSourceFiles(), /cannot contain symlinks/); }
    finally { fs.lstatSync = saved; syncBuiltinESMExports(); }
  });
});

test("changing source or native input invalidates an existing portable draft", () => {
  const draft = buildAnimeProductionInput(original);
  const current = clone();
  current["review.md"] += "\nSource review revision.\n";
  refreshReceipt(current);
  assert.equal(validateAnimeProductionInput(draft), true);
  assert.throws(() => validateAnimeProductionInput(draft, current), /source version changed/);
  for (const change of [
    (value) => { value.series_request.slug = "borrowed-dawn"; },
    (value) => { value.series_request.runtime_spec.slot_reserve_seconds = 360; },
    (value) => { value.ready_for_production = true; },
    (value) => { value.documents[0].body_json.characters[0].voice = { provider: "gemini", name: "invented" }; },
    (value) => { value.source_binding.file_sha256["plan.json"] = "0".repeat(64); },
  ]) {
    const changed = structuredClone(draft);
    change(changed);
    assert.throws(() => validateAnimeProductionInput(changed), /production input differs/);
  }
});

test("CLI is offline, creates only a review file, refuses overwrites and write actions", () => {
  const oldFetch = globalThis.fetch;
  globalThis.fetch = () => { throw new Error("network call is forbidden"); };
  try {
    temporary((directory) => {
      let output = "";
      let error = "";
      const streams = { stdout: { write: (value) => { output += value; } }, stderr: { write: (value) => { error += value; } } };
      const filename = path.join(directory, "draft.json");
      assert.equal(main(["--out", filename], streams), 0);
      assert.equal(error, "");
      assert.match(output, /no import, approval, activation or media generation performed/);
      const draft = JSON.parse(readFileSync(filename, "utf8"));
      assert.equal(validateAnimeProductionInput(draft, original), true);
      const before = readFileSync(filename, "utf8");
      assert.equal(main(["--out", filename], streams), 1);
      assert.equal(readFileSync(filename, "utf8"), before);
      for (const option of ["--apply", "--activate", "--approve", "--endpoint", "--token"]) assert.equal(main([option, "forbidden"], streams), 1);
      assert.equal(main(["--out", path.join(ROOT, "forbidden-draft.json")], streams), 1);
      const alias = path.join(directory, "repo-alias");
      symlinkSync(ROOT, alias, process.platform === "win32" ? "junction" : "dir");
      assert.equal(fs.lstatSync(alias).isSymbolicLink(), true);
      assert.equal(main(["--out", path.join(alias, "forbidden-draft.json")], streams), 1);
    });
  } finally { globalThis.fetch = oldFetch; }
});

test("portable direct CLI succeeds without API dependencies or configured providers", () => {
  temporary((directory) => {
    const out = path.join(directory, "draft.json");
    const result = spawnSync(process.execPath, [path.join(ROOT, "tools/video/production/anime-input.mjs"), "--out", out], { cwd: directory, encoding: "utf8", env: { PATH: process.env.PATH, HTTP_PROXY: "http://127.0.0.1:1", HTTPS_PROXY: "http://127.0.0.1:1" } });
    assert.equal(result.status, 0, result.stderr);
    assert.equal(JSON.parse(readFileSync(out, "utf8")).series_request.target_minutes, 22);
  });
});
