import assert from "node:assert/strict";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { sandbox } from "../core/fixtures/load.mjs";
import { Automation } from "./flow.mjs";

// The host's script gate (owner, 2026-11-19): a 奇聞, brand-story or 原來如此 script whose opening asks a
// question menu goes back to the writer before review-push, instead of parking the video on the refusal.
test("the host's script gate sends a question-menu opening back to the writer instead of pushing it", async () => {
  const box = sandbox("sothatswhy-x09", "drama");
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  doc.slug = "sothatswhy-x09";
  doc.scenes[0].lines[0].text = "為什麼雲會變灰？為什麼下午才下雨？雷又是從哪裡來的？";
  writeFileSync(file, JSON.stringify(doc));
  const calls = { fix: [], pushed: 0 };
  const host = {
    ctx: { root: box.root, runCommand: async () => { calls.pushed += 1; return { code: 0, out: "sent" }; } },
    settings: { drama: {} },
    workdir: () => box.workdir,
    decision: async () => null,
    fixScript: async (state, note, by, kind) => { calls.fix.push({ note, by, kind }); return "rewritten"; },
  };
  const answer = await Automation.prototype.scriptGate.call(host, { slug: "sothatswhy-x09" });
  assert.equal(answer, "rewritten");
  assert.equal(calls.pushed, 0, "nothing reaches review-push");
  assert.equal(calls.fix[0].by, "the opening check");
  assert.equal(calls.fix[0].kind, "opening", "its own round counter, stopped for the owner past MAX_PROMPT_FIX_ROUNDS");
  assert.match(calls.fix[0].note, /question menu/);
});

test("with 劇本先給我看 off, a question-menu opening is still sent back before the settings approve it", async () => {
  const box = sandbox("curio-x09", "drama");
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  doc.slug = "curio-x09";
  doc.scenes[0].lines[0].text = "為什麼雲會變灰？為什麼下午才下雨？雷又是從哪裡來的？";
  writeFileSync(file, JSON.stringify(doc));
  const calls = { fix: 0 };
  const host = {
    ctx: { root: box.root, now: () => new Date("2026-11-19T00:00:00Z") },
    settings: { drama: { series_script_gate: false } },
    workdir: () => box.workdir,
    fixScript: async () => { calls.fix += 1; return "rewritten"; },
  };
  assert.equal(await Automation.prototype.scriptGate.call(host, { slug: "curio-x09" }), "rewritten");
  assert.equal(calls.fix, 1);
  assert.equal(existsSync(path.join(box.workdir, "approvals.json")), false, "nothing is approved");
});
