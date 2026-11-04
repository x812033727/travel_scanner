import { DatabaseSync } from 'node:sqlite';
import { mkdirSync } from 'node:fs';
import path from 'node:path';
import { hash } from './core.mjs';

export function openStore(file) {
  if (file !== ':memory:') mkdirSync(path.dirname(file), { recursive: true });
  const db = new DatabaseSync(file);
  db.exec(`PRAGMA foreign_keys=ON;
    CREATE TABLE IF NOT EXISTS meta(key TEXT PRIMARY KEY,value TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS ingest_runs(snapshot TEXT PRIMARY KEY,finished_at TEXT NOT NULL,record_count INTEGER NOT NULL,selected_count INTEGER NOT NULL);
    CREATE TABLE IF NOT EXISTS revisions(content_hash TEXT PRIMARY KEY,kind TEXT NOT NULL,record_id TEXT NOT NULL,body TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS candidates(id TEXT PRIMARY KEY,question TEXT NOT NULL,domain TEXT NOT NULL,answer_target TEXT NOT NULL,scope TEXT NOT NULL,selected INTEGER NOT NULL,active INTEGER NOT NULL,content_hash TEXT NOT NULL REFERENCES revisions(content_hash),body TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS sources(id TEXT PRIMARY KEY,url TEXT NOT NULL UNIQUE,body TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS source_links(candidate_id TEXT NOT NULL REFERENCES candidates(id),source_id TEXT NOT NULL REFERENCES sources(id),locator TEXT NOT NULL,PRIMARY KEY(candidate_id,source_id,locator));
    CREATE TABLE IF NOT EXISTS aliases(raw_id TEXT PRIMARY KEY,canonical_id TEXT NOT NULL REFERENCES candidates(id),body TEXT NOT NULL);
    CREATE VIRTUAL TABLE IF NOT EXISTS candidate_search USING fts5(id UNINDEXED,question,answer_target,scope,tokenize='trigram');`);
  return db;
}

export function ingest(db, pool, { beforeCommit } = {}) {
  if (pool.status !== 'CURATED_CANDIDATE_POOL_NOT_PRODUCTION') throw new Error('Only reviewed selections may enter the index');
  const snapshot = hash(JSON.stringify(pool));
  const current = db.prepare("SELECT value FROM meta WHERE key='snapshot'").get()?.value;
  if (current === snapshot) return { status: 'UNCHANGED', snapshot, writes: 0 };
  db.exec('BEGIN IMMEDIATE');
  try {
    const revision = db.prepare('INSERT OR IGNORE INTO revisions(content_hash,kind,record_id,body) VALUES (?,?,?,?)');
    const source = db.prepare('INSERT INTO sources(id,url,body) VALUES (?,?,?) ON CONFLICT(id) DO UPDATE SET url=excluded.url,body=excluded.body');
    for (const row of pool.sources) {
      const body = JSON.stringify(row);
      revision.run(hash(body), 'source', row.id, body);
      source.run(row.id, row.url, body);
    }
    // Removed records stay in the index as inactive; prior revisions remain in revisions.
    db.exec('UPDATE candidates SET active=0,selected=0');
    const candidate = db.prepare('INSERT INTO candidates(id,question,domain,answer_target,scope,selected,active,content_hash,body) VALUES (?,?,?,?,?,?,1,?,?) ON CONFLICT(id) DO UPDATE SET question=excluded.question,domain=excluded.domain,answer_target=excluded.answer_target,scope=excluded.scope,selected=excluded.selected,active=1,content_hash=excluded.content_hash,body=excluded.body');
    const link = db.prepare('INSERT OR IGNORE INTO source_links(candidate_id,source_id,locator) VALUES (?,?,?)');
    for (const row of pool.candidates) {
      const body = JSON.stringify(row); const digest = hash(body);
      revision.run(digest, 'canonical_question', row.id, body);
      candidate.run(row.id, row.question, row.domain, row.answer_target, row.scope, Number(row.selected), digest, body);
      db.prepare('DELETE FROM source_links WHERE candidate_id=?').run(row.id);
      for (const ref of row.source_refs) link.run(row.id, ref.source_id, ref.locator);
    }
    const alias = db.prepare('INSERT INTO aliases(raw_id,canonical_id,body) VALUES (?,?,?) ON CONFLICT(raw_id) DO UPDATE SET canonical_id=excluded.canonical_id,body=excluded.body');
    for (const row of pool.raw_records) {
      const body = JSON.stringify(row);
      revision.run(hash(body), 'raw_record', row.id, body);
      alias.run(row.id, pool.dedup.aliases[row.id], body);
    }
    db.exec('DELETE FROM candidate_search');
    db.exec('INSERT INTO candidate_search(id,question,answer_target,scope) SELECT id,question,answer_target,scope FROM candidates WHERE active=1');
    db.prepare('INSERT INTO meta(key,value) VALUES (?,?) ON CONFLICT(key) DO UPDATE SET value=excluded.value').run('snapshot', snapshot);
    db.prepare('INSERT INTO ingest_runs(snapshot,finished_at,record_count,selected_count) VALUES (?,?,?,?) ON CONFLICT(snapshot) DO UPDATE SET finished_at=excluded.finished_at').run(snapshot, new Date().toISOString(), pool.counts.raw_records, pool.counts.selected_candidates);
    beforeCommit?.();
    db.exec('COMMIT');
    return { status: 'IMPORTED', snapshot, writes: pool.raw_records.length + pool.candidates.length, selected: pool.counts.selected_candidates };
  } catch (error) {
    db.exec('ROLLBACK');
    throw error;
  }
}

