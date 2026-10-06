import assert from "node:assert/strict";
import { rmSync, writeFileSync } from "node:fs";
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

const HELD = "held-e001";
const OLDER = "older-video";

/**
 * Two videos under two lanes that share what cli.mjs shares: the older one waits on the owner,
 * the newer one (HELD) has a screenplay and the owner's line on it, which the site hands over on
 * every call until it is answered. `advance(lane, state, clock)` plays a video's own unit and
 * `stage(clock)` answers a model request; every request is listed in `sent`.
 */
function discussed({ advance, stage }) {
  const box = sandbox();
  const save = (slug, extra = {}) => atomicWrite(path.join(box.work, slug, "auto.json"), JSON.stringify({ slug, status: "active", format: "drama", notes: [], verified: true, listener_done: true, created_at: slug === OLDER ? "2026-10-05T00:00:00Z" : "2026-10-05T01:00:00Z", ...extra }));
  save(OLDER);
  save(HELD);
  atomicWrite(path.join(box.root, "docs", "videos", HELD, "video.json"), JSON.stringify({ slug: HELD, scenes: [] }));
  const clock = { now: Date.parse("2026-10-06T10:00:00Z") };
  const ctx = { root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base, stdout: { write: () => {} }, stderr: { write: () => {} }, now: () => new Date(clock.now) };
  const waiting = [{ target: "script", subject: "script:1", message: { id: "m1", body_md: "沈瀾為什麼不回答？" }, thread: [], series: { slug: "held" }, episode: { slug: HELD } }];
  const answered = [];
  const sent = [];
  const api = {
    videos: async () => [],
    report: async () => {},
    settleRuns: async () => {},
    // Asking the site takes a moment, as every call does.
    messageNext: async () => {
      clock.now += 1_000;
      return waiting[0] ?? null;
    },
    messageAnswer: async (id) => {
      answered.push(id);
      waiting.shift();
    },
    seriesNext: async () => null,
    dramaNext: async () => null,
  };
  const settings = { enabled: true, max_waiting_drafts: 0, drama: { drama_enabled: true } };
  const shared = { busy: new Set(), skipped: new Set(), pendingUntil: new Map() };
  const lanes = [false, true].map((secondary) => {
    const lane = new Automation(ctx, api, settings, { ...shared, secondary });
    lane.languages = async () => null;
    lane.due = () => false;
    lane.scriptPayload = (_state, extra) => ({ ...extra });
    lane.freshIds = () => [];
    lane.stage = async (name, slug, _payload, _tokens, _format, variant) => {
      sent.push(`${name}:${variant ?? ""} for ${slug}`);
      return stage(clock);
    };
    lane.advance = (state) => advance(lane, state, clock);
    return lane;
  });
  return { clock, lanes, shared, api, waiting, answered, sent, save, work: box.work };
}

test("a discussion holds its video from the check to the answer: while its writer request is in flight no other lane runs the video's own stage, and the video is free again afterwards", async () => {
  let release;
  let asked;
  const flying = new Promise((resolve) => (release = resolve));
  const inFlight = new Promise((resolve) => (asked = resolve));
  let sentBack = false;
  const staged = [];
  const { lanes: [first, second], shared, sent, answered } = discussed({
    // The screenplay waits for the owner; once the owner sends it back, the video's own stage is due.
    advance: async (lane, state) => {
      if (state.slug !== HELD || !sentBack) return null;
      staged.push(lane.secondary ? "second lane" : "first lane");
      return `${state.slug}: screenplay rewritten after the owner's note`;
    },
    stage: async () => {
      asked();
      await flying;
      return { reply: "因為沈瀾此時不能說破。", revised: null };
    },
  });
  const discussing = first.step();
  await inFlight;
  assert.deepEqual([...shared.busy], [HELD], "the discussion holds its video as a lane's unit does");
  // The owner sends the screenplay back while the writer answers the line. Before: busy was
  // empty, so the second lane took the video and sent its own request beside the discussion's.
  sentBack = true;
  assert.equal(await second.step(), null, "the other lane leaves the video alone");
  assert.deepEqual([staged, sent], [[], ["writer:discuss for held-e001"]]);
  release();
  assert.equal(await discussing, "held-e001: the writer answered the owner on script:1");
  assert.deepEqual([[...shared.busy], answered], [[], ["m1"]], "let go once the line is answered");
  assert.equal(await second.step(), "held-e001: screenplay rewritten after the owner's note");
  assert.deepEqual(staged, ["second lane"]);

  // An exception on the way does not leave the video held.
  const broken = discussed({ advance: async () => null, stage: async () => { throw new TypeError("a bug"); } });
  await assert.rejects(broken.lanes[0].step(), TypeError);
  assert.deepEqual([...broken.shared.busy], []);
});

