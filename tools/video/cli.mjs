#!/usr/bin/env node
// The automated YouTube video pipeline, one subcommand per stage (docs/videos/DESIGN.md).
//
// The core commands live in ./core. Media stages live in their own directories and are built by
// their own tickets; until one exists, its command says which ticket builds it and exits with
// the "missing tool" code, so an agent following `status` knows the gap is expected.
import { randomInt } from "node:crypto";
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { approve, GATES } from "./core/approvals.mjs";
import { docDir, resolveWorkdir, ROOT, UsageError } from "./core/paths.mjs";
import { eachLine, LINE_ID } from "./core/schema.mjs";
import { StageError, runCaptions } from "./core/stages.mjs";
import { lintProject, loadProject, pipelineStatus } from "./core/state.mjs";

export const EXIT = { ok: 0, lint: 1, usage: 2, owner: 3, external: 4, missing: 5 };

const HERE = path.dirname(fileURLToPath(import.meta.url));

// Stage commands built outside the core: command -> [directory, ticket that builds it].
export const AREAS = {
  login: ["tts", "2026-09-24-video-tts-azure"],
  tts: ["tts", "2026-09-24-video-tts-azure"],
  audition: ["tts", "2026-09-24-video-tts-azure"],
  "check-audio": ["tts", "2026-09-24-video-audio-check"],
  render: ["render", "2026-09-24-video-render-slides"],
  assemble: ["assemble", "2026-09-24-video-assemble-package"],
  review: ["review", "2026-09-24-video-assemble-package"],
  "review-push": ["review", "2026-09-25-video-tool-pushes-reviews-and-pulls"],
  "review-pull": ["review", "2026-09-25-video-tool-pushes-reviews-and-pulls"],
  "i18n-sheet": ["i18n", "2026-09-24-video-captions-i18n"],
  "i18n-merge": ["i18n", "2026-09-24-video-captions-i18n"],
  package: ["package", "2026-09-24-video-assemble-package"],
  "youtube-sync": ["youtube", "2026-09-24-video-youtube-sync"],
  auto: ["automation", "2026-09-25-video-auto-orchestrator-one-command-that"],
};

const HELP = `Automated YouTube video pipeline (docs/videos/DESIGN.md)

Usage: node tools/video/cli.mjs <command> [options]

  status   --slug S [--workdir D]                  where the video is, and the next command
  lint     --slug S | --file F [--json]            check video.json, brief.md, dictionary, YouTube limits
  ids      [--count N] [--slug S]                  fresh line ids that are not in use
  approve  --slug S --gate outline|audio|final|publish [--workdir D] [--note T]
                                                   record the owner's approval of the file as it is now
  review-push --slug S [--gate G | --report-only]  report the video to /admin/videos and submit the next gate
  review-pull --slug S [--gate G]                  record the owner's decisions made on /admin/videos
  captions --slug S [--workdir D]                  caption files for every current locale
  i18n-sheet --slug S [--locale L,L]               a translation worksheet per locale, in the work directory
  i18n-merge --slug S [--locale L,L]               write i18n/<locale>.json from filled worksheets, hashes included
  auto [--once]                                    run the pipeline from the settings on /admin/videos (docs/videos/AUTOMATION.md)

  login [--name N] [--paste | --token-file F]     pair with the site: allow the printed code on the admin card
  check-audio --slug S [--threshold 0.5] [--force]  transcribe every line; Jev judges the ones that differ
  audition, tts, review, render, assemble, package, youtube-sync
                                                   media stages, each built by its own ticket

--workdir defaults to $VIDEO_WORKDIR, then ~/mokaair-work/videos; a video's files go in <workdir>/<slug>/, outside the repository.
Exit codes: 0 ok, 1 lint or check failed, 2 usage, 3 needs the owner, 4 external service, 5 tool missing.
`;

function parse(args, options) {
  return parseArgs({ args, options, allowPositionals: false, strict: true }).values;
}

