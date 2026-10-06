// A Short's listening check (check.mjs checkAudio) through the speech journal in its build
// directory (tts/speech-journal.mjs), with the real client and an injected counting fetch:
// nothing here reaches a live, paid endpoint.
import assert from 'node:assert/strict';
import { existsSync, mkdirSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import test from 'node:test';

import { tempDir } from '../core/fixtures/load.mjs';
import { SPEECH_UNCERTAIN, SpeechError } from '../tts/client.mjs';
import { JOURNAL_DIR, listSpeechJournal, main as journalCli } from '../tts/speech-journal.mjs';
import { encodeWav } from '../tts/wav.mjs';
import { CHECK_FILE, checkAudio, transcribable } from './check.mjs';

const TOKEN = `mkv_${'s'.repeat(43)}`;
const SITE = 'https://mokaair.test';
const PHRASES = ['一張手寫的發票', '再扣掉三十元的折價券', '最後只付了一百二十元'];
// The transcriber hears the second phrase with one character wrong, so Jev is asked about it.
const MISHEARD = '再扣掉三十元的這價券';
const clip = (pitch) => encodeWav(Int16Array.from({ length: 24_000 }, (_, index) => Math.round(8000 * Math.sin(index / pitch))));
const lost = () => Object.assign(new TypeError('fetch failed'), { cause: Object.assign(new Error('socket hang up'), { code: 'ECONNRESET' }) });
const held = (pattern = /./) => (error) => error instanceof SpeechError && error.code === SPEECH_UNCERTAIN && error.who === 'owner' && pattern.test(error.message);
const silent = { stdout: { write() {} }, stderr: { write() {} } };

/** A build directory as `build` leaves it, as far as the check reads it: the script and one clip per phrase. */
function buildDir() {
  const directory = path.join(tempDir('shorts-check-journal-'), 'shorts-receipt', 'build-1');
  mkdirSync(path.join(directory, 'audio'), { recursive: true });
  writeFileSync(path.join(directory, 'script.json'), JSON.stringify({ scenes: [{ narration: PHRASES }] }));
  PHRASES.forEach((_phrase, index) => writeFileSync(path.join(directory, 'audio', `${String(index).padStart(3, '0')}.wav`), clip(5 + index * 2)));
  return directory;
}

/**
 * The site's transcriber and Jev, counting their paid POSTs. A clip the build had when this site
 * was made is heard as its phrase (the second with one character wrong), any other as noise; Jev
 * passes every line; the `transcribe` and `judge` queues answer first, in turn (undefined: the
 * usual answer).
 */
function site(directory, { transcribe = [], judge = [] } = {}) {
  const posts = { transcribe: [], judge: [] };
  const known = new Map(PHRASES.map((_phrase, index) => [transcribable(readFileSync(path.join(directory, 'audio', `${String(index).padStart(3, '0')}.wav`))).toString('base64'), index]));
  const fetchImpl = async (url, init) => {
    const body = JSON.parse(init.body);
    if (url.endsWith('/api/video/speech/transcribe')) {
      posts.transcribe.push(body);
      const answer = transcribe.shift();
      if (answer) return answer(body);
      const index = known.get(body.audio);
      return Response.json({ text: index === undefined ? '聽不清楚' : index === 1 ? MISHEARD : PHRASES[index] });
    }
    assert.ok(url.endsWith('/api/video/speech/judge'), `unexpected request: ${url}`);
    posts.judge.push(body);
    const answer = judge.shift();
    if (answer) return answer(body);
    return Response.json({ results: body.lines.map((line) => ({ id: line.id, noul: 0.9 })) });
  };
  return { posts, client: { site: SITE, token: TOKEN, fetch: fetchImpl, sleep: async () => {} }, queue: { transcribe, judge } };
}

const check = (directory, server) => checkAudio({ directory, client: server.client });
const journalOf = (directory) => listSpeechJournal(path.join(directory, JOURNAL_DIR)).map((entry) => [entry.path, entry.status]).sort();
// atomicWrite's temporary file for check.json in this process: a directory there makes the save fail.
const blockSave = (directory) => mkdirSync(`${path.join(directory, CHECK_FILE)}.${process.pid}.tmp`, { recursive: true });
const unblockSave = (directory) => rmSync(`${path.join(directory, CHECK_FILE)}.${process.pid}.tmp`, { recursive: true, force: true });

test("a Short's check holds a transcription whose answer was lost, and keeps the ones it bought for the next run", async () => {
  const directory = buildDir();
  const server = site(directory, { transcribe: [undefined, () => { throw lost(); }] });
  const journal = path.join(directory, JOURNAL_DIR);
  const first = await check(directory, server).catch((error) => error);
  assert.ok(held(/^POST \/api\/video\/speech\/transcribe was sent and no usable answer came back \(socket hang up\)/)(first), first.message);
  assert.equal(first.journal, journal, 'the hold names the build directory\'s journal');
  assert.match(first.message, new RegExp(`forget --dir "[^"]+" --sha ${first.requestSha256} \\(${SPEECH_UNCERTAIN}`));
  assert.equal(server.posts.transcribe.length, 2);
  assert.ok(!existsSync(path.join(directory, CHECK_FILE)));
  assert.deepEqual(journalOf(directory), [['speech/transcribe', 'confirmed'], ['speech/transcribe', 'held']]);

  // The lab or the owner runs the check again: the first phrase comes from the journal, the second holds.
  await assert.rejects(check(directory, server), held(/is held in the speech journal/));
  assert.equal(server.posts.transcribe.length, 2, 'the next check sends nothing');

  assert.equal(journalCli(['forget', '--dir', journal, '--sha', first.requestSha256], silent), 0);
  const done = await check(directory, server);
  assert.equal(server.posts.transcribe.length, 4, 'only the forgotten phrase and the one never asked for');
  assert.equal(server.posts.judge.length, 1);
  assert.deepEqual([done.ok, done.checked, done.transcribe_calls, done.judge_calls], [true, 3, 2, 1], 'the phrase an earlier check paid for is not counted again');
  assert.deepEqual(done.results.map((result) => result.heard), [PHRASES[0], MISHEARD, PHRASES[2]]);
  const saved = JSON.parse(readFileSync(path.join(directory, CHECK_FILE), 'utf8'));
  assert.deepEqual([saved.ok, saved.transcribe_calls, saved.judge_calls], [true, 2, 1]);
  assert.deepEqual(readdirSync(journal), [], 'released once check.json is written');

  // A check of the build after that asks again, as before: a Short keeps no transcript cache.
  const again = await check(directory, server);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length, again.transcribe_calls, again.judge_calls], [7, 2, 3, 1]);
});

