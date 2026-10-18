// Recheck the original verified H07 sentence transfer against the current v2 script.
// Dry run by default. --record saves an immutable recheck receipt; --apply only adds
// request-identical missing WAVs and never overwrites old takes, caches or the first receipt.
import { createHash } from "node:crypto";
import { constants, copyFileSync, existsSync, lstatSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { audioEvidenceProblems } from "../../../tools/video/core/audio-evidence.mjs";
import { defaultWorkBase } from "../../../tools/video/core/paths.mjs";
import { loadProject } from "../../../tools/video/core/state.mjs";
import { speechHash } from "../../../tools/video/core/timeline.mjs";
import { dubRequests, dubScript, speechFingerprint, speechLexicon, translationHash } from "../../../tools/video/dubs/plan.mjs";
import { planRequests } from "../../../tools/video/tts/requests.mjs";
import { parseWav, requireNarrationFormat } from "../../../tools/video/tts/wav.mjs";

const slug = "curio-h07-v2";
const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "../../..");
const base = defaultWorkBase(os.homedir());
const source = path.join(base, "curio-h07");
const target = path.join(base, slug);
const args = process.argv.slice(2);
const mode = args.length === 0 ? "dry-run" : args.length === 1 && ["--record", "--apply"].includes(args[0]) ? args[0].slice(2) : null;
if (!mode) throw new Error("use --record for a new recheck receipt, --apply to add missing matching WAVs, or no flag for dry run");

const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const readJson = (file) => JSON.parse(readFileSync(file, "utf8"));
const assert = (condition, reason) => { if (!condition) throw new Error(reason); };

function regularFile(file) {
  const stat = lstatSync(file);
  assert(stat.isFile() && !stat.isSymbolicLink(), `not a regular file: ${file}`);
  return stat;
}

function safeDestination(file) {
  let parent = path.dirname(file);
  while (parent !== path.dirname(parent)) {
    if (existsSync(parent)) {
      const stat = lstatSync(parent);
      assert(stat.isDirectory() && !stat.isSymbolicLink(), `destination directory is not a plain directory: ${parent}`);
    }
    parent = path.dirname(parent);
  }
  if (existsSync(file)) regularFile(file);
}

function plannedLines(requests) {
  const lines = new Map();
  for (const request of requests) {
    assert(!request.audio_ref, `audio_ref ${request.id} needs a separate transfer rule`);
    for (const line of request.lines) {
      assert(!lines.has(line.id), `duplicate line id ${line.id}`);
      lines.set(line.id, { request, line });
    }
  }
  return lines;
}

const oldProject = loadProject({ slug: "curio-h07", root });
const newProject = loadProject({ slug, root });
assert(oldProject.doc.slug === "curio-h07" && newProject.doc.slug === slug, "source or target slug differs");
const oldSpeechHash = speechHash(oldProject.doc, oldProject.lexicon);
const newSpeechHash = speechHash(newProject.doc, newProject.lexicon);
const oldTimeline = readJson(path.join(source, "timeline.json"));
assert(oldTimeline.speech_hash === oldSpeechHash, "old narration timeline was built for a different source");
const evidence = audioEvidenceProblems(oldTimeline, source);
assert(evidence.length === 0, `old narration evidence differs: ${evidence.join("; ")}`);

