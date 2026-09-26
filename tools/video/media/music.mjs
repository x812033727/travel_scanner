// `music`: the drama's background track (docs/videos/DRAMA.md). `music.prompt` has the server
// generate one at least as long as the video into music/; `music.track` names the owner's own
// file under <work base>/_music/, checked against music.sha256 when given. Either way
// music/manifest.json carries the mix hash status compares.
import { existsSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { sha256File } from "../core/approvals.mjs";
import { isDrama, mixHash, resolveMusic } from "../core/drama.mjs";
import { atomicWrite, readJson, resolveWorkBase, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { FPS, speechHash } from "../core/timeline.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { mediaKey } from "./cache.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { clientOptions, requireCredentials } from "./cli.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { Stage, statusProblem, trackPrice } from "./stages.mjs";

// The track outlasts the video a little, so the fade-out never runs into silence; the server
// takes 10 to 600 seconds.
export const TAIL_SECONDS = 5;
export const MIN_TRACK_SECONDS = 10;
export const MAX_TRACK_SECONDS = 600;

/** Seconds of music to ask for, given the narration's frames. */
export function trackSeconds(totalFrames) {
  return Math.max(MIN_TRACK_SECONDS, Math.min(MAX_TRACK_SECONDS, Math.ceil(totalFrames / FPS) + TAIL_SECONDS));
}

const manifestFile = (workdir) => path.join(workdir, ARTIFACTS.music);

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, file: { type: "string" }, workdir: { type: "string" }, "dry-run": { type: "boolean" } }, strict: true }).values;
  if (!values.slug && !values.file) throw new UsageError("music needs --slug (or --file for an example outside docs/videos)");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const { doc, lexicon } = project;
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  if (!isDrama(doc)) throw new UsageError("music is for a drama (format \"drama\")");
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
      const problem = statusProblem(status, "music");
      ctx.stdout.write(`server: ${problem ? `NOT ready: ${problem}` : `${status.music.provider} ${status.music.model} ready`}; about US$${trackPrice(status).toFixed(2)}; this video so far US$${ledgerTotals(workdir).usd.toFixed(2)} of the US$${status.max_usd_per_video} cap\n`);
    } else {
      ctx.stdout.write("no video tool token yet; run `node tools/video/cli.mjs login` before generating\n");
    }
    return EXIT.ok;
  }

  const credentials = requireCredentials(ctx);
  const options = clientOptions(ctx, credentials);
  const status = await mediaStatus(options);
  const problem = statusProblem(status, "music");
  if (problem) throw new MediaError(problem, { who: "owner" });
  const stage = new Stage({ slug: doc.slug, workdir, options, status, stage: "music", now: ctx.now });
  const key = mediaKey("music", { provider: status.music.provider, model: status.music.model, prompt: music.prompt, seconds });
  const track = await stage.music({ id: "music", key, prompt: music.prompt, seconds, target: `music/${key}` });
  const manifest = { mix_hash: mix, source: "generated", file: track.file, sha256: track.sha256, seconds, prompt: music.prompt, key, model: manifest_model(status), generated_at: ctx.now().toISOString() };
  atomicWrite(manifestFile(workdir), `${JSON.stringify(manifest, null, 2)}\n`);
  recordStage(workdir, "music", { source: "generated", seconds, reused: track.reused, usd: ledgerTotals(workdir).usd }, ctx.now());
  ctx.stdout.write(`music: ${track.file} (${seconds} s${track.reused ? ", reused" : ""}); this video has spent US$${ledgerTotals(workdir).usd.toFixed(2)}\nnext: node tools/video/cli.mjs assemble --slug ${doc.slug}\n`);
  return EXIT.ok;
}

const manifest_model = (status) => ({ provider: status.music.provider, model: status.music.model });
