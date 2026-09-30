// External channel bookends are normalized once to the scene encoder, then joined around a
// body cut by video copy. Audio is decoded and trimmed on the 48 kHz frame grid before one
// final encode, avoiding AAC padding at either seam. The body and its timeline stay intact.
import { randomUUID } from "node:crypto";
import { existsSync, mkdirSync, renameSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";

import { sha256File } from "../core/approvals.mjs";
import { BRANDING_FILE, brandingHash, validateBranding } from "../core/branding.mjs";
import { isInside, UsageError } from "../core/paths.mjs";
import { FPS, SAMPLE_RATE, SAMPLES_PER_FRAME } from "../core/timeline.mjs";
import { joinList } from "../compile/plan.mjs";
import { locateFfmpeg, runTool } from "./ffmpeg.mjs";
import { ENCODER_VERSION, probeArgs, segmentArgs } from "./plan.mjs";

/** Verify the bytes and declared frames, rather than trusting the installed JSON. */
export async function verifyBrandingAssets(branding, { tools, exec = runTool } = {}) {
  const selected = validateBranding(branding);
  if (!selected) return null;
  const binaries = tools ?? await locateFfmpeg();
  for (const role of ["intro", "outro"]) {
    const clip = selected[role];
    if (!existsSync(clip.file)) throw new UsageError(`branding ${role} is missing: ${clip.file}`);
    if (await sha256File(clip.file) !== clip.sha256) throw new UsageError(`branding ${role} SHA-256 changed; reinstall the selected asset`);
    const probe = JSON.parse((await exec(binaries.ffprobe, probeArgs(clip.file))).stdout);
    const video = probe.streams?.find((stream) => stream.codec_type === "video");
    const audio = probe.streams?.find((stream) => stream.codec_type === "audio");
    if (!video || video.width !== 1920 || video.height !== 1080 || video.r_frame_rate !== `${FPS}/1` || Number(video.nb_read_packets) !== clip.frames) {
      throw new UsageError(`branding ${role} must have exactly ${clip.frames} frames at 1920×1080 / ${FPS} fps`);
    }
    if (!audio) throw new UsageError(`branding ${role} has no sound track`);
    if (Number.isFinite(Number(audio.duration)) && Number(audio.duration) < clip.frames / FPS - 1 / FPS) throw new UsageError(`branding ${role} audio is shorter than its picture`);
  }
  return selected;
}

/** The same picture encoder as an ordinary scene, opening a video instead of a PNG list. */
export function brandingSegmentArgs(source, outFile, frames) {
  const scene = segmentArgs("unused", outFile, frames);
  return ["-hide_banner", "-y", "-loglevel", "error", "-i", source, ...scene.slice(scene.indexOf("-vf"))];
}

function clipsOf(bodyFile, bodyFrames, branding) {
  if (!Number.isInteger(bodyFrames) || bodyFrames < 1) throw new UsageError("branding needs a positive body frame count");
  return [branding.intro, { file: bodyFile, frames: bodyFrames }, branding.outro];
}

/** Shared exact-sample sound join, with an optional copy-only video input before the sound. */
export function brandingJoinArgs({ bodyFile, bodyFrames, branding, outFile, videoList = null, outputCodec = ["-c:a", "aac", "-b:a", "384k"] }) {
  const args = ["-hide_banner", "-y", "-loglevel", "error"];
  const inputOffset = videoList ? 1 : 0;
  if (videoList) args.push("-f", "concat", "-safe", "0", "-i", videoList);
  const filters = [];
  const labels = [];
  clipsOf(bodyFile, bodyFrames, branding).forEach((clip, index) => {
    args.push("-i", clip.file);
    const samples = clip.frames * SAMPLES_PER_FRAME;
    filters.push(`[${index + inputOffset}:a:0]aresample=${SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,atrim=end_sample=${samples},apad=whole_len=${samples},atrim=end_sample=${samples},asetpts=PTS-STARTPTS[a${index}]`);
    labels.push(`[a${index}]`);
  });
  filters.push(`${labels.join("")}concat=n=3:v=0:a=1[a]`);
  args.push("-filter_complex", filters.join(";"));
  if (videoList) args.push("-map", "0:v:0", "-c:v", "copy");
  else args.push("-vn");
  args.push("-map", "[a]", ...outputCodec, "-ar", String(SAMPLE_RATE), "-ac", "2");
  if (videoList || /\.(?:mp4|m4a)$/i.test(outFile)) args.push("-movflags", "+faststart");
  args.push(outFile);
  return args;
}

function appliedRecord(branding, bodyFrames) {
  return { hash: brandingHash(branding), id: branding.id, intro_frames: branding.intro.frames, outro_frames: branding.outro.frames, body_frames: bodyFrames };
}

/** Write a partial final around bodyFile; the caller replaces the final after success. */
export async function wrapVideo({ tools, exec = runTool, workdir, bodyFile, bodyFrames, branding, outFile }) {
  if (path.resolve(bodyFile) === path.resolve(outFile)) throw new UsageError("branding output must not overwrite its body input");
  const selected = await verifyBrandingAssets(branding, { tools, exec });
  if (!selected) throw new UsageError("wrapVideo needs a branding package");
  const directory = path.join(workdir, "build", "branding", `${selected.hash}-${ENCODER_VERSION}`);
  mkdirSync(directory, { recursive: true });
  const pictures = [];
  for (const role of ["intro", "outro"]) {
    const clip = selected[role];
    const file = path.join(directory, `${role}.mp4`);
    if (!existsSync(file)) {
      const partial = path.join(directory, `${role}.partial.mp4`);
      await exec(tools.ffmpeg, brandingSegmentArgs(clip.file, partial, clip.frames));
      renameSync(partial, file);
    }
    pictures.push(file);
  }
  const list = path.join(directory, "join.ffconcat");
  writeFileSync(list, joinList([pictures[0], bodyFile, pictures[1]]));
  await exec(tools.ffmpeg, brandingJoinArgs({ bodyFile, bodyFrames, branding: selected, outFile, videoList: list }));
  return { ...appliedRecord(selected, bodyFrames), body_file: path.relative(workdir, bodyFile).split(path.sep).join("/"), body_sha256: await sha256File(bodyFile) };
}

/** A dub uses the exact same bookend audio, without changing its body's mix or fitted voice. */
export async function wrapAudio({ tools, exec = runTool, bodyFile, bodyFrames, branding, outFile, outputCodec }) {
  if (path.resolve(bodyFile) === path.resolve(outFile)) throw new UsageError("branding output must not overwrite its body input");
  const selected = await verifyBrandingAssets(branding, { tools, exec });
  if (!selected) throw new UsageError("wrapAudio needs a branding package");
  await exec(tools.ffmpeg, brandingJoinArgs({ bodyFile, bodyFrames, branding: selected, outFile, outputCodec }));
  return appliedRecord(selected, bodyFrames);
}

/**
 * Promote a checked cut and its binding records together, rolling back earlier renames when
 * any later one fails. Encoding and QA happen before this function; an invalid partial never
 * replaces the existing final, pin, checks, or compilation body.
 */
export function commitBrandedVideo({ workdir, branding, finalPartial, bodyPartial = null, checks, artifacts = [], now = new Date(), rename = renameSync }) {
  if (!checks?.ok) throw new UsageError("a failed branded cut cannot replace the current final");
  const selected = validateBranding(branding);
  if (!selected || checks.branding?.hash !== selected.hash) throw new UsageError("branded checks do not match the selected package");
  const suffix = `.branding-${randomUUID()}`;
  const pin = path.join(workdir, `${BRANDING_FILE}${suffix}.staged`);
  const checked = path.join(workdir, `checks.json${suffix}.staged`);
  const staged = [{ source: finalPartial, target: path.join(workdir, "final.mp4") }];
  if (bodyPartial) {
    const bodyTarget = path.resolve(workdir, checks.branding.body_file);
    if (!isInside(bodyTarget, path.join(workdir, "build"))) throw new UsageError("the retained branding body must stay in the video's build directory");
    staged.push({ source: bodyPartial, target: bodyTarget });
  }
  const coreTargets = ["final.mp4", BRANDING_FILE, "checks.json", checks.branding.body_file ?? "build/body.mp4"].map((file) => path.resolve(workdir, file));
  const targets = [...coreTargets];
  for (const artifact of artifacts) {
    if (typeof artifact?.source !== "string" || typeof artifact?.target !== "string") throw new UsageError("a staged branding artifact needs source and target paths");
    const source = path.resolve(workdir, artifact.source);
    const target = path.resolve(workdir, artifact.target);
    const strictlyInside = (file) => isInside(file, workdir) && !isInside(workdir, file);
    if (!strictlyInside(source) || !strictlyInside(target) || isInside(source, target) || isInside(target, source)) throw new UsageError("staged branding artifacts must have distinct paths inside the video work directory");
    if (targets.some((other) => isInside(target, other) || isInside(other, target))) throw new UsageError("staged branding artifact targets must not overlap each other or the final, body, pin or checks");
    targets.push(target);
    staged.push({ source, target });
  }
  staged.push({ source: pin, target: path.join(workdir, BRANDING_FILE) }, { source: checked, target: path.join(workdir, "checks.json") });
  const moved = [];
  const backups = [];
  let committed = false;
  try {
    writeFileSync(pin, `${JSON.stringify({ ...selected, adopted_at: now.toISOString() }, null, 2)}\n`);
    writeFileSync(checked, `${JSON.stringify(checks, null, 2)}\n`);
    for (const item of staged) {
      if (existsSync(item.target)) {
        const backup = `${item.target}${suffix}.previous`;
        rename(item.target, backup);
        backups.push({ target: item.target, backup });
      }
      rename(item.source, item.target);
      moved.push(item);
    }
    committed = true;
  } catch (error) {
    // Use the real rename for recovery, not an injected failure used to test promotion.
    for (const item of moved.toReversed()) if (existsSync(item.target)) renameSync(item.target, item.source);
    for (const { target, backup } of backups.toReversed()) if (existsSync(backup)) renameSync(backup, target);
    throw error;
  } finally {
    if (committed) for (const { backup } of backups) {
      // A compilation also replaces its captions directory. Every backup is constructed from
      // a checked target inside this workdir, so cleanup cannot recurse outside the video.
      if (!isInside(path.resolve(backup), path.resolve(workdir)) || isInside(path.resolve(workdir), path.resolve(backup))) throw new UsageError("branding backup escaped the video work directory");
      rmSync(backup, { recursive: true, force: true });
    }
    for (const temporary of [pin, checked]) rmSync(temporary, { force: true });
  }
}
