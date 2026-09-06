import { cache } from "react";
import {
  defaultUsageCatalog,
  isUsageCatalog,
  normalizeUsageCatalog,
  type UsageCatalogState,
  type UsageOperation,
} from "@/lib/usage-catalog";

export async function loadUsageCatalog(locale: string): Promise<UsageCatalogState> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${apiBase}/api/v1/usage-catalog?locale=${encodeURIComponent(locale)}`, {
      cache: "no-store",
      headers: { Accept: "application/json" },
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

export const getUsageCatalog = cache(loadUsageCatalog);
