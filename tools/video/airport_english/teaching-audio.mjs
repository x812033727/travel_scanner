// Airport teaching tracks deliberately differ from generic dubs: coaching is
// localized while every English dialogue take remains byte-identical to the
// reviewed main narration. All output uses a separate, explicit v1 contract.
import { createHash } from 'node:crypto';
import { existsSync, readFileSync, renameSync } from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';
import { CHANNEL_ACCENT } from '../core/accent.mjs';
import { approvalState, sha256File } from '../core/approvals.mjs';
import { audioEvidenceProblems, currentAudioCheck } from '../core/audio-evidence.mjs';
import { appliedBranding, brandingCurrent, presentationTimeline, readBranding } from '../core/branding.mjs';
import { buildCues, checkCues, toSrt, toVtt } from '../core/captions.mjs';
import { resolveMusic, resolveSfx } from '../core/drama.mjs';
import { emptyLexicon } from '../core/lexicon.mjs';
import { atomicWrite, isInside, readJson, ROOT, stopRequested } from '../core/paths.mjs';
import { acquireProjectLease } from '../core/project-lease.mjs';
import { eachLine, spokenText, textHash } from '../core/schema.mjs';
import { lintProject, loadProject } from '../core/state.mjs';
import { FPS, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash, visualHash } from '../core/timeline.mjs';
import { verifyBrandingAssets, wrapAudio } from '../assemble/branding.mjs';
import { locateFfmpeg, runTool } from '../assemble/ffmpeg.mjs';
import { encodeArgs, measureLoudnessArgs, parseLoudnorm, probeArgs, stretchArgs } from '../dubs/encode.mjs';
import { assembleTrack, speechLexicon } from '../dubs/plan.mjs';
import { DEFAULT_THRESHOLD, hintTerms, judgeBatches, matchKind, spokenForm } from '../tts/check.mjs';
import { judgeLines, speechStatus, synthesize, transcribeClip } from '../tts/client.mjs';
import { readCredentials } from '../tts/credentials.mjs';
import { billableForRequest, planRequests } from '../tts/requests.mjs';
import { JOURNAL_DIR, openSpeechJournal } from '../tts/speech-journal.mjs';
import { lineBody, synthesizeLines } from '../tts/synthesis.mjs';
import { staleTakes } from '../tts/takes.mjs';
import { downsample, encodeWav, parseWav, requireNarrationFormat } from '../tts/wav.mjs';

export const TEACHING_SCHEMA = 'airport-teaching-audio/v1';
export const TEACHING_LOCALES = ['zh-TW', 'zh-CN', 'ja', 'ko'];
export const MAX_COACH_TEMPO = 1.15;
export const TEACHING_ARTIFACTS = ['body.wav', 'presentation.wav', 'track.m4a', 'captions.srt', 'captions.vtt'];
const TARGET_FRAMES = 600 * FPS;
const SHA256 = /^[a-f0-9]{64}$/;
const hash = (value) => createHash('sha256').update(typeof value === 'string' || Buffer.isBuffer(value) ? value : JSON.stringify(value)).digest('hex');
const save = (file, value) => atomicWrite(file, `${JSON.stringify(value, null, 2)}\n`);
const bytesOf = (file) => readFileSync(file);
const clipOf = (file) => requireNarrationFormat(parseWav(bytesOf(file)));
function requireExternalWorkdir(workdir, project) {
  let sourceRoot = project.dir;
  for (let directory = project.dir; directory !== path.dirname(directory); directory = path.dirname(directory)) {
    if (path.basename(directory) === 'videos' && path.basename(path.dirname(directory)) === 'docs') { sourceRoot = path.dirname(path.dirname(directory)); break; }
  }
  if (!workdir || isInside(workdir, ROOT) || isInside(workdir, sourceRoot) || isInside(sourceRoot, workdir)) throw new Error('Media workdir must remain separate from the source repository');
}
const styles = {
  'zh-TW': `用${CHANNEL_ACCENT}教成年人練習機場英語。溫暖、清楚、口語化，保留原文的英文單字。不要添加內容，不要唱歌。`,
  'zh-CN': '用自然的中国大陆普通话教成年人练习机场英语。温暖、清楚、口语化，保留原文的英文单词。不要添加内容，不要唱歌。',
  ja: '成人向けの空港英語リスニング教材を、自然な標準日本語で温かく明瞭に話してください。英文の単語はそのまま保ち、内容の追加や歌唱はしないでください。',
  ko: '성인을 위한 공항 영어 듣기 학습 안내를 자연스러운 표준 한국어로 따뜻하고 또렷하게 읽으세요. 원문의 영어 단어는 유지하고 내용을 추가하거나 노래하지 마세요.',
};

