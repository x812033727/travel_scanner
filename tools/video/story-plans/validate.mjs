#!/usr/bin/env node
// Check a brand-story plan, and compile it (docs/videos/STORY.md §企劃清單與集數列).
//
//   node tools/video/story-plans/validate.mjs            check the plan and that stories.json is current
//   node tools/video/story-plans/validate.mjs --write    compile stories.json and SCHEDULE.md, then check
//   node tools/video/story-plans/validate.mjs --partial  while writing: check only the stories present
//   node tools/video/story-plans/validate.mjs --format   rewrite every story file with its fields in order
//   node tools/video/story-plans/validate.mjs --fetch    also request every source (network; by hand only)
//   node tools/video/story-plans/validate.mjs --hash A01 print the hash a review of that story records
//   node tools/video/story-plans/validate.mjs --only A01,B18  report only these stories' problems
//
// --plan <dir> names another plan directory. The exit code is 1 when anything is wrong.
import { writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import { fileURLToPath } from "node:url";

import { canonical, compile, compiledCurrent, DEFAULT_PLAN, loadPlan, planProblems, scheduleMarkdown, serialize, storyHash } from "./plan.mjs";

// The worker reads pages under this name (docs/videos/AUTOMATION.md); a source it cannot fetch
// is no use to it, so the check asks the same way.
export const USER_AGENT = "Mokaair-editorial/1.0 (https://mokaair.com; support@mokaair.com)";
const HOST_GAP_MS = 1100;
const TIMEOUT_MS = 20_000;

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

/** Request every source once, one host at a time with a gap; returns [{ id, url, status | error }]. */
export async function fetchSources(plan, { fetchImpl = globalThis.fetch, gap = HOST_GAP_MS, log = () => {} } = {}) {
  const last = new Map();
  const results = [];
  for (const entry of plan.stories) {
    for (const source of entry.story?.sources ?? []) {
      let host = "";
      try {
        host = new URL(source.url).hostname;
      } catch {
        results.push({ id: entry.id, url: source.url, error: "not a URL" });
        continue;
      }
      const wait = (last.get(host) ?? 0) + gap - Date.now();
      if (wait > 0) await sleep(wait);
      last.set(host, Date.now());
      try {
        const response = await fetchImpl(source.url, { headers: { "User-Agent": USER_AGENT, Accept: "text/html,application/pdf;q=0.9,*/*;q=0.8" }, redirect: "follow", signal: AbortSignal.timeout(TIMEOUT_MS) });
        results.push({ id: entry.id, url: source.url, status: response.status });
        log(`${entry.id} ${response.status} ${source.url}`);
      } catch (error) {
        results.push({ id: entry.id, url: source.url, error: error.message });
        log(`${entry.id} ERROR ${source.url}: ${error.message}`);
      }
    }
  }
  return results;
}

export async function main(argv, { stdout = process.stdout, stderr = process.stderr } = {}) {
  const { values } = parseArgs({ args: argv, options: { plan: { type: "string" }, write: { type: "boolean" }, partial: { type: "boolean" }, fetch: { type: "boolean" }, format: { type: "boolean" }, hash: { type: "string" }, only: { type: "string" } }, strict: true });
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
    const results = await fetchSources(asked, { log: (line) => stdout.write(`${line}\n`) });
    for (const result of results) {
      if (result.error) problems.push(`${result.id}: ${result.url} could not be read (${result.error})`);
      else if (result.status !== 200) problems.push(`${result.id}: ${result.url} answered ${result.status}`);
    }
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
