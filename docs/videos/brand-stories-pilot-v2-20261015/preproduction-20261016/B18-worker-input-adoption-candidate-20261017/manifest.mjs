#!/usr/bin/env node
// Byte pins for the isolated candidate. sha256.json itself is deliberately excluded.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const files = [
  'B18.json', 'README.md', 'build.mjs', 'claim-coverage.json', 'manifest.mjs',
  'remapped-chapters/engine.json', 'remapped-chapters/hook.json',
  'remapped-chapters/idea.json', 'remapped-chapters/now.json',
  'remapped-chapters/origin.json', 'remapped-chapters/turn.json',
  'review-request.md', 'series-adoption.json', 'verification.json',
];
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const value = {
  schema_version: 1,
  status: 'OFFLINE_CANDIDATE_INDEPENDENT_REVIEW_PENDING',
  files: Object.fromEntries(files.map((file) => [file, sha(fs.readFileSync(path.join(here, file)))])),
};
const output = `${JSON.stringify(value, null, 2)}\n`;
const target = path.join(here, 'sha256.json');
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
if (mode === '--write') fs.writeFileSync(target, output);
else assert.equal(fs.readFileSync(target, 'utf8'), output, 'candidate file hash drift');
console.log(JSON.stringify({ files: files.length, manifest_sha256: sha(output), row_sha256: value.files['B18.json'] }, null, 2));
