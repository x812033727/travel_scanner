import type { Metadata } from "next";
import { renderTopicHub, topicHubMetadata } from "@/components/guides/topic-hub-page";
import type { Locale } from "@/i18n/routing";

type Params = { locale: Locale; topic: string };
type Search = { cursor?: string };

/** A travel topic's hub: every intel notice and guide under the topic, in one place. The
 *  screen itself lives in `topic-hub-page.tsx`, shared with the lifestyle section. */
export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale, topic }, search] = await Promise.all([params, searchParams]);
  return topicHubMetadata({ locale, section: "travel", topic, cursor: search.cursor });
}

export default async function TravelTopicHubPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale, topic }, search] = await Promise.all([params, searchParams]);
  return renderTopicHub({ locale, section: "travel", topic, cursor: search.cursor });
}
