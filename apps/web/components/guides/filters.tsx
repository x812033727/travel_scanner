import { TopicChips, type TopicChipLabels } from "@/components/guides/topic-chips";
import { guideListHref, guideSection, type GuideKind, type GuideTopic } from "@/lib/guides";

export type GuideFilterLabels = TopicChipLabels;

/**
 * The topic chips of a listing page. Each chip is a plain link to the topic's hub page, so a
 * filtered view is shareable and works with JavaScript off; the listing's own `?topic=`
 * view stays for old links and canonicalizes to that hub.
 */
export function GuideFilters({
  kind, topics, active, labels,
}: {
  kind: GuideKind;
  topics: GuideTopic[];
  active: string | null;
  labels: GuideFilterLabels;
}) {
  if (!topics.length) return null;
  // The listing URL comes from one place, so a `life` filter lands on `/life`, never `/guides/life`.
  return (
    <TopicChips
      section={guideSection(kind)}
      topics={topics}
      active={active}
      allHref={guideListHref(kind)}
      labels={labels}
    />
  );
}
