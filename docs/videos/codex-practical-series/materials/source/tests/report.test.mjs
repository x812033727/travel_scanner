import test from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, rmSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { runReport } from '../report.mjs';
import { runArchive } from '../archive.mjs';
import { runRestore } from '../restore.mjs';
const input=fileURLToPath(new URL('../fixtures/tasks.json',import.meta.url));
test('report creates new output and refuses rerun without losing source or prior result',()=>{
  const dir=mkdtempSync(join(tmpdir(),'codex-report-'));
  try {
    const output=join(dir,'report.json'), before=readFileSync(input,'utf8');
    const args=[input,'--from','2026-10-05','--to','2026-10-11','--out',output];
    const report=runReport(args); assert.equal(report.completedInWeek,2);
    const saved=readFileSync(output,'utf8'); assert.throws(()=>runReport(args));
    assert.equal(readFileSync(output,'utf8'),saved); assert.equal(readFileSync(input,'utf8'),before);
    assert.throws(()=>runReport([input,'--from','bad','--to','bad','--out',join(dir,'bad.json')]));
    assert.equal(existsSync(join(dir,'bad.json')),false);
  } finally { rmSync(dir,{recursive:true,force:true}); }
});
test('archive preview writes nothing; apply+restore keeps exact backup and all original tasks',()=>{
  const dir=mkdtempSync(join(tmpdir(),'codex-archive-'));
  try {
    const output=join(dir,'run'), before=readFileSync(input,'utf8');
    const args=[input,'--cutoff','2026-10-04T15:59:59.999Z','--out',output];
    assert.deepEqual(runArchive([...args]).archivedIds,['old']); assert.equal(existsSync(output),false);
    const done=runArchive([...args,'--apply']); assert.equal(done.retained,4); assert.equal(done.unknownCompleted,1);
    assert.equal(readFileSync(join(output,'backup.json'),'utf8'),before);
    assert.throws(()=>runArchive([...args,'--apply'])); assert.equal(readFileSync(input,'utf8'),before);
    const restored=join(dir,'restored.json'); assert.equal(runRestore([join(output,'backup.json'),restored]).restored,5);
    assert.equal(readFileSync(restored,'utf8'),before); assert.throws(()=>runRestore([join(output,'backup.json'),restored]));
    const broken=join(dir,'broken.json'); writeFileSync(broken,'{');
    assert.throws(()=>runRestore([broken,join(dir,'bad.json')])); assert.equal(existsSync(join(dir,'bad.json')),false);
  } finally { rmSync(dir,{recursive:true,force:true}); }
});
