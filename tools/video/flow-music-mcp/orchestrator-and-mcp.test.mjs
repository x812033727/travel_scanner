import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { applyClientConfigWrite, buildClientSetupPlan } from "./cli.mjs";
import { MusicDriver, MusicDriverError } from "./drivers/driver-interface.mjs";
import { JobQueue, RuntimeLock } from "./jobs/job-queue.mjs";
import { FlowMusicOrchestrator } from "./orchestrator.mjs";

const SERVER_SCRIPT = fileURLToPath(new URL("./server.mjs", import.meta.url));

class MockMusicDriver extends MusicDriver {
  constructor() {
    super({ name: "mock-music" });
    this.remoteClips = [
      {
        id: "clip-bed-1",
        title: "curio-bed-archive",
        status: "ready",
        duration: 162.4,
        sound_prompt: "Instrumental mystery archive bed, upright bass, 92 bpm",
        created_at: "2026-11-26T00:00:00Z",
      },
      {
        id: "clip-sfx-1",
        title: "curio-sfx-hits",
        status: "ready",
        duration: 58.0,
        sound_prompt: "Wooden rubber stamp, paper whoosh, light pop sound effects",
        created_at: "2026-11-26T00:01:00Z",
      },
    ];
    this.generatedCounter = 0;
  }

  async checkAuth({ profile = null } = {}) {
    return {
      authenticated: true,
      profile: profile || "default",
      userId: "user-123",
      account: "owner@example.com",
      handle: "twocypress84",
      plan: "MEMBER",
    };
  }

  async listProfiles() {
    return [
      { profile: "default", isDefault: true, cookiesPresent: true, account: "owner@example.com", handle: "twocypress84", plan: "MEMBER" },
    ];
  }

  async listRemoteClips({ profile = null } = {}) {
    return { profile: profile || "default", userId: "user-123", clips: this.remoteClips };
  }

  async downloadClip({ clipId, format, outFile }) {
    fs.mkdirSync(path.dirname(outFile), { recursive: true });
    fs.writeFileSync(outFile, Buffer.from(`audio-bytes:${clipId}:${format}`));
    return { clipId, format, outFile, byteLength: 32, sha256: "a".repeat(64) };
  }

  async generateTrack({ prompt, title }) {
    this.generatedCounter += 1;
    const id = `gen-clip-${this.generatedCounter}`;
    return {
      ok: true,
      clips: [{ id, title, status: "ready", duration: 155.0, sound_prompt: prompt }],
    };
  }
}

