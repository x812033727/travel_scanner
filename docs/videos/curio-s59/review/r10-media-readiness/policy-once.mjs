import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { automationClient } from "../../../../../tools/video/automation/client.mjs";
import { policyRequest, policyVerdict } from "../../../../../tools/video/qa/policy.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const repo = join(episode, "../../..");
const expected = {
  "research.md": "39a48f08ca01dfa18009e9c1819684d03b92c52656952affd3266a574d88067d",
  "brief.md": "9d68d7b4dad27f56b6dbc53f7890bc0db84590de3e445302f8f4836c286ac1e3",
  "claims.md": "5f3066ba0baaaf78404600f38e5e9eda4a93c2eece14bbc296eff274dc618cb7",
  "video.json": "70487214ddbb2cc45f4af58d28ab894de9235ab811c4250b5bf16dbd638f5ffa",
  "script.md": "94acc30b9822e77e26dae56625b179ec17e8af8ce3879d8b35289a3c60824b42",
};
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const save = (name, value) => writeFileSync(join(here, name), `${JSON.stringify(value, null, 2)}\n`);
const creative = () => Object.fromEntries(Object.keys(expected).map((name) => [name, hash(readFileSync(join(episode, name)))]));
const before = creative();
if (Object.keys(expected).some((name) => before[name] !== expected[name])) throw Error("creative input drift");
if (process.env.NODE_USE_ENV_PROXY !== "1") throw Error("proxy environment required");
if (process.argv.length !== 3 || process.argv[2] !== "--send-once") throw Error("explicit --send-once required");
const video = JSON.parse(readFileSync(join(episode, "video.json"), "utf8"));
const brief = readFileSync(join(episode, "brief.md"), "utf8");
const request = policyRequest({ doc: video, brief });
const requestBytes = `${JSON.stringify(request, null, 2)}\n`;
writeFileSync(join(here, "policy-request-body.json"), requestBytes);
const marker = join(here, "policy-send-attempt.json");
try {
  readFileSync(marker);
  throw Error("policy call already attempted; never repeat automatically");
} catch (error) {
  if (error.code !== "ENOENT") throw error;
}
save("policy-request-meta.json", { creative_sha256: before, request_sha256: hash(requestBytes), script_code_points: [...request.script].length, viewpoint_code_points: [...request.viewpoint].length });
save("policy-send-attempt.json", { attempted_at: new Date().toISOString(), post_count: 1, request_sha256: hash(requestBytes), attempts_option: 1 });
try {
  const answer = await automationClient({ root: repo, env: process.env, home: process.env.HOME }, { attempts: 1 }).judgePolicy(request);
  save("policy-response.raw.json", answer);
  const verdict = policyVerdict(answer);
  const after = creative();
  if (Object.keys(expected).some((name) => after[name] !== expected[name])) throw Error("creative drift after policy call");
  save("policy-receipt.json", { post_count: 1, request_sha256: hash(requestBytes), response_sha256: hash(readFileSync(join(here, "policy-response.raw.json"))), creative_sha256_before: before, creative_sha256_after: after, ...verdict });
  process.stdout.write(`${JSON.stringify({ passed: verdict.ok, detail: verdict.detail, request_sha256: hash(requestBytes) })}\n`);
  if (!verdict.ok) process.exitCode = 1;
} catch (error) {
  save("policy-error.json", { post_count: 1, request_sha256: hash(requestBytes), code: error.code ?? null, status: error.status ?? null, message: error.message, creative_sha256_after: creative() });
  process.stderr.write(`policy call did not return a verdict: ${error.code ?? "error"}\n`);
  process.exitCode = 1;
}
