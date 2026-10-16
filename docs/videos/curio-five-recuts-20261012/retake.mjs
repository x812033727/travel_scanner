// Bounded repairs and independent offline transcription for this five-video cohort.
// second-opinion never changes check.json: the assembler must independently consume
// readSecondOpinionResolutions(). A retake invalidates shared alignment and never passes QA.
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs, promisify } from "node:util";
import { atomicWrite } from "../../../tools/video/core/paths.mjs";
import { acquireProjectLease } from "../../../tools/video/core/project-lease.mjs";
import { spokenText } from "../../../tools/video/core/schema.mjs";
import { SPEECH_UNCERTAIN, speechStatus, synthesize } from "../../../tools/video/tts/client.mjs";
import { readCredentials, validSite } from "../../../tools/video/tts/credentials.mjs";
import { billableForRequest } from "../../../tools/video/tts/requests.mjs";
import { openSpeechJournal, requestSha256 } from "../../../tools/video/tts/speech-journal.mjs";
import { trimSilence } from "../../../tools/video/tts/split.mjs";
import { encodeWav, parseWav, requireNarrationFormat } from "../../../tools/video/tts/wav.mjs";
import { loadEpisode, LOCALES } from "./speech.mjs";

const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const read = (file) => JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
const need = (ok, message) => { if (!ok) throw new Error(message); };
const stamp = () => new Date().toISOString();
const same = (left, right) => JSON.stringify(left) === JSON.stringify(right);
const fileHash = (file) => hash(readFileSync(file));
const compare = (text) => String(text).normalize("NFKC").toLowerCase().replace(/[\p{P}\p{S}\p{Z}\s]/gu, "");
const MODEL = path.join(homedir(), ".cache/huggingface/hub/models--Systran--faster-whisper-small/snapshots/536b0662742c02347bc0e980a01041f333bce120");
const PYTHON = path.join(homedir(), "whisper/Scripts/python.exe");
const HELPER = path.resolve("tools/video/tts/whisper_second_opinion.py");
// Root's explicit editorial acceptance of three exact U02 JA transcript pairs.
// This is a fixed evidence allowlist, never a language-wide homophone rule.
const REVIEWED_JA = Object.freeze({
  "curio-u02": { evidence_sha256: "7bb2df0a1f2d7c94c9683c619c5c050c8e75086a9808df3544e383730652a29e",
  clips: {
    intro02: "0d1370dd38f432da8f751fb76a1e9f2d2134ca33671def2bb399ec136cf2a3f4",
    intro05: "00072558fc89fb6c3ea27bb6bb649aaaee1ddf291b2bb40275b13baefad7f297",
    intro06: "367b9eb26ba35c67928a43a7c44ad57f339e9394da232db828846fb6507930e9",
  } },
  "curio-l08": { evidence_sha256: "702b905940f02276660d3e91a9b3820658de72f838943b2311fb8fa323e08e05", clips: {
    intro05: "d0db963476712ce749dfac244f403e1f5488dc8b0d71eac5e340cd53e0728f4e",
  } },
});

function chineseInteger(value) {
  const digits = "零一二三四五六七八九";
  if (value === 0) return "零";
  let result = "", zero = false;
  for (const [unit, label] of [[1000, "千"], [100, "百"], [10, "十"], [1, ""]]) {
    const digit = Math.floor(value / unit) % 10;
    if (!digit) { if (result && value % unit) zero = true; continue; }
    if (zero) result += "零";
    zero = false;
    if (!(unit === 10 && digit === 1 && !result)) result += digits[digit];
    result += label;
  }
  return result;
}

