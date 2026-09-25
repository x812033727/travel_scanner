// `auto`: the pipeline running from the owner's settings (docs/videos/AUTOMATION.md). Each run
// does units of work until nothing can move — every video waits on the owner, or a new draft is
// not due yet — and exits; the worker's loop starts it again a few minutes later. `--once` does
// a single unit, for trying it by hand.
import { parseArgs } from "node:util";

import { stopRequested } from "../core/paths.mjs";
import { AutomationError, automationClient } from "./client.mjs";
import { Automation } from "./flow.mjs";

// A bound on one run, so a stage that keeps "succeeding" without moving cannot spin forever.
export const MAX_UNITS_PER_RUN = 40;

export async function run(command, args, ctx) {
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
    for (let unit = 0; unit < (values.once ? 1 : MAX_UNITS_PER_RUN); unit++) {
      if (stopRequested(automation.workBase)) {
        ctx.stdout.write("STOP found; stopping between units\n");
        break;
      }
      const done = await automation.step();
      if (!done) {
        ctx.stdout.write("nothing to do now: every video waits on the owner, or the next draft is not due\n");
        break;
      }
      ctx.stdout.write(`${done}\n`);
    }
    return EXIT.ok;
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return error.who === "owner" ? EXIT.owner : EXIT.external;
  }
}
