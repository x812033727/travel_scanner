// Adapt the six unchanged, imported long cuts for the existing language commands.
// No network, TTS, rendering, review decisions, or Shorts are performed here.
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, readdirSync, realpathSync, statSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs } from 'node:util';
import { isInside } from '../../../tools/video/core/paths.mjs';
import { validateVideo } from '../../../tools/video/core/schema.mjs';
import { lintVideo } from '../../../tools/video/core/lint.mjs';
import { FPS, SAMPLE_RATE, speechHash } from '../../../tools/video/core/timeline.mjs';
import { sceneProblems } from '../../../tools/video/templates/templates.mjs';
import { windowsOf } from '../../../tools/video/dubs/plan.mjs';
import { parseWav } from '../../../tools/video/tts/wav.mjs';

export const REPO = fileURLToPath(new URL('../../../', import.meta.url));
export const APPROVED_CUTS = Object.freeze({
  'ai-real-world-01-image-trust': 'a49bcf146dbb8ad0b0ee41ee47ed4241a51dd001eeca8d241b4ee54b9da956dd',
  'ai-real-world-02-confident-errors': '61f014f606419b4db6be9179f54b9523cf541d120f92dc434608701cefbd3e5c',
  'ai-real-world-03-machine-internet': '192ba5583273ee8e0724a2e76087eb4b73259d2342b198038a1700bcfb8fb2fd',
  'ai-real-world-04-tasks-and-jobs': 'e5366e1ba9df41b278ed47059847affa4270e5a5b097b722dc04f2c57dcc675a',
  'ai-real-world-05-uneven-abilities': '3da0a096e4ad76ba17fcaac427082069294c7abb1007454ff64d61f1713e68a7',
  'ai-real-world-06-digital-yesman': 'a163cb697d284427dfde17a90426e458ceef7e706abf6f0f9657e7a43345fca4',
});
export const TARGET_VOICE = Object.freeze({ provider: 'gemini', name: 'Sulafat', model: 'gemini-3.8-flash-tts' });
const NAME_SPELLINGS = ['YouTube', 'DeepMind', 'Deep', 'Think'];
const EPSILON = 0.00001;
const digest = (value) => createHash('sha256').update(value).digest('hex');
const readJson = (file) => JSON.parse(readFileSync(file, 'utf8').replace(/^\uFEFF/, ''));
const jsonBytes = (value) => `${JSON.stringify(value, null, 2)}\n`;
const writeJson = (file, value) => { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, jsonBytes(value)); };

export function requireSlug(slug) {
  if (!Object.hasOwn(APPROVED_CUTS, slug)) throw new Error(`Not one of the six allowed original long cuts (Shorts refused): ${slug}`);
  return slug;
}

export function fileRecord(role, file) {
  return { role, path: path.resolve(file), bytes: statSync(file).size, sha256: digest(readFileSync(file)) };
}

// Normalize spelling-equivalent punctuation only. In particular, do not remove decimal
// points, minus signs, digits, Latin letters, or words when checking source narration.
export function normalizedNarration(value) {
  return String(value).normalize('NFC').replace(/\s+/gu, '')
    .replace(/[“”]/gu, '"').replace(/[‘’]/gu, "'")
    .replace(/，/gu, ',').replace(/！/gu, '!').replace(/？/gu, '?');
}

export function captionText(value) { return String(value).replace(/^\uFEFF/, '').replace(/\r\n/g, '\n'); }

export function validateCaptionUnits(srt, timing) {
  const cues = captionText(srt).trim().split(/\n[ \t]*\n/);
  if (!Array.isArray(timing.units) || cues.length !== timing.units.length) throw new Error('Caption cue count differs from source timing units');
  const seconds = (stamp) => {
    const match = /^(\d{2,}):([0-5]\d):([0-5]\d),(\d{3})$/.exec(stamp);
    if (!match) throw new Error('Invalid source SRT timestamp');
    return Number(match[1]) * 3600 + Number(match[2]) * 60 + Number(match[3]) + Number(match[4]) / 1000;
  };
  let maximumError = 0;
  for (const [index, cue] of cues.entries()) {
    const [number, stamps, ...text] = cue.split('\n');
    const bounds = stamps?.split(' --> ');
    if (number !== String(index + 1) || bounds?.length !== 2 || !text.length) throw new Error(`Invalid/out-of-order source caption ${index + 1}`);
    const unit = timing.units[index];
    if (normalizedNarration(text.join('\n')) !== normalizedNarration(unit.text)) throw new Error(`Caption ${index + 1} text differs from source timing unit`);
    for (const [stamp, expected] of [[bounds[0], unit.start], [bounds[1], unit.end]]) {
      const error = Math.abs(seconds(stamp) - expected);
      if (!Number.isFinite(error) || error > 0.001 + Number.EPSILON) throw new Error(`Caption ${index + 1} timestamp differs from source timing unit`);
      maximumError = Math.max(maximumError, error);
    }
  }
  return { cue_count: cues.length, maximum_timestamp_error_seconds: maximumError, tolerance_seconds: 0.001,
    text_check: 'One cue per timing unit in source order; normalized whitespace and spelling-equivalent punctuation only' };
}

