import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { ROOT, DIR, hash, intake, assemble, loadDraft, buildPool, urlsIn, normalizeUrl, linkStatuses, validateEditorial } from './core.mjs';
import { validateThemes, renderHtml, renderDedup } from './render.mjs';
import { writeBaseline, readBaseline, validateBaseline } from './history.mjs';
import { openStore, ingest, search, lookup } from './store.mjs';

const BANK = 'docs/videos/history-curiosity';
const write = (root, file, value) => {
  fs.mkdirSync(path.dirname(path.join(root, file)), { recursive: true });
  fs.writeFileSync(path.join(root, file), typeof value === 'string' ? value : `${JSON.stringify(value, null, 2)}\n`);
};
const topic = (id, title, status = 'candidate', extra = {}) => ({ id, axis: id[0], title, hook: `${title} 的鉤子`, finding: `${title} 的紀錄`, key_visuals: [], photo_candidates: [], facts_to_verify: ['年份'], risk: 'none', status, ...extra });
const source = (id, url) => ({ id, url, title: `頁面 ${id}`, publisher: '機構', accessed_on: '2026-11-01', read_via: 'direct_fetch', reading_scope: '第一段', locator: '第一段', summary: '支持前提', rights: 'LINK_AND_ORIGINAL_SUMMARY_ONLY' });
const candidate = (id, question, extra = {}) => ({ id, axis: 'H', question, hook: '鉤子', case_key: `case.${id.toLowerCase()}`, answer_target: `${question} 的紀錄答案`, scope: '範圍', source_ids: ['S1', 'S2'], source_locator: 'S1 第一段；S2 第二段', premise_status: 'screened', editorial: { role: 'episode_core', payoff: '多懂一件事', visual: '一張地圖', minutes: [8, 11] }, ...extra });

function fixture({ topics = [], fg = [], batch = null, decisions = null, selection = null, checks = {}, episodes = {} } = {}) {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'curio-pool-'));
  write(root, `${BANK}/topics.json`, { schema_version: 1, series: { axes: { H: '歷史懸案', M: '奇異現象與科學', L: '都市傳說與民俗' } }, topics });
  write(root, `${BANK}/topics-fg.json`, { schema_version: 1, series: { axes: { F: '童話原版', G: '靈異事件' } }, topics: fg });
  for (const [id, text] of Object.entries(checks)) write(root, `${BANK}/topic-checks/${id}.md`, text);
  for (const [slug, files] of Object.entries(episodes)) for (const [name, value] of Object.entries(files)) write(root, `docs/videos/${slug}/${name}`, value);
  if (batch) write(root, `${DIR}/batches/wave1.json`, batch);
  if (decisions) write(root, `${DIR}/dedup-decisions.json`, decisions);
  if (selection) write(root, `${DIR}/selection.json`, selection);
  return root;
}
const checkFile = (urls, status = {}) => `# 查核\n\n## 逐項查核\n\n| # | 主張 | 來源 |\n|---|---|---|\n| 1 | 一 | ${urls.join('<br>')} |\n\n## 連結檢查\n\n| 網址 | 狀態 |\n|---|---|\n${urls.map((url) => `| ${url} | ${status[url] ?? '200'} |`).join('\n')}\n\n## 獨立覆核\n\n完成。\n`;
const theme = (id, ids, minutes = 10, extra = {}) => {
  const total = minutes * 60;
  const per = Math.floor(total / 4);
  const chapters = [0, 1, 2, 3].map((i) => ({ title: `章 ${i + 1}`, seconds: i === 3 ? total - per * 3 : per, new_information: `新理解 ${i + 1}`, candidate_ids: [ids[i % ids.length]] }));
  return { id, title: `題案 ${id}`, core_question: '追問', connection: '同一個核心', boredom_risk: '重複', drop_if: '撤案', evidence_gaps: '待補', status: 'EDITORIAL_THEME_NOT_SCRIPT', production_ready: false, target_minutes: minutes, range_minutes: [8, 13], candidate_ids: ids, chapters, ...extra };
};

test('topic-check files are read whole: every URL in a table cell is kept and non-200 link checks become limitations', () => {
  const urls = ['https://example.org/a', 'https://example.org/b', 'https://archive.example.net/c?utm_source=x'];
  const root = fixture({ topics: [topic('H02', '羅阿諾克殖民地', 'checked')], checks: { H02: checkFile(urls, { 'https://example.org/b': '403 Forbidden' }) } });
  const { records, sources } = intake(root);
  const row = records.find((record) => record.id === 'H02');
  assert.equal(new Set(row.source_refs.map((ref) => ref.source_id)).size, 3);
  assert.equal(row.premise_status, 'legacy_checked');
  assert.equal(row.eligible, true);
  const limited = sources.find((item) => item.url === 'https://example.org/b');
  assert.match(limited.readings[0].limitations, /403/);
  assert.ok(sources.some((item) => item.url === 'https://archive.example.net/c'), 'tracking parameters are stripped');
  assert.equal(linkStatuses(checkFile(urls)).size, 0);
});

