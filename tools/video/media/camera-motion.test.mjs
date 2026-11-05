// Camera-move measurement on synthetic clips whose move is known: a still, a push, a pull, pans,
// a tilt, and a locked shot with a large object crossing it (subject motion is not camera motion).
import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { mkdtempSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test, { after, before } from "node:test";
import { THRESHOLDS, classify, compareMove, expectedMove, measureClip, pairMotion, summarize } from "./camera-motion.mjs";

const FFMPEG = process.env.FFMPEG || "ffmpeg";
const HAVE_FFMPEG = spawnSync(FFMPEG, ["-version"]).status === 0;
let dir;
const clips = {};

// 5 s at 24 fps, 640x360, all cut from one textured 1920x1080 still so every move has detail.
const MOVES = {
  locked: "crop=1280:720:320:180,scale=640:360",
  push: "zoompan=z='1+0.18*on/120':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=640x360:fps=24",
  pull: "zoompan=z='1.18-0.18*on/120':d=1:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=640x360:fps=24",
  pan_right: "crop=1280:720:x='120+t*50':y=180,scale=640:360",
  pan_left: "crop=1280:720:x='520-t*50':y=180,scale=640:360",
  tilt_down: "crop=1280:720:x=320:y='40+t*45',scale=640:360",
  // A locked frame with a quarter-width box crossing it left to right.
  crossing: "crop=1280:720:320:180,scale=640:360,drawbox=x='-160+t*160':y=90:w=160:h=180:color=red@1:t=fill",
  // Barely moving: a 0.5% drift, inside what a locked shot may do.
  creep: "crop=1280:720:x='320+t*1.3':y=180,scale=640:360",
};

before(() => {
  if (!HAVE_FFMPEG) return;
  dir = mkdtempSync(path.join(tmpdir(), "camera-motion-"));
  const still = path.join(dir, "still.png");
  assert.equal(spawnSync(FFMPEG, ["-v", "error", "-f", "lavfi", "-i", "mandelbrot=s=1920x1080:maxiter=300", "-frames:v", "1", still]).status, 0);
  for (const [name, filter] of Object.entries(MOVES)) {
    const out = path.join(dir, `${name}.mp4`);
    const made = spawnSync(FFMPEG, ["-v", "error", "-loop", "1", "-framerate", "24", "-t", "5", "-i", still, "-vf", filter, "-frames:v", "120", "-pix_fmt", "yuv420p", "-c:v", "libx264", "-crf", "18", out]);
    assert.equal(made.status, 0, String(made.stderr));
    clips[name] = out;
  }
});

after(() => {
  if (dir) rmSync(dir, { recursive: true, force: true });
});

test("each synthetic move is measured as itself", { skip: !HAVE_FFMPEG && "ffmpeg is not installed" }, () => {
  const expected = {
    locked: { move: "locked" },
    push: { move: "push" },
    pull: { move: "pull" },
    pan_right: { move: "pan", direction: "right" },
    pan_left: { move: "pan", direction: "left" },
    tilt_down: { move: "tilt", direction: "down" },
    crossing: { move: "locked" },
    creep: { move: "locked" },
  };
  for (const [name, want] of Object.entries(expected)) {
    const report = measureClip(clips[name]);
    assert.deepEqual(report.measured, want, `${name}: ${JSON.stringify(report.summary)}`);
  }
  const push = measureClip(clips.push).summary;
  assert.ok(push.zoom > 1.1 && push.zoom < 1.3, `push total zoom ${push.zoom} is near 1.18`);
});

test("the measured move is compared with what craft reads from the camera field", { skip: !HAVE_FFMPEG && "ffmpeg is not installed" }, () => {
  assert.deepEqual(measureClip(clips.push, { shot: { camera: "Close-up, slow push in" } }).problems, []);
  assert.deepEqual(measureClip(clips.pan_right, { shot: { camera: "Wide shot, pans left" } }).problems, ["asked to pan left, the clip went right"]);
  assert.deepEqual(measureClip(clips.push, { shot: { camera: "Medium shot, locked" } }).problems, ["a locked shot moved (push)"]);
  assert.deepEqual(measureClip(clips.locked, { shot: { camera: "Medium close-up, slow push in" } }).problems, ["asked to push, the clip stayed still"]);
});

test("expectedMove reads craft's move and a named direction; untracked moves are not judged", () => {
  assert.deepEqual(expectedMove({ camera: "Wide shot, slow pan right" }), { move: "pan", direction: "right" });
  assert.deepEqual(expectedMove({ camera: "Crane up over the courtyard" }), { move: "tilt", direction: "up" });
  assert.deepEqual(expectedMove({ camera: "Medium shot, locked" }), { move: "locked", direction: null });
  assert.deepEqual(compareMove({ move: "track", direction: null }, { move: "pan", direction: "left" }), []);
  assert.deepEqual(compareMove({ move: "none", direction: null }, { move: "push" }), []);
});

test("the fit ignores a minority of blocks that move on their own", () => {
  // Twenty blocks on a 2 px pan to the left and six on a fast object going right.
  const vectors = [];
  for (let i = 0; i < 20; i++) vectors.push({ x: 20 + (i % 5) * 60, y: 20 + Math.floor(i / 5) * 40, u: -2, v: 0 });
  for (let i = 0; i < 6; i++) vectors.push({ x: 150 + i * 5, y: 90, u: 8, v: 1 });
  const pair = pairMotion(vectors, THRESHOLDS);
  assert.ok(Math.abs(pair.dx + 2) < 0.2 && Math.abs(pair.scale - 1) < 0.01, JSON.stringify(pair));
  const summary = summarize([pair, pair, pair], THRESHOLDS);
  assert.ok(Math.abs(summary.pan - 6 / THRESHOLDS.width) < 0.002);
  // A push toward a face above the centre slides the picture too: still a push, the slide noted.
  assert.deepEqual(classify({ zoom: 1.08, pan: 0, tilt: -0.05 }), { move: "push", also: ["tilt up"] });
  assert.deepEqual(classify({ zoom: 1.0, pan: 0.05, tilt: 0.05 }), { move: "mixed" });
  // Between the locked allowance (1.5%) and a deliberate pan (3%): drift.
  assert.deepEqual(classify({ zoom: 1.0, pan: 0.02, tilt: 0 }), { move: "drift" });
  assert.deepEqual(classify({ zoom: 1.0, pan: 0.01, tilt: 0 }), { move: "locked" });
});
