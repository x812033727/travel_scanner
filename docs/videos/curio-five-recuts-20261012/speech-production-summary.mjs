// Read-only media audit. Writes one bounded production receipt; no speech client.
import { createHash } from "node:crypto";
import { existsSync, lstatSync, readdirSync, readFileSync } from "node:fs";
import { homedir } from "node:os";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { audioEvidenceProblems } from "../../../tools/video/core/audio-evidence.mjs";
import { atomicWrite } from "../../../tools/video/core/paths.mjs";
import { speechHash } from "../../../tools/video/core/timeline.mjs";
import { parseWav, requireNarrationFormat } from "../../../tools/video/tts/wav.mjs";
import { ALLOWED_SLUGS, describePlan, loadEpisode, LOCALES } from "./speech.mjs";
import { readSecondOpinionResolutions } from "./retake.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const read = (file) => JSON.parse(readFileSync(file, "utf8").replace(/^\uFEFF/, ""));
const json = (value) => `${JSON.stringify(value, null, 2)}\n`;
const need = (ok, message) => { if (!ok) throw new Error(message); };
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const stamp = () => new Date().toISOString();

function jsonFiles(root) {
  if (!existsSync(root)) return [];
  const files = [];
  for (const entry of readdirSync(root, { withFileTypes: true })) {
    const file = path.join(root, entry.name), stat = lstatSync(file);
    need(!stat.isSymbolicLink(), "audit refuses links/junctions in production evidence");
    if (stat.isDirectory()) files.push(...jsonFiles(file));
    else if (entry.name.endsWith(".json")) files.push(file);
  }
  return files.sort();
}

export function responseKey(slug, locale, line, receipt) {
  // saved_at distinguishes separate provider responses even if identical audio
  // were returned twice; copied/archived receipts keep that exact timestamp.
  return [slug, locale, line, receipt.request_sha256, receipt.sha256, receipt.saved_at].join("|");
}

