// A bounded, operator-requested new take after a settled transcription refusal. This is not
// a transcript, Jev verdict, owner retry or voice approval. Integrate the exported hold guard
// into every producer before using executeServiceRetake; an ordinary --redo has no durable
// operation identity after its speech journal is released.
import {
  closeSync, existsSync, fsyncSync, lstatSync, mkdirSync, openSync, readFileSync,
  readdirSync, writeFileSync,
} from 'node:fs';
import path from 'node:path';
import { createHash, randomUUID } from 'node:crypto';
import { isDeepStrictEqual } from 'node:util';

import { approvalState } from '../core/approvals.mjs';
import { isInside, atomicWrite, resolveWorkdir, stopRequested } from '../core/paths.mjs';
import { acquireProjectLease } from '../core/project-lease.mjs';
import { loadProject, dubArtifacts } from '../core/state.mjs';
import { speechHash } from '../core/timeline.mjs';
import { dubRequests, speechFingerprint, translationHash } from '../dubs/plan.mjs';
import { lineBody } from '../tts/synthesis.mjs';
import { billableForRequest } from '../tts/requests.mjs';
import { listSpeechJournal } from '../tts/speech-journal.mjs';
import { encodeWav, parseWav, requireNarrationFormat, toNarrationRate } from '../tts/wav.mjs';
import { trimSilence } from '../tts/split.mjs';
import { siteClient } from '../shorts/site.mjs';
import { ITEM_IDS } from '../qa/checks.mjs';
import { MAX_DUB_RETAKE_ROUNDS } from './flow.mjs';

export const SERVICE_RETAKE_DIRECTORY = 'service-retakes';
export const MIN_SETTLED_FAILURES = 6;
const LOCALES = new Set(['en', 'ja', 'ko', 'es', 'pt', 'id', 'vi', 'th']);
const SHA = /^[0-9a-f]{64}$/;
const ID = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;
const bytes = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const digest = value => createHash('sha256').update(value).digest('hex');
const stamp = now => (typeof now === 'function' ? now() : now ?? new Date()).toISOString();

export class ServiceRetakeError extends Error {
  constructor(message, code = 'video_service_retake_refused') { super(message); this.code = code; }
}
function insist(ok, message) { if (!ok) throw new ServiceRetakeError(message); }
function read(file) { return JSON.parse(readFileSync(file, 'utf8')); }
function regular(file) {
  insist(existsSync(file) && lstatSync(file).isFile() && !lstatSync(file).isSymbolicLink(), `Missing or nonregular evidence: ${file}`);
  return readFileSync(file);
}
function filePin(file) { const data = regular(file); return { file, sha256: digest(data), bytes: data.length }; }
function verifyPin(pin) {
  const current = filePin(pin.file);
  insist(current.sha256 === pin.sha256 && current.bytes === pin.bytes, `Pinned evidence changed: ${pin.file}`);
}
function childFile(dir, relative) {
  insist(typeof relative === 'string' && !path.isAbsolute(relative) && !relative.includes('\\'), 'Evidence must have a relative path');
  const file = path.resolve(dir, relative);
  insist(isInside(file, dir) && file !== path.resolve(dir), 'Evidence escaped its project');
  return file;
}
function syncDirectory(dir) {
  if (process.platform === 'win32') return;
  const fd = openSync(dir, 'r'); try { fsyncSync(fd); } finally { closeSync(fd); }
}
function writeDurable(file, data) {
  atomicWrite(file, data);
  const fd = openSync(file, 'r+'); try { fsyncSync(fd); } finally { closeSync(fd); }
  syncDirectory(path.dirname(file));
}
function createDurable(file, data) {
  mkdirSync(path.dirname(file), { recursive: true });
  const fd = openSync(file, 'wx');
  try { writeFileSync(fd, data); fsyncSync(fd); } finally { closeSync(fd); }
  syncDirectory(path.dirname(file));
}

