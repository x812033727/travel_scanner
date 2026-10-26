// CANDIDATE ONLY: one separately authorized, zero-network native caption unit.
// No TTS/ASR, automation.moved, package, review-push, owner operation, or rollback.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual as same } from 'node:util';
import { execFileSync } from 'node:child_process';

const ROOT = '/workspace/travel_scanner_pdf';
const HOME = '/workspace/work/ai-pdf-01';
const SLUG = 'ai-pdf-quotes-to-comparison';
const WORK = path.join(HOME, 'media', SLUG);
const DOC = path.join(ROOT, 'docs/videos', SLUG);
const ORIGINAL = '/workspace/work/ai-animation-01/media/ai-editable-explainer-animation';
const PREP = '/workspace/work/ai-pdf-01/free-caption-preparation-20261026T2144Z';
const OUT = path.join(PREP, 'one-use-execution');
const AUDIT = '/workspace/work/ai-animation-01/watch-readonly-20261026T2136Z/audit.json';
const AUDIT_SHA = 'a74375e990fec5186cfd2ef7a1a61d0b65c7e00a0ffa9e2c6d2b28d6a8d0fea7';
const OTHER_INPUTS = ['docs/videos/lexicon.json', 'tools/video/cli.mjs', 'tools/video/core/state.mjs', 'tools/video/core/stages.mjs', 'tools/video/core/branding.mjs', 'tools/video/core/captions.mjs', 'tools/video/core/timeline.mjs', 'tools/video/core/paths.mjs', 'tools/video/core/project-lease.mjs', 'tools/video/core/schema.mjs', 'tools/video/core/approvals.mjs', 'tools/video/core/lexicon.mjs', 'tools/video/core/lexicon-store.mjs', 'tools/video/core/translations.mjs', 'tools/video/dubs/plan.mjs', 'tools/video/qa/checks.mjs', 'tools/video/review/renewal-handoff.mjs'];
const PRIMARY = '346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f';
const SOURCE = 'eac88936fbcb0324208d639b75ddad8f045c6bcc3cc8c4f60d89ebc6c65f3e04';
const FOREIGN = ['en', 'ja', 'ko', 'es', 'pt', 'id', 'vi', 'th'];
const LOCALES = ['zh-TW', ...FOREIGN];
const ALLOWED = new Set(['state.json', 'captions/manifest.json', ...LOCALES.flatMap(l => [`captions/${l}.srt`, `captions/${l}.vtt`])]);
const SELF = path.join(PREP, 'free-caption-one-use.mjs');
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const sha = file => hash(fs.readFileSync(file));
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const insist = (ok, message) => { if (!ok) throw new Error(message); };
const save = (name, value) => fs.writeFileSync(path.join(OUT, name), JSON.stringify(value, null, 2) + '\n', { flag: 'wx' });
const now = () => new Date().toISOString();
const git = (...args) => execFileSync('git', args, { cwd: ROOT, encoding: 'utf8' }).trim();
const keys = object => Object.keys(object ?? {}).sort();
const sameSet = (a, b) => same([...a].sort(), [...b].sort());
const age = stamp => (Date.now() - Date.parse(stamp)) / 1000;

