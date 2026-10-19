// The backup round (backup.mjs) against a fake rclone that copies between real folders, and a
// fake site: what is copied, when it is copied again, and when the tidy may clear a video.
import assert from "node:assert/strict";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { backupRound, contentsOf, drivePath, MANIFEST_FILE, planFiles, prefixUnder, STATE_FILE, verdictOf } from "./backup.mjs";
import { tidyRound } from "./tidy.mjs";

const NOW = new Date("2026-10-20T03:00:00Z");
const later = (minutes) => new Date(NOW.getTime() + minutes * 60_000);

function sandbox() {
  const box = mkdtempSync(path.join(os.tmpdir(), "backup-test-"));
  const work = path.join(box, "work");
  const drive = path.join(box, "drive");
  mkdirSync(work, { recursive: true });
  mkdirSync(drive, { recursive: true });
  const conf = path.join(box, "rclone.conf");
  writeFileSync(conf, "[videobackup]\ntype = alias\n");
  return { box, work, drive, conf };
}

function put(dir, name, content = name) {
  const file = path.join(dir, ...name.split("/"));
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, content);
}

/** A video on YouTube with an upload package, and the media that never goes to Drive. */
function video(work, slug, files = {}) {
  const dir = path.join(work, slug);
  put(dir, "auto.json", JSON.stringify({ slug, status: "done", youtube_video_id: "dQw4w9WgXcQ" }));
  const defaults = {
    "upload/final.mp4": "cut",
    "upload/metadata.json": JSON.stringify({ skipped_caption_locales: {}, skipped_dub_locales: {} }),
    "upload/description.zh-TW.txt": "說明",
    "upload/captions/zh-TW.srt": "字幕",
    "upload/thumbnail.jpg": "jpg",
    "segments/s1.mp4": "never",
    "build/video.mp4": "never",
    "frames/f.png": "never",
  };
  for (const [name, content] of Object.entries({ ...defaults, ...files })) if (content !== null) put(dir, name, content);
  return dir;
}

const listing = (dir, prefix = "") => (existsSync(dir) ? readdirSync(dir, { withFileTypes: true }).flatMap((entry) => (entry.isDirectory() ? listing(path.join(dir, entry.name), `${prefix}${entry.name}/`) : [`${prefix}${entry.name}`])).sort() : []);

/** rclone over real folders: the remote "videobackup:" is `drive`. `fail` makes a command fail. */
function fakeRclone(drive, { free = 100 * 1024 ** 3, fail = {}, corrupt = false } = {}) {
  const calls = [];
  const local = (where) => (where.startsWith("videobackup:") ? path.join(drive, ...where.slice("videobackup:".length).split("/").filter(Boolean)) : where);
  const run = async (args) => {
    calls.push(args);
    const [command] = args;
    if (fail[command]) return { code: 1, stdout: "", stderr: `${command} failed: ${fail[command]}` };
    if (command === "about") return { code: 0, stdout: JSON.stringify({ total: 15 * 1024 ** 3, free }), stderr: "" };
    if (command === "copy") {
      const [, source, target] = args;
      const backupDir = local(args[args.indexOf("--backup-dir") + 1]);
      for (const relative of listing(source)) {
        const into = path.join(local(target), relative);
        if (existsSync(into) && readFileSync(into, "utf8") !== readFileSync(path.join(source, relative), "utf8")) {
          mkdirSync(path.dirname(path.join(backupDir, relative)), { recursive: true });
          cpSync(into, path.join(backupDir, relative));
        }
        mkdirSync(path.dirname(into), { recursive: true });
        cpSync(path.join(source, relative), into);
        if (corrupt) writeFileSync(into, "garbled");
      }
      return { code: 0, stdout: "", stderr: "" };
    }
    if (command === "check") {
      const [, source, target] = args;
      const bad = listing(source).filter((relative) => !existsSync(path.join(local(target), relative)) || readFileSync(path.join(local(target), relative), "utf8") !== readFileSync(path.join(source, relative), "utf8"));
      return bad.length ? { code: 1, stdout: "", stderr: `ERROR : ${bad[0]}: sizes differ\nNOTICE: ${bad.length} differences found` } : { code: 0, stdout: "", stderr: "" };
    }
    if (command === "copyto") {
      const into = local(args[2]);
      mkdirSync(path.dirname(into), { recursive: true });
      cpSync(args[1], into);
      return { code: 0, stdout: "", stderr: "" };
    }
    if (command === "deletefile") {
      rmSync(local(args[1]), { force: true });
      return { code: 0, stdout: "", stderr: "" };
    }
    return { code: 2, stdout: "", stderr: `unknown command ${command}` };
  };
  return { run, calls };
}

