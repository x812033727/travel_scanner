import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main as runCli } from "../cli.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { AutomationError, automationClient, PAUSE_CODES, POLICY_HOLD, RUN_PENDING, RUN_UNCERTAIN } from "./client.mjs";
import { AUTO_ARCHIVE_REASON, INPUT_CHANGED_CODE, INPUT_CHANGED_MESSAGE, jobGoneReason, RUN_RECEIPTS_DIR, runReceiptStore } from "./run-receipts.mjs";

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

test("an error keeps the seconds of the server's Retry-After, for a stage run and for any other request; without the header, or with a date in it, it carries none", async () => {
  const box = sandbox();
  let answer;
  const sleeps = [];
  const client = automationClient({ ...credentials(box), fetch: async () => answer(), sleep: async (ms) => sleeps.push(ms) }, { attempts: 2 });
  const refused = (status, code, after) => () => Response.json({ code, detail: "later" }, { status, headers: after === undefined ? {} : { "Retry-After": after } });
  // Before: only a durable writer's failed receipt carried it, so flow.mjs deferred every other request by its own clock.
  answer = refused(429, "rate_limit_exceeded", "900");
  await assert.rejects(client.run("verifier", "draft-example", "Check", {}), (error) => error.status === 429 && error.retry_after === 900);
  assert.deepEqual(sleeps, [120_000, 120_000], "the client's own sleeps stay capped at two minutes");
  await assert.rejects(client.reviews("draft-example"), (error) => error.code === "rate_limit_exceeded" && error.retry_after === 900);
  answer = refused(503, "video_ai_upstream_busy", "30");
  await assert.rejects(client.run("translator", "draft-example", "Translate", {}), (error) => error.code === "video_ai_upstream_busy" && error.retry_after === 30);
  // A refusal that is thrown at once keeps it too.
  answer = refused(409, "video_ai_project_dropped", "60");
  await assert.rejects(client.run("planner", "draft-example", "Plan", {}), (error) => error.status === 409 && error.retry_after === 60);
  for (const after of [undefined, "0", "Wed, 21 Oct 2026 07:28:00 GMT"]) {
    answer = refused(503, "video_ai_upstream_busy", after);
    await assert.rejects(client.run("planner", "draft-example", "Plan", {}), (error) => error.status === 503 && !("retry_after" in error), String(after));
  }
});

// Every subscription account rests: at its usage cap, or because its CLI can no longer
// authenticate (the API's video_ai_subscription_auth_failed, 503 with a retry_after). Nothing
// ran either way; the run ends and the worker's next round asks again.
test("a subscription whose every account cannot authenticate pauses the run like one at its cap: one request, no wait, not the owner's", async () => {
  assert.deepEqual([...PAUSE_CODES].sort(), ["video_ai_subscription_auth_failed", "video_ai_subscription_paused"]);
  for (const [code, status, detail] of [
    ["video_ai_subscription_paused", 429, "every Claude account is at or above 80%"],
    ["video_ai_subscription_auth_failed", 503, "every subscription account's CLI failed to authenticate; sign one in again on /admin/ai-accounts"],
  ]) {
    const box = sandbox();
    let calls = 0;
    const sleeps = [];
    const client = automationClient({
      ...credentials(box),
      fetch: async () => {
        calls++;
        return Response.json({ code, detail }, { status, headers: { "Retry-After": "900" } });
      },
      sleep: async (ms) => sleeps.push(ms),
    }, { attempts: 3 });
    await assert.rejects(client.run("writer", "draft-example", "Write a video", {}), (error) => {
      assert.ok(error instanceof AutomationError, code);
      assert.equal(error.code, code);
      assert.equal(error.status, status);
      assert.equal(error.message, detail);
      assert.notEqual(error.who, "owner", `${code}: auto ends with exit 4 and the next round tries again, as for a pause`);
      return true;
    });
    assert.equal(calls, 1, `${code}: asked once in the run`);
    assert.deepEqual(sleeps, [], `${code}: not retried within the run`);
  }
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
    // The limiter answers its code with 503 only; the code on another status is not the limiter's.
    ["the limiter's code on a status it never answers", () => Response.json({ code: "rate_limit_unavailable", detail: "安全驗證服務暫時無法使用" }, { status: 502 }), 502],
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
      assert.match(error.message, /no answer came back.*the model may have run, so it is not sent again/, what);
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
    // The API's limiter could not count the request (app/infra.py), before the route ran.
    ["the API's limiter away", () => Response.json({ code: "rate_limit_unavailable", detail: "安全驗證服務暫時無法使用" }, { status: 503 })],
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
  // A read and a review submit spend nothing: a gateway's 500 and a dropped submit are asked again.
  let reads = 0;
  const reader = automationClient({ ...credentials(sandbox()), fetch: async () => (++reads === 1 ? Response.json({ detail: "Internal Server Error" }, { status: 500 }) : Response.json({ reviews: [] })), sleep: async () => {} });
  assert.deepEqual(await reader.reviews("long-video"), { reviews: [] });
  assert.equal(reads, 2);
  let submits = 0;
  const submitter = automationClient({ ...credentials(sandbox()), fetch: async () => {
    if (++submits === 1) throw failed("UND_ERR_SOCKET");
    return Response.json({ id: "r1" }, { status: 201 });
  }, sleep: async () => {} });
  assert.deepEqual(await submitter.submit("long-video", { gate: "outline" }), { id: "r1" });
  assert.equal(submits, 2);
});

