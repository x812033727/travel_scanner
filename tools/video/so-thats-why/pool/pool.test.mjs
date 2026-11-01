import assert from 'node:assert/strict';
import test from 'node:test';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { assemble, normalizeUrl, urlsIn, readPool, similarityPairs, validateEditorial, DIR, ROOT } from './core.mjs';
import { readBaseline, compareBaseline, validateBaseline, validateCheckpoints, sourceImpact } from './history.mjs';
import { openStore, ingest, assertSnapshot, search, lookup } from './store.mjs';
import { validateThemes, renderHtml } from './render.mjs';

const source = (id) => ({ id, url: `https://example.org/${id}`, readings: [{ origin: 'fixture', title: id, publisher: 'fixture', accessed_on: '2026-11-01', reading_scope: 'test fixture' }] });
const record = (id, question, target = 'different mechanism') => ({ id, origin: 'fixture', question, domain: 'test', mechanism_key: id, answer_target: target, scope: 'fixture scope', source_refs: [{ source_id: id, locator: `section ${id}` }], premise_status: 'screened', eligible: true, notes: '', local_references: [] });
const input = (rows) => ({ records: rows, sources: rows.map((row) => source(row.id)), inputs: [] });
const empty = () => ({ merges: [], distinct: [], excluded: [] });
const choose = (ids) => ({ ids, target_count: ids.length, reason: 'Test fixture selection' });

test('exact wording variants preserve both source histories and raw IDs', () => {
  const rows = [record('a', '門把為什麼會電人？', '電荷與放電'), record('b', '門把為什麼會電人?', '另一份資料')];
  const pool = assemble(input(rows), empty(), choose(['a']));
  assert.equal(pool.counts.raw_records, 2);
  assert.equal(pool.counts.canonical_questions, 1);
  assert.equal(pool.dedup.aliases.b, 'a');
  assert.deepEqual(pool.candidates[0].source_refs.map((ref) => ref.source_id), ['a', 'b']);
  assert.equal(pool.candidates[0].production_ready, false);
});

test('similarity never silently merges or publishes an unresolved pair', () => {
  const rows = [record('a', '冰箱的門打開為什麼不能讓房間變涼？', '房間邊界中的熱量收支'), record('b', '冰箱門打開為什麼不能讓整個房間變涼？', '房間邊界中的熱量收支')];
  const draft = assemble(input(rows));
  assert.equal(draft.counts.canonical_questions, 2);
  assert.equal(draft.counts.high_similarity_pending, 1);
  assert.throws(() => assemble(input(rows), empty(), choose(['a', 'b'])), /high-similarity/);
  const decisions = { ...empty(), merges: [{ duplicate_id: 'b', canonical_id: 'a', reason: 'Same boundary and causal question' }] };
  assert.equal(assemble(input(rows), decisions, choose(['a'])).counts.selected_candidates, 1);
});

test('rejected historical questions cannot be revived through a new alias', () => {
  const old = { ...record('old', '已拒絕的錯誤前提'), premise_status: 'excluded_legacy', eligible: false };
  const next = record('new', '同核心改成新標題');
  const decisions = { ...empty(), merges: [{ duplicate_id: 'old', canonical_id: 'new', reason: 'same rejected core' }] };
  assert.throws(() => assemble(input([old, next]), decisions, choose(['new'])), /eligible canonical/);
  assert.throws(() => assemble(input([next]), empty(), choose(['missing'])), /eligible canonical/);
});

test('common mechanism keys and answer-only matches still reach editorial review', () => {
  const rows = Array.from({ length: 45 }, (_, i) => ({ ...record(String(i), String.fromCodePoint(0x4e00 + i), `target ${i}`), mechanism_key: 'same_mechanism' }));
  assert.equal(similarityPairs(rows).filter((pair) => pair.required).length, 45 * 44 / 2);
  const differentTitles = [record('a', '鐘錶', '地球自轉造成觀測方向隨時間改變'), record('b', '雨鞋', '地球自轉造成觀測方向隨時間改變')];
  assert.equal(similarityPairs(differentTitles)[0].required, true);
});

test('source parser preserves balanced paths, splits prose and rejects unsafe URL schemes', () => {
  assert.deepEqual(urlsIn('[x](https://example.org/A_(B)/C)中文；https://example.org/q?id=1。'), ['https://example.org/A_(B)/C', 'https://example.org/q?id=1']);
  assert.equal(normalizeUrl('https://example.org/a?x=1&utm_source=test#part'), 'https://example.org/a?x=1');
  for (const url of ['file:///secret', 'javascript:alert(1)', 'https://u:p@example.org', 'http://127.0.0.1/']) assert.throws(() => normalizeUrl(url));
});