function printProblems(out, label, problems) {
  for (const problem of problems) out.write(`${label} ${problem.path || "(file)"}: ${problem.message}\n`);
}

async function cmdLint(args, ctx) {
  const values = parse(args, { slug: { type: "string" }, file: { type: "string" }, json: { type: "boolean" } });
  if (!values.slug && !values.file) throw new UsageError("lint needs --slug or --file");
  const project = loadProject({ slug: values.slug, file: values.file, root: ctx.root });
  const result = lintProject(project);
  if (values.json) {
    ctx.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
    return result.errors.length ? EXIT.lint : EXIT.ok;
  }
  ctx.stdout.write(`${project.doc.slug ?? project.file}: ${result.errors.length} errors, ${result.warnings.length} warnings\n`);
  printProblems(ctx.stdout, "ERROR", result.errors);
  printProblems(ctx.stdout, "WARN ", result.warnings);
  if (result.summary) {
    const { minutes, lines, spoken_units: units, billable_characters: billable, chapters } = result.summary;
    ctx.stdout.write(`\nEstimate: ${minutes.toFixed(1)} min, ${lines} lines, ${units} spoken units\n`);
    ctx.stdout.write(`Azure billable characters (estimate): ${billable}, ${((billable / 500_000) * 100).toFixed(1)}% of the free tier's 500,000 a month\n`);
    ctx.stdout.write(`Chapters (estimated times):\n${chapters.map((chapter) => `  ${chapter}`).join("\n")}\n`);
  }
  return result.errors.length ? EXIT.lint : EXIT.ok;
}

async function cmdStatus(args, ctx) {
  const values = parse(args, { slug: { type: "string" }, workdir: { type: "string" } });
  if (!values.slug) throw new UsageError("status needs --slug");
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: values.slug, root: ctx.root });
  const status = await pipelineStatus({ slug: values.slug, root: ctx.root, workdir });
  ctx.stdout.write(`${values.slug}  (work directory: ${workdir})\n`);
  for (const step of status.steps) {
    ctx.stdout.write(`  [${step.done ? "x" : " "}] ${step.id}${!step.done && step.note ? `: ${step.note}` : ""}\n`);
  }
  if (status.stop) ctx.stdout.write("\nA STOP file is present: stages will exit after their current unit of work.\n");
  ctx.stdout.write(status.next ? `\nNext: ${status.next.todo}\n` : "\nDone: the video is on YouTube.\n");
  return EXIT.ok;
}

export function freshIds(count, taken, random = randomInt) {
  const alphabet = "abcdefghijkmnpqrstuvwxyz23456789"; // no l, o, 0, 1: they read alike
  const ids = [];
  while (ids.length < count) {
    let id = "";
    for (let index = 0; index < 4; index++) id += alphabet[random(alphabet.length)];
    if (LINE_ID.test(id) && !taken.has(id) && !ids.includes(id)) ids.push(id);
  }
  return ids;
}

async function cmdIds(args, ctx) {
  const values = parse(args, { count: { type: "string", default: "10" }, slug: { type: "string" } });
  const count = Number(values.count);
  if (!Number.isInteger(count) || count < 1 || count > 500) throw new UsageError("--count must be 1 to 500");
  const taken = new Set();
  if (values.slug) for (const { line } of eachLine(loadProject({ slug: values.slug, root: ctx.root }).doc)) taken.add(line.id);
  ctx.stdout.write(`${freshIds(count, taken).join("\n")}\n`);
  return EXIT.ok;
}

