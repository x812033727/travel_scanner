// The Shorts tool's own site client (site.mjs): a Jev policy reading is paid for once it reaches the
// API (apps/api/app/video_automation/judge.py `_ask`), so it is not sent again after a lost answer,
// while a request that never left and every other route keep their retries. Fake transports only:
// nothing here asks Jev.
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { RUN_UNCERTAIN } from '../automation/client.mjs';
import { buildTimeline, phrasesOf, saveJson } from './core.mjs';
import { runQa } from './qa.mjs';
import { SiteError, siteClient } from './site.mjs';

const TOKEN = `mkv_${'s'.repeat(43)}`;
const env = { MOKAAIR_SITE: 'https://site.test', MOKAAIR_VIDEO_TOKEN: TOKEN };
const POLICY = '/api/video/automation/judge/policy';
const BODY = { slug: 'shorts-smoke-receipt', script: '旁白', viewpoint: '' };
// A failed verdict as the API returns it: it is handed back exactly as it came.
const VERDICT = { stance: 0.31, demo: 0.82, advice: 0.04, sponsored: 0.02, passed: false, note: 'Jev：立場 0.31；沒過（立場低於 0.6）', questions: 'tutorial', observation: null, disparage: null };
const json = (body, status = 200) => new Response(JSON.stringify(body), { status, headers: { 'content-type': 'application/json' } });
// What undici throws: a TypeError whose cause names the socket's error code.
const failed = (code) => Object.assign(new TypeError('fetch failed'), { cause: Object.assign(new Error(`socket ${code}`), { code }) });

// Each answer is what the first request gets; any later one gets the verdict.
function recording(first) {
  const calls = [];
  const sleeps = [];
  const client = siteClient({
    env,
    fetch: async (url, init) => {
      calls.push({ path: new URL(url).pathname, method: init.method, body: init.body === undefined ? undefined : init.body instanceof Uint8Array ? 'bytes' : JSON.parse(init.body) });
      return calls.length === 1 ? first() : json(VERDICT);
    },
    sleep: async (ms) => sleeps.push(ms),
  });
  return { client, calls, sleeps };
}

const LOST = [
  ['a connection reset after sending', () => {
    throw failed('ECONNRESET');
  }, 0],
  ['a connection dropped mid-way', () => {
    throw failed('UND_ERR_SOCKET');
  }, 0],
  ["Node's deadline for the headers", () => {
    throw failed('UND_ERR_HEADERS_TIMEOUT');
  }, 0],
  ['a verdict that breaks off', () => new Response('{"stance": 0.3, "passed": fal', { status: 200, headers: { 'content-type': 'application/json' } }), 200],
  ["an error without the API's code", () => json({ detail: 'Internal Server Error' }, 500), 500],
  ["a gateway's timeout page", () => new Response('<html>504 Gateway Time-out</html>', { status: 504, headers: { 'content-type': 'text/html' } }), 504],
  // The judge route's answer for a request the API took and whose answer was lost.
  ["the judge route's lost answer", () => json({ code: 'video_judge_answer_lost', detail: 'Jev 可能已經判斷' }, 504), 504],
  // The API's own 502 for a Jev call whose outcome it cannot tell: a 502, but not a settled one.
  ["the API's uncertain Jev outcome", () => json({ code: 'video_judge_outcome_uncertain', detail: 'Jev 可能已處理這次請求' }, 502), 502],
  // Only the route's 502 says the API was never reached; no judge route answers this one.
  ['an upstream_unavailable no judge route answers', () => json({ code: 'upstream_unavailable', detail: 'API 服務目前無法回應' }, 503), 503],
  // The API's rate limiter answers its code only as a 503.
  ['a rate_limit_unavailable at another status', () => json({ code: 'rate_limit_unavailable', detail: '安全驗證服務暫時無法使用' }, 500), 500],
];

test('a policy judgement sent and left without its answer is not asked again: a dropped connection, a broken body, a gateway, a lost answer', async () => {
  for (const [what, answer, status] of LOST) {
    const { client, calls, sleeps } = recording(answer);
    await assert.rejects(client.judgePolicy(BODY), (error) => {
      assert.ok(error instanceof SiteError, what);
      assert.equal(error.code, RUN_UNCERTAIN, what);
      assert.equal(error.who, 'service', `${what}: a later QA run may ask again`);
      assert.equal(error.status, status, what);
      assert.match(error.message, /^automation\/judge\/policy was sent and no answer came back \(.+\); Jev may have judged it, so the outcome is unknown and it is not sent again$/, what);
      return true;
    });
    assert.deepEqual(calls, [{ path: POLICY, method: 'POST', body: BODY }], `${what}: sent once`);
    assert.deepEqual(sleeps, [], `${what}: no wait for a second try`);
  }
});

