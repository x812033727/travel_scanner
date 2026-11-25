import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { classifyDriverError } from "./drivers/driver-interface.mjs";
import { GflowCliDriver, resolveGflowBinary } from "./drivers/gflow-cli-driver.mjs";
import { writeClipsQaGallery, writeStillsQaGallery } from "./postprocess/qa-contact-sheet.mjs";
import {
  buildClipQa4Args,
  buildUpscale1080p30Args,
  upscaleClipTo1080p30,
} from "./postprocess/upscale-1080p30.mjs";

test("resolveGflowBinary locates Windows uv tool install shim under %USERPROFILE%\\.local\\bin", () => {
  const expected = "C:\\Users\\Owner\\.local\\bin\\gflow.exe";
  const resolved = resolveGflowBinary({
    platform: "win32",
    env: { USERPROFILE: "C:\\Users\\Owner" },
    existsSync: (p) => p === expected,
  });
  assert.equal(resolved, expected);
});

test("GflowCliDriver constructs verified gflow CLI arguments for t2i, i2i, and i2v with start+end frame", async () => {
  const calls = [];
  const driver = new GflowCliDriver({
    binary: "gflow",
    profile: "pro-main",
    runtimeHome: "/tmp/mokaair-flow-test",
    runProcess: async (bin, args, opts) => {
      calls.push({ bin, args, env: opts.env });
      return {
        exitCode: 0,
        stdout: JSON.stringify({
          media_id: "media-123",
          project_id: "proj-1",
          credits_spent: 12,
          charged: "yes",
        }),
        stderr: "",
      };
    },
  });

  await driver.generateImage({
    prompt: "Calm misty harbor at dawn",
    model: "nano2.1",
    aspect: "16:9",
    projectId: "proj-scenery",
    outFile: "/tmp/s01.png",
  });
  assert.deepEqual(calls[0].args, [
    "image",
    "t2i",
    "Calm misty harbor at dawn",
    "--model",
    "nano2.1",
    "--aspect",
    "16:9",
    "--project",
    "proj-scenery",
    "--out-file",
    "/tmp/s01.png",
    "--json",
    "--profile",
    "pro-main",
  ]);
  assert.equal(calls[0].env.GFLOW_CLI_EXIT_CODES, "2");

  await driver.generateImage({
    prompt: "Ada examining a brass compass",
    refs: ["/tmp/ada-canon-v2.png"],
    model: "nano2.1",
    aspect: "16:9",
    projectId: "proj-char",
    outFile: "/tmp/s02.png",
  });
  assert.equal(calls[1].args[0], "image");
  assert.equal(calls[1].args[1], "i2i");
  assert.ok(calls[1].args.includes("--ref"));
  assert.ok(calls[1].args.includes("/tmp/ada-canon-v2.png"));

  const videoRes = await driver.generateVideo({
    prompt: "Slow push-in as compass needle spins",
    initialFrame: "/tmp/s02.png",
    endFrame: "/tmp/s02__end.png",
    model: "omni-1.2-flash",
    aspect: "16:9",
    durationSec: 4,
    resolution: "720p",
    maxCredits: 15,
    projectId: "proj-char",
    outFile: "/tmp/s02-720p.mp4",
  });
  assert.equal(videoRes.creditsSpent, 12);
  assert.deepEqual(calls[2].args, [
    "video",
    "i2v",
    "--initial-frame",
    "/tmp/s02.png",
    "--end-frame",
    "/tmp/s02__end.png",
    "Slow push-in as compass needle spins",
    "--model",
    "omni-1.2-flash",
    "--aspect",
    "16:9",
    "--duration",
    "4",
    "--resolution",
    "720p",
    "--max-credits",
    "15",
    "--project",
    "proj-char",
    "--out-file",
    "/tmp/s02-720p.mp4",
    "--json",
    "--profile",
    "pro-main",
  ]);
});

test("classifyDriverError enforces Fail-Fast on tier-403, selector drift, and maybe-charged failures", () => {
  const tier403 = classifyDriverError({
    exitCode: 22,
    json: {
      status: "fail",
      error: { type: "errors/tier-refusal", title: "403 refused", retryable: true, charged: "no" },
    },
  });
  assert.equal(tier403.retryable, false);
  assert.equal(tier403.charged, "no");

  const lostSubmit = classifyDriverError({
    exitCode: 9,
    json: {
      status: "fail",
      error: {
        type: "errors/timeout",
        title: "Submit lost",
        retryable: true,
        charged: "maybe",
        operation_id: "op-99",
      },
    },
  });
  assert.equal(lostSubmit.retryable, false);
  assert.equal(lostSubmit.charged, "maybe");
  assert.equal(lostSubmit.nextAction, "reconcile");
  assert.equal(lostSubmit.operationId, "op-99");
});

test("FFmpeg upscale args lock Lanczos 1080p30, bt709, video_full_range_flag=0, and -an", async () => {
  const args = buildUpscale1080p30Args({ inputPath: "in.mp4", outputPath: "out.mp4" });
  assert.ok(args.includes("scale=1920:1080:flags=lanczos,fps=30,format=yuv420p"));
  assert.ok(args.includes("bt709"));
  assert.ok(args.includes("h264_metadata=video_full_range_flag=0"));
  assert.ok(args.includes("-an"));

  const qaArgs = buildClipQa4Args({ inputPath: "out.mp4", outputJpgPath: "qa4.jpg" });
  assert.ok(qaArgs.some((a) => a.includes("tile=2x2")));

  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "flow-post-"));
  try {
    const rawMp4 = path.join(dir, "raw.mp4");
    const upMp4 = path.join(dir, "up.mp4");
    const qa4 = path.join(dir, "qa4.jpg");
    fs.writeFileSync(rawMp4, Buffer.from("fake-raw-720p"));

    const seen = [];
    const res = await upscaleClipTo1080p30({
      inputPath: rawMp4,
      outputPath: upMp4,
      qa4OutputPath: qa4,
      runFfmpeg: async (_bin, ffArgs) => {
        seen.push(ffArgs);
        const dest = ffArgs[ffArgs.length - 1];
        fs.writeFileSync(dest, Buffer.from("fake-ffmpeg-output"));
        return { exitCode: 0, stderr: "" };
      },
    });
    assert.equal(seen.length, 2);
    assert.equal(res.spec.colorRange, "tv");
    assert.equal(res.spec.audioStripped, true);
    assert.ok(res.rawSha256 && res.upscaledSha256);

    const stillsHtml = writeStillsQaGallery({
      galleryFile: path.join(dir, "stills-qa.html"),
      slug: "curio-w31",
      series: "curio",
      items: [{ shotId: "s01", track: "character", width: 1376, height: 768, qaStatus: "approved", filePath: qa4, prompt: "Test" }],
    });
    assert.match(fs.readFileSync(stillsHtml, "utf8"), /1376×768/);

    const clipsHtml = writeClipsQaGallery({
      galleryFile: path.join(dir, "clips-qa.html"),
      slug: "curio-w31",
      series: "curio",
      clips: [{ shotId: "s01", model: "omni-1.2-flash", credits: 12, qa4Path: qa4, upscaledPath: upMp4, prompt: "Move" }],
    });
    assert.match(fs.readFileSync(clipsHtml, "utf8"), /omni-1\.2-flash/);
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});
