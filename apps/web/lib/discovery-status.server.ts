import { cache } from "react";

/**
 * The discovery flag, resolved on the server.
 *
 * `lib/discovery.ts` reads the same switch from the browser, but its `useSyncExternalStore`
 * server snapshot is a fixed `{ enabled: false, loading: true }`, so anything behind
 * `DiscoveryHomeGate` renders as a skeleton in the response body -- on the home page that is the
 * whole `<h1>`, the hero and the destination rail. A page that knows the answer before it renders
 * can decide whether it needs that gate at all.
 *
 * `GET /discovery/status` is public and reads a setting rather than the database, so this is a
 * cheap call. It is deliberately `no-store`, like site-visibility: a switch has to take effect
 * when it is flipped, not an hour later.
 */

export type DiscoveryStatus = { enabled: boolean };

const CLOSED: DiscoveryStatus = { enabled: false };

export async function loadDiscoveryStatus(): Promise<DiscoveryStatus> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1/discovery/status`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload: unknown = await response.json();
    if (typeof payload !== "object" || payload === null) throw new Error("Invalid discovery status");
    const enabled = (payload as Record<string, unknown>).enabled;
    if (typeof enabled !== "boolean") throw new Error("Invalid discovery status");
    return { enabled };
  } catch {
    // Unreachable means fall back to the marketing home, which is the page that works without
    // the discovery service. The client store still resolves the real value after hydration.
    return CLOSED;
  }
}

export const getDiscoveryStatus = cache(loadDiscoveryStatus);
