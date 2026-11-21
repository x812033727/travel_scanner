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
    // 需求（2026-11-17）：四個是非題換算的第六項與併分前的五項平均；還沒評的題案兩個都是 null。
    demand: value.demand ?? null, base: value.base ?? null,
    rounds: (value.rounds ?? []).map((round) => ({ score: round.score, comment: round.comment, changes: round.changes, reviewed_on: round.reviewed_on })),
  };
}

const CATALOG = 'docs/videos/explainer-series/catalog.json';
const base = (dir) => dir.split('/').pop();

/**
 * Produced episodes of a series, from the per-episode catalog (docs/videos/explainer-series/catalog.json) joined to
 * the pool cores they came from: Curio cores name their episode folders in production.locators; So That's Why
 * legacy cores name their episode code (P14) in prior_decision.episode. The API looks the slugs up in the site's
 * video projects for the live YouTube id; the catalog's id is only the fallback.
 */
function episodesFor(root, series, pool) {
  const catalog = existsSync(path.join(root, CATALOG)) ? json(root, CATALOG).episodes.filter((row) => row.series === series.name) : [];
  const byDir = new Map();
  const byCode = new Map();
  for (const row of pool.candidates) {
    for (const locator of row.production?.locators ?? []) if (/^docs\/videos\/(curio|sothatswhy)-/.test(locator)) byDir.set(base(locator), [...(byDir.get(base(locator)) ?? []), row.id]);
    const code = row.prior_decision?.episode;
    if (typeof code === 'string' && code) byCode.set(code.toUpperCase(), [...(byCode.get(code.toUpperCase()) ?? []), row.id]);
  }
  const used = new Set();
  const episodes = catalog.map((row) => {
    const slugs = [...new Set([row.slug, ...(row.repo_versions ?? []).map(base), ...(row.other_youtube_ids ?? []).map((pair) => pair.split('=')[0])].filter(Boolean))];
    const code = (row.folder ?? '').split('/').pop() || (row.slug.match(/^sothatswhy-([a-z]\d+)/)?.[1] ?? '').toUpperCase();
    const ids = new Set([...slugs.flatMap((slug) => byDir.get(slug) ?? []), ...(series.key === 'so-thats-why' && code ? byCode.get(code.toUpperCase()) ?? [] : [])]);
    for (const slug of slugs) used.add(slug);
    return {
      key: row.slug || row.folder || slugs[0] || row.title,
      code: code || null,
      title: row.title || slugs[0] || code,
      category: row.category || null,
      slugs,
      candidate_ids: [...ids].sort(),
      catalog: { youtube_id: row.youtube_id || null, privacy: row.privacy || null, status: row.status || null, version: row.version || null, final_date: row.final_date || null },
    };
  });
  // A produced core whose folders the catalog does not list still belongs on the list, unpublished until the site says otherwise.
  for (const [dir, ids] of [...byDir].sort(([a], [b]) => a.localeCompare(b))) {
    if (used.has(dir)) continue;
    episodes.push({ key: dir, code: null, title: pool.candidates.find((row) => row.id === ids[0])?.question ?? dir, category: null, slugs: [dir], candidate_ids: [...new Set(ids)].sort(), catalog: { youtube_id: null, privacy: null, status: null, version: null, final_date: null } });
  }
  return episodes.filter((episode) => episode.title);
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
  // 單集題：入選、可單獨成一集的題（editorial.role 為 episode_core）。它們不進題案，後台另有一個檢視列出來；
  // 商業與品牌奇聞整類都在這裡。原來如此池沒有這個角色，陣列是空的。
  const cores = pool.candidates
    .filter((row) => row.selected && row.editorial?.role === 'episode_core')
    .map((row) => ({
      id: row.id,
      category: row.category ?? null,
      question: row.question,
      hook: row.hook ?? '',
      payoff: row.editorial.payoff ?? '',
      minutes: row.editorial.minutes,
      audience: audience(row.audience),
      demand: row.demand?.demand ?? null,
      produced: Boolean(row.production?.locators?.length),
    }));
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
      cores: cores.length,
      cores_scored: cores.filter((row) => row.audience).length,
      cores_passing: cores.filter((row) => row.audience && row.audience.score >= AUDIENCE_MIN).length,
    },
    audience_min: AUDIENCE_MIN,
    themes: rows,
    cores,
    episodes: episodesFor(root, series, pool),
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
