// Restoring a video the host cleared (restore.mjs): backed up, purged, brought back byte for byte,
// and kept by the tidy while the late work is done.
import assert from "node:assert/strict";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { backupRound } from "./backup.mjs";
import { restoreVideo, workPathOf } from "./restore.mjs";
import { roundLines, tidyRound } from "./tidy.mjs";

const NOW = new Date("2026-11-03T03:00:00Z");
const YOUTUBE = "dQw4w9WgXcQ";

const listing = (dir, prefix = "") => (existsSync(dir) ? readdirSync(dir, { withFileTypes: true }).flatMap((entry) => (entry.isDirectory() ? listing(path.join(dir, entry.name), `${prefix}${entry.name}/`) : [`${prefix}${entry.name}`])).sort() : []);

function put(dir, name, content) {
  const file = path.join(dir, ...name.split("/"));
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, content);
}

/** rclone between real folders, both ways; `videobackup:` is the drive folder. */
function fakeRclone(drive) {
  const calls = [];
  const local = (where) => (where.startsWith("videobackup:") ? path.join(drive, ...where.slice("videobackup:".length).split("/").filter(Boolean)) : where);
  const excluded = (args) => args.flatMap((arg, index) => (args[index - 1] === "--exclude" ? [arg] : []));
  const skip = (relative, args) => excluded(args).some((pattern) => (pattern.endsWith("/**") ? `/${relative}`.startsWith(pattern.slice(0, -2)) : `/${relative}` === pattern));
  const run = async (args) => {
    calls.push(args);
    const [command, from, to] = args;
    if (command === "about") return { code: 0, stdout: JSON.stringify({ total: 15 * 1024 ** 3, free: 10 * 1024 ** 3 }), stderr: "" };
    if (command === "copy") {
      for (const relative of listing(local(from))) {
        if (skip(relative, args)) continue;
        mkdirSync(path.dirname(path.join(local(to), relative)), { recursive: true });
        cpSync(path.join(local(from), relative), path.join(local(to), relative));
      }
      return { code: 0, stdout: "", stderr: "" };
    }
    if (command === "check") return { code: 0, stdout: "", stderr: "" };
    if (command === "copyto") {
      if (!existsSync(local(from))) return { code: 3, stdout: "", stderr: "ERROR : object not found" };
      mkdirSync(path.dirname(local(to)), { recursive: true });
      cpSync(local(from), local(to));
      return { code: 0, stdout: "", stderr: "" };
    }
    return { code: 2, stdout: "", stderr: `unknown command ${command}` };
  };
  return { run, calls };
}

function siteWith(videos) {
  return {
    config: async () => ({ enabled: true, path: "AI/備份", lock_path: "AI/備份", remote_prefix: "", problem: null, test: null, videos }),
    lock: async () => ({}),
    report: async (_slug, body) => ({ state: body.state, missing: [] }),
  };
}

test("workPathOf puts each file of a backup back where planFiles took it from", () => {
  assert.equal(workPathOf("final.mp4"), "upload/final.mp4");
  assert.equal(workPathOf("captions/en.srt"), "upload/captions/en.srt");
  assert.equal(workPathOf("dubs/en.m4a"), "upload/dubs/en.m4a");
  assert.equal(workPathOf("descriptions/zh-TW.txt"), "upload/description.zh-TW.txt");
  assert.equal(workPathOf("thumbnails/ja.jpg"), "upload/thumbnails/ja.jpg");
  assert.equal(workPathOf("dubs/未進上傳包/ja.m4a"), "dubs/ja.m4a");
  assert.equal(workPathOf("captions/未進上傳包/ja.srt"), "captions/ja.srt");
  assert.equal(workPathOf("dub-lines/en/l1.wav"), "dubs/en/audio/l1.wav");
  for (const same of ["keyframes/k.png", "clips/s1.mp4", "audio/l1.wav", "i18n/en.json", "recordings/zh-TW.wav", "timeline.json", "narration.wav", "approvals.json", "languages.json"]) assert.equal(workPathOf(same), same);
  for (const never of ["backup.json", "_舊版/20261101T000000Z/final.mp4", "../escape", "a/../b", "/abs", ""]) assert.equal(workPathOf(never), null, never);
});

