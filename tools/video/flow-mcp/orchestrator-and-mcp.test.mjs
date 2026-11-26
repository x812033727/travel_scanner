import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { applyClientConfigWrite, buildClientSetupPlan } from "./cli.mjs";
import { FlowDriver } from "./drivers/driver-interface.mjs";
import { JobQueue } from "./jobs/job-queue.mjs";
import { FlowOrchestrator } from "./orchestrator.mjs";
import { MCP_TOOLS, createToolDispatcher, handleJsonRpcMessage } from "./server.mjs";

const SERVER_SCRIPT = fileURLToPath(new URL("./server.mjs", import.meta.url));

function makePngBuffer(width, height) {
  const buf = Buffer.alloc(33);
  Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]).copy(buf, 0);
  buf.writeUInt32BE(13, 8);
  buf.write("IHDR", 12, "ascii");
  buf.writeUInt32BE(width, 16);
  buf.writeUInt32BE(height, 20);
  return buf;
}

class MockFlowDriver extends FlowDriver {
  constructor({ squareOnShot = null } = {}) {
    super({ name: "mock-flow" });
    this.squareOnShot = squareOnShot;
    this.calls = [];
    this.credits = 500;
  }

  async checkAuth() {
    return { authenticated: true, profile: "default", account: "owner@example.com", plan: "Google AI Pro" };
  }

  async getCredits() {
    return { credits: this.credits, plan: "Google AI Pro" };
  }

  async createProject({ name }) {
    this.calls.push({ op: "createProject", name });
    return { projectId: `proj_${name}`, name };
  }

  async uploadAsset({ filePath, projectId }) {
    this.calls.push({ op: "uploadAsset", filePath, projectId });
    return { assetUuid: "uuid-canon-1", filePath, projectId };
  }

  async generateImage(params) {
    this.calls.push({ op: "generateImage", ...params });
    fs.mkdirSync(path.dirname(params.outFile), { recursive: true });
    const isSquare = this.squareOnShot && params.outFile.includes(this.squareOnShot);
    fs.writeFileSync(params.outFile, makePngBuffer(isSquare ? 1024 : 1376, isSquare ? 1024 : 768));
    return {
      outFile: params.outFile,
      mediaId: `img_${this.calls.length}`,
      projectId: params.projectId,
      model: params.model,
      charged: "no",
    };
  }

  async generateVideo(params) {
    this.calls.push({ op: "generateVideo", ...params });
    fs.mkdirSync(path.dirname(params.outFile), { recursive: true });
    fs.writeFileSync(params.outFile, Buffer.from("fake-720p-mp4-data"));
    this.credits -= 12;
    return {
      outFile: params.outFile,
      mediaId: `vid_${this.calls.length}`,
      projectId: params.projectId,
      model: params.model,
      creditsSpent: 12,
      charged: "yes",
    };
  }
}

