// Pitch-preserving speech speedup (`voice.tempo`, 1 to 1.5) for `tts` and `audition`, using the
// same ffmpeg `atempo` filter and 48 kHz 16-bit mono PCM format that `dubs/encode.mjs` uses.
//
// `tempo` is never below 1 (core/schema.mjs VOICE_TEMPO_MIN), so it can only shorten clips and
// tighten speaking pace — never pad a thin script over the eight-minute floor.
import { createHash } from "node:crypto";
import { rmSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";

import { UsageError } from "../core/paths.mjs";
import { VOICE_TEMPO_MAX, VOICE_TEMPO_MIN, eachLine, spokenText } from "../core/schema.mjs";
import { SAMPLE_RATE, samplesToMs } from "../core/timeline.mjs";
import { stretchArgs } from "../dubs/encode.mjs";
import { encodeWav, parseWav, requireNarrationFormat } from "./wav.mjs";

let tempCounter = 0;

/** Parse `--tempo` on the CLI; returns `null` for `1`, the numeric factor for `(1, 1.5]`. */
export function parseTempoFlag(raw) {
  const value = typeof raw === "string" && raw.trim() !== "" ? Number(raw) : NaN;
  if (!Number.isFinite(value) || value < VOICE_TEMPO_MIN || value > VOICE_TEMPO_MAX) {
    throw new UsageError(`--tempo must be a number from ${VOICE_TEMPO_MIN} to ${VOICE_TEMPO_MAX}`);
  }
  return value > 1 ? value : null;
}

/** The 1x clip key for a line (`[voiceFields, parts]`), independent of `voice.tempo`. */
export function rawClipKey(request, line) {
  const { segments: _segments, ...voice } = request.body;
  return createHash("sha256").update(JSON.stringify([voice, line.parts])).digest("hex").slice(0, 16);
}

/**
 * Speed `wavBytes` up by `tempo` (`> 1`) with `ffmpeg -af atempo=<tempo>`, keeping pitch and
 * returning `{ samples, bytes }` as canonical 44-byte-header 48 kHz 16-bit mono PCM WAV.
 */
export async function stretchWavBytes(wavBytes, tempo, workDir, stem, ffmpeg) {
  const inputSamples = requireNarrationFormat(parseWav(wavBytes));
  if (!(tempo > 1) || inputSamples.length === 0) {
    const clean = encodeWav(inputSamples);
    return { samples: inputSamples, bytes: clean };
  }
  ffmpeg.tools ??= await ffmpeg.locate(ffmpeg.env);
  const nonce = `${process.pid}-${++tempCounter}`;
  const safeStem = String(stem).replace(/[^A-Za-z0-9_.-]/g, "-");
  const inFile = path.join(workDir, `.${safeStem}.${nonce}.in.wav`);
  const outFile = path.join(workDir, `.${safeStem}.${nonce}.out.wav`);
  try {
    writeFileSync(inFile, encodeWav(inputSamples));
    await ffmpeg.run(ffmpeg.tools.ffmpeg, stretchArgs(inFile, tempo, outFile));
    const samples = requireNarrationFormat(parseWav(readFileSync(outFile)));
    return { samples, bytes: encodeWav(samples) };
  } finally {
    rmSync(inFile, { force: true });
    rmSync(outFile, { force: true });
  }
}

/** Scale an aligned take's character boundaries (`start_ms`, `end_ms`) to a clip sped up by `tempo`. */
export function scaleTiming(timing, tempo, clipSamples) {
  if (!timing || !(tempo > 1)) return timing ?? null;
  const maxMs = Math.max(0, Math.floor(samplesToMs(clipSamples)));
  const scale = (ms) => Math.min(maxMs, Math.max(0, Math.round(ms / tempo)));
  return {
    source: timing.source,
    model: timing.model,
    chars: timing.chars.map((char) => {
      const start = scale(char.start_ms);
      return { text: char.text, start_ms: start, end_ms: Math.max(start, scale(char.end_ms)) };
    }),
  };
}

/**
 * Measured speaking pace matching the channel's `>= 4.4 字／秒` rule (curio-episode/SKILL.md):
 * spoken characters excluding whitespace and punctuation, divided by summed clip audio seconds.
 */
export function narrationPace(doc, clips) {
  let chars = 0;
  let samples = 0;
  for (const { line } of eachLine(doc)) {
    chars += [...String(spokenText(line)).replace(/[\s\p{P}\p{S}]/gu, "")].length;
    samples += clips.get(line.id)?.length ?? 0;
  }
  if (chars === 0 || samples <= 0) return null;
  const seconds = samples / SAMPLE_RATE;
  return { chars, seconds, charsPerSecond: chars / seconds };
}
