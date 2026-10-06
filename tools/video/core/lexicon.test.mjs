import assert from "node:assert/strict";
import test from "node:test";

import { entriesUsed, isKnownTerm, latinTerms, substitutions, unknownTerms, validateLexicon } from "./lexicon.mjs";

const lexicon = { schema_version: 1, terms: { GPT: "G P T", Claude: null, "Claude Code": "Claude Code", Node: null, js: "J S", p95: "P 九十五" } };

test("latinTerms keeps joined terms whole and lists each once", () => {
  assert.deepEqual(latinTerms("用 GPT-5.5 和 Claude，再用 Claude 跑 Node.js 與 C#，看 p95"), ["GPT-5.5", "Claude", "Node.js", "C#", "p95"]);
  assert.deepEqual(latinTerms("全部是中文，還有 2026 年"), []);
});

test("a term is known when it is listed, a single letter, or made of known parts and numbers", () => {
  assert.ok(isKnownTerm("Claude", lexicon));
  assert.ok(isKnownTerm("A", lexicon));
  assert.ok(isKnownTerm("GPT-5.5", lexicon));
  assert.ok(isKnownTerm("Node.js", lexicon));
  assert.ok(!isKnownTerm("Gemini", lexicon));
  assert.ok(!isKnownTerm("GPT-mini", lexicon));
});

test("unknownTerms is what lint reports", () => {
  assert.deepEqual(unknownTerms("Claude 和 Gemini 還有 GPT-4o", lexicon), ["Gemini", "GPT-4o"]);
});

test("validateLexicon wants a spoken form or null for every term", () => {
  assert.deepEqual(validateLexicon(lexicon), []);
  const bad = validateLexicon({ schema_version: 1, terms: { API: "", "5G": null } });
  assert.deepEqual(bad.map((error) => error.path), ["terms.API", "terms.5G"]);
  assert.equal(validateLexicon([]).length, 1);
});

test("substitutions put longer terms first so a phrase wins over its first word", () => {
  assert.deepEqual(substitutions(lexicon).map(([term]) => term), ["Claude Code", "GPT", "p95", "js"]);
});

test("entriesUsed lists every dictionary entry a video's texts use, spoken or not, with the forms it appears in", () => {
  const texts = ["用 GPT-5.5 和 Claude Code 跑 Node.js，再看 p95。", "Claude 比 GPT-6 快，APIs 不算。"];
  assert.deepEqual(entriesUsed(texts, lexicon), [
    // "Claude Code" is its own entry, never a use of "Claude"; the standalone "Claude" is.
    { term: "Claude", say: null, forms: ["Claude"] },
    { term: "Claude Code", say: "Claude Code", forms: ["Claude Code"] },
    // A joined term shows the whole form the viewer sees, once per distinct form.
    { term: "GPT", say: "G P T", forms: ["GPT-5.5", "GPT-6"] },
    { term: "Node", say: null, forms: ["Node.js"] },
    { term: "js", say: "J S", forms: ["Node.js"] },
    { term: "p95", say: "P 九十五", forms: ["p95"] },
  ]);
  assert.deepEqual(entriesUsed(["全部是中文，還有 Gemini"], lexicon), [], "an unknown Latin word is not a dictionary entry");
  assert.deepEqual(entriesUsed(["Claude"], { schema_version: 1, terms: {} }), []);
  assert.deepEqual(entriesUsed(["Claude"], null), []);
});
