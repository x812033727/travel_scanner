// 48 kHz 16-bit mono PCM WAV: what the narration server returns and what the timeline is built on.
//
// Only the parts of RIFF the pipeline needs: find "fmt " and "data", check the format, and write a
// plain 44-byte header back. A clip's length is its sample count, never a duration from a decoder.
import { SAMPLE_RATE } from "../core/timeline.mjs";

export class WavError extends Error {}

/** Parse a RIFF/WAVE buffer into its format and 16-bit samples. */
export function parseWav(buffer) {
  const bytes = Buffer.isBuffer(buffer) ? buffer : Buffer.from(buffer);
  if (bytes.length < 12 || bytes.toString("ascii", 0, 4) !== "RIFF" || bytes.toString("ascii", 8, 12) !== "WAVE") {
    throw new WavError("not a RIFF/WAVE file");
  }
  let format = null;
  let offset = 12;
  while (offset + 8 <= bytes.length) {
    const id = bytes.toString("ascii", offset, offset + 4);
    let size = bytes.readUInt32LE(offset + 4);
    const start = offset + 8;
    if (id === "fmt ") {
      format = {
        audioFormat: bytes.readUInt16LE(start),
        channels: bytes.readUInt16LE(start + 2),
        sampleRate: bytes.readUInt32LE(start + 4),
        bitsPerSample: bytes.readUInt16LE(start + 14),
      };
    } else if (id === "data") {
      if (!format) throw new WavError("data chunk before fmt chunk");
      // A streamed response may leave the size at 0 or 0xFFFFFFFF: take the rest of the file.
      if (size === 0 || size === 0xffffffff || start + size > bytes.length) size = bytes.length - start;
      const usable = size - (size % 2);
      const copy = new Int16Array(usable / 2);
      for (let index = 0; index < copy.length; index++) copy[index] = bytes.readInt16LE(start + index * 2);
      return { ...format, samples: copy };
    }
    offset = start + size + (size % 2);
  }
  throw new WavError("no data chunk");
}

/** Refuse anything the timeline cannot place on its 1,600-samples-a-frame grid. */
export function requireNarrationFormat(wav) {
  const problems = [];
  if (wav.audioFormat !== 1 && wav.audioFormat !== 0xfffe) problems.push(`audio format ${wav.audioFormat}, expected PCM`);
  if (wav.channels !== 1) problems.push(`${wav.channels} channels, expected mono`);
  if (wav.sampleRate !== SAMPLE_RATE) problems.push(`${wav.sampleRate} Hz, expected ${SAMPLE_RATE}`);
  if (wav.bitsPerSample !== 16) problems.push(`${wav.bitsPerSample}-bit, expected 16-bit`);
  if (problems.length) throw new WavError(problems.join("; "));
  return wav.samples;
}

export function encodeWav(samples, sampleRate = SAMPLE_RATE) {
  const header = Buffer.alloc(44);
  const dataBytes = samples.length * 2;
  header.write("RIFF", 0, "ascii");
  header.writeUInt32LE(36 + dataBytes, 4);
  header.write("WAVE", 8, "ascii");
  header.write("fmt ", 12, "ascii");
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(1, 22);
  header.writeUInt32LE(sampleRate, 24);
  header.writeUInt32LE(sampleRate * 2, 28);
  header.writeUInt16LE(2, 32);
  header.writeUInt16LE(16, 34);
  header.write("data", 36, "ascii");
  header.writeUInt32LE(dataBytes, 40);
  const body = Buffer.alloc(dataBytes);
  for (let index = 0; index < samples.length; index++) body.writeInt16LE(samples[index], index * 2);
  return Buffer.concat([header, body]);
}

// Zero crossings of the interpolating sinc on each side. 16 keeps the passband flat to about
// 90% of the source Nyquist frequency (10.8 kHz for 24 kHz speech), which is all a voice uses.
const HALF_WIDTH = 16;

/**
 * Upsample by a whole factor with a Blackman-windowed sinc, one filter row per output phase.
 * Every row sums to one and phase 0 is the identity, so the original samples come through
 * unchanged and silence stays silence.
 */
