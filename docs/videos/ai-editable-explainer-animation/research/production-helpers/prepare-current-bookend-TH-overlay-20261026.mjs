// PREPARATION ONLY. ROOT MUST REVIEW THIS EXACT FILE BEFORE --execute.
// Produces a separate FAILED / NOT FOR UPLOAD Thai presentation overlay and text.
// No paid work, ASR, quality approval, renewal, package, upload or publication exists here.
import fs from 'node:fs';
import path from 'node:path';
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';
import { syncBuiltinESMExports } from 'node:module';
import http from 'node:http';
import https from 'node:https';
import net from 'node:net';
import tls from 'node:tls';
import dgram from 'node:dgram';
import dns from 'node:dns';

const ROOT = '/workspace/travel_scanner';
const HOME = '/workspace/work/ai-animation-01';
const SLUG = 'ai-editable-explainer-animation';
const ORIGINAL = path.join(HOME, 'media', SLUG);
const OLD = path.join(HOME, 'bookends-candidate-20261026', 'media', SLUG);
const STAGED = path.join(HOME, 'bookends-candidate-20261026', 'staged-renewal');
const SCRATCH = path.join(HOME, 'current-bookend-TH-overlay-20261026');
const DOC = path.join(ROOT, 'docs/videos', SLUG);
const LOCALES = ['en', 'ja', 'ko', 'es', 'pt', 'id', 'vi', 'th'];
const FLAGS = ['719e7c', '8eb4eb', 'ee8b7c', '28a3eb', 'c38a5e'];
const BODY_FRAMES = 17687, INTRO_AT = 934, INTRO_FRAMES = 150, OUTRO_FRAMES = 630;
const PRESENTED_FRAMES = BODY_FRAMES + INTRO_FRAMES + OUTRO_FRAMES;
const EXPECTED_SOURCE = 'e58ef664f7c6a27333e943fbafdbd5275cde396b53ced4009c8502ab48c8b806';
const EXPECTED_FINAL = 'ead26bf5740e1a47499a7bf406c5820bd4b84fd31495d367c1dd83f551a5b521';
const EXPECTED_OLD_FINAL = '77b542c9c1cb0e75680581d73d926db5f253e6dc5066bcbed26c0a54a061d076';
const EXPECTED_BRANDING = '39d34ab0d563aff4143d88518e178fe57e769747772084c7e9b05f42f6aeda64';
const EXPECTED_STAGE = '2fcf936f6141ace9a38311a8efbf4b4885037e515975a4d04bad03497e85a83a';
const UNKNOWN = 'audio/speech-journal/0bff2c18b57e5a34d3ee05af4dee4aea1d5b7b1cd937b54c39c013bbaa16fad9.json';
const TRANSLATION = {
  en: 'e6f09548e017a669aa6c7d8aa3c1705a318ad4384039ff03c38b5f2f4573ab57',
  ja: '50e547580f142c405a667b426e92a2c7b91fe4b3c9ce7c7487e4444e5144aabd',
  ko: '02cb830a188a3bbcfb6f8f8bd6aaee3d7f6ca81e8bb9995bb29c73ba457ee6dd',
  es: 'c14d83d73d72eda075fb16462548c2f07c564f7ce7a13d410ad92683814a2dca',
  pt: 'a64b95fa97a2d2bf76e7c27cd38d089e0144a2a6561f9a1fa0f93a4971c68857',
  id: '261b3cccc47b5f5d93cf7e5aa53f21b1dc7f73038f72395ef224ddf23ab65801',
  vi: 'b4529d2379c5c5498907cb3c343fce337c030fb8c83da27d295cb464a536d9db',
  th: '088dd503ef0147735a68d757bcd8c8be98b3c283e0c8d084183a4b09658e9b93',
};
const CRITICAL = {
  'auto.json': 'b4bb92c6dde27be074f4b5fa8cc9e6ad9b502e7ba912d6a65172cce05a7f3b4b',
  'approvals.json': '8fefeaec595d5ba964eb6c0712ce9b9c27d8db4f6d4524492027d3b8e3e21106',
  'checks.json': '47d29b73329991495bc2f7d6b90f6c1b1c43314f45a992606f67915a116b9637',
  'languages.json': 'd0a0ee8e8b5f9198e7fd4a633a3d804ab8e98f0ea8ece966e2d637e116e305c9',
  'dubs/th.m4a': '6070a20aa941268f31e093547fc25e01f0bb275dff1097bd818b8e51b96bcc1f',
  'dubs/th/fit.json': 'ca0310851f73dc3e16494e6c7897a8b99683ce157a7e7bd463a24e38c0947670',
  'dubs/th/timeline.json': '0cee1709894b5a215d571a5e908a9624ad303d262ff65912b40e5272cf5a47e2',
  'review/check.th.json': 'd4236f8d85ea5f8bdae8e6e29ccdbc59d2d09f9efde71acea614a891c654efcd',
  'review/check-flags.th.json': 'b65c7705b36c77590a77d749231e1ae6e4ab7321f1bbb9b6de6f41a827a5725a',
  [UNKNOWN]: '2d5203fc96618af71cc8cb557b4c831556bc7b07af09be27a490c2840394c5bf',
  'dubs/ko/skipped.json': 'f773249e7a2a4bc67fb2a99d351792d1ddc8ab55634fd329a195fa503d1d32dc',
  'dubs/pt/skipped.json': '51ced345c88dd85467c38d5db541e5632f77761fdfe954438fa1d13370e269ca',
  'dubs/id/skipped.json': 'e1ca99cd6f25b8fc74ad066634ca59ff1280adbad97f081dd8cfb247b2c1283c',
  'captions/th.srt': '567cb017adbd31deb4686d3a931ed5bea4106e3379b36df46ac09c49f04d84c3',
  'captions/th.vtt': '854af97bf91297db564444c98c8d98d61f013e05b6e22a44878f02a6b3b90f67',
};
const sha = bytes => createHash('sha256').update(bytes).digest('hex');
const digest = file => sha(fs.readFileSync(file));
const read = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const json = value => `${JSON.stringify(value, null, 2)}\n`;
const ensure = (value, message) => { if (!value) throw new Error(message); };
const self = path.resolve(process.argv[1]);
if (process.argv.length !== 3 || process.argv[2] !== '--execute') {
  console.log(`PREPARATION ONLY; root must review the exact script hash before --execute.\nOutput: ${SCRATCH}\nFAILED / NOT FOR UPLOAD Thai timing overlay only. No network, TTS, ASR, approval, renewal or package.`);
  process.exit(process.argv.length === 2 || process.argv[2] === '--help' ? 0 : 2);
}