// A Jev judgement takes one call off the daily Jev budget before Jev is asked
// (apps/api/app/video_automation/judge.py `_ask`): like a stage run, it is not asked again once it
// was sent and its answer lost, and a verdict that did come back is returned exactly as it came.
const JUDGES = [
  ["judgePolicy", "/api/video/automation/judge/policy", { slug: "long-video", script: "旁白", viewpoint: "" },
    { stance: 0.31, demo: 0.82, advice: 0.04, sponsored: 0.02, passed: false, note: "Jev：立場 0.31；沒過（立場低於 0.6）", questions: "tutorial", observation: null, disparage: null }],
  ["judgeOutline", "/api/video/automation/judge/outline", { slug: "long-video", brief: "企劃", options: [{ key: "A", title: "a", summary: "s", hook: "h" }, { key: "B", title: "b", summary: "s", hook: "h" }] },
    { choice: "B", probabilities: { A: 0.45, B: 0.55 }, options: { A: { stance: 0.5, demo: 0.4 }, B: { stance: 0.55, demo: 0.6 } }, advice: 0.1, passed: false, note: "Jev 挑了 B（0.55）；沒過關" }],
];

test("a Jev judgement sent and left without its answer is not asked again: a dropped connection, a broken body, a gateway, the judge route's lost answer, a 502 with another code", async () => {
  const lost = [
    ["a connection reset after sending", () => {
      throw failed("ECONNRESET");
    }, 0],
    ["a connection dropped mid-way", () => {
      throw failed("UND_ERR_SOCKET");
    }, 0],
    ["Node's deadline for the headers", () => {
      throw failed("UND_ERR_HEADERS_TIMEOUT");
    }, 0],
    ["a verdict that breaks off", () => new Response('{"stance": 0.3, "passed": fal', { status: 200, headers: { "Content-Type": "application/json" } }), 200],
    ["an error without the API's code", () => Response.json({ detail: "Internal Server Error" }, { status: 500 }), 500],
    // The limiter answers its code with 503 only; the code on another status is not the limiter's.
    ["the limiter's code on a status it never answers", () => Response.json({ code: "rate_limit_unavailable", detail: "安全驗證服務暫時無法使用" }, { status: 502 }), 502],
    ["a gateway's timeout page", () => new Response("<html>504 Gateway Time-out</html>", { status: 504, headers: { "Content-Type": "text/html" } }), 504],
    // The judge routes name their own lost answer (JUDGE_LOST in apps/web/app/api/video/speech/forward.ts).
    ["the judge route's lost answer", () => Response.json({ code: "video_judge_answer_lost", detail: "請求已送到 API" }, { status: 504 }), 504],
    // Only the route's never-reached 502 settles a judgement; the API's 502 for a Jev call whose
    // outcome it cannot tell (2026-10-05-jev-judge-endpoints-report-an-uncertain) does not.
    ["the API's uncertain Jev outcome", () => Response.json({ code: "video_judge_outcome_uncertain", detail: "Jev 可能已經判斷" }, { status: 502 }), 502],
  ];
  for (const [method, route, body] of JUDGES) {
    for (const [what, answer, status] of lost) {
      const calls = [];
      const sleeps = [];
      const client = automationClient({
        ...credentials(sandbox()),
        fetch: async (url, init) => {
          calls.push({ path: new URL(url).pathname, method: init.method, body: JSON.parse(init.body) });
          return answer();
        },
        sleep: async (ms) => sleeps.push(ms),
      });
      await assert.rejects(client[method](body), (error) => {
        assert.ok(error instanceof AutomationError, `${method}, ${what}`);
        assert.equal(error.code, RUN_UNCERTAIN, `${method}, ${what}`);
        assert.equal(error.who, "service", `${method}, ${what}: the caller leaves it for a later round`);
        assert.equal(error.status, status, `${method}, ${what}`);
        assert.match(error.message, /no answer came back.*Jev may have run, so it is not sent again/, `${method}, ${what}`);
        return true;
      });
      assert.deepEqual(calls, [{ path: route, method: "POST", body }], `${method}, ${what}: sent once`);
      assert.deepEqual(sleeps, [], `${method}, ${what}: no wait for a second try`);
    }
  }
});

test("a Jev judgement that never reached a server, or that the API settled, is asked again and its failed verdict comes back unchanged", async () => {
  const settled = [
    ["a refused connection", () => {
      throw failed("ECONNREFUSED");
    }],
    ["an unknown host", () => {
      throw failed("ENOTFOUND");
    }],
    // The judge routes keep this 502 for an API they never reached (forward.ts); a lost answer is their 504 above.
    ["the judge route's 502, an API it never reached", () => Response.json({ code: "upstream_unavailable", detail: "API 服務目前無法回應" }, { status: 502 })],
    ["the API's answer after Jev failed", () => Response.json({ code: "video_judge_upstream_failed", detail: "Jev 暫時無法判斷" }, { status: 502 })],
    ["the judge's hourly limit", () => Response.json({ code: "rate_limit_exceeded", detail: "slow down" }, { status: 429 })],
    ["the spent Jev budget", () => Response.json({ code: "jev_budget_exhausted", detail: "今天的 Jev 呼叫次數已用完" }, { status: 429 })],
    ["the API's limiter away", () => Response.json({ code: "rate_limit_unavailable", detail: "安全驗證服務暫時無法使用" }, { status: 503 })],
  ];
  for (const [method, route, body, verdict] of JUDGES) {
    for (const [what, answer] of settled) {
      const calls = [];
      const client = automationClient({
        ...credentials(sandbox()),
        fetch: async (url, init) => {
          calls.push({ path: new URL(url).pathname, body: JSON.parse(init.body) });
          return calls.length === 1 ? answer() : Response.json(verdict);
        },
        sleep: async () => {},
      });
      assert.deepEqual(await client[method](body), verdict, `${method}, ${what}: the verdict as Jev gave it`);
      assert.deepEqual(calls, [{ path: route, body }, { path: route, body }], `${method}, ${what}: the same request asked again`);
    }
  }
});

