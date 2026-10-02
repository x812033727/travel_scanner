// What the Shorts tab of /admin/videos reads and sends (docs/videos/SHORTS.md): the shapes of
// apps/api/app/video_shorts/schemas.py, and the few rules the page applies itself. No markup
// here, so the tab and every one of its views can import it without importing each other.

export const SHORTS_LINES = ["lab", "cut", "drama"] as const;
export type ShortsLine = (typeof SHORTS_LINES)[number];
export const SHORTS_STATES = ["needs_you", "making", "library", "missed", "slotted", "scheduled", "published", "dropped"] as const;
export type ShortsState = (typeof SHORTS_STATES)[number];
export type SlotStatus = "open" | "planned" | "assigned" | "locked" | "scheduled" | "published" | "missed" | "skipped";
export const VIEWS = ["calendar", "library", "metrics", "costs", "topics", "report", "settings"] as const;
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
  published_at: string | null; removed_at: string | null; dropped_at?: string | null; snapshots: Metric[];
};
export type Metrics = { items: ShortMetrics[] };

export type Voice = { provider: "azure" | "gemini"; name: string; style: string | null; model: string | null; rate: string };
export type PatternSegment = { days: number; counts: number[] };
// The models an experiment tests under a and b; b left out tests a's model (app/video_automation/ai.py subject_choice).
export const SUBJECT_VARIANTS = ["a", "b"] as const;
export type SubjectVariant = (typeof SUBJECT_VARIANTS)[number];
export type SubjectModel = { provider: string; model: string };
export type ShortsSettingsBody = {
  enabled: boolean; lines: ShortsLine[]; weekly_quota: Partial<Record<ShortsLine, number>>;
  daily_pattern: PatternSegment[]; slot_times: string[]; timezone: string;
  stock_days: number; lock_hours: number; upload_ahead_days: number; max_per_day: number; seconds_min: number; seconds_max: number;
  voice: Voice; locales: ShortsLocale[]; made_for_kids: boolean; auto_approve: boolean;
  budget_ntd_30d: number; budget_soft_ntd: number; budget_total_ntd: number;
  subject_models: Partial<Record<SubjectVariant, SubjectModel>>; max_per_month: number;
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
  "subject_models", "max_per_month",
] as const satisfies ReadonlyArray<keyof ShortsSettingsBody>;

// The topic library, the owner's material and the weekly report (apps/api/app/video_shorts/schemas.py, phase two).
export const TOPIC_STATUSES = ["idea", "ready", "needs_assets", "making", "made", "dropped"] as const;
export type TopicStatus = (typeof TOPIC_STATUSES)[number];
export type TopicOrigin = "campaign" | "planner" | "owner" | "auto";
// The protocol of an experiment, frozen before it runs (TEST_PROTOCOL_FIELDS).
export const PROTOCOL_FIELDS = ["setup", "input", "condition_a", "condition_b", "runs", "scoring", "failure_path"] as const;
export type AssetNeed = { key: string; label: string; count?: number };
export type Asset = {
  id: string; need: string; sha256: string; filename: string; content_type: string; size: number;
  author: string; taken_on: string | null; rights_note: string; created_at: string; download_path: string;
};
export type TopicBrief = {
  test_protocol?: Partial<Record<(typeof PROTOCOL_FIELDS)[number], string | null>>;
  truth_check?: string[]; acceptance?: string[]; notes?: string | null; requires?: string[];
};
export type Topic = {
  slug: string; line: ShortsLine; series: string | null; title: string; hook: string | null; status: TopicStatus;
  brief: TopicBrief; source_slug: string | null; origin: TopicOrigin; release_order: number | null;
  assets_needed: AssetNeed[]; assets: Asset[]; waiting_for: string[]; paid: boolean;
  project_slug: string | null; started_at: string | null; finished_at: string | null; note: string | null; created_at: string; updated_at: string;
};
export type TopicsWritten = { created: number; updated: number; skipped: number; items: Array<{ slug: string; result: "created" | "updated" | "exists"; status: TopicStatus | null }> };
export type AssetPart = { received: number[]; complete: boolean; asset: Asset | null; topic: Topic | null };
// A topic the owner may still change, give up or supply material for (topics.py EDITABLE, assets.py TAKES_ASSETS).
export const EDITABLE_TOPICS: readonly TopicStatus[] = ["idea", "ready", "needs_assets"];
export const topicTone: Record<TopicStatus, string> = { idea: "inactive", ready: "ok", needs_assets: "warning", making: "running", made: "active", dropped: "inactive" };

