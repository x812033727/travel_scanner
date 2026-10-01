import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { createHash } from 'node:crypto';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

// Text packages only: no remote calls, TTS, images, imports or scheduling.
const base = dirname(fileURLToPath(import.meta.url));
const batches = {
  batch01: ['B26', 'S26', 'T26', 'A31'],
  batch02: ['B27', 'S27', 'T28', 'A33'],
  batch03: ['B48', 'S44', 'T33', 'A36'],
  batch04: ['B37', 'S31', 'T29', 'A41'],
  batch05: ['B46', 'S32', 'T41', 'A40'],
};
const batch = process.argv.find((arg) => arg.startsWith('--batch='))?.slice(8) ?? 'batch01';
if (!Object.hasOwn(batches, batch)) {
  console.error(`FAIL: unknown batch ${batch}`);
  process.exit(1);
}
const ids = batches[batch];
const locales = ['en', 'ja', 'ko', 'zh-CN', 'zh-TW'];
const errors = [];
const assert = (ok, message) => { if (!ok) errors.push(message); };
const read = (path) => readFileSync(resolve(base, path), 'utf8');
const hash = (path) => createHash('sha256').update(readFileSync(resolve(base, path))).digest('hex');
const chars = (value) => [...value].length;
const units = (value) => (value.match(/\p{Script=Han}|[A-Za-z0-9]+/gu) ?? []).length;
const same = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const metadata = (value, label) => {
  assert(same(Object.keys(value ?? {}).sort(), locales), `${label}: exactly five locales required`);
  for (const lang of locales) {
    const row = value?.[lang];
    assert(typeof row?.title === 'string' && chars(row.title) > 0 && chars(row.title) <= 100,
      `${label}/${lang}: title length must be 1..100`);
    assert(typeof row?.description === 'string' && chars(row.description) > 0 && chars(row.description) <= 5000,
      `${label}/${lang}: description length must be 1..5000`);
    assert(/https:\/\//.test(row?.description ?? ''), `${label}/${lang}: source URL required`);
  }
};

try {
  const topics = JSON.parse(read('../season2-topics.json'));
  const topicIds = topics.episodes.map((e) => e.id);
  const originalIds = ['B', 'S', 'T', 'A'].flatMap((pillar) =>
    Array.from({ length: 25 }, (_, i) => `${pillar}${i + 26}`));
  assert(topicIds.length === 100 && new Set(topicIds).size === 100 &&
    same([...topicIds].sort(), originalIds.sort()), 'candidate inventory: original 100 IDs required');
  for (const topic of topics.episodes) {
    assert(topic.status === 'checked', `${topic.id}: preserve topic-check status`);
    assert(typeof topic.check === 'string' && existsSync(resolve(base, '..', topic.check)),
      `${topic.id}: original check report must exist`);
  }
  const episodes = ids.map((id, i) => {
    const path = `${id}.md`;
    const source = read(path);
    const jsonBlocks = [...source.matchAll(/```json\r?\n([\s\S]*?)\r?\n```/g)];
    const textBlocks = [...source.matchAll(/```text\r?\n([\s\S]*?)\r?\n```/g)].map((m) => m[1]);
    assert(jsonBlocks.length === 1, `${id}: one packaging JSON block required`);
    assert(textBlocks.length === 4, `${id}: premise, note, two spoken Shorts required`);
    const packaging = JSON.parse(jsonBlocks[0][1]);
    assert(packaging.id === id, `${id}: packaging ID mismatch`);
    metadata(packaging.localizations, id);
    assert(packaging.shorts?.length === 2, `${id}: exactly two Shorts required`);
    packaging.shorts.forEach((short, j) => {
      assert(short.id === `${id}-${j + 1}`, `${id}: Short ID/order mismatch`);
      metadata(short.localizations, short.id);
    });
    assert(chars(textBlocks[0]) <= 4000 && chars(textBlocks[1]) <= 2000,
      `${id}: backend premise/note exceeds field limit`);
    const shorts = textBlocks.slice(2).map((spoken, j) => {
      const count = units(spoken);
      const range = [count * 60 / 300, count * 60 / 250].map((n) => Number(n.toFixed(1)));
      assert(count >= 180 && count <= 220, `${id}-${j + 1}: expected 180..220 spoken units, got ${count}`);
      assert(range[0] >= 35 && range[1] <= 55, `${id}-${j + 1}: estimated range outside 35..55s`);
      return { ...packaging.shorts[j], spoken, spoken_units: count, estimated_seconds: range };
    });
    const beforeShorts = source.split('## Shorts')[0];
    const durations = beforeShorts.split(/\r?\n/).flatMap((line) => {
      if (!line.startsWith('| ')) return [];
      const cells = line.split('|').map((cell) => cell.trim());
      if (/^\d+$/.test(cells[2] ?? '') && cells[1] !== '合計') return [Number(cells[2])];
      if (/^[1-6]／/.test(cells[1] ?? '')) {
        const match = cells[1].match(/／(\d+)(?: 秒)?$/);
        if (match) return [Number(match[1])];
      }
      return [];
    });
    assert(durations.length === 6 && durations.reduce((a, b) => a + b, 0) === 480,
      `${id}: six chapters must total 480 proposed seconds`);
    for (const match of source.matchAll(/\[[^\]]+\]\(([^)]+)\)/g)) {
      const link = match[1].split('#')[0];
      if (link && !/^https?:/.test(link)) assert(existsSync(resolve(base, link)), `${id}: missing local link ${link}`);
    }
    const receiptPath = `reviews/${batch}/${id}.json`;
    const receipt = JSON.parse(read(receiptPath));
    assert(receipt.id === id && receipt.status === 'PASS', `${id}: passing receipt required`);
    assert(receipt.author_agent && receipt.reviewer_agent && receipt.author_agent !== receipt.reviewer_agent,
      `${id}: reviewer must differ from original author`);
    assert(receipt.review_scope === 'TEXT_ONLY', `${id}: review scope must remain text only`);
    assert(receipt.package === path && receipt.package_sha256 === hash(path), `${id}: stale package hash`);
    assert(receipt.report === `reviews/${batch}/${id}.md` && receipt.report_sha256 === hash(receipt.report),
      `${id}: stale report hash`);
    assert(read(receipt.report).toLowerCase().includes(receipt.package_sha256), `${id}: report must name current package hash`);
    const topic = topics.episodes.find((row) => row.id === id);
    assert(topic.production?.package === `season2/${path}` &&
      topic.production?.review === `season2/${receiptPath}` &&
      topic.production?.status === 'package-reviewed' && topic.production?.batch === batch,
      `${id}: candidate production pointer missing`);
    return { id, proposed_order: i + 1, package: path, package_sha256: hash(path),
      review_receipt: receiptPath, target_seconds: 480, localizations: packaging.localizations,
      backend_inputs: { premise: textBlocks[0], note: textBlocks[1] }, shorts };
  });
  const expected = { schema_version: 1, batch, source_checked_on: '2026-10-01',
    status: 'TEXT_PACKAGES_REVIEWED', schedule_status: 'PROPOSED_NOT_SCHEDULED',
    media_generated: false, platform_imported: false, published: false, episodes };
  if (process.argv.includes('--write')) {
    if (errors.length) throw new Error('Cannot write bundle with validation errors');
    writeFileSync(resolve(base, `${batch}-packaging.json`), `${JSON.stringify(expected, null, 2)}\n`);
  } else {
    assert(same(JSON.parse(read(`${batch}-packaging.json`)), expected), 'bundle differs from reviewed Markdown; regenerate with --write');
  }
} catch (error) {
  errors.push(error.message);
}
if (errors.length) {
  errors.forEach((message) => console.error(`FAIL: ${message}`));
  process.exitCode = 1;
} else {
  console.log(`PASS ${batch}: 100 candidate IDs, 4 packages, 8 Shorts, 60 localized title/description pairs, fields, chapters, links and review hashes.`);
  console.log('Text only. Timings are estimates; no media, platform or owner acceptance is asserted.');
}
