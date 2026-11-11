import test from 'node:test';
import assert from 'node:assert/strict';
import { loudnessProblems, loudnessResult, narrationLoudnormFilter } from './build.mjs';

test('ffmpeg progress after the JSON loudness block is not mistaken for JSON',()=>{
  const stats={input_i:'-14.1',input_tp:'-1.2',input_lra:'3.0',input_thresh:'-24.2',target_offset:'0.0'};
  assert.deepEqual(loudnessResult('progress\n'+JSON.stringify(stats)+'\n[out#0/null] muxing overhead: unknown\nframe=123'),stats);
  assert.throws(()=>loudnessResult('no statistics'),/did not report/);
  assert.throws(()=>loudnessResult(JSON.stringify({...stats,input_i:'-inf'})),/invalid loudness/);
});

test('the narration-only mix aims under the true-peak gate, leaving headroom for the AAC encode', () => {
  const filter = narrationLoudnormFilter({ input_i: '-20.1', input_tp: '-3.2', input_lra: '4.0', input_thresh: '-30.5', target_offset: '0.2' });
  const tp = Number(filter.match(/loudnorm=I=-14:TP=(-[\d.]+):/)[1]);
  assert.ok(tp <= -1.5, `TP target ${tp}`);
  assert.match(filter, /measured_I=-20\.1:measured_TP=-3\.2:measured_LRA=4\.0:measured_thresh=-30\.5:offset=0\.2:linear=true/);
  assert.deepEqual(loudnessProblems({ input_i: '-14.0', input_tp: String(tp + 0.5) }), []);
  assert.equal(loudnessProblems({ input_i: '-14.0', input_tp: '-0.65' }).length, 1);
});
