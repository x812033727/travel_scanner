export function splitFareCents(totalCents, people) {
  if (!Number.isSafeInteger(totalCents) || totalCents < 0) {
    throw new RangeError('totalCents must be a nonnegative safe integer');
  }
  if (!Number.isSafeInteger(people) || people < 1 || people > 100) {
    throw new RangeError('people must be a safe integer from 1 to 100');
  }
  const each = Math.round(totalCents / people);
  return Array(people).fill(each);
}