// Fail closed for all Node network paths before loading the native media modules.
// The exec wrapper below additionally accepts only local approved media inputs.
const networkAttempts = [];
const denyNetwork = (...args) => {
  networkAttempts.push({ at_utc: new Date().toISOString(), argument_type: typeof args[0] });
  throw new Error('This offline preparation forbids ALL network and provider calls.');
};
globalThis.fetch = denyNetwork;
for (const obj of [http, https]) { obj.request = denyNetwork; obj.get = denyNetwork; }
net.connect = denyNetwork; net.createConnection = denyNetwork; net.Socket.prototype.connect = denyNetwork;
tls.connect = denyNetwork; dgram.createSocket = denyNetwork;
for (const name of ['lookup', 'resolve', 'resolve4', 'resolve6', 'reverse']) dns[name] = denyNetwork;
syncBuiltinESMExports();

const { wrapAudio } = await import(`${ROOT}/tools/video/assemble/branding.mjs`);
const { locateFfmpeg, runTool } = await import(`${ROOT}/tools/video/assemble/ffmpeg.mjs`);
const { appliedBranding, brandingCurrent, introAtFrame, linesAcrossIntro, presentationTimeline, readBranding, shiftBrandingCues } = await import(`${ROOT}/tools/video/core/branding.mjs`);
const { checkCues, parseSrt, toSrt, toVtt } = await import(`${ROOT}/tools/video/core/captions.mjs`);
const { stopRequested } = await import(`${ROOT}/tools/video/core/paths.mjs`);
const { acquireProjectLease, leaseHolder } = await import(`${ROOT}/tools/video/core/project-lease.mjs`);
const { eachLine, narrationLocale, spokenText } = await import(`${ROOT}/tools/video/core/schema.mjs`);
const { currentDub, localeCues, localeTexts } = await import(`${ROOT}/tools/video/core/stages.mjs`);
const { dubArtifacts, lintProject, loadProject } = await import(`${ROOT}/tools/video/core/state.mjs`);
const { speechHash } = await import(`${ROOT}/tools/video/core/timeline.mjs`);
const { assertNoServiceRetakeHold } = await import(`${ROOT}/tools/video/automation/service-retake.mjs`);
const { CODECS } = await import(`${ROOT}/tools/video/dubs/encode.mjs`);
const { dubRequests, speechFingerprint, translationHash } = await import(`${ROOT}/tools/video/dubs/plan.mjs`);
const { composeMetadata } = await import(`${ROOT}/tools/video/package/metadata.mjs`);