test('unchecked topic cards without sources stay in reserve and cannot be selected', () => {
  const root = fixture({ topics: [topic('H30', '塞納河無名女子')], selection: { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 1, ids: ['H30'] } });
  const { draft } = loadDraft(root);
  assert.equal(draft.candidates[0].pool_status, 'reserve');
  assert.throws(() => buildPool(root), /eligible canonical core/);
});

test('produced episodes are locked: they can absorb a duplicate but cannot be merged away or dropped', () => {
  const episodes = { 'curio-h01': { 'video.json': { youtube: { title: '瑪麗賽勒斯特號｜奇聞檔案局' } }, 'research.md': '來源 https://example.org/celeste' } };
  const topics = [topic('H01', '瑪麗賽勒斯特號', 'scripted'), topic('L99', '瑪麗賽勒斯特號的另一種講法')];
  const merged = assemble(intake(fixture({ topics, episodes })), { merges: [{ duplicate_id: 'L99', canonical_id: 'H01', reason: '同一艘船、同一個答案' }] });
  const row = merged.candidates.find((item) => item.id === 'H01');
  assert.equal(row.pool_status, 'produced');
  assert.deepEqual(row.aliases, ['L99']);
  assert.ok(row.source_refs.some((ref) => ref.locator === 'docs/videos/curio-h01/research.md'));
  const input = intake(fixture({ topics, episodes }));
  assert.throws(() => assemble(input, { merges: [{ duplicate_id: 'H01', canonical_id: 'L99', reason: 'x' }] }), /cannot be merged away/);
  assert.throws(() => assemble(input, { dispositions: [{ id: 'H01', disposition: 'drop', reason: '太薄', reentry: '不重提' }] }), /cannot be dropped/);
});

test('episodes outside the bank (branch drafts, W axis) are registered as locked dedup targets', () => {
  const root = fixture({ topics: [topic('H01', '一艘船')] });
  write(root, `${DIR}/legacy/branch-episodes.json`, { episodes: [{ id: 'S49', slug: 'curio-s49', branch: 'codex/x', commit: 'abcdef0123456789', title: '1835 年月球騙局', heading: '', question: '', urls: [{ url: 'https://example.org/moon', file: 'docs/videos/curio-s49/research.md' }] }] });
  write(root, `${DIR}/legacy/w-axis.json`, { episodes: [{ id: 'W01', question: '杜比的授權費', locator: 'docs/videos/x.md' }] });
  const { records } = intake(root);
  const s49 = records.find((record) => record.id === 'S49');
  assert.equal(s49.locked, true);
  assert.match(s49.source_refs[0].locator, /^codex\/x@abcdef01:/);
  assert.equal(records.find((record) => record.id === 'W01').locked, true);
});

test('dispositions need reasons: a drop states how it may come back, a transfer names where it goes', () => {
  const input = intake(fixture({ topics: [topic('M02', '金戒指'), topic('L22', '掉落熊'), topic('M30', '石化鳥')] }));
  assert.throws(() => assemble(input, { dispositions: [{ id: 'L22', disposition: 'drop', reason: '玩笑' }] }), /re-entry/);
  assert.throws(() => assemble(input, { dispositions: [{ id: 'M02', disposition: 'transfer', reason: '科普' }] }), /destination/);
  assert.throws(() => assemble(input, { dispositions: [{ id: 'M30', disposition: 'shorts' }] }), /reason/);
  const pool = assemble(input, { dispositions: [{ id: 'L22', disposition: 'drop', reason: '玩笑', reentry: '找到起源' }, { id: 'M02', disposition: 'transfer', transfer_to: '原來如此事務所', reason: '科普' }, { id: 'M30', disposition: 'shorts', reason: '一句答完' }] });
  assert.deepEqual(['L22', 'M02', 'M30'].map((id) => pool.candidates.find((row) => row.id === id).pool_status), ['excluded', 'excluded', 'shorts']);
  assert.match(renderDedup(pool), /找到起源/);
});