function appliedProofIntact(intent, dir) {
  try {
    const plan = intent.plan, result = intent.outcome, response = read(path.join(dir, 'http-answer.json'));
    if (plan?.intent_id !== intent.intent_id || result?.status !== 'applied' || result.voice_ready !== false
      || result.asr_performed !== false || result.installed_raw_matches_response !== true
      || ![0, 1].includes(result.native_exit_code) || !SHA.test(intent.state_reserved_sha256 ?? '')
      || !SHA.test(result.target_after_sha256 ?? '') || !isDeepStrictEqual(result.confirmed_response, response)
      || response.request_sha256 !== plan.request_sha256 || !(response.response_status >= 200 && response.response_status < 300)
      || !Number.isSafeInteger(response.response_bytes) || response.response_bytes > 8 * 1024 * 1024) return false;
    const answer = regular(path.join(dir, 'http-answer.bin'));
    if (answer.length !== response.response_bytes || digest(answer) !== response.response_sha256) return false;
    const raw = encodeWav(trimSilence(requireNarrationFormat(parseWav(toNarrationRate(answer)))));
    const requestFile = path.join(dir, 'retake-request.json');
    return digest(raw) === result.target_after_sha256 && isDeepStrictEqual(read(requestFile), [plan.lineId])
      && isDeepStrictEqual(result.command, ['dub', '--slug', plan.slug, '--locale', plan.locale, '--redo', requestFile, '--line-by-line']);
  } catch { return false; }
}

/** Read-only discovery. An unreadable intent is a hold, never an invitation to create anew. */
export function inspectServiceRetakeIntents(workdir) {
  const dir = path.join(workdir, SERVICE_RETAKE_DIRECTORY);
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter(name => SHA.test(name)).sort().map(id => {
    const file = path.join(dir, id, 'intent.json');
    try {
      const intent = read(file);
      if (intent.schema_version !== 1 || intent.intent_id !== id) throw new Error('Invalid intent');
      const phase = intent.phase === 'applied' && !appliedProofIntact(intent, path.dirname(file)) ? 'unverified-applied' : intent.phase;
      return { id, file, phase, intent };
    } catch { return { id, file, phase: 'unreadable', intent: null }; }
  });
}

function ownStop(workdir, row, lease, now) {
  if (!lease) return { written: false, reason: 'No lease: the caller is refused without writing a STOP' };
  lease.verify();
  const ownerFile = path.join(path.dirname(row.file), 'stop-owner.json');
  let owner;
  if (existsSync(ownerFile)) owner = read(ownerFile);
  else {
    const contents = bytes({ schema_version: 1, kind: 'dub-service-retake-hold', intent_id: row.id,
      owner_token: randomUUID(), reason: 'An unfinished service-retake dispatch must be reconciled before any producer continues.' });
    owner = { schema_version: 1, intent_id: row.id, created_at: stamp(now), stop_sha256: digest(contents), stop_base64: contents.toString('base64') };
    createDurable(ownerFile, bytes(owner));
  }
  const contents = Buffer.from(owner.stop_base64, 'base64');
  insist(owner.intent_id === row.id && digest(contents) === owner.stop_sha256, 'The retained STOP ownership proof is invalid');
  const stop = path.join(workdir, 'STOP');
  if (existsSync(stop)) return { written: false, owned: digest(regular(stop)) === owner.stop_sha256, stop_sha256: owner.stop_sha256 };
  lease.verify();
  try { createDurable(stop, contents); }
  catch (error) { if (error.code !== 'EEXIST') throw error; }
  return { written: true, owned: digest(regular(stop)) === owner.stop_sha256, stop_sha256: owner.stop_sha256 };
}

/**
 * REQUIRED at every producer entry while its native project lease is held. A SIGKILL can
 * prevent execute's catch from running. This permanent intent guard then creates its own
 * bound STOP; it never overwrites or removes a STOP, nor resolves an unknown paid result.
 */
