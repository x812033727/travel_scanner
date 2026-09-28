import assert from "node:assert/strict";
import { test } from "node:test";

import { MAX_PAGE_CHARS } from "../automation/fetch.mjs";
import { main, readPage } from "./read.mjs";

const page = (body, { status = 200, type = "text/html; charset=utf-8" } = {}) => new Response(body, { status, headers: { "content-type": type } });
const html = (body) => `<html><head><title>年報</title></head><body>${body}</body></html>`;
const filler = "這一段是頁面上的其他文字。".repeat(40);
const capture = () => ({ text: "", write(chunk) { this.text += chunk; } });

test("readPage says whether the worker's reader finds the words on the page", async () => {
  const fetchImpl = async () => page(html(`<p>${filler}</p><p>２０２５ 年賣出 1,740 億個紙盒，營收 6.8 billion。</p>`));
  const read = await readPage("https://example.com/report", ["1740 億", "2025年", "6.8 Billion", "三千億", " "], { fetchImpl });
  assert.equal(read.status, 200);
  assert.equal(read.readable, true);
  assert.equal(read.cut, false);
  assert.equal(read.title, "年報");
  // Commas, spaces, letter case and full-width digits do not decide a match; an empty phrase finds nothing.
  assert.deepEqual(read.found.map((each) => each.found), [true, true, true, false, false]);
});

test("a sentence past what the reader keeps is not there for the worker", async () => {
  const fetchImpl = async () => page(html(`<p>${"x".repeat(MAX_PAGE_CHARS + 10)}</p><p>the figure is 1972</p>`));
  const read = await readPage("https://example.com/long", ["1972"], { fetchImpl });
  assert.equal(read.readable, true);
  assert.equal(read.cut, true);
  assert.equal(read.chars, MAX_PAGE_CHARS);
  assert.deepEqual(read.found, [{ words: "1972", found: false }]);
});

test("read.mjs reports a page, its phrases, and fails when the worker would have nothing", async () => {
  const good = capture();
  const fetchImpl = async (url) => (url.endsWith(".pdf") ? page("%PDF-1.7", { type: "application/pdf" }) : page(html(`<p>${filler}</p><p>founded in 1958</p>`)));
  assert.equal(await main(["https://example.com/history", "1958"], { stdout: good, stderr: good, fetchImpl }), 0);
  assert.match(good.text, /^200 text, [\d,]+ characters "年報"\nfound {5}1958\n$/);

  const missing = capture();
  assert.equal(await main(["https://example.com/history", "1958", "1962"], { stdout: missing, stderr: missing, fetchImpl }), 1);
  assert.match(missing.text, /NOT FOUND 1962/);

  const pdf = capture();
  assert.equal(await main(["https://example.com/report.pdf"], { stdout: pdf, stderr: pdf, fetchImpl }), 1);
  assert.match(pdf.text, /^200 no text \(not a text page \(application\/pdf\)\)\n$/);

  const text = capture();
  assert.equal(await main(["--text", "https://example.com/history"], { stdout: text, stderr: text, fetchImpl }), 0);
  assert.match(text.text, /founded in 1958/);

  const usage = capture();
  assert.equal(await main([], { stdout: usage, stderr: usage, fetchImpl }), 1);
  assert.match(usage.text, /^usage: /);
});
