// Owner-approved whole-film ceilings whose provider route and prior charges are not yet
// reconciled. Keep these requests local until the account, exact voice/model/region,
// price ceiling, and all-stage attribution have been reviewed and enabled together.
// The API independently rejects them; this local hold also protects a new CLI talking
// to an older API that would otherwise treat an unknown slug as an ordinary video.
export const PENDING_PILOT_SLUGS = Object.freeze([
  "story-everyday-oxo-c10",
  "story-everyday-frixion-c15",
]);

export const isPendingPilotBudget = (slug) => PENDING_PILOT_SLUGS.includes(slug);
