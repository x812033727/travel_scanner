// A stand-in narration: a soft tone per line, as long as the line would take to say, laid on the
// frame grid exactly as the tts stage lays real speech. The smoke test and a local dry run of the
// assembly use it so neither needs the narration server or a video tool token.
import { writeFileSync } from "node:fs";
import path from "node:path";

import { buildTimeline, estimatedSamples, SAMPLE_RATE, SAMPLES_PER_FRAME, speechHash } from "../core/timeline.mjs";

function wav(samples) {
  const header = Buffer.alloc(44);
  header.write("RIFF", 0, "ascii");
  header.writeUInt32LE(36 + samples.length * 2, 4);
  header.write("WAVEfmt ", 8, "ascii");
  header.writeUInt32LE(16, 16);
  header.writeUInt16LE(1, 20);
  header.writeUInt16LE(1, 22);
  header.writeUInt32LE(SAMPLE_RATE, 24);
  header.writeUInt32LE(SAMPLE_RATE * 2, 28);
  header.writeUInt16LE(2, 32);
  header.writeUInt16LE(16, 34);
  header.write("data", 36, "ascii");
  header.writeUInt32LE(samples.length * 2, 40);
  return Buffer.concat([header, Buffer.from(samples.buffer, samples.byteOffset, samples.byteLength)]);
}

/** Write timeline.json and narration.wav for `doc` into `workdir`, as the tts stage would. */
export function writeSyntheticNarration(doc, lexicon, workdir) {
  const samplesById = estimatedSamples(doc);
  const timeline = { ...buildTimeline(doc, samplesById), speech_hash: speechHash(doc, lexicon) };
  const narration = new Int16Array(timeline.total_frames * SAMPLES_PER_FRAME);
  timeline.lines.forEach((placed, index) => {
    const start = placed.start_frame * SAMPLES_PER_FRAME;
    const pitch = 180 + (index % 5) * 40;
    for (let sample = 0; sample < placed.audio_samples; sample++) {
      const envelope = Math.min(1, sample / 2400, (placed.audio_samples - sample) / 2400);
      narration[start + sample] = Math.round(6000 * envelope * Math.sin((2 * Math.PI * pitch * sample) / SAMPLE_RATE));
    }
  });
  writeFileSync(path.join(workdir, "narration.wav"), wav(narration));
  writeFileSync(path.join(workdir, "timeline.json"), `${JSON.stringify(timeline, null, 2)}\n`);
  return timeline;
}
