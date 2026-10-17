import test from 'node:test';import assert from 'node:assert/strict';
import {mkdtempSync,rmSync,readFileSync,existsSync,readdirSync,cpSync,copyFileSync,writeFileSync} from 'node:fs';import {tmpdir} from 'node:os';
import {join,resolve} from 'node:path';import {spawnSync} from 'node:child_process';import {fileURLToPath} from 'node:url';
import {materializeLesson,materializeAll,sourceRoot} from './labs.mjs';
const repo=fileURLToPath(new URL('../..',import.meta.url));
function temporary(fn){const root=mkdtempSync(join(tmpdir(),'codex-lessons-'));try{return fn(root);}finally{rmSync(root,{recursive:true,force:true});}}
function run(folder,args=['--test']){const env={...process.env};delete env.NODE_TEST_CONTEXT;const result=spawnSync(process.execPath,args,{cwd:folder,env,encoding:'utf8',timeout:20000,maxBuffer:4*1024*1024});if(result.error)throw result.error;return result;}
test('import has no materialization side effect and IDs/destinations are validated',()=>temporary(root=>{
  assert.equal(readdirSync(root).length,0);assert.throws(()=>materializeLesson(0,join(root,'bad')));assert.throws(()=>materializeLesson(19,join(root,'bad')));
  assert.equal(existsSync(join(root,'bad')),false);materializeLesson('01',join(root,'one'));assert.throws(()=>materializeLesson(1,join(root,'one')));
}));
test('01 matches original five files byte-for-byte and preserves exact three-test baseline',()=>temporary(root=>{
  const lesson=join(root,'01');materializeLesson(1,lesson);
  for(const [snapshot,source] of [['start','start'],['reference','expected'],['challenge','broken']]){
    for(const name of ['index.html','style.css','app.js','core.mjs','core.test.mjs'])assert.deepEqual(readFileSync(join(lesson,snapshot,name)),readFileSync(join(repo,'docs/codex-learning/practice',source,name)));
    assert.equal(existsSync(join(lesson,snapshot,'app.mjs')),false);
    const result=run(join(lesson,snapshot),['--test','core.test.mjs']);assert.equal(result.status,snapshot==='reference'?0:1,result.stdout+result.stderr);
    assert.match(result.stdout,/tests 3/);assert.match(result.stdout,snapshot==='reference'?/pass 3/:/pass 2/);
  }
}));
test('all 18 self-contained reference snapshots pass; intentional defects are actually detectable',()=>temporary(root=>{
  const all=materializeAll(join(root,'lessons'));assert.equal(all.length,18);
  for(const meta of all){
    for(const variant of ['start','reference','challenge']){
      const folder=join(meta.path,variant);assert.ok(existsSync(join(folder,'index.html')));assert.ok(existsSync(join(folder,'core.mjs')));
      const result=run(folder);const intended=meta.intentionalFailures.includes(variant);
      assert.equal(result.status,intended?1:0,`Lesson ${meta.id} ${variant}:\n${result.stdout}\n${result.stderr}`);
      if(intended)assert.match(result.stdout,/fail [1-9]/);
    }
    for(const name of ['README.md','prompts.md','acceptance.md','answers.md','lesson.json'])assert.ok(existsSync(join(meta.path,name)));
  }
}));
test('workflow artifacts are concrete, separate and label authored examples',()=>temporary(root=>{
  const expected={2:['docs/task-brief.md','docs/plan.md'],4:['AGENTS.md'],8:['git-lab.mjs','docs/git-lab.md','docs/pull-request.md'],
    12:['docs/handoff.md'],13:['.agents/skills/verify-delivery/SKILL.md'],14:['mcp-server.mjs','tests/mcp.test.mjs'],
    15:['docs/worktree-lab.md'],16:['docs/subagent-lab.md'],17:['exec-run.mjs','verify-result.mjs','docs/app-schedule.md'],
    18:['archive.mjs','restore.mjs','.github/workflows/practice.yml']};
  for(const [id,names] of Object.entries(expected)){
    const meta=materializeLesson(Number(id),join(root,id));for(const name of names)assert.ok(existsSync(join(meta.path,'reference',name)),`${id}/${name}`);
    assert.match(readFileSync(join(meta.path,'reference/AUTHORSHIP.md'),'utf8'),/未聲稱/);
  }
  const git=run(join(root,'8/reference'),['git-lab.mjs']);assert.equal(git.status,0,git.stdout+git.stderr);
  const evidence=JSON.parse(git.stdout);assert.equal(evidence.commits,3);assert.equal(evidence.notePreserved,true);assert.equal(evidence.remote,false);
  const dry=run(join(root,'17/reference'),['exec-run.mjs','--dry-run']);assert.equal(dry.status,0,dry.stderr);assert.equal(JSON.parse(dry.stdout).modelInvoked,false);
}));
test('Taipei fixture report CLI and archive/restore commands operate outside repository',()=>temporary(root=>{
  const meta=materializeLesson(18,join(root,'18')),folder=join(meta.path,'reference');
  const report=run(folder,['report.mjs','fixtures/tasks.json','--from','2026-10-05','--to','2026-10-11']);assert.equal(report.status,0,report.stderr);assert.deepEqual(JSON.parse(report.stdout),meta.expectedReport);
  const args=['archive.mjs','fixtures/tasks.json','--cutoff','2026-10-04T15:59:59.999Z','--out','archive-run'];
  const preview=run(folder,args);assert.equal(preview.status,0,preview.stderr);assert.deepEqual(JSON.parse(preview.stdout).archivedIds,['old']);assert.equal(existsSync(join(folder,'archive-run')),false);
  const apply=run(folder,[...args,'--apply']);assert.equal(apply.status,0,apply.stderr);
  const restore=run(folder,['restore.mjs','archive-run/backup.json','restored.json']);assert.equal(restore.status,0,restore.stderr);
  assert.deepEqual(readFileSync(join(folder,'restored.json')),readFileSync(join(folder,'fixtures/tasks.json')));
}));
test('15 real worktrees isolate UI/report changes, preserve a note and resolve a same-line conflict',()=>temporary(root=>{
  const meta=materializeLesson(15,join(root,'lesson')),main=join(root,'main'),ui=join(root,'ui'),report=join(root,'report');
  cpSync(join(meta.path,'start'),main,{recursive:true});
  const config=join(root,'empty.gitconfig');writeFileSync(config,'');
  const env={...process.env,GIT_CONFIG_GLOBAL:config,GIT_CONFIG_NOSYSTEM:'1',GIT_TERMINAL_PROMPT:'0',GIT_EDITOR:'true'};
  for(const key of Object.keys(env))if(key.startsWith('GIT_')&&!['GIT_CONFIG_GLOBAL','GIT_CONFIG_NOSYSTEM','GIT_TERMINAL_PROMPT','GIT_EDITOR'].includes(key))delete env[key];
  function command(folder,...args){return spawnSync('git',args,{cwd:folder,env,encoding:'utf8',timeout:20000});}
  function git(folder,...args){const result=command(folder,...args);assert.equal(result.status,0,result.stdout+result.stderr);return result.stdout.trim();}
  git(main,'init','-b','main');git(main,'config','user.name','Practice');git(main,'config','user.email','practice@example.test');git(main,'config','core.autocrlf','false');
  git(main,'add','.');git(main,'commit','-m','baseline');
  writeFileSync(join(main,'style.css'),readFileSync(join(main,'style.css'),'utf8')+'\n/* KEEP-MY-NOTE */\n');
  git(main,'worktree','add',ui,'-b','codex/filter-hint');git(main,'worktree','add',report,'-b','codex/report-compact');
  for(const folder of [ui,report])assert.doesNotMatch(readFileSync(join(folder,'style.css'),'utf8'),/KEEP-MY-NOTE/);
  assert.equal(run(report,['report.mjs','fixtures/tasks.json','--from','2026-10-05','--to','2026-10-11','--compact']).status,1);
  copyFileSync(join(meta.path,'reference/index.html'),join(ui,'index.html'));
  assert.equal(run(ui).status,0);git(ui,'add','index.html');git(ui,'commit','-m','add filter explanation');
  assert.equal(git(ui,'show','--format=','--name-only','HEAD'),'index.html');
  for(const name of ['report.mjs','tests/report-compact.test.mjs'])copyFileSync(join(meta.path,'reference',name),join(report,name));
  const reportTests=run(report);assert.equal(reportTests.status,0,reportTests.stdout+reportTests.stderr);
  git(report,'add','report.mjs','tests/report-compact.test.mjs');git(report,'commit','-m','add compact report');
  assert.equal(git(report,'show','--format=','--name-only','HEAD'),'report.mjs\ntests/report-compact.test.mjs');
  git(main,'cherry-pick','codex/filter-hint');git(main,'cherry-pick','codex/report-compact');
  assert.equal(git(main,'diff','--name-only'),'style.css');
  const compact=run(main,['report.mjs','fixtures/tasks.json','--from','2026-10-05','--to','2026-10-11','--compact']);
  assert.equal(compact.status,0,compact.stderr);assert.deepEqual(JSON.parse(compact.stdout),meta.expectedReport);assert.equal(compact.stdout.trim().split('\n').length,1);
  const backout=join(root,'backout');git(main,'worktree','add',backout,'-b','codex/backout');
  git(backout,'revert','--no-edit','codex/report-compact');git(backout,'revert','--no-edit','codex/filter-hint');
  assert.doesNotMatch(readFileSync(join(backout,'index.html'),'utf8'),/filter-hint/);
  assert.equal(run(backout,['report.mjs','fixtures/tasks.json','--from','2026-10-05','--to','2026-10-11','--compact']).status,1);
  const a=join(root,'conflict-a'),b=join(root,'conflict-b');
  git(main,'worktree','add',a,'-b','codex/conflict-a');git(main,'worktree','add',b,'-b','codex/conflict-b');
  const hint='搜尋會與目前狀態篩選一起套用。';
  for(const [folder,extra] of [[a,'首尾空白會被忽略'],[b,'搜尋不會刪除任務']]){
    writeFileSync(join(folder,'index.html'),readFileSync(join(folder,'index.html'),'utf8').replace(hint,'搜尋會與目前狀態篩選一起套用；'+extra+'。'));
    git(folder,'add','index.html');git(folder,'commit','-m','change same hint');
  }
  git(main,'cherry-pick','codex/conflict-a');const conflict=command(main,'cherry-pick','codex/conflict-b');assert.equal(conflict.status,1);
  assert.match(git(main,'status','--short'),/UU index.html/);
  const content=readFileSync(join(main,'index.html'),'utf8');assert.match(content,/<<<<<<< HEAD/);
  const combined='<p id="filter-hint">搜尋會與目前狀態篩選一起套用；首尾空白會被忽略，搜尋不會刪除任務。</p>';
  writeFileSync(join(main,'index.html'),content.replace(/<<<<<<< HEAD[\s\S]*?>>>>>>>[^\n]*(?:\n|$)/,combined+'\n'));
  git(main,'add','index.html');git(main,'cherry-pick','--continue');
  assert.doesNotMatch(readFileSync(join(main,'index.html'),'utf8'),/<<<<<<<|>>>>>>>/);
  assert.equal(git(main,'diff','--name-only'),'style.css');assert.match(readFileSync(join(main,'style.css'),'utf8'),/KEEP-MY-NOTE/);
  assert.equal(run(main).status,0);
  const inventory=git(main,'worktree','list','--porcelain');
  for(const folder of [ui,report,backout,a,b]){assert.ok(inventory.includes(folder.replaceAll('\\','/')));assert.equal(git(folder,'status','--short'),'');git(main,'worktree','remove',folder);}
  assert.equal(git(main,'remote'),'');
}));
test('06 old checks miss the defect; adding the supplied reference regression goes red before the fix',()=>temporary(root=>{
  // This author unit test checks the lesson progression, not learner/model execution evidence.
  const meta=materializeLesson(6,join(root,'06')),start=join(meta.path,'start'),reference=join(meta.path,'reference');
  const old=run(start);assert.equal(old.status,0,old.stdout+old.stderr);assert.match(old.stdout,/todo 1/);
  copyFileSync(join(reference,'tests/meaningful.test.mjs'),join(start,'tests/meaningful.test.mjs'));
  const red=run(start);assert.equal(red.status,1);assert.match(red.stdout,/fail [1-9]/);
  copyFileSync(join(reference,'core.mjs'),join(start,'core.mjs'));
  const green=run(start);assert.equal(green.status,0,green.stdout+green.stderr);assert.match(green.stdout,/todo 0/);
  assert.equal(existsSync(join(reference,'tests/review.test.mjs')),false);
}));
test('11 duplicated and refactored CLI retain identical success and invalid-calendar behavior',()=>temporary(root=>{
  const meta=materializeLesson(11,join(root,'11'));let expected;
  for(const variant of ['start','reference','challenge']){
    const folder=join(meta.path,variant),good=run(folder,['report.mjs','fixtures/tasks.json','--from','2026-10-05','--to','2026-10-11']);
    assert.equal(good.status,0,good.stderr);if(expected===undefined)expected=good.stdout;else assert.equal(good.stdout,expected);
    for(const [from,to,error] of [['2026-02-30','2026-03-08','calendar-date'],['2026-10-11','2026-10-05','date-order'],['2026-2-3','2026-03-08','calendar-date']]){
      const bad=run(folder,['report.mjs','fixtures/tasks.json','--from',from,'--to',to]);assert.equal(bad.status,1);assert.equal(bad.stderr.trim(),error);
    }
  }
}));
