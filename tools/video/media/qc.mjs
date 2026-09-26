// Automatic quality checks on generated clips and pictures, as pure functions over ffmpeg output.
//
// The checks the reference genre's viewers notice: a clip that freezes or goes black, a model
// that cut inside a shot, a first frame that is not the keyframe it was asked to animate, two
// near-identical keyframes in a row. The judge (a vision model on the server) covers what
// ffmpeg cannot: identity against the sheet, deformed hands, text. Thresholds live here so a
// pilot can calibrate them in one place.
export const THRESHOLDS = {
  // A clip may be up to a quarter second shorter than asked; the fit stage pads the rest.
  duration_slack_s: 0.25,
  min_width: 1280,
  min_height: 720,
  min_fps: 23,
  black_min_s: 0.3,
  black_picture_threshold: 0.98,
  freeze_noise: 0.003,
  freeze_min_s: 1.0,
  scene_cut: 0.5,
  // First frame against the keyframe: above CLEAR it is the keyframe; below MIN it is not.
  keyframe_clear_psnr: 30,
  keyframe_min_psnr: 22,
  keyframe_margin_db: 3,
  // Adjacent keyframes whose dHash differs in fewer bits than this read as the same picture.
  duplicate_hamming: 8,
};

/** ffprobe: the streams and the frame count of a clip. */
export function probeArgs(file) {
  return ["-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries", "stream=codec_name,width,height,r_frame_rate,avg_frame_rate,nb_read_packets,duration:format=duration", "-of", "json", file];
}

export function blackdetectArgs(file, thresholds = THRESHOLDS) {
  return ["-hide_banner", "-nostats", "-i", file, "-vf", `blackdetect=d=${thresholds.black_min_s}:pic_th=${thresholds.black_picture_threshold}`, "-an", "-f", "null", "-"];
}

export function freezedetectArgs(file, thresholds = THRESHOLDS) {
  return ["-hide_banner", "-nostats", "-i", file, "-vf", `freezedetect=n=${thresholds.freeze_noise}:d=${thresholds.freeze_min_s}`, "-an", "-f", "null", "-"];
}

export function sceneCutArgs(file, thresholds = THRESHOLDS) {
  return ["-hide_banner", "-nostats", "-i", file, "-vf", `select='gt(scene,${thresholds.scene_cut})',showinfo`, "-an", "-f", "null", "-"];
}

/** PSNR of a clip's frame `n` against an image, both scaled to the clip's size. */
export function framePsnrArgs(clip, n, image, width, height) {
  return ["-hide_banner", "-nostats", "-i", clip, "-i", image, "-lavfi", `[0:v]select=eq(n\\,${n}),scale=${width}:${height},format=rgb24[a];[1:v]scale=${width}:${height},format=rgb24[b];[a][b]psnr`, "-frames:v", "1", "-f", "null", "-"];
}

/** The 9×8 grey pixels of an image, for dHash. */
export function dhashArgs(image) {
  return ["-hide_banner", "-loglevel", "error", "-i", image, "-vf", "scale=9:8:flags=area,format=gray", "-frames:v", "1", "-f", "rawvideo", "-"];
}

/** A clip's shape from ffprobe's JSON: `{ width, height, fps, frames, duration }`. */
export function parseProbe(json) {
  const data = typeof json === "string" ? JSON.parse(json) : json;
  const stream = data.streams?.[0] ?? {};
  const rate = String(stream.avg_frame_rate || stream.r_frame_rate || "0/1");
  const [num, den] = rate.split("/").map(Number);
  const fps = den ? num / den : Number(num) || 0;
  const duration = Number(stream.duration ?? data.format?.duration ?? 0);
  return { codec: stream.codec_name ?? "", width: Number(stream.width) || 0, height: Number(stream.height) || 0, fps, frames: Number(stream.nb_read_packets) || 0, duration };
}

const intervals = (stderr, startKey, endKey) => {
  const found = [];
  const pattern = new RegExp(`${startKey}:\\s*([\\d.]+)[^\\n]*?${endKey}:\\s*([\\d.]+)`, "g");
  for (const match of stderr.matchAll(pattern)) found.push({ start: Number(match[1]), end: Number(match[2]) });
  return found;
};

/** `[{ start, end }]` of black intervals from blackdetect's log. */
export function parseBlackdetect(stderr) {
  return intervals(String(stderr), "black_start", "black_end");
}

/** `[{ start, end }]` of frozen intervals from freezedetect's log; an unclosed freeze ends at `duration`. */
export function parseFreezedetect(stderr, duration = Infinity) {
  const text = String(stderr);
  const starts = [...text.matchAll(/freeze_start:\s*([\d.]+)/g)].map((match) => Number(match[1]));
  const ends = [...text.matchAll(/freeze_end:\s*([\d.]+)/g)].map((match) => Number(match[1]));
  return starts.map((start, index) => ({ start, end: ends[index] ?? duration }));
}

