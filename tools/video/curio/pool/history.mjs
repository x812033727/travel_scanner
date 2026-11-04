// 奇聞檔案局素材池的快照與比對；照原來如此事務所素材池的 history.mjs。
// 差別：題庫（topics.json）會被別的票改（例如查核後改 checked），所以舊快照裡的原始紀錄可以變，
// 但每一筆變動都要在 selection.json 的 raw_changes 寫理由，不能默默改掉。
import fs from 'node:fs';
import path from 'node:path';
import { gzipSync, gunzipSync } from 'node:zlib';
import { DIR, ROOT, hash, normalizeUrl } from './core.mjs';

export function readBaseline(root = ROOT, metadata = 'baseline.json') {
  if (!/^(baseline|checkpoint-\d+)\.json$/.test(metadata)) throw new Error('Invalid checkpoint metadata path');
  const file = path.join(root, DIR, metadata);
  if (!fs.existsSync(file)) return null;
  const meta = JSON.parse(fs.readFileSync(file, 'utf8'));
  if (!/^baselines\/[\w.-]+\.json\.gz$/.test(meta.file)) throw new Error('Invalid baseline path');
  const bytes = fs.readFileSync(path.join(root, DIR, meta.file));
  if (hash(bytes) !== meta.sha256) throw new Error('Baseline hash mismatch');
  const baseline = JSON.parse(gunzipSync(bytes).toString('utf8'));
  if (baseline.pool.revision !== meta.revision || baseline.pool.counts.selected_candidates !== meta.selected_count || baseline.pool.raw_records.length !== meta.raw_count) throw new Error('Baseline metadata mismatch');
  return { meta, ...baseline };
}

export function writeBaseline(root, pool, themes, label) {
  if (pool.status !== 'CURATED_CANDIDATE_POOL_NOT_PRODUCTION') throw new Error('Only a reviewed pool can become a baseline');
  if (!/^[\w.-]+$/.test(label)) throw new Error('Invalid baseline label');
  const file = `baselines/${label}.json.gz`;
  const bytes = gzipSync(Buffer.from(JSON.stringify({ pool, themes })), { level: 9 });
  fs.mkdirSync(path.join(root, DIR, 'baselines'), { recursive: true });
  fs.writeFileSync(path.join(root, DIR, file), bytes);
  const meta = { file, sha256: hash(bytes), revision: pool.revision, selected_count: pool.counts.selected_candidates, raw_count: pool.raw_records.length };
  fs.writeFileSync(path.join(root, DIR, 'baseline.json'), `${JSON.stringify(meta, null, 2)}\n`);
  return meta;
}

export function compareBaseline(baseline, current) {
  const previous = baseline.pool;
  const raw = new Map(current.raw_records.map((row) => [row.id, row]));
  const changedRaw = previous.raw_records.filter((row) => !raw.has(row.id) || hash(JSON.stringify(row)) !== hash(JSON.stringify(raw.get(row.id)))).map((row) => row.id);
  const before = previous.candidates.filter((row) => row.selected).map((row) => row.id);
  const now = new Set(current.candidates.filter((row) => row.selected).map((row) => row.id));
  const carried = [...new Set(before.map((id) => current.dedup.aliases[id]).filter((id) => now.has(id)))];
  const sources = new Map(current.sources.map((row) => [row.id, row]));
  const changedSources = previous.sources.filter((row) => !sources.has(row.id) || hash(JSON.stringify(row)) !== hash(JSON.stringify(sources.get(row.id)))).map((row) => row.id);
  return {
    baseline_revision: previous.revision, current_revision: current.revision,
    baseline_selected: before.length, carried_distinct_cores: carried.length,
    added_selected_ids: [...now].filter((id) => !carried.includes(id)),
    removed_or_merged_baseline_ids: before.filter((id) => !now.has(id)),
    changed_baseline_raw_ids: changedRaw, changed_source_record_ids: changedSources,
    note: 'Source record changes include additional readings; they do not prove the external page changed.',
  };
}

export function validateBaseline(baseline, pool) {
  if (!baseline) return null;
  const changes = compareBaseline(baseline, pool);
  const declared = (list, what) => {
    if (!Array.isArray(list) || new Set(list.map((item) => item.id)).size !== list.length || list.some((item) => !item.id || !item.reason)) throw new Error(`Invalid ${what} declarations`);
    return new Set(list.map((item) => item.id));
  };
  // Declarations belong to the revision they explain; once a new baseline is written they are cleared.
  const sameRevision = baseline.pool.revision === pool.revision;
  const rawDeclared = declared(sameRevision ? [] : pool.selection?.raw_changes ?? [], 'raw change');
  const removedDeclared = declared(sameRevision ? [] : pool.selection?.baseline_changes ?? [], 'baseline change');
  for (const id of changes.changed_baseline_raw_ids) if (!rawDeclared.has(id)) throw new Error(`Raw record ${id} changed since the baseline; declare why in selection.raw_changes`);
  for (const id of changes.removed_or_merged_baseline_ids) if (!removedDeclared.has(id)) throw new Error(`Missing baseline disposition for ${id}`);
  for (const id of rawDeclared) if (!changes.changed_baseline_raw_ids.includes(id)) throw new Error(`Stale raw change declaration for ${id}`);
  for (const id of removedDeclared) if (!changes.removed_or_merged_baseline_ids.includes(id)) throw new Error(`Stale baseline disposition for ${id}`);
  return changes;
}

export function sourceImpact(pool, themes, value) {
  let source = pool.sources.find((row) => row.id === value);
  if (!source) {
    let url;
    try { url = normalizeUrl(value); } catch { throw new Error(`Unknown source ${value}`); }
    source = pool.sources.find((row) => row.url === url);
  }
  if (!source) throw new Error(`Unknown source ${value}`);
  const candidates = pool.candidates.filter((row) => row.source_refs.some((ref) => ref.source_id === source.id));
  const ids = new Set(candidates.map((row) => row.id));
  return {
    source,
    candidates: candidates.map((row) => ({ id: row.id, question: row.question, pool_status: row.pool_status, aliases: row.aliases, references: row.source_refs.filter((ref) => ref.source_id === source.id) })),
    theme_ids: themes.episodes.filter((theme) => theme.candidate_ids.some((id) => ids.has(id))).map((theme) => theme.id),
    action_on_change: 'Recheck the supported premise and dependent theme claims; update the reading record and editorial decisions before rebuilding. This command does not fetch or monitor external pages.',
    production_ready: false,
  };
}
