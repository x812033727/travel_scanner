import { cache } from "react";
import { isUsageCatalog, type UsageCatalogState } from "@/lib/usage-catalog";

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
    return { status: "ready", catalog: payload };
  } catch {
    return { status: "unavailable", catalog: null };
  }
}

export const getUsageCatalog = cache(loadUsageCatalog);