const entries = [];
const caches = [];
const localeSummary = {};
const locales = ["zh-TW", "en", "ja", "ko"];
for (const locale of locales) {
  let oldPlan;
  let newPlan;
  let oldCache;
  let oldDir;
  let newDir;
  let newCache;
  let missingTranslations = new Set();
  if (locale === "zh-TW") {
    oldPlan = planRequests(oldProject.doc, oldProject.lexicon);
    newPlan = planRequests(newProject.doc, newProject.lexicon);
    oldDir = path.join(source, "audio");
    newDir = path.join(target, "audio");
    oldCache = readJson(path.join(oldDir, "cache.json"));
    newCache = { lines: {}, sha256: {} };
  } else {
    const oldDub = dubRequests(oldProject, locale);
    assert(oldDub.missing.length === 0, `${locale} source has stale or absent line translations`);
    const newDub = dubScript(newProject.doc, newProject.translations?.[locale], locale);
    missingTranslations = new Set(newDub.missing);
    oldPlan = oldDub.requests;
    // dubRequests intentionally returns no requests if any translation is stale. Planning
    // the fallback script here lets a partial audit name every stale line without paying.
    newPlan = planRequests(newDub.doc, speechLexicon(newProject.shelfLexicon, locale));
    oldDir = path.join(source, "dubs", locale, "audio");
    newDir = path.join(target, "dubs", locale, "audio");
    oldCache = readJson(path.join(oldDir, "cache.json"));
    newCache = { lines: {}, stretched: {} };
    const oldFit = readJson(path.join(source, "dubs", locale, "fit.json"));
    assert(oldFit.speech_hash === oldSpeechHash, `${locale} fit is bound to a different narration`);
    assert(oldFit.translation_hash === translationHash(oldDub.script), `${locale} fit is bound to a different translation`);
    assert(oldFit.speech_fingerprint === speechFingerprint(oldPlan) && oldFit.style_override == null,
      `${locale} fit voice request differs from the default source plan`);
  }

  const oldLines = plannedLines(oldPlan);
  const newLines = plannedLines(newPlan);
  assert(oldLines.size === 100 && newLines.size === 100, `${locale} expected 100 sentence clips, found ${oldLines.size}/${newLines.size}`);
  const oldTimelineLines = locale === "zh-TW" ? new Map(oldTimeline.lines.map((line) => [line.id, line])) : null;
  if (oldTimelineLines) assert(oldTimelineLines.size === 100, "old narration timeline does not have 100 unique lines");
  const currentCacheFile = path.join(newDir, "cache.json");
  const currentCache = existsSync(currentCacheFile) ? readJson(currentCacheFile) : { lines: {} };
  const stale = [];
  const matching = [];
  let localeBytes = 0;
  for (const [id, current] of newLines) {
    const previous = oldLines.get(id);
    assert(previous, `${locale}/${id} is absent from the old request plan`);
    assert([previous.line.key, previous.request.key].includes(oldCache.lines?.[id]), `${locale}/${id} source cache key is stale`);
    const from = path.join(oldDir, `${id}.wav`);
    regularFile(from);
    const bytes = readFileSync(from);
    const hash = sha256(bytes);
    const samples = requireNarrationFormat(parseWav(bytes)).length;
    assert(samples > 0, `${locale}/${id} has an empty WAV`);
    if (locale === "zh-TW") {
      assert(oldTimelineLines.get(id)?.audio_sha256 === hash, `${locale}/${id} differs from approved source timeline`);
      assert(oldTimelineLines.get(id)?.audio_samples === samples, `${locale}/${id} sample count differs from source timeline`);
      assert(oldCache.sha256?.[id] === hash, `${locale}/${id} source cache SHA256 differs`);
    }
    const to = path.join(newDir, `${id}.wav`);
    safeDestination(to);
    const destinationHash = existsSync(to) ? sha256(readFileSync(to)) : null;
    const sourceMatches = !missingTranslations.has(id) && current.line.key === previous.line.key;
    const cacheMatches = [current.line.key, current.request.key].includes(currentCache.lines?.[id]);
    // Once the pipeline retakes a changed line, the destination WAV can differ from the
    // historical copy. The old transfer remains an audit trail, not an overwrite target.
    if (destinationHash && destinationHash !== hash && currentCache.lines?.[id] === oldCache.lines?.[id]) {
      throw new Error(`${locale}/${id} copied WAV changed while its cache still claims the old key`);
    }
    const currentlyReused = sourceMatches && cacheMatches && destinationHash === hash;
    if (currentlyReused) matching.push(id);
    else stale.push(id);
    if (sourceMatches) {
      newCache.lines[id] = current.line.key;
      if (locale === "zh-TW") newCache.sha256[id] = hash;
    }
    entries.push({ locale, id, source: from, destination: to, old_request_key: previous.line.key,
      current_request_key: current.line.key, source_matches: sourceMatches, currently_reused: currentlyReused,
      destination_sha256: destinationHash, sha256: hash, bytes: bytes.length, samples });
    localeBytes += bytes.length;
  }
  localeSummary[locale] = { source_lines: oldLines.size, current_lines: newLines.size, copied_bytes: localeBytes,
    source_matching: Object.keys(newCache.lines).length, currently_reused: matching.length,
    matching_ids: matching, stale_ids: stale,
    ...(missingTranslations.size ? { missing_translation_ids: [...missingTranslations] } : {}) };
  const cacheFile = path.join(newDir, "cache.json");
  const cacheBytes = Buffer.from(`${JSON.stringify(newCache, null, 2)}\n`);
  safeDestination(cacheFile);
  caches.push({ file: cacheFile, bytes: cacheBytes });
}

