// Exercise the complete QA -> package -> push boundary with real local receipts. Only media
// measurement and the remote services are substituted; no test fabricates a passing QA report.
import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

import { encodeWav } from '../tts/wav.mjs';
import { checkPhrases } from './check.mjs';
import { buildTimeline, phrasesOf, saveJson, sha256, srt } from './core.mjs';
import { packageBuild } from './package.mjs';
import { push } from './push.mjs';
import { ITEM_IDS, qaInputBindings, runQa } from './qa.mjs';

const FIXTURE = fileURLToPath(new URL('./fixtures/smoke/script.json', import.meta.url));
const SETTINGS = { locales: ['en'] };
const read = (directory, name) => JSON.parse(readFileSync(path.join(directory, name), 'utf8'));
const edit = (directory, name, change) => {
  const value = read(directory, name);
  change(value);
  saveJson(path.join(directory, name), value);
};

async function build(t) {
  const directory = mkdtempSync(path.join(os.tmpdir(), 'shorts-bindings-'));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  for (const name of ['audio', 'upload', 'evidence']) mkdirSync(path.join(directory, name));
  const doc = JSON.parse(readFileSync(FIXTURE, 'utf8'));
  const evidence = Buffer.from('{"expected":275,"observed":[275,275]}\n');
  doc.evidence = [{ path: 'result.json', sha256: sha256(evidence) }];
  doc.links = [{ label: 'Source', url: 'https://example.test/result' }];
  saveJson(path.join(directory, 'script.json'), doc);
  writeFileSync(path.join(directory, 'evidence/result.json'), evidence);

  const phrases = phrasesOf(doc);
  const timeline = buildTimeline(doc, phrases.map(() => 3));
  saveJson(path.join(directory, 'timeline.json'), timeline);
  const clips = phrases.map((_phrase, index) => {
    const samples = new Int16Array(48_000 * 3);
    for (let i = 0; i < samples.length; i++) samples[i] = Math.round(4000 * Math.sin(2 * Math.PI * (300 + index * 20) * i / 48_000));
    const clip = encodeWav(samples);
    writeFileSync(path.join(directory, 'audio', `${String(index).padStart(3, '0')}.wav`), clip);
    return clip;
  });
  let nextPhrase = 0;
  const check = await checkPhrases({
    phrases,
    clips,
    transcribe: async () => phrases[nextPhrase++],
    judge: async () => assert.fail('matching transcripts need no judge'),
  });
  assert.equal(check.ok, true);
  saveJson(path.join(directory, 'check.json'), check);
  saveJson(path.join(directory, 'checks.json'), { layout: timeline.cues.map((cue) => ({ cue: cue.index, problems: [] })) });
  saveJson(path.join(directory, 'verify.json'), {
    ok: true,
    document_sha256: sha256(readFileSync(path.join(directory, 'script.json'))),
    checked_by: 'test evidence checker',
    claims: [{ text: '85 * 2 + 45 * 3 - 30 = 275', ok: true }],
    problems: [],
  });
  writeFileSync(path.join(directory, 'upload/final.mp4'), 'fixed final cut; measurement is injected');
  writeFileSync(path.join(directory, 'upload/cover.png'), 'fixed cover');
  for (const locale of ['zh-TW', 'en', 'ja']) writeFileSync(path.join(directory, 'upload', `${locale}.srt`), srt(timeline));
  return { directory, timeline };
}

function measured(timeline) {
  return {
    video: { width: 1080, height: 1920, codec_name: 'h264', r_frame_rate: '30/1', nb_frames: String(timeline.frames) },
    audio: { codec_name: 'aac', sample_rate: '48000', duration: String(timeline.seconds) },
    loudness: { input_i: '-14', input_tp: '-1' },
    // The cut's two ends (qa.mjs grammar): the cover identical to frame 0, the last frame the first encoded again.
    grammar: { cover_psnr: Infinity, loop_psnr: 48.1 },
  };
}

