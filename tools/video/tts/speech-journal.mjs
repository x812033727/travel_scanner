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
//   <sha>.wav   a synthesis's confirmed answer as `send` returned it, saved before the entry says so.
//
// A run asking for the same body takes a confirmed answer from disk instead of buying it again,
// and stops on a sent or held one without sending it (SPEECH_UNCERTAIN, the owner's, exit 3): it
// may have run and been charged, and only `forget` clears it. A body that differs in any byte
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
import { closeSync, existsSync, fsyncSync, linkSync, mkdirSync, openSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { atomicWrite, UsageError } from "../core/paths.mjs";
import { NARRATION_LOCALE } from "../core/schema.mjs";
import { SPEECH_UNCERTAIN, SpeechError } from "./client.mjs";
import { parseWav, requireNarrationFormat } from "./wav.mjs";

/**
 * The journal's directory name, beside the cache it protects: <workdir>/audio/speech-journal for
 * tts, dub and check-audio; a Short's <build>/speech-journal for its check.
 */
export const JOURNAL_DIR = "speech-journal";
const SELF = "tools/video/tts/speech-journal.mjs";
const SHA256 = /^[0-9a-f]{64}$/;
const STATUSES = new Set(["sent", "held", "confirmed"]);

const sha256 = (data) => createHash("sha256").update(data).digest("hex");
/** What client.mjs names a request by: the sha256 of its JSON body as sent. */
export const requestSha256 = (body) => sha256(JSON.stringify(body));
const entryFile = (dir, sha) => path.join(dir, `${sha}.json`);
const wavFile = (dir, sha) => path.join(dir, `${sha}.wav`);
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
    if (entry?.schema_version === 1 && entry.request_sha256 === sha && STATUSES.has(entry.status) && route?.bound(entry.request, sha) && (!expected || route === expected)) return entry;
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
 * The journal in `dir`. `wrap(send)` gives a `send` with the same contract (body → { wav,
 * billable }); an answer taken from disk has `reused: true` and bills nothing in this run.
 * `wrapTranscribe` and `wrapJudge` do the same for client.mjs's `transcribeClip` and `judgeLines`
 * (or a stand-in with their contract): the transcript or the Map of Jev's probabilities, from
 * disk when an earlier run bought it. `reused` counts the answers taken from disk.
 * `release()` drops the confirmed entries handed out so far: call it once their results are saved.
 */
export function openSpeechJournal(dir, { now = () => new Date() } = {}) {
  const stamp = () => now().toISOString();
  const handed = new Set();

  function hold(entry, why) {
    try {
      durableWrite(entryFile(dir, entry.request_sha256), json({ ...entry, status: "held", held_at: stamp(), why: oneLine(why) }));
    } catch {
      // The sent entry stays, and holds as well.
    }
  }

  /** A confirmed answer from disk, or the hold an entry that is not one makes. */
  function saved(route, sha, entry) {
    if (entry.status === "confirmed") {
      const answer = route.load(dir, sha, entry);
      if (answer !== null) {
        if (!handed.has(sha)) journal.reused += 1;
        handed.add(sha);
        return answer;
      }
      hold(entry, "its saved answer is missing or changed on disk");
      throw holdError(route.path, dir, sha, "has a saved answer that is missing or changed on disk");
    }
    if (entry.status === "sent") throw holdError(route.path, dir, sha, `was sent at ${entry.sent_at} by a run that recorded no answer (it may still be running)`);
    if (entry.status === "held") throw holdError(route.path, dir, sha, `is held in the speech journal since ${entry.held_at}: ${entry.why}`);
    throw holdError(route.path, dir, sha, "has a speech journal entry that cannot be read");
  }

  async function sendOnce(route, send, entry) {
    const sha = entry.request_sha256;
    let result;
    try {
      result = await send();
    } catch (error) {
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
    durableWrite(entryFile(dir, sha), json({ ...entry, status: "confirmed", confirmed_at: stamp(), ...answer }));
    handed.add(sha);
    return result;
  }

  /** `send()` once for `body` on `route`, or its answer or hold from disk. */
  async function journaled(route, body, send) {
    const sha = requestSha256(body);
    const request = route.record(body);
    mkdirSync(dir, { recursive: true });
    // Another run may release or forget an entry between the two steps: look once more.
    for (let attempt = 0; attempt < 2; attempt++) {
      const sent = { schema_version: 1, path: route.path, request_sha256: sha, request, status: "sent", sent_at: stamp() };
      if (createOnce(entryFile(dir, sha), json(sent))) return sendOnce(route, send, sent);
      const entry = readEntry(dir, sha, route);
      if (entry) return saved(route, sha, entry);
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
      for (const sha of handed) {
        // The entry first: a WAV left without one is unused, an entry left without its WAV holds.
        rmSync(entryFile(dir, sha), { force: true });
        rmSync(wavFile(dir, sha), { force: true });
      }
      handed.clear();
    },
  };
  return journal;
}

/**
 * Every entry in `dir`, oldest first: { sha, path, status, sent_at, held_at, confirmed_at, why,
 * voice, text, about }; `about` is the request in a few words.
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
      return { sha, path: route?.path ?? null, status: entry.status, sent_at: entry.sent_at ?? null, held_at: entry.held_at ?? null, confirmed_at: entry.confirmed_at ?? null, why: entry.why ?? null, voice: entry.request?.voice ?? null, text, about: (route ?? SPEECH).describe(entry.request) };
    })
    .sort((a, b) => String(a.sent_at).localeCompare(String(b.sent_at)));
}

/** Drop one entry and its answer, whatever it says: the next run asking for that body sends it. */
export function forgetSpeechJournal(dir, sha) {
  if (!SHA256.test(sha ?? "")) throw new UsageError("--sha must be a request sha256 (64 hex characters)");
  const entry = readEntry(dir, sha);
  if (!entry) throw new UsageError(`no entry ${sha} in ${dir}`);
  rmSync(entryFile(dir, sha), { force: true });
  rmSync(wavFile(dir, sha), { force: true });
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
      const when = entry.held_at ?? entry.confirmed_at ?? entry.sent_at ?? "?";
      stdout.write(`${entry.sha} ${entry.status} ${when} ${entry.about}${entry.why ? ` (${entry.why})` : ""}\n`);
    }
    const holds = entries.filter((entry) => entry.status !== "confirmed").length;
    if (holds) stdout.write(`${holds} held: check the provider's usage, then forget each with --sha\n`);
    return 0;
  } catch (error) {
    if (!(error instanceof UsageError) && !String(error?.code).startsWith("ERR_PARSE_ARGS_")) throw error;
    stderr.write(`${error.message}\n`);
    return 2;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) process.exitCode = main(process.argv.slice(2));
