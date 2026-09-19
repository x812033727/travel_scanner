import assert from "node:assert/strict";
import test from "node:test";

import { CRAWLER_SOURCES, crawlerGeoBlock, prefixesFrom } from "./nginx-crawler-ranges.mjs";

test("reads both address families out of a published file", () => {
  const payload = { prefixes: [{ ipv4Prefix: "66.249.64.0/19" }, { ipv6Prefix: "2001:4860:4801:10::/64" }] };
  assert.deepEqual(prefixesFrom(payload), ["66.249.64.0/19", "2001:4860:4801:10::/64"]);
});

test("drops anything that is not a bare CIDR", () => {
  // This text goes straight into a file nginx parses, so a row carrying a stray directive
  // must not survive the read.
  const payload = { prefixes: [
    { ipv4Prefix: "66.249.64.0/19" },
    { ipv4Prefix: "1.2.3.4/24; } location / { deny all;" },
    { ipv4Prefix: "not-an-address" },
    { somethingElse: "66.249.65.0/24" },
  ] };
  assert.deepEqual(prefixesFrom(payload), ["66.249.64.0/19"]);
});

test("refuses a file with no usable prefixes rather than returning nothing", () => {
  // Silently emitting an empty allowlist would put every crawler back under the page limit
  // without anyone noticing, which is the bug this tool exists to fix.
  assert.throws(() => prefixesFrom({ prefixes: [] }), /no usable prefixes/);
  assert.throws(() => prefixesFrom({}), /no prefixes array/);
});

test("renders a geo block that defaults to untrusted", () => {
  const block = crawlerGeoBlock([{ name: "googlebot", prefixes: ["66.249.64.0/19"] }]);
  assert.match(block, /geo \$mokaair_verified_crawler \{/);
  // Everything not named is a 0: the limiter must keep applying to ordinary traffic.
  assert.match(block, /^ {4}default 0;$/m);
  assert.match(block, /^ {4}66\.249\.64\.0\/19 1;$/m);
  assert.ok(block.trimEnd().endsWith("}"));
});

test("sorts prefixes so a regenerated file diffs only where the engine changed", () => {
  const block = crawlerGeoBlock([{ name: "bingbot", prefixes: ["40.77.167.0/24", "13.66.139.0/24"] }]);
  assert.ok(block.indexOf("13.66.139.0/24") < block.indexOf("40.77.167.0/24"));
});

test("refuses to write an empty allowlist", () => {
  assert.throws(() => crawlerGeoBlock([]), /empty allowlist/);
  assert.throws(() => crawlerGeoBlock([{ name: "googlebot", prefixes: [] }]), /empty allowlist/);
});

test("names the sources it will fetch over https", () => {
  assert.ok(CRAWLER_SOURCES.length >= 2);
  for (const source of CRAWLER_SOURCES) assert.match(source.url, /^https:\/\//);
});