test("end-to-end FlowOrchestrator lifecycle enforces stills-first gate, 1:1 quarantine, confirm_token, and 1080p30 manifest", async () => {
  const fakeRepo = fs.mkdtempSync(path.join(os.tmpdir(), "flow-e2e-repo-"));
  const runtimeHome = fs.mkdtempSync(path.join(os.tmpdir(), "flow-e2e-home-"));
  const rulesRoot = path.join(fakeRepo, ".cache", "video-drive", "rules", "_規則");
  fs.mkdirSync(path.join(rulesRoot, "奇聞檔案局"), { recursive: true });
  const adaCanon = path.join(rulesRoot, "奇聞檔案局", "ada-canon-v2.png");
  fs.writeFileSync(adaCanon, makePngBuffer(1376, 768));

  const driver = new MockFlowDriver({ squareOnShot: "s02" });
  const queue = new JobQueue({ runtimeHome, minPauseMs: 0, maxPauseMs: 0 });
  const orchestrator = new FlowOrchestrator({
    driver,
    queue,
    repoRoot: fakeRepo,
    runtimeHome,
    rulesCacheRoot: rulesRoot,
    upscaleFn: async ({ inputPath, outputPath, qa4OutputPath }) => {
      fs.mkdirSync(path.dirname(outputPath), { recursive: true });
      fs.writeFileSync(outputPath, Buffer.from("fake-1080p30-bt709"));
      if (qa4OutputPath) {
        fs.mkdirSync(path.dirname(qa4OutputPath), { recursive: true });
        fs.writeFileSync(qa4OutputPath, Buffer.from("fake-qa4-jpg"));
      }
      return {
        inputPath,
        outputPath,
        qa4Path: qa4OutputPath,
        rawSha256: "rawsha",
        upscaledSha256: "upsha",
        spec: { width: 1920, height: 1080, fps: 30, colorspace: "bt709", colorRange: "tv", audioStripped: true },
      };
    },
  });

  try {
    const status = await orchestrator.flowStatus();
    assert.equal(status.ok, true);
    assert.equal(status.credits.credits, 500);

    const slug = "curio-w31-e2e";
    const init = await orchestrator.flowInitEpisode({
      slug,
      series: "curio",
      createProjects: true,
      uploadCanonRefs: true,
    });
    assert.equal(init.ok, true);
    assert.equal(init.dualProjectsReady, true);
    assert.equal(init.workspace.uploadedCanonAssets.length, 1);

    // Write valid 2-shot list (s01 character clip, s02 scenery still)
    const shotListPath = path.join(fakeRepo, "work", "video-episodes", slug, "flow-shot-list.json");
    fs.writeFileSync(
      shotListPath,
      JSON.stringify(
        {
          series: "curio",
          shots: [
            {
              id: "s01",
              chapter: "hook",
              track: "character",
              mode: "clip",
              still_prompt: "3.5-head-ratio Ada holding a brass compass in archive, theatrical gouache",
              video_prompt: "Slow push-in as Ada tilts the compass toward warm desk light",
            },
            {
              id: "s02",
              chapter: "hook",
              track: "scenery",
              mode: "still",
              duration_sec: 5,
              still_prompt: "Old parchment maritime map on dark oak desk, no text, candlelight",
            },
          ],
        },
        null,
        2,
      ),
    );

    const pre = await orchestrator.flowPreflightShotlist({ slug });
    assert.equal(pre.ok, true);
    assert.equal(pre.summary.estimatedCredits, 12);

    // Generate stills: s01 passes 1376x768, s02 simulates Flow's 1:1 silent reset and is quarantined
    const stillRun = await orchestrator.flowGenerateStills({ slug, waitMs: 5000 });
    assert.equal(stillRun.ok, true);
    assert.equal(stillRun.job.status, "completed_with_errors");
    assert.equal(stillRun.job.completed, 1);
    assert.equal(stillRun.job.failed, 1);
    assert.equal(stillRun.job.errors[0].code, "aspect_drift_1_1");

    // Verify dual-project isolation: s01 went to character project with ada-canon-v2.png; s02 went to scenery project with 0 refs
    const imgCalls = driver.calls.filter((c) => c.op === "generateImage");
    assert.equal(imgCalls[0].projectId, "proj_curio-w31-e2e-character");
    assert.deepEqual(imgCalls[0].refs, [adaCanon]);
    assert.equal(imgCalls[1].projectId, "proj_curio-w31-e2e-scenery");
    assert.deepEqual(imgCalls[1].refs, []);

    // Regenerate s02 now fixed to 16:9
    driver.squareOnShot = null;
    const retryStill = await orchestrator.flowGenerateStills({ slug, shotIds: ["s02"], waitMs: 5000 });
    assert.equal(retryStill.job.status, "completed");

    // Stills-First Gate blocks flow_plan_clips before QA sign-off
    const blockedPlan = await orchestrator.flowPlanClips({ slug });
    assert.equal(blockedPlan.ok, false);
    assert.equal(blockedPlan.reason, "stills_not_approved");

    // Approve both stills
    const approved = await orchestrator.flowApproveStills({ slug, approved: ["s01", "s02"] });
    assert.equal(approved.ok, true);
    assert.equal(approved.summary.approvedCount, 2);

    // Plan clips -> gets single-use confirm_token
    const plan = await orchestrator.flowPlanClips({ slug, checkLiveBalance: true });
    assert.equal(plan.ok, true);
    assert.equal(plan.plannedCredits, 12);
    assert.ok(plan.confirm_token);

    // Calling flow_generate_clips without confirm_token is refused
    const noToken = await orchestrator.flowGenerateClips({ slug, shotIds: ["s01"] });
    assert.equal(noToken.ok, false);
    assert.equal(noToken.reason, "missing_confirm_token");

    // Calling with valid confirm_token generates 720p raw + upscales 1080p30 + updates ledger & manifest
    const clipRun = await orchestrator.flowGenerateClips({
      slug,
      shotIds: ["s01"],
      confirm_token: plan.confirm_token,
      waitMs: 5000,
    });
    assert.equal(clipRun.ok, true);
    assert.equal(clipRun.job.status, "completed");

    const ledger = await orchestrator.flowEpisodeLedger({ slug });
    assert.equal(ledger.credits.spent, 12);
    assert.equal(ledger.clips.completed, 1);
    assert.equal(ledger.readyForDrivePush, true);
  } finally {
    fs.rmSync(fakeRepo, { recursive: true, force: true });
    fs.rmSync(runtimeHome, { recursive: true, force: true });
  }
});