/** The times (seconds) at which the scene filter saw a cut, from showinfo's log. */
export function parseSceneCuts(stderr) {
  return [...String(stderr).matchAll(/pts_time:\s*([\d.]+)/g)].map((match) => Number(match[1]));
}

export function parsePsnr(stderr) {
  const match = /PSNR .*average:(inf|[\d.]+)/.exec(String(stderr));
  if (!match) return null;
  return match[1] === "inf" ? Infinity : Number(match[1]);
}

/** A 64-bit difference hash of 9×8 grey pixels, as 16 hex characters. */
export function dHash(pixels) {
  const bytes = Buffer.isBuffer(pixels) ? pixels : Buffer.from(pixels);
  if (bytes.length < 72) throw new Error(`dHash needs 72 grey pixels, got ${bytes.length}`);
  let bits = "";
  for (let row = 0; row < 8; row++) {
    for (let column = 0; column < 8; column++) {
      bits += bytes[row * 9 + column] < bytes[row * 9 + column + 1] ? "1" : "0";
    }
  }
  return BigInt(`0b${bits}`).toString(16).padStart(16, "0");
}

export function hamming(a, b) {
  let distance = 0;
  let x = BigInt(`0x${a}`) ^ BigInt(`0x${b}`);
  while (x) {
    distance += Number(x & 1n);
    x >>= 1n;
  }
  return distance;
}

/**
 * The verdict on one clip: `{ ok, problems: [...], metrics }`. `needed_s` is how long the shot's
 * narration is; a freeze inside that window, a black interval, a cut, a wrong shape, a first
 * frame that is not the keyframe, or a failed judge all fail the clip.
 */
export function clipVerdict({ probe, requested_s: requested, needed_s: needed, black = [], freezes = [], cuts = [], keyframe_psnr: psnr = null, rival_psnr: rival = null, judge = null }, thresholds = THRESHOLDS) {
  const problems = [];
  if (probe.width < thresholds.min_width || probe.height < thresholds.min_height) problems.push(`the clip is ${probe.width}x${probe.height}; at least ${thresholds.min_width}x${thresholds.min_height} is needed`);
  if (probe.fps < thresholds.min_fps) problems.push(`the clip runs at ${probe.fps.toFixed(2)} fps`);
  if (requested && probe.duration < requested - thresholds.duration_slack_s) problems.push(`the clip lasts ${probe.duration.toFixed(2)} s, ${requested} s were asked for`);
  if (black.length) problems.push(`black from ${black[0].start.toFixed(2)} s to ${black[0].end.toFixed(2)} s`);
  const window = needed ?? probe.duration;
  const frozen = freezes.filter((freeze) => freeze.start < window && freeze.end - freeze.start >= thresholds.freeze_min_s);
  if (frozen.length) problems.push(`frozen from ${frozen[0].start.toFixed(2)} s to ${Math.min(frozen[0].end, window).toFixed(2)} s inside the narrated part`);
  const inside = cuts.filter((time) => time > 0.1);
  if (inside.length) problems.push(`the model cut at ${inside[0].toFixed(2)} s; a shot must be one continuous take`);
  if (psnr !== null) {
    if (psnr < thresholds.keyframe_min_psnr) problems.push(`the first frame does not show the keyframe (PSNR ${psnr.toFixed(1)} dB)`);
    else if (psnr < thresholds.keyframe_clear_psnr && rival !== null && psnr - rival < thresholds.keyframe_margin_db) problems.push(`the first frame looks as much like a neighbouring keyframe (${rival.toFixed(1)} dB) as its own (${psnr.toFixed(1)} dB)`);
  }
  if (judge && judge.passed === false) problems.push(`judge ${judge.overall}/10: ${judge.problems?.join("; ") || "below the bar"}`);
  return { ok: problems.length === 0, problems, metrics: { width: probe.width, height: probe.height, fps: probe.fps, duration: probe.duration, black: black.length, freezes: frozen.length, cuts: inside.length, keyframe_psnr: psnr, judge: judge ? judge.overall : null } };
}

/** The verdict on one picture (a sheet or a keyframe): the judge's, plus a size check. */
export function pictureVerdict({ width, height, judge = null, min_width: minWidth = 1024, min_height: minHeight = 576 }) {
  const problems = [];
  if (width < minWidth || height < minHeight) problems.push(`the picture is ${width}x${height}; at least ${minWidth}x${minHeight} is needed`);
  if (judge && judge.passed === false) problems.push(`judge ${judge.overall}/10: ${judge.problems?.join("; ") || "below the bar"}`);
  return { ok: problems.length === 0, problems };
}

/** Adjacent pictures whose hashes are too close: `[{ a, b, distance }]`. */
export function duplicates(hashes, thresholds = THRESHOLDS) {
  const found = [];
  for (let index = 1; index < hashes.length; index++) {
    const distance = hamming(hashes[index - 1].hash, hashes[index].hash);
    if (distance < thresholds.duplicate_hamming) found.push({ a: hashes[index - 1].id, b: hashes[index].id, distance });
  }
  return found;
}
