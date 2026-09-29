// What the Shorts tab of /admin/videos reads and sends (docs/videos/SHORTS.md): the shapes of
// apps/api/app/video_shorts/schemas.py, and the few rules the page applies itself. No markup
// here, so the tab and every one of its views can import it without importing each other.

export const SHORTS_LINES = ["lab", "cut", "drama"] as const;
export type ShortsLine = (typeof SHORTS_LINES)[number];
export const SHORTS_STATES = ["needs_you", "making", "library", "missed", "slotted", "scheduled", "published", "dropped"] as const;
export type ShortsState = (typeof SHORTS_STATES)[number];
export type SlotStatus = "open" | "planned" | "assigned" | "locked" | "scheduled" | "published" | "missed" | "skipped";
export const VIEWS = ["calendar", "library", "metrics", "costs", "settings"] as const;
export type View = (typeof VIEWS)[number];
export const SHORTS_LOCALES = ["en", "ja", "ko", "zh-CN"] as const;
export type ShortsLocale = (typeof SHORTS_LOCALES)[number];

export type Slot = {
  id: string; starts_at: string; local_date: string; local_time: string; phase: number;
  line: ShortsLine | null; series: string | null; topic_slug: string | null;
  project_slug: string | null; project_title: string | null; project_line: ShortsLine | null; youtube_video_id: string | null;
  status: SlotStatus; locked_at: string | null; note: string | null;
};
export type SlotsView = { timezone: string; slots: Slot[] };
export type SlotAction = "move" | "assign" | "clear" | "skip" | "reopen" | "note";

export type Budget = {
  period_start: string; period_end: string; spent_ntd: number; reserved_ntd: number; unknown: number; limit_ntd: number; soft_ntd: number;
  total_start: string; total_spent_ntd: number; total_limit_ntd: number; paid_work_allowed: boolean; reason: string | null;
};
export type NeedKind = "consent" | "channel" | "worker" | "missed" | "budget" | "upload" | "review" | "blocked" | "stock";
export type Need = { kind: NeedKind; detail: string; slug?: string | null; count?: number };
export type AutopublishState = "off" | "on" | "paused" | "expiring" | "expired" | "invalid";
export type Overview = {
  autopublish: AutopublishState; autopublish_problem: string | null; consent_expires_at: string | null; paused_at: string | null;
  timezone: string; today: Slot[]; tomorrow: Slot[];
  stock: { count: number; days: number | null; wanted_days: number };
  budget: Budget;
  channel: { linked: boolean; title: string | null; audited: boolean; problem: string | null };
  worker_seen_at: string | null;
  campaign: { start: string | null; last_day: string | null; slots: number; published: number; missed: number };
  needs: Need[]; needs_count: number;
};

export type UploadWaiting = { slug: string; title: string; line: ShortsLine | null; slot_at: string; file_name: string; size: number | null; seconds: number | null };
export type Uploads = { ahead_days: number; items: UploadWaiting[] };
export type ClaimResult = "matched" | "duplicate" | "not_found" | "not_private" | "length_differs";
export type ClaimItem = { slug: string; file_name: string; result: ClaimResult; detail: string; youtube_video_id: string | null };
export type ClaimAnswer = { claimed: number; items: ClaimItem[] };
export type RecallItem = { slug: string; youtube_video_id: string; recalled: boolean; detail: string };
export type RecallAnswer = { recalled: number; items: RecallItem[] };

export const COST_CATEGORIES = ["narration", "models", "checks", "media", "image", "clip", "music", "subscription", "tool", "other"] as const;
export type CostCategory = (typeof COST_CATEGORIES)[number];
export type CostStatus = "confirmed" | "reserved" | "unknown";
export type Cost = {
  id: string; occurred_at: string; project_slug: string | null; category: string; amount: number | null; currency: string; fx_rate: number | null;
  amount_ntd: number | null; status: CostStatus; source: "auto" | "manual"; units: Record<string, unknown> | null; note: string | null; created_at: string;
};
export type PeriodTotal = { start: string; end: string; spent_ntd: number; reserved_ntd: number; unknown: number; lines: number };
export type Costs = { items: Cost[]; budget: Budget; periods: PeriodTotal[] };

