// Reviewed revision of a pinned story's pronunciation dictionary (docs/videos/story-lexicon-revision.md).
//
// When a story writer uses a Latin word the story's pinned dictionary does not know, the worker saves
// the writer's suggestion as an immutable proposal, <workdir>/story/lexicon-proposals/<sha256>.json,
// and the story blocks. `reviseStoryLexicon` (lexicon-store.mjs) can publish a new version, but only
// with the SHA-256 of a review; nothing produced one. This module is that missing step:
//
//   - `inspectStoryLexiconRevision` lists the proposals (current, stale or already applied) and builds
//     a review receipt template for the current ones. It writes nothing.
//   - `applyStoryLexiconRevision` checks a filled receipt (a person, not the pipeline, decided each
//     term), builds the next dictionary bytes from the pinned version plus the accepted terms, keeps
//     the receipt's exact bytes in <workdir>/story/lexicon-reviews/<sha256>.json and publishes through
//     `reviseStoryLexicon` with that SHA-256. Without `apply` it is a dry run.
//
// Every refusal happens before a lease is taken or a byte is written. The final checks repeat under
// the project lease and the shared dictionary-writer lease, which `reviseStoryLexicon` then joins
// (both are reentrant within a process), so a second revision cannot slip in between.
import { createHash } from "node:crypto";
import { closeSync, existsSync, fsyncSync, lstatSync, mkdirSync, openSync, readFileSync, readdirSync, writeFileSync } from "node:fs";
import path from "node:path";

import { isProposableTerm } from "./lexicon.mjs";
import { workdirProof } from "./lexicon-migration.mjs";
import { reviseStoryLexicon, videoLexicon, withLexiconWriter } from "./lexicon-store.mjs";
import { docDir, stopRequested } from "./paths.mjs";
import { acquireProjectLease } from "./project-lease.mjs";
import { STORY_LEXICON_DIRECTORY, StoryLexiconError } from "./story-lexicon.mjs";

export const REVIEW_KIND = "story_lexicon_revision_review";
export const DECISIONS = ["accept", "accept_as", "reject"];
/** Names that say the pipeline reviewed itself. Any of these as a word of `reviewer` refuses. */
export const FORBIDDEN_REVIEWERS = new Set(["worker", "writer", "listener", "checker", "automation", "automated", "auto", "self", "me", "system", "pipeline", "cron", "bot", "unknown", "anonymous", "todo"]);
const REVIEW_KEYS = ["decisions", "independent", "kind", "lexicon_sha256", "proposals", "reviewed_at", "reviewer", "schema_version", "slug"];
const PROPOSAL_KEYS = ["additions", "before_sha256", "next", "schema_version", "slug"];
const HASH = /^[0-9a-f]{64}$/;
const FUTURE_SLACK_MS = 5 * 60 * 1000;

const hash = bytes => createHash("sha256").update(bytes).digest("hex");
const json = value => Buffer.from(`${JSON.stringify(value, null, 2)}\n`);
const fail = (code, detail) => { throw new StoryLexiconError(code, detail); };
const plainObject = value => value !== null && typeof value === "object" && !Array.isArray(value);
const sameKeys = (value, keys) => JSON.stringify(Object.keys(value).sort()) === JSON.stringify([...keys].sort());
export const proposalsDir = workdir => path.join(workdir, "story", "lexicon-proposals");
export const reviewsDir = workdir => path.join(workdir, "story", "lexicon-reviews");

function parse(bytes) {
  try { return JSON.parse(bytes.toString("utf8").replace(/^﻿/, "")); } catch { return undefined; }
}

/** What `proposeStoryLexicon` would add from `additions`: proposable, new, a reading or null. */
function spokenOf(term, spoken) {
  if (!isProposableTerm(term)) return undefined;
  if (spoken === null) return null;
  if (typeof spoken !== "string" || !spoken.trim() || spoken.length > 80) return undefined;
  return spoken.trim();
}