export function adapterLexicon(source) {
  const lexicon = structuredClone(source);
  const additions = {};
  for (const name of NAME_SPELLINGS) if (!Object.hasOwn(lexicon.terms, name)) { lexicon.terms[name] = name; additions[name] = name; }
  return { lexicon, additions };
}

export function assertOriginalCut(slug, imported, original) {
  requireSlug(slug);
  const expected = APPROVED_CUTS[slug];
  if (imported !== expected || original !== expected) throw new Error(`${slug}: imported/source final SHA does not match the frozen original cut`);
}

function sameTime(a, b, message) {
  if (!Number.isFinite(a) || !Number.isFinite(b) || Math.abs(a - b) > EPSILON) throw new Error(message);
}

export function validateTiming(episode, timing) {
  if (!Array.isArray(episode.scenes) || !episode.scenes.length || !Array.isArray(timing.scenes) || !Array.isArray(timing.units)) throw new Error('Missing source scenes or units');
  if (episode.scenes.length !== timing.scenes.length || !timing.units.length) throw new Error('Source scene count differs from timed cut');
  let end = 0;
  let previousScene = -1;
  for (const unit of timing.units) {
    if (!Number.isInteger(unit.scene) || unit.scene < 0 || unit.scene >= episode.scenes.length || unit.scene < previousScene || typeof unit.text !== 'string' || !unit.text.trim()) throw new Error('Invalid/out-of-order source unit');
    sameTime(unit.start, end, 'Source units contain a gap or overlap');
    if (!Number.isFinite(unit.end) || unit.end <= unit.start) throw new Error('Invalid source unit duration');
    end = unit.end;
    previousScene = unit.scene;
  }
  sameTime(end, timing.duration, 'Source duration differs from final unit');
  for (const [index, scene] of episode.scenes.entries()) {
    const units = timing.units.filter((unit) => unit.scene === index);
    if (!units.length) throw new Error(`No timed narration for scene ${index}`);
    if (normalizedNarration(units.map((unit) => unit.text).join('')) !== normalizedNarration(scene.narration)) throw new Error(`Timed narration differs from current long narration in scene ${index}`);
    sameTime(timing.scenes[index].start, units[0].start, `Scene ${index} starts at a different time`);
    sameTime(timing.scenes[index].end, units.at(-1).end, `Scene ${index} ends at a different time`);
    if (timing.scenes[index].heading !== scene.heading) throw new Error(`Scene ${index} heading differs from the original timing`);
  }
}

function briefFor(meta) {
  return `# ${meta.titles?.[0] ?? meta.title}\n\n此文件只供既有長片的語言續作。不是新企劃、原聲重製或新的核准。\n\n## 站主觀點\n本輪只依使用者指定續作既有成片的語言，不新增或推定站主的個人經驗與立場。原始內容保留在來源與雜湊紀錄中。\n\n## 觀眾看完能做到的事\n讓選用其他語言的觀眾理解同一支既有中文解說；不得改動數字、限制、證據強弱及虛構情境標示。\n`;
}

