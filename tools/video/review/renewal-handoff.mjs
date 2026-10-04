// A replacement owner decision is transferable only with its retained source. This module
// prepares a separate, stopped snapshot; it never generates media or approves a review.
import { createHash, randomUUID } from "node:crypto";
import { copyFileSync, createReadStream, existsSync, lstatSync, mkdirSync, openSync, closeSync, readdirSync, readFileSync, readSync, renameSync, rmSync } from "node:fs";
import path from "node:path";
import { isDeepStrictEqual, parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

import { locateFfmpeg, runTool } from "../assemble/ffmpeg.mjs";
import { assembledAudioProblems } from "../core/audio-evidence.mjs";
import { presentationTimeline, validateBranding } from "../core/branding.mjs";
import { buildCues, toSrt } from "../core/captions.mjs";
import { isCompilation } from "../core/compilation.mjs";
import { atomicWrite, isInside, readJson, ROOT, UsageError } from "../core/paths.mjs";
import { speechHash } from "../core/timeline.mjs";
import { eachLine } from "../core/schema.mjs";
import { captionTimelineOf, currentDub, dubsForUpload, localeTexts } from "../core/stages.mjs";
import { measureCut, measureProblems } from "../import/import.mjs";
import { checkPackage, listFiles, packageFiles } from "../package/check.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { renewedFinal } from "./renewal.mjs";

const HASH = /^[a-f0-9]{64}$/;
const UUID = /^[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}$/i;
const LOCALES = ["en", "ja", "ko", "zh-CN"];
const RECEIPT = "renewal-handoff.json";
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const requireThat = (ok, message) => { if (!ok) throw new UsageError(message); };
const save = (file, value) => atomicWrite(file, `${JSON.stringify(value, null, 2)}\n`);
const identity = (row) => ({ review_id: row.id, content_sha256: row.content_sha256 });
const latest = (remote, gate) => remote.reviews?.find((r) => r.gate === gate && !r.subject);
const normalizedChoices = (locales) => Object.fromEntries(LOCALES.map((locale) => {
  const v = locales?.[locale] ?? {};
  return [locale, { metadata: v.metadata === true, captions: v.captions === true || v.dub === true, dub: v.dub === true }];
}).filter(([, v]) => v.metadata || v.captions || v.dub));

// Activation immediately renames directories after hashing. Wait for the file handle's
// close, not merely stream end: an open Windows handle can otherwise interrupt rollback.
function sha256File(file) {
  return new Promise((resolve, reject) => {
    const hash = createHash("sha256"); let result;
    createReadStream(file).on("data", (chunk) => hash.update(chunk)).on("error", reject)
      .on("end", () => { result = hash.digest("hex"); }).on("close", () => { if (result) resolve(result); });
  });
}

function approved(remote, slug) {
  const final = renewedFinal(remote);
  requireThat(remote.slug === slug && final?.status === "approved" && UUID.test(final.id ?? "") && HASH.test(final.content_sha256 ?? "") && final.decided_at, "the current renewed final is not owner-approved for this slug");
  const candidate = final.payload.renewal_candidate;
  requireThat(candidate?.source?.final_review_id === final.payload._final_renewal.previous_review_id && candidate.source.final_sha256 === final.payload._final_renewal.previous_sha256 && HASH.test(candidate.source.body_sha256 ?? "") && candidate.candidate?.final_sha256 === final.content_sha256 && candidate.candidate.branding_hash === final.payload.branding_hash, "the approved final has no consistent original/body/branding source binding");
  return final;
}

function inactive(remote) {
  requireThat(!remote.youtube_video_id && !remote.youtube_sync && !remote.youtube_publish_at && !remote.youtube_upload_session && !remote.youtube_removed_at && !remote.dropped_at && !remote.shorts_line && remote.format !== "shorts", "upload, schedule, withdrawal or Shorts activity prevents handoff");
}

/** Reject links and special files: a snapshot must not retain mutable files outside itself. */
export async function fileInventory(directory, { exclude = [] } = {}) {
  const result = {};
  if (!existsSync(directory)) return result;
  const walk = async (at, prefix) => {
    requireThat(lstatSync(at).isDirectory() && !lstatSync(at).isSymbolicLink(), "snapshot directories cannot be symlinks");
    for (const name of readdirSync(at).sort()) {
      const relative = prefix ? `${prefix}/${name}` : name;
      if (exclude.includes(relative)) continue;
      const file = path.join(at, name), stat = lstatSync(file);
      requireThat(!stat.isSymbolicLink(), `snapshot symlink refused: ${relative}`);
      if (stat.isDirectory()) await walk(file, relative);
      else {
        requireThat(stat.isFile(), `snapshot special file refused: ${relative}`);
        result[relative] = { sha256: await sha256File(file), size: stat.size };
      }
    }
  };
  await walk(directory, "");
  return result;
}

async function copyVerified(source, target, expected) {
  requireThat(lstatSync(source).isFile() && !lstatSync(source).isSymbolicLink(), "a source attachment must be a regular file");
  requireThat(await sha256File(source) === expected, "source attachment SHA-256 differs");
  mkdirSync(path.dirname(target), { recursive: true });
  copyFileSync(source, target);
  requireThat(await sha256File(target) === expected && await sha256File(source) === expected, "attachment changed while copying");
}

/** Compare every encoded body picture and its timestamp; then decode the complete cut and
 * measure the re-encoded audio difference against its retained mix. No acceptance booleans
 * from an old candidate receipt substitute for this verification. */
export async function verifyRetainedMedia({ body, final, branding, bodyFrames, bodyStartFrames = 0, env = process.env, exec = runTool }) {
  const tools = await locateFfmpeg(env);
  const packets = async (file) => JSON.parse((await exec(tools.ffprobe, ["-v", "error", "-select_streams", "v:0", "-show_packets", "-show_entries", "packet=pts_time,data_hash", "-show_data_hash", "sha256", "-of", "json", file])).stdout).packets;
  const allOriginal = await packets(body), replacement = await packets(final);
  const startSeconds = bodyStartFrames / 30;
  const original = allOriginal?.filter((p) => Number(p.pts_time) >= startSeconds - 0.00001 && Number(p.pts_time) < startSeconds + bodyFrames / 30 - 0.00001);
  const offset = branding.intro.frames / 30;
  requireThat(original?.length === bodyFrames, "retained body packet count differs from its source timeline");
  const first = Number(original[0].pts_time);
  const selected = replacement.filter((p) => Number(p.pts_time) >= offset - 0.00001 && Number(p.pts_time) < offset + bodyFrames / 30 - 0.00001);
  requireThat(selected.length === original.length && original.every((p, i) => p.data_hash === selected[i].data_hash && Math.abs(Number(selected[i].pts_time) - (Number(p.pts_time) - first + offset)) < 0.0001), "the approved replacement does not preserve every retained body picture and timestamp");
  await exec(tools.ffmpeg, ["-v", "error", "-xerror", "-i", final, "-map", "0:v:0", "-map", "0:a:0", "-f", "null", "-"]);
  const seconds = bodyFrames / 30;
  // amix's negative weights do not invert samples; subtract channels explicitly after
  // merging, otherwise identical narration would incorrectly fail as a doubled signal.
  const { stderr } = await exec(tools.ffmpeg, ["-hide_banner", "-nostats", "-i", body, "-i", final, "-filter_complex", `[0:a]atrim=start=${startSeconds}:duration=${seconds},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[a];[1:a]atrim=start=${offset}:duration=${seconds},asetpts=PTS-STARTPTS,aformat=sample_rates=48000:channel_layouts=stereo[b];[a][b]amerge=inputs=2,pan=stereo|c0=c0-c2|c1=c1-c3,astats=metadata=0:reset=0`, "-t", String(seconds), "-vn", "-f", "null", "-"]);
  const values = [...stderr.matchAll(/RMS level dB:\s*(-?inf|[-\d.]+)/g)].map((m) => Number(m[1] === "-inf" ? -Infinity : m[1]));
  requireThat(values.length && values.every((v) => v <= -35), "replacement audio does not preserve the retained mix at the new intro offset");
  const measured = await measureCut(final, env), checked = measureProblems(measured.probe, measured.loudness);
  requireThat(!checked.problems.length && Math.abs(checked.seconds - (offset + seconds + branding.outro.frames / 30)) <= 0.1, `replacement media verification failed: ${checked.problems.join("; ") || "duration differs"}`);
  return { video_packets: original.length, packet_sha256: digest(JSON.stringify(original)), audio_difference_rms_db: values.map((v) => Number.isFinite(v) ? v : "-inf"), full_decode_ok: true, seconds: checked.seconds, loudness: measured.loudness };
}

/** Parse the complete SRT rather than shifting a guessed first/last timestamp. */
export function shiftSrt(bytes, offsetMs) {
  requireThat(Number.isSafeInteger(offsetMs), "caption offset must be integral milliseconds");
  const input = String(bytes).replace(/^\uFEFF/, "").replace(/\r\n/g, "\n").trim();
  const blocks = input.split(/\n\s*\n/);
  const clock = (value) => {
    const m = /^(\d{2,}):(\d{2}):(\d{2}),(\d{3})$/.exec(value);
    requireThat(m && +m[2] < 60 && +m[3] < 60, "invalid SRT timestamp");
    return +m[1] * 3600000 + +m[2] * 60000 + +m[3] * 1000 + +m[4];
  };
  const display = (ms) => `${String(Math.floor(ms / 3600000)).padStart(2, "0")}:${String(Math.floor(ms / 60000) % 60).padStart(2, "0")}:${String(Math.floor(ms / 1000) % 60).padStart(2, "0")},${String(ms % 1000).padStart(3, "0")}`;
  let last = -1;
  return `${blocks.map((block, i) => {
    const lines = block.split("\n"), times = /^(\S+) --> (\S+)$/.exec(lines[1] ?? "");
    requireThat(/^\d+$/.test(lines[0]) && +lines[0] === i + 1 && times && lines.slice(2).join("\n").trim(), "invalid or empty SRT cue");
    const start = clock(times[1]) + offsetMs, end = clock(times[2]) + offsetMs;
    requireThat(start >= 0 && start >= last && end > start, "caption shift produced invalid timing");
    last = start;
    return `${i + 1}\n${display(start)} --> ${display(end)}\n${lines.slice(2).join("\n")}`;
  }).join("\n\n")}\n`;
}

function validateRealAdapter(adapter, caption, branding, bodyFrames) {
  requireThat(adapter?.project?.doc && adapter.timeline?.speech_hash === speechHash(adapter.project.doc, adapter.project.lexicon) && adapter.timeline.total_frames === bodyFrames, "retained language adapter script/body timing is missing or stale");
  const lines = [...eachLine(adapter.project.doc)].map(({ line }) => line);
  const cues = shiftSrt(caption, 0).trim().split(/\n\s*\n/).map((block) => block.split("\n"));
  const texts = localeTexts(adapter.project.doc, adapter.project.translations ?? {}).texts["zh-TW"];
  const presented = presentationTimeline(adapter.timeline, { hash: branding.hash, intro_frames: branding.intro.frames, outro_frames: branding.outro.frames, body_frames: bodyFrames });
  if (toSrt(buildCues(presented, texts, "zh-TW").cues) === shiftSrt(caption, 0)) return;
  // The imported season adapter has one real source timing unit per caption. Its 30-fps
  // quantization may differ from the original SRT by at most one frame; text stays exact.
  const clock = (s) => { const m = /^(\d+):(\d{2}):(\d{2}),(\d{3})$/.exec(s); return (+m[1] * 3600 + +m[2] * 60 + +m[3] + +m[4] / 1000) * 30; };
  requireThat(cues.length === lines.length && cues.length === adapter.timeline.lines.length, "retained adapter does not map to the actual imported subtitle units");
  for (const [i, cue] of cues.entries()) {
    const times = cue[1].split(" --> "), timed = adapter.timeline.lines[i];
    const normalize = (v) => v.normalize("NFC").replace(/\s+/gu, "");
    requireThat(timed.id === lines[i].id && normalize(cue.slice(2).join("\n")) === normalize(lines[i].text) && Math.abs(clock(times[0]) - (timed.start_frame + branding.intro.frames)) <= 1.03 && Math.abs(clock(times[1]) - (timed.end_frame + branding.intro.frames)) <= 1.03, "retained adapter text/timing differs from the actual approved subtitle source");
  }
}

/** Only source reviews retained by this owner renewal can authorize imported artifacts. */
function retainedAttachment(remote, final, binding, role) {
  const ids = new Set([final.payload._final_renewal.previous_review_id, ...(final.payload._final_renewal.retained_review_ids ?? [])]);
  const row = remote.reviews?.find((v) => v.id === binding?.review_id);
  const file = row?.files?.find((v) => v.role === role && v.sha256 === binding.sha256);
  requireThat(ids.has(row?.id) && ["approved", "superseded"].includes(row?.status) && file && HASH.test(binding.sha256), `missing retained source review for ${role}`);
  return file;
}

function retainedMetadata(remote, final, binding) {
  if (binding?.kind !== "final-payload") return null;
  const row = remote.reviews?.find((v) => v.id === binding.review_id);
  requireThat(row?.id === final.payload._final_renewal.previous_review_id && row.gate === "final" && row.status === "superseded", "manual text must come from the renewal's original decided final");
  const fields = row.payload?.metadata?.["zh-TW"];
  requireThat(fields?.title?.trim() && fields?.description?.trim(), "the original final has no approved metadata text");
  return { ...fields, default_language: "zh-TW", chapters: (row.payload.chapters ?? []).map((c) => ({ ...c, time: c.time ?? c.at })), localizations: {}, source_final_payload_sha256: digest(JSON.stringify({ metadata: row.payload.metadata, chapters: row.payload.chapters ?? [] })) };
}

/** Imported cuts use their actual approved text/caption attachments, never a fabricated TTS
 * or scene timeline. Missing chosen translations/dubs remain explicit holds. */
export async function prepareManualPackage({ workdir, remote, final, source, offsetMs }) {
  const upload = path.join(workdir, "upload");
  requireThat(!existsSync(upload), "manual package must be prepared in a fresh upload directory");
  const choices = normalizedChoices(remote.locales);
  let old = retainedMetadata(remote, final, source.metadata);
  if (!old) {
    retainedAttachment(remote, final, source.metadata, "metadata");
    requireThat(await sha256File(source.metadata.file) === source.metadata.sha256, "original metadata bytes changed");
    old = readJson(source.metadata.file);
  }
  const narration = old.default_language ?? "zh-TW";
  requireThat(narration === "zh-TW" && typeof old.title === "string" && old.title.trim() && typeof old.description === "string" && old.description.trim(), "manual source requires approved zh-TW title and description");
  const oldChapters = old.chapters ?? [];
  const seconds = (clock) => { const p = String(clock).split(":").map(Number); requireThat(p.length >= 2 && p.length <= 3 && p.every((v) => Number.isInteger(v) && v >= 0), "invalid source chapter clock"); return p.reduce((n, v) => n * 60 + v, 0); };
  const clock = (s) => s >= 3600 ? `${String(Math.floor(s / 3600)).padStart(2, "0")}:${String(Math.floor(s / 60) % 60).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}` : `${String(Math.floor(s / 60)).padStart(2, "0")}:${String(s % 60).padStart(2, "0")}`;
  requireThat(offsetMs % 1000 === 0, "chapter offsets require whole seconds");
  const chapters = oldChapters.map((entry, i) => ({ ...entry, time: clock(i === 0 ? 0 : seconds(entry.time ?? entry.at) + offsetMs / 1000) }));
  const updateDescription = (text) => { let out = text; for (let i = oldChapters.length - 1; i >= 1; i--) { const time = oldChapters[i].time ?? oldChapters[i].at; const pattern = new RegExp(`^${time} (.+)$`, "m"); requireThat(pattern.test(out), "source description does not contain its approved chapter timestamps"); out = out.replace(pattern, `${chapters[i].time} $1`); } return out; };
  const captionProofs = {}, holds = [], localizations = {};
  mkdirSync(path.join(upload, "captions"), { recursive: true });
  for (const locale of ["zh-TW", ...Object.keys(choices)]) {
    const choice = locale === "zh-TW" ? { metadata: true, captions: true, dub: false } : choices[locale];
    if (choice.dub) holds.push(`${locale}: renewed dub requires its own retained mix and branding proof`);
    if (choice.metadata && locale !== "zh-TW") {
      const translated = old.localizations?.[locale];
      if (translated?.title?.trim() && translated?.description?.trim()) localizations[locale] = { ...translated, description: updateDescription(translated.description) };
      else holds.push(`${locale}: retained translated metadata is missing`);
    }
    if (choice.captions) {
      const binding = source.captions?.[locale];
      if (!binding) { holds.push(`${locale}: retained caption attachment is missing`); continue; }
      retainedAttachment(remote, final, binding, `captions_${locale}`);
      requireThat(await sha256File(binding.file) === binding.sha256, `${locale}: original captions changed`);
      const shifted = shiftSrt(readFileSync(binding.file, "utf8"), offsetMs);
      atomicWrite(path.join(upload, "captions", `${locale}.srt`), shifted);
      captionProofs[locale] = { review_id: binding.review_id, source_sha256: binding.sha256, offset_ms: offsetMs, sha256: digest(shifted) };
      if (locale === "zh-TW") requireThat(final.files.some((f) => f.role === "captions_zh-TW" && f.sha256 === digest(shifted)), "shifted default captions differ from the owner-approved replacement attachment");
    }
  }
  requireThat(captionProofs["zh-TW"], "the original zh-TW captions are required");
  retainedAttachment(remote, final, source.thumbnail, "thumbnail");
  await copyVerified(source.thumbnail.file, path.join(upload, "thumbnail.jpg"), source.thumbnail.sha256);
  requireThat(lstatSync(path.join(upload, "thumbnail.jpg")).size <= 2 * 1024 * 1024, "original thumbnail exceeds YouTube limit");
  await copyVerified(path.join(workdir, "final.mp4"), path.join(upload, "final.mp4"), final.content_sha256);
  const metadata = { ...old, title: old.title, description: updateDescription(old.description), default_language: narration, localizations, chapters, final_sha256: final.content_sha256, branding_hash: final.payload.branding_hash, final_review_id: final.id, language_choice: choices, thumbnail: "thumbnail.jpg", captions: Object.keys(captionProofs).map((locale) => `captions/${locale}.srt`), dubs: [], skipped_dub_locales: {}, skipped_caption_locales: {}, ...(source.disclosure ? { contains_synthetic_media: source.disclosure.synthetic, disclosure_reason: source.disclosure.reason } : {}), renewal_handoff: { schema_version: 1, kind: "manual-import", source_metadata: { review_id: source.metadata.review_id, sha256: source.metadata.sha256 ?? old.source_final_payload_sha256, kind: source.metadata.kind ?? "attachment" }, captions: captionProofs, holds } };
  requireThat(typeof metadata.contains_synthetic_media === "boolean" && metadata.disclosure_reason?.trim(), "the original package has no explicit disclosure answer");
  save(path.join(upload, "metadata.json"), metadata);
  for (const [locale, fields] of Object.entries({ "zh-TW": metadata, ...localizations })) atomicWrite(path.join(upload, `description.${locale}.txt`), `${fields.title}\n\n${fields.description}\n`);
  return { metadata, holds };
}

/** Preparation is safe while a worker runs: it reads sources, writes only NEW snapshot/out
 * paths, and will refuse activation if any canonical source changed meanwhile. */
export async function prepareHandoff({ slug, canonical, out, source, candidate, branding, remote, mode = "normal", project, verifyMedia = verifyRetainedMedia, now = new Date() }) {
  requireThat(/^[a-z0-9][a-z0-9-]{0,79}$/.test(slug), "invalid handoff slug");
  canonical = path.resolve(canonical); out = path.resolve(out);
  requireThat(!isInside(canonical, ROOT) && !isInside(ROOT, canonical) && canonical !== path.parse(canonical).root, "canonical media must be outside the repository and cannot be a filesystem root");
  requireThat(!existsSync(out) && path.dirname(out) === path.dirname(canonical) && !isInside(out, canonical) && !isInside(canonical, out), "prepare needs a new sibling directory on the canonical filesystem");
  requireThat(["normal", "manual-import"].includes(mode), "unknown handoff mode");
  const final = approved(remote, slug); inactive(remote);
  const pin = validateBranding(readJson(branding), { base: path.dirname(path.resolve(branding)) });
  requireThat(pin.hash === final.payload.branding_hash, "selected branding differs from the owner-approved final");
  const bound = final.payload.renewal_candidate.source;
  const rangeSource = mode === "manual-import" && source.body_from_original === true;
  requireThat(await sha256File(source.original) === bound.final_sha256 && (rangeSource || await sha256File(source.body) === bound.body_sha256) && await sha256File(candidate) === final.content_sha256, "original, retained body or candidate differs from the owner-approved source binding");
  const canonicalBefore = await fileInventory(canonical);
  const retained = mode === "normal" ? await fileInventory(source.workdir) : {};
  const bodyFrames = mode === "normal" ? readJson(path.join(source.workdir, "timeline.json")).total_frames : source.body_frames;
  requireThat(Number.isSafeInteger(bodyFrames) && bodyFrames > 0, "missing retained body frame proof");
  const bodyStartFrames = rangeSource ? source.old_intro_frames : 0;
  requireThat(Number.isSafeInteger(bodyStartFrames) && bodyStartFrames >= 0 && bodyStartFrames <= 900, "an original-cut body range needs its verified old intro frame count");
  requireThat(!rangeSource || source.old_intro_ms === bodyStartFrames * 1000 / 30, "caption source offset does not match the original-cut body range");
  if (mode === "normal") {
    requireThat(project?.doc?.slug === slug && !isCompilation(project.doc), "renewed compilations require an episode-source handoff; keep this project held");
    const timeline = readJson(path.join(source.workdir, "timeline.json")), checks = readJson(path.join(source.workdir, "checks.json"));
    const { checksCurrent } = await import("../package/cli.mjs");
    requireThat(timeline.speech_hash === speechHash(project.doc, project.lexicon) && checksCurrent(project.doc, project.lexicon, checks, readJson(path.join(source.workdir, "clips/manifest.json"), null), readJson(path.join(source.workdir, "keyframes/manifest.json"), null)) && !assembledAudioProblems(timeline, checks, source.workdir).length, "source script, pictures or actual narration differs from its original successful checks");
    requireThat(checks.branding ? checks.branding.body_sha256 === bound.body_sha256 && checks.branding.body_frames === bodyFrames : await sha256File(path.join(source.workdir, "final.mp4")) === bound.body_sha256, "the retained body does not match the original source checks");
  }
  for (const role of ["intro", "outro"]) requireThat(await sha256File(pin[role].file) === pin[role].sha256, `${role} branding asset changed`);
  const bodyFile = rangeSource ? source.original : source.body;
  const media = await verifyMedia({ body: bodyFile, final: candidate, branding: pin, bodyFrames, bodyStartFrames });
  requireThat(media.full_decode_ok === true && media.video_packets === bodyFrames, "replacement media proof is incomplete");
  mkdirSync(out);
  try {
    for (const [name, proof] of Object.entries(retained)) await copyVerified(path.join(source.workdir, name), path.join(out, name), proof.sha256);
    // Old packages/captions stay archived in retained-source, never masquerade as renewed.
    for (const name of ["upload", "captions", "dubs", "review/languages.json"]) if (existsSync(path.join(out, name))) {
      const target = path.join(out, "retained-source", name); mkdirSync(path.dirname(target), { recursive: true }); renameSync(path.join(out, name), target);
    }
    for (const name of ["checks.json", "branding.json", "approvals.json"]) if (existsSync(path.join(out, name))) await copyVerified(path.join(out, name), path.join(out, "retained-source", name), await sha256File(path.join(out, name)));
    await copyVerified(candidate, path.join(out, "final.mp4"), final.content_sha256);
    await copyVerified(source.original, path.join(out, "retained-source/original-final.mp4"), bound.final_sha256);
    const bodyPath = rangeSource ? "retained-source/body-original-cut.mp4" : "build/body.mp4";
    const actualBodySha = rangeSource ? bound.final_sha256 : bound.body_sha256;
    await copyVerified(bodyFile, path.join(out, bodyPath), actualBodySha);
    const internalPin = { ...pin };
    for (const role of ["intro", "outro"]) { const name = `build/branding-assets/${role}.mp4`; await copyVerified(pin[role].file, path.join(out, name), pin[role].sha256); internalPin[role] = { ...pin[role], file: name }; }
    save(path.join(out, "branding.json"), internalPin);
    atomicWrite(path.join(out, "STOP"), "Owner-approved renewal handoff; remain held until source, package and language readback are verified.\n");
    save(path.join(out, "languages.json"), { locales: normalizedChoices(remote.locales), decided_at: remote.locales_decided_at });
    let manual = null;
    if (mode === "normal") {
      const checks = readJson(path.join(source.workdir, "checks.json"));
      save(path.join(out, "checks.json"), { ...checks, metrics: { ...checks.metrics, frames: bodyFrames + pin.intro.frames + pin.outro.frames, loudness: media.loudness }, branding: { hash: pin.hash, id: pin.id, intro_frames: pin.intro.frames, outro_frames: pin.outro.frames, body_frames: bodyFrames, body_file: "build/body.mp4", body_sha256: bound.body_sha256 }, renewal_media: media });
    } else {
      requireThat(!existsSync(path.join(out, "timeline.json")), "manual imports must not invent a narration timeline");
      manual = await prepareManualPackage({ workdir: out, remote, final, source: source.package, offsetMs: pin.intro.frames * 1000 / 30 - (source.old_intro_ms ?? 0) });
      let adapter = null;
      if (source.adapter) {
        validateRealAdapter(source.adapter, readFileSync(path.join(out, "upload/captions/zh-TW.srt"), "utf8"), pin, bodyFrames);
        save(path.join(out, "language-adapter/project.json"), source.adapter.project);
        save(path.join(out, "language-adapter/timeline.json"), source.adapter.timeline);
        adapter = { project_file: "language-adapter/project.json", project_sha256: await sha256File(path.join(out, "language-adapter/project.json")), timeline_file: "language-adapter/timeline.json", timeline_sha256: await sha256File(path.join(out, "language-adapter/timeline.json")), doc_sha256: digest(JSON.stringify(source.adapter.project.doc)), lexicon_sha256: digest(JSON.stringify(source.adapter.project.lexicon)), speech_hash: source.adapter.timeline.speech_hash, original_narration_claimed: false };
      }
      save(path.join(out, "renewal-language-source.json"), { schema_version: 1, kind: "renewed-import-language-source", slug, source: { final: identity(final), original_final: { review_id: bound.final_review_id, content_sha256: bound.final_sha256 }, branding_hash: pin.hash, body: { kind: rangeSource ? "original-cut-range" : "retained-body-file", sha256: actualBodySha, file: bodyPath, start_frame: bodyStartFrames, frames: bodyFrames }, media }, choice: { locales: normalizedChoices(remote.locales), decided_at: remote.locales_decided_at }, metadata: { file: "upload/metadata.json", sha256: await sha256File(path.join(out, "upload/metadata.json")) }, captions_zh_TW: { file: "upload/captions/zh-TW.srt", sha256: await sha256File(path.join(out, "upload/captions/zh-TW.srt")), original: manual.metadata.renewal_handoff.captions["zh-TW"] }, adapter, holds: manual.holds, adapter_requirement: "Only a retained real script/body timing adapter may translate or fit dubs; this contract does not fabricate narration/TTS evidence." });
    }
    const receipt = { schema_version: 1, kind: "renewal-handoff", id: randomUUID(), slug, mode, prepared_at: now.toISOString(), canonical, snapshot: out, archive: `${canonical}.renewal-archive-${randomUUID()}`, owner_final: { ...identity(final), branding_hash: pin.hash, decided_at: final.decided_at }, source: { ...bound, body_frames: bodyFrames, ...(mode === "normal" ? { project: { doc_sha256: digest(JSON.stringify(project.doc)), lexicon_sha256: digest(JSON.stringify(project.lexicon)) } } : {}), body_proof: { kind: rangeSource ? "original-cut-range" : "retained-body-file", file: bodyPath, sha256: actualBodySha, start_frame: bodyStartFrames, frames: bodyFrames, ...(rangeSource ? { candidate_body_container_unavailable: true } : {}) }, canonical_files: canonicalBefore, retained_files: retained }, choice: { locales: normalizedChoices(remote.locales), decided_at: remote.locales_decided_at }, media, holds: manual?.holds ?? [], files: await fileInventory(out, { exclude: [RECEIPT, "STOP"] }) };
    save(path.join(out, RECEIPT), receipt);
    requireThat(isDeepStrictEqual(canonicalBefore, await fileInventory(canonical)) && (mode !== "normal" || isDeepStrictEqual(retained, await fileInventory(source.workdir))), "source changed while preparing; preserve the snapshot and prepare afresh");
    return receipt;
  } catch (error) { atomicWrite(path.join(out, "STOP"), `Failed renewal preparation: ${error.message}\n`); throw error; }
}

export async function verifyHandoff({ receipt, workdir = receipt.snapshot, remote, project, verifyCanonical = true }) {
  requireThat(receipt?.schema_version === 1 && receipt.kind === "renewal-handoff" && UUID.test(receipt.id ?? "") && ["normal", "manual-import"].includes(receipt.mode), "invalid handoff receipt");
  const final = approved(remote, receipt.slug); inactive(remote);
  requireThat(path.dirname(receipt.canonical) === path.dirname(receipt.snapshot) && path.dirname(receipt.archive) === path.dirname(receipt.canonical) && new Set([receipt.canonical, receipt.snapshot, receipt.archive]).size === 3 && !isInside(receipt.canonical, ROOT) && !isInside(ROOT, receipt.canonical), "handoff paths must be distinct siblings outside the repository");
  const bound = final.payload.renewal_candidate.source;
  requireThat(receipt.source.final_review_id === bound.final_review_id && receipt.source.final_sha256 === bound.final_sha256 && receipt.source.body_sha256 === bound.body_sha256 && receipt.source.body_proof?.frames === receipt.source.body_frames && receipt.media.full_decode_ok === true && receipt.media.video_packets === receipt.source.body_frames, "handoff source identity or media proof differs from the approved renewal");
  const bodyProof = receipt.source.body_proof;
  requireThat(bodyProof.kind === "retained-body-file" && bodyProof.sha256 === bound.body_sha256 && bodyProof.file === "build/body.mp4" && bodyProof.start_frame === 0 || receipt.mode === "manual-import" && bodyProof.kind === "original-cut-range" && bodyProof.sha256 === bound.final_sha256 && bodyProof.file === "retained-source/body-original-cut.mp4" && bodyProof.candidate_body_container_unavailable === true && Number.isSafeInteger(bodyProof.start_frame) && bodyProof.start_frame >= 0, "invalid retained-body file/range proof");
  requireThat(isDeepStrictEqual(receipt.owner_final, { ...identity(final), branding_hash: final.payload.branding_hash, decided_at: final.decided_at }) && isDeepStrictEqual(receipt.choice, { locales: normalizedChoices(remote.locales), decided_at: remote.locales_decided_at }), "owner final approval or language choice changed; keep both snapshots held");
  if (receipt.mode === "normal") requireThat(project && isDeepStrictEqual(receipt.source.project, { doc_sha256: digest(JSON.stringify(project.doc)), lexicon_sha256: digest(JSON.stringify(project.lexicon)) }), "source document or lexicon changed since prepare; keep the worker held");
  requireThat(isDeepStrictEqual(receipt.files, await fileInventory(workdir, { exclude: [RECEIPT, "STOP"] })), "prepared snapshot bytes changed; keep both snapshots held");
  requireThat(receipt.files["final.mp4"]?.sha256 === final.content_sha256 && receipt.files[receipt.source.body_proof?.file]?.sha256 === receipt.source.body_proof?.sha256 && existsSync(path.join(workdir, "STOP")), "snapshot is not the stopped approved final and retained body");
  if (verifyCanonical) requireThat(isDeepStrictEqual(receipt.source.canonical_files, await fileInventory(receipt.canonical)), "canonical source changed since prepare; keep the worker held");
  return receipt;
}

/** Caller must independently stop/drain the worker and all media jobs. A STOP file alone
 * does not prove a process has left its current unit. Both checks repeat after hashing. */
export async function activateHandoff({ receipt, readRemote, readProject, workerIdle, rename = renameSync, now = () => new Date() }) {
  requireThat(typeof readRemote === "function" && typeof workerIdle === "function", "activation requires fresh owner-state and stopped/idle worker probes");
  requireThat(receipt.mode !== "normal" || typeof readProject === "function", "normal activation requires a fresh source document/lexicon probe");
  const guard = async () => {
    const probe = await workerIdle(receipt.slug);
    requireThat(probe?.stopped === true && probe.idle === true && probe.active_jobs === 0, "worker or media jobs are still active; no activation");
    requireThat(probe.upload_inactive === true, "a fresh upload-session/job inactivity probe is required for activation");
    requireThat(existsSync(path.join(path.dirname(receipt.canonical), "STOP")), "activation requires the global worker STOP file");
    return readRemote(receipt.slug);
  };
  const journal = `${receipt.canonical}.handoff-${receipt.id}.json`, lock = `${receipt.canonical}.handoff.lock`;
  requireThat(!existsSync(journal) && !existsSync(receipt.archive), "activation already attempted; inspect its journal and both snapshots before recovery");
  let fd;
  try { fd = openSync(lock, "wx"); } catch { throw new UsageError("another handoff holds the activation lock"); }
  closeSync(fd);
  let archived = false, promoted = false;
  const state = (phase, extra = {}) => save(journal, { schema_version: 1, handoff_id: receipt.id, slug: receipt.slug, phase, at: now().toISOString(), canonical: receipt.canonical, snapshot: receipt.snapshot, archive: receipt.archive, ...extra });
  try {
    await verifyHandoff({ receipt, remote: await guard(), project: await readProject?.(receipt.slug) });
    // The expensive hash pass may outlive a decision: fetch owner and idle state again.
    await verifyHandoff({ receipt, remote: await guard(), project: await readProject?.(receipt.slug) });
    state("prepared");
    if (existsSync(receipt.canonical)) { state("archiving"); rename(receipt.canonical, receipt.archive); archived = true; }
    state("promoting"); rename(receipt.snapshot, receipt.canonical); promoted = true;
    await verifyHandoff({ receipt, workdir: receipt.canonical, remote: await guard(), project: await readProject?.(receipt.slug), verifyCanonical: false });
    state("activated-held", { final_sha256: receipt.owner_final.content_sha256 });
    return { ...receipt, activation: readJson(journal) };
  } catch (error) {
    // No source is deleted. If rollback is interrupted the journal keeps every exact path.
    try {
      if (promoted) { state("rolling-back-candidate"); rename(receipt.canonical, receipt.snapshot); promoted = false; }
      if (archived) { state("rolling-back-original"); rename(receipt.archive, receipt.canonical); archived = false; }
      state("failed-held", { error: error.message });
    } catch (rollback) { state("recovery-required", { error: error.message, rollback_error: rollback.message }); }
    throw error;
  } finally { rmSync(lock, { force: true }); }
}

/** A prepared manual package can be staged using existing attachment transport. This is a
 * publish proof, never a new final approval; unresolved chosen parts forbid submission. */
export async function bindManualSubmission({ body, remote, workdir }) {
  const receipt = readJson(path.join(workdir, RECEIPT), null);
  if (receipt?.mode !== "manual-import") return null;
  requireThat(body.gate === "publish", "manual language output requires bindManualLanguageSubmission with the real timed adapter");
  const final = approved(remote, receipt.slug); inactive(remote);
  requireThat((body.payload?.base_only === true || !receipt.holds.length) && isDeepStrictEqual(receipt.choice, { locales: normalizedChoices(remote.locales), decided_at: remote.locales_decided_at }), `manual package remains held: ${receipt.holds.join("; ") || "language choice changed"}`);
  const metadataFile = path.join(workdir, "upload/metadata.json"), metadata = readJson(metadataFile);
  requireThat(metadata.final_review_id === final.id && metadata.final_sha256 === final.content_sha256 && metadata.branding_hash === final.payload.branding_hash && body.content_sha256 === await sha256File(metadataFile), "manual package final, branding or metadata proof changed");
  for (const entry of packageFiles(Object.keys(receipt.files).filter((f) => f.startsWith("upload/")).map((f) => f.slice(7)))) {
    const file = path.join(workdir, "upload", entry.path), proof = receipt.files[`upload/${entry.path}`];
    requireThat(await sha256File(file) === proof.sha256 && body.files.some((f) => f.role === entry.role && f.sha256 === proof.sha256 && f.size === proof.size), `manual package attachment changed: ${entry.role}`);
  }
  const wanted = normalizedChoices(remote.locales);
  const report = checkPackage({ files: listFiles(path.join(workdir, "upload")), metadata, finalSha256: await sha256File(path.join(workdir, "upload/final.mp4")), approvedSha256: final.content_sha256, metadataSha256: body.content_sha256, locales: body.payload?.base_only === true ? metadata.captions.map((v) => path.basename(v, ".srt")) : ["zh-TW", ...Object.keys(wanted).filter((l) => wanted[l].captions)], descriptionLocales: body.payload?.base_only === true ? ["zh-TW", ...Object.keys(metadata.localizations)] : ["zh-TW", ...Object.keys(wanted).filter((l) => wanted[l].metadata)], brandingMatches: validateBranding(readJson(path.join(workdir, "branding.json")), { base: workdir }).hash === final.payload.branding_hash });
  requireThat(report.ok && isDeepStrictEqual(body.payload?.package, report), "manual package check is not successful or changed");
  return { ...body, payload: { ...body.payload, final_review_id: final.id, renewal_handoff_id: receipt.id, manual_source: metadata.renewal_handoff } };
}

/** A source-only import can be translated after its final approval without pretending it
 * has a standard TTS history. Fitting dubs still requires a real retained timing adapter. */
export async function readManualLanguageSource({ workdir, remote }) {
  const contractFile = path.join(workdir, "renewal-language-source.json"), source = readJson(contractFile, null), receipt = readJson(path.join(workdir, RECEIPT), null);
  requireThat(source?.schema_version === 1 && source.kind === "renewed-import-language-source", "renewed imported languages have no source-bound handoff contract");
  requireThat(receipt?.kind === "renewal-handoff" && receipt.mode === "manual-import" && receipt.slug === source.slug && receipt.files?.["renewal-language-source.json"]?.sha256 === await sha256File(contractFile), "renewed language source contract differs from its prepared handoff receipt");
  const final = approved(remote, source.slug);
  requireThat(isDeepStrictEqual(source.source.final, identity(final)) && source.source.branding_hash === final.payload.branding_hash && isDeepStrictEqual(source.choice, { locales: normalizedChoices(remote.locales), decided_at: remote.locales_decided_at }), "imported language source final, branding or owner choice changed");
  requireThat(isDeepStrictEqual(receipt.owner_final, { ...identity(final), branding_hash: final.payload.branding_hash, decided_at: final.decided_at }) && await sha256File(path.join(workdir, "final.mp4")) === final.content_sha256, "imported language handoff owner decision or final bytes changed");
  const bound = final.payload.renewal_candidate.source;
  requireThat(source.source.original_final.review_id === bound.final_review_id && source.source.original_final.content_sha256 === bound.final_sha256 && source.source.media.full_decode_ok === true && source.source.media.video_packets === source.source.body.frames, "imported language retained body proof is inconsistent with the approved final");
  const body = path.resolve(workdir, source.source.body.file);
  requireThat(isInside(body, workdir) && await sha256File(body) === source.source.body.sha256 && (source.source.body.kind === "retained-body-file" ? source.source.body.sha256 === bound.body_sha256 : source.source.body.kind === "original-cut-range" && source.source.body.sha256 === bound.final_sha256), "imported language retained body bytes changed");
  for (const item of [source.metadata, source.captions_zh_TW]) {
    const file = path.resolve(workdir, item.file);
    requireThat(isInside(file, workdir) && await sha256File(file) === item.sha256, "renewed imported metadata/default caption source changed");
  }
  requireThat(final.files.some((v) => v.role === "captions_zh-TW" && v.sha256 === source.captions_zh_TW.sha256), "imported language default captions differ from the owner-approved final attachment");
  const pin = validateBranding(readJson(path.join(workdir, "branding.json")), { base: workdir });
  requireThat(pin.hash === source.source.branding_hash, "imported language branding pin changed");
  for (const role of ["intro", "outro"]) requireThat(await sha256File(pin[role].file) === pin[role].sha256, `imported language ${role} asset changed`);
  if (source.adapter) {
    const files = ["project", "timeline"];
    for (const key of files) {
      const file = path.resolve(workdir, source.adapter[`${key}_file`]);
      requireThat(isInside(file, workdir) && await sha256File(file) === source.adapter[`${key}_sha256`] && receipt.files[source.adapter[`${key}_file`]]?.sha256 === source.adapter[`${key}_sha256`], "retained language adapter differs from the prepared source receipt");
    }
    const project = readJson(path.join(workdir, source.adapter.project_file)), timeline = readJson(path.join(workdir, source.adapter.timeline_file));
    requireThat(digest(JSON.stringify(project.doc)) === source.adapter.doc_sha256 && digest(JSON.stringify(project.lexicon)) === source.adapter.lexicon_sha256, "retained language adapter script/lexicon hash changed");
    validateRealAdapter({ project, timeline }, readFileSync(path.join(workdir, source.captions_zh_TW.file), "utf8"), pin, source.source.body.frames);
  }
  return source;
}

/** Local native stages remain synchronous. Resolve a genuine imported presentation from
 * pinned artifacts and the pulled owner final, without fabricating assemble/TTS checks. The
 * isolated runner additionally rechecks current remote identity immediately before commands. */
export function verifiedManualPresentation({ project, workdir, timeline }) {
  const contractFile = path.join(workdir, "renewal-language-source.json");
  if (!existsSync(contractFile)) return null;
  const sha = (relative) => {
    const file = path.resolve(workdir, relative);
    requireThat(isInside(file, workdir) && lstatSync(file).isFile() && !lstatSync(file).isSymbolicLink(), "manual presentation source is not a regular local file");
    const fd = openSync(file, "r"), hash = createHash("sha256"), buffer = Buffer.alloc(1024 * 1024);
    try { let size; while ((size = readSync(fd, buffer, 0, buffer.length, null)) > 0) hash.update(buffer.subarray(0, size)); }
    finally { closeSync(fd); }
    return hash.digest("hex");
  };
  const source = readJson(contractFile), receipt = readJson(path.join(workdir, RECEIPT)), pin = validateBranding(readJson(path.join(workdir, "branding.json")), { base: workdir });
  requireThat(source?.kind === "renewed-import-language-source" && receipt?.mode === "manual-import" && receipt.slug === project.doc.slug && source.slug === project.doc.slug && receipt.files?.["renewal-language-source.json"]?.sha256 === sha("renewal-language-source.json"), "manual presentation contract differs from its prepared source receipt");
  requireThat(isDeepStrictEqual(source.source.final, { review_id: receipt.owner_final.review_id, content_sha256: receipt.owner_final.content_sha256 }) && source.source.branding_hash === receipt.owner_final.branding_hash && pin.hash === source.source.branding_hash, "manual presentation owner final or branding changed");
  const approval = readJson(path.join(workdir, "approvals.json"), { approvals: [] }).approvals.filter((v) => v.gate === "final").at(-1);
  requireThat(approval?.sha256 === source.source.final.content_sha256 && sha("final.mp4") === source.source.final.content_sha256, "manual presentation needs the exact pulled owner final approval");
  const body = source.source.body, proof = receipt.source.body_proof;
  requireThat(isDeepStrictEqual(body, { kind: proof.kind, sha256: proof.sha256, file: proof.file, start_frame: proof.start_frame, frames: proof.frames }) && source.source.media.full_decode_ok === true && source.source.media.video_packets === body.frames && sha(body.file) === body.sha256, "manual presentation retained original body proof changed");
  requireThat(source.adapter && digest(JSON.stringify(project.doc)) === source.adapter.doc_sha256 && digest(JSON.stringify(project.lexicon)) === source.adapter.lexicon_sha256 && sha("timeline.json") === source.adapter.timeline_sha256, "manual presentation has no current real script/body timing adapter");
  for (const key of ["project", "timeline"]) requireThat(receipt.files[source.adapter[`${key}_file`]]?.sha256 === source.adapter[`${key}_sha256`] && sha(source.adapter[`${key}_file`]) === source.adapter[`${key}_sha256`], "manual presentation adapter differs from the prepared source receipt");
  requireThat(sha(source.captions_zh_TW.file) === source.captions_zh_TW.sha256 && receipt.files[source.captions_zh_TW.file]?.sha256 === source.captions_zh_TW.sha256, "manual presentation approved default caption bytes changed");
  for (const key of ["intro", "outro"]) requireThat(sha(pin[key].file) === pin[key].sha256, `manual presentation ${key} asset changed`);
  validateRealAdapter({ project, timeline }, readFileSync(path.join(workdir, source.captions_zh_TW.file), "utf8"), pin, body.frames);
  return { hash: pin.hash, id: pin.id, intro_frames: pin.intro.frames, outro_frames: pin.outro.frames, body_frames: body.frames, source_kind: "renewed-import-language-source", final_sha256: source.source.final.content_sha256 };
}

/** Forward cumulative READY parts only after verifying their real adapter/text/timing. The
 * pending source holds describe unfinished parts, not a prohibition on future valid output. */
export async function bindManualLanguageSubmission({ body, remote, workdir, project, request, upload }) {
  requireThat(["languages", "dubs"].includes(body.gate), "not a language submission");
  const contract = await readManualLanguageSource({ workdir, remote });
  const final = approved(remote, contract.slug), publish = latest(remote, "publish");
  requireThat(publish?.status === "approved" && publish.payload?.final_review_id === final.id && publish.content_sha256 === contract.metadata.sha256, "the exact renewed base publish metadata version must be approved before submitting its languages");
  requireThat(project?.doc?.slug === contract.slug && !isCompilation(project.doc), "a real retained script/timing adapter is required for language output; source contract stays preserved");
  const timeline = readJson(path.join(workdir, "timeline.json"), null), pin = validateBranding(readJson(path.join(workdir, "branding.json")), { base: workdir });
  requireThat(timeline && timeline.speech_hash === speechHash(project.doc, project.lexicon) && timeline.total_frames === contract.source.body.frames, "imported timed adapter differs from the retained body source");
  requireThat(contract.adapter && digest(JSON.stringify(project.doc)) === contract.adapter.doc_sha256 && digest(JSON.stringify(project.lexicon)) === contract.adapter.lexicon_sha256 && await sha256File(path.join(workdir, "timeline.json")) === contract.adapter.timeline_sha256, "language output has no verified real adapter from the approved subtitle source");
  const presented = presentationTimeline(timeline, { hash: pin.hash, intro_frames: pin.intro.frames, outro_frames: pin.outro.frames, body_frames: timeline.total_frames });
  const base = readJson(path.join(workdir, contract.metadata.file));
  requireThat(base.final_sha256 === final.content_sha256 && base.branding_hash === pin.hash, "renewed base metadata is stale");
  const translated = composeMetadata({ ...project, timeline: presented, locales: Object.keys(body.payload.locales ?? {}).filter((l) => body.payload.locales[l].metadata === "ready") });
  requireThat(!translated.problems.length, `translated metadata is invalid: ${translated.problems.join("; ")}`);
  const texts = localeTexts(project.doc, project.translations).texts;
  const files = [...body.files], metadata = { ...base, localizations: { ...base.localizations, ...translated.metadata.localizations } };
  const entry = (role) => files.find((f) => f.role === role);
  for (const [locale, status] of Object.entries(body.payload.locales ?? {})) {
    const choice = normalizedChoices(remote.locales)[locale];
    requireThat(choice, `${locale}: language is no longer selected`);
    if (status.metadata === "ready") {
      const fields = metadata.localizations[locale], expected = fields && `${fields.title}\n\n${fields.description}\n`;
      requireThat(choice.metadata && expected && entry(`description_${locale}`)?.sha256 === digest(expected), `${locale}: metadata attachment differs from current translated source`);
    }
    // A cached dub that has not passed this cumulative batch's check must not silently
    // change READY captions away from the retained narration presentation.
    const dubReady = status.dub === "ready" || body.gate === "dubs" && status.status === "ready";
    const current = choice.dub && dubReady ? currentDub(project, workdir, locale, timeline.speech_hash) : null;
    if (dubReady) {
      requireThat(current && !current.stale, `${locale}: ready dub has no current fitted source`);
      const flags = readJson(path.join(workdir, "review", `check-flags.${locale}.json`), null), cache = readJson(path.join(workdir, "review", `check.${locale}.json`), null);
      const check = readJson(path.join(workdir, "state.json"), { runs: [] }).runs.filter((v) => v.stage === "check-audio" && v.locale === locale).at(-1);
      requireThat(current.lines?.length > 0 && check?.lines === current.lines.length && check.unchecked === 0 && check.flagged === 0 && flags?.locale === locale && flags.speech_hash === current.speech_hash && flags.translation_hash === current.translation_hash && Array.isArray(flags.flags) && !flags.flags.length, `${locale}: ready dub has no complete current audio check`);
      for (const line of current.lines) {
        const checked = cache?.lines?.[line.id], clip = path.join(workdir, "dubs", locale, "audio", `${line.id}.wav`);
        requireThat(checked && typeof checked.heard === "string" && checked.intended === project.translations[locale]?.lines?.[line.id]?.text && checked.clip === (await sha256File(clip)).slice(0, 16), `${locale}: audio check does not cover the current dub clip ${line.id}`);
      }
    }
    if (status.captions === "ready") {
      requireThat(choice.captions && texts[locale] && !current?.stale, `${locale}: captions or dub timing source is stale`);
      const expected = toSrt(buildCues(current ? captionTimelineOf(current) : presented, texts[locale], locale).cues);
      requireThat(entry(`captions_${locale}`)?.sha256 === digest(expected), `${locale}: captions do not match the renewed presentation/dub timeline`);
    }
    if (status.dub === "ready" || status.status === "ready" && body.gate === "dubs") requireThat(choice.dub && current && !current.stale && current.branding_hash === pin.hash && entry(`dub_${locale}`)?.sha256 === await sha256File(current.file), `${locale}: dub is not fitted and branded for this retained body`);
    const skipped = status.dub?.status === "skipped" ? status.dub : status.status === "skipped" ? status : null;
    if (skipped) requireThat(choice.dub && skipped.reason?.trim() && dubsForUpload(project, workdir, timeline.speech_hash, [locale]).skipped[locale] === skipped.reason, `${locale}: dub skip has no current source-bound reason`);
  }
  requireThat(typeof upload === "function", "language submission requires hash-checked attachment transport");
  const metadataFile = path.join(workdir, "language-package/renewed-metadata.json"); save(metadataFile, metadata);
  const metadataEntry = await upload(request, contract.slug, metadataFile, "metadata", "application/json");
  requireThat(metadataEntry.sha256 === await sha256File(metadataFile), "language metadata changed while staging");
  const currentFiles = [...files.filter((f) => !["metadata", "languages_manifest"].includes(f.role)), metadataEntry];
  const manifest = { schema_version: 1, slug: contract.slug, source: { publish: identity(publish), final: identity(final), script: null, branding_hash: pin.hash, speech_hash: timeline.speech_hash, compilation_hash: null }, choice: { locales: normalizedChoices(remote.locales), decided_at: remote.locales_decided_at }, locales: body.payload.locales, files: currentFiles };
  const manifestFile = path.join(workdir, "language-package/renewed-languages-manifest.json"); save(manifestFile, manifest);
  const proof = await upload(request, contract.slug, manifestFile, "languages_manifest", "application/json");
  requireThat(proof.sha256 === await sha256File(manifestFile), "language source manifest changed while staging");
  return { ...body, content_sha256: proof.sha256, payload: { ...body.payload, final_review_id: final.id }, files: [...currentFiles, proof] };
}

/** Uses existing review transport, including hash-checked file receipts; a lost submission
 * response is preserved and never retried automatically. The uploader remains untouched. */
export async function stageManualPublish({ workdir, client, send, uploadInactive, baseOnly = false, now = new Date() }) {
  const receipt = readJson(path.join(workdir, RECEIPT));
  requireThat(receipt.mode === "manual-import" && (baseOnly || !receipt.holds.length), `manual package remains held: ${receipt.holds.join("; ")}`);
  const stagedFile = path.join(workdir, "review/manual-publish-submission.json");
  requireThat(!existsSync(stagedFile), "publish submission already attempted; inspect site state and the saved receipt before another attempt");
  requireThat(typeof uploadInactive === "function" && await uploadInactive(receipt.slug) === true, "publish staging requires a fresh upload-session/job inactivity probe");
  const remote = await client.project(receipt.slug), final = approved(remote, receipt.slug);
  inactive(remote);
  const metadata = readJson(path.join(workdir, "upload/metadata.json"));
  const sha = await sha256File(path.join(workdir, "upload/metadata.json"));
  const wanted = normalizedChoices(remote.locales);
  const report = checkPackage({ files: listFiles(path.join(workdir, "upload")), metadata, finalSha256: await sha256File(path.join(workdir, "upload/final.mp4")), approvedSha256: final.content_sha256, metadataSha256: sha, locales: baseOnly ? metadata.captions.map((v) => path.basename(v, ".srt")) : ["zh-TW", ...Object.keys(wanted).filter((l) => wanted[l].captions)], descriptionLocales: baseOnly ? ["zh-TW", ...Object.keys(metadata.localizations)] : ["zh-TW", ...Object.keys(wanted).filter((l) => wanted[l].metadata)], brandingMatches: validateBranding(readJson(path.join(workdir, "branding.json")), { base: workdir }).hash === final.payload.branding_hash });
  requireThat(report.ok, report.items.filter((v) => !v.ok).map((v) => v.detail).join("; "));
  const { uploadCandidate } = await import("./renewal.mjs");
  const files = [];
  for (const entry of packageFiles([...listFiles(path.join(workdir, "upload")).keys()])) files.push(await (send ?? uploadCandidate)(client, receipt.slug, path.join(workdir, "upload", entry.path), entry.role));
  const body = await bindManualSubmission({ body: { gate: "publish", content_sha256: sha, summary: baseOnly ? "Source-bound renewed base package; selected language parts remain pending" : "Source-bound renewed imported upload package; final approval retained", payload: { package: report, locales: ["zh-TW", ...Object.keys(metadata.localizations)], ...(baseOnly ? { base_only: true, pending_language_sources: receipt.holds } : {}) }, files }, remote: await client.project(receipt.slug), workdir });
  requireThat(await uploadInactive(receipt.slug) === true, "upload activity started while staging attachments; no publish submission");
  save(stagedFile, { at: now.toISOString(), status: "submitting", body });
  const result = await client.submit(receipt.slug, body);
  requireThat(result?.gate === "publish" && result.content_sha256 === body.content_sha256, "unexpected publish response; inspect the saved receipt without retrying");
  const current = latest(await client.project(receipt.slug), "publish");
  requireThat(current?.id === result.id && current.content_sha256 === body.content_sha256, "publish response not confirmed by readback; preserve the submission receipt");
  save(stagedFile, { at: now.toISOString(), status: "confirmed", review_id: result.id, body });
  return result;
}

// A standalone offline entry point avoids changing the normal worker/owner commands.
export async function handoffMain(args) {
  const [command, ...rest] = args;
  const { values } = parseArgs({ args: rest, options: { config: { type: "string" }, receipt: { type: "string" }, remote: { type: "string" }, project: { type: "string" } }, strict: true });
  if (command === "prepare" && values.config) return prepareHandoff(readJson(values.config));
  if (command === "verify" && values.receipt && values.remote) return verifyHandoff({ receipt: readJson(values.receipt), remote: readJson(values.remote), project: values.project ? readJson(values.project) : undefined });
  throw new UsageError("renewal-handoff.mjs prepare --config JSON; verify --receipt JSON --remote JSON. Activation is a guarded host operation requiring fresh probes.");
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) handoffMain(process.argv.slice(2)).then((r) => process.stdout.write(`${r.slug}: ${r.kind}; held, no approval or upload performed\n`)).catch((e) => { process.stderr.write(`${e.message}\n`); process.exitCode = 1; });
