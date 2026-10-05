import assert from 'node:assert/strict';
import test from 'node:test';

import { DISSOLVE_FRAMES, MOTION_SOURCE_SCALE } from '../assemble/drama.mjs';
import { PROFILE } from './core.mjs';
import { backgroundChain, backgroundOf, cameraOf, cardsList, CAMERA_WORDS, COVER_MIN_PSNR, firstFrameArgs, framePsnrArgs, lastFrameArgs, LOOP_FRAMES, LOOP_MIN_PSNR, loopProblems, MOTION_VERSION, parsePsnr, PSNR_CAP, psnrText, psnrValue, sceneSpans, segmentArgs, shortSfxPlan } from './motion.mjs';

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

test('the caption layer is the last input, laid over the cards at the bar; without it the arguments are what they were', () => {
  assert.equal(MOTION_VERSION, 'shorts-motion-v3');
  const scene = { background: '/w/assets/pic.png', move: 'push-in', frames: 90, cardsList: '/w/build/cards-000.txt', outFile: '/w/clips/000.mp4' };
  const plain = segmentArgs(scene);
  assert.deepEqual(segmentArgs({ ...scene, captionsList: null }), plain);
  assert.ok(!plain.some((arg) => arg.includes('captions')), 'a plain cut knows no layer');
  const lit = segmentArgs({ ...scene, captionsList: '/w/build/captions-000.txt' });
  assert.equal(lit.filter((arg) => arg === '-i').length, 3);
  const after = lit.indexOf('/w/build/cards-000.txt') + 1;
  assert.deepEqual(lit.slice(after, after + 6), ['-f', 'concat', '-safe', '0', '-i', '/w/build/captions-000.txt'], 'the layer is the last input');
  assert.match(lit[lit.indexOf('-filter_complex') + 1], /\[1:v\]format=rgba\[cards\];\[pic\]\[cards\]overlay=0:0:eof_action=pass\[carded\];\[2:v\]format=rgba\[captions\];\[carded\]\[captions\]overlay=80:1430:eof_action=pass\[captioned\];\[captioned\]format=yuv420p,setparams=.*\[out\]$/);
  const dissolved = segmentArgs({ ...scene, dissolveFrom: '/w/build/last-000.png', captionsList: '/w/build/captions-001.txt' });
  assert.equal(dissolved.filter((arg) => arg === '-i').length, 4);
  assert.match(dissolved[dissolved.indexOf('-filter_complex') + 1], /\[2:v\]scale=1080:1920,format=yuva420p,fade=t=out:st=0:d=0\.500000:alpha=1\[prev\];\[pic\]\[prev\]overlay=0:0:eof_action=pass\[dissolved\];\[1:v\]format=rgba\[cards\];\[dissolved\]\[cards\]overlay=0:0:eof_action=pass\[carded\];\[3:v\]format=rgba\[captions\];\[carded\]\[captions\]overlay=80:1430:eof_action=pass\[captioned\];\[captioned\]format=yuv420p/);
  for (const flag of ['libx264', '-g', '60', '-sc_threshold', '0', '+cgop', '-fps_mode', 'cfr']) assert.ok(lit.includes(flag), flag);
  // The layer's list is the cards' ffconcat: every state held for its frames, the last named again.
  assert.equal(cardsList([{ file: '/w/captions/000-00.png', frames: 40 }, { file: '/w/captions/000-01.png', frames: 20 }]), "ffconcat version 1.0\nfile '/w/captions/000-00.png'\noption framerate 30\nduration 1.333333\nfile '/w/captions/000-01.png'\noption framerate 30\nduration 0.666667\nfile '/w/captions/000-01.png'\noption framerate 30\n");
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

test('the last scene ends on the first frame: the still fades in by frame count over the loop frames, over everything, repeated to the end', () => {
  assert.equal(LOOP_FRAMES, 12);
  const scene = { background: '/w/backdrops/002.png', move: 'drift', frames: 90, cardsList: '/w/build/cards-002.txt', dissolveFrom: '/w/build/last-001.png', captionsList: '/w/build/captions-002.txt', outFile: '/w/clips/002.mp4' };
  const plain = segmentArgs(scene);
  assert.deepEqual(segmentArgs({ ...scene, loopTo: null }), plain);
  assert.ok(!plain.some((arg) => arg.includes('[loop]') || arg.includes('scene-000.png')), 'without a loop the arguments are what they were');
  const looped = segmentArgs({ ...scene, loopTo: '/w/build/scene-000.png' });
  assert.equal(looped.filter((arg) => arg === '-i').length, 5);
  const after = looped.indexOf('/w/build/captions-002.txt') + 1;
  assert.deepEqual(looped.slice(after, after + 8), ['-loop', '1', '-framerate', '30', '-t', (14 / 30).toFixed(6), '-i', '/w/build/scene-000.png'], 'the still is the last input, two frames longer than its fade');
  const graph = looped[looped.indexOf('-filter_complex') + 1];
  assert.match(graph, /\[2:v\]scale=1080:1920,format=yuva420p,fade=t=out:st=0:d=0\.500000:alpha=1\[prev\];\[pic\]\[prev\]overlay=0:0:eof_action=pass\[dissolved\];\[1:v\]format=rgba\[cards\];\[dissolved\]\[cards\]overlay=0:0:eof_action=pass\[carded\];\[3:v\]format=rgba\[captions\];\[carded\]\[captions\]overlay=80:1430:eof_action=pass\[captioned\];/, 'the dissolve and the caption layer are where they were');
  assert.match(graph, /\[captioned\];\[4:v\]scale=1080:1920,format=yuva420p,fade=t=in:s=0:n=12:alpha=1,setpts=PTS\+2\.566667\/TB\[loop\];\[captioned\]\[loop\]overlay=0:0:eof_action=repeat\[looped\];\[looped\]format=yuv420p,setparams=.*\[out\]$/, 'the still fades in over the last twelve frames of ninety and is the last frame');
  assert.ok(looped.includes('-frames:v') && looped[looped.indexOf('-frames:v') + 1] === '90');
  const bare = segmentArgs({ background: '/w/backdrops/002.png', move: 'drift', frames: 10, cardsList: '/w/build/cards-002.txt', loopTo: '/w/build/scene-000.png', outFile: '/w/clips/002.mp4' });
  assert.equal(bare.filter((arg) => arg === '-i').length, 3);
  assert.match(bare[bare.indexOf('-filter_complex') + 1], /\[carded\];\[2:v\]scale=1080:1920,format=yuva420p,fade=t=in:s=0:n=12:alpha=1,setpts=PTS\+0\.000000\/TB\[loop\];\[carded\]\[loop\]overlay=0:0:eof_action=repeat\[looped\]/, 'a scene shorter than the tail starts the fade at its first frame');
});

test('the two ends of a cut are measured as PSNR in RGB on one clock, read from ffmpeg, and judged against the loop thresholds', () => {
  assert.deepEqual(framePsnrArgs('/w/upload/final.mp4', 0, '/w/upload/cover.png'), ['-hide_banner', '-nostats', '-i', '/w/upload/final.mp4', '-i', '/w/upload/cover.png', '-lavfi', '[0:v]select=eq(n\\,0),setpts=PTS-STARTPTS,format=rgb24[a];[1:v]format=rgb24[b];[a][b]psnr', '-frames:v', '1', '-f', 'null', '-']);
  assert.deepEqual(framePsnrArgs('/w/upload/final.mp4', 1055, '/w/upload/final.mp4', 0), ['-hide_banner', '-nostats', '-i', '/w/upload/final.mp4', '-i', '/w/upload/final.mp4', '-lavfi', '[0:v]select=eq(n\\,1055),setpts=PTS-STARTPTS,format=rgb24[a];[1:v]select=eq(n\\,0),setpts=PTS-STARTPTS,format=rgb24[b];[a][b]psnr', '-frames:v', '1', '-f', 'null', '-']);
  assert.equal(parsePsnr('[Parsed_psnr_2 @ 0x1] PSNR r:48.130804 g:inf b:inf average:52.902016 min:52.902016 max:52.902016\n'), 52.902016);
  assert.equal(parsePsnr('PSNR y:inf u:inf v:inf average:inf min:inf max:inf'), Infinity);
  assert.throws(() => parsePsnr('nothing measured'), /did not report a PSNR/);
  assert.deepEqual([psnrValue(Infinity), psnrValue(52.902016), psnrValue(116.2), PSNR_CAP], [100, 52.9, 100, 100]);
  assert.deepEqual([psnrText(Infinity), psnrText(52.902016), psnrText(undefined)], ['inf, identical', '52.9 dB', 'not measured']);
  assert.deepEqual([COVER_MIN_PSNR, LOOP_MIN_PSNR], [40, 30]);
  assert.deepEqual(loopProblems({ cover_psnr: Infinity, loop_psnr: 52.9 }), []);
  assert.deepEqual(loopProblems({ cover_psnr: 40, loop_psnr: 30 }), [], 'the thresholds are inclusive');
  assert.deepEqual(loopProblems({ cover_psnr: 31.2, loop_psnr: 12 }), ['the cover is not the first frame (PSNR 31.2 dB, below 40 dB)', 'the last frame does not return to the first (PSNR 12.0 dB, below 30 dB)']);
  assert.deepEqual(loopProblems(null), ['the first and last frames were not measured against the cover']);
  assert.deepEqual(loopProblems({}), ['the cover is not the first frame (PSNR not measured, below 40 dB)', 'the last frame does not return to the first (PSNR not measured, below 30 dB)'], 'a missing number never passes');
});
