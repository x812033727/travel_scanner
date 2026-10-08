// A delivery supplement for the English-teaching profile. The official main
// package remains byte-for-byte intact. Mixed tracks have their own evidence;
// this helper never writes official QA, approvals or generic dub manifests.
import { createHash, randomUUID } from 'node:crypto';
import { copyFileSync, existsSync, lstatSync, mkdirSync, readFileSync, renameSync, rmSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { isDeepStrictEqual, parseArgs } from 'node:util';
import { approvalState, sha256File } from '../core/approvals.mjs';
import { checkCues, parseSrt, toSrt } from '../core/captions.mjs';
import { emptyLexicon } from '../core/lexicon.mjs';
import { atomicWrite, isInside, readJson, ROOT, stopRequested } from '../core/paths.mjs';
import { acquireProjectLease } from '../core/project-lease.mjs';
import { metadataLocalesOf, readLanguages } from '../core/stages.mjs';
import { loadProject } from '../core/state.mjs';
import { speechLexicon } from '../dubs/plan.mjs';
import { readPackageReport } from '../package/check.mjs';
import { composeMetadata } from '../package/metadata.mjs';
import { ITEM_IDS } from '../qa/checks.mjs';
import { parseWav, requireNarrationFormat } from '../tts/wav.mjs';
import { passedCurrentCheck, planTeachingAudio, requireCurrentTeachingPlan, requireTeachingSource, teachingCaptions, TEACHING_ARTIFACTS, TEACHING_LOCALES, TEACHING_SCHEMA, validateTeachingManifest } from './teaching-audio.mjs';

export const DELIVERY_SCHEMA = 'airport-teaching-delivery/v1';
export const PREVIEW_LOCALES = { 'zh-TW': 'zh-Hant', 'zh-CN': 'zh-Hans', ja: 'ja', ko: 'ko' };
const PREVIEW = fileURLToPath(new URL('./preview/', import.meta.url));
const ASSETS = ['START_HERE.html', 'player.mjs', 'controller.mjs', 'style.css', 'serve.py', 'README.txt'];
const hash = (value) => createHash('sha256').update(Buffer.isBuffer(value) || typeof value === 'string' ? value : JSON.stringify(value)).digest('hex');
const save = (file, data) => atomicWrite(file, `${JSON.stringify(data, null, 2)}\n`);
const pad = (day) => String(day).padStart(2, '0');
const SHA256 = /^[a-f0-9]{64}$/;

export function requireMainQa(report, finalSha) {
  if (report?.ok !== true || report.final_sha256 !== finalSha || report.items?.length !== ITEM_IDS.length || report.items.some((item, index) => item.id !== ITEM_IDS[index] || item.ok !== true)) throw new Error('Main video requires all eleven genuine QA items bound to its current final SHA256');
}

/** Re-evaluate every line, not just a stored passed flag or an empty flags list. */
export function requireMixedCheck({ manifest, manifestSha, report, readClip, lexicon }) {
  if (report?.schema !== TEACHING_SCHEMA || report.status !== 'mixed_audio_check_passed_pending_final_review' || report.manifest_sha256 !== manifestSha || report.track_sha256 !== manifest.artifacts['track.m4a'] || !Array.isArray(report.flags) || report.flags.length || report.unchecked !== 0) throw new Error('Mixed teaching-audio check is missing, stale or failed');
  if (!report.lines || Object.keys(report.lines).length !== manifest.lines.length) throw new Error('Mixed check must cover every current line exactly once');
  for (const line of manifest.lines) {
    const bytes = readClip(line.clip);
    if (hash(bytes) !== line.clip_sha256 || requireNarrationFormat(parseWav(bytes)).length !== line.audio_samples) throw new Error(`Mixed clip or timing changed: ${line.id}`);
    const check = report.lines[line.id];
    if (check?.passed !== true || check.language !== line.speech_locale || check.clip_sha256 !== line.clip_sha256 || !passedCurrentCheck(check, { id: line.id, text: line.text }, bytes, speechLexicon(lexicon, line.speech_locale), line.speech_locale)) throw new Error(`No genuine current mixed check for ${line.id}`);
  }
}

function regular(file) {
  if (!lstatSync(file).isFile()) throw new Error(`Delivery input must be a regular file: ${file}`);
}

/** Inspect current official and mixed evidence; no network, media writes or approvals. */
export async function inspectDeliveryEpisode({ projectRoot, mediaRoot, day }) {
  if (!Number.isInteger(day) || day < 1 || day > 60) throw new Error('day must be 1 through 60');
  const slug = `airport-english-day${pad(day)}`;
  const project = loadProject({ slug, root: projectRoot });
  const workdir = path.join(mediaRoot, slug);
  if (stopRequested(workdir)) throw new Error('STOP requested; delivery is incomplete');
  const specificationFile = path.join(project.dir, 'teaching-audio.json');
  const specification = readJson(specificationFile);
  const source = await requireTeachingSource({ project, workdir });
  const finalApproval = await approvalState({ gate: 'final', docDir: project.dir, workdir });
  if (finalApproval.status !== 'approved' || finalApproval.sha256 !== source.source_final_sha256) throw new Error('Current main final approval is required');
  const qaFile = path.join(workdir, 'review', 'qa.json');
  const qa = readJson(qaFile, null);
  requireMainQa(qa, source.source_final_sha256);
  const main = await readPackageReport(workdir);
  if (!main.report.ok || main.finalSha256 !== source.source_final_sha256 || main.metadata?.default_language !== 'en') throw new Error('Current official English main upload package must pass its own package check');
  const languages = readLanguages(workdir);
  if (!languages || TEACHING_LOCALES.some((locale) => !languages.locales[locale]?.dub || !languages.locales[locale]?.captions)) throw new Error('All four requested teaching audio/CC locales must remain selected');
  if ((main.metadata.dubs ?? []).length || [...main.files.keys()].some((name) => name.startsWith('dubs/'))) throw new Error('Generic dub files do not belong in the English-dialogue teaching delivery');
  const expected = composeMetadata({ doc: project.doc, timeline: source.presentation, translations: project.translations, pack: project.pack ?? null, locales: metadataLocalesOf(languages, 'en') });
  if (expected.problems.length || Object.entries(expected.metadata).some(([key, value]) => !isDeepStrictEqual(main.metadata[key], value))) throw new Error('Official package metadata differs from current source metadata/chapters/translations');

  const copies = [];
  for (const name of [...main.files.keys()].sort()) {
    const file = path.join(workdir, 'upload', name);
    regular(file);
    copies.push({ source: file, destination: `day${pad(day)}/main/${name}`, sha256: await sha256File(file) });
  }
  if (copies.find((file) => file.destination.endsWith('/main/metadata.json'))?.sha256 !== main.report.final_sha256) throw new Error('Main package changed while its report was read');
  copies.push({ source: qaFile, destination: `day${pad(day)}/evidence/main-qa.json`, sha256: await sha256File(qaFile) });
  const tracks = {};
  for (const locale of TEACHING_LOCALES) {
    const plan = planTeachingAudio({ project, specification, locale });
    const directory = path.join(workdir, 'teaching-audio', locale);
    const manifestFile = path.join(directory, 'manifest.json');
    const checkFile = path.join(directory, 'check.json');
    const manifest = readJson(manifestFile, null);
    validateTeachingManifest(manifest, plan, source);
    const manifestSha = await sha256File(manifestFile);
    for (const name of TEACHING_ARTIFACTS) {
      const file = path.join(directory, name); regular(file);
      if (await sha256File(file) !== manifest.artifacts[name]) throw new Error(`Stale ${locale} mixed artifact: ${name}`);
    }
    const report = readJson(checkFile, null);
    requireMixedCheck({ manifest, manifestSha, report, readClip: (name) => readFileSync(path.join(directory, name)), lexicon: project.shelfLexicon ?? emptyLexicon() });
    const captionFile = path.join(directory, 'captions.srt');
    const captionBytes = readFileSync(captionFile, 'utf8');
    const regenerated = teachingCaptions(manifest.lines, locale, manifest.intro_frames);
    if (toSrt(regenerated.cues) !== captionBytes) throw new Error(`The ${locale} CC no longer matches current mixed speech timing`);
    const cues = parseSrt(captionBytes);
    const errors = checkCues(cues, locale).filter((item) => !item.includes('characters a second'));
    if (!cues.length || errors.length || cues.some((cue) => cue.start_ms < 0 || cue.end_ms > 600000)) throw new Error(`Invalid ${locale} delivery captions`);
    const audioPath = `day${pad(day)}/teaching-audio/${locale}.m4a`;
    const captionPath = `day${pad(day)}/teaching-captions/${locale}.srt`;
    for (const [name, destination] of [['track.m4a', audioPath], ['captions.srt', captionPath], ['captions.vtt', `day${pad(day)}/teaching-captions/${locale}.vtt`]]) copies.push({ source: path.join(directory, name), destination, sha256: manifest.artifacts[name] });
    for (const [name, sha] of [['manifest.json', manifestSha], ['check.json', await sha256File(checkFile)]]) copies.push({ source: path.join(directory, name), destination: `day${pad(day)}/evidence/${locale}-${name}`, sha256: sha });
    tracks[locale] = { audio: audioPath, captions: captionPath, audio_sha256: manifest.artifacts['track.m4a'], captions_sha256: manifest.artifacts['captions.srt'], manifest_sha256: manifestSha, check_sha256: await sha256File(checkFile), cues, warnings: regenerated.warnings };
    requireCurrentTeachingPlan({ project, specificationFile, locale, fingerprint: plan.fingerprint });
  }
  const title = project.translations['zh-TW']?.title ?? project.doc.youtube.title;
  return { day, slug, title, copies, tracks, chapters: (source.presentation.chapters ?? []).map((chapter) => ({ start: chapter.start_frame / 30, title: chapter.title })),
    main_package_report: main.report, source_final_sha256: source.source_final_sha256, source_timeline_sha256: source.source_timeline_sha256,
    source_script_sha256: hash(project.doc), language_choice_sha256: hash(languages), qa_sha256: await sha256File(qaFile), main_audio_approval_sha256: source.approval.sha256,
    duration_seconds: 600, combined_formal_qa_approved: false, publication_approved: false };
}

export function previewLesson(episode) {
  return { day: episode.day, title: episode.title, master: `day${pad(episode.day)}/main/final.mp4`,
    audio: Object.fromEntries(TEACHING_LOCALES.map((locale) => [PREVIEW_LOCALES[locale], episode.tracks[locale].audio])),
    captions: Object.fromEntries(TEACHING_LOCALES.map((locale) => [PREVIEW_LOCALES[locale], episode.tracks[locale].cues.map((cue) => [cue.start_ms / 1000, cue.end_ms / 1000, cue.text])])),
    chapters: episode.chapters,
    files: episode.copies.filter((file) => !file.destination.includes('/evidence/') && !file.destination.includes('/main/captions/') && !file.destination.endsWith('/main/UPLOAD.md')).map((file) => ({ name: file.destination.split('/').slice(1).join('/'), url: file.destination })) };
}

export function combinedReviewTemplate(delivery, deliverySha) {
  return { schema: 'airport-combined-review/v1', status: 'pending_actual_combined_preview_review', delivery_sha256: deliverySha,
    official_qa_approval: false, publication_approval: false,
    instruction: 'Review the actual linked files. Filling this checklist does not create or replace an official approval.',
    episodes: delivery.episodes.map((episode) => ({ day: episode.day, final_sha256: episode.source_final_sha256, items: [
      { id: 'english-picture-and-main-audio', checked: false, notes: '' },
      ...TEACHING_LOCALES.map((locale) => ({ id: `mixed-audio-and-independent-cc-${locale}`, track_sha256: episode.tracks[locale].audio_sha256, captions_sha256: episode.tracks[locale].captions_sha256, checked: false, notes: '' })),
      { id: 'quiz-evidence-and-response-pauses', checked: false, notes: '' },
      { id: 'mobile-caption-controls-and-audio-switching', checked: false, notes: '' },
      { id: 'branding-600-seconds-metadata-and-thumbnail', checked: false, notes: '' },
    ] })) };
}

const guide = `機場英文系列：合併預覽與 YouTube Studio 準備資料\n\n此包保留已核准英文主片的官方上傳包，以及四種已完成逐句語音查核的教學音軌與 CC。\n整合預覽的最後審閱仍待完成；此包不是官方整合 QA／發布核准，也沒有上傳到 YouTube。\n\n預覽：執行 python3 serve.py（Windows 可用 py -3 serve.py），開啟顯示的本機網址。\n保持終端機開啟。字幕、音軌可各自選擇。英文固定在影片內，情境對話維持英文。\n\n每集資料夾：\n- main/final.mp4：英文主片。\n- teaching-audio/：繁中、簡中、日、韓四種教學音軌 M4A。\n- teaching-captions/：對應的四種 SRT CC；VTT 可供其他播放器使用。\n- main/metadata.json、description.*.txt、thumbnail*.jpg：保留官方英文主片包的原始 metadata、說明與縮圖。\n- main/captions/：官方主片原始字幕，留存來源證據；本合併預覽採用 teaching-captions/。\n- evidence/：原始主片 QA 和混合語音查核的證據快照；不代表原始 WAV 也包含在此包。\n\nmain/metadata.json 只描述原官方主片包；它不替四種混合音軌或本合併包提供核准。\n完整檔案清單、hash 與混合音軌對照在 delivery.json。\nCOMBINED_REVIEW.json 綁定此包的 hash，供實際整合預覽審閱；填寫它不會建立官方核准。\n\n未來獲准上架時，在 Studio 分別匯入主片、四份 SRT 與四條 M4A；頻道需具備多語音軌功能。\n付費宣傳、兒童觀眾、合成內容與公開／排程設定仍按頻道實際決定和核准執行。\n`;

/** Copy only known, hash-bound files; never hard-link mutable production media. */
export async function copyVerified(file, root) {
  if (!file.destination || path.isAbsolute(file.destination) || file.destination.split(/[\\/]/).includes('..') || !SHA256.test(file.sha256 ?? '')) throw new Error('Unsafe or unhashed delivery file');
  regular(file.source);
  if (await sha256File(file.source) !== file.sha256) throw new Error(`Source changed before copying: ${file.destination}`);
  const destination = path.join(root, file.destination);
  mkdirSync(path.dirname(destination), { recursive: true });
  copyFileSync(file.source, destination);
  if (await sha256File(destination) !== file.sha256 || await sha256File(file.source) !== file.sha256) throw new Error(`Source changed while copying: ${file.destination}`);
  return { path: file.destination, sha256: file.sha256, bytes: lstatSync(destination).size };
}

function validateRoots({ projectRoot, mediaRoot, out }) {
  if (!projectRoot || !mediaRoot || isInside(projectRoot, mediaRoot) || isInside(mediaRoot, projectRoot) || isInside(mediaRoot, ROOT)) throw new Error('Project and media directories must be separate; media must remain outside Git');
  if (out && [ROOT, projectRoot, mediaRoot].some((directory) => isInside(out, directory) || isInside(directory, out))) throw new Error('Delivery output must be separate from source and active media directories');
}
const fullSeries = () => Array.from({ length: 60 }, (_, index) => index + 1);
function selectedDays(days) {
  const selected = [...(days ?? fullSeries())].sort((a, b) => a - b);
  if (!selected.length || new Set(selected).size !== selected.length || selected.some((day) => !Number.isInteger(day) || day < 1 || day > 60)) throw new Error('Choose unique days from 1 through 60');
  return selected;
}

export async function planDelivery({ projectRoot, mediaRoot, days }) {
  validateRoots({ projectRoot, mediaRoot });
  const episodes = [];
  for (const day of selectedDays(days)) {
    try {
      const result = await inspectDeliveryEpisode({ projectRoot, mediaRoot, day });
      episodes.push({ day, ready_to_copy: true, source_final_sha256: result.source_final_sha256 });
    } catch (error) { episodes.push({ day, ready_to_copy: false, blocker: error.message }); }
  }
  return { schema: DELIVERY_SCHEMA, status: episodes.every((episode) => episode.ready_to_copy) ? 'inputs_checked_pending_copy_and_combined_review' : 'blocked_before_delivery', episodes, paid_requests: 0, media_created: false, combined_formal_qa_approved: false, publication_approved: false };
}

export async function buildDelivery({ projectRoot, mediaRoot, out, days }) {
  validateRoots({ projectRoot, mediaRoot, out });
  if (!out || existsSync(out)) throw new Error('Choose a new delivery output directory; existing deliverables are never overwritten');
  const chosen = selectedDays(days);
  const leases = [];
  const partial = `${out}.partial-${randomUUID()}`;
  try {
    for (const day of chosen) leases.push(acquireProjectLease(path.join(mediaRoot, `airport-english-day${pad(day)}`), { owner: 'airport-delivery' }));
    const episodes = [];
    for (const day of chosen) episodes.push(await inspectDeliveryEpisode({ projectRoot, mediaRoot, day }));
    mkdirSync(partial, { recursive: true });
    const files = [];
    for (const episode of episodes) {
      for (const file of episode.copies) {
        if (stopRequested(path.join(mediaRoot, episode.slug))) throw new Error('STOP requested; partial delivery was not promoted');
        files.push(await copyVerified(file, partial));
      }
      const reportName = `day${pad(episode.day)}/evidence/main-package-report.json`;
      save(path.join(partial, reportName), episode.main_package_report);
      files.push({ path: reportName, sha256: await sha256File(path.join(partial, reportName)), bytes: lstatSync(path.join(partial, reportName)).size });
    }
    for (const name of ASSETS) files.push(await copyVerified({ source: path.join(PREVIEW, name), destination: name, sha256: await sha256File(path.join(PREVIEW, name)) }, partial));
    atomicWrite(path.join(partial, 'lessons.js'), `window.SERIES={episodeCount:60};\nwindow.LESSONS=${JSON.stringify(episodes.map(previewLesson))};\n`);
    atomicWrite(path.join(partial, 'UPLOAD_GUIDE.txt'), guide);
    for (const name of ['lessons.js', 'UPLOAD_GUIDE.txt']) files.push({ path: name, sha256: await sha256File(path.join(partial, name)), bytes: lstatSync(path.join(partial, name)).size });
    // Validate every source again after the potentially long copy. A source edit
    // cannot silently promote a mixture of generations under one delivery hash.
    for (const episode of episodes) {
      const current = await inspectDeliveryEpisode({ projectRoot, mediaRoot, day: episode.day });
      if (!isDeepStrictEqual(current, episode)) throw new Error(`Day${pad(episode.day)} changed during packaging; no delivery was promoted`);
    }
    const publicEpisodes = episodes.map(({ copies, tracks, main_package_report, ...episode }) => ({ ...episode, tracks: Object.fromEntries(Object.entries(tracks).map(([locale, { cues, ...track }]) => [locale, track])), official_main_package_report_sha256: hash(`${JSON.stringify(main_package_report, null, 2)}\n`) }));
    const manifest = { schema: DELIVERY_SCHEMA, status: 'prepared_pending_actual_combined_review', episode_count: episodes.length, series_episode_count: 60, episodes: publicEpisodes, files,
      combined_formal_qa_approved: false, publication_approved: false, uploaded_to_youtube: false, created_at: new Date().toISOString() };
    save(path.join(partial, 'delivery.json'), manifest);
    const review = combinedReviewTemplate(manifest, await sha256File(path.join(partial, 'delivery.json')));
    save(path.join(partial, 'COMBINED_REVIEW.json'), review);
    renameSync(partial, out);
    return { directory: out, delivery_sha256: await sha256File(path.join(out, 'delivery.json')), ...manifest };
  } catch (error) {
    rmSync(partial, { recursive: true, force: true });
    throw error;
  } finally { for (const lease of leases.reverse()) lease.release(); }
}

export async function main(args = process.argv.slice(2)) {
  const [command, ...rest] = args;
  if (!['plan', 'build'].includes(command)) throw new Error('Usage: delivery.mjs plan|build --project-root /staged/project --media-root /external/media [--out /new/delivery] [--days 1,2]');
  const { values } = parseArgs({ args: rest, options: { 'project-root': { type: 'string' }, 'media-root': { type: 'string' }, out: { type: 'string' }, days: { type: 'string' } }, strict: true });
  const input = { projectRoot: values['project-root'] && path.resolve(values['project-root']), mediaRoot: values['media-root'] && path.resolve(values['media-root']), out: values.out && path.resolve(values.out), days: values.days?.split(',').map(Number) };
  return command === 'plan' ? planDelivery(input) : buildDelivery(input);
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().then((result) => { process.stdout.write(`${JSON.stringify(result, null, 2)}\n`); if (result.status === 'blocked_before_delivery') process.exitCode = 1; }).catch((error) => { process.stderr.write(`${error.message}\n`); process.exitCode = 1; });
}