/** Offline planning: validates every source/CC identity, never makes an API call. */
export function planTeachingAudio({ project, specification, locale }) {
  if (!TEACHING_LOCALES.includes(locale)) throw new Error(`Unsupported teaching locale: ${locale}`);
  const { doc } = project;
  if (doc.narration_locale !== 'en' || doc.voice?.provider !== 'gemini' || doc.voice.name !== 'Sulafat') throw new Error('Teaching tracks require official Sulafat English source narration');
  if (specification?.schema_version !== 1 || specification.source_locale !== 'en' || specification.source_script_sha256 !== hash(doc)) throw new Error('teaching-audio.json does not bind the current English video.json');
  const originals = [...eachLine(doc)].map(({ scene, line }) => ({ scene: scene.id, source_role: scene.data?.source, line }));
  const source = new Map(originals.map(({ line }) => [line.id, line]));
  const entries = specification.locales?.[locale]?.lines;
  if (!Array.isArray(entries) || entries.length !== originals.length || entries.some((entry, index) => entry.id !== originals[index].line.id)) throw new Error('Teaching lines must cover the English script exactly once, in order');
  const planned = entries.map((entry, index) => {
    const line = originals[index].line;
    const sourceRole = originals[index].source_role;
    if (!['Traveler', 'Staff', 'Airport English'].includes(sourceRole)) throw new Error(`Unrecognized canonical teaching role: ${entry.id}`);
    const sourceDialogue = sourceRole !== 'Airport English';
    if ((entry.kind === 'dialogue') !== sourceDialogue || !['dialogue', 'coach', 'question', 'choice', 'answer'].includes(entry.kind)) throw new Error(`Teaching kind contradicts the English source role: ${entry.id}`);
    if (!entry.text?.trim() || !entry.cc_text?.trim()) throw new Error(`Missing speech or CC: ${entry.id}`);
    const translation = project.translations?.[locale]?.lines?.[entry.id];
    if (!translation || translation.source_hash !== textHash(line.text) || translation.text !== entry.cc_text) throw new Error(`Missing or stale independent CC translation: ${entry.id}`);
    if (entry.kind === 'dialogue') {
      const original = source.get(entry.reuse_source_take);
      if (entry.speech_locale !== 'en' || !original || original.audio_ref || spokenText(original) !== entry.text || spokenText(line) !== entry.text || (line.audio_ref ?? line.id) !== entry.reuse_source_take) throw new Error(`Invalid English take reuse: ${entry.id}`);
    } else if (entry.speech_locale !== locale || entry.reuse_source_take || entry.text !== entry.cc_text) throw new Error(`Coaching must speak its current ${locale} translation: ${entry.id}`);
    return { ...entry, scene: originals[index].scene, protected_pause_ms: line.pause_after_ms ?? 300 };
  });
  const translated = { ...doc, voice: { ...doc.voice, style: styles[locale] }, scenes: planned.filter((entry) => entry.kind !== 'dialogue').map((entry) => ({ id: entry.scene, lines: [{ id: entry.id, text: entry.text }] })) };
  const lexicon = speechLexicon(project.shelfLexicon ?? emptyLexicon(), locale);
  const requests = planRequests(translated, lexicon);
  return { schema: TEACHING_SCHEMA, slug: doc.slug, locale, source_script_sha256: hash(doc), specification_sha256: hash(specification), lines: planned, requests, lexicon,
    fingerprint: hash([locale, specification, requests.map((request) => request.body)]),
    estimated_billable_characters: requests.reduce((sum, request) => sum + billableForRequest(request.body), 0),
    source_dialogue_lines: planned.filter((entry) => entry.kind === 'dialogue').length,
    translated_lines: planned.filter((entry) => entry.kind !== 'dialogue').length,
    status: 'planned_only', approvals_claimed: false };
}

/** Re-read all source inputs after long requests; in-memory objects prove no freshness. */
export function requireCurrentTeachingPlan({ project, specificationFile = path.join(project.dir, 'teaching-audio.json'), locale, fingerprint }) {
  const currentProject = loadProject({ file: project.file, root: ROOT });
  const specification = readJson(specificationFile);
  const plan = planTeachingAudio({ project: currentProject, specification, locale });
  if (plan.fingerprint !== fingerprint) throw new Error('Teaching specification, translations, lexicon or English script changed; rerun from current sources');
  return { project: currentProject, specification, plan };
}

