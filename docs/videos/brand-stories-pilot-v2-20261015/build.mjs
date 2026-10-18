#!/usr/bin/env node
// Compile the isolated A01/B18 remake only after its own hash-bound reviews exist.
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { STORY_KEYS, reviewProblems, seriesProblems, storyProblems } from "../../../tools/video/story-plans/plan.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const draft = process.argv.includes("--draft");
const write = process.argv.includes("--write");
if (draft === write) {
  process.stderr.write("choose exactly one of --draft (structural check) or --write (reviewed import file)\n");
  process.exit(1);
}
const read = (file) => JSON.parse(readFileSync(path.join(here, file), "utf8"));
const series = read("series.json");
const problems = seriesProblems(series).map((problem) => "series: " + problem);
if (series.slug !== "brand-stories-curio-pilot-v2" || series.planned_episodes !== 2 ||
    series.target_minutes !== 10 || series.image_model !== "image-01" ||
    JSON.stringify(series.look) !== JSON.stringify({ preset: "cute-mystery" })) {
  problems.push("series must keep its isolated slug, two episodes, 10 minutes, image-01 and exact cute-mystery look");
}
const ids = ["A01", "B18"];
const slugs = ["story-rolling-suitcase-v2", "story-conveyor-belt-sushi-v2"];
const rows = ids.map((id, index) => {
  const row = read(`episodes/${id}.json`);
  const source = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
  source.must_verify = source.must_verify.map(({ reviewer_only, ...claim }) => claim);
  problems.push(...storyProblems(source, id).map((problem) => `${id}: ${problem}`));
  if (row.number !== index + 1 || row.slug !== slugs[index] ||
      row.publish?.day !== index + 1 || row.publish?.slot !== "12:00") {
    problems.push(`${id}: episode identity or order differs from the isolated v2 plan`);
  }
  if (!draft) {
    const reviewFile = `episodes/reviews/${id}.json`;
    if (!existsSync(path.join(here, reviewFile))) {
      problems.push(`${id}: revised chapters have no independent hash-bound review`);
    } else {
      const review = read(reviewFile);
      problems.push(...reviewProblems(review, source, id).map((problem) => `${id}: ${problem}`));
      const reviewerOnly = new Set(review.reviewer_only ?? []);
      row.must_verify = source.must_verify.map((claim, claimIndex) =>
        reviewerOnly.has(claimIndex) ? { ...claim, reviewer_only: true } : claim);
      const caveats = [row.caveats?.trim(), review.notes?.trim()].filter(Boolean);
      row.caveats = [...new Set(caveats)].join("\n\n");
      if (row.caveats.length > 800) problems.push(`${id}: source and new reviewer caveats exceed 800 characters`);
    }
  }
  return row;
});
if (problems.length) {
  for (const problem of problems) process.stderr.write(problem + "\n");
  process.exit(1);
}
if (draft) {
  process.stdout.write("A01/B18 v2: two structurally valid rows; new independent reviews pending; no import file written\n");
} else {
  writeFileSync(path.join(here, "stories.json"), JSON.stringify({ schema_version: 1, series, stories: rows }, null, 2) + "\n");
  process.stdout.write("stories.json: two revised, independently reviewed v2 pilot rows\n");
}
