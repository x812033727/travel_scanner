#!/usr/bin/env node
// 後台「題目池」分頁的資料包：從兩個素材池（奇聞檔案局、原來如此事務所）抽出題案、獨立觀眾評分與擴池紀錄，
// 寫成 API 映像裡的唯讀 JSON（apps/api/app/video_pools/data/pools.json）。API 看不到 docs/，所以由這裡打包；
// 兩池的 `cli.mjs build` 會自動重產，CI 用 `check` 確認資料包和池子一致（站主 2026-11-14）。
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { themeCategory as curioCategory, materialReady as curioReady, AUDIENCE_MIN } from '../curio/pool/render.mjs';
import { themeCategory as stwCategory } from '../so-thats-why/pool/render.mjs';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
export const OUTPUT = 'apps/api/app/video_pools/data/pools.json';
const LONG_MIN = 8;

export const SERIES = [
  { key: 'curio', name: '奇聞檔案局', dir: 'docs/videos/history-curiosity/pool', category: curioCategory, producible: (episode) => episode.target_minutes >= LONG_MIN && curioReady(episode) },
  { key: 'so-thats-why', name: '原來如此事務所', dir: 'docs/videos/so-thats-why/pool', category: stwCategory, producible: (episode) => episode.target_minutes >= LONG_MIN && episode.material?.verdict === 'ready' },
];

const sha256 = (bytes) => createHash('sha256').update(bytes).digest('hex');
const read = (root, file) => readFileSync(path.join(root, file));
const json = (root, file) => JSON.parse(read(root, file));

function audience(value) {
  if (!value) return null;
  const { score, rank, of, click, hook, surprise, payoff, share, comment, reviewed_on: reviewedOn } = value;
  return {
    score, rank, of, click, hook, surprise, payoff, share, comment, reviewed_on: reviewedOn,
    rounds: (value.rounds ?? []).map((round) => ({ score: round.score, comment: round.comment, changes: round.changes, reviewed_on: round.reviewed_on })),
  };
}

function seriesBundle(root, series) {
  const themesBytes = read(root, `${series.dir}/themes.json`);
  const manifestBytes = read(root, `${series.dir}/manifest.json`);
  const themes = JSON.parse(themesBytes).episodes;
  const manifest = JSON.parse(manifestBytes);
  const pool = json(root, `${series.dir}/pool.json`);
  const byId = new Map(pool.candidates.map((row) => [row.id, row]));
  // A batch record may have been merged into another core: count it as selected when its canonical core is.
  const selectedRaw = new Set(pool.candidates.filter((row) => row.selected).flatMap((row) => [row.id, ...(row.provenance_ids ?? []), ...(row.aliases ?? [])]));
  const rows = themes.map((episode) => {
    const long = episode.target_minutes >= LONG_MIN && episode.format !== 'short_explainer';
    return {
      id: episode.id,
      title: episode.title,
      category: series.category(episode, byId) || null,
      core_question: episode.core_question,
      target_minutes: episode.target_minutes,
      long,
      producible: long && series.producible(episode),
      material: episode.material ? { verdict: episode.material.verdict, missing: episode.material.missing ?? null } : null,
      candidates: episode.candidate_ids.length,
      audience: audience(episode.audience),
      chapters: episode.chapters.map((chapter) => ({ title: chapter.title, seconds: chapter.seconds, new_information: chapter.new_information })),
      boredom_risk: episode.boredom_risk,
      drop_if: episode.drop_if,
      evidence_gaps: episode.evidence_gaps,
    };
  });
  const batchDir = path.join(root, series.dir, 'batches');
  const expansions = readdirSync(batchDir).filter((name) => name.endsWith('.json')).sort().map((name) => {
    const batch = json(root, `${series.dir}/batches/${name}`);
    const candidates = batch.candidates ?? [];
    return {
      batch_id: batch.batch_id ?? name.replace(/\.json$/, ''),
      created_on: batch.created_on ?? null,
      scope: batch.scope ?? '',
      candidates: candidates.length,
      selected: candidates.filter((row) => selectedRaw.has(row.id)).length,
      not_added: (batch.not_added ?? []).length,
      sources: (batch.sources ?? []).length,
    };
  }).sort((a, b) => (a.created_on ?? '').localeCompare(b.created_on ?? '') || a.batch_id.localeCompare(b.batch_id, 'en', { numeric: true }));
  const checkpointFile = `${series.dir}/checkpoints.json`;
  const checkpoints = existsSync(path.join(root, checkpointFile))
    ? json(root, checkpointFile).checkpoints.map((name) => {
      const point = json(root, `${series.dir}/${name}`);
      return { name: name.replace(/\.json$/, ''), revision: point.revision ?? null, selected: point.selected_count ?? null, raw: point.raw_count ?? null };
    })
    : [];
  const long = rows.filter((row) => row.long);
  const producible = rows.filter((row) => row.producible);
  return {
    key: series.key,
    name: series.name,
    revision: pool.revision,
    counts: {
      raw_records: manifest.counts.raw_records,
      selected: manifest.counts.selected_candidates,
      themes: rows.length,
      long_themes: long.length,
      producible: producible.length,
      long_reserve: long.filter((row) => !row.producible).length,
      scored: rows.filter((row) => row.audience).length,
      improved: rows.filter((row) => row.audience?.rounds.length).length,
    },
    audience_min: AUDIENCE_MIN,
    themes: rows,
    expansions,
    checkpoints,
    sources: { themes_sha256: sha256(themesBytes), manifest_sha256: sha256(manifestBytes) },
  };
}

export function buildBundle(root = ROOT) {
  return { schema_version: 1, status: 'EDITORIAL_THEMES_NOT_SCRIPTS', series: SERIES.map((series) => seriesBundle(root, series)) };
}

export const render = (bundle) => `${JSON.stringify(bundle)}\n`;

export function writeBundle(root = ROOT) {
  const content = render(buildBundle(root));
  mkdirSync(path.dirname(path.join(root, OUTPUT)), { recursive: true });
  writeFileSync(path.join(root, OUTPUT), content);
  return { status: 'WRITTEN', file: OUTPUT, bytes: Buffer.byteLength(content) };
}

export function checkBundle(root = ROOT) {
  const expected = render(buildBundle(root));
  const actual = existsSync(path.join(root, OUTPUT)) ? readFileSync(path.join(root, OUTPUT), 'utf8') : null;
  if (actual !== expected) throw new Error(`${OUTPUT} is out of date with the pools; run node tools/video/pool-admin/bundle.mjs build`);
  return { status: 'PASS', file: OUTPUT };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const command = process.argv[2] ?? 'check';
  try {
    if (command === 'build') console.log(JSON.stringify(writeBundle()));
    else if (command === 'check') console.log(JSON.stringify(checkBundle()));
    else throw new Error('usage: bundle.mjs build|check');
  } catch (error) {
    console.error(error.message); process.exitCode = 1;
  }
}
