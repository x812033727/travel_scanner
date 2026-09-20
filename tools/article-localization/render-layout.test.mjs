import assert from 'node:assert/strict';
import test from 'node:test';

import { containerFor, contains, overlaps } from './render-layout.mjs';

const box = (left, top, right, bottom) => ({
  left,
  top,
  right,
  bottom,
  width: right - left,
  height: bottom - top,
});

test('containerFor ignores a decorative strip that only crosses the source text centre', () => {
  const header = box(60, 126, 415, 200);
  const decorativeStrip = box(60, 176, 415, 200);
  const sourceText = { box: box(130, 167, 289, 191) };
  const localizedText = box(130, 170, 228, 190);

  const container = containerFor(
    { rectangles: [decorativeStrip, header] },
    sourceText,
  );

  assert.equal(container, header);
  assert.equal(contains(container, localizedText), true);
  assert.equal(contains(decorativeStrip, sourceText.box), false);
});

test('containerFor chooses the smallest shape that fully contains the source text', () => {
  const canvas = box(0, 0, 1600, 900);
  const card = box(60, 126, 415, 444);
  const header = box(60, 126, 415, 200);
  const sourceText = { box: box(130, 140, 310, 168) };

  assert.equal(containerFor({ rectangles: [canvas, card, header] }, sourceText), header);
});

test('overlaps requires more than a two-pixel intersection', () => {
  assert.equal(overlaps(box(0, 0, 10, 10), box(8, 8, 20, 20)), false);
  assert.equal(overlaps(box(0, 0, 10, 10), box(7, 7, 20, 20)), true);
});
