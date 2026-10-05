import assert from "node:assert/strict";
import { existsSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main as runCli } from "../cli.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { AutomationError, automationClient, RUN_PENDING, RUN_UNCERTAIN } from "./client.mjs";
import { RUN_RECEIPTS_DIR } from "./run-receipts.mjs";

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
      // No slides video of an article the owner asked for: the scheduled draft comes next.
      if (route === "/api/video/automation/slides-requests/next") return Response.json({ request: null });
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
    "GET /api/video/automation/slides-requests/next",
    "GET /api/video/automation/topics",
    "POST /api/video/automation/run",
  ]);
  assert.deepEqual(sleeps, []);
});

// A stage run's answer lost on the way (2026-09-29: a translation finished on the server after
// 302 s, past the web route's 295 s, recorded as ok): the run is sent once, never again on its own.
const failed = (code) => Object.assign(new TypeError("fetch failed"), { cause: Object.assign(new Error(`socket ${code}`), { code }) });

test("a stage run sent and left without its answer is not sent again: the route's deadline, a gateway, a dropped connection, a broken body", async () => {
  const lost = [
    ["the web route's deadline", () => Response.json({ code: RUN_UNCERTAIN, detail: "no answer within the deadline" }, { status: 504 }), 504],
    ["a gateway's timeout page", () => new Response("<html>504 Gateway Time-out</html>", { status: 504, headers: { "Content-Type": "text/html" } }), 504],
    ["an error without the API's code", () => Response.json({ detail: "Internal Server Error" }, { status: 500 }), 500],
    ["a connection dropped mid-way", () => {
      throw failed("UND_ERR_SOCKET");
    }, 0],
    ["Node's five minutes for the headers", () => {
      throw failed("UND_ERR_HEADERS_TIMEOUT");
    }, 0],
    ["an answer that breaks off", () => new Response('{"text": "{\\"worksheet\\"', { status: 200, headers: { "Content-Type": "application/json" } }), 200],
  ];
  for (const [what, answer, status] of lost) {
    const box = sandbox();
    let calls = 0;
    const sleeps = [];
    const client = automationClient({
      ...credentials(box),
      fetch: async () => {
        calls++;
        return answer();
      },
      sleep: async (ms) => sleeps.push(ms),
    });
    await assert.rejects(client.run("translator", "long-video", "Translate", { locale: "en" }), (error) => {
      assert.ok(error instanceof AutomationError, what);
      assert.equal(error.code, RUN_UNCERTAIN, what);
      assert.equal(error.who, "service", what);
      assert.equal(error.status, status, what);
      assert.match(error.message, /no answer came back.*not sent again/, what);
      return true;
    });
    assert.equal(calls, 1, `${what}: sent once`);
    assert.deepEqual(sleeps, [], `${what}: no wait for a second try`);
  }
});

test("a stage run that never reached a server, or that the API settled, is still tried again as before", async () => {
  const settled = [
    ["a refused connection", () => {
      throw failed("ECONNREFUSED");
    }],
    ["an unknown host", () => {
      throw failed("ENOTFOUND");
    }],
    ["the web route that never reached the API", () => Response.json({ code: "upstream_unavailable", detail: "API 服務目前無法回應" }, { status: 502 })],
    ["the API's rate limit", () => Response.json({ code: "rate_limit_exceeded", detail: "slow down" }, { status: 429 })],
    ["a busy vendor", () => Response.json({ code: "video_ai_upstream_busy", detail: "busy" }, { status: 503 })],
  ];
  for (const [what, answer] of settled) {
    const box = sandbox();
    let calls = 0;
    const client = automationClient({ ...credentials(box), fetch: async () => (++calls === 1 ? answer() : Response.json({ text: "{}", model: "m" })), sleep: async () => {} });
    assert.deepEqual(await client.run("translator", "long-video", "Translate", {}), { text: "{}", model: "m" }, what);
    assert.equal(calls, 2, `${what}: tried again`);
  }
});

test("the other requests keep their retries after a dropped connection", async () => {
  const box = sandbox();
  let calls = 0;
  const client = automationClient({
    ...credentials(box),
    fetch: async () => {
      if (++calls === 1) throw failed("UND_ERR_SOCKET");
      return Response.json({ enabled: true });
    },
    sleep: async () => {},
  });
  assert.deepEqual(await client.settings(), { enabled: true });
  assert.equal(calls, 2);
});

