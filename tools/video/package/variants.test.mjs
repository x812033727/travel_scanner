// Thumbnail variants B and C (YouTube Studio's 「測試與比較」) in the upload package, its check,
// and the final and publish reviews (ticket 2026-09-28-thumbnail-variants-in-the-upload-package).
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { writeSyntheticNarration } from "../assemble/synthetic.mjs";
import { EXIT, main } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { ITEM_IDS } from "../qa/checks.mjs";
import { checkPackage, packageFiles, THUMBNAIL_MAX_BYTES, thumbnailVariants, variantRole } from "./check.mjs";
import { thumbnailStep, uploadChecklist } from "./metadata.mjs";

const TOKEN = `mkv_${"v".repeat(43)}`;
const NOW = new Date("2026-10-01T00:00:00Z");
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");

/** The minimal fixture cut, checked, captioned and approved; with `variants`, render drew B and C. */
async function finishedVideo({ variants = false } = {}) {
  const box = sandbox();
  mkdirSync(box.workdir, { recursive: true });
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  const lexicon = JSON.parse(readFileSync(path.join(box.videos, "lexicon.json"), "utf8"));
  const timeline = writeSyntheticNarration(doc, lexicon, box.workdir);
  const final = Buffer.from("the finished cut");
  writeFileSync(path.join(box.workdir, "final.mp4"), final);
  writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify({ ok: true, speech_hash: speechHash(doc, lexicon), narration_sha256: timeline.audio_evidence.narration_sha256, visual_hash: visualHash(doc), problems: [] }));
  writeFileSync(path.join(box.workdir, "thumbnail.jpg"), Buffer.from("thumbnail A"));
  // Captions already cut for this narration, so package does not cut (and lint) them itself.
  mkdirSync(path.join(box.workdir, "captions"), { recursive: true });
  writeFileSync(path.join(box.workdir, "captions", "zh-TW.srt"), "1\n00:00:00,000 --> 00:00:01,000\nzh\n");
  writeFileSync(path.join(box.workdir, "captions", "manifest.json"), JSON.stringify({ speech_hash: speechHash(doc, lexicon), locales: { "zh-TW": { file: "captions/zh-TW.srt" } }, skipped: {} }));
  mkdirSync(path.join(box.workdir, "frames"), { recursive: true });
  const manifest = { visual_hash: visualHash(doc), thumbnail: "thumbnail.jpg" };
  if (variants) {
    writeFileSync(path.join(box.workdir, "thumbnail-b.jpg"), Buffer.from("thumbnail B"));
    writeFileSync(path.join(box.workdir, "thumbnail-c.jpg"), Buffer.from("thumbnail C"));
    manifest.thumbnail_variants = ["thumbnail-b.jpg", "thumbnail-c.jpg"];
  }
  writeFileSync(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify(manifest));
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir, now: NOW });
  return { box, final };
}

function site() {
  const state = { files: new Map(), reviews: [] };
  const fetchImpl = async (url, init = {}) => {
    if (!url.startsWith("https://mokaair.com/")) return new Response("", { status: 200 });
    const { pathname, searchParams } = new URL(url);
    if (pathname === "/api/video/automation/judge/policy") return Response.json({ detail: "Not Found" }, { status: 404 });
    const route = pathname.replace("/api/video/reviews/", "");
    if (init.method === "PUT" && route.includes("/files/")) {
      const parts = state.files.get(route.split("/files/")[1]) ?? [];
      parts[Number(searchParams.get("part"))] = Buffer.from(init.body);
      state.files.set(route.split("/files/")[1], parts);
      return Response.json({ received: parts.map((_, index) => index), complete: parts.filter(Boolean).length === Number(searchParams.get("parts")) });
    }
    if (init.method === "PUT") return Response.json({ ...JSON.parse(init.body), reviews: [], pending: 0 });
    if (init.method === "POST") {
      state.reviews.unshift({ id: `r${state.reviews.length}`, status: "pending", choice: null, note: null, decided_at: null, ...JSON.parse(init.body) });
      return Response.json(state.reviews[0], { status: 201 });
    }
    return Response.json({ slug: "fixture-minimal", reviews: state.reviews });
  };
  return { state, fetchImpl };
}

function context(box, extra = {}) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
      home: box.base,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => NOW,
      sleep: async () => {},
      ...extra,
    },
  };
}

const uploadOf = (box) => path.join(box.workdir, "upload");
const readUpload = (box, file) => readFileSync(path.join(uploadOf(box), file), "utf8");

