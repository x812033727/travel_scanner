import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { sandbox } from "./fixtures/load.mjs";
import { askOpeningReview, needsOpeningReview, openingHash, OPENING_PERSONAS, OPENING_REVIEW_MIN_SCORE, OPENING_REVIEW_SECONDS, openingPacket, openingReviewProblems, openingReviewRecord, parseOpeningAnswer } from "./opening-review.mjs";

const SITE = "https://mokaair.test";

function capture(box, fetchImpl = null) {
  const out = { stdout: "", stderr: "" };
  // Only the site's readers need the token; tts without one stops before any voice request.
  const env = fetchImpl ? { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: "t".repeat(40), MOKAAIR_SITE: SITE } : { VIDEO_WORKDIR: box.work };
  return {
    out,
    ctx: {
      root: box.root, env, home: box.base,
      ...(fetchImpl ? { fetch: fetchImpl } : {}),
      sleep: async () => {},
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-11-19T05:00:00Z"),
    },
  };
}

function episode(slug = "sothatswhy-x01") {
  const box = sandbox(slug, "drama");
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  doc.slug = slug;
  writeFileSync(file, JSON.stringify(doc));
  return { box, doc, file };
}

let current = null;
const pass = (persona, extra = {}) => ({ opening_hash: current, agent: `site:claude-test#${persona}`, via: "site", model: "claude-test", persona, score: 9, would_stay_300: true, swipe_at: null, problems: [], ...extra });
const allPass = () => Object.keys(OPENING_PERSONAS).map((persona) => pass(persona));

/** A site whose verifier answers as `answer(payload)` says. */
function fakeSite(answer) {
  const calls = [];
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    const body = init.body ? JSON.parse(init.body) : null;
    if (pathname === "/api/video/automation/run") {
      calls.push(body);
      return new Response(JSON.stringify({ text: `好的：\n${JSON.stringify(answer(body.payload))}`, provider: "anthropic", model: "claude-test", input_tokens: 10, output_tokens: 5, usage: { tokens: 15, token_budget: 1_000_000, drafts: 0, draft_budget: 8, calls: 1, failed_calls: 0 } }), { status: 200, headers: { "content-type": "application/json" } });
    }
    return new Response(JSON.stringify({ code: "not_found", detail: pathname }), { status: 404, headers: { "content-type": "application/json" } });
  };
  return { calls, fetchImpl };
}
const happy = (payload) => ({ opening_hash: payload.opening_hash, persona: payload.persona, agent: "x", score: 9, would_stay_300: true, swipe_at: null, problems: [] });