export function buildAdapter({ slug, episode, timing, meta, catalog, lexicon, audioSamples }) {
  requireSlug(slug);
  if (meta.slug !== slug || episode.id !== slug.replace(/^ai-real-world-/, '')) throw new Error('Episode/metadata identity mismatch');
  validateTiming(episode, timing);
  if (!Array.isArray(audioSamples) || audioSamples.length !== timing.units.length) throw new Error('Missing actual clip sample lengths');
  const seenIds = new Set();
  const lineMap = [];
  const scenes = episode.scenes.map((scene, sceneIndex) => {
    const id = `chapter-${digest(scene.heading).slice(0, 8)}`;
    const occurrences = new Map();
    const lines = timing.units.flatMap((unit, index) => {
      if (unit.scene !== sceneIndex) return [];
      const occurrence = occurrences.get(unit.text) ?? 0;
      occurrences.set(unit.text, occurrence + 1);
      const lineId = digest(JSON.stringify([slug, id, unit.text, occurrence])).slice(0, 8);
      if (seenIds.has(lineId)) throw new Error('Stable line ID collision');
      seenIds.add(lineId);
      const samples = audioSamples[index];
      if (!Number.isInteger(samples) || samples <= 0 || samples / SAMPLE_RATE > unit.end - unit.start + EPSILON) throw new Error(`Invalid spoken sample count for unit ${index}`);
      lineMap.push({ unit_index: index, scene_index: sceneIndex, scene_id: id, line_id: lineId,
        text: unit.text, source_start_seconds: unit.start, source_end_seconds: unit.end, audio_samples_48000: samples });
      return [{ id: lineId, text: unit.text, pause_after_ms: 0 }];
    });
    return { id, chapter: scene.heading, template: 'bullets', data: { title: scene.heading, items: scene.cards }, lines };
  });
  const sourceById = new Map(catalog.sources.map((source) => [source.id, source]));
  const sources = episode.sources.map((id) => {
    const source = sourceById.get(id);
    if (!source) throw new Error(`Missing cited source ${id}`);
    return { title: source.title, url: source.url, checked_on: catalog.checked_on };
  });
  const doc = {
    schema_version: 1, slug, format: 'slides', narration_locale: 'zh-TW', target_minutes: [8, 12],
    voice: { ...TARGET_VOICE },
    youtube: { category_id: 28, made_for_kids: false, default_language: 'zh-TW',
      title: meta.titles?.[0] ?? meta.title, description: meta.description.split(/\r?\n\s*章節\s*\r?\n/)[0].trim(),
      tags: ['AI', episode.theme], video_id: null },
    thumbnail: { template: 'thumb', data: { headline: episode.thumb_a, tag: 'AI 與真實世界' } },
    sources, scenes,
  };
  const errors = [...validateVideo(doc), ...scenes.flatMap((scene) => sceneProblems(scene))];
  if (errors.length) throw new Error(`Invalid adapter document: ${JSON.stringify(errors)}`);
  const brief = briefFor(meta);
  const lint = lintVideo(doc, { lexicon, brief });
  if (lint.errors.length) throw new Error(`Adapter does not pass language lint: ${JSON.stringify(lint.errors)}`);
  const frame = (seconds) => Math.round(seconds * FPS);
  // The existing board already shows all three cards. Its highlight variants do not
  // establish new semantic cue boundaries, so one source chapter is one dub window.
  const timeline = {
    fps: FPS, sample_rate: SAMPLE_RATE, total_frames: frame(timing.duration),
    scenes: scenes.map((scene, index) => ({ id: scene.id, template: scene.template,
      start_frame: frame(timing.scenes[index].start), end_frame: frame(timing.scenes[index].end),
      states: [{ reveal: 0, start_frame: frame(timing.scenes[index].start), end_frame: frame(timing.scenes[index].end) }] })),
    lines: lineMap.map((line) => ({ id: line.line_id, scene: line.scene_id,
      start_frame: frame(line.source_start_seconds), end_frame: frame(line.source_end_seconds), audio_samples: line.audio_samples_48000 })),
    chapters: scenes.map((scene, index) => ({ title: scene.chapter, scene: scene.id, start_frame: frame(timing.scenes[index].start) })),
    speech_hash: speechHash(doc, lexicon),
  };
  let last = 0;
  for (const line of timeline.lines) {
    if (line.start_frame !== last || line.end_frame <= line.start_frame) throw new Error('30 fps quantization collapses or disconnects a source unit');
    last = line.end_frame;
  }
  if (last !== timeline.total_frames) throw new Error('Timeline total differs from units');
  const windowLines = windowsOf(timeline).flatMap((window) => window.lines);
  if (windowLines.length !== timeline.lines.length || new Set(windowLines).size !== timeline.lines.length) throw new Error('A narration line does not belong to exactly one dub window');
  const maximumError = Math.max(...lineMap.flatMap((line) => [line.source_start_seconds, line.source_end_seconds]).map((seconds) => Math.abs(frame(seconds) / FPS - seconds)));
  return { doc, timeline, brief, lineMap, lint, maximumError };
}

