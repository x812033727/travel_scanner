// `dub`: one YouTube audio track per locale (docs/videos/DUBS.md). The narration voice reads the
// caption translation, line by line through the same server and cache as `tts`; the clips are laid
// into the zh-TW timeline's slide windows, sped up a little where a translation runs long, and the
// track is written with the video's own loudness, and, when the script names music or a
// sound-effect set (docs/videos/ILLUSTRATED.md), with the same bed and the cut's effects track
// under the voice as final.mp4 has. A window still over at MAX_TEMPO by a few frames is let
// through, into the pause after it or sped up alone a little further (plan.mjs absorbOverruns);
// one over by more is reported with a character budget per line, for the translator to shorten,
// and no track is written for that locale until it does. A retake (`--redo`) whose window is
// still over after that is given back its earlier take with `--keep-fitting`, once the worker has
// no shortening round left.
import { existsSync, mkdirSync, readFileSync, renameSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { measureMixArgs, mixArgs } from "../assemble/drama.mjs";
import { verifyBrandingAssets, wrapAudio } from "../assemble/branding.mjs";
import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { musicInputs, sfxInputs } from "../assemble/sound.mjs";
import { isDrama, mixHash, resolveMusic, resolveSfx, sfxHash } from "../core/drama.mjs";
import { appliedBranding, brandingCurrent, presentationTimeline, readBranding } from "../core/branding.mjs";
import { verifiedManualPresentation } from "../review/renewal-handoff.mjs";
import { atomicWrite, readJson, resolveWorkBase, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { requireProjectLease } from "../core/project-lease.mjs";
import { eachLine, LOCALES } from "../core/schema.mjs";
import { ARTIFACTS, dubArtifacts, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { FPS, SAMPLES_PER_FRAME, speechHash } from "../core/timeline.mjs";
import { SpeechError, speechStatus, synthesize } from "../tts/client.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { billableForRequest } from "../tts/requests.mjs";
import { JOURNAL_DIR, openSpeechJournal } from "../tts/speech-journal.mjs";
import { flaggedLines, lineBody, synthesizeLines, synthesizeRequest } from "../tts/synthesis.mjs";
import { encodeWav, parseWav, requireNarrationFormat } from "../tts/wav.mjs";
import { CODECS, encodeArgs, measureLoudnessArgs, parseLoudnorm, stretchArgs } from "./encode.mjs";
import {
  DEFAULT_FORMAT, DUB_FORMATS, MAX_TEMPO,
  absorbOverruns, assembleTrack, bareWindow, defaultDubLocales, defaultRate, dubLocales, dubRequests, estimatedLengths, layoutDub, layoutDubTolerant, measureRate, overrunSummary, placeLines, shrinkBudgets, speechFingerprint, translationHash, windowLimit,
} from "./plan.mjs";

// When a stretched window still sticks out (atempo rounds), the next try is this much faster.
const TEMPO_RETRY_STEP = 0.02;

function options(args) {
  const values = parseArgs({
    args,
    options: {
      slug: { type: "string" },
      file: { type: "string" },
      workdir: { type: "string" },
      locale: { type: "string" },
      format: { type: "string", default: DEFAULT_FORMAT },
      "dry-run": { type: "boolean" },
      redo: { type: "string" },
      "keep-fitting": { type: "boolean" },
      force: { type: "boolean" },
      "line-by-line": { type: "boolean" },
      style: { type: "string" },
    },
    strict: true,
  }).values;
  if (!values.slug && !values.file) throw new UsageError("dub needs --slug (or --file for an example outside docs/videos)");
  // Which locales can be dubbed depends on the narration language, so the list is checked once the video is read.
  const locales = values.locale ? values.locale.split(",").map((locale) => locale.trim()).filter(Boolean) : null;
  for (const locale of locales ?? []) if (!LOCALES.includes(locale)) throw new UsageError(`--locale must be among ${LOCALES.join(", ")}`);
  if (!DUB_FORMATS.includes(values.format)) throw new UsageError(`--format must be one of ${DUB_FORMATS.join(", ")}`);
  if (values["keep-fitting"] && !values.redo) throw new UsageError("--keep-fitting goes with --redo: it keeps the earlier take of a retaken line that no longer fits its window");
  return { ...values, locales };
}

function requireCredentials(ctx) {
  const credentials = readCredentials({ env: ctx.env, home: ctx.home });
  if (!credentials.token) throw new SpeechError("no video tool token yet: run `node tools/video/cli.mjs login` and allow it on the admin card", { who: "owner" });
  return credentials;
}

const clientOptions = (ctx, credentials) => ({ site: credentials.site, token: credentials.token, fetchImpl: ctx.fetch ?? globalThis.fetch, ...(ctx.sleep ? { sleep: ctx.sleep } : {}) });

/** Gemini characters left this month, or null when the server sets no limit. */
function geminiRemaining(status) {
  return status.gemini_monthly_limit > 0 && status.gemini_used !== null && status.gemini_used !== undefined ? status.gemini_monthly_limit - status.gemini_used : null;
}

/** The rate a locale's last fit measured, else the estimate from the narration's own rate. */
export function rateFor(fit, locale, doc, timeline) {
  return fit?.rates?.measured ?? defaultRate(locale, doc, timeline);
}

/** Everything one locale's dub is made from, before any audio: the script, the requests, the cache. */
function prepare(project, locale, values, workdir) {
  // project.lexicon is filtered for the source narration; dubRequests filters the shelf's raw
  // dictionary for the target, so a Chinese dub gets its aliases back. Status plans the same way.
  const { script, missing, requests } = dubRequests(project, locale, values.style);
  const texts = new Map();
  for (const { line } of eachLine(script)) texts.set(line.id, line.text);
  const files = dubArtifacts(workdir, locale);
  const cache = readJson(files.cache, { lines: {}, stretched: {} });
  cache.stretched ??= {};
  return {
    locale, script, missing, requests, texts, files, cache, hash: translationHash(script), style: script.voice.style,
    // What the voice is asked to say, for status and upload to compare (speechCurrent), and the
    // --style it was asked in, so a hand-styled dub is compared in its own style.
    fingerprint: speechFingerprint(requests), styleOverride: values.style ?? null,
  };
}

const readClip = (file) => requireNarrationFormat(parseWav(readFileSync(file)));

/**
 * Stretch a window's clips until they fit, or until `maxTempo` (MAX_TEMPO; MAX_TEMPO_OVERRUN
 * when absorbOverruns lets one window past it). atempo's output is a few milliseconds off the
 * exact division, so the layout is redone with the stretched lengths.
 */
async function fitWindow(window, originals, lengths, clips, dub, ffmpeg, values, { maxTempo = MAX_TEMPO } = {}) {
  const limit = windowLimit(window);
  // The laid-out window carries line objects; the placer takes the window as windowsOf gives it.
  const bare = bareWindow(window);
  let tempo = window.tempo;
  for (;;) {
    const stretched = new Map(lengths);
    for (const line of window.lines) {
      const raw = path.join(dub.files.audio, `${line.id}.wav`);
      const file = path.join(dub.files.audio, `${line.id}.x${tempo.toFixed(2)}.wav`);
      const key = `${dub.cache.lines[line.id]}@${tempo.toFixed(2)}`;
      if (values.force || dub.cache.stretched[line.id] !== key || !existsSync(file)) {
        await ffmpeg.run(ffmpeg.tools.ffmpeg, stretchArgs(raw, tempo, file));
        dub.cache.stretched[line.id] = key;
        atomicWrite(dub.files.cache, `${JSON.stringify(dub.cache, null, 2)}\n`);
      }
      const clip = readClip(file);
      clips.set(`${line.id}@${tempo.toFixed(2)}`, clip);
      stretched.set(line.id, Math.max(1, clip.length));
    }
    const lines = placeLines(bare, originals, stretched, { keepStarts: false }).map((line) => ({ ...line, tempo }));
    const end = lines.at(-1).end_frame;
    if (end <= limit) return { ...window, lines, tempo, kept_starts: false, over: false, slack_frames: limit - end };
    const next = Math.round((tempo + TEMPO_RETRY_STEP) * 100) / 100;
    if (next > maxTempo + 1e-9) return { ...window, lines, tempo, kept_starts: false, over: true, slack_frames: limit - end };
    tempo = next;
  }
}

/** The windows of fit.json and the dub's timeline: frames, tempo, slack, and how an overrun was let through. */
function fitWindows(windows) {
  return windows.map((window) => ({
    scene: window.scene, state: window.state, start_frame: window.start_frame, end_frame: window.end_frame,
    lines: window.lines.map((line) => line.id), tempo: window.tempo, slack_frames: window.slack_frames, over: window.over,
    ...(window.absorbed ? { absorbed: window.absorbed, overrun_seconds: window.overrun_seconds } : {}),
    ...(window.shifted_frames ? { shifted_frames: window.shifted_frames } : {}),
  }));
}

/**
 * The sound a dub carries under its voice (docs/videos/ILLUSTRATED.md): the music track the
 * script names, checked as `assemble` checks it, and the effects track `assemble` built for the
 * cut (build/sfx.wav) when checks.json shows it was built for this script's set and narration
 * timing; the dubbed lines sit in the zh-TW timeline's windows, so the cut's beats hold. A
 * missing music file is the owner's to put back; a cut not assembled yet only leaves the effects
 * out, and the dub's timeline records that so status marks it stale until the cut exists.
 * Returns `{ track, music, sfxFile, notes }`, all null and empty for a script naming neither.
 */
async function dubSound(doc, timeline, workdir, workBase) {
  const notes = [];
  let track = null;
  let music = null;
  if (resolveMusic(doc)) {
    const found = await musicInputs(doc, workdir, workBase);
    if (found.problem) throw new UsageError(`the dub cannot carry the music bed: ${found.problem}`);
    ({ track, music } = found);
  }
  let sfxFile = null;
  if (resolveSfx(doc)) {
    const found = await sfxInputs(doc, workBase);
    if (found.problem) throw new UsageError(`the dub cannot carry the sound effects: ${found.problem}`);
    const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
    const file = path.join(workdir, "build", "sfx.wav");
    if (checks?.sfx_hash === sfxHash(doc) && checks.speech_hash === timeline.speech_hash && existsSync(file)) sfxFile = file;
    else notes.push("no effects track yet: run assemble first, then dub again for the effects");
  }
  return { track, music, sfxFile, notes };
}

async function dubLocale(dub, project, timeline, values, ctx, options, ffmpeg, workdir, workBase) {
  const { EXIT } = ctx;
  const { locale, requests, texts, files, cache } = dub;
  if (dub.missing.length) {
    ctx.stdout.write(`${locale}: no track; ${dub.missing.length} lines have no current translation (${dub.missing.join(", ")}); run i18n-sheet and i18n-merge first\n`);
    return EXIT.lint;
  }
  const redo = values.redo ? flaggedLines(readJson(path.resolve(values.redo))) : new Set();
  const clipCurrent = (request, line) => !values.force && [line.key, request.key].includes(cache.lines[line.id]) && existsSync(path.join(files.audio, `${line.id}.wav`));
  const current = (request) => !request.lines.some((line) => redo.has(line.id)) && request.lines.every((line) => clipCurrent(request, line));
  // A whole scene goes as one request and is cut at its silences, unless only some of its lines
  // are stale or --line-by-line asks for one request a line: a split that fails is paid twice, and
  // one that passes by mistake leaves a neighbouring line inside a clip.
  const retakes = (request) => {
    const stale = request.lines.filter((line) => redo.has(line.id) || !clipCurrent(request, line));
    return stale.length && (values["line-by-line"] || stale.length < request.lines.length) ? stale : null;
  };
  const estimateFor = (request) => {
    const lines = retakes(request);
    return lines ? lines.reduce((sum, line) => sum + billableForRequest(lineBody(request, line)), 0) : billableForRequest(request.body);
  };
  const pending = requests.filter((request) => !current(request));
  const pendingEstimate = pending.reduce((sum, request) => sum + estimateFor(request), 0);
  // --keep-fitting: the take each flagged line has now, while it is current, so a retake that no
  // longer fits its window can be given back below. The worker asks for this once its shortening
  // rounds are spent: that take fitted, and only its wording was in doubt (docs/videos/DUBS.md).
  const earlier = new Map();
  if (values["keep-fitting"]) {
    for (const request of requests) {
      for (const line of request.lines) {
        if (redo.has(line.id) && clipCurrent(request, line)) earlier.set(line.id, { wav: readFileSync(path.join(files.audio, `${line.id}.wav`)), key: cache.lines[line.id] });
      }
    }
  }

  mkdirSync(files.audio, { recursive: true });
  let billable = 0;
  const fallbacks = [];
  // The video's speech journal, shared with tts (tts/speech-journal.mjs): an answer not yet in the
  // cache below is taken from disk by the next run, and a lost one holds until a person clears it.
  const journal = openSpeechJournal(path.join(workdir, ARTIFACTS.audio, JOURNAL_DIR), { now: ctx.now });
  const send = journal.wrap((body) => synthesize({ ...options, body }));
  for (const request of pending) {
    if (stopRequested(workdir)) {
      // The takes so far are in cache.json and a rerun reuses them, but fit.json, the dub's
      // timeline and its track are still the last run's (or absent): this is not a made track.
      ctx.stdout.write(`${locale}: stopped by the STOP file; ${pending.indexOf(request)} of ${pending.length} requests done, rerun to continue\n`);
      return EXIT.incomplete;
    }
    const lines = retakes(request);
    const result = lines ? { ...(await synthesizeLines(request, lines, send)), fallback: false } : await synthesizeRequest(request, send);
    billable += result.billable;
    if (result.fallback) fallbacks.push(request.id);
    for (const [id, clip] of result.clips) {
      atomicWrite(path.join(files.audio, `${id}.wav`), encodeWav(clip));
      cache.lines[id] = request.lines.find((line) => line.id === id).key;
      // A retaken line's stretched copies are of the old take.
      delete cache.stretched[id];
    }
    atomicWrite(files.cache, `${JSON.stringify(cache, null, 2)}\n`);
    journal.release();
    const done = lines ? `${lines.length} of ${request.lines.length} lines retaken` : `${request.lines.length} lines`;
    ctx.stdout.write(`${locale} ${request.id}: ${done}${result.fallback ? " (split did not match the text; synthesized line by line)" : ""}\n`);
  }

  // The clips as spoken, then the layout: which windows keep their rhythm, which pack, which speed up.
  const originals = new Map(timeline.lines.map((line) => [line.id, line]));
  // The layout runs on the takes as they stand on disk, and again after --keep-fitting gives
  // an earlier take back. A window still over by a few frames is let through (plan.mjs
  // absorbOverruns): into the pause after it, else sped up alone past MAX_TEMPO, with the next
  // real stretch each try.
  const layout = async () => {
    const clips = new Map();
    const lengths = new Map();
    for (const request of requests) {
      for (const line of request.lines) {
        const clip = readClip(path.join(files.audio, `${line.id}.wav`));
        clips.set(line.id, clip.length ? clip : new Int16Array(1));
        lengths.set(line.id, Math.max(1, clip.length));
      }
    }
    const stretch = async (window, ceiling = {}) => {
      if (!ffmpeg.tools) ffmpeg.tools = await ffmpeg.locate(ctx.env);
      return fitWindow(window, originals, lengths, clips, dub, ffmpeg, values, ceiling);
    };
    const laid = [];
    for (const window of layoutDub(timeline, lengths)) laid.push(window.tempo === 1 ? window : await stretch(window));
    const windows = await absorbOverruns(laid, originals, {
      speedUp: (window, maxTempo) => stretch({ ...window, tempo: Math.round((window.tempo + TEMPO_RETRY_STEP) * 100) / 100 }, { maxTempo }),
    });
    return { clips, lengths, windows };
  };
  let { clips, lengths, windows } = await layout();
  // A retaken line in a window that is still over, past what the tolerance above lets through,
  // gets its earlier take back (--keep-fitting), its sped-up copies with it, and the windows are
  // laid out again with the takes as they stand. A retake a few frames long keeps the new take.
  const kept = [];
  if (earlier.size && windows.some((window) => window.over)) {
    for (const window of windows.filter((window) => window.over)) {
      for (const line of window.lines) {
        const take = earlier.get(line.id);
        if (!take) continue;
        atomicWrite(path.join(files.audio, `${line.id}.wav`), take.wav);
        cache.lines[line.id] = take.key;
        delete cache.stretched[line.id];
        kept.push(line.id);
      }
    }
    if (kept.length) {
      atomicWrite(files.cache, `${JSON.stringify(cache, null, 2)}\n`);
      ({ clips, lengths, windows } = await layout());
      ctx.stdout.write(`${locale}: kept the earlier take of ${kept.join(", ")}: the retake did not fit its window\n`);
    }
  }
  const measured = measureRate(texts, lengths);
  const over = windows.filter((window) => window.over).flatMap((window) => shrinkBudgets(window, texts, { lengths }));
  const tempoMax = windows.reduce((max, window) => Math.max(max, window.tempo), 1);
  const absorbed = overrunSummary(windows);
  const fit = {
    locale,
    speech_hash: timeline.speech_hash,
    translation_hash: dub.hash,
    speech_fingerprint: dub.fingerprint,
    style_override: dub.styleOverride,
    rates: { default: defaultRate(locale, project.doc, timeline), measured },
    tempo_max: tempoMax,
    windows: fitWindows(windows),
    over,
    // The retaken lines given back their earlier take (--keep-fitting), for the worker and the batch.
    ...(values["keep-fitting"] ? { kept } : {}),
  };
  atomicWrite(files.fit, `${JSON.stringify(fit, null, 2)}\n`);
  if (over.length) {
    const windowsOver = windows.filter((window) => window.over).length;
    ctx.stdout.write(`${locale}: ${pending.length} requests synthesized (${billable} billable characters); ${windowsOver} windows do not fit even at ${MAX_TEMPO}x; shorten these lines to at most:\n`);
    for (const line of over) ctx.stdout.write(`  ${line.id}: ${line.max_chars} characters (now ${line.chars}, spoken in ${line.seconds} s; its window is ${line.window_over_seconds} s over)\n`);
    if (absorbed) ctx.stdout.write(`  ${absorbed}\n`);
    ctx.stdout.write(`  numbers and currency codes read slowly for their length: cut the words around them\n  budgets are in ${files.fit}; after i18n-merge, run dub --locale ${locale} again\n`);
    recordStage(workdir, "dub", { locale, requests: requests.length, synthesized: pending.length, billable, tempo_max: tempoMax, over: over.length, absorbed: windows.filter((window) => window.absorbed).length, ...(kept.length ? { kept } : {}) }, ctx.now());
    return EXIT.lint;
  }

  // The track: every clip at its frame, the video's length to the sample, then the upload file.
  const lines = windows.flatMap((window) => window.lines);
  const placed = new Map(lines.map((line) => [line.id, line.tempo === 1 ? clips.get(line.id) : clips.get(`${line.id}@${line.tempo.toFixed(2)}`)]));
  atomicWrite(files.narration, encodeWav(assembleTrack(timeline.total_frames, lines, placed)));
  if (!ffmpeg.tools) ffmpeg.tools = await ffmpeg.locate(ctx.env);
  const track = files.track(values.format);
  mkdirSync(path.dirname(track), { recursive: true });
  const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
  const manual = verifiedManualPresentation({ project, workdir, timeline });
  const branding = manual ?? appliedBranding(checks);
  const selection = readBranding(workdir);
  if (!manual && !brandingCurrent(checks, selection)) throw new UsageError("channel branding changed; run assemble before dub");
  const bodyTrack = branding ? path.join(files.dir, `body.${values.format}`) : track;
  const sound = await dubSound(project.doc, timeline, workdir, workBase);
  if (sound.track || sound.sfxFile) {
    // The same bed, ducking and effects as the cut's audio (assemble/cli.mjs), in the upload format.
    const totalSeconds = timeline.total_frames / FPS;
    const measured = parseLoudnorm((await ffmpeg.run(ffmpeg.tools.ffmpeg, measureMixArgs(files.narration, sound.track?.file ?? null, sound.music, totalSeconds, sound.sfxFile))).stderr);
    await ffmpeg.run(ffmpeg.tools.ffmpeg, mixArgs(files.narration, sound.track?.file ?? null, sound.music, totalSeconds, measured, bodyTrack, sound.sfxFile, CODECS[values.format]));
  } else {
    const loudness = parseLoudnorm((await ffmpeg.run(ffmpeg.tools.ffmpeg, measureLoudnessArgs(files.narration))).stderr);
    await ffmpeg.run(ffmpeg.tools.ffmpeg, encodeArgs(files.narration, loudness, bodyTrack, values.format));
  }
  if (branding) {
    const partial = path.join(files.dir, `branded.partial.${values.format}`);
    await wrapAudio({ tools: ffmpeg.tools, exec: ffmpeg.run, bodyFile: bodyTrack, bodyFrames: timeline.total_frames, branding: selection, outFile: partial, outputCodec: CODECS[values.format] });
    renameSync(partial, track);
  }
  const record = {
    locale,
    format: values.format,
    file: path.basename(track),
    speech_hash: timeline.speech_hash,
    translation_hash: dub.hash,
    // The voice and pronunciation the clips were asked for (dubs/plan.mjs speechFingerprint):
    // a changed target alias or dub voice marks the track stale for status and upload.
    speech_fingerprint: dub.fingerprint,
    style_override: dub.styleOverride,
    // What the mix carried beside the voice (docs/videos/ILLUSTRATED.md): dubsStatus compares
    // these with the script's, so a bed or a set changed after the dub marks it stale.
    mix_hash: sound.track ? mixHash(project.doc) : null,
    sfx_hash: sound.sfxFile ? sfxHash(project.doc) : null,
    voice: dub.script.voice,
    fps: FPS,
    sample_rate: FPS * SAMPLES_PER_FRAME,
    total_frames: timeline.total_frames,
    tempo_max: tempoMax,
    windows: fit.windows,
    lines,
    // The lines that kept their earlier take because the retake did not fit (--keep-fitting):
    // the languages batch names them beside the track (review/sync.mjs).
    ...(kept.length ? { kept } : {}),
  };
  atomicWrite(files.timeline, `${JSON.stringify(presentationTimeline(record, branding), null, 2)}\n`);
  recordStage(workdir, "dub", { locale, requests: requests.length, synthesized: pending.length, billable, fallbacks, tempo_max: tempoMax, over: 0, absorbed: windows.filter((window) => window.absorbed).length, file: path.basename(track), ...(kept.length ? { kept } : {}) }, ctx.now());
  const sped = windows.filter((window) => window.tempo > 1).length;
  const carried = [sound.track ? "music bed" : null, sound.sfxFile ? "sound effects" : null].filter(Boolean);
  ctx.stdout.write(`${locale}: ${pending.length} requests synthesized (${billable} billable characters), ${requests.length - pending.length} reused; ${sped} of ${windows.length} windows sped up (max ${tempoMax}x)${absorbed ? `; ${absorbed}` : ""}${carried.length ? `; with the ${carried.join(" and ")}` : ""}; ${track}\n`);
  for (const note of sound.notes) ctx.stdout.write(`  ${note}\n`);
  if (journal.reused) ctx.stdout.write(`  ${journal.reused} answers paid for by an earlier run came from the speech journal, not bought again\n`);
  if (fallbacks.length) ctx.stdout.write(`  line-by-line fallback for: ${fallbacks.join(", ")}\n`);
  return EXIT.ok;
}

async function dryRun(dubs, project, timeline, ctx, credentials) {
  for (const dub of dubs) {
    if (dub.missing.length) {
      ctx.stdout.write(`${dub.locale}: ${dub.missing.length} lines have no current translation (${dub.missing.slice(0, 8).join(", ")}${dub.missing.length > 8 ? ", …" : ""})\n`);
      continue;
    }
    const clipCurrent = (request, line) => [line.key, request.key].includes(dub.cache.lines[line.id]) && existsSync(path.join(dub.files.audio, `${line.id}.wav`));
    const pending = dub.requests.filter((request) => !request.lines.every((line) => clipCurrent(request, line)));
    const estimate = dub.requests.reduce((sum, request) => sum + billableForRequest(request.body), 0);
    const now = pending.reduce((sum, request) => sum + billableForRequest(request.body), 0);
    const rate = rateFor(readJson(dub.files.fit, null), dub.locale, project.doc, timeline);
    const windows = await layoutDubTolerant(timeline, estimatedLengths(dub.texts, rate));
    const over = windows.filter((window) => window.over).length;
    const sped = windows.filter((window) => !window.over && window.tempo > 1).length;
    const absorbed = overrunSummary(windows);
    ctx.stdout.write(`${dub.locale}: ${dub.requests.length} requests, ${pending.length} to synthesize; about ${now} billable characters now (${estimate} for the track)\n`);
    ctx.stdout.write(`  at ${rate} characters a second: ${sped} of ${windows.length} windows would speed up, ${over} would not fit even at ${MAX_TEMPO}x${absorbed ? `; ${absorbed}` : ""}\n`);
  }
  if (credentials.token) {
    const status = await speechStatus(clientOptions(ctx, credentials));
    const remaining = geminiRemaining(status);
    ctx.stdout.write(`server: Gemini ${status.gemini_configured ? "ready" : "NOT configured (admin: API 與供應商設定 → AI 服務)"}; ${remaining === null ? "no monthly limit" : `${remaining} characters left this month`}\n`);
  } else {
    ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before synthesizing\n");
  }
  return ctx.EXIT.ok;
}

async function dub(args, ctx) {
  const { EXIT } = ctx;
  const values = options(args);
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const allowed = dubLocales(project.doc);
  values.locales ??= defaultDubLocales(project.doc);
  for (const locale of values.locales) if (!allowed.includes(locale)) throw new UsageError(`--locale must be among ${allowed.join(", ")}: the video is narrated in the other one`);
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${project.doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const { doc } = project;
  if (isDrama(doc)) throw new UsageError("dub is for slides videos; a drama mixes its own audio (docs/videos/DUBS.md)");
  if (doc.voice.provider !== "gemini") throw new SpeechError(`dubs need a Gemini voice, which speaks every language; the narration voice is ${doc.voice.name}`, { who: "owner" });
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const workBase = resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  if (!timeline) throw new UsageError("no timeline.json yet; run tts first");
  if (timeline.speech_hash !== speechHash(doc, project.lexicon)) throw new UsageError("timeline.json was built for an older script; run tts again");
  const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
  const selection = readBranding(workdir);
  const manual = verifiedManualPresentation({ project, workdir, timeline });
  if (!manual && !brandingCurrent(checks, selection)) throw new UsageError("channel branding changed; run assemble before dub");
  if (!manual && checks?.branding && (checks.speech_hash !== timeline.speech_hash || checks.branding.body_frames !== timeline.total_frames)) throw new UsageError("branded cut was made for another body timeline; run assemble before dub");
  const dubs = values.locales.map((locale) => prepare(project, locale, values, workdir));

  if (values["dry-run"]) return dryRun(dubs, project, timeline, ctx, readCredentials({ env: ctx.env, home: ctx.home }));

  const ffmpeg = { locate: ctx.ffmpeg?.locate ?? locateFfmpeg, run: ctx.ffmpeg?.run ?? runTool, tools: null };
  if (selection) {
    ffmpeg.tools = await ffmpeg.locate(ctx.env);
    await verifyBrandingAssets(selection, { tools: ffmpeg.tools, exec: ffmpeg.run });
  }

  // Not while another producer holds the project (core/project-lease.mjs); the worker's unit holds it already.
  requireProjectLease(workdir, { owner: "dub", now: ctx.now, as: (error) => new SpeechError(error.message, { code: error.code, who: "owner" }) });
  const credentials = requireCredentials(ctx);
  const clientOpts = clientOptions(ctx, credentials);
  const status = await speechStatus(clientOpts);
  if (!status.gemini_configured) throw new SpeechError("the site has no Gemini key yet (admin: API 與供應商設定 → AI 服務)", { who: "owner" });
  const remaining = geminiRemaining(status);
  const needed = dubs.filter((dub) => !dub.missing.length).reduce((sum, dub) => sum + dub.requests.filter((request) => !request.lines.every((line) => [line.key, request.key].includes(dub.cache.lines[line.id]) && existsSync(path.join(dub.files.audio, `${line.id}.wav`)))).reduce((inner, request) => inner + billableForRequest(request.body), 0), 0);
  if (remaining !== null && needed > remaining) throw new SpeechError(`about ${needed} billable characters needed, ${remaining} left this month`, { code: "video_speech_budget_exhausted" });

  let worst = EXIT.ok;
  for (const dub of dubs) {
    const code = await dubLocale(dub, project, timeline, values, ctx, clientOpts, ffmpeg, workdir, workBase);
    // The STOP file stops the locales after this one as well: the run ends here.
    if (code === EXIT.incomplete) return code;
    worst = Math.max(worst, code);
  }
  if (worst === EXIT.ok) ctx.stdout.write(`next: node tools/video/cli.mjs check-audio --slug ${doc.slug} --locale ${values.locales[0]}\n`);
  return worst;
}

export async function run(command, args, ctx) {
  try {
    return await dub(args, ctx);
  } catch (error) {
    if (error instanceof SpeechError) {
      ctx.stderr.write(`${error.message}\n`);
      return error.who === "owner" ? ctx.EXIT.owner : ctx.EXIT.external;
    }
    if (error instanceof ToolMissing) {
      ctx.stderr.write(`${error.message}\n`);
      return ctx.EXIT.missing;
    }
    throw error;
  }
}
