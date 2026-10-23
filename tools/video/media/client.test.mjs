import assert from "node:assert/strict";
import test from "node:test";

import { judge, locate, pollOnce, submitImage } from "./client.mjs";

const options = (fetchImpl) => ({ site: "https://example.test", token: "test-token", fetchImpl, sleep: async () => {}, attempts: 3 });
const judged = { slug: "story-rolling-suitcase-v2", kind: "keyframe", files: [], rubric: [] };
const FOLLOWON_SLUGS = [
  "story-five-lego-legoland", "story-five-costco-hot-dog",
  "story-five-adidas-puma-brothers", "story-five-ajinomoto-chip-film",
  "story-five-pringles-vat-case",
];

test("a pilot judge call carries one operation ID and never repeats an uncertain provider answer", async () => {
  let calls = 0;
  let sent;
  const fetchImpl = async (_url, init) => {
    calls += 1;
    sent = JSON.parse(init.body);
    return new Response(JSON.stringify({ code: "video_media_judge_failed" }), { status: 502, headers: { "Content-Type": "application/json" } });
  };
  await assert.rejects(judge({ request: judged, ...options(fetchImpl) }), (error) => error.code === "video_media_outcome_uncertain" && error.who === "owner");
  assert.equal(calls, 1);
  assert.match(sent.operation_id, /^[0-9a-f]{8}-[0-9a-f-]{27,}$/i);
  assert.equal(sent.slug, judged.slug);
});

test("each follow-on judge and locate call carries an operation ID and stops on an uncertain answer", async () => {
  for (const slug of FOLLOWON_SLUGS) {
    for (const send of [
      (fetchImpl) => judge({ request: { ...judged, slug }, ...options(fetchImpl) }),
      (fetchImpl) => locate({ request: { slug, sha256: "a".repeat(64) }, ...options(fetchImpl) }),
    ]) {
      const calls = [];
      const fetchImpl = async (_url, init) => {
        calls.push(JSON.parse(init.body));
        return new Response(JSON.stringify({ code: "video_media_judge_failed" }), { status: 502, headers: { "Content-Type": "application/json" } });
      };
      await assert.rejects(send(fetchImpl), (error) => error.code === "video_media_outcome_uncertain" && error.who === "owner");
      assert.equal(calls.length, 1, `${slug}: uncertain request must not retry`);
      assert.equal(calls[0].slug, slug);
      assert.match(calls[0].operation_id, /^[0-9a-f]{8}-[0-9a-f-]{27,}$/i);
    }
  }
});

test("a lost pilot locate answer is held for owner reconciliation", async () => {
  let calls = 0;
  const fetchImpl = async () => { calls += 1; throw new Error("connection reset after send"); };
  await assert.rejects(locate({ request: { slug: "story-conveyor-belt-sushi", sha256: "a".repeat(64) }, ...options(fetchImpl) }), (error) => error.code === "video_media_outcome_uncertain" && error.who === "owner");
  assert.equal(calls, 1);
});

test("ordinary judge calls retain the existing retry behavior", async () => {
  let calls = 0;
  const fetchImpl = async () => {
    calls += 1;
    return calls === 1
      ? new Response(JSON.stringify({ code: "video_media_judge_failed" }), { status: 502, headers: { "Content-Type": "application/json" } })
      : new Response(JSON.stringify({ passed: true }), { status: 200, headers: { "Content-Type": "application/json" } });
  };
  const result = await judge({ request: { ...judged, slug: "another-video" }, ...options(fetchImpl) });
  assert.equal(result.passed, true);
  assert.equal(calls, 2);
});

test("a pilot image submission stops after one ambiguous answer", async () => {
  let calls = 0;
  const fetchImpl = async () => {
    calls += 1;
    throw new Error("connection reset after submit");
  };
  await assert.rejects(
    submitImage({ request: { slug: "story-rolling-suitcase-v2", purpose: "keyframe", prompt: "a suitcase" }, ...options(fetchImpl) }),
    (error) => error.code === "video_media_outcome_uncertain" && error.who === "owner",
  );
  assert.equal(calls, 1);
});

test("each follow-on image submission stops after one ambiguous answer", async () => {
  for (const slug of FOLLOWON_SLUGS) {
    let calls = 0;
    const fetchImpl = async (_url, init) => {
      calls += 1;
      assert.equal(JSON.parse(init.body).slug, slug);
      throw new Error("connection reset after submit");
    };
    await assert.rejects(
      submitImage({ request: { slug, purpose: "keyframe", prompt: "story illustration" }, ...options(fetchImpl) }),
      (error) => error.code === "video_media_outcome_uncertain" && error.who === "owner",
    );
    assert.equal(calls, 1, slug);
  }
});

test("a budget refusal during job polling reaches the owner without retries", async () => {
  let calls = 0;
  const fetchImpl = async () => {
    calls += 1;
    return new Response(JSON.stringify({ code: "video_budget_exhausted", detail: "cap" }), {
      status: 429, headers: { "Content-Type": "application/json" },
    });
  };
  await assert.rejects(
    pollOnce({ jobId: "00000000-0000-4000-8000-000000000001", ...options(fetchImpl) }),
    (error) => error.code === "video_budget_exhausted" && error.who === "owner",
  );
  assert.equal(calls, 1);
});

test("an uncertain pilot job refuses a fresh submit as an owner reconciliation", async () => {
  let calls = 0;
  const fetchImpl = async () => {
    calls += 1;
    return new Response(JSON.stringify({ code: "video_media_outcome_uncertain", detail: "reconcile old job" }), {
      status: 409, headers: { "Content-Type": "application/json" },
    });
  };
  await assert.rejects(
    submitImage({ request: { slug: "story-rolling-suitcase-v2", purpose: "keyframe", prompt: "a suitcase" }, ...options(fetchImpl) }),
    (error) => error.code === "video_media_outcome_uncertain" && error.who === "owner",
  );
  assert.equal(calls, 1);
});
