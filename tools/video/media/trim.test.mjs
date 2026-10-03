import assert from "node:assert/strict";
import test from "node:test";

import { ANALYSIS, grayArgs, marginCrop, marginsOf, scaleCrop, trimArgs, trimmedName, trimMargins } from "./trim.mjs";

/** A grey picture with a flat border of `tone` around a noisy interior. */
function bordered(width, height, border, tone = 230) {
  const gray = Buffer.alloc(width * height);
  let seed = 7;
  for (let y = 0; y < height; y++) {
    for (let x = 0; x < width; x++) {
      const inside = x >= border.left && x < width - border.right && y >= border.top && y < height - border.bottom;
      seed = (seed * 1103515245 + 12345) & 0x7fffffff;
      gray[y * width + x] = inside ? 40 + (seed % 150) : tone;
    }
  }
  return gray;
}

test("a flat paper margin is measured on each side and the largest box of the same aspect inside it is cut", () => {
  const border = { top: 6, bottom: 8, left: 12, right: 10 };
  const gray = bordered(512, 288, border);
  assert.deepEqual(marginsOf(gray, 512, 288), border);
  const crop = marginCrop(border, 512, 288);
  // The inner box is 490 × 274; the 16:9 box inside it is bounded by the height: 274 → 486 wide.
  assert.deepEqual(crop, { x: 14, y: 6, w: 486, h: 274 });
  assert.ok(crop.x >= border.left && crop.x + crop.w <= 512 - border.right);
  assert.ok(crop.y >= border.top && crop.y + crop.h <= 288 - border.bottom);
  assert.ok(Math.abs(crop.w / crop.h - 16 / 9) < 0.01);
  // Scaled to the real picture, the crop keeps its aspect and stays inside it.
  const scaled = scaleCrop(crop, ANALYSIS, { width: 2048, height: 1152 });
  assert.deepEqual(scaled, { x: 56, y: 24, w: 1944, h: 1096 });
  assert.ok(scaled.x + scaled.w <= 2048 && scaled.y + scaled.h <= 1152);
});

test("a picture with no margin, a dark vignette or a margin too thin to matter is left alone", () => {
  const plain = bordered(512, 288, { top: 0, bottom: 0, left: 0, right: 0 });
  assert.deepEqual(marginsOf(plain, 512, 288), { top: 0, bottom: 0, left: 0, right: 0 });
  assert.equal(marginCrop({ top: 0, bottom: 0, left: 0, right: 0 }, 512, 288), null);
  // One flat line at the top (0.35%) is under the share worth cutting.
  assert.equal(marginCrop({ top: 1, bottom: 0, left: 0, right: 0 }, 512, 288), null);
  assert.ok(marginCrop({ top: 2, bottom: 0, left: 0, right: 0 }, 512, 288), "0.7% on one side is cut");
  // The walk stops at 8% of the dimension: a flat picture is not all margin.
  const flat = Buffer.alloc(512 * 288, 200);
  assert.deepEqual(marginsOf(flat, 512, 288), { top: 23, bottom: 23, left: 40, right: 40 });
});

test("the ffmpeg arguments read a small grey copy, cut the crop and scale back; the trimmed file sits beside the picture", () => {
  assert.deepEqual(grayArgs("in.png").slice(-6), ["scale=512:288:flags=area,format=gray", "-frames:v", "1", "-f", "rawvideo", "-"]);
  assert.deepEqual(trimArgs("in.png", { x: 56, y: 24, w: 1944, h: 1096 }, { width: 2048, height: 1152 }, "out.png").slice(-5), ["-vf", "crop=1944:1096:56:24,scale=2048:1152:flags=lanczos", "-frames:v", "1", "out.png"]);
  assert.equal(trimmedName("keyframes/podium-1.png"), "keyframes/podium-1-trim.png");
  assert.equal(trimmedName("keyframes/plate-2.jpg"), "keyframes/plate-2-trim.jpg");
});

test("without ffmpeg, or with a picture ffmpeg cannot read, the picture is used as it came", async () => {
  assert.equal(await trimMargins({ env: { FFMPEG_PATH: "/nowhere/ffmpeg" } }, "/tmp", "keyframes/x.png"), null);
  assert.deepEqual(await trimMargins({ trimImage: async (file) => ({ file: `${file}-t`, sha256: "s", margins: {} }) }, "/tmp", "a.png"), { file: "a.png-t", sha256: "s", margins: {} });
});
