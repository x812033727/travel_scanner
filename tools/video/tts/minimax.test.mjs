// MiniMax voices in the video tool: the voice schema, the request body, the text the server sends
// MiniMax (mirrored from apps/api/app/video_speech/minimax.py), and `minimax-quota`.
import assert from "node:assert/strict";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { tempDir } from "../core/fixtures/load.mjs";
import { validateVoice } from "../core/schema.mjs";
import { writeCredentials } from "./credentials.mjs";
import { billableForRequest, minimaxText, voiceFields } from "./requests.mjs";

const TOKEN = `mkv_${"m".repeat(43)}`;
const VOICE = "Chinese (Mandarin)_News_Anchor";

const errorsOf = (voice) => {
  const errors = [];
  validateVoice(voice, errors);
  return errors.map((error) => `${error.path}: ${error.message}`);
};

test("a MiniMax voice names a voice id, takes a rate and a model, and no style", () => {
  assert.deepEqual(errorsOf({ provider: "minimax", name: VOICE }), []);
  assert.deepEqual(errorsOf({ provider: "minimax", name: VOICE, rate: "+10%", model: "speech-2.8-turbo" }), []);
  assert.match(errorsOf({ provider: "minimax", name: VOICE, style: "relaxed" }).join("\n"), /voice\.style: MiniMax takes no written style/);
  assert.match(errorsOf({ provider: "minimax", name: VOICE, model: "speech-9" }).join("\n"), /voice\.model: must be one of speech-2\.8-hd, speech-2\.8-turbo/);
  assert.match(errorsOf({ provider: "minimax", name: `minimax:${VOICE}` }).join("\n"), /without the minimax: prefix/);
  assert.match(errorsOf({ provider: "minimax", name: " padded" }).join("\n"), /voice\.name/);
  // Azure still refuses a model, Gemini still refuses a rate.
  assert.match(errorsOf({ provider: "azure", name: "zh-TW-HsiaoChenNeural", model: "speech-2.8-hd" }).join("\n"), /model for Gemini or MiniMax/);
  assert.match(errorsOf({ provider: "gemini", name: "Sulafat", rate: "+5%" }).join("\n"), /remove rate/);
});

test("the request carries the prefixed voice, the rate and the model only when given", () => {
  assert.deepEqual(voiceFields({ provider: "minimax", name: VOICE }), { voice: `minimax:${VOICE}`, rate: "+0%" });
  assert.deepEqual(voiceFields({ provider: "minimax", name: VOICE, rate: "-5%", model: "speech-2.8-turbo" }), { voice: `minimax:${VOICE}`, rate: "-5%", model: "speech-2.8-turbo" });
});

test("the text matches the server's: spoken forms, markers between speech only, no markup of its own", () => {
  // The same cases as apps/api/tests/test_video_speech_minimax.py.
  const segments = [
    { parts: [{ text: "用 " }, { text: "LLM", alias: "L L M" }, { text: " 算" }], break_after_ms: 800 },
    { parts: [{ text: "下一句" }], break_after_ms: 5 },
    { parts: [{ text: "  " }], break_after_ms: 300 },
    { parts: [{ text: "最後一句" }], break_after_ms: 900 },
  ];
  assert.equal(minimaxText(segments), "用 L L M 算<#0.80#>下一句<#0.01#>最後一句");
  assert.equal(minimaxText([{ parts: [{ text: "他笑了 (laughs) <#3#> 和(he2)平" }], break_after_ms: 0 }]), "他笑了 （laughs）   3   和（he2）平");
  const body = { voice: `minimax:${VOICE}`, rate: "+0%", segments };
  assert.equal(billableForRequest(body), minimaxText(segments).length);
});

function capture(overrides) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-11-12T05:00:00Z"),
      sleep: async () => {},
      ...overrides,
    },
  };
}

function quotaServer(answer) {
  const calls = [];
  const fetchImpl = async (url, init) => {
    calls.push({ url, init });
    return typeof answer === "function" ? answer() : Response.json(answer);
  };
  return { calls, fetchImpl };
}

test("minimax-quota prints each list entry with the fields MiniMax sent, or the whole answer with --json", async () => {
  const home = tempDir("minimax-quota-");
  writeCredentials({ site: "https://mokaair.com", token: TOKEN }, { home });
  const answer = {
    checked_at: "2026-11-12T05:00:00Z",
    host: "www.minimax.io",
    quota: { model_remains: [{ model_name: "speech-2.8-hd", remaining: 3200, window: { ends: "x" } }, "odd"], plan: "Plus" },
  };
  const server = quotaServer(answer);
  const { ctx, out } = capture({ root: home, home, env: {}, fetch: server.fetchImpl });
  assert.equal(await main(["minimax-quota"], ctx), EXIT.ok, out.stderr);
  assert.equal(server.calls[0].url, "https://mokaair.com/api/video/speech/minimax-quota");
  assert.equal(server.calls[0].init.method, "GET");
  assert.equal(server.calls[0].init.headers.Authorization, `Bearer ${TOKEN}`);
  assert.equal(
    out.stdout,
    [
      "MiniMax M Plan, asked www.minimax.io at 2026-11-12T05:00:00Z",
      "model_remains:",
      '  speech-2.8-hd: remaining 3200, window {"ends":"x"}',
      '  "odd"',
      "plan: Plus",
      "",
    ].join("\n"),
  );
  const json = capture({ root: home, home, env: {}, fetch: quotaServer(answer).fetchImpl });
  assert.equal(await main(["minimax-quota", "--json"], json.ctx), EXIT.ok);
  assert.deepEqual(JSON.parse(json.out.stdout), answer);
});

test("minimax-quota tells the owner when the key has no plan, and needs a paired token", async () => {
  const home = tempDir("minimax-quota-");
  writeCredentials({ site: "https://mokaair.com", token: TOKEN }, { home });
  const refused = quotaServer(() => Response.json({ code: "video_speech_upstream_rejected_key", detail: "這把 MiniMax 金鑰沒有生效中的 M Plan 訂閱" }, { status: 502 }));
  const { ctx, out } = capture({ root: home, home, env: {}, fetch: refused.fetchImpl });
  assert.notEqual(await main(["minimax-quota"], ctx), EXIT.ok);
  assert.match(out.stderr, /M Plan/);
  assert.equal(refused.calls.length, 1);
  const unpaired = tempDir("minimax-quota-");
  const bare = capture({ root: unpaired, home: unpaired, env: {}, fetch: async () => assert.fail("no request without a token") });
  assert.equal(await main(["minimax-quota"], bare.ctx), EXIT.owner);
});
