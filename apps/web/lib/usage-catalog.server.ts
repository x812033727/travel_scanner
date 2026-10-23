import { cache } from "react";
import {
  defaultUsageCatalog,
  isUsageCatalog,
  normalizeUsageCatalog,
  type UsageCatalogState,
  type UsageOperation,
} from "@/lib/usage-catalog";

const TIMEOUT_MS = 3000;

export async function loadUsageCatalog(locale: string): Promise<UsageCatalogState> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1/usage-catalog?locale=${encodeURIComponent(locale)}`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
      signal: AbortSignal.timeout(TIMEOUT_MS),
    });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload: unknown = await response.json();
    if (!isUsageCatalog(payload)) throw new Error("Invalid usage catalog response");
    const { catalog, missing } = normalizeUsageCatalog(payload);
    if (missing.length > 0) {
      // Version skew, not corruption: this web build knows an operation the API does not
      // price yet. It is charged the default cost until the API catches up.
      console.warn(
        `usage catalog from the API does not price ${missing.join(", ")}; using the default cost of ${missing
          .map((operation) => defaultCost(operation))
          .join(", ")} use(s). Deploy the API alongside this web build.`,
      );
    }
    return { status: "ready", catalog };
  } catch {
    return { status: "unavailable", catalog: null };
  }
}

function defaultCost(operation: UsageOperation): number {
  return defaultUsageCatalog.operation_costs[operation];
}

// Every page render reads the catalog from the root layout, so an uncached fetch turned each
// crawler hit into an API request and a database transaction; on 2026-10-23 a distributed
// crawl drained the API connection pool that way and took the admin console down with it.
// One fetch per locale per process every TTL is enough for prices that change by hand.
// A failure is remembered briefly so a struggling API is not asked again on every render,
// and the last good catalog keeps serving until a fetch succeeds again.
const READY_TTL_MS = 30_000;
const UNAVAILABLE_TTL_MS = 5_000;

type CacheEntry = { state: UsageCatalogState; expiresAt: number };
const entries = new Map<string, CacheEntry>();
const inflight = new Map<string, Promise<UsageCatalogState>>();

export function resetUsageCatalogCache() {
  entries.clear();
  inflight.clear();
}

export async function loadSharedUsageCatalog(locale: string): Promise<UsageCatalogState> {
  const entry = entries.get(locale);
  if (entry && entry.expiresAt > Date.now()) return entry.state;
  const pending = inflight.get(locale);
  if (pending) return pending;
  const request = loadUsageCatalog(locale).then((state) => {
    if (state.status === "ready") {
      entries.set(locale, { state, expiresAt: Date.now() + READY_TTL_MS });
      return state;
    }
    const fallback = entry?.state.status === "ready" ? entry.state : state;
    entries.set(locale, { state: fallback, expiresAt: Date.now() + UNAVAILABLE_TTL_MS });
    return fallback;
  }).finally(() => inflight.delete(locale));
  inflight.set(locale, request);
  return request;
}

export const getUsageCatalog = cache(loadSharedUsageCatalog);
