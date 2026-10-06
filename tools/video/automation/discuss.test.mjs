import assert from "node:assert/strict";
import path from "node:path";
import test from "node:test";

import { sandbox } from "../core/fixtures/load.mjs";
import { atomicWrite } from "../core/paths.mjs";
import { answerDocument, answerScript, documentDiscussionPayload } from "./discuss.mjs";
import { Automation } from "./flow.mjs";

test("discussion retains draft parent versions and missing parents without granting approval", () => {
  const automation = { reference: () => ({}), dramaPayload: () => ({ drama_settings: {} }) };
  const doc = { kind: "setting", version: 2, status: "review", needs_reconciliation: true, body_md: "# New cast", body_json: {} };
  const job = {
    subject: "chapter:1", message: { body_md: "Revise this chapter to match the new cast" },
    series: { slug: "preloaded" }, doc: { ...doc, kind: "chapter", version: 1 },
    context: { setting: doc, outline: null, chapter_range: [1, 10] },
  };
  const payload = documentDiscussionPayload(automation, job);
  assert.equal(payload.setting.version, 2);
  assert.equal(payload.setting.status, "review");
  assert.equal(payload.setting.needs_reconciliation, true);
  assert.equal(payload.setting.body_md, doc.body_md);
  assert.equal(payload.outline, null);
  assert.equal(payload.chapter_number, 1);
  assert.match(payload.context_instruction, /provisional/);
  assert.match(payload.context_instruction, /matching complete body_md and body_json/);
});

test("a document answer echoes its delivered snapshot and reports a refused revision accurately", async () => {
  const binding = "a".repeat(64);
  const revised = { body_md: "# Setting", body_json: { characters: [{ id: "lead", name: "Lead", appearance: "red coat" }], mysteries: [{ id: "letter", question: "Who wrote it?" }] } };
  const calls = [];
  const automation = {
    reference: () => ({}), dramaPayload: () => ({ drama_settings: {} }),
    stage: async () => ({ reply: "Revised", revised }),
    api: { messageAnswer: async (id, body) => { calls.push({ id, body }); return { revision: null, revision_refused: "文件已更新" }; } },
  };
  const result = await answerDocument(automation, {
    message: { id: "m1", body_md: "Reconcile" }, subject: "setting",
    series: { slug: "preloaded" }, revision_context: binding,
    doc: { ...revised, kind: "setting", version: 2, status: "review" },
  });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].body.revision_context, binding);
  assert.deepEqual(calls[0].body.revised.body_json, revised.body_json);
  assert.match(result, /only the reply was kept: 文件已更新/);
});

test("a line on a screenplay is held while its video is not at rest: a lane is moving it, a lane set it aside in this run, its writer is still running, or it waits on its own from an earlier round; no model is asked and nothing is answered", async () => {
  const box = sandbox();
  const slug = "held-e001";
  const save = (extra = {}) => atomicWrite(path.join(box.work, slug, "auto.json"), JSON.stringify({ slug, status: "active", format: "drama", notes: [], created_at: "2026-10-06T01:00:00Z", ...extra }));
  save();
  let now = Date.parse("2026-10-06T10:00:00Z");
  const said = [];
  const replies = [];
  let answering = false;
  const ctx = { root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, stdout: { write: (text) => said.push(text) }, stderr: { write: () => {} }, now: () => new Date(now) };
  const api = {
    messageAnswer: async (id, body) => {
      assert.ok(answering, "nothing is answered for a video at work");
      replies.push({ id, ...body });
    },
  };
  const automation = new Automation(ctx, api, {});
  automation.stage = async () => assert.fail("no model request for a video at work");
  const job = { message: { id: "m1", body_md: "沈瀾為什麼不回答？" }, subject: "script:1", series: { slug: "held" }, episode: { slug } };

  automation.busy.add(slug);
  assert.equal(await answerScript(automation, job), null, "another lane is moving it");
  automation.busy.clear();
  automation.skipped.add(slug);
  assert.equal(await answerScript(automation, job), null, "a lane set it aside in this run");
  automation.skipped.clear();
  automation.pendingUntil.set(slug, now + 300_000);
  assert.equal(await answerScript(automation, job), null, "its writer is still running on the server");
  // A video deferred in an earlier round is passed over before its unit, so this run never looked
  // its writer up: a job sent before the deferral may still be running, and the line waits too.
  automation.pendingUntil.clear();
  save({ deferred_until: new Date(now + 600_000).toISOString(), defer_count: 2 });
  assert.equal(await answerScript(automation, job), null, "it waits on its own");
  assert.deepEqual(said, ["held-e001: the owner's line on script:1 waits; the video is being worked on or waits on its own, and the line is answered once it is at rest\n"], "said once a run");

  // At rest (the wait is over, and so would a pending writer's recheck be), the line is taken up: this video has no screenplay yet, which the owner is told.
  now += 600_000;
  answering = true;
  assert.match(await answerScript(automation, job), /held-e001 has no video\.json yet; the owner is told and the thread waits$/);
  // A count of deferrals whose wait is over holds nothing: the next unit visits the video before any line.
  save({ defer_count: 2 });
  assert.match(await answerScript(automation, job), /held-e001 has no video\.json yet/);
  assert.deepEqual(replies.map((reply) => reply.id), ["m1", "m1"]);
});
