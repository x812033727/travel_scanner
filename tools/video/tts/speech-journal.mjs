// What a run sent for a paid speech request, on disk, so the next run neither buys a saved answer
// again nor resends a request whose answer was lost.
//
// tts/client.mjs never sends a paid request twice in one process: an answer lost on the way is
// SPEECH_UNCERTAIN. The journal carries that across runs for the commands that send one: a
// synthesis through a `send(body)` (tts and audition here, dubs/cli.mjs, shorts/speech.mjs), and
// a transcription or a Jev judgement through `wrapTranscribe`/`wrapJudge` (check-audio in
// check.mjs, a Short's check in shorts/check.mjs). One file per request, named by the sha256 of
// the JSON body exactly as client.mjs sends it (its `requestSha256`):
//
//   <sha>.json  before the body goes out: "sent", with the route, the body (a clip's audio only
//               as its sha256 and size) and the time. Once an answer arrives, "confirmed" with the
//               saved WAV's sha256 and the billable characters, or with the transcript or Jev's
//               results themselves and their sha256; when none usable does, "held" with why.
//               While client.mjs waits to try again after an answer that settled it (the routes'
//               rate limit, a provider busy), "waiting" with a wait id, and "sent" again before
//               the next POST.
//   <sha>.wav   a synthesis's confirmed answer as `send` returned it, saved before the entry says so.
//   <sha>.<wait id>.claim  for a moment, while a run turns a waiting entry back into its own sent
//               one: whoever creates it first sends, so two runs never both do.
//
// A run asking for the same body takes a confirmed answer from disk instead of buying it again,
// and stops on a sent or held one without sending it (SPEECH_UNCERTAIN, the owner's, exit 3): it
// may have run and been charged, and only `forget` clears it. A waiting one it sends: nothing
// that may have reached a provider is out, and the run that left it stopped mid-wait or, still
// asleep, stops when it wakes (exit 4) without sending. A body that differs in any byte
// (text, voice, model, style, language; a clip, its terms, Jev's lines) is another request and
// never reuses an answer. Once the caller has saved what it made of its answers (its own cache),
// `release` drops their entries, so a later retake of the same body buys a new take. Every write
// is whole or absent (a temporary file renamed or linked into place), and an entry is created
// only where none exists, so two runs on one directory cannot both send the same body.
//
// The journal decides nothing about voices, models or budgets, which stay with the server, and
// nothing about listening: a confirmed answer is only bytes that arrived whole, never accepted
// audio, a transcript that is right or a verdict that passes.
//
//   node tools/video/tts/speech-journal.mjs list --dir D
//   node tools/video/tts/speech-journal.mjs forget --dir D --sha S
import { createHash, randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, linkSync, lstatSync, mkdirSync, openSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { isDeepStrictEqual, parseArgs } from "node:util";

import { atomicWrite, UsageError } from "../core/paths.mjs";
import { NARRATION_LOCALE } from "../core/schema.mjs";
import { SPEECH_UNCERTAIN, SpeechError, withPaidWaits } from "./client.mjs";
import { parseWav, requireNarrationFormat } from "./wav.mjs";

/**
 * The journal's directory name, beside the cache it protects: <workdir>/audio/speech-journal for
 * tts, dub and check-audio; a Short's <build>/speech-journal for its check.
 */
export const JOURNAL_DIR = "speech-journal";
const SELF = "tools/video/tts/speech-journal.mjs";
const SHA256 = /^[0-9a-f]{64}$/;
const WAIT_ID = /^[0-9a-f-]{36}$/;
const STATUSES = new Set(["sent", "waiting", "held", "confirmed"]);

const sha256 = (data) => createHash("sha256").update(data).digest("hex");
/** What client.mjs names a request by: the sha256 of its JSON body as sent. */
export const requestSha256 = (body) => sha256(JSON.stringify(body));
const entryFile = (dir, sha) => path.join(dir, `${sha}.json`);
const claimFile = (dir, sha, waitId) => path.join(dir, `${sha}.${waitId}.claim`);
const wavFile = (dir, sha) => path.join(dir, `${sha}.wav`);
const answerFile = (dir, sha) => path.join(dir, `${sha}.answer.json`);
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const oneLine = (text) => String(text).replace(/\s+/g, " ").trim();

// Windows cannot open a directory to fsync it; POSIX also commits the rename or link that way.
function syncDirectory(dir) {
  if (process.platform === "win32") return;
  const fd = openSync(dir, "r");
  try { fsyncSync(fd); } finally { closeSync(fd); }
}

function durableWrite(file, data) {
  atomicWrite(file, data);
  const fd = openSync(file, "r+");
  try { fsyncSync(fd); } finally { closeSync(fd); }
  syncDirectory(path.dirname(file));
}

/** Put `data` at `file` whole, only when nothing is there yet; false when something is. */
function createOnce(file, data) {
  const temporary = `${file}.${process.pid}.${randomUUID()}.tmp`;
  const fd = openSync(temporary, "wx");
  try { writeFileSync(fd, data); fsyncSync(fd); } finally { closeSync(fd); }
  try {
    linkSync(temporary, file);
    syncDirectory(path.dirname(file));
    return true;
  } catch (error) {
    if (error?.code === "EEXIST") return false;
    throw error;
  } finally {
    rmSync(temporary, { force: true });
  }
}

// A permission error is not proof that another producer stopped. PID reuse is conservative:
// an unrelated live process with the same PID holds as well.
function processAlive(pid) {
  try { process.kill(pid, 0); return true; }
  catch (error) { return error?.code === "ESRCH" ? false : null; }
}

const regular = (file) => {
  try { return lstatSync(file).isFile(); } catch { return false; }
};
const CONFIRMED_FIELDS = ["confirmed_at", "sent_sha256", "wav_sha256", "wav_bytes", "billable", "answer", "answer_sha256"];
function asSent(entry) {
  const sent = { ...entry, status: "sent" };
  for (const name of CONFIRMED_FIELDS) delete sent[name];
  return sent;
}

// The complete confirmation is committed through a new name before the replace of `sent`.
// This is local persistence only: neither this file nor an orphan temp authorizes another POST.
function stageAnswer(route, dir, sha, sentBytes, confirmedBytes, create) {
  const data = json({ schema_version: 1, sent_sha256: sha256(sentBytes), sent_bytes: sentBytes.length,
    confirmed_sha256: sha256(confirmedBytes), confirmed_bytes: confirmedBytes.length,
    confirmed_base64: confirmedBytes.toString("base64") });
  const file = answerFile(dir, sha);
  if (!create(file, data) && (!regular(file) || !readFileSync(file).equals(Buffer.from(data)))) {
    throw holdError(route, dir, sha, "has a different retained answer confirmation");
  }
}

/** Strict recovery checks; ordinary accepted/cached answers still follow each route's contract. */
function recoveryAnswer(route, dir, sha, candidate, request) {
  const fields = Object.keys(asSent(candidate));
  fields.push("confirmed_at");
  if (candidate.sent_sha256 !== undefined) fields.push("sent_sha256");
  fields.push(...(route === SPEECH ? ["wav_sha256", "wav_bytes", "billable"] : ["answer", "answer_sha256"]));
  if (!isDeepStrictEqual(Object.keys(candidate).sort(), fields.sort())) return null;
  if (route === SPEECH) {
    if (!SHA256.test(candidate.wav_sha256 ?? "") || !Number.isInteger(candidate.wav_bytes) || candidate.wav_bytes <= 44 ||
        !Number.isFinite(candidate.billable) || candidate.billable < 0 || !regular(wavFile(dir, sha))) return null;
    const answer = route.load(dir, sha, candidate);
    if (!answer) return null;
    try {
      const wav = parseWav(answer.wav);
      requireNarrationFormat(wav);
      return wav.samples.length ? answer : null;
    } catch { return null; }
  }
  if (!SHA256.test(candidate.answer_sha256 ?? "") || !intact(candidate) || !candidate.answer || typeof candidate.answer !== "object") return null;
  const keys = Object.keys(candidate.answer);
  if (route === TRANSCRIBE) return keys.length === 1 && keys[0] === "text" && typeof candidate.answer.text === "string" ? candidate.answer.text : null;
  if (keys.length !== 1 || keys[0] !== "results" || !Array.isArray(candidate.answer.results)) return null;
  const ids = (request.lines ?? []).map((line) => line.id);
  const results = candidate.answer.results;
  if (!ids.length || new Set(ids).size !== ids.length || results.length !== ids.length || new Set(results.map((item) => item?.id)).size !== ids.length) return null;
  for (const result of results) {
    if (!result || !isDeepStrictEqual(Object.keys(result).sort(), ["id", "noul"]) || !ids.includes(result.id)) return null;
    const value = result.noul;
    if (!(typeof value === "number" && Number.isFinite(value) && value >= 0 && value <= 1) && !["NaN", "Infinity", "-Infinity"].includes(value)) return null;
  }
  return route.load(dir, sha, candidate);
}

/**
 * Read/reuse an exact complete answer left after a failed local promotion. Canonical `sent`
 * stays untouched, so recovery cannot replace a newer held, forgotten or retaken generation.
 * All evidence is preserved before hand-out, using exclusive content-addressed files. Archive
 * files are never discovery candidates. Concurrent readers may reuse one answer, as they can
 * for an ordinary confirmed entry; only the first creates its identical proof.
 */
function recoverAnswer(route, dir, sha, entry, request, { create, processAlive: alive }) {
  const file = entryFile(dir, sha);
  if (!regular(file)) return null;
  const sentBytes = readFileSync(file);
  try {
    if (!isDeepStrictEqual(JSON.parse(sentBytes.toString("utf8")), entry) || !isDeepStrictEqual(entry.request, request)) return null;
  } catch { return null; }
  const sentSha = sha256(sentBytes);
  const candidates = [];
  const names = readdirSync(dir).filter((name) => name === `${sha}.answer.json` || new RegExp(`^${sha}\\.json\\.[1-9][0-9]*\\.tmp$`).test(name)).sort();
  for (const name of names) {
    const source = path.join(dir, name);
    if (!regular(source)) return null;
    const sourceBytes = readFileSync(source);
    let raw, candidate, pid;
    try {
      if (name === `${sha}.answer.json`) {
        const stage = JSON.parse(sourceBytes.toString("utf8"));
        if (stage.schema_version !== 1 || stage.sent_sha256 !== sentSha || stage.sent_bytes !== sentBytes.length ||
            !SHA256.test(stage.confirmed_sha256 ?? "") || !Number.isInteger(stage.confirmed_bytes) || typeof stage.confirmed_base64 !== "string") return null;
        raw = Buffer.from(stage.confirmed_base64, "base64");
        if (raw.toString("base64") !== stage.confirmed_base64 || raw.length !== stage.confirmed_bytes || sha256(raw) !== stage.confirmed_sha256) return null;
        candidate = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(raw));
        pid = candidate.producer_pid;
      } else {
        raw = sourceBytes;
        candidate = JSON.parse(new TextDecoder("utf-8", { fatal: true }).decode(raw));
        pid = Number(name.slice(`${sha}.json.`.length, -4));
      }
    } catch { return null; }
    // A known older generation is retained, but cannot answer for this one.
    if (!isDeepStrictEqual(asSent(candidate), entry)) continue;
    if (candidate.status !== "confirmed" || candidate.schema_version !== 1 || candidate.request_sha256 !== sha ||
        (candidate.path ?? SPEECH.path) !== route.path || !Number.isInteger(pid) || pid <= 0 || pid > 0x7fffffff ||
        (candidate.producer_pid !== undefined && candidate.producer_pid !== pid) || alive(pid) !== false ||
        typeof candidate.confirmed_at !== "string" || !Number.isFinite(Date.parse(candidate.confirmed_at)) ||
        (candidate.sent_sha256 !== undefined && candidate.sent_sha256 !== sentSha)) return null;
    // Legacy temps have no byte hash/nonce. Only the exact JSON the old writer copied from
    // `sent`, including key order, whitespace and newline, establishes their original receipt.
    if (name !== `${sha}.answer.json` && !Buffer.from(json(asSent(candidate))).equals(sentBytes)) return null;
    const answer = recoveryAnswer(route, dir, sha, candidate, request);
    if (answer === null) return null;
    candidates.push({ name, sourceBytes, raw, candidate, pid, answer });
  }
  if (!candidates.length || new Set(candidates.map((item) => sha256(item.raw))).size !== 1) return null;
  const [chosen] = candidates;
  const recovery = path.join(dir, "recovery");
  const archive = path.join(recovery, sentSha);
  for (const directory of [recovery, archive]) {
    try { mkdirSync(directory); } catch (error) { if (error?.code !== "EEXIST") throw error; }
    const info = lstatSync(directory);
    if (!info.isDirectory() || info.isSymbolicLink()) throw holdError(route.path, dir, sha, "has a recovery directory that is not an ordinary directory");
  }
  const preserve = (name, bytes) => {
    const target = path.join(archive, name);
    if (!create(target, bytes) && (!regular(target) || !readFileSync(target).equals(Buffer.from(bytes)))) {
      throw holdError(route.path, dir, sha, "has changed recovery evidence");
    }
    return { name, sha256: sha256(bytes), bytes: bytes.length };
  };
  const evidence = { sent: preserve("sent.json", sentBytes), confirmed: preserve("confirmed.json", chosen.raw) };
  if (route === SPEECH) evidence.wav = preserve("answer.wav", chosen.answer.wav);
  evidence.sources = candidates.map((item, index) => ({ original_name: item.name, ...preserve(`source-${index}.json`, item.sourceBytes) }));
  const proof = json({ schema_version: 1, request_sha256: sha, path: route.path, sent_sha256: sentSha,
    confirmed_sha256: sha256(chosen.raw), producer_pid: chosen.pid, evidence });
  preserve("proof.json", Buffer.from(proof));
  // An intentional release/forget/retake that happened while evidence was copied cannot be
  // treated as the generation we just validated. No canonical write occurs in either case.
  if (!regular(file) || !readFileSync(file).equals(sentBytes)) return null;
  return { answer: chosen.answer, entryHash: sentSha };
}

