import assert from "node:assert/strict";
import { existsSync, linkSync, lstatSync, mkdirSync, mkdtempSync, readFileSync, realpathSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { ROOT } from "../core/paths.mjs";
import { STATE_FILE as FLOW_STATE_FILE } from "./flow.mjs";
import { DEFAULT_DAYS, PREVIEW, retentionFrom, STATE_FILE, TARGETS, targetRefusal, tidiedNote, tidyBase, tidyRound } from "./tidy.mjs";

const NOW = new Date("2026-10-20T12:00:00Z");
const daysAgo = (days) => new Date(NOW.getTime() - days * 86_400_000).toISOString();
const YOUTUBE = "dQw4w9WgXcQ";

// What the stages leave in a finished video's work directory. MEDIA is what the tidy removes,
// with each file's size; RECORDS is what it keeps.
const MEDIA = {
  "final.mp4": 1000,
  "upload/final.mp4": 1000,
  "upload/dubs/en.m4a": 100,
  "segments/s1-0a1b.mp4": 200,
  "segments/s1.ffconcat": 10,
  "build/video.mp4": 300,
  "build/audio.m4a": 50,
  "audio/k7p2.wav": 400,
  "audio/cache.json": 20,
  "narration.wav": 400,
  "frames/0a1b.png": 60,
  "frames/manifest.json": 30,
  "keyframes/s1.png": 70,
  "keyframes/manifest.json": 30,
  "clips/s1.mp4": 80,
  "clips/manifest.json": 30,
  "review/preview-0123456789abcdef.mp4": 500,
  "review/narration-0123456789abcdef.m4a": 90,
  "dubs/en/audio/k7p2.wav": 40,
  "dubs/en/narration.wav": 40,
  "dubs/en.m4a": 40,
};
const MEDIA_BYTES = Object.values(MEDIA).reduce((sum, size) => sum + size, 0);
const RECORDS = [
  "state.json",
  "checks.json",
  "timeline.json",
  "languages.json",
  "captions/zh-TW.srt",
  "captions/manifest.json",
  "i18n/en.todo.json",
  "media/ledger.json",
  "media/cache.json",
  "media/jobs.json",
  "answers/writer-2026-10-01.txt",
  "review/qa.json",
  "review/check.json",
  "review/final.html",
  "review/rewrites.json",
  "upload/metadata.json",
  "upload/UPLOAD.md",
  "upload/description.zh-TW.txt",
  "upload/captions/zh-TW.srt",
  "upload/thumbnail.jpg",
  "characters/manifest.json",
  "characters/hero-1.png",
  "music/manifest.json",
  "music/track.mp3",
  "thumbnail.jpg",
  "contact-sheet.png",
  "dubs/manifest.json",
  "dubs/en/timeline.json",
  "compile/manifest.json",
];

function put(dir, name, content) {
  const file = path.join(dir, ...name.split("/"));
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, content);
  return file;
}

/** A throwaway work base beside a throwaway repository, under the system's temporary directory. */
function place() {
  const top = realpathSync(mkdtempSync(path.join(tmpdir(), "video-tidy-")));
  const repo = path.join(top, "repo");
  const work = path.join(top, "work");
  mkdirSync(repo);
  mkdirSync(work);
  return { top, repo, work, repos: [repo, ROOT] };
}

/** A video the worker finished: the stages' media, the records, its approvals and auto.json. */
function finishedVideo(work, slug, { state = {}, published = daysAgo(8), media = MEDIA } = {}) {
  const dir = path.join(work, slug);
  for (const [name, size] of Object.entries(media)) put(dir, name, Buffer.alloc(size, 7));
  for (const name of RECORDS) put(dir, name, `${slug} ${name}\n`);
  const approvals = [{ gate: "final", file: "final.mp4", sha256: "a".repeat(64), approved_at: daysAgo(12), note: "" }];
  if (published) approvals.push({ gate: "publish", file: "metadata.json", sha256: "b".repeat(64), approved_at: published, note: "approved on /admin/videos" });
  put(dir, "approvals.json", `${JSON.stringify({ approvals }, null, 2)}\n`);
  put(dir, STATE_FILE, `${JSON.stringify({ slug, title: slug, status: "done", created_at: daysAgo(20), youtube_video_id: YOUTUBE, notes: [], ...state }, null, 2)}\n`);
  return dir;
}

