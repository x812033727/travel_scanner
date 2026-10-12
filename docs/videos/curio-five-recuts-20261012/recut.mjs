#!/usr/bin/env node
// Offline, source-bound recuts. This script never calls a server or writes to an original.
// Inputs: source-map.json from the source audit, intro-specs.json, and speech.mjs align output.
import { createHash } from 'node:crypto';
import { copyFileSync, existsSync, mkdirSync, readFileSync, realpathSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { spawnSync } from 'node:child_process';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FPS = 30, SR = 48000, SPF = 1600;
const LOCALES = ['zh-TW', 'en', 'ja', 'ko'];
const SLUGS = ['curio-h02', 'curio-u02', 'curio-h03', 'curio-l08', 'curio-h01'];
const OUTRO_SHA = '00eb9ccc8449fa8b47de0aab290b8aa7d55b09962c12a127e0f0c9c5f7834396';
const args = process.argv.slice(2);
const option = (key, fallback) => { const i = args.indexOf(key); return i < 0 ? fallback : args[i + 1]; };
const ROOT = path.resolve(option('--output-root', 'C:/Users/x8120/mokaair-work/curio-five-recuts-20261012'));
const BRAND = path.resolve(option('--brand-dir', 'C:/Users/x8120/mokaair-work/channel-outro-20261012/package-v4/channel'));
const MAP = path.resolve(option('--source-map', path.join(ROOT, 'source-map.json')));
const SPECS = path.resolve(option('--specs', path.join(HERE, 'intro-specs.json')));
const DRY = args.includes('--dry-run');
const json = (p) => JSON.parse(readFileSync(p, 'utf8').replace(/^\uFEFF/, ''));
const save = (p, value) => { mkdirSync(path.dirname(p), { recursive: true }); writeFileSync(p, `${JSON.stringify(value, null, 2)}\n`); };
const sha = (p) => createHash('sha256').update(readFileSync(p)).digest('hex');
const insist = (ok, message) => { if (!ok) throw new Error(message); };
const inside = (file, dir) => { const r = path.relative(dir, file); return r === '' || (!r.startsWith('..') && !path.isAbsolute(r)); };
function actual(file) {
  const absolute = path.resolve(file);
  return existsSync(absolute) ? realpathSync(absolute) : path.join(actual(path.dirname(absolute)), path.basename(absolute));
}
const q = (p) => `'${p.replaceAll('\\', '/').replaceAll("'", "'\\''")}'`;
let logDir = null, serial = 0, activeOutput = null;
function run(bin, argv) {
  const r = spawnSync(bin, argv, { encoding: 'utf8', windowsHide: true, maxBuffer: 128 * 1024 * 1024 });
  if (logDir) writeFileSync(path.join(logDir, `${String(++serial).padStart(3, '0')}-${path.basename(bin)}.log`), `${JSON.stringify(argv)}\n${r.stderr || ''}`);
  if (r.error || r.status !== 0) throw new Error(`${bin} failed (${r.status}): ${r.error?.message ?? r.stderr?.slice(-5000)}`);
  return { stdout: r.stdout, stderr: r.stderr };
}
function ff(argv) { return run('ffmpeg', ['-hide_banner', '-y', '-nostdin', ...argv]); }
function probe(file, count = false) {
  return JSON.parse(run('ffprobe', ['-v', 'error', ...(count ? ['-count_frames'] : []), '-show_streams', '-show_format', '-of', 'json', file]).stdout);
}
function picture(p) { return p.streams.find((s) => s.codec_type === 'video'); }
function sound(p) { return p.streams.find((s) => s.codec_type === 'audio'); }
function list(file, items) {
  let frames = 0, us = 0;
  writeFileSync(file, 'ffconcat version 1.0\n' + items.map((x) => {
    frames += x.frames; const end = Math.round(frames / FPS * 1e6), duration = (end - us) / 1e6; us = end;
    return `file ${q(x.file)}\nduration ${duration.toFixed(6)}\n`;
  }).join(''));
}
function packetHashes(file) {
  const r = run('ffprobe', ['-v', 'error', '-select_streams', 'v:0', '-show_packets', '-show_entries', 'packet=data_hash', '-show_data_hash', 'sha256', '-of', 'json', file]);
  return JSON.parse(r.stdout).packets.map((x) => x.data_hash);
}
function decodedHashes(file, start, end) {
  return ff(['-v', 'error', '-i', file, '-map', '0:v:0', '-vf', `trim=start_frame=${start}:end_frame=${end},setpts=PTS-STARTPTS`, '-fps_mode', 'passthrough', '-an', '-f', 'framemd5', '-']).stdout
    .split(/\r?\n/).filter((s) => s && !s.startsWith('#')).map((s) => s.split(',').at(-1).trim());
}
function pcmHash(file, startSamples, samples) {
  return ff(['-v', 'error', '-i', file, '-map', '0:a:0', '-af', `aresample=${SR},aformat=sample_fmts=s16:channel_layouts=stereo,atrim=start_sample=${startSamples}:end_sample=${startSamples + samples},asetpts=PTS-STARTPTS`, '-c:a', 'pcm_s16le', '-f', 'hash', '-hash', 'sha256', '-']).stdout.trim();
}
function loudness(file) {
  const r = ff(['-v', 'info', '-i', file, '-map', '0:a:0', '-vn', '-af', 'loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json', '-f', 'null', '-']);
  const m = r.stderr.match(/\{\s*"input_i"[\s\S]*?\}/g);
  insist(m?.length, `No loudness result: ${file}`);
  const measured = JSON.parse(m.at(-1));
  return { integrated: Number(measured.input_i), true_peak: Number(measured.input_tp), measured };
}
function normalizeIntro(input, output, frames) {
  const { measured: m } = loudness(input);
  const filter = `loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=${m.input_i}:measured_TP=${m.input_tp}:measured_LRA=${m.input_lra}:measured_thresh=${m.input_thresh}:offset=${m.target_offset}:linear=true,aresample=${SR},aformat=sample_fmts=s16:channel_layouts=stereo,apad=whole_len=${frames * SPF},atrim=end_sample=${frames * SPF}`;
  ff(['-v', 'error', '-i', input, '-af', filter, '-c:a', 'pcm_s16le', output]);
}
const srtMs = (s) => { const p = s.replace(',', ':').split(':').map(Number); return ((p[0] * 60 + p[1]) * 60 + p[2]) * 1000 + p[3]; };
function stamp(ms) {
  const n = Math.round(ms); return `${String(Math.floor(n / 3600000)).padStart(2, '0')}:${String(Math.floor(n / 60000) % 60).padStart(2, '0')}:${String(Math.floor(n / 1000) % 60).padStart(2, '0')},${String(n % 1000).padStart(3, '0')}`;
}
function cues(file) {
  return readFileSync(file, 'utf8').replace(/^\uFEFF/, '').trim().split(/\r?\n\s*\r?\n/).map((b) => {
    const rows = b.split(/\r?\n/), i = rows.findIndex((s) => s.includes(' --> '));
    insist(i >= 0, `Bad caption block in ${file}`);
    const [a, z] = rows[i].split(' --> ');
    return { start: srtMs(a.trim()), end: srtMs(z.trim()), text: rows.slice(i + 1).join('\n') };
  });
}
function writeSrt(file, items) {
  writeFileSync(file, items.map((c, i) => `${i + 1}\n${stamp(c.start)} --> ${stamp(c.end)}\n${c.text}\n`).join('\n'));
}
const chapterTime = (frame) => { const seconds = Math.floor(frame / FPS); return `${String(Math.floor(seconds / 60)).padStart(2, '0')}:${String(seconds % 60).padStart(2, '0')}`; };
function chapterDescription(description, chapters) {
  let seen = 0;
  const result = description.replace(/^\d{1,2}:\d{2}(?::\d{2})?\s+.+$/gm, (line) => {
    const c = chapters[seen++]; insist(c, 'Localized description has unexpected extra chapters');
    return `${c.at} ${seen === 1 ? c.title : line.replace(/^\d{1,2}:\d{2}(?::\d{2})?\s+/, '')}`;
  });
  insist(seen === chapters.length, `Description chapters mismatch (${seen}/${chapters.length})`);
  return result;
}
const openingTitles = { 'zh-TW': '開場濃縮：本集看點', en: 'Opening summary: inside this case', ja: 'オープニング：今回の見どころ', ko: '오프닝 요약: 이번 사건의 핵심' };
const musicHeadings = { 'zh-TW': '片尾配樂', en: 'End-screen music', ja: 'エンド画面の音楽', ko: '엔드스크린 음악' };
function addMusicCredit(description, locale) {
  const credit = `🎵 ${musicHeadings[locale]}\nGolden Hour — Telecasted (YouTube Audio Library)`;
  const tags = description.match(/\n\n(#[^\n]+)\s*$/);
  return tags ? description.slice(0, tags.index) + `\n\n${credit}\n\n${tags[1]}` : `${description}\n\n${credit}`;
}
function metadataLimits(title, description, locale) {
  const titleCharacters = Array.from(title).length, descriptionCharacters = Array.from(description).length;
  insist(titleCharacters > 0 && titleCharacters <= 100, `${locale} title exceeds YouTube's 100-character limit (${titleCharacters})`);
  insist(descriptionCharacters > 0 && descriptionCharacters <= 5000, `${locale} description exceeds YouTube's 5000-character limit (${descriptionCharacters}); edit summary text explicitly while retaining credits`);
  insist(!/[<>]/.test(title + description), `${locale} metadata contains unsupported angle brackets`);
  return { title_characters: titleCharacters, description_characters: descriptionCharacters, title_limit: 100, description_limit: 5000, passed: true };
}
function planUploadText(plan, openingFrames) {
  const { timeline, metadata, cut } = plan, bodyStart = openingFrames + 150;
  const chapters = [{ at: '00:00', title: openingTitles['zh-TW'], start_frame: 0 }, ...timeline.chapters.slice(1).map((c) => ({ at: chapterTime(c.start_frame - cut + bodyStart), title: c.title, start_frame: c.start_frame - cut + bodyStart }))];
  const plannedTitle = /CC字幕/.test(metadata.title) ? metadata.title : `${metadata.title}｜CC字幕`;
  const plannedDescription = addMusicCredit(chapterDescription(metadata.description, chapters), 'zh-TW');
  const metadataMetrics = { 'zh-TW': metadataLimits(plannedTitle, plannedDescription, 'zh-TW') };
  const plannedLocalizations = {};
  for (const locale of LOCALES.filter((l) => l !== 'zh-TW')) {
    insist(metadata.localizations?.[locale]?.title && metadata.localizations?.[locale]?.description, `Missing authoritative ${locale} metadata`);
    const original = metadata.localizations[locale];
    const translatedChapters = chapters.map((c, i) => ({ ...c, ...(i === 0 ? { title: openingTitles[locale] } : {}) }));
    plannedLocalizations[locale] = { ...original, description: addMusicCredit(chapterDescription(original.description, translatedChapters), locale) };
    metadataMetrics[locale] = metadataLimits(original.title, plannedLocalizations[locale].description, locale);
  }
  return { chapters, plannedTitle, plannedDescription, metadataMetrics, plannedLocalizations };
}

function sourcePlan(entry, spec) {
  const src = actual(entry.workdir), out = actual(path.join(ROOT, entry.slug));
  insist(!inside(out, src) && !inside(src, out), 'Output and source directories must be disjoint');
  const timelinePath = path.join(src, 'timeline.json'), checksPath = path.join(src, 'checks.json');
  const timeline = json(timelinePath), checks = json(checksPath), metadata = json(entry.metadata);
  insist(checks.ok && checks.branding?.body_sha256, `${entry.slug}: source body has no passing bound checks`);
  insist(timeline.fps === FPS && timeline.sample_rate === SR, 'Source time grid must be 30 fps / 48 kHz');
  const cut = timeline.chapters[1]?.start_frame;
  insist(Number.isInteger(cut) && cut > 0 && cut < timeline.total_frames, 'Missing second chapter cut');
  const segmentList = path.join(src, 'build', 'segments.ffconcat');
  const segmentFiles = readFileSync(segmentList, 'utf8').split(/\r?\n/).filter((s) => s.startsWith('file ')).map((s) => {
    const literal = s.slice(6, -1).replaceAll("'\\''", "'");
    const local = path.join(src, 'segments', path.basename(literal));
    return existsSync(local) ? local : path.resolve(literal);
  });
  insist(segmentFiles.length === timeline.scenes.length, 'Segment count does not match source scene timeline');
  const allScenes = timeline.scenes.map((s, i) => ({ ...s, file: segmentFiles[i], frames: s.end_frame - s.start_frame }));
  const bodyScenes = allScenes.filter((s) => s.start_frame >= cut);
  insist(bodyScenes[0].start_frame === cut && bodyScenes.at(-1).end_frame === timeline.total_frames, 'Body cut must retain exact full scenes');
  const sharedPath = path.join(out, 'intro', 'shared-timeline.json');
  const requiredIntro = [sharedPath, ...LOCALES.flatMap((l) => ['narration.wav', `${l}.srt`, 'check.json', 'receipt.json', 'timeline.json'].map((f) => path.join(out, 'intro', l, f)))];
  const missingIntro = requiredIntro.filter((p) => !existsSync(p));
  const body = path.join(src, checks.branding.body_file), final = path.join(src, 'final.mp4');
  const tracked = [...new Set([MAP, SPECS, timelinePath, checksPath, entry.metadata, segmentList, body, final,
    path.join(BRAND, 'manifest.json'), path.join(BRAND, 'intro.mp4'), path.join(BRAND, 'outro.mp4'),
    ...bodyScenes.map((s) => s.file), ...(spec?.lines ?? []).map((l) => { const s = allScenes.find((x) => x.id === l.scene); insist(s, `Intro source scene missing: ${l.scene}`); if (Object.hasOwn(l, 'source_frame')) insist(Number.isInteger(l.source_frame) && l.source_frame >= 0 && l.source_frame < s.frames, `Invalid source_frame for ${l.id}: must be an integer in [0, ${s.frames - 1}]`); return s.file; }),
    ...LOCALES.flatMap((l) => [entry.locales[l].captions, ...(l === 'zh-TW' ? [] : [entry.locales[l].audio])])])];
  tracked.forEach((p) => insist(existsSync(p), `Missing source: ${p}`));
  return { entry, spec, src, out, timeline, checks, metadata, cut, allScenes, bodyScenes, sharedPath, requiredIntro, missingIntro, body, final, tracked };
}

async function assemble(plan) {
  const { entry, spec, src, out, timeline, checks, metadata, cut, bodyScenes, sharedPath, requiredIntro, body, final } = plan;
  insist(plan.missingIntro.length === 0, `Intro still pending: ${plan.missingIntro.join(', ')}`);
  const build = path.join(out, 'build'), upload = path.join(out, 'upload');
  mkdirSync(build, { recursive: true }); mkdirSync(upload, { recursive: true });
  activeOutput = out;
  save(path.join(out, 'qa.json'), { ok: false, status: 'rendering', started_at: new Date().toISOString(), uploaded: false, published: false });
  logDir = path.join(out, 'logs'); mkdirSync(logDir, { recursive: true }); serial = 0;
  const shared = json(sharedPath), frames = shared.total_frames;
  insist(shared.duration_ok && shared.padding_ok && frames >= 900 && frames <= 1800 && shared.fps === FPS, 'Common introduction must be 30–60 seconds at 30 fps, with acceptable shared-language padding');
  const bumperFrames = 150, outroFrames = 630, bodyFrames = timeline.total_frames - cut;
  const bodyStart = frames + bumperFrames, totalFrames = bodyStart + bodyFrames + outroFrames;
  const sourceCut = checks.branding.intro_frames + cut;
  const deltaMs = (bodyStart - sourceCut) / FPS * 1000;
  const { chapters, plannedTitle, plannedDescription, metadataMetrics, plannedLocalizations } = planUploadText(plan, frames);
  const tracked = [...plan.tracked, ...requiredIntro];
  const before = Object.fromEntries(tracked.map((p) => [p, sha(p)]));
  insist(before[body] === checks.branding.body_sha256, 'Body SHA differs from the source check record');
  insist(before[final] === metadata.final_sha256, 'Original final SHA differs from its upload metadata; select the authoritative source');
  const brandManifest = json(path.join(BRAND, 'manifest.json'));
  for (const role of ['intro', 'outro']) {
    const asset = brandManifest.assets.find((a) => a.role === role), file = path.join(BRAND, `${role}.mp4`);
    insist(before[file] === asset.sha256, `Brand ${role} hash mismatch`);
    const v = picture(probe(file)); insist(Number(v.nb_frames) === asset.frames && v.width === 1920 && v.height === 1080 && v.r_frame_rate === '30/1', `Brand ${role} format mismatch`);
  }
  insist(before[path.join(BRAND, 'outro.mp4')] === OUTRO_SHA, 'The specified v4 outro changed');
  const sourceVideo = picture(probe(body));
  insist(Number(sourceVideo.nb_frames) === timeline.total_frames, 'Source body frame count mismatch');
  for (const s of bodyScenes) {
    const p = picture(probe(s.file));
    insist(p?.codec_name === 'h264' && p.width === 1920 && p.height === 1080 && p.r_frame_rate === '30/1' && Number(p.nb_frames) === s.frames, `Source scene format/count mismatch: ${s.id}`);
  }
  save(path.join(out, 'source-provenance.json'), { created_at: new Date().toISOString(), source: entry, hashes_before: before, old_hook_removed_frames: cut, source_original_final_sha256: before[final], source_check: checks, note: 'Read-only source assets are guarded by hashes before and after. Small source records are frozen below. No original approvals or readiness are adopted.' });
  for (const p of [entry.metadata, path.join(src, 'timeline.json'), path.join(src, 'checks.json')]) copyFileSync(p, path.join(build, `source-${path.basename(p)}`));
  console.log(`${entry.slug}: ${frames} intro + ${bumperFrames} bumper + ${bodyFrames} retained body + ${outroFrames} outro frames`);

  // Use the already approved source scene imagery. No new image generation.
  const introSegments = [], visuals = [];
  let previousEnd = 0;
  for (let i = 0; i < shared.lines.length; i++) {
    const line = shared.lines[i], specLine = spec.lines.find((x) => x.id === line.id);
    const scene = line.source_scene ?? specLine?.scene;
    insist(scene && line.start_frame === previousEnd && line.end_frame > line.start_frame, `Non-contiguous introduction window: ${line.id}`);
    previousEnd = line.end_frame;
    const sourceScene = plan.allScenes.find((s) => s.id === scene);
    insist(sourceScene, `Missing source scene: ${scene}`);
    // Candidate keyframe filenames do not establish which image was delivered. Extract the
    // midpoint of the exact original scene segment, including its delivered crop/composition.
    const sourceSegment = sourceScene.file, sourceFrame = specLine && Object.hasOwn(specLine, 'source_frame') ? specLine.source_frame : Math.floor(sourceScene.frames / 2);
    insist(Number.isInteger(sourceFrame) && sourceFrame >= 0 && sourceFrame < sourceScene.frames, `Invalid source_frame for ${line.id}: must be an integer in [0, ${sourceScene.frames - 1}]`);
    tracked.push(sourceSegment); before[sourceSegment] ??= sha(sourceSegment);
    const image = path.join(build, `intro-${i}-source.png`);
    ff(['-v', 'error', '-i', sourceSegment, '-vf', `select=eq(n\\,${sourceFrame})`, '-fps_mode', 'passthrough', '-frames:v', '1', image]);
    const segment = path.join(build, `intro-${String(i).padStart(2, '0')}.mp4`), n = line.end_frame - line.start_frame;
    ff(['-v', 'error', '-loop', '1', '-framerate', '30', '-i', image,
      '-vf', `scale=1920:1080,zoompan=z='1+0.03*on/${Math.max(1, n - 1)}':x='iw/2-iw/zoom/2':y='ih/2-ih/zoom/2':d=1:s=1920x1080:fps=30,setsar=1,format=yuv420p,setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709`,
      '-frames:v', String(n), '-c:v', 'libx264', '-profile:v', 'high', '-preset', 'medium', '-crf', '18', '-tune', 'stillimage', '-bf', '2', '-g', '60', '-keyint_min', '30', '-r', '30', '-fps_mode', 'cfr', '-video_track_timescale', '15360', '-an', segment]);
    introSegments.push({ file: segment, frames: n }); visuals.push({ line: line.id, scene, source_segment: sourceSegment, source_frame: sourceFrame, source_segment_sha256: before[sourceSegment], image, image_sha256: sha(image), motion: 'center push from 1.00 to 1.03', start_frame: line.start_frame, end_frame: line.end_frame });
  }
  insist(previousEnd === frames, 'Intro visual windows do not cover the full common duration');
  const videoList = path.join(build, 'recut-video.ffconcat');
  // Bookend audio must not affect concat demuxer timestamps; normalize to picture-only files.
  const brandVideo = {};
  for (const role of ['intro', 'outro']) {
    brandVideo[role] = path.join(build, `brand-${role}-video.mp4`);
    ff(['-v', 'error', '-i', path.join(BRAND, `${role}.mp4`), '-map', '0:v:0', '-an', '-c:v', 'copy', brandVideo[role]]);
  }
  list(videoList, [...introSegments, { file: brandVideo.intro, frames: bumperFrames }, ...bodyScenes, { file: brandVideo.outro, frames: outroFrames }]);
  const audioResults = {}, captionsResults = {};
  mkdirSync(path.join(upload, 'dubs'), { recursive: true }); mkdirSync(path.join(upload, 'captions'), { recursive: true });
  for (const locale of LOCALES) {
    console.log(`${entry.slug}: ${locale} audio/captions`);
    const introDir = path.join(out, 'intro', locale), introInput = path.join(introDir, 'narration.wav');
    const check = json(path.join(introDir, 'check.json'));
    const originalFlags = check.flags ?? [], openingCheck = { original_report_ok: check.ok === true, original_flags: originalFlags, second_opinion_resolved: [], second_opinion_evidence: null };
    if (!check.ok && originalFlags.length) {
      const evidence = path.join(introDir, 'second-opinion.json');
      insist(existsSync(evidence), `${locale} introduction still has unresolved audio flags: ${originalFlags.join(', ')}`);
      const { readSecondOpinionResolutions } = await import('./retake.mjs');
      const resolved = await readSecondOpinionResolutions(introDir, check);
      insist(resolved instanceof Set && originalFlags.every((id) => resolved.has(id)), `${locale} introduction second opinion does not resolve every original flag`);
      tracked.push(evidence); before[evidence] = sha(evidence);
      const evidenceIndex = json(evidence), evidenceFiles = [];
      for (const id of originalFlags) {
        const pointer = evidenceIndex.lines?.[id], file = path.resolve(introDir, 'second-opinion', pointer?.file ?? '');
        insist(pointer && inside(file, path.join(introDir, 'second-opinion')) && sha(file) === pointer.sha256, `${locale} second-opinion evidence pointer changed: ${id}`);
        const clip = path.join(introDir, 'audio', `${id}.wav`);
        tracked.push(file, clip); before[file] = sha(file); before[clip] = sha(clip);
        evidenceFiles.push({ line: id, file, sha256: before[file], clip_sha256: before[clip] });
      }
      openingCheck.second_opinion_resolved = originalFlags.filter((id) => resolved.has(id));
      openingCheck.second_opinion_evidence = { file: evidence, sha256: before[evidence], entries: evidenceFiles };
    } else insist(check.ok === true, `${locale} introduction automated audio check is not clear`);
    const receipt = json(path.join(introDir, 'receipt.json')), binding = shared.tracks?.[locale];
    insist(binding && receipt.aligned && receipt.padding_ok && receipt.duration_ok, `${locale} introduction has no current shared alignment`);
    for (const [field, file] of Object.entries({ narration_sha256: introInput, timeline_sha256: path.join(introDir, 'timeline.json'), captions_sha256: path.join(introDir, `${locale}.srt`), receipt_sha256: path.join(introDir, 'receipt.json') })) {
      const actual = sha(file);
      insist(binding[field] === actual, `${locale} shared timeline does not bind current ${path.basename(file)}`);
      if (field !== 'receipt_sha256') insist(check[field] === actual && receipt[field] === actual, `${locale} checked media hash changed: ${field}`);
    }
    const introProbe = sound(probe(introInput));
    insist(Number(introProbe.sample_rate) === SR && Math.abs(Number(introProbe.duration_ts) * Number(introProbe.time_base.split('/')[0]) / Number(introProbe.time_base.split('/')[1]) * SR - frames * SPF) <= 1, `${locale} intro sample count mismatch`);
    const normalized = path.join(build, `intro-${locale}.wav`);
    normalizeIntro(introInput, normalized, frames);
    const sourceAudio = locale === 'zh-TW' ? body : entry.locales[locale].audio;
    const sourceStartFrames = locale === 'zh-TW' ? cut : sourceCut;
    const srcAudioProbe = sound(probe(sourceAudio));
    insist(Number(srcAudioProbe.duration) >= (sourceStartFrames + bodyFrames) / FPS - .025, `${locale} source audio is shorter than retained body`);
    const wav = locale === 'zh-TW' ? path.join(build, 'zh-TW.wav') : path.join(upload, 'dubs', `${locale}.wav`);
    const lengths = [frames, bumperFrames, bodyFrames, outroFrames], starts = [0, 0, sourceStartFrames, 0];
    const filters = lengths.map((n, i) => `[${i}:a:0]aresample=${SR},aformat=sample_fmts=s16:channel_layouts=stereo,atrim=start_sample=${starts[i] * SPF}:end_sample=${(starts[i] + n) * SPF},asetpts=PTS-STARTPTS,apad=whole_len=${n * SPF},atrim=end_sample=${n * SPF}[a${i}]`);
    filters.push('[a0][a1][a2][a3]concat=n=4:v=0:a=1[a]');
    ff(['-v', 'error', '-i', normalized, '-i', path.join(BRAND, 'intro.mp4'), '-i', sourceAudio, '-i', path.join(BRAND, 'outro.mp4'), '-filter_complex', filters.join(';'), '-map', '[a]', '-c:a', 'pcm_s16le', '-ar', String(SR), '-ac', '2', wav]);
    const retainedSourcePcm = pcmHash(sourceAudio, sourceStartFrames * SPF, bodyFrames * SPF), retainedOutputPcm = pcmHash(wav, bodyStart * SPF, bodyFrames * SPF);
    insist(retainedSourcePcm === retainedOutputPcm, `${locale}: body PCM changed in recut`);
    const wp = sound(probe(wav)), samples = Number(wp.duration_ts);
    insist(wp.time_base === '1/48000' && samples === totalFrames * SPF, `${locale}: output WAV is not exact length`);
    const level = loudness(wav);
    insist(level.integrated >= -18 && level.integrated <= -11 && level.true_peak <= -0.2, `${locale}: output loudness/peak outside recut QA limits`);
    audioResults[locale] = { file: wav, sha256: sha(wav), samples, total_frames: totalFrames, loudness: level, retained_body_pcm_sha256: retainedSourcePcm, body_samples_unchanged: true, opening_check: openingCheck, source_review_note: entry.locales[locale].source_review_note ?? null };
    const newCues = cues(path.join(introDir, `${locale}.srt`)), oldCues = cues(entry.locales[locale].captions);
    insist(newCues.every((c) => c.start >= 0 && c.end <= frames / FPS * 1000 + 1), `${locale}: introduction caption exceeds intro`);
    const cutMs = sourceCut / FPS * 1000, oldEnd = (checks.branding.intro_frames + timeline.total_frames) / FPS * 1000;
    insist(!oldCues.some((c) => c.start < cutMs - 1 && c.end > cutMs + 1), `${locale}: an old caption straddles the body cut`);
    const retained = oldCues.filter((c) => c.start >= cutMs - 1 && c.end <= oldEnd + 1).map((c) => ({ ...c, start: c.start + deltaMs, end: c.end + deltaMs }));
    const combined = [...newCues, ...retained];
    insist(retained.length && combined.every((c, i) => c.end > c.start && c.end <= (bodyStart + bodyFrames) / FPS * 1000 + 1 && (i === 0 || c.start >= combined[i - 1].end - 1)), `${locale}: captions overlap or leave retained picture range`);
    const cf = path.join(upload, 'captions', `${locale}.srt`); writeSrt(cf, combined);
    captionsResults[locale] = { file: cf, sha256: sha(cf), intro_cues: newCues.length, retained_body_cues: retained.length, dropped_old_hook_cues: oldCues.length - retained.length, offset_ms: deltaMs, text_unchanged: true };
  }
  const result = path.join(upload, 'final.mp4');
  console.log(`${entry.slug}: mux and full audiovisual decode`);
  ff(['-v', 'error', '-f', 'concat', '-safe', '0', '-i', videoList, '-i', audioResults['zh-TW'].file, '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '384k', '-ar', String(SR), '-ac', '2', '-video_track_timescale', '15360', '-movflags', '+faststart', result]);
  ff(['-v', 'error', '-xerror', '-i', result, '-map', '0:v:0', '-map', '0:a:0', '-f', 'null', '-']);
  const outputProbe = probe(result, true), v = picture(outputProbe), a = sound(outputProbe);
  insist(Number(v.nb_read_frames) === totalFrames, `Final decoded frame count ${v.nb_read_frames} != ${totalFrames}`);
  insist(Math.abs(Number(v.duration) - totalFrames / FPS) <= 1 / FPS && Math.abs(Number(a.duration) - totalFrames / FPS) < .065, 'Final A/V duration mismatch');
  const sourcePackets = packetHashes(body).slice(cut), resultPackets = packetHashes(result).slice(bodyStart, bodyStart + bodyFrames);
  let retention = 'encoded_packet_sha256';
  if (JSON.stringify(sourcePackets) !== JSON.stringify(resultPackets)) {
    console.log(`${entry.slug}: MP4 packet headers differ; verifying decoded retained pictures`);
    const sourceFrames = decodedHashes(body, cut, timeline.total_frames), resultFrames = decodedHashes(result, bodyStart, bodyStart + bodyFrames);
    insist(sourceFrames.length === bodyFrames && JSON.stringify(sourceFrames) === JSON.stringify(resultFrames), 'Retained body pictures changed');
    retention = 'decoded_frame_md5';
  }
  const finalLevel = loudness(result);
  insist(finalLevel.integrated >= -18 && finalLevel.integrated <= -11 && finalLevel.true_peak <= -0.1, 'Final AAC loudness/peak outside QA limits');
  const finalSha = sha(result);
  const newMeta = {
    slug: entry.slug, edition: 'curio-five-recuts-20261012', default_language: 'zh-TW', category_id: metadata.category_id,
    made_for_kids: metadata.made_for_kids, privacy_status: 'private', video_id: null,
    title: plannedTitle, description: plannedDescription, tags: metadata.tags, chapters,
    localizations: plannedLocalizations, metadata_limits: metadataMetrics, final_sha256: finalSha, branding_hash: sha(path.join(BRAND, 'manifest.json')),
    captions: LOCALES.map((l) => `captions/${l}.srt`), caption_bindings: Object.fromEntries(LOCALES.map((l) => [l, { file: `captions/${l}.srt`, sha256: captionsResults[l].sha256, final_sha256: finalSha }])),
    dubs: LOCALES.filter((l) => l !== 'zh-TW').map((l) => ({ locale: l, file: `dubs/${l}.wav`, format: 'wav', total_frames: totalFrames, sha256: audioResults[l].sha256, final_sha256: finalSha })),
    thumbnail: metadata.thumbnail, thumbnails: {}, contains_synthetic_media: metadata.contains_synthetic_media, disclosure_reason: metadata.disclosure_reason,
    language_choice: Object.fromEntries(LOCALES.filter((l) => l !== 'zh-TW').map((l) => [l, { metadata: true, captions: true, dub: true }])),
    uploaded: false, published: false, owner_playback_verified: false, youtube_endscreens_configured: false,
  };
  for (const [locale, relative] of Object.entries(metadata.thumbnails ?? {})) {
    const name = typeof relative === 'string' ? relative : relative.file;
    if (!name) continue;
    const from = path.resolve(path.dirname(entry.metadata), name), to = path.join(upload, name);
    insist(inside(to, upload) && existsSync(from), `Missing/unsafe ${locale} thumbnail`);
    mkdirSync(path.dirname(to), { recursive: true }); copyFileSync(from, to); newMeta.thumbnails[locale] = name;
  }
  if (metadata.thumbnail) {
    const thumbnail = path.resolve(path.dirname(entry.metadata), metadata.thumbnail);
    insist(inside(path.join(upload, metadata.thumbnail), upload), 'Unsafe thumbnail output');
    copyFileSync(thumbnail, path.join(upload, metadata.thumbnail));
  }
  save(path.join(upload, 'metadata.json'), newMeta);
  for (const locale of LOCALES) {
    const m = locale === 'zh-TW' ? newMeta : newMeta.localizations[locale];
    writeFileSync(path.join(upload, `description.${locale}.txt`), `${m.title}\n\n${m.description}\n`);
  }
  writeFileSync(path.join(upload, 'chapters.txt'), chapters.map((c) => `${c.at} ${c.title}`).join('\n') + '\n');
  const endscreen = { template_video_id: 'oxEtlA8GWas', start_frame: totalFrames - 17 * FPS, end_frame: totalFrames, start_seconds: totalFrames / FPS - 17, end_seconds: totalFrames / FPS, elements: [{ type: 'video', choice: 'latest_upload' }, { type: 'video', choice: 'best_for_viewer' }, { type: 'subscribe' }], slots: brandManifest.outro_source.end_screen_slots, setup_in_youtube_studio_required: true, configured: false };
  insist(endscreen.start_frame >= totalFrames - outroFrames && endscreen.start_frame >= totalFrames - 20 * FPS && endscreen.end_frame === totalFrames && endscreen.end_seconds - endscreen.start_seconds === 17 && endscreen.elements.length === 3, 'End-screen interval is not a valid final-17-second interval inside the new outro');
  save(path.join(upload, 'endscreen-setup.json'), endscreen);
  const after = Object.fromEntries([...new Set(tracked)].map((p) => [p, sha(p)]));
  insist(Object.entries(before).every(([p, hash]) => after[p] === hash), 'A source changed during rendering; discard this recut and inspect ownership');
  const qa = { schema_version: 1, ok: true, created_at: new Date().toISOString(), final_sha256: finalSha, dimensions: [v.width, v.height], fps: FPS, total_frames: totalFrames, decoded_frames: Number(v.nb_read_frames), duration_seconds: totalFrames / FPS, full_av_decode: 'passed', original_hook_removed_frames: cut, intro_frames: frames, bumper_frames: bumperFrames, retained_body_frames: bodyFrames, outro_frames: outroFrames, retained_body_start_frame: bodyStart, retained_body_picture_check: retention, retained_body_picture_unchanged: true, body_video_reencoded: false, final_loudness: finalLevel, audio: audioResults, captions: captionsResults, chapters, metadata_limits: metadataMetrics, endscreen_interval_valid: true, intro_visuals: visuals, source_hashes_before: before, source_hashes_after: after, sources_unchanged: true, review_limitations: { original_locale_notes: Object.fromEntries(LOCALES.map((l) => [l, entry.locales[l].source_review_note ?? null])), owner_playback_verified: false, youtube_endscreens_configured: false, uploaded: false, published: false } };
  save(path.join(out, 'qa.json'), qa);
  save(path.join(upload, 'checksums.json'), Object.fromEntries([result, ...Object.values(audioResults).filter((r) => inside(r.file, upload)).map((r) => r.file), ...Object.values(captionsResults).map((r) => r.file), path.join(upload, 'metadata.json'), path.join(upload, 'endscreen-setup.json')].map((p) => [path.relative(upload, p).replaceAll('\\', '/'), sha(p)])));
  console.log(`${entry.slug}: PASS ${totalFrames} frames; ${finalSha}`);
  activeOutput = null;
  return { slug: entry.slug, final: result, final_sha256: finalSha, qa: path.join(out, 'qa.json') };
}

try {
  const sourceMap = json(MAP), specs = existsSync(SPECS) ? json(SPECS) : { episodes: [] };
  const selection = option('--slug', null), selected = selection ? [selection] : SLUGS;
  insist(selected.every((s) => SLUGS.includes(s)), 'Slug is not one of the five authorized recuts');
  const results = [];
  for (const slug of selected) {
    const entry = sourceMap.episodes.find((e) => e.slug === slug), spec = specs.episodes.find((e) => e.slug === slug);
    insist(entry, `No authoritative source map entry: ${slug}`);
    const plan = sourcePlan(entry, spec);
    if (DRY) {
      const aligned = existsSync(plan.sharedPath) ? json(plan.sharedPath) : null;
      const textPreview = planUploadText(plan, aligned?.total_frames ?? 1800);
      results.push({ slug, source: plan.src, output: plan.out, original_body_frames: plan.timeline.total_frames, old_hook_removed_frames: plan.cut, retained_body_frames: plan.timeline.total_frames - plan.cut, retained_scenes: plan.bodyScenes.length, pending_intro_files: plan.missingIntro, pending_spec: !spec, metadata_limits: textPreview.metadataMetrics, metadata_timing_basis: aligned ? 'actual-aligned-intro' : '60-second-preview', source_final_matches_metadata: sha(plan.final) === plan.metadata.final_sha256, source_body_matches_checks: sha(plan.body) === plan.checks.branding.body_sha256 });
    } else { insist(spec, `Missing opening spec: ${slug}`); results.push(await assemble(plan)); }
  }
  console.log(JSON.stringify({ dry_run: DRY, episodes: results }, null, 2));
} catch (error) {
  if (activeOutput) save(path.join(activeOutput, 'qa.json'), { ok: false, status: 'failed', failed_at: new Date().toISOString(), error: error.message, uploaded: false, published: false, note: 'Partial artifacts are not ready for upload. Inspect logs; rerun only after resolving the failure.' });
  console.error(error.stack || error.message); process.exitCode = 1;
}
