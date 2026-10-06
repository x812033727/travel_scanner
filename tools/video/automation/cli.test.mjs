import assert from "node:assert/strict";
import * as nodeFs from "node:fs";
import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { STATE_FILE } from "./tidy.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const SITE = "https://site.test";
const NOW = new Date("2026-10-20T12:00:00Z");
const daysAgo = (days) => new Date(NOW.getTime() - days * 86_400_000).toISOString();
const YOUTUBE = "dQw4w9WgXcQ";
const MEDIA = ["final.mp4", "upload/final.mp4", "segments/s1-0a1b.mp4", "build/video.mp4", "audio/k7p2.wav", "narration.wav", "keyframes/s1.png", "review/preview-0123456789abcdef.mp4"];
const RECORDS = ["timeline.json", "checks.json", "upload/metadata.json", "captions/zh-TW.srt", "media/ledger.json", "review/qa.json"];

function put(dir, name, content) {
  const file = path.join(dir, ...name.split("/"));
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, content);
}

/** A video in the work base with the stages' media and records; finished on YouTube unless `state` says otherwise. */
function video(work, slug, { state = {}, published = daysAgo(8) } = {}) {
  const dir = path.join(work, slug);
  for (const name of MEDIA) put(dir, name, Buffer.alloc(100, 7));
  // `status` parses the records, so the JSON ones hold JSON.
  for (const name of RECORDS) put(dir, name, name.endsWith(".json") ? `{"record": "${name}"}\n` : `${name}\n`);
  put(dir, "approvals.json", JSON.stringify({ approvals: published ? [{ gate: "publish", file: "metadata.json", sha256: "b".repeat(64), approved_at: published, note: "" }] : [] }));
  put(dir, STATE_FILE, `${JSON.stringify({ slug, title: slug, status: "done", created_at: daysAgo(20), youtube_video_id: YOUTUBE, notes: [], ...state }, null, 2)}\n`);
  return dir;
}

const listing = (slug, extra = {}) => ({ slug, title: slug, youtube_video_id: YOUTUBE, publish_approved_at: daysAgo(8), youtube_publish_at: null, dropped_at: null, dropped_note: null, locales: {}, locales_decided_at: daysAgo(10), languages: {}, ...extra });
const cleared = (dir) => MEDIA.every((name) => !existsSync(path.join(dir, ...name.split("/"))));
const untouched = (dir) => MEDIA.every((name) => existsSync(path.join(dir, ...name.split("/")))) && !JSON.parse(readFileSync(path.join(dir, STATE_FILE), "utf8")).tidied_at;

/** The site as `auto` reads it here: the settings and the video list. No draft is due (no room). */
function fakeSite({ settings = {}, videos = [], down = false, reviews = false } = {}) {
  const calls = [];
  const sent = [];
  const fetchImpl = async (url, init = {}) => {
    const { pathname } = new URL(url);
    calls.push(`${init.method ?? "GET"} ${pathname}`);
    if (down) throw new Error("connect ECONNREFUSED");
    if (pathname === "/api/video/automation/settings") return Response.json({ enabled: true, max_waiting_drafts: 0, draft_interval_hours: 72, ...settings });
    if (pathname === "/api/video/automation/videos") return Response.json(videos);
    // With `reviews`, the site takes a review and a report and keeps what was sent.
    if (reviews && pathname.startsWith("/api/video/reviews/") && ["POST", "PUT"].includes(init.method)) {
      const body = JSON.parse(init.body);
      sent.push({ method: init.method, pathname, body });
      return Response.json(init.method === "POST" ? { id: `r${sent.length}`, status: "approved", ...body } : { reviews: [] });
    }
    return Response.json({ code: "not_found", detail: pathname }, { status: 404 });
  };
  return { calls, sent, fetchImpl };
}

/** A context for `main`: the sandbox's repository and work base, the fake site, and a stage runner that records. */
function context(box, site, { env = {}, ...extra } = {}) {
  const out = { stdout: "", stderr: "" };
  const commands = [];
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE, ...env },
    home: box.base,
    fetch: site.fetchImpl,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => NOW,
    sleep: async () => {},
    // No stage may run in these tests: anything `auto` asks for is recorded.
    runCommand: async (command) => {
      commands.push(command.join(" "));
      return { code: 0, out: "" };
    },
    ...extra,
  };
  return { ctx, out, commands };
}

