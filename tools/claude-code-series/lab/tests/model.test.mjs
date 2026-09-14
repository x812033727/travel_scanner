import { test } from 'node:test';
import assert from 'node:assert/strict';
import { addTodo, toggleTodo, removeTodo } from '../model.js';

test('新增待辦會去除前後空白並保留既有資料', () => {
  const original = [{ id: 'a', title: '買早餐', completed: true }];
  const added = addTodo(original, '  讀書  ', 'b');
  assert.deepEqual(added, [...original, { id: 'b', title: '讀書', completed: false }]);
  assert.equal(original.length, 1);
});
test('拒絕空白與過長內容', () => {
  const original = [];
  assert.equal(addTodo(original, '   ', 'a'), original);
  assert.equal(addTodo(original, '字'.repeat(101), 'a'), original);
});
test('依照識別碼切換指定項目，不改動其他項目', () => {
  const original = [{ id: 'a', title: '相同標題', completed: false }, { id: 'b', title: '相同標題', completed: true }];
  const updated = toggleTodo(original, 'a');
  assert.equal(updated[0].completed, true);
  assert.equal(updated[1].completed, true);
  assert.equal(original[0].completed, false);
});
test('刪除依識別碼進行，找不到項目時仍保留資料', () => {
  const original = [{ id: 'a', title: '測試', completed: false }];
  assert.deepEqual(removeTodo(original, 'missing'), original);
  assert.deepEqual(removeTodo(original, 'a'), []);
});
