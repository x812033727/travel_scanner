// C04-C06 have unresolved pre-ledger paid history treated as full exposure;
// C07/C10/C15 have approved ceilings but no account. These six need explicit
// review before activation. All other everyday stories have no paid account or
// approval yet, so the whole series remains held locally. The current API
// independently rejects attributed calls; the local hold also protects a new
// CLI talking to an older API that treats an unknown slug as an ordinary video.
//
// C03 Moleskine was activated by the owner on 2026-10-24: its pre-ledger
// exposure is closed at the full US$25 ceiling on the host ledger, and the
// film may buy what finishes it (one narration line, then unpaid steps). The
// API still refuses it until that settlement is applied, so the local client
// sends the attributed request and lets the server answer.
//
// The C11 UCC remake was activated by the owner on 2026-10-26: a new film with
// no pre-ledger history, its own US$25 account from migration 0140.
export const EVERYDAY_STORY_PREFIX = "story-everyday-";
export const ACTIVATED_STORY_SLUGS = Object.freeze([
  "story-everyday-moleskine-c03",
  "story-everyday-ucc-c11-remake-20261025",
]);
export const PREPRODUCTION_HOLD_SLUGS = Object.freeze([
  "story-everyday-bubble-wrap-c04",
  "story-everyday-kincho-c05",
  "story-everyday-play-doh-c06",
  "story-everyday-dr-martens-c07",
  "story-everyday-oxo-c10",
  "story-everyday-frixion-c15",
]);

export const isPreproductionHeld = (slug) => typeof slug === "string"
  && slug.startsWith(EVERYDAY_STORY_PREFIX)
  && !ACTIVATED_STORY_SLUGS.includes(slug);