test("auto clears one finished video once a round, after the units, whether or not one moved", async () => {
  const box = sandbox();
  const onYouTube = video(box.work, "old-on-youtube");
  // The owner dropped this one a month ago; this round's first unit records it.
  const dropped = video(box.work, "dropped-now", { published: null, state: { status: "active", youtube_video_id: undefined } });
  const site = fakeSite({ videos: [listing("old-on-youtube"), listing("dropped-now", { youtube_video_id: null, publish_approved_at: null, dropped_at: daysAgo(30), dropped_note: "not needed" })] });

  const first = context(box, site);
  assert.equal(await main(["auto"], first.ctx), EXIT.ok);
  const lines = first.out.stdout.trim().split("\n");
  assert.equal(lines[0], "dropped-now: the owner dropped it (not needed); the worker leaves it");
  assert.equal(lines[1], "nothing to do now: every video waits on the owner, or the next draft is not due");
  assert.match(lines[2], /^tidy: dropped-now \(dropped on 2026-09-20\): removed final\.mp4, upload\/final\.mp4, segments\/ \(1 file\), .*; 800 bytes freed$/);
  assert.equal(lines.length, 3);
  assert.ok(cleared(dropped));
  assert.ok(untouched(onYouTube), "one video a round");

  // A round where no unit moves still ends with the tidy.
  const second = context(box, site);
  assert.equal(await main(["auto"], second.ctx), EXIT.ok);
  assert.match(second.out.stdout, /^nothing to do now: .*\ntidy: old-on-youtube \(on YouTube, counted from 2026-10-12\): removed final\.mp4/);
  assert.ok(cleared(onYouTube));

  const third = context(box, site);
  assert.equal(await main(["auto"], third.ctx), EXIT.ok);
  assert.doesNotMatch(third.out.stdout, /tidy/, "nothing is left to clear and nothing is said");
  assert.deepEqual([...first.commands, ...second.commands, ...third.commands], [], "no stage ran");
});

test("a round that moves nothing because videos wait on their own names them with the time each is tried again, instead of saying every video waits on the owner", async () => {
  const { idleLine } = await import("./cli.mjs");
  assert.equal(idleLine(), "nothing to do now: every video waits on the owner, or the next draft is not due");
  assert.equal(idleLine([{ slug: "one-video", until: "2026-10-20T12:30:00.000Z" }]), "nothing to do now: 1 deferred and tried again later (one-video until 2026-10-20T12:30:00.000Z); the other videos wait on the owner, or the next draft is not due");
  // A video only this run left (a STOP file between requests) has no time of its own.
  assert.match(idleLine([{ slug: "one-video", until: "2026-10-20T12:30:00.000Z" }, { slug: "stopped-video", until: null }]), /^nothing to do now: 2 deferred and tried again later \(one-video until 2026-10-20T12:30:00\.000Z, stopped-video until the next round\); /);

  const box = sandbox();
  const state = (slug, extra) => put(path.join(box.work, slug), STATE_FILE, `${JSON.stringify({ slug, title: slug, created_at: daysAgo(3), notes: [], ...extra })}\n`);
  state("vendor-busy", { status: "active", created_at: daysAgo(5), deferred_until: "2026-10-20T12:30:00.000Z", defer_count: 3 });
  state("push-refused", { status: "active", created_at: daysAgo(4), deferred_until: "2026-10-20T13:10:00.000Z", defer_count: 5 });
  // Its wait is over: the round looks at it, finds nothing to do and ends its row of deferrals; it is not named.
  state("wait-over", { status: "done", deferred_until: "2026-10-20T11:00:00.000Z", defer_count: 1 });
  const site = fakeSite({ videos: ["vendor-busy", "push-refused", "wait-over"].map((slug) => listing(slug, { youtube_video_id: null, publish_approved_at: null, locales_decided_at: null })) });
  const round = context(box, site, { env: { VIDEO_TIDY_DAYS: "off" } });
  assert.equal(await main(["auto"], round.ctx), EXIT.ok);
  // Before: "nothing to do now: every video waits on the owner, or the next draft is not due".
  assert.equal(round.out.stdout, "nothing to do now: 2 deferred and tried again later (vendor-busy until 2026-10-20T12:30:00.000Z, push-refused until 2026-10-20T13:10:00.000Z); the other videos wait on the owner, or the next draft is not due\n");
  assert.deepEqual(round.commands, [], "no stage ran for a video whose wait is not over");
  const rested = JSON.parse(readFileSync(path.join(box.work, "wait-over", STATE_FILE), "utf8"));
  assert.deepEqual([rested.deferred_until, rested.defer_count], [undefined, undefined]);
  assert.equal(JSON.parse(readFileSync(path.join(box.work, "vendor-busy", STATE_FILE), "utf8")).defer_count, 3);
});