test("the owner's slides requests go through the worker relay, and a site from before them reads as none at once", async () => {
  const box = sandbox();
  const id = "6f1d2c3b-4a59-4e6f-8a7b-9c0d1e2f3a4b";
  const queued = { id, source_guide: "ai-freelance-getting-started", title: "AI 接案入門", url: "https://mokaair.com/zh-TW/life/ai-freelance-getting-started", note: null, status: "queued", slug: null };
  const calls = [];
  const sleeps = [];
  let older = false;
  const client = automationClient({
    ...credentials(box),
    fetch: async (url, init) => {
      const route = new URL(url).pathname;
      calls.push({ route, method: init.method, body: init.body ? JSON.parse(init.body) : null });
      if (older) return Response.json({ code: "not_found", detail: route }, { status: 404 });
      if (route.endsWith("/next")) return Response.json({ request: queued });
      if (route.endsWith("/start")) return Response.json({ ...queued, status: "started", slug: "ai-freelance-pricing" });
      return Response.json({ ...queued, status: "done", slug: "ai-freelance-pricing" });
    },
    sleep: async (ms) => sleeps.push(ms),
  });
  assert.deepEqual(await client.slidesNext(), queued);
  assert.equal((await client.slidesStart(id, "ai-freelance-pricing")).status, "started");
  assert.equal((await client.slidesDone(id)).status, "done");
  assert.deepEqual(calls, [
    { route: "/api/video/automation/slides-requests/next", method: "GET", body: null },
    { route: `/api/video/automation/slides-requests/${id}/start`, method: "POST", body: { slug: "ai-freelance-pricing" } },
    { route: `/api/video/automation/slides-requests/${id}/done`, method: "POST", body: null },
  ]);
  older = true;
  assert.equal(await client.slidesNext(), null, "a site without the queue has nothing queued");
  assert.equal(calls.length, 4, "a 404 is not asked again");
  assert.deepEqual(sleeps, []);
});

const DURABLE_SLUG = "saved-writer";
const DURABLE_PATH = "/api/video/automation/run/jobs";
const savedAnswer = { text: '{"answer":"exact saved body"}', provider: "gemini", model: "original-model", input_tokens: 20, output_tokens: 15, usage: { tokens: 35, token_budget: 1000 } };
const durableFiles = (box, slug = DURABLE_SLUG) => {
  const dir = path.join(box.work, slug, RUN_RECEIPTS_DIR);
  return existsSync(dir) ? readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => path.join(dir, name)) : [];
};
function job(body, status = "succeeded") {
  return { id: "00112233-4455-6677-8899-aabbccddeeff", request_key: body.request_key, request_hash: "a".repeat(64), input_hash: "b".repeat(64),
    provider: savedAnswer.provider, model: savedAnswer.model, status, result: status === "succeeded" ? savedAnswer : null,
    error_code: null, error_detail: null, error_status: null, retry_after: null };
}
function durableClient(box, fetch, options = {}) {
  return automationClient({ ...credentials(box), root: box.root, fetch: async (url, init) => {
    if (new URL(url).pathname === "/api/video/automation/settings") return Response.json({ durable_stage_runs: true, model: "new-model" });
    return fetch(url, init);
  }, sleep: async () => {} }, { durablePollMs: 5, durablePollIntervalMs: 5, ...options });
}
const runWriter = (client, payload = { text: "原稿", rows: [1, 2] }) => client.run("writer", DURABLE_SLUG, "Write exact source", payload);

test("durable writer persists its key and exact body before POST, then reconnects with the same key after a lost POST or body", async () => {
  for (const loss of ["socket", "body"]) {
    const box = sandbox(), posts = [];
    const client = durableClient(box, async (url, init) => {
      assert.equal(new URL(url).pathname, DURABLE_PATH);
      const body = JSON.parse(init.body), files = durableFiles(box);
      assert.equal(files.length, 1, "the request journal exists before dispatch");
      const persisted = JSON.parse(readFileSync(files[0], "utf8"));
      assert.equal(persisted.request_key, body.request_key);
      assert.deepEqual(persisted.request, Object.fromEntries(Object.entries(body).filter(([key]) => key !== "request_key")));
      posts.push(body);
      if (posts.length === 1) {
        if (loss === "socket") throw failed("UND_ERR_SOCKET");
        return new Response('{"id":', { status: 200 });
      }
      return Response.json(job(body));
    }, { durablePollMs: 5000, durablePollIntervalMs: 1 });
    await client.settings();
    assert.deepEqual(await runWriter(client), savedAnswer, loss);
    assert.equal(posts.length, 2, loss);
    assert.deepEqual(posts[0], posts[1], "a lost submit uses one server operation");
    assert.equal(durableFiles(box).length, 1, "a returned result survives until the unit is persisted");
    client.settleRuns([DURABLE_SLUG]);
    assert.deepEqual(durableFiles(box), []);
  }
});