function resolvedCandidate(candidate) {
  let existing = path.resolve(candidate);
  const tail = [];
  while (!existsSync(existing)) { tail.unshift(path.basename(existing)); existing = path.dirname(existing); }
  return path.join(realpathSync(existing), ...tail);
}

export function assertOutputIsolation(output, forbidden) {
  const target = resolvedCandidate(output);
  for (const item of forbidden) {
    const source = resolvedCandidate(item);
    if (isInside(target, source) || isInside(source, target)) throw new Error(`Output overlaps an input/repository: ${target}`);
  }
  return target;
}

function sourcePlan({ slug, sourceSeason, importBase, output, lexicon }) {
  const episodeId = requireSlug(slug).replace(/^ai-real-world-/, '');
  const source = {
    import_dir: path.join(importBase, slug), episode: path.join(sourceSeason, 'episodes', `${episodeId}.json`),
    timing: path.join(sourceSeason, 'media', episodeId, 'timing.json'),
    final: path.join(importBase, slug, 'final.mp4'), captions: path.join(importBase, slug, 'zh-TW.srt'),
    thumbnail: path.join(importBase, slug, 'thumbnail.png'),
  };
  const media = path.join(sourceSeason, 'media', episodeId);
  const records = [
    ['import-final', source.final], ['import-metadata', path.join(source.import_dir, 'meta.json')],
    ['import-captions', source.captions], ['import-thumbnail', source.thumbnail],
    ['season-episode', source.episode], ['season-timing', source.timing],
    ['season-render-receipt', path.join(media, 'render-receipt.json')],
    ['season-sources', path.join(sourceSeason, 'sources.json')], ['season-final', path.join(media, 'review.mp4')],
    ['season-narration', path.join(media, 'narration.wav')], ['season-speech-input', path.join(media, 'speech-input.json')],
    ['season-probe', path.join(media, 'probe.json')], ['season-captions', path.join(media, 'captions.srt')],
  ].map(([role, file]) => fileRecord(role, file));
  const byRole = Object.fromEntries(records.map((record) => [record.role, record]));
  assertOriginalCut(slug, byRole['import-final'].sha256, byRole['season-final'].sha256);
  if (captionText(readFileSync(source.captions, 'utf8')) !== captionText(readFileSync(byRole['season-captions'].path, 'utf8'))) throw new Error(`${slug}: imported captions differ from the original cut`);
  const episode = readJson(source.episode), timing = readJson(source.timing);
  const captionTiming = validateCaptionUnits(readFileSync(source.captions, 'utf8'), timing);
  const receipt = readJson(byRole['season-render-receipt'].path);
  if (!receipt.voice?.includes('Microsoft Hanhan Desktop') || receipt.voice_rate !== 0) throw new Error(`${slug}: unexpected original voice provenance`);
  const speech = readJson(byRole['season-speech-input'].path);
  if (speech.length !== timing.units.length) throw new Error(`${slug}: speech inputs differ from timing`);
  const cacheRoot = realpathSync(path.join(sourceSeason, 'media', 'voice-cache'));
  const audioSamples = speech.map((unit, index) => {
    const timed = timing.units[index];
    if (unit.scene !== timed.scene || unit.text !== timed.text) throw new Error(`${slug}: speech input ${index} differs from timing`);
    const file = realpathSync(unit.path);
    if (!isInside(file, cacheRoot) || path.extname(file).toLowerCase() !== '.wav') throw new Error('Voice clip path escapes the season WAV cache');
    const record = fileRecord('season-voice-clip', file);
    records.push({ ...record, unit_index: index });
    const wav = parseWav(readFileSync(file));
    if (wav.sampleRate !== 24000 || wav.channels !== 1 || wav.bitsPerSample !== 16 || wav.audioFormat !== 1) throw new Error('Original Hanhan clip is not 24 kHz mono PCM16');
    sameTime(wav.samples.length / wav.sampleRate + 0.08, timed.end - timed.start, `${slug}: clip duration differs from timed unit ${index}`);
    return wav.samples.length * (SAMPLE_RATE / wav.sampleRate);
  });
  const adapter = buildAdapter({ slug, episode, timing, meta: readJson(byRole['import-metadata'].path), catalog: readJson(byRole['season-sources'].path), lexicon, audioSamples });
  const docFile = path.join(output, 'root', 'docs', 'videos', slug, 'video.json');
  const workdir = path.join(output, 'work', slug);
  const probe = readJson(byRole['season-probe'].path);
  const provenance = {
    schema_version: 1, slug, purpose: 'Language-only adapter for unchanged imported original cut',
    actual_original_narration: { provider: 'Windows System.Speech', voice: 'Microsoft Hanhan Desktop', rate: 0, sample_rate: 24000, channels: 1 },
    target_dub_configuration: { ...TARGET_VOICE },
    voice_warning: 'video.json.voice configures future target-language dubs only. It does not describe or authenticate the existing Hanhan narration.',
    speech_hash_contract: 'Adapter script/configuration identity computed by the standard speechHash helper; not proof that Gemini generated original narration.',
    operation_boundary: 'Do not run tts, render, assemble or automatic stage recovery on this adapter. No approvals or QA passes are fabricated.',
    source_files: records, final_sha256: byRole['import-final'].sha256,
    source_captions_match: 'Exact text and timestamps after BOM/CRLF normalization; both original byte hashes retained',
    source_captions_timing: captionTiming,
    timing: { original_seconds: timing.duration, adapter_seconds: adapter.timeline.total_frames / FPS,
      delta_seconds: adapter.timeline.total_frames / FPS - timing.duration, fps: FPS,
      maximum_endpoint_quantization_error_seconds: adapter.maximumError, added_pause_seconds: 0,
      original_unit_tail_silence_seconds: 0.08, audio_samples_method: 'actual 24kHz WAV sample count multiplied by 2',
      window_policy: 'one original source scene; unchanged card content, no invented per-card semantic alignment' },
    original_recorded_probe: { format_duration: probe.format?.duration, streams: probe.streams?.map(({ codec_type, codec_name, duration, sample_rate, channels, r_frame_rate }) => ({ codec_type, codec_name, duration, sample_rate, channels, r_frame_rate })) },
    line_map: adapter.lineMap, lint: { errors: adapter.lint.errors, warnings: adapter.lint.warnings },
    approval_files_created: false, qa_pass_created: false, original_media_changed: false,
  };
  const { shorts: _omittedShorts, ...longEpisode } = episode;
  const snapshots = { 'long-episode.json': longEpisode, 'timing.json': timing,
    'meta.json': readJson(byRole['import-metadata'].path), 'sources.json': readJson(byRole['season-sources'].path),
    'render-receipt.json': receipt, 'probe.json': probe };
  return { ...adapter, provenance, snapshots, manifest: { slug, title: adapter.doc.youtube.title, final_sha256: provenance.final_sha256,
    doc_file: docFile, workdir, source, source_files: records, provenance_file: path.join(workdir, 'provenance.json'),
    relative_paths: { doc_file: `root/docs/videos/${slug}/video.json`, workdir: `work/${slug}`, provenance_file: `work/${slug}/provenance.json` } } };
}