/** A transcript verdict belongs to current bytes AND the current expected words. */
export function passedCurrentCheck(entry, line, bytes, lexicon, locale, threshold = DEFAULT_THRESHOLD) {
  if (!entry || entry.clip !== hash(bytes).slice(0, 16) || entry.intended !== spokenText(line) || entry.spoken_form !== spokenForm(line, lexicon)) return false;
  if (matchKind(entry.heard ?? '', line, lexicon, locale)) return true;
  if (Number.isFinite(entry.noul) && entry.noul >= threshold) return true;
  return Boolean(entry.second) && (Boolean(matchKind(entry.second.heard ?? '', line, lexicon, locale)) || (Number.isFinite(entry.second.noul) && entry.second.noul >= threshold));
}

/** Real production prerequisite check; it never writes an approval. */
export async function requireTeachingSource({ project, workdir }) {
  const errors = lintProject(project).errors;
  if (errors.length) throw new Error('Main project has lint errors; run the official lint first');
  const timeline = readJson(path.join(workdir, 'timeline.json'), null);
  if (!timeline || timeline.timing_basis === 'estimated' || timeline.fps !== FPS || timeline.sample_rate !== SAMPLE_RATE || timeline.speech_hash !== speechHash(project.doc, project.lexicon)) throw new Error('Current measured English timeline is required');
  const evidenceProblems = audioEvidenceProblems(timeline, workdir);
  if (evidenceProblems.length) throw new Error(evidenceProblems.join('; '));
  if (staleTakes(project.doc, project.lexicon, workdir).length) throw new Error('Main English takes do not match the current official speech requests');
  const approval = await approvalState({ gate: 'audio', docDir: project.dir, workdir });
  if (approval.status !== 'approved') throw new Error(`Current main narration approval required (${approval.status})`);
  const checks = currentAudioCheck(readJson(path.join(workdir, 'review', 'check.json'), null), timeline);
  for (const { line } of eachLine(project.doc)) {
    if (!passedCurrentCheck(checks.lines?.[line.id], line, bytesOf(path.join(workdir, 'audio', `${line.id}.wav`)), project.lexicon, 'en')) throw new Error(`Main English audio check is absent, stale or failed: ${line.id}`);
  }
  const branding = readBranding(workdir);
  const videoChecks = readJson(path.join(workdir, 'checks.json'), null);
  if (!branding || !brandingCurrent(videoChecks, branding)) throw new Error('Assemble and pin the installed branding before teaching audio');
  if (!videoChecks.ok || videoChecks.speech_hash !== timeline.speech_hash || videoChecks.narration_sha256 !== timeline.audio_evidence.narration_sha256 || videoChecks.visual_hash !== visualHash(project.doc)) throw new Error('Main picture must be assembled from the same current English narration and script');
  const presentation = presentationTimeline(timeline, appliedBranding(videoChecks));
  if (presentation.total_frames !== TARGET_FRAMES) throw new Error(`Final presentation must be exactly ${TARGET_FRAMES} measured frames, currently ${presentation.total_frames}`);
  if (resolveMusic(project.doc) || resolveSfx(project.doc)) throw new Error('This teaching profile does not support an additional music/SFX bed; explicit mix integration is required');
  return { timeline, branding, presentation, approval, checks, source_final_sha256: await sha256File(path.join(workdir, 'final.mp4')), source_timeline_sha256: hash(bytesOf(path.join(workdir, 'timeline.json'))), main_check_sha256: hash(bytesOf(path.join(workdir, 'review', 'check.json'))) };
}

/** Per-line windows preserve English onset and never borrow a later dialogue's time. */
export function teachingWindows(plan, timeline) {
  const source = new Map(timeline.lines.map((line) => [line.id, line]));
  if (timeline.lines.length !== plan.lines.length) throw new Error('Timeline does not cover every teaching line');
  return plan.lines.map((line, index) => {
    const original = source.get(line.id);
    const next = source.get(plan.lines[index + 1]?.id)?.start_frame ?? timeline.total_frames;
    if (!original || !Number.isSafeInteger(original.start_frame) || !Number.isSafeInteger(original.end_frame)) throw new Error(`Unmeasured line window: ${line.id}`);
    const state = timeline.scenes.find((scene) => scene.id === original.scene)?.states?.find((entry) => entry.start_frame <= original.start_frame && original.start_frame < entry.end_frame);
    const end = Math.min(next, state?.end_frame ?? original.end_frame, original.end_frame) - Math.ceil(line.protected_pause_ms * FPS / 1000);
    if (end <= original.start_frame) throw new Error(`Empty teaching window: ${line.id}`);
    return { ...line, start_frame: original.start_frame, window_end_frame: end };
  });
}