test("package carries B and C beside A, records them, and UPLOAD.md sends all three to Studio's thumbnail test", async (t) => {
  const { box } = await finishedVideo({ variants: true });
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const { out, ctx } = context(box);
  assert.equal(await main(["package", "--slug", box.slug], ctx), EXIT.ok, out.stderr + out.stdout);
  assert.equal(readUpload(box, "thumbnail-b.jpg"), "thumbnail B");
  assert.equal(readUpload(box, "thumbnail-c.jpg"), "thumbnail C");
  const metadata = JSON.parse(readUpload(box, "metadata.json"));
  assert.deepEqual(metadata.thumbnail_variants, ["thumbnail-b.jpg", "thumbnail-c.jpg"]);
  assert.deepEqual(Object.keys(metadata).slice(-2), ["contains_synthetic_media", "disclosure_reason"], "the disclosure stays last");
  const md = readUpload(box, "UPLOAD.md");
  assert.match(md, /4\. 縮圖：在「縮圖」點「測試與比較」，選縮圖測試，`thumbnail\.jpg`（A）、`thumbnail-b\.jpg`（B）、`thumbnail-c\.jpg`（C）全部上傳（一支影片最多三張/);
  assert.match(md, /\*\*測試期間不要改標題\*\*/);
  assert.match(out.stdout, /thumbnail\.jpg, thumbnail-b\.jpg, thumbnail-c\.jpg \(Test & compare\)/);
  assert.match(out.stdout, /\[x\] files: final\.mp4, thumbnail\.jpg, thumbnail-b\.jpg, thumbnail-c\.jpg, metadata\.json;/);

  // The publish review attaches B and C under roles the site's cards do not read as a language.
  const server = site();
  const push = context(box, { fetch: server.fetchImpl });
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "publish"], push.ctx), EXIT.ok, push.out.stderr);
  const roles = server.state.reviews[0].files.map((file) => [file.role, file.content_type]);
  assert.deepEqual(roles.filter(([role]) => role.startsWith("thumbnail")), [["thumbnail-b", "image/jpeg"], ["thumbnail-c", "image/jpeg"], ["thumbnail", "image/jpeg"]]);
  assert.equal(server.state.reviews[0].payload.package.ok, true);

  // A variant render listed that is gone by package time is recorded, and the check names it.
  rmSync(path.join(box.workdir, "thumbnail-c.jpg"));
  const again = context(box);
  assert.equal(await main(["package", "--slug", box.slug], again.ctx), EXIT.lint);
  assert.match(again.out.stdout, /\[ \] files: thumbnail-c\.jpg is listed but missing/);
});

test("a video without variants packages byte for byte as before: no new key, file, line or output", async (t) => {
  const { box } = await finishedVideo();
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const { out, ctx } = context(box);
  assert.equal(await main(["package", "--slug", box.slug], ctx), EXIT.ok, out.stderr + out.stdout);
  assert.deepEqual(readdirSync(uploadOf(box)).sort(), ["UPLOAD.md", "captions", "description.zh-TW.txt", "final.mp4", "metadata.json", "thumbnail.jpg"]);
  const metadata = JSON.parse(readUpload(box, "metadata.json"));
  assert.equal(Object.hasOwn(metadata, "thumbnail_variants"), false);
  assert.deepEqual(Object.keys(metadata).slice(-10), ["thumbnail", "thumbnails", "skipped_thumbnail_locales", "captions", "skipped_caption_locales", "dubs", "skipped_dub_locales", "language_choice", "contains_synthetic_media", "disclosure_reason"]);
  assert.match(readUpload(box, "UPLOAD.md"), /\n4\. 縮圖：上傳 `thumbnail\.jpg`（帳號需完成手機驗證）。\n/);
  assert.doesNotMatch(readUpload(box, "UPLOAD.md"), /測試與比較/);
  assert.match(out.stdout, /\n {2}final\.mp4, thumbnail\.jpg, 1 caption files,/);
  assert.match(out.stdout, /\[x\] files: final\.mp4, thumbnail\.jpg, metadata\.json; final\.mp4 is the approved final/);
  // Variants listed without a thumbnail.jpg go nowhere: there is no A to test them against.
  rmSync(path.join(box.workdir, "thumbnail.jpg"));
  writeFileSync(path.join(box.workdir, "thumbnail-b.jpg"), "B");
  writeFileSync(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ thumbnail: null, thumbnail_variants: ["thumbnail-b.jpg"] }));
  const bare = context(box);
  assert.equal(await main(["package", "--slug", box.slug], bare.ctx), EXIT.ok, bare.out.stderr + bare.out.stdout);
  assert.equal(existsSync(path.join(uploadOf(box), "thumbnail-b.jpg")), false);
  assert.equal(Object.hasOwn(JSON.parse(readUpload(box, "metadata.json")), "thumbnail_variants"), false);
});

