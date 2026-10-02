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
  batch06: ['B44', 'S43', 'T43', 'A46'],
  batch07: ['B47', 'S48', 'T48', 'A44'],
  batch08: ['B50', 'S36', 'T45', 'A39'],
  batch09: ['B42', 'S35', 'T35', 'A37'],
};
const batch = process.argv.find((arg) => arg.startsWith('--batch='))?.slice(8) ?? 'batch01';
if (batch !== 'completion' && !Object.hasOwn(batches, batch)) {
  console.error(`FAIL: unknown batch ${batch}`);
  process.exit(1);
}
let ids = batches[batch];
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
  if (batch === 'completion') {
    const dispositions = JSON.parse(read('dispositions.json'));
    assert(dispositions.schema_version === 1 && dispositions.status === 'COMPLETE' &&
      dispositions.review_scope === 'TEXT_ONLY', 'dispositions: complete text review required');
    assert(dispositions.media_generated === false && dispositions.platform_imported === false &&
      dispositions.published === false && dispositions.schedule_status === 'PROPOSED_NOT_SCHEDULED',
      'dispositions: media, import, publication and scheduling must remain unaccepted');
    const rows = dispositions.episodes ?? [];
    assert(rows.length === 100 && new Set(rows.map((row) => row.id)).size === 100 &&
      same(rows.map((row) => row.id).sort(), [...topicIds].sort()), 'dispositions: exact original 100 IDs required');
    const inventory = topics.episodes.map(({ production, ...original }) => original);
    assert(dispositions.source_inventory_sha256 === createHash('sha256').update(JSON.stringify(inventory)).digest('hex'),
      'dispositions: original topic inventory changed');
    for (const review of dispositions.pillar_reviews ?? []) {
      assert(review.review_scope === 'TEXT_ONLY', `${review.pillar}: disposition review scope must remain text only`);
      assert(review.author_agent && review.reviewer_agent && review.author_agent !== review.reviewer_agent,
        `${review.pillar}: independent disposition review required`);
      assert(review.status === 'PASS' && hash(review.report) === review.report_sha256,
        `${review.pillar}: stale or missing disposition report`);
      assert(hash(review.selection) === review.selection_sha256 &&
        read(review.report).toLowerCase().includes(review.selection_sha256),
        `${review.pillar}: disposition report must bind current selection`);
    }
    assert(same((dispositions.pillar_reviews ?? []).map((row) => row.pillar).sort(), ['A', 'B', 'S', 'T']),
      'dispositions: four pillar reviews required');
    for (const row of rows) {
      const topic = topics.episodes.find((entry) => entry.id === row.id);
      assert(['adopt', 'angle', 'reject-duplicate'].includes(row.decision) && row.status === 'reviewed',
        `${row.id}: unresolved disposition`);
      assert(typeof row.reason === 'string' && chars(row.reason) >= 20, `${row.id}: concrete disposition reason required`);
      assert(row.original_title === topic?.title && row.original_check === topic?.check && row.original_verdict === topic?.verdict,
        `${row.id}: original title, check and verdict must be preserved`);
      if (row.decision === 'reject-duplicate') {
        assert(row.package === null && row.review_receipt === null && row.batch === null,
          `${row.id}: rejected topic must not have a fabricated production package`);
        assert((row.duplicate_of ?? []).length > 0, `${row.id}: duplicate evidence required`);
        for (const evidence of row.duplicate_of ?? []) {
          assert(typeof evidence.core === 'string' && chars(evidence.core) >= 10 &&
            existsSync(resolve(base, evidence.path)), `${row.id}: duplicate source or explanation missing`);
          assert(evidence.source_sha256 === hash(evidence.path), `${row.id}: duplicate source changed since review`);
          if (evidence.record_id) {
            const document = JSON.parse(read(evidence.path));
            const record = (document.episodes ?? document.stories ?? document.terms ?? []).find((entry) => entry.id === evidence.record_id);
            assert(record,
              `${row.id}: duplicate record ID not found`);
            assert(evidence.record_sha256 === createHash('sha256').update(JSON.stringify(record)).digest('hex'),
              `${row.id}: duplicate record changed since review`);
          }
        }
        assert(topic?.production?.status === 'not-adopted' &&
          topic.production.disposition === `season2/dispositions.json#${row.id}`,
          `${row.id}: non-adopted production pointer missing`);
      } else {
        assert(row.batch === 'completion' || Object.hasOwn(batches, row.batch), `${row.id}: unknown production batch`);
        assert(row.package === `${row.id}.md` &&
          row.review_receipt === `reviews/${row.batch}/${row.id}.json`, `${row.id}: adopted package/receipt required`);
        const receipt = JSON.parse(read(row.review_receipt));
        assert(receipt.status === 'PASS' && receipt.package_sha256 === hash(row.package) &&
          receipt.report_sha256 === hash(receipt.report), `${row.id}: disposition points to stale review`);
        assert(receipt.author_agent && receipt.reviewer_agent && receipt.author_agent !== receipt.reviewer_agent &&
          receipt.review_scope === 'TEXT_ONLY', `${row.id}: disposition must point to independent text review`);
        assert(topic?.production?.package === `season2/${row.package}` &&
          topic.production.review === `season2/${row.review_receipt}` && topic.production.status === 'package-reviewed',
          `${row.id}: adopted production pointer missing`);
      }
    }
    const preserved = JSON.parse(read('reviews/completion/preserved-artifacts.json'));
    assert(preserved.base_commit === 'aa203808e0729b9c66bea1c3d611a353dc8952ad' && preserved.files.length === 117,
      'preservation: previous nine batches require 117 artifacts');
    assert(new Set(preserved.files.map((row) => row.path)).size === 117, 'preservation: duplicate artifact paths');
    for (const row of preserved.files) assert(hash(row.path) === row.sha256, `preservation: changed ${row.path}`);
    ids = rows.filter((row) => row.batch === 'completion' && row.decision !== 'reject-duplicate').map((row) => row.id);
    assert(ids.length > 0, 'completion: no adopted packages');
    const adopted = rows.filter((row) => row.decision !== 'reject-duplicate').map((row) => row.id);
    assert(same(dispositions.totals, { candidates: rows.length, adopted: adopted.length,
      reject_duplicate: rows.length - adopted.length, pending: 0, new_packages: ids.length,
      preserved_packages: adopted.length - ids.length, shorts: adopted.length * 2,
      localized_title_description_pairs: adopted.length * 15 }), 'dispositions: totals differ from reviewed rows');
    const order = dispositions.proposed_order ?? [];
    assert(order.length === adopted.length && new Set(order.map((row) => row.id)).size === adopted.length &&
      same(order.map((row) => row.id).sort(), [...adopted].sort()) &&
      order.every((row, i) => row.proposed_order === i + 1), 'dispositions: proposed order must contain each adopted ID once');
  }
  const episodes = ids.map((id, i) => {
    const path = `${id}.md`;
    const source = read(path);
    if (batch === 'completion') {
      assert(!source.includes('\r') && !source.startsWith('\uFEFF') && source.endsWith('\n') &&
        !source.endsWith('\n\n'), `${id}: LF text with a single final newline required`);
      let promptGroup = 'other';
      const promptGroups = { chapters: 0, short1: 0, short2: 0, thumbnails: 0, other: 0 };
      const prompts = source.split('```json')[0].split(/\r?\n/).flatMap((line) => {
        const shortHeading = line.match(/^### Short ([12])(?:\s|$)/);
        if (shortHeading) promptGroup = `short${shortHeading[1]}`;
        else if (line.startsWith('## ')) promptGroup = /縮圖/.test(line) ? 'thumbnails' : /^## 六章/.test(line) ? 'chapters' : 'other';
        const collect = (values) => { promptGroups[promptGroup] += values.length; return values; };
        if (line.startsWith('|')) {
          const cells = line.split('|').map((cell) => cell.trim()).filter(Boolean);
          const value = cells.at(-1)?.replace(/^`|`$/g, '') ?? '';
          return collect(/^[A-Z]/.test(value) && value.length > 80 && !/\p{Script=Han}/u.test(value) ? [value] : []);
        }
        const labeled = line.match(/Prompt[：:]\s*([A-Z][^\r\n]+)$/);
        if (labeled) {
          const value = labeled[1].replace(/^`|`$/g, '');
          return collect(value.length > 80 && !/\p{Script=Han}/u.test(value) ? [value] : []);
        }
        return collect([...line.matchAll(/`([^`\r\n]+)`/g)].map((match) => match[1])
          .filter((value) => /^[A-Z]/.test(value) && value.length > 80 && !/\p{Script=Han}/u.test(value)));
      });
      assert(prompts.length === 18 && same(promptGroups, { chapters: 6, short1: 5, short2: 5, thumbnails: 2, other: 0 }),
        `${id}: six chapter, ten Short and two thumbnail prompts required (6/5/5/2)`);
    }
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
      if (batch === 'completion') {
        const sentences = (spoken.match(/[^。！？]+(?:[。！？]+|$)/gu) ?? []).map((sentence) => sentence.trim());
        assert(sentences.every((sentence) => chars(sentence) <= 40), `${id}-${j + 1}: sentence exceeds 40 characters`);
        assert(!/https?:|[()（）]/.test(spoken), `${id}-${j + 1}: spoken script contains URL or parenthesis`);
      }
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
  console.log(`PASS ${batch}: 100 candidate IDs, ${ids.length} packages, ${ids.length * 2} Shorts, ${ids.length * 15} localized title/description pairs, fields, chapters, links and review hashes.`);
  console.log('Text only. Timings are estimates; no media, platform or owner acceptance is asserted.');
}
