import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import { mkdtempSync, mkdirSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { syncBuiltinESMExports } from 'node:module';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { BEATS, PROFILE, buildTimeline, callsToAction, cameraWords, captionHtml, captionWords, saveJson, sceneHtml, sha256, sourcePath, srt, validate, verifyEvidence } from './core.mjs';
import { themeOf } from './layouts.mjs';

const base = fileURLToPath(new URL('../../../docs/videos/ai-shorts/',import.meta.url));
const pilot = () => JSON.parse(readFileSync(path.join(base,'pilots/shorts-receipt-total.json'),'utf8'));

for (const [version, line] of [[1, 'lab'], [2, 'lab'], [2, 'cut'], [2, 'drama']]) {
  const validScript = () => ({
    ...pilot(),
    schema_version: version,
    ...(version === 2 ? { line } : {}),
    ...(line !== 'lab' ? { series: 'source-video', source: { slug: 'source-video' } } : {}),
  });
  test(`v${version} ${line} reports malformed scene collections and rows without throwing`, () => {
    assert.deepEqual(validate(validScript()), []);
    for (const scenes of [{}, 'invalid', 0, true, null, [null], [undefined], [[]], [false]]) {
      let errors;
      assert.doesNotThrow(() => { errors = validate({ ...validScript(), scenes }); }, `scenes: ${JSON.stringify(scenes)}`);
      assert.ok(errors.some((error) => /scenes|scene /.test(error)), `scenes: ${JSON.stringify(scenes)}`);
    }
  });
  test(`v${version} ${line} reports malformed evidence collections and rows without throwing`, () => {
    for (const evidence of [
      {}, 'invalid', 0, true, null, [null], [undefined], [[]], [false],
      [{ path: 123, sha256: 'a'.repeat(64) }], [{ path: ' ', sha256: 'a'.repeat(64) }],
    ]) {
      let errors;
      assert.doesNotThrow(() => { errors = validate({ ...validScript(), evidence }); }, `evidence: ${JSON.stringify(evidence)}`);
      assert.ok(errors.some((error) => error.includes('evidence')), `evidence: ${JSON.stringify(evidence)}`);
    }
  });
}

test('a failed report write preserves the previous complete JSON', (t) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), 'shorts-atomic-report-'));
  const file = path.join(directory, 'qa.json');
  const previous = `${JSON.stringify({ ok: false, final_sha256: 'previous-artifact' }, null, 2)}\n`;
  const originalWrite = fs.writeFileSync;
  writeFileSync(file, previous);
  const interrupted = Object.assign(new Error('simulated interrupted report write'), { code: 'EIO' });
  try {
    t.mock.method(fs, 'writeFileSync', (target, data, ...options) => {
      originalWrite(target, String(data).slice(0, 7), ...options);
      throw interrupted;
    });
    syncBuiltinESMExports();
    assert.throws(() => saveJson(file, { ok: true, final_sha256: 'new-artifact' }), (error) => error === interrupted);
    assert.equal(readFileSync(file, 'utf8'), previous, 'a failed update must not truncate the last report');
  } finally {
    t.mock.restoreAll();
    syncBuiltinESMExports();
    rmSync(directory, { recursive: true, force: true });
  }
});

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

test('schema 2 takes a camera over a picture and the owner\'s music and effect set; schema 1 stays as it was', () => {
  const cut = { schema_version: 2, slug: 'moving-cut', format: 'shorts', locale: 'zh-TW', line: 'cut', series: 'illustrated', titles: ['a', 'b'], description: 'd', source: { slug: 'long-video' }, scenes: [{ headline: '一', narration: ['一句'], shot: 'podium', camera: 'push in' }, { headline: '二', narration: ['兩句'] }, { headline: '三', narration: ['三句'], camera: 'drift' }] };
  assert.deepEqual(validate(cut), []);
  assert.deepEqual(validate({ ...cut, scenes: [{ ...cut.scenes[0], camera: 'zoom' }, ...cut.scenes.slice(1)] }), ['scene 0: camera must be one of push in, pull out, pan left, pan right, tilt up, tilt down, drift (schema 2)']);
  assert.deepEqual(validate({ ...cut, music: { track: 'bed.mp3', gain_db: -22 }, sfx: { set: 'studio-a', gain_db: -12 } }), []);
  assert.deepEqual(validate({ ...cut, music: { prompt: 'light, curious' } }), ['music.track must be a file name like bed.mp3 under <work base>/_music/ (a Short never generates music)', 'music.prompt is not a field of a Short\'s music']);
  assert.deepEqual(validate({ ...cut, music: { track: 'bed.mp3', gain_db: 3 } }), ['music.gain_db must be -40 to 0']);
  assert.deepEqual(validate({ ...cut, sfx: { set: 'Studio A' } }), ['sfx.set must name a sound-effect set under <work base>/_sfx/']);
  const v1 = pilot();
  assert.deepEqual(validate(v1), []);
  assert.ok(validate({ ...v1, scenes: [{ ...v1.scenes[0], camera: 'drift' }, ...v1.scenes.slice(1)] }).some((error) => error.includes('camera')), 'the first format knows no camera');
});

