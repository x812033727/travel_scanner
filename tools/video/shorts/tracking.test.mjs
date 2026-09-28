import assert from 'node:assert/strict';
import { linkSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import test from 'node:test';
import { buildCalendar, buildTrackingReport, CALENDAR_HEADERS, COST_HEADERS, initTracking, main, METRIC_HEADERS, parseCsv, parseInstant, reportMarkdown, stringifyCsv, trackingReport } from './tracking.mjs';

const DAY = 86_400_000;
const START = '2026-01-17';
const PUBLISHED = '2026-01-17T19:30:00+08:00';
const atAge = (days, published = PUBLISHED) => new Date(Date.parse(published) + days * DAY).toISOString();
const NOW = '2026-02-15T23:59:00+08:00';
const snapshot = (overrides = {}) => ({ slug: 'shorts-receipt-total', video_id: 'video-one', published_at: PUBLISHED, captured_at: atAge(7), views: 2000, engaged_views: 1000, stayed_pct: 60, avg_pct: 110, shares: 5, subscribers: 2, series: 'daily', ...overrides });
const cost = (overrides = {}) => ({ occurred_at: PUBLISHED, slug: 'shorts-receipt-total', category: 'voice', amount_ntd: 10, status: 'confirmed', ...overrides });
const report = (overrides = {}) => buildTrackingReport({ startDate: START, now: NOW, ...overrides });

function box(t) {
  const base = mkdtempSync(path.join(os.tmpdir(), 'shorts-tracking-'));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  return { base, directory: path.join(base, 'tracking'), campaignPath: path.join(base, 'campaign.json') };
}

test('CSV round trip preserves BOM, Chinese, commas, quoted text and embedded CRLF', () => {
  const row = { name: '台灣,"原樣"\r\n第二行', note: '' };
  const csv = stringifyCsv(['name', 'note'], [row]);
  assert.ok(csv.startsWith('\uFEFF"name","note"\r\n'));
  assert.match(csv, /""原樣""/);
  assert.deepEqual(parseCsv(csv, ['name', 'note']), [row]);
  assert.deepEqual(parseCsv('name,note\r\nalpha,beta\r\n'), [{ name: 'alpha', note: 'beta' }]);
  for (const invalid of ['a,a\n1,2', 'a,b\n"unfinished,2', 'a,b\n"a"x,2', 'a,b\n1,2,3', 'a,b\nwo"rd,2']) assert.throws(() => parseCsv(invalid), /CSV/);
});

test('calendar has 120 chronological slots over exactly 90 Taipei dates, distributed 30/45/45', () => {
  const rows = buildCalendar({ startDate: START });
  assert.equal(rows.length, 120);
  assert.equal(new Set(rows.map(row => row.scheduled_at.slice(0, 10))).size, 90);
  assert.deepEqual([rows.filter(row => row.day <= 30).length, rows.filter(row => row.day > 30 && row.day <= 60).length, rows.filter(row => row.day > 60).length], [30, 45, 45]);
  assert.equal(rows[0].scheduled_at, '2026-01-17T19:30:00+08:00');
  assert.deepEqual(rows.filter(row => row.day === 31).map(row => row.scheduled_at), ['2026-02-16T12:30:00+08:00', '2026-02-16T19:30:00+08:00']);
  assert.equal(rows.at(-1).scheduled_at, '2026-04-16T19:30:00+08:00');
  assert.equal(rows.at(-1).slot_id, 'slot-120');
  assert.ok(rows.every((row, i) => !row.slug && !row.title && row.timezone === 'Asia/Taipei' && (i === 0 || Date.parse(row.scheduled_at) > Date.parse(rows[i - 1].scheduled_at))));
});

test('calendar copies only the first 15 ordered real topics, and preserves pilot flags', () => {
  const topics = Array.from({ length: 16 }, (_, i) => ({ slug: `topic-${i}`, topic_zh: `題目 ${i}`, release_order: i + 1, series: 'blind', pilot: i < 3 })).reverse();
  const rows = buildCalendar({ startDate: START, campaign: { topics } });
  assert.equal(rows[0].slug, 'topic-0');
  assert.equal(rows[0].title, '題目 0');
  assert.equal(rows[0].is_pilot, 'true');
  assert.equal(rows[14].slug, 'topic-14');
  assert.equal(rows[15].slug, '');
});

test('init creates empty metric/cost templates and refuses any existing content without changing bytes', t => {
  const options = box(t);
  writeFileSync(options.campaignPath, JSON.stringify({ topics: [{ slug: 'real-pilot', topic_zh: '真實題目', series: 'daily', pilot: true }] }));
  const result = initTracking({ ...options, startDate: START });
  assert.equal(result.slots, 120);
  assert.deepEqual(parseCsv(readFileSync(path.join(options.directory, 'metrics.csv'), 'utf8'), METRIC_HEADERS), []);
  assert.deepEqual(parseCsv(readFileSync(path.join(options.directory, 'costs.csv'), 'utf8'), COST_HEADERS), []);
  assert.equal(parseCsv(readFileSync(path.join(options.directory, 'calendar.csv'), 'utf8'), CALENDAR_HEADERS)[0].slug, 'real-pilot');
  writeFileSync(path.join(options.directory, 'metrics.csv'), 'private existing records\n');
  const before = Object.fromEntries(readdirSync(options.directory).map(name => [name, readFileSync(path.join(options.directory, name), 'utf8')]));
  assert.throws(() => initTracking({ ...options, startDate: '2026-03-01' }), /empty directory/);
  assert.deepEqual(Object.fromEntries(readdirSync(options.directory).map(name => [name, readFileSync(path.join(options.directory, name), 'utf8')])), before);
  assert.throws(() => initTracking({ directory: options.base, startDate: START, campaignPath: options.campaignPath }), /empty directory/);
  assert.ok(!readdirSync(options.base).includes('metrics.csv'));
});

test('both file adapters reject repository destinations before generating artifacts', () => {
  const directory = fileURLToPath(new URL('./should-not-exist', import.meta.url));
  assert.throws(() => initTracking({ directory, startDate: START }), /outside the repository/);
  assert.throws(() => trackingReport({ directory, now: NOW }), /outside the repository/);
});

test('empty metrics produce explicit no_metrics JSON and Markdown with no invented samples', t => {
  const options = box(t);
  initTracking({ ...options, startDate: START });
  const result = trackingReport({ ...options, now: NOW });
  assert.equal(result.status, 'no_metrics');
  assert.equal(result.json.data.distinct_videos, 0);
  assert.equal(result.json.series.cohort_median_views, null);
  assert.deepEqual(result.json.series.decisions.map(item => item.status), ['insufficient', 'insufficient', 'insufficient']);
  assert.deepEqual(JSON.parse(readFileSync(result.files.json, 'utf8')), result.json);
  assert.equal(readFileSync(result.files.markdown, 'utf8'), result.markdown);
  assert.match(result.markdown, /no_metrics/);
  assert.match(result.markdown, /不代表 YouTube 演算法/);
});

test('latest snapshot per video supplies totals; repeated snapshots never inflate totals or sample size', () => {
  const first = snapshot({ captured_at: atAge(1), views: 1500, engaged_views: 500 });
  const week = snapshot();
  const latest = snapshot({ captured_at: atAge(10), views: 5000, engaged_views: 2500 });
  const other = snapshot({ video_id: 'video-two', slug: 'other', views: 3000 });
  const result = report({ metrics: [latest, first, week, latest, week, other] });
  assert.equal(result.totals.views, 8000);
  assert.equal(result.totals.engaged_views, 3500);
  assert.equal(result.data.distinct_videos, 2);
  assert.equal(result.data.duplicate_snapshots_ignored, 2);
  assert.equal(result.series.decisions[0].mature_eligible_videos, 2);
  assert.equal(result.series.decisions[0].status, 'insufficient');
  assert.equal(result.videos[0].checkpoints['7d'].snapshot.views, 2000);
  assert.throws(() => report({ metrics: [week, snapshot({ views: 2500 })] }), /conflicting duplicate/);
  assert.throws(() => report({ metrics: [week, snapshot({ captured_at: atAge(8), series: 'blind' })] }), /inconsistent identity/);
});

test('checkpoints use earliest actual captures in independent age windows and reject six-day or late seven-day substitutes', () => {
  const rows = [snapshot({ captured_at: atAge(0.9), views: 20 }), snapshot({ captured_at: atAge(1.5), views: 100 }), snapshot({ captured_at: atAge(3), views: 300 }), snapshot({ captured_at: atAge(6.99), views: 500 }), snapshot({ captured_at: atAge(8), views: 800 }), snapshot({ captured_at: atAge(9), views: 900 }), snapshot({ captured_at: atAge(10), views: 1000 })];
  const result = report({ metrics: rows });
  const checkpoints = result.videos[0].checkpoints;
  assert.equal(checkpoints['24h'].snapshot.views, 100);
  assert.equal(checkpoints['72h'].snapshot.views, 300);
  assert.equal(checkpoints['7d'].snapshot.views, 800);
  assert.equal(checkpoints['7d'].age_hours, 192);
  const early = report({ metrics: [snapshot({ captured_at: atAge(6.99) })] });
  assert.equal(early.videos[0].checkpoints['7d'].status, 'insufficient');
  assert.equal(report({ metrics: [snapshot({ captured_at: atAge(9.00001) })] }).videos[0].checkpoints['7d'].status, 'insufficient');
  assert.equal(report({ metrics: [snapshot({ captured_at: atAge(9) })] }).videos[0].checkpoints['7d'].status, 'available');
  const historical = report({ metrics: rows, now: atAge(4) });
  assert.equal(historical.totals.views, 300);
  assert.equal(historical.data.future_snapshots_ignored, 4);
  assert.equal(historical.videos[0].checkpoints['7d'].status, 'insufficient');
});

test('numeric validation rejects missing, infinite, negative and fractional counts while allowing average retention over 100%', () => {
  assert.equal(report({ metrics: [snapshot({ avg_pct: '180.5' })] }).videos[0].latest.avg_pct, 180.5);
  for (const views of ['', ' ', 'NaN', 'Infinity', '-1', '0.5', '9007199254740992']) assert.throws(() => report({ metrics: [snapshot({ views })] }), /views/);
  for (const stayed_pct of ['-0.1', '100.01', 'NaN']) assert.throws(() => report({ metrics: [snapshot({ stayed_pct })] }), /stayed_pct/);
  assert.throws(() => report({ metrics: [snapshot({ avg_pct: '-1' })] }), /avg_pct/);
});

test('dates require a real calendar date and an explicit timezone', () => {
  for (const value of ['2026-02-30T10:00:00+08:00', '2026-01-01T10:00:00', '2026-01-01', '2026-01-01T24:00:00Z', '2026-01-01T10:00:00+25:00']) assert.throws(() => parseInstant(value), /date|timezone/);
  assert.equal(parseInstant('2028-02-29T10:00:00+08:00'), Date.parse('2028-02-29T02:00:00Z'));
  assert.throws(() => buildCalendar({ startDate: '2026-02-29' }), /startDate/);
  assert.throws(() => report({ metrics: [snapshot({ captured_at: atAge(-1) })] }), /capture precedes/);
});

function seriesRows(series, values, offset = 0) {
  return values.map(([views, avg_pct], i) => {
    const published_at = atAge(offset + i);
    return snapshot({ slug: `${series}-${i}`, video_id: `${series}-${i}`, series, published_at, captured_at: atAge(7, published_at), views, avg_pct });
  });
}

test('series gate requires five distinct 7-day videos, each with at least 1000 engaged views', () => {
  const low = seriesRows('daily', Array(5).fill([2000, 80])).map(row => ({ ...row, engaged_views: 999 }));
  assert.equal(report({ metrics: low }).series.decisions[0].status, 'insufficient');
  assert.equal(report({ metrics: seriesRows('daily', Array(5).fill([2000, 80])) }).series.decisions[0].status, 'revise');
});

test('series decisions compare same-age cohort medians and require retained expansion hits', () => {
  const rows = [...seriesRows('daily', [[2000, 80], [2000, 80], [2000, 80], [8000, 90], [9000, 100]]), ...seriesRows('blind', Array(5).fill([2000, 80]))];
  const result = report({ metrics: rows });
  assert.equal(result.series.cohort_median_views, 2000);
  assert.equal(result.series.cohort_median_retention_pct, 80);
  assert.equal(result.series.decisions[0].status, 'expand');
  assert.equal(result.series.decisions[0].expand_hits, 2);
  const badRetention = rows.map(row => row.views > 4000 ? { ...row, avg_pct: 30 } : row);
  assert.equal(report({ metrics: badRetention }).series.decisions[0].status, 'revise');
});

test('pause needs the most recent five consecutive qualifying videos below both medians', () => {
  const low = seriesRows('daily', Array(5).fill([1000, 30]));
  const peers = [...seriesRows('blind', Array(5).fill([5000, 90])), ...seriesRows('prompts', Array(5).fill([5000, 90]))];
  assert.equal(report({ metrics: [...low, ...peers] }).series.decisions[0].status, 'pause');
  const young = snapshot({ slug: 'daily-young', video_id: 'daily-young', published_at: atAge(10), captured_at: atAge(11), views: 100 });
  assert.equal(report({ metrics: [...low, ...peers, young] }).series.decisions[0].status, 'revise');
  assert.equal(report({ metrics: [...low, ...peers, young] }).series.decisions[0].consecutive_below_both, 0);
});

test('unknown cost with a missing amount blocks paid work without silently becoming zero', () => {
  const result = report({ costs: [cost({ amount_ntd: '', status: 'unknown' }), cost({ amount_ntd: 50, status: 'reserved' })] });
  assert.equal(result.costs.paid_allowed, false);
  assert.equal(result.costs.status, 'hold');
  assert.deepEqual(result.costs.hold_reasons, ['unknown_cost']);
  assert.equal(result.costs.unknown_amount_entries, 1);
  assert.equal(result.costs.committed_ntd, 50);
  assert.equal(report({ costs: [cost({ amount_ntd: 100, status: 'unknown' })] }).costs.paid_allowed, false);
  assert.throws(() => report({ costs: [cost({ amount_ntd: '' })] }), /amount_ntd/);
  assert.throws(() => report({ costs: [cost({ amount_ntd: -1 })] }), /amount_ntd/);
});

test('30-day cost periods use campaign start rather than calendar months, including exact boundary', () => {
  const result = report({ now: '2026-02-16T00:00:00+08:00', costs: [cost({ occurred_at: '2026-02-15T23:59:59+08:00', amount_ntd: 2300 }), cost({ occurred_at: '2026-02-16T00:00:00+08:00', amount_ntd: 2500, status: 'reserved' })] });
  assert.deepEqual(result.costs.windows.map(window => window.amount_ntd), [2300, 2500, 0]);
  assert.equal(result.costs.windows[0].end_exclusive, '2026-02-16T00:00:00+08:00');
  assert.equal(result.costs.status, 'soft_limit');
  assert.equal(result.costs.paid_allowed, true);
  assert.equal(result.costs.new_experiments_allowed, false);
  assert.equal(result.costs.completion_spend_allowed, true);
  assert.equal(result.costs.completion_remaining_ntd, 500);
  assert.equal(result.costs.committed_ntd, 4800);
  assert.equal(report({ costs: [cost({ amount_ntd: 3000 })] }).costs.paid_allowed, false);
  assert.ok(report({ costs: [cost({ amount_ntd: 9000 })] }).costs.hold_reasons.includes('campaign_total_limit'));
});

test('three identified pilots share one 300 NTD ceiling; unrelated spend does not count as a pilot', () => {
  const campaign = { pilot_slugs: ['one', 'two', 'three'] };
  const result = report({ campaign, costs: [cost({ slug: 'one', amount_ntd: 100 }), cost({ slug: 'two', amount_ntd: 100 }), cost({ slug: 'three', amount_ntd: 100, status: 'reserved' }), cost({ slug: 'other', amount_ntd: 200 })] });
  assert.equal(result.costs.pilot.amount_ntd, 300);
  assert.equal(result.costs.paid_allowed, true);
  assert.equal(result.costs.pilot.spend_allowed, false);
  assert.ok(result.costs.pilot.hold_reasons.includes('pilot_limit'));
  assert.equal(result.costs.new_experiments_allowed, true);
  assert.equal(report().costs.pilot.status, 'not_identified');
});

test('prelaunch costs carry into the first budget period and exact 2400 stops new experiments only', () => {
  const rows = [cost({ occurred_at: '2026-01-10T10:00:00+08:00', amount_ntd: 300 }), cost({ amount_ntd: 2100, status: 'reserved' })];
  const result = report({ costs: rows });
  assert.equal(result.costs.windows[0].amount_ntd, 2400);
  assert.equal(result.costs.prelaunch_carryover_ntd, 300);
  assert.equal(result.costs.new_experiments_allowed, false);
  assert.equal(result.costs.new_experiments_remaining_ntd, 0);
  assert.equal(result.costs.completion_spend_allowed, true);
  assert.equal(result.costs.completion_remaining_ntd, 600);
  const stopped = report({ costs: [...rows, cost({ amount_ntd: 600 })] });
  assert.equal(stopped.costs.completion_spend_allowed, false);
  const nextPeriod = report({ now: '2026-02-16T00:00:00+08:00', costs: [...rows, cost({ amount_ntd: 600 })] });
  assert.equal(nextPeriod.costs.active_period, 2);
  assert.equal(nextPeriod.costs.new_experiments_allowed, true, 'a completed period at exactly its cap must not freeze later periods');
});

test('prelaunch reports show no active daily target, and unrelated publication dates never count toward campaign totals', () => {
  const before = report({ now: '2026-01-01T00:00:00+08:00', metrics: [snapshot()] });
  assert.equal(before.goal.status, 'not_started');
  assert.equal(before.goal.days_remaining, null);
  assert.equal(before.goal.required_daily, null);
  assert.equal(before.totals.views, 0);
  assert.equal(before.data.future_snapshots_ignored, 1);
  const old = snapshot({ video_id: 'old', slug: 'old', published_at: '2025-12-01T00:00:00Z', views: 99_000_000 });
  const late = snapshot({ video_id: 'late', slug: 'late', published_at: '2026-04-17T00:00:00+08:00', captured_at: '2026-04-18T00:00:00+08:00', views: 99_000_000 });
  const result = report({ now: '2026-05-01T00:00:00+08:00', metrics: [old, snapshot(), late] });
  assert.equal(result.totals.views, 2000);
  assert.equal(result.data.outside_campaign_snapshots_ignored, 2);
  assert.equal(result.goal.measured_views, 2000);
});

test('post-deadline growth remains visible in lifetime totals but cannot retroactively achieve the 90-day goal', () => {
  const result = report({ now: '2026-05-01T00:00:00+08:00', metrics: [snapshot(), snapshot({ captured_at: '2026-04-18T00:00:00+08:00', views: 10_000_001 })] });
  assert.equal(result.totals.views, 10_000_001);
  assert.equal(result.goal.measured_views, 2000);
  assert.equal(result.goal.status, 'expired');
  assert.equal(result.goal.remaining, 9_998_000);
});

test('a linked report output is refused without modifying its other target', t => {
  const options = box(t);
  initTracking({ ...options, startDate: START });
  const target = path.join(options.base, 'keep.json');
  writeFileSync(target, 'untouched');
  linkSync(target, path.join(options.directory, 'report.json'));
  assert.throws(() => trackingReport({ ...options, now: NOW }), /linked report/);
  assert.equal(readFileSync(target, 'utf8'), 'untouched');
  assert.ok(!readdirSync(options.directory).includes('report.md'));
});

test('active daily goal uses ceiling; before or after the campaign no daily target is invented', () => {
  const end = '2026-04-17T00:00:00+08:00';
  for (const now of [end, '2027-01-01T00:00:00+08:00']) {
    const result = report({ now });
    assert.equal(result.goal.status, 'expired');
    assert.equal(result.goal.days_remaining, 0);
    assert.equal(result.goal.required_daily, null);
    assert.equal(result.goal.remaining, 10_000_000);
    assert.equal(result.goal.daily_basis, 'campaign_ended');
    assert.equal(result.costs.paid_allowed, false);
  }
  assert.equal(report({ now: '2026-01-17T00:00:00+08:00' }).goal.required_daily, 111112);
  assert.equal(report({ metrics: [snapshot({ views: 10_000_001 })] }).goal.required_daily, 0);
  const achievedAfterDeadline = report({ now: end, metrics: [snapshot({ views: 10_000_001 })] });
  assert.equal(achievedAfterDeadline.goal.status, 'achieved');
  assert.equal(achievedAfterDeadline.goal.required_daily, null);
  assert.match(reportMarkdown(report({ now: end })), /活動期限已到/);
});

test('CLI adapters support explicit input paths, deterministic now and JSON output, with invalid input failing', async t => {
  const options = box(t);
  let stdout = '', stderr = '';
  const io = { stdout: { write: text => { stdout += text; } }, stderr: { write: text => { stderr += text; } } };
  assert.equal(await main(['track-init', '--dir', options.directory, '--start', START, '--campaign', options.campaignPath], io), 0);
  assert.equal(JSON.parse(stdout).slots, 120);
  stdout = '';
  assert.equal(await main(['report', '--dir', options.directory, '--now', NOW, '--campaign', options.campaignPath, '--format', 'json'], io), 0);
  assert.equal(JSON.parse(stdout).status, 'no_metrics');
  assert.equal(await main(['report', '--dir', options.directory, '--now', '2026-01-01'], io), 2);
  assert.match(stderr, /explicit timezone/);
});
