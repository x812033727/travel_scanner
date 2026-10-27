// A sticker drama's pace (docs/videos/BINGE.md §畫面等級): a take read slower than the form wants is
// sped up after synthesis, without changing its pitch.
//
// Gemini voices have no rate (requests.mjs voiceFields: their pace is in the style), and a style
// asking for four to five characters a second read 3.8 on 系統說我是 BUG e001-redo1, its characters
// 2.7; the funny-dub references it was measured against speak 5.8–7.6 inside a sentence (ticket
// 2026-10-27-1-3-5-5-5). So the take is measured as the timeline counts it, spoken units
// (core/timeline.mjs spokenUnits) over the trimmed clip's seconds, and one under its speaker's
// floor goes through ffmpeg's atempo by as much as reaches the floor, at most MAX_TEMPO: past
// that a voice stops sounding like one.
import { spawnSync } from "node:child_process";

import { locateFfmpeg } from "../assemble/ffmpeg.mjs";
import { NARRATOR } from "../core/drama.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { encodeWav, parseWav, requireNarrationFormat } from "./wav.mjs";

export const NARRATOR_MIN_RATE = 5.5;
export const CHARACTER_MIN_RATE = 4.5;
export const MAX_TEMPO = 1.35;
// A line this short is an interjection, whose length is its performance: it is left as read.
export const TEMPO_MIN_UNITS = 4;

const hundredths = (value) => Math.round(value * 100) / 100;

/**
 * How fast a take is read and how much to speed it up: { rate, target, factor }, the rate in
 * spoken units a second and the factor 1 when the take is fast enough (or too short to judge).
 * The factor is rounded up to hundredths, so a sped take reaches its floor unless MAX_TEMPO stops it.
 */
export function tempoFor({ units, samples, speaker }) {
  const target = speaker === NARRATOR ? NARRATOR_MIN_RATE : CHARACTER_MIN_RATE;
  const rate = units / (Math.max(1, samples) / SAMPLE_RATE);
  if (units < TEMPO_MIN_UNITS || rate >= target) return { rate: hundredths(rate), target, factor: 1 };
  // Less a hair before rounding up, so 5.5 / 5 = 1.1000000000000001 stays 1.1.
  return { rate: hundredths(rate), target, factor: Math.min(MAX_TEMPO, Math.ceil((target / rate) * 100 - 1e-9) / 100) };
}

/** A take's character timing on its sped clip: every time divided by the factor, within the clip. */
export function scaledTiming(timing, factor, samples) {
  if (!timing) return null;
  const length = Math.floor((samples * 1000) / SAMPLE_RATE);
  const at = (ms) => Math.min(length, Math.round(ms / factor));
  return { ...timing, chars: timing.chars.map((char) => ({ ...char, start_ms: at(char.start_ms), end_ms: at(char.end_ms) })) };
}

/**
 * `atempo(clip, factor)` through the ffmpeg the assembly uses (assemble/ffmpeg.mjs), found once:
 * 48 kHz 16-bit mono in and out, so the sped clip sits on the timeline like any take.
 */
export function ffmpegAtempo(env = process.env) {
  let located = null;
  return async (clip, factor) => {
    located ??= await locateFfmpeg(env);
    const args = ["-hide_banner", "-loglevel", "error", "-f", "wav", "-i", "pipe:0", "-filter:a", `atempo=${factor}`, "-map_metadata", "-1", "-fflags", "+bitexact", "-flags:a", "+bitexact", "-ac", "1", "-ar", String(SAMPLE_RATE), "-c:a", "pcm_s16le", "-f", "wav", "pipe:1"];
    const result = spawnSync(located.ffmpeg, args, { input: encodeWav(clip), maxBuffer: 256 * 1024 * 1024, windowsHide: true });
    if (result.status !== 0) {
      const tail = String(result.stderr ?? result.error?.message ?? "").trim().split("\n").slice(-6).join("\n");
      throw new Error(`ffmpeg atempo=${factor} failed: ${tail}`);
    }
    return requireNarrationFormat(parseWav(result.stdout));
  };
}