// The values a report row keeps, as YouTube gave them (apps/api/app/video_shorts/reports.py ROW_FIELDS).
export const REPORT_VALUES = ["views", "engaged_views", "likes", "comments", "shares", "subscribers_gained", "avg_view_seconds", "avg_view_percent", "stayed_percent"] as const;
export type ReportValue = (typeof REPORT_VALUES)[number];
export type ReportRow = {
  slug: string; title: string | null; youtube_video_id: string; period: MetricPeriod; source: MetricSource; captured_at: string;
  range_start: string | null; range_end: string | null;
} & Partial<Record<ReportValue, number | null>>;
export type ReportPlanItem = { starts_at?: string; topic_slug?: string; line?: ShortsLine; note?: string };
export type Report = {
  id: string; week_start: string; body_md: string; rows: ReportRow[]; plan: ReportPlanItem[];
  provider: string | null; model: string | null; generated_at: string; updated_at: string;
};
export type Reports = { items: Report[] };

// A file goes up in parts of 4 MiB (PART_BYTES in apps/api/app/video_reviews/storage.py): under the
// same-origin proxy's 5 MiB request cap and nginx's 6 MB.
export const PART_BYTES = 4 * 1024 * 1024;
// A photo is drawn again at most this long on its long edge before it goes up.
export const LONG_EDGE = 2048;

/** The SHA-256 of a file as 64 hex digits, which names it to the API. */
export async function sha256Hex(blob: Blob): Promise<string> {
  const digest = await crypto.subtle.digest("SHA-256", await blob.arrayBuffer());
  return Array.from(new Uint8Array(digest), (byte) => byte.toString(16).padStart(2, "0")).join("");
}

/** How a picture's sides scale so the long edge is at most `edge`; never enlarged. */
export function fitted(width: number, height: number, edge = LONG_EDGE): { width: number; height: number } {
  const scale = Math.min(1, edge / Math.max(width, height, 1));
  return { width: Math.max(1, Math.round(width * scale)), height: Math.max(1, Math.round(height * scale)) };
}

/**
 * The photo as it goes up: drawn again in the browser at most 2,048 px on its long edge, which also
 * leaves its EXIF (where and with what it was taken) behind, since a canvas carries pixels only. A
 * PNG stays a PNG (a sketch keeps its lines); anything else becomes a JPEG.
 */
export async function shrinkImage(file: File): Promise<{ blob: Blob; filename: string }> {
  const bitmap = await createImageBitmap(file, { imageOrientation: "from-image" });
  const size = fitted(bitmap.width, bitmap.height);
  const canvas = document.createElement("canvas");
  canvas.width = size.width;
  canvas.height = size.height;
  const context = canvas.getContext("2d");
  if (!context) throw new Error("canvas");
  context.drawImage(bitmap, 0, 0, size.width, size.height);
  bitmap.close();
  const png = file.type === "image/png";
  const blob = await new Promise<Blob | null>((resolve) => canvas.toBlob(resolve, png ? "image/png" : "image/jpeg", 0.9));
  if (!blob) throw new Error("canvas");
  const stem = file.name.replace(/\.[^.]*$/, "").slice(0, 180) || "photo";
  return { blob, filename: `${stem}.${png ? "png" : "jpg"}` };
}

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
export type BlankReason = "early" | "waiting" | "missed" | "removed" | "dropped";
type Stop = { reason: "removed" | "dropped"; at: number };

/** When the site stopped reading a Short, and why: the earlier of being taken down and being dropped. */
function stopped(short: { removed_at?: string | null; dropped_at?: string | null }): Stop | null {
  const stops = ([["removed", short.removed_at], ["dropped", short.dropped_at]] as const)
    .map(([reason, time]) => ({ reason, at: time ? Date.parse(time) : Number.NaN }))
    .filter((stop) => Number.isFinite(stop.at));
  return stops.reduce<Stop | null>((first, stop) => (first && first.at <= stop.at ? first : stop), null);
}

/**
 * Why a window has no number: its time has not come, it is open and unread, or it closed unread.
 * A Short that was taken down or dropped is read no more (apps/api/app/video_shorts/stats.py), so a
 * window of it that had not closed by then stays empty for that reason, and so does its latest read.
 */
export function blankReason(period: MetricPeriod, short: { published_at: string | null; removed_at?: string | null; dropped_at?: string | null }, now = Date.now()): BlankReason {
  const stop = stopped(short);
  if (period === "now") return stop ? stop.reason : "waiting";
  const since = short.published_at ? Date.parse(short.published_at) : Number.NaN;
  if (!Number.isFinite(since)) return stop ? stop.reason : "early";
  const [opens, closes] = METRIC_WINDOWS[period];
  // The window closed while the Short was still read: it was missed, whatever happened later.
  if (stop) return stop.at - since >= closes ? "missed" : stop.reason;
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