test("the package check fails a listed variant that is missing or over 2 MB, as it does A", () => {
  const metadata = { thumbnail: "thumbnail.jpg", thumbnails: {}, thumbnail_variants: ["thumbnail-b.jpg", "thumbnail-c.jpg"], final_sha256: "f".repeat(64), default_language: "zh-TW", localizations: {}, captions: [], contains_synthetic_media: false, disclosure_reason: "slides" };
  const files = (extra) => new Map([["final.mp4", 10], ["metadata.json", 10], ["thumbnail.jpg", 10], ["thumbnail-b.jpg", 10], ["thumbnail-c.jpg", 10], ["description.zh-TW.txt", 10], ["captions/zh-TW.srt", 10], ...extra]);
  const check = (map) => checkPackage({ files: map, metadata, finalSha256: "f".repeat(64), approvedSha256: "f".repeat(64), metadataSha256: "m".repeat(64), locales: ["zh-TW"] }).items[0];
  assert.equal(check(files([])).ok, true);
  assert.match(check(files([])).detail, /^final\.mp4, thumbnail\.jpg, thumbnail-b\.jpg, thumbnail-c\.jpg, metadata\.json;/);
  const gone = files([]);
  gone.delete("thumbnail-c.jpg");
  assert.equal(check(gone).detail, "thumbnail-c.jpg is listed but missing");
  assert.equal(check(files([["thumbnail-b.jpg", THUMBNAIL_MAX_BYTES + 1]])).detail, `thumbnail-b.jpg is ${THUMBNAIL_MAX_BYTES + 1} bytes; YouTube's limit is 2 MB`);
  assert.equal(check(files([["thumbnail.jpg", THUMBNAIL_MAX_BYTES + 1]])).ok, false, "A is held to the same limit");
  assert.equal(check(files([["thumbnail-b.jpg", THUMBNAIL_MAX_BYTES]])).ok, true, "exactly 2 MB is within the limit");
});

test("variants come only from render's list, and each goes up under its own role", () => {
  assert.deepEqual(thumbnailVariants({ thumbnail_variants: ["thumbnail-b.jpg", "../thumbnail-c.jpg", "thumbnails/en.jpg", 3, "thumbnail-c.jpg"] }), ["thumbnail-b.jpg", "thumbnail-c.jpg"]);
  assert.deepEqual(thumbnailVariants(null), []);
  assert.deepEqual(thumbnailVariants({ thumbnail: "thumbnail.jpg" }), []);
  assert.equal(variantRole("thumbnail-b.jpg"), "thumbnail-b");
  assert.deepEqual(packageFiles(["thumbnail.jpg", "thumbnail-b.jpg", "thumbnails/en.jpg", "UPLOAD.md"]), [
    { path: "thumbnail-b.jpg", role: "thumbnail-b", content_type: "image/jpeg" },
    { path: "thumbnail.jpg", role: "thumbnail", content_type: "image/jpeg" },
    { path: "thumbnails/en.jpg", role: "thumbnail_en", content_type: "image/jpeg" },
  ]);
  assert.equal(thumbnailStep(false, ["thumbnail-b.jpg"]), "這次沒有縮圖，Studio 會自動挑一格");
  assert.equal(thumbnailStep(true), "上傳 `thumbnail.jpg`（帳號需完成手機驗證）");
  const metadata = { title: "t", made_for_kids: false, category_id: "28" };
  assert.match(uploadChecklist({ metadata, captions: [], thumbnail: true, variants: ["thumbnail-b.jpg"] }), /`thumbnail\.jpg`（A）、`thumbnail-b\.jpg`（B）全部上傳/);
});

test("the final review sends B and C with A so the owner sees all three; without variants A goes alone, as before", async (t) => {
  for (const variants of [true, false]) {
    const { box, final } = await finishedVideo({ variants });
    t.after(() => rmSync(box.base, { recursive: true, force: true }));
    const server = site();
    const qa = async () => {
      mkdirSync(path.join(box.workdir, "review"), { recursive: true });
      writeFileSync(path.join(box.workdir, "review", "qa.json"), JSON.stringify({ ok: true, final_sha256: sha(final), items: ITEM_IDS.map((id) => ({ id, ok: true, detail: "passed" })) }));
      return { code: EXIT.ok };
    };
    const encode = async (kind, source, target) => writeFileSync(target, Buffer.from(`${kind} of ${path.basename(source)}`));
    const push = context(box, { fetch: server.fetchImpl, runCommand: qa, encode });
    assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "final"], push.ctx), EXIT.ok, push.out.stderr);
    const files = server.state.reviews[0].files;
    assert.deepEqual(files.map((file) => file.role), variants ? ["preview", "thumbnail", "thumbnail-b", "thumbnail-c"] : ["preview", "thumbnail"]);
    if (variants) assert.equal(files.find((file) => file.role === "thumbnail-c").sha256, sha(Buffer.from("thumbnail C")));
  }
});