test('index import is idempotent, atomic, and retains earlier revisions', () => {
  const db = openStore(':memory:');
  try {
    const first = assemble(input([record('a', '冰箱怎麼搬走熱量？', '熱量與功'), record('b', '雲裡的水滴如何形成？', '凝結條件')]), empty(), choose(['a', 'b']));
    assert.equal(ingest(db, first).status, 'IMPORTED');
    assert.equal(ingest(db, first).writes, 0);
    assert.deepEqual(search(db, '冰箱').map((row) => row.id), ['a']);
    assert.deepEqual(search(db, '水滴如何').map((row) => row.id), ['b']);
    assert.deepEqual(search(db, '"; DROP TABLE candidates; --'), []);
    assert.equal(lookup(db, 'a').sources[0].id, 'a');
    const second = structuredClone(first);
    second.candidates[0].question = '冰箱換了一個研究角度？';
    assert.throws(() => ingest(db, second, { beforeCommit: () => { throw new Error('interrupt'); } }), /interrupt/);
    assertSnapshot(db, first);
    assert.equal(lookup(db, 'a').candidate.question, first.candidates[0].question);
    ingest(db, second);
    assert.throws(() => assertSnapshot(db, first), /stale/);
    assert.equal(db.prepare("SELECT count(*) AS n FROM revisions WHERE kind='canonical_question' AND record_id='a'").get().n, 2);
    const third = assemble(input([record('b', '雲裡的水滴如何形成？', '凝結條件')]), empty(), choose(['b']));
    third.sources[0].readings[0].reading_scope = 'revised source scope';
    ingest(db, third);
    assert.equal(lookup(db, 'a').indexed_active, false);
    assert.equal(lookup(db, 'a').candidate.selected, false);
    assert.equal(db.prepare("SELECT count(*) AS n FROM revisions WHERE kind='source' AND record_id='b'").get().n, 2);
  } finally { db.close(); }
});

test('immutable first 1000 baseline remains readable with raw rows, aliases and themes', () => {
  const baseline = readBaseline();
  assert.equal(baseline.pool.counts.selected_candidates, 1000);
  assert.equal(baseline.pool.raw_records.length, 1224);
  assert.equal(baseline.pool.dedup.aliases.N098, 'L097');
  assert.equal(baseline.themes.episodes.length, 12);
  assert.equal(baseline.pool.candidates.filter((row) => row.selected).length, 1000);
});

test('immutable second revision has 2000 distinct candidates without rewriting baseline records', () => {
  const pool = readBaseline(ROOT, 'checkpoint-2000.json').pool;
  const selected = pool.candidates.filter((row) => row.selected);
  assert.equal(pool.revision, '2026-11-01-pool-2000');
  assert.equal(selected.length, 2000);
  assert.equal(new Set(selected.map((row) => row.id)).size, 2000);
  const changes = compareBaseline(readBaseline(), pool);
  assert.deepEqual(changes.changed_baseline_raw_ids, []);
  assert.equal(changes.added_selected_ids.length + changes.carried_distinct_cores, 2000);
  assert.equal(pool.counts.historical_records, 313);
  assert.equal(pool.counts.high_similarity_pending, 0);
  for (const row of selected) {
    assert.ok(row.source_refs.length);
    assert.ok(row.source_refs.every((ref) => pool.sources.some((source) => source.id === ref.source_id)));
    assert.equal(row.production_ready, false);
    assert.equal(row.eligible, true);
  }
});

test('immutable third revision preserves 2328 selections and all previous raw records', () => {
  const baseline = readBaseline(ROOT, 'checkpoint-2328.json');
  assert.equal(baseline.pool.revision, '2026-11-01-pool-2328');
  assert.equal(baseline.pool.raw_records.length, 2661);
  assert.equal(baseline.pool.counts.selected_candidates, 2328);
  assert.equal(baseline.themes.episodes.length, 38);
  assert.deepEqual(compareBaseline(readBaseline(ROOT, 'checkpoint-2000.json'), baseline.pool).changed_baseline_raw_ids, []);
  assert.equal(baseline.pool.dedup.aliases.L042, 'L041');
});

test('immutable fourth revision preserves 2449 selections, source aliases and timed themes', () => {
  const baseline = readBaseline(ROOT, 'checkpoint-2449.json');
  assert.equal(baseline.pool.revision, '2026-11-01-pool-2449');
  assert.equal(baseline.pool.raw_records.length, 2790);
  assert.equal(baseline.pool.counts.selected_candidates, 2449);
  assert.equal(baseline.themes.episodes.length, 48);
  assert.deepEqual(compareBaseline(readBaseline(ROOT, 'checkpoint-2328.json'), baseline.pool).changed_baseline_raw_ids, []);
  assert.equal(baseline.pool.dedup.aliases.F4018, 'D2025');
  assert.equal(baseline.themes.episodes.find((episode) => episode.id === 'G37').body_seconds, 220);
});

