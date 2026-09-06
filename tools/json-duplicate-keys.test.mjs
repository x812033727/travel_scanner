import assert from "node:assert/strict";
import test from "node:test";

import { duplicateKeys } from "./json-duplicate-keys.mjs";

test("finds nothing in a file with unique keys", () => {
  assert.deepEqual(duplicateKeys('{"a": 1, "b": {"a": 2}}'), []);
});

test("finds the duplicate that shipped in trips.json", () => {
  const source = `{
  "editor": {
    "transfersCount": "{count}",
    "metricFare": "Fare",
    "transfersCount": "{count} transfers"
  }
}`;
  assert.deepEqual(duplicateKeys(source), ["editor.transfersCount"]);
});

test("reports a key repeated more than twice once per extra occurrence", () => {
  assert.deepEqual(duplicateKeys('{"a": 1, "a": 2, "a": 3}'), ["a", "a"]);
});

test("does not confuse a value that looks like a key", () => {
  // The colon is inside the string, so "b:" is a value and not a second key.
  assert.deepEqual(duplicateKeys('{"a": "b: c", "d": "a"}'), []);
});

test("does not confuse an escaped quote inside a value", () => {
  assert.deepEqual(duplicateKeys('{"a": "he said \\"a\\": no", "b": 1}'), []);
});

test("scopes keys to their own object", () => {
  // Same key name in two sibling objects is correct JSON, not a duplicate.
  assert.deepEqual(duplicateKeys('{"one": {"name": 1}, "two": {"name": 2}}'), []);
});

test("finds a duplicate inside an object nested in an array", () => {
  assert.deepEqual(duplicateKeys('{"rows": [{"id": 1, "id": 2}]}'), ["rows.id"]);
});

test("attributes a nested object to its own key, not to the previous scalar", () => {
  const source = '{"first": "scalar", "second": {"x": 1, "x": 2}}';
  assert.deepEqual(duplicateKeys(source), ["second.x"]);
});

test("handles a key whose text needs unescaping", () => {
  assert.deepEqual(duplicateKeys('{"a\\"b": 1, "a\\"b": 2}'), ['a"b']);
});