const target = (slug, extra = {}) => ({
  slug, youtube_video_id: "dQw4w9WgXcQ", category: "explainer", series_key: "curio", series_slug: null, episode_number: null,
  folder: `奇聞檔案局/${slug}`, shared_folder: "奇聞檔案局/_共用", tier: "basic",
  expected: { required: ["final.mp4", "metadata.json"], descriptions: [], captions: [], dubs: [] }, backup: null, ...extra,
});

/** The site's backup routes: the config the worker reads, and every report it sends. */
function fakeSite({ videos = [], enabled = true, lock = "AI/備份", prefix = "", answer = () => "done", test: probe = null } = {}) {
  const site = { reports: [], locks: [], answers: [], lock, test: probe };
  site.client = {
    config: async () => ({ enabled, path: "AI/備份", lock_path: site.lock, remote_prefix: enabled && site.lock ? prefix : null, problem: enabled ? (site.lock ? null : "no lock") : "備份尚未開啟", test: site.test, videos }),
    lock: async (body) => {
      site.locks.push(body);
      site.lock = body.lock_path;
      return {};
    },
    answer: async (id, body) => {
      site.answers.push({ id, ...body });
      site.test = null;
      return {};
    },
    report: async (slug, body) => {
      site.reports.push({ slug, ...body });
      const state = body.state === "done" ? answer(slug, body) : body.state;
      return { state, missing: state === "partial" ? ["dubs/en"] : [] };
    },
  };
  return site;
}

function ctxFor(box, { now = NOW, env = {} } = {}) {
  return { env: { VIDEO_WORKDIR: box.work, VIDEO_BACKUP_RCLONE_CONFIG: box.conf, VIDEO_BACKUP_LOCK_PATH: "AI/備份", TMPDIR: box.box, ...env }, now: () => now, root: path.join(box.box, "repo") };
}

const stateOf = (dir) => JSON.parse(readFileSync(path.join(dir, STATE_FILE), "utf8"));

test("paths: a pasted PC path and a lock read as the site reads them", () => {
  assert.equal(drivePath("G:\\我的雲端硬碟\\AI\\備份\\"), "AI/備份");
  assert.equal(drivePath("G:\\My Drive\\AI\\備份"), "AI/備份");
  assert.equal(prefixUnder("AI/備份", "AI/備份"), "");
  assert.equal(prefixUnder("AI/備份/影片", "G:\\My Drive\\AI\\備份"), "影片");
  assert.equal(prefixUnder("AI/備份二", "AI/備份"), null);
  assert.equal(prefixUnder("AI/備份", ""), null);
});