test("a Jev judgement whose route never reaches the API is asked within the bounded attempts, then left for a later round", async () => {
  for (const [method, route, body] of JUDGES) {
    const calls = [];
    const client = automationClient({
      ...credentials(sandbox()),
      fetch: async (url) => {
        calls.push(new URL(url).pathname);
        return Response.json({ code: "upstream_unavailable", detail: "API 服務目前無法回應" }, { status: 502 });
      },
      sleep: async () => {},
    }, { attempts: 2 });
    await assert.rejects(client[method](body), (error) => {
      assert.ok(error instanceof AutomationError, method);
      assert.equal(error.code, "upstream_unavailable", method);
      assert.equal(error.status, 502, method);
      assert.equal(error.who, "service", `${method}: the caller leaves it for a later round`);
      return true;
    });
    assert.deepEqual(calls, [route, route], `${method}: no more than the attempts it was given`);
  }
});

test("a judge's refusal is thrown after one request, with the status its callers read", async () => {
  const refusals = [
    [409, "video_judge_not_enabled", "頻道立場還是空白"],
    [404, "", "Not Found"],
    [422, "video_judge_invalid", "Jev 拒絕這個問題"],
  ];
  for (const [method, , body] of JUDGES) {
    for (const [status, code, detail] of refusals) {
      let calls = 0;
      const client = automationClient({ ...credentials(sandbox()), fetch: async () => {
        calls++;
        return Response.json({ code, detail }, { status });
      }, sleep: async () => {} });
      await assert.rejects(client[method](body), (error) => error instanceof AutomationError && error.status === status && error.code === code && error.message === detail);
      assert.equal(calls, 1, `${method}, ${status}`);
    }
  }
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

test("a translation's translator and caption reviewer are durable jobs too: a lost submit, a lost body or a restart reconnects to the same operation", async () => {
  for (const [stage, variant] of [["translator", null], ["caption_reviewer", null], ["translator", "shorten"]]) {
    const box = sandbox(), posts = [], lookups = [];
    const translate = (client) => client.run(stage, DURABLE_SLUG, "Translate the worksheet", { locale: "en", worksheet: { lines: [{ id: "k7p2", source: "原句" }] } }, 32_000, "slides", variant);
    let original = null;
    const answer = (status) => async (url, init) => {
      if (init.method === "GET") { lookups.push(new URL(url).pathname); return Response.json(job(original, status)); }
      assert.equal(new URL(url).pathname, DURABLE_PATH, "never the synchronous route");
      const body = JSON.parse(init.body);
      original ??= body;
      posts.push(body);
      if (posts.length === 1) throw failed("UND_ERR_SOCKET");
      if (posts.length === 2) return new Response('{"id":', { status: 200 });
      return Response.json(job(body, status));
    };
    const first = durableClient(box, answer("running"), { durablePollMs: 5000, durablePollIntervalMs: 1 });
    await first.settings();
    await assert.rejects(translate(first), (error) => error.code === RUN_PENDING && error.stage === stage, stage);
    assert.equal(new Set(posts.map((body) => body.request_key)).size, 1, `${stage}: one server operation for the lost submit and the lost body`);
    assert.equal(posts.at(-1).stage, stage);
    assert.equal(posts.at(-1).variant ?? null, variant);
    lookups.length = 0;
    const restarted = durableClient(box, answer("succeeded"));
    await restarted.settings();
    assert.deepEqual(await translate(restarted), savedAnswer, `${stage}: the restarted worker takes the same job's answer`);
    assert.equal(posts.length, 3, `${stage}: the restart looks the job up and posts nothing`);
    assert.equal(lookups.length, 1);
    restarted.settleRuns([DURABLE_SLUG]);
    assert.deepEqual(durableFiles(box), []);
  }
});

test("a project STOP keeps a translation unit from being submitted; its request key waits for the resume", async () => {
  for (const stage of ["translator", "caption_reviewer"]) {
    const box = sandbox();
    let posts = 0;
    const client = durableClient(box, async (_url, init) => {
      posts++;
      return Response.json(job(JSON.parse(init.body)));
    });
    await client.settings();
    const stop = path.join(box.work, DURABLE_SLUG, "STOP");
    mkdirSync(path.dirname(stop), { recursive: true });
    writeFileSync(stop, "owner hold");
    const translate = () => client.run(stage, DURABLE_SLUG, "Translate", { locale: "en", worksheet: { lines: [] } }, 32_000);
    await assert.rejects(translate(), (error) => error.code === RUN_PENDING, stage);
    assert.equal(posts, 0, `${stage}: nothing is sent under STOP`);
    const [file] = durableFiles(box);
    const key = JSON.parse(readFileSync(file, "utf8")).request_key;
    rmSync(stop);
    assert.deepEqual(await translate(), savedAnswer);
    assert.equal(posts, 1);
    assert.equal(JSON.parse(readFileSync(file, "utf8")).request_key, key, `${stage}: the resumed submit keeps the key saved under STOP`);
  }
});

test("a translation stays on the synchronous route while the site has not turned durable runs on", async () => {
  const box = sandbox(), routes = [];
  const client = automationClient({ ...credentials(box), root: box.root, sleep: async () => {}, fetch: async (url, init) => {
    const route = new URL(url).pathname;
    routes.push(route);
    if (route.endsWith("/settings")) return Response.json({ durable_stage_runs: false });
    return Response.json(savedAnswer);
  } });
  await client.settings();
  for (const stage of ["translator", "caption_reviewer"]) assert.deepEqual(await client.run(stage, DURABLE_SLUG, "Translate", { locale: "en" }), savedAnswer);
  assert.deepEqual(routes.slice(1), ["/api/video/automation/run", "/api/video/automation/run"]);
  assert.deepEqual(durableFiles(box), []);
});

test("a pending writer says why its last look failed, only while it did: a read after a 429 clears it, and a POST the server never confirmed has no receipt", async () => {
  const limited = () => Response.json({ code: "rate_limit_exceeded", detail: "請求過於頻繁，請稍後再試" }, { status: 429 });
  // Every look at the saved job's receipt meets the rate limit: the cause and the last status the server gave.
  let box = sandbox();
  let original;
  let lookups = 0;
  let client = durableClient(box, async (url, init) => {
    if (init.method === "POST") { original = JSON.parse(init.body); return Response.json(job(original, "running")); }
    lookups += 1;
    return limited();
  }, { durablePollMs: 5000, durablePollIntervalMs: 1 });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING && error.polling === "請求過於頻繁，請稍後再試" && error.receipt_status === "running");
  assert.ok(lookups >= 1);
  // A 429 and then a read that says running: the server's own word replaces the failed look.
  box = sandbox();
  lookups = 0;
  client = durableClient(box, async (url, init) => {
    if (init.method === "POST") { original = JSON.parse(init.body); return Response.json(job(original, "running")); }
    lookups += 1;
    return lookups === 1 ? limited() : Response.json(job(original, "running"));
  }, { durablePollMs: 3000, durablePollIntervalMs: 1000 });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING && error.polling === null && error.receipt_status === "running");
  // The fake sleeps alone use the budget up: the POST, the 429, then the read that clears it.
  assert.equal(lookups, 2);
  // The round's own budget cuts off a read of a job the server already confirmed: no lookup failed.
  box = sandbox();
  let reads = 0;
  client = durableClient(box, async (url, init) => {
    if (init.method === "POST") { original = JSON.parse(init.body); return Response.json(job(original, "running")); }
    reads += 1;
    // A read that answers only once aborted; the timer keeps the process up meanwhile, as a socket would.
    return new Promise((_resolve, reject) => {
      const open = setTimeout(() => {}, 10_000);
      init.signal.addEventListener("abort", () => { clearTimeout(open); reject(init.signal.reason); });
    });
  }, { durablePollMs: 1500, durablePollIntervalMs: 1500 });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING && error.polling === null && error.receipt_status === "running");
  assert.equal(reads, 1, "the read the budget cut off");
  // The POST itself is refused for a while: no job was confirmed, so there is no receipt status.
  box = sandbox();
  let posts = 0;
  client = durableClient(box, async () => { posts += 1; return limited(); }, { durablePollMs: 5000, durablePollIntervalMs: 1 });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING && error.polling === "請求過於頻繁，請稍後再試" && error.receipt_status === null);
  assert.equal(posts, 4, "the same key, sent the client's attempts and no more");
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