test("a pending writer restarts with GET and returns the persisted result despite changed models, capability or budgets", async () => {
  const box = sandbox(), calls = [];
  let original;
  const first = durableClient(box, async (url, init) => {
    calls.push({ url, method: init.method });
    if (init.method === "POST") original = JSON.parse(init.body);
    return Response.json(job(original, "running"));
  });
  await first.settings();
  await assert.rejects(runWriter(first), (error) => error.code === RUN_PENDING && error.who === "service" && error.slug === DURABLE_SLUG && error.stage === "writer");
  assert.equal(calls.filter((call) => call.method === "POST").length, 1);
  const restarted = durableClient(box, async (url, init) => {
    assert.equal(init.method, "GET");
    assert.equal(new URL(url).pathname, `${DURABLE_PATH}/${job(original).id}`);
    assert.equal(new URL(url).searchParams.get("input_hash"), "b".repeat(64));
    return Response.json(job(original));
  });
  await restarted.settings();
  assert.deepEqual(await runWriter(restarted), savedAnswer);
  // A crash before settle leaves the completed result, available even without settings or HTTP.
  const disconnected = automationClient({ ...credentials(box), root: box.root, fetch: async () => assert.fail("completed results must be recovered before provider/budget checks") });
  assert.deepEqual(await runWriter(disconnected), savedAnswer);
  disconnected.settleRuns([DURABLE_SLUG]);
  assert.deepEqual(durableFiles(box), []);
});

test("malformed and rebound receipts preserve their saved key and never dispatch a replacement run", async () => {
  for (const wrong of ["key", "GET hash", "GET id", "journal"]) {
    const box = sandbox(), calls = [];
    let original;
    const client = durableClient(box, async (url, init) => {
      calls.push(init.method);
      if (init.method === "POST") original = JSON.parse(init.body);
      const answer = job(original, "running");
      if (wrong === "key") answer.request_key = "11112233-4455-6677-8899-aabbccddeeff";
      if (init.method === "GET" && wrong === "GET hash") answer.input_hash = "c".repeat(64);
      if (init.method === "GET" && wrong === "GET id") answer.id = "11112233-4455-6677-8899-aabbccddeeff";
      return Response.json(answer);
    }, { durablePollMs: 5000, durablePollIntervalMs: 1 });
    await client.settings();
    if (wrong === "journal") {
      const stopped = path.join(box.work, "STOP"); writeFileSync(stopped, "owner stop");
      await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING);
      writeFileSync(durableFiles(box)[0], '{"interrupted":');
    }
    await assert.rejects(runWriter(client), (error) => error.code === RUN_UNCERTAIN && error.who === "owner");
    assert.equal(calls.filter((method) => method === "POST").length, wrong === "journal" ? 0 : 1);
    assert.equal(durableFiles(box).length, 1);
    if (wrong !== "journal") {
      await assert.rejects(runWriter(client), (error) => [RUN_UNCERTAIN, RUN_PENDING].includes(error.code));
      assert.equal(calls.filter((method) => method === "POST").length, wrong === "key" ? 2 : 1,
        "a malformed initial receipt retries the same persisted key; a known receipt uses GET");
    }
  }
});

