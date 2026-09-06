/**
 * Find duplicate object keys in JSON source text.
 *
 * `JSON.parse` keeps the last of two identical keys and reports nothing, so a duplicate is
 * invisible to every check that reads the file as data. All five `messages/*​/trips.json`
 * files carried two `transfersCount` entries and nothing displayed wrongly, because the
 * runtime also kept the last one. The cost showed up elsewhere: any tool that read one of
 * those files and wrote it back collapsed the pair, and the collapse arrived in the diff
 * looking like a copy change nobody made.
 *
 * So this reads the text rather than the parsed value. It is a scanner, not a parser: it
 * walks the source tracking string literals and object nesting, and treats a string as a key
 * when the next non-whitespace character is a colon. That is enough for well-formed JSON,
 * which is all these files ever are — `JSON.parse` runs on them first and rejects the rest.
 */

/**
 * @param {string} source well-formed JSON text
 * @returns {string[]} dotted paths of keys that appear more than once in the same object,
 *   in the order the duplicate occurrences were found
 */
export function duplicateKeys(source) {
  const duplicates = [];
  const seenPerObject = [];
  const path = [];
  let pendingKey = null;
  let index = 0;

  while (index < source.length) {
    const character = source[index];

    if (character === '"') {
      const start = index;
      index += 1;
      while (index < source.length) {
        if (source[index] === "\\") {
          index += 2;
          continue;
        }
        if (source[index] === '"') break;
        index += 1;
      }
      const literal = source.slice(start, index + 1);
      index += 1;

      let lookahead = index;
      while (lookahead < source.length && /\s/.test(source[lookahead])) lookahead += 1;
      if (source[lookahead] === ":" && seenPerObject.length > 0) {
        const key = JSON.parse(literal);
        const seen = seenPerObject[seenPerObject.length - 1];
        if (seen.has(key)) duplicates.push([...path, key].filter(Boolean).join("."));
        seen.add(key);
        pendingKey = key;
      }
      continue;
    }

    if (character === "{") {
      seenPerObject.push(new Set());
      path.push(pendingKey);
      pendingKey = null;
    } else if (character === "}") {
      seenPerObject.pop();
      path.pop();
      pendingKey = null;
    } else if (character === ",") {
      // Without this a scalar value would leave its key in place, and the next sibling
      // object would be attributed to it.
      pendingKey = null;
    }
    index += 1;
  }

  return duplicates;
}