// The bodies client.mjs sends for a clip and for Jev (transcribeClip, judgeLines), built the same
// way, so the journal names a request as the client does: a field goes only when it says
// something the server's default does not.
const trackLanguage = (language) => (language === NARRATION_LOCALE ? {} : { language });

/** The JSON body `transcribeClip` sends for one clip. */
export const transcribeBody = ({ wav, terms = [], language = NARRATION_LOCALE }) => ({ audio: Buffer.from(wav).toString("base64"), ...(terms.length ? { terms } : {}), ...trackLanguage(language) });

/** The JSON body `judgeLines` sends for one Jev call. */
export const judgeBody = ({ lines, language = NARRATION_LOCALE }) => ({ lines, ...trackLanguage(language) });

/** Why an answer `send` returned cannot be saved as confirmed, or null. */
function unusable(result) {
  if (!result || !(Buffer.isBuffer(result.wav) || result.wav instanceof Uint8Array)) return "the answer has no WAV bytes";
  try {
    requireNarrationFormat(parseWav(result.wav));
    return null;
  } catch (error) {
    return `the answer is not narration audio: ${error.message}`;
  }
}

// A transcript or Jev's results are kept in the confirmed entry itself, bound by their sha256.
const inline = (answer) => ({ answer, answer_sha256: sha256(JSON.stringify(answer)) });
const intact = (entry) => entry.answer !== undefined && sha256(JSON.stringify(entry.answer)) === entry.answer_sha256;
const preview = (text, max = 40) => (text.length > max ? `${text.slice(0, max)}…` : text);