test('a policy judgement that never reached a server, or that the API settled, is asked again and its failed verdict comes back unchanged', async () => {
  const settled = [
    ...['ECONNREFUSED', 'ENOTFOUND', 'EAI_AGAIN', 'EHOSTUNREACH', 'ENETUNREACH', 'UND_ERR_CONNECT_TIMEOUT'].map((code) => [`a connection that never opened (${code})`, () => {
      throw failed(code);
    }]),
    ["the API's answer after Jev failed", () => json({ code: 'video_judge_upstream_failed', detail: 'Jev 暫時無法判斷' }, 502)],
    // Only an API the judge route never reached, since the route answers a lost one with its 504.
    ["the judge route's 502", () => json({ code: 'upstream_unavailable', detail: 'API 服務目前無法回應' }, 502)],
    ["the judge's hourly limit", () => json({ code: 'rate_limit_exceeded', detail: 'slow down' }, 429)],
    ['the spent Jev budget', () => json({ code: 'jev_budget_exhausted', detail: '今天的 Jev 呼叫次數已用完' }, 429)],
    // Redis could not count the call: the API refused it before Jev (2026-10-07-the-speech-and-shorts-clients-hold).
    ["the API's rate limiter away", () => json({ code: 'rate_limit_unavailable', detail: '安全驗證服務暫時無法使用' }, 503)],
  ];
  for (const [what, answer] of settled) {
    const { client, calls, sleeps } = recording(answer);
    assert.deepEqual(await client.judgePolicy(BODY), VERDICT, `${what}: the verdict as Jev gave it`);
    assert.deepEqual(calls, [{ path: POLICY, method: 'POST', body: BODY }, { path: POLICY, method: 'POST', body: BODY }], `${what}: the same request asked again`);
    assert.equal(sleeps.length, 1, `${what}: one wait before it`);
  }
  // A verdict that comes back at once is not touched either.
  const { client, calls } = recording(() => json(VERDICT));
  assert.deepEqual(await client.judgePolicy(BODY), VERDICT);
  assert.equal(calls.length, 1);
});

test('a judge\'s refusal is thrown after one request, with its status and code', async () => {
  for (const [status, code, detail] of [[409, 'video_judge_not_enabled', '頻道立場還是空白'], [422, 'video_judge_invalid', 'Jev 拒絕這個問題'], [404, '', 'Not Found']]) {
    const { client, calls } = recording(() => json({ code, detail }, status));
    await assert.rejects(client.judgePolicy(BODY), (error) => error instanceof SiteError && error.status === status && error.code === code && error.message === detail);
    assert.equal(calls.length, 1, `${status}`);
  }
});

test('the other requests keep their retries: reads, reviews and uploads spend nothing', async () => {
  const retried = [
    ['a list read on a 500', (client) => client.videos({ shorts: 'only' }), () => json({ detail: 'Internal Server Error' }, 500)],
    ['a list read after a dropped connection', (client) => client.videos(), () => {
      throw failed('UND_ERR_SOCKET');
    }],
    ['a review read behind a gateway', (client) => client.project('a-short'), () => new Response('<html>504</html>', { status: 504 })],
    ['a review report on the route\'s 502', (client) => client.report('a-short', { title: 't' }), () => json({ code: 'upstream_unavailable' }, 502)],
    ['a file part after a reset', (client) => client.part('a-short', 'f'.repeat(64), new Uint8Array([1, 2, 3]), { offset: '0' }), () => {
      throw failed('ECONNRESET');
    }],
    ['a review submit after a reset', (client) => client.submit('a-short', { gate: 'final' }), () => {
      throw failed('ECONNRESET');
    }],
    ['the worker\'s knock on a 503', (client) => client.tick(), () => json({ detail: 'busy' }, 503)],
  ];
  for (const [what, call, first] of retried) {
    const { client, calls } = recording(first);
    assert.deepEqual(await call(client), VERDICT, what);
    assert.equal(calls.length, 2, `${what}: tried again`);
    assert.deepEqual(calls[0], calls[1], `${what}: the same request`);
  }
});

test('the QA\'s policy item says the outcome is unknown, and the QA run asks Jev once', async (t) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), 'shorts-site-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  mkdirSync(path.join(directory, 'upload'));
  const doc = JSON.parse(readFileSync(fileURLToPath(new URL('./fixtures/smoke/script.json', import.meta.url)), 'utf8'));
  saveJson(path.join(directory, 'script.json'), doc);
  const timeline = buildTimeline(doc, phrasesOf(doc).map(() => 3));
  saveJson(path.join(directory, 'timeline.json'), timeline);
  writeFileSync(path.join(directory, 'upload/final.mp4'), 'a final cut; measurement is injected');
  const { client, calls } = recording(() => {
    throw failed('ECONNRESET');
  });
  const report = await runQa({
    directory,
    client,
    settings: { locales: [] },
    tools: {},
    measureImpl: async () => ({
      video: { width: 1080, height: 1920, codec_name: 'h264', r_frame_rate: '30/1', nb_frames: String(timeline.frames) },
      audio: { codec_name: 'aac', sample_rate: '48000', duration: String(timeline.seconds) },
      loudness: { input_i: '-14', input_tp: '-1' },
    }),
    linkCheck: async (url) => ({ url, ok: true, status: 200 }),
    history: [],
  });
  const policy = report.items.find((item) => item.id === 'policy');
  assert.equal(policy.ok, false);
  assert.match(policy.detail, /the outcome is unknown and it is not sent again/);
  assert.deepEqual(calls.map((call) => call.path), [POLICY]);
});

test('a request the site keeps refusing is told after its last attempt, with no wait after it', async () => {
  for (const [what, answer] of [
    ['a busy route', () => json({ code: 'rate_limit_exceeded', detail: 'slow down' }, 429)],
    ['a site that is down', () => {
      throw failed('ECONNREFUSED');
    }],
  ]) {
    let calls = 0;
    const sleeps = [];
    const client = siteClient({ env, fetch: async () => { calls += 1; return answer(); }, sleep: async (ms) => sleeps.push(ms) });
    await assert.rejects(client.judgePolicy(BODY), (error) => error instanceof SiteError && error.who === 'service', what);
    assert.equal(calls, 4, what);
    assert.equal(sleeps.length, 3, `${what}: a wait between two attempts, none after the last`);
  }
});