function normalizeNumbers(text) {
  return text.replace(/[零〇一二三四五六七八九十百千]+/gu, (raw) => {
    const token = raw.replaceAll("〇", "零");
    if (!/[十百千]/u.test(token)) return [...token].map((char) => "零一二三四五六七八九".indexOf(char)).join("");
    let total = 0, digit = 0;
    for (const char of token) {
      const unit = { 十: 10, 百: 100, 千: 1000 }[char];
      if (unit) { total += (digit || 1) * unit; digit = 0; }
      else digit = "零一二三四五六七八九".indexOf(char);
    }
    total += digit;
    // Refuse ambiguous or malformed number spellings instead of guessing.
    const canonical = chineseInteger(total);
    return canonical === token || (total >= 10 && total < 20 && `一${canonical}` === token) ? String(total) : raw;
  });
}

/** No phonetic, semantic or approximate comparison. Digits always remain significant. */
export function strictMatch(intended, heard, locale) {
  const expected = compare(intended), actual = compare(heard);
  if (!expected || !actual) return null;
  if (expected === actual) return "resolved-exact";
  if (locale === "zh-TW" && normalizeNumbers(expected) === normalizeNumbers(actual)) return "resolved-numeric";
  return null;
}

function reviewedPair(evidence) {
  const accepted = REVIEWED_JA[evidence.slug];
  if (!accepted) return false;
  const encoded = evidence.reviewed_package_base64;
  if (typeof encoded !== "string" || encoded.length > 100000) return false;
  const bytes = Buffer.from(encoded, "base64");
  if (hash(bytes) !== accepted.evidence_sha256) return false;
  if (evidence.locale !== "ja" || accepted.clips[evidence.line] !== evidence.clip_sha256) return false;
  const reviewed = JSON.parse(bytes.toString("utf8").replace(/^\uFEFF/, ""));
  const line = reviewed.lines.find((entry) => entry.line_id === evidence.line);
  return Boolean(line && line.audio_sha256 === evidence.clip_sha256 && line.intended === evidence.intended &&
    line.qualified_review?.whisper_transcript === evidence.heard &&
    line.qualified_review?.decision === "accept_as_scoped_homophonic_second_opinion" &&
    line.qualified_review?.canonical_kana && reviewed.owner_listened === false && reviewed.full_video_approved === false);
}

function fresh(item) {
  need(fileHash(item.sourceFile) === item.identity.source_sha256, "source document changed");
  need(fileHash(item.lexiconFile) === item.identity.lexicon_sha256, "source lexicon changed");
  if (item.voiceFile) need(fileHash(item.voiceFile) === item.identity.voice_source_sha256, "original dub voice changed");
  for (const dir of [item.directory, path.dirname(item.directory), path.dirname(path.dirname(item.directory)), item.out]) need(!existsSync(path.join(dir, "STOP")), `STOP found at ${dir}`);
}

function leasesFor(item) {
  const leases = [];
  try {
    for (const dir of [path.dirname(item.directory), ...LOCALES.map((locale) => path.join(path.dirname(item.directory), locale))]) leases.push(acquireProjectLease(dir, { owner: "curio-bounded-audio-review" }));
    return { verify() { for (const lease of leases) lease.verify(); fresh(item); }, release() { for (const lease of leases.reverse()) lease.release(); } };
  } catch (error) { for (const lease of leases.reverse()) lease.release(); throw error; }
}

function current(item, id) {
  fresh(item);
  const line = item.lines.find((candidate) => candidate.id === id);
  const request = item.requests.find((candidate) => candidate.lines[0].id === id);
  need(line && request, "line is outside the selected opening");
  const receipt = read(path.join(item.directory, "receipt.json"));
  const checkFile = path.join(item.directory, "check.json");
  const check = read(checkFile);
  need(same(receipt.identity, item.identity) && same(check.identity, item.identity), "source/request/check identity changed");
  const entry = check.lines?.[id], cached = receipt.lines?.[id];
  const wavFile = path.join(item.directory, "audio", `${id}.wav`);
  const sha256 = fileHash(wavFile);
  need(check.flags?.includes(id) && entry && !entry.match_kind && !(entry.noul >= (check.threshold ?? 0.5)), "selected line is not currently flagged");
  need(sha256 === cached?.sha256 && sha256 === entry.sha256, "flag does not identify the exact current WAV");
  need(cached.request_sha256 === requestSha256(request.body), "saved request identity changed");
  need(entry.intended === spokenText(line), "checked text does not match the opening specification");
  need(requireNarrationFormat(parseWav(readFileSync(wavFile))).length === cached.samples, "cached sample length changed");
  return { line, request, receipt, check, checkFile, entry, cached, wavFile, sha256 };
}

