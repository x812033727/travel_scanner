/** Pure geometry helpers used by the localized SVG renderer. */

// The reviewers' floor for a diagram's text (the travel diagram policy, and the business
// reviews too): the renderer never shrinks a label below it, and a label that is below it after
// localization while its source was not is reported. A source drawn smaller is not this check's
// to refuse; it is the drawing's.
export const MIN_FONT_PX = 15;
// The inner padding of a card: text closer than this to an edge of the shape that holds it reads
// as touching the border, as two readers saw on the English Japan entry diagram.
export const EDGE_PADDING = 4;

export const contains = (outer, inner, tolerance = 1) =>
  inner.left >= outer.left - tolerance &&
  inner.top >= outer.top - tolerance &&
  inner.right <= outer.right + tolerance &&
  inner.bottom <= outer.bottom + tolerance;

export const overlaps = (a, b) =>
  Math.min(a.right, b.right) - Math.max(a.left, b.left) > 2 &&
  Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top) > 2;

export function containerFor(original, text) {
  return original.rectangles
    .filter(rect => rect.width > 0 && rect.height > 0 && contains(rect, text.box))
    .sort((a, b) => a.width * a.height - b.width * b.height)[0];
}

/** The smallest gap between `box` and the inside of each edge of `container` (negative when it crosses one). */
export const edgeClearance = (container, box) =>
  Math.min(box.left - container.left, box.top - container.top, container.right - box.right, container.bottom - box.bottom);

// A shape is in the way of a label when the label crosses it and the shape does not hold the
// label: a legend's swatch beside its text, a neighbouring card. Shapes do not move in
// localization, so the source's shapes are the ones measured.
const inTheWay = (shape, textBox, sourceBox) =>
  shape.width > 0 && shape.height > 0 && !contains(shape, sourceBox) && overlaps(shape, textBox);

// A line's box has no thickness (getBoundingClientRect leaves the stroke out), so an axis-aligned
// arrow would never "overlap" anything: it is widened by a few pixels first. A polygon that holds
// the label (an arrow-shaped box, a badge) is its shape, not something in its way.
const STROKE_REACH = 3;
const widened = stroke => ({
  left: stroke.left - STROKE_REACH,
  top: stroke.top - STROKE_REACH,
  right: stroke.right + STROKE_REACH,
  bottom: stroke.bottom + STROKE_REACH,
});
const strokeHits = (stroke, textBox, sourceBox) => !contains(stroke, sourceBox) && overlaps(widened(stroke), textBox);

/**
 * Every layout problem of a localized SVG against its source, measured from rendered geometry:
 * `original` and `localized` hold `text` (value, box, size), `rectangles` (rect, circle and
 * ellipse boxes) and, when measured, `strokes` (line, polyline, polygon and path boxes: arrows
 * and connectors). Only problems the localization introduced are reported: a label that already
 * touched a shape or an edge in the source keeps doing so without a word.
 */
export function layoutIssues({ original, localized, size }) {
  const issues = [];
  if (original.text.length !== localized.text.length) issues.push({ reason: 'visible text node count changed' });
  const canvas = { left: 0, top: 0, right: size.width, bottom: size.height };
  const shapes = original.rectangles ?? [];
  const strokes = original.strokes ?? [];
  localized.text.forEach((text, textIndex) => {
    const originalText = original.text[textIndex];
    if (!contains(canvas, text.box)) issues.push({ textIndex, text: text.value, reason: 'outside SVG canvas' });
    if (originalText) {
      const container = containerFor(original, originalText);
      if (container && !contains(container, text.box)) issues.push({ textIndex, text: text.value, reason: 'outside original containing shape' });
      else if (container && edgeClearance(container, text.box) < EDGE_PADDING && edgeClearance(container, originalText.box) >= EDGE_PADDING) {
        issues.push({ textIndex, text: text.value, reason: 'touches the edge of its containing shape' });
      }
      if (text.size < MIN_FONT_PX && !(originalText.size < MIN_FONT_PX)) {
        issues.push({ textIndex, text: text.value, size: text.size, reason: `font size below ${MIN_FONT_PX}px` });
      }
      shapes.forEach((shape, shapeIndex) => {
        if (inTheWay(shape, text.box, originalText.box) && !overlaps(shape, originalText.box)) {
          issues.push({ textIndex, text: text.value, shapeIndex, reason: 'new overlap with a neighbouring shape' });
        }
      });
      strokes.forEach((stroke, strokeIndex) => {
        if (strokeHits(stroke, text.box, originalText.box) && !overlaps(widened(stroke), originalText.box)) {
          issues.push({ textIndex, text: text.value, strokeIndex, reason: 'new overlap with a line or arrow' });
        }
      });
    }
    for (let other = 0; other < textIndex; other++) {
      if (overlaps(text.box, localized.text[other].box) && originalText && original.text[other] && !overlaps(originalText.box, original.text[other].box)) issues.push({ textIndex, other, reason: 'new text overlap' });
    }
  });
  return issues;
}