test("the opening review reads 300 seconds with three site readers, one per viewer, all strict (owner 2026-11-19)", () => {
  assert.equal(OPENING_REVIEW_SECONDS, 300);
  assert.equal(OPENING_REVIEW_MIN_SCORE, 8.5);
  assert.deepEqual(Object.keys(OPENING_PERSONAS), ["newcomer", "scroller", "stickler"]);
  const { doc } = episode();
  current = openingHash(doc);
  const packet = openingPacket(doc);
  assert.ok(packet.includes(current), "the packet carries the hash each reader echoes");
  assert.ok(/精衛：|炎帝：/.test(packet) && !/jingwei：|yandi：/.test(packet), "readers see the characters' names, not their ids");
  assert.match(packet, /縮圖大字/);
  assert.match(packet, /問題菜單/);
  assert.match(packet, /沒頭沒尾/);
  assert.match(packet, /- \[00:00\]/);

  assert.deepEqual(openingReviewProblems(doc, openingReviewRecord(doc, allPass())), []);
  assert.match(openingReviewProblems(doc, null)[0], /--record.*--ask/);
  const unrecorded = openingReviewRecord(doc, Object.keys(OPENING_PERSONAS).map((persona) => pass(persona, { via: undefined, model: undefined })));
  assert.ok(openingReviewProblems(doc, unrecorded).some((problem) => /not a recorded reader/.test(problem)), "a verdict counts only through --record or --ask");
  const session = (persona, agent = `subagent-${persona}`, extra = {}) => pass(persona, { via: "session", model: undefined, agent, ...extra });
  const sessionRound = (list, author = "writer") => openingReviewRecord(doc, list, { author });
  assert.deepEqual(openingReviewProblems(doc, sessionRound([session("newcomer"), session("scroller"), session("stickler")])), [], "three subagents of the session that made it");
  assert.ok(openingReviewProblems(doc, sessionRound([session("newcomer", "Writer "), session("scroller"), session("stickler")])).some((problem) => /author cannot be a reader/.test(problem)), "the author never reads its own script, whatever the case or spaces");
  assert.ok(openingReviewProblems(doc, openingReviewRecord(doc, [session("newcomer"), session("scroller"), session("stickler")])).some((problem) => /names its author/.test(problem)));
  const two = openingReviewRecord(doc, allPass().slice(0, 2));
  assert.ok(openingReviewProblems(doc, two).some((problem) => /no reader read as stickler/.test(problem)), "every viewer is read");
  const same = openingReviewRecord(doc, [pass("newcomer", { agent: "Reader " }), pass("scroller", { agent: "reader" }), pass("stickler")]);
  assert.ok(openingReviewProblems(doc, same).some((problem) => /different agent/.test(problem)), "names compare without case or spaces");
  const low = openingReviewRecord(doc, [pass("newcomer", { score: 8 }), pass("scroller"), pass("stickler")]);
  assert.ok(openingReviewProblems(doc, low).some((problem) => /under 8.5/.test(problem)));
  const swipe = openingReviewRecord(doc, [pass("newcomer"), pass("scroller", { would_stay_300: false, swipe_at: "01:40" }), pass("stickler")]);
  assert.ok(openingReviewProblems(doc, swipe).some((problem) => /swipe away at 01:40/.test(problem)));
  const nit = openingReviewRecord(doc, [pass("newcomer"), pass("scroller"), pass("stickler", { problems: [{ at: "00:42", line: "某句", why: "沒交代是誰", fix: "先說他是誰" }] })]);
  assert.ok(openingReviewProblems(doc, nit).some((problem) => /沒交代是誰/.test(problem)), "any problem named keeps it from passing");
  const text = openingReviewRecord(doc, [pass("newcomer"), pass("scroller"), pass("stickler", { problems: "drags at 1:40" })]);
  assert.ok(openingReviewProblems(doc, text).some((problem) => /must be a list/.test(problem)));
  const stale = openingReviewRecord(doc, [pass("newcomer", { opening_hash: "0".repeat(64) }), pass("scroller"), pass("stickler")]);
  assert.ok(openingReviewProblems(doc, stale).some((problem) => /read another version/.test(problem)), "a reader of an older packet does not count");

  const passed = openingReviewRecord(doc, allPass());
  const edited = structuredClone(doc);
  edited.scenes[0].lines[0].text += "改了一句。";
  assert.ok(openingReviewProblems(edited, passed).some((problem) => /first 300 seconds changed/.test(problem)), "an edit in the opening asks for a new round");
  const retitled = { ...structuredClone(doc), youtube: { ...doc.youtube, title: "另一個標題" } };
  assert.ok(openingReviewProblems(retitled, passed).some((problem) => /changed after the opening review/.test(problem)), "so does a new title");
  const reheadlined = { ...structuredClone(doc), thumbnail: { ...doc.thumbnail, data: { ...doc.thumbnail.data, headline: "新大字" } } };
  assert.ok(openingReviewProblems(reheadlined, passed).length > 0, "and a new thumbnail headline");

  assert.equal(needsOpeningReview(doc, { voiced: true }), false, "a voice already made for this script is not asked again");
  assert.equal(needsOpeningReview(doc, { retake: true }), false, "nor a retake");
  assert.equal(needsOpeningReview({ slug: "daily-ai-20261119" }), false, "other series are untouched");
  assert.deepEqual(parseOpeningAnswer("```json\n{\"score\": 9}\n```"), { score: 9 });
});

test("askOpeningReview sends one verifier request per viewer and records that the site answered", async () => {
  const { doc } = episode();
  const calls = [];
  const api = { run: async (...args) => { calls.push(args); return { text: JSON.stringify(happy(args[3])), model: "claude-test", input_tokens: 1, output_tokens: 1 }; } };
  const verdicts = await askOpeningReview(api, doc);
  assert.deepEqual(calls.map((call) => [call[0], call[5], call[6], call[3].persona]), [["verifier", "drama", "opening-review", "newcomer"], ["verifier", "drama", "opening-review", "scroller"], ["verifier", "drama", "opening-review", "stickler"]]);
  assert.ok(verdicts.every((verdict) => verdict.via === "site" && verdict.model === "claude-test"));
  assert.deepEqual(openingReviewProblems(doc, openingReviewRecord(doc, verdicts)), []);
  const broken = await askOpeningReview({ run: async () => ({ text: "我覺得很好看", model: "m" }) }, doc);
  assert.ok(openingReviewProblems(doc, openingReviewRecord(doc, broken)).some((problem) => /could not be read/.test(problem)), "an unreadable answer fails, it never passes");
});