/** Read only, fail closed. A stale independent transcript cannot clear a new take. */
export function readSecondOpinionResolutions(directory, check) {
  const indexFile = path.join(directory, "second-opinion.json");
  const resolved = new Set();
  if (!existsSync(indexFile)) return resolved;
  const index = read(indexFile);
  need(index.schema_version === 1 && index.kind === "curio-independent-audio-review" && same(index.identity, check.identity), "second-opinion index identity mismatch");
  for (const id of check.flags ?? []) {
    const pointer = index.lines?.[id];
    if (!pointer) continue;
    need(/^[a-z0-9]{4,8}-[a-f0-9]{64}\.json$/.test(pointer.file), "unsafe second-opinion evidence path");
    const file = path.join(directory, "second-opinion", pointer.file);
    need(fileHash(file) === pointer.sha256, "independent evidence changed");
    const evidence = read(file), entry = check.lines[id];
    if (evidence.clip_sha256 !== entry.sha256) continue;
    need(evidence.schema_version === 1 && evidence.kind === "curio-offline-second-opinion" && evidence.line === id && evidence.locale === check.identity.locale, "independent evidence identity mismatch");
    need(evidence.intended === entry.intended && evidence.original_check_entry.sha256 === entry.sha256 && evidence.original_check_entry.intended === entry.intended, "independent expected text changed");
    need(evidence.clip_sha256 === fileHash(path.join(directory, "audio", `${id}.wav`)), "independent evidence WAV changed");
    need(evidence.expected_text_sent === false && evidence.offline === true && evidence.model.files?.["model.bin"] && evidence.command?.length && evidence.helper_sha256, "independent model/command evidence incomplete");
    const outcome = strictMatch(evidence.intended, evidence.heard, evidence.locale);
    if ((outcome && evidence.outcome === outcome) || (evidence.outcome === "resolved-reviewed-homophone" && reviewedPair(evidence))) resolved.add(id);
  }
  return resolved;
}

