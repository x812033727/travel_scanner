import { Link } from "@/i18n/navigation";
import { guideListHref, type GuideKind, type GuideTopic } from "@/lib/guides";

export type GuideFilterLabels = { allTopics: string; topicsLabel: string };

/**
 * Plain links, not a client form: the results are server-rendered for the URL the reader is
 * on, so a filtered view is shareable and works with JavaScript off.
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
  const href = (topic: string | null) => guideListHref(kind, topic);
  const chip = (selected: boolean) =>
    `inline-flex min-h-11 items-center rounded-full border px-3 py-1 text-sm ${
      selected
        ? "border-[var(--teal)] bg-[var(--teal)] text-white"
        : "border-[var(--line)] text-[var(--muted)]"
    }`;
  return (
    <nav aria-label={labels.topicsLabel} className="mt-6">
      <ul className="flex flex-wrap gap-2">
        <li>
          <Link aria-current={active ? undefined : "page"} className={chip(!active)} href={href(null)}>
            {labels.allTopics}
          </Link>
        </li>
        {topics.map((topic) => (
          <li key={topic.slug}>
            <Link
              aria-current={active === topic.slug ? "page" : undefined}
              className={chip(active === topic.slug)}
              href={href(topic.slug)}
            >
              {topic.label}
            </Link>
          </li>
        ))}
      </ul>
    </nav>
  );
}
