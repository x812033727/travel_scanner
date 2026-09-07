import { cache } from "react";
import { isUiTextPayload, type UiTextEntries } from "@/lib/ui-text";

export type UiTextState = {
  status: "ready" | "unavailable";
  version: string | null;
  entries: UiTextEntries;
};

// Fail open: the bundled catalogs are the default, so an API that is down or slow costs
// the overrides, not the page. The timeout keeps a hung API from holding every render.
const EMPTY: UiTextState = { status: "unavailable", version: null, entries: {} };
const TIMEOUT_MS = 2000;

export async function loadUiTextOverrides(locale: string): Promise<UiTextState> {
  const apiBase = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(
      `${apiBase}/api/v1/runtime/ui-text?locale=${encodeURIComponent(locale)}`,
      {
        cache: "no-store",
        headers: { Accept: "application/json" },
        signal: AbortSignal.timeout(TIMEOUT_MS),
      },
    );
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const payload: unknown = await response.json();
    if (!isUiTextPayload(payload)) throw new Error("Invalid ui text response");
    return { status: "ready", version: payload.version, entries: payload.entries };
  } catch {
    return EMPTY;
  }
}

// Per-request memo only. next-intl can build its request config twice in one request —
// generateMetadata asks with an explicit locale while the layout asks without one — and
// this keeps that to a single call. There is deliberately no cross-request cache: the API
// invalidates its own Redis copy on every write, so an edit shows on the next render.
export const getUiTextOverrides = cache(loadUiTextOverrides);
