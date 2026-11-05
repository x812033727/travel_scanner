// `runpod-reap`: ask the site to stop RunPod pods nobody is using (ticket 2026-10-30-runpod-pod-broker).
//
// The video worker runs it after every `auto` round (ops/video/worker.sh), so a pod whose runner
// crashed, or one past the admin's longest run or monthly cap, is stopped within five minutes. The
// site decides what to stop and holds the RunPod key; this only knocks with the video tool token,
// which needs no RunPod permission for this one call because it can only ever stop pods.
import { parseArgs } from "node:util";
import { readCredentials } from "../tts/credentials.mjs";
import { USER_AGENT } from "../tts/client.mjs";

const TIMEOUT_MS = 60_000;

export async function reap({ site, token, fetchImpl = globalThis.fetch }) {
  const response = await fetchImpl(`${site}/api/video/runpod/reap`, {
    method: "POST",
    headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Content-Type": "application/json" },
    body: "{}",
    signal: AbortSignal.timeout(TIMEOUT_MS),
  });
  const body = await response.json().catch(() => ({}));
  if (!response.ok) {
    const error = new Error(`${response.status} ${body.code ?? ""} ${body.detail ?? ""}`.trim());
    error.status = response.status;
    throw error;
  }
  return Array.isArray(body.stopped) ? body.stopped : [];
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  if (command !== "runpod-reap") return EXIT.usage;
  const { values } = parseArgs({ args, options: { json: { type: "boolean" } }, allowPositionals: false });
  const { site, token } = readCredentials({ env: ctx.env, home: ctx.home });
  if (!token) {
    ctx.stderr.write("runpod-reap: no video tool token; run `login` first\n");
    return EXIT.usage;
  }
  let stopped;
  try {
    stopped = await reap({ site, token, fetchImpl: ctx.fetchImpl ?? globalThis.fetch });
  } catch (error) {
    ctx.stderr.write(`runpod-reap: ${error.message}\n`);
    return EXIT.external;
  }
  if (values.json) ctx.stdout.write(`${JSON.stringify({ stopped })}\n`);
  else for (const pod of stopped) ctx.stdout.write(`runpod-reap: stopped ${pod.pod_id ?? pod.session_id} (${pod.label}): ${pod.stop_reason}, US$${Number(pod.usd).toFixed(2)}\n`);
  return EXIT.ok;
}
