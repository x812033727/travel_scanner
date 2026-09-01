import { cache } from "react";
import {
  closedSiteVisibility,
  siteFeatureKeys,
  type SiteVisibility,
  type SiteVisibilityState,
} from "@/lib/site-features";

function isSiteVisibility(value: unknown): value is SiteVisibility {
  if (typeof value !== "object" || value === null) return false;
  return siteFeatureKeys.every(
    (feature) => typeof (value as Record<string, unknown>)[`${feature}_enabled`] === "boolean",
  );
}

export async function loadSiteVisibility(): Promise<SiteVisibilityState> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1/runtime/site-visibility`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload: unknown = await response.json();
    if (!isSiteVisibility(payload)) throw new Error("Invalid site visibility response");
    return { status: "ready", features: payload };
  } catch {
    return { status: "unavailable", features: closedSiteVisibility };
  }
}

export const getSiteVisibility = cache(loadSiteVisibility);