/** One proposal file, checked: its name is its SHA-256, it is this story's, and its fields are the writer's shape. */
function readProposal(file, slug, current) {
  const name = path.basename(file, ".json");
  const entry = { sha256: name, file, status: "invalid", problem: null, before_sha256: null, additions: null, pending: {} };
  const stat = lstatSync(file);
  if (!stat.isFile() || stat.isSymbolicLink()) return { ...entry, problem: "not a regular file" };
  const bytes = readFileSync(file);
  if (!HASH.test(name) || hash(bytes) !== name) return { ...entry, problem: "file name is not the SHA-256 of its bytes" };
  const value = parse(bytes);
  if (!plainObject(value) || !sameKeys(value, PROPOSAL_KEYS) || value.schema_version !== 1 || !plainObject(value.additions)
      || !plainObject(value.next) || !plainObject(value.next.terms) || !HASH.test(value.before_sha256 ?? ""))
    return { ...entry, problem: "not a story lexicon proposal" };
  if (value.slug !== slug) return { ...entry, problem: `belongs to ${JSON.stringify(value.slug)}` };
  const pending = {};
  for (const [term, spoken] of Object.entries(value.additions)) {
    const reading = spokenOf(term, spoken);
    if (reading === undefined || Object.hasOwn(current.lexicon.terms, term)) continue;
    pending[term] = reading;
  }
  const stale = value.before_sha256 !== current.lexicon_sha256;
  if (!stale) {
    // The writer's `next` was the pinned dictionary plus these terms; anything else was not made here.
    const expected = { ...current.lexicon, terms: { ...current.lexicon.terms, ...pending } };
    if (JSON.stringify(value.next) !== JSON.stringify(expected)) return { ...entry, before_sha256: value.before_sha256, additions: value.additions, problem: "its next dictionary is not the pinned one plus its additions" };
  }
  return {
    ...entry, before_sha256: value.before_sha256, additions: value.additions, pending,
    status: !Object.keys(pending).length ? "applied" : stale ? "stale" : "current",
  };
}

function listProposals(workdir, slug, current) {
  const dir = proposalsDir(workdir);
  if (!existsSync(dir)) return [];
  return readdirSync(dir).filter(name => name.endsWith(".json")).sort()
    .map(name => readProposal(path.join(dir, name), slug, current));
}

/** Each pending term of the chosen proposals, with what was proposed (a list when proposals disagree). */
function candidateTerms(proposals) {
  const terms = {};
  for (const proposal of proposals) {
    for (const [term, spoken] of Object.entries(proposal.pending)) {
      terms[term] ??= [];
      if (!terms[term].some(each => each === spoken)) terms[term].push(spoken);
    }
  }
  return Object.fromEntries(Object.entries(terms).map(([term, options]) => [term, options.length === 1 ? options[0] : options]));
}

/** Read-side checks that every mode shares; returns the pinned dictionary or a list of refusals. */
function preflight({ root, slug, workdir }) {
  const refusals = [];
  const proof = workdirProof(workdir, slug);
  if (proof) refusals.push({ code: "STORY_LEXICON_REVISION_WORKDIR_UNPROVEN", detail: proof });
  if (stopRequested(workdir)) refusals.push({ code: "LEXICON_STOPPED", detail: "a STOP file is present" });
  let current = null;
  try { current = videoLexicon({ root, slug, workdir, requireSnapshot: true }); }
  catch (error) {
    if (!(error instanceof StoryLexiconError)) throw error;
    refusals.push({ code: error.code, detail: error.message });
  }
  return { current, refusals };
}

/** The receipt a person fills in: every pending term of the chosen current proposals, undecided. */
export function reviewTemplate({ slug, current, proposals }) {
  const terms = candidateTerms(proposals);
  return {
    schema_version: 1, kind: REVIEW_KIND, slug,
    lexicon_sha256: current.lexicon_sha256,
    proposals: proposals.map(proposal => proposal.sha256),
    decisions: Object.fromEntries(Object.entries(terms).map(([term, proposed]) => [term, { proposed, decision: null }])),
    reviewer: null,
    reviewed_at: null,
    independent: false,
  };
}

