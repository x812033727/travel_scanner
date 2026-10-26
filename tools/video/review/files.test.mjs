import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdtempSync, readFileSync, rmSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { main } from "../cli.mjs";
import { liveFiles } from "./files.mjs";

const TOKEN = `mkv_${"a".repeat(43)}`;
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const FINAL = Buffer.from("the approved final cut");
const CAPTIONS = Buffer.from("1\n00:00:00,000 --> 00:00:01,000\n第一句\n");
const OLD = Buffer.from("a superseded cut");
const entry = (role, bytes, content_type) => ({ role, sha256: sha(bytes), size: bytes.length, content_type });
const project = {
  slug: "video-one",
  reviews: [
    { id: "r3", gate: "final", status: "approved", created_at: "2026-10-20T00:00:00Z", files: [entry("final", FINAL, "video/mp4"), entry("captions_zh-TW", CAPTIONS, "application/x-subrip")] },
    { id: "r2", gate: "final", status: "superseded", created_at: "2026-10-19T00:00:00Z", files: [entry("final", OLD, "video/mp4")] },
    { id: "r1", gate: "final", status: "approved", created_at: "2026-10-18T00:00:00Z", files: [entry("final", OLD, "video/mp4")] },
  ],
};

function harness(t, { bodies = { [sha(FINAL)]: FINAL, [sha(CAPTIONS)]: CAPTIONS }, listing = project, status = {} } = {}) {
  const base = mkdtempSync(path.join(os.tmpdir(), "review-files-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const calls = [];
  const out = [], err = [];
  const ctx = {
    env: { MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: "https://mokaair.test" },
    home: base,
    sleep: async () => {},
    stdout: { write: (s) => out.push(s) },
    stderr: { write: (s) => err.push(s) },
    fetch: async (url, init) => {
      calls.push({ url, headers: init.headers });
      const hash = url.split("/files/")[1];
      if (!hash) return Response.json(listing);
      if (status[hash]) return Response.json({ code: "video_review_file_not_found", detail: "gone" }, { status: status[hash] });
      return new Response(bodies[hash], { headers: { "content-type": "application/octet-stream" } });
    },
  };
  return { base, out: path.join(base, "out"), ctx, calls, stdout: out, stderr: err };
}

test("only pending and approved reviews count, newest first, one file per gate and role", () => {
  const files = liveFiles(project);
  assert.deepEqual(files.map((f) => [f.file, f.review_id]), [["final/final.mp4", "r3"], ["final/captions_zh-TW.srt", "r3"]]);
});

test("a live renewal's retained reviews come back under retained/, other superseded ones do not", () => {
  const renewed = {
    reviews: [
      { id: "n1", gate: "final", status: "pending", created_at: "2026-10-26T07:17:00Z", payload: { _final_renewal: { retained_review_ids: ["r3", "r9"] } }, files: [entry("final", Buffer.from("new cut"), "video/mp4")] },
      { id: "r9", gate: "languages", status: "superseded", created_at: "2026-10-25T14:00:00Z", files: [entry("dub_en", Buffer.from("dub"), "audio/mp4")] },
      ...project.reviews.map((review) => ({ ...review, status: review.id === "r3" ? "superseded" : review.status })),
    ],
  };
  assert.deepEqual(liveFiles(renewed).map((f) => [f.file, f.review_id]), [
    ["final/final.mp4", "n1"],
    ["retained/languages/dub_en.m4a", "r9"],
    ["retained/final/final.mp4", "r3"],
    ["retained/final/captions_zh-TW.srt", "r3"],
  ]);
  renewed.reviews[0].status = "rejected";
  assert.deepEqual(liveFiles(renewed).map((f) => f.review_id), ["r1"]);
});

test("review-files fetches each live file with the token, checks its hash and writes a manifest", async (t) => {
  const h = harness(t);
  assert.equal(await main(["review-files", "--slug", "video-one", "--out", h.out], h.ctx), 0);
  assert.deepEqual(readFileSync(path.join(h.out, "final", "final.mp4")), FINAL);
  assert.deepEqual(readFileSync(path.join(h.out, "final", "captions_zh-TW.srt")), CAPTIONS);
  assert.equal(h.calls[0].url, "https://mokaair.test/api/video/reviews/video-one");
  assert.ok(h.calls.every((call) => call.headers.Authorization === `Bearer ${TOKEN}`));
  assert.ok(!h.calls.some((call) => call.url.endsWith(sha(OLD))), "a superseded or older file is never asked for");
  const manifest = JSON.parse(readFileSync(path.join(h.out, "review-files.json"), "utf8"));
  assert.deepEqual(manifest.files.map((f) => f.sha256), [sha(FINAL), sha(CAPTIONS)]);

  // A second run keeps what is already here and asks only for the listing.
  const again = harness(t);
  again.ctx.home = h.base;
  assert.equal(await main(["review-files", "--slug", "video-one", "--out", h.out], again.ctx), 0);
  assert.equal(again.calls.length, 1);
});

test("a file whose bytes do not match the review is not kept, and the run says so", async (t) => {
  const h = harness(t, { bodies: { [sha(FINAL)]: Buffer.from("something else"), [sha(CAPTIONS)]: CAPTIONS } });
  assert.equal(await main(["review-files", "--slug", "video-one", "--out", h.out], h.ctx), 4);
  assert.equal(existsSync(path.join(h.out, "final", "final.mp4")), false);
  assert.equal(existsSync(path.join(h.out, "final", "final.mp4.part")), false);
  assert.ok(h.stderr.join("").includes("not fetched: final/final.mp4"));
  assert.deepEqual(readFileSync(path.join(h.out, "final", "captions_zh-TW.srt")), CAPTIONS);
});

test("a refused file, a dry run, no token and no live review each end plainly", async (t) => {
  const refused = harness(t, { status: { [sha(CAPTIONS)]: 404 } });
  assert.equal(await main(["review-files", "--slug", "video-one", "--out", refused.out], refused.ctx), 4);
  assert.ok(refused.stderr.join("").includes("captions_zh-TW.srt: gone"));

  const dry = harness(t);
  assert.equal(await main(["review-files", "--slug", "video-one", "--dry-run"], dry.ctx), 0);
  assert.equal(dry.calls.length, 1);
  assert.match(dry.stdout.join(""), /final\/final\.mp4 {2}approved/);

  const tokenless = harness(t);
  tokenless.ctx.env = { MOKAAIR_SITE: "https://mokaair.test" };
  assert.equal(await main(["review-files", "--slug", "video-one", "--out", tokenless.out], tokenless.ctx), 3);
  assert.equal(tokenless.calls.length, 0);

  const empty = harness(t, { listing: { slug: "video-one", reviews: [project.reviews[1]] } });
  assert.equal(await main(["review-files", "--slug", "video-one", "--out", empty.out], empty.ctx), 5);

  const usage = harness(t);
  assert.equal(await main(["review-files", "--slug", "video-one"], usage.ctx), 2);
});
