import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { appendFileSync, existsSync, mkdirSync, readFileSync, rmSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { approve, readApprovals } from "../core/approvals.mjs";
import { lookHash } from "../core/drama.mjs";
import { scriptCheckBinding } from "../core/script-check.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { writeLanguages } from "../core/stages.mjs";
import { COMPILATION_STEPS, DRAMA_STEPS, SLIDES_STEPS } from "../core/state.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { COMPILATION_ITEM_IDS, ITEM_IDS } from "../qa/checks.mjs";
import { encodeWav } from "../tts/wav.mjs";
import { compilationSandbox, compileContext, EPISODE_FRAMES, EPISODES, fakeFfmpeg, writeTranslations } from "../compile/fixture.mjs";
import { audioCheck, checklistFrom, clearedSummary, downloadNote, guideSlugs, judgeBody, MAX_REVIEW_FILES, outlineOptions, PART_BYTES, previewArgs, REVIEW_GATES, sourceGuideOf, STEP_LABELS, storyboardSheets, uploadItems } from "./sync.mjs";

const TOKEN = `mkv_${"r".repeat(43)}`;
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("a brief's outline options come out with their one-line angle and spoken hook", () => {
  const brief = [
    "## 大綱",
    "",
    "### 選項 A：判斷方法框架（推薦）",
    "",
    "一行說明：照觀點解說的骨架走。",
    "",
    "開場鉤子（口語）：「你以為升級就沒有廣告了嗎？」",
    "",
    "### 選項 B：從一個情境開始",
    "一行說明：用情境貫穿全片。",
    "## 會過期的事實",
    "開場鉤子：不該被算進 B",
  ].join("\n");
  assert.deepEqual(outlineOptions(brief), [
    { key: "A", title: "判斷方法框架", summary: "照觀點解說的骨架走。", hook: "你以為升級就沒有廣告了嗎？" },
    { key: "B", title: "從一個情境開始", summary: "用情境貫穿全片。" },
  ]);
});

test("the checklist, the Jev summary and the upload items are what the page shows", () => {
  assert.deepEqual(checklistFrom([{ id: "outline approved", done: true }, { id: "on YouTube", done: false }]), [
    { key: "outline_approved", label: "站主選好大綱", done: true },
    { key: "on_youtube", label: "已上 YouTube", done: false },
  ]);
  const check = { lines: { a: { match: true, match_kind: "exact" }, b: { match: true, match_kind: "sound" }, c: { match: false, noul: 0.9 }, d: { match: false, noul: 0.1, intended: "稿子", heard: "聽到" } } };
  assert.deepEqual(audioCheck(check, { flags: ["d"] }, 5), {
    check: { lines: 5, checked: 4, exact: 1, alike: 1, judged_fine: 1, flagged: 1 },
    flagged_lines: [{ id: "d", script: "稿子", heard: "聽到", noul: 0.1 }],
  });
  assert.equal(clearedSummary(audioCheck(check, { flags: ["d"] }, 5)), "");
  // A line Jev doubted that a second transcript cleared is counted apart, with both transcripts.
  const second = { ...check.lines, e: { match: false, noul: 0.05, intended: "Veo 三點一", heard: "算便宜", second: { by: "whisper.py", heard: "Veo 3.1", match_kind: null, noul: 0.9 } } };
  const withSecond = audioCheck({ lines: second }, { flags: ["d"] }, 5);
  assert.deepEqual(withSecond.check, { lines: 5, checked: 5, exact: 1, alike: 1, judged_fine: 1, flagged: 1, cleared: 1 });
  assert.deepEqual(withSecond.cleared_lines, [{ id: "e", script: "Veo 三點一", heard: "算便宜", second: { by: "whisper.py", heard: "Veo 3.1" } }]);
  assert.equal(clearedSummary(withSecond), "；whisper.py 另外轉寫、排除 1 句（e）");
  assert.deepEqual(uploadItems("# 上架\n- [ ] **AI 使用揭露**：看情況\n- [x] 已完成\n- [ ] 縮圖看得懂"), ["AI 使用揭露：看情況", "縮圖看得懂"]);
});

/**
 * The site: it keeps what the tool sends and answers reads with the reviews it was given. The
 * judge answers as `judge()` and `policy()` say (an object, or a Response for an error); by
 * default the outline judge is off (409) and the policy judge is not there (404). Any other
 * address is a description's link the quality check opens.
 */
function site({ judge = null, policy = null } = {}) {
  const state = { calls: [], files: new Map(), reviews: [], judge: [] };
  const answer = (value) => (value instanceof Response ? value : Response.json(value));
  const fetchImpl = async (url, init = {}) => {
    if (!url.startsWith("https://mokaair.com/")) return new Response("", { status: 200 });
    const { pathname, searchParams } = new URL(url);
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
    if (pathname === "/api/video/automation/judge/outline") {
      state.judge.push(JSON.parse(init.body));
      return judge ? answer(judge()) : Response.json({ code: "video_judge_not_enabled", detail: "頻道立場還是空白，或「由 Jev 挑大綱」關著；大綱照舊等站主" }, { status: 409 });
    }
    if (pathname === "/api/video/automation/judge/policy") return policy ? answer(policy()) : Response.json({ detail: "Not Found" }, { status: 404 });
    state.calls.push({ method: init.method, pathname });
    const route = pathname.replace("/api/video/reviews/", "");
    if (init.method === "PUT" && route.includes("/files/")) {
      const hash = route.split("/files/")[1];
      const parts = state.files.get(hash) ?? [];
      parts[Number(searchParams.get("part"))] = Buffer.from(init.body);
      state.files.set(hash, parts);
      const complete = parts.filter(Boolean).length === Number(searchParams.get("parts"));
      return Response.json({ received: parts.map((_, index) => index), complete });
    }
    if (init.method === "PUT") return Response.json({ ...JSON.parse(init.body), reviews: [], pending: 0 });
    if (init.method === "POST") {
      const body = JSON.parse(init.body);
      // Match ReviewSubmit.summary's character limit so the real push path cannot hide a 422.
      if ([...body.summary].length > 500) return Response.json({ detail: "summary：內容太長" }, { status: 422 });
      state.reviews.unshift({ id: `r${state.reviews.length}`, status: "pending", choice: null, note: null, decided_at: null, ...body });
      return Response.json(state.reviews[0], { status: 201 });
    }
    return Response.json({ slug: "fixture-minimal", reviews: state.reviews });
  };
  return { state, fetchImpl };
}

function context(box, fetchImpl, extra = {}) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
      home: box.base,
      fetch: fetchImpl,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-25T06:00:00Z"),
      sleep: async () => {},
      ...extra,
    },
  };
}