/** deps only support offline tests; CLI uses the local cached model without downloads. */
export async function secondOpinion(item, id, { python = PYTHON, model = MODEL, helper = HELPER, run = promisify(execFile) } = {}) {
  const leases = leasesFor(item);
  try {
    const selected = current(item, id);
    const evidenceFile = `${id}-${selected.sha256}.json`;
    const directory = path.join(item.directory, "second-opinion");
    const target = path.join(directory, evidenceFile);
    const indexFile = path.join(item.directory, "second-opinion.json");
    let evidence;
    if (existsSync(target)) {
      evidence = read(target);
      need(evidence.clip_sha256 === selected.sha256 && evidence.intended === selected.entry.intended, "saved independent evidence conflicts");
    } else {
      need(path.isAbsolute(model) && existsSync(model), "offline model must be an existing absolute directory");
      const modelFiles = Object.fromEntries(["model.bin", "config.json", "tokenizer.json", "vocabulary.txt"].map((name) => [name, fileHash(path.join(model, name))]));
      const helperSha = fileHash(helper);
      const args = ["-X", "utf8", helper, item.locale, selected.wavFile];
      const env = { ...process.env, WHISPER_MODEL: model, HF_HUB_OFFLINE: "1", TRANSFORMERS_OFFLINE: "1", HF_HUB_DISABLE_TELEMETRY: "1", PYTHONUTF8: "1" };
      delete env.VIDEO_SECOND_OPINION_HINTS;
      leases.verify();
      const result = await run(python, args, { env, windowsHide: true, encoding: "utf8", timeout: 240000, maxBuffer: 1024 * 1024 });
      leases.verify();
      need(fileHash(selected.wavFile) === selected.sha256 && fileHash(helper) === helperSha, "audio/helper changed during transcription");
      const prefix = `${id}.wav `;
      const text = String(result.stdout).split(/\r?\n/).find((value) => value.startsWith(prefix))?.slice(prefix.length).trim();
      need(text, "offline helper did not return this line");
      const checkBytes = readFileSync(selected.checkFile);
      const checkSha = hash(checkBytes);
      atomicWrite(path.join(directory, `${checkSha}.original-check.json`), checkBytes);
      evidence = { schema_version: 1, kind: "curio-offline-second-opinion", slug: item.slug, locale: item.locale, line: id, clip_sha256: selected.sha256, intended: selected.entry.intended, heard: text, outcome: strictMatch(selected.entry.intended, text, item.locale) ?? "unresolved", created_at: stamp(), expected_text_sent: false, offline: true, command: [python, ...args], helper_sha256: helperSha, model: { directory: model, files: modelFiles }, environment: { WHISPER_MODEL: model, HF_HUB_OFFLINE: "1", TRANSFORMERS_OFFLINE: "1", HF_HUB_DISABLE_TELEMETRY: "1", PYTHONUTF8: "1", VIDEO_SECOND_OPINION_HINTS: null }, stdout: String(result.stdout), stderr: String(result.stderr ?? ""), original_check_sha256: checkSha, original_check_entry: selected.entry, owner_listened: false, full_video_approved: false };
      atomicWrite(target, json(evidence));
    }
    leases.verify();
    const index = existsSync(indexFile) ? read(indexFile) : { schema_version: 1, kind: "curio-independent-audio-review", identity: item.identity, lines: {}, owner_listened: false, full_video_approved: false };
    need(same(index.identity, item.identity), "independent review identity changed");
    index.lines[id] = { file: evidenceFile, sha256: fileHash(target) };
    atomicWrite(indexFile, json(index));
    const resolved = readSecondOpinionResolutions(item.directory, selected.check).has(id);
    return { line: id, locale: item.locale, evidence_file: target, outcome: evidence.outcome, resolved, owner_listened: false };
  } finally { leases.release(); }
}

/** Install only the three source-bound Japanese comparisons explicitly reviewed by
 * the independent reviewer and accepted by root. The original Gemini report stays.
 * This performs no transcription, synthesis, fuzzy matching or owner playback.
 */
