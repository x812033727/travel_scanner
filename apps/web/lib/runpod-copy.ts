import en from "./runpod-messages/en.json";
import zhTW from "./runpod-messages/zh-TW.json";
import zhCN from "./runpod-messages/zh-CN.json";
import ja from "./runpod-messages/ja.json";
import ko from "./runpod-messages/ko.json";

// The RunPod GPU card's words live here rather than in messages/<locale>/admin.json: those five
// files are bound by SHA-256 in docs/videos/long-form/review.json, so a non-video feature that
// edits them needs a duration review it has nothing to do with.
export type RunpodCopy = typeof en;
type FieldCopy = { label: string; help?: string; options?: Record<string, string> };
const catalogs: Record<string, RunpodCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function runpodCopy(locale: string): RunpodCopy {
  return catalogs[locale] ?? en;
}

/** The card's label, help and option names for one field, when it is a RunPod field. */
export function runpodField(copy: RunpodCopy, field: string): FieldCopy | undefined {
  return (copy.fields as Record<string, FieldCopy>)[field];
}

export function runpodSecret(copy: RunpodCopy, field: string): { label: string; help?: string } | undefined {
  return (copy.secrets as Record<string, { label: string; help?: string }>)[field];
}
