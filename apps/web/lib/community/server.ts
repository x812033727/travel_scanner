import "server-only";
import { cache } from "react";
import { closedCommunity, type CommunityState, type CommunityFlags } from "./types";

export async function loadCommunityState(): Promise<CommunityState> {
  const base = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${base}/api/v1/community/status`, {
      cache: "no-store", signal: AbortSignal.timeout(5000), headers: { Accept: "application/json" },
    });
    if (!response.ok) return closedCommunity;
    const flags: unknown = await response.json();
    if (!flags || typeof flags !== "object" || Object.keys(closedCommunity.flags).some(
      (key) => typeof (flags as Record<string, unknown>)[key] !== "boolean",
    )) return closedCommunity;
    return { status: "ready", flags: flags as CommunityFlags };
  } catch { return closedCommunity; }
}
export const getCommunityState = cache(loadCommunityState);