/** The video as the site's list carries it (ProjectSummary), on YouTube with its languages settled. */
const listing = (slug, extra = {}) => ({ slug, youtube_video_id: YOUTUBE, publish_approved_at: daysAgo(8), youtube_publish_at: null, dropped_at: null, locales_decided_at: daysAgo(10), languages: {}, ...extra });

const exists = (dir, name) => existsSync(path.join(dir, ...name.split("/")));
const autoJson = (dir) => JSON.parse(readFileSync(path.join(dir, STATE_FILE), "utf8"));
const round = (where, extra = {}) => tidyRound({ base: where.work, repos: where.repos, now: NOW, days: DEFAULT_DAYS, ...extra });

function assertUntouched(dir) {
  for (const name of Object.keys(MEDIA)) assert.ok(exists(dir, name), `${name} is still there`);
  assert.equal(autoJson(dir).tidied_at, undefined);
}

test("the tidy reads the same auto.json the flow writes, and keeps the site's seven days", () => {
  assert.equal(STATE_FILE, FLOW_STATE_FILE);
  assert.equal(DEFAULT_DAYS, 7, "apps/api/app/video_reviews/admin_service.py PREVIEW_RETENTION");
  assert.deepEqual(retentionFrom({}), { days: 7 });
  assert.deepEqual(retentionFrom({ VIDEO_TIDY_DAYS: " 14 " }), { days: 14 });
  assert.deepEqual(retentionFrom({ VIDEO_TIDY_DAYS: "OFF" }), { off: true });
  for (const value of ["0", "-3", "7d", "1.5", "99999"]) assert.match(retentionFrom({ VIDEO_TIDY_DAYS: value }).problem, /VIDEO_TIDY_DAYS/);
  // Every target is a name inside the video's folder, never an absolute path, a parent or a shared "_" folder.
  for (const target of TARGETS) {
    assert.ok(!path.isAbsolute(target) && !target.split(path.sep).includes("..") && !target.startsWith("_"), target);
  }
  assert.ok(PREVIEW.test("preview-0123456789abcdef.mp4") && PREVIEW.test("narration-0123456789abcdef.m4a"));
  assert.ok(!PREVIEW.test("qa.json") && !PREVIEW.test("preview-0123456789abcdef.mp4.json") && !PREVIEW.test("languages.json"));
});

test("a video on YouTube past the retention loses its media and keeps its records", () => {
  const where = place();
  const dir = finishedVideo(where.work, "on-youtube-old");
  const result = round(where, { site: [listing("on-youtube-old")] });
  assert.equal(result.cleared.slug, "on-youtube-old");
  for (const name of Object.keys(MEDIA)) assert.ok(!exists(dir, name), `${name} is removed`);
  for (const name of ["segments", "build", "audio", "frames", "keyframes", "clips", "upload/dubs", "dubs/en/audio"]) assert.ok(!exists(dir, name), `${name}/ is removed`);
  for (const name of RECORDS) assert.equal(readFileSync(path.join(dir, ...name.split("/")), "utf8"), `on-youtube-old ${name}\n`, `${name} stays as it was`);
  assert.ok(exists(dir, "approvals.json"));
  assert.equal(result.cleared.bytes, MEDIA_BYTES);
  const state = autoJson(dir);
  assert.equal(state.tidied_at, NOW.toISOString());
  assert.equal(state.status, "done", "the rest of auto.json is as it was");
  assert.equal(state.youtube_video_id, YOUTUBE);
  assert.equal(state.tidied.bytes, MEDIA_BYTES);
  assert.ok(state.tidied.removed.includes("final.mp4") && state.tidied.removed.includes("segments") && state.tidied.removed.includes("review/preview-0123456789abcdef.mp4"));
  assert.deepEqual(state.tidied.failed, []);
});

