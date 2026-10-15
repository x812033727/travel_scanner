import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdtempSync, mkdirSync, readFileSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { isInside } from "../../../tools/video/core/paths.mjs";
import { requestSha256 } from "../../../tools/video/tts/speech-journal.mjs";
import { encodeWav } from "../../../tools/video/tts/wav.mjs";
import { loadEpisode, LOCALES, describePlan } from "./speech.mjs";
import { retakeLine } from "./retake.mjs";
import { prepareL08Revision, TEXT_REPAIRS, validateRevision } from "./prepare-l08-revision.mjs";

const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const read = (file) => JSON.parse(readFileSync(file, "utf8"));
function save(file, object) { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, JSON.stringify(object)); }

function fixture(t) {
  const base = mkdtempSync(path.join(os.tmpdir(), "curio-l08-revision-"));
  t.after(() => { const full = realpathSync(base); assert.ok(isInside(full, realpathSync(os.tmpdir())) && path.basename(full).startsWith("curio-l08-revision-")); rmSync(full, { recursive: true }); });
  const sources = path.join(base, "sources"), out = path.join(base, "out"), slug = "curio-l08";
  const voice = { provider: "gemini", name: "Sulafat", style: "Original documentary voice" };
  save(path.join(sources, slug, "video.json"), { slug, voice, scenes: [] });
  save(path.join(sources, "lexicon.json"), { schema_version: 1, terms: {} });
  const lines = ["一個問題。", "另一個問題。", "第三個問題。", "第四個問題。", "第五個問題。", "第六個問題。", "多年後，道格還說，後悔把這件事告訴大家。", "最後的問題。"].map((text, i) => ({ id: `intro0${i + 1}`, text }));
  const episode = { slug, lines, locales: {} };
  for (const locale of LOCALES.slice(1)) {
    save(path.join(sources, slug, "dubs", locale, "timeline.json"), { locale, voice });
    episode.locales[locale] = { lines: lines.map((line) => ({ ...line })) };
  }
  const oldSpec = { schema_version: 1, episodes: [episode] }, newSpec = structuredClone(oldSpec);
  for (const line of newSpec.episodes[0].lines) if (TEXT_REPAIRS[line.id]) line.text = TEXT_REPAIRS[line.id];
  const oldSpecFile = path.join(base, "old.json"), newSpecFile = path.join(base, "new.json");
  save(oldSpecFile, oldSpec); save(newSpecFile, newSpec);
  const items = LOCALES.map((locale) => loadEpisode({ episode, sources, out, locale }));
  const bytes = encodeWav(Int16Array.from({ length: 4800 }, (_, i) => Math.round(3000 * Math.sin(i * 0.1))));
  for (const item of items) {
    const receipt = { identity: item.identity, aligned: true, lines: {} }, check = { identity: item.identity, ok: item.locale !== "zh-TW", flags: item.locale === "zh-TW" ? ["intro07"] : [], lines: {} };
    mkdirSync(path.join(item.directory, "audio"), { recursive: true });
    for (const request of item.requests) {
      const line = request.lines[0], sha256 = hash(bytes);
      writeFileSync(path.join(item.directory, "audio", `${line.id}.wav`), bytes);
      receipt.lines[line.id] = { sha256, samples: 4800, request_sha256: requestSha256(request.body) };
      check.lines[line.id] = { sha256, intended: line.text, heard: line.text, match_kind: check.flags.includes(line.id) ? null : "exact", noul: check.flags.includes(line.id) ? 0.05 : null };
    }
    save(path.join(item.directory, "receipt.json"), receipt);
    save(path.join(item.directory, "check.json"), check);
    save(path.join(item.directory, "video.json"), item.doc);
    save(path.join(item.directory, "second-opinion.json"), { identity: item.identity, lines: {}, test_cache: item.locale });
    if (item.locale === "zh-TW") for (const id of Object.keys(TEXT_REPAIRS)) save(path.join(path.dirname(item.directory), "retakes", `zh-TW-${id}`, "attempt-1", "operation.json"), { state: "committed", attempt: 1, candidate_sha256: hash(bytes), identity: item.identity });
  }
  const intro = path.dirname(items[0].directory);
  save(path.join(intro, "shared-timeline.json"), { duration_ok: true, padding_ok: true });
  return { base, sources, out, oldSpec, newSpec, oldSpecFile, newSpecFile, items, intro };
}

test("only the exact one source-equivalent wording field may differ", (t) => {
  const b = fixture(t);
  assert.doesNotThrow(() => validateRevision(b.oldSpec, b.newSpec));
  const bad = structuredClone(b.newSpec);
  bad.episodes[0].locales.ja.lines[4].text = "別の文。";
  assert.throws(() => validateRevision(b.oldSpec, bad), /only the approved/);
  const wrong = structuredClone(b.newSpec);
  wrong.episodes[0].lines[6].text = "多年後，道格沒有後悔。";
  assert.throws(() => validateRevision(b.oldSpec, wrong), /only the approved/);
});

test("preserves complete history and unchanged takes while exposing exactly one request", async (t) => {
  const b = fixture(t), oldHash = hash(readFileSync(b.oldSpecFile));
  const result = prepareL08Revision(b);
  assert.equal(result.state, "installed");
  assert.equal(hash(readFileSync(b.oldSpecFile)), oldHash);
  assert.deepEqual(result.pending_lines, ["zh-TW/intro07"]);
  assert.equal(result.plans.reduce((sum, plan) => sum + plan.pending_lines, 0), 1);
  for (const [name, sha] of Object.entries(result.before)) assert.equal(hash(readFileSync(path.join(result.history, name))), sha);
  for (const locale of LOCALES) {
    const item = loadEpisode({ episode: b.newSpec.episodes[0], sources: b.sources, out: b.out, locale });
    assert.equal(describePlan(item).pending_lines, locale === "zh-TW" ? 1 : 0);
    const receipt = read(path.join(item.directory, "receipt.json"));
    const check = read(path.join(item.directory, "check.json"));
    assert.equal(receipt.aligned, false);
    assert.equal(check.ok, false);
    const index = path.join(item.directory, "second-opinion.json");
    if (locale === "zh-TW") assert.equal(existsSync(index), false);
    else assert.equal(hash(readFileSync(index)), result.before[`${locale}/second-opinion.json`]);
    assert.deepEqual(receipt.identity, item.identity);
    for (const line of item.lines) {
      const file = path.join(item.directory, "audio", `${line.id}.wav`);
      if (locale === "zh-TW" && TEXT_REPAIRS[line.id]) { assert.equal(existsSync(file), false); assert.equal(check.lines[line.id], undefined); }
      else assert.equal(hash(readFileSync(file)), result.before[`${locale}/audio/${line.id}.wav`]);
    }
    if (locale === "zh-TW") await assert.rejects(retakeLine(item, "intro07"), /further paid retakes are disabled/);
  }
  assert.equal(read(path.join(b.intro, "shared-timeline.json")).duration_ok, false);
  const again = prepareL08Revision(b);
  assert.equal(again.state, "installed");
  assert.equal(again.plans.reduce((sum, plan) => sum + plan.pending_lines, 0), 1);
});

test("a prior second retake stops the revision before preserving or changing media", (t) => {
  const b = fixture(t);
  mkdirSync(path.join(b.intro, "retakes", "zh-TW-intro07", "attempt-2"));
  assert.throws(() => prepareL08Revision(b), /second extra take already exists/);
  assert.equal(existsSync(path.join(b.intro, "RETAKES_DISABLED")), false);
});