export function tempoForWindow(line, samples) {
  const room = (line.window_end_frame - line.start_frame) * SAMPLES_PER_FRAME;
  if (samples <= room) return 1;
  if (line.kind === 'dialogue') throw new Error(`English take does not fit unchanged: ${line.id}`);
  const tempo = Math.ceil((samples / room) * 100) / 100;
  if (tempo > MAX_COACH_TEMPO) throw new Error(`Shorten coaching ${line.id}: needs ${tempo.toFixed(2)}×; maximum is ${MAX_COACH_TEMPO}`);
  return tempo;
}

/** Official TTS cache contract plus full WAV hashes; corrupted clips cannot be reused. */
export class TeachingClipCache {
  constructor(directory) { this.directory = directory; this.file = path.join(directory, 'cache.json'); this.data = readJson(this.file, { schema: TEACHING_SCHEMA, lines: {}, sha256: {}, timings: {} }); }
  get(line) {
    const file = path.join(this.directory, `${line.id}.wav`);
    if (this.data.lines[line.id] !== line.key || !existsSync(file)) return null;
    const bytes = bytesOf(file);
    return this.data.sha256[line.id] === hash(bytes) ? { file, bytes, timing: this.data.timings?.[line.id] ?? null } : null;
  }
  put(line, clip, timing) {
    if (!clip?.length) throw new Error(`Official synthesis returned empty speech: ${line.id}`);
    const bytes = encodeWav(clip);
    atomicWrite(path.join(this.directory, `${line.id}.wav`), bytes);
    this.data.lines[line.id] = line.key;
    this.data.sha256[line.id] = hash(bytes);
    this.data.timings[line.id] = timing ?? null;
    save(this.file, this.data);
  }
}

async function serviceOptions({ env = process.env, home, fetchImpl = globalThis.fetch }, billable = 0) {
  const credentials = readCredentials({ env, home });
  if (!credentials.token) throw new Error('Official video token missing: complete the existing device pairing before synthesis/checking');
  const options = { site: credentials.site, token: credentials.token, fetchImpl };
  const status = await speechStatus(options);
  if (!status.gemini_configured) throw new Error('Official Gemini speech service is not configured');
  if (status.gemini_monthly_limit > 0 && status.gemini_used != null && billable > status.gemini_monthly_limit - status.gemini_used) throw new Error('Planned translated coaching exceeds the remaining official TTS quota');
  return options;
}

function stop(workdir) { if (stopRequested(workdir)) throw new Error('STOP requested; cached speech is retained, production is incomplete'); }
const locationFor = (workdir, locale) => path.join(workdir, 'teaching-audio', locale);

export async function synthesizeTeachingClips({ plan, workdir, directory, options, send = synthesize }) {
  const cache = new TeachingClipCache(path.join(directory, 'audio'));
  const journal = openSpeechJournal(path.join(workdir, 'audio', JOURNAL_DIR));
  const speak = journal.wrap((body) => send({ ...options, body }));
  for (const request of plan.requests) for (const line of request.lines) {
    if (cache.get(line)) continue;
    stop(workdir);
    const result = await synthesizeLines(request, [line], speak);
    cache.put(line, result.clips.get(line.id), result.timings.get(line.id));
    journal.release();
  }
  return cache;
}

/** Measured CC uses the actual mixed-language takes, separately from speech text. */
export function teachingCaptions(lines, locale, offsetFrames = 0) {
  const cues = lines.flatMap((line) => {
    const shifted = { ...line, start_frame: line.start_frame + offsetFrames, end_frame: line.end_frame + offsetFrames };
    const narration = line.kind === 'dialogue' ? { locale: 'en', texts: { [line.id]: line.text } } : null;
    const result = buildCues({ lines: [shifted] }, { [line.id]: line.cc_text }, locale, narration);
    if (result.missing.length) throw new Error(`Missing CC: ${line.id}`);
    return result.cues;
  });
  const problems = checkCues(cues, locale);
  const warnings = problems.filter((problem) => problem.includes('characters a second'));
  const errors = problems.filter((problem) => !warnings.includes(problem));
  if (errors.length) throw new Error(`Caption segmentation failed: ${errors.join('; ')}`);
  return { cues, warnings };
}

