import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, mkdtempSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { test } from "node:test";

import { AREAS, EXIT, main } from "../cli.mjs";
import { UsageError } from "../core/paths.mjs";
import { chaptersFrom, finalReview, IMPORTED, importLong, measureProblems, projectBody, readMeta } from "./import.mjs";

const DESCRIPTION = "一段說明。\n\n章節\n00:00 一張圖，三個問題\n00:48 畫面真，不代表故事真\n1:02:03 很長的一章\n\n資料來源\nS01｜NIST";
const META = { slug: "ai-real-world-01-image-trust", titles: ["照片不能當證據之後，我們還能相信什麼？", "AI 圖片越來越真：我們該怎麼查證？"], description: DESCRIPTION };

// What ffprobe says of a cut the pipeline would make, and of season one's 24 fps review cuts.
const stream = (overrides = {}) => ({
  streams: [
    { codec_type: "video", codec_name: "h264", width: 1920, height: 1080, r_frame_rate: "30/1", pix_fmt: "yuv420p", duration: "480.000000", nb_read_packets: "14400", ...overrides.video },
    { codec_type: "audio", codec_name: "aac", sample_rate: "48000", channels: 2, duration: "480.021333", ...overrides.audio },
  ],
});
const LOUD = { integrated: -14.2, truePeak: -1.3 };

test("the command is registered under its own area", () => {
  assert.deepEqual(AREAS.import, ["import", "2026-09-28-video-tool-import-a-finished-long"]);
});

test("chapters come from the description's clock lines", () => {
  assert.deepEqual(chaptersFrom(DESCRIPTION), [
    { time: "00:00", title: "一張圖，三個問題" },
    { time: "00:48", title: "畫面真，不代表故事真" },
    { time: "1:02:03", title: "很長的一章" },
  ]);
  assert.deepEqual(chaptersFrom("no chapters here"), []);
});

test("meta.json takes one title or two, and reads chapters from the description", () => {
  const meta = readMeta(META);
  assert.deepEqual(meta.titles, META.titles);
  assert.equal(meta.chapters.length, 3);
  assert.equal(meta.source_guide, null);
  assert.equal(meta.category, null, "the owner files an unfiled import on the page");
  assert.equal(readMeta({ ...META, category: "tutorial" }).category, "tutorial");
  assert.deepEqual(readMeta({ ...META, titles: undefined, title: " 一個標題 " }).titles, ["一個標題"]);
  const listed = readMeta({ ...META, chapters: [{ time: "00:00", title: "開場" }] });
  assert.deepEqual(listed.chapters, [{ time: "00:00", title: "開場" }]);
});

test("meta.json that cannot be imported lists every problem", () => {
  assert.throws(() => readMeta({ slug: "Bad Slug", titles: ["a", "b", "c"], description: "" }), (error) => {
    assert.ok(error instanceof UsageError);
    assert.match(error.message, /slug/);
    assert.match(error.message, /titles/);
    assert.match(error.message, /description required/);
    return true;
  });
  assert.throws(() => readMeta({ ...META, titles: ["x".repeat(101)] }), /titles/);
  assert.throws(() => readMeta({ ...META, titles: ["<b>bold</b>"] }), /angle brackets/);
  assert.throws(() => readMeta({ ...META, description: "字".repeat(1700) }), /5100 bytes, YouTube takes 5000/);
  assert.throws(() => readMeta({ ...META, chapters: [{ time: "later", title: "x" }] }), /chapters/);
  assert.throws(() => readMeta({ ...META, source_guide: "Not A Slug" }), /source_guide/);
  assert.throws(() => readMeta({ ...META, category: "news" }), /category must be one of ai-terms, ai-news/);
});

test("a cut on the pipeline's profile has nothing to say", () => {
  const { seconds, problems } = measureProblems(stream(), LOUD);
  assert.equal(seconds, 480);
  assert.deepEqual(problems, []);
});

