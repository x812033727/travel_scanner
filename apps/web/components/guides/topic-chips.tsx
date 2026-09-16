"use client";

import { ChipRow } from "@/components/chip-row";
import { Link } from "@/i18n/navigation";
import { guideTopicHref, type GuideSection, type GuideTopic } from "@/lib/guides";

export type TopicChipLabels = {
  allTopics: string;
  topicsLabel: string;
  subtopics: string;
  /** ICU-free: `{count}` is replaced here, because a function cannot cross into a client component. */
  moreChips: string;
  fewerChips: string;
};

/**
 * The two-level topic navigation: one row of top-level topics, and under the selected
 * family a second row of its sub-topics. Every chip is a plain link to a topic hub, so a
 * filtered view is shareable and works without JavaScript; `ChipRow` only folds a long row.
 *
 * A topic nothing is published under in this language is left out unless it is the one
 * the reader is on: a chip that leads to an empty page is worse than no chip. A topic
 * whose count the API did not send (an older API) is kept.
 */
export function TopicChips({
  section, topics, active, allHref, labels, className = "mt-6 grid gap-2",
}: {
  section: GuideSection;
  topics: readonly GuideTopic[];
  active: string | null;
  allHref: string;
  labels: TopicChipLabels;
  /** The nav's own classes; the toolbar supplies its spacing itself. */
  className?: string;
}) {
  const shown = (topic: GuideTopic) => topic.count === undefined || topic.count > 0 || topic.slug === active;
  const parents = topics.filter((topic) => !topic.parent && shown(topic));
  const current = topics.find((topic) => topic.slug === active) ?? null;
  const family = current?.parent ? topics.find((topic) => topic.slug === current.parent) ?? null : current;
  const children = family ? topics.filter((topic) => topic.parent === family.slug && shown(topic)) : [];
  if (!parents.length && !children.length) return null;
  const more = (count: number) => labels.moreChips.replace("{count}", String(count));
  const chip = (topic: GuideTopic, exact: boolean, familyMember: boolean) => (
    <Link
      key={topic.slug}
      href={guideTopicHref(section, topic.slug)}
      aria-current={exact ? "page" : undefined}
      className={`app-filter-chip ${exact || familyMember ? "app-filter-chip-active" : ""}`}
    >
      {topic.label}
      {topic.count !== undefined && topic.count > 0 ? <span className="app-filter-count">{topic.count}</span> : null}
    </Link>
  );
  const leading = (
    <Link
      key="__all"
      href={allHref}
      aria-current={active ? undefined : "page"}
      className={`app-filter-chip ${active ? "" : "app-filter-chip-active"}`}
    >
      {labels.allTopics}
    </Link>
  );
  return (
    <nav aria-label={labels.topicsLabel} className={className}>
      <ChipRow
        leading={leading}
        chips={parents.map((topic) => chip(topic, topic.slug === active, family?.slug === topic.slug))}
        activeIndex={parents.findIndex((topic) => topic.slug === (family?.slug ?? active))}
        moreLabel={more}
        fewerLabel={labels.fewerChips}
      />
      {children.length ? (
        <div className="flex flex-wrap items-center gap-2 pl-1">
          <span className="text-[length:var(--text-label)] text-[var(--muted)]">{labels.subtopics}</span>
          <ChipRow
            chips={children.map((topic) => chip(topic, topic.slug === active, false))}
            activeIndex={children.findIndex((topic) => topic.slug === active)}
            limit={12}
            moreLabel={more}
            fewerLabel={labels.fewerChips}
          />
        </div>
      ) : null}
    </nav>
  );
}