test('immutable sixth revision preserves 2609 topics and the shortened lossless treatment', () => {
  const baseline = readBaseline(ROOT, 'checkpoint-2609.json');
  assert.equal(baseline.pool.raw_records.length, 2959);
  assert.equal(baseline.pool.counts.selected_candidates, 2609);
  assert.equal(baseline.themes.episodes.length, 69);
  assert.deepEqual(compareBaseline(readBaseline(ROOT, 'checkpoint-2546.json'), baseline.pool).changed_baseline_raw_ids, []);
  const lossless = baseline.themes.episodes.find((episode) => episode.id === 'G59');
  assert.equal(lossless.body_seconds, 140);
  assert.deepEqual(lossless.candidate_ids, ['M5004', 'M5009']);
  assert.equal(baseline.pool.candidates.find((row) => row.id === 'J6016').selected, false);
});

test('immutable fifth revision preserves 2546 selected topics and canonical audio variants', () => {
  const baseline = readBaseline(ROOT, 'checkpoint-2546.json');
  assert.equal(baseline.pool.raw_records.length, 2895);
  assert.equal(baseline.pool.counts.selected_candidates, 2546);
  assert.equal(baseline.themes.episodes.length, 60);
  assert.deepEqual(compareBaseline(readBaseline(ROOT, 'checkpoint-2449.json'), baseline.pool).changed_baseline_raw_ids, []);
  assert.equal(baseline.pool.dedup.aliases.M5008, 'M5004');
  assert.equal(baseline.pool.dedup.aliases.M5012, 'I3036');
  assert.equal(baseline.themes.episodes.find((episode) => episode.id === 'G60').body_seconds, 135);
});

test('current expansion preserves all checkpoints and requires usable editorial fields on new records', () => {
  const pool = readPool();
  const previous = readBaseline(ROOT, 'checkpoint-2000.json');
  assert.deepEqual(validateBaseline(readBaseline(), pool).changed_baseline_raw_ids, []);
  for (const checkpoint of validateCheckpoints(pool)) assert.deepEqual(checkpoint.changed_baseline_raw_ids, []);
  const oldIds = new Set(previous.pool.raw_records.map((row) => row.id));
  const added = pool.raw_records.filter((row) => !oldIds.has(row.id));
  assert.ok(added.length > 0);
  for (const row of added) validateEditorial(row);
  assert.ok(pool.counts.selected_candidates > 2000);
  assert.equal(new Set(pool.candidates.filter((row) => row.selected).map((row) => row.id)).size, pool.counts.selected_candidates);
  assert.equal(pool.counts.high_similarity_pending, 0);
});

test('missing required checkpoint metadata and an empty registry cannot disable historical protection', () => {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'stw-checkpoint-test-'));
  const dir = path.join(root, DIR);
  fs.mkdirSync(dir, { recursive: true });
  const registry = path.join(dir, 'checkpoints.json');
  try {
    assert.throws(() => validateCheckpoints({}, root), /ENOENT/);
    fs.writeFileSync(registry, JSON.stringify({ checkpoints: ['checkpoint-2000.json'], editorial_baseline: 'checkpoint-2000.json' }));
    assert.throws(() => validateCheckpoints({}, root), /ENOENT/);
    fs.writeFileSync(registry, JSON.stringify({ checkpoints: [], editorial_baseline: 'checkpoint-2000.json' }));
    assert.throws(() => validateCheckpoints({}, root), /Invalid required checkpoint/);
    fs.writeFileSync(registry, JSON.stringify({ checkpoints: ['../checkpoint-2000.json'], editorial_baseline: '../checkpoint-2000.json' }));
    assert.throws(() => validateCheckpoints({}, root), /Invalid required checkpoint/);
  } finally { fs.rmSync(root, { recursive: true, force: true }); }
});

test('new questions cannot omit payoff, visual or plausible segment duration', () => {
  const row = { id: 'new' };
  assert.throws(() => validateEditorial(row), /invalid editorial/);
  assert.doesNotThrow(() => validateEditorial(row, { required: false }));
  const editorial = { role: 'segment', payoff: 'new causal understanding', visual: 'one changing condition', seconds: [30, 75] };
  assert.doesNotThrow(() => validateEditorial({ ...row, editorial }));
  for (const override of [{ payoff: '' }, { payoff: 1 }, { visual: ' ' }, { seconds: [80, 40] }, { seconds: [0, 40] }, { seconds: [30, 601] }, { role: 'finished_film' }]) {
    assert.throws(() => validateEditorial({ ...row, editorial: { ...editorial, ...override } }), /invalid/);
  }
});