test('a merged alias keeps its own id and sources, and only exact wording merges automatically', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '為什麼 1962 年三個人逃出惡魔島？'), candidate('N102', '為什麼1962年三個人逃出惡魔島'), candidate('N103', '惡魔島越獄的人去了哪裡？')] };
  const input = intake(fixture({ batch }));
  const pool = assemble(input, { merges: [{ duplicate_id: 'N103', canonical_id: 'N101', reason: '同一次越獄、同一個答案' }] });
  const row = pool.candidates.find((item) => item.id === 'N101');
  assert.deepEqual(row.aliases.sort(), ['N102', 'N103']);
  assert.equal(pool.dedup.merges.find((item) => item.duplicate_id === 'N102').kind, 'exact_question');
  assert.equal(pool.raw_records.length, 3, 'raw records are never deleted');
});

test('the same case key must be merged or declared distinct before a selection can be built', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '橡樹島錢坑從哪年開始挖？', { case_key: 'case.oak_island' }), candidate('N102', '加拿大一座小島的寶藏', { case_key: 'case.oak_island' })] };
  const selection = { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 2, ids: ['N101', 'N102'] };
  assert.throws(() => buildPool(fixture({ batch, selection })), /high-similarity pairs/);
  const pool = buildPool(fixture({ batch, selection, decisions: { distinct: [{ a: 'N101', b: 'N102', reason: '一個問起源、一個問寶藏' }] } }));
  assert.equal(pool.counts.selected_candidates, 2);
  assert.equal(pool.counts.high_similarity_pending, 0);
});

test('screening research attaches sources to an unchecked topic card without losing the card text', () => {
  const batch = { batch_id: 'legacy1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [], legacy_updates: [{ id: 'H30', question: '修正後的題目？', answer_target: '查到的紀錄', scope: '不主張的事', source_ids: ['S1', 'S2'], source_locator: 'S1 第一段', premise_status: 'screened', editorial: { role: 'episode_core', payoff: 'a', visual: 'b', minutes: [8, 10] } }] };
  const root = fixture({ topics: [topic('H30', '塞納河無名女子'), topic('H01', '一艘船', 'scripted')], batch, episodes: { 'curio-h01': { 'video.json': { title: '一艘船' } } } });
  const { records } = intake(root);
  const row = records.find((record) => record.id === 'H30');
  assert.equal(row.card_question, '塞納河無名女子');
  assert.equal(row.question, '修正後的題目？');
  assert.equal(row.eligible, true);
  assert.equal(new Set(row.source_refs.map((ref) => ref.source_id)).size, 2);
  write(root, `${DIR}/batches/wave1.json`, { ...batch, legacy_updates: [{ ...batch.legacy_updates[0], id: 'H01' }] });
  assert.throws(() => intake(root), /produced topics are researched in their episode folder/);
});

test('a recheck in a later batch adds sources to a held topic and keeps the card text', () => {
  const update = { id: 'H30', question: '修正後的題目？', answer_target: '查到的紀錄', scope: '範圍', source_ids: ['S1'], source_locator: 'S1', premise_status: 'needs_check', editorial: { role: 'episode_core', payoff: 'a', visual: 'b', minutes: [8, 10] } };
  const wave2 = { batch_id: 'wave2', sources: [source('S1', 'https://example.org/one')], candidates: [], legacy_updates: [update] };
  const wave3 = { batch_id: 'wave3', sources: [source('S9', 'https://example.org/nine')], candidates: [], rechecks: [{ id: 'H30', of_batch: 'wave2', source_ids: ['S9'], source_locator: 'S9 第三頁', premise_status: 'screened', fields: { answer_target: '補到一手來源後的紀錄' } }] };
  const root = fixture({ topics: [topic('H30', '塞納河無名女子'), topic('H01', '一艘船', 'scripted')], episodes: { 'curio-h01': { 'video.json': { title: '一艘船' } } } });
  write(root, `${DIR}/batches/wave2.json`, wave2);
  write(root, `${DIR}/batches/wave3.json`, wave3);
  const row = intake(root).records.find((record) => record.id === 'H30');
  assert.equal(row.eligible, true);
  assert.equal(row.rechecked_in, 'wave3');
  assert.equal(row.card_question, '塞納河無名女子');
  assert.equal(row.question, '修正後的題目？');
  assert.equal(row.answer_target, '補到一手來源後的紀錄');
  assert.equal(new Set(row.source_refs.map((ref) => ref.source_id)).size, 2);
  write(root, `${DIR}/batches/wave3.json`, { ...wave3, rechecks: [{ ...wave3.rechecks[0], of_batch: 'wave9' }] });
  assert.throws(() => intake(root), /recheck names wave9/);
  write(root, `${DIR}/batches/wave3.json`, { ...wave3, rechecks: [{ ...wave3.rechecks[0], fields: { answer_target: '把『X』改成『Y』' } }] });
  assert.throws(() => intake(root), /edit instruction/);
  write(root, `${DIR}/batches/wave3.json`, { ...wave3, rechecks: [{ ...wave3.rechecks[0], id: 'H01' }] });
  assert.throws(() => intake(root), /produced topics/);
});

test('eligible cores must be either selected or held with a reason', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '費斯托斯圓盤是誰做的？'), candidate('N102', '比爾密碼的寶藏在哪？')] };
  assert.throws(() => buildPool(fixture({ batch, selection: { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 1, ids: ['N101'] } })), /neither selected nor held/);
  const pool = buildPool(fixture({ batch, selection: { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 1, ids: ['N101'], held: [{ id: 'N102', reason: '只有一個可讀來源' }] } }));
  assert.equal(pool.candidates.find((row) => row.id === 'N102').exclusion_reason, '只有一個可讀來源');
});

