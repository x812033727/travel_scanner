import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { createHash } from 'node:crypto';
import assert from 'node:assert/strict';

const original = 'ß';
const upper = original.toUpperCase();
const returned = upper.toLowerCase();
assert.equal(upper, 'SS');
assert.notEqual(returned, original);
const turkish = 'i'.toLocaleUpperCase('tr');
const defaultUpper = 'i'.toUpperCase();
assert.notEqual(turkish, defaultUpper);
const lookalikes = ['B', '\u0392'].map(input => ({ input, code_point: input.codePointAt(0), lower: input.toLowerCase() }));
assert.notEqual(lookalikes[0].lower, lookalikes[1].lower);
const sorting = ['de', 'sv'].map(locale => {
  const collator = new Intl.Collator(locale);
  return { requested_locale: locale, resolved: collator.resolvedOptions(), output: ['z', 'ä', 'a'].sort(collator.compare) };
});
assert.notDeepEqual(sorting[0].output, sorting[1].output);
const hostname = new URL('https://例子.test').hostname;
assert.match(hostname, /^xn--/);
const here = fileURLToPath(import.meta.url);
const receipt = {
  status: 'PASS_LOCAL_TEXT_PROBES_NOT_FONT_DISPLAY_OR_AUDIENCE_TEST',
  tested_on: new Date().toISOString(),
  runtime: { node: process.version, icu: process.versions.icu, unicode: process.versions.unicode },
  source_sha256: createHash('sha256').update(fs.readFileSync(here)).digest('hex'),
  probes: {
    U4006: { original, upper, returned },
    U4007: { input: 'i', default_upper: defaultUpper, turkish_upper: turkish },
    U4012: lookalikes,
    U4004: sorting,
    U4011: { input: '例子.test', ascii_hostname: hostname, network_request: false },
  },
  limits: 'Actual outputs from one pinned local runtime. No claim about every editor, font, browser, current Unicode implementation or all locales. Domains use reserved .test; no network operation. Typography, ZWJ fallback, OCR and complete script timing were not tested.',
  production_ready: false,
};
fs.writeFileSync(path.resolve(path.dirname(here), '../reviews/wave4-text-probes.json'), JSON.stringify(receipt, null, 2) + '\n');
console.log(JSON.stringify(receipt));
