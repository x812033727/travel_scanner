/**
 * The RunPod H3 route offline: a fake site broker and a fake ComfyUI in this process, the real
 * gate.py in front of the fake ComfyUI, and the real runner against both. No RunPod account, no
 * GPU, no money. Pinned: the gate opens five routes behind the token and nothing else; the runner
 * starts a pod, beats, uploads, submits a graph with every placeholder filled, saves the clip, and
 * always stops the pod it started; existing outputs start no pod; a failed job still stops it.
 */
import assert from "node:assert/strict";
import { spawn } from "node:child_process";
import { readdirSync, existsSync, mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { createServer } from "node:http";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { startPairing } from "./video/tts/pairing.mjs";

const ROOT = fileURLToPath(new URL("../", import.meta.url));
const RUNPOD = path.join(ROOT, "ops", "runpod");
const RUNNER = path.join(ROOT, ".agents", "skills", "minimax-h3-runpod", "scripts", "runpod_runner.py");
const PYTHON = process.env.MINIMAX_H3_TEST_PYTHON || "python3";
const GATE_TOKEN = "gate-token-for-the-offline-test";
const VIDEO_TOKEN = "mkv_offline_test_token_offline_test_token";
const PNG = Buffer.from("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==", "base64");

function listen(handler) {
  return new Promise((resolve) => {
    const server = createServer(handler);
    server.listen(0, "127.0.0.1", () => resolve({ server, url: `http://127.0.0.1:${server.address().port}`, port: server.address().port }));
  });
}

function collect(request) {
  return new Promise((resolve) => {
    const chunks = [];
    request.on("data", (chunk) => chunks.push(chunk));
    request.on("end", () => resolve(Buffer.concat(chunks)));
  });
}

function json(response, status, body) {
  response.writeHead(status, { "Content-Type": "application/json" });
  response.end(JSON.stringify(body));
}

async function fakeComfy({ failPrompts = false } = {}) {
  const seen = { prompts: [], uploads: 0 };
  const box = await listen(async (request, response) => {
    const body = await collect(request);
    const url = new URL(request.url, "http://x");
    if (url.pathname === "/system_stats") return json(response, 200, {});
    if (url.pathname === "/upload/image") {
      seen.uploads += 1;
      return json(response, 200, { name: `up${seen.uploads}.png` });
    }
    if (url.pathname === "/prompt") {
      seen.prompts.push(JSON.parse(body).prompt);
      return failPrompts ? json(response, 400, { error: "bad graph" }) : json(response, 200, { prompt_id: "abc-123" });
    }
    if (url.pathname === "/history/abc-123") {
      return json(response, 200, { "abc-123": { status: { status_str: "success", completed: true }, outputs: { 15: { gifs: [{ filename: "o.mp4", subfolder: "", type: "output" }] } } } });
    }
    if (url.pathname === "/view") {
      response.writeHead(200, { "Content-Type": "video/mp4", "Content-Length": "9" });
      return response.end("mp4-bytes");
    }
    return json(response, 500, { error: `unexpected ${url.pathname}` });
  });
  return { ...box, seen };
}

function startGate(comfyUrl, port) {
  const child = spawn(PYTHON, ["-I", path.join(RUNPOD, "gate.py")], {
    env: { ...process.env, GATE_TOKEN, GATE_PORT: String(port), COMFY_URL: comfyUrl },
    stdio: "ignore",
  });
  return child;
}

async function freePort() {
  const { server, port } = await listen(() => {});
  await new Promise((resolve) => server.close(resolve));
  return port;
}

async function waitFor(url, headers) {
  for (let attempt = 0; attempt < 100; attempt += 1) {
    try {
      const response = await fetch(url, { headers });
      if (response.status) return response;
    } catch {
      await new Promise((resolve) => setTimeout(resolve, 100));
    }
  }
  throw new Error(`nothing answered at ${url}`);
}

async function rig(options) {
  const comfy = await fakeComfy(options);
  const port = await freePort();
  const gate = startGate(comfy.url, port);
  const gateUrl = `http://127.0.0.1:${port}`;
  await waitFor(`${gateUrl}/health`, { Authorization: `Bearer ${GATE_TOKEN}` });
  const calls = [];
  const broker = await listen(async (request, response) => {
    await collect(request);
    const url = new URL(request.url, "http://x").pathname;
    calls.push(`${request.method} ${url}`);
    assert.equal(request.headers.authorization, `Bearer ${VIDEO_TOKEN}`);
    if (request.method === "GET" && url === "/api/video/runpod/pods") return json(response, 200, []);
    if (request.method === "POST" && url === "/api/video/runpod/pods") {
      return json(response, 201, { session_id: "s1", pod_id: "p1", base_url: gateUrl, gate_token: GATE_TOKEN, cost_per_hr: "2.59", idle_stop_minutes: 15, max_pod_hours: 8, default_profile: "hero" });
    }
    if (url === "/api/video/runpod/pods/s1/stop") return json(response, 200, { usd: "0.05", stop_reason: "manual" });
    if (url === "/api/video/runpod/pods/s1/heartbeat") return json(response, 200, {});
    return json(response, 404, { detail: `unexpected ${url}` });
  });
  const home = mkdtempSync(path.join(tmpdir(), "h3r-"));
  return {
    comfy, gateUrl, calls, home,
    env: { ...process.env, HOME: home, USERPROFILE: home, MOKAAIR_SITE: broker.url, MOKAAIR_VIDEO_TOKEN: VIDEO_TOKEN, H3R_POLL_SECONDS: "0.05", H3R_HEARTBEAT_SECONDS: "0.05" },
    close() {
      gate.kill();
      comfy.server.close();
      broker.server.close();
      rmSync(home, { recursive: true, force: true });
    },
  };
}

function run(env, args) {
  return new Promise((resolve) => {
    const child = spawn(PYTHON, ["-I", RUNNER, ...args], { env });
    let out = "";
    child.stdout.on("data", (chunk) => { out += chunk; });
    child.stderr.on("data", (chunk) => { out += chunk; });
    child.on("close", (code) => resolve({ code, out }));
  });
}

function manifest(home, extra = {}) {
  const dir = path.join(home, "work");
  mkdirSync(dir, { recursive: true });
  writeFileSync(path.join(dir, "f.png"), PNG);
  writeFileSync(path.join(dir, "p.txt"), "<Picture 1> walks to the door and holds a static shot.");
  const file = path.join(dir, "jobs.json");
  writeFileSync(file, JSON.stringify({ jobs: [{ id: "s01", inference_mode: "first_frame", reference_images: ["f.png"], prompt_file: "p.txt", duration_seconds: 6, width: 1312, height: 736, seed: 7, ...extra }] }));
  return file;
}

test("the gate refuses a wrong token and every route outside the five", async () => {
  const box = await rig();
  try {
    const auth = { Authorization: `Bearer ${GATE_TOKEN}` };
    assert.equal((await fetch(`${box.gateUrl}/health`)).status, 401);
    assert.equal((await fetch(`${box.gateUrl}/health`, { headers: { Authorization: "Bearer wrong" } })).status, 401);
    assert.equal((await fetch(`${box.gateUrl}/health`, { headers: auth })).status, 200);
    for (const route of ["/system_stats", "/object_info", "/queue", "/", "/history/../object_info"]) {
      assert.equal((await fetch(`${box.gateUrl}${route}`, { headers: auth })).status, 404, route);
    }
    assert.equal((await fetch(`${box.gateUrl}/view`, { method: "DELETE", headers: auth })).status, 404);
    assert.equal((await fetch(`${box.gateUrl}/history/abc-123`, { headers: auth })).status, 200);
  } finally {
    box.close();
  }
});

test("a batch starts a pod, fills the graph, saves the clip and stops the pod", async () => {
  const box = await rig();
  try {
    const out = path.join(box.home, "out");
    const progress = path.join(out, "progress.json");
    const result = await run(box.env, ["batch", "--manifest", manifest(box.home), "--output-dir", out, "--progress", progress, "--label", "test"]);
    assert.equal(result.code, 0, result.out);
    assert.equal(readFileSync(path.join(out, "s01.mp4"), "utf8"), "mp4-bytes");
    assert.ok(box.calls.includes("POST /api/video/runpod/pods"));
    assert.ok(box.calls.includes("POST /api/video/runpod/pods/s1/stop"));
    const graph = box.comfy.seen.prompts[0];
    assert.ok(!JSON.stringify(graph).includes('"$'), "every placeholder is filled");
    assert.equal(graph["11"].inputs.steps, 20);
    assert.equal(graph["2"].inputs.strength_model, 0);
    assert.equal(graph["7"].inputs.length, 158);
    assert.equal(graph["9"].inputs.noise_seed, 7);
    const report = JSON.parse(readFileSync(progress, "utf8"));
    assert.equal(report.status, "completed");
    assert.equal(report.usd, "0.05");
    assert.equal(report.jobs[0].seed, 7);
    assert.equal(report.jobs[0].profile, "hero", "with no --profile, the card's default applies");
    assert.equal(existsSync(path.join(box.home, ".cache", "minimax-h3-runpod", "session.json")), false);
  } finally {
    box.close();
  }
});

test("reference mode wires every image", async () => {
  const box = await rig();
  try {
    const file = manifest(box.home, { inference_mode: "reference", reference_images: ["f.png", "f.png"] });
    const result = await run(box.env, ["batch", "--manifest", file, "--output-dir", path.join(box.home, "out"), "--no-check"]);
    assert.equal(result.code, 0, result.out);
    const graph = box.comfy.seen.prompts[0];
    assert.deepEqual(graph["7"].inputs["ref_images.ref_image_1"], ["101", 0]);
    assert.equal(graph["11"].inputs.steps, 20);
    assert.equal(graph["101"].inputs.image, "up2.png");
  } finally {
    box.close();
  }
});

test("existing outputs start no pod, and a failed job still stops the pod", async () => {
  const box = await rig({ failPrompts: true });
  try {
    const out = path.join(box.home, "out");
    const failed = await run(box.env, ["batch", "--manifest", manifest(box.home), "--output-dir", out]);
    assert.equal(failed.code, 1, failed.out);
    assert.ok(box.calls.includes("POST /api/video/runpod/pods/s1/stop"));
    box.calls.length = 0;
    mkdirSync(out, { recursive: true });
    writeFileSync(path.join(out, "s01.mp4"), "done");
    const skipped = await run(box.env, ["batch", "--manifest", manifest(box.home), "--output-dir", out]);
    assert.equal(skipped.code, 0, skipped.out);
    assert.deepEqual(box.calls, []);
  } finally {
    box.close();
  }
});

test("the manifest check stops a bad batch before any pod", async () => {
  const box = await rig();
  try {
    const result = await run(box.env, ["batch", "--manifest", manifest(box.home, { width: 1000 }), "--output-dir", path.join(box.home, "out")]);
    assert.equal(result.code, 1, result.out);
    assert.deepEqual(box.calls, []);
  } finally {
    box.close();
  }
});

test("a --runpod pairing asks the site for RunPod access", async () => {
  const bodies = [];
  const fetchImpl = async (_url, init) => {
    bodies.push(JSON.parse(init.body));
    return new Response(JSON.stringify({ device_code: "d" }), { status: 200 });
  };
  await startPairing({ site: "https://example.test", clientName: "雲端 session", runpod: true, fetchImpl });
  assert.deepEqual(bodies, [{ client_name: "雲端 session", runpod: true }]);
});

test("every model a workflow or profile names is in the lock", () => {
  const lock = JSON.parse(readFileSync(path.join(RUNPOD, "models.lock"), "utf8")).files;
  const names = new Set(lock.map((file) => path.posix.basename(file.path)));
  for (const file of lock) assert.match(file.sha256, /^[0-9a-f]{64}$/);
  const named = [];
  for (const name of readdirSync(path.join(RUNPOD, "workflows"))) {
    const graph = JSON.parse(readFileSync(path.join(RUNPOD, "workflows", name), "utf8"));
    for (const node of Object.values(graph)) {
      for (const [key, value] of Object.entries(node.inputs)) {
        if (typeof value === "string" && /\.safetensors$/.test(value)) named.push(`${key}:${value}`);
      }
    }
  }
  const profiles = JSON.parse(readFileSync(path.join(RUNPOD, "profiles.json"), "utf8"));
  for (const profile of Object.values(profiles)) named.push(`lora:${profile.reference.lora}`, `lora:${profile.first_frame.lora}`);
  assert.ok(named.length > 10);
  for (const item of named) assert.ok(names.has(item.split(":")[1]), `${item} is not in models.lock`);
});
