#!/usr/bin/env node
// Compile the twenty everyday C stories only after independent, hash-bound plan review.
// --draft checks structure for editing; stories.draft.json must never be imported.
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import { createHash } from "node:crypto";
import path from "node:path";
import { fileURLToPath } from "node:url";

import {
  STORY_KEYS, reviewProblems, seriesProblems, storyProblems,
} from "../../../tools/video/story-plans/plan.mjs";

const here = path.dirname(fileURLToPath(import.meta.url));
const IDs = Array.from({ length: 20 }, (_, index) => `C${String(index + 1).padStart(2, "0")}`);
const draft = process.argv.includes("--draft");
const read = (file) => JSON.parse(readFileSync(path.join(here, file), "utf8"));
const stableJson = (value) => JSON.stringify(value, (_key, item) => item && !Array.isArray(item) && typeof item === "object"
  ? Object.fromEntries(Object.keys(item).sort().map((key) => [key, item[key]])) : item);
const digest = (value) => createHash("sha256").update(stableJson(value)).digest("hex");
const problems = [];
const reviewCertification = [];
const series = read("series.json");
problems.push(...seriesProblems(series).map((problem) => `series: ${problem}`));
if (series.slug !== "brand-stories-everyday-reversals" || series.planned_episodes !== IDs.length) {
  problems.push("series must keep the everyday reversals slug and twenty planned episodes");
}
if (series.target_minutes !== 10 || series.image_model !== "image-01" ||
    JSON.stringify(series.look) !== JSON.stringify({ preset: "cute-mystery" })) {
  problems.push("series must use 10 minutes, image-01 and exactly the cute-mystery look");
}

const rows = IDs.map((id, index) => {
  const file = path.join("episodes", `${id}.json`);
  if (!existsSync(path.join(here, file))) {
    problems.push(`${id}: episode plan is missing`);
    return null;
  }
  const row = read(file);
  const base = Object.fromEntries(STORY_KEYS.map((key) => [key, row[key]]));
  base.must_verify = (base.must_verify ?? []).map(({ reviewer_only, ...claim }) => claim);
  problems.push(...storyProblems(base, id, { seriesSlug: series.slug }).map((problem) => `${id}: ${problem}`));
  // The independent receipt also binds the author's caveats. They are imported for the
  // worker to read, so changing one after review must invalidate that receipt.
  const source = { ...base, caveats: row.caveats };
  if (row.number !== index + 1 || row.publish?.day !== index + 1 || row.publish?.slot !== "12:00") {
    problems.push(`${id}: number and noon publish day must follow the twenty-film order`);
  }
  const c08Short = id === "C08" && row.slug === "story-everyday-kikkoman-c08-short-v8";
  const c20Short = id === "C20" && row.slug === "story-everyday-zippo-c20-short-v8";
  if (typeof row.slug !== "string" || (!(c08Short || c20Short) && (!/^story-everyday-[a-z0-9-]+-c\d{2}$/.test(row.slug) ||
      !row.slug.endsWith(`-${id.toLowerCase()}`)))) {
    problems.push(`${id}: slug must be distinct story-everyday-...-${id.toLowerCase()}`);
  }
  if (!draft) {
    const reviewFile = path.join("episodes", "reviews", `${id}.json`);
    if (!existsSync(path.join(here, reviewFile))) {
      problems.push(`${id}: independent source review is missing`);
    } else {
      const review = read(reviewFile);
      problems.push(...reviewProblems(review, source, id).map((problem) => `${id}: ${problem}`));
      const reviewerOnly = new Set(review.reviewer_only ?? []);
      row.must_verify = source.must_verify.map((claim, claimIndex) =>
        reviewerOnly.has(claimIndex) ? { ...claim, reviewer_only: true } : claim);
      const editorCaveats = typeof row.caveats === "string" ? row.caveats.trim() : "";
      const reviewCaveats = typeof review.notes === "string" ? review.notes.trim() : "";
      if (row.caveats !== editorCaveats) problems.push(`${id}: author caveats must be trimmed before review`);
      row.caveats = editorCaveats === reviewCaveats
        ? editorCaveats
        : [editorCaveats, reviewCaveats].filter(Boolean).join("\n\n");
      if (Array.from(row.caveats).length > 800) problems.push(`${id}: combined caveats exceed 800 characters`);
      reviewCertification.push({ id, number: row.number, reviewer: review.reviewer,
        reviewed: review.reviewed, source_story_sha256: review.story_sha256,
        compiled_story_sha256: digest(row), author_caveats: editorCaveats,
        review_notes: reviewCaveats });
    }
  }
  return row;
});

const realRows = rows.filter(Boolean);
if (new Set(realRows.map((row) => row.slug)).size !== realRows.length) problems.push("episode slugs must differ");
if (problems.length) {
  for (const problem of problems) process.stderr.write(`${problem}\n`);
  process.exitCode = 1;
} else {
  const name = draft ? "stories.draft.json" : "stories.json";
  const bundle = { schema_version: 1, series, stories: realRows };
  if (!draft) bundle.review_certification = {
    series_slug: series.slug, status: "independent-verified", entries: reviewCertification,
  };
  writeFileSync(path.join(here, name), `${JSON.stringify(bundle, null, 2)}\n`);
  process.stdout.write(`${name}: ${realRows.length} rows, structural checks passed${draft ? "; independent reviews pending; do not import" : "; independent reviews bound"}\n`);
}
