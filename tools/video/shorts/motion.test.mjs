import assert from 'node:assert/strict';
import test from 'node:test';

import { DISSOLVE_FRAMES, MOTION_SOURCE_SCALE } from '../assemble/drama.mjs';
import { PROFILE } from './core.mjs';
import { backgroundChain, backgroundOf, cameraOf, cardsList, CAMERA_WORDS, firstFrameArgs, lastFrameArgs, sceneSpans, segmentArgs, shortSfxPlan } from './motion.mjs';

const timeline = {
  fps: 30,
  frames: 300,
  cues: [
    { index: 0, sceneIndex: 0, startFrame: 0, endFrame: 60, frames: 60, text: 'a' },
    { index: 1, sceneIndex: 0, startFrame: 60, endFrame: 120, frames: 60, text: 'b' },
    { index: 2, sceneIndex: 1, startFrame: 120, endFrame: 210, frames: 90, text: 'c' },
    { index: 3, sceneIndex: 2, startFrame: 210, endFrame: 300, frames: 90, text: 'd' },
  ],
};

test('a scene is one span of the timeline, and its background is its picture under a camera or the theme backdrop', () => {
  assert.deepEqual(sceneSpans(timeline).map(({ sceneIndex, startFrame, frames, cues }) => [sceneIndex, startFrame, frames, cues.length]), [[0, 0, 120, 2], [1, 120, 90, 1], [2, 210, 90, 1]]);
  assert.equal(backgroundOf({ asset: 'keyframes/a.png', camera: 'push in' }), 'picture');
  assert.equal(backgroundOf({ asset: 'evidence/result.html' }), 'backdrop', "an experiment's evidence stays inside the card");
  assert.equal(backgroundOf({ headline: 'x' }), 'backdrop');
  // As in the long video: "pan left" slides the window right so the picture travels left (assemble/drama.mjs).
  assert.deepEqual(CAMERA_WORDS.map((word) => cameraOf({ camera: word }).name), ['push-in', 'pull-out', 'pan-right', 'pan-left', 'tilt-up', 'tilt-down', 'drift']);
  assert.equal(cameraOf({}).name, 'drift');
});

test('the background chain covers the portrait frame, keeps the middle of a wide picture and travels as the move says', () => {
  const chain = backgroundChain('push-in', 90);
  const w = Math.round(PROFILE.width * MOTION_SOURCE_SCALE);
  const h = Math.round(PROFILE.height * MOTION_SOURCE_SCALE);
  assert.equal(chain[0], `scale=${w}:${h}:force_original_aspect_ratio=increase:flags=lanczos`);
  assert.equal(chain[1], `crop=${w}:${h}`);
  assert.match(chain[2], /^zoompan=z='1\+0\.1\*on\/89':x='iw\/2-\(iw\/zoom\/2\)':y='ih\/2-\(ih\/zoom\/2\)':d=1:s=1080x1920:fps=30$/);
  assert.match(chain[3], /^scale=1080:1920:out_color_matrix=bt709/);
  assert.deepEqual(chain.slice(-2), ['trim=end_frame=90', 'setpts=PTS-STARTPTS']);
  assert.match(backgroundChain('pan-left', 60)[2], /x='\(iw-iw\/zoom\)\*on\/59'/);
  assert.match(backgroundChain('drift', 60)[2], /z='1\+0\.04\*on\/59'/);
});

