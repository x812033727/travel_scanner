#!/usr/bin/env node
// The channel's YouTube Reporting API reports, read from the site with the video tool token
// (docs/videos/YOUTUBE-REPORTS.md, skill youtube-channel-reports).
//
// The site downloads YouTube's daily report files and keeps them; this asks the site, never
// Google, so a paired session needs nothing but its mkv_ token. The rows come back exactly as
// YouTube wrote them: any total, ratio or ranking made from them is the session's own analysis
// for the owner, and is labelled that way, never passed off as YouTube's number.
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { readCredentials } from "../tts/credentials.mjs";
import { USER_AGENT } from "../tts/client.mjs";

export const EXIT = { ok: 0, usage: 2, owner: 3, external: 4 };
const TIMEOUT_MS = 240_000;
const MAX_SPAN_DAYS = 120;
const MAX_SYNC_ROUNDS = 20;
// YouTube posts a day's report 48 to 72 hours later (Pacific days).
const LATENCY_DAYS = 2;
const DAY = /^\d{4}-\d{2}-\d{2}$/;

const HELP = `YouTube channel reports, read from the site (docs/videos/YOUTUBE-REPORTS.md)

Usage: node tools/video/youtube-reports/cli.mjs <command> [options]

  overview [--json]                 what the site keeps: report families, days covered, the site's
                                    videos with their YouTube ids, and whether the grant reads Analytics
  sync [--force] [--limit N]        ask the site to fetch what YouTube made since the last run;
                                    repeats while files remain (without --force, once per 12 hours)
  rows --report F [--from D] [--to D] [--video ID]... [--slug S]... [--format csv|json] [--out FILE]
                                    one family's rows for Pacific days D..D (default: the last 28
                                    days with data), as YouTube wrote them; --slug maps a site video
  export --out DIR [--days N] [--report F]...
                                    overview.json plus one <family>.csv per report for the last N
                                    days (default 28), ready to analyse

Families: channel_basic (views, engaged views, watch time, average view duration and percentage,
likes, shares, subscribers), channel_reach_basic (thumbnail impressions and CTR),
channel_reach_combined, channel_traffic_source, channel_playback_location, channel_device_os,
channel_demographics, channel_sharing_service, channel_subtitles, channel_end_screens.

Exit codes: 0 ok, 2 usage, 3 needs the owner (link the channel again with YouTube Analytics),
4 the site or YouTube refused.
`;

class UsageError extends Error {}

export class SiteError extends Error {
  constructor(status, body) {
    super(`${status} ${body?.code ?? ""} ${body?.detail ?? ""}`.trim());
    this.status = status;
    this.body = body;
  }
}