test("an uncertain writer needs explicit owner retry, while a stopped worker retains an undispatched journal", async () => {
  const box = sandbox();
  const keys = [];
  let original;
  const client = durableClient(box, async (_url, init) => {
    if (init.method === "GET") return Response.json(job(original, "uncertain"));
    assert.equal(init.method, "POST");
    const body = JSON.parse(init.body); keys.push(body.request_key); original = body;
    return Response.json(job(body, keys.length === 1 ? "uncertain" : "succeeded"));
  });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_UNCERTAIN && error.who === "owner");
  await assert.rejects(runWriter(client), (error) => error.code === RUN_UNCERTAIN);
  assert.equal(keys.length, 1, "uncertain runs are not re-dispatched automatically");
  await client.retryRuns(DURABLE_SLUG);
  assert.deepEqual(await runWriter(client), savedAnswer);
  assert.notEqual(keys[0], keys[1], "only the owner's retry permits a new operation");
  const stopped = sandbox(); writeFileSync(path.join(stopped.work, "STOP"), "stop");
  const held = durableClient(stopped, async () => assert.fail("STOP must prevent a new paid submit"));
  await held.settings();
  await assert.rejects(runWriter(held), (error) => error.code === RUN_PENDING);
  assert.equal(durableFiles(stopped).length, 1);
});

test("owner retry queries an uncertain run first and recovers its late completed answer without a second paid POST", async () => {
  const box = sandbox();
  let original, posts = 0, gets = 0;
  const client = durableClient(box, async (url, init) => {
    if (init.method === "POST") { posts++; original = JSON.parse(init.body); return Response.json(job(original, "uncertain")); }
    gets++;
    assert.equal(new URL(url).searchParams.get("input_hash"), "b".repeat(64));
    return Response.json(job(original));
  });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_UNCERTAIN);
  await client.retryRuns(DURABLE_SLUG, { requestId: "11112233-4455-6677-8899-aabbccddeeff", reason: "model run uncertain" });
  assert.deepEqual(await runWriter(client), savedAnswer);
  assert.equal(posts, 1);
  assert.equal(gets, 1);
});

test("a durable receipt keeps the chosen model alias while returning the upstream's exact reported model", async () => {
  const box = sandbox();
  const client = durableClient(box, async (_url, init) => Response.json({ ...job(JSON.parse(init.body)), model: "configured-model-alias" }));
  await client.settings();
  assert.deepEqual(await runWriter(client), savedAnswer);
  const saved = JSON.parse(readFileSync(durableFiles(box)[0], "utf8"));
  assert.equal(saved.receipt.model, "configured-model-alias");
  assert.equal(saved.receipt.result.model, savedAnswer.model);
});

test("owner retry for changed input archives verified stale success before one new source request", async () => {
  const box = sandbox();
  const posted = [];
  let original;
  const client = durableClient(box, async (_url, init) => {
    if (init.method === "GET") return Response.json(job(original));
    const body = JSON.parse(init.body); posted.push(body); original = body;
    return Response.json(job(body));
  });
  await client.settings();
  await runWriter(client);
  const changed = { text: "owner's changed source" };
  // Model a restarted worker whose prior successful result was never adopted into artifacts.
  const restarted = durableClient(box, async (_url, init) => {
    if (init.method === "GET") return Response.json(job(original));
    const body = JSON.parse(init.body); posted.push(body); return Response.json(job(body));
  });
  await restarted.settings();
  await assert.rejects(runWriter(restarted, changed), (error) => error.code === RUN_UNCERTAIN && /inputs changed/.test(error.why));
  const requestId = "11112233-4455-6677-8899-aabbccddeeff";
  await restarted.retryRuns(DURABLE_SLUG, { requestId, reason: "stage inputs changed while the previous result was unfinished" });
  const archive = path.join(box.work, DURABLE_SLUG, RUN_RECEIPTS_DIR, "archive");
  const archived = JSON.parse(readFileSync(path.join(archive, readdirSync(archive)[0]), "utf8"));
  assert.equal(archived.owner_retry.request_id, requestId);
  assert.equal(archived.receipt.result.text, savedAnswer.text);
  assert.deepEqual(await runWriter(restarted, changed), savedAnswer);
  assert.equal(posted.length, 2);
  assert.notEqual(posted[0].request_key, posted[1].request_key);
  assert.deepEqual(posted[1].payload, changed);
});

test("a failed owner retry lookup preserves the uncertain journal and never authorizes a new paid request", async () => {
  const box = sandbox();
  let original, posts = 0;
  const client = durableClient(box, async (_url, init) => {
    if (init.method === "POST") { posts++; original = JSON.parse(init.body); return Response.json(job(original, "uncertain")); }
    return Response.json({ code: "upstream_unavailable", detail: "Cannot read its current state" }, { status: 502 });
  });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_UNCERTAIN);
  await assert.rejects(client.retryRuns(DURABLE_SLUG), (error) => error.code === RUN_UNCERTAIN && /retained/.test(error.message));
  await assert.rejects(runWriter(client), (error) => error.code === RUN_UNCERTAIN);
  assert.equal(posts, 1);
  assert.equal(durableFiles(box).length, 1);
});