/**
 * Everything the tool can say without writing: the pinned dictionary, each proposal and its
 * status, and a receipt template for the current ones (all of them, or `only`).
 */
export function inspectStoryLexiconRevision({ root, slug, workdir, only = [] }) {
  const { current, refusals } = preflight({ root, slug, workdir });
  if (!current) return { slug, lexicon_sha256: null, sequence: null, refusals, proposals: [], template: null };
  const proposals = listProposals(workdir, slug, current);
  const unknown = only.filter(sha => !proposals.some(proposal => proposal.sha256 === sha));
  for (const sha of unknown) refusals.push({ code: "STORY_LEXICON_PROPOSAL_UNKNOWN", detail: sha });
  const chosen = proposals.filter(proposal => proposal.status === "current" && (!only.length || only.includes(proposal.sha256)));
  return {
    slug, lexicon_sha256: current.lexicon_sha256, sequence: current.sequence, refusals, proposals,
    template: chosen.length ? reviewTemplate({ slug, current, proposals: chosen }) : null,
  };
}

function checkReviewer(reviewer) {
  if (typeof reviewer !== "string" || reviewer.trim().length < 2 || reviewer.length > 120) return "reviewer must name the person or independent agent who reviewed it";
  const banned = reviewer.toLowerCase().split(/[^a-z0-9]+/).filter(word => FORBIDDEN_REVIEWERS.has(word));
  return banned.length ? `reviewer ${JSON.stringify(reviewer)} names the pipeline (${banned.join(", ")}), not an independent reviewer` : null;
}

function checkTime(value, now) {
  if (typeof value !== "string" || !/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(:\d{2}(\.\d+)?)?(Z|[+-]\d{2}:\d{2})$/.test(value) || Number.isNaN(Date.parse(value)))
    return "reviewed_at must be an ISO 8601 time with a zone";
  if (Date.parse(value) > now().getTime() + FUTURE_SLACK_MS) return "reviewed_at is in the future";
  return null;
}

function checkDecision(term, entry, proposed) {
  if (!plainObject(entry)) return `${term}: the decision must be an object`;
  const allowed = new Set(["proposed", "decision", "spoken", "reason"]);
  const extra = Object.keys(entry).filter(key => !allowed.has(key));
  if (extra.length) return `${term}: unexpected field ${extra.join(", ")}`;
  if (JSON.stringify(entry.proposed) !== JSON.stringify(proposed)) return `${term}: "proposed" is not what the proposals say (${JSON.stringify(proposed)})`;
  if (!DECISIONS.includes(entry.decision)) return `${term}: decision must be one of ${DECISIONS.join(", ")}`;
  if (entry.reason !== undefined && typeof entry.reason !== "string") return `${term}: reason must be text`;
  if (entry.decision === "accept_as") {
    if (!Object.hasOwn(entry, "spoken")) return `${term}: accept_as needs "spoken" (a reading, or null for "read it as written")`;
    if (entry.spoken !== null && (typeof entry.spoken !== "string" || !entry.spoken.trim() || entry.spoken.length > 80)) return `${term}: spoken must be 1 to 80 characters, or null`;
  } else if (Object.hasOwn(entry, "spoken")) return `${term}: "spoken" belongs only to accept_as`;
  if (entry.decision === "accept" && Array.isArray(proposed)) return `${term}: the proposals disagree; choose a reading with accept_as`;
  return null;
}

/**
 * Check a receipt against the pinned dictionary and the proposals on disk. Returns
 * `{ problems: [{code, detail}], accepted, rejected, nextBytes, nextSha256 }`.
 */
