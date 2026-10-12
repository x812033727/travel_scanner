// The channel outro with room for YouTube's end screen (docs/videos/BRANDING.md). It keeps the
// installed like/share/bell clip after a one-second pause, then holds a quiet moving canvas with
// faint outlines where the owner places the end-screen elements in YouTube Studio: two videos
// and the subscribe button. A video cannot draw clickable links itself, and the YouTube Data API
// cannot set an end screen, so the picture only leaves the room and the music fills it.
//
//   node tools/video/branding/outro.mjs --base OUTRO.mp4 --music TRACK --music-start 105.5 \
//     --intro CHANNEL_INTRO.mp4 [--series-intro SOTHATSWHY_INTRO.mp4] --out DIR
//
// DIR receives a package per intro (channel/, sothatswhy/), each with intro.mp4, outro.mp4 and
// manifest.json, ready for `branding --install DIR/channel --dry-run`.
import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

import { locateFfmpeg, runTool } from "../assemble/ffmpeg.mjs";
import { parseLoudnorm, probeArgs } from "../assemble/plan.mjs";
import { sha256File } from "../core/approvals.mjs";
import { atomicWrite, UsageError } from "../core/paths.mjs";
import { FPS, SAMPLE_RATE } from "../core/timeline.mjs";

export const OUTRO_FRAMES = FPS * 21;
// A beat of quiet after the body's last line (which already ends about 1.8 s before the cut):
// the base clip's first frame holds while the music fades in from silence (owner, 2026-10-12).
export const LEAD_FRAMES = FPS;
// The installed clip's own picture and sound play next, unchanged.
export const BASE_FRAMES = 90;
// The icons fade off the canvas in this many frames, and the outlines fade in.
export const FADE_FRAMES = 15;
// Music alone reads louder than a voice at the same LUFS; the outro sits a little under the body.
export const OUTRO_LOUDNESS = { integrated: -16, truePeak: -1, range: 11 };
// Under the like/share/bell sound effects the music plays at this gain, rising after them.
const UNDER_GAIN = 0.4;

export const PALETTE = { cream: "F6F0E4", teal: [12, 108, 102], brown: [106, 73, 56] };
// Measured on the last frame of mokaair-brand-package-v2-cc's outro: the wordmark stays where it was.
export const LOGO = { x: 740, y: 225, w: 440, h: 110 };
// Where the end-screen elements sit in YouTube Studio, measured in its editor on 2026-10-12 and
// saved on oxEtlA8GWas as the template later uploads import: one row under the wordmark, video |
// subscribe | video. Studio keeps elements inside a safe area (about y 140-912 at 1080p) and the
// subscribe button has one fixed size, so the outlines follow Studio, not the other way round.
export const SLOTS = {
  videos: [{ x: 109, y: 371, w: 619, h: 349 }, { x: 1190, y: 371, w: 619, h: 349 }],
  subscribe: { cx: 960, cy: 550, r: 148 },
  radius: 12,
};
// The outline sits just outside each element, so a thin frame stays visible around the cards.
const OUTLINE_GAP = 5;

export const PACKAGES = {
  channel: { id: "mokaair-brand-package-v4-endscreen", introFlag: "intro" },
  sothatswhy: { id: "mokaair-sothatswhy-bookends-v3-endscreen", introFlag: "series-intro" },
};

/** Signed distance to the slots, as an ffmpeg expression in X and Y (negative inside). */
export function slotDistance(slots = SLOTS) {
  const box = ({ x, y, w, h }) => {
    const r = slots.radius;
    const qx = `(abs(X-${x + w / 2})-${w / 2 - r})`;
    const qy = `(abs(Y-${y + h / 2})-${h / 2 - r})`;
    return `(hypot(max(${qx},0),max(${qy},0))+min(max(${qx},${qy}),0)-${r})`;
  };
  const { cx, cy, r } = slots.subscribe;
  return [...slots.videos.map(box), `(hypot(X-${cx},Y-${cy})-${r})`].reduce((a, b) => `min(${a},${b})`);
}

