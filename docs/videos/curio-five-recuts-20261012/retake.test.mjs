// Offline tests only: all speech/model invocations are replaced by bounded mocks.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdtempSync, mkdirSync, readFileSync, realpathSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { loadEpisode } from "./speech.mjs";
import { readSecondOpinionResolutions, retakeLine, secondOpinion, strictMatch } from "./retake.mjs";
import { isInside } from "../../../tools/video/core/paths.mjs";
import { SpeechError, SPEECH_UNCERTAIN } from "../../../tools/video/tts/client.mjs";
import { requestSha256 } from "../../../tools/video/tts/speech-journal.mjs";
import { encodeWav, parseWav, requireNarrationFormat } from "../../../tools/video/tts/wav.mjs";

const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const read = (file) => JSON.parse(readFileSync(file, "utf8"));
const save = (file, value) => writeFileSync(file, JSON.stringify(value));
const wav = (n = 0) => encodeWav(Int16Array.from({ length: 48000 }, (_, i) => Math.round(4000 * Math.sin(i * (0.12 + n / 100)))));
const client = { site: "https://test.invalid", token: "offline-only" };
const statusImpl = async () => ({ gemini_configured: true, gemini_monthly_limit: 10000, gemini_used: 0 });

function fixture(t) {
  const base = mkdtempSync(path.join(os.tmpdir(), "curio-retake-offline-"));
  t.after(() => {
    const absolute = realpathSync(base);
    assert.ok(isInside(absolute, realpathSync(os.tmpdir())) && path.basename(absolute).startsWith("curio-retake-offline-"));
    rmSync(absolute, { recursive: true });
  });
  const sources = path.join(base, "sources"), out = path.join(base, "out"), slug = "curio-h02";
  mkdirSync(path.join(sources, slug), { recursive: true });
  save(path.join(sources, slug, "video.json"), { slug, voice: { provider: "gemini", name: "Sulafat", style: "Original style", performance: "Original performance" }, scenes: [] });
  save(path.join(sources, "lexicon.json"), { schema_version: 1, terms: {} });
  const episode = { slug, lines: ["一百一十多人不在了。", "原來的第二句。", "原來的第三句。", "原來的第四句。"].map((text, i) => ({ id: `intro0${i + 1}`, text })) };
  const item = loadEpisode({ episode, sources, out });
  mkdirSync(path.join(item.directory, "audio"), { recursive: true });
  const bytes = wav(), sha = hash(bytes);
  writeFileSync(path.join(item.directory, "audio", "intro01.wav"), bytes);
  const receipt = { identity: item.identity, lines: { intro01: { sha256: sha, request_sha256: requestSha256(item.requests[0].body), samples: requireNarrationFormat(parseWav(bytes)).length } }, aligned: true, duration_ok: true, padding_ok: true };
  const check = { identity: item.identity, lines: { intro01: { sha256: sha, heard: "錯誤的句子", intended: episode.lines[0].text, match_kind: null, noul: 0.05 } }, flags: ["intro01"], threshold: 0.5, ok: false };
  save(path.join(item.directory, "receipt.json"), receipt);
  save(path.join(item.directory, "check.json"), check);
  save(path.join(item.directory, "check-flags.json"), { flags: ["intro01"] });
  save(path.join(path.dirname(item.directory), "shared-timeline.json"), { duration_ok: true, padding_ok: true });
  const model = path.join(base, "model"), helper = path.join(base, "helper.py");
  mkdirSync(model);
  for (const name of ["model.bin", "config.json", "tokenizer.json", "vocabulary.txt"]) writeFileSync(path.join(model, name), `mock ${name}`);
  writeFileSync(helper, "# offline mocked helper");
  return { base, item, model, helper, check, sha };
}

test("strict comparison preserves numeric values and rejects wrong phonemes and Japanese alternatives", () => {
  assert.equal(strictMatch("一百一十多人不在了。", "110多人不在了", "zh-TW"), "resolved-numeric");
  for (const wrong of ["111多人不在了", "多人不在了", "1100多人不在了"]) assert.equal(strictMatch("一百一十多人不在了", wrong, "zh-TW"), null);
  assert.equal(strictMatch("銀光", "螢光", "zh-TW"), null);
  assert.equal(strictMatch("高空", "航空", "ja"), null);
  assert.equal(strictMatch("八千万本", "8000本", "ja"), null);
  assert.equal(strictMatch("Tests identified its material.", "tests identified its material!", "en"), "resolved-exact");
});