export function assertNoServiceRetakeHold(workdir, { lease = null, now } = {}) {
  const held = inspectServiceRetakeIntents(workdir).find(row => row.phase !== 'applied');
  if (!held) return;
  const stop = ownStop(workdir, held, lease, now);
  const error = new ServiceRetakeError(`Service retake ${held.id} is ${held.phase}; no replay or normal producer is allowed before reconciliation.`, 'video_service_retake_held');
  error.intent_file = held.file; error.stop = stop; throw error;
}

function journalPins(workdir) {
  const dir = path.join(workdir, 'audio', 'speech-journal');
  return listSpeechJournal(dir).map(entry => ({ file: path.join(dir, `${entry.sha}.json`), status: entry.status,
    sha256: filePin(path.join(dir, `${entry.sha}.json`)).sha256 })).sort((a, b) => a.file.localeCompare(b.file));
}
function receiptJournalPins(receipt) {
  return (receipt.unresolved_speech_journals ?? []).map(row => ({ file: row.path, status: row.status, sha256: row.sha256 })).sort((a, b) => a.file.localeCompare(b.file));
}
function finalReview(remote) { return remote?.reviews?.find(row => row.gate === 'final' && (row.subject ?? null) === null); }
function validateRemote(remote, plan) {
  const review = finalReview(remote);
  insist(remote?.slug === plan.slug && !remote.dropped_at && !remote.youtube_video_id && review?.status === 'approved'
    && review.content_sha256 === plan.pins.final.sha256
    && review.id === plan.pins.final.review_id, 'The actual current remote final does not approve the pinned cut');
  insist(Object.keys(remote.dub_retries ?? {}).length === 0 && Object.keys(remote.dub_retry_blocked ?? {}).length === 0,
    'An actual owner dub request or conflict arrived; this separate retake was not dispatched');
}

/**
 * Build an inspectable plan from real local files. This does not acquire a lease, change a
 * counter, contact a service, or ignore a future backoff. Execution rechecks every pin and due.
 */