// What each paid route (client.mjs) records of its body, which answer it saves, and how the
// answer comes back from disk: `load` gives null when it is missing or changed.
const SPEECH = {
  path: "speech",
  record: (body) => body,
  bound: (request, sha) => requestSha256(request) === sha,
  problem: unusable,
  save(dir, sha, result) {
    const wav = Buffer.from(result.wav);
    durableWrite(wavFile(dir, sha), wav);
    return { wav_sha256: sha256(wav), wav_bytes: wav.length, billable: Number(result.billable) || 0 };
  },
  load(dir, sha, entry) {
    const file = wavFile(dir, sha);
    const wav = existsSync(file) ? readFileSync(file) : null;
    return wav && wav.length === entry.wav_bytes && sha256(wav) === entry.wav_sha256 ? { wav, billable: 0, reused: true } : null;
  },
  describe(request) {
    const text = (request?.segments ?? []).flatMap((segment) => segment.parts ?? []).map((part) => part.text ?? "").join("");
    return `${request?.voice ?? "?"} "${preview(text)}"`;
  },
};

const TRANSCRIBE = {
  path: "speech/transcribe",
  // The clip goes out as base64: the entry keeps its sha256 and size, and the file name the body's.
  record({ audio, ...rest }) {
    const bytes = Buffer.from(audio, "base64");
    return { audio_sha256: sha256(bytes), audio_bytes: bytes.length, ...rest };
  },
  bound: (request) => SHA256.test(request?.audio_sha256 ?? "") && Number.isInteger(request.audio_bytes),
  problem: (text) => (typeof text === "string" ? null : "the answer has no transcript"),
  save: (_dir, _sha, text) => inline({ text }),
  load: (_dir, _sha, entry) => (intact(entry) && typeof entry.answer?.text === "string" ? entry.answer.text : null),
  describe: (request) => `${TRANSCRIBE.path} ${request?.audio_bytes} bytes of audio${request?.terms ? `, terms ${request.terms.join(" ")}` : ""}${request?.language ? ` (${request.language})` : ""}`,
};