test("offline second opinion binds exact WAV/model and retains original Gemini flag", async (t) => {
  const b = fixture(t), checkFile = path.join(b.item.directory, "check.json"), before = hash(readFileSync(checkFile));
  let calls = 0;
  const options = { python: "offline-python", model: b.model, helper: b.helper, run: async (_program, args, opts) => {
    calls++;
    assert.equal(opts.env.HF_HUB_OFFLINE, "1");
    assert.equal(opts.env.VIDEO_SECOND_OPINION_HINTS, undefined);
    assert.ok(!args.some((arg) => arg.includes("一百一十")));
    return { stdout: "intro01.wav 110多人不在了。\n", stderr: "" };
  } };
  const result = await secondOpinion(b.item, "intro01", options);
  assert.equal(result.resolved, true);
  assert.equal(result.owner_listened, false);
  assert.equal(hash(readFileSync(checkFile)), before);
  assert.deepEqual([...readSecondOpinionResolutions(b.item.directory, b.check)], ["intro01"]);
  await secondOpinion(b.item, "intro01", options);
  assert.equal(calls, 1);
  await assert.rejects(retakeLine(b.item, "intro01"), /already has a matching independent transcript/);
  writeFileSync(path.join(b.item.directory, "audio", "intro01.wav"), wav(1));
  assert.throws(() => readSecondOpinionResolutions(b.item.directory, b.check), /WAV changed/);
});

test("retake saves old WAV/report/alignment, invalidates QA and never repeats a committed replacement", async (t) => {
  const b = fixture(t);
  let calls = 0;
  const deps = { client, statusImpl, synthesizeImpl: async ({ body, attempts }) => {
    calls++;
    assert.equal(attempts, 1);
    assert.equal(requestSha256(body), requestSha256(b.item.requests[0].body));
    return { wav: wav(calls), billable: 10 };
  } };
  const first = await retakeLine(b.item, "intro01", deps);
  assert.equal(first.state, "committed");
  assert.equal(first.attempt, 1);
  assert.equal(first.owner_listened, false);
  const intro = path.dirname(b.item.directory);
  const history = path.join(intro, "retakes", "zh-TW-intro01", "attempt-1", "before");
  assert.equal(hash(readFileSync(path.join(history, "zh-TW", "audio", "intro01.wav"))), b.sha);
  assert.deepEqual(read(path.join(b.item.directory, "check.json")).flags, ["intro01"]);
  assert.equal(read(path.join(b.item.directory, "receipt.json")).aligned, false);
  assert.equal(read(path.join(intro, "shared-timeline.json")).duration_ok, false);
  await retakeLine(b.item, "intro01", deps);
  assert.equal(calls, 1);
  // Simulate a new check that still flags this exact replacement SHA.
  const nextCheck = read(path.join(b.item.directory, "check.json"));
  nextCheck.lines.intro01.sha256 = first.candidate_sha256;
  save(path.join(b.item.directory, "check.json"), nextCheck);
  const second = await retakeLine(b.item, "intro01", deps);
  assert.equal(second.attempt, 2);
  nextCheck.lines.intro01.sha256 = second.candidate_sha256;
  save(path.join(b.item.directory, "check.json"), nextCheck);
  await assert.rejects(retakeLine(b.item, "intro01", deps), /two new takes already attempted/);
  assert.equal(calls, 2);
  assert.equal(existsSync(path.join(intro, "LEASE")), false);
});

test("an uncertain retake POST remains held across invocation, without a second attempt", async (t) => {
  const b = fixture(t);
  let calls = 0;
  const deps = { client, statusImpl, synthesizeImpl: async () => { calls++; throw new SpeechError("lost response", { code: SPEECH_UNCERTAIN, who: "owner" }); } };
  await assert.rejects(retakeLine(b.item, "intro01", deps), /not sent again/);
  await assert.rejects(retakeLine(b.item, "intro01", deps), /not sent again/);
  assert.equal(calls, 1);
  assert.equal(hash(readFileSync(path.join(b.item.directory, "audio", "intro01.wav"))), b.sha);
});

test("wrong flag SHA and a live locale lease stop before any speech call", async (t) => {
  const b = fixture(t);
  const checkFile = path.join(b.item.directory, "check.json");
  const wrong = structuredClone(b.check);
  wrong.lines.intro01.sha256 = "0".repeat(64);
  save(checkFile, wrong);
  await assert.rejects(retakeLine(b.item, "intro01"), /exact current WAV/);
  save(checkFile, b.check);
  const lease = path.join(path.dirname(b.item.directory), "en", "LEASE");
  save(lease, { schema_version: 1, token: "unrelated-live-producer", pid: process.pid, host: os.hostname(), start_ticks: null, owner: "offline-competing-check" });
  await assert.rejects(retakeLine(b.item, "intro01"), /held by/);
});
