export const TEXT_SIZE_STORAGE_KEY = "mokaair-text-size";
export const TEXT_SIZE_CHANGE_EVENT = "mokaair:text-size";

export const textSizes = ["standard", "large", "largest"] as const;
export type TextSize = (typeof textSizes)[number];

export function isTextSize(value: unknown): value is TextSize {
  return typeof value === "string" && textSizes.includes(value as TextSize);
}

/**
 * Runs before first paint, next to the theme bootstrap, so a reader who chose
 * larger text never sees the page render small and then jump.
 */
export const TEXT_SIZE_BOOTSTRAP_SCRIPT = `(function(){var r=document.documentElement;var s="standard";try{var v=localStorage.getItem("${TEXT_SIZE_STORAGE_KEY}");if(v==="large"||v==="largest")s=v}catch(e){}r.dataset.textSize=s})()`;