export async function planServiceRetake({ ctx, slug, locale, lineId, failureReceipt, now = ctx?.now }) {
  insist(ctx?.root && ID.test(slug ?? '') && LOCALES.has(locale) && ID.test(lineId ?? ''), 'A scoped project, supported locale and line ID are required');
  const workdir = resolveWorkdir({ env: ctx.env, slug, root: ctx.root, home: ctx.home });
  insist(!stopRequested(workdir), 'STOP holds the project');
  insist(!inspectServiceRetakeIntents(workdir).some(row => row.phase !== 'applied'), 'An earlier service-retake intent is unresolved');
  insist(failureReceipt && SHA.test(failureReceipt.sha256 ?? ''), 'The actual settled-failure receipt needs its exact SHA-256');
  const evidencePin = filePin(failureReceipt.file);
  insist(evidencePin.sha256 === failureReceipt.sha256, 'Settled-failure receipt bytes differ');
  const evidence = read(failureReceipt.file);
  const stateFile = path.join(workdir, 'auto.json'), statePin = filePin(stateFile), state = read(stateFile);
  const rounds = state.languages?.[locale];
  insist(state.slug === slug && ['active', 'done'].includes(state.status) && !state.blocked && !state.tidied_at, 'The native project is absent, blocked or tidied');
  insist(rounds?.shorten === 1 && rounds.retakes === MAX_DUB_RETAKE_ROUNDS - 1 && rounds.reword === 0 && rounds.check_stopped === true,
    'This recovery requires exactly the existing unfinished first-retake boundary; no cap is reset');
  insist(state.defer_count === MIN_SETTLED_FAILURES && Number.isFinite(Date.parse(state.deferred_until ?? '')), 'The genuine six-failure native backoff is required');
  insist(evidence.slug === slug && evidence.one_native_invocation_only === true
    && evidence.native_quality_result === 'unfinished_due_explicit_known_service_refusal_not_quality_ready'
    && evidence.before_defer_count === MIN_SETTLED_FAILURES - 1 && evidence.after_defer_count === MIN_SETTLED_FAILURES
    && evidence.next_native_due_utc === state.deferred_until && evidence.no_new_unknown_speech_journal === true,
  'The receipt is not the exact settled sixth service failure');
  insist(typeof evidence.native_log_exact === 'string' && evidence.native_log_exact.includes(lineId)
    && evidence.native_log_exact.includes('Gemini') && evidence.native_log_exact.includes('OTHER')
    && /no transcript|無法轉寫/.test(evidence.native_log_exact) && !/uncertain|answer.lost/i.test(evidence.native_log_exact),
  'Only the explicitly settled no-transcript refusal qualifies; no uncertain result or generic outage');
  insist(SHA.test(evidence.preflight_sha256 ?? '') && typeof evidence.preflight_file === 'string', 'The actual failure needs its source-bound preflight receipt');
  const preflightPin = filePin(evidence.preflight_file);
  insist(preflightPin.sha256 === evidence.preflight_sha256, 'The historical preflight receipt changed');
  const preflight = read(preflightPin.file);
  insist(preflight.all_preflight_checks_passed === true && preflight.remote?.final?.status === 'approved'
    && typeof preflight.remote.final.id === 'string' && SHA.test(preflight.remote.final.sha256 ?? ''), 'The historical primary approval was not recorded');
  const project = loadProject({ root: ctx.root, slug });
  insist(project.doc.format === 'slides', 'This recovery is limited to a narrated slides project');
  const sourcePin = filePin(path.join(ctx.root, 'docs', 'videos', slug, 'video.json'));
  const translationPin = filePin(path.join(ctx.root, 'docs', 'videos', slug, 'i18n', `${locale}.json`));
  insist(preflight.media_source_sha256 === sourcePin.sha256, 'The current source is stale against the historical approved-primary preflight');
  insist(evidence[`${locale.toUpperCase()}_source_sha256`] === translationPin.sha256, 'The receipt does not bind the current translation');
  const files = dubArtifacts(workdir, locale);
  insist(!existsSync(files.skipped), 'A native skip requires its actual owner retry; this adapter cannot clear it');
  const timelinePin = filePin(path.join(workdir, 'timeline.json')), timeline = read(timelinePin.file);
  const speech = speechHash(project.doc, project.lexicon);
  insist(timeline.speech_hash === speech, 'The primary narration/source binding is stale');
  const { requests, script, missing } = dubRequests(project, locale);
  insist(missing.length === 0, 'The authored translation is incomplete');
  const target = requests.flatMap(request => request.lines.map(line => ({ request, line }))).find(row => row.line.id === lineId);
  insist(target, 'The target is not a current translated line');
  const cachePin = filePin(files.cache), cache = read(files.cache), allClips = [];
  for (const request of requests) for (const line of request.lines) {
    insist([line.key, request.key].includes(cache.lines?.[line.id]), `A clip is stale: ${line.id}`);
    allClips.push({ id: line.id, ...filePin(path.join(files.audio, `${line.id}.wav`)), line_key: line.key });
  }
  const clip = allClips.find(row => row.id === lineId);
  insist(evidence[`${lineId}_wav_sha256`] === clip.sha256, 'The repeated-failure WAV is not the current target');
  insist(requireNarrationFormat(parseWav(regular(clip.file))).length > 0, 'The target WAV has no samples');
  const fitPin = filePin(files.fit), fit = read(files.fit), fingerprint = speechFingerprint(requests), translation = translationHash(script);
  insist(fit.speech_hash === speech && fit.translation_hash === translation && fit.speech_fingerprint === fingerprint
    && Array.isArray(fit.over) && fit.over.length === 0 && (fit.kept ?? []).length === 0, 'The existing fit or voice fingerprint is stale or unresolved');
  const primary = await approvalState({ gate: 'final', docDir: path.join(ctx.root, 'docs', 'videos', slug), workdir });
  const finalPin = filePin(path.join(workdir, 'final.mp4'));
  insist(primary.status === 'approved' && primary.sha256 === finalPin.sha256, 'The current primary final is not genuinely approved');
  const qaPin = filePin(path.join(workdir, 'review', 'qa.json')), qa = read(qaPin.file);
  insist(qa.ok === true && qa.final_sha256 === finalPin.sha256 && qa.items?.length === ITEM_IDS.length
    && isDeepStrictEqual(qa.items.map(row => row.id).sort(), [...ITEM_IDS].sort())
    && qa.items.every(row => row.ok === true), 'The pinned primary lacks its successful eleven distinct native QA items');
  insist(preflight.remote.final.sha256 === finalPin.sha256, 'The historical and current primary final differ');
  const protectedPins = Object.entries(evidence.protected_evidence ?? {}).map(([relative, row]) => {
    insist(row.unchanged === true && SHA.test(row.after_sha256 ?? '') && row.before_sha256 === row.after_sha256, 'A protected-file receipt is not intact');
    const pin = filePin(childFile(workdir, relative));
    insist(pin.sha256 === row.after_sha256, `Protected evidence changed since the settled outcome: ${relative}`);
    return pin;
  });
  for (const relative of ['final.mp4', 'approvals.json', 'timeline.json', 'checks.json', 'languages.json'])
    insist(protectedPins.some(pin => pin.file === path.join(workdir, relative)), `Required protected evidence is missing: ${relative}`);
  const journals = journalPins(workdir);
  insist(isDeepStrictEqual(journals, receiptJournalPins(evidence)), 'The unresolved speech-journal inventory changed; nothing was forgotten or replayed');
  const requestBody = lineBody(target.request, target.line), requestHash = digest(JSON.stringify(requestBody));
  insist(!journals.some(row => path.basename(row.file) === `${requestHash}.json`), 'This target TTS request already has a retained/unknown generation');
  const finalReviewId = preflight.remote.final.id;
  const identity = { slug, locale, line_id: lineId, primary_sha256: finalPin.sha256, speech_hash: speech,
    translation_hash: translation, target_wav_sha256: clip.sha256, request_sha256: requestHash,
    retake_before: rounds.retakes, retake_after: MAX_DUB_RETAKE_ROUNDS };
  return { schema_version: 1, kind: 'settled-service-retake-plan', planned_at: stamp(now), intent_id: digest(JSON.stringify(identity)),
    ...identity, lineId, site: ctx.site ?? 'https://mokaair.com', root: ctx.root, workdir,
    due_at: state.deferred_until, earliest_execution_reached: Date.parse(state.deferred_until) <= Date.parse(stamp(now)),
    request_body: requestBody, billable_characters: billableForRequest(requestBody), voice_ready: false,
    pins: { state: statePin, source: sourcePin, translation: translationPin, primary_timeline: timelinePin, cache: cachePin,
      fit: fitPin, qa: qaPin, final: { ...finalPin, review_id: finalReviewId }, failure_receipt: evidencePin, preflight: preflightPin,
      protected: protectedPins, all_clips: allClips, journals },
    required_integration: 'Every original producer must call assertNoServiceRetakeHold under its native lease before any paid action.' };
}

