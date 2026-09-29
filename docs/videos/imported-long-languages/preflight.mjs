import { createHash } from 'node:crypto';
import { createReadStream, mkdirSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { parseArgs } from 'node:util';
import { automationClient } from '../../../tools/video/automation/client.mjs';
import { siteClient } from '../../../tools/video/shorts/site.mjs';
import { speechStatus } from '../../../tools/video/tts/client.mjs';

const EPISODES = ['01-image-trust', '02-confident-errors', '03-machine-internet', '04-tasks-and-jobs', '05-uneven-abilities', '06-digital-yesman'];
const { values } = parseArgs({ options: { imports: { type: 'string' }, out: { type: 'string' } }, strict: true });
if (!values.imports || !values.out) throw new Error('--imports and --out are required');
const api = automationClient({ env: process.env }, { attempts: 1 });
const site = siteClient({ attempts: 1 });
if (new URL(site.site).hostname !== 'mokaair.com') throw new Error('Expected mokaair.com pairing');
async function sha256(file) {
  const hash = createHash('sha256');
  for await (const chunk of createReadStream(file)) hash.update(chunk);
  return hash.digest('hex');
}
const settings = await api.settings();
const speech = await speechStatus({ site: site.site, token: site.token, attempts: 1 });
const result = { checked_at: new Date().toISOString(), voice: settings.voice, gemini_configured: speech.gemini_configured, projects: [] };
for (const episode of EPISODES) {
  const slug = `ai-real-world-${episode}`;
  const project = await site.project(slug);
  if (!project || project.dropped_at || project.shorts_line) throw new Error(`${slug}: unavailable, dropped or Shorts`);
  const hash = await sha256(path.join(values.imports, slug, 'final.mp4'));
  const final = project.reviews.filter(r => r.gate === 'final' && ['approved', 'pending'].includes(r.status))
    .sort((a, b) => String(b.created_at).localeCompare(String(a.created_at)))[0];
  if (!final || final.status !== 'approved' || final.content_sha256 !== hash || !project.locales_decided_at) {
    throw new Error(`${slug}: latest final approval does not match or language choice missing`);
  }
  result.projects.push({ slug, title: project.title, final_sha256: hash, final_review_id: final.id, final_decided_at: final.decided_at, locales: project.locales, locales_decided_at: project.locales_decided_at, youtube_video_id: project.youtube_video_id, stage: project.stage, checklist: project.checklist, existing_language_reviews: project.reviews.filter(r => r.gate === 'languages').map(r => ({ id: r.id, status: r.status, content_sha256: r.content_sha256 })) });
  console.log(JSON.stringify({ slug, approved_hash_matches: true, languages: project.locales, language_reviews: result.projects.at(-1).existing_language_reviews.length }));
  await new Promise(resolve => setTimeout(resolve, 1100));
}
mkdirSync(values.out, { recursive: true });
writeFileSync(path.join(values.out, 'preflight.json'), JSON.stringify(result, null, 2) + '\n');
console.log(JSON.stringify({ checked_at: result.checked_at, voice: result.voice, gemini_configured: result.gemini_configured, projects: result.projects.length }));