test('cross-series duplicates against the so-thats-why pool block selection until decided', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '黃金的來歷，為什麼會追到兩顆死去恆星的相撞？')] };
  const root = fixture({ batch, selection: { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 1, ids: ['N101'] } });
  write(root, `${DIR}/external/so-thats-why-cores.json`, { series: '原來如此事務所', commit: 'c'.repeat(40), pool_revision: 'p', cores: [{ id: 'X2020', question: '黃金的來歷，為什麼會追到兩顆死去恆星的相撞？' }] });
  assert.throws(() => buildPool(root), /cross-series/);
  write(root, `${DIR}/dedup-decisions.json`, { cross_series: [{ id: 'N101', external_id: 'X2020', decision: 'transfer', reason: '同一題' }] });
  assert.throws(() => buildPool(root), /transfer disposition/);
});

test('editorial estimates are honest: an episode core must reach 8 minutes, otherwise it is a chapter', () => {
  assert.throws(() => validateEditorial({ id: 'N1', editorial: { role: 'episode_core', payoff: 'a', visual: 'b', minutes: [3, 5] } }), /mark it a chapter/);
  assert.throws(() => validateEditorial({ id: 'N1', editorial: { role: 'chapter', payoff: 'a', visual: 'b', minutes: [3, 15] } }), /within/);
  validateEditorial({ id: 'N1', editorial: { role: 'chapter', payoff: 'a', visual: 'b', minutes: [2, 4] } });
});

test('themes are 8–13 minutes, add up exactly, use each core once and never plan produced or thin-alone cores', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '貝奇莫號為什麼漂了幾十年？'), candidate('N102', 'Carroll Deering 號的船員去哪了？', { editorial: { role: 'chapter', payoff: 'a', visual: 'b', minutes: [3, 5] } })] };
  const episodes = { 'curio-h01': { 'video.json': { title: '一艘船' } } };
  const pool = buildPool(fixture({ topics: [topic('H01', '一艘船', 'scripted')], batch, episodes, selection: { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 2, ids: ['N101', 'N102'] } }));
  const ok = { episodes: [theme('T01', ['N101', 'N102'], 10)] };
  assert.equal(validateThemes(ok, pool), ok);
  assert.throws(() => validateThemes({ episodes: [theme('T01', ['N101'], 10)] }, pool), /N102.*cannot stand alone/);
  assert.throws(() => validateThemes({ episodes: [theme('T01', ['N101', 'N102'], 7, { range_minutes: [7, 9] })] }, pool), /8–13 minutes/);
  assert.throws(() => validateThemes({ episodes: [theme('T01', ['N101', 'N102'], 14, { range_minutes: [12, 14] })] }, pool), /8–13 minutes/);
  const off = theme('T01', ['N101', 'N102'], 10); off.chapters[0].seconds += 5;
  assert.throws(() => validateThemes({ episodes: [off] }, pool), /add up to the target exactly/);
  const short = theme('T01', ['N101', 'N102'], 10); short.chapters[0].seconds -= 140; short.chapters[1].seconds += 140;
  assert.throws(() => validateThemes({ episodes: [short] }, pool), /≥30 s/);
  assert.throws(() => validateThemes({ episodes: [theme('T01', ['N101', 'N102'], 10), theme('T02', ['N101'], 10)] }, pool), /one core feeds one episode/);
  assert.throws(() => validateThemes({ episodes: [theme('T01', ['N101', 'H01'], 10)] }, pool), /produced/);
  assert.throws(() => validateThemes({ episodes: [{ ...theme('T01', ['N101', 'N102'], 10), production_ready: true }] }, pool), /production approval/);
});