test("the line names the video, what was removed and the bytes freed", async () => {
  const where = place();
  finishedVideo(where.work, "named-line");
  const { roundLines } = await import("./tidy.mjs");
  const lines = roundLines(round(where, { site: [listing("named-line")] }));
  assert.equal(lines.length, 1);
  assert.match(lines[0], /^tidy: named-line \(on YouTube, counted from 2026-10-12\): removed final\.mp4, upload\/final\.mp4, upload\/dubs\/ \(1 file\), segments\/ \(2 files\)/);
  assert.match(lines[0], /review\/preview-0123456789abcdef\.mp4/);
  assert.match(lines[0], new RegExp(`; 4 KB \\(${MEDIA_BYTES} bytes\\) freed$`));
});

test("a video on YouTube within the retention keeps everything; the publish time counts as on the site", () => {
  const where = place();
  const recent = finishedVideo(where.work, "on-youtube-recent", { published: daysAgo(3) });
  const scheduled = finishedVideo(where.work, "scheduled-late", { published: daysAgo(12) });
  const result = round(where, { site: [listing("on-youtube-recent", { publish_approved_at: daysAgo(3) }), listing("scheduled-late", { publish_approved_at: daysAgo(12), youtube_publish_at: daysAgo(2) })] });
  assert.equal(result.cleared, null);
  assertUntouched(recent);
  assertUntouched(scheduled);
  assert.deepEqual(result.waiting.map((video) => video.slug), ["on-youtube-recent", "scheduled-late"]);
  // Public for eight days: the later of the confirmation and the publish time is past the seven.
  const later = round(where, { site: [listing("scheduled-late", { publish_approved_at: daysAgo(12), youtube_publish_at: daysAgo(8) })] });
  assert.equal(later.cleared.slug, "scheduled-late");
  assertUntouched(recent);
});

test("a video being made, blocked or waiting for the owner's upload keeps everything however old", () => {
  const where = place();
  const made = finishedVideo(where.work, "being-made", { published: daysAgo(90), state: { status: "active", created_at: daysAgo(120), youtube_video_id: undefined } });
  const blocked = finishedVideo(where.work, "blocked-long", { published: daysAgo(90), state: { status: "blocked", blocked: "tts failed", youtube_video_id: undefined } });
  const waiting = finishedVideo(where.work, "confirmed-not-uploaded", { published: daysAgo(90), state: { youtube_video_id: undefined } });
  const result = round(where, { site: ["being-made", "blocked-long", "confirmed-not-uploaded"].map((slug) => listing(slug, { youtube_video_id: null, publish_approved_at: daysAgo(90) })) });
  assert.equal(result.cleared, null);
  assert.deepEqual([result.due, result.waiting, result.held, result.undated].map((list) => list.length), [0, 0, 0, 0], "none of them is finished");
  for (const dir of [made, blocked, waiting]) assertUntouched(dir);
});

test("a dropped video goes the same way after the retention; without a date it stays and the round says so", async () => {
  const where = place();
  const old = finishedVideo(where.work, "dropped-old", { published: null, state: { status: "dropped", youtube_video_id: undefined, dropped: { at: daysAgo(9), note: "wrong topic" } } });
  const recent = finishedVideo(where.work, "dropped-recent", { published: null, state: { status: "dropped", youtube_video_id: undefined, dropped: { at: daysAgo(2), note: "" } } });
  const undated = finishedVideo(where.work, "dropped-undated", { published: null, state: { status: "dropped", youtube_video_id: undefined, dropped: { note: "" } } });
  const result = round(where, { site: [] });
  assert.equal(result.cleared.slug, "dropped-old");
  assert.equal(result.cleared.how, "dropped");
  assert.ok(!exists(old, "final.mp4"));
  assertUntouched(recent);
  assertUntouched(undated);
  const { roundLines } = await import("./tidy.mjs");
  assert.match(roundLines(result).at(-1), /^tidy: finished but kept, no usable date: dropped-undated \(dropped, but auto\.json has no date in dropped\.at\)$/);
});