test("a Short's check holds a Jev call whose answer broke, without buying the transcripts again", async () => {
  const directory = buildDir();
  const broken = () => new Response('{"results":[', { status: 200, headers: { 'Content-Type': 'application/json' } });
  const server = site(directory, { judge: [broken] });
  await assert.rejects(check(directory, server), held(/^POST \/api\/video\/speech\/judge was sent and no usable answer came back \(the answer could not be read/));
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [3, 1]);
  const again = await check(directory, server).catch((error) => error);
  assert.ok(held(/speech\/judge is held in the speech journal/)(again), again.message);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [3, 1], 'neither is sent again');

  assert.equal(journalCli(['forget', '--dir', again.journal, '--sha', again.requestSha256], silent), 0);
  const done = await check(directory, server);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [3, 2]);
  assert.deepEqual([done.ok, done.transcribe_calls, done.judge_calls], [true, 0, 1]);
  assert.deepEqual(readdirSync(again.journal), []);
});

test("a Short's check that stopped before saving check.json takes what it bought from the journal; a changed clip is asked again", async () => {
  const directory = buildDir();
  const server = site(directory);
  // What a check that never stopped makes of the same script and clips, in another build.
  const other = buildDir();
  const plain = await check(other, site(other));

  blockSave(directory);
  await assert.rejects(check(directory, server), 'saving check.json fails after every answer came back');
  unblockSave(directory);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [3, 1]);
  assert.deepEqual(journalOf(directory), [['speech/judge', 'confirmed'], ['speech/transcribe', 'confirmed'], ['speech/transcribe', 'confirmed'], ['speech/transcribe', 'confirmed']]);
  const resumed = await check(directory, server);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [3, 1], 'nothing is bought again');
  assert.deepEqual([resumed.transcribe_calls, resumed.judge_calls], [0, 0]);
  assert.deepEqual({ ...resumed, transcribe_calls: 3, judge_calls: 1 }, plain, 'the same check as one that never stopped');
  assert.deepEqual(readdirSync(path.join(directory, JOURNAL_DIR)), []);

  // Stopped again; then the third clip is made again before the next check.
  blockSave(directory);
  await assert.rejects(check(directory, server));
  unblockSave(directory);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [6, 2]);
  writeFileSync(path.join(directory, 'audio', '002.wav'), clip(17));
  const changed = await check(directory, server);
  assert.deepEqual([server.posts.transcribe.length, server.posts.judge.length], [7, 3], 'the new clip is transcribed, and Jev asked about the new transcript');
  assert.deepEqual(server.posts.judge.at(-1).lines.map((line) => line.heard), [MISHEARD, '聽不清楚']);
  assert.deepEqual([changed.transcribe_calls, changed.judge_calls, changed.results[2].heard], [1, 1, '聽不清楚']);
  // What the stopped check bought for the old clip was never asked for again: it stays, confirmed,
  // and holds nothing.
  assert.deepEqual(journalOf(directory), [['speech/judge', 'confirmed'], ['speech/transcribe', 'confirmed']]);
});
