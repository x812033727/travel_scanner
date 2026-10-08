import assert from 'node:assert/strict';
import { once } from 'node:events';
import { mkdtemp, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { spawn } from 'node:child_process';
import { test } from 'node:test';
import { fileURLToPath } from 'node:url';
import { MediaController, replaceCues } from './preview/controller.mjs';

class Media extends EventTarget {
  muted = false; volume = 1; playbackRate = 1; defaultPlaybackRate = 1;
  currentTime = 0; readyState = 0; paused = true; seeking = false; src = '';
  load() { this.currentTime = 0; this.readyState = 0; this.playbackRate = 1; }
  removeAttribute(name) { if (name === 'src') this.src = ''; }
  pause() { this.paused = true; this.dispatchEvent(new Event('pause')); }
  async play() { this.paused = false; this.dispatchEvent(new Event('play')); }
  ready() { this.readyState = 4; this.dispatchEvent(new Event('loadedmetadata')); }
}
const lesson = (day) => ({ day, master: `day${day}.mp4`, audio: { ja: `day${day}.ja.m4a`, ko: `day${day}.ko.m4a` } });
function setup() {
  const video = new Media(), audio = new Media();
  const messages = [];
  const controller = new MediaController(video, audio, { timeout: 200, update: (message) => { if (message) messages.push(message); } });
  controller.selectLesson(lesson(2)); video.ready();
  return { video, audio, controller, messages };
}

test('Day02 -> Day03 -> Day02 retains exactly the current caption cues', () => {
  const stored = [];
  const track = { mode: 'disabled', get cues() { return this.mode === 'disabled' ? null : stored; },
    addCue(cue) { stored.push(cue); }, removeCue(cue) { stored.splice(stored.indexOf(cue), 1); } };
  class Cue { constructor(startTime, endTime, text) { Object.assign(this, { startTime, endTime, text }); } }
  for (const day of [2, 3, 2]) {
    track.mode = 'disabled';
    replaceCues(track, [[0, 3, `day${day}-first`], [3, 6, `day${day}-second`]], Cue);
    assert.deepEqual(stored.map((cue) => cue.text), [`day${day}-first`, `day${day}-second`]);
    assert.equal(track.mode, 'hidden');
  }
});

for (const muted of [false, true]) test(`failed alternate recovers English and preserves user mute=${muted}`, async () => {
  const { video, audio, controller, messages } = setup();
  controller.setMuted(muted);
  await video.play();
  const switching = controller.selectVoice('ko');
  assert.equal(video.muted, true);
  audio.dispatchEvent(new Event('error'));
  await switching;
  assert.equal(controller.voice, 'en');
  assert.equal(video.muted, muted);
  assert.equal(audio.src, '');
  assert.equal(video.paused, false);
  assert.equal(controller.loading, false);
  assert.match(messages.join(' '), /已切回英文/);
  controller.destroy();
});

test('episode changes preserve speed, volume and mute after metadata resets', async () => {
  const { video, audio, controller } = setup();
  controller.setRate(1.25); controller.setVolume(0.35); controller.setMuted(true);
  const switching = controller.selectVoice('ja'); audio.ready(); await switching;
  controller.selectLesson(lesson(3));
  video.playbackRate = 1; video.ready();
  assert.equal(controller.voice, 'en');
  assert.equal(video.playbackRate, 1.25);
  assert.equal(audio.playbackRate, 1.25);
  assert.equal(video.volume, 0.35);
  assert.equal(video.muted, true);
  assert.equal(video.paused, true);
  controller.destroy();
});

test('alternate follows seek, pause, playback rate, and resumes after seek', async () => {
  const { video, audio, controller } = setup();
  const switching = controller.selectVoice('ja'); audio.ready(); await switching;
  await video.play();
  video.seeking = true; video.dispatchEvent(new Event('seeking'));
  assert.equal(audio.paused, true);
  video.currentTime = 480;
  video.seeking = false; video.dispatchEvent(new Event('seeked'));
  assert.equal(audio.currentTime, 480);
  assert.equal(audio.paused, false);
  controller.setRate(0.75);
  assert.equal(audio.playbackRate, 0.75);
  video.pause(); assert.equal(audio.paused, true);
  controller.destroy();
});

test('changing episode cancels pending voice load without a stale fallback or autoplay', async () => {
  const { video, audio, controller, messages } = setup();
  await video.play();
  const switching = controller.selectVoice('ja');
  controller.selectLesson(lesson(3));
  audio.ready(); await switching;
  assert.equal(video.src, 'day3.mp4');
  assert.equal(video.paused, true);
  assert.equal(controller.voice, 'en');
  assert.equal(video.muted, false);
  assert.equal(messages.some((message) => message.includes('載入失敗')), false);
  controller.destroy();
});

test('local launcher serves byte ranges and refuses invalid ranges', async () => {
  const directory = await mkdtemp(path.join(tmpdir(), 'airport-preview-'));
  const launcher = fileURLToPath(new URL('./preview/serve.py', import.meta.url));
  let server;
  try {
    await writeFile(path.join(directory, 'START_HERE.html'), 'preview');
    await writeFile(path.join(directory, 'test.mp4'), '0123456789');
    server = spawn('python3', [launcher, '--directory', directory, '--port', '0'], { stdio: ['ignore', 'pipe', 'pipe'] });
    const [output] = await once(server.stdout, 'data');
    const base = String(output).match(/http:\/\/127\.0\.0\.1:\d+/)?.[0];
    assert.ok(base, String(output));
    for (const [range, status, expected] of [['bytes=2-5', 206, '2345'], ['bytes=-3', 206, '789'], ['bytes=8-', 206, '89'], ['bytes=20-', 416, '']]) {
      const response = await fetch(`${base}/test.mp4`, { headers: { Range: range } });
      assert.equal(response.status, status);
      assert.equal(await response.text(), expected);
    }
    const response = await fetch(`${base}/START_HERE.html`);
    assert.equal(await response.text(), 'preview');
  } finally {
    if (server) { server.kill(); await once(server, 'exit'); }
    await rm(directory, { recursive: true, force: true });
  }
});
