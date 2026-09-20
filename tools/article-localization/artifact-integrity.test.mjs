import assert from 'node:assert/strict';
import test from 'node:test';
import { mkdtemp, mkdir, readFile, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import path from 'node:path';
import { digest, sha256, inventory, loadBoundJob, finishRenderBinding } from './artifact-integrity.mjs';

const put = (filename, value) => writeFile(filename, JSON.stringify(value, null, 2) + '\n');
async function fixture(t, stage = 'translated') {
  const root = await mkdtemp(path.join(tmpdir(), 'article-integrity-'));
  t.after(async () => { assert.equal(path.dirname(root), tmpdir()); assert.ok(path.basename(root).startsWith('article-integrity-')); await rm(root, { recursive: true, force: true }); });
  const directory = path.join(root, 'work/test/en');
  const outputFolder = path.join(directory, 'assets/guides/test');
  const sourceFolder = path.join(root, 'apps/web/public/guides/test');
  await mkdir(outputFolder, { recursive: true });
  await mkdir(sourceFolder, { recursive: true });
  const svg = '<svg xmlns="http://www.w3.org/2000/svg" width="300" height="200"><text x="10" y="60">原文</text></svg>';
  const source = { title: '原文', description: '原文說明', blocks: [{ type: 'paragraph', text: '保留內容' }] };
  const reference = { pointer: '/hero/src', source: '/guides/test/diagram.svg', source_sha256: sha256(svg), target: '/guides/test/diagram-en.svg' };
  const asset = { source: reference.source, source_sha256: reference.source_sha256, source_svg: svg, target_svg: reference.target, references: [reference] };
  const job = { slug: 'test', locale: 'en', source_locale: 'zh-TW', source_document: source, source_sha256: digest(source), pack_path: null, assets: [asset], fields: {} };
  job.job_sha256 = digest(job);
  await writeFile(path.join(sourceFolder, 'diagram.svg'), svg);
  await put(path.join(directory, 'source.json'), job);
  await put(path.join(directory, 'fields.json'), job.fields);
  await put(path.join(directory, 'document.json'), source);
  await put(path.join(directory, 'translated-fields.json'), { translations: {} });
  await put(path.join(directory, 'assets.json'), [{ svg: path.join(outputFolder, 'diagram-en.svg'), public_svg: reference.target, targets: [reference.target], source_sha256: asset.source_sha256 }]);
  await writeFile(path.join(outputFolder, 'diagram-en.svg'), svg.replace('原文', 'Text'));
  if (stage === 'rendered') {
    await writeFile(path.join(outputFolder, 'diagram-en-preview.png'), 'preview bytes');
    await writeFile(path.join(outputFolder, 'hero-en.jpg'), 'raster bytes');
    await put(path.join(directory, 'render-receipt.json'), { automatedLayoutPassed: true });
  }
  const manifest = { binding_version: 1, job_sha256: job.job_sha256, stage, schema_validated: true, files: await inventory(directory) };
  await put(path.join(directory, 'artifact-manifest.json'), manifest);
  const receipt = { status: stage, job_sha256: job.job_sha256, document_sha256: digest(source), artifact_manifest_sha256: sha256(await readFile(path.join(directory, 'artifact-manifest.json'))) };
  await put(path.join(directory, 'receipt.json'), receipt);
  return { root, directory, receipt };
}

test('first render accepts translated binding before render artifacts exist', async t => {
  const { root, directory } = await fixture(t);
  const bound = await loadBoundJob(directory, root);
  assert.equal(bound.manifest.stage, 'translated');
  assert.equal(bound.assets.length, 1);
});

test('renderer rejects stale status and every bound input/output mutation', async t => {
  for (const relative of ['source.json', 'document.json', 'translated-fields.json', 'assets.json', 'artifact-manifest.json', 'render-receipt.json', 'assets/guides/test/diagram-en.svg', 'assets/guides/test/hero-en.jpg', 'assets/guides/test/diagram-en-preview.png']) {
    await t.test(relative, async sub => {
      const { root, directory } = await fixture(sub, 'rendered');
      const filename = path.join(directory, relative);
      await writeFile(filename, Buffer.concat([await readFile(filename), Buffer.from('\n')]));
      await assert.rejects(loadBoundJob(directory, root), /changed|hashes/);
    });
  }
});

test('receipt alone cannot promote an unrendered document', async t => {
  const { root, directory, receipt } = await fixture(t);
  await put(path.join(directory, 'receipt.json'), { ...receipt, status: 'rendered' });
  await assert.rejects(loadBoundJob(directory, root), /stage mismatch/);
});

test('authorized render binds SVG changes, preview and render receipt without cycles', async t => {
  const { root, directory } = await fixture(t);
  const bound = await loadBoundJob(directory, root);
  const svgPath = bound.assets[0].svg;
  await writeFile(svgPath, (await readFile(svgPath, 'utf8')).replace('x="10"', 'font-size="18" x="10"'));
  await writeFile(svgPath.replace('.svg', '-preview.png'), 'new preview bytes');
  await finishRenderBinding(bound, { automatedLayoutPassed: true }, true);
  const after = await loadBoundJob(directory, root);
  assert.equal(after.manifest.stage, 'rendered');
  assert.ok(after.manifest.files['render-receipt.json']);
  assert.ok(after.manifest.files['assets/guides/test/diagram-en-preview.png']);
  assert.ok(!after.manifest.files['receipt.json']);
  assert.ok(!after.manifest.files['artifact-manifest.json']);
});

test('changes to document or source during rendering prevent new binding', async t => {
  const { root, directory } = await fixture(t);
  const bound = await loadBoundJob(directory, root);
  await writeFile(path.join(directory, 'document.json'), '{}');
  await assert.rejects(finishRenderBinding(bound, {}, true), /Input changed while rendering/);
  const receipt = JSON.parse(await readFile(path.join(directory, 'receipt.json'), 'utf8'));
  assert.equal(receipt.status, 'translated');
});