test("a discussion an earlier round left unfinished comes before its video's own stage on the first lane, and the other lanes leave the video to it; a saved run no line claims holds nothing on the first lane", async () => {
  // The owner sent the screenplay back: the video's own stage is due, once, on whichever lane takes it.
  const rewriting = (done) => async (_lane, state) => {
    if (state.slug !== HELD || done.includes("the video's own stage")) return null;
    done.push("the video's own stage");
    return `${state.slug}: screenplay rewritten after the owner's note`;
  };
  const done = [];
  const { lanes: [first, second], api, answered } = discussed({
    advance: rewriting(done),
    stage: async () => {
      done.push("the discussion");
      return { reply: "因為沈瀾此時不能說破。", revised: null };
    },
  });
  // What the receipt store lists while the writer job of last round's discussion has an answer still to take.
  let saved = [{ stage: "writer", variant: "discuss", status: "running" }];
  api.untakenRuns = (slug) => (slug === HELD ? saved : []);
  // Both lanes start their unit at once, as `auto` drives them. Before: whichever lane came to
  // the video first ran its own stage, and the rewrite left the discussion's saved request
  // matching no script, its paid answer set aside and bought again.
  assert.deepEqual(await Promise.all([first.step(), second.step()]), ["held-e001: the writer answered the owner on script:1", null]);
  assert.deepEqual([done, answered], [["the discussion"], ["m1"]]);
  // The unit settled the saved run, and the video is any lane's again.
  saved = [];
  assert.equal(await second.step(), "held-e001: screenplay rewritten after the owner's note");
  assert.deepEqual(done, ["the discussion", "the video's own stage"]);

  // A saved run whose line the site no longer hands over (answered for or withdrawn since): the
  // first lane finds no line and moves the video in the same unit, so nothing waits for ever.
  const moved = [];
  const orphan = discussed({ advance: rewriting(moved), stage: async () => assert.fail("no line, so no request") });
  orphan.waiting.length = 0;
  orphan.api.untakenRuns = (slug) => (slug === HELD ? [{ stage: "writer", variant: "anime-discuss-plan", status: "succeeded" }] : []);
  assert.equal(await orphan.lanes[1].step(), null, "the other lanes still leave it to the first");
  assert.equal(await orphan.lanes[0].step(), "held-e001: screenplay rewritten after the owner's note");

  // A saved run of the video's own writer is its own unit's to look up, on any lane: only a discussion's is waited for.
  const own = [];
  const writing = discussed({ advance: rewriting(own), stage: async () => assert.fail("no request") });
  writing.waiting.length = 0;
  writing.api.untakenRuns = () => [{ stage: "writer", variant: "episode", status: "running" }, { stage: "planner", variant: "discuss", status: "running" }];
  assert.equal(await writing.lanes[1].step(), "held-e001: screenplay rewritten after the owner's note");
});

test("a line waits for a video the unit's loop left alone, though the video's wait ran out while the loop visited the other videos", async () => {
  const { clock, lanes: [worker], shared, sent, answered, waiting, save, work } = discussed({
    // The older video's unit reads its status and its reviews: two seconds on the clock.
    advance: async (_lane, state, time) => {
      if (state.slug === OLDER) time.now += 2_000;
      return null;
    },
    stage: async () => ({ reply: "因為沈瀾此時不能說破。", revised: null }),
  });
  // The video's own writer fix was found still running five minutes ago; its recheck is due in one second.
  shared.pendingUntil.set(HELD, clock.now + 1_000);
  assert.equal(await worker.step(), null);
  // Before: the loop passed the video over (the recheck was not due), and three seconds later the
  // guard read the clock again, called the video at rest and sent writer/discuss beside the
  // running fix, whose job this unit never looked up.
  assert.deepEqual([sent, answered, waiting.length], [[], [], 1]);
  // The same for a wait saved in an earlier round that runs out during the loop.
  shared.pendingUntil.clear();
  save(HELD, { deferred_until: new Date(clock.now + 1_000).toISOString(), defer_count: 2 });
  assert.equal(await worker.step(), null);
  assert.deepEqual([sent, answered, waiting.length], [[], [], 1]);
  // A video its own STOP file holds is left alone by the loop too: its stages are held, and so is its line.
  save(HELD);
  writeFileSync(path.join(work, HELD, "STOP"), "");
  assert.equal(await worker.step(), null);
  assert.deepEqual([sent, answered, waiting.length], [[], [], 1]);
  rmSync(path.join(work, HELD, "STOP"));
  // The next unit visits the video first; at rest after that visit, its line is answered.
  assert.equal(await worker.step(), "held-e001: the writer answered the owner on script:1");
  assert.deepEqual([sent, answered, waiting.length], [["writer:discuss for held-e001"], ["m1"], 0]);
});
