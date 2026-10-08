// The drama format's media stages: `media-status` here; `look`, `keyframes`, `clips` and `music`
// in their own modules, each built by its own ticket (docs/videos/DRAMA.md). Until a module
// exists its command says which ticket builds it and exits with the "missing tool" code, the
// way tools/video/cli.mjs does for whole areas. `stock` (stock.mjs, docs/videos/ILLUSTRATED.md
// §圖庫照片) is reached the same way, `node tools/video/cli.mjs stock …`; this file also runs on
// its own (main below).
import { existsSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { EXIT as EXIT_CODES } from "../cli.mjs";
import { docDir, readJson, resolveWorkdir, ROOT, UsageError } from "../core/paths.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { MediaError, mediaStatus } from "./client.mjs";
import { ledgerTotals } from "./ledger.mjs";
import { imageStatus } from "./stages.mjs";

const HERE = path.dirname(fileURLToPath(import.meta.url));

// Stage command -> [module file, ticket that builds it].
export const STAGES = {
  look: ["look.mjs", "2026-09-26-video-drama-look-keyframes"],
  keyframes: ["keyframes.mjs", "2026-09-26-video-drama-look-keyframes"],
  clips: ["clips.mjs", "2026-09-26-video-drama-clips-music"],
  music: ["music.mjs", "2026-09-26-video-drama-clips-music"],
  stock: ["stock.mjs", "2026-10-05-stock-photo-slides-and-attribution"],
};

const HELP = `Media commands of the video pipeline (docs/videos/DRAMA.md, docs/videos/ILLUSTRATED.md)

Usage: node tools/video/media/cli.mjs <command> [options]

  media-status [--slug S] [--json]                 what the server allows and what this video has spent
  stock search --query "Seoul skyline" [--provider pexels|pixabay] [--orientation landscape|portrait|square]
               [--per-page N] [--page N] [--slug S] [--json]
                                                   stock photo candidates with the credit each vendor asks for; nothing is downloaded
  stock fetch --slug S --provider P --id N [--workdir D] [--json]
                                                   the photo into <workdir>/stock/<sha256>.<ext> and its credit into video.json assets[]
  look, keyframes, clips, music                    the drama format's generation stages (node tools/video/cli.mjs <stage> …)

Exit codes: 0 ok, 1 lint or check failed, 2 usage, 3 needs the owner, 4 external service, 5 tool missing.
`;

export function exitFor(error, EXIT) {
  if (error.who === "owner") return EXIT.owner;
  if (error.who === "tool") return EXIT.usage;
  return EXIT.external;
}

/** The site and token every media command needs; a MediaError for the owner when there is none. */
export function requireCredentials(ctx) {
  const credentials = readCredentials({ env: ctx.env, home: ctx.home });
  if (!credentials.token) {
    throw new MediaError("no video tool token yet: run `node tools/video/cli.mjs login` and allow it on the admin card", { who: "owner" });
  }
  return credentials;
}

export function clientOptions(ctx, credentials) {
  return { site: credentials.site, token: credentials.token, fetchImpl: ctx.fetch ?? globalThis.fetch, ...(ctx.sleep ? { sleep: ctx.sleep } : {}) };
}

const money = (value) => `US$${Number(value || 0).toFixed(2)}`;

/** Print what the server allows and what this video has spent. */
export function statusText(status, totals) {
  const lines = [];
  lines.push(`drama: ${status.enabled ? "on" : "OFF (turn it on in the settings tab of /admin/videos)"}; music ${status.music_enabled ? "on" : "off"}`);
  for (const kind of ["image", "clip", "music"]) {
    const choice = status[kind];
    const shape = kind === "clip" ? ` ${choice.resolution}, ${choice.seconds} s` : "";
    lines.push(`${kind}: ${choice.provider} ${choice.model}${shape}${choice.configured === null ? " (provider key checked on submit)" : choice.configured ? "" : " (NO KEY on the site)"}`);
  }
  for (const [name, budget] of Object.entries(status.budgets ?? {})) {
    lines.push(`budget ${name}: ${budget.used} of ${budget.limit} ${budget.unit} used this month, ${budget.remaining} left`);
  }
  lines.push(`this month on the site: about ${money(status.estimated_usd)}; per-video cap ${money(status.max_usd_per_video)}; judge threshold ${status.judge_min_score}/10`);
  lines.push(`store: ${(status.store.used_bytes / 1e9).toFixed(2)} of ${(status.store.max_total_bytes / 1e9).toFixed(0)} GB${status.store.writable ? "" : " (NOT writable)"}`);
  if (totals) lines.push(`this video: ${money(totals.usd)} (${totals.images} images, ${totals.clip_seconds} clip seconds, ${totals.music} tracks, ${totals.judge_calls} judge calls)`);
  return `${lines.join("\n")}\n`;
}

async function cmdStatus(args, ctx) {
  const values = parseArgs({ args, options: { slug: { type: "string" }, workdir: { type: "string" }, json: { type: "boolean" } }, strict: true }).values;
  const credentials = requireCredentials(ctx);
  const series = values.slug ? readJson(path.join(docDir(values.slug, ctx.root), "series.json"), null) : null;
  const status = imageStatus(await mediaStatus(clientOptions(ctx, credentials)), series);
  let totals = null;
  if (values.slug) {
    const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: values.slug, root: ctx.root, home: ctx.home });
    totals = ledgerTotals(workdir);
  }
  if (values.json) ctx.stdout.write(`${JSON.stringify({ status, totals }, null, 2)}\n`);
  else ctx.stdout.write(statusText(status, totals));
  return ctx.EXIT.ok;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  try {
    if (command === "media-status") return await cmdStatus(args, ctx);
    const stage = STAGES[command];
    if (!stage) throw new UsageError(`unknown media command "${command}"`);
    const entry = path.join(ctx.mediaHere ?? HERE, stage[0]);
    if (!existsSync(entry)) {
      ctx.stderr.write(`"${command}" is not built yet: ticket ${stage[1]} builds tools/video/media/${stage[0]}.\n`);
      return EXIT.missing;
    }
    const module = await import(pathToFileURL(entry).href);
    return await module.run(command, args, ctx);
  } catch (error) {
    if (error instanceof MediaError) {
      ctx.stderr.write(`${error.message}\n`);
      return exitFor(error, EXIT);
    }
    throw error;
  }
}

