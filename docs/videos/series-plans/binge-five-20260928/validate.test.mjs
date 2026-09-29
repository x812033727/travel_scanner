import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs/promises';
import os from 'node:os';
import path from 'node:path';
import { SLUGS, compile, hash, loadSource } from './build.mjs';
import { validateSource, validateReview, validateFiles } from './validate.mjs';
import { REQUIRED_VERDICTS } from '../../../../tools/video/automation/series.mjs';

const original=await loadSource('wedding-reckoning');
const clone=()=>structuredClone(original);
test('complete authored plan passes the existing production document checks',()=>assert.deepEqual(validateSource(original),[]));
test('rejects a missing episode',()=>{const s=clone();s.chapters[1].episodes.pop();assert.ok(validateSource(s).some(e=>e.includes('expected 40')));});
test('rejects unknown cast and scene references',()=>{const s=clone();s.chapters[0].episodes[0].characters[0]='unregistered';s.chapters[0].episodes[0].locations[0]='unregistered';const e=validateSource(s);assert.ok(e.some(x=>x.includes('unknown character')));assert.ok(e.some(x=>x.includes('unknown location')));});
test('checks ending variation across chapter boundaries',()=>{const s=clone();s.chapters[1].episodes[0].cliffhanger.type=s.chapters[0].episodes[9].cliffhanger.type;assert.ok(validateSource(s).some(e=>e.includes('including chapter boundary')));});
test('rejects unearned payoffs before planting',()=>{const s=clone();s.chapters[0].episodes[0].payoffs.push('m07');assert.ok(validateSource(s).some(e=>e.includes('payoff before planting')));});
test('rejects a mystery without on-screen resolution',()=>{const s=clone();const m=s.setting.mysteries.find(m=>m.id==='m09');s.chapters.flatMap(c=>c.episodes).find(e=>e.number===m.revealed).payoffs=[];assert.ok(validateSource(s).some(e=>e.includes('missing actual resolution')));});
test('does not mistake the final emotional payoff for an open sequel',()=>{const s=clone();s.chapters[3].episodes[9].closed_ending=false;assert.ok(validateSource(s).some(e=>e.includes('closure must be reserved')));});
test('requires a concrete first reward planned within thirty seconds',()=>{const s=clone();s.chapters[0].episodes[0].satisfaction[0].planned_seconds=45;assert.ok(validateSource(s).some(e=>e.includes('within 30 seconds')));});
test('rejects thumbnail references to later material unavailable to the compiler',()=>{const s=clone();s.packaging.thumbnail_variants[0].episode=35;assert.ok(validateSource(s).some(e=>e.includes('reference outside first three')));});

test('rejects an appearance that only holds for some episodes',()=>{
  for(const words of ['navy suit; no veil after episode 1','a cane, later a wheelchair','orderly at first']){
    const s=clone();s.setting.characters[0].appearance=`East Asian woman, 28, ${words}.`;
    assert.ok(validateSource(s).some(e=>e.includes('must not depend on the episode')),words);
  }
});

test('rejects a missing required compilation tag',()=>{const s=clone();s.packaging.tags=s.packaging.tags.filter(t=>t!=='AI漫劇');assert.ok(validateSource(s).includes('missing required tag: AI漫劇'));});

test('renders structured narrator casting in the human-readable setting',()=>{const s=clone();s.setting.world.narrator={provider:'gemini',name:'Sulafat',style:'沉穩台灣國語'};assert.ok(compile(s)['setting.md'].includes('gemini / Sulafat / 沉穩台灣國語'));});

test('generated artifacts and manifest remain valid after Git LF normalization',()=>{const files=compile(clone());const manifest=JSON.parse(files['manifest.json']);for(const [name,body] of Object.entries(files)){const checkout=body.replaceAll('\r\n','\n');assert.ok(body===checkout,`${name} changes during Git checkout`);if(name!=='manifest.json')assert.equal(manifest.files[name],hash(checkout),`${name} has a stale manifest hash`);}});

