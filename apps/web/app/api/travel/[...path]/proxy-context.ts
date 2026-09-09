const SUPPORTED_LOCALES = new Set(["en", "ja", "ko", "zh-TW", "zh-CN"]);

const RENEWAL_FALLBACK_MAX_AGE = 60 * 60;
const RENEWAL_CAP_MAX_AGE = 60 * 60 * 24;
const STEP_UP_CAP_MAX_AGE = 5 * 60;

/** The token from an upstream `Set-Cookie`, when the API slid the session forward. */
/**
 * The locale the API should answer in. The page the browser is showing wins (the client
 * sends it as X-Travel-Locale on every call), then the preference remembered at sign-in,
 * then the catalog's own language. Without the header an anonymous reader of /en or /ja
 * got Chinese city names in every select, because the cookie only exists after sign-in.
 */
/**
 * The browser's analytics session id, when it sent one that is actually an id.
 *
 * It travels so an event the API records for this call lands on the same session hash
 * as the page views around it. The value is client-controlled and ends up as an HMAC
 * input on the other side, so anything but a UUID is dropped rather than forwarded:
 * a caller that can choose the hash input can group other people's rows under it.
 */
export function forwardedAnalyticsSession(value: string | null): string | null {
  if (!value) return null;
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value) ? value : null;
}

export function upstreamLocale(requested: string | null | undefined, remembered: string | null | undefined): string {
  if (requested && SUPPORTED_LOCALES.has(requested)) return requested;
  if (remembered && SUPPORTED_LOCALES.has(remembered)) return remembered;
  return "zh-TW";
}

export function renewedSession(upstream: Response): { token: string; maxAge: number } | null {
  for (const cookie of upstream.headers.getSetCookie()) {
    const token = /^travel_access=([^;]+)/.exec(cookie)?.[1];
    if (!token) continue;
    const declared = Number(/;\s*max-age=(\d+)/i.exec(cookie)?.[1]);
    const maxAge = Number.isFinite(declared) && declared > 0
      ? Math.min(declared, RENEWAL_CAP_MAX_AGE)
      : RENEWAL_FALLBACK_MAX_AGE;
    return { token: decodeURIComponent(token), maxAge };
  }
  return null;
}

/** Copy the API's HttpOnly step-up cookie without exposing its token to JavaScript. */
export function stepUpSession(upstream: Response): { token: string; maxAge: number } | null {
  for (const cookie of upstream.headers.getSetCookie()) {
    const rawToken = /^admin_step_up=([^;]+)/.exec(cookie)?.[1];
    if (!rawToken) continue;
    const token = decodeURIComponent(rawToken);
    if (token.length < 16 || token.length > 4096 || !/^[A-Za-z0-9._~-]+$/.test(token)) return null;
    const declared = Number(/;\s*max-age=(\d+)/i.exec(cookie)?.[1]);
    return {
      token,
      maxAge: Number.isFinite(declared) && declared > 0
        ? Math.min(declared, STEP_UP_CAP_MAX_AGE)
        : STEP_UP_CAP_MAX_AGE,
    };
  }
  return null;
}