test("a client lists a video's saved runs whose answer is still to be taken, from the journals alone: a pending discussion until its unit settles it, and none for a journal that cannot be read", async () => {
  const box = sandbox(), requests = [];
  let original;
  let status = "running";
  const client = durableClient(box, async (url, init) => {
    requests.push(init.method);
    if (init.method === "POST") original = JSON.parse(init.body);
    return Response.json(job(original, status));
  });
  await client.settings();
  const discuss = (from) => from.run("writer", DURABLE_SLUG, "Answer the owner's line", { message: "沈瀾為什麼不回答？" }, 16_000, "drama", "discuss");
  const listed = (state) => [{ stage: "writer", variant: "discuss", status: state }];
  assert.deepEqual(client.untakenRuns(DURABLE_SLUG), []);
  await assert.rejects(discuss(client), (error) => error.code === RUN_PENDING && error.slug === DURABLE_SLUG);
  const sent = requests.length;
  assert.deepEqual(client.untakenRuns(DURABLE_SLUG), listed("running"));
  // The next round is another process: it reads the same, and asks the server nothing for it.
  const restarted = durableClient(box, async () => assert.fail("listing the saved runs sends nothing"));
  assert.deepEqual(restarted.untakenRuns(DURABLE_SLUG), listed("running"));
  assert.deepEqual(restarted.untakenRuns("another-video"), []);
  assert.equal(requests.length, sent);
  // The answer arrives: still to be taken until the unit that used it settles the journal.
  status = "succeeded";
  assert.deepEqual(await discuss(client), savedAnswer);
  assert.deepEqual(client.untakenRuns(DURABLE_SLUG), listed("succeeded"));
  client.settleRuns([DURABLE_SLUG]);
  assert.deepEqual(client.untakenRuns(DURABLE_SLUG), []);

  // A journal that cannot be read is the business of the stage that owns it, which blocks the video with the reason.
  status = "running";
  await assert.rejects(discuss(client), (error) => error.code === RUN_PENDING);
  writeFileSync(durableFiles(box)[0], "{ not json");
  assert.deepEqual(client.untakenRuns(DURABLE_SLUG), []);
  await assert.rejects(discuss(client), (error) => error.code === RUN_UNCERTAIN && /unreadable/.test(error.message));
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

const archiveOf = (box) => {
  const dir = path.join(box.work, DURABLE_SLUG, RUN_RECEIPTS_DIR, "archive");
  return readdirSync(dir).map((name) => JSON.parse(readFileSync(path.join(dir, name), "utf8")));
};

test("a stale journal whose run succeeded is archived by the worker after one lookup, and one new source request follows", async () => {
  const box = sandbox();
  const posted = [];
  let original, gets = 0;
  const client = durableClient(box, async (_url, init) => {
    if (init.method === "GET") return Response.json(job(original));
    const body = JSON.parse(init.body); posted.push(body); original = body;
    return Response.json(job(body));
  });
  await client.settings();
  await runWriter(client);
  const changed = { text: "a deploy changed the prompt" };
  // Model a restarted worker whose prior successful result was never adopted into artifacts.
  const restarted = durableClient(box, async (url, init) => {
    if (init.method === "GET") { gets++; assert.equal(new URL(url).searchParams.get("input_hash"), "b".repeat(64)); return Response.json(job(original)); }
    const body = JSON.parse(init.body); posted.push(body); return Response.json(job(body));
  });
  await restarted.settings();
  assert.deepEqual(await runWriter(restarted, changed), savedAnswer, "no owner retry is needed: the spent run is over");
  assert.equal(gets, 1, "the stale job is looked up exactly once");
  assert.equal(posted.length, 2, "exactly one new POST follows");
  assert.notEqual(posted[0].request_key, posted[1].request_key);
  assert.deepEqual(posted[1].payload, changed);
  const [archived] = archiveOf(box);
  assert.equal(archived.request_key, posted[0].request_key);
  assert.equal(archived.owner_retry.request_id, null, "no owner request id was consumed");
  assert.equal(archived.owner_retry.reason, AUTO_ARCHIVE_REASON);
  assert.equal(archived.receipt.result.text, savedAnswer.text, "the paid answer is kept for inspection");
  assert.equal(durableFiles(box).length, 1, "only the new request's journal remains");
  assert.equal(JSON.parse(readFileSync(durableFiles(box)[0], "utf8")).request_key, posted[1].request_key);
});

test("a stale journal that never reached the server is archived without a lookup, then the current request is sent", async () => {
  const box = sandbox();
  writeFileSync(path.join(box.work, "STOP"), "stop");
  const held = durableClient(box, async () => assert.fail("STOP must prevent a new paid submit"));
  await held.settings();
  await assert.rejects(runWriter(held), (error) => error.code === RUN_PENDING);
  const [undispatched] = durableFiles(box);
  const key = JSON.parse(readFileSync(undispatched, "utf8")).request_key;
  const { unlinkSync } = await import("node:fs");
  unlinkSync(path.join(box.work, "STOP"));
  const calls = [];
  const client = durableClient(box, async (_url, init) => {
    calls.push(init.method);
    assert.equal(init.method, "POST", "a journal with no receipt has no job to look up");
    return Response.json(job(JSON.parse(init.body)));
  });
  await client.settings();
  assert.deepEqual(await runWriter(client, { text: "the owner edited the stance" }), savedAnswer);
  assert.deepEqual(calls, ["POST"]);
  const [archived] = archiveOf(box);
  assert.equal(archived.request_key, key);
  assert.equal(archived.receipt, null);
  assert.deepEqual({ ...archived.owner_retry, archived_at: null }, { request_id: null, reason: AUTO_ARCHIVE_REASON, archived_at: null });
  assert.notEqual(JSON.parse(readFileSync(durableFiles(box)[0], "utf8")).request_key, key);
});

test("a stale journal whose run is uncertain still needs the owner, and a lookup that fails waits instead of blocking", async () => {
  for (const answer of ["uncertain", "HTTP 502", "connection lost", "half a body"]) {
    const box = sandbox(), posts = [];
    let original, gets = 0, stale = false;
    const client = durableClient(box, async (_url, init) => {
      if (init.method === "POST") { original = JSON.parse(init.body); posts.push(original); return Response.json(job(original, "running")); }
      // The first round's own poll sees a running job; the answers below are for the stale lookup.
      if (!stale) return Response.json(job(original, "running"));
      gets++;
      if (answer === "uncertain") return Response.json({ ...job(original, "uncertain"), error_detail: "HTTP 403: the subscription refused this run", error_status: 403 });
      if (answer === "HTTP 502") return Response.json({ code: "upstream_unavailable", detail: "Cannot read its current state" }, { status: 502 });
      if (answer === "half a body") return new Response('{"id":', { status: 200, headers: { "Content-Type": "application/json" } });
      throw Object.assign(new TypeError("fetch failed"), { cause: { code: "ECONNRESET", message: "socket hang up" } });
    });
    await client.settings();
    await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING, answer);
    const [file] = durableFiles(box), before = readFileSync(file, "utf8");
    const changed = { text: "a deploy changed the prompt" };
    stale = true;
    if (answer === "uncertain") {
      await assert.rejects(runWriter(client, changed), (error) => {
        assert.equal(error.code, RUN_UNCERTAIN); assert.equal(error.who, "owner"); assert.equal(error.receipt_code, INPUT_CHANGED_CODE);
        assert.equal(error.slug, DURABLE_SLUG); assert.equal(error.stage, "writer");
        // The owner's card (flow.mjs unanswered) shows the saved run's own cause before the input-changed sentence.
        assert.equal(error.message, `HTTP 403: the subscription refused this run; ${INPUT_CHANGED_MESSAGE}`);
        assert.equal(error.why, error.message);
        return true;
      }, answer);
    } else {
      await assert.rejects(runWriter(client, changed), (error) => error.code === RUN_PENDING && error.slug === DURABLE_SLUG && error.stage === "writer" && /could not be looked up/.test(error.message), answer);
    }
    assert.equal(gets, 1, answer);
    assert.equal(posts.length, 1, `${answer}: the stale run is never paid for again and no new run starts`);
    assert.deepEqual(durableFiles(box), [file], answer);
    if (answer !== "uncertain") assert.equal(readFileSync(file, "utf8"), before, `${answer}: the journal is intact`);
    else assert.equal(JSON.parse(readFileSync(file, "utf8")).receipt.status, "uncertain", "the lookup's answer is recorded for the owner");
  }
});

test("a stale journal whose lookup answers a settled 4xx is archived with the answer named, and one new request follows; 408 and 429 wait", async () => {
  for (const [status, code] of [[404, "video_ai_job_not_found"], [409, "video_ai_job_input_changed"], [422, ""], [408, ""], [429, "rate_limit_exceeded"]]) {
    const box = sandbox(), posted = [];
    let original, stale = false, gets = 0;
    const client = durableClient(box, async (_url, init) => {
      if (init.method === "POST") { const body = JSON.parse(init.body); posted.push(body); original ??= body; return Response.json(job(body, body === original ? "running" : "succeeded")); }
      if (!stale) return Response.json(job(original, "running"));
      gets++;
      return Response.json({ code, detail: code ? `the server says ${code}` : "" }, { status });
    });
    await client.settings();
    await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING, status);
    const [file] = durableFiles(box), before = readFileSync(file, "utf8");
    stale = true;
    const changed = { text: "a deploy changed the prompt" };
    if ([408, 429].includes(status)) {
      await assert.rejects(runWriter(client, changed), (error) => error.code === RUN_PENDING && /could not be looked up/.test(error.message)
        && error.polling === (code ? `the server says ${code}` : `HTTP ${status}`) && error.receipt_status === "running", status);
      assert.deepEqual(durableFiles(box), [file], status);
      assert.equal(readFileSync(file, "utf8"), before, `${status}: the journal is intact for the next round`);
      assert.equal(posted.length, 1, status);
    } else {
      assert.deepEqual(await runWriter(client, changed), savedAnswer, status);
      assert.equal(posted.length, 2, `${status}: exactly one new POST follows`);
      assert.deepEqual(posted[1].payload, changed, status);
      const [archived] = archiveOf(box);
      assert.equal(archived.request_key, posted[0].request_key, status);
      assert.equal(archived.receipt.status, "running", `${status}: the receipt bytes are kept`);
      assert.deepEqual({ ...archived.owner_retry, archived_at: null }, { request_id: null, reason: jobGoneReason({ status, code }), archived_at: null }, status);
      assert.equal(durableFiles(box).length, 1, status);
    }
    assert.equal(gets, 1, `${status}: the stale job is looked up once`);
  }
});