test("planFiles: the whole upload package, descriptions renamed, and the full tier's media; never segments, build or frames", () => {
  const box = sandbox();
  const dir = video(box.work, "ou-ep-1", {
    "upload/description.en.txt": "en",
    "upload/thumbnails/en.jpg": "jpg",
    "upload/thumbnail-b.jpg": "jpg",
    "upload/dubs/en.m4a": "dub",
    "clips/s1.mp4": "clip",
    "clips/manifest.json": "{}",
    "keyframes/s1.png": "png",
    "characters/a/sheet.png": "png",
    "timeline.json": "{}",
    "narration.wav": "wav",
    "audio/k1.wav": "never",
    "review/preview-0123456789abcdef.mp4": "never",
  });
  const basic = planFiles(dir, "basic").map((item) => item.path);
  assert.deepEqual(basic, [
    "captions/zh-TW.srt", "descriptions/en.txt", "descriptions/zh-TW.txt", "dubs/en.m4a", "final.mp4", "metadata.json",
    "thumbnail-b.jpg", "thumbnail.jpg", "thumbnails/en.jpg",
  ]);
  const full = planFiles(dir, "full").map((item) => item.path);
  assert.deepEqual(full.filter((item) => !basic.includes(item)), [
    "characters/a/sheet.png", "clips/manifest.json", "clips/s1.mp4", "keyframes/s1.png", "narration.wav", "timeline.json",
  ]);
  assert.ok(!full.some((item) => /^(segments|build|frames|audio|review|media)\//.test(item)));
});

test("contentsOf: what the site counts, a Short's caption beside its cut, and the parts skipped with a reason", () => {
  const contents = contentsOf(
    ["final.mp4", "metadata.json", "thumbnail.jpg", "descriptions/en.txt", "captions/en.srt", "dubs/en.m4a", "zh-TW.srt", "clips/manifest.json", "clips/a.mp4"],
    { skipped_caption_locales: { ja: "12 lines missing" }, skipped_dub_locales: { ja: "dub given up" } },
  );
  assert.deepEqual(contents, {
    final: true, metadata: true, thumbnail: true, descriptions: ["en"], captions: ["en", "zh-TW"], dubs: ["en"],
    skipped: { descriptions: [], captions: ["ja"], dubs: ["ja"] }, clips: 1, keyframes: 0,
  });
});

test("a round copies the package into the series folder, checks it, uploads backup.json last and reports done", async () => {
  const box = sandbox();
  const dir = video(box.work, "curio-h01");
  const site = fakeSite({ videos: [target("curio-h01")] });
  const rclone = fakeRclone(box.drive);
  const { lines, gate } = await backupRound(ctxFor(box), { client: site.client, rclone: rclone.run });
  const episode = path.join(box.drive, "奇聞檔案局", "curio-h01");
  assert.deepEqual(listing(episode), ["backup.json", "captions/zh-TW.srt", "descriptions/zh-TW.txt", "final.mp4", "metadata.json", "thumbnail.jpg"]);
  assert.deepEqual(rclone.calls.map(([command]) => command), ["about", "copy", "check", "copyto"], "backup.json only after the check");
  const copy = rclone.calls.find(([command]) => command === "copy");
  assert.ok(copy.includes("--checksum") && copy.includes(`videobackup:奇聞檔案局/curio-h01/_舊版/20261020T030000Z`));
  assert.ok(!rclone.calls.some(([command]) => command === "sync" || command === "delete" || command === "purge"), "never deletes in Drive");
  const [queued, done] = site.reports;
  assert.equal(queued.state, "pending");
  assert.equal(done.state, "done");
  assert.equal(done.files, 5);
  assert.match(done.files_hash, /^[0-9a-f]{64}$/);
  assert.deepEqual(done.contents.captions, ["zh-TW"]);
  const manifest = JSON.parse(readFileSync(path.join(episode, MANIFEST_FILE), "utf8"));
  assert.equal(manifest.files_hash, done.files_hash);
  assert.equal(stateOf(dir).site_state, "done");
  assert.deepEqual(gate.verdicts.get("curio-h01"), { ok: true, why: "in Drive" });
  assert.ok(!existsSync(path.join(box.work, "_backup-stage", "curio-h01")), "the staging folder goes");
  assert.match(lines.at(-1), /curio-h01: 5 files/);
});

test("a file added after the backup queues it again, copies only that, and keeps the overwritten version", async () => {
  const box = sandbox();
  const dir = video(box.work, "curio-h02");
  const site = fakeSite({ videos: [target("curio-h02")] });
  await backupRound(ctxFor(box), { client: site.client, rclone: fakeRclone(box.drive).run });
  put(dir, "upload/dubs/en.m4a", "dub");
  put(dir, "upload/description.zh-TW.txt", "說明，改過");
  const quiet = await backupRound(ctxFor(box, { env: { VIDEO_BACKUP_PER_ROUND: "0" } }), { client: site.client, rclone: fakeRclone(box.drive).run });
  assert.equal(quiet.gate.verdicts.get("curio-h02").ok, false, "the tidy waits while new files are not in Drive");
  assert.equal(stateOf(dir).state, "pending");
  const again = await backupRound(ctxFor(box, { now: later(10) }), { client: site.client, rclone: fakeRclone(box.drive).run });
  const episode = path.join(box.drive, "奇聞檔案局", "curio-h02");
  assert.ok(listing(episode).includes("dubs/en.m4a"));
  assert.equal(readFileSync(path.join(episode, "descriptions", "zh-TW.txt"), "utf8"), "說明，改過");
  assert.equal(readFileSync(path.join(episode, "_舊版", "20261020T031000Z", "descriptions", "zh-TW.txt"), "utf8"), "說明");
  assert.ok(again.gate.verdicts.get("curio-h02").ok);
  assert.deepEqual(site.reports.at(-1).contents.dubs, ["en"]);
});

test("nothing changed: a done video is not copied again", async () => {
  const box = sandbox();
  video(box.work, "curio-h03");
  const site = fakeSite({ videos: [target("curio-h03")] });
  await backupRound(ctxFor(box), { client: site.client, rclone: fakeRclone(box.drive).run });
  const rclone = fakeRclone(box.drive);
  const { gate } = await backupRound(ctxFor(box, { now: later(5) }), { client: site.client, rclone: rclone.run });
  assert.deepEqual(rclone.calls, []);
  assert.ok(gate.verdicts.get("curio-h03").ok);
});

test("a check that finds Drive's copy different never reports done; three in a row is failed, tried again in six hours", async () => {
  const box = sandbox();
  const dir = video(box.work, "curio-h04");
  const site = fakeSite({ videos: [target("curio-h04")] });
  for (const minutes of [0, 5, 10]) {
    const { gate } = await backupRound(ctxFor(box, { now: later(minutes) }), { client: site.client, rclone: fakeRclone(box.drive, { corrupt: true }).run });
    assert.equal(gate.verdicts.get("curio-h04").ok, false);
  }
  assert.equal(stateOf(dir).state, "failed");
  assert.equal(stateOf(dir).attempts, 3);
  assert.match(stateOf(dir).error, /^rclone check: .*differences found/);
  assert.ok(!site.reports.some((report) => report.state === "done"));
  assert.ok(!existsSync(path.join(box.drive, "奇聞檔案局", "curio-h04", MANIFEST_FILE)), "no backup.json for a backup that did not check");
  const soon = fakeRclone(box.drive);
  await backupRound(ctxFor(box, { now: later(60) }), { client: site.client, rclone: soon.run });
  assert.deepEqual(soon.calls, [], "a failed video waits six hours");
  await backupRound(ctxFor(box, { now: later(10 + 6 * 60) }), { client: site.client, rclone: fakeRclone(box.drive).run });
  assert.equal(stateOf(dir).state, "done");
});

test("not enough space: nothing is copied, the video waits and the site hears the free space", async () => {
  const box = sandbox();
  const dir = video(box.work, "curio-h05");
  const site = fakeSite({ videos: [target("curio-h05")] });
  const rclone = fakeRclone(box.drive, { free: 1024 ** 3 });
  const { gate } = await backupRound(ctxFor(box), { client: site.client, rclone: rclone.run });
  assert.deepEqual(rclone.calls.map(([command]) => command), ["about"]);
  assert.equal(stateOf(dir).state, "blocked_quota");
  assert.equal(site.reports.at(-1).free_bytes, 1024 ** 3);
  assert.match(gate.verdicts.get("curio-h05").why, /Drive space/);
});

test("the site answers partial: the tidy keeps the files and says what is missing", async () => {
  const box = sandbox();
  video(box.work, "curio-h06");
  const site = fakeSite({ videos: [target("curio-h06")], answer: () => "partial" });
  const { gate, lines } = await backupRound(ctxFor(box), { client: site.client, rclone: fakeRclone(box.drive).run });
  assert.deepEqual(gate.verdicts.get("curio-h06"), { ok: false, why: "backup partial: missing dubs/en" });
  assert.match(lines.at(-1), /the site reads it partial, missing dubs\/en; the tidy keeps its files/);
});

test("a done the site did not hear is sent again; until then the tidy waits", async () => {
  const box = sandbox();
  const dir = video(box.work, "curio-h07");
  const site = fakeSite({ videos: [target("curio-h07")] });
  const report = site.client.report;
  site.client.report = async (slug, body) => {
    if (body.state === "done") throw new Error("connect ECONNREFUSED");
    return report(slug, body);
  };
  const first = await backupRound(ctxFor(box), { client: site.client, rclone: fakeRclone(box.drive).run });
  assert.equal(first.gate.verdicts.get("curio-h07").ok, false);
  assert.equal(stateOf(dir).state, "done");
  site.client.report = report;
  const rclone = fakeRclone(box.drive);
  const second = await backupRound(ctxFor(box, { now: later(5) }), { client: site.client, rclone: rclone.run });
  assert.deepEqual(rclone.calls, [], "only the report is sent again");
  assert.ok(second.gate.verdicts.get("curio-h07").ok);
});

test("a video tidied before backups existed: what is left is copied, and the site decides it is partial", async () => {
  const box = sandbox();
  video(box.work, "old-video", { "upload/final.mp4": null });
  const site = fakeSite({ videos: [target("old-video")], answer: (_slug, body) => (body.contents.final ? "done" : "partial") });
  await backupRound(ctxFor(box), { client: site.client, rclone: fakeRclone(box.drive).run });
  const done = site.reports.find((report) => report.state === "done");
  assert.equal(done.contents.final, false);
  assert.ok(listing(path.join(box.drive, "奇聞檔案局", "old-video")).includes("metadata.json"));
});

test("a round copies at most VIDEO_BACKUP_PER_ROUND videos, oldest first, and holds the rest", async () => {
  const box = sandbox();
  for (const slug of ["a-one", "b-two", "c-three"]) video(box.work, slug);
  const site = fakeSite({ videos: ["a-one", "b-two", "c-three"].map((slug) => target(slug, { folder: `其他/${slug}` })) });
  const { gate } = await backupRound(ctxFor(box), { client: site.client, rclone: fakeRclone(box.drive).run });
  assert.deepEqual([...gate.verdicts].map(([slug, verdict]) => [slug, verdict.ok]), [["a-one", true], ["b-two", true], ["c-three", false]]);
});

test("the full tier copies the media and the series' shared character sheets once", async () => {
  const box = sandbox();
  video(box.work, "ou-ep-1", { "clips/s1.mp4": "clip", "keyframes/s1.png": "png" });
  put(path.join(box.work, "_series", "ou-de-jianghu"), "characters/hero/sheet.png", "sheet");
  const site = fakeSite({ videos: [target("ou-ep-1", { tier: "full", series_slug: "ou-de-jianghu", folder: "偶的江湖/001-ou-ep-1", shared_folder: "偶的江湖/_共用" })] });
  await backupRound(ctxFor(box), { client: site.client, rclone: fakeRclone(box.drive).run });
  assert.ok(listing(path.join(box.drive, "偶的江湖", "001-ou-ep-1")).includes("clips/s1.mp4"));
  assert.deepEqual(listing(path.join(box.drive, "偶的江湖", "_共用")), ["characters/hero/sheet.png"]);
  assert.equal(site.reports.at(-1).contents.clips, 1);
});

test("a series set to off is never copied and never holds the tidy", async () => {
  const box = sandbox();
  video(box.work, "curio-off");
  const site = fakeSite({ videos: [target("curio-off", { tier: "off" })] });
  const rclone = fakeRclone(box.drive);
  const { gate } = await backupRound(ctxFor(box), { client: site.client, rclone: rclone.run });
  assert.deepEqual(rclone.calls, []);
  assert.ok(gate.verdicts.get("curio-off").ok);
});

test("off, an older site and a STOP file: nothing copied; off and an older site leave the tidy as before", async () => {
  const box = sandbox();
  video(box.work, "curio-h08");
  const off = await backupRound(ctxFor(box), { client: fakeSite({ enabled: false, videos: [target("curio-h08")] }).client, rclone: fakeRclone(box.drive).run });
  assert.deepEqual(off.gate, { enabled: false });
  const older = { config: async () => Promise.reject(Object.assign(new (await import("./backup.mjs")).BackupError("not found", { status: 404, code: "not_found" }))) };
  assert.deepEqual((await backupRound(ctxFor(box), { client: older })).gate, { enabled: false });
  const down = { config: async () => Promise.reject(new Error("connect ECONNREFUSED")) };
  assert.ok((await backupRound(ctxFor(box), { client: down })).gate.unknown, "a site that cannot answer holds the tidy");
  put(box.work, "STOP", "");
  assert.ok((await backupRound(ctxFor(box), { client: down })).gate.unknown);
  assert.equal(listing(box.drive).length, 0);
});

test("a host without the rclone file says so to the site, and backups that are on hold the tidy", async () => {
  const box = sandbox();
  video(box.work, "curio-h09");
  const site = fakeSite({ videos: [target("curio-h09")] });
  const { gate, lines } = await backupRound(ctxFor(box, { env: { VIDEO_BACKUP_RCLONE_CONFIG: path.join(box.box, "missing.conf") } }), { client: site.client });
  assert.equal(site.locks[0].lock_path, null);
  assert.match(site.locks[0].problem, /rclone/);
  assert.ok(gate.unknown);
  assert.match(lines.at(-1), /not copying/);
});

test("the owner's test: a probe file written and deleted in the configured folder, with the free space", async () => {
  const box = sandbox();
  const site = fakeSite({ test: { id: "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b", requested_at: NOW.toISOString() } });
  const rclone = fakeRclone(box.drive);
  await backupRound(ctxFor(box, { env: { VIDEO_BACKUP_LOCK_PATH: "G:\\我的雲端硬碟\\AI\\備份" } }), { client: site.client, rclone: rclone.run });
  const [answer] = site.answers;
  assert.equal(answer.ok, true);
  assert.match(answer.message, /AI\/備份/);
  assert.equal(answer.free_bytes, 100 * 1024 ** 3);
  assert.deepEqual(rclone.calls.map(([command]) => command).slice(0, 2), ["copyto", "deletefile"]);
  assert.equal(listing(box.drive).length, 0, "the probe file is gone");
  assert.deepEqual(site.locks, [], "the lock the site already has is not sent again");
});

test("verdictOf: only a done the site confirmed lets the tidy clear", () => {
  assert.equal(verdictOf({ state: "done", site_state: "done" }).ok, true);
  for (const state of [{ state: "done" }, { state: "done", site_state: "partial" }, { state: "pending" }, { state: "failed", error: "x" }, { state: "blocked_quota" }, null]) {
    assert.equal(verdictOf(state).ok, false, JSON.stringify(state));
  }
});

test("the tidy keeps a video on YouTube that Drive does not have, and clears it once Drive does", () => {
  const box = sandbox();
  const dir = video(box.work, "on-youtube");
  put(dir, "final.mp4", "big");
  put(dir, "approvals.json", JSON.stringify({ approvals: [{ gate: "publish", approved_at: "2026-10-01T00:00:00Z" }] }));
  const site = [{ slug: "on-youtube", youtube_video_id: "dQw4w9WgXcQ", publish_approved_at: "2026-10-01T00:00:00Z", youtube_publish_at: null, locales: {}, locales_decided_at: "2026-10-01T00:00:00Z", languages: {}, pending: 0 }];
  const repos = [path.join(box.box, "repo")];
  const round = (backup) => tidyRound({ base: box.work, repos, site, backup, now: NOW, days: 7, dryRun: true });
  const held = round({ enabled: true, verdicts: new Map([["on-youtube", { ok: false, why: "backup pending" }]]) });
  assert.deepEqual(held.held, [{ slug: "on-youtube", why: "not in Google Drive yet: backup pending" }]);
  assert.equal(held.cleared, null);
  assert.match(round({ unknown: "the site did not answer" }).held[0].why, /unknown/);
  assert.match(round({ enabled: true, verdicts: new Map() }).held[0].why, /no entry/);
  assert.equal(round({ enabled: true, verdicts: new Map([["on-youtube", { ok: true, why: "in Drive" }]]) }).cleared.slug, "on-youtube");
  assert.equal(round({ enabled: false }).cleared.slug, "on-youtube", "backups off: as before");
  assert.equal(round(undefined).cleared.slug, "on-youtube");
});
