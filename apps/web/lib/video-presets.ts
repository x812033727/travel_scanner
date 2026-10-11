// The explainer family of drama style presets: a narrator, still pictures, no cast, 8 to 20
// minutes. A plain module, so a form can ask "is this an explainer" without importing the
// settings component. The API (apps/api/app/video_automation/schemas.py EXPLAINER_PRESETS) and
// the tools (tools/video/core/drama.mjs EXPLAINER_PRESETS) keep the same list, and
// tools/video/core/explainer-family.test.mjs reads the line below to compare the three.
export const EXPLAINER_PRESETS = ["flat-explainer", "cute-cartoon", "cute-mystery"] as const;

/** Whether a style preset is one of the explainer family's. */
export const isExplainerPreset = (preset: string): boolean => (EXPLAINER_PRESETS as readonly string[]).includes(preset);
