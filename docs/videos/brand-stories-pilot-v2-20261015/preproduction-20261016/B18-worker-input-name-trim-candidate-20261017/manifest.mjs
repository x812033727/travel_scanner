#!/usr/bin/env node
// Pin exact bytes of the isolated successor. The manifest does not hash itself.
import assert from 'node:assert/strict';
import crypto from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
const files = [
  'B18.json', 'README.md', 'build.mjs', 'claim-coverage.json', 'delta.json',
  'manifest.mjs', 'remapped-chapters/engine.json', 'remapped-chapters/hook.json',
  'remapped-chapters/idea.json', 'remapped-chapters/now.json',
  'remapped-chapters/origin.json', 'remapped-chapters/turn.json',
  'review-request.md', 'series-adoption.json', 'verification.json',
];
const sha = (data) => crypto.createHash('sha256').update(data).digest('hex');
const content = `${JSON.stringify({
  schema_version: 1, status: 'OFFLINE_NARROW_SUCCESSOR_INDEPENDENT_REVIEW_PENDING',
  files: Object.fromEntries(files.map((file) => [file, sha(fs.readFileSync(path.join(here, file)))])),
}, null, 2)}\n`;
const target = path.join(here, 'sha256.json');
const mode = process.argv[2];
assert(['--write', '--check'].includes(mode), 'use --write or --check');
if (mode === '--write') fs.writeFileSync(target, content);
else assert.equal(fs.readFileSync(target, 'utf8'), content, 'successor file hash drift');
console.log(JSON.stringify({ files: files.length, manifest_sha256: sha(content) }, null, 2));
