// `auto`: the pipeline running from the owner's settings (docs/videos/AUTOMATION.md). Each run
// does units of work until nothing can move — every video waits on the owner, or a new draft is
// not due yet — and exits; the worker's loop starts it again a few minutes later. `--once` does
// a single unit, for trying it by hand. After the units, once a run, the tidy clears the work
// files of the oldest video finished long enough ago (tidy.mjs); `tidy` runs that by hand, and
// `tidy --dry-run` only says what would go. `restyle --slug S` retells one of the worker's videos
// in the storytelling register (docs/videos/ILLUSTRATED.md §說書式旁白) through the listener's
// register pass; `--dry-run` only measures the script.
import { parseArgs } from "node:util";

import { resolveWorkBase, ROOT, stopRequested, UsageError } from "../core/paths.mjs";
import { AutomationError, automationClient } from "./client.mjs";
import { Automation } from "./flow.mjs";
import { shortsStep, ShortsWorker } from "./shorts.mjs";
import { DAYS_ENV, repositories, retentionFrom, roundLines, tidyBase, tidyRound } from "./tidy.mjs";

// A bound on one run, so a stage that keeps "succeeding" without moving cannot spin forever.
export const MAX_UNITS_PER_RUN = 40;

/**
 * The tidy at the end of a round of `auto`, given the round's video list from the site: the
 * lines it prints. It never stops the worker: a file that cannot go is reported, and anything
 * unexpected ends the tidy with a line while the round ends as usual.
 */
export function tidyAfterRound(ctx, site) {
  try {
    const retention = retentionFrom(ctx.env);
    if (retention.off) return [];
    if (retention.problem) return [`tidy: not run: ${retention.problem}`];
    const where = tidyBase({ env: ctx.env, root: ctx.root, home: ctx.home });
    if (where.refused) return [`tidy: not run: ${where.refused}`];
    if (where.missing) return [];
    // ctx.tidyFs: tests hand in a file system whose removals fail; the worker uses node:fs.
    const round = tidyRound({ base: where.base, repos: repositories(ctx.root ?? ROOT), site: Array.isArray(site) ? site : null, now: ctx.now(), days: retention.days, fs: ctx.tidyFs });
    return roundLines(round);
  } catch (error) {
    return [`tidy: stopped by an error (${error.message}); the round ends as usual`];
  }
}

/** `tidy [--dry-run] [--workdir D]`: one round of the tidy by hand, with what waits and why. */
async function tidy(args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { "dry-run": { type: "boolean" }, workdir: { type: "string" } }, strict: true }).values;
  const dryRun = Boolean(values["dry-run"]);
  const retention = retentionFrom(ctx.env);
  if (retention.problem) {
    ctx.stderr.write(`${retention.problem}; nothing is cleared\n`);
    return EXIT.usage;
  }
  if (retention.off) {
    ctx.stdout.write(`${DAYS_ENV}=off: the tidy is switched off; nothing is cleared\n`);
    return EXIT.ok;
  }
  const where = tidyBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
  if (where.refused) {
    ctx.stderr.write(`${where.refused}; nothing is cleared\n`);
    return EXIT.usage;
  }
  if (where.missing) {
    ctx.stdout.write(`${where.missing} does not exist; nothing to clear\n`);
    return EXIT.ok;
  }
  if (!dryRun && stopRequested(where.base)) {
    ctx.stdout.write("STOP found in the work base; nothing is cleared\n");
    return EXIT.ok;
  }
  let site;
  try {
    site = await automationClient(ctx).videos();
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    ctx.stderr.write(`the site's video list, which dates the videos on YouTube, could not be read: ${error.message}\n`);
    return error.who === "owner" ? EXIT.owner : EXIT.external;
  }
  const round = tidyRound({ base: where.base, repos: repositories(ctx.root ?? ROOT), site, now: ctx.now(), days: retention.days, dryRun, fs: ctx.tidyFs });
  ctx.stdout.write(`work base ${where.base}; a finished video keeps its work files for ${retention.days} days\n`);
  for (const line of roundLines(round, { verbose: true })) ctx.stdout.write(`${line}\n`);
  return EXIT.ok;
}

/** `restyle --slug S [--dry-run]`: the narration retold in the storytelling register, or, dry, how far it keeps it now. */
async function restyle(args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, "dry-run": { type: "boolean" } }, strict: true }).values;
  if (!values.slug) throw new UsageError("restyle needs --slug");
  try {
    // The dry run reads files only, without a token; the live run needs the site's settings for the listener's prompt.
    const api = values["dry-run"] ? null : automationClient(ctx);
    const automation = new Automation(ctx, api, api ? await api.settings() : {});
    ctx.stdout.write(`${await automation.restyle(values.slug, { dryRun: Boolean(values["dry-run"]) })}\n`);
    return EXIT.ok;
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return error.who === "owner" ? EXIT.owner : EXIT.external;
  }
}