test("review-push submits the outline bound to brief.md, and review-pull records only that brief's approval", async () => {
  const box = sandbox();
  const server = site();
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug], push.ctx), EXIT.ok, push.out.stderr);
  assert.deepEqual(server.state.calls.map((call) => `${call.method} ${call.pathname}`), [
    `PUT /api/video/reviews/${box.slug}`,
    `POST /api/video/reviews/${box.slug}/reviews`,
  ]);
  const [outline] = server.state.reviews;
  const brief = readFileSync(path.join(box.dir, "brief.md"));
  assert.equal(outline.gate, "outline");
  assert.equal(outline.content_sha256, sha(brief));
  assert.equal(outline.payload.brief, brief.toString("utf8"));
  assert.equal("pick" in outline.payload, false, "a brief without options is nothing for Jev: the owner chooses");
  assert.match(push.out.stdout, /the owner chooses the outline \(the brief has 0 options/);

  const waiting = context(box, server.fetchImpl);
  assert.equal(await main(["review-pull", "--slug", box.slug], waiting.ctx), EXIT.owner);
  assert.match(waiting.out.stdout, /outline: waiting for the owner/);

  Object.assign(outline, { status: "approved", choice: "A", decided_at: "2026-09-25T06:30:00Z" });
  const pulled = context(box, server.fetchImpl);
  assert.equal(await main(["review-pull", "--slug", box.slug], pulled.ctx), EXIT.ok, pulled.out.stderr);
  const [entry] = readApprovals(box.workdir).approvals;
  assert.equal(entry.gate, "outline");
  assert.equal(entry.sha256, sha(brief));
  assert.match(entry.note, /chose outline A/);

  const again = context(box, server.fetchImpl);
  await main(["review-pull", "--slug", box.slug], again.ctx);
  assert.match(again.out.stdout, /already recorded/);
  appendFileSync(path.join(box.dir, "brief.md"), "\n改過一行。\n");
  const changed = context(box, server.fetchImpl);
  await main(["review-pull", "--slug", box.slug], changed.ctx);
  assert.match(changed.out.stdout, /has since changed/);
  assert.equal(readApprovals(box.workdir).approvals.length, 1, "an approval of the old brief is not recorded for the new one");
});

const PICK = { choice: "A", probabilities: { A: 0.8 }, options: { A: { stance: 0.9, demo: 0.7 } }, advice: 0.1, passed: true, note: "Jev 挑了 A（0.80）：符合立場 0.90、有示範 0.70、建議 0.10，依設定自動核准" };
// A brief with the two outline options a judge takes; the fixture's has none.
const OPTIONS_BRIEF = "# AI 模型怎麼挑\n\n## 觀眾看完能做到的事\n\n挑出一個模型。\n\n## 站主觀點\n\n套用立場：1\n排行榜只是起點。\n\n## 大綱\n\n### 選項 A：三個問題\n一行說明：照三個問題走。\n開場鉤子：「排行榜第一名不一定最好用」\n\n### 選項 B：從一個情境開始\n一行說明：用情境貫穿。\n";

test("review-push --gate outline asks Jev first and sends the pick with the brief; a judge that is down still sends the outline, for the owner", async () => {
  const box = sandbox();
  writeFileSync(path.join(box.dir, "brief.md"), OPTIONS_BRIEF);
  const server = site({ judge: () => PICK });
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "outline"], push.ctx), EXIT.ok, push.out.stderr);
  const [asked] = server.state.judge;
  assert.deepEqual(Object.keys(asked), ["slug", "brief", "options"], "the judge's strict request model");
  assert.equal(asked.slug, box.slug);
  assert.deepEqual(asked.options.map((option) => Object.keys(option)), [["key", "title", "summary", "hook"], ["key", "title", "summary", "hook"]]);
  assert.equal(asked.options[1].hook, "", "a missing hook is sent as an empty string, never left out");
  assert.deepEqual(judgeBody("s", "b", [{ key: "A", title: "t" }]).options, [{ key: "A", title: "t", summary: "", hook: "" }]);
  const [outline] = server.state.reviews;
  assert.deepEqual(outline.payload.pick, PICK, "the whole answer travels as the pick");
  assert.equal(outline.summary, "企劃書與 2 個大綱選項；Jev 挑了 A");
  assert.match(push.out.stdout, /Jev 挑了 A（0\.80）/);

  const failed = site({ judge: () => ({ ...PICK, passed: false, note: "Jev 挑了 A（0.80）：…；沒過關" }) });
  const again = context(box, failed.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "outline"], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(failed.state.reviews[0].payload.pick.passed, false, "a pick that did not pass still goes up, so the card shows the table");
  assert.equal(failed.state.reviews[0].summary, "企劃書與 2 個大綱選項；Jev 沒有挑出過關的大綱，請站主選");

  const down = site({ judge: () => Response.json({ code: "video_judge_upstream_failed", detail: "Jev 暫時無法判斷" }, { status: 502 }) });
  const later = context(box, down.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "outline"], later.ctx), EXIT.ok, later.out.stderr);
  assert.equal("pick" in down.state.reviews[0].payload, false);
  assert.match(later.out.stdout, /Jev could not judge the outline \(Jev 暫時無法判斷\); it goes up for the owner/);

  const revoked = site({ judge: () => Response.json({ code: "video_tool_token_invalid", detail: "token revoked" }, { status: 401 }) });
  const owner = context(box, revoked.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "outline"], owner.ctx), EXIT.owner);
  assert.match(owner.out.stderr, /token revoked/);
  assert.equal(revoked.state.reviews.length, 0);
});

test("the article a video retells is its source_guide, or else the first site article it cites", () => {
  const urls = ["https://example.com/a", "https://mokaair.com/zh-TW/guides/ai-news-x-20260820?utm_source=y", "https://www.mokaair.com/en/guides/other/", "https://mokaair.com/zh-TW/hotspots/x"];
  assert.deepEqual(guideSlugs(urls), ["ai-news-x-20260820", "other"]);
  assert.equal(sourceGuideOf({ source_guide: "pack-slug", sources: [{ url: urls[1] }] }), "pack-slug");
  assert.equal(sourceGuideOf({ sources: urls.map((url) => ({ url })) }), "ai-news-x-20260820");
  assert.equal(sourceGuideOf({ sources: [{ url: urls[0] }] }), null);
  // Where the site serves articles: life under /life, the other kinds under /guides/<kind>.
  const served = ["https://mokaair.com/zh-TW/life/ai-news-gpt-6-sol-luna-20260923", "https://mokaair.com/ja/guides/howto/tokyo-subway?utm_source=youtube"];
  assert.deepEqual(guideSlugs(served), ["ai-news-gpt-6-sol-luna-20260923", "tokyo-subway"]);
  assert.equal(sourceGuideOf({ sources: [{ url: served[0] }] }), "ai-news-gpt-6-sol-luna-20260923");
});