async function quality(fixture, overrides = {}) {
  return runQa({
    directory: fixture.directory,
    client: { judgePolicy: async () => ({ passed: true, note: 'The example meets the channel rules.' }) },
    settings: SETTINGS,
    tools: {},
    measureImpl: async () => measured(fixture.timeline),
    linkCheck: async (url) => ({ url, ok: true, status: 200 }),
    history: [],
    ...overrides,
  });
}

async function passingBuild(t) {
  const fixture = await build(t);
  const report = await quality(fixture);
  assert.equal(report.ok, true, JSON.stringify(report.items.filter((item) => !item.ok)));
  assert.deepEqual(report.items.map((item) => item.id), ITEM_IDS);
  assert.ok(report.items.every((item) => item.ok));
  assert.equal(packageBuild({ directory: fixture.directory, settings: SETTINGS }).report.ok, true);
  return fixture;
}

function site({
  onPart = async () => {},
  onReport = async () => {},
  onSubmit = async (body) => ({
    id: `${body.gate}-review`,
    status: body.gate === 'final' && !body.payload.qa.ok ? 'pending' : 'approved',
    payload: structuredClone(body.payload),
  }),
} = {}) {
  const writes = [];
  return {
    writes,
    report: async (slug, body) => {
      writes.push({ method: 'report', slug, body });
      await onReport(body);
    },
    part: async (slug, hash, bytes) => {
      writes.push({ method: 'part', slug, hash, bytes });
      await onPart({ hash, bytes });
      return { complete: true };
    },
    submit: async (slug, body) => {
      writes.push({ method: 'submit', slug, body });
      return onSubmit(body);
    },
  };
}

test('an all-pass run binds every local QA input and still permits packaging and pushing', async (t) => {
  const { directory } = await passingBuild(t);
  const qa = read(directory, 'qa.json');
  assert.deepEqual(qa.inputs, qaInputBindings(directory));
  for (const name of ['script.json', 'timeline.json', 'check.json', 'verify.json', 'checks.json', 'upload/final.mp4', 'audio/000.wav', 'audio/010.wav', 'upload/zh-TW.srt', 'upload/en.srt', 'upload/ja.srt', 'evidence/result.json']) {
    assert.equal(qa.inputs.files[name], sha256(readFileSync(path.join(directory, name))), name);
  }
  assert.equal(qa.inputs.files['upload/ko.srt'], null);
  const client = site();
  const result = await push({ directory, client });
  assert.equal(result.waits, null);
  assert.equal(result.final.status, 'approved');
  assert.equal(result.publish.status, 'approved');
  const submitted = client.writes.filter((write) => write.method === 'submit');
  assert.deepEqual(submitted.map((write) => write.body.gate), ['final', 'publish']);
  assert.deepEqual(submitted[0].body.payload.qa.inputs, qa.inputs);
  assert.equal(submitted[1].body.payload.final_review_id, result.final.id);
});

const MUTATIONS = [
  ['description', (directory) => edit(directory, 'script.json', (doc) => { doc.description += ' Changed description.'; })],
  ['audio receipt', (directory) => edit(directory, 'check.json', (check) => { check.ok = false; })],
  ['fact receipt', (directory) => edit(directory, 'verify.json', (verify) => { verify.claims[0].ok = false; })],
  ['layout receipt', (directory) => edit(directory, 'checks.json', (checks) => { checks.layout[0].problems.push('clipped'); })],
  ['timeline', (directory) => edit(directory, 'timeline.json', (timeline) => { timeline.cues[0].text += ' changed'; })],
  ['audio clip', (directory) => writeFileSync(path.join(directory, 'audio/000.wav'), encodeWav(new Int16Array(48_000)))],
  ['primary captions', (directory) => writeFileSync(path.join(directory, 'upload/zh-TW.srt'), '1\n00:00:00,000 --> 00:00:03,000\nchanged\n')],
  ['selected captions', (directory) => writeFileSync(path.join(directory, 'upload/en.srt'), '1\n00:00:00,000 --> 00:00:03,000\nchanged\n')],
  ['unselected captions', (directory) => writeFileSync(path.join(directory, 'upload/ja.srt'), 'changed unselected track')],
  ['added captions', (directory) => writeFileSync(path.join(directory, 'upload/ko.srt'), 'new track')],
  ['evidence', (directory) => writeFileSync(path.join(directory, 'evidence/result.json'), '{"observed":[999]}\n')],
];

