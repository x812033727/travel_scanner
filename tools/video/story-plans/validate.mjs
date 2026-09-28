#!/usr/bin/env node
// Check a brand-story plan, and compile it (docs/videos/STORY.md §企劃清單與集數列).
//
//   node tools/video/story-plans/validate.mjs            check the plan and that stories.json is current
//   node tools/video/story-plans/validate.mjs --write    compile stories.json and SCHEDULE.md, then check
//   node tools/video/story-plans/validate.mjs --partial  while writing: check only the stories present
//   node tools/video/story-plans/validate.mjs --format   rewrite every story file with its fields in order
//   node tools/video/story-plans/validate.mjs --fetch    also read every source (network; by hand only)
//   node tools/video/story-plans/validate.mjs --hash A01 print the hash a review of that story records
//   node tools/video/story-plans/validate.mjs --only A01,B18  report only these stories' problems
//
// --plan <dir> names another plan directory; --report <file> keeps what --fetch read, as JSON.
// The exit code is 1 when anything is wrong.
import { writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

import { EDITORIAL_USER_AGENT, pageReader } from "../automation/fetch.mjs";
import { linkChecker } from "../qa/links.mjs";
import { canonical, compile, compiledCurrent, DEFAULT_PLAN, loadPlan, planProblems, reviewerOnly, scheduleMarkdown, serialize, storyHash } from "./plan.mjs";

// The check reads a page with the worker's own reader (tools/video/automation/fetch.mjs), under
// the worker's name: what the reader cannot turn into text, the worker's fact check cannot rest
// on, whatever status the page answers with.
export const USER_AGENT = EDITORIAL_USER_AGENT;
// A page that answers with less text than this is drawn by a script the reader does not run.
export const MIN_PAGE_CHARS = 400;
const HOSTS_AT_ONCE = 8;

/** What the reader's answer means: { status, readable, chars, error? }. */
export function reading(page) {
  const chars = page.ok ? page.text.length : 0;
  const readable = page.ok && chars >= MIN_PAGE_CHARS;
  const error = page.ok ? (readable ? null : `only ${chars} characters of text`) : page.error;
  return { status: page.status, readable, chars, ...(error ? { error } : {}) };
}

const transient = (result) => result.status === 0 || result.status === 429 || result.status >= 500;

/**
 * Read every source as the worker will: one page of a host at a time (the reader keeps the gap
 * between them), several hosts at once, and a second try for a page that timed out or answered
 * with a server's error. The results come in the plan's order:
 * [{ id, index, url, status, readable, chars, error? }]. Status 200 with `readable` false is a
 * page that is there and gives the worker no text: a PDF, a page over the reader's size, or one
 * a script draws. A page the reader gave up on (a ten-megabyte report does not arrive within
 * its time) is asked for once more the way the finished video's link check asks
 * (tools/video/qa/links.mjs, which waits for the status and not for the page): when that opens,
 * the source is there and unreadable, not dead. `onPage(result, page)` is handed each page as
 * the reader returned it, for a caller that wants the text.
 */
export async function fetchSources(plan, { fetchImpl = globalThis.fetch, hosts = HOSTS_AT_ONCE, log = () => {}, onPage = () => {}, sleep, now } = {}) {
  const clocks = { ...(sleep ? { sleep } : {}), ...(now ? { now } : {}) };
  const read = pageReader({ fetchImpl, ...clocks });
  const opens = linkChecker({ fetchImpl, ...clocks });
  const results = [];
  const queues = new Map();
  for (const entry of plan.stories) {
    (entry.story?.sources ?? []).forEach((source, index) => {
      const result = { id: entry.id, index, url: source?.url, status: 0, readable: false, chars: 0 };
      results.push(result);
      let host;
      try {
        host = new URL(result.url).host;
      } catch {
        result.error = "not a URL";
        return;
      }
      if (!queues.has(host)) queues.set(host, []);
      queues.get(host).push(result);
    });
  }
  const ask = async (result, again) => {
    delete result.error;
    const page = await read(result.url);
    Object.assign(result, reading(page));
    onPage(result, page);
    log(`${result.id} ${result.status} ${result.readable ? "text" : `no text (${result.error})`}${again ? " again" : ""} ${result.url}`);
  };
  const asLink = async (result) => {
    const link = await opens(result.url);
    if (!link.ok) return;
    result.status = link.status;
    result.error = `the link opens, the reader gave up: ${result.error}`;
    log(`${result.id} ${result.status} no text (${result.error}) ${result.url}`);
  };
  const waiting = [...queues.values()];
  const drain = async () => {
    for (let queue = waiting.shift(); queue; queue = waiting.shift()) {
      for (const result of queue) {
        await ask(result, false);
        if (transient(result)) await ask(result, true);
        if (result.status === 0) await asLink(result);
      }
    }
  };
  await Promise.all(Array.from({ length: Math.min(hosts, waiting.length) }, drain));
  return results;
}

/**
 * What the readings mean for the plan: a source that does not answer is a dead link in the
 * description and fails the finished video's link check; a fact none of whose pages the worker
 * can read is one its fact check cannot confirm, unless the story's review lists it in
 * `reviewer_only` (the reviewer looked for a page the worker can read and there is none). The
 * list is held to the readings both ways: a fact on it that has a readable page comes off.
 */
export function fetchProblems(plan, results) {
  const problems = [];
  const read = new Map();
  for (const result of results) {
    read.set(`${result.id} ${result.index}`, result);
    if (result.status !== 200) problems.push(`${result.id}: sources[${result.index}] ${result.url} ${result.status ? `answered ${result.status}` : `could not be read (${result.error})`}`);
  }
  for (const entry of plan.stories) {
    const listed = new Set(reviewerOnly(entry.review));
    (entry.story?.must_verify ?? []).forEach((claim, index) => {
      const cited = (Array.isArray(claim?.sources) ? claim.sources : []).map((each) => read.get(`${entry.id} ${each}`)).filter(Boolean);
      const there = cited.filter((each) => each.status === 200);
      const readable = there.find((each) => each.readable);
      if (listed.has(index)) {
        if (readable) problems.push(`${entry.id}: must_verify[${index}] is in the review's reviewer_only, but the worker can read sources[${readable.index}]: take it off the list`);
      } else if (there.length && !readable) {
        problems.push(`${entry.id}: must_verify[${index}] cites only pages the worker cannot read (${there.map((each) => `sources[${each.index}]: ${each.error}`).join("; ")}): cite one it can read as well, or list the fact in the review's reviewer_only when there is none`);
      }
    });
  }
  return problems;
}

/** The facts the worker takes on the plan's word, as [{ id, index, core, claim }]. */
export function reviewerOnlyFacts(plan) {
  return plan.stories.flatMap((entry) =>
    reviewerOnly(entry.review)
      .filter((index) => entry.story?.must_verify?.[index])
      .map((index) => ({ id: entry.id, index, core: entry.story.must_verify[index].core === true, claim: entry.story.must_verify[index].claim })),
  );
}

export async function main(argv, { stdout = process.stdout, stderr = process.stderr, fetchImpl = globalThis.fetch } = {}) {
  const { values } = parseArgs({ args: argv, options: { plan: { type: "string" }, write: { type: "boolean" }, partial: { type: "boolean" }, fetch: { type: "boolean" }, format: { type: "boolean" }, hash: { type: "string" }, only: { type: "string" }, report: { type: "string" } }, strict: true });
  const dir = values.plan ? path.resolve(values.plan) : DEFAULT_PLAN;
  let plan = loadPlan(dir);
  if (values.hash) {
    const entry = plan.stories.find((each) => each.id === values.hash);
    if (!entry?.story) {
      stderr.write(`${values.hash} is not a story of this plan, or its file is not valid JSON\n`);
      return 1;
    }
    stdout.write(`${storyHash(entry.story)}\n`);
    return 0;
  }
  const only = values.only ? new Set(values.only.split(",").map((each) => each.trim()).filter(Boolean)) : null;
  if (values.format) {
    for (const entry of plan.stories) if (entry.story) writeFileSync(entry.file, `${JSON.stringify(canonical(entry.story), null, 2)}\n`);
    plan = loadPlan(dir);
  }
  if (values.write) {
    writeFileSync(path.join(dir, "stories.json"), serialize(compile(plan)));
    writeFileSync(path.join(dir, "SCHEDULE.md"), scheduleMarkdown(plan));
  }
  // With --only, the plan is read as a whole (a slug may clash with another story's) and the
  // report keeps the lines that name one of the stories asked for.
  const all = planProblems(plan, values.partial || only ? { expected: null } : {});
  const problems = only ? all.filter((problem) => only.has(problem.split(":")[0])) : all;
  if (!values.partial && !only && !compiledCurrent(plan)) problems.push("stories.json or SCHEDULE.md is missing or older than its sources: run validate.mjs --write");
  const sound = plan.stories.filter((entry) => entry.story);
  const counts = {};
  for (const entry of sound) counts[entry.story.category] = (counts[entry.story.category] ?? 0) + 1;
  stdout.write(`${sound.length} stories (${Object.entries(counts).map(([category, count]) => `${category} ${count}`).join(", ") || "none"}); ${(plan.schedule.days ?? []).length} days scheduled\n`);
  if (values.fetch) {
    const asked = only ? { ...plan, stories: plan.stories.filter((entry) => only.has(entry.id)) } : plan;
    const results = await fetchSources(asked, { fetchImpl, log: (line) => stdout.write(`${line}\n`) });
    if (values.report) writeFileSync(path.resolve(values.report), `${JSON.stringify(results, null, 2)}\n`);
    const unread = results.filter((result) => result.status === 200 && !result.readable).length;
    stdout.write(`${results.length} sources read: ${results.filter((result) => result.readable).length} give the worker text, ${unread} answer without text, ${results.filter((result) => result.status !== 200).length} do not answer\n`);
    problems.push(...fetchProblems(asked, results));
    const taken = reviewerOnlyFacts(asked);
    if (taken.length) stdout.write(`${taken.length} facts rest on documents the worker cannot read (the review's reviewer_only): ${[...new Set(taken.map((fact) => fact.id))].join(", ")}\n`);
  }
  for (const problem of problems) stderr.write(`PROBLEM ${problem}\n`);
  stdout.write(`${problems.length} problems\n`);
  return problems.length ? 1 : 0;
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  main(process.argv.slice(2)).then((code) => {
    process.exitCode = code;
  });
}