test("every difference from the pipeline's profile is said, none refuses", () => {
  const probe = stream({ video: { r_frame_rate: "24/1", width: 1280, height: 720, duration: "454.500000" }, audio: { channels: 1, sample_rate: "44100", duration: "454.520000" } });
  const { seconds, problems } = measureProblems(probe, { integrated: -18.4, truePeak: 0.2 });
  assert.equal(seconds, 454.5);
  assert.deepEqual(problems, [
    "picture is 1280×720, the pipeline makes 1920×1080",
    "24 fps, the pipeline makes 30",
    "audio at 44100 Hz, the pipeline makes 48000",
    "1 audio channel(s), the pipeline makes stereo",
    "loudness -18.4 LUFS, the pipeline makes -14 ± 1",
    "true peak 0.2 dBFS, above -1",
  ]);
  assert.deepEqual(measureProblems({ streams: [] }, LOUD), { seconds: 0, problems: ["no video stream"] });
  assert.deepEqual(measureProblems(stream({ audio: { duration: "470.000000" } }), LOUD).problems, ["sound lasts 470.00 s, picture 480.00 s"]);
  const silent = { streams: [stream().streams[0]] };
  assert.deepEqual(measureProblems(silent, LOUD).problems, ["no audio stream"]);
});

test("the site is told of a tutorial waiting at its final cut, marked as imported", () => {
  const body = projectBody(readMeta({ ...META, source_guide: "ai-image-trust" }));
  assert.equal(body.title, META.titles[0]);
  assert.equal(body.format, "slides");
  assert.equal(body.stage, "final video approved");
  assert.equal(body.source_guide, "ai-image-trust");
  assert.deepEqual(body.checklist.map((item) => [item.key, item.done]), [[IMPORTED, true], ["final_video_approved", false]]);
  assert.equal(projectBody(readMeta(META)).source_guide, undefined);
  assert.equal(projectBody(readMeta(META)).category, undefined, "nothing filed is left to the page");
  assert.equal(projectBody(readMeta({ ...META, category: "comparison" })).category, "comparison");
});

test("the final review carries what the page shows and says it was imported", () => {
  const meta = readMeta({ ...META, note: "PR #880" });
  const review = finalReview({ meta, sha256: "a".repeat(64), seconds: 481.4, problems: ["24 fps, the pipeline makes 30"], captions: true });
  assert.equal(review.gate, "final");
  assert.equal(review.content_sha256, "a".repeat(64));
  assert.equal(review.summary, "成片 08:01，別的工具做好後匯入；有 1 項跟產線規格不同；沒有自動品管報告");
  assert.deepEqual(review.payload.checks, { ok: false, problems: ["24 fps, the pipeline makes 30"] });
  assert.deepEqual(review.payload.titles, META.titles);
  assert.equal(review.payload.chapters.length, 3);
  assert.deepEqual(review.payload.metadata, { "zh-TW": { title: META.titles[0], description: DESCRIPTION } });
  assert.deepEqual(review.payload.imported, { note: "PR #880", captions: true });
  const single = finalReview({ meta: readMeta({ ...META, titles: ["一個"] }), sha256: "b".repeat(64), seconds: 60, problems: [], captions: false });
  assert.equal(single.payload.titles, undefined);
  assert.match(single.summary, /規格檢查全部通過/);
});

/** A directory to import, a work directory outside it, and a site that records what it is sent. */
function fixture(t, { meta = META, known = null, thumbnail = true, captions = true } = {}) {
  const box = mkdtempSync(path.join(os.tmpdir(), "video-import-"));
  t.after(() => rmSync(box, { recursive: true, force: true }));
  const from = path.join(box, "from");
  mkdirSync(from);
  writeFileSync(path.join(from, "final.mp4"), "the cut");
  writeFileSync(path.join(from, "meta.json"), JSON.stringify(meta));
  if (thumbnail) writeFileSync(path.join(from, "thumbnail.png"), "png");
  if (captions) writeFileSync(path.join(from, "zh-TW.srt"), "1\n00:00:00,000 --> 00:00:01,000\n字幕\n");
  const calls = [];
  const client = {
    project: async (slug) => (calls.push(["project", slug]), known),
    report: async (slug, body) => (calls.push(["report", slug, body]), {}),
    part: async (slug, sha) => (calls.push(["part", slug, sha]), { complete: true }),
    submit: async (slug, review) => (calls.push(["submit", slug, review]), { status: "pending" }),
  };
  const encodes = [];
  const encode = async (source, target) => (encodes.push(source), writeFileSync(target, "preview"));
  const measure = async () => ({ probe: stream({ video: { r_frame_rate: "24/1" } }), loudness: LOUD });
  return { from, workdir: path.join(box, "work"), client, calls, encode, encodes, measure };
}