export async function buildTeachingAudio({ project, specification, specificationFile, locale, workdir, env = process.env, home }) {
  requireExternalWorkdir(workdir, project);
  const lease = acquireProjectLease(workdir, { owner: 'airport-teaching-audio' });
  try {
    stop(workdir);
    const plan = planTeachingAudio({ project, specification, locale });
    requireCurrentTeachingPlan({ project, specificationFile, locale, fingerprint: plan.fingerprint });
    const source = await requireTeachingSource({ project, workdir });
    const tools = await locateFfmpeg(env);
    await verifyBrandingAssets(source.branding, { tools });
    const directory = locationFor(workdir, locale);
    const before = new TeachingClipCache(path.join(directory, 'audio'));
    const pendingBillable = plan.requests.reduce((sum, request) => sum + request.lines.filter((line) => !before.get(line)).reduce((count, line) => count + billableForRequest(lineBody(request, line)), 0), 0);
    const options = await serviceOptions({ env, home }, pendingBillable);
    const cache = await synthesizeTeachingClips({ plan, workdir, directory, options });
    const requests = new Map(plan.requests.flatMap((request) => request.lines.map((line) => [line.id, line])));
    const clips = new Map();
    const lines = [];
    for (const window of teachingWindows(plan, source.timeline)) {
      stop(workdir);
      const reused = window.kind === 'dialogue';
      const cached = reused ? null : cache.get(requests.get(window.id));
      const file = reused ? path.join(workdir, 'audio', `${window.reuse_source_take}.wav`) : cached.file;
      const originalBytes = bytesOf(file);
      if (reused && source.timeline.lines.find((line) => line.id === window.id)?.audio_sha256 !== hash(originalBytes)) throw new Error(`Main dialogue occurrence differs from its approved original take: ${window.id}`);
      let clip = requireNarrationFormat(parseWav(originalBytes));
      let tempo = tempoForWindow(window, clip.length);
      let selectedFile = file;
      if (reused) {
        // Copy the exact approved container bytes, not a re-encoded equivalent.
        selectedFile = path.join(directory, 'audio', `${window.id}.wav`);
        atomicWrite(selectedFile, originalBytes);
      } else if (tempo > 1) {
        const room = (window.window_end_frame - window.start_frame) * SAMPLES_PER_FRAME;
        while (tempo <= MAX_COACH_TEMPO) {
          selectedFile = path.join(directory, 'audio', `${window.id}.fit.wav`);
          await runTool(tools.ffmpeg, stretchArgs(file, tempo, selectedFile));
          clip = clipOf(selectedFile);
          if (clip.length <= room) break;
          tempo = Math.round((tempo + .01) * 100) / 100;
        }
        if (tempo > MAX_COACH_TEMPO) throw new Error(`Coaching still overflows after actual atempo output: ${window.id}; shorten its text`);
      }
      const originalLine = source.timeline.lines.find((line) => line.id === window.id);
      const timing = reused ? originalLine.timing : tempo === 1 ? cached.timing : null;
      clips.set(window.id, clip);
      lines.push({ ...window, end_frame: window.start_frame + Math.ceil(clip.length / SAMPLES_PER_FRAME), audio_samples: clip.length, tempo,
        clip: path.relative(directory, selectedFile), clip_sha256: hash(bytesOf(selectedFile)), source_take_sha256: reused ? hash(originalBytes) : null,
        ...(timing ? { timing } : {}) });
    }
    const bodyFile = path.join(directory, 'body.wav');
    atomicWrite(bodyFile, encodeWav(assembleTrack(source.timeline.total_frames, lines, clips)));
    const joined = path.join(directory, 'presentation.wav');
    await wrapAudio({ tools, bodyFile, bodyFrames: source.timeline.total_frames, branding: source.branding, outFile: joined, outputCodec: ['-c:a', 'pcm_s16le'] });
    // Preserve stereo branding channels; the shared helper normally duplicates a
    // mono narration channel. Both passes here operate on the same stereo mix.
    const stereo = (args) => args.map((arg) => arg.replace('pan=stereo|c0=c0|c1=c0,', 'aformat=channel_layouts=stereo,'));
    const measured = parseLoudnorm((await runTool(tools.ffmpeg, stereo(measureLoudnessArgs(joined)))).stderr);
    const target = path.join(directory, 'track.m4a');
    const partial = path.join(directory, 'track.partial.m4a');
    await runTool(tools.ffmpeg, stereo(encodeArgs(joined, measured, partial, 'm4a')));
    const probe = JSON.parse((await runTool(tools.ffprobe, probeArgs(partial))).stdout);
    const audio = probe.streams.find((stream) => stream.codec_name === 'aac');
    if (!audio || audio.channels !== 2 || Number(audio.sample_rate) !== SAMPLE_RATE || Math.abs(Number(probe.format.duration) - 600) > 1 / FPS) throw new Error('Encoded teaching audio does not meet stereo48k/600s requirements');
    const finalLoudness = parseLoudnorm((await runTool(tools.ffmpeg, stereo(measureLoudnessArgs(partial)))).stderr);
    if (Math.abs(Number(finalLoudness.input_i) + 14) > .5 || Number(finalLoudness.input_tp) > -.9) throw new Error('Encoded teaching track failed measured loudness/true-peak limits');
    const { cues, warnings } = teachingCaptions(lines, locale, source.branding.intro.frames);
    atomicWrite(path.join(directory, 'captions.srt'), toSrt(cues));
    atomicWrite(path.join(directory, 'captions.vtt'), toVtt(cues));
    // Recheck the source immediately before promotion: edits during synthesis may
    // preserve individual cached takes, but never preserve this build's approval.
    const current = requireCurrentTeachingPlan({ project, specificationFile, locale, fingerprint: plan.fingerprint });
    const refreshed = await requireTeachingSource({ project: current.project, workdir });
    if (refreshed.source_timeline_sha256 !== source.source_timeline_sha256 || refreshed.source_final_sha256 !== source.source_final_sha256 || hash(readJson(path.join(project.dir, 'video.json'))) !== plan.source_script_sha256) throw new Error('English source changed during the teaching build');
    renameSync(partial, target);
    const artifacts = Object.fromEntries(TEACHING_ARTIFACTS.map((name) => [name, hash(bytesOf(path.join(directory, name)))]));
    const manifest = { schema: TEACHING_SCHEMA, status: 'built_pending_mixed_audio_check_and_review', slug: project.doc.slug, locale,
      source_script_sha256: plan.source_script_sha256, specification_sha256: plan.specification_sha256, fingerprint: plan.fingerprint,
      source_timeline_sha256: source.source_timeline_sha256, source_final_sha256: source.source_final_sha256, main_check_sha256: source.main_check_sha256, main_audio_approval_sha256: source.approval.sha256,
      branding_hash: source.branding.hash, body_frames: source.timeline.total_frames, intro_frames: source.branding.intro.frames, total_frames: TARGET_FRAMES,
      sample_rate: SAMPLE_RATE, lines, artifacts, caption_warnings: warnings, final_loudness: finalLoudness,
      formal_qa_approved: false, publication_approved: false, built_at: new Date().toISOString() };
    save(path.join(directory, 'manifest.json'), manifest);
    return manifest;
  } finally { lease.release(); }
}