test('editing any QA input with the same MP4 blocks every site write, even after repackaging', async (t) => {
  for (const [name, mutate] of MUTATIONS) {
    await t.test(name, async (t) => {
      const { directory } = await passingBuild(t);
      const finalHash = sha256(readFileSync(path.join(directory, 'upload/final.mp4')));
      mutate(directory);
      packageBuild({ directory, settings: SETTINGS });
      assert.equal(sha256(readFileSync(path.join(directory, 'upload/final.mp4'))), finalHash);
      const client = site();
      const result = await push({ directory, client });
      assert.match(result.waits, /QA inputs changed/);
      assert.equal(result.final, null);
      assert.equal(result.publish, null);
      assert.deepEqual(client.writes, [], 'stale QA must stop before report or uploads');
    });
  }
});

test('missing, legacy and incomplete bindings require a real QA rerun before push', async (t) => {
  const invalid = [
    ['no QA', (directory) => rmSync(path.join(directory, 'qa.json'))],
    ['legacy QA', (directory) => edit(directory, 'qa.json', (qa) => { delete qa.inputs; })],
    ['old version', (directory) => edit(directory, 'qa.json', (qa) => { qa.inputs.version = 0; })],
    ['partial map', (directory) => edit(directory, 'qa.json', (qa) => { delete qa.inputs.files['upload/ko.srt']; })],
    ['extra input', (directory) => edit(directory, 'qa.json', (qa) => { qa.inputs.files['unrecognized.json'] = null; })],
  ];
  for (const [name, invalidate] of invalid) {
    await t.test(name, async (t) => {
      const fixture = await passingBuild(t);
      invalidate(fixture.directory);
      const refused = site();
      assert.match((await push({ directory: fixture.directory, client: refused })).waits, /no binding/);
      assert.deepEqual(refused.writes, []);
      assert.equal((await quality(fixture)).ok, true);
      packageBuild({ directory: fixture.directory, settings: SETTINGS });
      assert.equal((await push({ directory: fixture.directory, client: site() })).publish.status, 'approved');
    });
  }
});

test('rerunning QA on a failed receipt preserves its failure and sends the cut for owner review', async (t) => {
  const fixture = await passingBuild(t);
  edit(fixture.directory, 'verify.json', (verify) => {
    verify.ok = false;
    verify.claims[0].ok = false;
    verify.problems = ['The evidence does not support this claim.'];
  });
  const report = await quality(fixture);
  assert.equal(report.ok, false);
  assert.deepEqual(report.items.filter((item) => !item.ok).map((item) => item.id), ['facts']);
  packageBuild({ directory: fixture.directory, settings: SETTINGS });
  const client = site();
  const result = await push({ directory: fixture.directory, client });
  assert.equal(result.final.status, 'pending');
  assert.equal(result.publish, null);
  assert.match(result.waits, /owner/);
  const submitted = client.writes.filter((write) => write.method === 'submit');
  assert.equal(submitted.length, 1);
  assert.equal(submitted[0].body.payload.qa.ok, false);
  assert.equal(submitted[0].body.payload.qa.items.find((item) => item.id === 'facts').ok, false);
});

