import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { appendFileSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { readApprovals } from "../core/approvals.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { SAMPLE_RATE } from "../core/timeline.mjs";
import { encodeWav } from "../tts/wav.mjs";
import { audioCheck, checklistFrom, outlineOptions, PART_BYTES, uploadItems } from "./sync.mjs";

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
