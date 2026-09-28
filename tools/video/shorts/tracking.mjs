// Local campaign bookkeeping. Thresholds are internal editorial rules, not platform rules.
import { existsSync, lstatSync, mkdirSync, readFileSync, readdirSync, realpathSync, unlinkSync, writeFileSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';
import { parseArgs } from 'node:util';

const DAY = 86_400_000;
const SERIES = ['daily', 'blind', 'prompts'];
const SOURCE_ROOT = fileURLToPath(new URL('../../../', import.meta.url));
const DEFAULT_CAMPAIGN = fileURLToPath(new URL('../../../docs/videos/ai-shorts/campaign/campaign.json', import.meta.url));
export const CALENDAR_HEADERS = ['slot_id', 'day', 'scheduled_at', 'timezone', 'slug', 'title', 'series', 'is_pilot'];
// subscribers means subscribers gained, never Studio's potentially negative net change.
// Incomplete exports belong in separate raw/staging files, not zero-filled metrics.csv rows.
export const METRIC_HEADERS = ['slug', 'video_id', 'published_at', 'captured_at', 'views', 'engaged_views', 'stayed_pct', 'avg_pct', 'shares', 'subscribers', 'series'];
export const COST_HEADERS = ['occurred_at', 'slug', 'category', 'amount_ntd', 'status'];
export const INTERNAL_THRESHOLDS = Object.freeze({ minimum_videos: 5, minimum_engaged_per_video: 1000, expand_hits: 2, views_multiple: 2, pause_streak: 5, monthly_soft_ntd: 2400, monthly_hard_ntd: 3000, total_ntd: 9000, pilot_ntd: 300, goal_views: 10_000_000 });

/** RFC 4180 fields, CRLF records and UTF-8 BOM for spreadsheet applications. */
export function stringifyCsv(headers, rows = []) {
  const quote = value => `"${String(value ?? '').replaceAll('"', '""')}"`;
  return '\uFEFF' + [headers, ...rows.map(row => headers.map(key => row[key]))].map(row => row.map(quote).join(',')).join('\r\n') + '\r\n';
}

/** Preserve quoted commas, quotes and newlines; refuse ambiguous, malformed input. */
export function parseCsv(input, expectedHeaders) {
  const text = String(input).replace(/^\uFEFF/, '');
  const records = [];
  let row = [], field = '', quoted = false, closed = false;
  const finishField = () => { row.push(field); field = ''; closed = false; };
  const finishRow = () => { finishField(); if (row.some(value => value !== '')) records.push(row); row = []; };
  for (let i = 0; i < text.length; i++) {
    const char = text[i];
    if (quoted) {
      if (char === '"' && text[i + 1] === '"') { field += '"'; i++; }
      else if (char === '"') { quoted = false; closed = true; }
      else field += char;
    } else if (char === ',') finishField();
    else if (char === '\r' || char === '\n') { if (char === '\r' && text[i + 1] === '\n') i++; finishRow(); }
    else if (closed) throw new Error('CSV: unexpected character after closing quote');
    else if (char === '"') { if (field !== '') throw new Error('CSV: unescaped quote'); quoted = true; }
    else field += char;
  }
  if (quoted) throw new Error('CSV: unterminated quoted field');
  if (field || row.length || closed) finishRow();
  const headers = records.shift();
  if (!headers || new Set(headers).size !== headers.length || headers.some(header => !header)) throw new Error('CSV: missing or duplicate headers');
  if (expectedHeaders && (headers.length !== expectedHeaders.length || headers.some((header, i) => header !== expectedHeaders[i]))) throw new Error(`CSV: expected headers ${expectedHeaders.join(',')}`);
  return records.map((values, i) => {
    if (values.length !== headers.length) throw new Error(`CSV record ${i + 2}: expected ${headers.length} fields, got ${values.length}`);
    return Object.fromEntries(headers.map((header, index) => [header, values[index]]));
  });
}

function validDate(value) {
  const match = /^(\d{4})-(\d{2})-(\d{2})$/.exec(value);
  if (!match) return false;
  const [, y, m, d] = match.map(Number);
  const leap = y % 4 === 0 && (y % 100 !== 0 || y % 400 === 0);
  return m >= 1 && m <= 12 && d >= 1 && d <= [31, leap ? 29 : 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m - 1];
}

export function parseInstant(value, label = 'timestamp') {
  const match = typeof value === 'string' && /^(\d{4}-\d{2}-\d{2})T(\d{2}):(\d{2})(?::(\d{2})(?:\.\d{1,3})?)?(Z|[+-]\d{2}:\d{2})$/.exec(value);
  if (!match || !validDate(match[1]) || Number(match[2]) > 23 || Number(match[3]) > 59 || Number(match[4] ?? 0) > 59) throw new Error(`${label}: valid ISO date with explicit timezone required`);
  const result = Date.parse(value);
  if (!Number.isFinite(result)) throw new Error(`${label}: invalid date or timezone`);
  return result;
}

function campaignStart(startDate) {
  if (typeof startDate !== 'string' || !validDate(startDate)) throw new Error('startDate must be a valid YYYY-MM-DD date');
  return parseInstant(`${startDate}T00:00:00+08:00`, 'startDate');
}
const taipeiDate = ms => new Date(ms + 8 * 3_600_000).toISOString().slice(0, 10);
const sum = values => values.reduce((a, b) => a + b, 0);
const median = values => { const list = [...values].sort((a, b) => a - b); const n = list.length; return n ? (list[Math.floor((n - 1) / 2)] + list[Math.floor(n / 2)]) / 2 : null; };
const rounded = value => Math.round(value * 1_000_000) / 1_000_000;

function pilotSlugs(campaign = {}) {
  const explicit = campaign.pilot_slugs ?? [];
  return [...new Set([...explicit, ...(campaign.topics ?? []).filter(topic => topic.pilot === true || topic.is_pilot === true).map(topic => topic.slug)].filter(slug => typeof slug === 'string' && slug))];
}

export function buildCalendar({ startDate, campaign = {} }) {
  const start = campaignStart(startDate);
  if (campaign.topics !== undefined && !Array.isArray(campaign.topics)) throw new Error('campaign.topics must be an array');
  const topics = [...(campaign.topics ?? [])].sort((a, b) => (a.release_order ?? Infinity) - (b.release_order ?? Infinity)).slice(0, 15);
  const pilots = new Set(pilotSlugs(campaign));
  const slots = [];
  for (let day = 1; day <= 90; day++) {
    const date = taipeiDate(start + (day - 1) * DAY);
    // Day 31 is relative day 1 of the second phase; odd relative days have two posts.
    const times = day > 30 && (day - 30) % 2 === 1 ? ['12:30', '19:30'] : ['19:30'];
    for (const time of times) {
      const topic = topics[slots.length];
      slots.push({ slot_id: `slot-${String(slots.length + 1).padStart(3, '0')}`, day, scheduled_at: `${date}T${time}:00+08:00`, timezone: 'Asia/Taipei', slug: topic?.slug ?? '', title: topic?.topic_zh ?? topic?.title ?? '', series: topic?.series ?? '', is_pilot: topic?.slug && pilots.has(topic.slug) ? 'true' : '' });
    }
  }
  return slots;
}

function optionalCampaign(campaignPath) {
  try { return JSON.parse(readFileSync(campaignPath, 'utf8').replace(/^\uFEFF/, '')); }
  catch (error) { if (error.code === 'ENOENT') return {}; throw error; }
}

function externalDirectory(directory) {
  if (typeof directory !== 'string' || !directory.trim()) throw new Error('directory required; use a directory outside the repository');
  const resolved = path.resolve(directory);
  let ancestor = resolved;
  while (!existsSync(ancestor)) ancestor = path.dirname(ancestor);
  const real = path.resolve(realpathSync(ancestor), path.relative(ancestor, resolved));
  const relative = path.relative(realpathSync(SOURCE_ROOT), real);
  if (relative === '' || (!relative.startsWith('..' + path.sep) && relative !== '..' && !path.isAbsolute(relative))) throw new Error('tracking directory must be outside the repository, including symlink targets');
  return resolved;
}

/** Require an empty external directory. Existing files are never overwritten. */
export function initTracking({ directory, startDate, campaignPath = DEFAULT_CAMPAIGN }) {
  directory = externalDirectory(directory);
  const calendar = buildCalendar({ startDate, campaign: optionalCampaign(campaignPath) });
  if (existsSync(directory) && readdirSync(directory).length) throw new Error('track-init requires an empty directory; existing data was not changed');
  mkdirSync(directory, { recursive: true });
  const created = [];
  try {
    for (const [name, headers, rows] of [['calendar.csv', CALENDAR_HEADERS, calendar], ['metrics.csv', METRIC_HEADERS, []], ['costs.csv', COST_HEADERS, []]]) {
      writeFileSync(path.join(directory, name), stringifyCsv(headers, rows), { encoding: 'utf8', flag: 'wx' }); created.push(name);
    }
  } catch (error) {
    for (const name of created) unlinkSync(path.join(directory, name));
    throw error;
  }
  return { status: 'initialized', directory, start_date: startDate, slots: calendar.length, created };
}

function numeric(value, label, { integer = false, max = Infinity } = {}) {
  if (value === '' || value === null || value === undefined || (typeof value === 'string' && !value.trim())) throw new Error(`${label}: number required`);
  const number = Number(value);
  if (!Number.isFinite(number) || number < 0 || number > max || (integer && !Number.isSafeInteger(number))) throw new Error(`${label}: finite nonnegative ${integer ? 'safe integer' : 'number'}${max < Infinity ? ` <= ${max}` : ''} required`);
  return number;
}

function normalizeMetrics(rows) {
  const unique = new Map(), identities = new Map();
  let duplicates = 0;
  for (const [index, input] of rows.entries()) {
    const label = `metrics record ${index + 2}`;
    if (!input.slug?.trim() || !input.video_id?.trim() || !SERIES.includes(input.series)) throw new Error(`${label}: slug, video_id and daily/blind/prompts series required`);
    const row = { ...input, published_ms: parseInstant(input.published_at, `${label} published_at`), captured_ms: parseInstant(input.captured_at, `${label} captured_at`) };
    if (row.captured_ms < row.published_ms) throw new Error(`${label}: capture precedes publication`);
    for (const key of ['views', 'engaged_views', 'shares', 'subscribers']) row[key] = numeric(input[key], `${label} ${key}`, { integer: true });
    row.stayed_pct = numeric(input.stayed_pct, `${label} stayed_pct`, { max: 100 });
    row.avg_pct = numeric(input.avg_pct, `${label} avg_pct`);
    const identity = JSON.stringify([row.slug, row.series, row.published_ms]);
    if (identities.has(row.video_id) && identities.get(row.video_id) !== identity) throw new Error(`${label}: inconsistent identity for video ${row.video_id}`);
    identities.set(row.video_id, identity);
    const key = JSON.stringify([row.video_id, row.captured_ms]);
    const previous = unique.get(key);
    if (previous) {
      if (['views', 'engaged_views', 'shares', 'subscribers', 'stayed_pct', 'avg_pct'].some(field => previous[field] !== row[field])) throw new Error(`${label}: conflicting duplicate snapshot for ${row.video_id}`);
      duplicates++;
    } else unique.set(key, row);
  }
  return { rows: [...unique.values()].sort((a, b) => a.captured_ms - b.captured_ms), duplicates };
}

const publicSnapshot = row => row ? Object.fromEntries(METRIC_HEADERS.map(key => [key, row[key]])) : null;
const BUCKETS = { '24h': [DAY, 2 * DAY], '72h': [3 * DAY, 4 * DAY], '7d': [7 * DAY, 9 * DAY] };

function videoSummaries(rows) {
  const byVideo = new Map();
  for (const row of rows) { if (!byVideo.has(row.video_id)) byVideo.set(row.video_id, []); byVideo.get(row.video_id).push(row); }
  return [...byVideo.values()].map(snapshots => {
    const latest = snapshots.at(-1);
    const checkpoints = Object.fromEntries(Object.entries(BUCKETS).map(([name, [min, max]]) => {
      // The first observed value in each age window is used; never interpolate a missing capture.
      const snapshot = snapshots.find(row => row.captured_ms - row.published_ms >= min && (name === '7d' ? row.captured_ms - row.published_ms <= max : row.captured_ms - row.published_ms < max));
      return [name, { status: snapshot ? 'available' : 'insufficient', age_hours: snapshot ? (snapshot.captured_ms - snapshot.published_ms) / 3_600_000 : null, snapshot: publicSnapshot(snapshot) }];
    }));
    return { slug: latest.slug, video_id: latest.video_id, series: latest.series, published_at: latest.published_at, latest: publicSnapshot(latest), checkpoints };
  }).sort((a, b) => parseInstant(a.published_at) - parseInstant(b.published_at) || a.video_id.localeCompare(b.video_id));
}

function seriesDecisions(videos) {
  const eligible = video => video.checkpoints['7d'].snapshot?.engaged_views >= INTERNAL_THRESHOLDS.minimum_engaged_per_video;
  const cohort = videos.filter(eligible).map(video => video.checkpoints['7d'].snapshot);
  const viewMedian = median(cohort.map(row => row.views));
  const retentionMedian = median(cohort.map(row => row.avg_pct));
  const decisions = SERIES.map(series => {
    const published = videos.filter(video => video.series === series);
    const mature = published.filter(eligible);
    const hits = mature.filter(video => {
      const snapshot = video.checkpoints['7d'].snapshot;
      return viewMedian > 0 && snapshot.views >= 2 * viewMedian && snapshot.avg_pct >= retentionMedian;
    });
    let streak = 0;
    for (const video of [...published].reverse()) {
      const snapshot = video.checkpoints['7d'].snapshot;
      if (!eligible(video) || snapshot.views >= viewMedian || snapshot.avg_pct >= retentionMedian) break;
      streak++;
    }
    const status = mature.length < 5 ? 'insufficient' : streak >= 5 ? 'pause' : hits.length >= 2 ? 'expand' : 'revise';
    return { series, status, mature_eligible_videos: mature.length, observed_videos: published.length, expand_hits: hits.length, consecutive_below_both: streak, hit_video_ids: hits.map(video => video.video_id) };
  });
  return { label: 'Internal editorial thresholds; not a claim about YouTube algorithms.', checkpoint: '7d', minimum_engaged_views_per_video: 1000, cohort_videos: cohort.length, cohort_median_views: viewMedian, retention_metric: 'avg_pct', cohort_median_retention_pct: retentionMedian, decisions };
}

function costSummary(rows, start, now, pilots) {
  const normalized = rows.map((row, index) => {
    const label = `cost record ${index + 2}`;
    if (!['confirmed', 'reserved', 'unknown'].includes(row.status) || !row.category?.trim()) throw new Error(`${label}: category and confirmed/reserved/unknown status required`);
    const amount = row.status === 'unknown' && (row.amount_ntd === '' || row.amount_ntd == null) ? null : numeric(row.amount_ntd, `${label} amount_ntd`);
    return { ...row, amount_ntd: amount, occurred_ms: parseInstant(row.occurred_at, `${label} occurred_at`) };
  });
  // Reservations and unresolved costs remain commitments even when dated in the future.
  const known = normalized.filter(row => row.status !== 'unknown');
  const total = rounded(sum(known.map(row => row.amount_ntd)));
  if (!Number.isFinite(total)) throw new Error('cost total exceeds finite numeric range');
  const windows = Array.from({ length: 3 }, (_, index) => {
    const from = start + index * 30 * DAY, until = from + 30 * DAY;
    // Preparation belongs to the first budget period even when production precedes launch.
    const matching = known.filter(row => (index === 0 || row.occurred_ms >= from) && row.occurred_ms < until);
    const amount = rounded(sum(matching.map(row => row.amount_ntd)));
    return { period: index + 1, start: `${taipeiDate(from)}T00:00:00+08:00`, end_exclusive: `${taipeiDate(until)}T00:00:00+08:00`, amount_ntd: amount, prelaunch_carryover_ntd: index === 0 ? rounded(sum(matching.filter(row => row.occurred_ms < start).map(row => row.amount_ntd))) : 0, status: amount >= 3000 ? 'hard_limit' : amount >= 2400 ? 'soft_limit' : 'within_budget' };
  });
  const pilotRows = known.filter(row => pilots.includes(row.slug));
  const pilot = { status: pilots.length === 3 ? 'identified' : 'not_identified', slugs: pilots, amount_ntd: pilots.length ? rounded(sum(pilotRows.map(row => row.amount_ntd))) : null, limit_ntd: 300 };
  const active = windows[Math.min(2, Math.max(0, Math.floor((now - start) / (30 * DAY))))];
  const unknown = normalized.filter(row => row.status === 'unknown');
  const reasons = [];
  if (unknown.length) reasons.push('unknown_cost');
  if (active.amount_ntd >= 3000) reasons.push('30_day_hard_limit');
  if (windows.some(window => window.amount_ntd > 3000)) reasons.push('30_day_budget_overrun');
  if (total >= 9000) reasons.push('campaign_total_limit');
  if (now >= start + 90 * DAY) reasons.push('campaign_ended');
  const completionAllowed = reasons.length === 0;
  const newAllowed = completionAllowed && active.amount_ntd < 2400;
  const completionRemaining = completionAllowed ? Math.max(0, rounded(Math.min(3000 - active.amount_ntd, 9000 - total))) : 0;
  pilot.spend_allowed = pilot.status === 'identified' ? completionAllowed && pilot.amount_ntd < 300 : null;
  pilot.hold_reasons = pilot.status === 'identified' && pilot.amount_ntd >= 300 ? ['pilot_limit'] : [];
  pilot.remaining_ntd = pilot.status === 'identified' ? Math.max(0, rounded(300 - pilot.amount_ntd)) : null;
  return { status: reasons.length ? 'hold' : active.amount_ntd >= 2400 ? 'soft_limit' : 'within_budget', paid_allowed: completionAllowed, new_experiments_allowed: newAllowed, completion_spend_allowed: completionAllowed, completion_remaining_ntd: completionRemaining, new_experiments_remaining_ntd: newAllowed ? Math.max(0, rounded(Math.min(2400 - active.amount_ntd, 9000 - total))) : 0, active_period: active.period, hold_reasons: reasons, confirmed_ntd: rounded(sum(known.filter(row => row.status === 'confirmed').map(row => row.amount_ntd))), reserved_ntd: rounded(sum(known.filter(row => row.status === 'reserved').map(row => row.amount_ntd))), committed_ntd: total, unknown_entries: unknown.length, unknown_amount_entries: unknown.filter(row => row.amount_ntd === null).length, prelaunch_carryover_ntd: windows[0].prelaunch_carryover_ntd, after_campaign_ntd: rounded(sum(known.filter(row => row.occurred_ms >= start + 90 * DAY).map(row => row.amount_ntd))), windows, pilot, label: 'NTD; confirmed + reserved commitments. Unknown costs block paid work. At 2400 stop new experiments; completion may use the remaining reserve up to 3000. The 300 pilot cap applies only to those three pilot slugs.' };
}

/** Pure report builder; all timestamps and source rows are explicit inputs. */
export function buildTrackingReport({ startDate, metrics = [], costs = [], now, campaign = {} }) {
  const start = campaignStart(startDate), current = parseInstant(now, 'now');
  const end = start + 90 * DAY;
  const normalized = normalizeMetrics(metrics);
  const inCampaign = normalized.rows.filter(row => row.published_ms >= start && row.published_ms < end);
  const observed = inCampaign.filter(row => row.captured_ms <= current);
  const videos = videoSummaries(observed);
  const totals = Object.fromEntries(['views', 'engaged_views', 'shares', 'subscribers'].map(key => {
    const total = sum(videos.map(video => video.latest[key]));
    if (!Number.isSafeInteger(total)) throw new Error(`total ${key} exceeds safe integer range`);
    return [key, total];
  }));
  const goalCutoff = Math.min(current, end);
  const goalViews = sum(videoSummaries(observed.filter(row => row.captured_ms <= goalCutoff)).map(video => video.latest.views));
  const remaining = Math.max(0, 10_000_000 - goalViews);
  const days = Math.max(0, Math.min(90, Math.ceil((end - current) / DAY)));
  const notStarted = current < start;
  const goal = { metric: 'views', label: 'Internal 10 million view goal; not a YPP eligibility calculation. Only observations captured by the 90-day deadline count toward this goal.', target: 10_000_000, measured_views: goalViews, observation_cutoff: new Date(goalCutoff).toISOString(), remaining, planned_days: 90, days_remaining: notStarted ? null : days, required_daily: notStarted || days === 0 ? null : Math.ceil(remaining / days), status: notStarted ? 'not_started' : remaining === 0 ? 'achieved' : days === 0 ? 'expired' : 'in_progress', daily_basis: notStarted ? 'not_started' : days === 0 ? 'campaign_ended' : 'remaining_campaign_days' };
  return { schema_version: 1, status: videos.length ? 'ok' : 'no_metrics', as_of: now, campaign_start: startDate, timezone: 'Asia/Taipei', thresholds: INTERNAL_THRESHOLDS, data: { input_rows: metrics.length, duplicate_snapshots_ignored: normalized.duplicates, outside_campaign_snapshots_ignored: normalized.rows.length - inCampaign.length, future_snapshots_ignored: inCampaign.length - observed.length, distinct_videos: videos.length }, metric_scope: 'daily/blind/prompts videos published within the 90-day campaign; latest snapshots captured by as_of. The goal additionally excludes post-deadline captures.', totals, goal, checkpoint_policy: { '24h': 'Earliest capture at age >=24h and <48h.', '72h': 'Earliest capture at age >=72h and <96h.', '7d': 'Earliest capture at age >=7 days and <=9 days; missing data is insufficient.' }, videos, series: seriesDecisions(videos), costs: costSummary(costs, start, current, pilotSlugs(campaign)) };
}

function md(value) { return String(value ?? '').replaceAll('|', '\\|').replace(/[\r\n]+/g, ' '); }

export function reportMarkdown(report) {
  const dailyLabel = report.goal.required_daily ?? (report.goal.status === 'not_started' ? '尚未開始' : '活動已結束');
  const lines = ['# AI Shorts 追蹤報告', '', `狀態：${report.status}；資料截止：${report.as_of}。`, '', '以下為內部編輯判斷門檻，不代表 YouTube 演算法規則；觀看目標也不是 YPP 資格核算。', '', `活動 90 天內發布之 daily/blind/prompts 影片，每支僅使用最新一筆累計：${report.data.distinct_videos} 支，views ${report.totals.views}，engaged views ${report.totals.engaged_views}。`, `重複快照忽略 ${report.data.duplicate_snapshots_ignored} 筆；未來快照忽略 ${report.data.future_snapshots_ignored} 筆；活動外影片快照忽略 ${report.data.outside_campaign_snapshots_ignored} 筆。`, 'metrics.csv 為完整、已正規化資料；缺指標的匯出留在 raw/staging，不可填 0。subscribers 欄是新增訂閱數（subscribers gained），不是可能為負數的淨增減。', '', `1,000 萬 views 目標：期限內已觀測 ${report.goal.measured_views}；剩 ${report.goal.remaining}；剩餘天數 ${report.goal.days_remaining ?? '尚未開始'}；每日需求 ${dailyLabel}；${report.goal.status}。`];
  if (report.goal.status === 'expired') lines.push('活動期限已到；保留尚未達成的觀看缺口，每日需求不再計算。');
  lines.push('', '## 同齡快照', '', '24h：滿 24 至未滿 48 小時；72h：滿 72 至未滿 96 小時；7d：滿 7 至 9 天（含端點）。各取區間內最早實際快照，缺資料不補值。', '', '| 影片 | 系列 | 24h views | 72h views | 7d views |', '| --- | --- | ---: | ---: | ---: |');
  for (const video of report.videos) lines.push(`| ${md(video.slug)} (${md(video.video_id)}) | ${video.series} | ${['24h', '72h', '7d'].map(name => video.checkpoints[name].snapshot?.views ?? 'insufficient').join(' | ')} |`);
  lines.push('', '## 系列判定', '', `至少 5 支各有 1,000 engaged views 的 7 日快照；同齡群組共 ${report.series.cohort_videos} 支，views 中位數 ${report.series.cohort_median_views ?? 'insufficient'}、avg_pct 中位數 ${report.series.cohort_median_retention_pct ?? 'insufficient'}。`, 'expand：至少 2 支觀看達中位數 2 倍，且 avg_pct 不低於中位數；pause：最近連續 5 支兩項均低於中位數；其餘 revise，樣本不足 insufficient。', '', '| 系列 | 判定 | 合格影片 | 達標影片 | 連續低於兩項 |', '| --- | --- | ---: | ---: | ---: |');
  for (const item of report.series.decisions) lines.push(`| ${item.series} | ${item.status} | ${item.mature_eligible_videos} | ${item.expand_hits} | ${item.consecutive_below_both} |`);
  lines.push('', '## 費用（NTD）', '', `已確認 ${report.costs.confirmed_ntd} + 已預留 ${report.costs.reserved_ntd} = ${report.costs.committed_ntd}。未知 ${report.costs.unknown_entries} 筆；狀態 ${report.costs.status}。`, `當前第 ${report.costs.active_period} 期：可開新實驗 ${report.costs.new_experiments_allowed ? '是' : '否'}；可支付收尾費 ${report.costs.completion_spend_allowed ? '是' : '否'}；收尾剩餘額度 ${report.costs.completion_remaining_ntd}。`, `阻擋原因：${report.costs.hold_reasons.join(', ') || '無'}。`, '每個固定 30 天區間：滿 2,400 停止新實驗，剩餘額度只供收尾；滿 3,000 停止該期付費；全期上限 9,000。未知成本一律阻擋，尚未發生的預留也計入。', '預留轉實支時更新原列狀態為 confirmed，不另加相同款項，避免重複計費。', '', '| 期別 | 起日（含） | 迄日（不含） | 已確認＋預留 | 狀態 |', '| --- | --- | --- | ---: | --- |');
  for (const window of report.costs.windows) lines.push(`| ${window.period} | ${window.start} | ${window.end_exclusive} | ${window.amount_ntd} | ${window.status} |`);
  lines.push('', `試播 3 支合計上限 300：${report.costs.pilot.status}；金額 ${report.costs.pilot.amount_ntd ?? 'insufficient'}；可再付試播費 ${report.costs.pilot.spend_allowed === null ? '未識別' : report.costs.pilot.spend_allowed ? '是' : '否'}。此上限只限制這 3 支試播，不阻擋其他影片。`, `開跑前費用 ${report.costs.prelaunch_carryover_ntd} 已併入第一期；活動結束後費用 ${report.costs.after_campaign_ntd} 仍計入全期總額。`, '未上架、缺少快照或未識別試播名單，都不當成零成效或已通過驗收。', '');
  return lines.join('\n');
}

/** File adapter: CSV inputs remain untouched; reports are reproducible derived artifacts. */
export function trackingReport({ directory, now = new Date().toISOString(), campaignPath = DEFAULT_CAMPAIGN }) {
  directory = externalDirectory(directory);
  const readCsv = (name, headers) => parseCsv(readFileSync(externalDirectory(path.join(directory, name)), 'utf8'), headers);
  const calendar = readCsv('calendar.csv', CALENDAR_HEADERS);
  if (!calendar.length) throw new Error('calendar.csv has no slots; run track-init first');
  const instants = calendar.map(row => parseInstant(row.scheduled_at, 'calendar scheduled_at'));
  const startDate = taipeiDate(Math.min(...instants));
  const campaign = optionalCampaign(campaignPath);
  // Calendar preserves the original pilot assignments if the planning document later changes.
  campaign.pilot_slugs = [...new Set([...pilotSlugs(campaign), ...calendar.filter(row => row.is_pilot === 'true').map(row => row.slug).filter(Boolean)])];
  const json = buildTrackingReport({ startDate, metrics: readCsv('metrics.csv', METRIC_HEADERS), costs: readCsv('costs.csv', COST_HEADERS), now, campaign });
  const markdown = reportMarkdown(json);
  const files = { json: path.resolve(directory, 'report.json'), markdown: path.resolve(directory, 'report.md') };
  for (const file of Object.values(files)) {
    externalDirectory(file);
    if (existsSync(file) && (lstatSync(file).isSymbolicLink() || lstatSync(file).nlink > 1)) throw new Error('refusing to overwrite a linked report file');
  }
  writeFileSync(files.json, JSON.stringify(json, null, 2) + '\n', 'utf8');
  writeFileSync(files.markdown, markdown, 'utf8');
  return { status: json.status, json, markdown, files };
}

export async function main(args = process.argv.slice(2), io = process) {
  try {
    const [command, ...rest] = args;
    if (!['track-init', 'report'].includes(command)) throw new Error('Usage: tracking.mjs track-init --dir DIR --start YYYY-MM-DD [--campaign PATH] | report --dir DIR [--now ISO] [--campaign PATH] [--format json|markdown]');
    const optionsForCommand = command === 'track-init' ? { start: { type: 'string' } } : { now: { type: 'string' }, format: { type: 'string' } };
    const { values } = parseArgs({ args: rest, options: { dir: { type: 'string' }, campaign: { type: 'string' }, ...optionsForCommand }, strict: true });
    if (values.format && !['json', 'markdown'].includes(values.format)) throw new Error('--format must be json or markdown');
    const options = { directory: values.dir, campaignPath: values.campaign };
    const result = command === 'track-init' ? initTracking({ ...options, startDate: values.start }) : trackingReport({ ...options, now: values.now });
    io.stdout.write(command === 'report' && values.format !== 'json' ? result.markdown : JSON.stringify(result.json ?? result, null, 2) + '\n');
    return 0;
  } catch (error) { io.stderr.write(`${error.message}\n`); return 2; }
}

if (process.argv[1] && pathToFileURL(path.resolve(process.argv[1])).href === import.meta.url) process.exitCode = await main();
