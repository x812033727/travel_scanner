// C03-C06 have unresolved pre-ledger paid history treated as full exposure;
// C07/C10/C15 have approved ceilings but no account. These seven need explicit
// review before activation. All other everyday stories have no paid account or
// approval yet, so the whole series remains held locally. The current API
// independently rejects attributed calls; the local hold also protects a new
// CLI talking to an older API that treats an unknown slug as an ordinary video.
export const EVERYDAY_STORY_PREFIX = "story-everyday-";
export const PREPRODUCTION_HOLD_SLUGS = Object.freeze([
  "story-everyday-moleskine-c03",
  "story-everyday-bubble-wrap-c04",
  "story-everyday-kincho-c05",
  "story-everyday-play-doh-c06",
  "story-everyday-dr-martens-c07",
  "story-everyday-oxo-c10",
  "story-everyday-frixion-c15",
]);

export const isPreproductionHeld = (slug) => typeof slug === "string" && slug.startsWith(EVERYDAY_STORY_PREFIX);
