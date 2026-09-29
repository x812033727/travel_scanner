// Verification evidence follows the narrative and its timing, not media prompts.
import { createHash } from "node:crypto";

import { narrativeHash } from "./screenplay.mjs";
import { speechHash } from "./timeline.mjs";

export function scriptCheckBinding(doc) {
  return {
    narrative_hash: narrativeHash(doc),
    script_hash: createHash("sha256").update(JSON.stringify([
      narrativeHash(doc), speechHash(doc, null),
    ])).digest("hex"),
  };
}

export function scriptCheckMatches(check, doc) {
  const current = scriptCheckBinding(doc);
  return Boolean(check && check.narrative_hash === current.narrative_hash && check.script_hash === current.script_hash);
}

// A report the worker wrote before reports named their script: a verdict, and no hash to compare.
export function scriptCheckUnbound(check) {
  return Boolean(check) && check.narrative_hash === undefined && check.script_hash === undefined;
}
