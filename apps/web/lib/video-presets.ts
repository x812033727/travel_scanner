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
// it; tools/video/core/explainer-family.test.mjs reads the line below to compare the two. Keyed
// by string: the request form does not offer the cute presets until they have their own prompts.
export const PRESET_IMAGE_MODEL: Readonly<Record<string, string>> = { "cute-cartoon": "image-01", "cute-mystery": "image-01" };

// Not yet a choice for the settings' default style: a drama that carries no preset of its own takes
// the default, and these two have no prompts of their own before pull request 3 of
// docs/videos/explainer-route/DESIGN.md; they join the select with it (ticket 2026-10-11-settings-default-style-offers-explainer-presets).
export const DEFAULT_STYLE_HELD_PRESETS: readonly string[] = ["cute-cartoon", "cute-mystery"];

/** The presets the default-style select offers: the held ones left out, the saved value always kept. */
export const defaultStyleChoices = (presets: readonly string[], saved: string): string[] =>
  presets.filter((preset) => preset === saved || !DEFAULT_STYLE_HELD_PRESETS.includes(preset));