/** A still RGBA layer drawn once with geq: a constant colour and an alpha expression. */
export function layerArgs({ width, height, rgb, alpha, outFile }) {
  const [r, g, b] = rgb;
  return [
    "-hide_banner", "-y", "-loglevel", "error",
    "-f", "lavfi", "-i", `color=c=black:s=${width}x${height}:d=1`,
    "-vf", `format=rgba,geq=r=${r}:g=${g}:b=${b}:a='${alpha}'`,
    "-frames:v", "1", outFile,
  ];
}

/** The four still layers: the slot fill, the slot outline and two soft colour blobs. */
export function layerPlan(dir) {
  const d = slotDistance();
  // A Gaussian lowered by its value at the square's inner edge, so the blob ends at zero there
  // instead of showing the square.
  const sigma2 = 2 * 150 * 150;
  const blob = (peak) => `${peak}*max(exp(-(pow(X-450,2)+pow(Y-450,2))/${sigma2})-${Math.exp(-450 * 450 / sigma2).toFixed(5)},0)`;
  return {
    fill: layerArgs({ width: 1920, height: 1080, rgb: [255, 255, 255], alpha: `90*clip(0.5-${d},0,1)`, outFile: path.join(dir, "fill.png") }),
    stroke: layerArgs({ width: 1920, height: 1080, rgb: PALETTE.teal, alpha: `150*clip(2-abs(${d}-${OUTLINE_GAP}),0,1)`, outFile: path.join(dir, "stroke.png") }),
    teal: layerArgs({ width: 900, height: 900, rgb: PALETTE.teal, alpha: blob(46), outFile: path.join(dir, "blob-teal.png") }),
    brown: layerArgs({ width: 900, height: 900, rgb: PALETTE.brown, alpha: blob(34), outFile: path.join(dir, "blob-brown.png") }),
  };
}

const drift = (x, y, ax, ay, period, phase) => [
  `x='${x}+${ax}*sin(2*PI*(t/${period}+${phase}))'`,
  `y='${y}+${ay}*cos(2*PI*(t/${period * 1.3}+${phase}))'`,
].join(":");

/**
 * Picture: the base clip's first frame held, its frames, then the canvas. The canvas starts as the base clip's last
 * frame, whose icons fade out before the outlines fade in; the wordmark is that frame's own
 * pixels, keyed off the cream so the blobs pass behind it.
 */
export function videoFilter({ leadFrames = LEAD_FRAMES, baseFrames = BASE_FRAMES, frames = OUTRO_FRAMES, fadeFrames = FADE_FRAMES } = {}) {
  const canvas = frames - leadFrames - baseFrames;
  const seconds = canvas / FPS;
  const fade = fadeFrames / FPS;
  return [
    `color=c=0x${PALETTE.cream}:s=1920x1080:r=${FPS}:d=${seconds},format=rgba[bg]`,
    `[bg][3:v]overlay=${drift(-260, -240, 140, 90, 17, 0)}:eval=frame[b1]`,
    `[b1][4:v]overlay=${drift(1240, 420, 120, 110, 19, 0.35)}:eval=frame[b2]`,
    `[b2][3:v]overlay=${drift(700, 620, 160, 70, 23, 0.7)}:eval=frame[b3]`,
    `[5:v]loop=-1:1,trim=end_frame=${canvas},fade=in:st=${fade}:d=${fade}:alpha=1[fill]`,
    `[6:v]loop=-1:1,trim=end_frame=${canvas},fade=in:st=${fade}:d=${fade}:alpha=1[stroke]`,
    `[b3][fill]overlay[c1]`,
    `[c1][stroke]overlay[c2]`,
    `[1:v]loop=-1:1,trim=end_frame=${canvas},crop=${LOGO.w}:${LOGO.h}:${LOGO.x}:${LOGO.y},format=rgba,colorkey=0x${PALETTE.cream}:0.06:0.12[logo]`,
    `[c2][logo]overlay=${LOGO.x}:${LOGO.y}[c3]`,
    `[1:v]loop=-1:1,trim=end_frame=${canvas},format=rgba,fade=out:d=${fade}:alpha=1[icons]`,
    `[c3][icons]overlay,trim=end_frame=${canvas},setpts=N/(${FPS}*TB),format=yuv420p[canvas]`,
    `[0:v]trim=end_frame=${baseFrames},setpts=N/(${FPS}*TB),tpad=start=${leadFrames}:start_mode=clone,format=yuv420p[base]`,
    `[base][canvas]concat=n=2:v=1:a=0[v]`,
  ].join(";");
}

