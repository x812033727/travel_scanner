export type AnalyticsEventName =
  | "page_view"
  | "registration_completed"
  | "search_completed"
  | "trip_created"
  | "outbound_click";

export function trackAnalytics(name: Exclude<AnalyticsEventName, "page_view">) {
  if (typeof window === "undefined") return;
  window.dispatchEvent(new CustomEvent("travel:analytics", { detail: { name } }));
}
