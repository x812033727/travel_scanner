// The session's own arithmetic on YouTube's report rows: per-video totals over a window since
// publishing, and where the views came from. Everything here is computed locally, from the raw
// rows the site hands back, and is labelled that way wherever it is printed (YouTube's developer
// policies: a number derived from API data is never presented as YouTube's own).
import { codeName, TRAFFIC_SOURCE_DETAIL } from "./codes.mjs";

export const DERIVED_NOTE = "Self-computed from YouTube Reporting API rows (sums and weighted averages); not numbers YouTube reported.";
const PACIFIC = "America/Los_Angeles";

const number = (value) => {
  const parsed = Number(value);
  return value === "" || value === undefined || value === null || !Number.isFinite(parsed) ? null : parsed;
};

/** The Pacific day an instant falls on, as YYYY-MM-DD. */
export function pacificDay(instant) {
  const parts = new Intl.DateTimeFormat("en-CA", { timeZone: PACIFIC, year: "numeric", month: "2-digit", day: "2-digit" }).formatToParts(new Date(instant));
  const get = (type) => parts.find((part) => part.type === type).value;
  return `${get("year")}-${get("month")}-${get("day")}`;
}

export const addDays = (day, days) => new Date(Date.parse(`${day}T00:00:00Z`) + days * 86_400_000).toISOString().slice(0, 10);

/** Rows as objects keyed by column name. */
export function records({ columns, rows }) {
  return rows.map((row) => Object.fromEntries(columns.map((name, index) => [name, row[index]])));
}

/** The window of a video: its first ``days`` Pacific days from publishing, cut at ``lastDay``
 * (the newest day with data). ``complete`` is false while the window has not run out. */
export function windowOf(video, days, lastDay) {
  if (!video.published_at) return null;
  const start = pacificDay(video.published_at);
  const end = addDays(start, days - 1);
  if (start > lastDay) return null;
  return { start, end: end < lastDay ? end : lastDay, complete: end <= lastDay };
}

function sum(items, key) {
  let total = 0;
  let seen = false;
  for (const item of items) {
    const value = number(item[key]);
    if (value !== null) {
      total += value;
      seen = true;
    }
  }
  return seen ? total : null;
}

function weighted(items, key, weightKey) {
  let top = 0;
  let bottom = 0;
  for (const item of items) {
    const value = number(item[key]);
    const weight = number(item[weightKey]);
    if (value !== null && weight !== null && weight > 0) {
      top += value * weight;
      bottom += weight;
    }
  }
  return bottom > 0 ? top / bottom : null;
}

const round = (value, places = 2) => (value === null ? null : Math.round(value * 10 ** places) / 10 ** places);

/** Per-video totals from channel_basic and channel_reach_basic rows, each row inside its video's
 * window. Averages are recomputed from the parts (watch time over views; CTR weighted by
 * impressions; average view percentage weighted by views), never averaged across rows. */
export function videoSummaries(videos, windows, basicRows, reachRows) {
  const inWindow = (row) => {
    const span = windows.get(row.video_id);
    return span && row.date >= span.start && row.date <= span.end;
  };
  const byVideo = (rows) => {
    const grouped = new Map();
    for (const row of rows) if (inWindow(row)) grouped.set(row.video_id, [...(grouped.get(row.video_id) ?? []), row]);
    return grouped;
  };
  const basic = byVideo(basicRows);
  const reach = byVideo(reachRows);
  return videos.filter((video) => windows.has(video.video_id)).map((video) => {
    const span = windows.get(video.video_id);
    const rows = basic.get(video.video_id) ?? [];
    const shown = reach.get(video.video_id) ?? [];
    const views = sum(rows, "views");
    const watch = sum(rows, "watch_time_minutes");
    const gained = sum(rows, "subscribers_gained");
    const lost = sum(rows, "subscribers_lost");
    return {
      video_id: video.video_id,
      slug: video.slug,
      title: video.title,
      category: video.category,
      shorts: video.shorts,
      published_day: span.start,
      window: `${span.start}..${span.end}`,
      window_complete: span.complete,
      days_with_data: new Set(rows.map((row) => row.date)).size,
      views,
      engaged_views: sum(rows, "engaged_views"),
      watch_time_minutes: round(watch, 1),
      average_view_duration_seconds: views ? round((watch * 60) / views, 1) : null,
      average_view_duration_percentage: round(weighted(rows, "average_view_duration_percentage", "views")),
      likes: sum(rows, "likes"),
      comments: sum(rows, "comments"),
      shares: sum(rows, "shares"),
      subscribers_net: gained === null && lost === null ? null : (gained ?? 0) - (lost ?? 0),
      thumbnail_impressions: sum(shown, "video_thumbnail_impressions"),
      thumbnail_ctr: round(weighted(shown, "video_thumbnail_impressions_ctr", "video_thumbnail_impressions"), 4),
    };
  });
}

/** Views and watch time by traffic source, and the top details (search terms, suggesting
 * videos, external pages) of each source. */
export function trafficBreakdown(rows, { top = 10 } = {}) {
  const sources = new Map();
  let allViews = 0;
  for (const row of rows) {
    const type = String(row.traffic_source_type ?? "");
    const views = number(row.views) ?? 0;
    const watch = number(row.watch_time_minutes) ?? 0;
    allViews += views;
    const entry = sources.get(type) ?? { traffic_source_type: type, name: codeName("traffic_source_type", type), views: 0, watch_time_minutes: 0, details: new Map() };
    entry.views += views;
    entry.watch_time_minutes += watch;
    const detail = row.traffic_source_detail;
    if (detail) entry.details.set(detail, (entry.details.get(detail) ?? 0) + views);
    sources.set(type, entry);
  }
  return [...sources.values()]
    .sort((a, b) => b.views - a.views)
    .map((entry) => ({
      traffic_source_type: entry.traffic_source_type,
      name: entry.name,
      views: entry.views,
      share_of_views: allViews ? round(entry.views / allViews, 4) : null,
      watch_time_minutes: round(entry.watch_time_minutes, 1),
      detail_kind: TRAFFIC_SOURCE_DETAIL[Number(entry.traffic_source_type)] ?? null,
      top_details: [...entry.details.entries()].sort((a, b) => b[1] - a[1]).slice(0, top).map(([detail, views]) => ({ detail, views })),
    }));
}

const cell = (value) => (value === null || value === undefined ? "—" : String(value));

/** A Markdown table of ``items`` with ``columns``, with the derived-numbers note above it. */
export function markdownTable(items, columns) {
  const head = `| ${columns.join(" | ")} |\n| ${columns.map(() => "---").join(" | ")} |\n`;
  const body = items.map((item) => `| ${columns.map((name) => cell(item[name]).replace(/\|/g, "\\|")).join(" | ")} |`).join("\n");
  return `${DERIVED_NOTE}\n\n${head}${body}\n`;
}
