import { cache } from "react";
import {
  closedSiteVisibility,
  type SiteVisibility,
  type SiteVisibilityState,
} from "@/lib/site-features";

const REQUIRED_VISIBILITY_FIELDS = [
  "hotspots_enabled",
  "trips_enabled",
  "alerts_enabled",
  "flight_status_enabled",
  "airline_fares_enabled",
  "pricing_enabled",
] as const;

const OPTIONAL_VISIBILITY_FIELDS = [
  "flight_search_enabled",
  "videos_enabled",
  "member_features_enabled",
] as const;

function parseSiteVisibility(value: unknown): SiteVisibility | null {
  if (typeof value !== "object" || value === null) return null;
  const record = value as Record<string, unknown>;
  if (!REQUIRED_VISIBILITY_FIELDS.every((field) => typeof record[field] === "boolean")) {
    return null;
  }
  for (const field of OPTIONAL_VISIBILITY_FIELDS) {
    if (record[field] !== undefined && typeof record[field] !== "boolean") {
      return null;
    }
  }
  return {
    hotspots_enabled: record.hotspots_enabled as boolean,
    trips_enabled: record.trips_enabled as boolean,
    alerts_enabled: record.alerts_enabled as boolean,
    flight_status_enabled: record.flight_status_enabled as boolean,
    airline_fares_enabled: record.airline_fares_enabled as boolean,
    pricing_enabled: record.pricing_enabled as boolean,
    flight_search_enabled: (record.flight_search_enabled as boolean | undefined) ?? false,
    videos_enabled: (record.videos_enabled as boolean | undefined) ?? false,
    member_features_enabled: (record.member_features_enabled as boolean | undefined) ?? false,
  };
}

/**
 * The last answer the settings service actually gave this process.
 *
 * Module scope on purpose, and unlike the client store in `lib/discovery-status.server.ts`
 * this is safe: every value here came from the API itself, so the worst it can do is repeat
 * something that was true moments ago. It exists because the failure mode without it is
 * silent and expensive -- a 3 s timeout made `featureEnabled` answer false, which put
 * `noindex` on /hotspots, /pricing, /flights/status and /labs/airlines and dropped the same
 * routes from that request's sitemap. One slow moment while Googlebot is reading is enough
 * for it to record the URL as noindexed, and it keeps believing that long after the blip.
 */
let lastGood: { features: SiteVisibility; readAt: number } | null = null;

/**
 * How long a remembered answer may stand in for a live one. Long enough to cover an API
 * restart or a slow moment, short enough that closing a feature in the admin console still
 * takes effect promptly when the service is reachable -- a successful read always wins and
 * replaces this immediately.
 */
const STALE_LIMIT_MS = 10 * 60 * 1000;

/** Tests only: the snapshot is process state, so a case that needs a cold start must say so. */
export function resetSiteVisibilitySnapshot() {
  lastGood = null;
}

export async function loadSiteVisibility(): Promise<SiteVisibilityState> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1/runtime/site-visibility`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
      signal: AbortSignal.timeout(3_000),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload: unknown = await response.json();
    const parsed = parseSiteVisibility(payload);
    if (!parsed) throw new Error("Invalid site visibility response");
    lastGood = { features: parsed, readAt: Date.now() };
    return { status: "ready", features: parsed };
  } catch {
    if (lastGood && Date.now() - lastGood.readAt < STALE_LIMIT_MS) {
      return { status: "stale", features: lastGood.features };
    }
    // Nothing known: no read has ever succeeded here, or the last one is too old to stand
    // behind. Only now is closing everything the honest answer.
    return { status: "unavailable", features: closedSiteVisibility };
  }
}

export const getSiteVisibility = cache(loadSiteVisibility);
