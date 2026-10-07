import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { AiHubRails, loadAiHubRails } from "@/components/guides/ai-hub-rails";
import { renderTopicHub, topicHubMetadata } from "@/components/guides/topic-hub-page";
import type { Locale } from "@/i18n/routing";
import { AI_HUB_TOPIC } from "@/lib/guides";

type Params = { locale: Locale };
type Search = { cursor?: string; sort?: string };

/** The AI section's hub: the `ai` topic family with its sub-topics, at its own address.
 *  `guideTopicHref("life", "ai")` names this page, so its canonical, its pagination and every
 *  breadcrumb that climbs to the family already point here. */
export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const [hub, t] = await Promise.all([
    topicHubMetadata({ locale, section: "life", topic: AI_HUB_TOPIC, cursor: search.cursor, sort: search.sort }),
    getTranslations({ locale, namespace: "metadata" }),
  ]);
  // Its own title and description rather than the generic "<topic> articles": this is a
  // section's front page, and the one the header names.
  return { ...hub, title: t("aiHubTitle"), description: t("aiHubDescription") };
}

export default async function AiHubPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  return renderTopicHub(
    { locale, section: "life", topic: AI_HUB_TOPIC, cursor: search.cursor, sort: search.sort },
    async (topics) => {
      const [{ rails, news }, t] = await Promise.all([
        loadAiHubRails(locale, topics),
        getTranslations({ locale, namespace: "common" }),
      ]);
      return (
        <AiHubRails
          rails={rails}
          news={news}
          labels={{
            heading: t("guides.aiHubRails"),
            seeAll: t("guides.seeAll"),
            cards: { intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life") },
          }}
        />
      );
    },
  );
}