test("writer reconnect across midnight and shared lexicon changes uses the original saved operation", async () => {
  const box = sandbox();
  let original;
  const before = { text: "same approved source", today: "2026-10-04", lexicon: { terms: { GPU: "原唸法" } } };
  const first = durableClient(box, async (_url, init) => {
    if (init.method === "POST") original = JSON.parse(init.body);
    return Response.json(job(original, "running"));
  });
  await first.settings();
  await assert.rejects(runWriter(first, before), (error) => error.code === RUN_PENDING);
  const restarted = durableClient(box, async (_url, init) => {
    assert.equal(init.method, "GET", "derived context drift must not start a new model run");
    return Response.json(job(original));
  });
  const after = { ...before, today: "2026-10-05", lexicon: { terms: { GPU: "原唸法", CPU: "另一工作新增" } } };
  assert.deepEqual(await runWriter(restarted, after), savedAnswer);
  assert.deepEqual(JSON.parse(readFileSync(durableFiles(box)[0], "utf8")).request.payload, before);
});

test("definitive failed receipts surface their stored error, and input changes cannot replace an unfinished writer", async () => {
  const box = sandbox(), posted = [];
  const client = durableClient(box, async (_url, init) => {
    const body = JSON.parse(init.body); posted.push(body);
    return Response.json({ ...job(body, "failed"), error_code: "video_ai_upstream_busy", error_detail: "Saved vendor refusal", error_status: 503, retry_after: "2026-10-04T15:00:00Z" });
  });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === "video_ai_upstream_busy" && error.status === 503 && error.message === "Saved vendor refusal" && error.retry_after === "2026-10-04T15:00:00Z");
  assert.deepEqual(durableFiles(box), [], "the server definitively settled this failure");
  const pendingBox = sandbox();
  const pending = durableClient(pendingBox, async (_url, init) => Response.json(job(JSON.parse(init.body), "running")));
  await pending.settings();
  await assert.rejects(runWriter(pending), (error) => error.code === RUN_PENDING);
  await assert.rejects(runWriter(pending, { text: "new source" }), (error) => error.code === RUN_UNCERTAIN && error.who === "owner" && /inputs changed/.test(error.why));
  assert.equal(durableFiles(pendingBox).length, 1);
});

test("durable capability preserves the synchronous planner and bounded anime/story writer checkpoints", async () => {
  const box = sandbox(), paths = [];
  const client = durableClient(box, async (url) => { paths.push(new URL(url).pathname); return Response.json(savedAnswer); });
  await client.settings();
  assert.deepEqual(await client.run("planner", "draft-example", "Plan", {}), savedAnswer);
  for (const variant of ["anime-act", "story"]) {
    const slug = `${variant}-example`;
    assert.deepEqual(await client.run("writer", slug, "Write a bounded chapter", {}, 16_000, "drama", variant), savedAnswer, variant);
    assert.deepEqual(durableFiles(box, slug), [], `${variant}: checkpoint transport creates no generic run receipt`);
  }
  assert.deepEqual(paths, Array(3).fill("/api/video/automation/run"));
  assert.deepEqual(durableFiles(box, "draft-example"), []);
});

test("the durable polling window caps at 25 seconds and leaves the paid operation saved for the next round", async () => {
  const box = sandbox(), sleeps = [], calls = [];
  let original;
  const client = automationClient({ ...credentials(box), root: box.root, sleep: async (ms) => sleeps.push(ms), fetch: async (url, init) => {
    if (new URL(url).pathname.endsWith("/settings")) return Response.json({ durable_stage_runs: true });
    calls.push(init.method);
    if (init.method === "POST") original = JSON.parse(init.body);
    return Response.json(job(original, "running"));
  } }, { durablePollMs: 295_000, durablePollIntervalMs: 25_000 });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING);
  assert.equal(calls.filter((method) => method === "POST").length, 1);
  assert.ok(sleeps.length > 0 && sleeps.every((ms) => ms > 0) && sleeps.reduce((total, ms) => total + ms, 0) <= 25_000);
  assert.equal(durableFiles(box).length, 1);
});