test('a reused approval for the same MP4 with older input bindings cannot publish', async (t) => {
  const fixture = await passingBuild(t);
  const original = await push({ directory: fixture.directory, client: site() });
  assert.equal(original.final.status, 'approved');
  const oldQa = original.final.payload.qa;
  edit(fixture.directory, 'script.json', (doc) => { doc.description += ' Revised description.'; });
  edit(fixture.directory, 'verify.json', (verify) => {
    verify.document_sha256 = sha256(readFileSync(path.join(fixture.directory, 'script.json')));
  });
  const currentQa = await quality(fixture);
  assert.equal(currentQa.ok, true);
  assert.equal(currentQa.final_sha256, oldQa.final_sha256);
  assert.notDeepEqual(currentQa.inputs, oldQa.inputs);
  assert.equal(packageBuild({ directory: fixture.directory, settings: SETTINGS }).report.ok, true);

  const client = site({ onSubmit: async () => structuredClone(original.final) });
  const result = await push({ directory: fixture.directory, client });
  assert.equal(result.final.status, 'approved');
  assert.equal(result.publish, null);
  assert.match(result.waits, /approval for different QA evidence/);
  assert.deepEqual(client.writes.filter((write) => write.method === 'submit').map((write) => write.body.gate), ['final']);
  assert.equal(client.writes.at(-1).method, 'submit', 'stale approval stops before package uploads');
});

test('a reused passing approval cannot override a fresh policy failure with identical local inputs', async (t) => {
  const fixture = await passingBuild(t);
  const original = await push({ directory: fixture.directory, client: site() });
  const currentQa = await quality(fixture, {
    client: { judgePolicy: async () => ({ passed: false, note: 'The current channel rules reject the narration.' }) },
  });
  assert.equal(currentQa.ok, false);
  assert.deepEqual(currentQa.inputs, original.final.payload.qa.inputs);
  assert.equal(currentQa.final_sha256, original.final.payload.qa.final_sha256);
  assert.deepEqual(currentQa.items.filter((item) => !item.ok).map((item) => item.id), ['policy']);
  assert.equal(packageBuild({ directory: fixture.directory, settings: SETTINGS }).report.ok, true);

  const client = site({ onSubmit: async () => structuredClone(original.final) });
  const result = await push({ directory: fixture.directory, client });
  assert.equal(result.publish, null);
  assert.match(result.waits, /approval for different QA evidence/);
  const submitted = client.writes.filter((write) => write.method === 'submit');
  assert.equal(submitted.length, 1);
  assert.equal(submitted[0].body.payload.qa.ok, false);
  assert.equal(submitted[0].body.payload.qa.items.find((item) => item.id === 'policy').ok, false);
  assert.equal(client.writes.at(-1).method, 'submit');
});

test('an approved final response without its stored QA payload cannot publish', async (t) => {
  const { directory } = await passingBuild(t);
  const client = site({ onSubmit: async () => ({ status: 'approved' }) });
  const result = await push({ directory, client });
  assert.equal(result.publish, null);
  assert.match(result.waits, /approval for different QA evidence/);
  assert.deepEqual(client.writes.filter((write) => write.method === 'submit').map((write) => write.body.gate), ['final']);
  assert.equal(client.writes.at(-1).method, 'submit');
});

test('an approval without a usable final review ID stops before uploading its package', async (t) => {
  for (const id of [undefined, null, '', '   ', 7]) {
    await t.test(String(id), async (t) => {
      const { directory } = await passingBuild(t);
      const client = site({ onSubmit: async (body) => ({ id, status: 'approved', payload: structuredClone(body.payload) }) });
      const result = await push({ directory, client });
      assert.equal(result.final.status, 'approved');
      assert.equal(result.publish, null);
      assert.match(result.waits, /without a final review ID/);
      assert.deepEqual(client.writes.filter((write) => write.method === 'submit').map((write) => write.body.gate), ['final']);
      assert.equal(client.writes.at(-1).method, 'submit');
    });
  }
});

test('the same package follows the final review ID returned on each push', async (t) => {
  const { directory } = await passingBuild(t);
  const packages = [];
  for (const finalId of ['00000000-0000-4000-8000-000000000001', '00000000-0000-4000-8000-000000000002']) {
    const client = site({ onSubmit: async (body) => ({
      id: body.gate === 'final' ? finalId : 'publish-review',
      status: 'approved',
      payload: structuredClone(body.payload),
    }) });
    const result = await push({ directory, client });
    assert.equal(result.waits, null);
    const publish = client.writes.find((write) => write.method === 'submit' && write.body.gate === 'publish').body;
    assert.equal(publish.payload.final_review_id, finalId);
    packages.push(publish);
  }
  assert.equal(packages[0].content_sha256, packages[1].content_sha256, 'the metadata bytes did not change');
  assert.notEqual(packages[0].payload.final_review_id, packages[1].payload.final_review_id);
});