test("auto clears nothing when automatic drafts are off, when STOP is found, or when VIDEO_TIDY_DAYS is off", async () => {
  const box = sandbox();
  const dir = video(box.work, "old-on-youtube");
  const videos = [listing("old-on-youtube")];

  const off = context(box, fakeSite({ settings: { enabled: false }, videos }));
  assert.equal(await main(["auto"], off.ctx), EXIT.ok);
  assert.equal(off.out.stdout, "automatic drafts are off in the settings on /admin/videos; nothing to do\n");

  const switched = context(box, fakeSite({ videos }), { env: { VIDEO_TIDY_DAYS: "off" } });
  assert.equal(await main(["auto"], switched.ctx), EXIT.ok);
  assert.doesNotMatch(switched.out.stdout, /tidy/);

  put(box.work, "STOP", "");
  const stopped = context(box, fakeSite({ videos }));
  assert.equal(await main(["auto"], stopped.ctx), EXIT.ok);
  assert.equal(stopped.out.stdout, "STOP found; stopping between units\n");
  assert.ok(untouched(dir));
});

test("a file that cannot go, a bad setting or an error in the tidy does not stop the worker", async () => {
  const box = sandbox();
  const dir = video(box.work, "old-on-youtube");
  const site = fakeSite({ videos: [listing("old-on-youtube")] });

  const wrong = context(box, site, { env: { VIDEO_TIDY_DAYS: "7d" } });
  assert.equal(await main(["auto"], wrong.ctx), EXIT.ok);
  assert.match(wrong.out.stdout, /\ntidy: not run: VIDEO_TIDY_DAYS=7d is neither a number of days from 1 to 3650 nor "off"\n$/);

  const broken = context(box, site, { tidyFs: { ...nodeFs, existsSync: () => { throw new Error("disk went away"); } } });
  assert.equal(await main(["auto"], broken.ctx), EXIT.ok);
  assert.match(broken.out.stdout, /\ntidy: stopped by an error \(disk went away\); the round ends as usual\n$/);
  assert.ok(untouched(dir));

  // The tidy walks the work base's real path; the lock is set on the same name.
  const cut = path.join(nodeFs.realpathSync(dir), "final.mp4");
  const locked = context(box, site, {
    tidyFs: {
      ...nodeFs,
      unlinkSync: (file) => {
        if (file === cut) throw Object.assign(new Error(`EBUSY: resource busy or locked, unlink '${file}'`), { code: "EBUSY" });
        return nodeFs.unlinkSync(file);
      },
    },
  });
  assert.equal(await main(["auto"], locked.ctx), EXIT.ok);
  assert.match(locked.out.stdout, /\ntidy: old-on-youtube .*; could not remove 1: final\.mp4 \(EBUSY\)\n$/);
  assert.ok(existsSync(cut) && !existsSync(path.join(dir, "segments")));
});

