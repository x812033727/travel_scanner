#!/usr/bin/env node
// 奇聞檔案局素材池 CLI；指令照原來如此事務所素材池的 cli.mjs。
import fs from 'node:fs';
import path from 'node:path';
import { ROOT, DIR, hash, loadDraft, buildPool, readPool, writeJson } from './core.mjs';
import { openStore, ingest, assertSnapshot, search, lookup } from './store.mjs';
import { renderQuestions, renderSources, renderDedup, renderThemes, renderHtml, validateThemes, themeReadiness } from './render.mjs';
import { readBaseline, writeBaseline, compareBaseline, validateBaseline, sourceImpact } from './history.mjs';

const [command = 'help', value, flag] = process.argv.slice(2);
const readThemes = (pool) => validateThemes(JSON.parse(fs.readFileSync(path.join(ROOT, DIR, 'themes.json'), 'utf8')), pool);
const exportsFor = (pool, themes) => ({ 'QUESTIONS.md': renderQuestions(pool), 'SOURCES.md': renderSources(pool), 'DEDUP.md': renderDedup(pool), 'THEMES.md': renderThemes(themes, pool), 'index.html': renderHtml(pool, themes) });
let db;
try {
  if (process.argv.length > 5 || (flag && (flag !== '--all' || command !== 'search')) || (['help', 'preview', 'pairs', 'build', 'check', 'index', 'stats', 'themes', 'baseline'].includes(command) && value)) throw new Error('Unexpected arguments');
  if (command === 'help') console.log('奇聞檔案局素材池: preview | pairs | build | check | index | stats | search <text> [--all] | show <id> | themes | theme <id> | baseline | snapshot <label> | source <id-or-url>');
  else if (command === 'preview' || command === 'pairs') {
    const { draft } = loadDraft();
    fs.mkdirSync(path.join(ROOT, DIR, '.cache'), { recursive: true });
    writeJson(ROOT, '.cache/draft.json', draft);
    if (command === 'preview') console.log(JSON.stringify({ status: 'DRAFT_ONLY', ...draft.counts }));
    else {
      for (const pair of draft.dedup.required_pending) console.log(`pending\t${pair.a}\t${pair.b}\tq=${pair.question_score}\ta=${pair.answer_score}\t${pair.questions.join(' ｜ ')}`);
      for (const pair of draft.dedup.cross_series_pending) console.log(`cross\t${pair.curio_id}\t${pair.external_id}\tq=${pair.question_score}\t${pair.questions.join(' ｜ ')}`);
      console.log(JSON.stringify({ pending: draft.dedup.required_pending.length, cross_pending: draft.dedup.cross_series_pending.length }));
    }
  } else if (command === 'build') {
    const pool = buildPool(); validateBaseline(readBaseline(), pool);
    const themes = readThemes(pool); const rendered = exportsFor(pool, themes);
    writeJson(ROOT, 'pool.json', pool);
    for (const [name, content] of Object.entries(rendered)) fs.writeFileSync(path.join(ROOT, DIR, name), content);
    writeJson(ROOT, 'manifest.json', { status: 'CANDIDATE_EXPORT_NOT_PRODUCTION', revision: pool.revision, counts: pool.counts, theme_count: themes.episodes.length, inputs: pool.inputs, theme_definition_sha256: hash(fs.readFileSync(path.join(ROOT, DIR, 'themes.json'))), files: ['pool.json', ...Object.keys(rendered)].map((name) => ({ file: name, sha256: hash(fs.readFileSync(path.join(ROOT, DIR, name))) })) });
    console.log(JSON.stringify({ status: 'BUILT', ...pool.counts, themes: themes.episodes.length }));
  } else {
    const pool = readPool();
    if (command === 'check') {
      validateBaseline(readBaseline(), pool);
      const themes = readThemes(pool); const rendered = exportsFor(pool, themes);
      const manifest = JSON.parse(fs.readFileSync(path.join(ROOT, DIR, 'manifest.json'), 'utf8'));
      if (manifest.theme_definition_sha256 !== hash(fs.readFileSync(path.join(ROOT, DIR, 'themes.json')))) throw new Error('Theme definition drift');
      for (const [name, content] of Object.entries(rendered)) if (fs.readFileSync(path.join(ROOT, DIR, name), 'utf8') !== content) throw new Error(`${name}: generated view drift`);
      for (const entry of manifest.files) if (hash(fs.readFileSync(path.join(ROOT, DIR, entry.file))) !== entry.sha256) throw new Error(`${entry.file}: manifest drift`);
      console.log(JSON.stringify({ status: 'PASS', ...pool.counts, themes: themes.episodes.length, production_ready: false }));
    } else if (command === 'stats') console.log(JSON.stringify(pool.counts, null, 2));
    else if (command === 'baseline') {
      const baseline = readBaseline();
      console.log(JSON.stringify(baseline ? compareBaseline(baseline, pool) : { status: 'NO_BASELINE' }, null, 2));
    } else if (command === 'snapshot') {
      if (!value) throw new Error('A snapshot label is required, e.g. 2026-11-01-<selected>');
      console.log(JSON.stringify(writeBaseline(ROOT, pool, readThemes(pool), value)));
    } else if (command === 'source') {
      if (!value) throw new Error('A source ID or URL is required');
      console.log(JSON.stringify(sourceImpact(pool, readThemes(pool), value), null, 2));
    } else if (command === 'themes' || command === 'theme') {
      const themes = readThemes(pool);
      if (command === 'themes') for (const theme of themes.episodes) { const ready = themeReadiness(theme, pool); console.log(`${theme.id}\t${theme.target_minutes} min\t${ready.ready ? 'sourced' : `needs research: ${ready.unsourced.join(',')}`}\t${theme.title}`); }
      else {
        const theme = themes.episodes.find((item) => item.id === value);
        if (!theme) throw new Error(`Unknown theme ${value}`);
        const candidates = theme.candidate_ids.map((id) => pool.candidates.find((row) => row.id === id));
        const sources = new Set(candidates.flatMap((row) => row.source_refs.map((ref) => ref.source_id)));
        console.log(JSON.stringify({ status: 'EDITORIAL_THEME_NOT_IMPORT_READY', readiness: themeReadiness(theme, pool), theme, candidates, sources: pool.sources.filter((source) => sources.has(source.id)), production_ready: false }, null, 2));
      }
    } else if (['index', 'search', 'show'].includes(command)) {
      db = openStore(path.join(ROOT, DIR, '.cache', 'pool.sqlite'));
      if (command === 'index') console.log(JSON.stringify(ingest(db, pool)));
      else {
        assertSnapshot(db, pool);
        if (!value) throw new Error('A search text or candidate id is required');
        console.log(JSON.stringify(command === 'search' ? search(db, value, { all: flag === '--all' }) : lookup(db, value), null, 2));
      }
    } else throw new Error(`Unknown command ${command}`);
  }
} catch (error) {
  console.error(error.message); process.exitCode = 1;
} finally { db?.close(); }