test("tts refuses a hand-made 原來如此 episode until the site's readers pass it; --dry-run says where it stands", async () => {
  const { box } = episode();
  const blocked = capture(box);
  assert.notEqual(await main(["tts", "--slug", box.slug], blocked.ctx), EXIT.ok);
  assert.match(blocked.out.stderr, /have not passed the opening review/);
  const dry = capture(box);
  assert.equal(await main(["tts", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, "a dry run only prices");
  assert.match(dry.out.stdout, /opening review: not passed yet \(opening-review --slug sothatswhy-x01, then --record three subagents' answers or --ask\)/);

  const strict = fakeSite((payload) => ({ ...happy(payload), ...(payload.persona === "scroller" ? { score: 7, would_stay_300: false, swipe_at: "02:10", problems: [{ at: "02:10", line: "…", why: "拖", fix: "砍半" }] } : {}) }));
  const failed = capture(box, strict.fetchImpl);
  assert.equal(await main(["opening-review", "--slug", box.slug, "--ask"], failed.ctx), EXIT.lint, failed.out.stderr);
  assert.equal(strict.calls.length, 3, "three requests, one per viewer");
  assert.ok(strict.calls.every((call) => call.stage === "verifier" && call.variant === "opening-review"));
  assert.match(failed.out.stdout, /round 1 not passed/);
  assert.match(failed.out.stdout, /swipe away at 02:10/);
  assert.match(readFileSync(path.join(box.workdir, "review", "opening-packet.md"), "utf8"), /前 300 秒觀眾審查/);

  const good = fakeSite(happy);
  const passed = capture(box, good.fetchImpl);
  assert.equal(await main(["opening-review", "--slug", box.slug, "--ask"], passed.ctx), EXIT.ok, passed.out.stdout + passed.out.stderr);
  assert.match(passed.out.stdout, /round 2 passed/);
  const check = capture(box);
  assert.equal(await main(["opening-review", "--slug", box.slug, "--check"], check.ctx), EXIT.ok);
  const after = capture(box);
  await main(["tts", "--slug", box.slug], after.ctx);
  assert.doesNotMatch(after.out.stderr, /opening review/, "past the gate");

  mkdirSync(box.workdir, { recursive: true });
  writeFileSync(path.join(box.workdir, "auto.json"), "{}");
  assert.equal(needsOpeningReview({ slug: box.slug }, { workdir: box.workdir }), false, "the host's worker keeps its own blind panel");
});

test("the site's readers are kept robust: a lost request keeps the answers before it, 無 means no swipe, the tool binds the hash, pauses alone ask for nothing", async () => {
  const { doc } = episode();
  current = openingHash(doc);
  let n = 0;
  const saved = [];
  const api = { run: async (...args) => {
    n += 1;
    if (n === 2) throw new Error("429 too many");
    return { text: JSON.stringify({ ...happy(args[3]), opening_hash: "a mis-copied hash", swipe_at: "無" }), model: "claude-test" };
  } };
  const verdicts = await askOpeningReview(api, doc, { onVerdict: (list) => saved.push(list.length) });
  assert.deepEqual(saved, [1, 2, 3], "each answer is saved as it arrives");
  assert.equal(verdicts[0].swipe_at, null, "無 is no swipe");
  assert.equal(verdicts[0].opening_hash, current, "the tool binds the packet it sent");
  assert.equal(verdicts[1].via, "error");
  const problems = openingReviewProblems(doc, openingReviewRecord(doc, verdicts));
  assert.ok(problems.some((problem) => /did not answer: 429/.test(problem)), "the lost reader fails the round");
  assert.ok(!problems.some((problem) => /newcomer.*read another version/.test(problem)));

  const paced = { ...structuredClone(doc), pauses: { line_ms: 900, scene_ms: 2000 } };
  assert.equal(openingHash(paced), current, "a pause change alone keeps the review");
});

test("tts --redo on a script never voiced is a first voice and still waits for the review", async () => {
  const { box } = episode();
  const redo = path.join(box.base, "flags.json");
  writeFileSync(redo, JSON.stringify({ flags: [] }));
  const run = capture(box);
  assert.notEqual(await main(["tts", "--slug", box.slug, "--redo", redo], run.ctx), EXIT.ok);
  assert.match(run.out.stderr, /have not passed the opening review/);
});

test("a session's own three subagents can pass the review through --record, with the author named apart", async () => {
  const { box } = episode();
  current = openingHash(JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8")));
  const packet = capture(box);
  assert.equal(await main(["opening-review", "--slug", box.slug], packet.ctx), EXIT.ok);
  assert.match(packet.out.stdout, /three fresh subagents of this session/);
  const answers = path.join(box.base, "answers.json");
  const reader = (persona, agent) => ({ opening_hash: current, agent, persona, score: 9, would_stay_300: true, swipe_at: "無", problems: [] });
  writeFileSync(answers, JSON.stringify([reader("newcomer", "writer"), reader("scroller", "b"), reader("stickler", "c")]));
  const self = capture(box);
  assert.equal(await main(["opening-review", "--slug", box.slug, "--record", answers, "--author", "writer"], self.ctx), EXIT.lint);
  assert.match(self.out.stdout, /author cannot be a reader/);
  writeFileSync(answers, JSON.stringify([reader("newcomer", "a"), reader("scroller", "b"), reader("stickler", "c")]));
  const ok = capture(box);
  assert.equal(await main(["opening-review", "--slug", box.slug, "--record", answers, "--author", "writer"], ok.ctx), EXIT.ok, ok.out.stdout);
  const after = capture(box);
  await main(["tts", "--slug", box.slug], after.ctx);
  assert.doesNotMatch(after.out.stderr, /opening review/, "past the gate");
});