test("review-push --report-only lists the video on the site with its article and submits nothing", async () => {
  const box = sandbox();
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  doc.sources.push({ title: "站內文章", url: "https://mokaair.com/zh-TW/guides/ai-workflow-cost-quality-latency", checked_on: "2026-09-24" });
  writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`);
  const server = site();
  let reported = null;
  const push = context(box, async (url, init) => {
    if (init.method === "PUT") reported = JSON.parse(init.body);
    return server.fetchImpl(url, init);
  });
  assert.equal(await main(["review-push", "--slug", box.slug, "--report-only"], push.ctx), EXIT.ok, push.out.stderr);
  assert.deepEqual(server.state.calls.map((call) => call.method), ["PUT"]);
  assert.equal(reported.source_guide, "ai-workflow-cost-quality-latency");
  assert.match(push.out.stdout, /nothing submitted/);
});

test("the narration goes up as an encoded copy, in parts, before its review is submitted", async () => {
  const box = sandbox();
  const server = site();
  const brief = readFileSync(path.join(box.dir, "brief.md"));
  mkdirSync(box.workdir, { recursive: true });
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "outline", file: "brief.md", sha256: sha(brief), approved_at: "2026-09-25T00:00:00Z", note: "" }] }));
  const timeline = { fps: 30, total_frames: 90, lines: [{ id: "a" }, { id: "b" }], scenes: [], chapters: [] };
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  writeFileSync(path.join(box.workdir, "narration.wav"), encodeWav(new Int16Array(SAMPLE_RATE * 3)));
  // The lines the worker's listener reworded after the retakes (docs/videos/HANDS-OFF.md §旁白).
  const rewrites = [{ id: "b", before: "這就是它的答", after: "這就是它的回答", heard: "這就是它的打" }];
  mkdirSync(path.join(box.workdir, "review"), { recursive: true });
  writeFileSync(path.join(box.workdir, "review", "rewrites.json"), JSON.stringify(rewrites));
  const encoded = Buffer.alloc(PART_BYTES + 10, 7);
  const encode = async (kind, source, target) => {
    assert.equal(kind, "narration");
    writeFileSync(target, encoded);
  };
  const push = context(box, server.fetchImpl, { encode });
  assert.equal(await main(["review-push", "--slug", box.slug], push.ctx), EXIT.ok, push.out.stderr);
  const uploads = server.state.calls.filter((call) => call.pathname.includes("/files/"));
  assert.equal(uploads.length, 2, "a file over one part goes up in two");
  const [audio] = server.state.reviews;
  assert.equal(audio.gate, "audio");
  assert.equal(audio.content_sha256, sha(readFileSync(path.join(box.workdir, "timeline.json"))));
  assert.deepEqual(audio.files, [{ role: "narration", sha256: sha(encoded), size: encoded.length, content_type: "audio/mp4" }]);
  assert.equal(Buffer.concat(server.state.files.get(sha(encoded))).equals(encoded), true);
  assert.equal(audio.payload.duration_seconds, 3);
  assert.deepEqual(audio.payload.rewrites, rewrites, "the review card lists what the listener reworded");
  assert.match(audio.summary, /Jev 標記 0 句；改寫 1 句$/);
});

/** A work directory with a narration and a cut, enough for the final gate to hash and preview. */
function cutVideo(box) {
  mkdirSync(box.workdir, { recursive: true });
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const lexicon = JSON.parse(readFileSync(path.join(box.videos, "lexicon.json"), "utf8"));
  writeSyntheticNarration(doc, lexicon, box.workdir);
  const final = Buffer.from("the finished cut");
  writeFileSync(path.join(box.workdir, "final.mp4"), final);
  return { doc, final };
}

const encode = async (kind, source, target) => writeFileSync(target, Buffer.from(`${kind} of ${path.basename(source)}`));

test("review-push --gate final runs the quality check and sends its report; a check that could not finish sends nothing", async () => {
  const box = sandbox();
  const { final } = cutVideo(box);
  const server = site();
  const push = context(box, server.fetchImpl, { encode });
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "final"], push.ctx), EXIT.ok, push.out.stderr);
  assert.match(push.out.stdout, /\[ \] policy: judge endpoint not available/, "qa ran, and printed its items");
  const [review] = server.state.reviews;
  assert.equal(review.gate, "final");
  assert.equal(review.content_sha256, sha(final));
  assert.equal(review.payload.qa.final_sha256, sha(final), "the report is of this very final.mp4");
  assert.equal(review.payload.qa.ok, false);
  assert.deepEqual(review.payload.qa.items.map((item) => item.id), ITEM_IDS);
  assert.match(review.summary, /^成片 00:\d\d，自動品管 \d+ 項沒過：assemble、render/);
  assert.deepEqual(review.files.map((file) => file.role), ["preview"]);
  assert.ok(existsSync(path.join(box.workdir, "review", "qa.json")));

  // Jev unreachable: the quality check ends with exit 4, and so does the push, without a review.
  const down = site({ policy: () => { throw new TypeError("fetch failed"); } });
  const later = context(box, down.fetchImpl, { encode });
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "final"], later.ctx), EXIT.external);
  assert.match(later.out.stderr, /the quality check could not finish/);
  assert.equal(down.state.reviews.length, 0);
});

test("review-push --gate publish attaches every file of the package with the package check and what the card shows", async () => {
  const box = sandbox();
  const { final } = cutVideo(box);
  const upload = path.join(box.workdir, "upload");
  mkdirSync(path.join(upload, "captions"), { recursive: true });
  writeFileSync(path.join(upload, "final.mp4"), final);
  writeFileSync(path.join(upload, "thumbnail.jpg"), Buffer.from([0xff, 0xd8, 0xff, 0xd9]));
  for (const locale of ["zh-TW", "en"]) {
    writeFileSync(path.join(upload, "captions", `${locale}.srt`), `1\n00:00:00,000 --> 00:00:01,000\n${locale}\n`);
    writeFileSync(path.join(upload, `description.${locale}.txt`), `${locale} title\n\n${locale} body\n`);
  }
  writeFileSync(path.join(upload, "UPLOAD.md"), "# 上傳步驟\n");
  const metadata = {
    slug: box.slug, title: "AI 模型怎麼挑", description: "本文", tags: ["AI 模型"], chapters: [{ at: "00:00", title: "開場" }, { at: "00:10", title: "三個問題" }, { at: "00:20", title: "結論" }],
    default_language: "zh-TW", localizations: { en: { title: "en title", description: "en body" } },
    final_sha256: sha(final), thumbnail: "thumbnail.jpg", captions: ["captions/en.srt", "captions/zh-TW.srt"],
    skipped_caption_locales: { ja: "no translation", ko: "no translation", "zh-CN": "no translation" },
    contains_synthetic_media: false, disclosure_reason: "slides read by a stock TTS voice",
  };
  const bytes = `${JSON.stringify(metadata, null, 2)}\n`;
  writeFileSync(path.join(upload, "metadata.json"), bytes);
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", file: "final.mp4", sha256: sha(final), approved_at: "2026-09-25T00:00:00Z", note: "" }] }));
  const server = site();
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "publish"], push.ctx), EXIT.ok, push.out.stderr);
  const [publish] = server.state.reviews;
  assert.equal(publish.gate, "publish");
  assert.equal(publish.content_sha256, sha(bytes), "bound to metadata.json");
  assert.equal(publish.summary, "上傳包 4 項齊全：請確認可以上架");
  assert.deepEqual(publish.payload.package.items.map((item) => [item.id, item.ok]), [["files", true], ["descriptions", true], ["captions", true], ["disclosure", true]]);
  assert.equal(publish.payload.package.final_sha256, sha(bytes), "the report names the file the gate hashes");
  assert.equal(publish.payload.chapters, 3);
  assert.ok(publish.payload.minutes > 0);
  assert.deepEqual(publish.payload.locales, ["zh-TW", "en"]);
  assert.deepEqual(publish.payload.zh, { title: "AI 模型怎麼挑", description: "本文", tags: ["AI 模型"] });
  assert.deepEqual(publish.payload.disclosure, { synthetic: false, reason: "slides read by a stock TTS voice" });
  assert.deepEqual(publish.payload.checklist, [], "UPLOAD.md has no self-check list any more");
  assert.deepEqual(publish.files.map((file) => [file.role, file.content_type]), [
    ["captions_en", "text/plain"],
    ["captions_zh-TW", "text/plain"],
    ["description_en", "text/plain"],
    ["description_zh-TW", "text/plain"],
    ["final", "video/mp4"],
    ["metadata", "application/json"],
    ["thumbnail", "image/jpeg"],
  ]);
  assert.equal(server.state.files.size, 7, "every file went up; UPLOAD.md did not");
  assert.equal(Buffer.concat(server.state.files.get(sha(bytes))).toString("utf8"), bytes);

  // The thumbnail gone: the check fails its files item and the summary says so; the owner decides.
  rmSync(path.join(upload, "thumbnail.jpg"));
  const broken = site();
  const again = context(box, broken.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "publish"], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(broken.state.reviews[0].summary, "上傳包 1 項沒過：files");
  assert.equal(broken.state.reviews[0].payload.package.ok, false);
});

test("without a token the push needs the owner", async () => {
  const box = sandbox();
  const out = context(box, site().fetchImpl);
  out.ctx.env = { VIDEO_WORKDIR: box.work };
  assert.equal(await main(["review-push", "--slug", box.slug], out.ctx), EXIT.owner);
  assert.match(out.out.stderr, /login/);
});

test("language reviews fit the summary limit without losing any locale, files or full skip reasons", async (t) => {
  const emptyReasonSummary = "語言：en 標題說明、CC、配音跳過（）。沒有要你上傳的配音";
  const boundaryReason = "𠮷".repeat(500 - [...emptyReasonSummary].length);
  const longReasons = Object.fromEntries(["en", "ja", "ko", "zh-CN"].map((locale) => [locale, `${locale}: ${Array.from({ length: 120 }, (_, index) => `line-${index}`).join(", ")} 無法塞入視窗𠮷`]));
  for (const [label, reasons, detailed] of [["exactly 500 Unicode characters", { en: boundaryReason }, true], ["several long locale reasons", longReasons, false]]) {
    await t.test(label, async () => {
      const box = sandbox();
      const chosen = Object.fromEntries(Object.keys(reasons).map((locale) => [locale, { metadata: true, captions: true, dub: true }]));
      writeLanguages(box.workdir, { locales: chosen, decided_at: "2026-09-29T01:00:00Z" });
      mkdirSync(path.join(box.workdir, "upload", "captions"), { recursive: true });
      for (const [locale, reason] of Object.entries(reasons)) {
        const dubDir = path.join(box.workdir, "dubs", locale);
        mkdirSync(dubDir, { recursive: true });
        writeFileSync(path.join(dubDir, "skipped.json"), JSON.stringify({ reason }));
        writeFileSync(path.join(box.workdir, "upload", `description.${locale}.txt`), `${locale} title and description`);
        writeFileSync(path.join(box.workdir, "upload", "captions", `${locale}.srt`), `1\n00:00:00,000 --> 00:00:01,000\n${locale}\n`);
      }
      const server = site();
      const push = context(box, server.fetchImpl);
      assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "languages"], push.ctx), EXIT.ok, push.out.stderr);
      assert.equal(server.state.reviews.length, 1);
      const [review] = server.state.reviews;
      assert.equal(review.gate, "languages");
      assert.ok([...review.summary].length <= 500);
      assert.equal(review.summary, `語言：${Object.entries(reasons).map(([locale, reason]) => `${locale} 標題說明、CC、配音跳過${detailed ? `（${reason}）` : ""}`).join("；")}。沒有要你上傳的配音`);
      if (detailed) assert.equal([...review.summary].length, 500, "the API counts characters, not UTF-16 code units");
      assert.deepEqual(review.payload.locales, Object.fromEntries(Object.entries(reasons).map(([locale, reason]) => [locale, { metadata: "ready", captions: "ready", dub: { status: "skipped", reason } }])));
      assert.deepEqual(review.files.map((file) => file.role), Object.keys(reasons).flatMap((locale) => [`description_${locale}`, `captions_${locale}`]));
      const manifest = readFileSync(path.join(box.workdir, "review", "languages.json"));
      assert.equal(review.content_sha256, sha(manifest));
      assert.deepEqual(JSON.parse(manifest).locales, review.payload.locales, "full diagnostic reasons remain bound to the reviewed manifest");
    });
  }
});

test("review-push distinguishes permanent request failures from service and owner failures", async (t) => {
  const cases = [
    [413, EXIT.lint, 1], [422, EXIT.lint, 1],
    [400, EXIT.external, 1],
    [401, EXIT.owner, 1], [403, EXIT.external, 1],
    [429, EXIT.external, 4], [500, EXIT.external, 4], [503, EXIT.external, 4],
    ["network", EXIT.external, 4],
  ];
  for (const [status, expected, attempts] of cases) {
    await t.test(String(status), async () => {
      const box = sandbox();
      const server = site();
      let sends = 0;
      const detail = status === 422 ? "summary：內容太長" : `review failure ${status}`;
      const fetchImpl = async (url, init) => {
        if (init.method !== "POST" || !new URL(url).pathname.endsWith("/reviews")) return server.fetchImpl(url, init);
        sends += 1;
        if (status === "network") throw new TypeError(detail);
        return Response.json({ detail }, { status });
      };
      const push = context(box, fetchImpl);
      assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "outline"], push.ctx), expected);
      assert.equal(sends, attempts);
      assert.ok(push.out.stderr.includes(detail), push.out.stderr);
      assert.equal(server.state.reviews.length, 0);
      assert.doesNotMatch(push.out.stdout, /submitted for review/);
    });
  }
});

test("invalid file uploads are isolated, while invalid project reports and reads remain service failures", async (t) => {
  for (const [phase, status, expected] of [["file", 413, EXIT.lint], ["file", 422, EXIT.lint], ["project", 422, EXIT.external], ["read", 422, EXIT.external]]) {
    await t.test(`${phase} ${status}`, async () => {
      const box = sandbox();
      writeLanguages(box.workdir, { locales: { en: { metadata: true } } });
      mkdirSync(path.join(box.workdir, "upload"), { recursive: true });
      writeFileSync(path.join(box.workdir, "upload", "description.en.txt"), "title and description");
      const server = site();
      let rejected = 0;
      const detail = `${phase} payload rejected`;
      const fetchImpl = async (url, init) => {
        const pathname = new URL(url).pathname;
        const target = phase === "read" ? init.method === "GET" : init.method === "PUT" && (phase === "file" ? pathname.includes("/files/") : pathname.endsWith(`/${box.slug}`));
        if (!target) return server.fetchImpl(url, init);
        rejected += 1;
        return Response.json({ detail }, { status });
      };
      const run = context(box, fetchImpl);
      const args = phase === "read" ? ["review-pull", "--slug", box.slug] : ["review-push", "--slug", box.slug, "--gate", "languages"];
      assert.equal(await main(args, run.ctx), expected);
      assert.equal(rejected, 1, "a malformed request is not retried inside the client");
      assert.ok(run.out.stderr.includes(detail), run.out.stderr);
      assert.equal(server.state.reviews.length, 0);
    });
  }
});

test("every pipeline step of every format has a label for the site", () => {
  for (const id of [...SLIDES_STEPS, ...DRAMA_STEPS, ...COMPILATION_STEPS]) assert.ok(STEP_LABELS[id], `no label for "${id}"`);
  assert.deepEqual(COMPILATION_STEPS.map((id) => STEP_LABELS[id]), ["合集標題與說明", "章節卡與縮圖", "合集串接", "五語標題與說明", "成片核准", "上傳包", "已上 YouTube"]);
  assert.deepEqual(REVIEW_GATES, ["outline", "script", "look", "audio", "storyboard", "final", "publish", "languages", "dubs"]);
});

const png = (text) => Buffer.concat([Buffer.from("\x89PNG\r\n\x1a\n", "binary"), Buffer.from(text)]);

/** A drama work directory with two characters' sheets, as the look stage leaves it. */
function lookManifest(box, hash) {
  const manifest = { look_hash: hash, characters: {} };
  for (const [id, name] of [["jingwei", "精衛"], ["yandi", "炎帝"]]) {
    mkdirSync(path.join(box.workdir, "characters", id), { recursive: true });
    const candidates = [1, 2].map((n) => {
      const file = `characters/${id}/00${n}.png`;
      writeFileSync(path.join(box.workdir, file), png(`${id}${n}`));
      return { n, seed: n, file, sha256: sha(png(`${id}${n}`)), key: `k${n}`, judge: { overall: 6 + n, passed: n === 2, problems: n === 1 ? ["blurry"] : [] } };
    });
    manifest.characters[id] = { name, prompt: "sheet", candidates, suggested: 2, needs_review: false };
  }
  writeFileSync(path.join(box.workdir, "characters", "manifest.json"), JSON.stringify(manifest));
  return manifest;
}

test("the look goes up as one review per character, and the owner's picks come back as the choice and the approval", async () => {
  const box = sandbox("fixture-drama", "drama");
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const manifest = lookManifest(box, lookHash(doc));
  const server = site();
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "look"], push.ctx), EXIT.ok, push.out.stderr);
  const reviews = [...server.state.reviews].reverse();
  assert.deepEqual(reviews.map((review) => [review.gate, review.subject]), [["look", "jingwei"], ["look", "yandi"]]);
  const jingwei = reviews[0];
  assert.equal(jingwei.content_sha256, sha(readFileSync(path.join(box.workdir, "characters", "manifest.json"))));
  assert.deepEqual(jingwei.files.map((file) => [file.role, file.content_type]), [["candidate_a", "image/png"], ["candidate_b", "image/png"]]);
  assert.equal(jingwei.payload.character.name, "精衛");
  assert.equal(jingwei.payload.character.voice, "gemini:Kore");
  assert.deepEqual(jingwei.payload.options.map((option) => [option.key, option.index, option.file_role, option.judge.overall]), [["A", 1, "candidate_a", 7], ["B", 2, "candidate_b", 8]]);
  assert.equal(jingwei.payload.suggested, "B");
  assert.match(jingwei.summary, /精衛 的設定圖 2 張，judge 建議 B/);
  assert.match(push.out.stdout, /look \(jingwei\) submitted/);
  assert.equal(server.state.files.size, 4, "every candidate went up");

  // One character decided: the choice is written, the gate waits for the other.
  Object.assign(reviews[0], { status: "approved", choice: "A", decided_at: "2026-09-26T09:00:00Z" });
  const half = context(box, server.fetchImpl);
  assert.equal(await main(["review-pull", "--slug", box.slug], half.ctx), EXIT.owner);
  assert.match(half.out.stdout, /look \(yandi\): waiting for the owner/);
  assert.match(half.out.stdout, /look: jingwei = A; waiting for yandi/);
  const choice = JSON.parse(readFileSync(path.join(box.workdir, "characters", "choice.json"), "utf8"));
  assert.deepEqual(choice.chosen, { jingwei: 1 });
  assert.equal(choice.look_hash, manifest.look_hash);
  assert.equal(readApprovals(box.workdir).approvals.length, 0);

  Object.assign(reviews[1], { status: "approved", choice: null, decided_at: "2026-09-26T09:05:00Z" });
  const full = context(box, server.fetchImpl);
  assert.equal(await main(["review-pull", "--slug", box.slug], full.ctx), EXIT.ok, full.out.stderr);
  assert.match(full.out.stdout, /look: approval recorded \(jingwei = A, yandi = B\)/, "approved without a pick takes the judge's suggestion");
  assert.deepEqual(JSON.parse(readFileSync(path.join(box.workdir, "characters", "choice.json"), "utf8")).chosen, { jingwei: 1, yandi: 2 });
  const [entry] = readApprovals(box.workdir).approvals;
  assert.equal(entry.gate, "look");
  assert.equal(entry.sha256, jingwei.content_sha256);
  assert.match(entry.note, /chose sheets jingwei = A, yandi = B/);
  const again = context(box, server.fetchImpl);
  await main(["review-pull", "--slug", box.slug], again.ctx);
  assert.match(again.out.stdout, /already recorded/);
});

test("the storyboard goes up with every keyframe and the judge's lowest score, and its approval is recorded", async () => {
  const box = sandbox("fixture-drama", "drama");
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  const shots = {};
  for (const [index, scene] of doc.scenes.filter((each) => each.template === "shot").entries()) {
    const file = `keyframes/${scene.id}-1.png`;
    writeFileSync(path.join(box.workdir, file), png(scene.id));
    shots[scene.id] = { file, sha256: sha(png(scene.id)), seed: 1, judge: { overall: 9 - index, passed: index < 3, problems: index < 3 ? [] : ["no bird"] }, needs_review: index === 3 };
  }
  writeFileSync(path.join(box.workdir, "keyframes", "contact-sheet.png"), png("sheet"));
  writeFileSync(path.join(box.workdir, "keyframes", "manifest.json"), JSON.stringify({ look_hash: "l", visual_hash: "v", shots, duplicates: [{ a: "opening", b: "farewell", distance: 3 }] }));
  const server = site();
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "storyboard"], push.ctx), EXIT.ok, push.out.stderr);
  const [board] = server.state.reviews;
  assert.equal(board.gate, "storyboard");
  assert.equal(board.subject, undefined);
  assert.deepEqual(board.files.map((file) => file.role), ["shot_01", "shot_02", "shot_03", "shot_04", "contact_sheet"]);
  assert.deepEqual(board.payload.shots.map((shot) => [shot.id, shot.chapter, shot.file_role, shot.needs_review]), [["opening", "發鳩山", "shot_01", false], ["farewell", null, "shot_02", false], ["sea-storm", "東海", "shot_03", false], ["bird", null, "shot_04", true]]);
  assert.deepEqual(board.payload.judge, { overall: 6, problems: ["no bird"] });
  assert.deepEqual(board.payload.duplicates, [{ a: "opening", b: "farewell", distance: 3 }]);
  assert.match(board.summary, /分鏡 4 鏡，judge 最低 6\/10，1 鏡待修/);

  Object.assign(board, { status: "approved", decided_at: "2026-09-26T10:00:00Z", note: "第四鏡再改" });
  const pull = context(box, server.fetchImpl);
  assert.equal(await main(["review-pull", "--slug", box.slug], pull.ctx), EXIT.ok, pull.out.stderr);
  assert.match(pull.out.stdout, /storyboard: approval recorded/);
  const [entry] = readApprovals(box.workdir).approvals;
  assert.equal(entry.gate, "storyboard");
  assert.equal(entry.sha256, board.content_sha256);
});

/**
 * The drama fixture stretched to `count` shots (s1, s2, …), drawn as the keyframes stage leaves
 * them: the shot numbers in `waiting` are left for a prompt fix; `pages` lists the contact sheet
 * as pages of 24 shots in contact_sheets, otherwise one keyframes/contact-sheet.png holds them all.
 */
function longStoryboard(box, count, { waiting = [], pages = false } = {}) {
  const file = path.join(box.dir, "video.json");
  const doc = JSON.parse(readFileSync(file, "utf8"));
  const [first] = doc.scenes;
  doc.scenes = Array.from({ length: count }, (_, index) => ({ ...first, id: `s${index + 1}`, chapter: index % 24 ? undefined : `第 ${index / 24 + 1} 段`, data: { ...first.data, prompt: `shot ${index + 1}` }, lines: [{ id: `l${index + 1}`, text: "一句旁白。" }] }));
  writeFileSync(file, `${JSON.stringify(doc, null, 2)}\n`);
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  const ids = doc.scenes.map((scene) => scene.id);
  const shots = {};
  for (const [index, id] of ids.entries()) {
    const fix = waiting.includes(index + 1);
    writeFileSync(path.join(box.workdir, "keyframes", `${id}-1.png`), png(id));
    shots[id] = { file: `keyframes/${id}-1.png`, sha256: sha(png(id)), seed: 1, judge: { overall: fix ? 5 : 8, passed: !fix, problems: fix ? ["no bird"] : [] }, needs_review: fix };
  }
  const manifest = { look_hash: "l", visual_hash: "v", shots, duplicates: [] };
  if (pages) {
    manifest.contact_sheets = [];
    for (let start = 0; start < count; start += 24) {
      const sheet = `keyframes/contact-sheet-${String(start / 24 + 1).padStart(2, "0")}.png`;
      writeFileSync(path.join(box.workdir, sheet), png(sheet));
      manifest.contact_sheets.push({ file: sheet, shots: ids.slice(start, start + 24) });
    }
    manifest.contact_sheet = manifest.contact_sheets[0].file;
  } else {
    writeFileSync(path.join(box.workdir, "keyframes", "contact-sheet.png"), png("sheet"));
    manifest.contact_sheet = "keyframes/contact-sheet.png";
  }
  const bytes = JSON.stringify(manifest);
  writeFileSync(path.join(box.workdir, "keyframes", "manifest.json"), bytes);
  return { ids, bytes };
}

test("illustrated slides push their storyboard too, and it is the gate after the narration (docs/videos/ILLUSTRATED.md)", async () => {
  const box = sandbox("fixture-illustrated", "illustrated");
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  const shots = {};
  for (const scene of doc.scenes.filter((each) => each.template === "shot")) {
    const file = `keyframes/${scene.id}-1.png`;
    writeFileSync(path.join(box.workdir, file), png(scene.id));
    shots[scene.id] = { file, sha256: sha(png(scene.id)), seed: 1, judge: { overall: 8, passed: true, problems: [] }, needs_review: false };
  }
  writeFileSync(path.join(box.workdir, "keyframes", "manifest.json"), JSON.stringify({ look_hash: "l", pictures_hash: "p", shots }));
  // The outline and the narration approved, the storyboard is what review-push picks next.
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir, note: "t" });
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify({ speech_hash: "s", lines: [], scenes: [], total_frames: 0 }));
  await approve({ gate: "audio", docDir: box.dir, workdir: box.workdir, note: "t" });
  const server = site();
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug], push.ctx), EXIT.ok, push.out.stderr);
  const [board] = server.state.reviews;
  assert.equal(board.gate, "storyboard");
  assert.equal(board.payload.shots.length, Object.keys(shots).length);
  assert.deepEqual(board.payload.shots.map((shot) => shot.id), Object.keys(shots));
  assert.match(board.summary, /分鏡 5 鏡，judge 最低 8\/10/);
});

/** review-push --gate storyboard against a fresh site: the review it received and the files it holds. */
async function pushStoryboard(box) {
  const server = site();
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "storyboard"], push.ctx), EXIT.ok, push.out.stderr);
  return { review: server.state.reviews[0], stored: server.state.files };
}

const shotRole = (n) => `shot_${String(n).padStart(2, "0")}`;

test("47 shots still fit a review: every keyframe, then the contact sheet, with the payload and summary as before", async () => {
  const box = sandbox("fixture-drama", "drama");
  const { ids } = longStoryboard(box, 47, { waiting: [5] });
  const { review, stored } = await pushStoryboard(box);
  assert.deepEqual(review.files.map((file) => file.role), [...ids.map((_, index) => shotRole(index + 1)), "contact_sheet"]);
  assert.equal(review.files.at(-1).content_type, "image/png");
  assert.equal(stored.size, MAX_REVIEW_FILES);
  assert.deepEqual(Object.keys(review.payload), ["shots", "judge", "duplicates"], "no sheets and no omitted count");
  assert.deepEqual(review.payload.shots.map((shot) => shot.file_role), ids.map((_, index) => shotRole(index + 1)));
  assert.deepEqual(review.payload.shots[4], { id: "s5", chapter: null, prompt: "shot 5", seconds: null, file_role: "shot_05", needs_review: true, judge: { overall: 5, problems: ["no bird"] } });
  assert.deepEqual(review.payload.judge, { overall: 5, problems: ["no bird"] });
  assert.equal(review.summary, "分鏡 47 鏡，judge 最低 5/10，1 鏡待修");
});

test("48 shots and the sheet are one file too many: the contact sheet goes up with the shots left for a fix", async () => {
  const box = sandbox("fixture-drama", "drama");
  const { ids } = longStoryboard(box, 48, { waiting: [48] });
  const { review } = await pushStoryboard(box);
  assert.deepEqual(review.files.map((file) => file.role), ["contact_sheet", "shot_48"]);
  assert.equal(review.payload.shots.length, 48);
  assert.deepEqual(review.payload.shots.filter((shot) => shot.file_role).map((shot) => shot.id), ["s48"]);
  assert.deepEqual(review.payload.sheets, [{ role: "contact_sheet", shots: ids }]);
  assert.equal(review.payload.omitted, 47);
  assert.equal(review.summary, "分鏡 48 鏡（聯絡表 1 頁），judge 最低 5/10，1 鏡待修");
});

test("a brand story's 95 shots go up as four contact sheet pages and the three shots left for a fix; the payload still lists every shot", async () => {
  const box = sandbox("fixture-drama", "drama");
  const { ids, bytes } = longStoryboard(box, 95, { waiting: [7, 50, 95], pages: true });
  const { review } = await pushStoryboard(box);
  assert.equal(review.content_sha256, sha(bytes), "bound to keyframes/manifest.json as before");
  assert.deepEqual(review.files.map((file) => [file.role, file.content_type]), [
    ["contact_sheet_01", "image/png"],
    ["contact_sheet_02", "image/png"],
    ["contact_sheet_03", "image/png"],
    ["contact_sheet_04", "image/png"],
    ["shot_07", "image/png"],
    ["shot_50", "image/png"],
    ["shot_95", "image/png"],
  ]);
  assert.deepEqual(review.payload.shots.map((shot) => shot.id), ids);
  assert.deepEqual(review.payload.shots.filter((shot) => shot.file_role).map((shot) => [shot.id, shot.file_role]), [["s7", "shot_07"], ["s50", "shot_50"], ["s95", "shot_95"]]);
  assert.deepEqual(review.payload.shots[24], { id: "s25", chapter: "第 2 段", prompt: "shot 25", seconds: null, file_role: null, needs_review: false, judge: { overall: 8, problems: [] } });
  assert.deepEqual(review.payload.sheets.map((sheet) => [sheet.role, sheet.shots.length, sheet.shots[0]]), [["contact_sheet_01", 24, "s1"], ["contact_sheet_02", 24, "s25"], ["contact_sheet_03", 24, "s49"], ["contact_sheet_04", 23, "s73"]]);
  assert.equal(review.payload.omitted, 92);
  assert.deepEqual(review.payload.judge, { overall: 5, problems: ["no bird"] });
  assert.equal(review.summary, "分鏡 95 鏡（聯絡表 4 頁），judge 最低 5/10，3 鏡待修");
});

test("95 shots drawn on one contact sheet go up as that sheet and the shots left for a fix", async () => {
  const box = sandbox("fixture-drama", "drama");
  const { ids } = longStoryboard(box, 95, { waiting: [7, 50, 95] });
  const { review } = await pushStoryboard(box);
  assert.deepEqual(review.files.map((file) => file.role), ["contact_sheet", "shot_07", "shot_50", "shot_95"]);
  assert.equal(review.payload.shots.length, 95);
  assert.deepEqual(review.payload.sheets, [{ role: "contact_sheet", shots: ids }]);
  assert.equal(review.payload.omitted, 92);
  assert.equal(review.summary, "分鏡 95 鏡（聯絡表 1 頁），judge 最低 5/10，3 鏡待修");
});

test("120 shots with 60 left for a fix never send more files than a review takes, and the summary counts the fixes without a picture", async () => {
  const waiting = Array.from({ length: 60 }, (_, index) => index * 2 + 1);
  for (const [pages, sheets] of [[true, 5], [false, 1]]) {
    const box = sandbox("fixture-drama", "drama");
    longStoryboard(box, 120, { waiting, pages });
    const { review } = await pushStoryboard(box);
    const sent = MAX_REVIEW_FILES - sheets;
    assert.equal(review.files.length, MAX_REVIEW_FILES);
    assert.deepEqual(review.files.slice(sheets).map((file) => file.role), waiting.slice(0, sent).map(shotRole), "the first shots left for a fix, in shot order");
    assert.equal(review.payload.shots.length, 120);
    assert.equal(review.payload.omitted, 120 - sent);
    assert.equal(review.summary, `分鏡 120 鏡（聯絡表 ${sheets} 頁），judge 最低 5/10，60 鏡待修，其中 ${60 - sent} 鏡沒附單張圖`);
  }
});

test("a storyboard that fits sends every keyframe with its pages: one page reads as the contact sheet, two are named and listed", async () => {
  const one = sandbox("fixture-drama", "drama");
  longStoryboard(one, 20, { pages: true });
  const { review: short } = await pushStoryboard(one);
  assert.equal(short.files.at(-1).role, "contact_sheet");
  assert.deepEqual(Object.keys(short.payload), ["shots", "judge", "duplicates"]);
  assert.equal(short.summary, "分鏡 20 鏡，judge 最低 8/10");

  const two = sandbox("fixture-drama", "drama");
  const { ids } = longStoryboard(two, 30, { pages: true });
  const { review: long } = await pushStoryboard(two);
  assert.deepEqual(long.files.map((file) => file.role), [...ids.map((_, index) => shotRole(index + 1)), "contact_sheet_01", "contact_sheet_02"]);
  assert.deepEqual(long.payload.sheets, [{ role: "contact_sheet_01", shots: ids.slice(0, 24) }, { role: "contact_sheet_02", shots: ids.slice(24) }]);
  assert.equal(long.payload.omitted, 0);
  assert.equal(long.summary, "分鏡 30 鏡（聯絡表 2 頁），judge 最低 8/10");
});

test("pages listed as bare files hold 24 shots each, and a page whose file is gone is left out", () => {
  const box = sandbox("fixture-drama", "drama");
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  for (const name of ["a.png", "c.png"]) writeFileSync(path.join(box.workdir, "keyframes", name), png(name));
  const ids = Array.from({ length: 50 }, (_, index) => `s${index + 1}`);
  const sheets = storyboardSheets({ contact_sheets: ["keyframes/a.png", "keyframes/b.png", { file: "keyframes/c.png" }] }, ids, box.workdir);
  assert.deepEqual(sheets.map((sheet) => [sheet.file, sheet.shots.length, sheet.shots[0]]), [["keyframes/a.png", 24, "s1"], ["keyframes/c.png", 2, "s49"]]);
  assert.deepEqual(storyboardSheets({ shots: {} }, ids, box.workdir), [], "no pages listed and no sheet drawn");
});

test("the 720p preview of a compilation caps its bitrate; a cut's and the narration's arguments are unchanged", () => {
  const cut = previewArgs("preview", "final.mp4", "review/p.mp4");
  assert.equal(cut.join(" "), "-hide_banner -y -loglevel error -i final.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -preset veryfast -crf 26 -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart review/p.mp4");
  const long = previewArgs("preview", "final.mp4", "review/p.mp4", { compilation: true });
  assert.equal(long.join(" "), "-hide_banner -y -loglevel error -i final.mp4 -vf scale=1280:720:flags=lanczos -c:v libx264 -preset veryfast -crf 26 -maxrate 2M -bufsize 4M -pix_fmt yuv420p -c:a aac -b:a 128k -movflags +faststart review/p.mp4");
  assert.equal(previewArgs("narration", "n.wav", "n.m4a").join(" "), "-hide_banner -y -loglevel error -i n.wav -c:a aac -b:a 96k -ac 1 -movflags +faststart n.m4a");
  assert.equal(downloadNote(2.5 * 1024 ** 3), "合集 2.50 GB，成片從網站下載後上傳");
});

test("the script gate sends the checker's similar works and retention verdict when the worker wrote them", async () => {
  const box = sandbox("fixture-drama", "drama");
  mkdirSync(path.join(box.workdir, "review"), { recursive: true });
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  writeFileSync(path.join(box.workdir, "review", "script-check.json"), JSON.stringify({ ...scriptCheckBinding(doc), coverage: { hook: "yes" }, problems: ["a name changed"], similar_works: [{ title: "魔道祖師", how: "a sect rivalry" }], retention: { score: 0.8, passed: true } }));
  const server = site();
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "script"], push.ctx), EXIT.ok, push.out.stderr);
  const [script] = server.state.reviews;
  assert.equal(script.gate, "script");
  assert.deepEqual(script.payload.similar_works, [{ title: "魔道祖師", how: "a sect rivalry" }]);
  assert.deepEqual(script.payload.retention, { score: 0.8, passed: true });
  assert.deepEqual(script.payload.continuity_problems, ["a name changed"]);
  assert.equal(script.payload.check_status, "current");
  doc.scenes[0].lines[0].text += "新的情節。";
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const changed = site();
  const stalePush = context(box, changed.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "script"], stalePush.ctx), EXIT.ok, stalePush.out.stderr);
  const stale = changed.state.reviews[0].payload;
  assert.equal(stale.check_status, "stale");
  assert.equal(stale.coverage, null);
  assert.equal(stale.retention, null);
  assert.deepEqual(stale.similar_works, []);
  assert.match(stale.continuity_problems[0], /舊查核報告不適用/);
  rmSync(path.join(box.workdir, "review", "script-check.json"));
  const bare = site();
  const again = context(box, bare.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "script"], again.ctx), EXIT.ok, again.out.stderr);
  assert.deepEqual(bare.state.reviews[0].payload.similar_works, []);
  assert.equal(bare.state.reviews[0].payload.retention, null);
});

const COMPILATION_FRAMES = EPISODES.reduce((sum, slug) => sum + EPISODE_FRAMES[slug], 0) + EPISODES.length * 60 + 120;

test("a compilation reports its series, goes up for the final gate with the six-item check and a capped preview, and its package keeps final.mp4 home", async () => {
  const box = compilationSandbox({ captions: Object.fromEntries(EPISODES.map((slug) => [slug, ["zh-TW", "en", "ja", "ko", "zh-CN"]])) });
  writeTranslations(box, box.doc);
  const compiled = compileContext(box, fakeFfmpeg({ total: COMPILATION_FRAMES }));
  assert.equal(await main(["compile", "--slug", box.slug], compiled.ctx), EXIT.ok, compiled.out.stderr);
  const server = site();
  let reported = null;
  const encodes = [];
  const encodeCompilation = async (kind, source, target, env, options) => {
    encodes.push({ kind, options });
    writeFileSync(target, Buffer.from(`${kind} of ${path.basename(source)}`));
  };
  const push = context(box, async (url, init) => {
    if (init.method === "PUT" && !url.includes("/files/")) reported = JSON.parse(init.body);
    return server.fetchImpl(url, init);
  }, { encode: encodeCompilation });
  assert.equal(await main(["review-push", "--slug", box.slug], push.ctx), EXIT.ok, push.out.stderr + push.out.stdout);
  assert.equal(reported.series_slug, "wuxia");
  assert.equal("episode_number" in reported, false);
  assert.equal(reported.stage, "final video approved");
  assert.ok(reported.checklist.some((item) => item.key === "video_compiled" && item.done && item.label === "合集串接"));
  const [review] = server.state.reviews;
  assert.equal(review.gate, "final", "the first gate a compilation waits at");
  assert.equal(review.content_sha256, sha(readFileSync(path.join(box.workdir, "final.mp4"))));
  assert.equal(review.payload.qa.kind, "compilation");
  assert.equal(review.payload.qa.ok, true);
  assert.deepEqual(review.payload.qa.items.map((item) => item.id), COMPILATION_ITEM_IDS);
  assert.deepEqual(review.payload.compilation, { series: "wuxia", episodes: EPISODES, total_frames: COMPILATION_FRAMES });
  assert.equal(review.payload.chapters.length, 3);
  assert.match(review.summary, /^成片 07:31，自動品管 6 項全過$/);
  assert.deepEqual(encodes, [{ kind: "preview", options: { compilation: true } }]);
  assert.deepEqual(review.files.map((file) => file.role), ["preview", "contact_sheet", "thumbnail"].filter((role) => role !== "contact_sheet" || existsSync(path.join(box.workdir, "contact-sheet.png"))));

  // Approved on the site: recorded, then the package and its publish review without the cut.
  Object.assign(review, { status: "approved", decided_at: "2026-09-27T07:00:00Z" });
  const pull = context(box, server.fetchImpl);
  assert.equal(await main(["review-pull", "--slug", box.slug], pull.ctx), EXIT.ok, pull.out.stderr);
  const packaged = compileContext(box, fakeFfmpeg({ total: COMPILATION_FRAMES }));
  assert.equal(await main(["package", "--slug", box.slug], packaged.ctx), EXIT.ok, packaged.out.stderr + packaged.out.stdout);
  const publish = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug], publish.ctx), EXIT.ok, publish.out.stderr);
  const [confirm] = server.state.reviews;
  assert.equal(confirm.gate, "publish");
  assert.equal(confirm.payload.package.ok, true);
  const bytes = statSync(path.join(box.workdir, "upload", "final.mp4")).size;
  assert.deepEqual(confirm.payload.download, { path: "upload/final.mp4", bytes, sha256: sha(readFileSync(path.join(box.workdir, "final.mp4"))) });
  assert.deepEqual(confirm.payload.episodes, EPISODES);
  assert.equal(confirm.summary, `上傳包 4 項齊全：合集 ${(bytes / 1024 ** 3).toFixed(2)} GB，成片從網站下載後上傳；請確認可以上架`);
  const roles = confirm.files.map((file) => file.role);
  assert.equal(roles.includes("final"), false, "the cut is downloaded from the site, not stored twice");
  assert.ok(roles.includes("metadata") && roles.includes("thumbnail") && roles.includes("captions_zh-TW") && roles.includes("description_en"));
  assert.equal(server.state.files.has(sha(readFileSync(path.join(box.workdir, "final.mp4")))), false);
});
