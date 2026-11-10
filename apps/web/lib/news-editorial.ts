import en from "./news-editorial-messages/en.json";
import ja from "./news-editorial-messages/ja.json";
import ko from "./news-editorial-messages/ko.json";
import zhCN from "./news-editorial-messages/zh-CN.json";
import zhTW from "./news-editorial-messages/zh-TW.json";

const catalogs: Record<string, typeof en> = { en, ja, ko, "zh-CN": zhCN, "zh-TW": zhTW };
export const newsEditorialCopy = (locale: string) => catalogs[locale] ?? en;

export type FreshnessItem = {
  candidate_id: string;
  title: string;
  published_at: string | null;
  checked_at: string | null;
  status: "unchanged" | "changed" | "unverified" | "pending";
  review_due: boolean;
  validity_expired: boolean;
};
export type FreshnessReport = {
  enabled: boolean;
  coverage_days: number;
  interval_days: number;
  daily_limit: number;
  eligible_count: number;
  due_count: number;
  total_count: number;
  page: number;
  pages: number;
  items: FreshnessItem[];
};
