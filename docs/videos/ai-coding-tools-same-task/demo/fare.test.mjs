import assert from 'node:assert/strict';
import test from 'node:test';
import { splitFareCents } from './fare.mjs';

test('evenly divisible total', () => {
  assert.deepEqual(splitFareCents(120, 3), [40, 40, 40]);
});

test('invalid passenger count', () => {
  assert.throws(() => splitFareCents(100, 0), RangeError);
});