export const METRIC_PERIODS = ["d1", "d3", "d7", "now"] as const;
export type MetricPeriod = (typeof METRIC_PERIODS)[number];
export type MetricSource = "data_api" | "analytics_api" | "studio_export";
export type Metric = {
  period: MetricPeriod; source: MetricSource; captured_at: string;
  views: number | null; likes: number | null; comments: number | null;
  engaged_views?: number | null; shares?: number | null; subscribers_gained?: number | null;
  avg_view_seconds?: number | null; avg_view_percent?: number | null; stayed_percent?: number | null;
};
export type ShortMetrics = {
  slug: string; title: string; line: ShortsLine | null; series: string | null; youtube_video_id: string;
  published_at: string | null; removed_at: string | null; snapshots: Metric[];
};
export type Metrics = { items: ShortMetrics[] };

export type Voice = { provider: "azure" | "gemini"; name: string; style: string | null; model: string | null; rate: string };
export type PatternSegment = { days: number; counts: number[] };
export type ShortsSettingsBody = {
  enabled: boolean; lines: ShortsLine[]; weekly_quota: Partial<Record<ShortsLine, number>>;
  daily_pattern: PatternSegment[]; slot_times: string[]; timezone: string;
  stock_days: number; lock_hours: number; upload_ahead_days: number; max_per_day: number; seconds_min: number; seconds_max: number;
  voice: Voice; locales: ShortsLocale[]; made_for_kids: boolean; auto_approve: boolean;
  budget_ntd_30d: number; budget_soft_ntd: number; budget_total_ntd: number;
};
export type ConsentState = "none" | "valid" | "expiring" | "expired" | "invalid";
export type ConsentOffer = { text: string; text_sha256: string; scope: Record<string, unknown> };
export type Consent = {
  state: ConsentState; problem: string | null; granted_at: string | null; granted_by_user_id: string | null; expires_at: string | null;
  text_sha256: string | null; scope: Record<string, unknown> | null; offer: ConsentOffer | null;
};
export type ShortsSettings = ShortsSettingsBody & { campaign_start: string | null; autopublish: boolean; paused_at: string | null; consent: Consent; updated_at: string | null };
export type Campaign = { campaign_start: string; last_day: string; slots: number; assigned: number };

// The fields a consent names (apps/api/app/video_shorts/settings.py SCOPE_FIELDS): saving a change
// to one of them can end the consent, so the form says so beside them.
export const SCOPE_FIELDS = ["lines", "max_per_day", "slot_times", "timezone"] as const;
export const SETTINGS_KEYS = [
  "enabled", "lines", "weekly_quota", "daily_pattern", "slot_times", "timezone", "stock_days", "lock_hours", "upload_ahead_days", "max_per_day",
  "seconds_min", "seconds_max", "voice", "locales", "made_for_kids", "auto_approve", "budget_ntd_30d", "budget_soft_ntd", "budget_total_ntd",
] as const satisfies ReadonlyArray<keyof ShortsSettingsBody>;

/** What a save sends: the settings without the consent and the run, every field present. */
export function settingsBody(view: ShortsSettings | ShortsSettingsBody): ShortsSettingsBody {
  return Object.fromEntries(SETTINGS_KEYS.map((key) => [key, view[key]])) as ShortsSettingsBody;
}

export const slotTone: Record<SlotStatus, string> = {
  open: "inactive", planned: "queued", assigned: "pending", locked: "running", scheduled: "queued", published: "ok", missed: "failed", skipped: "inactive",
};
export const stateTone: Record<ShortsState, string> = {
  making: "running", needs_you: "warning", library: "active", slotted: "pending", scheduled: "queued", published: "ok", missed: "warning", dropped: "inactive",
};
export const autopublishTone: Record<AutopublishState, string> = { off: "inactive", on: "ok", paused: "warning", expiring: "warning", expired: "failed", invalid: "failed" };
// A slot that is on YouTube, or past, is changed by a recall or not at all (slots.py CHANGEABLE_STATUSES).
export const CHANGEABLE: readonly SlotStatus[] = ["open", "planned", "assigned", "locked", "skipped"];

const HOUR = 60 * 60 * 1000;
// The windows a snapshot is taken in, counted from the moment the Short went public
// (apps/api/app/video_shorts/stats.py WINDOWS).
export const METRIC_WINDOWS: Record<Exclude<MetricPeriod, "now">, readonly [number, number]> = {
  d1: [24 * HOUR, 48 * HOUR], d3: [72 * HOUR, 96 * HOUR], d7: [7 * 24 * HOUR, 9 * 24 * HOUR],
};
export type BlankReason = "early" | "waiting" | "missed" | "removed";

/**
 * Why a window has no number: its time has not come, it is open and unread, or it closed unread.
 * A Short that was taken down is read no more (apps/api/app/video_shorts/stats.py), so a window of
 * it that had not closed by then stays empty for that reason, and so does its latest read.
 */
