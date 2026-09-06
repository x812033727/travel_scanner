import assert from "node:assert/strict";
import { test } from "node:test";
import { duplicateKeys } from "./duplicate-keys.mjs";

test("a key declared twice in the same object is reported with its path", () => {
  const source = `{
  "editor": {
    "transfersCount": "{count} 次",
    "other": "x",
    "transfersCount": "轉乘 {count} 次"
  }
}`;
  assert.deepEqual(duplicateKeys(source), ["editor.transfersCount"]);
});

test("the same key in two different objects is not a duplicate", () => {
  const source = '{"a": {"label": "x"}, "b": {"label": "y"}}';
  assert.deepEqual(duplicateKeys(source), []);
});

test("a duplicate object-valued key is reported too", () => {
  const source = '{"tabs": {"one": "1"}, "tabs": {"two": "2"}}';
  assert.deepEqual(duplicateKeys(source), ["tabs"]);
});

test("a colon inside a value is not read as a key", () => {
  const source = '{"note": "來源：內閣府", "url": "https://example.test/a:b", "note2": "ok"}';
  assert.deepEqual(duplicateKeys(source), []);
});

test("an escaped quote inside a value does not end the string early", () => {
  const source = '{"quote": "she said \\"hi\\": really", "quote2": "fine"}';
  assert.deepEqual(duplicateKeys(source), []);
});

test("arrays of strings are not mistaken for keys", () => {
  const source = '{"list": ["a", "b"], "list2": ["c"], "tail": "x"}';
  assert.deepEqual(duplicateKeys(source), []);
});

test("a real message file parses to nothing", () => {
  const source = '{\n  "a": {"b": "1", "c": "2"},\n  "d": "3"\n}';
  assert.deepEqual(duplicateKeys(source), []);
});
