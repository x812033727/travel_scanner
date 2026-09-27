// The ffmpeg side of a dub: speeding a clip up, and turning the assembled track into the file
// the owner uploads. Loudness is handled exactly as final.mp4's audio is (assemble/plan.mjs):
// mono to stereo, two-pass loudnorm to -14 LUFS / -1 dBTP, so a viewer who switches tracks hears
// the same level.
import { LOUDNESS, measureLoudnessArgs, parseLoudnorm } from "../assemble/plan.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";

export { measureLoudnessArgs, parseLoudnorm };

const STEREO = "pan=stereo|c0=c0|c1=c0";
const loudnormFilter = (extra) => `loudnorm=I=${LOUDNESS.integrated}:TP=${LOUDNESS.truePeak}:LRA=${LOUDNESS.range}${extra}`;

/** A clip at `tempo` times its speed, pitch kept, still 48 kHz 16-bit mono. */
export function stretchArgs(inFile, tempo, outFile) {
  return ["-hide_banner", "-y", "-loglevel", "error", "-i", inFile, "-af", `atempo=${tempo}`, "-c:a", "pcm_s16le", "-ar", String(SAMPLE_RATE), "-ac", "1", outFile];
}

// What each upload format is encoded as. AAC in an .m4a is the video's own audio; MP3 and WAV are
// the fallbacks should YouTube Studio refuse it (docs/videos/DUBS.md).
const CODECS = {
  m4a: ["-c:a", "aac", "-b:a", "384k"],
  mp3: ["-c:a", "libmp3lame", "-b:a", "320k"],
  wav: ["-c:a", "pcm_s16le"],
};

/** Second loudnorm pass with the first pass's measurement, then the format's codec, stereo 48 kHz. */
export function encodeArgs(track, measured, outFile, format) {
  if (!Object.hasOwn(CODECS, format)) throw new Error(`unknown dub format ${format}`);
  const second = `:measured_I=${measured.input_i}:measured_TP=${measured.input_tp}:measured_LRA=${measured.input_lra}:measured_thresh=${measured.input_thresh}:offset=${measured.target_offset}:linear=true`;
  return [
    "-hide_banner", "-y", "-loglevel", "error", "-i", track,
    "-af", `${STEREO},${loudnormFilter(second)},aresample=${SAMPLE_RATE}`,
    ...CODECS[format], "-ar", String(SAMPLE_RATE), "-ac", "2", outFile,
  ];
}

export function probeArgs(file) {
  return ["-v", "error", "-show_entries", "stream=codec_name,sample_rate,channels:format=duration", "-of", "json", file];
}