test("end-to-end FlowMusicOrchestrator lifecycle: generate, download, slice, cut, audition gallery, approve, _sfx v2 export, _music staging, and Drive 0-diff sync", async () => {
  const fakeRepo = fs.mkdtempSync(path.join(os.tmpdir(), "flow-music-repo-"));
  const runtimeHome = fs.mkdtempSync(path.join(os.tmpdir(), "flow-music-home-"));
  const workBase = fs.mkdtempSync(path.join(os.tmpdir(), "flow-music-workbase-"));
  const fakeDrive = fs.mkdtempSync(path.join(os.tmpdir(), "flow-music-drive-"));

  const driver = new MockMusicDriver();
  const queue = new JobQueue({ runtimeHome, minPauseMs: 0, maxPauseMs: 0 });
  const orchestrator = new FlowMusicOrchestrator({
    driver,
    queue,
    repoRoot: fakeRepo,
    runtimeHome,
    measureFn: async (filePath) => ({
      file: path.basename(filePath),
      filePath,
      sha256: "b".repeat(64),
      seconds: 155.2,
      lufs_i: -16.5,
      lufs_m: -14.2,
      peak_dbtp: -1.1,
      silences: 1,
      nearSilent: false,
      clipping: false,
    }),
    detectSlicesFn: async (filePath) => ({
      file: path.basename(filePath),
      filePath,
      seconds: 58.0,
      lufs_i: -18.0,
      peak_dbtp: -1.5,
      nearSilent: false,
      silenceCount: 3,
      slices: [
        { index: 1, startSec: 0.2, endSec: 1.0, durationSec: 0.8 },
        { index: 2, startSec: 4.0, endSec: 4.9, durationSec: 0.9 },
        { index: 3, startSec: 8.1, endSec: 8.7, durationSec: 0.6 },
      ],
    }),
    cutFn: async ({ inputPath, outputPath, startSec, endSec }) => {
      fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      fs.writeFileSync(outputPath, Buffer.from(`cut:${path.basename(outputPath)}`));
      return {
        inputPath,
        outputPath,
        file: path.basename(outputPath),
        cut: { startSec, endSec, fadeInSec: 0.01, fadeOutSec: 0.08 },
        sha256: "c".repeat(64),
        seconds: Number((endSec - startSec).toFixed(3)),
        lufs_i: -15.4,
        lufs_m: -14.0,
        peak_dbtp: -2.0,
        nearSilent: false,
        clipping: false,
      };
    },
  });

  try {
    // 1. Status & profiles
    const status = await orchestrator.musicStatus();
    assert.equal(status.ok, true);
    assert.equal(status.auth.handle, "twocypress84");

    const profiles = await orchestrator.musicProfiles();
    assert.equal(profiles.count, 1);

    // 2. Init + preflight + generate + download
    const col = "curio-pack-20261126";
    const init = await orchestrator.musicInitCollection({ collection: col, series: "curio" });
    assert.equal(init.ok, true);

    const pre = await orchestrator.musicPreflightPlan({
      collection: col,
      series: "curio",
      tracks: [{ kind: "bed", name: "archive", prompt: "Upright bass and celesta, 92 bpm" }],
    });
    assert.equal(pre.ok, true);

    const gen = await orchestrator.musicGenerate({ collection: col, series: "curio", waitMs: 5000 });
    assert.equal(gen.done, true);
    assert.equal(gen.job.status, "completed");

    const dl = await orchestrator.musicDownload({
      collection: col,
      series: "curio",
      clips: [{ clipId: "clip-sfx-1", title: "curio-sfx-hits", kind: "sfx" }],
      waitMs: 5000,
    });
    assert.equal(dl.done, true);
    assert.equal(dl.job.completed, 1);

    // 3. Detect slices & cut stamp / whoosh / pop
    const sliced = await orchestrator.musicDetectSlices({ collection: col, series: "curio" });
    assert.equal(sliced.analyzedCount, 1);
    assert.equal(sliced.results[0].slices.length, 3);

    const cuts = await orchestrator.musicCut({
      collection: col,
      series: "curio",
      cuts: [
        { file: "curio-sfx-hits-take1.m4a", outputName: "stamp", soundName: "stamp", kind: "sfx", startSec: 0.2, endSec: 1.0 },
        { file: "curio-sfx-hits-take1.m4a", outputName: "whoosh", soundName: "whoosh", kind: "sfx", startSec: 4.0, endSec: 4.9 },
        { file: "curio-sfx-hits-take1.m4a", outputName: "pop", soundName: "pop", kind: "sfx", startSec: 8.1, endSec: 8.7 },
      ],
    });
    assert.equal(cuts.createdCount, 3);

    // 4. Generate audition gallery & approve
    const gallery = await orchestrator.musicQaGallery({ collection: col, series: "curio" });
    assert.ok(fs.existsSync(gallery.galleryFile));
    const html = fs.readFileSync(gallery.galleryFile, "utf8");
    assert.match(html, /copyApprovePayload/);
    assert.match(html, /curio-bed-archive-take1\.m4a/);

    // Staging before approval is blocked
    const blockedStage = await orchestrator.musicStageForEpisode({
      collection: col,
      series: "curio",
      file: "curio-bed-archive-take1.m4a",
      workBase,
    });
    assert.equal(blockedStage.ok, false);
    assert.equal(blockedStage.reason, "track_not_approved");

    const approved = await orchestrator.musicApprove({
      collection: col,
      series: "curio",
      approved: ["curio-bed-archive-take1.m4a", "stamp.m4a", "whoosh.m4a", "pop.m4a"],
      reasons: { "curio-bed-archive-take1.m4a": "Clean instrumental bed" },
    });
    assert.equal(approved.summary.approved, 4);

    // 5. Stage approved bed into _music/ and export validated v2 _sfx/ set
    const staged = await orchestrator.musicStageForEpisode({
      collection: col,
      series: "curio",
      file: "curio-bed-archive-take1.m4a",
      workBase,
    });
    assert.equal(staged.ok, true);
    assert.ok(fs.existsSync(staged.destPath));
    assert.equal(staged.videoJsonSnippet.music.track, "curio-bed-archive-take1.m4a");

    const sfxSet = await orchestrator.musicExportSfxSet({
      collection: col,
      series: "curio",
      setName: "curio-flow",
      soundMapping: { stamp: "stamp.m4a", whoosh: "whoosh.m4a", pop: "pop.m4a" },
      workBase,
      account: "twocypress84",
    });
    assert.equal(sfxSet.ok, true);
    assert.equal(sfxSet.measuredProblems.length, 0);
    assert.ok(fs.existsSync(sfxSet.manifestFile));

    // 6. Sync to Google Drive with SHA-256 0-diff verification
    const pushed = await orchestrator.musicPushDrive({
      collection: col,
      series: "curio",
      driveRoot: fakeDrive,
    });
    assert.equal(pushed.ok, true);
    assert.equal(pushed.mismatches.length, 0);
    assert.ok(pushed.copied >= 5);

    const pushedAgain = await orchestrator.musicPushDrive({
      collection: col,
      series: "curio",
      driveRoot: fakeDrive,
    });
    assert.equal(pushedAgain.copied, 0);
    assert.equal(pushedAgain.unchanged, pushed.totalFiles);
  } finally {
    fs.rmSync(fakeRepo, { recursive: true, force: true });
    fs.rmSync(runtimeHome, { recursive: true, force: true });
    fs.rmSync(workBase, { recursive: true, force: true });
    fs.rmSync(fakeDrive, { recursive: true, force: true });
  }
});