export function upsample(samples, factor) {
  if (!Number.isInteger(factor) || factor < 1) throw new WavError(`cannot upsample by ${factor}`);
  if (factor === 1) return samples;
  const taps = 2 * HALF_WIDTH;
  const rows = [];
  for (let phase = 0; phase < factor; phase++) {
    const row = new Float64Array(taps);
    let sum = 0;
    for (let index = 0; index < taps; index++) {
      const distance = phase / factor - (index - HALF_WIDTH + 1);
      const sinc = distance === 0 ? 1 : Math.sin(Math.PI * distance) / (Math.PI * distance);
      const x = distance / HALF_WIDTH;
      const window = Math.abs(x) >= 1 ? 0 : 0.42 + 0.5 * Math.cos(Math.PI * x) + 0.08 * Math.cos(2 * Math.PI * x);
      row[index] = sinc * window;
      sum += row[index];
    }
    for (let index = 0; index < taps; index++) row[index] /= sum;
    rows.push(row);
  }
  const out = new Int16Array(samples.length * factor);
  const last = samples.length - 1;
  for (let at = 0; at < samples.length; at++) {
    for (let phase = 0; phase < factor; phase++) {
      const row = rows[phase];
      let value = 0;
      for (let index = 0; index < taps; index++) {
        const source = at + index - HALF_WIDTH + 1;
        if (source >= 0 && source <= last) value += samples[source] * row[index];
      }
      out[at * factor + phase] = Math.max(-32768, Math.min(32767, Math.round(value)));
    }
  }
  return out;
}

/**
 * Downsample by a whole factor: a Blackman-windowed sinc low-pass at the new Nyquist frequency,
 * then every factor-th sample. Used to send clips for transcription at a third of the size.
 */
export function downsample(samples, factor) {
  if (!Number.isInteger(factor) || factor < 1) throw new WavError(`cannot downsample by ${factor}`);
  if (factor === 1) return samples;
  const half = HALF_WIDTH * factor;
  const taps = new Float64Array(2 * half + 1);
  let sum = 0;
  for (let offset = -half; offset <= half; offset++) {
    const t = offset / factor;
    const sinc = t === 0 ? 1 : Math.sin(Math.PI * t) / (Math.PI * t);
    const x = offset / half;
    taps[offset + half] = sinc * (0.42 + 0.5 * Math.cos(Math.PI * x) + 0.08 * Math.cos(2 * Math.PI * x));
    sum += taps[offset + half];
  }
  for (let index = 0; index < taps.length; index++) taps[index] /= sum;
  const out = new Int16Array(Math.floor(samples.length / factor));
  for (let at = 0; at < out.length; at++) {
    const center = at * factor;
    let value = 0;
    for (let offset = -half; offset <= half; offset++) {
      const source = center - offset;
      if (source >= 0 && source < samples.length) value += samples[source] * taps[offset + half];
    }
    out[at] = Math.max(-32768, Math.min(32767, Math.round(value)));
  }
  return out;
}

/**
 * A server WAV on the narration grid. Gemini speaks at 24 kHz; the timeline is 48 kHz, so a mono
 * 16-bit clip at a rate that divides 48,000 is upsampled. Anything else is returned as is, for
 * `requireNarrationFormat` to refuse with a clear message.
 */
export function toNarrationRate(buffer) {
  const wav = parseWav(buffer);
  if (wav.sampleRate === SAMPLE_RATE) return buffer;
  if (wav.channels !== 1 || wav.bitsPerSample !== 16 || wav.sampleRate < 8000 || SAMPLE_RATE % wav.sampleRate !== 0) return buffer;
  return encodeWav(upsample(wav.samples, SAMPLE_RATE / wav.sampleRate));
}

export function concatSamples(parts) {
  const total = parts.reduce((sum, part) => sum + part.length, 0);
  const out = new Int16Array(total);
  let offset = 0;
  for (const part of parts) {
    out.set(part, offset);
    offset += part.length;
  }
  return out;
}
