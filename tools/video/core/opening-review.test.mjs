import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { sandbox } from "./fixtures/load.mjs";
import { needsOpeningReview, OPENING_PERSONAS, OPENING_REVIEW_MIN_SCORE, OPENING_REVIEW_SECONDS, openingPacket, openingReviewProblems, openingReviewRecord } from "./opening-review.mjs";

function capture(box) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root, env: { VIDEO_WORKDIR: box.work }, home: box.base,
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

const pass = (persona, agent = `reader-${persona}`) => ({ agent, persona, score: 9, would_stay_300: true, swipe_at: null, problems: [] });
const allPass = () => Object.keys(OPENING_PERSONAS).map((persona) => pass(persona));

test("the opening review reads 300 seconds with three readers, one per viewer, all strict (owner 2026-11-19)", () => {
  assert.equal(OPENING_REVIEW_SECONDS, 300);
  assert.equal(OPENING_REVIEW_MIN_SCORE, 8.5);
  assert.deepEqual(Object.keys(OPENING_PERSONAS), ["newcomer", "scroller", "stickler"]);
  const { doc } = episode();
  const packet = openingPacket(doc);
  assert.match(packet, /前 300 秒觀眾審查/);
  assert.match(packet, /縮圖大字/);
  assert.match(packet, /問題菜單/);
  assert.match(packet, /沒頭沒尾/);
  assert.match(packet, /- \[00:00\]/);

  assert.deepEqual(openingReviewProblems(doc, openingReviewRecord(doc, allPass(), { author: "writer" })), []);
  assert.match(openingReviewProblems(doc, null)[0], /no opening review yet/);
  const two = openingReviewRecord(doc, allPass().slice(0, 2), { author: "writer" });
  assert.ok(openingReviewProblems(doc, two).some((problem) => /no reader read as stickler/.test(problem)), "every viewer is read");
  const same = openingReviewRecord(doc, Object.keys(OPENING_PERSONAS).map((persona) => pass(persona, "one-agent")), { author: "writer" });
  assert.ok(openingReviewProblems(doc, same).some((problem) => /different agent/.test(problem)));
  const self = openingReviewRecord(doc, [pass("newcomer", "writer"), pass("scroller"), pass("stickler")], { author: "writer" });
  assert.ok(openingReviewProblems(doc, self).some((problem) => /author cannot be a reader/.test(problem)));
  const low = openingReviewRecord(doc, [{ ...pass("newcomer"), score: 8 }, pass("scroller"), pass("stickler")], { author: "writer" });
  assert.ok(openingReviewProblems(doc, low).some((problem) => /under 8.5/.test(problem)));
  const swipe = openingReviewRecord(doc, [pass("newcomer"), { ...pass("scroller"), would_stay_300: false, swipe_at: "1:40" }, pass("stickler")], { author: "writer" });
  assert.ok(openingReviewProblems(doc, swipe).some((problem) => /swipe away at 1:40/.test(problem)));
  const nit = openingReviewRecord(doc, [pass("newcomer"), pass("scroller"), { ...pass("stickler"), problems: [{ at: "0:42", line: "某句", why: "沒交代是誰", fix: "先說他是誰" }] }], { author: "writer" });
  assert.ok(openingReviewProblems(doc, nit).some((problem) => /沒交代是誰/.test(problem)), "any problem named keeps it from passing");

  const edited = structuredClone(doc);
  edited.scenes[0].lines[0].text += "改了一句。";
  assert.ok(openingReviewProblems(edited, openingReviewRecord(doc, allPass(), { author: "writer" })).some((problem) => /script changed/.test(problem)), "an edit asks for a new round");
  assert.equal(needsOpeningReview({ slug: "daily-ai-20261119" }), false, "other series are untouched");
});

test("tts refuses a hand-made 原來如此 episode until the opening review passes; the command records a round", async () => {
  const { box } = episode();
  const blocked = capture(box);
  assert.notEqual(await main(["tts", "--slug", box.slug], blocked.ctx), EXIT.ok);
  assert.match(blocked.out.stderr, /have not passed the opening review/);
  const dry = capture(box);
  assert.equal(await main(["tts", "--slug", box.slug, "--dry-run"], dry.ctx), EXIT.ok, "a dry run only prices");

  const packet = capture(box);
  assert.equal(await main(["opening-review", "--slug", box.slug], packet.ctx), EXIT.ok, packet.out.stderr);
  assert.match(readFileSync(path.join(box.workdir, "review", "opening-packet.md"), "utf8"), /前 300 秒觀眾審查/);

  const answers = path.join(box.base, "answers.json");
  writeFileSync(answers, JSON.stringify([pass("newcomer"), { ...pass("scroller"), score: 7 }, pass("stickler")]));
  const failed = capture(box);
  assert.equal(await main(["opening-review", "--slug", box.slug, "--record", answers, "--author", "writer"], failed.ctx), EXIT.lint);
  assert.match(failed.out.stdout, /round 1 failed/);

  writeFileSync(answers, JSON.stringify(allPass()));
  const passed = capture(box);
  assert.equal(await main(["opening-review", "--slug", box.slug, "--record", answers, "--author", "writer"], passed.ctx), EXIT.ok, passed.out.stdout);
  assert.match(passed.out.stdout, /round 2 passed/);
  const after = capture(box);
  await main(["tts", "--slug", box.slug], after.ctx);
  assert.doesNotMatch(after.out.stderr, /opening review/, "past the gate (the voice itself still needs its login)");

  mkdirSync(box.workdir, { recursive: true });
  writeFileSync(path.join(box.workdir, "auto.json"), "{}");
  assert.equal(needsOpeningReview({ slug: box.slug }, { workdir: box.workdir }), false, "the host's worker keeps its own blind panel");
});
