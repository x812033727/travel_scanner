#!/usr/bin/env node
// Read one page the way the worker will, and say whether the words a fact rests on are in the
// part of it the worker keeps (docs/videos/STORY.md §查核與來源規則).
//
//   node tools/video/story-plans/read.mjs <url> [words to look for ...]
//   node tools/video/story-plans/read.mjs --text <url>    also print the text the worker keeps
//
// The worker's reader (tools/video/automation/fetch.mjs) takes pages of text up to its size
// limit and keeps the first MAX_PAGE_CHARS characters: a PDF, a page too large, a page a script
// draws, or a sentence far down a long page gives the worker's fact check nothing to read.
// The exit code is 1 when the page gives no text or a phrase is not in what is kept.
import path from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

import { MAX_PAGE_CHARS, pageReader } from "../automation/fetch.mjs";
import { reading } from "./validate.mjs";

// "1,740" on the page is the "1740" of a claim, and a full-width digit is its plain one.
const fold = (text) => String(text).normalize("NFKC").toLowerCase().replace(/[\s,，、]+/g, "");

/** { url, status, readable, chars, cut, title, error?, found: [{ words, found }], text }. */
export async function readPage(url, words = [], { fetchImpl = globalThis.fetch, sleep, now } = {}) {
  const page = await pageReader({ fetchImpl, ...(sleep ? { sleep } : {}), ...(now ? { now } : {}) })(url);
  const text = page.ok ? page.text : "";
  const folded = fold(text);
  return { url, ...reading(page), cut: Boolean(page.truncated), title: page.title ?? "", found: words.map((each) => ({ words: each, found: fold(each).length > 0 && folded.includes(fold(each)) })), text };
}

export async function main(argv, { stdout = process.stdout, stderr = process.stderr, fetchImpl = globalThis.fetch } = {}) {
  const { values, positionals } = parseArgs({ args: argv, options: { text: { type: "boolean" } }, allowPositionals: true, strict: true });
  const [url, ...words] = positionals;
  if (!url) {
    stderr.write("usage: node tools/video/story-plans/read.mjs [--text] <url> [words to look for ...]\n");
    return 1;
  }
  const page = await readPage(url, words, { fetchImpl });
  const size = `${page.chars.toLocaleString("en-US")} characters${page.cut ? `, cut at ${MAX_PAGE_CHARS.toLocaleString("en-US")}` : ""}`;
  stdout.write(`${page.status} ${page.readable ? `text, ${size}` : `no text (${page.error})`}${page.title ? ` "${page.title}"` : ""}\n`);
  for (const each of page.found) stdout.write(`${each.found ? "found    " : "NOT FOUND"} ${each.words}\n`);
  if (values.text && page.text) stdout.write(`\n${page.text}\n`);
  return page.readable && page.found.every((each) => each.found) ? 0 : 1;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2)).then((code) => {
    process.exitCode = code;
  });
}