const JUDGE = {
  path: "speech/judge",
  record: (body) => body,
  bound: (request, sha) => requestSha256(request) === sha,
  problem: (verdicts) => (verdicts instanceof Map ? null : "the answer has no Jev results"),
  // JSON has no NaN: a probability the client could not read is kept by its name, read back as it.
  save: (_dir, _sha, verdicts) => inline({ results: [...verdicts].map(([id, noul]) => ({ id, noul: Number.isFinite(noul) ? noul : String(noul) })) }),
  load: (_dir, _sha, entry) => (intact(entry) && Array.isArray(entry.answer?.results) ? new Map(entry.answer.results.map((result) => [result?.id, Number(result?.noul)])) : null),
  describe: (request) => {
    const ids = (request?.lines ?? []).map((line) => line?.id);
    return `${JUDGE.path} ${ids.length} lines ${preview(ids.join(", "))}${request?.language ? ` (${request.language})` : ""}`;
  },
};

const ROUTES = new Map([SPEECH, TRANSCRIBE, JUDGE].map((route) => [route.path, route]));

/**
 * An entry as written, or `{ status: "unreadable" }` when its file is there and is not one (or is
 * another route's than `expected`); null when absent. An entry that names no route is a synthesis.
 */
function readEntry(dir, sha, expected = null) {
  const file = entryFile(dir, sha);
  if (!existsSync(file)) return null;
  try {
    const entry = JSON.parse(readFileSync(file, "utf8"));
    const route = ROUTES.get(entry?.path ?? SPEECH.path);
    const waits = entry?.status !== "waiting" || WAIT_ID.test(entry.wait_id ?? "");
    if (entry?.schema_version === 1 && entry.request_sha256 === sha && STATUSES.has(entry.status) && waits && route?.bound(entry.request, sha) && (!expected || route === expected)) return entry;
  } catch {
    // An unreadable entry still says something was recorded: it holds like a sent one.
  }
  return { status: "unreadable", request_sha256: sha };
}

