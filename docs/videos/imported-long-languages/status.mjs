// Read persisted review state without changing projects or exposing paired credentials.
import { readFileSync, writeFileSync } from 'node:fs';
import { parseArgs } from 'node:util';
import { assertProject, createSiteClient } from './runner.mjs';
const { values } = parseArgs({ options: { manifest: { type: 'string' }, out: { type: 'string' } }, strict: true });
if (!values.manifest) throw new Error('--manifest is required');
const manifest = JSON.parse(readFileSync(values.manifest, 'utf8'));
const sleep = ms => new Promise(resolve => setTimeout(resolve, ms));
const api = createSiteClient({ env: process.env, fetch: globalThis.fetch, sleep });
const receipt = { checked_at: new Date().toISOString(), projects: [] };
for (const entry of manifest.videos) {
  const project = await api.reviews(entry.slug);
  assertProject(project, entry);
  const reviews = project.reviews.filter(r => r.gate === 'languages' && r.status !== 'superseded')
    .map(r => ({ id: r.id, status: r.status, created_at: r.created_at, content_sha256: r.content_sha256,
      locales: r.payload?.locales, files: r.files?.map(({ role, sha256, size }) => ({ role, sha256, size })) }));
  receipt.projects.push({ slug: entry.slug, final_sha256: entry.final_sha256, languages: project.languages,
    reviews, youtube_video_id: project.youtube_video_id });
  console.log(JSON.stringify({ slug: entry.slug, languages: project.languages, reviews: reviews.map(({ id, status }) => ({ id, status })) }));
  await sleep(1100);
}
if (values.out) writeFileSync(values.out, JSON.stringify(receipt, null, 2) + '\n');
