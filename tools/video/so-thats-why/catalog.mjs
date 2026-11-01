// Read-only editorial selector. Legacy reviewed packages and production are never mutated.
import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { decisions, firstBatch } from './editorial.mjs';

export const ROOT = fileURLToPath(new URL('../../../', import.meta.url));
export const BASE = 'docs/videos/so-thats-why';
export const DIRECTORY = `${BASE}/refresh-20261101`;
export const SOURCES = ['episodes.json', 'season2-topics.json', 'season3-topics.json'].map((name) => `${BASE}/${name}`);
export const LABELS = { retain: '保留', reframe: '換角度採用', add: '新增採用', shorts: '改短片', merge: '併題', transfer: '轉其他系列候選', hold: '暫緩', drop: '剔除' };
export const ACTIVE = new Set(['retain', 'reframe', 'add']);
const hash = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (root, file) => readFileSync(path.join(root, file));
const json = (root, file) => JSON.parse(read(root, file).toString('utf8'));

export const PROFILE = {
  name: '原來如此事務所', revision: '2026-11-01',
  target_minutes: 13, minimum_body_seconds: 480, minimum_final_seconds: 480,
  body_budget_seconds: 780, estimated_spoken_characters: [3300, 3500],
  opening_seconds: [30, 60], opening_teasers_max: 2, hook_gap_seconds: 45, minimum_loops: 11,
  format: 'drama', look: { preset: 'cute-cartoon' }, characters: [], visual: 'still',
  image_model: 'image-01', illustration_fraction_min: 0.7, consecutive_cards_max: 3,
  subtitles: { burn_in: true }, intro_at: 'after_first_chapter',
  music: { prompt: 'light, curious, playful, no vocals', gain_db: -20, duck_db: -10 },
  spec: `${DIRECTORY}/SPEC.md`, production_synced: false,
};

export function buildCatalog(root = ROOT) {
  const sourceFiles = [...SOURCES, `${DIRECTORY}/new-topics.json`, `${DIRECTORY}/SPEC.md`, 'tools/video/so-thats-why/editorial.mjs'];
  const sources = sourceFiles.map((file) => ({ file, sha256: hash(read(root, file)) }));
  const legacy = SOURCES.flatMap((file, index) => json(root, file).episodes.map((entry) => ({ file, season: index + 1, entry })));
  if (legacy.length !== 300 || new Set(legacy.map(({ entry }) => entry.id)).size !== 300) throw new Error('Expected 300 unique legacy topics');
  const byId = new Map(decisions.map((decision) => [decision.id, decision]));
  if (byId.size !== 300 || decisions.length !== 300 || legacy.some(({ entry }) => !byId.has(entry.id))) throw new Error('Every legacy id needs exactly one explicit editorial decision');
  const episodes = legacy.map(({ file, season, entry }) => {
    const decision = byId.get(entry.id);
    if (!Object.hasOwn(LABELS, decision.disposition) || decision.disposition === 'add' || !decision.reason) throw new Error(`${entry.id}: invalid decision`);
    if (entry.production?.status === 'not-adopted' && decision.disposition !== 'drop') throw new Error(`${entry.id}: a historical rejected duplicate cannot be revived`);
    const refs = [entry.fact_check, entry.check, entry.production?.package].filter(Boolean).map((ref) => `${BASE}/${ref}`);
    const referenceHashes = refs.map((ref) => ({ file: ref, sha256: hash(read(root, ref)) }));
    return {
      id: entry.id, season, pillar: entry.pillar, original_title: entry.title,
      title: decision.title ?? entry.title, disposition: decision.disposition,
      active: ACTIVE.has(decision.disposition), reason: decision.reason, related: decision.related,
      source_file: file, source_record_sha256: hash(JSON.stringify(entry)), historical_status: entry.status,
      source_references: refs, source_reference_hashes: referenceHashes,
      verification: 'EDITORIAL_ONLY_LEGACY_FACTS_NOT_RECHECKED',
      production_ready: false,
    };
  });
  const additions = json(root, `${DIRECTORY}/new-topics.json`);
  for (const entry of additions.episodes) {
    if (episodes.some((old) => old.id === entry.id)) throw new Error(`${entry.id}: id reused`);
    if (!entry.sources?.length || entry.sources.some(({ url, supports }) => !url.startsWith('https://') || !supports) || entry.spine?.length < 3 || !entry.limits?.length || !entry.distinct_from) throw new Error(`${entry.id}: missing source, limits or story spine`);
    episodes.push({
      ...entry, season: null, original_title: null, disposition: 'add', active: true,
      reason: '獨立查核核心機制與舊題差異後新增；完整逐字稿另查核。', related: null,
      source_file: `${DIRECTORY}/new-topics.json`, source_record_sha256: hash(JSON.stringify(entry)),
      verification: additions.review_scope, checked_on: additions.checked_on, production_ready: false,
    });
  }
  for (const entry of episodes) {
    if (entry.disposition === 'merge' && !episodes.some((target) => target.id === entry.related && target.active)) throw new Error(`${entry.id}: merge target must remain active`);
  }
  if (firstBatch.length !== 24 || new Set(firstBatch).size !== 24 || firstBatch.some((id) => !episodes.some((entry) => entry.id === id && entry.active))) throw new Error('First batch needs 24 unique active topics');
  const counts = Object.fromEntries(Object.keys(LABELS).map((key) => [key, episodes.filter((entry) => entry.disposition === key).length]));
  return {
    schema_version: 1, edited_on: '2026-11-01', status: 'EDITORIAL_CATALOG_NOT_PRODUCTION',
    selection_scope: 'NEW_LONG_FORM_SELECTION_ONLY', profile: PROFILE, sources,
    counts: { original: 300, added: additions.episodes.length, active: episodes.filter((entry) => entry.active).length, ...counts },
    first_batch: firstBatch, episodes, new_topics_not_added: additions.not_added,
  };
}