function assertDirectory(dir) {
  const st = fs.lstatSync(dir);
  ensure(st.isDirectory() && !st.isSymbolicLink() && fs.realpathSync(dir) === dir, `Unsafe directory: ${dir}`);
}
function snapshot(dir, ignoreLiveLease = false) {
  assertDirectory(dir);
  const out = {};
  const visit = (at, prefix = '') => {
    for (const name of fs.readdirSync(at).sort()) {
      const rel = prefix ? `${prefix}/${name}` : name;
      if (ignoreLiveLease && rel === 'LEASE') continue;
      const f = path.join(at, name), st = fs.lstatSync(f);
      ensure(!st.isSymbolicLink(), `Symlink in protected tree: ${f}`);
      if (st.isDirectory()) visit(f, rel);
      else { ensure(st.isFile(), `Nonregular protected file: ${f}`); out[rel] = { sha256: digest(f), size: st.size }; }
    }
  };
  visit(dir); return out;
}
function verifyPins() {
  ensure(digest(path.join(DOC, 'video.json')) === EXPECTED_SOURCE, 'Current primary source changed.');
  for (const locale of LOCALES) ensure(digest(path.join(DOC, 'i18n', `${locale}.json`)) === TRANSLATION[locale], `${locale} source changed.`);
  for (const [rel, h] of Object.entries(CRITICAL)) ensure(digest(path.join(ORIGINAL, rel)) === h, `Current canonical evidence changed: ${rel}`);
  ensure(digest(path.join(ORIGINAL, 'final.mp4')) === EXPECTED_FINAL, 'Canonical final changed.');
  ensure(digest(path.join(OLD, 'final.mp4')) === EXPECTED_OLD_FINAL, 'Old candidate final changed.');
  ensure(digest(path.join(STAGED, 'renewal-candidate.json')) === EXPECTED_STAGE, 'Old staged renewal receipt changed.');
  for (const [dir, expected] of [[ORIGINAL, EXPECTED_FINAL], [OLD, EXPECTED_OLD_FINAL]]) {
    const q = read(path.join(dir, 'review/qa.json'));
    ensure(q.ok === true && q.final_sha256 === expected && q.items?.length === 11 && q.items.every(i => i.ok === true), 'Current exact primary QA proof differs.');
  }
}
function assertNoStops() {
  for (const dir of [HOME, path.dirname(ORIGINAL), ORIGINAL, OLD, STAGED, SCRATCH]) ensure(!stopRequested(dir), `STOP holds ${dir}`);
}
assertDirectory(HOME); assertDirectory(ORIGINAL); assertDirectory(OLD); assertDirectory(STAGED); assertDirectory(DOC);
ensure(!fs.existsSync(SCRATCH), 'One-use scratch already exists; inspect it, NEVER overwrite or rerun.');
ensure(leaseHolder(ORIGINAL) === null && leaseHolder(OLD) === null && leaseHolder(STAGED) === null, 'A project holder exists; do not take over.');
assertNoStops(); verifyPins();

let originalLease = null, scratchLease = null, before = null, created = false;
const startedAt = new Date().toISOString();
const forbiddenClaims = { voice_ready: false, quality_approval_created: false, complete_language_package: false,
  final_renewal_submitted: false, canonical_adoption_performed: false, uploaded: false, published: false,
  new_synthesis_requests: 0, new_ASR_requests: 0, provider_calls: 0 };