function verifyStaticPins(plan, { after = false, ownSentSince = null, requireOwnSent = false } = {}) {
  for (const key of ['source', 'translation', 'primary_timeline', 'qa', 'final', 'failure_receipt', 'preflight']) verifyPin(plan.pins[key]);
  plan.pins.protected.forEach(verifyPin);
  for (const pin of plan.pins.all_clips) if (!after || pin.id !== plan.lineId) verifyPin(pin);
  let journals = journalPins(plan.workdir);
  if (ownSentSince !== null) {
    const targetFile = path.join(plan.workdir, 'audio', 'speech-journal', `${plan.request_sha256}.json`);
    const own = journals.find(row => row.file === targetFile);
    insist(!requireOwnSent || own, 'The native synthesis has no current-process sent journal');
    if (own) {
      const entry = read(targetFile);
      insist(entry.status === 'sent' && entry.path === 'speech' && entry.producer_pid === process.pid
        && entry.request_sha256 === plan.request_sha256 && isDeepStrictEqual(entry.request, plan.request_body)
        && Number.isFinite(Date.parse(entry.sent_at ?? '')) && Date.parse(entry.sent_at) >= Date.parse(ownSentSince),
      'The target journal is not this dispatch\'s exact current-process sent generation');
      journals = journals.filter(row => row.file !== targetFile);
    }
  }
  insist(isDeepStrictEqual(journals, plan.pins.journals), 'The speech journals changed or contain an unresolved target operation');
}
function verifyPlanShape(plan, ctx) {
  insist(plan?.schema_version === 1 && plan.kind === 'settled-service-retake-plan' && SHA.test(plan.intent_id ?? ''), 'A real reviewed service-retake plan is required');
  insist(ctx.root === plan.root && resolveWorkdir({ env: ctx.env, slug: plan.slug, root: ctx.root, home: ctx.home }) === plan.workdir, 'The plan is bound to another repository or work base');
  insist(LOCALES.has(plan.locale) && plan.retake_before === MAX_DUB_RETAKE_ROUNDS - 1 && plan.retake_after === MAX_DUB_RETAKE_ROUNDS
    && digest(JSON.stringify(plan.request_body)) === plan.request_sha256, 'The native retake cap or planned request changed');
}
function resultCode(result) { return typeof result === 'number' ? result : result?.code; }

