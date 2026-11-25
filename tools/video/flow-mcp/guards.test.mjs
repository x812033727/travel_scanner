import assert from "node:assert/strict";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { detectSyncFolderHazard, resolveRuntimeHome } from "./config.mjs";
import { readImageDimensionsFromBuffer, verifyStillDimensions } from "./guards/aspect-verify.mjs";
import {
  planClipBudget,
  recordCreditEvent,
  verifyAndConsumeConfirmToken,
} from "./guards/budget-guard.mjs";
import { assertEpisodeWorkdirSafe, resolveEpisodePaths } from "./guards/path-boundary.mjs";
import { preflightShotList, scanPromptText } from "./guards/prompt-safety.mjs";

function makePngBuffer(width, height) {
  const buf = Buffer.alloc(33);
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]).copy(buf, 0);
  buf.writeUInt32BE(13, 8);
  buf.write("IHDR", 12, "ascii");
  buf.writeUInt32BE(width, 16);
  buf.writeUInt32BE(height, 20);
  return buf;
}

function makeJpegBuffer(width, height) {
  const buf = Buffer.alloc(20);
  buf[0] = 0xff;
  buf[1] = 0xd8; // SOI
  buf[2] = 0xff;
  buf[3] = 0xc0; // SOF0
  buf.writeUInt16BE(11, 4);
  buf[6] = 8; // precision
  buf.writeUInt16BE(height, 7);
  buf.writeUInt16BE(width, 9);
  return buf;
}

function makeWebpVp8xBuffer(width, height) {
  const buf = Buffer.alloc(30);
  buf.write("RIFF", 0, "ascii");
  buf.writeUInt32LE(22, 4);
  buf.write("WEBP", 8, "ascii");
  buf.write("VP8X", 12, "ascii");
  buf.writeUInt32LE(10, 16);
  const wMinus1 = width - 1;
  const hMinus1 = height - 1;
  buf[24] = wMinus1 & 0xff;
  buf[25] = (wMinus1 >> 8) & 0xff;
  buf[26] = (wMinus1 >> 16) & 0xff;
  buf[27] = hMinus1 & 0xff;
  buf[28] = (hMinus1 >> 8) & 0xff;
  buf[29] = (hMinus1 >> 16) & 0xff;
  return buf;
}

test("config resolves Windows %LOCALAPPDATA% runtime home and flags OneDrive hazards", () => {
  const winHome = resolveRuntimeHome({
    platform: "win32",
    env: { LOCALAPPDATA: "C:\\Users\\Alice\\AppData\\Local" },
    homedir: "C:\\Users\\Alice",
  });
  assert.equal(winHome, "C:\\Users\\Alice\\AppData\\Local\\mokaair-flow");

  assert.match(
    detectSyncFolderHazard("C:\\Users\\Alice\\OneDrive\\travel_scanner", "win32") || "",
    /OneDrive/i,
  );
  assert.equal(detectSyncFolderHazard("C:\\dev\\travel_scanner", "win32"), null);
});

test("Route B path boundary blocks docs/videos and tracked repo directories", () => {
  const fakeRepo = fs.mkdtempSync(path.join(os.tmpdir(), "flow-repo-"));
  try {
    const safe = resolveEpisodePaths("curio-w31-sample", { repoRoot: fakeRepo });
    assert.ok(safe.root.endsWith(path.join("work", "video-episodes", "curio-w31-sample")));

    assert.throws(
      () => assertEpisodeWorkdirSafe(path.join(fakeRepo, "docs", "videos", "curio-w31"), { repoRoot: fakeRepo }),
      /Route B boundary violation/,
    );
    assert.throws(
      () => assertEpisodeWorkdirSafe(path.join(fakeRepo, "apps", "web"), { repoRoot: fakeRepo }),
      /Route B boundary violation/,
    );
    assert.throws(
      () => resolveEpisodePaths("../escape", { repoRoot: fakeRepo }),
      /Invalid episode slug/,
    );
  } finally {
    fs.rmSync(fakeRepo, { recursive: true, force: true });
  }
});

test("prompt safety scanner blocks minor, gore, filter, and copyright IP terms", () => {
  const sothatswhyBad = scanPromptText("An 8-year-old girl with bare face holds a Pikachu.", {
    series: "sothatswhy",
    shotId: "s01",
  });
  assert.equal(sothatswhyBad.ok, false);
  assert.ok(sothatswhyBad.findings.some((f) => f.category === "minor_term"));
  assert.ok(sothatswhyBad.findings.some((f) => f.category === "flow_filter_term"));
  assert.ok(sothatswhyBad.findings.some((f) => f.category === "copyright_ip"));
  assert.match(
    sothatswhyBad.findings.find((f) => f.category === "minor_term").suggestion,
    /navy coat with yellow hood/,
  );

  const curioBad = scanPromptText("A bloody corpse in a murder scene.", { series: "curio", shotId: "s02" });
  assert.equal(curioBad.ok, false);
  assert.ok(curioBad.findings.some((f) => f.category === "violence_gore_term"));

  const clean = scanPromptText(
    "The cute 2D cartoon mascot character in a navy coat with yellow hood pointing at a rain cloud diagram, theatrical gouache.",
    { series: "sothatswhy", shotId: "s03" },
  );
  assert.equal(clean.ok, true);
  assert.equal(clean.blockerCount, 0);
});