/** The one-line SPEECH_UNCERTAIN the CLIs print and the worker blocks a video on (automation/flow.mjs). */
function holdError(route, dir, sha, what, status = 0) {
  const message = `POST /api/video/${route} ${oneLine(what)}; it may have run and been charged, so it is not sent again. Once the provider's usage shows whether it was, clear it with: node ${SELF} forget --dir "${dir}" --sha ${sha} (${SPEECH_UNCERTAIN}, request sha256 ${sha})`;
  return Object.assign(new SpeechError(message, { status, code: SPEECH_UNCERTAIN, who: "owner" }), { path: route, requestSha256: sha, journal: dir });
}

/**
 * The code of a request this run left waiting and another run sent meanwhile: this one stops
 * without sending it, the service's (exit 4), and a later run takes the other's answer.
 */
export const SPEECH_TAKEN_OVER = "video_speech_taken_over";

function takenOver(route, dir, sha) {
  const message = `POST /api/video/${route} was sent by another run while this one waited to send it again, so it is not sent twice; run again once that run is done (${SPEECH_TAKEN_OVER}, request sha256 ${sha})`;
  return Object.assign(new SpeechError(message, { code: SPEECH_TAKEN_OVER }), { path: route, requestSha256: sha, journal: dir });
}

/**
 * The journal in `dir`. `wrap(send)` gives a `send` with the same contract (body → { wav,
 * billable }); an answer taken from disk has `reused: true` and bills nothing in this run.
 * `wrapTranscribe` and `wrapJudge` do the same for client.mjs's `transcribeClip` and `judgeLines`
 * (or a stand-in with their contract): the transcript or the Map of Jev's probabilities, from
 * disk when an earlier run bought it. `reused` counts the answers taken from disk.
 * `release()` drops the confirmed entries handed out so far: call it once their results are saved.
 */
