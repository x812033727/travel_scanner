import assert from "node:assert/strict";
import test from "node:test";

import { EXIT, main as runCli } from "../cli.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { AutomationError, automationClient } from "./client.mjs";

const SITE = "https://site.test";
const TOKEN = `mkv_${"t".repeat(43)}`;
const OUTDATED = "video_ai_subscription_cli_outdated";
const DETAIL = "Claude Code 2.1.259 does not support this model; version 2.1.280 or newer is required. Run `claude update` on the host.";

function credentials(box) {
  return {
    home: box.base,
    env: { MOKAAIR_SITE: SITE, MOKAAIR_VIDEO_TOKEN: TOKEN, VIDEO_WORKDIR: box.work },
  };
}

test("an outdated subscription CLI is the owner's to fix after one request, with the version guidance intact", async () => {
  const box = sandbox();
  const calls = [];
  const sleeps = [];
  const client = automationClient({
    ...credentials(box),
    fetch: async (url, init) => {
      calls.push({ url, method: init.method, body: JSON.parse(init.body) });
      return Response.json({ code: OUTDATED, detail: DETAIL }, { status: 409 });
    },
    sleep: async (ms) => sleeps.push(ms),
  });

  await assert.rejects(client.run("planner", "draft-example", "Plan a video", {}), (error) => {
    assert.ok(error instanceof AutomationError);
    assert.equal(error.who, "owner");
    assert.equal(error.status, 409);
    assert.equal(error.code, OUTDATED);
    assert.equal(error.message, DETAIL);
    return true;
  });
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, `${SITE}/api/video/automation/run`);
  assert.equal(calls[0].method, "POST");
  assert.equal(calls[0].body.stage, "planner");
  assert.deepEqual(sleeps, [], "a CLI upgrade cannot be fixed by waiting and retrying");
});

test("a generic upstream failure remains a service error with bounded retries", async () => {
  const box = sandbox();
  let calls = 0;
  const sleeps = [];
  const client = automationClient({
    ...credentials(box),
    fetch: async () => {
      calls++;
      return Response.json({ code: "video_ai_upstream_failed", detail: "Claude run failed" }, { status: 502 });
    },
    sleep: async (ms) => sleeps.push(ms),
  }, { attempts: 3 });

  await assert.rejects(client.run("planner", "draft-example", "Plan a video", {}), (error) => {
    assert.ok(error instanceof AutomationError);
    assert.equal(error.who, "service");
    assert.equal(error.status, 502);
    assert.equal(error.code, "video_ai_upstream_failed");
    return true;
  });
  assert.equal(calls, 3);
  assert.deepEqual(sleeps, [5000, 10000, 20000]);
});

test("auto exits for the owner after one real stage request when Claude Code needs updating", async () => {
  const box = sandbox();
  const calls = [];
  const stages = [];
  const sleeps = [];
  const out = { stdout: "", stderr: "" };
  const code = await runCli(["auto"], {
    ...credentials(box),
    root: box.root,
    now: () => new Date("2026-09-30T02:00:00Z"),
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    sleep: async (ms) => sleeps.push(ms),
    runCommand: async () => assert.fail("no media stage should run after the planner was refused"),
    fetch: async (url, init) => {
      assert.equal(new URL(url).origin, SITE);
      const route = new URL(url).pathname;
      calls.push(`${init.method} ${route}`);
      if (route === "/api/video/automation/settings") {
        return Response.json({ enabled: true, max_waiting_drafts: 1, draft_interval_hours: 72, target_minutes_min: 5, target_minutes_max: 8 });
      }
      if (route === "/api/video/automation/videos") return Response.json([]);
      // A site from before Shorts (docs/videos/SHORTS.md): the Shorts round has nothing to do.
      if (route.startsWith("/api/video/automation/shorts/")) return Response.json({ code: "not_found", detail: route }, { status: 404 });
      if (route === "/api/video/automation/topics") return Response.json({ topics: [], notes: "" });
      if (route === "/api/video/automation/run") {
        stages.push(JSON.parse(init.body));
        return Response.json({ code: OUTDATED, detail: DETAIL }, { status: 409 });
      }
      assert.fail(`unexpected request: ${init.method} ${route}`);
    },
  });

  assert.equal(code, EXIT.owner);
  assert.equal(code, 3);
  assert.equal(out.stderr, `${DETAIL}\n`);
  assert.equal(out.stdout, "");
  assert.deepEqual(stages.map(({ stage }) => stage), ["planner"]);
  assert.deepEqual(calls, [
    "GET /api/video/automation/settings",
    "GET /api/video/automation/shorts/settings",
    "GET /api/video/automation/videos",
    "GET /api/video/automation/topics",
    "POST /api/video/automation/run",
  ]);
  assert.deepEqual(sleeps, []);
});