async function cmdApprove(args, ctx) {
  const values = parse(args, { slug: { type: "string" }, gate: { type: "string" }, workdir: { type: "string" }, note: { type: "string", default: "" } });
  if (!values.slug || !values.gate) throw new UsageError("approve needs --slug and --gate");
  if (!Object.hasOwn(GATES, values.gate)) throw new UsageError(`--gate must be one of ${Object.keys(GATES).join(", ")}`);
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: values.slug, root: ctx.root });
  const entry = await approve({ gate: values.gate, docDir: docDir(values.slug, ctx.root), workdir, now: ctx.now(), note: values.note });
  ctx.stdout.write(`approved ${entry.gate}: ${entry.file} sha256 ${entry.sha256.slice(0, 12)} at ${entry.approved_at}\n`);
  return EXIT.ok;
}

async function cmdCaptions(args, ctx) {
  const values = parse(args, { slug: { type: "string" }, workdir: { type: "string" } });
  if (!values.slug) throw new UsageError("captions needs --slug");
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: values.slug, root: ctx.root });
  const manifest = runCaptions({ slug: values.slug, root: ctx.root, workdir, now: ctx.now() });
  for (const [locale, result] of Object.entries(manifest.locales)) {
    ctx.stdout.write(`${locale}: ${result.cues} cues${result.problems.length ? `, ${result.problems.length} to review` : ""}\n`);
    for (const problem of result.problems) ctx.stdout.write(`  ${problem}\n`);
  }
  for (const [locale, lines] of Object.entries(manifest.skipped)) {
    ctx.stdout.write(`${locale}: not written, ${lines.length} lines missing or older than zh-TW (${lines.join(", ")})\n`);
  }
  for (const problem of manifest.chapters) ctx.stdout.write(`chapters: ${problem}\n`);
  return manifest.chapters.length ? EXIT.lint : EXIT.ok;
}

async function delegate(command, args, ctx) {
  const [area, ticket] = AREAS[command];
  const entry = path.join(ctx.here, area, "cli.mjs");
  if (!existsSync(entry)) {
    ctx.stderr.write(`"${command}" is not built yet: ticket ${ticket} builds tools/video/${area}/.\n`);
    return EXIT.missing;
  }
  const module = await import(pathToFileURL(entry).href);
  return module.run(command, args, { ...ctx, EXIT });
}

const COMMANDS = { lint: cmdLint, status: cmdStatus, ids: cmdIds, approve: cmdApprove, captions: cmdCaptions };

export async function main(argv, overrides = {}) {
  const ctx = { root: ROOT, here: HERE, env: process.env, stdout: process.stdout, stderr: process.stderr, now: () => new Date(), ...overrides };
  const [command, ...args] = argv;
  if (!command || command === "help" || command === "--help" || command === "-h") {
    ctx.stdout.write(HELP);
    return command ? EXIT.ok : EXIT.usage;
  }
  try {
    if (Object.hasOwn(COMMANDS, command)) return await COMMANDS[command](args, ctx);
    if (Object.hasOwn(AREAS, command)) return await delegate(command, args, ctx);
    throw new UsageError(`unknown command "${command}"; run with --help`);
  } catch (error) {
    if (error instanceof UsageError || error?.code === "ERR_PARSE_ARGS_UNKNOWN_OPTION" || error?.code === "ERR_PARSE_ARGS_INVALID_OPTION_VALUE" || error?.code === "ERR_PARSE_ARGS_UNEXPECTED_POSITIONAL") {
      ctx.stderr.write(`${error.message}\n`);
      return EXIT.usage;
    }
    if (error instanceof StageError) {
      ctx.stderr.write(`${error.message}\n`);
      return error.code === "lint" ? EXIT.lint : EXIT.usage;
    }
    if (error instanceof SyntaxError) {
      ctx.stderr.write(`invalid JSON: ${error.message}\n`);
      return EXIT.lint;
    }
    throw error;
  }
}

// No top-level await here: `auto` runs sub-commands through `main` by importing this module
// (automation/flow.mjs), and importing a module that is still awaiting at its top level never
// settles. The worker's `auto` hung that way on its first approved gate (exit 13, 2026-09-25).
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).then((code) => {
    process.exitCode = code;
  });
}