export function openSpeechJournal(dir, { now = () => new Date(), write = durableWrite, create = createOnce, processAlive: alive = processAlive } = {}) {
  const stamp = () => now().toISOString();
  // Byte hashes identify the consumed generation, not merely its same-body request key.
  const handed = new Map();

  function hold(entry, why) {
    try {
      write(entryFile(dir, entry.request_sha256), json({ ...entry, status: "held", held_at: stamp(), why: oneLine(why) }));
    } catch {
      // The sent entry stays, and holds as well.
    }
  }

  /** A confirmed answer from disk, or the hold an entry that is not one makes. */
  function saved(route, sha, entry, request) {
    if (entry.status === "confirmed") {
      const file = entryFile(dir, sha);
      let snapshot;
      try {
        if (!regular(file)) throw new Error("not an ordinary receipt");
        snapshot = readFileSync(file);
        if (!isDeepStrictEqual(JSON.parse(snapshot.toString("utf8")), entry) || !isDeepStrictEqual(entry.request, request)) throw new Error("another receipt");
      } catch { throw holdError(route.path, dir, sha, "has a confirmed receipt that changed before reuse"); }
      const answer = route.load(dir, sha, entry);
      if (!regular(file) || !readFileSync(file).equals(snapshot)) throw holdError(route.path, dir, sha, "has a confirmed receipt that changed during reuse");
      if (answer !== null) {
        if (!handed.has(sha)) journal.reused += 1;
        handed.set(sha, sha256(snapshot));
        return answer;
      }
      hold(entry, "its saved answer is missing or changed on disk");
      throw holdError(route.path, dir, sha, "has a saved answer that is missing or changed on disk");
    }
    if (entry.status === "sent") {
      const recovered = recoverAnswer(route, dir, sha, entry, request, { create, processAlive: alive });
      if (recovered) {
        if (!handed.has(sha)) journal.reused += 1;
        handed.set(sha, recovered.entryHash);
        return recovered.answer;
      }
      throw holdError(route.path, dir, sha, `was sent at ${entry.sent_at} by a run that recorded no answer that can be safely reused (it may still be running)`);
    }
    if (entry.status === "held") throw holdError(route.path, dir, sha, `is held in the speech journal since ${entry.held_at}: ${entry.why}`);
    throw holdError(route.path, dir, sha, "has a speech journal entry that cannot be read");
  }

  /**
   * Make the entry `sent` (this run's) again where it still says waiting with `waitId`: true when
   * this run may send. The claim file makes the read and the write one step against other runs.
   */
  function resume(sha, waitId, sent) {
    const claim = claimFile(dir, sha, waitId);
    if (!create(claim, "")) return false;
    try {
      const current = readEntry(dir, sha);
      if (current?.status !== "waiting" || current.wait_id !== waitId) return false;
      write(entryFile(dir, sha), json(sent));
      return true;
    } finally {
      rmSync(claim, { force: true });
    }
  }

  async function sendOnce(route, send, sent, initialSentBytes) {
    const sha = sent.request_sha256;
    let entry = sent;
    let sentBytes = initialSentBytes;
    let waitId = null;
    // client.mjs tells of each wait between two tries; every answer before one settled the request.
    const waits = {
      waiting({ status, code, ms }) {
        const id = randomUUID();
        const why = `${status ? `HTTP ${status}${code ? ` ${code}` : ""}` : "the API was not reached"}; sent again in ${Math.ceil(ms / 1000)} s`;
        // A write that fails may still have landed (the rename, then a failed fsync), and a
        // waiting entry is one another run sends: the request stops here, before the sleep, and
        // sendOnce holds it. Nothing is sent again by this run.
        try {
          write(entryFile(dir, sha), json({ ...entry, status: "waiting", wait_id: id, waiting_at: stamp(), why }));
        } catch (error) {
          throw new Error(`the journal could not record its wait: ${error.message}`, { cause: error });
        }
        waitId = id;
      },
      resending() {
        if (waitId === null) return;
        const id = waitId;
        waitId = null;
        entry = { ...sent, sent_at: stamp() };
        if (!resume(sha, id, entry)) throw takenOver(route.path, dir, sha);
        // A settled refusal can change the sent timestamp before the actual successful POST.
        // Bind its answer to that complete final sent receipt, never the initial attempt's.
        sentBytes = Buffer.from(json(entry));
      },
    };
    let result;
    try {
      result = await withPaidWaits(waits, send);
    } catch (error) {
      // Another run's now: its entry is left as it is.
      if (error?.code === SPEECH_TAKEN_OVER) throw error;
      if (error instanceof SpeechError && error.code !== SPEECH_UNCERTAIN) {
        // Settled by client.mjs: it never left, the API refused it, or the API answered for it.
        rmSync(entryFile(dir, sha), { force: true });
        throw error;
      }
      const why = error instanceof SpeechError ? `no usable answer came back (${error.why ?? error.message})` : `the run failed while it was out (${error?.message ?? error})`;
      hold(entry, why);
      if (!(error instanceof SpeechError)) throw error;
      throw holdError(route.path, dir, sha, `was sent and ${why}`, error.status);
    }
    const problem = route.problem(result);
    if (problem) {
      hold(entry, problem);
      throw holdError(route.path, dir, sha, `was answered, and ${problem}`);
    }
    const answer = route.save(dir, sha, result);
    const confirmedBytes = Buffer.from(json({ ...entry, status: "confirmed", confirmed_at: stamp(), sent_sha256: sha256(sentBytes), ...answer }));
    stageAnswer(route.path, dir, sha, sentBytes, confirmedBytes, create);
    if (!regular(entryFile(dir, sha)) || !readFileSync(entryFile(dir, sha)).equals(sentBytes)) {
      throw holdError(route.path, dir, sha, "has a sent receipt that changed while its complete answer was received");
    }
    write(entryFile(dir, sha), confirmedBytes);
    handed.set(sha, sha256(confirmedBytes));
    // The fsynced canonical confirmation now contains the complete answer. Normal success
    // keeps the original journal shape; only a failed promotion needs the staged confirmation.
    try {
      const file = entryFile(dir, sha);
      const stage = answerFile(dir, sha);
      if (regular(file) && readFileSync(file).equals(confirmedBytes) && regular(stage)) {
        const retained = JSON.parse(readFileSync(stage, "utf8"));
        if (retained.sent_sha256 === sha256(sentBytes) && retained.confirmed_sha256 === sha256(confirmedBytes)
          && regular(file) && readFileSync(file).equals(confirmedBytes)) rmSync(stage);
      }
    } catch { /* Retained complete evidence is safe to keep. */ }
    return result;
  }

  /** `send()` once for `body` on `route`, or its answer or hold from disk. */
  async function journaled(route, body, send) {
    const sha = requestSha256(body);
    const request = route.record(body);
    mkdirSync(dir, { recursive: true });
    // Another run may release or forget an entry between the two steps: look once more.
    for (let attempt = 0; attempt < 2; attempt++) {
      if (!existsSync(entryFile(dir, sha)) && existsSync(answerFile(dir, sha))) {
        throw holdError(route.path, dir, sha, "has a retained answer without its original sent receipt");
      }
      const sent = { schema_version: 1, path: route.path, request_sha256: sha, request, status: "sent", sent_at: stamp(), generation: randomUUID(), producer_pid: process.pid };
      const sentBytes = Buffer.from(json(sent));
      if (create(entryFile(dir, sha), sentBytes)) return sendOnce(route, send, sent, sentBytes);
      const entry = readEntry(dir, sha, route);
      // Left mid-wait: every answer it had settled it, so this run sends it, unless another run
      // claims it first.
      if (entry?.status === "waiting") {
        if (existsSync(answerFile(dir, sha))) throw holdError(route.path, dir, sha, "has a retained answer beside a waiting receipt");
        if (resume(sha, entry.wait_id, sent)) return sendOnce(route, send, sent, sentBytes);
        continue;
      }
      if (entry) return saved(route, sha, entry, request);
    }
    throw holdError(route.path, dir, sha, "has a speech journal entry another run keeps changing");
  }

  const journal = {
    dir,
    /** Answers taken from disk in this run: paid for by an earlier one, not bought again. */
    reused: 0,
    wrap(send) {
      return async (body) => journaled(SPEECH, body, () => send(body));
    },
    wrapTranscribe(transcribe) {
      return async ({ wav, terms = [], language = NARRATION_LOCALE, ...options }) =>
        journaled(TRANSCRIBE, transcribeBody({ wav, terms, language }), () => transcribe({ ...options, wav, terms, language }));
    },
    wrapJudge(judge) {
      return async ({ lines, language = NARRATION_LOCALE, ...options }) => journaled(JUDGE, judgeBody({ lines, language }), () => judge({ ...options, lines, language }));
    },
    release() {
      for (const [sha, consumed] of handed) {
        const file = entryFile(dir, sha);
        // A stale reader must not remove a newer intentional same-body retake.
        if (!regular(file) || sha256(readFileSync(file)) !== consumed) continue;
        const stage = answerFile(dir, sha);
        if (regular(stage)) {
          try {
            const retained = JSON.parse(readFileSync(stage, "utf8"));
            const current = readEntry(dir, sha);
            const original = current.status === "sent" ? consumed : current.sent_sha256;
            if (retained.sent_sha256 === original) rmSync(stage);
          } catch { /* Unreadable retained evidence holds rather than being silently deleted. */ }
        }
        // The entry first: a WAV left without one is unused, an entry left without its WAV holds.
        rmSync(file, { force: true });
        rmSync(wavFile(dir, sha), { force: true });
      }
      handed.clear();
    },
  };
  return journal;
}