test('URL parsing keeps balanced parentheses, stops at CJK text and table pipes, and rejects private hosts', () => {
  assert.deepEqual(urlsIn('見 https://en.wikipedia.org/wiki/Oak_Island_(Nova_Scotia)。以及 https://example.org/a|b'), ['https://en.wikipedia.org/wiki/Oak_Island_(Nova_Scotia)', 'https://example.org/a']);
  assert.deepEqual(urlsIn('https://example.org/x<br>https://example.org/y'), ['https://example.org/x', 'https://example.org/y']);
  assert.throws(() => normalizeUrl('http://127.0.0.1/admin'), /public/);
  assert.throws(() => normalizeUrl('ftp://example.org/a'), /public/);
  assert.equal(normalizeUrl('https://example.org/a?gclid=1&q=2#frag'), 'https://example.org/a?q=2');
});

test('baseline snapshots: a changed raw record must be declared with a reason', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '費斯托斯圓盤是誰做的？')] };
  const root = fixture({ batch, selection: { revision: 'r1', reviewed_on: '2026-11-01', reason: 'test', target_count: 1, ids: ['N101'] } });
  const pool = buildPool(root);
  writeBaseline(root, pool, { episodes: [] }, 'test-1');
  assert.ok(validateBaseline(readBaseline(root), pool));
  const changed = { ...batch, candidates: [{ ...batch.candidates[0], answer_target: '改過的答案' }] };
  write(root, `${DIR}/batches/wave1.json`, changed);
  write(root, `${DIR}/selection.json`, { revision: 'r2', reviewed_on: '2026-11-02', reason: 'test', target_count: 1, ids: ['N101'] });
  assert.throws(() => validateBaseline(readBaseline(root), buildPool(root)), /declare why/);
  write(root, `${DIR}/selection.json`, { revision: 'r2', reviewed_on: '2026-11-02', reason: 'test', target_count: 1, ids: ['N101'], raw_changes: [{ id: 'N101', reason: '覆核改了答案' }] });
  assert.ok(validateBaseline(readBaseline(root), buildPool(root)));
});

test('the SQLite index is idempotent and resolves aliases to their canonical core', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '水晶頭骨是古代的嗎？'), candidate('N102', '大英博物館的水晶頭骨')] };
  const pool = buildPool(fixture({ batch, decisions: { merges: [{ duplicate_id: 'N102', canonical_id: 'N101', reason: '同一批頭骨、同一個工具痕跡答案' }] }, selection: { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 1, ids: ['N101'] } }));
  const db = openStore(':memory:');
  assert.equal(ingest(db, pool).status, 'IMPORTED');
  assert.deepEqual(ingest(db, pool), { status: 'UNCHANGED', snapshot: hash(JSON.stringify(pool)), writes: 0 });
  assert.equal(search(db, '水晶頭骨')[0].id, 'N101');
  assert.equal(lookup(db, 'N102').candidate.id, 'N101');
  db.close();
});

test('the page escapes embedded text so a title cannot close the data script', () => {
  const batch = { batch_id: 'wave1', sources: [source('S1', 'https://example.org/one'), source('S2', 'https://example.org/two')], candidates: [candidate('N101', '</script><script>alert(1)</script>？')] };
  const pool = buildPool(fixture({ batch, selection: { revision: 'r', reviewed_on: '2026-11-01', reason: 'test', target_count: 1, ids: ['N101'] } }));
  const html = renderHtml(pool, { episodes: [] });
  assert.equal(html.match(/<\/script>/g).length, 2);
});

test('the committed pool export is internally consistent', { skip: !fs.existsSync(path.join(ROOT, DIR, 'manifest.json')) }, () => {
  // Hash checks only: the full rebuild (`cli.mjs check`) depends on topics.json, which other tasks edit.
  const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, DIR, 'manifest.json'), 'utf8'));
  for (const entry of manifest.files) assert.equal(hash(fs.readFileSync(path.join(ROOT, DIR, entry.file))), entry.sha256, entry.file);
  const pool = JSON.parse(fs.readFileSync(path.join(ROOT, DIR, 'pool.json'), 'utf8'));
  assert.equal(pool.counts.high_similarity_pending, 0);
  assert.equal(pool.counts.cross_series_pending, 0);
  assert.equal(pool.counts.approved_scripts, 0);
  assert.equal(pool.candidates.filter((row) => row.selected).length, pool.counts.selected_candidates);
  assert.ok(pool.candidates.every((row) => row.production_ready === false));
  const themes = JSON.parse(fs.readFileSync(path.join(ROOT, DIR, 'themes.json'), 'utf8'));
  assert.equal(hash(fs.readFileSync(path.join(ROOT, DIR, 'themes.json'))), manifest.theme_definition_sha256);
  validateThemes(themes, pool);
});
