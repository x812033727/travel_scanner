import test from 'node:test';import assert from 'node:assert/strict';
import {countTodos as before} from '../legacy-stats.js';import {countTodos as after} from '../reference/stats.js';
test('legacy and refactored statistics preserve the characterized outputs',()=>{
 for(const items of [[],[{completed:false}],[{completed:true}],[{completed:false},{completed:true},{completed:false}]]){
  const snapshot=structuredClone(items);assert.deepEqual(after(items),before(items));assert.deepEqual(items,snapshot);
 }
 assert.deepEqual(after([]),{total:0,completed:0,active:0});
});
