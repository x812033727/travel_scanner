import assert from 'node:assert/strict';
import test from 'node:test';
import { slugify } from '../src/text.mjs';

test('slugify joins words with dashes', () => {
  assert.equal(slugify('  Hello, World  '), 'hello-world');
});
