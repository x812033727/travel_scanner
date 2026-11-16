#!/usr/bin/env node
// 後台「劇本」分頁的資料包：把 AI 劇（漫劇）各集的 brief／script／storyboard／review 與系列企劃的 Markdown
// 打包成 API 映像裡的唯讀 JSON（apps/api/app/video_dramas/data/）。API 看不到 docs/，所以由這裡打包；
// 劇本或企劃改了就跑 build，CI 用 check 擋過期的資料包（站主 2026-11-14：劇本先只放 AI 劇）。
import { createHash } from 'node:crypto';
import { readFileSync, writeFileSync, readdirSync, existsSync, mkdirSync, statSync, rmSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

export const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../../..');
export const OUTPUT_DIR = 'apps/api/app/video_dramas/data';
export const EPISODE_DOCS = ['brief', 'script', 'storyboard', 'review'];
const VIDEOS = 'docs/videos';

/**
 * The AI dramas shown in the admin, with the series planning folder whose top-level Markdown (outline, seasons,
 * setting, README) is shown beside the episodes. Rules and lessons change often and stay out, so editing them
 * never makes the bundle stale.
 */
export const SERIES = [
  { key: 'tai-nainai', name: '恁祖媽今年18', plans: ['docs/videos/series-plans/top40-2025-2026/2025-01-tai-nainai'] },
  { key: 'zhong-tian-qu-qi', name: '種田娶妻打天下', plans: ['docs/videos/series-plans/zhong-tian-qu-qi'] },
  { key: 'ou-de-jianghu', name: '歐德江湖', plans: ['docs/videos/series-plans/ou-de-jianghu'] },
  { key: 'zero-root-yaozu', name: '零根妖族', plans: ['docs/videos/series-plans/zero-root-yaozu'] },
  { key: 'xiuxian-jiangli', name: '修仙獎勵', plans: ['docs/videos/series-plans/xiuxian-jiangli'] },
];

const sha256 = (value) => createHash('sha256').update(value).digest('hex');
const readText = (root, file) => readFileSync(path.join(root, file), 'utf8');
const exists = (root, file) => existsSync(path.join(root, file));
const firstHeading = (markdown) => markdown.match(/^#{1,3}\s+(.+?)\s*$/m)?.[1] ?? null;
const docId = (file) => file.replace(/^docs\/videos\//, '').replace(/\.md$/, '').replace(/[^A-Za-z0-9_-]+/g, '-');

function episodeTitle(root, dir, docs) {
  const video = path.join(root, dir, 'video.json');
  if (existsSync(video)) {
    try {
      const title = JSON.parse(readFileSync(video, 'utf8')).youtube?.title;
      if (typeof title === 'string' && title.trim()) return title.trim();
    } catch { /* a broken video.json falls back to the script heading */ }
  }
  return firstHeading(docs.script ?? docs.brief ?? '') ?? dir.split('/').pop();
}

function seriesDocuments(root, series) {
  const files = [];
  for (const dir of series.plans) {
    if (!exists(root, dir)) continue;
    for (const name of readdirSync(path.join(root, dir)).sort()) {
      const file = `${dir}/${name}`;
      if (name.endsWith('.md') && statSync(path.join(root, file)).isFile()) files.push(file);
    }
  }
  return files.map((file) => {
    const markdown = readText(root, file);
    return { id: docId(file), path: file, title: firstHeading(markdown) ?? path.basename(file), bytes: Buffer.byteLength(markdown), markdown };
  });
}

function seriesBundle(root, series) {
  const pattern = new RegExp(`^${series.key}-e(\\d{3})(?:-(r\\d+))?$`);
  const dirs = readdirSync(path.join(root, VIDEOS)).filter((name) => pattern.test(name) && statSync(path.join(root, VIDEOS, name)).isDirectory()).sort();
  const episodes = dirs.map((name) => {
    const [, number, variant] = name.match(pattern);
    const dir = `${VIDEOS}/${name}`;
    const docs = Object.fromEntries(EPISODE_DOCS.filter((kind) => exists(root, `${dir}/${kind}.md`)).map((kind) => [kind, readText(root, `${dir}/${kind}.md`)]));
    let minutes = null;
    if (exists(root, `${dir}/video.json`)) {
      try { minutes = JSON.parse(readText(root, `${dir}/video.json`)).target_minutes ?? null; } catch { minutes = null; }
    }
    return { slug: name, number: Number(number), variant: variant ?? null, title: episodeTitle(root, dir, docs), target_minutes: Array.isArray(minutes) || typeof minutes === 'number' ? minutes : null, docs };
  });
  const documents = seriesDocuments(root, series);
  const index = {
    key: series.key,
    name: series.name,
    counts: { episodes: episodes.length, ...Object.fromEntries(EPISODE_DOCS.map((kind) => [kind, episodes.filter((episode) => episode.docs[kind]).length])) },
    episodes: episodes.map(({ docs, ...episode }) => ({ ...episode, docs: EPISODE_DOCS.filter((kind) => docs[kind]).map((kind) => ({ kind, bytes: Buffer.byteLength(docs[kind]) })) })),
    documents: documents.map(({ markdown, ...document }) => document),
  };
  const detail = {
    key: series.key,
    episodes: Object.fromEntries(episodes.map((episode) => [episode.slug, episode.docs])),
    documents: Object.fromEntries(documents.map((document) => [document.id, document.markdown])),
  };
  return { index, detail };
}

export function buildFiles(root = ROOT) {
  const bundles = SERIES.map((series) => seriesBundle(root, series));
  const files = {};
  for (const { index, detail } of bundles) files[`${index.key}.json`] = `${JSON.stringify(detail)}\n`;
  const series = bundles.map(({ index }) => ({ ...index, content_sha256: sha256(files[`${index.key}.json`]) }));
  files['index.json'] = `${JSON.stringify({ schema_version: 1, status: 'AUTHORED_TEXT_NOT_PRODUCTION_STATE', series })}\n`;
  return files;
}

export function writeFiles(root = ROOT) {
  const files = buildFiles(root);
  const directory = path.join(root, OUTPUT_DIR);
  if (existsSync(directory)) for (const name of readdirSync(directory)) if (name.endsWith('.json') && !files[name]) rmSync(path.join(directory, name));
  mkdirSync(directory, { recursive: true });
  for (const [name, content] of Object.entries(files)) writeFileSync(path.join(directory, name), content);
  return { status: 'WRITTEN', dir: OUTPUT_DIR, files: Object.keys(files).length, bytes: Object.values(files).reduce((sum, content) => sum + Buffer.byteLength(content), 0) };
}

export function checkFiles(root = ROOT) {
  const files = buildFiles(root);
  const directory = path.join(root, OUTPUT_DIR);
  const present = existsSync(directory) ? readdirSync(directory).filter((name) => name.endsWith('.json')).sort() : [];
  const stale = [...new Set([...present, ...Object.keys(files)])].filter((name) => !existsSync(path.join(directory, name)) || readFileSync(path.join(directory, name), 'utf8') !== files[name]);
  if (stale.length) throw new Error(`${OUTPUT_DIR} is out of date (${stale.join(', ')}); run node tools/video/drama-admin/bundle.mjs build after changing an AI drama script or plan`);
  return { status: 'PASS', dir: OUTPUT_DIR, files: Object.keys(files).length };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const command = process.argv[2] ?? 'check';
  try {
    if (command === 'build') console.log(JSON.stringify(writeFiles()));
    else if (command === 'check') console.log(JSON.stringify(checkFiles()));
    else throw new Error('usage: bundle.mjs build|check');
  } catch (error) {
    console.error(error.message); process.exitCode = 1;
  }
}