export function prepare({ sourceSeason, importBase, output, slugs = Object.keys(APPROVED_CUTS), dryRun = false, repo = REPO }) {
  if (!Array.isArray(slugs) || !slugs.length || new Set(slugs).size !== slugs.length) throw new Error('Choose unique allowed long-video slugs');
  slugs.forEach(requireSlug);
  sourceSeason = realpathSync(sourceSeason); importBase = realpathSync(importBase);
  output = assertOutputIsolation(output, [repo, sourceSeason, importBase]);
  const manifestFile = path.join(output, 'manifest.json');
  if (existsSync(manifestFile)) throw new Error('Prepared manifest already exists; resume the runner against it without re-preparing or overwriting it');
  if (existsSync(output) && readdirSync(output).length) throw new Error('Output is not empty; choose a new isolated directory');
  const shared = ['lexicon.json', 'README.md'].map((name) => fileRecord(name === 'lexicon.json' ? 'shared-lexicon' : 'channel-reference', path.join(repo, 'docs', 'videos', name)));
  const { lexicon, additions } = adapterLexicon(readJson(shared[0].path));
  const plans = slugs.map((slug) => sourcePlan({ slug, sourceSeason, importBase, output, lexicon }));
  const manifest = { schema_version: 1, status: dryRun ? 'dry-run' : 'prepared-local-language-adapter',
    root: path.join(output, 'root'), work_base: path.join(output, 'work'), created_at: new Date().toISOString(),
    portable: true, relative_paths: { root: 'root', work_base: 'work' }, source_files_are_provenance_only: true,
    prepare_sha256: digest(readFileSync(fileURLToPath(import.meta.url))), shared_source_files: shared,
    target_lexicon_additions: { terms: additions, purpose: 'Preserve proper-name spelling for future dubs; not an assertion of human pronunciation approval. Original Hanhan audio remains unchanged.' },
    videos: plans.map((plan) => plan.manifest) };
  if (dryRun) return manifest;
  // Validate every source before making any output; then copy without any media transform.
  mkdirSync(path.join(manifest.root, 'docs', 'videos'), { recursive: true });
  for (const record of shared) {
    const target = path.join(manifest.root, 'docs', 'videos', path.basename(record.path));
    if (record.role === 'shared-lexicon') writeJson(target, lexicon);
    else copyFileSync(record.path, target);
  }
  for (const plan of plans) {
    const { workdir, source, doc_file: docFile } = plan.manifest;
    writeJson(docFile, plan.doc);
    writeFileSync(path.join(path.dirname(docFile), 'brief.md'), plan.brief);
    writeJson(path.join(workdir, 'timeline.json'), plan.timeline);
    mkdirSync(path.join(workdir, 'captions'), { recursive: true });
    for (const [from, relative] of [[source.final, 'final.mp4'], [source.captions, 'captions/zh-TW.srt'], [source.captions, 'original-zh-TW.srt'], [source.thumbnail, 'thumbnail.png']]) {
      const target = path.join(workdir, relative);
      copyFileSync(from, target);
      if (digest(readFileSync(target)) !== digest(readFileSync(from))) throw new Error(`Copy hash mismatch: ${target}`);
    }
    // Recheck the complete read set, including shared JSON that another task may edit.
    for (const record of [...shared, ...plan.manifest.source_files]) if (digest(readFileSync(record.path)) !== record.sha256) throw new Error(`Source changed during preparation: ${record.path}`);
    writeJson(plan.manifest.provenance_file, plan.provenance);
    const snapshots = Object.entries(plan.snapshots).map(([name, value]) => {
      const file = path.join(workdir, 'source-snapshots', name); writeJson(file, value); return file;
    });
    plan.manifest.generated_files = [docFile, path.join(path.dirname(docFile), 'brief.md'), path.join(workdir, 'timeline.json'), path.join(workdir, 'final.mp4'), path.join(workdir, 'original-zh-TW.srt'), path.join(workdir, 'thumbnail.png'), plan.manifest.provenance_file, ...snapshots]
      .map((file) => ({ ...fileRecord('prepared-artifact', file), relative_path: path.relative(output, file).split(path.sep).join('/') }));
  }
  manifest.shared_generated_files = shared.map((record) => {
    const file = path.join(manifest.root, 'docs', 'videos', path.basename(record.path));
    return { ...fileRecord(record.role, file), relative_path: path.relative(output, file).split(path.sep).join('/') };
  });
  writeJson(manifestFile, manifest);
  return manifest;
}

function main() {
  const { values } = parseArgs({ options: { 'source-season': { type: 'string' }, 'import-base': { type: 'string' }, output: { type: 'string' }, slug: { type: 'string' }, 'dry-run': { type: 'boolean' } }, strict: true });
  if (!values['source-season'] || !values['import-base'] || !values.output) throw new Error('Usage: prepare.mjs --source-season DIR --import-base DIR --output NEW_EXTERNAL_DIR [--slug allowed-slug,...] [--dry-run]');
  const result = prepare({ sourceSeason: values['source-season'], importBase: values['import-base'], output: values.output, slugs: values.slug?.split(','), dryRun: values['dry-run'] });
  console.log(JSON.stringify({ status: result.status, root: result.root, work_base: result.work_base, videos: result.videos.map(({ slug, final_sha256 }) => ({ slug, final_sha256 })) }, null, 2));
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try { main(); } catch (error) { console.error(error.message); process.exitCode = 1; }
}
