// An imported video's upload package, fetched from the review store into video_work before the
// backup (review-package.mjs), and the full tier then copying its clips/ to Drive.
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { BackupError, backupClient, backupRound } from "./backup.mjs";
import { descriptionsOf, fetchReviewPackage, PACKAGE_RECORD, placeOf } from "./review-package.mjs";

const NOW = new Date("2026-10-31T12:00:00Z");
const SLUG = "zhong-tian-qu-qi-e033";
const sha = (text) => createHash("sha256").update(text).digest("hex");
const METADATA = JSON.stringify({ title: "第 33 集", description: "說明", default_language: "zh-TW", localizations: { en: { title: "Episode 33", description: "About it" } }, skipped_caption_locales: {}, skipped_dub_locales: {} });

/** The store's bytes by SHA-256, and the approved publish review naming them. */
function storeOf(entries) {
  const bytes = new Map();
  const files = entries.map(([role, content_type, text]) => {
    bytes.set(sha(text), text);
    return { role, content_type, sha256: sha(text), size: Buffer.byteLength(text) };
  });
  const review = { id: "11111111-2222-3333-4444-555555555555", gate: "publish", status: "approved", content_sha256: sha(METADATA), files };
  return { bytes, review };
}

const PACKAGE = [
  ["metadata", "application/json", METADATA],
  ["final", "video/mp4", "the 1080p cut"],
  ["thumbnail", "image/png", "png"],
  ["captions_zh-TW", "application/x-subrip", "1\n00:00:00,000 --> 00:00:01,000\n字幕\n"],
  ["captions_en", "application/x-subrip", "1\n00:00:00,000 --> 00:00:01,000\nCaptions\n"],
  ["dub_en", "audio/mp4", "english dub"],
  ["clip_s01-t1", "video/mp4", "shot one"],
  ["clip_s02-t1", "video/mp4", "shot two"],
  ["evidence_qa", "application/json", "{}"],
];

/** The site's review routes over a store; `gone` answers 404 for a hash, `downloads` counts. */
function siteOf(store, { gone = new Set(), corrupt = false } = {}) {
  const site = { downloads: [], projects: 0, store };
  site.client = {
    project: async () => {
      site.projects += 1;
      return { slug: SLUG, reviews: [site.store.review] };
    },
    download: async (_slug, digest, target) => {
      site.downloads.push(digest);
      if (gone.has(digest)) throw new BackupError("not here", { status: 404, code: "video_review_file_not_found" });
      writeFileSync(target, corrupt ? "garbled" : site.store.bytes.get(digest));
    },
  };
  return site;
}

const packageOf = (store) => ({ review_id: store.review.id, content_sha256: store.review.content_sha256 });
const videoOf = (store, extra = {}) => ({ slug: SLUG, review_package: packageOf(store), tier: "full", ...extra });
const listing = (dir, prefix = "") => (existsSync(dir) ? readdirSync(dir, { withFileTypes: true }).flatMap((entry) => (entry.isDirectory() ? listing(path.join(dir, entry.name), `${prefix}${entry.name}/`) : [`${prefix}${entry.name}`])).sort() : []);

test("each package role has its place in the work directory, as package lays it out; others have none", () => {
  assert.equal(placeOf("metadata", "application/json"), "upload/metadata.json");
  assert.equal(placeOf("final", "video/mp4"), "upload/final.mp4");
  assert.equal(placeOf("thumbnail", "image/png"), "upload/thumbnail.png");
  assert.equal(placeOf("thumbnail-b", "image/jpeg"), "upload/thumbnail-b.jpg");
  assert.equal(placeOf("thumbnail_ja", "image/jpeg"), "upload/thumbnails/ja.jpg");
  assert.equal(placeOf("captions_zh-TW", "application/x-subrip"), "upload/captions/zh-TW.srt");
  assert.equal(placeOf("description_en", "text/plain"), "upload/description.en.txt");
  assert.equal(placeOf("dub_pt", "audio/mp4"), "upload/dubs/pt.m4a");
  assert.equal(placeOf("clip_s01-t1", "video/mp4"), "clips/s01-t1.mp4");
  for (const [role, type] of [["clip_s01-t1", "image/png"], ["clip_../x", "video/mp4"], ["dub_unchecked_en", "audio/mp4"], ["evidence_qa", "application/json"], ["preview", "video/mp4"], ["final", "image/png"]]) {
    assert.equal(placeOf(role, type), null, `${role} ${type}`);
  }
});

