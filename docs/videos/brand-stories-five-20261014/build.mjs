#!/usr/bin/env node
// Build the five-film story import only from reviewed episode rows.
// --draft writes a structurally checked file for local dry-run; never import it with --apply.
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  STORY_KEYS, reviewProblems, seriesProblems, storyProblems,
} from "../../../tools/video/story-plans/plan.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const IDs = ["A29", "A16", "A37", "B14", "A21"];
const draft = process.argv.includes("--draft");
const read = (file) => JSON.parse(readFileSync(path.join(here, file), "utf8"));
const problems = [];
const series = read("series.json");
problems.push(...seriesProblems(series).map((problem) => "series: " + problem));
if (series.slug !== "brand-stories-curio-five" || series.style_preset !== "custom") {
  problems.push("series must keep the five-film slug and custom six-chapter story writer");
}
if (series.target_minutes !== 10 || series.image_model !== "image-01" ||
    JSON.stringify(series.look) !== JSON.stringify({ preset: "cute-mystery" })) {
  problems.push("series must use 10 minutes, image-01 and exactly the cute-mystery look");
}

const rows = IDs.map((id, index) => {
  const row = read(path.join("episodes", id + ".json"));
  const source = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
  // The prior review's reviewer_only flags are compiled metadata, not part of an author's plan.
  source.must_verify = source.must_verify.map(({ reviewer_only, ...claim }) => claim);
  problems.push(...storyProblems(source, id).map((problem) => id + ": " + problem));
  if (row.number !== index + 1 || row.publish?.day !== index + 1 || row.publish?.slot !== "12:00") {
    problems.push(id + ": number and noon publish day must follow the five-film order");
  }
  if (!row.slug?.startsWith("story-five-")) problems.push(id + ": needs a distinct story-five- slug");
  if (!draft) {
    const reviewFile = path.join("episodes", "reviews", id + ".json");
    if (!existsSync(path.join(here, reviewFile))) {
      problems.push(id + ": new six-chapter text has no independent review");
    } else {
      const review = read(reviewFile);
      problems.push(...reviewProblems(review, source, id).map((problem) => id + ": " + problem));
      const reviewerOnly = new Set(review.reviewer_only ?? []);
      row.must_verify = source.must_verify.map((claim, claimIndex) =>
        reviewerOnly.has(claimIndex) ? { ...claim, reviewer_only: true } : claim);
      // The editor's fact boundaries and the independent review both guide the writer. Neither
      // replaces the other, and the API allows at most 800 characters of compiled caveats.
      const editorCaveats = typeof row.caveats === "string" ? row.caveats.trim() : "";
      const reviewCaveats = typeof review.notes === "string" ? review.notes.trim() : "";
      row.caveats = editorCaveats === reviewCaveats
        ? editorCaveats
        : [editorCaveats, reviewCaveats].filter(Boolean).join("\n\n");
      if (row.caveats.length > 800) problems.push(id + ": combined caveats exceed API's 800-character limit");
    }
  }
  return row;
});

if (new Set(rows.map((row) => row.slug)).size !== IDs.length) problems.push("five episode slugs must differ");
if (problems.length) {
  for (const problem of problems) process.stderr.write(problem + "\n");
  process.exitCode = 1;
} else {
  const name = draft ? "stories.draft.json" : "stories.json";
  writeFileSync(path.join(here, name), JSON.stringify({ schema_version: 1, series, stories: rows }, null, 2) + "\n");
  process.stdout.write(name + ": five rows, structural checks passed" +
    (draft ? "; reviews pending; do not --apply\n" : "; five independent reviews bound\n"));
}