export function readCatalog(root = ROOT) {
  const saved = json(root, `${DIRECTORY}/catalog.json`);
  const fresh = buildCatalog(root);
  if (JSON.stringify(saved) !== JSON.stringify(fresh)) throw new Error('Catalog drift: sources or editorial decisions changed; review them and rebuild before selection');
  if (read(root, `${DIRECTORY}/AUDIT.md`).toString('utf8') !== renderAudit(saved)) throw new Error('Audit drift: regenerate the review table from the reviewed catalog');
  if (read(root, `${DIRECTORY}/TOPICS.md`).toString('utf8') !== renderTopics(saved)) throw new Error('Topics drift: regenerate the active topic list from the reviewed catalog');
  return saved;
}

export function select(catalog, id, { activeOnly = false } = {}) {
  const entry = catalog.episodes.find((topic) => topic.id === id);
  if (!entry) throw new Error(`Unknown topic: ${id}`);
  if (activeOnly && !entry.active) throw new Error(`${id} is excluded from new long-form selection: ${LABELS[entry.disposition]} — ${entry.reason}`);
  return entry;
}

export function brief(catalog, id, root = ROOT) {
  const entry = select(catalog, id, { activeOnly: true });
  const original = json(root, entry.source_file).episodes.find((topic) => topic.id === id);
  return {
    status: 'EDITORIAL_BRIEF_NOT_IMPORT_READY', id, title: `${entry.title}｜原來如此事務所`,
    editorial_reason: entry.reason, current_profile: catalog.profile,
    causal_spine: entry.spine ?? null,
    needs: ['完整因果 treatment 與 11 個伏筆回收', '逐主張重新查核與獨立聽眾審稿', '確認現有影片／製作狀態後才決定是否新做', '媒體報價及實際製作驗收'],
    source_material: { warning: '歷史資料或選題級查核，並非當期逐字稿事實通過；不得直接當已核准輸入。', references: entry.source_references ?? entry.sources, record: original },
    merged_topics: catalog.episodes.filter((topic) => topic.disposition === 'merge' && topic.related === id).map((topic) => ({
      id: topic.id, title: topic.original_title, reason: topic.reason,
      use: '可選的短對照，需另查核；不能為塞題破壞主線，也不代表已合併成稿。',
      source_file: topic.source_file, references: topic.source_references,
      record: json(root, topic.source_file).episodes.find((source) => source.id === topic.id),
    })),
    chapter_budget_seconds: [45, 110, 140, 150, 150, 150, 35],
    notes: '使用 SPEC.md 五步開場，因果相接；舊稿、舊核准、舊翻譯不會自動適用新標題與規格。',
  };
}

export function renderAudit(catalog) {
  const cells = (text) => String(text ?? '—').replaceAll('|', '／').replaceAll('\n', ' ');
  const lines = ['# 300 個舊題的逐題取捨', '', '2026-11-01。這是編輯取捨，不是 300 題重新事實查核。移出本系列只影響新長片選擇；轉系列是候選建議，沒有自動匯入其他系列或撤下舊影片。', '', '| 題號 | 原題 | 決定 | 新題／理由 | 去向 |', '| --- | --- | --- | --- | --- |'];
  for (const e of catalog.episodes.filter((e) => e.season !== null)) lines.push(`| ${e.id} | ${cells(e.original_title)} | ${LABELS[e.disposition]} | ${e.title !== e.original_title ? `${cells(e.title)}<br>` : ''}${cells(e.reason)} | ${cells(e.related)} |`);
  return `${lines.join('\n')}\n`;
}

export function renderTopics(catalog) {
  const pillars = { science: '生活與自然科學', tech: '日用科技', travel: '交通、建築與城市', business: '價格、支付與制度' };
  const lines = ['# 原來如此事務所：100 個有效長片題目', '', '2026-11-01。87 個舊題重新切入、13 個新增；這是選題清單，尚非完整劇本、成片或排程。前 24 題的建議順序見 [總覽](README.md)，全部取捨理由見 [300 題處置表](AUDIT.md)。新題核心來源見 [新題資料](new-topics.json)。', ''];
  for (const [pillar, name] of Object.entries(pillars)) {
    const entries = catalog.episodes.filter((entry) => entry.active && entry.pillar === pillar);
    lines.push(`## ${name}（${entries.length} 題）`, '', '| 題號 | 題目 | 編輯優先序 |', '| --- | --- | --- |');
    for (const entry of entries) {
      const position = catalog.first_batch.indexOf(entry.id);
      lines.push(`| ${entry.id}${entry.disposition === 'add' ? ' 新' : ''} | ${entry.title} | ${position < 0 ? '後續題池' : `首批 ${position + 1}`} |`);
    }
    lines.push('');
  }
  return `${lines.join('\n').trimEnd()}\n`;
}
