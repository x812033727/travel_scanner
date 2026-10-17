import test from 'node:test';import assert from 'node:assert/strict';
import {loadStorage,saveStorage} from '../storage.mjs';import {decodeTasks,encodeTasks} from '../core.mjs';
function store(initial){const values=new Map(Object.entries(initial));return{values,getItem:key=>values.get(key)??null,setItem:(key,value)=>values.set(key,value)};}
test('damaged data is retained verbatim and no write occurs on load',()=>{
  const storage=store({practice:'bad-json',unrelated:'KEEP'});
  const state=loadStorage(storage,'practice',decodeTasks);assert.equal(state.available,false);
  assert.deepEqual([...storage.values],[['practice','bad-json'],['unrelated','KEEP']]);
});
test('legacy copy has unknown date and original value remains untouched',()=>{
  const raw='{"version":1,"tasks":[{"id":"old","title":"Read","completed":true}]}';
  const storage=store({v1:raw});const result=loadStorage(storage,'v2',decodeTasks,'v1');
  assert.equal(result.migrated,true);assert.equal(result.tasks[0].completedAt,null);assert.equal(storage.values.get('v1'),raw);assert.equal(storage.values.has('v2'),false);
});
test('storage denied write fails explicitly without clearing unrelated data',()=>{
  const storage=store({unrelated:'KEEP'});storage.setItem=()=>{throw new Error('denied')};
  assert.equal(saveStorage(storage,'v2','{}'),false);assert.equal(storage.values.get('unrelated'),'KEEP');
});
test('v2 reset writes an empty document so preserved v1 cannot remigrate on reload',()=>{
  const old='{"version":1,"tasks":[{"id":"old","title":"Read","completed":true}]}';
  const storage=store({v1:old,other:'KEEP'});
  assert.equal(loadStorage(storage,'v2',decodeTasks,'v1').tasks.length,1);
  assert.equal(saveStorage(storage,'v2',encodeTasks([])),true);
  const reloaded=loadStorage(storage,'v2',decodeTasks,'v1');assert.deepEqual(reloaded.tasks,[]);assert.equal(reloaded.migrated,false);
  assert.equal(storage.values.get('v1'),old);assert.equal(storage.values.get('other'),'KEEP');
});