/** A saved build cannot replace expected speech or loosen the timeline contract. */
export function validateTeachingManifest(manifest, plan, source) {
  if (manifest?.schema !== TEACHING_SCHEMA || manifest.fingerprint !== plan.fingerprint || manifest.source_timeline_sha256 !== source.source_timeline_sha256 || manifest.source_final_sha256 !== source.source_final_sha256 || manifest.branding_hash !== source.branding.hash || manifest.total_frames !== TARGET_FRAMES || manifest.body_frames !== source.timeline.total_frames) throw new Error('No current mixed teaching-audio build to check');
  if (manifest.intro_frames !== source.branding.intro.frames || manifest.sample_rate !== SAMPLE_RATE || manifest.slug !== plan.slug || manifest.locale !== plan.locale || manifest.source_script_sha256 !== plan.source_script_sha256 || manifest.specification_sha256 !== plan.specification_sha256) throw new Error('Mixed manifest branding offset, audio format or source identity changed');
  const windows = teachingWindows(plan, source.timeline);
  if (!manifest.artifacts || typeof manifest.artifacts !== 'object' || Array.isArray(manifest.artifacts) || Object.keys(manifest.artifacts).length !== TEACHING_ARTIFACTS.length || TEACHING_ARTIFACTS.some((name) => !SHA256.test(manifest.artifacts[name] ?? ''))) throw new Error('Mixed manifest must bind every required track, WAV and caption artifact by SHA256');
  if (manifest.lines?.length !== windows.length) throw new Error('Mixed manifest omits speech lines');
  for (const [index, line] of manifest.lines.entries()) {
    const expected = windows[index];
    for (const field of ['id', 'text', 'kind', 'speech_locale', 'cc_text', 'reuse_source_take', 'protected_pause_ms', 'start_frame', 'window_end_frame']) {
      if (line[field] !== expected[field]) throw new Error(`Mixed manifest changed ${field}: ${expected.id}`);
    }
    if (!Number.isInteger(line.audio_samples) || line.audio_samples <= 0 || line.end_frame !== line.start_frame + Math.ceil(line.audio_samples / SAMPLES_PER_FRAME) || line.end_frame > line.window_end_frame || !(line.tempo >= 1 && line.tempo <= MAX_COACH_TEMPO)) throw new Error(`Mixed manifest has invalid fitted timing: ${line.id}`);
    if (!/^audio\/[a-z0-9]{4,8}(?:\.fit)?\.wav$/.test(line.clip)) throw new Error(`Unsafe mixed clip path: ${line.id}`);
    if (line.kind === 'dialogue') {
      const original = source.timeline.lines.find((item) => item.id === line.id);
      if (line.tempo !== 1 || line.clip_sha256 !== original.audio_sha256 || line.source_take_sha256 !== original.audio_sha256 || line.audio_samples !== original.audio_samples) throw new Error(`English dialogue changed from its approved take: ${line.id}`);
    }
  }
}

