/** Shared, noncircular staged-artifact contract; no browser or model calls. */
import { createHash } from 'node:crypto';
import { readFile, writeFile, readdir, lstat } from 'node:fs/promises';
import path from 'node:path';

export const sha256 = data => createHash('sha256').update(data).digest('hex');
const ordered = value => Array.isArray(value) ? value.map(ordered) : value && typeof value === 'object' ? Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key])])) : value;
export const digest = value => sha256(JSON.stringify(ordered(value)));
const json = async filename => JSON.parse(await readFile(filename, 'utf8'));

export function contained(root, relative) {
  const resolved = path.resolve(root, relative);
  const check = path.relative(path.resolve(root), resolved);
  if (check === '..' || check.startsWith(`..${path.sep}`) || path.isAbsolute(check)) throw new Error(`Artifact escaped root: ${relative}`);
  return resolved;
}

const inputNames = new Set(['source.json', 'fields.json', 'translated-fields.json', 'document.json', 'assets.json', 'prompt.txt', 'output-schema.json', 'render-receipt.json']);

export async function inventory(directory) {
  const files = [];
  async function collect(folder, assets = false) {
    for (const entry of await readdir(folder, { withFileTypes: true })) {
      const filename = path.join(folder, entry.name);
      if (entry.isSymbolicLink()) throw new Error(`Symlink artifact is not supported: ${filename}`);
      if (entry.isDirectory() && (assets || entry.name === 'assets')) await collect(filename, true);
      if (entry.isFile() && (assets || inputNames.has(entry.name) || entry.name.startsWith('attempt-'))) files.push(filename);
    }
  }
  await collect(directory);
  const result = {};
  for (const filename of files.sort()) result[path.relative(directory, filename).split(path.sep).join('/')] = sha256(await readFile(filename));
  return result;
}

async function sourceUnchanged(job, root) {
  const { job_sha256: expectedJobHash, ...unsigned } = job;
  if (digest(unsigned) !== expectedJobHash || digest(job.source_document) !== job.source_sha256) throw new Error('Staged source or job manifest changed after preparation');
  async function verify(relative, expected) {
    const filename = contained(root, relative);
    if ((await lstat(filename)).isSymbolicLink() || sha256(await readFile(filename)) !== expected) throw new Error(`Source changed: ${relative}`);
  }
  if (job.pack_path) await verify(job.pack_path, job.pack_sha256);
  for (const asset of job.assets) {
    await verify(`apps/web/public/${asset.source.replace(/^\//, '')}`, asset.source_sha256);
    for (const reference of asset.references) await verify(`apps/web/public/${reference.source.replace(/^\//, '')}`, reference.source_sha256);
  }
  for (const [src, hash] of Object.entries(job.raster_source_hashes ?? {})) await verify(`apps/web/public/${src.replace(/^\//, '')}`, hash);
}

export async function loadBoundJob(directory, root) {
  const receiptBytes = await readFile(path.join(directory, 'receipt.json'));
  const receipt = JSON.parse(receiptBytes.toString('utf8'));
  if (!receipt.artifact_manifest_sha256) throw new Error('Legacy staged job requires explicit materialize migration and re-render');
  const manifestBytes = await readFile(path.join(directory, 'artifact-manifest.json'));
  if (sha256(manifestBytes) !== receipt.artifact_manifest_sha256) throw new Error('Artifact manifest changed after validation');
  const manifest = JSON.parse(manifestBytes.toString('utf8'));
  const job = await json(path.join(directory, 'source.json'));
  await sourceUnchanged(job, root);
  if (manifest.binding_version !== 1 || manifest.job_sha256 !== job.job_sha256 || receipt.job_sha256 !== job.job_sha256 || manifest.stage !== receipt.status) throw new Error('Source, manifest and receipt identity/stage mismatch');
  if (!['translated', 'rendered'].includes(manifest.stage) || !manifest.schema_validated) throw new Error('Only schema-validated translations may be rendered');
  const actual = await inventory(directory);
  if (digest(actual) !== digest(manifest.files)) throw new Error('Staged artifact input/output hashes or inventory changed after validation');
  for (const name of ['source.json', 'fields.json', 'translated-fields.json', 'document.json', 'assets.json']) if (!(name in manifest.files)) throw new Error(`Missing bound input: ${name}`);
  if (manifest.stage === 'rendered' && !('render-receipt.json' in manifest.files)) throw new Error('Rendered job is missing its bound render receipt');
  if (digest(await json(path.join(directory, 'fields.json'))) !== digest(job.fields)) throw new Error('Editable fields disagree with immutable job');
  if (digest(await json(path.join(directory, 'document.json'))) !== receipt.document_sha256) throw new Error('Document no longer matches schema-validation receipt');
  const assets = await json(path.join(directory, 'assets.json'));
  const expectedAssets = job.assets.map(asset => ({ svg: contained(path.join(directory, 'assets'), asset.target_svg.replace(/^\//, '')), public_svg: asset.target_svg, targets: [...new Set(asset.references.map(reference => reference.target))].sort(), source_sha256: asset.source_sha256 }));
  if (digest(assets) !== digest(expectedAssets)) throw new Error('Asset manifest differs from immutable job');
  return { directory, root, job, receipt, assets, manifest, receiptHash: sha256(receiptBytes), manifestHash: sha256(manifestBytes) };
}

export async function finishRenderBinding(bound, renderReceipt, passed) {
  const { directory, job, receipt, root } = bound;
  // Font fitting legitimately changes staged SVGs. Every other original input,
  // attempt and document remains pinned to the pre-render binding.
  await sourceUnchanged(job, root);
  if (sha256(await readFile(path.join(directory, 'receipt.json'))) !== bound.receiptHash || sha256(await readFile(path.join(directory, 'artifact-manifest.json'))) !== bound.manifestHash) throw new Error('Job receipt or manifest changed while rendering');
  const before = bound.manifest.files;
  const actual = await inventory(directory);
  const immutable = name => !name.startsWith('assets/') && name !== 'render-receipt.json';
  const originalInputs = Object.keys(before).filter(immutable).sort();
  const currentInputs = Object.keys(actual).filter(immutable).sort();
  if (JSON.stringify(originalInputs) !== JSON.stringify(currentInputs)) throw new Error('Input inventory changed while rendering');
  for (const name of originalInputs) if (actual[name] !== before[name]) throw new Error(`Input changed while rendering: ${name}`);
  await writeFile(path.join(directory, 'render-receipt.json'), JSON.stringify(renderReceipt, null, 2) + '\n');
  const stage = passed ? 'rendered' : 'translated';
  const manifest = { binding_version: 1, job_sha256: job.job_sha256, stage, schema_validated: true, files: await inventory(directory) };
  const manifestBytes = JSON.stringify(manifest, null, 2) + '\n';
  await writeFile(path.join(directory, 'artifact-manifest.json'), manifestBytes);
  await writeFile(path.join(directory, 'receipt.json'), JSON.stringify({ ...receipt, status: stage, artifact_manifest_sha256: sha256(manifestBytes), automated_layout_passed: passed, reviewed: false, editorial_review_complete: false, visual_review_complete: false, glyph_review_complete: false }, null, 2) + '\n');
}