test("descriptions come from metadata.json: zh-TW's own and each localization's", () => {
  assert.deepEqual(descriptionsOf(JSON.parse(METADATA)), {
    "upload/description.zh-TW.txt": "第 33 集\n\n說明\n",
    "upload/description.en.txt": "Episode 33\n\nAbout it\n",
  });
});

test("the package is fetched once, checked, laid out with its clips, and never into a folder made here", async (t) => {
  const base = mkdtempSync(path.join(os.tmpdir(), "review-package-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const store = storeOf(PACKAGE);
  const site = siteOf(store);
  const result = await fetchReviewPackage({ base, video: videoOf(store), client: site.client, now: NOW });
  assert.equal(result.complete, true);
  assert.match(result.line, /8 file\(s\), 2 clip\(s\)/);
  const dir = path.join(base, SLUG);
  assert.deepEqual(listing(dir), [
    "clips/s01-t1.mp4", "clips/s02-t1.mp4", PACKAGE_RECORD,
    "upload/captions/en.srt", "upload/captions/zh-TW.srt", "upload/description.en.txt", "upload/description.zh-TW.txt",
    "upload/dubs/en.m4a", "upload/final.mp4", "upload/metadata.json", "upload/thumbnail.png",
  ]);
  assert.equal(readFileSync(path.join(dir, "clips", "s02-t1.mp4"), "utf8"), "shot two");
  const record = JSON.parse(readFileSync(path.join(dir, PACKAGE_RECORD), "utf8"));
  assert.equal(record.review_id, store.review.id);
  assert.deepEqual(record.gone, []);

  assert.equal(await fetchReviewPackage({ base, video: videoOf(store), client: site.client, now: NOW }), null, "fetched once");
  assert.equal(site.projects, 1);

  const other = siteOf(storeOf(PACKAGE));
  mkdirSync(path.join(base, "made-by-hand"));
  assert.equal(await fetchReviewPackage({ base, video: videoOf(store, { slug: "made-by-hand" }), client: other.client, now: NOW }), null);
  mkdirSync(path.join(base, "worker-made"));
  writeFileSync(path.join(base, "worker-made", "auto.json"), "{}");
  assert.equal(await fetchReviewPackage({ base, video: videoOf(store, { slug: "worker-made" }), client: other.client, now: NOW }), null);
  assert.equal(other.projects, 0, "neither folder is asked about");
});

test("a broken download is never placed; a file the store let go is recorded as gone; a round's budget is kept", async (t) => {
  const base = mkdtempSync(path.join(os.tmpdir(), "review-package-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const store = storeOf(PACKAGE);
  const bad = await fetchReviewPackage({ base, video: videoOf(store), client: siteOf(store, { corrupt: true }).client, now: NOW });
  assert.equal(bad.complete, false);
  assert.match(bad.line, /did not match the review's SHA-256/);
  assert.ok(!existsSync(path.join(base, SLUG, "upload", "metadata.json")));

  const slow = siteOf(store);
  const first = await fetchReviewPackage({ base, video: videoOf(store), client: slow.client, budget: 3, now: NOW });
  assert.equal(first.complete, false);
  assert.equal(slow.downloads.length, 3);
  const gone = siteOf(store, { gone: new Set([sha("shot two")]) });
  const rest = await fetchReviewPackage({ base, video: videoOf(store), client: gone.client, now: NOW });
  assert.equal(rest.complete, true);
  assert.ok(!gone.downloads.includes(sha(METADATA)), "what is already here is not fetched again");
  assert.match(rest.line, /no longer in the review store: clips\/s02-t1.mp4/);
  assert.deepEqual(JSON.parse(readFileSync(path.join(base, SLUG, PACKAGE_RECORD), "utf8")).gone, ["clips/s02-t1.mp4"]);
  assert.equal(readFileSync(path.join(base, SLUG, "upload", "final.mp4"), "utf8"), "the 1080p cut", "the first round's files stand");
});

test("a renewed package replaces what the old one placed and only that", async (t) => {
  const base = mkdtempSync(path.join(os.tmpdir(), "review-package-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const old = storeOf(PACKAGE);
  await fetchReviewPackage({ base, video: videoOf(old), client: siteOf(old).client, now: NOW });
  writeFileSync(path.join(base, SLUG, "notes.txt"), "someone's");
  const renewed = storeOf([...PACKAGE.filter(([role]) => role !== "dub_en" && role !== "final"), ["final", "video/mp4", "the renewed cut"]]);
  renewed.review.id = "99999999-2222-3333-4444-555555555555";
  const result = await fetchReviewPackage({ base, video: videoOf(renewed), client: siteOf(renewed).client, now: NOW });
  assert.equal(result.complete, true);
  const dir = path.join(base, SLUG);
  assert.equal(readFileSync(path.join(dir, "upload", "final.mp4"), "utf8"), "the renewed cut");
  assert.ok(!existsSync(path.join(dir, "upload", "dubs", "en.m4a")), "the dub the new package dropped goes from here");
  assert.ok(existsSync(path.join(dir, "notes.txt")), "a file it did not place stays");
});

test("the backup round fetches an imported video's package first and the full tier copies its clips to Drive", async (t) => {
  const box = mkdtempSync(path.join(os.tmpdir(), "review-package-round-"));
  t.after(() => rmSync(box, { recursive: true, force: true }));
  const work = path.join(box, "work");
  const drive = path.join(box, "drive");
  mkdirSync(work, { recursive: true });
  mkdirSync(drive, { recursive: true });
  writeFileSync(path.join(box, "rclone.conf"), "[videobackup]\ntype = alias\n");
  const store = storeOf(PACKAGE);
  const reviews = siteOf(store);
  const reports = [];
  const video = {
    slug: SLUG, youtube_video_id: null, category: "drama", series_key: "zhong-tian-qu-qi", series_slug: "zhong-tian-qu-qi", episode_number: 33,
    folder: "zhong-tian-qu-qi/033-zhong-tian-qu-qi-e033", shared_folder: "zhong-tian-qu-qi/_共用", tier: "full",
    expected: { required: ["final.mp4", "metadata.json"], descriptions: ["en"], captions: ["en"], dubs: ["en"] }, backup: null,
    review_package: packageOf(store),
  };
  const client = {
    ...reviews.client,
    config: async () => ({ enabled: true, path: "AI/備份", lock_path: "AI/備份", remote_prefix: "", problem: null, test: null, videos: [video] }),
    lock: async () => ({}),
    answer: async () => ({}),
    report: async (slug, body) => {
      reports.push({ slug, ...body });
      return { state: body.state, missing: [] };
    },
  };
  const local = (where) => (where.startsWith("videobackup:") ? path.join(drive, ...where.slice("videobackup:".length).split("/").filter(Boolean)) : where);
  const rclone = async (args) => {
    const [command, source, target] = args;
    if (command === "about") return { code: 0, stdout: JSON.stringify({ total: 5 * 1024 ** 4, free: 4 * 1024 ** 4 }), stderr: "" };
    if (command === "copy") {
      for (const relative of listing(source)) {
        mkdirSync(path.dirname(path.join(local(target), relative)), { recursive: true });
        cpSync(path.join(source, relative), path.join(local(target), relative));
      }
    }
    if (command === "copyto") {
      mkdirSync(path.dirname(local(target)), { recursive: true });
      cpSync(source, local(target));
    }
    return { code: 0, stdout: "", stderr: "" };
  };
  const ctx = { env: { VIDEO_WORKDIR: work, VIDEO_BACKUP_RCLONE_CONFIG: path.join(box, "rclone.conf"), VIDEO_BACKUP_LOCK_PATH: "AI/備份", TMPDIR: box }, now: () => NOW, root: path.join(box, "repo") };
  const { lines } = await backupRound(ctx, { client, rclone });
  assert.ok(lines.some((line) => /fetched its upload package from the site \(8 file\(s\), 2 clip\(s\)\)/.test(line)), lines.join("\n"));
  const episode = path.join(drive, "zhong-tian-qu-qi", "033-zhong-tian-qu-qi-e033");
  const copied = listing(episode);
  for (const name of ["clips/s01-t1.mp4", "clips/s02-t1.mp4", "final.mp4", "metadata.json", "descriptions/en.txt", "captions/en.srt", "dubs/en.m4a", "backup.json"]) {
    assert.ok(copied.includes(name), `${name} in Drive: ${copied.join(", ")}`);
  }
  assert.ok(!copied.some((name) => name.includes(PACKAGE_RECORD) || name.includes("partial")), "the fetch's own record stays on the host");
  const done = reports.find((report) => report.state === "done");
  assert.equal(done.contents.clips, 2);
  assert.deepEqual(done.contents.dubs, ["en"]);

  const again = await backupRound(ctx, { client, rclone });
  assert.ok(!again.lines.some((line) => /fetched its upload package/.test(line)));
  assert.equal(reviews.projects, 1, "the package is fetched once");
});

test("a package the store let go entirely is told to the site once, not retried, and a renewed one is backed up", async (t) => {
  const box = mkdtempSync(path.join(os.tmpdir(), "review-package-gone-"));
  t.after(() => rmSync(box, { recursive: true, force: true }));
  const work = path.join(box, "work");
  mkdirSync(work, { recursive: true });
  writeFileSync(path.join(box, "rclone.conf"), "[videobackup]\ntype = alias\n");
  const store = storeOf(PACKAGE);
  const reviews = siteOf(store, { gone: new Set(PACKAGE.map(([, , text]) => sha(text))) });
  const reports = [];
  const video = { slug: SLUG, youtube_video_id: "abc", category: "drama", series_key: "zhong-tian-qu-qi", folder: `zhong-tian-qu-qi/${SLUG}`, tier: "full", backup: null, review_package: packageOf(store) };
  const client = {
    ...reviews.client,
    config: async () => ({ enabled: true, path: "AI/備份", lock_path: "AI/備份", remote_prefix: "", problem: null, test: null, videos: [video] }),
    lock: async () => ({}),
    answer: async () => ({}),
    report: async (slug, body) => {
      reports.push(body);
      return { state: body.state, missing: [] };
    },
  };
  const rclone = async (args) => (args[0] === "about" ? { code: 0, stdout: JSON.stringify({ total: 5 * 1024 ** 4, free: 4 * 1024 ** 4 }), stderr: "" } : { code: 0, stdout: "", stderr: "" });
  const ctx = { env: { VIDEO_WORKDIR: work, VIDEO_BACKUP_RCLONE_CONFIG: path.join(box, "rclone.conf"), VIDEO_BACKUP_LOCK_PATH: "AI/備份", TMPDIR: box }, now: () => NOW, root: path.join(box, "repo") };

  const first = await backupRound(ctx, { client, rclone });
  assert.ok(!first.lines.some((line) => /\bfailed\b/.test(line)), first.lines.join("\n"));
  assert.ok(first.lines.some((line) => /no longer holds its upload package/.test(line)), first.lines.join("\n"));
  assert.equal(first.gate.verdicts.get(SLUG).ok, false, "the tidy never reads it as backed up");
  assert.deepEqual(reports.filter((report) => report.state === "failed").map((report) => report.attempts), [0]);

  const later = { ...ctx, now: () => new Date(NOW.getTime() + 24 * 3600_000) };
  const second = await backupRound(later, { client, rclone });
  assert.deepEqual(second.lines, [], "nothing to say, and nothing tried, a day later");
  assert.equal(reports.filter((report) => report.state === "failed").length, 1);

  // The owner renews the package: a new review, its files in the store again.
  const renewed = siteOf(store);
  store.review.id = "99999999-2222-3333-4444-555555555555";
  video.review_package = packageOf(store);
  client.download = renewed.client.download;
  const third = await backupRound(later, { client, rclone });
  assert.ok(third.lines.some((line) => /fetched its upload package from the site \(8 file/.test(line)), third.lines.join("\n"));
  assert.ok(reports.some((report) => report.state === "done"), JSON.stringify(reports.map((report) => report.state)));
});

test("the worker reads the package through the review store's tool routes with its token", async (t) => {
  const dir = mkdtempSync(path.join(os.tmpdir(), "review-package-client-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const asked = [];
  const fetch = async (url, init) => {
    asked.push([url, init.headers.Authorization, init.headers.Accept]);
    if (url.endsWith("/files/" + "f".repeat(64))) return new Response(JSON.stringify({ code: "video_review_file_not_found", detail: "gone" }), { status: 404 });
    if (url.includes("/files/")) return new Response("clip bytes");
    return Response.json({ slug: SLUG, reviews: [] });
  };
  const client = backupClient({ env: { MOKAAIR_SITE: "http://web:3000", MOKAAIR_VIDEO_TOKEN: "mkv_token" }, home: dir, fetch });
  assert.deepEqual(await client.project(SLUG), { slug: SLUG, reviews: [] });
  await client.download(SLUG, "a".repeat(64), path.join(dir, "part"));
  assert.equal(readFileSync(path.join(dir, "part"), "utf8"), "clip bytes");
  await assert.rejects(client.download(SLUG, "f".repeat(64), path.join(dir, "gone")), (error) => error.status === 404 && error.code === "video_review_file_not_found");
  assert.deepEqual(asked.slice(0, 2), [
    [`http://web:3000/api/video/reviews/${SLUG}`, "Bearer mkv_token", "application/json"],
    [`http://web:3000/api/video/reviews/${SLUG}/files/${"a".repeat(64)}`, "Bearer mkv_token", "*/*"],
  ]);
});