test('a card can be drawn transparent over a moving background, on a panel over a picture, or as the backdrop alone; the safe area never moves', () => {
  const doc = pilot();
  const cue = { sceneIndex: 0, text: '一張手寫的發票' };
  const plain = sceneHtml(doc, cue);
  const transparent = sceneHtml(doc, cue, { transparent: true });
  const onPicture = sceneHtml(doc, cue, { transparent: true, picture: true });
  const backdrop = sceneHtml(doc, cue, { backdrop: true });
  assert.match(plain, /body\{margin:0;width:1080px;height:1920px;overflow:hidden;background:#0b2026/);
  assert.match(transparent, /background:transparent;color/);
  assert.ok(!transparent.includes('class="glow"'), 'the glow belongs to the backdrop');
  assert.match(transparent, /data-transparent="1"/);
  assert.ok(!transparent.includes('class="scrim'), 'no scrims over the backdrop');
  assert.match(onPicture, /<div class="scrim top"><\/div><div class="scrim bottom"><\/div>/);
  assert.match(onPicture, /class="content on-picture"/);
  assert.match(onPicture, /\.content\.on-picture\{height:auto;max-height:1120px/);
  assert.match(backdrop, /data-backdrop="1"/);
  assert.match(backdrop, /<div class="glow"><\/div><\/body>/);
  assert.ok(!backdrop.includes('caption') && !backdrop.includes('h1'), 'the backdrop carries no words');
  for (const page of [plain, transparent, onPicture]) {
    assert.match(page, /\.content\{position:absolute;left:80px;top:258px;width:820px;height:1120px/);
    assert.match(page, /\.caption\{position:absolute;left:80px;top:1430px;width:820px;height:165px/);
  }
  assert.deepEqual(['slow push in', 'pull back a little', 'pan to the left', 'pan right', 'tilt up', 'crane down', 'hold still', undefined].map(cameraWords), ['push in', 'pull out', 'pan left', 'pan right', 'tilt up', 'tilt down', 'drift', 'drift']);
});

test('a karaoke card hides its words behind the caption bar; the layer draws them lit, at the same place, changing only their colour', () => {
  const doc = pilot();
  const cue = { sceneIndex: 0, text: '一張手寫的發票，兩個品項' };
  const lines = ['一張手寫的發票，', '兩個品項'];
  const groups = [{ text: '一張手寫的發票，', line: 0 }, { text: '兩個品項', line: 1 }];
  const plain = sceneHtml(doc, cue, { transparent: true });
  assert.equal(sceneHtml(doc, cue, { transparent: true, caption: null }), plain, 'without a caption contract the markup is what it was');
  assert.ok(!plain.includes('words hidden') && !plain.includes('visibility:hidden'));
  assert.match(plain, /<div class="caption">一張手寫的發票，兩個品項<\/div>/);
  const card = sceneHtml(doc, cue, { transparent: true, caption: { lines, groups } });
  assert.match(card, /<div class="caption"><div class="words hidden"><span class="g">一張手寫的發票，<\/span><br><span class="g">兩個品項<\/span><\/div><\/div>/);
  assert.match(card, /\.caption \.words\.hidden\{visibility:hidden\}/);
  assert.match(card, /\.caption\{position:absolute;left:80px;top:1430px;width:820px;height:165px;padding:14px 20px;background:/, 'the bar keeps its background on the card');
  const layer = captionHtml(doc, { lines, groups, active: 1 });
  assert.match(layer, /data-caption-layer="1"/);
  assert.ok(!layer.includes('class="content') && !layer.includes('<h1') && !layer.includes('class="brand"'), 'the layer is the bar alone');
  assert.match(layer, /\.caption\{position:absolute;left:80px;top:1430px;width:820px;height:165px;padding:14px 20px;border-radius:22px;font-size:49px;line-height:1.36;font-weight:650;display:flex;align-items:center;justify-content:center;text-align:center\}/);
  assert.ok(!/\.caption\{[^}]*background/.test(layer), "the bar's background stays on the card");
  assert.match(layer, /html,body\{[^}]*background:transparent/);
  assert.match(layer, /<div class="caption"><div class="words"><span class="g">一張手寫的發票，<\/span><br><span class="g on">兩個品項<\/span><\/div><\/div>/);
  const rule = /\.g\.on\{([^}]*)\}/.exec(layer)[1];
  assert.deepEqual(rule.split(';').filter(Boolean).map((part) => part.split(':')[0]), ['color', 'text-shadow'], 'only the colour changes between states, never the layout');
  assert.ok(rule.startsWith(`color:${themeOf(doc).colors.highlight}`), 'lit in the theme\'s highlight unless it names a karaoke colour');
  assert.equal(captionWords(lines, groups, 0), '<span class="g on">一張手寫的發票，</span><br><span class="g">兩個品項</span>');
  assert.ok(!captionWords(lines, groups, -1).includes(' on'));
  assert.equal(captionWords(['<b>'], [{ text: '<b>', line: 0 }], 0), '<span class="g on">&lt;b&gt;</span>', 'the words are escaped');
});

test('a schema 2 scene may name its beat, the six in order, a beat over two scenes but never going back; the first format knows none', () => {
  assert.deepEqual(BEATS, ['hook', 'setup', 'turn', 'proof', 'payoff', 'loop']);
  const base = { schema_version: 2, slug: 'six-beats', format: 'shorts', locale: 'zh-TW', line: 'cut', series: 'long-video', titles: ['a', 'b'], description: 'd', source: { slug: 'long-video' } };
  const withBeats = (...beats) => ({ ...base, scenes: beats.map((beat, index) => ({ headline: `第 ${index + 1} 張`, narration: ['一句'], ...(beat ? { beat } : {}) })) });
  assert.deepEqual(validate(withBeats('hook', 'setup', 'turn', 'proof', 'payoff', 'loop')), []);
  assert.deepEqual(validate(withBeats('hook', 'setup', 'setup', 'proof', 'payoff', 'loop')), [], 'a beat may run over two scenes');
  assert.deepEqual(validate(withBeats(null, 'turn', null, 'loop')), [], 'a scene may name none');
  assert.deepEqual(validate(withBeats('hook', 'proof', 'turn')), ['scene 2: beat turn comes after proof; the order is hook, setup, turn, proof, payoff, loop']);
  assert.deepEqual(validate(withBeats('setup', 'hook', 'loop')), ['scene 1: beat hook comes after setup; the order is hook, setup, turn, proof, payoff, loop']);
  assert.deepEqual(validate(withBeats('hook', 'quiz', 'loop')), ['scene 1: beat must be one of hook, setup, turn, proof, payoff, loop (schema 2)']);
  assert.deepEqual(validate(withBeats('hook', 'loop', 'proof', 'loop')), ['scene 2: beat proof comes after loop; the order is hook, setup, turn, proof, payoff, loop'], 'the latest beat named holds, not the last scene\'s');
  const v1 = pilot();
  assert.ok(validate({ ...v1, scenes: [{ ...v1.scenes[0], beat: 'hook' }, ...v1.scenes.slice(1)] }).some((error) => error.includes('beat')), 'the first format knows no beat');
});

test('a call to action is the ask, in Chinese or English, never a word a Short may need', () => {
  for (const text of ['記得訂閱頻道', '別忘了訂閱', '訂閱加開啟小鈴鐺', '按讚', '點個讚', '給我一個讚', '點連結看完整影片', '點擊連結', '追蹤我們', '請追蹤', '追蹤一下', 'Subscribe for more', 'hit that like button', 'like and subscribe', 'ring the bell', 'link in bio', 'click the link', 'follow us']) {
    assert.ok(callsToAction(text).length, text);
  }
  for (const text of ['訂閱制方案每月 20 美元', '付費訂閱的差別', '追蹤包裹的進度', '追蹤這個數字', '完整影片在說明欄', '這條線像鐘形曲線', 'the subscription plan', 'unsubscribe from the list', 'follow the steps', 'a bell curve', 'I like it', '', undefined]) {
    assert.deepEqual(callsToAction(text), [], String(text));
  }
  assert.deepEqual(callsToAction('按讚、訂閱我們，再開小鈴鐺'), ['按讚', '小鈴鐺', '訂閱我們'], 'every ask, as the words that make it');
});