test("tidy by hand: --dry-run lists and keeps everything, a run clears one video, a bad work base is refused", async () => {
  const box = sandbox();
  const dir = video(box.work, "old-on-youtube");
  const recent = video(box.work, "recent", { published: daysAgo(2) });
  const undecided = video(box.work, "undecided");
  const site = fakeSite({ videos: [listing("old-on-youtube"), listing("recent", { publish_approved_at: daysAgo(2) }), listing("undecided", { locales_decided_at: null })] });

  const dry = context(box, site);
  assert.equal(await main(["tidy", "--dry-run"], dry.ctx), EXIT.ok);
  assert.match(dry.out.stdout, /^work base .*; a finished video keeps its work files for 7 days\n/);
  assert.match(dry.out.stdout, /\ntidy --dry-run: old-on-youtube \(on YouTube, counted from 2026-10-12\) would lose final\.mp4, .*; 800 bytes would be freed\n/);
  assert.match(dry.out.stdout, /\ntidy: finished but kept while something needs the files: undecided \(its languages are not decided on \/admin\/videos yet\)\n/);
  assert.match(dry.out.stdout, /\ntidy: 1 finished video keeps its files for 7 days; the next, recent, is due on 2026-10-25\n$/);
  assert.ok(untouched(dir) && untouched(recent) && untouched(undecided));

  const real = context(box, site);
  assert.equal(await main(["tidy"], real.ctx), EXIT.ok);
  assert.ok(cleared(dir));
  assert.ok(untouched(recent) && untouched(undecided));
  const again = context(box, site);
  assert.equal(await main(["tidy"], again.ctx), EXIT.ok);
  assert.match(again.out.stdout, /\ntidy: nothing is due\n/);

  for (const [env, flag, why] of [
    [{}, [""], /the work base is empty/],
    [{ VIDEO_WORKDIR: "work" }, [], /is a relative path/],
    [{ VIDEO_WORKDIR: path.parse(box.base).root }, [], /drive's root/],
    [{ VIDEO_WORKDIR: box.root }, [], /inside the repository/],
    [{ VIDEO_WORKDIR: box.base }, [], /holds the repository/],
  ]) {
    const refused = context(box, site, { env });
    assert.equal(await main(["tidy", ...(flag.length ? ["--workdir", ...flag] : [])], refused.ctx), EXIT.usage, String(why));
    assert.match(refused.out.stderr, why);
    assert.match(refused.out.stderr, /nothing is cleared\n$/);
  }
  const off = context(box, site, { env: { VIDEO_TIDY_DAYS: "off" } });
  assert.equal(await main(["tidy"], off.ctx), EXIT.ok);
  assert.equal(off.out.stdout, "VIDEO_TIDY_DAYS=off: the tidy is switched off; nothing is cleared\n");
  const unreachable = context(box, fakeSite({ down: true }));
  assert.equal(await main(["tidy"], unreachable.ctx), EXIT.external);
  assert.match(unreachable.out.stderr, /the site's video list, which dates the videos on YouTube, could not be read/);
  put(box.work, "STOP", "");
  const stopped = context(box, site);
  assert.equal(await main(["tidy"], stopped.ctx), EXIT.ok);
  assert.equal(stopped.out.stdout, "STOP found in the work base; nothing is cleared\n");
  assert.ok(untouched(recent) && untouched(undecided));
});

test("a tidied video is not made again, and status says it was cleared instead of a next step", async () => {
  const box = sandbox();
  // The sandbox's video, finished: its script records the YouTube id, as flow.mjs writes it.
  const doc = JSON.parse(readFileSync(path.join(box.dir, "video.json"), "utf8"));
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify({ ...doc, youtube: { ...doc.youtube, video_id: YOUTUBE } }, null, 2)}\n`);
  const dir = video(box.work, box.slug);

  const before = context(box, fakeSite());
  assert.equal(await main(["status", "--slug", box.slug], before.ctx), EXIT.ok);
  assert.match(before.out.stdout, /\nNext: /);

  const site = fakeSite({ videos: [listing(box.slug)] });
  const tidy = context(box, site);
  assert.equal(await main(["tidy"], tidy.ctx), EXIT.ok);
  assert.ok(cleared(dir));

  const after = context(box, site);
  assert.equal(await main(["status", "--slug", box.slug], after.ctx), EXIT.ok);
  assert.doesNotMatch(after.out.stdout, /Next:|Done:/);
  assert.match(after.out.stdout, /\[ \] video assembled/, "the checklist still reads the files as they are");
  assert.match(after.out.stdout, /\nOn YouTube as dQw4w9WgXcQ; the work files were cleared on 2026-10-20 \(800 bytes freed\)\. The steps above that read those files show as not done; nothing makes them again\.\n$/);

  // The owner ticks English captions after the tidy: the worker neither advances the video nor
  // makes its languages, which need the cut that is gone; it reports the parts as skipped with
  // the date the files were cleared, and runs no stage.
  const later = fakeSite({ reviews: true, videos: [listing(box.slug, { locales: { en: { metadata: true, captions: true, dub: false } }, languages: { en: { metadata: { state: "working" }, captions: { state: "working" } } } })] });
  const round = context(box, later);
  assert.equal(await main(["auto"], round.ctx), EXIT.ok);
  assert.match(round.out.stdout, new RegExp(`^${box.slug}: work files cleared on 2026-10-20; en metadata\\+captions reported to /admin/videos as skipped, not made\\n`));
  assert.deepEqual(round.commands, []);
  assert.ok(cleared(dir), "nothing was made again");
  const [review] = later.sent.filter((each) => each.method === "POST");
  const skipped = { status: "skipped", reason: "工作檔已在 2026-10-20 清掉，成片與旁白都不在了，清理後才勾的部件做不出來；要這個語言得重做影片" };
  assert.deepEqual([review.pathname, review.body.gate, review.body.payload, review.body.files], [`/api/video/reviews/${box.slug}/reviews`, "languages", { locales: { en: { metadata: skipped, captions: skipped } } }, []]);
});
