import { Link } from "@/i18n/navigation";
import { guideTopicHref, type GuideSection, type GuideTopic } from "@/lib/guides";

export type TopicTileLabels = {
  heading: string;
  /** ICU-free: `{count}` is replaced here, the way `TopicChips` does it. */
  articles: string;
  more: string;
};

/** Sub-topics a tile shows before it says "and N more". */
export const TOPIC_TILE_SUBTOPICS = 3;

/**
 * A section's top-level topics as tiles: the label linking to the topic hub, how many
 * articles this language has under it, the hub's lead, and the first few sub-topics as
 * chips. A topic nothing is published under is left out unless the reader is on it, for
 * the reason `TopicChips` gives: a tile that leads to an empty page is worse than none. A
 * topic whose count an older API did not send is kept.
 */
export function TopicTiles({
  section, topics, active = null, labels,
}: {
  section: GuideSection;
  topics: readonly GuideTopic[];
  active?: string | null;
  labels: TopicTileLabels;
}) {
  const shown = (topic: GuideTopic) => topic.count === undefined || topic.count > 0 || topic.slug === active;
  const parents = topics.filter((topic) => !topic.parent && shown(topic));
  if (!parents.length) return null;
  const fill = (template: string, count: number) => template.replace("{count}", String(count));
  return (
    <section aria-labelledby="topic-tiles-heading" className="mt-10" data-testid="topic-tiles">
      <h2 id="topic-tiles-heading" className="text-2xl font-bold tracking-tight">{labels.heading}</h2>
      <ul className="mt-4 grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
        {parents.map((topic) => {
          const children = topics.filter((child) => child.parent === topic.slug && shown(child));
          const inFamily = topic.slug === active || children.some((child) => child.slug === active);
          return (
            <li
              key={topic.slug}
              className={`rounded-2xl border p-4 ${inFamily ? "border-[var(--teal)] bg-[var(--teal-soft)]" : "border-[var(--line)] bg-[var(--surface)]"}`}
            >
              <h3 className="flex items-baseline justify-between gap-3 text-lg font-bold">
                <Link
                  className="inline-flex min-h-11 items-center text-[var(--teal)] underline-offset-4 hover:underline"
                  href={guideTopicHref(section, topic.slug)}
                  aria-current={topic.slug === active ? "page" : undefined}
                >
                  {topic.label}
                </Link>
                {topic.count ? (
                  <span className="shrink-0 text-[length:var(--text-meta)] font-normal text-[var(--muted)]">
                    {fill(labels.articles, topic.count)}
                  </span>
                ) : null}
              </h3>
              {topic.description ? <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{topic.description}</p> : null}
              {children.length ? (
                <ul className="mt-3 flex flex-wrap items-center gap-2">
                  {children.slice(0, TOPIC_TILE_SUBTOPICS).map((child) => (
                    <li key={child.slug}>
                      <Link
                        className={`app-filter-chip ${child.slug === active ? "app-filter-chip-active" : ""}`}
                        href={guideTopicHref(section, child.slug)}
                        aria-current={child.slug === active ? "page" : undefined}
                      >
                        {child.label}
                      </Link>
                    </li>
                  ))}
                  {children.length > TOPIC_TILE_SUBTOPICS ? (
                    <li className="text-[length:var(--text-meta)] text-[var(--muted)]">
                      {fill(labels.more, children.length - TOPIC_TILE_SUBTOPICS)}
                    </li>
                  ) : null}
                </ul>
              ) : null}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
