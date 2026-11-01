// The backup between units of a long `auto` round (cli.mjs BACKUP_EVERY_MS). On 2026-11-01 a
// round with a daily brief's eight languages ran for more than three hours, and four imported
// zhong-tian episodes waited all that time for their packages to be fetched and copied, because
// the backup ran only once a round had ended.
import assert from "node:assert/strict";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { BACKUP_EVERY_MS, backupBetweenUnits } from "./cli.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;
const SITE = "https://site.test";
const START = Date.parse("2026-11-01T04:43:00Z");

/** A backup client with backups off; `asked` counts how many backups read the settings. */
function backupClient() {
  const asked = [];
  return {
    asked,
    config: async () => {
      asked.push("config");
      return { enabled: false, path: "AI/備份", lock_path: null, remote_prefix: null, problem: "備份尚未開啟", test: null, videos: [] };
    },
    lock: async () => ({}),
  };
}

const backups = (client) => client.asked.length / 2; // each backup reads the settings, reports the lock, reads them again

function context(box, clock, client, extra = {}) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN, MOKAAIR_SITE: SITE },
    home: box.base,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date(clock.now),
    sleep: async (ms) => {
      clock.now += ms;
    },
    backupClient: client,
    EXIT,
    ...extra,
  };
  return { ctx, out };
}

test("between units, the backup runs once BACKUP_EVERY_MS has passed since the round began or the last one, and never twice at once", async () => {
  const box = sandbox();
  const clock = { now: START };
  const client = backupClient();
  const { ctx } = context(box, clock, client);
  const backupNow = backupBetweenUnits(ctx);

  assert.equal(await backupNow(), false, "not at the start of a round");
  clock.now += BACKUP_EVERY_MS - 1;
  assert.equal(await backupNow(), false);
  clock.now += 1;
  assert.equal(await backupNow(), true);
  assert.equal(backups(client), 1);
  clock.now += BACKUP_EVERY_MS / 2;
  assert.equal(await backupNow(), false, "counted from the last backup");
  clock.now += BACKUP_EVERY_MS / 2;
  assert.equal(await backupNow(), true);
  assert.equal(backups(client), 2);

  // A backup still running (rclone on a large episode) is not started again beside itself.
  let release;
  const gate = new Promise((resolve) => (release = resolve));
  const off = { enabled: false, lock_path: null, remote_prefix: null, videos: [] };
  const slow = { ...backupClient(), config: async () => (await gate, off) };
  const held = backupBetweenUnits(context(box, clock, slow).ctx);
  clock.now += BACKUP_EVERY_MS;
  const first = held();
  assert.equal(await held(), false);
  release();
  assert.equal(await first, true);

  // A STOP file stops it, as it stops the backup at the end of a round.
  const stopped = backupBetweenUnits(ctx, { stop: () => true });
  clock.now += BACKUP_EVERY_MS;
  assert.equal(await stopped(), false);
  assert.equal(backups(client), 2);
});

test("auto backs up between units of a round that runs past BACKUP_EVERY_MS, and again at its end; --once does not", async () => {
  const box = sandbox();
  // A site with nothing to do; every reading of the clock is eleven minutes later, as in a round
  // whose units each take that long.
  const fetch = async (url) => {
    const { pathname } = new URL(url);
    if (pathname === "/api/video/automation/settings") return Response.json({ enabled: true, max_waiting_drafts: 0, draft_interval_hours: 72 });
    if (pathname === "/api/video/automation/videos") return Response.json([]);
    return Response.json({ code: "not_found", detail: pathname }, { status: 404 });
  };
  const runCommand = async () => ({ code: 0, out: "" });
  const slowClock = (from) => {
    let now = from;
    return () => new Date((now += 11 * 60_000));
  };

  const long = backupClient();
  const round = context(box, { now: START }, long, { fetch, runCommand, now: slowClock(START) });
  assert.equal(await main(["auto"], round.ctx), EXIT.ok, round.out.stderr);
  assert.equal(backups(long), 2, "one between units, one at the end of the round");

  const once = backupClient();
  const single = context(box, { now: START }, once, { fetch, runCommand, now: slowClock(START) });
  assert.equal(await main(["auto", "--once"], single.ctx), EXIT.ok, single.out.stderr);
  assert.equal(backups(once), 1, "a single unit by hand backs up only at its end");

  // A STOP file in the work base: neither runs.
  mkdirSync(box.work, { recursive: true });
  writeFileSync(path.join(box.work, "STOP"), "");
  const halted = backupClient();
  const stopped = context(box, { now: START }, halted, { fetch, runCommand, now: slowClock(START) });
  await main(["auto"], stopped.ctx);
  assert.equal(backups(halted), 0);
});