export function importReviewedHomophone(item, id, evidenceFile) {
  const leases = leasesFor(item);
  try {
    const selected = current(item, id);
    const bytes = readFileSync(evidenceFile);
    need(hash(bytes) === REVIEWED_JA[item.slug]?.evidence_sha256, "reviewed evidence is outside the explicitly accepted package");
    const reviewed = JSON.parse(bytes.toString("utf8").replace(/^\uFEFF/, ""));
    const line = reviewed.lines.find((entry) => entry.line_id === id);
    need(line && item.locale === "ja" && line.audio_sha256 === selected.sha256 && line.intended === selected.line.text, "reviewed pair does not identify this source and take");
    const evidence = { schema_version: 1, kind: "curio-offline-second-opinion", slug: item.slug, locale: item.locale, line: id, clip_sha256: selected.sha256, intended: selected.line.text, heard: line.qualified_review.whisper_transcript, outcome: "resolved-reviewed-homophone", created_at: stamp(), expected_text_sent: false, offline: true, command: [reviewed.python_executable, "-X", "utf8", reviewed.script, reviewed.locale, ...reviewed.lines.map((entry) => entry.audio_file)], helper_sha256: reviewed.script_sha256, model: { directory: reviewed.model_path, files: reviewed.model_files_sha256 }, reviewed_package_base64: bytes.toString("base64"), reviewer: reviewed.reviewer, review_basis: reviewed.review_basis, qualified_review: line.qualified_review, original_check_sha256: fileHash(selected.checkFile), original_check_entry: selected.entry, owner_listened: false, full_video_approved: false };
    need(reviewedPair(evidence), "exact reviewed pair validation failed");
    leases.verify();
    const directory = path.join(item.directory, "second-opinion");
    const filename = `${id}-${selected.sha256}.json`, target = path.join(directory, filename);
    if (existsSync(target)) {
      const previous = read(target);
      need(previous.clip_sha256 === selected.sha256 && previous.intended === selected.line.text, "existing review evidence conflicts");
      atomicWrite(path.join(directory, `${hash(readFileSync(target))}.previous-evidence.json`), readFileSync(target));
    }
    atomicWrite(path.join(directory, `${evidence.original_check_sha256}.original-check.json`), readFileSync(selected.checkFile));
    atomicWrite(target, json(evidence));
    const indexFile = path.join(item.directory, "second-opinion.json");
    const index = existsSync(indexFile) ? read(indexFile) : { schema_version: 1, kind: "curio-independent-audio-review", identity: item.identity, lines: {}, owner_listened: false, full_video_approved: false };
    need(same(index.identity, item.identity), "independent review identity changed");
    index.lines[id] = { file: filename, sha256: fileHash(target) };
    atomicWrite(indexFile, json(index));
    need(readSecondOpinionResolutions(item.directory, selected.check).has(id), "consumer rejected scoped reviewed pair");
    return { line: id, locale: item.locale, evidence_file: target, outcome: evidence.outcome, resolved: true, owner_listened: false };
  } finally { leases.release(); }
}

function retakeOptions(client) {
  const credentials = client ?? readCredentials();
  need(credentials.token && validSite(`${credentials.site}/`), "established speech credentials are unavailable");
  return { site: credentials.site, token: credentials.token, ...(credentials.fetchImpl ? { fetchImpl: credentials.fetchImpl } : {}), attempts: 1 };
}

function ready(status, item, billable) {
  if (item.doc.voice.provider === "gemini") {
    need(status.gemini_configured, "Gemini narration is not configured");
    if (item.doc.voice.model && status.gemini_models?.length) need(status.gemini_models.includes(item.doc.voice.model), "original Gemini model is unavailable");
    if (status.gemini_monthly_limit > 0 && status.gemini_used != null) need(billable <= status.gemini_monthly_limit - status.gemini_used, "Gemini budget insufficient");
  } else {
    need(status.configured && status.voices?.includes(item.doc.voice.name), "original Azure voice unavailable");
    if (status.monthly_limit > 0 && status.remaining != null) need(billable <= status.remaining, "Azure budget insufficient");
  }
}

function snapshotFiles(item, id, destination) {
  const intro = path.dirname(item.directory);
  const names = ["shared-timeline.json", `${item.locale}/audio/${id}.wav`];
  for (const locale of LOCALES) {
    names.push(...["receipt.json", "check.json", "check-flags.json", "timeline.json", "narration.wav", `${locale}.srt`, "second-opinion.json"].map((name) => `${locale}/${name}`));
  }
  const files = {};
  for (const name of names) {
    const source = path.join(intro, name);
    if (!existsSync(source)) continue;
    const bytes = readFileSync(source);
    atomicWrite(path.join(destination, "before", name), bytes);
    files[name] = hash(bytes);
  }
  need(files["shared-timeline.json"], "retake requires an existing shared alignment");
  return files;
}

function validateOperation(item, id, operation, directory) {
  need(operation.schema_version === 1 && operation.kind === "curio-bounded-line-retake" && operation.line === id && operation.locale === item.locale && same(operation.identity, item.identity), "retake operation identity changed");
  need(["prepared", "candidate-saved", "committing", "committed"].includes(operation.state), "unknown retake operation state; inspect manually");
  need(operation.attempt >= 1 && operation.attempt <= 2, "invalid retake attempt");
  for (const [name, sha] of Object.entries(operation.before)) need(fileHash(path.join(directory, "before", name)) === sha, "retake history changed");
}

