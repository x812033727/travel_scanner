// Independent assertions run against the actual two-teammate deliverable.
import assert from 'node:assert/strict';
import {test} from 'node:test';
import {pathToFileURL} from 'node:url';
import {resolve} from 'node:path';
const project=process.env.TEAM_FEATURE_PROJECT;
assert.ok(project, 'TEAM_FEATURE_PROJECT is required');
const {selectTodos}=await import(pathToFileURL(resolve(project,'filter.js')).href);
const {toggleTodo,removeTodo}=await import(pathToFileURL(resolve(project,'model.js')).href);
const items=Object.freeze([
  Object.freeze({id:'a',title:'重複名稱',completed:false}),
  Object.freeze({id:'b',title:'重複名稱',completed:true}),
  Object.freeze({id:'c',title:'<img src=x onerror=alert(1)>',completed:false}),
]);
test('three filters retain the correct IDs and leave frozen source data intact',()=>{
  for(const [mode,ids] of [['all',['a','b','c']],['active',['a','c']],['completed',['b']]]){
    const result=selectTodos(items,mode);
    assert.deepEqual(result.map(x=>x.id),ids);
    assert.notEqual(result,items);
  }
  assert.equal(items.length,3);
});
test('the resolved unknown-mode contract returns all items in a new array',()=>{
  for(const mode of ['stale-mode',undefined,null,'']){
    const result=selectTodos(items,mode);
    assert.deepEqual(result,items);
    assert.notEqual(result,items);
  }
});
test('actions on a filtered duplicate title remain ID based and retain hidden items',()=>{
  const toggled=toggleTodo(items,selectTodos(items,'active')[0].id);
  assert.deepEqual(selectTodos(toggled,'completed').map(x=>x.id),['a','b']);
  const removed=removeTodo(toggled,'a');
  assert.deepEqual(removed.map(x=>x.id),['b','c']);
  assert.deepEqual(selectTodos(removed,'active').map(x=>x.id),['c']);
});
