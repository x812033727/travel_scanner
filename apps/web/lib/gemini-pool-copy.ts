import en from "./gemini-pool-messages/en.json";
import zhTW from "./gemini-pool-messages/zh-TW.json";
import zhCN from "./gemini-pool-messages/zh-CN.json";
import ja from "./gemini-pool-messages/ja.json";
import ko from "./gemini-pool-messages/ko.json";

// The Gemini key pool's words live here rather than in messages/<locale>/admin.json, for the
// reason lib/runpod-copy.ts gives: those files are bound by SHA-256 in a video duration review.
export type GeminiPoolCopy = typeof en;
const catalogs: Record<string, GeminiPoolCopy> = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };

export function geminiPoolCopy(locale: string): GeminiPoolCopy {
  return catalogs[locale] ?? en;
}

export function geminiPoolField(copy: GeminiPoolCopy, field: string): { label: string; help?: string } | undefined {
  return (copy.fields as Record<string, { label: string; help?: string }>)[field];
}

export function geminiPoolSecret(copy: GeminiPoolCopy, field: string): { label: string; help?: string } | undefined {
  return (copy.secrets as Record<string, { label: string; help?: string }>)[field];
}