test('every continuity rule reaches the setting and its importable document', async () => {
  for (const slug of SLUGS) {
    const source = await loadSource(slug);
    const files = compile(source);
    const setting = JSON.parse(files['setting.json']);
    const imported = JSON.parse(files['documents.json']).documents.find(d => d.kind === 'setting');
    assert.deepEqual(setting.body_json.continuity_notes, source.continuity_notes, slug);
    assert.deepEqual(imported.body_json.continuity_notes, source.continuity_notes, slug);
    assert.equal(imported.body_md, setting.body_md, slug);
    assert.equal(files['setting.md'], setting.body_md, slug);
    for (const rule of source.continuity_notes) assert.ok(imported.body_md.includes(rule), `${slug}: ${rule}`);
  }
});

test('a continuity-only edit invalidates the setting and import bundle until rebuilt', async (t) => {
  const root = await fs.mkdtemp(path.join(os.tmpdir(), 'codex-plan-drift-'));
  assert.equal(path.dirname(root), path.resolve(os.tmpdir()));
  t.after(() => fs.rm(root, { recursive: true, force: true }));
  const source = clone();
  const slug = source.series.slug;
  await fs.mkdir(path.join(root, slug));
  const write = async () => {
    for (const [name, body] of Object.entries(compile(source))) await fs.writeFile(path.join(root, slug, name), body);
  };
  await write();
  assert.deepEqual(await validateFiles(slug, source, root), []);
  source.continuity_notes.push('回歸測試專用：第三十五集仍須保留前集證物封條。');
  const errors = await validateFiles(slug, source, root);
  for (const name of ['setting.md', 'setting.json', 'documents.json', 'manifest.json']) {
    assert.ok(errors.some(e => e.startsWith(`${name}:`)), `${name} failed to detect changed continuity`);
  }
  await write();
  assert.deepEqual(await validateFiles(slug, source, root), []);
});

test('blank continuity constraints cannot be delivered as production guidance', () => {
  const source = clone();
  source.continuity_notes = ['one', 'two', '   '];
  assert.ok(validateSource(source).some(e => e.includes('continuity guidance')));
});

// Synthetic receipts are test fixtures, never editorial evidence or production approval.
const receipt=()=>({slug:original.series.slug,source_sha256:hash(original),reviewer:'test-reviewer',author:'test-author',evidence_type:'independent-editorial-review',scope:'Test fixture only',limitations:'Not a real editorial review',open_findings:[],documents:Object.fromEntries(['setting','outline','chapter-01','chapter-02','chapter-03','chapter-04'].map(name=>[name,{verdicts:Object.fromEntries(REQUIRED_VERDICTS[name.startsWith('chapter')?'chapter':name].map(k=>[k,'有'])),problems:[],similar_works:[],notes:'Test fixture only'}]))});
test('accepts a complete review shape bound to the source',()=>assert.deepEqual(validateReview(receipt(),original),[]));
test('invalidates the review when the story changes',()=>{const s=clone();s.setting.ending+=' revised';assert.ok(validateReview(receipt(),s).includes('review: stale source hash'));});
test('requires a different reviewer and no unresolved findings',()=>{const r=receipt();r.reviewer=r.author;r.open_findings=['unresolved chronology'];assert.deepEqual(validateReview(r,original),['review: independent reviewer required','review: unresolved findings']);});
test('rejects missing document verdicts without crashing',()=>{const r=receipt();delete r.documents['chapter-03'];assert.ok(validateReview(r,original).some(e=>e.includes('chapter-03 did not pass')));assert.deepEqual(validateReview(null,original),['review: invalid receipt']);});
test('rejects a failing editorial verdict even when its hash matches',()=>{const r=receipt();r.documents.outline.verdicts.midpoint_reveal='無';assert.ok(validateReview(r,original).includes('review: outline did not pass'));});
