// C03-C06 have unresolved pre-ledger paid history treated as full exposure;
// C07/C10/C15 have approved ceilings but no account. Keep all seven requests local until the account,
// old charges, exact voice/model/region, price ceiling, and all-stage attribution
// have been reviewed and enabled together.
// The API independently rejects them; this local hold also protects a new CLI talking
// to an older API that would otherwise treat an unknown slug as an ordinary video.
export const PREPRODUCTION_HOLD_SLUGS = Object.freeze([
  "story-everyday-moleskine-c03",
  "story-everyday-bubble-wrap-c04",
  "story-everyday-kincho-c05",
  "story-everyday-play-doh-c06",
  "story-everyday-dr-martens-c07",
  "story-everyday-oxo-c10",
  "story-everyday-frixion-c15",
]);

export const isPreproductionHeld = (slug) => PREPRODUCTION_HOLD_SLUGS.includes(slug);