/** Shared real checker; injected transports are for isolated tests only. */
export async function checkMixedLines({ lines, directory, workdir, lexicon, options, sourceChecks = null, transcribe = transcribeClip, judge = judgeLines }) {
  const file = path.join(directory, 'check-cache.json');
  const cache = readJson(file, { schema: TEACHING_SCHEMA, lines: {} });
  const journal = openSpeechJournal(path.join(workdir, 'audio', JOURNAL_DIR));
  const hear = journal.wrapTranscribe(transcribe), decide = journal.wrapJudge(judge);
  const results = {};
  for (const line of lines) {
    stop(workdir);
    const bytes = bytesOf(path.join(directory, line.clip));
    if (hash(bytes) !== line.clip_sha256) throw new Error(`Mixed audio clip changed: ${line.id}`);
    const samples = requireNarrationFormat(parseWav(bytes));
    if (samples.length !== line.audio_samples) throw new Error(`Mixed audio sample count differs from its timing: ${line.id}`);
    const language = line.speech_locale;
    const dictionary = speechLexicon(lexicon, language);
    const expected = { id: line.id, text: line.text };
    const intended = spokenText(expected), spoken = spokenForm(expected, dictionary);
    const terms = hintTerms(expected, { locale: language, lexicon: dictionary });
    const key = hash([hash(bytes), language, intended, spoken, terms]);
    let entry = cache.lines[key];
    if (entry && (entry.clip_sha256 !== hash(bytes) || entry.language !== language || entry.intended !== intended || entry.spoken_form !== spoken)) entry = null;
    const sourceCheck = sourceChecks?.lines?.[line.reuse_source_take];
    if (!entry && line.kind === 'dialogue' && passedCurrentCheck(sourceCheck, expected, bytes, dictionary, 'en')) {
      entry = { ...sourceCheck, clip_sha256: hash(bytes), language, terms, provenance: 'current_checked_approved_main_take' };
      cache.lines[key] = entry;
      save(file, cache);
    }
    if (!entry) {
      const wav = encodeWav(downsample(samples, 3), 16000);
      const heard = await hear({ ...options, wav, terms, language });
      entry = { clip: hash(bytes).slice(0, 16), clip_sha256: hash(bytes), language, intended, spoken_form: spoken, terms, heard,
        match_kind: matchKind(heard, expected, dictionary, language), noul: null };
      cache.lines[key] = entry;
      save(file, cache); journal.release();
    }
    entry.match_kind = matchKind(entry.heard, expected, dictionary, language);
    if (!entry.match_kind && !Number.isFinite(entry.noul)) {
      if ([intended, spoken].some((text) => text.length > 400) || entry.heard.length > 800) throw new Error(`Mixed audio check would truncate ${line.id}; shorten or independently review instead`);
      for (const batch of judgeBatches([{ id: line.id, intended, spoken_form: spoken, heard: entry.heard }])) {
        stop(workdir);
        const verdicts = await decide({ ...options, lines: batch, language });
        entry.noul = verdicts.get(line.id) ?? 0;
        save(file, cache); journal.release();
      }
    }
    results[line.id] = { ...entry, passed: passedCurrentCheck(entry, expected, bytes, dictionary, language) };
  }
  return results;
}

