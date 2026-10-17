import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { cpSync, mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import test from 'node:test';
import { addedTermsInSpoken, prepareProposedEvent, proposeRebaseline,
  verifyProposedTransition } from '../A01-lexicon-rebaseline-e640-candidate/rebaseline.mjs';

const SLUG = 'story-rolling-suitcase-v2';
const CANDIDATE_ID = 'a01-lexicon-rebaseline-e6403c824aac13b4-20261017';
const CHAPTERS = ['hook', 'origin', 'idea', 'engine', 'turn', 'now'];
// Test fixture is intentionally explicit instead of importing the production allowlist.
const ADDITIONS = {
  pull: null, request: null, Eiliko: null, Energize: null, Lab: null,
  CVE: 'C V E', IP: 'I P', Seiko: '精工', Quartz: '夸茲', Astron: '阿斯特朗',
  K: null, CEH: 'C E H', IEEE: 'I triple E', Beta: '貝塔', swissinfo: 'swiss info',
  Europa: '歐羅巴', Star: null, Donz: '東澤', Swatch: null, Group: null,
  SSIH: 'S S I H', ASUAG: 'A S U A G', Hayek: '海耶克',
};
const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const json = (value) => Buffer.from(`${JSON.stringify(value)}\n`);
const getCode = (call) => { try { call(); return null; } catch (error) { return error.code ?? error.message; } };

export function fixture(t, { narrationText = '這是原始旁白。', narrationSay,
  videoText = '這是影片旁白。', videoSay } = {}) {
  const parent = mkdtempSync(path.join(os.tmpdir(), 'a01-lexicon-rebaseline-'));
  t.after(() => rmSync(parent, { recursive: true, force: true }));
  const beforeRoot = path.join(parent, 'before');
  const afterRoot = path.join(parent, 'after');
  mkdirSync(beforeRoot);
  const at = (root, rel) => path.join(root, ...rel.split('/'));
  const write = (root, rel, bytes) => {
    const file = at(root, rel);
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, bytes);
    return file;
  };
  const hash = (root, rel) => sha(readFileSync(at(root, rel)));
  write(beforeRoot, 'A01-LEXICON-E640-OFFLINE-FIXTURE.json',
    json({ schema_version: 1, slug: SLUG, synthetic_fixture: true }));
  const docs = `docs/videos/${SLUG}`;
  const oldLexicon = json({ schema_version: 1, terms: { OpenAI: 'Open A I', Plath: null } });
  const newLexicon = json({ schema_version: 1, terms: { OpenAI: 'Open A I', Plath: null, ...ADDITIONS } });
  const oldLexiconFile = write(parent, 'old-lexicon.json', oldLexicon);
  for (const [rel, content] of Object.entries({
    [`${docs}/series.json`]: 'series\n',
    [`${docs}/claims.md`]: 'claims\n', [`${docs}/script.md`]: 'script\n',
    [`${SLUG}/review/narrative.json`]: 'narrative\n',
  })) write(beforeRoot, rel, content);
  write(beforeRoot, `${docs}/video.json`, json({ schema_version: 1, slug: SLUG,
    scenes: [{ id: 'video-01', lines: [{ id: 'video-line-01', text: videoText,
      ...(videoSay === undefined ? {} : { say: videoSay }) }] }] }));
  write(beforeRoot, 'docs/videos/lexicon.json', newLexicon);
  for (const key of CHAPTERS) write(beforeRoot, `${SLUG}/story/chapters/${key}.json`, json({ key,
    scenes: [{ id: `${key}-01`, lines: [{ id: 'line-01', text: narrationText,
      ...(narrationSay === undefined ? {} : { say: narrationSay }) }] }] }));
  write(beforeRoot, `${SLUG}/auto.json`, json({ step: 80, status: 'blocked', story: { chapters: {}, narrative_fixes: 2 } }));
  const source = (n, lexiconHash = sha(oldLexicon)) => ({
    auto: sha(json({ step: n, status: 'blocked', story: { chapters: {}, narrative_fixes: 2 } })), video: hash(beforeRoot, `${docs}/video.json`),
    series: hash(beforeRoot, `${docs}/series.json`), claims: hash(beforeRoot, `${docs}/claims.md`),
    script: hash(beforeRoot, `${docs}/script.md`), lexicon: lexiconHash,
    narrative: hash(beforeRoot, `${SLUG}/review/narrative.json`), pilot: null, verify: null,
    chapters: Object.fromEntries(CHAPTERS.map((key) => [key, hash(beforeRoot, `${SLUG}/story/chapters/${key}.json`)])),
  });
  const installed = {
    'docs/video.json': source(0).video, 'docs/script.md': source(0).script,
    'docs/claims.md': source(0).claims, 'docs/series.json': source(0).series,
    ...Object.fromEntries(CHAPTERS.map((key) => [`work/story/chapters/${key}.json`, source(0).chapters[key]])),
    'work/auto.json': source(0).auto,
  };
  const receiptRel = `${SLUG}/manual-revisions/initial/installation-receipt.json`;
  write(beforeRoot, receiptRel, json({ schema_version: 1, kind: 'a01-candidate-installation', slug: SLUG,
    installed_sha256: installed }));
  const manifest = [];
  for (let n = 0; n < 80; n++) {
    const id = `event-${String(n).padStart(3, '0')}`;
    const dir = `${SLUG}/story/recheck-audit/${id}`;
    const journalBytes = json({ n, result: 'saved' });
    const journalHash = sha(journalBytes);
    write(beforeRoot, `${dir}/${journalHash}.json`, journalBytes);
    const before = source(n), after = source(n + 1);
    const index = { schema_version: 1, slug: SLUG, result_kind: 'saved',
      install_receipt_sha256: hash(beforeRoot, receiptRel),
      before_source_sha256: sha(JSON.stringify(before)), after_source_sha256: sha(JSON.stringify(after)),
      before, after, journals: [{ name: `${journalHash}.json`, sha256: journalHash }] };
    write(beforeRoot, `${dir}/index.json`, json(index));
    manifest.push({ id, index_sha256: hash(beforeRoot, `${dir}/index.json`) });
  }
  const pins = { id: 'synthetic-fixed-80', links: 80,
    install_receipt_sha256: hash(beforeRoot, receiptRel),
    tip_index_sha256: manifest.at(-1).index_sha256,
    source_composite_sha256: sha(JSON.stringify(source(80))),
    archive_index_manifest_sha256: sha(JSON.stringify(manifest)) };
  const options = { snapshotRoot: beforeRoot, oldLexiconFile, pins,
    expectedOldSha: sha(oldLexicon), expectedNewSha: sha(newLexicon) };
  const clone = () => cpSync(beforeRoot, afterRoot, { recursive: true });
  return { parent, beforeRoot, afterRoot, oldLexiconFile, at, write, hash, clone, options };
}