/**
 * One irreversible dispatch opportunity. No automatic retry, cancellation, counter refund,
 * journal forget or held-intent resolution exists here. All test transports/runners are
 * injected; the default runner uses the real unchanged native dub command.
 */
export async function executeServiceRetake({ plan, ctx, getRemote, fetch: fetchImpl = ctx.fetch ?? globalThis.fetch,
  runNative, checkpoint = async () => {} }) {
  verifyPlanShape(plan, ctx);
  const dir = path.join(plan.workdir, SERVICE_RETAKE_DIRECTORY, plan.intent_id), intentFile = path.join(dir, 'intent.json');
  const prior = inspectServiceRetakeIntents(plan.workdir).find(row => row.id === plan.intent_id);
  if (prior?.phase === 'applied') return { status: 'already_applied', intent_file: intentFile, voice_ready: false, dispatched: false };
  let lease, intent = null;
  const now = ctx.now ?? (() => new Date());
  const assertOwned = () => { lease.verify(); insist(!stopRequested(plan.workdir), 'STOP holds this operation'); };
  const save = value => { lease.verify(); writeDurable(intentFile, bytes(value)); intent = value; };
  try {
    lease = acquireProjectLease(plan.workdir, { owner: 'bounded-service-retake', now });
    assertNoServiceRetakeHold(plan.workdir, { lease, now });
    assertOwned();
    insist(Date.parse(plan.due_at) <= Date.parse(stamp(now)), `Native backoff remains in force until ${plan.due_at}`);
    const current = await planServiceRetake({ ctx, slug: plan.slug, locale: plan.locale, lineId: plan.lineId,
      failureReceipt: { file: plan.pins.failure_receipt.file, sha256: plan.pins.failure_receipt.sha256 }, now });
    insist(current.intent_id === plan.intent_id && current.due_at === plan.due_at && current.site === plan.site
      && current.earliest_execution_reached === true && isDeepStrictEqual(current.pins, plan.pins)
      && isDeepStrictEqual(current.request_body, plan.request_body), 'The reviewed plan is stale or its real backoff is not due');
    let remote = getRemote;
    if (!remote) {
      const client = siteClient({ env: ctx.env, home: ctx.home, attempts: 1 });
      insist(client.site === plan.site, 'The configured site differs from the reviewed plan');
      remote = () => client.project(plan.slug);
    }
    validateRemote(await remote(), plan);
    assertOwned(); verifyStaticPins(plan); verifyPin(plan.pins.state); verifyPin(plan.pins.cache); verifyPin(plan.pins.fit);
    mkdirSync(dir, { recursive: true });
    const reserved = read(plan.pins.state.file);
    reserved.languages[plan.locale].retakes = MAX_DUB_RETAKE_ROUNDS;
    reserved.languages[plan.locale].check_stopped = true;
    const reservedBytes = bytes(reserved);
    intent = { schema_version: 1, intent_id: plan.intent_id, slug: plan.slug, locale: plan.locale, line_id: plan.lineId,
      phase: 'prepared', prepared_at: stamp(now), plan, state_reserved_sha256: digest(reservedBytes),
      meaning: 'A remaining native retake is reserved for one new synthesis; this is not audio acceptance.' };
    createDurable(intentFile, bytes(intent));
    createDurable(path.join(dir, 'before-auto.json'), regular(plan.pins.state.file));
    createDurable(path.join(dir, 'before-target.wav'), regular(plan.pins.all_clips.find(row => row.id === plan.lineId).file));
    createDurable(path.join(dir, 'before-video.json'), regular(plan.pins.source.file));
    createDurable(path.join(dir, 'before-translation.json'), regular(plan.pins.translation.file));
    await checkpoint('after_intent');
    assertOwned(); verifyStaticPins(plan); verifyPin(plan.pins.state);
    writeDurable(plan.pins.state.file, reservedBytes);
    save({ ...intent, phase: 'reserved', reserved_at: stamp(now) });
    await checkpoint('after_reservation');
    assertOwned(); verifyStaticPins(plan);
    insist(filePin(plan.pins.state.file).sha256 === intent.state_reserved_sha256, 'The counted reservation changed');
    const requestFile = path.join(dir, 'retake-request.json');
    createDurable(requestFile, bytes([plan.lineId])); // Honest requested IDs, never fabricated QA flags.
    createDurable(path.join(dir, 'DISPATCHED.json'), bytes({ intent_id: plan.intent_id, request_sha256: plan.request_sha256, at: stamp(now) }));
    save({ ...intent, phase: 'dispatched', dispatched_at: stamp(now), request_file: requestFile });
    await checkpoint('after_dispatch_marker');
    assertOwned();
    let postCount = 0, successfulResponse = null;
    const guardedFetch = async (input, init = {}) => {
      assertOwned();
      const url = new URL(String(input)), method = init.method ?? 'GET';
      insist(url.origin === plan.site && !url.search, 'The native retake refused another origin/query');
      if (method === 'GET') {
        insist(url.pathname === '/api/video/speech/status', 'Only the native speech-budget GET is allowed');
        return fetchImpl(input, { ...init, redirect: 'error' });
      }
      insist(method === 'POST' && url.pathname === '/api/video/speech'
        && typeof init.body === 'string' && digest(init.body) === plan.request_sha256, 'Only the exact one-line synthesis POST is allowed');
      insist(postCount === 0, 'The durable retake opportunity was already dispatched; no second POST is allowed');
      // Native synthesis creates its own sent journal immediately before this call. Admit
      // only that new exact generation; the pre-existing EN hold remains byte-bound.
      verifyStaticPins(plan, { ownSentSince: intent.dispatched_at, requireOwnSent: !runNative });
      verifyPin(plan.pins.cache); verifyPin(plan.pins.fit);
      insist(filePin(plan.pins.state.file).sha256 === intent.state_reserved_sha256, 'The counted reservation changed before the actual POST');
      postCount += 1;
      createDurable(path.join(dir, 'HTTP-SENT.json'), bytes({ intent_id: plan.intent_id, request_sha256: plan.request_sha256, at: stamp(now) }));
      const response = await fetchImpl(input, { ...init, redirect: 'error' });
      const answer = Buffer.from(await response.clone().arrayBuffer());
      insist(answer.length <= 8 * 1024 * 1024, 'The single-line response exceeds the retained-answer bound');
      createDurable(path.join(dir, 'http-answer.bin'), answer);
      const receipt = { request_sha256: plan.request_sha256, response_status: response.status,
        response_sha256: digest(answer), response_bytes: answer.length,
        billable_characters_reported: response.headers.get('x-billable-characters'), received_at: stamp(now) };
      createDurable(path.join(dir, 'http-answer.json'), bytes(receipt));
      if (response.ok) successfulResponse = receipt;
      return response;
    };
    const command = ['dub', '--slug', plan.slug, '--locale', plan.locale, '--redo', requestFile, '--line-by-line'];
    const guardedCtx = { ...ctx, fetch: guardedFetch };
    const runner = runNative ?? (async (args, context) => {
      const { main } = await import('../cli.mjs'); let out = '';
      const sink = { write(text) { out += text; ctx.stdout?.write(text); } };
      const code = await main(args, { ...context, stdout: sink, stderr: sink }); return { code, out };
    });
    const result = await runner(command, guardedCtx);
    await checkpoint('after_native_return');
    assertOwned();
    insist([0, 1].includes(resultCode(result)) && postCount === 1 && successfulResponse,
      'The retake has no single confirmed successful synthesis; preserve its evidence and do not replay it');
    verifyStaticPins(plan, { after: true });
    insist(filePin(plan.pins.state.file).sha256 === intent.state_reserved_sha256, 'The native retake counter changed unexpectedly');
    const files = dubArtifacts(plan.workdir, plan.locale), cache = read(files.cache), target = plan.pins.all_clips.find(row => row.id === plan.lineId);
    const after = filePin(target.file);
    insist(requireNarrationFormat(parseWav(regular(target.file))).length > 0 && cache.lines[plan.lineId] === target.line_key, 'The actual current raw take/cache is not intact');
    // --line-by-line takes exactly this native normalization/trim path. A 200 response and
    // an old intact raw alone do not prove the returned take was actually installed.
    const expectedRaw = encodeWav(trimSilence(requireNarrationFormat(parseWav(toNarrationRate(regular(path.join(dir, 'http-answer.bin')))))));
    insist(digest(expectedRaw) === after.sha256, 'The confirmed response was not installed as the exact native raw take');
    validateRemote(await remote(), plan);
    await checkpoint('before_applied');
    assertOwned();
    const outcome = { status: 'applied', intent_file: intentFile, command, native_exit_code: resultCode(result),
      target_before_sha256: target.sha256, target_after_sha256: after.sha256, same_wav_bytes: target.sha256 === after.sha256,
      confirmed_response: successfulResponse, installed_raw_matches_response: true,
      retakes_before: plan.retake_before, retakes_after: MAX_DUB_RETAKE_ROUNDS,
      voice_ready: false, check_stopped: true, asr_performed: false,
      next: 'Use plain native makeDub/dub and real ASR/Jev. Never repeat this redo; all original caps/backoff remain.' };
    save({ ...intent, phase: 'applied', applied_at: stamp(now), outcome });
    return outcome;
  } catch (error) {
    let owned = false; try { lease?.verify(); owned = Boolean(lease); } catch { /* Permanent intent still fences the next producer. */ }
    if (intent && owned) {
      try {
        save({ ...intent, phase: 'held', held_at: stamp(now), hold_reason: error.message,
          meaning: 'No replay, counter refund, journal forgetting or voice approval is authorized.' });
        ownStop(plan.workdir, { id: plan.intent_id, file: intentFile, intent }, lease, now);
      } catch { /* Do not replace the original error or write through a successor lease. */ }
    }
    throw error;
  } finally { lease?.release(); }
}
