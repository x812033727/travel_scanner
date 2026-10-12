// Bounded opening-segment production; never writes to an original video work directory.
// CLI: node docs/videos/curio-five-recuts-20261012/speech.mjs plan|synthesize|align|check
//   --spec intros.json --sources /outside/videos --out /outside/recuts [--slug curio-h01]
//   [--locale zh-TW,en,ja,ko] (default: all four; align always requires all four)
// Spec: {schema_version:1,episodes:[{slug,source_doc?,lexicon_file?,lines:[
//   {id:"h1op0001",text:"...",say?,pause_after_ms?,emotion?,source_scene?}],
//   locales:{en:{lines:[same ids]},ja:{lines:[same ids]},ko:{lines:[same ids]}}}]}.
// source_doc defaults to <sources>/<slug>/video.json. lexicon_file defaults to the
// source document's shelf lexicon.json. Both sources are hashed and never edited.
// A locale may specify voice_source (a real original dub timeline file); by default
// <sources>/<slug>/dubs/<locale>/timeline.json supplies its actual saved voice.
// New media: <out>/<slug>/intro/<locale>/{audio/,narration.wav,timeline.json,<locale>.srt,...}.
// This is an opening fragment, not a short full-video document. It deliberately uses
// the existing speech primitives instead of disabling full-video duration/QA gates.
import { createHash } from "node:crypto";
import { existsSync, readFileSync, realpathSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { bindAudioEvidence, audioEvidenceProblems } from "../../../tools/video/core/audio-evidence.mjs";
import { buildCues, checkCues, toSrt } from "../../../tools/video/core/captions.mjs";
import { isKnownTerm, latinTerms, validateLexicon } from "../../../tools/video/core/lexicon.mjs";
import { atomicWrite, isInside, readJson, ROOT } from "../../../tools/video/core/paths.mjs";
import { acquireProjectLease } from "../../../tools/video/core/project-lease.mjs";
import { spokenText } from "../../../tools/video/core/schema.mjs";
import { buildTimeline, estimateTimeline, speechHash } from "../../../tools/video/core/timeline.mjs";
import { speechLexicon } from "../../../tools/video/dubs/plan.mjs";
import { judgeLines, speechStatus, synthesize, transcribeClip } from "../../../tools/video/tts/client.mjs";
import { readCredentials, validSite } from "../../../tools/video/tts/credentials.mjs";
import { billableForRequest, planRequests } from "../../../tools/video/tts/requests.mjs";
import { openSpeechJournal, requestSha256 } from "../../../tools/video/tts/speech-journal.mjs";
import { trimSilence } from "../../../tools/video/tts/split.mjs";
import { buildNarration } from "../../../tools/video/tts/synthesis.mjs";
import { downsample, encodeWav, parseWav, requireNarrationFormat } from "../../../tools/video/tts/wav.mjs";

export const ALLOWED_SLUGS = Object.freeze(["curio-h01", "curio-h02", "curio-h03", "curio-u02", "curio-l08"]);
export const LOCALES = Object.freeze(["zh-TW", "en", "ja", "ko"]);
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const need = (ok, message) => { if (!ok) throw new Error(message); };
const read = (file) => JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
const stamp = () => new Date().toISOString();

// Resolve existing ancestors so a junction cannot redirect output into canonical media.
function actual(file) {
  const absolute = path.resolve(file);
  if (existsSync(absolute)) return realpathSync(absolute);
  return path.join(actual(path.dirname(absolute)), path.basename(absolute));
}

export function loadEpisode({ episode, sources, out, locale = "zh-TW" }) {
  need(ALLOWED_SLUGS.includes(episode?.slug), "slug is outside the five-video cohort");
  need(LOCALES.includes(locale), "unsupported opening locale");
  const sourceFile = path.resolve(episode.source_doc ?? path.join(sources, episode.slug, "video.json"));
  const sourceBytes = readFileSync(sourceFile);
  const source = JSON.parse(sourceBytes.toString("utf8").replace(/^\uFEFF/, ""));
  need(source.slug === episode.slug, "source document slug does not match episode");
  need(source.voice?.name && ["gemini", "azure"].includes(source.voice.provider), "source voice is missing or unsupported");
  need(!source.narration_locale || source.narration_locale === "zh-TW", "only the original zh-TW narration is authorized here");
  const lexiconFile = path.resolve(episode.lexicon_file ?? path.join(path.dirname(path.dirname(sourceFile)), "lexicon.json"));
  need(existsSync(lexiconFile), "source lexicon is missing; specify lexicon_file explicitly");
  const lexiconBytes = readFileSync(lexiconFile);
  const shelfLexicon = JSON.parse(lexiconBytes.toString("utf8").replace(/^\uFEFF/, ""));
  need(validateLexicon(shelfLexicon).length === 0, "source lexicon is invalid");
  const lexicon = speechLexicon(shelfLexicon, locale);
  const localeSpec = locale === "zh-TW" ? episode : episode.locales?.[locale];
  need(localeSpec && Array.isArray(localeSpec.lines), `missing ${locale} opening lines`);
  let voice = source.voice;
  let voiceFile = null;
  let voiceSourceSha256 = null;
  if (locale !== "zh-TW") {
    voiceFile = path.resolve(localeSpec.voice_source ?? path.join(sources, episode.slug, "dubs", locale, "timeline.json"));
    const bytes = readFileSync(voiceFile);
    const original = JSON.parse(bytes.toString("utf8").replace(/^\uFEFF/, ""));
    need(original.locale === locale && original.voice?.name, `original ${locale} dub voice identity is missing`);
    voice = original.voice;
    voiceSourceSha256 = hash(bytes);
  }
  need(["gemini", "azure"].includes(voice.provider), "unsupported original voice provider");
  need(localeSpec.lines.length >= 4 && localeSpec.lines.length <= 16, "an opening needs 4-16 bounded lines");
  if (locale !== "zh-TW") need(JSON.stringify(localeSpec.lines.map((line) => line.id)) === JSON.stringify(episode.lines.map((line) => line.id)), "all opening locales must use the same line ids and order");
  const ids = new Set();
  const lines = localeSpec.lines.map((line) => {
    need(/^[a-z0-9]{4,8}$/.test(line.id ?? "") && !ids.has(line.id), "opening ids must be unique, 4-8 lowercase letters or digits");
    ids.add(line.id);
    need(typeof line.text === "string" && line.text.trim().length > 0 && line.text.length <= 350, `invalid text on ${line.id}`);
    need(line.say === undefined || (typeof line.say === "string" && line.say.trim().length > 0 && line.say.length <= 350), `invalid say on ${line.id}`);
    need(line.emotion === undefined || (typeof line.emotion === "string" && line.emotion.length <= 80), `invalid emotion on ${line.id}`);
    need(line.pause_after_ms === undefined || (Number.isInteger(line.pause_after_ms) && line.pause_after_ms >= 0 && line.pause_after_ms <= 1500), `invalid pause on ${line.id}`);
    const kept = Object.fromEntries(["id", "text", "say", "pause_after_ms", "emotion"].filter((key) => line[key] !== undefined).map((key) => [key, line[key]]));
    const unknown = locale === "zh-TW" ? latinTerms(spokenText(kept)).filter((term) => !isKnownTerm(term, lexicon)) : [];
    need(!unknown.length, `unknown pronunciation terms on ${line.id}: ${unknown.join(", ")}`);
    return kept;
  });
  const doc = { ...source, voice, narration_locale: locale, scenes: [{ id: "opening-condensation", template: "title", chapter: "開場濃縮", lines }] };
  // One line per request: no paid whole-scene attempt followed by an automatic split retry.
  const requests = planRequests({ ...doc, scenes: lines.map((line) => ({ id: `opening-${line.id}`, lines: [line] })) }, lexicon);
  const billable = requests.reduce((sum, item) => sum + billableForRequest(item.body), 0);
  need(billable <= 3000, `opening exceeds the bounded speech budget: ${billable} characters`);
  const directory = path.resolve(out, episode.slug, "intro", locale);
  need(!isInside(actual(directory), actual(ROOT)), "media output must be outside the repository");
  need(!isInside(actual(directory), actual(sources)) && !isInside(actual(sources), actual(directory)), "output overlaps the source work base");
  need(!isInside(actual(sourceFile), actual(directory)), "output overlaps source document");
  const identity = { schema_version: 1, slug: episode.slug, locale, source_doc: sourceFile, source_sha256: hash(sourceBytes), lexicon_file: lexiconFile, lexicon_sha256: hash(lexiconBytes), voice_source: voiceFile, voice_source_sha256: voiceSourceSha256, opening_sha256: hash(json(lines)), voice_sha256: hash(json(voice)), request_sha256: requests.map((item) => requestSha256(item.body)) };
  return { slug: episode.slug, locale, directory, out: path.resolve(out), sourceFile, lexiconFile, voiceFile, identity, doc, lexicon, lines, requests, billable, visualLines: episode.lines, estimated_seconds: estimateTimeline(doc).total_frames / 30 };
}

function fresh(item) {
  need(hash(readFileSync(item.sourceFile)) === item.identity.source_sha256, "source document changed after planning");
  need(hash(readFileSync(item.lexiconFile)) === item.identity.lexicon_sha256, "source lexicon changed after planning");
  if (item.voiceFile) need(hash(readFileSync(item.voiceFile)) === item.identity.voice_source_sha256, "original dub voice source changed after planning");
  for (const directory of [item.directory, path.dirname(item.directory), path.dirname(path.dirname(item.directory)), item.out]) need(!existsSync(path.join(directory, "STOP")), `STOP found at ${directory}`);
}

function receiptFor(item, create = false) {
  const file = path.join(item.directory, "receipt.json");
  const receipt = readJson(file, null);
  if (receipt) need(JSON.stringify(receipt.identity) === JSON.stringify(item.identity), "opening/source identity changed; prepare a new external output root instead of overwriting this revision");
  else need(create, "opening has not been synthesized");
  return receipt ?? { schema_version: 1, kind: "curio-opening-fragment", identity: item.identity, created_at: stamp(), lines: {}, full_video_approved: false, owner_listened: false };
}

function cachedLine(item, receipt, request) {
  const line = request.lines[0];
  const entry = receipt.lines[line.id];
  if (!entry) return null;
  need(entry.request_sha256 === requestSha256(request.body), `request identity changed: ${line.id}`);
  const file = path.join(item.directory, "audio", `${line.id}.wav`);
  need(existsSync(file) && hash(readFileSync(file)) === entry.sha256, `cached WAV changed or missing: ${line.id}; do not repurchase automatically`);
  const samples = requireNarrationFormat(parseWav(readFileSync(file)));
  need(samples.length === entry.samples, `cached sample count changed: ${line.id}`);
  return samples;
}

export function describePlan(item) {
  const receipt = receiptFor(item, true);
  const pending = item.requests.filter((request) => !cachedLine(item, receipt, request));
  return { slug: item.slug, locale: item.locale, directory: item.directory, voice: item.doc.voice, lines: item.lines.length, estimated_seconds: item.estimated_seconds, total_billable_characters: item.billable, pending_lines: pending.length, pending_billable_characters: pending.reduce((sum, request) => sum + billableForRequest(request.body), 0), identity: item.identity };
}

function clientOptions(client) {
  const credentials = client ?? readCredentials();
  need(credentials.token, "video tool credentials are unavailable; use the established login pairing flow");
  need(validSite(`${credentials.site}/`), "invalid speech service origin");
  return { site: credentials.site, token: credentials.token, ...(credentials.fetchImpl ? { fetchImpl: credentials.fetchImpl } : {}), attempts: 1 };
}

function readiness(status, item, needed) {
  if (item.doc.voice.provider === "gemini") {
    need(status.gemini_configured, "Gemini narration is not configured");
    if (item.doc.voice.model && status.gemini_models?.length) need(status.gemini_models.includes(item.doc.voice.model), "source Gemini model is unavailable");
    if (status.gemini_monthly_limit > 0 && status.gemini_used != null) need(needed <= status.gemini_monthly_limit - status.gemini_used, "Gemini narration budget is insufficient");
  } else {
    need(status.configured && status.voices?.includes(item.doc.voice.name), "source Azure voice is unavailable");
    if (status.monthly_limit > 0 && status.remaining != null) need(needed <= status.remaining, "Azure narration budget is insufficient");
  }
}

/** deps are for offline verification; CLI always uses the real guarded client and journal. */
export async function synthesizeOpening(item, { client, synthesizeImpl = synthesize, statusImpl = speechStatus, onProgress = () => {} } = {}) {
  fresh(item);
  const lease = acquireProjectLease(item.directory, { owner: "curio-opening-speech" });
  try {
    const receipt = receiptFor(item, true);
    const planned = describePlan(item);
    if (!planned.pending_lines && receipt.aligned) {
      const timeline = read(path.join(item.directory, "timeline.json"));
      need(hash(json(timeline)) === receipt.timeline_sha256 && !audioEvidenceProblems(timeline, item.directory).length, "aligned output changed; inspect instead of overwriting it");
      return receipt;
    }
    const options = planned.pending_lines ? clientOptions(client) : null;
    if (options) readiness(await statusImpl(options), item, planned.pending_billable_characters);
    fresh(item);
    atomicWrite(path.join(item.directory, "receipt.json"), json(receipt));
    atomicWrite(path.join(item.directory, "video.json"), json(item.doc));
    atomicWrite(path.join(item.directory, "lexicon.json"), json(item.lexicon));
    const journal = openSpeechJournal(path.join(item.directory, "audio", "speech-journal"));
    const send = journal.wrap((body) => synthesizeImpl({ ...options, body }));
    const clips = new Map();
    for (const request of item.requests) {
      lease.verify(); fresh(item);
      const line = request.lines[0];
      let samples = cachedLine(item, receipt, request);
      if (!samples) {
        onProgress({ slug: item.slug, locale: item.locale, line: line.id, stage: "synthesizing", saved: Object.keys(receipt.lines).length, total: item.lines.length });
        const result = await send(request.body);
        samples = trimSilence(requireNarrationFormat(parseWav(result.wav)));
        need(samples.length > 0, `speech returned an empty take: ${line.id}`);
        const wav = encodeWav(samples);
        atomicWrite(path.join(item.directory, "audio", `${line.id}.wav`), wav);
        receipt.lines[line.id] = { request_sha256: requestSha256(request.body), sha256: hash(wav), samples: samples.length, billable: result.billable, saved_at: stamp() };
        atomicWrite(path.join(item.directory, "receipt.json"), json(receipt));
        journal.release();
        onProgress({ slug: item.slug, locale: item.locale, line: line.id, stage: "saved", seconds: samples.length / 48000, saved: Object.keys(receipt.lines).length, total: item.lines.length });
      }
      clips.set(line.id, samples);
    }
    fresh(item);
    const timeline = { ...buildTimeline(item.doc, Object.fromEntries([...clips].map(([id, samples]) => [id, samples.length]))), speech_hash: speechHash(item.doc, item.lexicon) };
    atomicWrite(path.join(item.directory, "narration.wav"), encodeWav(buildNarration(timeline, clips)));
    const bound = bindAudioEvidence(timeline, item.directory);
    atomicWrite(path.join(item.directory, "timeline.json"), json(bound));
    const { cues, missing } = buildCues(bound, Object.fromEntries(item.lines.map((line) => [line.id, line.text])), item.locale);
    const captionProblems = [...missing.map((id) => `missing caption ${id}`), ...checkCues(cues, item.locale)];
    atomicWrite(path.join(item.directory, `${item.locale}.srt`), toSrt(cues));
    const seconds = bound.total_frames / 30;
    Object.assign(receipt, { completed_at: stamp(), seconds, total_frames: bound.total_frames, duration_ok: seconds >= 30 && seconds <= 60, caption_problems: captionProblems, narration_sha256: bound.audio_evidence.narration_sha256, timeline_sha256: hash(json(bound)), captions_sha256: hash(toSrt(cues)), aligned: false, status: "synthesized-awaiting-shared-alignment" });
    atomicWrite(path.join(item.directory, "receipt.json"), json(receipt));
    return receipt;
  } finally { lease.release(); }
}

/** The four intros share native-speed line windows; no audio is time-stretched.
 * Tracks become exactly total_frames * 1,600 mono samples at 48 kHz. The shared
 * manifest is committed last and binds every consumer WAV, timeline and SRT hash.
 */
export function alignOpenings(items) {
  need(items.length === 4 && LOCALES.every((locale) => items.some((item) => item.locale === locale)), "alignment needs all four locales");
  need(new Set(items.map((item) => item.slug)).size === 1, "alignment mixes episodes");
  const ordered = LOCALES.map((locale) => items.find((item) => item.locale === locale));
  const leases = [];
  try {
    for (const item of ordered) { fresh(item); leases.push(acquireProjectLease(item.directory, { owner: "curio-opening-alignment" })); }
    const records = ordered.map((item) => {
      const receipt = receiptFor(item);
      const clips = new Map(item.requests.map((request) => {
        const samples = cachedLine(item, receipt, request);
        need(samples, `${item.locale} has an unfinished take`);
        return [request.lines[0].id, samples];
      }));
      return { item, receipt, clips };
    });
    const primary = records[0].item;
    const lines = [];
    const paddingWarnings = [];
    let frame = 0;
    for (const [index, line] of primary.lines.entries()) {
      const samples = records.map((record) => record.clips.get(line.id).length);
      const max = Math.max(...samples);
      const pause = (line.pause_after_ms ?? 300) + (index === primary.lines.length - 1 ? 1500 : 0);
      const frames = Math.ceil((max + pause * 48) / 1600);
      const source = primary.visualLines.find((original) => original.id === line.id);
      const sourceScene = source?.source_scene ?? source?.scene;
      lines.push({ id: line.id, start_frame: frame, end_frame: frame + frames, ...(sourceScene ? { source_scene: sourceScene } : {}) });
      records.forEach((record, localeIndex) => {
        const extra = (max - samples[localeIndex]) / 48;
        if (extra > 3000) paddingWarnings.push({ locale: record.item.locale, id: line.id, extra_padding_ms: Math.round(extra) });
      });
      frame += frames;
    }
    const shared = { schema_version: 1, kind: "curio-common-opening-windows", slug: primary.slug, fps: 30, sample_rate: 48000, total_frames: frame, seconds: frame / 30, lines, locales: LOCALES, duration_ok: frame >= 900 && frame <= 1800, padding_ok: paddingWarnings.length === 0, padding_warnings: paddingWarnings, time_stretched: false, tracks: {}, created_at: stamp() };
    for (const { item, receipt, clips } of records) {
      fresh(item);
      const timeline = {
        fps: 30, sample_rate: 48000, total_frames: frame,
        scenes: lines.map((line) => ({ id: `opening-${line.id}`, template: "shot", start_frame: line.start_frame, end_frame: line.end_frame, states: [{ reveal: 0, start_frame: line.start_frame, end_frame: line.end_frame }] })),
        lines: lines.map((line) => ({ ...line, scene: `opening-${line.id}`, audio_samples: clips.get(line.id).length })),
        chapters: [{ title: "開場濃縮", scene: `opening-${lines[0].id}`, start_frame: 0 }],
        speech_hash: speechHash(item.doc, item.lexicon),
      };
      atomicWrite(path.join(item.directory, "narration.wav"), encodeWav(buildNarration(timeline, clips)));
      const bound = bindAudioEvidence(timeline, item.directory);
      const { cues, missing } = buildCues(bound, Object.fromEntries(item.lines.map((line) => [line.id, line.text])), item.locale);
      const captions = toSrt(cues);
      const problems = [...missing.map((id) => `missing caption ${id}`), ...checkCues(cues, item.locale)];
      atomicWrite(path.join(item.directory, "timeline.json"), json(bound));
      atomicWrite(path.join(item.directory, `${item.locale}.srt`), captions);
      Object.assign(receipt, { seconds: shared.seconds, total_frames: frame, aligned: true, aligned_at: stamp(), duration_ok: shared.duration_ok, padding_ok: shared.padding_ok, caption_problems: problems, narration_sha256: bound.audio_evidence.narration_sha256, timeline_sha256: hash(json(bound)), captions_sha256: hash(captions), status: shared.duration_ok && shared.padding_ok && !problems.length ? "aligned-awaiting-audio-check" : "needs-segment-review" });
      atomicWrite(path.join(item.directory, "receipt.json"), json(receipt));
      shared.tracks[item.locale] = { narration_sha256: receipt.narration_sha256, timeline_sha256: receipt.timeline_sha256, captions_sha256: receipt.captions_sha256, receipt_sha256: hash(json(receipt)) };
    }
    atomicWrite(path.join(primary.out, primary.slug, "intro", "shared-timeline.json"), json(shared));
    return shared;
  } finally { for (const lease of leases.reverse()) lease.release(); }
}

/** Same transcription, same-sound/filler comparison and Jev threshold as check-audio.
 * The receipt identifies this as segment QA; it grants no full-video/owner approval.
 */
export async function checkOpening(item, { client, transcribeImpl = transcribeClip, judgeImpl = judgeLines, onProgress = () => {} } = {}) {
  // Keep pure planning/synthesis usable before the optional listening dependency
  // (pinyin-pro, declared by the repository) has been installed in this checkout.
  const { DEFAULT_THRESHOLD, hintTerms, matchKind, spokenForm } = await import("../../../tools/video/tts/check.mjs");
  fresh(item);
  const lease = acquireProjectLease(item.directory, { owner: "curio-opening-check" });
  try {
    const receipt = receiptFor(item);
    const timeline = read(path.join(item.directory, "timeline.json"));
    need(hash(json(timeline)) === receipt.timeline_sha256 && timeline.speech_hash === speechHash(item.doc, item.lexicon), "opening timeline identity changed");
    need(audioEvidenceProblems(timeline, item.directory).length === 0, "opening audio evidence changed");
    need(hash(readFileSync(path.join(item.directory, `${item.locale}.srt`))) === receipt.captions_sha256, "opening captions changed after alignment");
    const file = path.join(item.directory, "check.json");
    const report = readJson(file, { schema_version: 1, kind: "curio-opening-audio-check", identity: item.identity, lines: {}, full_video_approved: false, owner_listened: false });
    need(JSON.stringify(report.identity) === JSON.stringify(item.identity), "audio check belongs to another opening");
    const journal = openSpeechJournal(path.join(item.directory, "audio", "speech-journal"));
    const transcribe = journal.wrapTranscribe(transcribeImpl);
    const judge = journal.wrapJudge(judgeImpl);
    let options;
    const credentials = () => (options ??= clientOptions(client));
    for (const line of item.lines) {
      lease.verify(); fresh(item);
      const bytes = readFileSync(path.join(item.directory, "audio", `${line.id}.wav`));
      const sha256 = hash(bytes);
      const terms = hintTerms(line, { locale: item.locale, lexicon: item.lexicon });
      let entry = report.lines[line.id];
      if (!entry || entry.sha256 !== sha256 || JSON.stringify(entry.terms) !== JSON.stringify(terms)) {
        onProgress({ slug: item.slug, locale: item.locale, line: line.id, stage: "transcribing" });
        const wav = encodeWav(downsample(requireNarrationFormat(parseWav(bytes)), 3), 16000);
        const heard = await transcribe({ ...credentials(), wav, terms, language: item.locale });
        need(heard.length <= 800, `transcript exceeds Jev bound for ${line.id}`);
        entry = { sha256, clip: sha256.slice(0, 16), terms, heard, intended: spokenText(line), spoken_form: spokenForm(line, item.lexicon), match_kind: matchKind(heard, line, item.lexicon, item.locale), noul: null };
        report.lines[line.id] = entry;
        atomicWrite(file, json(report)); journal.release();
        onProgress({ slug: item.slug, locale: item.locale, line: line.id, stage: "transcribed", match_kind: entry.match_kind });
      }
    }
    const questions = Object.entries(report.lines).filter(([, entry]) => !entry.match_kind && entry.noul === null).map(([id, entry]) => ({ id, intended: entry.intended, spoken_form: entry.spoken_form, heard: entry.heard }));
    if (questions.length) {
      lease.verify(); fresh(item);
      onProgress({ slug: item.slug, locale: item.locale, stage: "judging", lines: questions.map((line) => line.id) });
      const verdicts = await judge({ ...credentials(), lines: questions, language: item.locale });
      for (const question of questions) {
        const probability = verdicts.get(question.id);
        need(Number.isFinite(probability) && probability >= 0 && probability <= 1, `Jev returned no valid probability for ${question.id}`);
        report.lines[question.id].noul = probability;
      }
      atomicWrite(file, json(report)); journal.release();
    }
    report.flags = Object.entries(report.lines).filter(([, entry]) => !entry.match_kind && !(entry.noul >= DEFAULT_THRESHOLD)).map(([id]) => id);
    report.ok = report.flags.length === 0 && receipt.aligned && receipt.duration_ok && receipt.padding_ok && receipt.caption_problems.length === 0;
    report.threshold = DEFAULT_THRESHOLD;
    report.checked_at = stamp();
    report.narration_sha256 = receipt.narration_sha256;
    report.timeline_sha256 = receipt.timeline_sha256;
    report.captions_sha256 = receipt.captions_sha256;
    atomicWrite(file, json(report));
    atomicWrite(path.join(item.directory, "check-flags.json"), json({ flags: report.flags }));
    return report;
  } finally { lease.release(); }
}

export async function main(args) {
  const [command, ...rest] = args;
  need(["plan", "synthesize", "align", "check"].includes(command), "command must be plan, synthesize, align, or check");
  const { values } = parseArgs({ args: rest, options: { spec: { type: "string" }, sources: { type: "string" }, out: { type: "string" }, slug: { type: "string" }, locale: { type: "string" } }, strict: true });
  need(values.spec && values.sources && values.out, "provide --spec, --sources and --out");
  const spec = read(values.spec);
  need(spec.schema_version === 1 && Array.isArray(spec.episodes) && spec.episodes.length >= 1 && spec.episodes.length <= 5, "invalid bounded opening spec");
  need(new Set(spec.episodes.map((item) => item.slug)).size === spec.episodes.length, "duplicate episode slug");
  const episodes = spec.episodes.filter((item) => !values.slug || item.slug === values.slug);
  need(episodes.length, "selected slug is missing from spec");
  // Validate the entire selected cohort before the first paid call.
  const locales = values.locale ? values.locale.split(",") : LOCALES;
  need(locales.length > 0 && new Set(locales).size === locales.length && locales.every((locale) => LOCALES.includes(locale)), "invalid --locale list");
  if (command === "align") need(locales.length === 4, "align requires all four locales");
  const planned = episodes.flatMap((episode) => locales.map((locale) => loadEpisode({ episode, sources: values.sources, out: values.out, locale })));
  for (const item of planned) describePlan(item);
  let failed = false;
  const onProgress = (value) => process.stdout.write(`${JSON.stringify(value)}\n`);
  if (command === "align") {
    for (const episode of episodes) {
      const shared = alignOpenings(planned.filter((item) => item.slug === episode.slug));
      process.stdout.write(json({ slug: episode.slug, seconds: shared.seconds, duration_ok: shared.duration_ok, padding_ok: shared.padding_ok, padding_warnings: shared.padding_warnings }));
      failed ||= !shared.duration_ok || !shared.padding_ok;
    }
    return failed ? 1 : 0;
  }
  for (const item of planned) {
    if (command === "plan") process.stdout.write(json(describePlan(item)));
    else if (command === "synthesize") {
      const receipt = await synthesizeOpening(item, { onProgress });
      process.stdout.write(json({ slug: item.slug, locale: item.locale, status: receipt.status, seconds: receipt.seconds, duration_ok: receipt.duration_ok, caption_problems: receipt.caption_problems, directory: item.directory }));
    } else {
      const report = await checkOpening(item, { onProgress });
      process.stdout.write(json({ slug: item.slug, locale: item.locale, ok: report.ok, flags: report.flags, full_video_approved: false, owner_listened: false }));
      failed ||= !report.ok;
    }
  }
  return failed ? 1 : 0;
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) {
  main(process.argv.slice(2)).then((code) => { process.exitCode = code; }).catch((error) => { process.stderr.write(`${error.message}\n`); process.exitCode = error.code === "video_speech_uncertain" ? 3 : 2; });
}