export function assertSnapshot(db, pool) {
  const saved = db.prepare("SELECT value FROM meta WHERE key='snapshot'").get()?.value;
  if (saved !== hash(JSON.stringify(pool))) throw new Error('Index is stale; run index after reviewing the current pool');
}

export function search(db, query, { all = false, limit = 30 } = {}) {
  if (!query.trim() || !Number.isInteger(limit) || limit < 1 || limit > 200) throw new Error('Search needs text and a limit from 1 to 200');
  const selection = all ? '' : ' AND c.selected=1';
  if ([...query.trim()].length < 3) {
    const like = `%${query.replaceAll('\\', '\\\\').replaceAll('%', '\\%').replaceAll('_', '\\_')}%`;
    return db.prepare(`SELECT c.id,c.question,c.domain,c.selected FROM candidates c WHERE c.active=1${selection} AND (c.question LIKE ? ESCAPE '\\' OR c.answer_target LIKE ? ESCAPE '\\') ORDER BY c.id LIMIT ?`).all(like, like, limit);
  }
  const phrase = `"${query.replaceAll('"', '""')}"`;
  return db.prepare(`SELECT c.id,c.question,c.domain,c.selected FROM candidate_search s JOIN candidates c ON c.id=s.id WHERE candidate_search MATCH ? AND c.active=1${selection} ORDER BY rank,c.id LIMIT ?`).all(phrase, limit);
}

export function lookup(db, id) {
  const alias = db.prepare('SELECT canonical_id FROM aliases WHERE raw_id=?').get(id);
  const row = db.prepare('SELECT body,active,selected FROM candidates WHERE id=?').get(alias?.canonical_id ?? id);
  if (!row) throw new Error(`Unknown candidate ${id}`);
  const candidate = JSON.parse(row.body);
  candidate.selected = Boolean(row.selected);
  const sources = db.prepare('SELECT s.body,l.locator FROM source_links l JOIN sources s ON s.id=l.source_id WHERE l.candidate_id=? ORDER BY s.id,l.locator').all(candidate.id).map((source) => ({ ...JSON.parse(source.body), locator: source.locator }));
  return { requested_id: id, indexed_active: Boolean(row.active), candidate, sources };
}