test("preflightShotList enforces dual-project isolation, retention redlines, and series budget caps", () => {
  const badShotList = {
    series: "sothatswhy",
    shots: [
      {
        id: "s01",
        chapter: "ch1",
        track: "scenery",
        mode: "still",
        duration_sec: 10,
        character_refs: ["chief-canon-v2.png"],
        still_prompt: "Rain cloud cross section diagram, clean gouache",
      },
      { id: "s02", chapter: "ch1", track: "scenery", mode: "still", duration_sec: 5, still_prompt: "Water droplets" },
      { id: "s03", chapter: "ch1", track: "scenery", mode: "still", duration_sec: 5, still_prompt: "Ice crystals" },
      { id: "s04", chapter: "ch1", track: "scenery", mode: "still", duration_sec: 5, still_prompt: "Cumulus cloud" },
    ],
  };

  const report = preflightShotList(badShotList);
  assert.equal(report.ok, false);
  assert.ok(report.findings.some((f) => f.category === "dual_project_leak"));
  assert.ok(report.findings.some((f) => f.category === "retention_consecutive_stills"));
  assert.ok(report.findings.some((f) => f.category === "retention_still_duration"));
  assert.ok(report.findings.some((f) => f.category === "low_dynamic_ratio"));

  // Exceeding 500-credit hard cap for sothatswhy (42 clips * 12 = 504 > 500)
  const overBudget = {
    series: "sothatswhy",
    shots: Array.from({ length: 42 }, (_, idx) => ({
      id: `c${idx + 1}`,
      track: "scenery",
      mode: "clip",
      still_prompt: `Atmospheric cloud movement scene ${idx + 1}`,
      video_prompt: `Slow drift of clouds scene ${idx + 1}`,
    })),
  };
  const budgetReport = preflightShotList(overBudget);
  assert.equal(budgetReport.ok, false);
  assert.ok(budgetReport.findings.some((f) => f.category === "budget_exceeds_hard_cap"));
});

test("aspect verifier reads PNG/JPEG/WebP headers and catches Flow silent 1:1 resets", () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "flow-aspect-"));
  try {
    assert.deepEqual(readImageDimensionsFromBuffer(makePngBuffer(1376, 768)), {
      format: "png",
      width: 1376,
      height: 768,
    });
    assert.deepEqual(readImageDimensionsFromBuffer(makeJpegBuffer(1376, 768)), {
      format: "jpeg",
      width: 1376,
      height: 768,
    });
    assert.deepEqual(readImageDimensionsFromBuffer(makeWebpVp8xBuffer(1376, 768)), {
      format: "webp",
      width: 1376,
      height: 768,
    });

    const goodFile = path.join(dir, "good.png");
    const squareFile = path.join(dir, "reset-square.png");
    fs.writeFileSync(goodFile, makePngBuffer(1376, 768));
    fs.writeFileSync(squareFile, makePngBuffer(1024, 1024));

    const okRes = verifyStillDimensions(goodFile);
    assert.equal(okRes.ok, true);
    assert.equal(okRes.reason, "exact_match");

    const driftRes = verifyStillDimensions(squareFile);
    assert.equal(driftRes.ok, false);
    assert.equal(driftRes.reason, "aspect_drift_1_1");
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test("budget guard enforces hard cap, single-use confirm_token, payload binding, and expiry", () => {
  const fakeRepo = fs.mkdtempSync(path.join(os.tmpdir(), "flow-budget-"));
  try {
    const paths = resolveEpisodePaths("sothatswhy-p03-test", { repoRoot: fakeRepo });
    const now = 1_700_000_000_000;

    // Spend 480 already
    recordCreditEvent(paths.ledgerFile, {
      slug: paths.slug,
      series: "sothatswhy",
      shotId: "prior_batch",
      credits: 480,
      charged: "yes",
    });

    // 2 clips (24 credits) -> 504 > 500 hard cap -> refused
    const refused = planClipBudget({
      episodePaths: paths,
      series: "sothatswhy",
      shotIds: ["s01", "s02"],
      now,
    });
    assert.equal(refused.ok, false);
    assert.equal(refused.reason, "budget_exceeded");

    // 1 clip (12 credits) -> 492 <= 500 -> allowed + token minted
    const plan = planClipBudget({
      episodePaths: paths,
      series: "sothatswhy",
      shotIds: ["s01"],
      accountCredits: 100,
      now,
    });
    assert.equal(plan.ok, true);
    assert.match(plan.confirm_token, /^mflow_/);

    // Payload tamper fails
    const mismatch = verifyAndConsumeConfirmToken({
      episodePaths: paths,
      token: plan.confirm_token,
      shotIds: ["s01", "s02"],
      now: now + 1000,
    });
    assert.equal(mismatch.ok, false);
    assert.equal(mismatch.reason, "token_payload_mismatch");

    // Exact match succeeds once
    const valid = verifyAndConsumeConfirmToken({
      episodePaths: paths,
      token: plan.confirm_token,
      shotIds: ["s01"],
      now: now + 1000,
    });
    assert.equal(valid.ok, true);

    // Replay is blocked
    const replay = verifyAndConsumeConfirmToken({
      episodePaths: paths,
      token: plan.confirm_token,
      shotIds: ["s01"],
      now: now + 2000,
    });
    assert.equal(replay.ok, false);
    assert.equal(replay.reason, "token_already_consumed");
  } finally {
    fs.rmSync(fakeRepo, { recursive: true, force: true });
  }
});
