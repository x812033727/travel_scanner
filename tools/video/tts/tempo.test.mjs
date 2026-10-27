import assert from "node:assert/strict";
import test from "node:test";

import { locateFfmpeg } from "../assemble/ffmpeg.mjs";
import { NARRATOR } from "../core/drama.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { CHARACTER_MIN_RATE, MAX_TEMPO, NARRATOR_MIN_RATE, TEMPO_MIN_UNITS, ffmpegAtempo, scaledTiming, tempoFor } from "./tempo.mjs";

const seconds = (value) => Math.round(value * SAMPLE_RATE);

test("only a take slower than its speaker's floor is sped up, by enough to reach it and never past MAX_TEMPO", () => {
  assert.deepEqual([NARRATOR_MIN_RATE, CHARACTER_MIN_RATE, MAX_TEMPO], [5.5, 4.5, 1.35]);
  // The narrator of e001-redo1 read 3.8 a second: capped. 5 a second needs 1.1×.
  assert.deepEqual(tempoFor({ units: 19, samples: seconds(5), speaker: NARRATOR }), { rate: 3.8, target: 5.5, factor: MAX_TEMPO });
  assert.deepEqual(tempoFor({ units: 20, samples: seconds(4), speaker: NARRATOR }), { rate: 5, target: 5.5, factor: 1.1 });
  // At or above the floor nothing changes; a character's floor is lower than the narrator's.
  assert.equal(tempoFor({ units: 22, samples: seconds(4), speaker: NARRATOR }).factor, 1);
  assert.equal(tempoFor({ units: 30, samples: seconds(5), speaker: NARRATOR }).factor, 1);
  assert.deepEqual(tempoFor({ units: 20, samples: seconds(4), speaker: "jiang" }), { rate: 5, target: 4.5, factor: 1 });
  assert.deepEqual(tempoFor({ units: 16, samples: seconds(4), speaker: "jiang" }), { rate: 4, target: 4.5, factor: 1.13 });
  // Rounded up: the sped take reaches its floor.
  const { rate, factor } = tempoFor({ units: 17, samples: seconds(3.3), speaker: NARRATOR });
  assert.ok(factor > 1 && factor < MAX_TEMPO && rate * factor >= NARRATOR_MIN_RATE - 0.01, `${rate} × ${factor}`);
  // An interjection is left as read, however long it is drawn out.
  assert.equal(tempoFor({ units: TEMPO_MIN_UNITS - 1, samples: seconds(3), speaker: NARRATOR }).factor, 1);
});

test("a sped take's character times shrink with it and stay inside the clip", () => {
  const timing = { source: "azure", model: "v", chars: [{ text: "好", start_ms: 0, end_ms: 270 }, { text: "啊", start_ms: 270, end_ms: 1350 }] };
  assert.deepEqual(scaledTiming(timing, 1.35, seconds(0.9)), { source: "azure", model: "v", chars: [{ text: "好", start_ms: 0, end_ms: 200 }, { text: "啊", start_ms: 200, end_ms: 900 }] });
  assert.equal(scaledTiming(null, 1.2, 100), null);
});

test("atempo through ffmpeg shortens a take by its factor and keeps it 48 kHz mono", async (t) => {
  try {
    await locateFfmpeg();
  } catch {
    t.skip("no ffmpeg here");
    return;
  }
  const clip = Int16Array.from({ length: seconds(2) }, (_, index) => Math.round(8000 * Math.sin((2 * Math.PI * 220 * index) / SAMPLE_RATE)));
  const sped = await ffmpegAtempo()(clip, 1.25);
  assert.ok(sped instanceof Int16Array);
  assert.ok(Math.abs(sped.length - clip.length / 1.25) < SAMPLE_RATE * 0.05, `${sped.length} samples`);
});
