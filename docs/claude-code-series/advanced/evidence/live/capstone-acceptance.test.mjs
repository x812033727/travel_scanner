import test from 'node:test';
import assert from 'node:assert/strict';
import {pathToFileURL} from 'node:url';
import path from 'node:path';

const directory=process.env.CAPSTONE_DIRECTORY;
if(!directory)throw new Error('CAPSTONE_DIRECTORY is required');
const {filterTodos}=await import(pathToFileURL(path.join(directory,'filter.js')));
const {toggleTodo}=await import(pathToFileURL(path.join(directory,'model.js')));
const items=Object.freeze([
  Object.freeze({id:'a',title:'同名',completed:false}),
  Object.freeze({id:'b',title:'同名',completed:true}),
  Object.freeze({id:'c',title:'另一筆',completed:false}),
]);
test('three filters preserve full source and handle unknown mode',()=>{
  assert.deepEqual(filterTodos(items,'all'),items);
  assert.deepEqual(filterTodos(items,'active').map(item=>item.id),['a','c']);
  assert.deepEqual(filterTodos(items,'completed').map(item=>item.id),['b']);
  assert.deepEqual(filterTodos(items,'unknown'),items);
  assert.equal(items.length,3);
  assert.deepEqual(items.map(item=>item.completed),[false,true,false]);
});
test('empty filters are valid for every mode',()=>{
  for(const mode of ['all','active','completed','unknown'])assert.deepEqual(filterTodos(Object.freeze([]),mode),[]);
});
test('duplicate titles remain independent when toggling inside a filtered view',()=>{
  const visible=filterTodos(items,'active');
  const updated=toggleTodo(items,visible[0].id);
  assert.deepEqual(updated.map(item=>[item.id,item.completed]),[['a',true],['b',true],['c',false]]);
  assert.deepEqual(filterTodos(updated,'active').map(item=>item.id),['c']);
  assert.deepEqual(items.map(item=>item.completed),[false,true,false]);
  assert.deepEqual(toggleTodo(items,'missing'),items);
});