test('an owner approval of the current failed QA still permits publishing', async (t) => {
  const fixture = await passingBuild(t);
  const currentQa = await quality(fixture, {
    client: { judgePolicy: async () => ({ passed: false, note: 'The narration needs owner review.' }) },
  });
  assert.equal(currentQa.ok, false);
  packageBuild({ directory: fixture.directory, settings: SETTINGS });
  const client = site({ onSubmit: async (body) => ({ id: `${body.gate}-review`, status: 'approved', payload: structuredClone(body.payload) }) });
  const result = await push({ directory: fixture.directory, client });
  assert.equal(result.final.status, 'approved');
  assert.equal(result.final.payload.qa.ok, false);
  assert.equal(result.publish.status, 'approved');
  assert.equal(result.waits, null);
  assert.deepEqual(client.writes.filter((write) => write.method === 'submit').map((write) => write.body.gate), ['final', 'publish']);
});

test('inputs edited while QA awaits a measurement or service never overwrite the previous report', async (t) => {
  for (const stage of ['measurement', 'policy']) {
    await t.test(stage, async (t) => {
      const fixture = await passingBuild(t);
      const previous = readFileSync(path.join(fixture.directory, 'qa.json'));
      const mutate = async () => {
        await Promise.resolve();
        edit(fixture.directory, 'script.json', (doc) => { doc.description += ' Edited during QA.'; });
      };
      const override = stage === 'measurement'
        ? { measureImpl: async () => { await mutate(); return measured(fixture.timeline); } }
        : { client: { judgePolicy: async () => { await mutate(); return { passed: true }; } } };
      await assert.rejects(quality(fixture, override), /QA inputs changed while checking/);
      assert.deepEqual(readFileSync(path.join(fixture.directory, 'qa.json')), previous);
    });
  }
});

test('an input edited during final uploads prevents submitting the final review', async (t) => {
  const { directory } = await passingBuild(t);
  let changed = false;
  const client = site({ onPart: async () => {
    if (changed) return;
    changed = true;
    edit(directory, 'check.json', (check) => { check.ok = false; });
  } });
  const result = await push({ directory, client });
  assert.match(result.waits, /QA inputs changed during push/);
  assert.equal(result.final, null);
  assert.equal(result.publish, null);
  assert.ok(client.writes.some((write) => write.method === 'part'));
  assert.equal(client.writes.filter((write) => write.method === 'submit').length, 0);
});

test('an input edited during package uploads prevents submitting the publish review', async (t) => {
  const { directory } = await passingBuild(t);
  const metadataHash = sha256(readFileSync(path.join(directory, 'upload/metadata.json')));
  const client = site({ onPart: async ({ hash }) => {
    if (hash === metadataHash) edit(directory, 'verify.json', (verify) => { verify.ok = false; });
  } });
  const result = await push({ directory, client });
  assert.match(result.waits, /QA inputs changed during push/);
  assert.equal(result.final.status, 'approved');
  assert.equal(result.publish, null);
  assert.deepEqual(client.writes.filter((write) => write.method === 'submit').map((write) => write.body.gate), ['final']);
});

test('an input edited while reporting the publish stage prevents submitting the publish review', async (t) => {
  const { directory } = await passingBuild(t);
  const client = site({ onReport: async (body) => {
    if (body.stage === 'publish') edit(directory, 'verify.json', (verify) => { verify.ok = false; });
  } });
  const result = await push({ directory, client });
  assert.match(result.waits, /QA inputs changed during push/);
  assert.equal(result.publish, null);
  assert.deepEqual(client.writes.filter((write) => write.method === 'submit').map((write) => write.body.gate), ['final']);
});
