#!/usr/bin/env node
import { readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";
import { buildPlans, DIRECTORY, findPlan, ROOT, validatePlans } from "./plans.mjs";
import { checkDurationReview } from "./review.mjs";

try {
  const [command, ...args] = process.argv.slice(2);
  const { values } = parseArgs({ args, options: { catalog: { type: "string" }, id: { type: "string" } }, strict: true });
  if (!["build", "check", "plan", "inputs"].includes(command)) throw new Error("use build | check | plan --catalog NAME --id ID | inputs --catalog NAME --id ID");
  const expected = buildPlans();
  const destination = path.join(ROOT, DIRECTORY, "plans.json");
  if (command === "build") {
    writeFileSync(destination, `${JSON.stringify(expected, null, 2)}\n`);
    console.log(`Built ${expected.totals.entries} duration plans; originals preserved. No media, imports or scheduling.`);
  } else {
    const current = JSON.parse(readFileSync(destination, "utf8"));
    const problems = [...validatePlans(current, expected), ...checkDurationReview()];
    if (problems.length) throw new Error(problems.join("; "));
    if (command === "check") console.log(`PASS: all ${current.totals.entries} plans; 600/780-second targets, 480-second measured minimums, original source hashes and covered status.`);
    else {
      const entry = findPlan(current, values.catalog, values.id, { forProduction: command === "inputs" });
      if (command === "inputs" && !entry.backend_inputs) throw new Error(`${entry.catalog}/${entry.id}: use the catalog's ${entry.stage} workflow; no one-off request is ready`);
      console.log(JSON.stringify(command === "inputs" ? entry.backend_inputs : entry, null, 2));
    }
  }
} catch (error) {
  console.error(`FAIL: ${error.message}`);
  process.exitCode = 1;
}