test("a purged video comes back from Drive byte for byte, and the tidy keeps it while the late work is done", async () => {
  const box = mkdtempSync(path.join(os.tmpdir(), "restore-test-"));
  const work = path.join(box, "work");
  const drive = path.join(box, "drive");
  mkdirSync(drive, { recursive: true });
  const conf = path.join(box, "rclone.conf");
  writeFileSync(conf, "[videobackup]\ntype = alias\n");
  const dir = path.join(work, "curio-b01");
  const files = {
    "auto.json": JSON.stringify({ slug: "curio-b01", status: "done", youtube_video_id: YOUTUBE }),
    "upload/final.mp4": "the cut",
    "upload/metadata.json": JSON.stringify({ skipped_caption_locales: {}, skipped_dub_locales: {} }),
    "upload/description.zh-TW.txt": "說明",
    "upload/captions/zh-TW.srt": "字幕",
    "upload/dubs/en.m4a": "english dub",
    "upload/thumbnail.jpg": "jpg",
    "keyframes/ch1-open.jpg": "keyframe",
    "audio/l1.wav": "line take",
    "dubs/en/audio/l1.wav": "english line take",
    "narration.wav": "narration",
    "timeline.json": "{}",
    "approvals.json": "{}",
  };
  for (const [name, content] of Object.entries(files)) put(dir, name, content);
  const ctx = { env: { VIDEO_WORKDIR: work, VIDEO_BACKUP_RCLONE_CONFIG: conf, VIDEO_BACKUP_LOCK_PATH: "AI/備份", TMPDIR: box }, now: () => NOW, root: path.join(box, "repo") };
  const target = { slug: "curio-b01", youtube_video_id: YOUTUBE, category: "explainer", series_key: "curio", series_slug: null, episode_number: null, folder: "奇聞檔案局/curio-b01", shared_folder: "奇聞檔案局/_共用", tier: "full", expected: { required: ["final.mp4", "metadata.json"], descriptions: [], captions: [], dubs: [] }, backup: null };
  const rclone = fakeRclone(drive);
  const { gate } = await backupRound(ctx, { client: siteWith([target]), rclone: rclone.run });
  assert.deepEqual(gate.verdicts.get("curio-b01"), { ok: true, why: "in Drive" });

  // Purged: only the records stay.
  const row = { slug: "curio-b01", youtube_video_id: YOUTUBE, publish_approved_at: NOW.toISOString(), youtube_publish_at: null, locales: {}, locales_decided_at: NOW.toISOString(), languages: {}, pending: 0 };
  const repos = [path.join(box, "repo")];
  assert.equal(tidyRound({ base: work, repos, site: [row], backup: gate, now: NOW }).cleared.slug, "curio-b01");
  assert.deepEqual(listing(dir), ["auto.json", "backup-state.json", "backup.json"]);

  const restoreCtx = { ...ctx, backupClient: siteWith([target]), backupRclone: rclone.run };
  const dry = await restoreVideo(restoreCtx, { slug: "curio-b01", base: work, dryRun: true });
  assert.match(dry.lines[0], /^restore --dry-run: curio-b01: 12 files/);
  assert.deepEqual(listing(dir), ["auto.json", "backup-state.json", "backup.json"], "a dry run places nothing");

  const done = await restoreVideo(restoreCtx, { slug: "curio-b01", base: work });
  assert.equal(done.ok, true, done.lines.join("\n"));
  assert.match(done.lines[0], /12 file\(s\) back from Drive/);
  for (const [name, content] of Object.entries(files)) {
    if (name === "auto.json") continue;
    assert.equal(readFileSync(path.join(dir, ...name.split("/")), "utf8"), content, name);
  }
  assert.equal(readFileSync(path.join(dir, "final.mp4"), "utf8"), "the cut", "the worker's own cut at the root again");
  assert.ok(!existsSync(path.join(work, "_restore-stage", "curio-b01")), "the staging folder goes");
  const state = JSON.parse(readFileSync(path.join(dir, "auto.json"), "utf8"));
  assert.equal(state.restored_at, NOW.toISOString());
  assert.ok(!state.tidied_at && !state.tidied, "the stages see a video with its files again");

  // Kept for the late work, then cleared again the usual way.
  const held = tidyRound({ base: work, repos, site: [row], backup: gate, now: NOW, dryRun: true });
  assert.equal(held.cleared, null);
  assert.match(roundLines(held, { verbose: true }).join("\n"), /restored from Google Drive on 2026-11-03 for late work; kept 14 days/);
  const later = new Date(NOW.getTime() + 15 * 86_400_000);
  assert.equal(tidyRound({ base: work, repos, site: [row], backup: gate, now: later, dryRun: true }).cleared.slug, "curio-b01");
});

test("a file Drive no longer holds as backup.json says is not placed, and the restore says so", async () => {
  const box = mkdtempSync(path.join(os.tmpdir(), "restore-test-"));
  const work = path.join(box, "work");
  const drive = path.join(box, "drive");
  const folder = path.join(drive, "奇聞檔案局", "curio-b02");
  put(folder, "final.mp4", "changed in Drive");
  put(folder, "metadata.json", "{}");
  const sha = (text) => (import("node:crypto").then(({ createHash }) => createHash("sha256").update(text).digest("hex")));
  put(folder, "backup.json", JSON.stringify({ slug: "curio-b02", folder: "奇聞檔案局/curio-b02", files: [
    { path: "final.mp4", size: 7, sha256: await sha("the cut") },
    { path: "metadata.json", size: 2, sha256: await sha("{}") },
  ] }));
  mkdirSync(path.join(work, "curio-b02"), { recursive: true });
  const ctx = { env: { VIDEO_WORKDIR: work }, now: () => NOW, backupClient: siteWith([{ slug: "curio-b02", folder: "奇聞檔案局/curio-b02" }]), backupRclone: fakeRclone(drive).run };
  const result = await restoreVideo(ctx, { slug: "curio-b02", base: work });
  assert.equal(result.ok, false);
  assert.match(result.lines.join("\n"), /1 file\(s\) did not match backup\.json and were not placed: final\.mp4/);
  assert.ok(!existsSync(path.join(work, "curio-b02", "upload", "final.mp4")));
  assert.equal(readFileSync(path.join(work, "curio-b02", "upload", "metadata.json"), "utf8"), "{}");
  assert.deepEqual(JSON.parse(readFileSync(path.join(work, "curio-b02", "tidied.json"), "utf8")), { restored_at: NOW.toISOString() });
  const refused = await restoreVideo(ctx, { slug: "../etc", base: work });
  assert.equal(refused.ok, false);
});