/**
 * This file run on its own: the context tools/video/cli.mjs would build, and the same answers to
 * a usage mistake (exit 2). tools/video/cli.mjs is the entry point for every command here,
 * `stock` included; the media tests call this one.
 */
export async function main(argv, overrides = {}) {
  const ctx = { root: ROOT, env: process.env, stdout: process.stdout, stderr: process.stderr, now: () => new Date(), EXIT: EXIT_CODES, ...overrides };
  const [command, ...args] = argv;
  if (!command || command === "help" || command === "--help" || command === "-h") {
    ctx.stdout.write(HELP);
    return command ? ctx.EXIT.ok : ctx.EXIT.usage;
  }
  try {
    return await run(command, args, ctx);
  } catch (error) {
    if (error instanceof UsageError || error?.code === "ERR_PARSE_ARGS_UNKNOWN_OPTION" || error?.code === "ERR_PARSE_ARGS_INVALID_OPTION_VALUE" || error?.code === "ERR_PARSE_ARGS_UNEXPECTED_POSITIONAL") {
      ctx.stderr.write(`${error.message}\n`);
      return ctx.EXIT.usage;
    }
    if (error instanceof SyntaxError) {
      ctx.stderr.write(`invalid JSON: ${error.message}\n`);
      return ctx.EXIT.lint;
    }
    throw error;
  }
}

// No top-level await: a stage module imports this file back (clientOptions), and a module still
// awaiting at its top level never settles for the module that imports it.
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main(process.argv.slice(2)).then((code) => {
    process.exitCode = code;
  });
}
