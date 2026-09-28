import test from 'node:test';
import assert from 'node:assert/strict';
import { loudnessResult } from './build.mjs';

test('ffmpeg progress after the JSON loudness block is not mistaken for JSON',()=>{
  const stats={input_i:'-14.1',input_tp:'-1.2',input_lra:'3.0',input_thresh:'-24.2',target_offset:'0.0'};
  assert.deepEqual(loudnessResult('progress\n'+JSON.stringify(stats)+'\n[out#0/null] muxing overhead: unknown\nframe=123'),stats);
  assert.throws(()=>loudnessResult('no statistics'),/did not report/);
  assert.throws(()=>loudnessResult(JSON.stringify({...stats,input_i:'-inf'})),/invalid loudness/);
});
