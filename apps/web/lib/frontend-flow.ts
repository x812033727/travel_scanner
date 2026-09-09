import { safeNextPath } from "./navigation";

const uuid = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;
const kinds = ["hotspot", "food", "merchant", "hotel", "article", "video"];
const keyPrefix = "mokaair-pending-plan:";
type PlanningIntent = { kind: string; id: string; returnTo: string; accountId: string; createdAt: number };

export function planningReturnPath(value: string) {
  const safe = safeNextPath(value, "/explore").replace(/^\/(?:en|ja|ko|zh-TW|zh-CN)(?=\/)/, "");
  const url = new URL(safe, "https://mokaair.invalid");
  if (!["/explore", "/hotspots", "/foods", "/destinations"].some((prefix) => url.pathname === prefix || url.pathname.startsWith(prefix + "/"))) return "/explore";
  return url.pathname + url.search + url.hash;
}

export function planningResumeUrl(returnTo: string, kind: string, id: string, tripId?: string) {
  const url = new URL(planningReturnPath(returnTo), "https://mokaair.invalid");
  // The intended item may no longer be in the first page after authentication or
  // a new trip. A detail URL reauthorizes it independently of the current feed.
  if (url.pathname === "/explore" || url.pathname.startsWith("/explore/")) url.searchParams.set("content", `${kind}:${id}`);
  url.searchParams.set("resume_action", "trip");
  url.searchParams.set("resume_item", `${kind}:${id}`);
  url.searchParams.set("resume_kind", kind);
  if (tripId && uuid.test(tripId)) url.searchParams.set("resume_trip", tripId);
  return url.pathname + url.search + url.hash;
}

/** Only an account-bound reference is persisted, never content or trip data. */
export function rememberPlanningIntent(accountId: string, kind: string, id: string, returnTo: string) {
  if (!accountId || !uuid.test(id) || !kinds.includes(kind)) return false;
  try {
    sessionStorage.setItem(keyPrefix + accountId, JSON.stringify({ accountId, kind, id, returnTo: planningReturnPath(returnTo), createdAt: Date.now() } satisfies PlanningIntent));
    return true;
  } catch { return false; }
}

/** Creating a trip only returns to a confirmation; it never adds the pending item. */
export function completedTripDestination(accountId: string, tripId: string, resume = false) {
  const fallback = `/trips/${tripId}`;
  if (!resume) return fallback;
  try {
    const raw = sessionStorage.getItem(keyPrefix + accountId);
    if (!raw) return fallback;
    const value = JSON.parse(raw) as PlanningIntent;
    sessionStorage.removeItem(keyPrefix + accountId);
    if (value.accountId !== accountId || !kinds.includes(value.kind) || !uuid.test(value.id) || typeof value.returnTo !== "string"
      || !Number.isFinite(value.createdAt) || value.createdAt > Date.now() || Date.now() - value.createdAt > 24 * 60 * 60 * 1000) return fallback;
    return planningResumeUrl(value.returnTo, value.kind, value.id, tripId);
  } catch { return fallback; }
}

export function tripDayOptions(start: string, end: string, locale: string) {
  const first = Date.parse(start + "T00:00:00Z"), last = Date.parse(end + "T00:00:00Z");
  if (!Number.isFinite(first) || !Number.isFinite(last) || last < first) return [];
  const count = Math.min(61, Math.floor((last - first) / 86400000) + 1);
  return Array.from({ length: count }, (_, index) => {
    const date = new Date(first + index * 86400000);
    return { value: date.toISOString().slice(0, 10), number: index + 1, label: date.toLocaleDateString(locale, { month: "short", day: "numeric", weekday: "short", timeZone: "UTC" }) };
  });
}