export function evaluateReview({ slug, current, proposals, review, now = () => new Date() }) {
  const problems = [];
  const add = (code, detail) => problems.push({ code, detail });
  if (!plainObject(review)) return { problems: [{ code: "STORY_LEXICON_REVIEW_INVALID", detail: "the receipt must be a JSON object" }] };
  const keys = Object.keys(review).filter(key => key !== "note");
  if (!sameKeys(Object.fromEntries(keys.map(key => [key, 1])), REVIEW_KEYS) || (review.note !== undefined && typeof review.note !== "string"))
    add("STORY_LEXICON_REVIEW_INVALID", `fields must be exactly ${REVIEW_KEYS.join(", ")} (and an optional note)`);
  if (review.schema_version !== 1 || review.kind !== REVIEW_KIND) add("STORY_LEXICON_REVIEW_INVALID", `schema_version 1 and kind ${REVIEW_KIND}`);
  if (review.slug !== slug) add("STORY_LEXICON_REVIEW_SLUG_MISMATCH", `the receipt is for ${JSON.stringify(review.slug)}`);
  if (review.lexicon_sha256 !== current.lexicon_sha256) add("STORY_LEXICON_REVIEW_STALE", `the receipt reviewed ${review.lexicon_sha256}; the pinned dictionary is ${current.lexicon_sha256}`);
  const reviewer = checkReviewer(review.reviewer);
  if (reviewer) add("STORY_LEXICON_REVIEWER_INVALID", reviewer);
  const time = checkTime(review.reviewed_at, now);
  if (time) add("STORY_LEXICON_REVIEW_TIME_INVALID", time);
  if (review.independent !== true) add("STORY_LEXICON_REVIEW_NOT_INDEPENDENT", "independent must be true");

  const shas = Array.isArray(review.proposals) ? review.proposals : [];
  if (!shas.length || shas.some(sha => typeof sha !== "string") || new Set(shas).size !== shas.length)
    add("STORY_LEXICON_REVIEW_INVALID", "proposals must list one or more distinct proposal SHA-256s");
  const chosen = [];
  for (const sha of shas) {
    const proposal = proposals.find(each => each.sha256 === sha);
    if (!proposal) add("STORY_LEXICON_PROPOSAL_UNKNOWN", String(sha));
    else if (proposal.status === "stale") add("STORY_LEXICON_PROPOSAL_STALE", `${sha} was made against ${proposal.before_sha256}`);
    else if (proposal.status === "applied") add("STORY_LEXICON_PROPOSAL_APPLIED", `${sha}: every term is already pinned`);
    else if (proposal.status !== "current") add("STORY_LEXICON_PROPOSAL_INVALID", `${sha}: ${proposal.problem}`);
    else chosen.push(proposal);
  }
  if (problems.length) return { problems };

  const candidates = candidateTerms(chosen);
  const decisions = plainObject(review.decisions) ? review.decisions : null;
  if (!decisions) return { problems: [{ code: "STORY_LEXICON_REVIEW_INVALID", detail: "decisions must map each term to a decision" }] };
  const missing = Object.keys(candidates).filter(term => !Object.hasOwn(decisions, term));
  const extra = Object.keys(decisions).filter(term => !Object.hasOwn(candidates, term));
  if (missing.length || extra.length)
    add("STORY_LEXICON_REVIEW_DECISIONS_MISMATCH", [missing.length && `undecided: ${missing.join(", ")}`, extra.length && `not proposed: ${extra.join(", ")}`].filter(Boolean).join("; "));
  for (const [term, proposed] of Object.entries(candidates)) {
    if (!Object.hasOwn(decisions, term)) continue;
    const problem = checkDecision(term, decisions[term], proposed);
    if (problem) add("STORY_LEXICON_REVIEW_DECISION_INVALID", problem);
  }
  if (problems.length) return { problems };

  const accepted = {};
  const rejected = [];
  for (const [term, entry] of Object.entries(decisions)) {
    if (entry.decision === "reject") rejected.push(term);
    else accepted[term] = entry.decision === "accept" ? candidates[term] : entry.spoken === null ? null : entry.spoken.trim();
  }
  if (!Object.keys(accepted).length) return { problems: [{ code: "STORY_LEXICON_REVISION_NOTHING_ACCEPTED", detail: "every term was rejected; there is no new dictionary to publish" }], accepted, rejected };
  const nextBytes = json({ ...current.lexicon, terms: { ...current.lexicon.terms, ...accepted } });
  return { problems, accepted, rejected, nextBytes, nextSha256: hash(nextBytes) };
}