/**
 * Every entry in `dir`, oldest first: { sha, path, status, claimed, sent_at, waiting_at, held_at,
 * confirmed_at, why, voice, text, about }; `about` is the request in a few words, and `claimed` a
 * waiting entry a stopped run left its claim beside.
 */
export function listSpeechJournal(dir) {
  if (!existsSync(dir)) return [];
  return readdirSync(dir)
    .filter((name) => name.endsWith(".json") && SHA256.test(name.slice(0, -5)))
    .map((name) => {
      const sha = name.slice(0, -5);
      const entry = readEntry(dir, sha);
      const route = entry.status === "unreadable" ? null : ROUTES.get(entry.path ?? SPEECH.path);
      const text = (entry.request?.segments ?? []).flatMap((segment) => segment.parts ?? []).map((part) => part.text ?? "").join("");
      // A claim left beside a waiting entry: a run stopped while it took the entry back, before it
      // wrote it as sent, so nothing of it went out. Every run holds it until it is forgotten.
      const claimed = entry.status === "waiting" && existsSync(claimFile(dir, sha, entry.wait_id));
      return { sha, path: route?.path ?? null, status: entry.status, claimed, sent_at: entry.sent_at ?? null, waiting_at: entry.waiting_at ?? null, held_at: entry.held_at ?? null, confirmed_at: entry.confirmed_at ?? null, why: entry.why ?? null, voice: entry.request?.voice ?? null, text, about: (route ?? SPEECH).describe(entry.request) };
    })
    .sort((a, b) => String(a.sent_at).localeCompare(String(b.sent_at)));
}