export function auditProduction(out) {
  out = path.resolve(out);
  const sources = path.join(out, "sources"), originalFile = path.join(HERE, "intro-specs.json");
  const originalSpec = read(originalFile), before = new Map(), fileHashes = new Map();
  const recordFile = (file) => {
    const sha = hash(readFileSync(file));
    if (before.has(file)) need(before.get(file) === sha, "evidence changed during audit");
    before.set(file, sha); fileHashes.set(file, sha); return sha;
  };
  const fileHash = (file) => fileHashes.get(file) ?? recordFile(file);
  recordFile(originalFile);
  const tracks = [], responses = new Map(), journals = [];
  const baseline = new Map();
  for (const slug of ALLOWED_SLUGS) {
    const original = originalSpec.episodes.find((episode) => episode.slug === slug);
    for (const locale of LOCALES) {
      const item = loadEpisode({ episode: original, sources, out, locale });
      for (const request of item.requests) baseline.set(`${slug}|${locale}|${request.lines[0].id}`, item.identity.request_sha256[item.requests.indexOf(request)]);
    }
    const specFile = path.join(HERE, slug === "curio-h03" ? "h03-pronunciation-specs.json" : slug === "curio-l08" ? "l08-wording-specs.json" : "intro-specs.json");
    const specSha = recordFile(specFile), spec = read(specFile), episode = spec.episodes.find((entry) => entry.slug === slug);
    const sharedFile = path.join(out, slug, "intro", "shared-timeline.json"), shared = read(sharedFile);
    recordFile(sharedFile);
    need(shared.duration_ok && shared.padding_ok && shared.seconds >= 30 && shared.seconds <= 60 && shared.time_stretched === false, `${slug}: shared opening gate failed`);
    for (const locale of LOCALES) {
      const item = loadEpisode({ episode, sources, out, locale });
      const plan = describePlan(item);
      need(plan.pending_lines === 0, `${slug}/${locale}: unfinished synthesis`);
      const receiptFile = path.join(item.directory, "receipt.json"), checkFile = path.join(item.directory, "check.json"), timelineFile = path.join(item.directory, "timeline.json"), captionFile = path.join(item.directory, `${locale}.srt`), narrationFile = path.join(item.directory, "narration.wav");
      const receipt = read(receiptFile), check = read(checkFile), timeline = read(timelineFile);
      const receiptSha = recordFile(receiptFile), checkSha = recordFile(checkFile), timelineSha = recordFile(timelineFile), captionSha = recordFile(captionFile), narrationSha = recordFile(narrationFile);
      need(same(receipt.identity, item.identity) && same(check.identity, item.identity), `${slug}/${locale}: identity mismatch`);
      need(receipt.aligned && receipt.duration_ok && receipt.padding_ok && receipt.caption_problems.length === 0, `${slug}/${locale}: receipt gate failed`);
      need(receipt.timeline_sha256 === timelineSha && receipt.captions_sha256 === captionSha && receipt.narration_sha256 === narrationSha, `${slug}/${locale}: output hash mismatch`);
      need(check.timeline_sha256 === timelineSha && check.captions_sha256 === captionSha && check.narration_sha256 === narrationSha, `${slug}/${locale}: check is stale`);
      need(shared.tracks[locale].receipt_sha256 === receiptSha && shared.tracks[locale].narration_sha256 === narrationSha && shared.tracks[locale].timeline_sha256 === timelineSha && shared.tracks[locale].captions_sha256 === captionSha, `${slug}/${locale}: shared binding mismatch`);
      need(timeline.speech_hash === speechHash(item.doc, item.lexicon) && audioEvidenceProblems(timeline, item.directory).length === 0, `${slug}/${locale}: audio evidence failed`);
      need(requireNarrationFormat(parseWav(readFileSync(narrationFile))).length === shared.total_frames * 1600, `${slug}/${locale}: sample/frame mismatch`);
      const resolved = readSecondOpinionResolutions(item.directory, check), flags = check.flags ?? [];
      const unresolved = flags.filter((id) => !resolved.has(id));
      need(unresolved.length === 0 && (check.ok === true || flags.length > 0), `${slug}/${locale}: unresolved opening audio gate`);
      const independent = [];
      const indexFile = path.join(item.directory, "second-opinion.json");
      if (existsSync(indexFile)) {
        const index = read(indexFile); recordFile(indexFile);
        for (const id of resolved) {
          const pointer = index.lines[id], file = path.join(item.directory, "second-opinion", pointer.file), evidence = read(file);
          need(recordFile(file) === pointer.sha256, "independent evidence index changed");
          independent.push({ line: id, outcome: evidence.outcome, wav_sha256: evidence.clip_sha256, evidence_file: file, evidence_sha256: pointer.sha256, intended: evidence.intended, heard: evidence.heard });
        }
      }
      tracks.push({ slug, locale, spec_file: specFile, spec_sha256: specSha, source_voice: item.doc.voice, voice_sha256: item.identity.voice_sha256, source_voice_file: item.voiceFile ?? item.sourceFile, source_voice_file_sha256: item.identity.voice_source_sha256 ?? item.identity.source_sha256, current_lines: item.lines.length, pending_lines: 0, seconds: shared.seconds, primary_check_ok: check.ok, primary_flags_preserved: flags, primary_clear_lines: item.lines.length - flags.length, validated_second_opinion_lines: [...resolved], independent_evidence: independent, automated_opening_audio_gate: true, receipt_file: receiptFile, receipt_sha256: receiptSha, check_file: checkFile, check_sha256: checkSha, narration_sha256: narrationSha, timeline_sha256: timelineSha, captions_sha256: captionSha, owner_listened: false, full_video_approved: false });
    }
    const evidenceFiles = [...jsonFiles(path.join(out, slug, "intro")), ...jsonFiles(path.join(out, slug, "intro-revisions"))];
    for (const file of evidenceFiles) {
      const normalized = file.replaceAll("\\", "/");
      if (/\/speech-journal\/[a-f0-9]{64}\.json$/.test(normalized)) {
        const journal = read(file);
        journals.push({ file, sha256: recordFile(file), status: journal.status, route: journal.route ?? null, request_sha256: journal.request_sha256 ?? path.basename(file, ".json") });
      }
      if (path.basename(file) !== "receipt.json") continue;
      const receipt = read(file);
      if (receipt.kind !== "curio-opening-fragment") continue;
      need(receipt.identity.slug === slug && LOCALES.includes(receipt.identity.locale), "receipt escaped audited cohort");
      const receiptSha = recordFile(file), locale = receipt.identity.locale;
      for (const [line, entry] of Object.entries(receipt.lines)) {
        need(entry.saved_at && /^[a-f0-9]{64}$/.test(entry.sha256) && /^[a-f0-9]{64}$/.test(entry.request_sha256), "incomplete saved synthesis response");
        const key = responseKey(slug, locale, line, entry);
        const classification = entry.retake_attempt ? "same-text-retake" : entry.request_sha256 !== baseline.get(`${slug}|${locale}|${line}`) ? (slug === "curio-h03" ? "pronunciation-revision" : "wording-revision") : "initial";
        let response = responses.get(key);
        if (response) need(response.reported_billable_characters === entry.billable && response.samples === entry.samples && response.classification === classification, "duplicate receipt disagrees about its synthesis response");
        else {
          response = { slug, locale, line, request_sha256: entry.request_sha256, wav_sha256: entry.sha256, saved_at: entry.saved_at, samples: entry.samples, reported_billable_characters: entry.billable ?? null, classification, retake_attempt: entry.retake_attempt ?? null, receipt_evidence: [], wav_evidence: null };
          responses.set(key, response);
        }
        response.receipt_evidence.push({ file, sha256: receiptSha });
        const wavFile = path.join(path.dirname(file), "audio", `${line}.wav`);
        if (!response.wav_evidence && existsSync(wavFile) && fileHash(wavFile) === entry.sha256) response.wav_evidence = { file: wavFile, sha256: entry.sha256 };
      }
    }
  }
  const saved = [...responses.values()].sort((a, b) => a.saved_at.localeCompare(b.saved_at) || a.slug.localeCompare(b.slug));
  for (const response of saved) need(response.wav_evidence, `saved response has no matching preserved WAV: ${response.slug}/${response.locale}/${response.line}/${response.saved_at}`);
  const byClass = {};
  for (const response of saved) {
    const row = byClass[response.classification] ??= { responses: 0, reported_billable_characters: 0, missing_billable_receipts: 0 };
    row.responses++;
    if (Number.isFinite(response.reported_billable_characters)) row.reported_billable_characters += response.reported_billable_characters;
    else row.missing_billable_receipts++;
  }
  need(saved.length === 152 && byClass.initial?.responses === 144 && byClass["same-text-retake"]?.responses === 5 && byClass["pronunciation-revision"]?.responses === 2 && byClass["wording-revision"]?.responses === 1, "observed synthesis lineage differs from the authorized 144 + 5 + 2 + 1");
  const holds = journals.filter((entry) => ["sent", "held", "waiting"].includes(entry.status));
  need(holds.length === 0, "paid speech journal contains unresolved work");
  const sourceMapFile = path.join(out, "source-map.json"), sourceMap = read(sourceMapFile);
  const sourceMapSha = recordFile(sourceMapFile);
  const sourceQualification = sourceMap.episodes.find((episode) => episode.slug === "curio-h01").locales.ja.source_review_note;
  need(sourceQualification, "H01 original Japanese source qualification is missing");
  // The report is a snapshot only if every source read remains unchanged.
  for (const [file, sha] of before) need(hash(readFileSync(file)) === sha, `production evidence changed before receipt commit: ${file}`);
  return { schema_version: 1, kind: "curio-bounded-speech-production-summary", created_at: stamp(), output_root: out, media_read_only: true, service_calls_made_by_audit: 0, totals: { current_tracks: tracks.length, current_lines: tracks.reduce((sum, track) => sum + track.current_lines, 0), pending_synthesis_requests: 0, recorded_synthesis_responses: saved.length, unique_audio_sha256: new Set(saved.map((response) => response.wav_sha256)).size, unique_request_sha256: new Set(saved.map((response) => response.request_sha256)).size, reported_synthesis_billable_characters: saved.reduce((sum, response) => sum + (response.reported_billable_characters ?? 0), 0), missing_billable_receipts: saved.filter((response) => response.reported_billable_characters === null).length, primary_clear_tracks: tracks.filter((track) => track.primary_check_ok).length, primary_clear_lines: tracks.reduce((sum, track) => sum + track.primary_clear_lines, 0), tracks_with_validated_second_opinions: tracks.filter((track) => track.independent_evidence.length).length, validated_second_opinion_lines: tracks.reduce((sum, track) => sum + track.validated_second_opinion_lines.length, 0), automated_opening_audio_gate_tracks: tracks.length, unresolved_paid_journal_entries: holds.length }, synthesis_by_class: byClass, billing_scope: "Exact billable character values from saved synthesis responses only. Transcription/judge billing, currency charges and provider account balance are not inferred.", deduplication: "slug + locale + line + request SHA256 + returned clip SHA256 + saved_at; all copied/archived receipt paths retained as evidence, never counted again", paid_journal_audit: { scope: "All five intro and intro-revisions trees, including preserved retake histories. Original body/other projects and test fixtures excluded.", files_found: journals.length, entries: journals, unresolved: holds }, source_qualifications: [{ slug: "curio-h01", locale: "ja", applies_to: "reused original full body dub, not the newly checked opening", source_map_file: sourceMapFile, source_map_sha256: sourceMapSha, qualification: sourceQualification }], tracks, synthesis_responses: saved, owner_listened: false, full_video_approved: false, uploaded: false, published: false };
}

export function main(args = process.argv.slice(2)) {
  const { values } = parseArgs({ args, options: { out: { type: "string", default: path.join(homedir(), "mokaair-work/curio-five-recuts-20261012") } } });
  const summary = auditProduction(values.out), file = path.join(summary.output_root, "speech-production-summary.json");
  atomicWrite(file, json(summary));
  const readback = read(file);
  need(same(readback, summary), "production summary readback failed");
  console.log(json({ file, sha256: hash(readFileSync(file)), totals: summary.totals, synthesis_by_class: summary.synthesis_by_class, qualification: summary.source_qualifications[0].qualification, owner_listened: false }));
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) { try { main(); } catch (error) { console.error(error.message); process.exitCode = 1; } }