test("JobQueue enforces Fail-Fast on auth_expired and supports RuntimeLock stale recovery + cancel", async () => {
  const runtimeHome = fs.mkdtempSync(path.join(os.tmpdir(), "flow-music-queue-"));
  try {
    const lockFile = path.join(runtimeHome, "runtime.lock");
    fs.writeFileSync(lockFile, JSON.stringify({ pid: 999999, acquiredAt: "2020-01-01T00:00:00Z" }));
    const lock = new RuntimeLock(lockFile);
    const rec = lock.acquire({ jobId: "j1" });
    assert.equal(rec.acquired, true);
    assert.equal(rec.recoveredStale, true);
    lock.release();

    const queue = new JobQueue({ runtimeHome, minPauseMs: 0, maxPauseMs: 0 });
    const tried = [];
    const job = queue.enqueue({
      kind: "music_generate",
      collection: "c1",
      items: [{ cue: "t1" }, { cue: "t2" }, { cue: "t3" }],
      worker: async (item) => {
        tried.push(item.cue);
        throw new MusicDriverError("Session expired", { code: "auth_expired", statusCode: 401 });
      },
    });
    const res = await queue.waitForJob(job.jobId, { timeoutMs: 3000 });
    assert.equal(res.job.status, "failed");
    assert.deepEqual(tried, ["t1"]);
    assert.equal(res.job.skipped, 2);
  } finally {
    fs.rmSync(runtimeHome, { recursive: true, force: true });
  }
});

test("Windows setup plan targets ~/.gemini/config/mcp_config.json and handles 0-byte JSON safely", () => {
  const plan = buildClientSetupPlan({
    repoRoot: "C:\\dev\\travel_scanner",
    platform: "win32",
    env: {
      USERPROFILE: "C:\\Users\\Owner",
      APPDATA: "C:\\Users\\Owner\\AppData\\Roaming",
      LOCALAPPDATA: "C:\\Users\\Owner\\AppData\\Local",
    },
  });
  assert.equal(plan.clients.antigravity.configPath, "C:\\Users\\Owner\\.gemini\\config\\mcp_config.json");
  assert.match(plan.clients.codex.snippet, /\[mcp_servers\.mokaair-flow-music\]/);

  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "flow-music-setup-"));
  try {
    const emptyJson = path.join(tmp, "mcp_config.json");
    fs.writeFileSync(emptyJson, "", "utf8");
    const res = applyClientConfigWrite({ ...plan.clients.antigravity, configPath: emptyJson }, plan.serverName);
    assert.equal(res.written, true);
    assert.ok(JSON.parse(fs.readFileSync(emptyJson, "utf8")).mcpServers["mokaair-flow-music"]);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test("MCP stdio server handles initialize, tools/list (17 tools), and Content-Length framing", async () => {
  const child = spawn(process.execPath, [SERVER_SCRIPT], { stdio: ["pipe", "pipe", "pipe"] });
  try {
    const responses = [];
    const done = new Promise((resolve, reject) => {
      let buf = "";
      child.stdout.on("data", (chunk) => {
        buf += chunk.toString("utf8");
        const lines = buf.split("\n");
        buf = lines.pop() || "";
        for (const line of lines) {
          if (line.trim()) responses.push(JSON.parse(line));
        }
        if (responses.length >= 2) resolve();
      });
      child.on("error", reject);
      setTimeout(() => reject(new Error("MCP stdio timeout")), 5000);
    });

    child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id: 1, method: "initialize", params: {} })}\n`);
    child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id: 2, method: "tools/list" })}\n`);
    await done;

    assert.equal(responses[0].result.serverInfo.name, "mokaair-flow-music");
    assert.equal(responses[1].result.tools.length, 17);
  } finally {
    child.kill("SIGTERM");
  }

  // Content-Length framing check
  const child2 = spawn(process.execPath, [SERVER_SCRIPT], { stdio: ["pipe", "pipe", "pipe"] });
  try {
    const body = JSON.stringify({ jsonrpc: "2.0", id: 9, method: "ping" });
    const raw = await new Promise((resolve, reject) => {
      let acc = "";
      child2.stdout.on("data", (d) => {
        acc += d.toString("utf8");
        if (acc.includes('"id":9')) resolve(acc);
      });
      child2.on("error", reject);
      setTimeout(() => reject(new Error("Content-Length timeout")), 5000);
      child2.stdin.write(`Content-Length: ${Buffer.byteLength(body, "utf8")}\r\n\r\n${body}`);
    });
    assert.match(raw, /^Content-Length: \d+\r\n\r\n/);
    assert.deepEqual(JSON.parse(raw.split("\r\n\r\n")[1]), { jsonrpc: "2.0", id: 9, result: {} });
  } finally {
    child2.kill("SIGTERM");
  }
});