test("an import reports the video, sends its files and submits the final cut", async (t) => {
  const box = fixture(t);
  const result = await importLong({ from: box.from, workdir: box.workdir, client: box.client, measure: box.measure, encode: box.encode });
  assert.deepEqual(result, { slug: META.slug, status: "pending", seconds: 480, problems: ["24 fps, the pipeline makes 30"] });
  assert.deepEqual(box.calls.map((call) => call[0]), ["project", "report", "part", "part", "part", "submit"]);
  assert.equal(box.calls[1][2].title, META.titles[0]);
  const review = box.calls.at(-1)[2];
  assert.deepEqual(review.files.map((file) => [file.role, file.content_type]), [["preview", "video/mp4"], ["thumbnail", "image/png"], ["captions_zh-TW", "application/x-subrip"]]);
  // The review is bound to the cut itself, not to the 720p copy the page plays.
  assert.equal(review.content_sha256, createHash("sha256").update("the cut").digest("hex"));
  assert.notEqual(review.content_sha256, review.files[0].sha256);
  assert.equal(review.payload.imported.captions, true);
  assert.equal(box.encodes.length, 1);

  // Sent again: the copy is reused, and the site answers with the review it has.
  await importLong({ from: box.from, workdir: box.workdir, client: box.client, measure: box.measure, encode: box.encode });
  assert.equal(box.encodes.length, 1);
});

test("a directory without a thumbnail or captions sends the cut alone", async (t) => {
  const box = fixture(t, { thumbnail: false, captions: false });
  await importLong({ from: box.from, workdir: box.workdir, client: box.client, measure: box.measure, encode: box.encode });
  const review = box.calls.at(-1)[2];
  assert.deepEqual(review.files.map((file) => file.role), ["preview"]);
  assert.equal(review.payload.imported.captions, false);
});

test("a video the site knows from elsewhere is not overwritten without --force", async (t) => {
  const box = fixture(t, { known: { slug: META.slug, checklist: [{ key: "brief", label: "企劃書", done: true }] } });
  await assert.rejects(importLong({ from: box.from, workdir: box.workdir, client: box.client, measure: box.measure, encode: box.encode }), /already on the site and was not imported/);
  assert.deepEqual(box.calls.map((call) => call[0]), ["project"]);
  const forced = await importLong({ from: box.from, workdir: box.workdir, client: box.client, measure: box.measure, encode: box.encode, force: true });
  assert.equal(forced.status, "pending");
  // One it imported before is updated without asking.
  const again = fixture(t, { known: { slug: META.slug, checklist: [{ key: IMPORTED, label: "別的工具做好的成片", done: true }] } });
  assert.equal((await importLong({ from: again.from, workdir: again.workdir, client: again.client, measure: again.measure, encode: again.encode })).status, "pending");
});

test("a directory missing its cut or meta.json is refused before the site is asked", async (t) => {
  const box = fixture(t);
  rmSync(path.join(box.from, "meta.json"));
  await assert.rejects(importLong({ from: box.from, workdir: box.workdir, client: box.client, measure: box.measure, encode: box.encode }), /has no meta.json/);
  assert.deepEqual(box.calls, []);
});

test("the command asks for --from", async () => {
  let err = "";
  const code = await main(["import"], { stderr: { write: (chunk) => { err += chunk; } }, stdout: { write: () => {} } });
  assert.equal(code, EXIT.usage);
  assert.match(err, /import needs --from DIR/);
});