test("an owner retry on a still-running stale journal waits without consuming the request, and clears a plain failed journal", async () => {
  const box = sandbox();
  let original, gets = 0;
  const client = durableClient(box, async (_url, init) => {
    if (init.method === "POST") { original = JSON.parse(init.body); return Response.json(job(original, "running")); }
    gets++;
    return Response.json(job(original, "queued"));
  });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING);
  const [file] = durableFiles(box);
  const authorization = { requestId: "11112233-4455-6677-8899-aabbccddeeff", reason: "writer may have run on the server (stage inputs changed while a saved run is unfinished)" };
  gets = 0;
  await assert.rejects(client.retryRuns(DURABLE_SLUG, authorization), (error) => error.code === RUN_PENDING && error.slug === DURABLE_SLUG && error.stage === "writer");
  assert.equal(gets, 1, "the retry looks the job up once");
  assert.deepEqual(durableFiles(box), [file], "the running journal stays for the next round");
  assert.equal(JSON.parse(readFileSync(file, "utf8")).receipt.status, "queued");
  assert.equal(existsSync(path.join(path.dirname(file), "archive")), false);
  // A plain failure left on disk (the process died before removeFailed) is cleared by the retry.
  const failedBox = sandbox(), store = runReceiptStore({ ...credentials(failedBox), root: failedBox.root }, SITE);
  const entry = store.prepare({ stage: "writer", slug: DURABLE_SLUG, instructions: "Write exact source", payload: { text: "原稿" } });
  store.receive(entry, { ...job({ request_key: entry.record.request_key }, "failed"), error_code: "video_ai_upstream_failed", error_detail: "vendor error", error_status: 502 });
  const quiet = durableClient(failedBox, async () => assert.fail("a settled failure needs no lookup"));
  await quiet.settings();
  const stop = path.join(failedBox.work, DURABLE_SLUG, "STOP");
  writeFileSync(stop, "hold");
  await assert.rejects(quiet.retryRuns(DURABLE_SLUG, authorization), (error) => error.code === RUN_UNCERTAIN && /STOP/.test(error.message));
  assert.ok(existsSync(entry.file), "nothing is mutated under a STOP file");
  const { unlinkSync } = await import("node:fs");
  unlinkSync(stop);
  await quiet.retryRuns(DURABLE_SLUG, authorization);
  assert.deepEqual(durableFiles(failedBox), []);
  assert.equal(existsSync(path.join(path.dirname(entry.file), "archive")), false, "a failure is deleted, not archived");
  // The job the owner wants replaced is gone from the server (a re-pair): the retry archives
  // the journal instead of looping on "could not verify" every round.
  const goneBox = sandbox();
  let goneOriginal, goneStale = false;
  const goneClient = durableClient(goneBox, async (_url, init) => {
    if (init.method === "POST") { goneOriginal = JSON.parse(init.body); return Response.json(job(goneOriginal, "running")); }
    if (!goneStale) return Response.json(job(goneOriginal, "running"));
    return Response.json({ code: "video_ai_job_not_found", detail: "no job for this token" }, { status: 404 });
  });
  await goneClient.settings();
  await assert.rejects(runWriter(goneClient), (error) => error.code === RUN_PENDING);
  goneStale = true;
  await goneClient.retryRuns(DURABLE_SLUG, authorization);
  assert.deepEqual(durableFiles(goneBox), []);
  const [goneArchived] = archiveOf(goneBox);
  assert.equal(goneArchived.owner_retry.reason, jobGoneReason({ status: 404, code: "video_ai_job_not_found" }));
  assert.equal(goneArchived.owner_retry.request_id, null);
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

test("a running journal whose lookup answers a settled 4xx says the job is gone and stays in place; only the owner's retry of a job_gone block archives it, and one new request follows", async () => {
  for (const [status, code] of [[404, "video_ai_job_not_found"], [409, "video_ai_job_input_changed"], [400, "video_ai_receipt_invalid"]]) {
    const box = sandbox(), posted = [];
    let lost = false, gets = 0;
    const client = durableClient(box, async (_url, init) => {
      if (init.method === "POST") { const body = JSON.parse(init.body); posted.push(body); return Response.json(job(body, posted.length === 1 ? "running" : "succeeded")); }
      gets++;
      return lost ? Response.json({ code, detail: `the server says ${code}` }, { status }) : Response.json(job(posted[0], "running"));
    });
    await client.settings();
    await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING, status);
    const [file] = durableFiles(box), before = readFileSync(file, "utf8");
    // The worker was paired again: the same request finds its journal and looks the job up.
    lost = true;
    gets = 0;
    await assert.rejects(runWriter(client), (error) => {
      assert.deepEqual([error.status, error.code, error.slug, error.stage], [status, code, DURABLE_SLUG, "writer"], status);
      assert.deepEqual(error.gone, { status, code }, `${status}: as lookupReceipt marks it`);
      return true;
    });
    assert.equal(gets, 1, `${status}: thrown at once`);
    // The old job may still be running under the old token: nothing is archived or sent on the worker's own.
    assert.equal(readFileSync(file, "utf8"), before, status);
    assert.equal(existsSync(path.join(path.dirname(file), "archive")), false, status);
    assert.equal(posted.length, 1, status);

    // An owner retry of any other block leaves a running journal alone: with no kind, with another kind, without the owner's request.
    const requestId = "22223333-4455-6677-8899-aabbccddeeff";
    const reason = "the server no longer has the saved writer job";
    for (const authorization of [{ requestId, reason }, { requestId, reason, kind: "failures:writer" }, { requestId, reason, kind: "job_gone:verifier" }, { reason, kind: "job_gone:writer" }]) {
      gets = 0;
      await client.retryRuns(DURABLE_SLUG, authorization);
      assert.deepEqual([gets, durableFiles(box).length, posted.length], [0, 1, 1], `${status} ${JSON.stringify(authorization)}`);
    }
    // The retry of the job_gone block looks the job up once more and, the server still answering the same, archives the journal.
    await client.retryRuns(DURABLE_SLUG, { requestId, reason, kind: "job_gone:writer" });
    assert.equal(gets, 1, status);
    assert.deepEqual(durableFiles(box), [], status);
    const [archived] = archiveOf(box);
    assert.equal(archived.request_key, posted[0].request_key, status);
    assert.equal(archived.receipt.status, "running", `${status}: the receipt bytes are kept`);
    assert.deepEqual({ ...archived.owner_retry, archived_at: null }, { request_id: null, reason: jobGoneReason({ status, code }), archived_at: null }, status);
    assert.deepEqual(await runWriter(client), savedAnswer, status);
    assert.equal(posted.length, 2, `${status}: exactly one new POST follows`);
    assert.notEqual(posted[1].request_key, posted[0].request_key, status);
  }
});

