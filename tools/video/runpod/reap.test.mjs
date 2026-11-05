import assert from "node:assert/strict";
import { test } from "node:test";
import { main } from "../cli.mjs";

const TOKEN = `mkv_${"a".repeat(40)}`;

function harness(answer) {
  const out = [];
  const err = [];
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    return new Response(JSON.stringify(answer.body), { status: answer.status ?? 200, headers: { "Content-Type": "application/json" } });
  };
  const overrides = {
    env: { MOKAAIR_SITE: "https://mokaair.example", MOKAAIR_VIDEO_TOKEN: TOKEN },
    home: "/nonexistent",
    fetchImpl,
    stdout: { write: (text) => out.push(text) },
    stderr: { write: (text) => err.push(text) },
  };
  return { out, err, calls, overrides };
}

test("runpod-reap knocks once with the token and reports what the site stopped", async () => {
  const { out, calls, overrides } = harness({
    body: { stopped: [{ session_id: "s1", pod_id: "pod123", label: "e031", stop_reason: "idle", usd: "0.5150" }] },
  });
  assert.equal(await main(["runpod-reap"], overrides), 0);
  assert.equal(calls.length, 1);
  assert.equal(calls[0].url, "https://mokaair.example/api/video/runpod/reap");
  assert.equal(calls[0].init.method, "POST");
  assert.equal(calls[0].init.headers.Authorization, `Bearer ${TOKEN}`);
  assert.equal(out.join(""), "runpod-reap: stopped pod123 (e031): idle, US$0.52\n");
});

test("runpod-reap is quiet when nothing was stopped and exits 4 when the site refuses", async () => {
  const quiet = harness({ body: { stopped: [] } });
  assert.equal(await main(["runpod-reap"], quiet.overrides), 0);
  assert.deepEqual(quiet.out, []);
  const refused = harness({ status: 401, body: { code: "video_tool_token_invalid", detail: "bad" } });
  assert.equal(await main(["runpod-reap"], refused.overrides), 4);
  assert.match(refused.err.join(""), /401 video_tool_token_invalid/);
});

test("runpod-reap needs a token", async () => {
  const { err, overrides } = harness({ body: {} });
  overrides.env = { MOKAAIR_SITE: "https://mokaair.example" };
  assert.equal(await main(["runpod-reap"], overrides), 2);
  assert.match(err.join(""), /no video tool token/);
});
