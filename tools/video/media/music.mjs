// `music`: the video's background track (docs/videos/DRAMA.md; slides: docs/videos/ILLUSTRATED.md). `music.prompt` has the server
// request a track at least as long as the video into music/; the decoded result is measured
// before assembly because the provider may return less audio. `music.track` names the owner's own
// file under <work base>/_music/, checked against music.sha256 when given. Either way
// music/manifest.json carries the mix hash status compares.
import { existsSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { locateFfmpeg, runTool } from "../assemble/ffmpeg.mjs";
import { isLongAnime } from "../core/anime-policy.mjs";
import { sha256File } from "../core/approvals.mjs";
import { mixHash, resolveMusic } from "../core/drama.mjs";
import { loopCovers, MIN_LOOP_SECONDS } from "../core/music-loop.mjs";
import { atomicWrite, isInside, readJson, resolveWorkBase, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { STORY_KIND } from "../core/story.mjs";
import { FPS, speechHash } from "../core/timeline.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { mediaKey, readCache, readJobs } from "./cache.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { ledgerTotals, readLedger } from "./ledger.mjs";
import { mayWriteProject, Stage, statusProblem, trackPrice } from "./stages.mjs";

// Ask for a little more than the video so the fade-out does not reach silence; the server
// accepts requests of 10 to 600 seconds, but may return a shorter decoded track.
export const TAIL_SECONDS = 5;
export const MIN_TRACK_SECONDS = 10;
export const MAX_TRACK_SECONDS = 600;

/** Seconds of music to ask for, given the narration's frames. */
export function trackSeconds(totalFrames) {
  return Math.max(MIN_TRACK_SECONDS, Math.min(MAX_TRACK_SECONDS, Math.ceil(totalFrames / FPS) + TAIL_SECONDS));
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.music);

/** Final decoded timestamp from ffmpeg -progress (its historical out_time_ms is microseconds). */
export function decodedProgressSeconds(output) {
  const fields = Object.fromEntries(String(output).trim().split(/\r?\n/).map((line) => line.split(/=(.*)/s, 2)));
  if (fields.progress !== "end") return null;
  const micros = Number(fields.out_time_us ?? fields.out_time_ms);
  if (Number.isFinite(micros) && micros > 0) return micros / 1_000_000;
  const stamp = /^(\d+):(\d{2}):(\d{2}(?:\.\d+)?)$/.exec(fields.out_time ?? "");
  if (!stamp) return null;
  const seconds = Number(stamp[1]) * 3600 + Number(stamp[2]) * 60 + Number(stamp[3]);
  return Number.isFinite(seconds) && seconds > 0 ? seconds : null;
}

/** Decode the complete audio stream. ffprobe's MP3 header duration alone is not delivery proof. */
export async function decodedMusicSeconds(file, env = process.env, tool = null) {
  const ffmpeg = tool ?? (await locateFfmpeg({ ...process.env, ...env })).ffmpeg;
  const { stdout } = await runTool(ffmpeg, ["-nostats", "-v", "error", "-xerror", "-i", file, "-map", "0:a:0", "-f", "null", "-", "-progress", "pipe:1"]);
  const seconds = decodedProgressSeconds(stdout);
  if (seconds === null) {
    throw new Error(`could not measure the fully decoded music duration: ${file}`);
  }
  return seconds;
}

/** A prior music purchase must be reused or reconciled, never silently replaced. */
async function retainedGeneratedTrack(workdir, key) {
  const manifest = readJson(manifestFile(workdir), null);
  const prior = manifest?.source === "generated" ? manifest : null;
  if (prior && prior.key !== key) {
    throw new MediaError(`a paid music track already has request ${prior.key ?? "unknown"}; preserve it and review the changed prompt, model or cut length before buying another`, { who: "owner" });
  }
  const entry = prior ?? readCache(workdir).entries[key];
  if (entry) {
    if (!entry.file || !entry.sha256) throw new MediaError("retained music has no file or SHA-256 binding; reconcile the paid artifact before rerunning music", { who: "owner" });
    const file = path.join(workdir, entry.file);
    if (!existsSync(file) || (await sha256File(file)) !== entry.sha256) {
      throw new MediaError(`retained music ${entry.file} is missing or differs from its saved SHA-256; restore or reconcile the paid file before rerunning music`, { who: "owner" });
    }
    return { file: entry.file, sha256: entry.sha256, key, reused: true };
  }
  const paid = readLedger(workdir).entries.some((row) => row.kind === "music" && (row.status !== "failed" || Number(row.cost_usd) > 0));
  const pending = readJobs(workdir).jobs[key];
  if (paid && !pending) {
    throw new MediaError("a music request was already paid or reserved, but no retained file or pending job is bound to this request; reconcile its cache and ledger before another purchase", { who: "owner" });
  }
  return null;
}

/**
 * The most times a hands-off series' music stage loops a short track on its own: the track
 * covers at least half the cut, so the loop only fills a tail. A track shorter than that is far
 * from what was asked for, and the owner looks at it.
 */
export const HANDS_OFF_MAX_PLAYS = 2;

/**
 * Whether the checks, not the owner, decide a short generated track's loop: an episode of a
 * hands-off drama series (docs/videos/BINGE.md: its checks decide every gate), from the
 * episode's series.json. A long anime keeps its owner's gates however the flag reads, as the
 * site's hands_off_series has it. A brand story's series is hands-off too, but the hold was
 * written for its beds (#1669, a 174 s track under a 600 s request), which play three or more
 * times under its cut, so a story's loop stays the owner's `music --loop`.
 */
export function loopDecidedByChecks(series) {
  return Boolean(series) && series.kind !== STORY_KIND && !isLongAnime(series) && !isLongAnime(series.series) && series.series?.hands_off === true;
}

/** The loop music/manifest.json records (read by core/music-loop.mjs loopCovers). */
function loopRecord({ sha256, track, cut, basis, decidedBy, now }) {
  return { method: "stream_loop", sha256, track_seconds: track, cut_seconds: cut, plays: Math.ceil(cut / track), basis, decided_by: decidedBy, decided_at: now.toISOString() };
}

/**
 * `music --loop`: the owner's decision that a retained generated track shorter than the cut
 * plays looped, as every mix already plays it (assemble/drama.mjs soundGraph, `-stream_loop -1`).
 * Free: no provider request, no credentials. Checked: the file still matches its saved SHA-256,
 * the manifest was made for these music settings, its length comes from a full decode, it is at
 * least MIN_LOOP_SECONDS, and the cut is the current timeline's (speech_hash). That cut may not be
 * assembled yet: a new video's assembly needs the loop first (assemble/sound.mjs musicInputs), and
 * a published video's dubs reuse the bed its cut was mixed with, so `basis` says which it was.
 * Writes the loop into music/manifest.json, which musicInputs and status read (loopCovers).
 */
async function recordLoop({ doc, lexicon, workdir, mix, ctx, EXIT }) {
  const manifest = readJson(manifestFile(workdir), null);
  if (manifest?.source !== "generated" || !manifest.file || !manifest.sha256) {
    throw new UsageError("music --loop needs a retained generated track with its SHA-256 in music/manifest.json; an owner's own track loops by its own file");
  }
  const file = path.join(workdir, manifest.file);
  if (!isInside(file, workdir) || !existsSync(file) || (await sha256File(file)) !== manifest.sha256) {
    throw new UsageError(`retained music ${manifest.file} is missing or differs from its saved SHA-256; restore the paid file before recording a loop`);
  }
  // A held track keeps its request's hash in requested_mix_hash; a passing or older one in mix_hash.
  if ((manifest.requested_mix_hash ?? manifest.mix_hash) !== mix) throw new UsageError("music/manifest.json was made for older music settings; run music first, then record the loop of its track");
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  if (!timeline || timeline.speech_hash !== speechHash(doc, lexicon)) throw new UsageError("timeline.json is missing or was built for an older script; the loop is recorded for the current cut");
  const actualSeconds = await decodedMusicSeconds(file, ctx.env);
  if (actualSeconds < MIN_LOOP_SECONDS) throw new UsageError(`the track decodes to ${actualSeconds.toFixed(3)} s, under the ${MIN_LOOP_SECONDS} s a looped bed needs; choose another licensed track`);
  const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
  const assembled = existsSync(path.join(workdir, ARTIFACTS.video)) && Boolean(checks?.ok) && checks.mix_hash === mix && checks.speech_hash === timeline.speech_hash;
  const cutSeconds = timeline.total_frames / FPS;
  const loop = loopRecord({ sha256: manifest.sha256, track: actualSeconds, cut: cutSeconds, basis: assembled ? "assembled_cut" : "timeline", decidedBy: "command", now: ctx.now() });
  if (!mayWriteProject(ctx, workdir, "music")) return EXIT.incomplete;
  atomicWrite(manifestFile(workdir), `${JSON.stringify({ ...manifest, mix_hash: mix, actual_seconds: actualSeconds, duration_measurement: "ffmpeg_full_decode", duration_hold: false, loop }, null, 2)}\n`);
  recordStage(workdir, "music", { source: "generated", looped: true, actual_seconds: actualSeconds, cut_seconds: cutSeconds }, ctx.now());
  ctx.stdout.write(`music: ${manifest.file} (decoded ${actualSeconds.toFixed(3)} s) plays ${loop.plays} times under the ${cutSeconds.toFixed(3)} s cut${assembled ? ", as the assembled cut does" : ""}; recorded in music/manifest.json\n`);
  if (!assembled) ctx.stdout.write(`next: node tools/video/cli.mjs assemble --slug ${doc.slug}\n`);
  return EXIT.ok;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, "dry-run": { type: "boolean" }, loop: { type: "boolean" } }, strict: true }).values;
  if (!values.slug && !values.file) throw new UsageError("music needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc, lexicon } = project;
  if (values.loop) {
    if (!resolveMusic(doc)?.prompt) throw new UsageError(`${doc.slug} has no generated music to loop`);
    const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
    // A decision about the bed alone, so the script's lint today does not stand in the way;
    // assemble lints before it mixes.
    return recordLoop({ doc, lexicon, workdir, mix: mixHash(doc), ctx, EXIT });
  }
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  // Any format may carry music (docs/videos/ILLUSTRATED.md); a script without any has nothing to make.
  const music = resolveMusic(doc);
  if (!music) throw new UsageError(`${doc.slug} has no music: add music.prompt or music.track to video.json`);
  const workBase = resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const mix = mixHash(doc);

  if (music.track) {
    const file = path.join(workBase, "_music", music.track);
    if (!existsSync(file)) throw new MediaError(`music.track ${music.track} is not in ${path.join(workBase, "_music")}: put the licensed file there`, { who: "owner" });
    const sha256 = await sha256File(file);
    if (music.sha256 && music.sha256 !== sha256) throw new MediaError(`${music.track} hashes to ${sha256.slice(0, 12)}…, not music.sha256; check the file or update video.json`, { who: "owner" });
    if (!mayWriteProject(ctx, workdir, "music")) return EXIT.incomplete;
    atomicWrite(manifestFile(workdir), `${JSON.stringify({ mix_hash: mix, source: "track", track: music.track, sha256, checked_at: ctx.now().toISOString() }, null, 2)}\n`);
    recordStage(workdir, "music", { source: "track", track: music.track }, ctx.now());
    ctx.stdout.write(`music: ${music.track} (${sha256.slice(0, 12)}…) from ${path.join(workBase, "_music")}\nnext: node tools/video/cli.mjs assemble --slug ${doc.slug}\n`);
    return EXIT.ok;
  }

  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  if (!timeline || timeline.speech_hash !== speechHash(doc, lexicon)) {
    ctx.stderr.write("timeline.json is missing or was built for an older script; run tts first (the track is as long as the video)\n");
    return EXIT.usage;
  }
  const seconds = trackSeconds(timeline.total_frames);
  if (values["dry-run"]) {
    ctx.stdout.write(`music: ${seconds} s for a ${(timeline.total_frames / FPS).toFixed(1)} s video; prompt: ${music.prompt}\n`);
    const credentials = readCredentials({ env: ctx.env, home: ctx.home });
    if (credentials.token) {
      const status = await mediaStatus(clientOptions(ctx, credentials));
      const problem = statusProblem(status, "music", doc.format);
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${status.music.provider} ${status.music.model} ready`}; about US$${trackPrice(status).toFixed(2)}; this video so far US$${ledgerTotals(workdir).usd.toFixed(2)} of the US$${status.max_usd_per_video} cap\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before generating\n");
    }
    return EXIT.ok;
  }

  if (!mayWriteProject(ctx, workdir, "music")) return EXIT.incomplete;
  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = await mediaStatus(options);
  const problem = statusProblem(status, "music", doc.format);
  if (problem) throw new MediaError(problem, { who: "owner" });
  const { ffmpeg } = await locateFfmpeg({ ...process.env, ...ctx.env }); // fail before a paid request if decoding is unavailable
  const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "music", format: doc.format, now: ctx.now });
  const key = mediaKey("music", { provider: status.music.provider, model: status.music.model, prompt: music.prompt, seconds });
  const track = (await retainedGeneratedTrack(workdir, key)) ?? (await stage.music({ id: "music", key, prompt: music.prompt, seconds, target: `music/${key}` }));
  const actualSeconds = await decodedMusicSeconds(path.join(workdir, track.file), ctx.env, ffmpeg);
  const requiredSeconds = timeline.total_frames / FPS;
  const short = actualSeconds < requiredSeconds;
  // A short track plays looped only by a recorded decision: the one already made for this file
  // and cut (a rerun keeps it), or, on a hands-off series, the checks' own (loopDecidedByChecks).
  const prior = readJson(manifestFile(workdir), null)?.loop;
  const plays = Math.ceil(requiredSeconds / actualSeconds);
  const checksDecide = loopDecidedByChecks(project.series);
  let loop = null;
  if (short && loopCovers({ sha256: track.sha256, actual_seconds: actualSeconds, loop: prior }, requiredSeconds)) loop = prior;
  else if (short && checksDecide && actualSeconds >= MIN_LOOP_SECONDS && plays <= HANDS_OFF_MAX_PLAYS) {
    loop = loopRecord({ sha256: track.sha256, track: actualSeconds, cut: requiredSeconds, basis: "timeline", decidedBy: "hands_off", now: ctx.now() });
  }
  const held = short && !loop;
  // An insufficient track retains the requested mix binding for audit, but has no passing mix_hash.
  // This keeps the existing status checklist from marking "music generated" complete.
  const manifest = { mix_hash: held ? null : mix, requested_mix_hash: mix, source: "generated", file: track.file, sha256: track.sha256, requested_seconds: seconds, actual_seconds: actualSeconds, duration_measurement: "ffmpeg_full_decode", duration_hold: held, prompt: music.prompt, key, model: manifest_model(status), generated_at: ctx.now().toISOString(), ...(loop ? { loop } : {}) };
  atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);
  recordStage(workdir, "music", { source: "generated", requested_seconds: seconds, actual_seconds: actualSeconds, duration_hold: held, ...(loop ? { looped: true } : {}), reused: track.reused, usd: ledgerTotals(workdir).usd }, ctx.now());
  ctx.stdout.write(`music: ${track.file} (decoded ${actualSeconds.toFixed(3)} s; requested ${seconds} s${track.reused ? "; reused" : ""}); this video has spent US$${ledgerTotals(workdir).usd.toFixed(2)}\n`);
  if (loop) {
    const by = loop === prior ? "the loop already recorded for this file and cut" : "a hands-off series' checks recorded the loop";
    ctx.stdout.write(`music: plays ${loop.plays} times under the ${requiredSeconds.toFixed(3)} s cut (${by}; music/manifest.json)\n`);
  }
  if (held) {
    const handsOff = !checksDecide ? "" : actualSeconds < MIN_LOOP_SECONDS ? ` Under ${MIN_LOOP_SECONDS} s it is no bed to loop.` : ` It would play ${plays} times, more than the ${HANDS_OFF_MAX_PLAYS} a hands-off series loops on its own.`;
    ctx.stderr.write(`music needs the owner: decoded track is shorter than the ${requiredSeconds.toFixed(3)} s cut.${handsOff} Keep this paid file; record a checked loop (node tools/video/cli.mjs music --slug ${doc.slug} --loop) or arrange another licensed track. No replacement was bought.\n`);
    return EXIT.owner;
  }
  ctx.stdout.write(`next: node tools/video/cli.mjs assemble --slug ${doc.slug}\n`);
  return EXIT.ok;
}

const manifest_model = (status) => ({ provider: status.music.provider, model: status.music.model });
