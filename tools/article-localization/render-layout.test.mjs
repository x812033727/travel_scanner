import assert from 'node:assert/strict';
import test from 'node:test';

import { containerFor, contains, EDGE_PADDING, edgeClearance, layoutIssues, MIN_FONT_PX, overlaps } from './render-layout.mjs';

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

// Geometry of a small two-card diagram, as Chromium measures it: two 300x120 cards side by side,
// an arrow between them, and a legend row of swatch + label pairs underneath.
const card = box(40, 40, 340, 160);
const nextCard = box(400, 40, 700, 160);
const arrow = box(345, 99, 395, 101); // a horizontal line: its box has almost no height
const swatchTaiwan = box(40, 200, 56, 216);
const swatchJapan = box(170, 200, 186, 216);
const source = (overrides = {}) => ({
  text: [
    { value: '入境卡', box: box(60, 80, 160, 104), size: 20 },
    { value: '春節', box: box(64, 200, 112, 216), size: 16 },
  ],
  rectangles: [card, nextCard, swatchTaiwan, swatchJapan],
  strokes: [arrow],
  ...overrides,
});
const SIZE = { width: 760, height: 260 };
const reasons = issues => issues.map(issue => issue.reason);

test('a label that is localized cleanly raises nothing, in CJK or in English', () => {
  const localized = source({ text: [{ value: 'Arrival card', box: box(60, 80, 220, 104), size: 20 }, { value: 'Lunar NY', box: box(64, 200, 140, 216), size: 16 }] });
  assert.deepEqual(layoutIssues({ original: source(), localized, size: SIZE }), []);
  assert.deepEqual(layoutIssues({ original: source(), localized: source(), size: SIZE }), []);
});

test('a label shrunk below 15px is reported, and one already drawn smaller in the source is not', () => {
  const shrunk = source({ text: [{ value: 'Arrival card', box: box(60, 80, 220, 98), size: 14 }, source().text[1]] });
  assert.deepEqual(reasons(layoutIssues({ original: source(), localized: shrunk, size: SIZE })), [`font size below ${MIN_FONT_PX}px`]);
  const smallSource = source({ text: [{ ...source().text[0], size: 12 }, source().text[1]] });
  const smallLocalized = source({ text: [{ value: 'Arrival card', box: box(60, 80, 200, 96), size: 12 }, source().text[1]] });
  assert.deepEqual(layoutIssues({ original: smallSource, localized: smallLocalized, size: SIZE }), [], 'the drawing chose 12px; not the localization');
});

test('an English legend label drawn over the next colour swatch is a new overlap (Taiwan 2027 holidays, 2026-10-07)', () => {
  const localized = source({ text: [source().text[0], { value: 'Lunar New Year', box: box(64, 200, 196, 216), size: 16 }] });
  const issues = layoutIssues({ original: source(), localized, size: SIZE });
  assert.deepEqual(reasons(issues), ['new overlap with a neighbouring shape']);
  assert.equal(issues[0].shapeIndex, 3, 'the Japan swatch');
});

test('a label that touches its card border, or reaches the arrow, is reported (Japan entry, 2026-10-07)', () => {
  const touching = source({ text: [{ value: 'Landing sticker', box: box(60, 80, 338, 104), size: 20 }, source().text[1]] });
  assert.deepEqual(reasons(layoutIssues({ original: source(), localized: touching, size: SIZE })), ['touches the edge of its containing shape']);
  // Outside the card and onto the arrow: the container check says it, and so does the arrow's.
  const onArrow = source({ text: [{ value: 'Landing sticker', box: box(60, 90, 360, 110), size: 20 }, source().text[1]] });
  assert.deepEqual(reasons(layoutIssues({ original: source(), localized: onArrow, size: SIZE })), ['outside original containing shape', 'new overlap with a line or arrow']);
  assert.equal(edgeClearance(card, box(60, 80, 338, 104)), 2);
  assert.ok(EDGE_PADDING > 2);
});

test('what already touched in the source is left alone, and a polygon that holds the label is its shape', () => {
  const tight = source({ text: [{ value: '入境卡', box: box(42, 80, 160, 104), size: 20 }, source().text[1]] });
  const tightLocalized = source({ text: [{ value: 'Arrival', box: box(42, 80, 150, 104), size: 20 }, source().text[1]] });
  assert.deepEqual(layoutIssues({ original: tight, localized: tightLocalized, size: SIZE }), [], 'the source already sat 2px from the edge');
  const badge = box(30, 30, 350, 170); // an arrow-shaped polygon around the label
  const withBadge = source({ strokes: [arrow, badge] });
  const localized = source({ text: [{ value: 'Arrival card', box: box(60, 80, 220, 104), size: 20 }, source().text[1]], strokes: [arrow, badge] });
  assert.deepEqual(layoutIssues({ original: withBadge, localized, size: SIZE }), []);
});

test('the earlier checks still hold: text count, canvas and new text overlaps', () => {
  assert.deepEqual(reasons(layoutIssues({ original: source(), localized: source({ text: [source().text[0]] }), size: SIZE })), ['visible text node count changed']);
  const offCanvas = source({ text: [source().text[0], { value: 'Lunar New Year', box: box(700, 240, 790, 256), size: 16 }] });
  assert.ok(reasons(layoutIssues({ original: source(), localized: offCanvas, size: SIZE })).includes('outside SVG canvas'));
});
