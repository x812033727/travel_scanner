#!/usr/bin/env node
// Lists the AI and technology news the site published for one event day, for the daily brief
// (references/daily-brief.md). Reads the public list endpoint the way earlier batch checks did:
// no login, the editorial User-Agent, 1.5 s between requests.
//
//   node .agents/skills/youtube-video/scripts/daily_news_pick.mjs [--date YYYY-MM-DD] [--json]
//
// The date is the event day (news_date), Taipei time, yesterday by default. published_at is not
// used: news is imported in batches, so a week of stories can share one publication minute.

const SITE = "https://mokaair.com";
const TOPICS = ["ai-news", "tech-news"];
const USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)";
const PAGE_LIMIT = 50;
const MAX_PAGES = 4;
const GAP_MS = 1500;

function taipeiYesterday(now = new Date()) {
  const taipei = new Date(now.getTime() + 8 * 3600 * 1000);
  taipei.setUTCDate(taipei.getUTCDate() - 1);
  return taipei.toISOString().slice(0, 10);
}

export function parseArgs(argv) {
  const args = { date: null, json: false };
  for (let index = 0; index < argv.length; index += 1) {
    if (argv[index] === "--date") args.date = argv[++index];
    else if (argv[index] === "--json") args.json = true;
    else throw new Error(`unknown argument: ${argv[index]}`);
  }
  if (args.date !== null && !/^\d{4}-\d{2}-\d{2}$/.test(args.date ?? "")) throw new Error("--date takes YYYY-MM-DD");
  return args;
}

/** The stories of one event day from the list pages of every topic, one row per slug. */
export function pickDay(pagesByTopic, date) {
  const rows = new Map();
  for (const [topic, pages] of Object.entries(pagesByTopic)) {
    for (const page of pages) {
      for (const article of page.articles ?? []) {
        if (article.news_date !== date) continue;
        const row = rows.get(article.slug);
        if (row) {
          row.topics.add(topic);
          continue;
        }
        rows.set(article.slug, {
          slug: article.slug,
          title: article.title,
          description: article.description ?? "",
          url: `${SITE}/zh-TW/life/${article.slug}`,
          topics: new Set([topic]),
        });
      }
    }
  }
  return [...rows.values()].map((row) => ({ ...row, topics: [...row.topics] }));
}

/** Whether another page could still hold the day: the list is newest news_date first. */
export function morePagesNeeded(page, date) {
  const dates = (page.articles ?? []).map((article) => article.news_date).filter(Boolean);
  return Boolean(page.next_cursor) && dates.length > 0 && dates[dates.length - 1] >= date;
}

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

async function fetchTopic(topic, date) {
  const pages = [];
  let cursor = null;
  for (let count = 0; count < MAX_PAGES; count += 1) {
    if (count > 0 || topic !== TOPICS[0]) await sleep(GAP_MS);
    const url = new URL(`${SITE}/api/travel/guides`);
    url.search = new URLSearchParams({ locale: "zh-TW", topic, sort: "news", limit: String(PAGE_LIMIT), ...(cursor ? { cursor } : {}) }).toString();
    const response = await fetch(url, { headers: { "User-Agent": USER_AGENT, Accept: "application/json" } });
    if (!response.ok) throw new Error(`${url} answered ${response.status}`);
    const page = await response.json();
    pages.push(page);
    if (!morePagesNeeded(page, date)) break;
    cursor = page.next_cursor;
  }
  return pages;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  const date = args.date ?? taipeiYesterday();
  const pagesByTopic = {};
  for (const topic of TOPICS) pagesByTopic[topic] = await fetchTopic(topic, date);
  const rows = pickDay(pagesByTopic, date);
  if (args.json) {
    process.stdout.write(`${JSON.stringify({ date, stories: rows }, null, 2)}\n`);
    return;
  }
  process.stdout.write(`${date}: ${rows.length} stories\n\n`);
  for (const row of rows) process.stdout.write(`- ${row.title}\n  ${row.description}\n  ${row.url} [${row.topics.join(", ")}]\n\n`);
}

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    process.stderr.write(`${error.message}\n`);
    process.exit(1);
  });
}
