import en from "./life-discovery-messages/en.json";
import ja from "./life-discovery-messages/ja.json";
import ko from "./life-discovery-messages/ko.json";
import zhCN from "./life-discovery-messages/zh-CN.json";
import zhTW from "./life-discovery-messages/zh-TW.json";
import { NEWS_TOPICS, type GuideSummary } from "./guides";

const catalogs: Record<string, typeof en> = { en, ja, ko, "zh-CN": zhCN, "zh-TW": zhTW };
export const lifeDiscoveryCopy = (locale: string) => catalogs[locale] ?? en;
export const LIFE_NEWS_PREVIEW = 6;
export const LIFE_KNOWLEDGE_LIMIT = 3;
export const lifeArticleKey = (article: Pick<GuideSummary, "kind" | "slug">) => `${article.kind}:${article.slug}`;

/** Keep the API's existing curated order. A missing news date alone is not a knowledge
 * label: news topics and every time-limited article stay in the ordinary listing instead.
 * No expiry date is not proof that an article's facts are still current. */
export function selectLifeKnowledge(articles: readonly GuideSummary[]): GuideSummary[] {
  const seen = new Set<string>();
  return articles.filter((article) => {
    if (article.kind !== "life" || article.news_date || article.valid_until !== null
      || article.topics.some((topic) => NEWS_TOPICS.includes(topic.slug))) return false;
    const key = lifeArticleKey(article);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  }).slice(0, LIFE_KNOWLEDGE_LIMIT);
}