assert(entries.length === 400, `expected 400 WAVs, found ${entries.length}`);
const sourceSet = new Set(entries.map((entry) => entry.source));
const destinationSet = new Set(entries.map((entry) => entry.destination));
assert(sourceSet.size === 400 && destinationSet.size === 400, "duplicate source or destination WAV path");
const totalBytes = entries.reduce((sum, entry) => sum + entry.bytes, 0);
const manifestFile = path.join(target, "audio-transfer-manifest.json");
regularFile(manifestFile);
const manifestBytes = readFileSync(manifestFile);
const originalManifest = JSON.parse(manifestBytes);
assert(originalManifest.operation === "verified-additive-sentence-cache-copy" &&
  originalManifest.source_slug === "curio-h07" && originalManifest.target_slug === slug &&
  originalManifest.source_speech_hash === oldSpeechHash && originalManifest.total_wavs === 400 &&
  originalManifest.total_bytes === totalBytes, "historical transfer manifest header differs");
assert(originalManifest.source_timeline_sha256 === sha256(readFileSync(path.join(source, "timeline.json"))) &&
  originalManifest.source_narration_sha256 === oldTimeline.audio_evidence.narration_sha256,
  "historical transfer manifest is bound to a different source timeline");
const originals = new Map(originalManifest.files.map((file) => [`${file.locale}/${file.id}`, file]));
assert(originals.size === 400, "historical transfer manifest does not name 400 unique WAVs");
for (const entry of entries) {
  const original = originals.get(`${entry.locale}/${entry.id}`);
  assert(original?.request_key === entry.old_request_key && original.sha256 === entry.sha256 &&
    original.bytes === entry.bytes && original.samples === entry.samples,
  `historical transfer receipt differs from the old source: ${entry.locale}/${entry.id}`);
}

const sourceFiles = ["video.json", "i18n/en.json", "i18n/ja.json", "i18n/ko.json"];
const currentSourceHashes = Object.fromEntries(sourceFiles.map((name) =>
  [name, sha256(readFileSync(path.join(root, "docs", "videos", slug, name)))]));
const recheck = {
  schema_version: 1,
  operation: "current-source-audio-reuse-recheck",
  source_slug: "curio-h07",
  target_slug: slug,
  historical_manifest_sha256: sha256(manifestBytes),
  current_source_sha256: currentSourceHashes,
  source_speech_hash: oldSpeechHash,
  target_speech_hash: newSpeechHash,
  locales: localeSummary,
  historical_wavs: entries.length,
  historical_bytes: totalBytes,
  // The old clips and cache entries remain on disk for a later explicit retake. A copied
  // WAV is reusable only when both its request key and its destination cache still match.
  pending_ids: Object.fromEntries(Object.entries(localeSummary).map(([locale, value]) => [locale, value.stale_ids])),
};
const recheckBytes = Buffer.from(`${JSON.stringify(recheck, null, 2)}\n`);
const recheckFile = path.join(target, `audio-transfer-recheck-${sha256(recheckBytes).slice(0, 12)}.json`);
safeDestination(recheckFile);
if (existsSync(recheckFile)) assert(readFileSync(recheckFile).equals(recheckBytes), "existing recheck receipt differs");

if (mode === "apply") {
  for (const entry of entries.filter((item) => item.source_matches)) {
    mkdirSync(path.dirname(entry.destination), { recursive: true });
    if (!existsSync(entry.destination)) copyFileSync(entry.source, entry.destination, constants.COPYFILE_EXCL);
    if (entry.destination_sha256 === null) assert(sha256(readFileSync(entry.destination)) === entry.sha256,
      `copied WAV differs: ${entry.locale}/${entry.id}`);
  }
  for (const cache of caches) if (!existsSync(cache.file)) writeFileSync(cache.file, cache.bytes, { flag: "wx" });
} else if (mode === "record" && !existsSync(recheckFile)) {
  writeFileSync(recheckFile, recheckBytes, { flag: "wx" });
}
console.log(JSON.stringify({ mode, source, target, source_speech_hash: oldSpeechHash,
  target_speech_hash: newSpeechHash, locales: Object.fromEntries(Object.entries(localeSummary)
    .map(([locale, value]) => [locale, { source_matching: value.source_matching, currently_reused: value.currently_reused,
      stale_ids: value.stale_ids }])),
  historical_wavs: entries.length, historical_bytes: totalBytes,
  historical_manifest_sha256: sha256(manifestBytes), recheck_file: mode === "record" ? recheckFile : null }, null, 2));
