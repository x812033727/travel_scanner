import fs from 'node:fs';
import path from 'node:path';
import { gunzipSync } from 'node:zlib';
import { DIR, ROOT, hash, normalizeUrl, checkpointFiles } from './core.mjs';

export function readBaseline(root = ROOT, metadata = 'baseline.json') {
  if (!/^(baseline|checkpoint-\d+)\.json$/.test(metadata)) throw new Error('Invalid checkpoint metadata path');
  const meta = JSON.parse(fs.readFileSync(path.join(root, DIR, metadata), 'utf8'));
  if (!/^baselines\/[\w.-]+\.json\.gz$/.test(meta.file)) throw new Error('Invalid baseline path');
  const bytes = fs.readFileSync(path.join(root, DIR, meta.file));
  if (hash(bytes) !== meta.sha256) throw new Error('Baseline hash mismatch');
  const baseline = JSON.parse(gunzipSync(bytes).toString('utf8'));
  if (baseline.pool.revision !== meta.revision || baseline.pool.counts.selected_candidates !== meta.selected_count || baseline.pool.raw_records.length !== meta.raw_count) throw new Error('Baseline metadata mismatch');
  return { meta, ...baseline };
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
    note: 'Source record changes include additional readings; they do not prove the external page changed. Retained historical rows must not be silently rewritten.',
  };
}

export function validateBaseline(baseline, pool, declarations = pool.selection?.baseline_changes ?? []) {
  const changes = compareBaseline(baseline, pool);
  if (changes.changed_baseline_raw_ids.length) throw new Error('Baseline raw records changed; preserve old rows and add an explicit new revision instead');
  if (!Array.isArray(declarations) || new Set(declarations.map((item) => item.id)).size !== declarations.length) throw new Error('Invalid baseline change declarations');
  for (const id of changes.removed_or_merged_baseline_ids) {
    if (!declarations.some((item) => item.id === id && item.reason)) throw new Error(`Missing baseline disposition for ${id}`);
  }
  for (const item of declarations) if (!changes.removed_or_merged_baseline_ids.includes(item.id) || !item.reason) throw new Error(`Stale baseline disposition for ${item.id}`);
  return changes;
}

export function validateCheckpoints(pool, root = ROOT) {
  return checkpointFiles(root).checkpoints.map((file) => {
    const checkpoint = readBaseline(root, file);
    const declarations = pool.selection?.checkpoint_changes?.[checkpoint.pool.revision] ?? [];
    return validateBaseline(checkpoint, pool, declarations);
  });
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
    candidates: candidates.map((row) => ({ id: row.id, question: row.question, selected: row.selected, aliases: row.aliases, references: row.source_refs.filter((ref) => ref.source_id === source.id) })),
    theme_ids: themes.episodes.filter((theme) => theme.candidate_ids.some((id) => ids.has(id))).map((theme) => theme.id),
    action_on_change: 'Recheck the supported premise and dependent theme claims; update the reading record and editorial decisions before rebuilding. This command does not fetch or monitor external pages.',
    production_ready: false,
  };
}
