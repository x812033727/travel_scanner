/**
 * The one place the web server asks the API whether article advertising is on.
 *
 * `proxy.ts` calls this on every matched request to decide which Content-Security-Policy to
 * emit, so it must not become a network round trip per page view — hence the short-lived
 * process-local cache. It also must not import `next/headers`, which is why this is separate
 * from `lib/adsense.server.ts`.
 *
 * Failure is always "off": a broken or slow API leaves the site exactly as it is today
 * rather than emitting a relaxed policy for a slot that will not render anyway.
 */
import { disabledAdsense, validAdsenseConfig, type AdsenseConfig } from "./adsense";

const TTL_MS = 60_000;
const TIMEOUT_MS = 1_000;
/**
 * How long a fresh answer may keep being served once refreshes start failing.
 *
 * Riding out a blip is worth it; riding out an outage is not. Past this the answer is
 * "off" — the owner's switch has to be able to take effect even when the API is unwell,
 * and an unreachable API must never be what keeps advertising running.
 */
const MAX_STALE_MS = 600_000;

let cached: { value: AdsenseConfig; at: number } | null = null;
let inFlight: Promise<AdsenseConfig> | null = null;

/** Tests only: the module-level cache outlives a single case otherwise. */
export function resetAdsenseConfigCache(): void {
  cached = null;
  inFlight = null;
}

/** The API's answer, or `null` when it could not be reached — which is not an answer. */
async function load(): Promise<AdsenseConfig | null> {
  const base = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${base}/api/v1/ads/config`, {
      headers: { Accept: "application/json" },
      cache: "no-store",
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!response.ok) return disabledAdsense;
    const config: unknown = await response.json();
    return validAdsenseConfig(config) ? config : disabledAdsense;
  } catch {
    return null;
  }
}

export async function fetchAdsenseConfig(now: number = Date.now()): Promise<AdsenseConfig> {
  if (cached && now - cached.at < TTL_MS) return cached.value;
  // One refresh at a time: a burst of requests on a cold cache must not become a burst of
  // calls to the API.
  inFlight ??= load().then((value) => {
    inFlight = null;
    // A reachable API replaces the answer and restamps it. An unreachable one does NEITHER:
    // restamping on failure would reset the clock on every attempt, so a stale "enabled"
    // would outlive any outage and the owner could never switch advertising off.
    if (value !== null) {
      cached = { value, at: now };
      return value;
    }
    if (cached && now - cached.at < MAX_STALE_MS) return cached.value;
    return disabledAdsense;
  }).catch(() => {
    // `load` catches everything, so this should be unreachable — but proxy.ts awaits this on
    // every single request, and a rejected promise left in `inFlight` would be handed to
    // every later caller too. That is the whole site down over an advertising switch.
    inFlight = null;
    return disabledAdsense;
  });
  return inFlight;
}