/** Exactly one requested line, at most two new takes; uncertain paid outcomes stay held.
 * Same text, original voice and request identity. No pronunciation edits or retries.
 */
export async function retakeLine(item, id, { client, synthesizeImpl = synthesize, statusImpl = speechStatus, onProgress = () => {} } = {}) {
  const leases = leasesFor(item);
  try {
    need(!existsSync(path.join(path.dirname(item.directory), "RETAKES_DISABLED")), "further paid retakes are disabled for this revision");
    need(item.lines.some((line) => line.id === id), "line is outside this opening");
    const intro = path.dirname(item.directory);
    const root = path.join(intro, "retakes", `${item.locale}-${id}`);
    const existing = existsSync(root) ? readdirSync(root).filter((name) => /^attempt-[12]$/.test(name)).sort() : [];
    const request = item.requests.find((candidate) => candidate.lines[0].id === id);
    let operation, directory;
    if (existing.length) {
      directory = path.join(root, existing.at(-1));
      operation = read(path.join(directory, "operation.json"));
      validateOperation(item, id, operation, directory);
      if (operation.state === "committed") {
        const check = read(path.join(item.directory, "check.json"));
        if (check.lines?.[id]?.sha256 === operation.before_clip_sha256) {
          need(operation.after && Object.entries(operation.after).every(([name, sha]) => fileHash(path.join(intro, name)) === sha), "committed retake output changed before recheck");
          return operation; // Resume after commit: never buy the same replacement again.
        }
        operation = null;
      }
    }
    if (!operation) {
      const selected = current(item, id);
      need(!readSecondOpinionResolutions(item.directory, selected.check).has(id), "line already has a matching independent transcript; retake refused");
      need(existing.length < 2, "two new takes already attempted for this line; stop and review");
      directory = path.join(root, `attempt-${existing.length + 1}`);
      leases.verify();
      const before = snapshotFiles(item, id, directory);
      operation = { schema_version: 1, kind: "curio-bounded-line-retake", identity: item.identity, locale: item.locale, line: id, attempt: existing.length + 1, state: "prepared", created_at: stamp(), before_clip_sha256: selected.sha256, request_sha256: requestSha256(request.body), request: request.body, before, owner_listened: false, full_video_approved: false };
      atomicWrite(path.join(directory, "operation.json"), json(operation));
    }
    need(operation.request_sha256 === requestSha256(request.body), "retake request changed");
    // Every resume can accept only the original bytes or this operation's already
    // committed bytes. A check/align run after a partial commit is a conflict.
    for (const [name, sha] of Object.entries(operation.before)) {
      const currentSha = fileHash(path.join(intro, name));
      need(currentSha === sha || currentSha === operation.after?.[name], `retake output conflict: ${name}`);
    }
    if (operation.state === "prepared") {
      const candidateFile = path.join(directory, "candidate.wav");
      const candidateReceipt = path.join(directory, "candidate.json");
      let candidate;
      if (existsSync(candidateReceipt)) {
        candidate = read(candidateReceipt);
        need(candidate.request_sha256 === operation.request_sha256 && fileHash(candidateFile) === candidate.sha256, "saved retake candidate changed");
      } else {
        const options = retakeOptions(client);
        ready(await statusImpl(options), item, billableForRequest(request.body));
        const journal = openSpeechJournal(path.join(directory, "speech-journal"));
        const send = journal.wrap((body) => synthesizeImpl({ ...options, body }));
        leases.verify();
        onProgress({ line: id, locale: item.locale, attempt: operation.attempt, stage: "synthesizing" });
        const result = await send(request.body);
        const samples = trimSilence(requireNarrationFormat(parseWav(result.wav)));
        need(samples.length > 0, "retake returned an empty take");
        const wav = encodeWav(samples);
        candidate = { request_sha256: operation.request_sha256, sha256: hash(wav), samples: samples.length, billable: result.billable, saved_at: stamp(), retake_attempt: operation.attempt };
        leases.verify();
        atomicWrite(candidateFile, wav);
        atomicWrite(candidateReceipt, json(candidate));
        need(fileHash(candidateFile) === candidate.sha256, "candidate readback failed");
        journal.release(); // Safe only once the exact candidate WAV+receipt are durable.
      }
      const receipt = read(path.join(directory, "before", item.locale, "receipt.json"));
      receipt.lines[id] = candidate;
      Object.assign(receipt, { aligned: false, status: "retaken-awaiting-shared-alignment", retake: { line: id, attempt: operation.attempt, before_sha256: operation.before_clip_sha256, after_sha256: candidate.sha256 }, owner_listened: false, full_video_approved: false });
      const check = read(path.join(directory, "before", item.locale, "check.json"));
      // Preserve every original flag and ASR result. checkOpening will transcribe
      // the new SHA and cache all unchanged clips after alignOpenings runs again.
      Object.assign(check, { ok: false, retake_pending: { line: id, attempt: operation.attempt, new_sha256: candidate.sha256 }, owner_listened: false, full_video_approved: false });
      const shared = read(path.join(directory, "before", "shared-timeline.json"));
      Object.assign(shared, { duration_ok: false, padding_ok: false, retake_pending: { locale: item.locale, line: id, new_sha256: candidate.sha256 }, status: "invalidated-awaiting-shared-alignment" });
      const changes = { [`${item.locale}/audio/${id}.wav`]: readFileSync(candidateFile), [`${item.locale}/receipt.json`]: json(receipt), [`${item.locale}/check.json`]: json(check), "shared-timeline.json": json(shared) };
      operation.after = {};
      for (const [name, bytes] of Object.entries(changes)) { atomicWrite(path.join(directory, "after", name), bytes); operation.after[name] = hash(bytes); }
      operation.state = "candidate-saved";
      operation.candidate_sha256 = candidate.sha256;
      atomicWrite(path.join(directory, "operation.json"), json(operation));
    }
    operation.state = "committing";
    atomicWrite(path.join(directory, "operation.json"), json(operation));
    for (const [name, sha] of Object.entries(operation.after)) {
      leases.verify();
      const bytes = readFileSync(path.join(directory, "after", name));
      need(hash(bytes) === sha, "staged replacement changed");
      atomicWrite(path.join(intro, name), bytes);
      need(fileHash(path.join(intro, name)) === sha, "replacement readback failed");
    }
    operation.state = "committed";
    operation.committed_at = stamp();
    atomicWrite(path.join(directory, "operation.json"), json(operation));
    return operation;
  } finally { leases.release(); }
}

export async function main(args = process.argv.slice(2)) {
  const { values, positionals } = parseArgs({ args, allowPositionals: true, options: Object.fromEntries(["spec", "sources", "out", "slug", "locale", "line", "python", "model", "evidence"].map((key) => [key, { type: "string" }])) });
  for (const field of ["spec", "sources", "out", "slug", "locale", "line"]) need(values[field], `--${field} is required`);
  const spec = read(values.spec), episode = spec.episodes?.find((entry) => entry.slug === values.slug);
  need(episode, "episode is absent from the opening specification");
  const item = loadEpisode({ episode, sources: values.sources, out: values.out, locale: values.locale });
  need(positionals.length === 1 && ["second-opinion", "reviewed-homophone", "retake"].includes(positionals[0]), "command must be second-opinion, reviewed-homophone or retake");
  const result = positionals[0] === "second-opinion" ? await secondOpinion(item, values.line, { python: values.python, model: values.model }) : positionals[0] === "reviewed-homophone" ? importReviewedHomophone(item, values.line, values.evidence) : await retakeLine(item, values.line);
  console.log(json(result));
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) main().catch((error) => { console.error(error.message); process.exitCode = error.code === SPEECH_UNCERTAIN ? 3 : 1; });
