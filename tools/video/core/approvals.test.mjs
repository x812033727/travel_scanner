import assert from "node:assert/strict";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { ANIME_APPROVAL_GATES, approvalState, approve, readApprovals } from "./approvals.mjs";
import { LONG_ANIME_POLICY, runtimePolicyHash } from "./anime-policy.mjs";
import { dramaFixture, sandbox } from "./fixtures/load.mjs";

function approvalFixture(t) {
  const box = sandbox("fixture-drama", "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = {
    ...dramaFixture(), category: "anime", production_policy: LONG_ANIME_POLICY, target_minutes: [22, 22], look: { preset: "anime-2d" },
    runtime_spec: { body_target_seconds: 1320, op_ed_budget_seconds: 180, broadcast_slot_seconds: 1800, slot_reserve_seconds: 300 },
    series: { slug: "original-anime", episode: 1, chapter: 1, planned_episodes: 120, open_ended: false, closed_ending: false, kind: "series", genre: "custom", lead: "ensemble" },
  };
  const save = () => writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  save();
  mkdirSync(path.join(box.workdir, "upload"), { recursive: true });
  writeFileSync(path.join(box.dir, "script.md"), "unchanged screenplay fixture");
  writeFileSync(path.join(box.workdir, "timeline.json"), "unchanged timeline fixture bytes");
  writeFileSync(path.join(box.workdir, "final.mp4"), "local approval fixture, not real media");
  writeFileSync(path.join(box.workdir, "upload", "metadata.json"), "unchanged package fixture bytes");
  return { ...box, doc, save, places: { docDir: box.dir, workdir: box.workdir } };
}

test("marked script, audio, final and publish approvals bind episode context even when their file bytes stay unchanged", async (t) => {
  const box = approvalFixture(t);
  const originalHash = runtimePolicyHash(box.doc);
  for (const gate of ANIME_APPROVAL_GATES) {
    const entry = await approve({ gate, ...box.places });
    assert.equal(entry.runtime_policy_hash, originalHash, gate);
    assert.equal((await approvalState({ gate, ...box.places })).status, "approved", gate);
  }
  box.doc.series.episode = 2;
  box.save();
  const nextHash = runtimePolicyHash(box.doc);
  for (const gate of ANIME_APPROVAL_GATES) {
    assert.equal((await approvalState({ gate, ...box.places })).status, "stale", gate);
    const count = readApprovals(box.workdir).approvals.length;
    await assert.rejects(approve({ gate, ...box.places, expected_runtime_policy_hash: originalHash }), /episode context has changed/);
    assert.equal(readApprovals(box.workdir).approvals.length, count, "an old remote approval cannot be relabelled with the new context");
    await approve({ gate, ...box.places, expected_runtime_policy_hash: nextHash });
    assert.equal((await approvalState({ gate, ...box.places })).status, "approved", gate);
  }
});

test("removing or corrupting a marked policy never revives its previous approval as ordinary drama", async (t) => {
  const box = approvalFixture(t);
  await approve({ gate: "final", ...box.places });
  const policy = box.doc.production_policy;
  const runtime = box.doc.runtime_spec;
  delete box.doc.production_policy;
  delete box.doc.runtime_spec;
  box.save();
  assert.equal((await approvalState({ gate: "final", ...box.places })).status, "stale");
  box.doc.production_policy = "unknown-anime-policy";
  box.doc.runtime_spec = runtime;
  box.save();
  assert.equal((await approvalState({ gate: "final", ...box.places })).status, "stale");
  await assert.rejects(approve({ gate: "final", ...box.places }), /production_policy must/);
  box.doc.production_policy = policy;
  box.save();
  assert.equal((await approvalState({ gate: "final", ...box.places })).status, "approved", "the original unchanged context restores its original approval");
});

test("ordinary approvals retain their byte-only record and cannot be reused after opting into the explicit profile", async (t) => {
  const box = approvalFixture(t);
  const policy = box.doc.production_policy;
  const runtime = box.doc.runtime_spec;
  delete box.doc.production_policy;
  delete box.doc.runtime_spec;
  box.save();
  const entry = await approve({ gate: "script", ...box.places });
  assert.equal(Object.hasOwn(entry, "runtime_policy_hash"), false);
  assert.equal((await approvalState({ gate: "script", ...box.places })).status, "approved");
  box.doc.production_policy = policy;
  box.doc.runtime_spec = runtime;
  box.save();
  assert.equal((await approvalState({ gate: "script", ...box.places })).status, "stale");
  const outline = await approve({ gate: "outline", ...box.places });
  assert.equal(Object.hasOwn(outline, "runtime_policy_hash"), false, "outline and look gates preserve their existing contract");
});
