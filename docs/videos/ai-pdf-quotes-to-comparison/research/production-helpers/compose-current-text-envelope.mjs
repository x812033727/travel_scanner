// Pure native metadata composition plus exact caption copies. No canonical writes or network.
import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual as same } from 'node:util';

const ROOT = '/workspace/travel_scanner_pdf';
const HOME = '/workspace/work/ai-pdf-01';
const SLUG = 'ai-pdf-quotes-to-comparison';
const WORK = path.join(HOME, 'media', SLUG);
const DOC = path.join(ROOT, 'docs/videos', SLUG);
const PREP = path.join(HOME, 'free-caption-preparation-20261026T2144Z');
const EXEC = path.join(PREP, 'one-use-execution');
const OUT = path.join(HOME, 'language-text-delivery-20261026T2154Z');
const LOCALES = ['zh-TW', 'en', 'ja', 'ko', 'es', 'pt', 'id', 'vi', 'th'];
const PRIMARY = '346a5bbd4b47884f301a9dfc9b67fe81e1a504232a0f4746e60ddead54d94e3f';
const hash = bytes => createHash('sha256').update(bytes).digest('hex');
const sha = file => hash(fs.readFileSync(file));
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const insist = (value, message) => { if (!value) throw new Error(message); };
const files = dir => fs.readdirSync(dir, { withFileTypes: true }).flatMap(e => e.isDirectory() ? files(path.join(dir, e.name)) : e.isFile() ? [path.join(dir, e.name)] : []);
const snapshot = dir => Object.fromEntries(files(dir).sort().map(f => [path.relative(dir, f), sha(f)]));
const save = (file, value) => fs.writeFileSync(file, JSON.stringify(value, null, 2) + '\n', { flag: 'wx' });
insist(process.argv.length === 3 && process.argv[2] === '--execute', 'Read the exact helper before its one external text-only execution.');
const networkAttempts = [];
const fetchBefore = globalThis.fetch;
globalThis.fetch = async () => { networkAttempts.push('forbidden network attempt'); throw new Error('No network in text-only composition.'); };
let created = false, result = { ok: false, started_at_utc: new Date().toISOString() };
try {
  const [state, stages, branding, metadata, timeline] = await Promise.all([
    import(path.join(ROOT, 'tools/video/core/state.mjs')),
    import(path.join(ROOT, 'tools/video/core/stages.mjs')),
    import(path.join(ROOT, 'tools/video/core/branding.mjs')),
    import(path.join(ROOT, 'tools/video/package/metadata.mjs')),
    import(path.join(ROOT, 'tools/video/core/timeline.mjs')),
  ]);
  insist(!fs.existsSync(path.join(WORK, 'LEASE')) && !fs.existsSync(path.join(WORK, 'STOP')), 'Another native holder or STOP exists.');
  const beforeRuntime = snapshot(WORK), beforeSource = snapshot(DOC);
  const captionResult = read(path.join(EXEC, 'actual-outcome.json'));
  const frozen = read(path.join(EXEC, 'after-final-audit.json'));
  insist(captionResult.ok && captionResult.caption_component.ok && same(beforeRuntime, frozen.runtime_files) && same(beforeSource, frozen.full_movie_source_files), 'Actual checked caption outputs/protected runtime/source have changed.');
  insist(same(captionResult.actual_checked_foreign_voices, ['ko', 'es']), 'Existing actual voice readiness differs.');
  insist(sha(path.join(WORK, 'final.mp4')) === PRIMARY, 'Approved primary bytes changed.');
  const project = state.loadProject({ slug: SLUG, root: ROOT });
  const lint = state.lintProject(project);
  insist(lint.errors.length === 0, 'Current source has lint errors.');
  const body = read(path.join(WORK, 'timeline.json')), checks = read(path.join(WORK, 'checks.json'));
  const applied = branding.appliedBranding(checks);
  insist(applied && branding.brandingCurrent(checks, branding.readBranding(WORK)) && body.speech_hash === timeline.speechHash(project.doc, project.lexicon) && applied.body_frames === body.total_frames, 'Actual presentation bindings differ.');
  const presented = branding.presentationTimeline(body, applied);
  const choice = stages.readLanguages(WORK);
  const wanted = stages.metadataLocalesOf(choice, 'zh-TW');
  insist(same([...wanted].sort(), [...LOCALES].sort()), 'Exact9 metadata choice differs.');
  const composed = metadata.composeMetadata({ doc: project.doc, timeline: presented, translations: project.translations, pack: project.pack ?? null, locales: wanted });
  insist(composed.problems.length === 0 && same(Object.keys(composed.metadata.localizations).sort(), LOCALES.filter(l => l !== 'zh-TW').sort()), 'Native metadata fields/budgets/locales failed.');
  const chapterProblems = timeline.checkChapters(presented);
  insist(chapterProblems.length === 0, 'Actual chapter timing failed.');
  fs.mkdirSync(OUT); created = true;
  fs.mkdirSync(path.join(OUT, 'captions'));
  save(path.join(OUT, 'metadata.native.json'), composed.metadata);
  const rows = [];
  for (const locale of LOCALES) {
    const fields = locale === 'zh-TW' ? composed.metadata : composed.metadata.localizations[locale];
    const description = path.join(OUT, `description.${locale}.txt`);
    fs.writeFileSync(description, fields.description, { flag: 'wx' });
    for (const kind of ['srt', 'vtt']) fs.copyFileSync(path.join(WORK, 'captions', `${locale}.${kind}`), path.join(OUT, 'captions', `${locale}.${kind}`), fs.constants.COPYFILE_EXCL);
    rows.push({ locale, title: fields.title, description_file: path.basename(description), description_utf8_bytes: Buffer.byteLength(fields.description), description_sha256: sha(description), caption_cues: captionResult.caption_rows.find(r => r.locale === locale).cues, caption_reading_speed_warnings: captionResult.caption_rows.find(r => r.locale === locale).reading_speed_warnings, associated_voice_checked: locale === 'zh-TW' || captionResult.actual_checked_foreign_voices.includes(locale) });
  }
  const contentFiles = Object.fromEntries(files(OUT).sort().map(f => [path.relative(OUT, f), { bytes: fs.statSync(f).size, sha256: sha(f) }]));
  insist(Object.keys(contentFiles).length === 28, 'Text delivery must contain native metadata,9 descriptions and18 caption files.');
  const runtimeExact = same(beforeRuntime, snapshot(WORK)), sourceExact = same(beforeSource, snapshot(DOC));
  insist(runtimeExact && sourceExact && networkAttempts.length === 0, 'Canonical/source/network protection failed.');
  result = { ...result, ok: true, ended_at_utc: new Date().toISOString(), kind: 'text-only-nine-locale-delivery-not-a-full-upload-package-or-publication', slug: SLUG, primary_final_sha256: PRIMARY, native_metadata_problems: composed.problems, actual_chapter_problems: chapterProblems, actual_chapter_count: composed.metadata.chapters.length, presented_frames: presented.total_frames, presentation_frame_duration_seconds: presented.total_frames / 30, rows, content_files: contentFiles, native_lint_warnings_retained: lint.warnings, caption_component_warning_count: captionResult.caption_component.warnings.length, caption_outcome_file: path.join(EXEC, 'actual-outcome.json'), caption_outcome_sha256: sha(path.join(EXEC, 'actual-outcome.json')), input_hashes: { video: sha(path.join(DOC, 'video.json')), body_timeline: sha(path.join(WORK, 'timeline.json')), branding_checks: sha(path.join(WORK, 'checks.json')), captions_manifest: sha(path.join(WORK, 'captions/manifest.json')), metadata_native_module: sha(path.join(ROOT, 'tools/video/package/metadata.mjs')) }, all_canonical_runtime_byte_exact: runtimeExact, whole_movie_source_byte_exact: sourceExact, network_attempts: networkAttempts, actual_checked_foreign_voices: captionResult.actual_checked_foreign_voices, primary_upload_package_untouched: true, native_paid_backoff_and_failures_untouched: true, private_metadata_value_is_template_only_not_a_site_or_YouTube_action: true, owner_or_publication_actions: false, full_eight_package_claimed: false, helper_sha256: sha(process.argv[1]) };
} catch (error) {
  result = { ...result, ended_at_utc: new Date().toISOString(), ok: false, error: error.message, partial_external_files_preserved: true, canonical_writes_performed_by_this_helper: false, network_attempts: networkAttempts };
} finally {
  globalThis.fetch = fetchBefore;
  if (created) save(path.join(OUT, 'text-delivery-manifest.json'), result);
  else save(path.join(PREP, `text-delivery-refusal-${new Date().toISOString().replace(/[:.]/g, '-')}.json`), result);
}
console.log(JSON.stringify({ output: created ? OUT : null, ok: result.ok, content_files: Object.keys(result.content_files ?? {}).length, chapter_count: result.actual_chapter_count, caption_warning_count: result.caption_component_warning_count, actual_checked_foreign_voices: result.actual_checked_foreign_voices, canonical_runtime_byte_exact: result.all_canonical_runtime_byte_exact, error: result.error ?? null }));
process.exitCode = result.ok ? 0 : 1;
