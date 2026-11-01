import assert from 'node:assert/strict';
import test from 'node:test';
import { assemble, normalizeUrl, urlsIn, readPool, similarityPairs } from './core.mjs';
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

test('checked-in pool is exactly the reviewed 1000 canonical candidates with source links', () => {
  const pool = readPool();
  const selected = pool.candidates.filter((row) => row.selected);
  assert.equal(selected.length, 1000);
  assert.equal(new Set(selected.map((row) => row.id)).size, 1000);
  assert.equal(pool.counts.historical_records, 313);
  assert.equal(pool.counts.high_similarity_pending, 0);
  for (const row of selected) {
    assert.ok(row.source_refs.length);
    assert.ok(row.source_refs.every((ref) => pool.sources.some((source) => source.id === ref.source_id)));
    assert.equal(row.production_ready, false);
    assert.equal(row.eligible, true);
  }
});

test('themes cannot reference excluded records or masquerade as approved scripts; HTML contains inert escaped data', () => {
  const pool = assemble(input([record('a', '</script><script>alert(1)</script>')]), empty(), choose(['a']));
  const theme = { id: 'G01', title: 'fixture', core_question: 'fixture', connection: 'fixture', boredom_risk: 'fixture', drop_if: 'fixture', evidence_gaps: 'fixture', production_ready: false, status: 'EDITORIAL_THEME_NOT_SCRIPT', candidate_ids: ['a'], target_minutes: 10, range_minutes: [9, 11], chapters: Array.from({ length: 4 }, () => ({ title: 'fixture', new_information: 'fixture', candidate_ids: ['a'], seconds: 150 })) };
  validateThemes({ episodes: [theme] }, pool);
  assert.ok(!renderHtml(pool, { episodes: [theme] }).includes('</script><script>alert(1)</script>'));
  assert.throws(() => validateThemes({ episodes: [{ ...theme, candidate_ids: ['missing'] }] }, pool), /unselected/);
  assert.throws(() => validateThemes({ episodes: [{ ...theme, production_ready: true }] }, pool), /approval/);
});