/**
 * Sound: the base clip's effects, after the pause, over a window of the music, which fades in
 * through the pause, plays under the effects, rises once they are done and fades out at the end. `loudnorm` either measures
 * (no `measured`) or applies the second, linear pass.
 */
export function audioFilter({ musicStart, frames = OUTRO_FRAMES, leadFrames = LEAD_FRAMES, baseFrames = BASE_FRAMES, measured = null, loudness = OUTRO_LOUDNESS }) {
  if (!Number.isFinite(musicStart) || musicStart < 0) throw new UsageError("--music-start needs a non-negative number of seconds");
  const seconds = frames / FPS;
  const lead = leadFrames / FPS;
  const rise = lead + baseFrames / FPS - 0.5;
  const norm = `loudnorm=I=${loudness.integrated}:TP=${loudness.truePeak}:LRA=${loudness.range}${measured
    ? `:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}:linear=true`
    : ":print_format=json"}`;
  return [
    `[0:a:0]aresample=${SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,adelay=${Math.round(lead * 1000)}:all=1,apad=whole_dur=${seconds}[fx]`,
    `[2:a:0]atrim=start=${musicStart}:duration=${seconds},asetpts=PTS-STARTPTS,aresample=${SAMPLE_RATE},aformat=sample_fmts=fltp:channel_layouts=stereo,`
      + `volume='${UNDER_GAIN}+${1 - UNDER_GAIN}*clip((t-${rise})/1,0,1)':eval=frame,afade=t=in:d=${Math.max(lead, 0.3)},afade=t=out:st=${seconds - 1.5}:d=1.5,apad=whole_dur=${seconds}[music]`,
    `[fx][music]amix=inputs=2:duration=first:normalize=0,atrim=end_sample=${frames * (SAMPLE_RATE / FPS)},${norm},aresample=${SAMPLE_RATE}[a]`,
  ].join(";");
}

function inputs({ base, last, music, layers }) {
  return [
    "-i", base,
    "-i", last,
    "-i", music,
    "-i", layers.teal.at(-1),
    "-i", layers.brown.at(-1),
    "-i", layers.fill.at(-1),
    "-i", layers.stroke.at(-1),
  ];
}

/** First pass: measure the mixed sound only. */
export function measureArgs({ base, last, music, layers, musicStart }) {
  return ["-hide_banner", "-nostats", ...inputs({ base, last, music, layers }), "-filter_complex", audioFilter({ musicStart }), "-map", "[a]", "-f", "null", "-"];
}

/** Second pass: the outro, encoded like an ordinary scene so the join copies it cleanly. */
export function outroArgs({ base, last, music, layers, musicStart, measured, outFile }) {
  return [
    "-hide_banner", "-y", "-loglevel", "error",
    ...inputs({ base, last, music, layers }),
    "-filter_complex", `${videoFilter()};${audioFilter({ musicStart, measured })}`,
    "-map", "[v]", "-map", "[a]",
    "-frames:v", String(OUTRO_FRAMES),
    "-c:v", "libx264", "-profile:v", "high", "-preset", "medium", "-crf", "16",
    "-x264-params", "colorprim=bt709:transfer=bt709:colormatrix=bt709",
    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv",
    "-r", String(FPS), "-fps_mode", "cfr",
    "-c:a", "aac", "-b:a", "384k", "-ar", String(SAMPLE_RATE), "-ac", "2",
    "-movflags", "+faststart", outFile,
  ];
}

export function lastFrameArgs(base, outFile, baseFrames = BASE_FRAMES) {
  return ["-hide_banner", "-y", "-loglevel", "error", "-i", base, "-vf", `select='eq(n,${baseFrames - 1})'`, "-frames:v", "1", outFile];
}

