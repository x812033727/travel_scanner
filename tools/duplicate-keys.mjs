/**
 * Keys a JSON object declares twice, as `path.key` strings.
 *
 * `JSON.parse` keeps the last one and silently drops the rest, so a duplicate is invisible
 * to every check that parses first — including check-i18n's own. It stays invisible until
 * something reads a file and writes it back, and then the collapsed keys arrive in a diff
 * looking like copy changes nobody made. Hence a scan of the raw text, which has to know
 * where a string ends so a `":"` inside a value is not read as a key.
 */
export function duplicateKeys(source) {
  const duplicates = [];
  const path = [];
  const seen = [];
  let index = 0;
  let pendingKey = null;
  let lastKey = null;
  while (index < source.length) {
    const character = source[index];
    if (character === '"') {
      let end = index + 1;
      while (end < source.length && (source[end] !== '"' || source[end - 1] === "\\")) end += 1;
      pendingKey = source.slice(index + 1, end);
      index = end + 1;
      continue;
    }
    if (character === "{") {
      seen.push(new Set());
      path.push(lastKey ?? "");
      lastKey = null;
      pendingKey = null;
    } else if (character === "}") {
      seen.pop();
      path.pop();
      pendingKey = null;
    } else if (character === ":" && pendingKey !== null && seen.length > 0) {
      const current = seen[seen.length - 1];
      if (current.has(pendingKey)) duplicates.push([...path.filter(Boolean), pendingKey].join("."));
      current.add(pendingKey);
      lastKey = pendingKey;
      pendingKey = null;
    } else if (character === "," || character === "[" || character === "]") {
      pendingKey = null;
    }
    index += 1;
  }
  return duplicates;
}
