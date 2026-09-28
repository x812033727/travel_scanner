// `auto`: the pipeline running from the owner's settings (docs/videos/AUTOMATION.md). Each run
// does units of work until nothing can move — every video waits on the owner, or a new draft is
// not due yet — and exits; the worker's loop starts it again a few minutes later. `--once` does
// a single unit, for trying it by hand. After the units, once a run, the tidy clears the work
// files of the oldest video finished long enough ago (tidy.mjs); `tidy` runs that by hand, and
// `tidy --dry-run` only says what would go.
import { parseArgs } from "node:util";

import { ROOT, stopRequested } from "../core/paths.mjs";
import { AutomationError, automationClient } from "./client.mjs";
import { Automation } from "./flow.mjs";
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

export async function run(command, args, ctx) {
  if (command === "tidy") return tidy(args, ctx);
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { once: { type: "boolean" } }, strict: true }).values;
  try {
    const api = automationClient(ctx);
    const settings = await api.settings();
    if (!settings.enabled) {
      ctx.stdout.write("automatic drafts are off in the settings on /admin/videos; nothing to do\n");
      return EXIT.ok;
    }
    const automation = new Automation(ctx, api, settings);
    let stopped = false;
    for (let unit = 0; unit < (values.once ? 1 : MAX_UNITS_PER_RUN); unit++) {
      if (stopRequested(automation.workBase)) {
        ctx.stdout.write("STOP found; stopping between units\n");
        stopped = true;
        break;
      }
      const done = await automation.step();
      if (!done) {
        ctx.stdout.write("nothing to do now: every video waits on the owner, or the next draft is not due\n");
        break;
      }
      ctx.stdout.write(`${done}\n`);
      // The unit could not move and would fail the same way right now: wait for the next round.
      if (automation.halted) break;
    }
    // Once a round, after the units and whether or not any moved; a STOP file stops it too.
    if (!stopped && !stopRequested(automation.workBase)) for (const line of tidyAfterRound(ctx, automation.site)) ctx.stdout.write(`${line}\n`);
    return EXIT.ok;
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return error.who === "owner" ? EXIT.owner : EXIT.external;
  }
}
