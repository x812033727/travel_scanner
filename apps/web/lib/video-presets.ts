// The explainer family of drama style presets: a narrator, still pictures, no cast, 8 to 20
// minutes. A plain module, so a form can ask "is this an explainer" without importing the
// settings component. The API (apps/api/app/video_automation/schemas.py EXPLAINER_PRESETS) and
// the tools (tools/video/core/drama.mjs EXPLAINER_PRESETS) keep the same list, and
// tools/video/core/explainer-family.test.mjs reads the line below to compare the three.
export const EXPLAINER_PRESETS = ["flat-explainer", "cute-cartoon", "cute-mystery"] as const;

/** Whether a style preset is one of the explainer family's. */
export const isExplainerPreset = (preset: string): boolean => (EXPLAINER_PRESETS as readonly string[]).includes(preset);

// The image model a one-off of this preset is drawn with when its request names none: the cute
// looks are positive-only text written for MiniMax image-01. The server stores the same id
// (apps/api/app/video_automation/schemas.py PRESET_IMAGE_MODELS) and the request form preselects
// it; tools/video/core/explainer-family.test.mjs reads the line below to compare the two. A
// preset listed here never follows the drama settings' model, so the form offers no such entry.
export const PRESET_IMAGE_MODEL: Readonly<Record<string, string>> = { "cute-cartoon": "image-01", "cute-mystery": "image-01" };
