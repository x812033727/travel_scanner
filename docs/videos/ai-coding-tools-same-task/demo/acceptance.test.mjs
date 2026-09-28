import assert from 'node:assert/strict';
import test from 'node:test';
import { splitFareCents } from './fare.mjs';

test('100 cents across three people', () => {
  assert.deepEqual(splitFareCents(100, 3), [34, 33, 33]);
});

test('remainder order and zeros', () => {
  assert.deepEqual(splitFareCents(2, 3), [1, 1, 0]);
  assert.deepEqual(splitFareCents(0, 4), [0, 0, 0, 0]);
});

test('all shares sum and differ by at most one cent', () => {
  for (let total = 0; total <= 500; total += 1) {
    for (let people = 1; people <= 20; people += 1) {
      const shares = splitFareCents(total, people);
      assert.equal(shares.length, people);
      assert.equal(shares.reduce((sum, amount) => sum + amount, 0), total);
      assert.ok(Math.max(...shares) - Math.min(...shares) <= 1);
    }
  }
});

test('invalid totals and people', () => {
  for (const total of [-1, 1.5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => splitFareCents(total, 3), RangeError);
  }
  for (const people of [0, 101, 2.5, Number.MAX_SAFE_INTEGER + 1]) {
    assert.throws(() => splitFareCents(100, people), RangeError);
  }
});