export function blankReason(period: MetricPeriod, short: { published_at: string | null; removed_at?: string | null }, now = Date.now()): BlankReason {
  const gone = short.removed_at ? Date.parse(short.removed_at) : Number.NaN;
  const removed = Number.isFinite(gone);
  if (period === "now") return removed ? "removed" : "waiting";
  const since = short.published_at ? Date.parse(short.published_at) : Number.NaN;
  if (!Number.isFinite(since)) return removed ? "removed" : "early";
  const [opens, closes] = METRIC_WINDOWS[period];
  // The window closed while the Short was still up: it was missed, whatever happened later.
  if (removed) return gone - since >= closes ? "missed" : "removed";
  const age = now - since;
  if (age < opens) return "early";
  return age < closes ? "waiting" : "missed";
}

const PARTS: Intl.DateTimeFormatOptions = { year: "numeric", month: "2-digit", day: "2-digit", hour: "2-digit", minute: "2-digit", second: "2-digit", hourCycle: "h23" };

/** The wall clock a zone shows at an instant, as the milliseconds the same reading would be in UTC. */
export function wallClock(instant: Date, zone: string): number {
  const parts = Object.fromEntries(new Intl.DateTimeFormat("en-CA", { ...PARTS, timeZone: zone }).formatToParts(instant).map((part) => [part.type, part.value]));
  return Date.UTC(Number(parts.year), Number(parts.month) - 1, Number(parts.day), Number(parts.hour), Number(parts.minute), Number(parts.second));
}

/**
 * The instant a zone's wall clock reads `local` ("2026-10-05T19:30"), or null when it is no such
 * reading. A slot's time is a time of day in the calendar's zone, whatever zone the browser is in.
 */
export function zonedInstant(local: string, zone: string): Date | null {
  if (!/^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}$/.test(local)) return null;
  const reading = Date.parse(`${local}:00Z`);
  if (!Number.isFinite(reading)) return null;
  try {
    // The zone's offset at the reading taken as UTC, then again at the instant that gives: the
    // second pass is what a change of clocks between the two needs.
    const first = reading - (wallClock(new Date(reading), zone) - reading);
    const instant = new Date(reading - (wallClock(new Date(first), zone) - first));
    // A spring-forward gap has no matching instant; never silently move the chosen wall time.
    return localInput(instant.toISOString(), zone) === local ? instant : null;
  } catch {
    return null;
  }
}

/** An instant as a datetime-local value in a zone: the reverse of zonedInstant. */
export function localInput(instant: string, zone: string): string {
  const moment = Date.parse(instant);
  if (!Number.isFinite(moment)) return "";
  try {
    return new Date(wallClock(new Date(moment), zone)).toISOString().slice(0, 16);
  } catch {
    return "";
  }
}

/** The calendar day a zone is on at an instant, as YYYY-MM-DD. */
export function dayIn(zone: string, now = new Date()): string {
  try {
    return new Date(wallClock(now, zone)).toISOString().slice(0, 10);
  } catch {
    return now.toISOString().slice(0, 10);
  }
}

export function addDays(day: string, days: number): string {
  const moment = Date.parse(`${day}T00:00:00Z`);
  return Number.isFinite(moment) ? new Date(moment + days * 24 * HOUR).toISOString().slice(0, 10) : day;
}

/**
 * New Taiwan dollars as the page writes them: 1,234, or 0.29 for a line that costs less than a
 * dollar. A narration is a few cents, so an amount rounded to whole dollars would read as nothing spent.
 */
export const dollars = (value: number | null | undefined) => (typeof value === "number" && Number.isFinite(value) ? value.toLocaleString("en-US", { maximumFractionDigits: 2 }) : "0");

export const sizeOf = (bytes: number) => (bytes >= 1_000_000 ? `${(bytes / 1_000_000).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1000))} KB`);
export const message = (problem: unknown) => (problem instanceof Error ? problem.message : "");

/** "19:30, 12:30" or one a line, as the list the API stores. */
export const timesOf = (value: string) => value.split(/[\s,，、]+/).map((part) => part.trim()).filter(Boolean);
/** "2, 1" as the counts of a stretch of the run; null when a part is no whole number from 0 to 4. */
export function countsOf(value: string): number[] | null {
  const parts = value.split(/[\s,，、]+/).map((part) => part.trim()).filter(Boolean);
  const counts = parts.map(Number);
  return parts.length > 0 && counts.every((count) => Number.isInteger(count) && count >= 0 && count <= 4) ? counts : null;
}
