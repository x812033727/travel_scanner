import assert from "node:assert/strict";
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { approve, approvalState } from "./approvals.mjs";
import { audioEvidenceProblems, bindAudioEvidence, currentAudioCheck } from "./audio-evidence.mjs";
import { fixture, fixtureLexicon, sandbox } from "./fixtures/load.mjs";

test("audio approval rejects missing bindings and changed take or narration bytes even at the same duration", async () => {
  const box = sandbox();
  const timeline = writeSyntheticNarration(fixture(), fixtureLexicon(), box.workdir);
  const places = { docDir: box.dir, workdir: box.workdir, gate: "audio" };
  assert.deepEqual(audioEvidenceProblems(timeline, box.workdir), []);
  await approve(places);
  assert.equal((await approvalState(places)).status, "approved");
  for (const relative of [`audio/${timeline.lines[0].id}.wav`, "narration.wav"]) {
    const file = path.join(box.workdir, relative);
    const before = readFileSync(file);
    const changed = Buffer.from(before); changed[48] ^= 1;
    writeFileSync(file, changed);
    assert.equal((await approvalState(places)).status, "stale");
    await assert.rejects(approve(places), /differs from the take/);
    writeFileSync(file, before);
  }
  const unbound = structuredClone(timeline);
  delete unbound.audio_evidence;
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(unbound));
  assert.equal((await approvalState(places)).status, "stale");
  await assert.rejects(approve(places), /no current audio evidence/);
  assert.deepEqual(bindAudioEvidence(unbound, box.workdir), timeline);
});

test("transcript judgments cannot clear a different take, a missing hash, or an unrelated line", () => {
  const timeline = { lines: [{ id: "same", audio_sha256: "a".repeat(64) }, { id: "redo", audio_sha256: "b".repeat(64) }, { id: "old1" }] };
  const good = { clip: "a".repeat(16), match: true };
  const check = { lines: { same: good, redo: good, old1: good, extra: good } };
  assert.deepEqual(currentAudioCheck(check, timeline).lines, { same: good });
});
