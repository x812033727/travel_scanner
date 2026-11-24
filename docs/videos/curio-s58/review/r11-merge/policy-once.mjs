import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { automationClient } from "../../../../../tools/video/automation/client.mjs";
import { policyRequest, policyVerdict } from "../../../../../tools/video/qa/policy.mjs";

const here = dirname(fileURLToPath(import.meta.url));
const episode = join(here, "../..");
const sha = (value) => createHash("sha256").update(value).digest("hex");
const expected = {
  "research.md": "b26201dd469744fe10c8d259beb93ebcda23609fdb6bc989a6f1d784d9f9779e",
  "brief.md": "5afefc8547bc4fb4a597bcfc99e4e93bcec7631ad237085af78b596aa269a21f",
  "claims.md": "db0457996d4a99337e56c5b763986e1621286b258eeec1bbac9c0d1668b47aa9",
  "video.json": "c3464296eea71e0e65d93dc52340bec4720a8c4c9eb55e5db10e837070955d8b",
  "script.md": "eff9457c6d99f680b4dc5d17b10f2ec5f68504f905631590bfb0e333b3e548b9",
};
for (const [name, hash] of Object.entries(expected)) if (sha(readFileSync(join(episode, name))) !== hash) throw new Error(`R11 ${name} SHA drift`);
const doc = JSON.parse(readFileSync(join(episode, "video.json"), "utf8"));
const brief = readFileSync(join(episode, "brief.md"), "utf8");
const request = policyRequest({ doc, brief });
const privateFile = join(process.env.VIDEO_WORKDIR ?? "/workspace/.video-work", "curio-s58/review/policy-pre-tts-r11.json");
const publicFile = join(here, "policy-result.json");
if (existsSync(privateFile) || existsSync(publicFile)) throw new Error("R11 policy already attempted; inspect receipt, do not resend");
mkdirSync(dirname(privateFile), { recursive: true });
const base = {
  slug: doc.slug,
  at: new Date().toISOString(),
  creative_sha256: expected,
  request_sha256: sha(JSON.stringify(request)),
  viewpoint_sha256: sha(request.viewpoint),
  narration_sha256: sha(request.script),
};
writeFileSync(privateFile, `${JSON.stringify({ ...base, state: "sent_or_unknown" }, null, 2)}\n`);
try {
  const answer = await automationClient({ env: process.env }, { attempts: 1 }).judgePolicy(request);
  const parsed = policyVerdict(answer);
  const receipt = { ...base, state: "answered", response: answer, parsed };
  writeFileSync(privateFile, `${JSON.stringify(receipt, null, 2)}\n`);
  writeFileSync(publicFile, `${JSON.stringify(receipt, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({ state: receipt.state, request_sha256: base.request_sha256, response: answer, parsed }, null, 2)}\n`);
  if (!parsed.ok) process.exitCode = 1;
} catch (error) {
  const receipt = { ...base, state: "held_unknown_or_failed", error: { name: error.name, code: error.code ?? null, status: error.status ?? null, who: error.who ?? null, message: error.message } };
  writeFileSync(privateFile, `${JSON.stringify(receipt, null, 2)}\n`);
  process.stderr.write(`${JSON.stringify({ state: receipt.state, error: receipt.error }, null, 2)}\n`);
  process.exitCode = 1;
}