function files(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir, { withFileTypes: true }).flatMap(entry => {
    const file = path.join(dir, entry.name);
    if (entry.isDirectory()) return files(file);
    insist(entry.isFile(), `Non-regular file needs inspection: ${file}`);
    return [file];
  });
}
function snapshot(dir, excluded = new Set()) {
  return Object.fromEntries(files(dir).sort().filter(f => !excluded.has(path.relative(dir, f))).map(f => [path.relative(dir, f), sha(f)]));
}
function changed(before, after) {
  return [...new Set([...keys(before), ...keys(after)])].sort().filter(file => before[file] !== after[file]);
}
function controllers() {
  return fs.readdirSync('/proc').filter(name => /^\d+$/.test(name) && Number(name) !== process.pid).flatMap(name => {
    try {
      const args = fs.readFileSync(`/proc/${name}/cmdline`, 'utf8').split('\0').filter(Boolean);
      const executable = path.basename(args[0] ?? '');
      const selected = /^(node|python(?:3(?:\.\d+)?)?|ffmpeg)$/.test(executable)
        && args.slice(1).some(arg => /ai-pdf-01|ai-animation-01|whisper_second_opinion/.test(arg));
      return selected ? [{ pid: Number(name), executable }] : [];
    } catch { return []; }
  });
}
function idleControls() {
  insist(controllers().length === 0, 'An actual PDF/original/Whisper controller is live');
  for (const dir of [WORK, path.dirname(WORK), HOME, ORIGINAL, path.dirname(ORIGINAL), '/workspace/work/ai-animation-01']) {
    for (const name of ['LEASE', 'STOP']) insist(!fs.existsSync(path.join(dir, name)), `${name} exists at ${dir}`);
  }
}
function nativeState() {
  const state = read(path.join(WORK, 'auto.json'));
  insist(state.status === 'done' && !state.tidied_at && state.defer_count === 3 && state.deferred_until === '2026-10-26T22:03:11.200Z', 'Saved global defer3 is different; do not reset or ignore it');
  insist(same(state.languages.pt, { shorten: 0, retakes: 0, reword: 0, check_stopped: true }), 'PT native state differs');
  insist(same(state.languages.en, { shorten: 1, retakes: 2, reword: 2, check_stopped: true }), 'EN exhausted state differs');
  insist(same(state.languages.ja, { shorten: 0, retakes: 2, reword: 2, check_stopped: true }), 'JA exhausted state differs');
  // No time comparison: this FREE unit cannot dispatch speech or clear the future backoff.
  return state;
}
function meaningChains() {
  insist(sha(path.join(DOC, 'video.json')) === SOURCE, 'Chinese source changed');
  return FOREIGN.map(locale => {
    const file = path.join(DOC, 'research/translation-reviews', `${locale}.meaning-review.json`);
    const index = read(file);
    const report = path.resolve(DOC, index.report_file ?? '');
    insist(index.schema_version === 1 && index.passed === true && index.scope === 'source-meaning-and-naturalness'
      && index.source_video_sha256 === SOURCE && index.translation_sha256 === sha(path.join(DOC, 'i18n', `${locale}.json`))
      && report.startsWith(DOC + path.sep) && sha(report) === index.report_sha256, `${locale} actual meaning chain is not current`);
    for (const boundary of files(path.join(HOME, 'author-review-boundaries')).filter(f => new RegExp(`^${locale}\\.(shorten|reword)\\.round-[12]\\..+\\.json$`).test(path.basename(f)))) {
      insist((index.reviewed_boundaries ?? []).some(row => row.file === path.relative(HOME, boundary) && row.sha256 === sha(boundary)), `${locale} has an actual unreviewed model boundary`);
    }
    return { locale, index_sha256: sha(file), translation_sha256: index.translation_sha256, report_sha256: index.report_sha256 };
  });
}

const argv = process.argv.slice(2);
insist(argv.shift() === '--execute', 'Candidate is not an execution authorization: explicit root GO and --execute required');
const options = {};
while (argv.length) {
  const flag = argv.shift();
  insist(['--grant-file', '--grant-sha256', '--source-commit', '--original-task-file'].includes(flag) && argv.length && !options[flag], 'Unexpected, duplicate or missing argument');
  options[flag] = argv.shift();
}
insist(keys(options).length === 4, 'All four pinned coordination arguments are required');
const grantFile = options['--grant-file'];
insist(/^[a-f0-9]{64}$/.test(options['--grant-sha256']) && sha(grantFile) === options['--grant-sha256'], 'Root grant bytes differ');
const grant = read(grantFile);
insist(grant.schema_version === 1 && grant.kind === 'one-free-nine-locale-caption-unit' && grant.slug === SLUG
  && grant.authorized_by === '/root' && grant.helper_sha256 === sha(SELF)
  && grant.all_network_and_paid_forbidden === true && same(grant.locales, LOCALES)
  && /^[a-f0-9]{64}$/.test(grant.original_task_guard_sha256 ?? '')
  && sha(options['--original-task-file']) === grant.original_task_guard_sha256, 'This exact caption-only helper lacks its concrete root grant');

const networkAttempts = [];
const originalFetch = globalThis.fetch;
globalThis.fetch = async (input, init = {}) => {
  let origin = 'unparseable', pathname = 'unparseable';
  try { const url = new URL(typeof input === 'string' ? input : input.url); origin = url.origin; pathname = url.pathname; } catch { /* no raw URL, query, headers or body */ }
  networkAttempts.push({ method: init.method ?? 'GET', origin, pathname });
  throw new Error('ALL network is forbidden in this separate free caption-only unit');
};

