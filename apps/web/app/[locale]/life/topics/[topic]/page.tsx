import type { Metadata } from "next";
import { renderTopicHub, topicHubMetadata } from "@/components/guides/topic-hub-page";
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
  return renderTopicHub({ locale, section: "life", topic, cursor: search.cursor, sort: search.sort });
}
