import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { appendFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { readApprovals } from "../core/approvals.mjs";
import { lookHash } from "../core/drama.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { DRAMA_STEPS, SLIDES_STEPS } from "../core/state.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { encodeWav } from "../tts/wav.mjs";
import { audioCheck, checklistFrom, guideSlugs, outlineOptions, PART_BYTES, REVIEW_GATES, sourceGuideOf, STEP_LABELS, uploadItems } from "./sync.mjs";

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
  assert.deepEqual(uploadItems("# 上架\n- [ ] **AI 使用揭露**：看情況\n- [x] 已完成\n- [ ] 縮圖看得懂"), ["AI 使用揭露：看情況", "縮圖看得懂"]);
});

/** The site: it keeps what the tool sends and answers reads with the reviews it was given. */
function site() {
  const state = { calls: [], files: new Map(), reviews: [] };
  const fetchImpl = async (url, init = {}) => {
    const { pathname, searchParams } = new URL(url);
    state.calls.push({ method: init.method, pathname });
    assert.equal(new Headers(init.headers).get("authorization"), `Bearer ${TOKEN}`);
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

test("the article a video retells is its source_guide, or else the first site article it cites", () => {
  const urls = ["https://example.com/a", "https://mokaair.com/zh-TW/guides/ai-news-x-20260820?utm_source=y", "https://www.mokaair.com/en/guides/other/", "https://mokaair.com/zh-TW/hotspots/x"];
  assert.deepEqual(guideSlugs(urls), ["ai-news-x-20260820", "other"]);
  assert.equal(sourceGuideOf({ source_guide: "pack-slug", sources: [{ url: urls[1] }] }), "pack-slug");
  assert.equal(sourceGuideOf({ sources: urls.map((url) => ({ url })) }), "ai-news-x-20260820");
  assert.equal(sourceGuideOf({ sources: [{ url: urls[0] }] }), null);
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
});

test("without a token the push needs the owner", async () => {
  const box = sandbox();
  const out = context(box, site().fetchImpl);
  out.ctx.env = { VIDEO_WORKDIR: box.work };
  assert.equal(await main(["review-push", "--slug", box.slug], out.ctx), EXIT.owner);
  assert.match(out.out.stderr, /login/);
});

test("every pipeline step of both formats has a label for the site", () => {
  for (const id of [...SLIDES_STEPS, ...DRAMA_STEPS]) assert.ok(STEP_LABELS[id], `no label for "${id}"`);
  assert.deepEqual(REVIEW_GATES, ["outline", "look", "audio", "storyboard", "final", "publish"]);
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
