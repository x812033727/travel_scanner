import type { Metadata } from "next";
import { permanentRedirect } from "next/navigation";
import { renderTopicHub, topicHubMetadata } from "@/components/guides/topic-hub-page";
import { AI_HUB_PATH, AI_HUB_TOPIC } from "@/lib/guides";
import type { Locale } from "@/i18n/routing";

type Params = { locale: Locale; topic: string };
type Search = { cursor?: string; sort?: string };

/** A lifestyle topic's hub, parent or sub-topic: `/life/topics/ai` lists everything under
 *  `ai` including its sub-topics; `/life/topics/ai-terms` lists the glossary alone. */
export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale, topic }, search] = await Promise.all([params, searchParams]);
  return topicHubMetadata({ locale, section: "life", topic, cursor: search.cursor, sort: search.sort });
}

export default async function LifeTopicHubPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale, topic }, search] = await Promise.all([params, searchParams]);
  // The AI family moved to `/ai`; the old address keeps its query (`?sort=`, `?cursor=`)
  // and answers permanently, so links and rankings follow it there.
  if (topic === AI_HUB_TOPIC) {
    const query = new URLSearchParams(Object.entries(search).filter((entry): entry is [string, string] => typeof entry[1] === "string"));
    permanentRedirect(`/${locale}${AI_HUB_PATH}${query.size ? `?${query}` : ""}`);
  }
  return renderTopicHub({ locale, section: "life", topic, cursor: search.cursor, sort: search.sort });
}
