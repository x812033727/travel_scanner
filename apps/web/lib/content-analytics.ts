import en from "./content-analytics-messages/en.json";
import ja from "./content-analytics-messages/ja.json";
import ko from "./content-analytics-messages/ko.json";
import zhTW from "./content-analytics-messages/zh-TW.json";
import zhCN from "./content-analytics-messages/zh-CN.json";

const catalogs: Record<string, typeof en> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };
export const contentAnalyticsCopy = (locale: string) => catalogs[locale] ?? en;

export type ContentLink = { placement: "related" | "topic"; target_path: string };

/** Mirrors the API's closed content route vocabulary, including its storage bound. */
export function contentPath(value: string, articleOnly = false): string | null {
  const path = value.replace(/^\/(?:en|ja|ko|zh-TW|zh-CN)(?=\/)/, "");
  if (path.length > 128) return null;
  const article = path !== "/life/topics" && /^\/(?:life\/[a-z0-9]+(?:-[a-z0-9]+)*|guides\/(?:intel|howto)\/[a-z0-9]+(?:-[a-z0-9]+)*)$/.test(path);
  const topic = path === "/ai" || /^\/(?:life|guides)\/topics\/[a-z0-9]+(?:-[a-z0-9]+)*$/.test(path);
  return article || (!articleOnly && topic) ? path : null;
}

export type ContentAnalyticsReport = {
  range: string;
  timezone: string;
  available: boolean;
  reason: "raw_window_only" | null;
  from: string;
  to: string;
  retention_days: number;
  window_clipped: boolean;
  first_recorded_at: string | null;
  total_clicks: number;
  rows: Array<{ source_path: string; target_path: string; placement: ContentLink["placement"]; locale: string; clicks: number }>;
};

export function isContentAnalyticsReport(value: unknown): value is ContentAnalyticsReport {
  if (!value || typeof value !== "object") return false;
  const data = value as Partial<ContentAnalyticsReport>;
  return typeof data.available === "boolean" && typeof data.total_clicks === "number" && Number.isInteger(data.total_clicks) && data.total_clicks >= 0 &&
    typeof data.from === "string" && Number.isFinite(Date.parse(data.from)) && typeof data.to === "string" && Number.isFinite(Date.parse(data.to)) &&
    (data.first_recorded_at === null || (typeof data.first_recorded_at === "string" && Number.isFinite(Date.parse(data.first_recorded_at)))) &&
    typeof data.window_clipped === "boolean" && Array.isArray(data.rows) && data.rows.every((row) =>
      row && typeof row.source_path === "string" && contentPath(row.source_path, true) === row.source_path &&
      typeof row.target_path === "string" && contentPath(row.target_path) === row.target_path &&
      (row.placement === "related" || row.placement === "topic") && typeof row.locale === "string" &&
      typeof row.clicks === "number" && Number.isInteger(row.clicks) && row.clicks >= 0);
}
