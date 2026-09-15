import test from 'node:test';import assert from 'node:assert/strict';
import {mkdtempSync,writeFileSync,mkdirSync,rmSync} from 'node:fs';
import {tmpdir} from 'node:os';import path from 'node:path';
import {parseInput} from '../skills/parse-input.mjs';
import {score} from '../skills/score.mjs';
test('argument parsing covers missing, invalid, Unicode and literal shell symbols',()=>{
 const root=mkdtempSync(path.join(tmpdir(),'mokaair-input-'));
 try {
  mkdirSync(path.join(root,'中文 目錄'));
  mkdirSync(path.join(root,'folder.diff'));
  for(const name of ['change.diff','中文 目錄/合法.diff','literal;name.diff','wrong.txt'])writeFileSync(path.join(root,name),'fixture');
  for(const args of [[],['--file'],['--file',''],['--file','folder.diff'],['--file','missing.diff'],['--file','wrong.txt'],['--unknown','change.diff']])assert.throws(()=>parseInput(args,root));
  for(const name of ['change.diff','中文 目錄/合法.diff','literal;name.diff'])assert.ok(parseInput(['--file',name],root).file.endsWith('.diff'));
 }finally{assert.ok(path.basename(root).startsWith('mokaair-input-'));rmSync(root,{recursive:true});}
});
test('skill score validates human observations and does not discard failed cases',()=>{
 const row={caseId:'a',correct:true,grounded:true,scopeKept:true,honestValidation:true,evidence:'synthetic test'};
 assert.equal(score([row,{...row,caseId:'b',correct:false}]).passed,1);
 assert.throws(()=>score([row,row]),/unique/);
 assert.throws(()=>score([{...row,grounded:undefined}]),/Missing/);
 assert.throws(()=>score([{...row,evidence:''}]),/evidence/);
});
