import assert from "node:assert/strict";
import test from "node:test";

import { answerDocument, documentDiscussionPayload } from "./discuss.mjs";

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