test("the retry of a job_gone block waits when the job is found running after all, and takes its answer when it finished: no new request either way", async () => {
  for (const found of ["running", "succeeded"]) {
    const box = sandbox();
    let original, posts = 0, state = "running";
    const client = durableClient(box, async (_url, init) => {
      if (init.method === "POST") { posts++; original = JSON.parse(init.body); return Response.json(job(original, "running")); }
      return state === "lost" ? Response.json({ code: "video_ai_job_not_found", detail: "no job for this token" }, { status: 404 }) : Response.json(job(original, state));
    });
    await client.settings();
    await assert.rejects(runWriter(client), (error) => error.code === RUN_PENDING, found);
    state = "lost";
    await assert.rejects(runWriter(client), (error) => error.gone?.status === 404, found);
    const authorization = { requestId: "33334444-5566-7788-99aa-bbccddeeff00", reason: "the server no longer has the saved writer job", kind: "job_gone:writer" };
    state = found;
    if (found === "running") {
      await assert.rejects(client.retryRuns(DURABLE_SLUG, authorization), (error) => error.code === RUN_PENDING && error.stage === "writer");
    } else {
      await client.retryRuns(DURABLE_SLUG, authorization);
      assert.deepEqual(await runWriter(client), savedAnswer, "the late answer is recovered by the normal run");
    }
    assert.equal(durableFiles(box).length, 1, `${found}: the journal is kept`);
    assert.equal(existsSync(path.join(box.work, DURABLE_SLUG, RUN_RECEIPTS_DIR, "archive")), false, found);
    assert.equal(posts, 1, found);
  }
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

test("definitive failed receipts surface their stored error, and input changes wait for an unfinished writer instead of replacing it", async () => {
  const box = sandbox(), posted = [];
  const client = durableClient(box, async (_url, init) => {
    const body = JSON.parse(init.body); posted.push(body);
    return Response.json({ ...job(body, "failed"), error_code: "video_ai_upstream_busy", error_detail: "Saved vendor refusal", error_status: 503, retry_after: "2026-10-04T15:00:00Z" });
  });
  await client.settings();
  await assert.rejects(runWriter(client), (error) => error.code === "video_ai_upstream_busy" && error.status === 503 && error.message === "Saved vendor refusal" && error.retry_after === "2026-10-04T15:00:00Z");
  assert.deepEqual(durableFiles(box), [], "the server definitively settled this failure");
  const pendingBox = sandbox(), calls = [];
  let original;
  const pending = durableClient(pendingBox, async (_url, init) => {
    calls.push(init.method);
    if (init.method === "POST") original = JSON.parse(init.body);
    return Response.json(job(original, "running"));
  });
  await pending.settings();
  await assert.rejects(runWriter(pending), (error) => error.code === RUN_PENDING);
  const [file] = durableFiles(pendingBox), before = readFileSync(file, "utf8");
  calls.length = 0;
  await assert.rejects(runWriter(pending, { text: "new source" }), (error) => error.code === RUN_PENDING && error.slug === DURABLE_SLUG && /still running/.test(error.message));
  assert.deepEqual(calls, ["GET"], "the running job is looked up once and nothing new is paid for");
  assert.deepEqual(durableFiles(pendingBox), [file]);
  assert.equal(readFileSync(file, "utf8"), before, "the running journal is intact for the next round");
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

test("a settled policy refusal survives repeated rounds and client restarts without another job POST", async () => {
  for (const direct of [false, true]) {
    const box = sandbox(), posts = [];
    const make = () => durableClient(box, async (_url, init) => {
      assert.equal(init.method, "POST");
      const body = JSON.parse(init.body);
      posts.push(body);
      if (direct) return Response.json({ code: POLICY_HOLD, detail: "drama disabled" }, { status: 409 });
      return Response.json({ ...job(body, "failed"), error_code: POLICY_HOLD, error_detail: "drama disabled", error_status: 409, dispatched_at: null });
    });
    const first = make();
    await first.settings();
    await assert.rejects(runWriter(first), (error) => error.code === POLICY_HOLD && error.who === "owner");
    const file = durableFiles(box)[0], before = readFileSync(file, "utf8");
    await assert.rejects(runWriter(first), (error) => error.code === POLICY_HOLD);
    const restarted = make();
    await restarted.settings();
    await assert.rejects(runWriter(restarted), (error) => error.code === POLICY_HOLD);
    assert.equal(posts.length, 1, "the original policy refusal is a project hold, not a new request every round");
    assert.equal(readFileSync(file, "utf8"), before, "the original key, source and exact refusal survive");
  }
});

test("policy retry requires a fresh enabled route, a new owner request, and no STOP; it archives the original refusal", async () => {
  const box = sandbox(), calls = [], requestId = "11112233-4455-6677-8899-aabbccddeeff";
  let enabled = false, current;
  const client = automationClient({ ...credentials(box), root: box.root, sleep: async () => {}, fetch: async (url, init) => {
    const route = new URL(url).pathname;
    calls.push({ route, method: init.method });
    if (route.endsWith("/settings")) return Response.json({ enabled: true, durable_stage_runs: true, drama: { drama_enabled: enabled }, model: "changed-provider-does-not-resume" });
    if (init.method === "POST") current = { ...job(JSON.parse(init.body), "failed"), error_code: POLICY_HOLD, error_detail: "drama disabled", error_status: 409, dispatched_at: null };
    return Response.json(current);
  } });
  await client.settings();
  const run = () => client.run("writer", DURABLE_SLUG, "Original drama", { video: { format: "drama" } }, 16_000, "drama");
  await assert.rejects(run(), (error) => error.code === POLICY_HOLD);
  const file = durableFiles(box)[0], original = JSON.parse(readFileSync(file, "utf8"));
  await client.retryRuns(DURABLE_SLUG, { reason: "old retry without request identity" });
  assert.ok(existsSync(file));
  await assert.rejects(client.retryRuns(DURABLE_SLUG, { requestId, format: "drama" }), (error) => error.code === POLICY_HOLD);
  assert.deepEqual(JSON.parse(readFileSync(file, "utf8")), original);
  enabled = true;
  const stop = path.join(box.work, DURABLE_SLUG, "STOP");
  writeFileSync(stop, "hold");
  await assert.rejects(client.retryRuns(DURABLE_SLUG, { requestId, format: "drama" }), (error) => error.code === RUN_UNCERTAIN && /STOP/.test(error.message));
  assert.ok(existsSync(file));
  const { unlinkSync } = await import("node:fs");
  unlinkSync(stop);
  await client.retryRuns(DURABLE_SLUG, { requestId, format: "drama", reason: "owner retry after enabling the route" });
  assert.equal(existsSync(file), false);
  const archiveDir = path.join(path.dirname(file), "archive");
  const archived = JSON.parse(readFileSync(path.join(archiveDir, readdirSync(archiveDir)[0]), "utf8"));
  assert.deepEqual(archived.receipt, original.receipt);
  assert.equal(archived.request_key, original.request_key);
  assert.equal(archived.owner_retry.request_id, requestId);
  assert.equal(calls.filter((call) => call.method === "POST").length, 1, "authorizing resume never runs a model by itself");
});

test("a verified undispatched slides repair may resume its corrected format while drama stays disabled", async () => {
  for (const video of [{ format: "slides" }, {}]) {
    const box = sandbox();
    let refusal;
    const client = automationClient({ ...credentials(box), root: box.root, sleep: async () => {}, fetch: async (url, init) => {
      if (new URL(url).pathname.endsWith("/settings")) return Response.json({ enabled: true, durable_stage_runs: true, drama: { drama_enabled: false } });
      if (init.method === "POST") refusal = { ...job(JSON.parse(init.body), "failed"), error_code: POLICY_HOLD, error_detail: "misrouted slides repair", error_status: 409, dispatched_at: null };
      return Response.json(refusal);
    } });
    await client.settings();
    await assert.rejects(client.run("writer", DURABLE_SLUG, "Repair keyframes", { video, fix: { kind: "keyframes" } }, 16_000, "drama"), (error) => error.code === POLICY_HOLD);
    await client.retryRuns(DURABLE_SLUG, { requestId: "11112233-4455-6677-8899-aabbccddeeff", format: "slides", reason: "owner resumes the corrected slides route" });
    assert.deepEqual(durableFiles(box), []);
    const dir = path.join(box.work, DURABLE_SLUG, RUN_RECEIPTS_DIR, "archive");
    assert.equal(readdirSync(dir).length, 1, "preserve the refused drama request instead of editing its identity");
  }
});

test("a mixed legacy set of policy holds cannot be partly archived by one owner retry", async () => {
  const box = sandbox();
  let requests = 0;
  const client = automationClient({ ...credentials(box), root: box.root, sleep: async () => {}, fetch: async (url, init) => {
    requests++;
    if (new URL(url).pathname.endsWith("/settings")) return Response.json({ enabled: true, durable_stage_runs: true, drama: { drama_enabled: true } });
    assert.equal(init.method, "POST");
    return Response.json({ ...job(JSON.parse(init.body), "failed"), error_code: POLICY_HOLD, error_detail: "saved refusal", error_status: 409, dispatched_at: null });
  } });
  await client.settings();
  for (const variant of [null, "discuss"]) {
    await assert.rejects(client.run("writer", DURABLE_SLUG, "Original source", { video: { format: "drama" } }, 16_000, "drama", variant), (error) => error.code === POLICY_HOLD);
  }
  const files = durableFiles(box), before = files.map((file) => readFileSync(file, "utf8"));
  assert.equal(files.length, 2);
  const beforeRequests = requests;
  await assert.rejects(client.retryRuns(DURABLE_SLUG, { requestId: "11112233-4455-6677-8899-aabbccddeeff", format: "drama" }), (error) => error.code === RUN_UNCERTAIN && /multiple saved runs/.test(error.message));
  assert.deepEqual(durableFiles(box), files);
  assert.deepEqual(files.map((file) => readFileSync(file, "utf8")), before, "retain every original refusal byte before any partial archive");
  assert.equal(requests, beforeRequests, "an ambiguous retry does not dispatch, poll or buy work");
  assert.equal(existsSync(path.join(path.dirname(files[0]), "archive")), false);
});