test('a segment lays the phrases\' cards over the moving background, dissolves from the previous scene, and encodes like every other segment', () => {
  const list = cardsList([{ file: '/w/frames/000.png', frames: 60 }, { file: "/w/it's/001.png", frames: 30 }]);
  assert.equal(list, "ffconcat version 1.0\nfile '/w/frames/000.png'\noption framerate 30\nduration 2.000000\nfile '/w/it'\\''s/001.png'\noption framerate 30\nduration 1.000000\nfile '/w/it'\\''s/001.png'\noption framerate 30\n", 'the last card is named again so its duration holds');
  const cut = segmentArgs({ background: '/w/assets/pic.png', move: 'push-in', frames: 90, cardsList: '/w/build/cards-000.txt', outFile: '/w/clips/000.mp4' });
  assert.deepEqual(cut.slice(0, 13), ['-y', '-v', 'error', '-loop', '1', '-framerate', '30', '-t', '3.000000', '-i', '/w/assets/pic.png', '-f', 'concat']);
  const graph = cut[cut.indexOf('-filter_complex') + 1];
  assert.match(graph, /^\[0:v\]scale=.*zoompan=.*\[pic\];\[1:v\]format=rgba\[cards\];\[pic\]\[cards\]overlay=0:0:eof_action=pass\[carded\];\[carded\]format=yuv420p,setparams=.*\[out\]$/);
  assert.equal(cut.filter((arg) => arg === '-i').length, 2, 'no dissolve input on the first scene');
  assert.ok(cut.includes('-frames:v') && cut[cut.indexOf('-frames:v') + 1] === '90');
  assert.ok(!cut.includes('stillimage'), 'the picture moves');
  const joined = segmentArgs({ background: '/w/backdrops/001.png', move: 'drift', frames: 60, cardsList: '/w/build/cards-001.txt', dissolveFrom: '/w/build/last-000.png', outFile: '/w/clips/001.mp4' });
  assert.equal(joined.filter((arg) => arg === '-i').length, 3);
  assert.match(joined[joined.indexOf('-filter_complex') + 1], new RegExp(`\\[2:v\\]scale=1080:1920,format=yuva420p,fade=t=out:st=0:d=${(DISSOLVE_FRAMES / 30).toFixed(6)}:alpha=1\\[prev\\];\\[pic\\]\\[prev\\]overlay=0:0:eof_action=pass\\[dissolved\\];\\[1:v\\]format=rgba\\[cards\\];\\[dissolved\\]\\[cards\\]overlay`));
  // Every segment shares the encoder, so the join copies.
  for (const args of [cut, joined]) {
    for (const flag of ['libx264', '-profile:v', 'high', '-g', '60', '-keyint_min', '60', '-sc_threshold', '0', '+cgop', 'bt709', '-fps_mode', 'cfr']) assert.ok(args.includes(flag), flag);
  }
  assert.deepEqual(lastFrameArgs('/w/clips/000.mp4', 90, '/w/build/last-000.png'), ['-y', '-v', 'error', '-i', '/w/clips/000.mp4', '-vf', 'select=eq(n\\,89)', '-fps_mode', 'passthrough', '-frames:v', '1', '/w/build/last-000.png']);
  assert.deepEqual(firstFrameArgs('/w/clips/000.mp4', '/w/build/scene-000.png'), ['-y', '-v', 'error', '-i', '/w/clips/000.mp4', '-frames:v', '1', '/w/build/scene-000.png']);
});

test('the sound effects fall on scene changes and big numbers, never at frame 0, never within 1.5 seconds of each other', () => {
  const doc = { scenes: [{ headline: 'a', big: '275' }, { headline: 'b' }, { headline: 'c', big: '3' }] };
  assert.deepEqual(shortSfxPlan(doc, timeline), [
    { frame: 120, sound: 'stamp', scene: 1 },
    { frame: 210, sound: 'stamp', scene: 2 },
  ], 'the first scene\'s big number sits at frame 0, the third\'s pop lands within 1.5 s of its stamp');
  const later = { ...timeline, cues: [...timeline.cues.slice(0, 3), { index: 3, sceneIndex: 2, startFrame: 210, endFrame: 300, frames: 90, text: 'd' }] };
  assert.deepEqual(shortSfxPlan({ scenes: [{ headline: 'a' }, { headline: 'b' }, { headline: 'c' }] }, later).map((event) => event.sound), ['stamp', 'stamp']);
  assert.deepEqual(shortSfxPlan({ scenes: [{ headline: 'only' }] }, { cues: [timeline.cues[0]] }), [], 'one scene has no beat');
});
