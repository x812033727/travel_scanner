import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { PROFILE, buildTimeline, sceneHtml, sha256, sourcePath, srt, validate, verifyEvidence } from './core.mjs';

const base = fileURLToPath(new URL('../../../docs/videos/ai-shorts/',import.meta.url));
const pilot = () => JSON.parse(readFileSync(path.join(base,'pilots/shorts-receipt-total.json'),'utf8'));

test('actual pilot sources are intact and all three scripts have bounded real-evidence scenes',()=>{
  for(const slug of ['shorts-receipt-total','shorts-poster-blind','shorts-prompt-check']){
    const doc=JSON.parse(readFileSync(path.join(base,`pilots/${slug}.json`),'utf8'));
    assert.deepEqual(validate(doc),[]);
    assert.ok(verifyEvidence(doc,base).length>=2);
  }
});
test('evidence modification and path traversal fail before rendering',()=>{
  const temp=mkdtempSync(path.join(os.tmpdir(),'shorts-evidence-'));
  try{
    const root=path.join(temp,'source');mkdirSync(root);
    writeFileSync(path.join(root,'answer.txt'),'275');
    writeFileSync(path.join(temp,'outside.txt'),'private');
    const doc={evidence:[{path:'answer.txt',sha256:sha256('275')}]};
    assert.equal(verifyEvidence(doc,root).length,1);
    writeFileSync(path.join(root,'answer.txt'),'300');
    assert.throws(()=>verifyEvidence(doc,root),/evidence changed/);
    assert.throws(()=>sourcePath(root,'../outside.txt'),/outside campaign/);
  } finally {rmSync(temp,{recursive:true,force:true});}
});
test('captions follow measured speech on frame boundaries, never guessed word duration',()=>{
  const doc={scenes:[{narration:['第一句','第二句','第三句']}]};
  const timing=buildTimeline(doc,[8.123,9.751,9.003]);
  assert.equal(timing.cues[1].startFrame,timing.cues[0].endFrame);
  assert.equal(timing.cues[2].endFrame,timing.frames);
  for(const [i,cue] of timing.cues.entries()) assert.ok(cue.frames/PROFILE.fps>[8.123,9.751,9.003][i]);
  assert.match(srt(timing),/^1\n00:00:00,000 --> 00:00:08,333\n第一句/);
  assert.throws(()=>buildTimeline(doc,[8,9]),/every phrase/);
  assert.throws(()=>buildTimeline(doc,[20,20,20]),/never truncate/);
  assert.throws(()=>buildTimeline(doc,[0,10,20]),/positive/);
});
test('rendered result text is escaped and undeclared assets are refused',()=>{
  const doc=pilot();
  doc.scenes[0].headline='<script>alert(1)</script>';
  const html=sceneHtml(doc,{sceneIndex:0,text:'<img src=x onerror=bad>'});
  assert.ok(!html.includes('<script>'));
  assert.ok(html.includes('&lt;script&gt;'));
  assert.ok(!html.includes('<img src=x'));
  doc.scenes[0].asset='unknown.png';
  assert.ok(validate(doc).some(e=>e.includes('evidence-bound')));
});
test('measurable answer key agrees with raw outputs, with no claim of OCR or model ranking',()=>{
  const receipt=85*2+45*3-30;
  assert.equal(receipt,275);
  const keys=[String(240*.8-30),String(3*2*45),'11:20'];
  for(const file of ['plain.json','structured.json']){
    const result=JSON.parse(readFileSync(path.join(base,'experiments',file),'utf8'));
    assert.ok(result.receipt_answer.includes(String(receipt)));
    keys.forEach((answer,i)=>assert.ok(result.quiz_answers[i].includes(answer)));
  }
});