export function client({ site, token, fetchImpl = globalThis.fetch }) {
  async function call(method, route, { body, accept = "application/json" } = {}) {
    const response = await fetchImpl(`${site}/api/video/${route}`, {
      method,
      headers: {
        Authorization: `Bearer ${token}`,
        "User-Agent": USER_AGENT,
        Accept: accept,
        ...(body ? { "Content-Type": "application/json" } : {}),
      },
      body: body ? JSON.stringify(body) : undefined,
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!response.ok) throw new SiteError(response.status, await response.json().catch(() => ({})));
    return response.json();
  }
  return {
    overview: () => call("GET", "youtube-reports"),
    sync: (options) => call("POST", "youtube-reports/sync", { body: options }),
    rows: ({ report, start, end, videos = [] }) => {
      const query = new URLSearchParams({ report, start, end, format: "json" });
      for (const video of videos) query.append("video_id", video);
      return call("GET", `youtube-reports/rows?${query}`);
    },
  };
}

const iso = (date) => date.toISOString().slice(0, 10);
const addDays = (day, days) => iso(new Date(Date.parse(`${day}T00:00:00Z`) + days * 86_400_000));

/** Spans of at most MAX_SPAN_DAYS days covering ``start`` to ``end``, both included. */
export function spans(start, end, size = MAX_SPAN_DAYS) {
  const found = [];
  for (let from = start; from <= end; from = addDays(from, size)) {
    const to = addDays(from, size - 1);
    found.push([from, to < end ? to : end]);
  }
  return found;
}

/** The rows of ``report`` for ``start`` to ``end``, read in spans the site accepts. The columns
 * are the union, in the order the site gave them; a column a span lacks is empty there. */
export async function readRows(api, { report, start, end, videos = [] }) {
  const columns = [];
  const parts = [];
  let truncated = false;
  let reportType = null;
  for (const [from, to] of spans(start, end)) {
    const answer = await api.rows({ report, start: from, end: to, videos });
    reportType ??= answer.report_type_id;
    truncated ||= Boolean(answer.truncated);
    for (const name of answer.columns) if (!columns.includes(name)) columns.push(name);
    parts.push(answer);
  }
  const rows = parts.flatMap((answer) => answer.rows.map((row) => columns.map((name) => {
    const at = answer.columns.indexOf(name);
    return at < 0 ? "" : row[at];
  })));
  return { report_type_id: reportType, columns, rows, truncated, days: parts.flatMap((answer) => answer.days) };
}

function csvCell(value) {
  const text = String(value ?? "");
  return /[",\n\r]/.test(text) ? `"${text.replace(/"/g, '""')}"` : text;
}

export function toCsv({ columns, rows }) {
  return `${[columns, ...rows].map((row) => row.map(csvCell).join(",")).join("\n")}\n`;
}

function defaultSpan(values, now) {
  const to = values.to ?? iso(new Date(now.getTime() - LATENCY_DAYS * 86_400_000));
  const from = values.from ?? addDays(to, -27);
  for (const [name, value] of [["--from", from], ["--to", to]]) if (!DAY.test(value)) throw new UsageError(`${name} must be YYYY-MM-DD`);
  if (from > to) throw new UsageError("--from is after --to");
  return { from, to };
}

async function videosFor(api, values) {
  const videos = [...(values.video ?? [])];
  if (values.slug?.length) {
    const overview = await api.overview();
    for (const slug of values.slug) {
      const video = overview.videos.find((item) => item.slug === slug);
      if (!video) throw new UsageError(`no video on YouTube with the slug ${slug}`);
      videos.push(video.video_id);
    }
  }
  return videos;
}

function needsOwner(problem) {
  return /yt-analytics|重新連結|連結 YouTube/.test(problem ?? "");
}

async function cmdOverview(api, values, ctx) {
  const view = await api.overview();
  if (values.json) {
    ctx.stdout.write(`${JSON.stringify(view, null, 2)}\n`);
  } else {
    ctx.stdout.write(`channel: ${view.channel_title ?? "(not linked)"}${view.channel_id ? ` (${view.channel_id})` : ""}\n`);
    ctx.stdout.write(`analytics granted: ${view.analytics_granted ? "yes" : "no"}; last complete sync: ${view.synced_at ?? "never"}${view.sync_due ? " (due)" : ""}\n`);
    for (const item of view.reports) ctx.stdout.write(`  ${item.report_type_id}: ${item.days} days, ${item.first_day} to ${item.last_day}, ${item.rows} rows\n`);
    for (const item of view.waiting_for_first_report) ctx.stdout.write(`  ${item.report_type_id}: scheduled, no report yet\n`);
    ctx.stdout.write(`videos on YouTube known to the site: ${view.videos.length}\n`);
    if (view.problem) ctx.stdout.write(`problem: ${view.problem}\n`);
  }
  if (view.problem && needsOwner(view.problem)) return EXIT.owner;
  return EXIT.ok;
}

async function cmdSync(api, values, ctx) {
  const limit = values.limit ? Number(values.limit) : undefined;
  if (limit !== undefined && !(Number.isInteger(limit) && limit >= 1 && limit <= 400)) throw new UsageError("--limit is 1 to 400");
  let force = Boolean(values.force);
  let total = 0;
  for (let round = 0; round < MAX_SYNC_ROUNDS; round += 1) {
    const result = await api.sync({ force, ...(limit ? { limit } : {}) });
    total += result.downloaded + result.replaced;
    if (result.status === "needs_relink" || result.status === "not_linked") {
      ctx.stderr.write(`sync: ${result.problem}\n`);
      return EXIT.owner;
    }
    if (result.status === "partial" && !result.remaining) {
      ctx.stderr.write(`sync: ${result.problem ?? "stopped early"}\n`);
      return EXIT.external;
    }
    if (result.status !== "partial") {
      ctx.stdout.write(`sync: ${result.status}, ${total} files downloaded or updated${result.jobs_created.length ? `; scheduled ${result.jobs_created.join(", ")}` : ""}\n`);
      return EXIT.ok;
    }
    // More files wait: the next round goes on where this one stopped.
    force = true;
  }
  ctx.stdout.write(`sync: ${total} files so far; run sync again for the rest\n`);
  return EXIT.ok;
}

async function cmdRows(api, values, ctx) {
  if (!values.report) throw new UsageError("rows needs --report");
  const format = values.format ?? "csv";
  if (!["csv", "json"].includes(format)) throw new UsageError("--format is csv or json");
  const { from, to } = defaultSpan(values, ctx.now());
  const result = await readRows(api, { report: values.report, start: from, end: to, videos: await videosFor(api, values) });
  const text = format === "json" ? `${JSON.stringify(result)}\n` : toCsv(result);
  if (values.out) {
    mkdirSync(path.dirname(path.resolve(values.out)), { recursive: true });
    writeFileSync(values.out, text);
    ctx.stderr.write(`rows: ${result.rows.length} rows of ${result.report_type_id} (${result.days.length} days) -> ${values.out}${result.truncated ? " (truncated: ask for fewer days)" : ""}\n`);
  } else {
    ctx.stdout.write(text);
  }
  return EXIT.ok;
}

async function cmdExport(api, values, ctx) {
  if (!values.out) throw new UsageError("export needs --out");
  const days = values.days ? Number(values.days) : 28;
  if (!(Number.isInteger(days) && days >= 1 && days <= 730)) throw new UsageError("--days is 1 to 730");
  const overview = await api.overview();
  mkdirSync(values.out, { recursive: true });
  writeFileSync(path.join(values.out, "overview.json"), `${JSON.stringify(overview, null, 2)}\n`);
  const { to } = defaultSpan({}, ctx.now());
  const from = addDays(to, -(days - 1));
  const families = values.report?.length ? values.report : [...new Set(overview.reports.map((item) => item.family).filter(Boolean))];
  for (const family of families) {
    const result = await readRows(api, { report: family, start: from, end: to });
    writeFileSync(path.join(values.out, `${family}.csv`), toCsv(result));
    ctx.stdout.write(`export: ${family}.csv ${result.rows.length} rows (${result.days.length} days, ${result.report_type_id})${result.truncated ? " truncated" : ""}\n`);
  }
  if (!families.length) ctx.stdout.write("export: no report yet; run sync, and give YouTube a day or two after the first one\n");
  writeFileSync(path.join(values.out, "README.txt"), `${overview.policy}\nDays ${from} to ${to}, Pacific time. Exported ${ctx.now().toISOString()}.\n`);
  return overview.problem && needsOwner(overview.problem) ? EXIT.owner : EXIT.ok;
}

const COMMANDS = {
  overview: [cmdOverview, { json: { type: "boolean" } }],
  sync: [cmdSync, { force: { type: "boolean" }, limit: { type: "string" } }],
  rows: [cmdRows, { report: { type: "string" }, from: { type: "string" }, to: { type: "string" }, video: { type: "string", multiple: true }, slug: { type: "string", multiple: true }, format: { type: "string" }, out: { type: "string" } }],
  export: [cmdExport, { out: { type: "string" }, days: { type: "string" }, report: { type: "string", multiple: true } }],
};

export async function main(argv, overrides = {}) {
  const ctx = { env: process.env, stdout: process.stdout, stderr: process.stderr, now: () => new Date(), ...overrides };
  const [command = "overview", ...args] = argv;
  if (["help", "--help", "-h"].includes(command)) {
    ctx.stdout.write(HELP);
    return EXIT.ok;
  }
  if (!Object.hasOwn(COMMANDS, command)) {
    ctx.stderr.write(`unknown command "${command}"; run with --help\n`);
    return EXIT.usage;
  }
  const { site, token } = readCredentials({ env: ctx.env, home: ctx.home });
  if (!token) {
    ctx.stderr.write("youtube-reports: no video tool token; run `node tools/video/cli.mjs login` first, or set MOKAAIR_VIDEO_TOKEN\n");
    return EXIT.usage;
  }
  const [handler, options] = COMMANDS[command];
  try {
    const { values } = parseArgs({ args, options, allowPositionals: false, strict: true });
    return await handler(client({ site, token, fetchImpl: ctx.fetchImpl ?? globalThis.fetch }), values, ctx);
  } catch (error) {
    if (error instanceof UsageError || error?.code?.startsWith?.("ERR_PARSE_ARGS")) {
      ctx.stderr.write(`${error.message}\n`);
      return EXIT.usage;
    }
    if (error instanceof SiteError || error?.name === "TimeoutError" || error instanceof TypeError) {
      ctx.stderr.write(`youtube-reports: ${error.message}\n`);
      return EXIT.external;
    }
    throw error;
  }
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).then((code) => {
    process.exitCode = code;
  });
}
