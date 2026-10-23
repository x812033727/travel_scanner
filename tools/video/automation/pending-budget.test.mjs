import assert from "node:assert/strict";
import test from "node:test";

import { PREPRODUCTION_HOLD_SLUGS } from "../core/pending-pilot-budget.mjs";
import { automationClient } from "./client.mjs";

test("held everyday paid model and Jev stages stop before contacting an older API", async () => {
  for (const slug of PREPRODUCTION_HOLD_SLUGS) {
    let calls = 0;
    const client = automationClient({
      home: process.cwd(),
      root: process.cwd(),
      env: {
        MOKAAIR_SITE: "https://example.test",
        MOKAAIR_VIDEO_TOKEN: `mkv_${"t".repeat(43)}`,
      },
      fetch: async () => { calls += 1; return Response.json({ unexpected: true }); },
    });
    for (const send of [
      () => client.run("writer", slug, "write", {}),
      () => client.judgePolicy({ slug, script: "旁白" }),
      () => client.judgeOutline({ slug, brief: "企劃", options: [] }),
      () => client.retryRuns(slug),
    ]) {
      await assert.rejects(send(), (error) => error.code === "video_budget_preproduction_hold" && error.who === "owner");
    }
    assert.equal(calls, 0, slug);
  }
});
