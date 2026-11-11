import en from "./topic-feed-messages/en.json";
import ja from "./topic-feed-messages/ja.json";
import ko from "./topic-feed-messages/ko.json";
import zhCN from "./topic-feed-messages/zh-CN.json";
import zhTW from "./topic-feed-messages/zh-TW.json";
import { guideTopicHref } from "./guides";

const catalogs: Record<string, typeof en> = { en, ja, ko, "zh-CN": zhCN, "zh-TW": zhTW };
export const topicFeedCopy = (locale: string) => catalogs[locale] ?? en;
export const TOPIC_FEED_SIZE = 30;
export const topicFeedPath = (topic: string) => `${guideTopicHref("life", topic)}/feed.xml`;