let lease, outCreated = false, nativeStarted = false, nativeExit = null;
let beforeRuntimeSaved, beforeSourceSaved, originalProtectedSaved, otherInputsBeforeSaved;
let outcome = { started_at_utc: now(), helper_sha256: sha(SELF), grant_file: grantFile, grant_sha256: options['--grant-sha256'], source_commit: options['--source-commit'], native_exit: null, ok: false, network_attempts: networkAttempts };
try {
  const [{ main, EXIT }, { acquireProjectLease }, stateMod, stages, branding, caption, timelineMod, qaMod, approvals, paths, schema] = await Promise.all([
    import(path.join(ROOT, 'tools/video/cli.mjs')),
    import(path.join(ROOT, 'tools/video/core/project-lease.mjs')),
    import(path.join(ROOT, 'tools/video/core/state.mjs')),
    import(path.join(ROOT, 'tools/video/core/stages.mjs')),
    import(path.join(ROOT, 'tools/video/core/branding.mjs')),
    import(path.join(ROOT, 'tools/video/core/captions.mjs')),
    import(path.join(ROOT, 'tools/video/core/timeline.mjs')),
    import(path.join(ROOT, 'tools/video/qa/checks.mjs')),
    import(path.join(ROOT, 'tools/video/core/approvals.mjs')),
    import(path.join(ROOT, 'tools/video/core/paths.mjs')),
    import(path.join(ROOT, 'tools/video/core/schema.mjs')),
  ]);
  idleControls();
  insist(git('rev-parse', 'HEAD') === options['--source-commit'] && git('status', '--porcelain') === '', 'Pinned source commit is not clean/current');
  const originalTask = read(options['--original-task-file']);
  insist(originalTask.owner === 'codex-ai-video' && age(originalTask.latest_checkpoint) > 7200
    && age(originalTask.observed_at_utc) >= 0 && age(originalTask.observed_at_utc) < 600, 'Original recent-owner protection or stale task read');
  const autoBefore = nativeState();
  const chains = meaningChains();
  insist(sha(path.join(WORK, 'final.mp4')) === PRIMARY, 'Exact approved primary cut changed');
  const final = await approvals.approvalState({ gate: 'final', docDir: DOC, workdir: WORK });
  const primaryQA = read(path.join(WORK, 'review/qa.json'));
  insist(final.status === 'approved' && final.sha256 === PRIMARY && primaryQA.ok === true && primaryQA.final_sha256 === PRIMARY
    && primaryQA.items?.length === 11 && primaryQA.items.every(item => item.ok === true), 'Current genuine primary approval/matching11QA missing');
  const choice = stages.readLanguages(WORK), authorization = read(path.join(HOME, 'local-language-authorization.json'));
  const wanted = Object.fromEntries(FOREIGN.map(locale => [locale, { metadata: true, captions: true, dub: true }]));
  insist(same(choice?.locales, wanted) && authorization.source === 'user-chat-authorization' && authorization.final_sha256 === PRIMARY
    && same(authorization.locales, wanted) && authorization.local_choice_recorded_at === choice.decided_at
    && authorization.plan_sha256 === sha(path.join(DOC, 'production-plan.json')), 'Existing local exact8 authorization differs');
  insist(sha(AUDIT) === AUDIT_SHA, 'Original immutable read-only audit changed');
  const originalProtected = read(AUDIT).protected_files_observed_sha256;
  insist(keys(originalProtected).length === 14 && Object.entries(originalProtected).every(([file, digest]) => sha(file) === digest), 'An original protected file changed');
  insist(!files(WORK).some(file => file.includes('/speech-journal/')), 'A current speech journal requires its own reconciliation');
  insist(!fs.readdirSync(path.join(WORK, 'run-receipts'), { withFileTypes: true }).filter(e => e.isFile() && e.name.endsWith('.json')).some(e => !read(path.join(WORK, 'run-receipts', e.name)).adopted), 'Current unadopted model receipt exists; preserve it');

  const project = stateMod.loadProject({ slug: SLUG, root: ROOT });
  const lint = stateMod.lintProject(project);
  insist(lint.errors.length === 0, 'Actual source lint errors block captions');
  const speech = timelineMod.speechHash(project.doc, project.lexicon);
  const body = read(path.join(WORK, 'timeline.json')), checks = read(path.join(WORK, 'checks.json'));
  const applied = branding.appliedBranding(checks);
  const brandingMatches = branding.brandingCurrent(checks, branding.readBranding(WORK))
    && (!applied || applied.body_frames === body.total_frames && checks.speech_hash === body.speech_hash);
  insist(body.speech_hash === speech && applied && brandingMatches, 'Actual body/official-branding context differs');
  const presented = branding.presentationTimeline(body, applied);
  const { texts, skipped } = stages.localeTexts(project.doc, project.translations);
  insist(sameSet(stages.captionLocalesOf(choice, 'zh-TW'), LOCALES) && FOREIGN.every(locale => texts[locale] && skipped[locale]?.length === 0), 'All9 current written caption translations are required');
  const sourceIds = [...schema.eachLine(project.doc)].map(({ line }) => line.id);
  const voiceReadiness = () => {
    const currentAuto = read(path.join(WORK, 'auto.json'));
    const dubStatus = stateMod.dubsStatus(project, WORK, speech);
    return FOREIGN.map(locale => {
    const dub = stages.currentDub(project, WORK, locale, speech);
    const flagsFile = path.join(WORK, 'review', `check-flags.${locale}.json`);
    const checkFile = path.join(WORK, 'review', `check.${locale}.json`);
    const fitFile = path.join(WORK, 'dubs', locale, 'fit.json');
    const flags = fs.existsSync(flagsFile) ? read(flagsFile) : null;
    const cache = fs.existsSync(checkFile) ? read(checkFile) : null;
    const fit = fs.existsSync(fitFile) ? read(fitFile) : null;
    const keptFit = fit?.kept ?? [], keptDub = dub?.kept ?? [];
    const currentRawChecks = sourceIds.every(id => {
      const wav = path.join(WORK, 'dubs', locale, 'audio', `${id}.wav`);
      return fs.existsSync(wav) && cache?.lines?.[id]?.clip === sha(wav).slice(0, 16);
    });
    const ready = dubStatus[locale]?.status === 'current' && dub && !dub.stale && !currentAuto.languages?.[locale]?.check_stopped
      && flags?.speech_hash === speech && flags.translation_hash === dub.translation_hash && Array.isArray(flags.flags) && flags.flags.length === 0
      && Array.isArray(fit?.over) && fit.over.length === 0 && Array.isArray(keptFit) && keptFit.length === 0
      && Array.isArray(keptDub) && keptDub.length === 0 && currentRawChecks;
    return { locale, actual_checked_voice_ready: Boolean(ready), failed_flags: flags?.flags ?? null, native_rounds: currentAuto.languages?.[locale] ?? null, current_raw_checks_for_all101: currentRawChecks };
    });
  };
  const voicesBefore = voiceReadiness();
  insist(same(voicesBefore.filter(row => row.actual_checked_voice_ready).map(row => row.locale), ['ko', 'es']), 'True pre-caption checked voice count differs from saved2/8');
  const expected = {};
  for (const locale of LOCALES) {
    const dub = locale === 'zh-TW' ? null : stages.currentDub(project, WORK, locale, speech);
    const timed = dub && !dub.stale;
    const generated = stages.localeCues(presented, texts, locale, 'zh-TW', timed ? dub : null);
    const cueTimeline = timed ? dub : presented;
    const problems = caption.checkCues(generated.cues, locale);
    if (dub?.stale) problems.unshift(`the ${locale} dub track is older than the script or its translation (or how they are pronounced), or does not match the branding; these cues follow the narration, run dub again`);
    expected[locale] = { ...generated, problems, timing: timed ? 'dub' : 'narration', timeline: cueTimeline,
      voice_ready: locale === 'zh-TW' ? true : voicesBefore.find(row => row.locale === locale).actual_checked_voice_ready };
  }
  const beforeRuntime = snapshot(WORK, new Set(['LEASE']));
  const beforeSource = snapshot(DOC);
  const otherInputsBefore = Object.fromEntries(OTHER_INPUTS.map(file => [file, sha(path.join(ROOT, file))]));
  const stateBefore = read(path.join(WORK, 'state.json'));
  const originalBefore = Object.fromEntries(keys(originalProtected).map(file => [file, sha(file)]));
  beforeRuntimeSaved = beforeRuntime; beforeSourceSaved = beforeSource; originalProtectedSaved = originalBefore; otherInputsBeforeSaved = otherInputsBefore;
  idleControls();
  fs.mkdirSync(OUT); outCreated = true;
  save('before.json', { observed_at_utc: now(), runtime_files: beforeRuntime, full_movie_source_files: beforeSource, shared_lexicon_and_native_code_inputs: otherInputsBefore, original_protected: originalBefore, native_auto: autoBefore, checked_voices: voicesBefore, current_meaning_chains: chains, original_task_guard_sha256: sha(options['--original-task-file']) });
  save('ONE_USE.json', { consumed_at_utc: now(), purpose: 'Exactly one separate free native9CC call; no replay even on failure', grant_sha256: options['--grant-sha256'], helper_sha256: sha(SELF) });
  lease = acquireProjectLease(WORK, { owner: 'codex-ai-video-pdf-caption-only' });
  lease.verify(); insist(!paths.stopRequested(WORK), 'STOP arrived before caption write');
  insist(same(beforeRuntime, snapshot(WORK, new Set(['LEASE']))) && same(beforeSource, snapshot(DOC)), 'Project/source changed before the one caption call');
  insist(same(otherInputsBefore, Object.fromEntries(OTHER_INPUTS.map(file => [file, sha(path.join(ROOT, file))]))), 'Shared lexicon/native input changed before the caption call');
  const captionAt = new Date(); let nativeLog = '';
  const capture = { write: value => { nativeLog += value; return true; } };
  nativeStarted = true;
  try {
    nativeExit = await main(['captions', '--slug', SLUG], { root: ROOT, env: { ...process.env, VIDEO_WORKDIR: path.join(HOME, 'media') }, stdout: capture, stderr: capture, now: () => captionAt });
  } finally {
    fs.writeFileSync(path.join(OUT, 'native-captions.log'), nativeLog, { flag: 'wx' });
  }
  outcome.native_exit = nativeExit;
  lease.verify();
  const actualManifest = read(path.join(WORK, 'captions/manifest.json'));
  const expectedManifest = { speech_hash: speech, branding_hash: applied.hash, chapters: timelineMod.checkChapters(presented), locales: {}, skipped: {} };
  const captionRows = [];
  for (const locale of Object.keys(texts).filter(locale => LOCALES.includes(locale))) {
    const e = expected[locale];
    expectedManifest.locales[locale] = { cues: e.cues.length, problems: e.problems, timing: e.timing };
    const srt = fs.readFileSync(path.join(WORK, 'captions', `${locale}.srt`), 'utf8');
    const vtt = fs.readFileSync(path.join(WORK, 'captions', `${locale}.vtt`), 'utf8');
    const parsed = caption.parseSrt(srt);
    const plain = e.cues.map(({ start_ms, end_ms, text }) => ({ start_ms, end_ms, text }));
    const introAt = e.timeline.intro_at_frame == null ? null : timelineMod.frameToMs(e.timeline.intro_at_frame);
    const introEnd = e.timeline.intro_end_frame == null ? null : timelineMod.frameToMs(e.timeline.intro_end_frame);
    const contentEnd = timelineMod.frameToMs(e.timeline.content_end_frame ?? e.timeline.total_frames);
    const noBookendOverlap = parsed.every(cue => cue.start_ms >= 0 && cue.end_ms <= contentEnd
      && (introAt === null || introEnd === null || cue.end_ms <= introAt || cue.start_ms >= introEnd));
    captionRows.push({ locale, cues: parsed.length, timing: e.timing, associated_voice_checked: e.voice_ready,
      timing_interpretation: e.timing === 'narration' ? 'Native primary-narration timing; missing foreign dub is not accepted' : e.voice_ready ? 'Native current checked dub timeline' : 'Native current physical dub timeline; EN/JA voice remains failed/stopped',
      all101_source_line_ids_covered: e.missing.length === 0 && sameSet(new Set(e.cues.map(c => c.line)), sourceIds),
      srt_byte_exact_to_unchanged_native_cues: srt === caption.toSrt(e.cues), vtt_byte_exact_to_unchanged_native_cues: vtt === caption.toVtt(e.cues),
      srt_roundtrip_exact: same(parsed, plain), native_cue_problems: e.problems, parsed_SRT_problems_with_questionmark_line_labels: caption.checkCues(parsed, locale),
      reading_speed_warnings: e.problems.filter(p => /characters a second/.test(p)), hard_cue_problems: e.problems.filter(p => !/characters a second/.test(p)),
      no_intro_or_outro_overlap: noBookendOverlap, intro_start_ms: introAt, intro_end_ms: introEnd, content_end_ms: contentEnd, presentation_frame_duration_seconds: e.timeline.total_frames / (e.timeline.fps ?? 30),
      srt_sha256: hash(srt), vtt_sha256: hash(vtt) });
  }
  const captionComponent = qaMod.captionsItem({ lintWarnings: lint.warnings, manifest: actualManifest,
    current: actualManifest.speech_hash === speech && brandingMatches && (actualManifest.branding_hash ?? null) === applied.hash,
    locales: LOCALES, hasCaptionFile: locale => fs.existsSync(path.join(WORK, 'captions', `${locale}.srt`)), skippedDubs: {}, untranslated: [] });
  const afterRuntime = snapshot(WORK, new Set(['LEASE']));
  const afterSource = snapshot(DOC);
  const stateAfter = read(path.join(WORK, 'state.json'));
  const afterNonRuns = { ...stateAfter }; delete afterNonRuns.runs;
  const beforeNonRuns = { ...stateBefore }; delete beforeNonRuns.runs;
  const appended = stateAfter.runs?.at(-1);
  const exactStateAppend = same(beforeNonRuns, afterNonRuns) && Array.isArray(stateBefore.runs) && Array.isArray(stateAfter.runs)
    && stateAfter.runs.length === stateBefore.runs.length + 1 && same(stateAfter.runs.slice(0, -1), stateBefore.runs)
    && same(keys(appended), ['at', 'locales', 'stage']) && appended.stage === 'captions' && appended.at === captionAt.toISOString()
    && same(appended.locales, Object.keys(actualManifest.locales));
  const changes = changed(beforeRuntime, afterRuntime);
  const originalAfter = Object.fromEntries(keys(originalProtected).map(file => [file, sha(file)]));
  const voicesAfter = voiceReadiness();
  const guards = { native_returned_zero: nativeExit === EXIT.ok, network_attempts_zero: networkAttempts.length === 0,
    canonical_change_allowlist_only: changes.every(file => ALLOWED.has(file)), state_only_one_exact_caption_run_append: exactStateAppend,
    all_other_canonical_files_byte_exact: keys(beforeRuntime).filter(file => !ALLOWED.has(file)).every(file => beforeRuntime[file] === afterRuntime[file])
      && keys(afterRuntime).filter(file => !ALLOWED.has(file)).every(file => beforeRuntime[file] === afterRuntime[file]),
    full_movie_source_byte_exact: same(beforeSource, afterSource), original_protected14_byte_exact: same(originalBefore, originalAfter),
    shared_lexicon_and_native_code_byte_exact: same(otherInputsBefore, Object.fromEntries(OTHER_INPUTS.map(file => [file, sha(path.join(ROOT, file))]))),
    native_auto_defer_flags_caps_byte_exact: sha(path.join(WORK, 'auto.json')) === beforeRuntime['auto.json'] && same(nativeState(), autoBefore),
    native_manifest_exact_to_actual_current_context: same(actualManifest, expectedManifest), all9_locale_files_present: sameSet(keys(actualManifest.locales), LOCALES) && keys(actualManifest.skipped).length === 0,
    all_caption_bytes_line_coverage_and_bookend_bounds_pass: captionRows.length === 9 && captionRows.every(r => r.all101_source_line_ids_covered && r.srt_byte_exact_to_unchanged_native_cues && r.vtt_byte_exact_to_unchanged_native_cues && r.srt_roundtrip_exact && r.no_intro_or_outro_overlap),
    genuine_caption_component_passed: captionComponent.ok === true, checked_voice_rows_unchanged: same(voicesBefore, voicesAfter),
    actual_checked_voice_count_still_two: same(voicesAfter.filter(row => row.actual_checked_voice_ready).map(row => row.locale), ['ko', 'es']),
    git_still_clean_at_pinned_commit: git('rev-parse', 'HEAD') === options['--source-commit'] && git('status', '--porcelain') === '' };
  save('after.json', { observed_at_utc: now(), runtime_files: afterRuntime, full_movie_source_files: afterSource, original_protected: originalAfter, actual_manifest: actualManifest, caption_component: captionComponent, caption_rows: captionRows, checked_voice_rows: voicesAfter });
  outcome = { ...outcome, ended_at_utc: now(), native_exit: nativeExit, actual_native_call_count: 1, changed_canonical_paths: changes, checks: guards, ok: Object.values(guards).every(Boolean),
    caption_component: captionComponent, caption_rows: captionRows, actual_checked_foreign_voices: voicesAfter.filter(row => row.actual_checked_voice_ready).map(row => row.locale), native_state_preserved: { defer_count: 3, deferred_until: autoBefore.deferred_until, PT: autoBefore.languages.pt, EN: autoBefore.languages.en, JA: autoBefore.languages.ja },
    no_new_voice_or_full_film_QA_or_package_claim: true, no_owner_or_publication_actions: true, native_log_sha256: sha(path.join(OUT, 'native-captions.log')), no_rollback_or_automatic_retry: true };
} catch (error) {
  outcome = { ...outcome, ended_at_utc: now(), ok: false, native_exit: nativeExit, native_call_started: nativeStarted, error: error.message, actual_partial_outputs_preserved: true, no_rollback_or_automatic_retry: true };
} finally {
  try { lease?.release(); }
  catch (error) { outcome.ok = false; outcome.lease_release_error = error.message; }
  outcome.LEASE_STOP_absent_after_release = !fs.existsSync(path.join(WORK, 'LEASE')) && !fs.existsSync(path.join(WORK, 'STOP'));
  outcome.network_attempts = networkAttempts;
  if (!outcome.LEASE_STOP_absent_after_release || networkAttempts.length) outcome.ok = false;
  if (outCreated) {
    try {
      const finalRuntime = snapshot(WORK, new Set(['LEASE'])), finalSource = snapshot(DOC);
      const finalOriginal = Object.fromEntries(keys(originalProtectedSaved).map(file => [file, sha(file)]));
      const finalInputs = Object.fromEntries(OTHER_INPUTS.map(file => [file, sha(path.join(ROOT, file))]));
      const finalChanges = changed(beforeRuntimeSaved, finalRuntime);
      const finalProtection = { canonical_change_allowlist_only: finalChanges.every(file => ALLOWED.has(file)), full_movie_source_byte_exact: same(beforeSourceSaved, finalSource), original_protected14_byte_exact: same(originalProtectedSaved, finalOriginal), shared_lexicon_and_native_code_byte_exact: same(otherInputsBeforeSaved, finalInputs), auto_byte_exact: finalRuntime['auto.json'] === beforeRuntimeSaved['auto.json'] };
      save('after-final-audit.json', { observed_at_utc: now(), runtime_files: finalRuntime, full_movie_source_files: finalSource, original_protected: finalOriginal, shared_lexicon_and_native_code_inputs: finalInputs, changed_canonical_paths: finalChanges, final_protection: finalProtection });
      outcome.final_protection = finalProtection;
      if (!Object.values(finalProtection).every(Boolean)) outcome.ok = false;
    } catch (error) { outcome.ok = false; outcome.final_protection_audit_error = error.message; }
    save('actual-outcome.json', outcome);
  }
  else fs.writeFileSync(path.join(PREP, `refusal-${new Date().toISOString().replace(/[:.]/g, '-')}.json`), JSON.stringify(outcome, null, 2) + '\n', { flag: 'wx' });
  globalThis.fetch = originalFetch;
}
console.log(JSON.stringify({ outcome_file: outCreated ? path.join(OUT, 'actual-outcome.json') : null, native_exit: nativeExit, ok: outcome.ok, caption_component: outcome.caption_component, original_global_defer_byte_exact: outcome.final_protection?.auto_byte_exact ?? null, no_voice_acceptance_inferred: true }, null, 2));
process.exitCode = outcome.ok ? 0 : 1;