// How many videos the worker moves at once: the rendering, the assembly and the model calls of
// each lane share the container's memory, so it stays small.
export const MAX_LANES = 3;

/**
 * What `auto` prints when the first lane finds nothing to do. A video waiting on its own
 * (flow.mjs defer, or a writer still running on the server; `deferred` is
 * Automation.deferredVideos(): [{ slug, until }]) does not wait on the owner: it is named with
 * the time it is tried again (the next round when `until` is null: only this run left it), so a
 * round that moved nothing because of a deferral does not read as one in which the owner is
 * awaited.
 */
export function idleLine(deferred = []) {
  if (!deferred.length) return "nothing to do now: every video waits on the owner, or the next draft is not due";
  const named = deferred.map(({ slug, until }) => `${slug} until ${until ?? "the next round"}`).join(", ");
  return `nothing to do now: ${deferred.length} deferred and tried again later (${named}); the other videos wait on the owner, or the next draft is not due`;
}

/** VIDEO_WORKER_LANES as a lane count: 1 when unset or unreadable, at most MAX_LANES. */
export function laneCount(env = {}) {
  const lanes = Number.parseInt(env.VIDEO_WORKER_LANES ?? "", 10);
  return Number.isInteger(lanes) && lanes >= 1 ? Math.min(lanes, MAX_LANES) : 1;
}

export async function run(command, args, ctx) {
  if (command === "tidy") return tidy(args, ctx);
  if (command === "restyle") return restyle(args, ctx);
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { once: { type: "boolean" } }, strict: true }).values;
  try {
    const api = automationClient(ctx);
    const settings = await api.settings();
    // The Shorts go by their own settings (shorts.mjs), before the tutorials' switch is read: first
    // while the library runs low, otherwise after the tutorials and the dramas.
    const shorts = new ShortsWorker(ctx, api, settings);
    const stopNow = () => stopRequested(resolveWorkBase({ env: ctx.env, root: ctx.root, home: ctx.home }));
    const low = stopNow() ? false : await shorts.low().catch((error) => {
      ctx.stdout.write(`shorts: could not tell how full the library is (${error.message}); the Shorts go after the other videos\n`);
      return false;
    });
    if (low) await shortsStep(shorts);
    if (!settings.enabled) {
      if (!low && !stopNow()) await shortsStep(shorts);
      ctx.stdout.write("automatic drafts are off in the settings on /admin/videos; nothing to do\n");
      return EXIT.ok;
    }
    // Several lanes move different videos at once (VIDEO_WORKER_LANES, default 1); only the
    // first starts anything new, and a lane never picks a video another lane is moving, one
    // another lane set aside for this run (a deferral, flow.mjs defer), or one whose writer
    // another lane found still running on the server (pendingUntil: one lookup per round).
    const busy = new Set();
    const skipped = new Set();
    const pendingUntil = new Map();
    const lanes = Array.from({ length: laneCount(ctx.env) }, (_, index) => new Automation(ctx, api, settings, { busy, skipped, pendingUntil, secondary: index > 0 }));
    const [automation] = lanes;
    let stopped = false;
    const drive = async (lane, index) => {
      const tag = index ? `[lane ${index + 1}] ` : "";
      for (let unit = 0; unit < (values.once ? 1 : MAX_UNITS_PER_RUN); unit++) {
        if (stopRequested(lane.workBase)) {
          ctx.stdout.write(`${tag}STOP found; stopping between units\n`);
          stopped = true;
          break;
        }
        const done = await lane.step();
        if (!done) {
          if (!index) ctx.stdout.write(`${idleLine(lane.deferredVideos())}\n`);
          break;
        }
        ctx.stdout.write(`${tag}${done}\n`);
        // Nothing could move for a reason that is everyone's: wait for the next round. A video's
        // own trouble only set that video aside, and the lane takes the next unit.
        if (lane.halted) break;
      }
    };
    await Promise.all(lanes.map(drive));
    if (!low && !stopped && !stopNow()) await shortsStep(shorts);
    // Once a round, after the units and whether or not any moved; a STOP file stops it too.
    if (!stopped && !stopRequested(automation.workBase)) for (const line of tidyAfterRound(ctx, automation.site)) ctx.stdout.write(`${line}\n`);
    return EXIT.ok;
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return error.who === "owner" ? EXIT.owner : EXIT.external;
  }
}
