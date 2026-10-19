import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import { dramaFixture, explainerFixture, fixture, fixtureBrief, fixtureLexicon, storyFixture, storySeries } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";
import {
  CALLBACK,
  DEFAULT_CADENCE,
  chapterOpenerProblems,
  HOOK_GAP_SECONDS,
  hookCadenceProblems,
  isNarrated,
  LABEL_OPENERS,
  loopProblems,
  mergePanelVerdicts,
  NARRATIVE_PANEL,
  narrationText,
  narrativeProblems,
  narrativeRecord,
  narrativeReviewMatches,
  NEXT_VIDEO,
  outroNextVideoProblems,
  PANEL_INSTRUCTIONS,
  PANEL_RULES_SHA256,
  panelPayload,
  panelVerdict,
  repeatedFactProblems,
  requiredLoops,
  STORY_PANEL_READERS,
  TIGHT_CADENCE,
} from "./narrative.mjs";
import { scriptCheckMatches } from "./script-check.mjs";
import { MIN_EPISODE_MINUTES } from "./schema.mjs";
import { estimateTimeline, FPS } from "./timeline.mjs";

// The fixture videos run seconds; the eight-minute floor has tests of its own.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const context = (overrides = {}) => ({ lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {}, ...overrides });
const messages = (problems) => problems.map((problem) => problem.message).join("\n");

// The minimal example stretched to episode length as lint.test.mjs stretches it: a 30 to 60 s
// condensation, then padded chapters whose sentences say nothing, then the outro. Each padded
// scene opens a chapter of its own, so the body has turns but no hooks between them.
const CONDENSATION = [
  { id: "cd01", text: "一八七二年十二月四日，一艘雙桅帆船在大西洋上漂著。" },
  { id: "cd02", text: "帆還張著，船身沒有傷，艙裡的水只到腳踝。" },
  { id: "cd03", text: "半年的食物和水都在，桌上的鍋子洗好了。" },
  { id: "cd04", text: "可是船上一個人都沒有。" },
  { id: "cd05", text: "船長、太太、兩歲的女兒，七個水手，都不在。" },
  { id: "cd06", text: "十個人，去了哪裡？" },
];
function stretched(doc = fixture(), { pad = "這一句只是把範例拉長到一集的長度，數字留在正文裡。" } = {}) {
  doc.target_minutes = [MIN_EPISODE_MINUTES, MIN_EPISODE_MINUTES + 4];
  doc.scenes[0].lines.push(...structuredClone(CONDENSATION));
  let n = 0;
  while (estimateTimeline(doc).total_frames / FPS / 60 < MIN_EPISODE_MINUTES + 0.5) {
    const lines = Array.from({ length: 6 }, () => ({ id: `pad${(n++).toString(36).padStart(4, "0")}`, text: pad }));
    doc.scenes.splice(doc.scenes.length - 1, 0, { id: `pad-${n}`, chapter: `第 ${n} 段`, template: "bullets", data: { title: "拉長", items: ["一"] }, lines });
  }
  return doc;
}
const padScenes = (doc) => doc.scenes.filter((scene) => scene.id.startsWith("pad-"));

test("a narrated video is a slides video, an explainer or a brand story; a drama with a cast and a compilation are not", () => {
  assert.equal(isNarrated(fixture()), true);
  assert.equal(isNarrated(explainerFixture()), true);
  assert.equal(isNarrated(storyFixture(), storySeries()), true);
  assert.equal(isNarrated(dramaFixture()), false);
  assert.equal(isNarrated({ format: "drama", look: { preset: "ink" }, scenes: [] }), false);
});