test("a video on YouTube with no date for its upload confirmation stays, and the round says so", async () => {
  const where = place();
  const dir = finishedVideo(where.work, "no-confirmation", { published: null });
  const result = round(where, { site: [listing("no-confirmation", { publish_approved_at: null })] });
  assert.equal(result.cleared, null);
  assertUntouched(dir);
  assert.deepEqual(result.undated.map((entry) => entry.slug), ["no-confirmation"]);
  const { roundLines } = await import("./tidy.mjs");
  assert.match(roundLines(result)[0], /no-confirmation \(on YouTube, but its upload confirmation has no date/);
  // An unreadable publish time is no date either.
  const odd = round(where, { site: [listing("no-confirmation", { youtube_publish_at: "next week" })] });
  assert.match(odd.undated[0].why, /publish time "next week" is not a date/);
  // The site's confirmation alone dates it, as on the site.
  assert.equal(round(where, { site: [listing("no-confirmation")] }).cleared.slug, "no-confirmation");
});

test("one video a round, the oldest finished first", () => {
  const where = place();
  const newer = finishedVideo(where.work, "a-newer", { published: daysAgo(10) });
  const older = finishedVideo(where.work, "b-older", { published: daysAgo(20) });
  const site = [listing("a-newer", { publish_approved_at: daysAgo(10) }), listing("b-older", { publish_approved_at: daysAgo(20) })];
  const first = round(where, { site });
  assert.equal(first.cleared.slug, "b-older");
  assert.ok(!exists(older, "final.mp4"));
  assertUntouched(newer);
  const second = round(where, { site });
  assert.equal(second.cleared.slug, "a-newer");
  assert.ok(!exists(newer, "final.mp4"));
  const third = round(where, { site });
  assert.equal(third.cleared, null, "a tidied video is not looked at again");
  assert.equal(autoJson(older).tidied_at, NOW.toISOString(), "the first tidy's record stands");
});

test("--dry-run lists what would go and removes nothing", async () => {
  const where = place();
  const dir = finishedVideo(where.work, "dry-run");
  const result = round(where, { site: [listing("dry-run")], dryRun: true });
  assert.equal(result.cleared.dryRun, true);
  assert.equal(result.cleared.bytes, MEDIA_BYTES);
  assertUntouched(dir);
  for (const name of RECORDS) assert.ok(exists(dir, name));
  const { roundLines } = await import("./tidy.mjs");
  assert.match(roundLines(result)[0], /^tidy --dry-run: dry-run \(on YouTube, counted from 2026-10-12\) would lose final\.mp4, .*; 4 KB \(4490 bytes\) would be freed$/);
});

test("a finished video stays while something still needs its files", () => {
  const where = place();
  const undecided = finishedVideo(where.work, "languages-undecided");
  const working = finishedVideo(where.work, "languages-working");
  const stopped = finishedVideo(where.work, "stop-file");
  put(stopped, "STOP", "");
  // An episode of a binge series: compile joins its cut into the series' compilation later.
  const episode = finishedVideo(where.work, "saga-e001", { state: { format: "drama", series: { slug: "saga", episode: 1, compilation: true } } });
  const site = [
    listing("languages-undecided", { locales_decided_at: null }),
    listing("languages-working", { languages: { en: { metadata: { state: "ready" }, captions: { state: "working" } } } }),
    listing("stop-file"),
    listing("saga-e001"),
  ];
  const result = round(where, { site });
  assert.equal(result.cleared, null);
  for (const dir of [undecided, working, stopped, episode]) assertUntouched(dir);
  const why = Object.fromEntries(result.held.map((entry) => [entry.slug, entry.why]));
  assert.match(why["languages-undecided"], /languages are not decided/);
  assert.match(why["languages-working"], /en captions in the making/);
  assert.match(why["stop-file"], /STOP/);
  assert.match(why["saga-e001"], /episode of saga, whose compilation has not started/);
  // Without the round's list from the site, a video on YouTube cannot be dated or checked.
  assert.ok(round(where, { site: null }).held.some((entry) => entry.slug === "languages-undecided" && /list was not read/.test(entry.why)));
  // Once the compilation is on YouTube, the episode goes like any other video.
  finishedVideo(where.work, "saga-full", { published: daysAgo(30), state: { format: "drama", compilation: { series: "saga", episodes: ["saga-e001"] }, series: { slug: "saga", compilation: true } } });
  const after = round(where, { site: [...site, listing("saga-full", { publish_approved_at: daysAgo(30) })] });
  assert.equal(after.cleared.slug, "saga-full", "the compilation is the oldest");
  assert.equal(round(where, { site: [...site, listing("saga-full", { publish_approved_at: daysAgo(30) })] }).cleared.slug, "saga-e001");
});

test("a compilation's hard-linked cut frees its bytes once", () => {
  const where = place();
  const dir = finishedVideo(where.work, "saga-full", { media: { "final.mp4": 5000 }, state: { compilation: { series: "saga", episodes: [] } } });
  mkdirSync(path.join(dir, "upload"), { recursive: true });
  linkSync(path.join(dir, "final.mp4"), path.join(dir, "upload", "final.mp4"));
  const dry = round(where, { site: [listing("saga-full")], dryRun: true });
  assert.equal(dry.cleared.bytes, 5000);
  const result = round(where, { site: [listing("saga-full")] });
  assert.equal(result.cleared.bytes, 5000);
  assert.ok(!exists(dir, "final.mp4") && !exists(dir, "upload/final.mp4"));
});

test("the shared folders and anything whose name begins with _ are never touched", () => {
  const where = place();
  const shared = ["_series/saga/characters/hero.png", "_series/saga/index.json", "_music/licensed.mp3", "_audition/2026-10-01/index.html", "_old/final.mp4", "_old/segments/s1.mp4", "auto-state.json"];
  for (const name of shared) put(where.work, name, `shared ${name}`);
  // A shared folder that looks like a finished video is still not read.
  put(where.work, "_old/auto.json", JSON.stringify({ slug: "_old", status: "done", youtube_video_id: YOUTUBE }));
  finishedVideo(where.work, "on-youtube-old");
  assert.equal(round(where, { site: [listing("on-youtube-old")] }).cleared.slug, "on-youtube-old");
  assert.equal(round(where, { site: [listing("on-youtube-old")] }).cleared, null);
  for (const name of shared) assert.equal(readFileSync(path.join(where.work, ...name.split("/")), "utf8"), `shared ${name}`, `${name} is untouched`);
});

test("a folder whose auto.json names another video is not that video's work directory", () => {
  const where = place();
  // Copied or renamed by hand: the folder is not the one the flow writes for "the-real-one".
  const copy = finishedVideo(where.work, "a-copy", { state: { slug: "the-real-one" } });
  const result = round(where, { site: [listing("the-real-one"), listing("a-copy")] });
  assert.equal(result.cleared, null);
  assert.deepEqual([result.due, result.held, result.undated].map((list) => list.length), [0, 0, 0]);
  assertUntouched(copy);
});

test("a work base that is empty, relative, a drive's root or the repository is refused outright", () => {
  const where = place();
  const refused = (options) => tidyBase({ root: where.repo, home: where.top, ...options }).refused;
  assert.match(refused({ env: { VIDEO_WORKDIR: "" } }), /empty/);
  assert.match(refused({ env: { VIDEO_WORKDIR: "   " } }), /empty/);
  assert.match(refused({ flag: "" }), /empty/);
  assert.match(refused({ env: { VIDEO_WORKDIR: "work" } }), /relative/);
  assert.match(refused({ flag: path.join("..", "work") }), /relative/);
  assert.match(refused({ env: { VIDEO_WORKDIR: path.parse(where.top).root } }), /drive's root/);
  assert.match(refused({ env: { VIDEO_WORKDIR: where.repo } }), /inside the repository/);
  assert.match(refused({ env: { VIDEO_WORKDIR: path.join(where.repo, "media") } }), /inside the repository/);
  assert.match(refused({ env: { VIDEO_WORKDIR: where.top } }), /holds the repository/);
  assert.match(refused({ env: { VIDEO_WORKDIR: ROOT } }), /inside the repository/, "this tool's own repository too");
  assert.deepEqual(tidyBase({ env: { VIDEO_WORKDIR: where.work }, root: where.repo }), { base: where.work });
  assert.deepEqual(tidyBase({ env: { VIDEO_WORKDIR: path.join(where.top, "nowhere") }, root: where.repo }), { missing: path.join(where.top, "nowhere") });
  // Handed a base that holds the repository anyway, the round still removes nothing and says so.
  const dir = finishedVideo(where.top, "beside-the-repo");
  const result = tidyRound({ base: where.top, repos: where.repos, site: [listing("beside-the-repo")], now: NOW });
  assert.equal(result.cleared, null);
  assert.match(result.refused[0].refused, /holds the repository/);
  assertUntouched(dir);
});

test("a path outside the video's own folder in the work base is refused", () => {
  const where = place();
  const workdir = path.join(where.work, "one-video");
  const places = { base: where.work, workdir, repos: where.repos };
  assert.equal(targetRefusal(path.join(workdir, "final.mp4"), places), null);
  assert.equal(targetRefusal(path.join(workdir, "dubs", "en", "audio"), places), null);
  assert.match(targetRefusal(where.work, places), /the work base itself/);
  assert.match(targetRefusal(workdir, places), /whole work directory/);
  assert.match(targetRefusal(path.join(where.work, "other-video", "final.mp4"), places), /outside the video's work directory/);
  assert.match(targetRefusal(path.join(where.work, "_series", "saga"), places), /outside the video's work directory/);
  assert.match(targetRefusal(path.join(workdir, "..", "..", "repo", "x"), places), /outside/);
  assert.match(targetRefusal(path.join(where.top, "elsewhere"), places), /outside/);
  assert.match(targetRefusal(path.join(where.work, "_series", "final.mp4"), { ...places, workdir: path.join(where.work, "_series") }), /not a video's folder/);
  assert.match(targetRefusal(path.join(where.work, "a", "b", "final.mp4"), { ...places, workdir: path.join(where.work, "a", "b") }), /not a video's folder directly in the work base/);
  assert.match(targetRefusal(path.join(where.repo, "v", "final.mp4"), { base: where.repo, workdir: path.join(where.repo, "v"), repos: where.repos }), /inside the repository/);
  const root = path.parse(where.top).root;
  assert.match(targetRefusal(path.join(root, "v", "final.mp4"), { base: root, workdir: path.join(root, "v"), repos: where.repos }), /drive's root/);
});

test("a link is removed as a link, never what it points at", () => {
  const where = place();
  const outside = path.join(where.top, "outside");
  put(outside, "precious.mp4", "precious");
  put(outside, "final.mp4", "outside cut");
  put(where.work, "_series/saga/characters/hero.png", "hero");
  const dir = finishedVideo(where.work, "linked-inside", { media: { "final.mp4": 10, "build/video.mp4": 10 } });
  // A folder the tidy removes is a link to a shared folder; a link sits deep in another one.
  symlinkSync(path.join(where.work, "_series", "saga"), path.join(dir, "segments"), "junction");
  symlinkSync(outside, path.join(dir, "build", "escape"), "junction");
  // upload/ is a link out of the work directory: nothing inside it is reached through it.
  rmSync(path.join(dir, "upload"), { recursive: true });
  symlinkSync(outside, path.join(dir, "upload"), "junction");
  const result = round(where, { site: [listing("linked-inside")] });
  assert.equal(result.cleared.slug, "linked-inside");
  assert.equal(readFileSync(path.join(where.work, "_series", "saga", "characters", "hero.png"), "utf8"), "hero", "the shared folder behind the link is intact");
  assert.equal(readFileSync(path.join(outside, "precious.mp4"), "utf8"), "precious");
  assert.equal(readFileSync(path.join(outside, "final.mp4"), "utf8"), "outside cut", "upload/final.mp4 is not reached through the upload/ link");
  assert.ok(!existsSync(path.join(dir, "segments")), "the segments/ link itself is gone");
  assert.ok(!existsSync(path.join(dir, "build")), "build/ went, its link removed as a link");
  assert.ok(!exists(dir, "final.mp4"));
  assert.ok(lstatSync(path.join(dir, "upload")).isSymbolicLink(), "the upload/ link is not a target and stays");
  assert.ok(result.cleared.failed.some((entry) => entry.path === "upload/final.mp4" && /link or a file, not a folder/.test(entry.error)));
});

test("a video folder that is a link is never followed", () => {
  const where = place();
  // A finished video's folder outside the work base, linked into it under the slug it names.
  const outside = finishedVideo(where.top, "outside-video", { state: { slug: "linked-video" } });
  symlinkSync(outside, path.join(where.work, "linked-video"), "junction");
  const result = round(where, { site: [listing("linked-video")] });
  assert.equal(result.cleared, null, "a linked video folder is not a video of this work base");
  assert.deepEqual([result.due, result.held, result.undated].map((list) => list.length), [0, 0, 0]);
  assert.ok(existsSync(path.join(outside, "final.mp4")) && existsSync(path.join(outside, "segments", "s1-0a1b.mp4")));
});

test("a file link is removed as a link", (t) => {
  const where = place();
  const dir = finishedVideo(where.work, "file-link", { media: {} });
  put(where.top, "elsewhere.mp4", "keep me");
  try {
    symlinkSync(path.join(where.top, "elsewhere.mp4"), path.join(dir, "final.mp4"), "file");
  } catch (error) {
    // Windows without Developer Mode makes no file links; the junction tests cover folders there.
    if (error.code === "EPERM") return t.skip("this system does not allow file symbolic links");
    throw error;
  }
  const linked = round(where, { site: [listing("file-link")] });
  assert.equal(linked.cleared.slug, "file-link");
  assert.equal(lstatSync(path.join(dir, "final.mp4"), { throwIfNoEntry: false }), undefined, "the link itself is gone");
  assert.equal(readFileSync(path.join(where.top, "elsewhere.mp4"), "utf8"), "keep me");
  assert.equal(linked.cleared.bytes, 0, "a link frees nothing");
});

test("a locked or missing file is reported and the round ends normally", async () => {
  const where = place();
  const dir = finishedVideo(where.work, "locked-file");
  const locked = path.join(dir, "segments", "s1-0a1b.mp4");
  const vanished = path.join(dir, "audio", "k7p2.wav");
  const fs = await import("node:fs");
  const failing = {
    existsSync: fs.existsSync,
    lstatSync: fs.lstatSync,
    readdirSync: fs.readdirSync,
    readFileSync: fs.readFileSync,
    realpathSync: fs.realpathSync,
    rmdirSync: fs.rmdirSync,
    unlinkSync(file) {
      if (file === locked) throw Object.assign(new Error(`EBUSY: resource busy or locked, unlink '${file}'`), { code: "EBUSY" });
      if (file === vanished) {
        fs.unlinkSync(file);
        throw Object.assign(new Error(`ENOENT: no such file or directory, unlink '${file}'`), { code: "ENOENT" });
      }
      return fs.unlinkSync(file);
    },
  };
  const result = round(where, { site: [listing("locked-file")], fs: failing });
  assert.equal(result.cleared.slug, "locked-file");
  assert.deepEqual(result.cleared.failed, [{ path: "segments/s1-0a1b.mp4", error: "EBUSY" }]);
  assert.deepEqual(result.cleared.gone, ["audio/k7p2.wav"]);
  assert.ok(existsSync(locked), "the locked file stays, with its folder");
  assert.ok(!exists(dir, "segments/s1.ffconcat") && !exists(dir, "final.mp4") && !exists(dir, "audio"), "everything else went");
  assert.equal(result.cleared.bytes, MEDIA_BYTES - 200 - 400);
  const state = autoJson(dir);
  assert.equal(state.tidied_at, NOW.toISOString(), "the video is not looked at again");
  assert.deepEqual(state.tidied.failed, [{ path: "segments/s1-0a1b.mp4", error: "EBUSY" }]);
  const { roundLines } = await import("./tidy.mjs");
  assert.match(roundLines(result)[0], /; could not remove 1: segments\/s1-0a1b\.mp4 \(EBUSY\); already gone: audio\/k7p2\.wav$/);
});

test("status reads a tidied video as cleared, not as a next step", () => {
  const where = place();
  const dir = finishedVideo(where.work, "noted");
  assert.equal(tidiedNote(dir), null);
  round(where, { site: [listing("noted")] });
  assert.match(tidiedNote(dir), /^On YouTube as dQw4w9WgXcQ; the work files were cleared on 2026-10-20 \(4 KB freed\)\. The steps above that read those files show as not done; nothing makes them again\.$/);
  const dropped = finishedVideo(where.work, "dropped-noted", { published: null, state: { status: "dropped", youtube_video_id: undefined, dropped: { at: daysAgo(30), note: "" } } });
  round(where, { site: [] });
  assert.match(tidiedNote(dropped), /^Dropped by the owner on 2026-09-20; the work files were cleared on 2026-10-20/);
});
