import assert from 'node:assert/strict';
import test from 'node:test';
import { add } from './calc.mjs';

test('add returns the sum', () => {
  assert.equal(add(2, 3), 5);
});
