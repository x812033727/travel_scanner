export const STAY22_SCRIPT_URL = "https://scripts.stay22.com/letmeallez.js";
export const STAY22_SCRIPT_ELEMENT_ID = "stay22-lma";
export function isStay22LmaId(value: unknown): value is string {
  return typeof value === "string" && /^[0-9a-f]{24}$/.test(value);
}

export type Stay22ScriptConfig = {
  enabled: boolean;
  integration_mode: "allez" | "script";
  lma_id: string | null;
};

export const disabledStay22Script: Stay22ScriptConfig = {
  enabled: false, integration_mode: "allez", lma_id: null,
};

export function isStay22ScriptOrigin(value: string): boolean {
  try {
    const url = new URL(value);
    return !url.username && !url.password && ["https://mokaair.com", "https://www.mokaair.com"].includes(url.origin);
  } catch { return false; }
}

export function validStay22ScriptConfig(value: unknown): value is Stay22ScriptConfig {
  if (!value || typeof value !== "object") return false;
  const config = value as Partial<Stay22ScriptConfig>;
  return typeof config.enabled === "boolean"
    && (config.integration_mode === "allez" || config.integration_mode === "script")
    && (config.lma_id === null || isStay22LmaId(config.lma_id))
    && (!config.enabled || (config.integration_mode === "script" && isStay22LmaId(config.lma_id)));
}

export function privacyBlocksStay22(signals: { doNotTrack?: string | null; globalPrivacyControl?: boolean }) {
  return signals.doNotTrack === "1" || signals.globalPrivacyControl === true;
}

/** The SDK can read document.referrer; clean props alone cannot hide a private source URL. */
export function isSafeStay22Referrer(referrer: string, origin: string): boolean {
  if (!referrer) return true;
  try {
    const url = new URL(referrer);
    if (!isStay22ScriptOrigin(origin) || url.origin !== origin || url.username || url.password || url.search || url.hash) return false;
    return url.pathname === "/"
      || /^\/(?:en|ja|ko|zh-TW|zh-CN)\/?$/.test(url.pathname)
      || /^\/(?:en|ja|ko|zh-TW|zh-CN)\/destinations\/(?:tokyo|osaka|kyoto|osaka-kyoto|seoul|busan|taipei)\/services\/?$/.test(url.pathname);
  } catch { return false; }
}

/** Only server-reviewed originals belong in this public script document. */
export function isOriginalHotelUrl(value: string): boolean {
  try {
    const url = new URL(value);
    return url.protocol === "https:" && !url.username && !url.password && !url.search && !url.hash
      && url.hostname !== "stay22.com" && !url.hostname.endsWith(".stay22.com");
  } catch { return false; }
}
