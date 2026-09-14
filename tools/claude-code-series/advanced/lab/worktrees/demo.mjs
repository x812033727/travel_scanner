import {mkdtempSync,mkdirSync,copyFileSync,writeFileSync,readFileSync,existsSync} from 'node:fs';
import {tmpdir} from 'node:os';import path from 'node:path';import {fileURLToPath} from 'node:url';import {spawnSync} from 'node:child_process';
const source=fileURLToPath(new URL('../',import.meta.url));
const root=mkdtempSync(path.join(tmpdir(),'mokaair-worktree-'));
const main=path.join(root,'main');mkdirSync(main);
const history=[];
function run(cmd,args,cwd=main,accepted=[0]){
 const r=spawnSync(cmd,args,{cwd,encoding:'utf8',windowsHide:true,timeout:30000});
 history.push({command:[cmd,...args],directory:path.relative(root,cwd),exit:r.status,output:(r.stdout+r.stderr).slice(-2500)});
 if(!accepted.includes(r.status))throw new Error(r.stdout+r.stderr);
 return r;
}
const git=(args,cwd=main,accepted=[0])=>run('git',['-c','user.name=Mokaair Lab','-c','user.email=lab@example.com','-c','commit.gpgsign=false',...args],cwd,accepted);
try{
 for(const f of ['model.js','tests/model.test.mjs']){mkdirSync(path.dirname(path.join(main,f)),{recursive:true});copyFileSync(path.join(source,f),path.join(main,f));}
 writeFileSync(path.join(main,'package.json'),'{"private":true,"type":"module"}\n');
 writeFileSync(path.join(main,'view-mode.txt'),'default=all\nlabel=全部\n');
 git(['init','--initial-branch=main']);git(['add','.']);git(['commit','-m','Create exercise baseline']);
 const base=git(['rev-parse','HEAD']).stdout.trim();
 const filter=path.join(root,'filter');const labels=path.join(root,'labels');
 git(['worktree','add','-b','lab/filter',filter,base]);git(['worktree','add','-b','lab/labels',labels,base]);
 writeFileSync(path.join(filter,'filter.js'),"export const filterTasks=(items,mode)=>mode==='active'?items.filter(x=>!x.completed):items;\n");
 writeFileSync(path.join(filter,'tests/filter.test.mjs'),"import test from 'node:test';import assert from 'node:assert/strict';import {filterTasks} from '../filter.js';test('integrated filter keeps only active ids without changing source',()=>{const items=[{id:'a',completed:false},{id:'b',completed:true}];const before=structuredClone(items);assert.deepEqual(filterTasks(items,'active').map(x=>x.id),['a']);assert.deepEqual(items,before);});\n");
 writeFileSync(path.join(filter,'view-mode.txt'),'default=active\nlabel=全部\n');
 git(['add','.'],filter);git(['commit','-m','Add active filter'],filter);
 writeFileSync(path.join(labels,'view-mode.txt'),'default=all\nlabel=所有待辦\n');
 git(['add','view-mode.txt'],labels);git(['commit','-m','Clarify display label'],labels);
 git(['merge','--no-edit','lab/filter']);
 const merge=git(['merge','--no-edit','lab/labels'],main,[0,1]);
 if(merge.status!==1 || !readFileSync(path.join(main,'view-mode.txt'),'utf8').includes('<<<<<<<'))throw new Error('Expected controlled text conflict');
 writeFileSync(path.join(main,'view-mode.txt'),'default=active\nlabel=所有待辦\n');
 git(['add','view-mode.txt']);git(['commit','-m','Preserve active filter and new label']);
 const env={...process.env};delete env.NODE_TEST_CONTEXT;
 const tests=spawnSync(process.execPath,['--test','tests/model.test.mjs','tests/filter.test.mjs'],{cwd:main,env,encoding:'utf8',windowsHide:true,timeout:15000});
 if(tests.status!==0)throw new Error(tests.stdout+tests.stderr);
 if(readFileSync(path.join(main,'view-mode.txt'),'utf8')!=='default=active\nlabel=所有待辦\n')throw new Error('Integrated requirements lost');
 for(const worktree of [filter,labels]){
  if(!path.resolve(worktree).startsWith(path.resolve(root)+path.sep))throw new Error('Unsafe cleanup target');
  if(git(['status','--porcelain'],worktree).stdout.trim())throw new Error('Do not remove dirty worktree');
  git(['worktree','remove',worktree]);
 }
 const receipt={passed:true,root,base,head:git(['rev-parse','HEAD']).stdout.trim(),controlledConflict:true,coreTests:tests.stdout,remainingWorktrees:git(['worktree','list','--porcelain']).stdout,history};
 writeFileSync(path.join(root,'receipt.json'),JSON.stringify(receipt,null,2)+'\n');
 console.log(JSON.stringify({passed:true,receipt:path.join(root,'receipt.json')}));
}catch(error){writeFileSync(path.join(root,'failure.json'),JSON.stringify({error:error.message,history},null,2));console.error(error.message);process.exitCode=1;}