test('source changes identify canonical candidates and dependent themes without losing aliases', () => {
  const rows = [record('a', '測試的原始核心'), record('b', '另一個來源的別名', '完全另一份研究摘要')];
  const decisions = { ...empty(), merges: [{ duplicate_id: 'b', canonical_id: 'a', reason: 'Reviewed same core' }] };
  const pool = assemble(input(rows), decisions, choose(['a']));
  const themes = { episodes: [{ id: 'theme1', candidate_ids: ['a'] }, { id: 'theme2', candidate_ids: ['x'] }] };
  const report = sourceImpact(pool, themes, 'https://example.org/b?utm_source=discard#section');
  assert.deepEqual(report.candidates.map((row) => row.id), ['a']);
  assert.deepEqual(report.candidates[0].aliases, ['b']);
  assert.deepEqual(report.theme_ids, ['theme1']);
  assert.equal(report.production_ready, false);
  assert.throws(() => sourceImpact(pool, themes, 'https://example.org/missing'), /Unknown source/);
  const next = structuredClone(pool);
  next.sources[1].readings[0].reading_scope = 'New supported scope';
  next.raw_records[0].question = 'Edited old input';
  const changes = compareBaseline({ pool }, next);
  assert.deepEqual(changes.changed_source_record_ids, ['b']);
  assert.deepEqual(changes.changed_baseline_raw_ids, ['a']);
  assert.throws(() => validateBaseline({ pool }, next), /Baseline raw records changed/);
  const retired = structuredClone(pool);
  retired.candidates[0].selected = false;
  assert.throws(() => validateBaseline({ pool }, retired), /Missing baseline disposition/);
  retired.selection.baseline_changes = [{ id: 'a', reason: 'Explicit retirement with old rows retained' }];
  assert.deepEqual(validateBaseline({ pool }, retired).removed_or_merged_baseline_ids, ['a']);
});

test('same source and locator read in different batches retain both origins after merge', () => {
  const rows = [record('a', '同一核心問題'), record('b', '同一核心問題？')];
  rows[0].source_refs = [{ source_id: 'shared', locator: 'section1', origin: 'first-wave' }];
  rows[1].source_refs = [{ source_id: 'shared', locator: 'section1', origin: 'second-wave' }];
  const pool = assemble({ records: rows, sources: [source('shared')], inputs: [] }, empty(), choose(['a']));
  assert.deepEqual(pool.candidates[0].source_refs.map((ref) => ref.origin), ['first-wave', 'second-wave']);
});

test('themes cannot reference excluded records or masquerade as approved scripts; HTML contains inert escaped data', () => {
  const pool = assemble(input([record('a', '</script><script>alert(1)</script>')]), empty(), choose(['a']));
  const theme = { id: 'G01', title: 'fixture', core_question: 'fixture', connection: 'fixture', boredom_risk: 'fixture', drop_if: 'fixture', evidence_gaps: 'fixture', production_ready: false, status: 'EDITORIAL_THEME_NOT_SCRIPT', candidate_ids: ['a'], target_minutes: 10, range_minutes: [9, 11], chapters: Array.from({ length: 4 }, () => ({ title: 'fixture', new_information: 'fixture', candidate_ids: ['a'], seconds: 150 })) };
  validateThemes({ episodes: [theme] }, pool);
  assert.ok(!renderHtml(pool, { episodes: [theme] }).includes('</script><script>alert(1)</script>'));
  assert.throws(() => validateThemes({ episodes: [{ ...theme, candidate_ids: ['missing'] }] }, pool), /unselected/);
  assert.throws(() => validateThemes({ episodes: [{ ...theme, production_ready: true }] }, pool), /approval/);
  const short = { ...theme, format: 'short_explainer', target_minutes: 2, range_minutes: [1.5, 3], chapters: [{ title: 'observable comparison', new_information: 'hold the input fixed and change one condition', candidate_ids: ['a'], seconds: 45 }, { title: 'explanation and boundary', new_information: 'explain the changed outcome and where it stops applying', candidate_ids: ['a'], seconds: 75 }] };
  assert.doesNotThrow(() => validateThemes({ episodes: [short] }, pool));
  assert.throws(() => validateThemes({ episodes: [{ ...short, format: undefined }] }, pool), /every chapter/);
  assert.throws(() => validateThemes({ episodes: [{ ...short, chapters: [short.chapters[0]] }] }, pool), /every chapter/);
  assert.throws(() => validateThemes({ episodes: [{ ...short, target_minutes: 3 }] }, pool), /time budget/);
  const fractionalMinutes = { ...short, target_minutes: 250 / 60, range_minutes: [4, 5], chapters: short.chapters.map(chapter => ({ ...chapter, seconds: 125 })) };
  assert.doesNotThrow(() => validateThemes({ episodes: [fractionalMinutes] }, pool));
  assert.throws(() => validateThemes({ episodes: [{ ...fractionalMinutes, target_minutes: 251 / 60 }] }, pool), /time budget/);
});
