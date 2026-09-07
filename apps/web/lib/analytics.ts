export type AnalyticsEventName =
  | "page_view"
  | "registration_completed"
  | "search_completed"
  | "outbound_click"
  | "discover_requested"
  | "login_resumed";

/** Where the browser keeps the id it reports events under; see AnalyticsProvider. */
export const ANALYTICS_SESSION_KEY = "travel_analytics_session";
export const ANALYTICS_SESSION_HEADER = "X-Travel-Analytics-Session";

/**
 * The id this browser reports analytics under, or null when there is not one yet.
 *
 * Read-only on purpose: only the provider creates the id, and only once it knows the
 * visitor has not opted out. An API call is not a reason to start tracking someone,
 * so this never writes. `sessionStorage` throws in some privacy modes rather than
 * returning null, hence the catch.
 */
export function analyticsSessionId(): string | null {
  if (typeof window === "undefined") return null;
  try {
    return sessionStorage.getItem(ANALYTICS_SESSION_KEY);
  } catch {
    return null;
  }
}

export function trackAnalytics(name: Exclude<AnalyticsEventName, "page_view">) {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new CustomEvent("travel:analytics", { detail: { name } }));
}
