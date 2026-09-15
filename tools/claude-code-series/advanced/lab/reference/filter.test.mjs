import test from 'node:test';
import assert from 'node:assert/strict';
import {filterTasks} from '../filter.js';
test('filters preserve stable ids, original data and all three modes',()=>{
 const items=[{id:'a',title:'同名',completed:false},{id:'b',title:'同名',completed:true}];
 const before=structuredClone(items);
 assert.deepEqual(filterTasks(items,'active').map(x=>x.id),['a']);
 assert.deepEqual(filterTasks(items,'completed').map(x=>x.id),['b']);
 assert.deepEqual(filterTasks(items,'all'),items);
 assert.notEqual(filterTasks(items,'all'),items);
 assert.deepEqual(items,before);
 assert.deepEqual(filterTasks([],'active'),[]);
 assert.throws(()=>filterTasks(items,'invalid'),/Unknown/);
});