test("the narration as the panel reads it: the title, each chapter with its start, each line with its id and start", () => {
  const doc = fixture();
  const text = narrationText(doc, estimateTimeline(doc));
  assert.match(text, /^# AI 模型怎麼挑？三個問題幫你決定\n\n## 開場（00:00）\n\[k7p2 00:00\] 每次有新模型出來/);
  assert.match(text, /\n## 三個問題（00:1\d）\n\[x9fe 00:1\d\] 第一個問題是/);
  assert.match(text, /\n## 結論（00:2\d）\n/);
  assert.doesNotMatch(text, /reveal|template|bullets|emotion/);
  const payload = panelPayload(doc, estimateTimeline(doc));
  assert.deepEqual(Object.keys(payload), ["narration", "questions"]);
  assert.deepEqual(payload.questions.map((question) => question.id), NARRATIVE_PANEL.map((question) => question.id));
  assert.equal(payload.questions.some((question) => "required" in question), false, "the reader is not told which questions count");
});

test("a chapter that opens on a label is a warning; one that opens on the event is not", () => {
  const doc = fixture();
  const timeline = estimateTimeline(doc);
  assert.deepEqual(chapterOpenerProblems(doc, timeline), [], "「第一個問題是」 is the chapter's own content");
  for (const label of ["先講大家聽過的那個版本。", "打開檔案的第一頁，先回到她離開紐約的那一天。", "回到清單上，看看船上少了什麼。", "這一章回答三個問題。", "接下來我們來看第二點。", "最後一頁的線索，在熱那亞卸貨的時候才出現。", "第二頁是法庭的紀錄。"]) {
    const labelled = fixture();
    labelled.scenes[1].lines[0].text = label;
    const problems = chapterOpenerProblems(labelled, estimateTimeline(labelled));
    assert.deepEqual(problems.map((problem) => problem.path), ["scenes[1].lines[0] (x9fe)"], label);
    assert.match(problems[0].message, /opens on a label/);
  }
  assert.equal(LABEL_OPENERS.length, 10);
  const outro = fixture();
  outro.scenes[2].lines[0].text = "接下來，把這三個答案寫下來。";
  assert.deepEqual(chapterOpenerProblems(outro, estimateTimeline(outro)), [], "the outro's close is not a chapter opening");
});

test("the body carries an open loop at least every 90 seconds: a question, a forward hook, an escalation or a chapter turn", () => {
  assert.equal(HOOK_GAP_SECONDS, 90);
  const doc = fixture();
  assert.deepEqual(hookCadenceProblems(doc, estimateTimeline(doc)), [], "a body shorter than the gap is not read");
  // Each padded chapter is a turn: with six 23-character lines a chapter runs about 33 s, under the gap.
  const turns = stretched();
  assert.deepEqual(hookCadenceProblems(turns, estimateTimeline(turns)), []);
  // The same sentences in one long chapter: one stretch with nothing hanging.
  const flat = stretched();
  for (const scene of padScenes(flat)) delete scene.chapter;
  const problems = hookCadenceProblems(flat, estimateTimeline(flat));
  assert.equal(problems.length, 1);
  assert.match(problems[0].message, /no open loop between 00:\d\d and 0\d:\d\d \(\d+ s\)/);
  // A question every fourth scene, or a forward hook, or an escalation, closes the gaps.
  for (const device of ["那它到底怎麼做到的？", "先記住這個數字，等一下它會回來。", "但這還不是最怪的。"]) {
    const hooked = stretched();
    for (const scene of padScenes(hooked)) delete scene.chapter;
    padScenes(hooked).forEach((scene, index) => {
      if (index % 2 === 0) scene.lines[0].text = device;
    });
    assert.deepEqual(hookCadenceProblems(hooked, estimateTimeline(hooked)), [], device);
  }
});

test("the loops table: enough for the length, three planted in the condensation, none in the outro", () => {
  assert.deepEqual([requiredLoops(8), requiredLoops(10), requiredLoops(13), requiredLoops(3)], [2, 3, 4, 2]);
  const doc = stretched();
  const timeline = estimateTimeline(doc);
  const minutes = timeline.total_frames / FPS / 60;
  assert.match(messages(loopProblems(doc, timeline, minutes)), /0 open loops planted; a narrated video of about 9 minutes plants at least 3/);
  const pads = padScenes(doc);
  doc.loops = [
    { setup: "cd06", payoff: pads[3].lines[0].id, what: "十個人去了哪裡" },
    { setup: pads[0].lines[1].id, payoff: pads[4].lines[2].id, what: "那九個桶" },
    { setup: pads[1].lines[0].id, payoff: pads[5].lines[0].id, what: "劍上的痕跡" },
  ];
  // One teaser in the condensation is not enough: after its one scene it teases three later
  // moments (owner, 2026-10-13: the opening needs many hooks).
  assert.match(messages(loopProblems(doc, timeline, minutes)), /the condensation plants 1 loop; after its one scene it teases at least 3 later moments/);
  doc.loops[1].setup = "cd04";
  doc.loops[2].setup = "cd05";
  assert.deepEqual(loopProblems(doc, timeline, minutes), []);
  doc.loops[1].setup = pads[0].lines[1].id;
  doc.loops[2].setup = pads[1].lines[0].id;
  doc.loops[0].setup = pads[2].lines[0].id;
  assert.match(messages(loopProblems(doc, timeline, minutes)), /the condensation plants no loop/);
  doc.loops[0].setup = "h2cz";
  assert.match(messages(loopProblems(doc, timeline, minutes)), /sits in the outro/);
  doc.loops = doc.loops.slice(0, 2);
  assert.match(messages(loopProblems(doc, timeline, minutes)), /2 open loops planted; .* at least 3/);
});

test("a brand story and a 奇聞檔案局 episode keep the tighter cadence: a hook inside 45 s, eight loops for ten minutes", () => {
  assert.deepEqual(TIGHT_CADENCE, { gap: 45, loopsPer10: 8 });
  assert.deepEqual(DEFAULT_CADENCE, { gap: HOOK_GAP_SECONDS, loopsPer10: 3 });
  assert.deepEqual([requiredLoops(10, TIGHT_CADENCE.loopsPer10), requiredLoops(13, TIGHT_CADENCE.loopsPer10)], [8, 10]);
  // Two padded scenes to a chapter: about 66 s between turns, inside 90 s and over 45 s.
  const doc = stretched();
  padScenes(doc).forEach((scene, index) => {
    if (index % 2) delete scene.chapter;
  });
  const timeline = estimateTimeline(doc);
  assert.deepEqual(hookCadenceProblems(doc, timeline), []);
  const tight = hookCadenceProblems(doc, timeline, TIGHT_CADENCE.gap);
  assert.ok(tight.length > 0);
  assert.match(tight[0].message, /plant one at least every 45 s/);
  const minutes = timeline.total_frames / FPS / 60;
  assert.match(messages(narrativeProblems(doc, timeline, { minutes, cadence: TIGHT_CADENCE }).warnings), /plants at least 7/);

  // lint picks the cadence by the series: a curio- slug is read at 45 s, any other narrated video at 90 s.
  const warnings = (slug) => messages(lintVideo({ ...structuredClone(doc), slug }, context()).warnings);
  assert.match(warnings("curio-x01"), /plant one at least every 45 s/);
  assert.doesNotMatch(warnings("ai-term-x01"), /plant one at least every/);
});

test("a number said in three sentences is a repeat, unless a sentence brings it back on purpose", () => {
  const doc = fixture();
  const lines = doc.scenes[1].lines;
  lines[0].text = "一千七百零一桶酒精，運到了熱那亞。";
  lines[1].text = "一千七百零一桶裡，有九桶是空的。";
  assert.deepEqual(repeatedFactProblems(doc), [], "twice is telling it and then turning it");
  lines[2].text = "一千七百零一桶的清單，法庭上又念了一次。";
  const [problem] = repeatedFactProblems(doc);
  assert.match(problem.message, /「一千七百零一桶」 is said in 3 lines \(x9fe, b3tn, r8wd\)/);
  assert.match(problem.message, /a fact is told once/);
  lines[2].text = "還記得那一千七百零一桶嗎？";
  assert.deepEqual(repeatedFactProblems(doc), [], "a callback names it on purpose");
  assert.match("剛剛那個數字", CALLBACK);
  // Arabic numerals of two digits or more count the same way.
  const digits = fixture();
  ["一八七二年，1872 年的紀錄寫下來了。", "1872 年的清單又點了一次。", "1872 年的法庭又念了一次。"].forEach((text, index) => {
    digits.scenes[1].lines[index].text = text;
  });
  assert.match(messages(repeatedFactProblems(digits)), /「1872」 is said in 3 lines/);
});

test("the close never names the next video: the outro card's words, its lines and the last three sentences", () => {
  const doc = fixture();
  assert.deepEqual(outroNextVideoProblems(doc), [], "the example's close invites a subscription instead");
  for (const next of ["下一集", "下一支", "下一份檔案", "下一部", "下次我們", "下一期", "下一個故事", "下集"]) {
    assert.match(`${next}再見。`, NEXT_VIDEO, next);
  }
  assert.doesNotMatch("下一步怎麼做？", NEXT_VIDEO, "the next step is not the next video");
  const teaser = fixture();
  teaser.scenes[2].lines[1].text = "下一份檔案是五十一區，記得訂閱。";
  const [problem] = outroNextVideoProblems(teaser);
  assert.equal(problem.path, "scenes[2] (wrap).lines[1] (p5vs)");
  assert.match(problem.message, /the close names the next video \(「下一份檔案」\)/);
  assert.equal(outroNextVideoProblems(teaser).length, 1, "the same line is reported once, card and tail alike");
  const card = fixture();
  card.scenes[2].data.cta = "下一支示範第一次對話";
  assert.deepEqual(outroNextVideoProblems(card).map((each) => each.path), ["scenes[2] (wrap).data.cta"]);
});

test("the panel passes only when every required question is yes; a missing or malformed answer is a no", () => {
  assert.equal(NARRATIVE_PANEL.length, 13);
  assert.deepEqual(NARRATIVE_PANEL.filter((question) => !question.required).map((question) => question.id), ["chapters_are_events"]);
  const all = (yes) => ({ answers: NARRATIVE_PANEL.map((question) => ({ id: question.id, yes, evidence: "[k7p2] 每次有新模型出來" })) });
  const passed = panelVerdict(all(true));
  assert.equal(passed.passed, true);
  assert.deepEqual(passed.failed, []);
  assert.deepEqual(passed.problems, []);
  const failed = panelVerdict(all(false));
  assert.equal(failed.passed, false);
  assert.equal(failed.failed.length, NARRATIVE_PANEL.length - 1, "every required question");
  assert.deepEqual(failed.advisory.map((each) => each.id), ["chapters_are_events"]);
  assert.match(failed.problems[0], /^scene_first：/);
  const advisory = all(true);
  advisory.answers.find((answer) => answer.id === "chapters_are_events").yes = false;
  assert.equal(panelVerdict(advisory).passed, true, "an advisory question alone does not send the script back");
  const missing = all(true);
  missing.answers = missing.answers.filter((answer) => answer.id !== "payoffs");
  assert.deepEqual(panelVerdict(missing).failed.map((each) => each.id), ["payoffs"]);
  assert.equal(panelVerdict(missing).failed[0].evidence, "no answer");
  const loose = all(true);
  loose.answers.find((answer) => answer.id === "no_recap").yes = "true";
  assert.deepEqual(panelVerdict(loose).failed.map((each) => each.id), ["no_recap"]);
  assert.equal(panelVerdict({}).passed, false);
  assert.equal(panelVerdict(null).failed.length, NARRATIVE_PANEL.filter((question) => question.required).length);
});

test("a story's two readers: a required question fails only when both say no, and a yes counts only with a quoted line id", () => {
  assert.equal(STORY_PANEL_READERS, 2);
  const reader = (no = [], { uncited = [] } = {}) => panelVerdict({ answers: NARRATIVE_PANEL.map(({ id }) => ({
    id, yes: !no.includes(id), evidence: uncited.includes(id) ? "開場很好" : `[k7p2] ${no.includes(id) ? "這句講掉了結局" : "這句沒問題"}`,
  })) });

  // Both say no: the question fails, and the writer is told what each reader quoted.
  const both = mergePanelVerdicts([reader(["no_spoiler", "payoffs"]), reader(["no_spoiler"])]);
  assert.equal(both.passed, false);
  assert.deepEqual(both.failed.map((each) => each.id), ["no_spoiler"], "payoffs had one yes and is met");
  assert.equal(both.problems.length, 1);
  assert.match(both.problems[0], /^no_spoiler：.*讀者一：\[k7p2\] 這句講掉了結局；讀者二：\[k7p2\] 這句講掉了結局/);
  assert.equal(both.answers.find((each) => each.id === "payoffs").yes_readers, 1);

  // One no and one cited yes: met, with the yes reader's line as the evidence.
  const split = mergePanelVerdicts([reader(["no_spoiler"]), reader()]);
  assert.equal(split.passed, true);
  assert.deepEqual(split.failed, []);
  assert.equal(split.answers.find((each) => each.id === "no_spoiler").evidence, "[k7p2] 這句沒問題");

  // A yes with no line id quoted is no yes: the other reader's no stands.
  const uncited = mergePanelVerdicts([reader(["no_spoiler"]), reader([], { uncited: ["no_spoiler"] })]);
  assert.equal(uncited.passed, false);
  assert.deepEqual(uncited.failed.map((each) => each.id), ["no_spoiler"]);
  assert.match(uncited.problems[0], /讀者二：no line id quoted: 開場很好/);

  // An advisory question both readers fail is still advisory; one reader is that reader's verdict.
  assert.equal(mergePanelVerdicts([reader(["chapters_are_events"]), reader(["chapters_are_events"])]).passed, true);
  const alone = reader(["payoffs"]);
  assert.equal(mergePanelVerdicts([alone]), alone);
  assert.throws(() => mergePanelVerdicts([]), /at least one reader/);

  // The record keeps the merged answers where they were and each reader's own beside them.
  const record = narrativeRecord(fixture(), both, 3);
  assert.equal(record.passed, false);
  assert.deepEqual(record.failed, ["no_spoiler"]);
  assert.equal(record.answers.length, NARRATIVE_PANEL.length);
  assert.equal(record.readers.length, 2);
  assert.deepEqual(record.readers.map((each) => each.failed), [["no_spoiler", "payoffs"], ["no_spoiler"]]);
  assert.deepEqual(record.readers[1].answers.find((each) => each.id === "payoffs"), { id: "payoffs", yes: true, evidence: "[k7p2] 這句沒問題" });
  assert.equal(narrativeReviewMatches(record, fixture()), true, "the binding is the one a single reader's record has");
  assert.equal("readers" in narrativeRecord(fixture(), alone, 1), false, "a single reader's record is unchanged");
});

test("a narrative PASS is reusable only for the script and exact panel rules that judged it", () => {
  const doc = fixture();
  const verdict = panelVerdict({ answers: NARRATIVE_PANEL.map(({ id }) => ({
    id, yes: true, evidence: "[k7p2] 被審查的逐字稿原句",
  })) });
  const current = narrativeRecord(doc, verdict, 1);
  assert.equal(current.panel_rules_sha256, PANEL_RULES_SHA256);
  assert.match(current.panel_narration_sha256, /^[a-f0-9]{64}$/);
  assert.equal(narrativeReviewMatches(current, doc), true);

  const legacy = { ...current };
  delete legacy.panel_rules_sha256;
  assert.equal(scriptCheckMatches(legacy, doc), true, "other script checks keep their existing binding");
  assert.equal(narrativeReviewMatches(legacy, doc), false, "an old PASS without rules is stale");
  const withoutNarration = { ...current };
  delete withoutNarration.panel_narration_sha256;
  assert.equal(narrativeReviewMatches(withoutNarration, doc), false, "an old PASS without its full panel input is stale");

  const rulesHash = ({ instructions = PANEL_INSTRUCTIONS, questions = NARRATIVE_PANEL.map(({ id, question, required }) => ({ id, question, required })) } = {}) => createHash("sha256").update(JSON.stringify({
    instructions,
    questions,
    verdict_version: 1,
  })).digest("hex");
  const changedQuestion = NARRATIVE_PANEL.map(({ id, question, required }) => ({
    id, question: id === "payoffs" ? `${question} Additional requirement.` : question, required,
  }));
  const changedRequired = NARRATIVE_PANEL.map(({ id, question, required }) => ({
    id, question, required: id === "payoffs" ? !required : required,
  }));
  for (const changedRulesHash of [
    rulesHash({ questions: changedQuestion }),
    rulesHash({ questions: changedRequired }),
    rulesHash({ instructions: `${PANEL_INSTRUCTIONS}\nAdditional panel rule.` }),
  ]) {
    assert.notEqual(changedRulesHash, PANEL_RULES_SHA256);
    assert.equal(narrativeReviewMatches({ ...current, panel_rules_sha256: changedRulesHash }, doc), false);
  }
  const changedDoc = structuredClone(doc);
  changedDoc.scenes[0].lines[0].text += "又一句。";
  assert.equal(narrativeReviewMatches(current, changedDoc), false);
  const renamedVideo = structuredClone(doc);
  renamedVideo.youtube.title += "：新版片名";
  assert.equal(scriptCheckMatches(current, renamedVideo), true, "the shared script binding intentionally ignores title metadata");
  assert.equal(narrativeReviewMatches(current, renamedVideo), false, "the title appears in the panel input and must invalidate its PASS");
});

test("the panel carries a concrete protagonist or problem end to end and still rejects detours", () => {
  // 2026-10-15: three AI videos switched example and metaphor from chapter to chapter, spent a
  // third of one on a detour and read lists out; the one thread they had was what read best.
  const byId = new Map(NARRATIVE_PANEL.map((question) => [question.id, question]));
  assert.equal(byId.get("one_thread")?.required, true);
  assert.match(byId.get("one_thread").question, /一個可辨認的主角或具體難題/);
  assert.match(byId.get("one_thread").question, /從開場一路帶到結尾/);
  assert.equal(byId.get("no_detour")?.required, true);
  assert.match(byId.get("no_detour").question, /沒有岔出去的段落/);
  assert.match(byId.get("no_detour").question, /產品、分數或誰說了什麼的清單/);
  const payload = panelPayload(fixture(), estimateTimeline(fixture()));
  assert.ok(["one_thread", "no_detour"].every((id) => payload.questions.some((question) => question.id === id)), "the reader is asked both");
  for (const id of ["one_thread", "no_detour"]) {
    const verdict = panelVerdict({ answers: NARRATIVE_PANEL.map((question) => ({ id: question.id, yes: question.id !== id, evidence: "[k7p2] 每次有新模型出來" })) });
    assert.equal(verdict.passed, false, id);
    assert.deepEqual(verdict.failed.map((each) => each.id), [id]);
    assert.match(verdict.problems[0], new RegExp(`^${id}：`));
  }
});

test("panel questions distinguish an adjacent answer from a distant callback without excusing missing answers", () => {
  const byId = new Map(NARRATIVE_PANEL.map((entry) => [entry.id, entry.question]));
  const payoff = byId.get("payoffs");
  // Valid adjacent pair: 「顧客買不買帳？」→「據他回憶，顧客很快接受了。」
  // Valid distant callback: the early suitcase question returns minutes later by naming that
  // suitcase and telling what happened to it. Invalid: a question never answered, or merely
  // repeated as 「那顧客究竟買不買帳呢？」.
  assert.match(payoff, /緊鄰的問答可以直接回答，不必再用「還記得」點名/);
  assert.match(payoff, /隔了幾分鐘才回收的問題，須點名原先具體的人、物或疑問/);
  assert.match(payoff, /只重複問題、換句話說，或回答另一件事，都不算回收/);

  const link = byId.get("chapters_link");
  // Valid cold-open return: start at the earlier suitcase already previewed in the opening and
  // show why it matters to the opening question. Invalid: 「回到 1928 年」 as a chapter label,
  // or claiming that one inventor taught another when the sources establish no such link.
  assert.match(link, /預告式開場之後可以回到更早的故事起點/);
  assert.match(link, /第一句要讓觀眾聽懂它從哪裡接上開場的問題/);
  assert.match(link, /重述剛問過的話/);
  assert.match(link, /沒有來源支持卻硬說兩件事有因果/);
});

test("product-history thread must advance the same use problem, not merely share a category", () => {
  const question = NARRATIVE_PANEL.find((entry) => entry.id === "one_thread").question;
  // Valid product history: a heavy suitcase becomes movable, reaches the shelf, then changes
  // shape when dragging through a terminal proves awkward. Invalid: three suitcases introduced
  // only because they all have wheels, or an invented transfer of know-how between makers.
  assert.match(question, /跨年代的產品故事可以追同一個使用難題/);
  assert.match(question, /上一種用法留下什麼困難、下一個做法如何回應/);
  assert.match(question, /只因同屬一類商品就連續換例子，不算同一條線/);
  assert.match(question, /不能沒有來源就聲稱不同發明者彼此承襲或互相啟發/);

  // Rewording the questions does not turn a previously recorded no into a yes. The reader must
  // make a fresh judgment about the actual script using this new payload.
  const failedIds = ["chapters_link", "payoffs", "one_thread"];
  const previousNo = { answers: NARRATIVE_PANEL.map(({ id }) => ({
    id, yes: !failedIds.includes(id), evidence: "[k7p2] 被審查的逐字稿原句",
  })) };
  assert.deepEqual(panelVerdict(previousNo).failed.map(({ id }) => id), failedIds);
  assert.equal(panelVerdict(previousNo).passed, false);
});

test("a yes the reader quotes no line for is not a yes", () => {
  // The questions ask for one line of the narration quoted with its id in brackets, and every one
  // of the 240 answers the first five episodes were judged on carried one. So a yes with nothing
  // quoted is a malformed reply, and approving a script on it would leave no auditable basis at
  // all: a truncated or lazy answer would pass everything (PR #1478 review, 2026-10-13).
  const every = (entry) => ({ answers: NARRATIVE_PANEL.map((question) => ({ id: question.id, ...entry })) });
  const quoted = panelVerdict(every({ yes: true, evidence: "[mc1a] 一八七二年十二月四日下午。" }));
  assert.equal(quoted.passed, true);
  for (const [what, entry] of [
    ["no evidence key at all", { yes: true }],
    ["blank evidence", { yes: true, evidence: "   " }],
    ["evidence that is not a string", { yes: true, evidence: 7 }],
  ]) {
    const verdict = panelVerdict(every(entry));
    assert.equal(verdict.passed, false, what);
    assert.equal(verdict.failed.length, NARRATIVE_PANEL.filter((question) => question.required).length, what);
    assert.equal(verdict.failed[0].evidence, "no evidence quoted", what);
  }
  // Something was written, but it quotes no line, so the answer still cannot be audited. The
  // problem keeps the text so a person can see what the reader actually said.
  const unquoted = panelVerdict(every({ yes: true, evidence: "是，整支片都很好" }));
  assert.equal(unquoted.passed, false);
  assert.equal(unquoted.failed[0].evidence, "no line id quoted: 是，整支片都很好");
  assert.match(unquoted.problems[0], /no line id quoted/);
  // A chapter name carries no line id, so a reader quoting one quotes a line from that chapter
  // instead; ids are short and may carry a digit or a dash.
  for (const evidence of ["[a1] 一句。", "[tg7af] 一句。", "[q1-ex] 一句。", "前面說過 [ro101] 這句"]) {
    assert.equal(panelVerdict(every({ yes: true, evidence })).passed, true, evidence);
  }
  // The narration prints each line as [id start], so a reader copying a line exactly as shown
  // quotes it with its time (story-adapt-seiko-quartz-astron round 9 failed all 13 questions on
  // "[48m5 00:00] …"). Only a clock may follow the id: words in brackets still quote no line.
  for (const evidence of ["[48m5 00:00] 一句。", "[q1-ex 12:34] 一句。", "[ro101 1:02:03] 一句。"]) {
    assert.equal(panelVerdict(every({ yes: true, evidence })).passed, true, evidence);
  }
  for (const evidence of ["[是 整支片] 很好", "[a1 很好] 一句。", "[a1 12:34 很好] 一句。", "[a1 1:2] 一句。"]) {
    const verdict = panelVerdict(every({ yes: true, evidence }));
    assert.equal(verdict.passed, false, evidence);
    assert.equal(verdict.failed[0].evidence, `no line id quoted: ${evidence}`, evidence);
  }
  // A no still records what the reader quoted, so the writer knows which line to look at.
  const no = every({ yes: false, evidence: "[mc5b] 不見的，是船上唯一那艘小艇。" });
  assert.equal(panelVerdict(no).failed[0].evidence, "[mc5b] 不見的，是船上唯一那艘小艇。");
});

test("lint reads the storytelling of a narrated episode: the teaser is an error, the rest are warnings, all of them tagged", () => {
  const doc = stretched();
  doc.scenes.at(-1).lines = [
    { id: "cl01", text: "所以答案是，三個問題問完，五分鐘就能選好。" },
    { id: "cl02", text: "你每天最常叫模型做的是哪一種工作？留言告訴我。" },
    { id: "cl03", text: "下一支拆它的價格表，訂閱頻道就不會錯過。" },
  ];
  const result = lintVideo(doc, context());
  assert.equal(result.errors.length, 1);
  assert.equal(result.errors[0].kind, "narrative");
  assert.match(result.errors[0].message, /the close names the next video/);
  assert.ok(result.warnings.some((warning) => warning.kind === "narrative" && /open loops planted/.test(warning.message)));
  assert.equal(result.warnings.every((warning) => !warning.kind || warning.kind === "narrative"), true);
  // The same script as a drama with a cast keeps its own craft rules, and an example that runs
  // seconds is not read at all.
  assert.deepEqual(lintVideo(fixture(), context()).errors, []);
  assert.deepEqual(narrativeProblems(fixture(), estimateTimeline(fixture()), { minutes: 0.5 }).errors, []);
});
