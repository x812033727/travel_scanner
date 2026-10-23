// Independent, read-only verification of the complete A01 104-event source.
import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { SLUG, sourceTuple, sourceHash, auditInventory,
  PRODUCTION_104_PINS } from './transaction.mjs';

const sha = (bytes) => createHash('sha256').update(bytes).digest('hex');
const exact = (file) => {
  const stat = fs.lstatSync(file);
  assert.ok(stat.isFile() && !stat.isSymbolicLink(), `regular file required: ${file}`);
  return fs.readFileSync(file);
};

export function verifySource104(roots) {
  const before = sourceTuple(roots);
  const source = sourceHash(before);
  const audit = path.join(roots.work, SLUG, 'story', 'recheck-audit');
  const entries = fs.readdirSync(audit, { withFileTypes: true });
  assert.equal(entries.length, 104, 'expected exactly 104 prior events');
  assert.ok(entries.every((entry) => entry.isDirectory() && !entry.isSymbolicLink()));
  const oldAudit = auditInventory(audit);
  assert.equal(oldAudit.count, PRODUCTION_104_PINS.audit_file_count,
    '104 immutable audit file count changed');
  const edges = entries.map((entry) => {
    const file = path.join(audit, entry.name, 'index.json');
    const index = JSON.parse(exact(file));
    assert.equal(index.schema_version, 1, 'old audit index schema changed');
    assert.equal(index.slug, SLUG, 'old audit slug changed');
    assert.equal(sourceHash(index.before), index.before_source_sha256,
      'old audit before tuple changed');
    assert.equal(sourceHash(index.after), index.after_source_sha256,
      'old audit after tuple changed');
    return { id: entry.name, file, index };
  });
  const byBefore = new Map();
  for (const edge of edges) {
    assert.ok(!byBefore.has(edge.index.before_source_sha256), 'old audit chain fork');
    byBefore.set(edge.index.before_source_sha256, edge);
  }
  const afterSet = new Set(edges.map((edge) => edge.index.after_source_sha256));
  const starts = edges.filter((edge) => !afterSet.has(edge.index.before_source_sha256));
  assert.equal(starts.length, 1, 'old audit chain root changed');
  const seen = new Set();
  let current = starts[0].index.before_source_sha256;
  while (byBefore.has(current)) {
    const edge = byBefore.get(current);
    assert.ok(!seen.has(edge.id), 'old audit chain cycle');
    seen.add(edge.id);
    current = edge.index.after_source_sha256;
  }
  assert.equal(seen.size, 104, 'old audit chain gap');
  assert.equal(current, source, 'old audit tip is not captured source');
  const tips = edges.filter((edge) => edge.index.after_source_sha256 === source);
  assert.equal(tips.length, 1, '104 source tip must be unique');
  const tip = JSON.parse(exact(tips[0].file));
  assert.equal(sourceHash(tip.after), source, '104 tip tuple changed');
  assert.deepEqual(tip.after, before, '104 files differ from tip');
  assert.equal(tip.after.pilot, null, 'script review already exists');
  assert.equal(source, PRODUCTION_104_PINS.source_sha256,
    'independent 104 source pin changed');
  const oldIndexSha = sha(exact(tips[0].file));
  assert.equal(oldIndexSha, PRODUCTION_104_PINS.tip_index_sha256,
    'independent 104 tip pin changed');
  assert.equal(oldAudit.sha256, PRODUCTION_104_PINS.audit_inventory_sha256,
    'independent 104 audit inventory changed');
  return { before, source, oldAudit, oldEventId: tips[0].id, oldIndexSha };
}