export async function checkTeachingAudio({ project, specification, specificationFile, locale, workdir, env = process.env, home }) {
  requireExternalWorkdir(workdir, project);
  const lease = acquireProjectLease(workdir, { owner: 'airport-teaching-audio-check' });
  try {
    const plan = planTeachingAudio({ project, specification, locale });
    requireCurrentTeachingPlan({ project, specificationFile, locale, fingerprint: plan.fingerprint });
    const source = await requireTeachingSource({ project, workdir });
    const directory = locationFor(workdir, locale);
    const manifestFile = path.join(directory, 'manifest.json');
    const manifest = readJson(manifestFile, null);
    validateTeachingManifest(manifest, plan, source);
    const manifestHash = hash(bytesOf(manifestFile));
    for (const [name, expected] of Object.entries(manifest.artifacts)) if (hash(bytesOf(path.join(directory, name))) !== expected) throw new Error(`Mixed track artifact changed: ${name}`);
    const options = await serviceOptions({ env, home });
    const results = await checkMixedLines({ lines: manifest.lines, directory, workdir, lexicon: project.shelfLexicon ?? emptyLexicon(), options, sourceChecks: source.checks });
    if (hash(bytesOf(manifestFile)) !== manifestHash || hash(readJson(project.file)) !== plan.source_script_sha256) throw new Error('Teaching manifest or English script changed during audio checks');
    for (const line of manifest.lines) if (hash(bytesOf(path.join(directory, line.clip))) !== line.clip_sha256) throw new Error(`Mixed take changed during audio checks: ${line.id}`);
    for (const [name, expected] of Object.entries(manifest.artifacts)) if (hash(bytesOf(path.join(directory, name))) !== expected) throw new Error(`Mixed artifact changed during audio checks: ${name}`);
    const current = requireCurrentTeachingPlan({ project, specificationFile, locale, fingerprint: plan.fingerprint });
    const refreshed = await requireTeachingSource({ project: current.project, workdir });
    if (refreshed.source_timeline_sha256 !== source.source_timeline_sha256 || refreshed.source_final_sha256 !== source.source_final_sha256) throw new Error('Main English media changed during audio checks');
    const flags = Object.entries(results).filter(([, entry]) => !entry.passed).map(([id]) => id);
    const report = { schema: TEACHING_SCHEMA, status: flags.length ? 'mixed_audio_check_failed' : 'mixed_audio_check_passed_pending_final_review',
      manifest_sha256: manifestHash, track_sha256: manifest.artifacts['track.m4a'], checked_at: new Date().toISOString(),
      threshold: DEFAULT_THRESHOLD, lines: results, flags, unchecked: manifest.lines.length - Object.keys(results).length,
      formal_qa_approved: false, publication_approved: false };
    save(path.join(directory, 'check.json'), report);
    return report;
  } finally { lease.release(); }
}

export async function main(args = process.argv.slice(2)) {
  const command = args[0];
  if (!['plan', 'build', 'check'].includes(command)) throw new Error('Usage: teaching-audio.mjs plan|build|check --file video.json --workdir /external/media/slug --locale zh-TW [--spec teaching-audio.json]');
  const { values } = parseArgs({ args: args.slice(1), options: { file: { type: 'string' }, workdir: { type: 'string' }, locale: { type: 'string' }, spec: { type: 'string' }, 'dry-run': { type: 'boolean' } }, strict: true });
  if (!values.file || !values.locale) throw new Error('--file and --locale are required');
  const project = loadProject({ file: path.resolve(values.file), root: process.cwd() });
  const specificationFile = values.spec ? path.resolve(values.spec) : path.join(project.dir, 'teaching-audio.json');
  const specification = readJson(specificationFile);
  const input = { project, specification, specificationFile, locale: values.locale, workdir: values.workdir && path.resolve(values.workdir) };
  if (command === 'plan' || values['dry-run']) {
    const plan = planTeachingAudio(input);
    return { ...plan, requests: plan.requests.map(({ id, lines, body }) => ({ id, line_ids: lines.map((line) => line.id), voice: body.voice, model: body.model })), production_gates_checked: false, paid_requests: 0 };
  }
  if (!input.workdir) throw new Error('--workdir is required for build/check');
  if (input.workdir.startsWith(path.resolve(project.dir) + path.sep)) throw new Error('Media workdir must remain outside the source directory');
  return command === 'build' ? buildTeachingAudio(input) : checkTeachingAudio(input);
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().then((result) => { process.stdout.write(`${JSON.stringify(result, null, 2)}\n`); if (result.flags?.length) process.exitCode = 1; }).catch((error) => { process.stderr.write(`${error.message}\n`); process.exitCode = 1; });
}