test("MCP JSON-RPC 2.0 server handles initialize, tools/list (10 tools), and tools/call over real stdio", async () => {
  // Direct unit check on handleJsonRpcMessage
  const dispatch = createToolDispatcher({
    flowStatus: async () => ({ ok: true, driver: "mock", credits: { credits: 420 } }),
  });
  const initResp = await handleJsonRpcMessage(
    { jsonrpc: "2.0", id: 1, method: "initialize", params: { protocolVersion: "2025-03-26" } },
    { dispatch },
  );
  assert.equal(initResp.result.protocolVersion, "2025-03-26");
  assert.equal(initResp.result.serverInfo.name, "mokaair-flow");

  const listResp = await handleJsonRpcMessage(
    { jsonrpc: "2.0", id: 2, method: "tools/list" },
    { dispatch },
  );
  assert.equal(listResp.result.tools.length, 18);
  assert.equal(MCP_TOOLS.length, 18);

  // Live subprocess check using both newline JSON-RPC and Content-Length framing
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
      setTimeout(() => reject(new Error("MCP stdio subprocess timed out")), 5000);
    });

    child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id: 10, method: "initialize", params: {} })}\n`);
    child.stdin.write(`${JSON.stringify({ jsonrpc: "2.0", id: 11, method: "tools/list" })}\n`);
    await done;

    assert.equal(responses[0].id, 10);
    assert.equal(responses[0].result.serverInfo.name, "mokaair-flow");
    assert.equal(responses[1].id, 11);
    assert.equal(responses[1].result.tools.length, 18);
  } finally {
    child.kill("SIGTERM");
  }
});

test("Windows setup plan escapes paths cleanly and writes JSON/TOML configs safely with .bak backup", () => {
  const plan = buildClientSetupPlan({
    repoRoot: "C:\\dev\\travel_scanner",
    platform: "win32",
    env: {
      USERPROFILE: "C:\\Users\\Owner",
      APPDATA: "C:\\Users\\Owner\\AppData\\Roaming",
      LOCALAPPDATA: "C:\\Users\\Owner\\AppData\\Local",
    },
  });

  assert.equal(plan.serverScript, "C:\\dev\\travel_scanner\\tools\\video\\flow-mcp\\server.mjs");
  assert.equal(
    plan.clients.antigravity.configPath,
    "C:\\Users\\Owner\\.gemini\\config\\mcp_config.json",
  );
  assert.equal(
    plan.clients["claude-desktop"].configPath,
    "C:\\Users\\Owner\\AppData\\Roaming\\Claude\\claude_desktop_config.json",
  );
  assert.match(plan.clients.codex.snippet, /\[mcp_servers\.mokaair-flow\]/);
  assert.match(plan.clients.codex.snippet, /C:\\\\dev\\\\travel_scanner\\\\tools\\\\video\\\\flow-mcp\\\\server\.mjs/);

  // Test real file merge + backup in a temp dir
  const tmp = fs.mkdtempSync(path.join(os.tmpdir(), "flow-setup-"));
  try {
    const jsonPath = path.join(tmp, "mcp_config.json");
    fs.writeFileSync(jsonPath, JSON.stringify({ mcpServers: { existing: { command: "echo" } } }, null, 2));
    const jsonRes = applyClientConfigWrite(
      { ...plan.clients.antigravity, configPath: jsonPath },
      plan.serverName,
    );
    assert.equal(jsonRes.written, true);
    assert.ok(fs.existsSync(`${jsonPath}.bak`));
    const mergedJson = JSON.parse(fs.readFileSync(jsonPath, "utf8"));
    assert.ok(mergedJson.mcpServers.existing);
    assert.ok(mergedJson.mcpServers["mokaair-flow"]);

    // Empty 0-byte existing JSON config file must not throw SyntaxError
    const emptyJsonPath = path.join(tmp, "empty_mcp_config.json");
    fs.writeFileSync(emptyJsonPath, "", "utf8");
    const emptyRes = applyClientConfigWrite(
      { ...plan.clients.antigravity, configPath: emptyJsonPath },
      plan.serverName,
    );
    assert.equal(emptyRes.written, true);
    assert.ok(JSON.parse(fs.readFileSync(emptyJsonPath, "utf8")).mcpServers["mokaair-flow"]);

    const tomlPath = path.join(tmp, "config.toml");
    fs.writeFileSync(tomlPath, 'model = "gpt-5"\n\n[mcp_servers.mokaair-flow]\ncommand = "old"\n');
    const tomlRes = applyClientConfigWrite(
      { ...plan.clients.codex, configPath: tomlPath },
      plan.serverName,
    );
    assert.equal(tomlRes.written, true);
    const mergedToml = fs.readFileSync(tomlPath, "utf8");
    assert.match(mergedToml, /model = "gpt-5"/);
    assert.doesNotMatch(mergedToml, /command = "old"/);
    assert.match(mergedToml, /command = "node"/);
  } finally {
    fs.rmSync(tmp, { recursive: true, force: true });
  }
});

test("RuntimeLock rejects concurrent live PID holders and recovers stale dead-PID locks", async () => {
  const { RuntimeLock } = await import("./jobs/job-queue.mjs");
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), "flow-lock-"));
  try {
    const lockFile = path.join(dir, "runtime.lock");
    const lockA = new RuntimeLock(lockFile);
    const lockB = new RuntimeLock(lockFile);

    const first = lockA.acquire({ jobId: "job-1" });
    assert.equal(first.acquired, true);

    const second = lockB.acquire({ jobId: "job-2" });
    assert.equal(second.acquired, false);
    assert.equal(second.holder.pid, process.pid);

    lockA.release();
    assert.equal(fs.existsSync(lockFile), false);

    // Simulate a crashed process leaving a stale lock behind
    fs.writeFileSync(
      lockFile,
      JSON.stringify({ pid: 999999, acquiredAt: "2020-01-01T00:00:00.000Z", jobId: "dead-job" }),
    );
    const recovered = lockB.acquire({ jobId: "job-3" });
    assert.equal(recovered.acquired, true);
    assert.equal(recovered.recoveredStale, true);
    lockB.release();
  } finally {
    fs.rmSync(dir, { recursive: true, force: true });
  }
});

test("JobQueue enforces Fail-Fast on tier-403 (exit 22) and supports flow_cancel mid-batch", async () => {
  const runtimeHome = fs.mkdtempSync(path.join(os.tmpdir(), "flow-queue-"));
  try {
    const queue = new JobQueue({ runtimeHome, minPauseMs: 0, maxPauseMs: 0 });
    const attempted = [];

    const failFastJob = queue.enqueue({
      kind: "generate_stills",
      slug: "curio-failfast",
      items: [{ shotId: "s01" }, { shotId: "s02" }, { shotId: "s03" }],
      worker: async (item) => {
        attempted.push(item.shotId);
        const err = new Error("403 tier refusal");
        err.exitCode = 22;
        err.code = "errors/tier-refusal";
        err.retryable = false;
        err.charged = "no";
        throw err;
      },
    });

    const waited = await queue.waitForJob(failFastJob.jobId, { timeoutMs: 3000 });
    assert.equal(waited.job.status, "failed");
    assert.deepEqual(attempted, ["s01"]);
    assert.equal(waited.job.skipped, 2);

    // Test cancelling a running batch preserves already completed shots
    const completedIds = [];
    const slowJob = queue.enqueue({
      kind: "generate_stills",
      slug: "curio-cancel",
      items: [{ shotId: "c01" }, { shotId: "c02" }, { shotId: "c03" }],
      worker: async (item, { signal }) => {
        if (item.shotId === "c01") {
          completedIds.push("c01");
          return { shotId: "c01" };
        }
        await new Promise((resolve, reject) => {
          const t = setTimeout(resolve, 2000);
          signal.addEventListener("abort", () => {
            clearTimeout(t);
            reject(new Error("aborted"));
          });
        });
        completedIds.push(item.shotId);
        return { shotId: item.shotId };
      },
    });

    // Wait briefly so c01 finishes and c02 starts, then cancel
    await new Promise((r) => setTimeout(r, 80));
    const cancelRes = queue.cancelJob(slowJob.jobId);
    assert.equal(cancelRes.ok, true);

    const afterCancel = await queue.waitForJob(slowJob.jobId, { timeoutMs: 3000 });
    assert.equal(afterCancel.job.status, "cancelled");
    assert.deepEqual(completedIds, ["c01"]);
  } finally {
    fs.rmSync(runtimeHome, { recursive: true, force: true });
  }
});

test("MCP stdio server also handles Content-Length framed JSON-RPC requests", async () => {
  const child = spawn(process.execPath, [SERVER_SCRIPT], { stdio: ["pipe", "pipe", "pipe"] });
  try {
    const body = JSON.stringify({ jsonrpc: "2.0", id: 99, method: "ping" });
    const frame = `Content-Length: ${Buffer.byteLength(body, "utf8")}\r\n\r\n${body}`;

    const rawOutput = await new Promise((resolve, reject) => {
      let acc = "";
      child.stdout.on("data", (chunk) => {
        acc += chunk.toString("utf8");
        if (acc.includes('"id":99')) resolve(acc);
      });
      child.on("error", reject);
      setTimeout(() => reject(new Error("Content-Length stdio test timed out")), 5000);
      child.stdin.write(frame);
    });

    assert.match(rawOutput, /^Content-Length: \d+\r\n\r\n/);
    const jsonPart = rawOutput.split("\r\n\r\n")[1];
    assert.deepEqual(JSON.parse(jsonPart), { jsonrpc: "2.0", id: 99, result: {} });
  } finally {
    child.kill("SIGTERM");
  }
});