try {
  originalLease = acquireProjectLease(ORIGINAL, { owner: 'current-bookend-TH-overlay-offline' });
  originalLease.verify(); assertNoStops(); assertNoServiceRetakeHold(ORIGINAL, { lease: originalLease }); verifyPins();
  const sourceExtraFiles = [path.join(ROOT, 'docs/videos/lexicon.json'), self];
  before = {
    canonical: snapshot(ORIGINAL, true), old_candidate: snapshot(OLD, true), staged_renewal: snapshot(STAGED, true),
    film_source: snapshot(DOC), native_implementation: snapshot(path.join(ROOT, 'tools/video')),
    extra_sources: Object.fromEntries(sourceExtraFiles.map(f => [f, { sha256: digest(f), size: fs.statSync(f).size }])),
  };
  const project = loadProject({ slug: SLUG, root: ROOT }), lint = lintProject(project);
  ensure(lint.errors.length === 0, 'Actual current source has lint errors.');
  ensure(!project.doc.source_guide && !project.pack, 'Unexpected content pack dependency; review its source first.');
  const body = read(path.join(ORIGINAL, 'timeline.json')), auto = read(path.join(ORIGINAL, 'auto.json'));
  ensure(auto.status === 'done' && !auto.youtube_video_id && !project.doc.youtube?.video_id, 'Canonical is not the expected unpublished completed primary.');
  assert.deepEqual(auto.languages?.th, { shorten: 1, retakes: 2, reword: 2, check_stopped: true });
  ensure(read(path.join(ORIGINAL, UNKNOWN)).status === 'sent', 'English unknown billing hold changed.');
  for (const locale of ['ko', 'pt', 'id']) ensure(typeof read(path.join(ORIGINAL, `dubs/${locale}/skipped.json`)).reason === 'string', 'Native skip missing.');
  ensure(body.total_frames === BODY_FRAMES && body.fps === 30 && body.chapters?.[1]?.start_frame === INTRO_AT
    && body.speech_hash === speechHash(project.doc, project.lexicon), 'Body timing or primary speech differs.');
  const selected = readBranding(OLD), oldChecks = read(path.join(OLD, 'checks.json')), applied = appliedBranding(oldChecks);
  ensure(selected.hash === EXPECTED_BRANDING && selected.intro.frames === INTRO_FRAMES && selected.outro.frames === OUTRO_FRAMES
    && selected.intro_at === 'after_first_chapter' && brandingCurrent(oldChecks, selected), 'Official selected branding differs.');
  ensure(applied.hash === EXPECTED_BRANDING && introAtFrame(applied) === INTRO_AT && applied.body_frames === BODY_FRAMES,
    'Old candidate presentation does not match this body.');
  for (const role of ['intro', 'outro']) {
    ensure(path.isAbsolute(selected[role].file) && fs.realpathSync(selected[role].file) === selected[role].file, 'Branding path is not a local regular file.');
    ensure(digest(selected[role].file) === selected[role].sha256, 'Branding asset bytes changed.');
    before.extra_sources[selected[role].file] = { sha256: digest(selected[role].file), size: fs.statSync(selected[role].file).size };
  }
  const files = dubArtifacts(ORIGINAL, 'th'), planned = dubRequests(project, 'th');
  const th = currentDub(project, ORIGINAL, 'th', body.speech_hash);
  ensure(th && !th.stale && th.file === files.track('m4a') && !th.branding_hash && th.total_frames === BODY_FRAMES,
    'Native currentDub must accept the exact existing Thai body track.');
  const fit = read(files.fit), cache = read(files.cache), check = read(path.join(ORIGINAL, 'review/check.th.json'));
  const flags = read(path.join(ORIGINAL, 'review/check-flags.th.json'));
  const sourceIds = [...eachLine(project.doc)].map(({ line }) => line.id).sort();
  ensure(sourceIds.length === 101 && isDeepStrictEqual(th.lines.map(l => l.id).sort(), sourceIds), 'Expected101 exact current Thai timeline lines.');
  assert.deepEqual(flags.flags, FLAGS);
  ensure(flags.translation_hash === th.translation_hash && flags.speech_hash === body.speech_hash, 'Failed voice flags are not current.');
  ensure(planned.missing.length === 0 && th.translation_hash === translationHash(planned.script)
    && th.speech_fingerprint === speechFingerprint(planned.requests) && fit.translation_hash === th.translation_hash
    && fit.speech_hash === body.speech_hash && fit.speech_fingerprint === th.speech_fingerprint
    && Array.isArray(fit.over) && fit.over.length === 0 && !(th.kept?.length) && !(fit.kept?.length)
    && linesAcrossIntro(th.lines, INTRO_AT).length === 0, 'Thai track needs synthesis/fit/kept-line changes or crosses the intro.');
  ensure(planned.requests.every(r => r.lines.every(l => [l.key, r.key].includes(cache.lines?.[l.id]) && fs.existsSync(path.join(files.audio, `${l.id}.wav`)))), 'At least one native Thai request is not cached.');
  const thaiLines = new Map([...eachLine(planned.script)].map(({ line }) => [line.id, line]));
  ensure(isDeepStrictEqual(Object.keys(check.lines ?? {}).sort(), sourceIds), 'Not all101 current original raw checks exist.');
  const rawHashes = {};
  for (const id of sourceIds) {
    const raw = path.join(files.audio, `${id}.wav`), h = digest(raw), r = check.lines[id]; rawHashes[id] = h;
    ensure(r.clip === h.slice(0, 16) && r.intended === spokenText(thaiLines.get(id)) && typeof r.heard === 'string', `Current raw/check/intended proof differs for ${id}.`);
  }
  const { texts, skipped } = localeTexts(project.doc, project.translations);
  ensure(Object.values(skipped).every(ids => ids.length === 0) && LOCALES.every(l => Object.keys(texts[l] ?? {}).length === 101), 'Any locale text is stale or missing.');
  const canonicalCues = localeCues(body, texts, 'th', narrationLocale(project.doc), th).cues;
  ensure(canonicalCues.length === 104 && toSrt(canonicalCues) === fs.readFileSync(path.join(ORIGINAL, 'captions/th.srt'), 'utf8')
    && toVtt(canonicalCues) === fs.readFileSync(path.join(ORIGINAL, 'captions/th.vtt'), 'utf8'), 'Native exact current Thai body captions differ.');
  const presentedPrimary = presentationTimeline(body, applied), presentedThai = presentationTimeline(th, applied);
  ensure(presentedThai.total_frames === PRESENTED_FRAMES && presentedThai.content_end_frame === BODY_FRAMES + INTRO_FRAMES
    && presentedThai.intro_at_frame === INTRO_AT && presentedThai.intro_end_frame === INTRO_AT + INTRO_FRAMES,
    'Presented Thai timeline shape differs.');
  const cues = localeCues(presentedPrimary, texts, 'th', narrationLocale(project.doc), presentedThai).cues;
  ensure(cues.length === 104 && checkCues(cues, 'th').length === 0, 'Actual native Thai caption mechanics failed.');
  ensure(toSrt(cues) === toSrt(shiftBrandingCues(parseSrt(fs.readFileSync(path.join(ORIGINAL, 'captions/th.srt'), 'utf8')), applied)), 'Native regenerated CC is not the exact native shift of the current104body cues.');
  const introStartMs = Math.round(INTRO_AT * 1000 / 30), introEndMs = Math.round((INTRO_AT + INTRO_FRAMES) * 1000 / 30);
  const contentEndMs = Math.round((BODY_FRAMES + INTRO_FRAMES) * 1000 / 30);
  ensure(cues.every(c => c.end_ms <= introStartMs || c.start_ms >= introEndMs)
    && cues.every(c => c.start_ms >= 0 && c.end_ms <= contentEndMs), 'Thai caption overlaps an official bookend.');
  const metadata = composeMetadata({ doc: project.doc, timeline: presentedPrimary, translations: project.translations, pack: project.pack, locales: LOCALES });
  ensure(metadata.problems.length === 0 && isDeepStrictEqual(Object.keys(metadata.metadata.localizations ?? {}).sort(), [...LOCALES].sort()), 'Nine-locale native metadata composition failed.');

  // mkdir without recursive plus wx admission is a permanent one-use boundary.
  originalLease.verify(); assertNoStops(); verifyPins();
  fs.mkdirSync(SCRATCH); created = true;
  scratchLease = acquireProjectLease(SCRATCH, { owner: 'FAILED-TH-overlay-only-offline' });
  const verifyHeld = () => { originalLease.verify(); scratchLease.verify(); assertNoStops(); ensure(leaseHolder(OLD) === null && leaseHolder(STAGED) === null, 'An old candidate/stage holder arrived.'); };
  const write = (relative, bytes) => { verifyHeld(); const file = path.join(SCRATCH, relative); ensure(path.relative(SCRATCH, file) && !path.relative(SCRATCH, file).startsWith('..'), 'Output escapes scratch.'); fs.mkdirSync(path.dirname(file), { recursive: true }); fs.writeFileSync(file, bytes, { flag: 'wx', mode: 0o600 }); };
  write('ONE_USE_ADMISSION.NOT_ADOPTED.json', json({ started_at_utc: startedAt, pid: process.pid, script_sha256: digest(self), scratch: SCRATCH,
    status: 'FAILED / NOT FOR UPLOAD — current-text timing preparation only', ...forbiddenClaims }));
  write('protected-before.json', json(before));
  write('README.NOT_FOR_UPLOAD.txt', 'FAILED / NOT FOR UPLOAD\nThis track contains the existing Thai speech with five unresolved native voice flags.\nIt is only a local current-text presentation-timing overlay for the unchanged bookend candidate.\nNo new voice, ASR, approval, renewal, upload or publication occurred.\nNo auto.json, approvals.json, final.mp4, package or ready-voice role is created here.\nPreserve this one-use directory even on failure; do not overwrite or replay it.\n');
  const tools = await locateFfmpeg();
  const track = path.join(SCRATCH, 'TH_FAILED_NOT_FOR_UPLOAD.presentation-only.m4a');
  const allowedInputs = new Set([files.track('m4a'), selected.intro.file, selected.outro.file]);
  const localExec = async (binary, args, options) => {
    verifyHeld();
    ensure([tools.ffmpeg, tools.ffprobe].includes(binary), 'Only native ffmpeg/ffprobe are allowed.');
    ensure(args.every(a => !/(?:https?|ftp|tcp|udp|rtmp|srt|unix):\/\//i.test(String(a))), 'Network protocol in media arguments.');
    for (let i = 0; i < args.length; i++) if (args[i] === '-i') ensure(allowedInputs.has(args[i + 1]) && fs.realpathSync(args[i + 1]) === args[i + 1], 'Unapproved media input.');
    // The native algorithm/filters stay exact. This exec boundary additionally
    // forbids protocols in the child media decoder, including nested references.
    const offlineArgs = binary === tools.ffprobe
      ? ['-protocol_whitelist', 'file,pipe', ...args]
      : args.flatMap(a => a === '-i' ? ['-protocol_whitelist', 'file,pipe', a] : [a]);
    const result = await runTool(binary, offlineArgs, options);
    verifyHeld(); return result;
  };
  const audioProbe = async (file, expectedFrames) => {
    verifyHeld();
    const p = JSON.parse((await localExec(tools.ffprobe, ['-v', 'error', '-show_entries', 'stream=codec_type,codec_name,sample_rate,channels:format=duration,size', '-of', 'json', file])).stdout);
    const a = p.streams?.find(s => s.codec_type === 'audio');
    ensure(p.streams?.length === 1 && a?.codec_name === 'aac' && a.sample_rate === '48000' && a.channels === 2
      && Math.abs(Number(p.format?.duration) - expectedFrames / 30) <= 0.1, 'Actual AAC track shape/duration failed.');
    return p;
  };
  const bodyProbe = await audioProbe(files.track('m4a'), BODY_FRAMES);
  verifyHeld(); ensure(!fs.existsSync(track), 'Output track already exists.');
  const wrapped = await wrapAudio({ tools, exec: localExec, bodyFile: files.track('m4a'), bodyFrames: BODY_FRAMES,
    branding: selected, outFile: track, outputCodec: CODECS.m4a, introAtFrame: INTRO_AT });
  ensure(wrapped.hash === applied.hash && wrapped.body_frames === BODY_FRAMES && wrapped.intro_frames === INTRO_FRAMES
    && wrapped.outro_frames === OUTRO_FRAMES && introAtFrame(wrapped) === INTRO_AT, 'Native wrapAudio returned another presentation.');
  const outputProbe = await audioProbe(track, PRESENTED_FRAMES);
  write('TH_FAILED_NOT_FOR_UPLOAD.timeline.json', json(presentedThai));
  write('captions/th.srt', toSrt(cues)); write('captions/th.vtt', toVtt(cues));
  write('metadata/nine-locales.NOT_ADOPTED.json', json({ status: 'NOT ADOPTED — metadata preparation only', candidate_final_sha256: EXPECTED_OLD_FINAL,
    branding_hash: EXPECTED_BRANDING, ...forbiddenClaims, native_composition: metadata }));
  for (const locale of ['zh-TW', ...LOCALES]) {
    const fields = locale === 'zh-TW' ? metadata.metadata : metadata.metadata.localizations[locale];
    write(`metadata/description.${locale}.NOT_ADOPTED.txt`, `${fields.title}\n\n${fields.description}\n`);
  }
  const otherCaptions = ['zh-TW', ...LOCALES.filter(l => l !== 'th')].map(locale => ({ locale, copied: false,
    source: 'Preserved old candidate caption reference only; not a new voice pass',
    srt: { path: path.join(OLD, `captions/${locale}.srt`), sha256: digest(path.join(OLD, `captions/${locale}.srt`)) },
    vtt: { path: path.join(OLD, `captions/${locale}.vtt`), sha256: digest(path.join(OLD, `captions/${locale}.vtt`)) } }));
  verifyHeld(); verifyPins();
  const after = {
    canonical: snapshot(ORIGINAL, true), old_candidate: snapshot(OLD, true), staged_renewal: snapshot(STAGED, true),
    film_source: snapshot(DOC), native_implementation: snapshot(path.join(ROOT, 'tools/video')),
    extra_sources: Object.fromEntries(Object.keys(before.extra_sources).map(f => [f, { sha256: digest(f), size: fs.statSync(f).size }])),
  };
  ensure(isDeepStrictEqual(after, before), 'Protected original/candidate/stage/source bytes changed; overlay remains held, not adoptable.');
  ensure(networkAttempts.length === 0, 'A network attempt occurred; never call this offline success.');
  write('protected-after.json', json(after));
  const artifacts = snapshot(SCRATCH, true);
  write('result.NOT_ADOPTED.json', json({ schema_version: 1, started_at_utc: startedAt, finished_at_utc: new Date().toISOString(),
    status: 'FAILED TH VOICE / NOT FOR UPLOAD — local timing preparation completed', ...forbiddenClaims,
    scratch: SCRATCH, canonical: ORIGINAL, old_candidate: OLD, staged_renewal: STAGED,
    primary_source_sha256: EXPECTED_SOURCE, current_th_translation_sha256: TRANSLATION.th,
    canonical_final_sha256: EXPECTED_FINAL, candidate_final_sha256: EXPECTED_OLD_FINAL, staged_receipt_sha256: EXPECTED_STAGE,
    preserved_native_rounds: auto.languages.th, unresolved_native_voice_flags: FLAGS,
    current_native_currentDub_nonstale: true, current101raw_WAV_hashes: rawHashes, original_body_track_sha256: digest(files.track('m4a')),
    fit_over: fit.over, kept_lines: [], thai_cues: cues.length, actual_native_caption_problems: checkCues(cues, 'th'),
    intro_body_frame: INTRO_AT, intro_frames: INTRO_FRAMES, outro_frames: OUTRO_FRAMES, body_frames: BODY_FRAMES,
    presented_frames: PRESENTED_FRAMES, no_cue_overlaps_bookends: true, caption_bytes_equal_native_shift_of_current104cues: true,
    actual_ffprobe: { body: bodyProbe, overlay: outputProbe }, preserved_other8caption_references: otherCaptions,
    source_lint: { errors: lint.errors, warnings: lint.warnings }, protected_before_after_byte_exact: true,
    protected_manifest_sha256: sha(json(before)), network_attempts: networkAttempts, artifacts_before_result: artifacts,
    next: 'Independent root review of these actual local files; preserve NOT ADOPTED / NOT FOR UPLOAD. Only supported genuine owner renewal/reconciliation/fresh retry can advance the original blocked film. Do not import this failed Thai track as a ready dub, clear any flags/caps/unknown hold, run a generic package, or overwrite the old candidate/stage.' }));
  verifyHeld();
  console.log(json({ scratch: SCRATCH, status: 'Local timing preparation completed; TH voice FAILED / NOT FOR UPLOAD',
    result_sha256: digest(path.join(SCRATCH, 'result.NOT_ADOPTED.json')), thai_cues: 104, unresolved_voice_flags: FLAGS.length,
    protected_before_after_byte_exact: true, ...forbiddenClaims }));
} catch (error) {
  // Keep the permanent one-use admission and partial outputs. Never delete or replay.
  console.error(`Overlay preparation stopped: ${error.message}. Scratch is held for inspection; no adoption is permitted.`);
  process.exitCode = 1;
} finally {
  scratchLease?.release(); originalLease?.release();
}