/** The manifest `branding --install` reads (docs/videos/BRANDING.md). */
export function packageManifest({ id, intro, outro, music }) {
  return {
    schema_version: 1,
    package_id: id,
    assets: [
      { role: "intro", file: "intro.mp4", frames: intro.frames, sha256: intro.sha256 },
      { role: "outro", file: "outro.mp4", frames: OUTRO_FRAMES, sha256: outro.sha256 },
    ],
    // Provenance only: the installer trusts the files and their hashes, not these fields.
    outro_source: { base_sha256: outro.base_sha256, lead_frames: LEAD_FRAMES, base_frames: BASE_FRAMES, music: music.name, music_sha256: music.sha256, music_start_seconds: music.start, end_screen_slots: SLOTS },
  };
}

async function framesOf(tools, exec, file) {
  const probe = JSON.parse((await exec(tools.ffprobe, probeArgs(file))).stdout);
  return Number(probe.streams?.find((stream) => stream.codec_type === "video")?.nb_read_packets);
}

export async function buildOutro({ base, music, musicStart, intros, out, tools, exec = runTool }) {
  for (const file of [base, music, ...Object.values(intros)]) if (!existsSync(file)) throw new UsageError(`missing input: ${file}`);
  if (await framesOf(tools, exec, base) !== BASE_FRAMES) throw new UsageError(`--base must be the ${BASE_FRAMES}-frame like/share/bell outro`);
  const work = path.join(out, "build");
  mkdirSync(work, { recursive: true });
  const layers = layerPlan(work);
  for (const args of Object.values(layers)) await exec(tools.ffmpeg, args);
  const last = path.join(work, "last.png");
  await exec(tools.ffmpeg, lastFrameArgs(base, last));
  const measured = parseLoudnorm((await exec(tools.ffmpeg, measureArgs({ base, last, music, layers, musicStart }))).stderr);
  const outro = path.join(work, "outro.mp4");
  await exec(tools.ffmpeg, outroArgs({ base, last, music, layers, musicStart, measured, outFile: outro }));
  const frames = await framesOf(tools, exec, outro);
  if (frames !== OUTRO_FRAMES) throw new UsageError(`the outro came out ${frames} frames, not ${OUTRO_FRAMES}`);
  const outroRecord = { sha256: await sha256File(outro), base_sha256: await sha256File(base) };
  const musicRecord = { name: path.basename(music), sha256: await sha256File(music), start: musicStart };
  const packages = {};
  for (const [name, intro] of Object.entries(intros)) {
    const dir = path.join(out, name);
    mkdirSync(dir, { recursive: true });
    copyFileSync(intro, path.join(dir, "intro.mp4"));
    copyFileSync(outro, path.join(dir, "outro.mp4"));
    const manifest = packageManifest({ id: PACKAGES[name].id, intro: { frames: await framesOf(tools, exec, intro), sha256: await sha256File(intro) }, outro: outroRecord, music: musicRecord });
    atomicWrite(path.join(dir, "manifest.json"), `${JSON.stringify(manifest, null, 2)}\n`);
    packages[name] = { dir, manifest };
  }
  return { outro, measured, packages };
}

export async function main(argv = process.argv.slice(2), { stdout = process.stdout } = {}) {
  const { values } = parseArgs({ args: argv, options: {
    base: { type: "string" }, music: { type: "string" }, "music-start": { type: "string" },
    intro: { type: "string" }, "series-intro": { type: "string" }, out: { type: "string" },
  }, strict: true });
  if (!values.base || !values.music || !values.intro || !values.out) throw new UsageError("outro needs --base, --music, --intro and --out");
  const intros = { channel: path.resolve(values.intro), ...(values["series-intro"] ? { sothatswhy: path.resolve(values["series-intro"]) } : {}) };
  const tools = await locateFfmpeg();
  const result = await buildOutro({ base: path.resolve(values.base), music: path.resolve(values.music), musicStart: Number(values["music-start"] ?? 0), intros, out: path.resolve(values.out), tools });
  stdout.write(`outro: ${result.outro} (${OUTRO_FRAMES} frames)\n`);
  for (const [name, { dir, manifest }] of Object.entries(result.packages)) stdout.write(`${name}: ${dir} ${manifest.package_id}\n`);
  stdout.write("next: node tools/video/cli.mjs branding --install <package> --workdir <work> --dry-run\n");
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main().catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exitCode = error instanceof UsageError ? 2 : 1;
  });
}