/** The SHA-256 of every review a revision event in this story's chain was published with. */
function publishedReviews(root, slug, current) {
  const events = path.join(docDir(slug, root), STORY_LEXICON_DIRECTORY, "events");
  const found = new Set();
  let sha = current.head_event_sha256;
  for (let guard = 0; sha && guard <= current.sequence; guard++) {
    const file = path.join(events, `${sha}.json`);
    const event = existsSync(file) ? parse(readFileSync(file)) : null;
    if (!event) break;
    if (event.review_sha256) found.add(event.review_sha256);
    sha = event.previous_event_sha256;
  }
  return found;
}

/** Create the receipt's immutable copy once; an existing copy must be the same bytes. */
function keepReview(file, bytes) {
  mkdirSync(path.dirname(file), { recursive: true });
  if (existsSync(file)) {
    if (!readFileSync(file).equals(bytes)) fail("LEXICON_IMMUTABLE_COLLISION", file);
    return;
  }
  const fd = openSync(file, "wx");
  try { writeFileSync(fd, bytes); fsyncSync(fd); } finally { closeSync(fd); }
  if (process.platform !== "win32") {
    const directory = openSync(path.dirname(file), "r");
    try { fsyncSync(directory); } finally { closeSync(directory); }
  }
}

function refuse(problems) {
  fail(problems[0].code, problems.map(problem => problem.detail ? `${problem.code} (${problem.detail})` : problem.code).join("; "));
}

/**
 * Check a review receipt and, with `apply`, publish the reviewed dictionary.
 * Returns `{ status: "dry_run" | "applied" | "already_applied", review_sha256, accepted, rejected, ... }`.
 * Throws StoryLexiconError for every refusal, before any lease or write.
 */
export function applyStoryLexiconRevision({ root, slug, workdir, reviewBytes, apply = false, now = () => new Date(), checkpoint }) {
  if (!Buffer.isBuffer(reviewBytes)) fail("STORY_LEXICON_REVIEW_INVALID", "the receipt must be read as bytes");
  const reviewSha256 = hash(reviewBytes);
  const review = parse(reviewBytes);
  if (review === undefined) fail("STORY_LEXICON_REVIEW_INVALID", "the receipt is not JSON");
  const { current, refusals } = preflight({ root, slug, workdir });
  if (refusals.length) refuse(refusals);
  if (publishedReviews(root, slug, current).has(reviewSha256))
    return { status: "already_applied", slug, review_sha256: reviewSha256, lexicon_sha256: current.lexicon_sha256, head_event_sha256: current.head_event_sha256 };
  const evaluated = evaluateReview({ slug, current, proposals: listProposals(workdir, slug, current), review, now });
  if (evaluated.problems.length) refuse(evaluated.problems);
  const summary = { slug, review_sha256: reviewSha256, before_sha256: current.lexicon_sha256, next_sha256: evaluated.nextSha256, accepted: evaluated.accepted, rejected: evaluated.rejected };
  if (!apply) return { status: "dry_run", ...summary };

  const lease = acquireProjectLease(workdir, { owner: "story-lexicon-revision" });
  try {
    return withLexiconWriter(root, () => {
      // Again under both leases: nothing may have changed since the checks above.
      const again = preflight({ root, slug, workdir });
      if (again.refusals.length) refuse(again.refusals);
      const check = evaluateReview({ slug, current: again.current, proposals: listProposals(workdir, slug, again.current), review, now });
      if (check.problems.length) refuse(check.problems);
      if (!check.nextBytes.equals(evaluated.nextBytes)) fail("STORY_LEXICON_REVIEW_STALE", "the proposals changed while checking");
      const reviewFile = path.join(reviewsDir(workdir), `${reviewSha256}.json`);
      keepReview(reviewFile, reviewBytes);
      const result = reviseStoryLexicon({ root, slug, workdir, nextBytes: check.nextBytes, reviewSha256, checkpoint });
      return { status: "applied", ...summary, review_file: reviewFile, lexicon_sha256: result.lexicon_sha256, head_event_sha256: result.head_event_sha256, sequence: result.sequence };
    });
  } finally { lease.release(); }
}
