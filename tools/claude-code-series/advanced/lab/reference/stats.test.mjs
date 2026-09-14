import test from 'node:test';import assert from 'node:assert/strict';import {countTodos} from '../stats.js';
test('statistics preserve empty, mixed and same-title data without mutation',()=>{
 assert.deepEqual(countTodos([]),{total:0,completed:0,active:0});
 const items=[{id:'a',title:'同名',completed:false},{id:'b',title:'同名',completed:true}];
 const before=structuredClone(items);
 assert.deepEqual(countTodos(items),{total:2,completed:1,active:1});assert.deepEqual(items,before);
});
