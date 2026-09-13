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

let cached: { value: AdsenseConfig; at: number } | null = null;
let inFlight: Promise<AdsenseConfig> | null = null;

/** Tests only: the module-level cache outlives a single case otherwise. */
export function resetAdsenseConfigCache(): void {
  cached = null;
  inFlight = null;
}

async function load(): Promise<AdsenseConfig> {
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
    // Keep serving the last good answer while the API is briefly unreachable, so one slow
    // response does not flip every article page's policy for a minute.
    return cached ? cached.value : disabledAdsense;
  }
}

export async function fetchAdsenseConfig(now: number = Date.now()): Promise<AdsenseConfig> {
  if (cached && now - cached.at < TTL_MS) return cached.value;
  // One refresh at a time: a burst of requests on a cold cache must not become a burst of
  // calls to the API.
  inFlight ??= load().then((value) => {
    cached = { value, at: Date.now() };
    inFlight = null;
    return value;
  });
  return inFlight;
}
