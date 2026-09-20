/** Pure geometry helpers used by the localized SVG renderer. */

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
