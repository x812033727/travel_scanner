// Bind a listening decision to the actual takes and narration, not just their durations.
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import path from "node:path";

import { parseWav, requireNarrationFormat } from "../tts/wav.mjs";

const SHA256 = /^[a-f0-9]{64}$/;
const LINE_ID = /^[a-z0-9]{4,8}$/;
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
// The full file is hashed on every check. Reusing the format/sample count of those exact
// bytes avoids decoding millions of PCM samples on every worker status update.
const sampleCounts = new Map();
const MAX_MEASUREMENTS = 1024;

function audioFiles(timeline, workdir) {
  if (!Array.isArray(timeline?.lines) || !timeline.lines.length) throw new Error("timeline has no audio lines");
  const ids = new Set();
  const files = timeline.lines.map((line) => {
    if (!LINE_ID.test(line.id ?? "") || ids.has(line.id)) throw new Error("timeline has an invalid or duplicate audio line id");
    ids.add(line.id);
    return { label: `audio/${line.id}.wav`, file: path.join(workdir, "audio", `${line.id}.wav`), expected: line.audio_sha256, samples: line.audio_samples };
  });
  files.push({ label: "narration.wav", file: path.join(workdir, "narration.wav"), expected: timeline.audio_evidence?.narration_sha256, samples: timeline.total_frames * (48_000 / timeline.fps) });
  return files;
}

function measured(file, verify = false) {
  const bytes = readFileSync(file.file);
  const hash = digest(bytes);
  if (verify && hash !== file.expected) return hash;
  let samples = sampleCounts.get(hash);
  if (samples === undefined) {
    samples = requireNarrationFormat(parseWav(bytes)).length;
    if (sampleCounts.size >= MAX_MEASUREMENTS) sampleCounts.delete(sampleCounts.keys().next().value);
    sampleCounts.set(hash, samples);
  }
  if (!Number.isInteger(file.samples) || file.samples <= 0 || samples !== file.samples) throw new Error(`${file.label} sample length does not match timeline.json`);
  return hash;
}

/** Call only after saving every take and the assembled narration. Does not approve any audio. */
export function bindAudioEvidence(timeline, workdir) {
  const hashes = audioFiles(timeline, workdir).map((file) => measured(file));
  return {
    ...timeline,
    lines: timeline.lines.map((line, index) => ({ ...line, audio_sha256: hashes[index] })),
    audio_evidence: { schema_version: 1, narration_sha256: hashes.at(-1) },
  };
}

/** Legacy bindings are unreviewed; `tts` can refresh the manifest from cached WAVs. */
export function audioEvidenceProblems(timeline, workdir) {
  if (timeline?.audio_evidence?.schema_version !== 1) return ["timeline.json has no current audio evidence; run tts to refresh cached takes, then review the narration again"];
  try {
    const problems = [];
    for (const file of audioFiles(timeline, workdir)) {
      if (!SHA256.test(file.expected ?? "")) problems.push(`${file.label} has no SHA256 binding in timeline.json`);
      else if (measured(file, true) !== file.expected) problems.push(`${file.label} differs from the take bound to timeline.json; restore the reviewed take or refresh and review the narration again`);
    }
    return problems;
  } catch (error) {
    return [`audio evidence cannot be verified: ${error.message}`];
  }
}

/** A transcript verdict belongs only to this exact take. Others remain unchecked. */
export function currentAudioCheck(check, timeline) {
  const lines = {};
  for (const line of timeline?.lines ?? []) {
    const entry = check?.lines?.[line.id];
    if (SHA256.test(line.audio_sha256 ?? "") && entry?.clip === line.audio_sha256.slice(0, 16)) lines[line.id] = entry;
  }
  return { ...check, lines };
}

/** The final cut must have been mixed from the same dry narration that is being reviewed now. */
export function assembledAudioProblems(timeline, checks, workdir) {
  const problems = audioEvidenceProblems(timeline, workdir);
  if (!SHA256.test(checks?.narration_sha256 ?? "") || checks.narration_sha256 !== timeline?.audio_evidence?.narration_sha256) problems.push("final.mp4 was not assembled from the current narration take; run assemble and review the new cut");
  return problems;
}