/** Drop one entry and its answer, whatever it says: the next run asking for that body sends it. */
export function forgetSpeechJournal(dir, sha) {
  if (!SHA256.test(sha ?? "")) throw new UsageError("--sha must be a request sha256 (64 hex characters)");
  const entry = readEntry(dir, sha);
  if (!entry) throw new UsageError(`no entry ${sha} in ${dir}`);
  const stage = answerFile(dir, sha);
  if (regular(stage)) {
    try {
      const retained = JSON.parse(readFileSync(stage, "utf8"));
      const original = entry.status === "sent" ? sha256(readFileSync(entryFile(dir, sha))) : entry.sent_sha256;
      if (retained.sent_sha256 === original) rmSync(stage);
    } catch { /* Keep an unknown generation as evidence; it cannot authorize another POST. */ }
  }
  rmSync(entryFile(dir, sha), { force: true });
  rmSync(wavFile(dir, sha), { force: true });
  for (const name of readdirSync(dir)) if (name.startsWith(`${sha}.`) && name.endsWith(".claim")) rmSync(path.join(dir, name), { force: true });
  return entry;
}

const USAGE = `Usage: node ${SELF} list --dir D
       node ${SELF} forget --dir D --sha S
D is the journal a hold names (a video's <workdir>/audio/${JOURNAL_DIR}, or a Short's). forget clears
one entry: the next run that asks for that request sends it again and may be charged again.
`;

/** The command line: list a journal, or forget one entry. Exit 0, or 2 for a usage error. */
export function main(args, { stdout = process.stdout, stderr = process.stderr } = {}) {
  try {
    const [command, ...rest] = args;
    const values = parseArgs({ args: rest, options: { dir: { type: "string" }, sha: { type: "string" } }, strict: true }).values;
    if (!["list", "forget"].includes(command) || !values.dir) throw new UsageError(USAGE.trimEnd());
    const dir = path.resolve(values.dir);
    if (command === "forget") {
      const entry = forgetSpeechJournal(dir, values.sha);
      stdout.write(`forgot ${values.sha} (${entry.status}); the next run that asks for this request sends it again\n`);
      return 0;
    }
    const entries = listSpeechJournal(dir);
    if (!entries.length) stdout.write(`no entries in ${dir}\n`);
    for (const entry of entries) {
      const when = entry.held_at ?? entry.confirmed_at ?? entry.waiting_at ?? entry.sent_at ?? "?";
      stdout.write(`${entry.sha} ${entry.claimed ? "claimed" : entry.status} ${when} ${entry.about}${entry.why ? ` (${entry.why})` : ""}\n`);
    }
    const holds = entries.filter((entry) => !["confirmed", "waiting"].includes(entry.status)).length;
    if (holds) stdout.write(`${holds} held: check the provider's usage, then forget each with --sha\n`);
    const claimed = entries.filter((entry) => entry.claimed).length;
    if (claimed) stdout.write(`${claimed} claimed by a run that stopped while taking it back: nothing of it went out, and every run holds it until you forget it with --sha\n`);
    const waiting = entries.filter((entry) => entry.status === "waiting" && !entry.claimed).length;
    if (waiting) stdout.write(`${waiting} waiting: nothing of it is out, and the next run that asks for it sends it\n`);
    return 0;
  } catch (error) {
    if (!(error instanceof UsageError) && !String(error?.code).startsWith("ERR_PARSE_ARGS_")) throw error;
    stderr.write(`${error.message}\n`);
    return 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) process.exitCode = main(process.argv.slice(2));
