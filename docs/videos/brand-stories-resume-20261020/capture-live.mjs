// Safe production observation: only GET through the existing paired tool client.
// Tokens, raw settings, user identities, full review payloads and media never enter the export.
import { parseArgs } from 'node:util';
import { writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { automationClient } from '../../../tools/video/automation/client.mjs';
import { readCredentials } from '../../../tools/video/tts/credentials.mjs';
import { mediaStatus } from '../../../tools/video/media/client.mjs';

const { values } = parseArgs({ options: { 'credential-home': { type: 'string' } }, strict: true });
const here = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(here, '../../..');
const ctx = { env: process.env, root, home: values['credential-home'] };
const client = automationClient(ctx, { attempts: 1 });
const credentials = readCredentials({ env: ctx.env, home: ctx.home });
const started = new Date().toISOString();
const settings = await client.settings();
const media = await mediaStatus({ site: credentials.site, token: credentials.token, attempts: 1 });
const catalog = await client.videos();
const videos = catalog.filter(v => v.slug.startsWith('story-'));
const exactSlugs = [...new Set([...videos.map(v => v.slug),
  'story-rolling-suitcase-v2', 'story-conveyor-belt-sushi-v2',
  'story-five-lego-legoland', 'story-five-costco-hot-dog', 'story-five-adidas-puma-brothers',
  'story-five-ajinomoto-chip-film', 'story-five-pringles-vat-case'])];
const projects = [];
const unregistered = [];
for (const slug of exactSlugs) {
  const detail = await client.reviews(slug);
  if (!detail) { unregistered.push(slug); continue; }
  const final = detail.reviews.find(r => r.gate === 'final' && r.status === 'approved');
  projects.push({
    slug: detail.slug, stage: detail.stage, series_slug: detail.series_slug,
    ready_to_upload: detail.ready_to_upload, last_synced_at: detail.last_synced_at,
    worker_state: detail.worker_state, download_available: detail.download_available,
    media_usd: detail.media_usd,
    media_usd_scope: 'Media subtotal only; not an all-in production ledger.',
    youtube_video_id: detail.youtube_video_id,
    languages: Object.fromEntries(Object.entries(detail.languages ?? {}).map(([locale, parts]) =>
      [locale, Object.fromEntries(Object.entries(parts).map(([part, value]) =>
        [part, { state: value.state, reason: value.reason ?? null }]))])),
    latest_approved_final: final ? {
      content_sha256: final.content_sha256, created_at: final.created_at,
      decided_at: final.decided_at,
      submitted_duration_seconds: final.payload.duration_seconds,
      duration_scope: 'Stored submitted final duration; not a new ffprobe or body-only measurement.',
      qa_ok_at_submission: final.payload.qa?.ok ?? null,
      failed_qa_items_at_submission: (final.payload.qa?.items ?? []).filter(i => i.ok === false)
        .map(i => ({ id: i.id, detail: i.detail })),
      caveat: 'An approved record can retain QA exceptions. This observation does not revoke an owner decision or claim a fresh media review.',
    } : null,
    reviews: detail.reviews.map(r => ({ gate: r.gate, status: r.status, created_at: r.created_at })),
  });
}
const relevantBudgets = Object.fromEntries(Object.entries(media.pilot_budgets ?? {})
  .filter(([slug]) => ['story-rolling-suitcase-v2', 'story-conveyor-belt-sushi-v2'].includes(slug)));
const output = {
  schema_version: 1, started_at: started, completed_at: new Date().toISOString(),
  site: credentials.site, observation_only: true,
  paired_authentication_verified: true,
  catalog_scope: { returned_rows: catalog.length, server_cap: 200,
    exhaustive: false, exact_slugs_probed: exactSlugs,
    unregistered_exact_slugs: unregistered,
    note: 'The list endpoint caps its results; known pilot and five-series slugs are also queried exactly. A 404 means no project row, not no host files.' },
  observed_routes: ['GET automation/settings', 'GET media/status', 'GET automation/videos?shorts=exclude',
    ...exactSlugs.map(slug => `GET reviews/${slug}`)],
  settings: { automation_enabled: settings.enabled,
    drama_enabled: settings.drama?.drama_enabled,
    series_max_in_flight: settings.drama?.series_max_in_flight,
    auto_approve_final: settings.drama?.drama_auto_approve_final,
    generic_media_cap_usd: media.max_usd_per_video,
    image: { provider: media.image?.provider, model: media.image?.model, configured: media.image?.configured } },
  pilot_budgets: relevantBudgets,
  provider_cash_balance: null,
  provider_cash_balance_note: 'Configured provider and quota do not disclose actual vendor credit balance.',
  projects,
  limitations: ['No host workspace, release SHA, locks or producer liveness readback is available through these responses.',
    'worker_state unavailable means the API cannot read producer state; it is not proof the worker stopped.',
    'Review-file descriptors are not the host chapter files, timeline, speech journal or complete original media.',
    'No import, retry, setting change, model call, asset generation or upload was performed.'],
};
writeFileSync(path.join(here, 'live-status.json'), JSON.stringify(output, null, 2) + '\n');
console.log(JSON.stringify({ projects: projects.length, paired: true,
  ready_to_upload: projects.filter(p => p.ready_to_upload).length,
  approved_finals_with_qa_exceptions: projects.filter(p => p.latest_approved_final?.qa_ok_at_submission === false).length,
  output: 'live-status.json', paid_calls: 0 }));
