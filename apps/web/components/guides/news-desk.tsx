import { Link } from "@/i18n/navigation";
import { guideTopicHref, type GuideSummary, type GuideTopic } from "@/lib/guides";
import { NewsList } from "./news-list";

/** Use the supplied chronology and published vocabulary, with no popularity claim. */
export function NewsDesk({ articles, topics, topicsLabel, lead = true, active, titleTag = "h3" }: {
  articles: readonly GuideSummary[];
  topics: readonly GuideTopic[];
  topicsLabel: string;
  lead?: boolean;
  active?: string;
  titleTag?: "h2" | "h3";
}) {
  if (!articles.length) return null;
  return (
    <div data-testid="news-desk" className={`mt-6 grid min-w-0 gap-8 ${topics.length ? "lg:grid-cols-[minmax(0,1fr)_15rem] lg:gap-10" : ""}`}>
      <NewsList articles={articles} lead={lead} titleTag={titleTag} className="min-w-0" />
      {topics.length ? (
        <aside className="min-w-0">
          <nav aria-label={topicsLabel} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-5 lg:sticky lg:top-24">
            <h2 className="border-b border-[var(--line)] pb-4 text-lg font-bold">{topicsLabel}</h2>
            <ul className="divide-y divide-[var(--line)]">
              {topics.map((topic) => (
                <li key={topic.slug}>
                  <Link href={guideTopicHref("life", topic.slug)} aria-current={active === topic.slug ? "page" : undefined}
                    className="group block min-h-11 py-4 outline-offset-4">
                    <span className="flex items-center justify-between gap-3 font-semibold text-[var(--teal)] group-hover:underline">
                      {topic.label}<span aria-hidden="true">→</span>
                    </span>
                    {topic.description ? <span className="mt-2 block text-sm leading-6 text-[var(--muted)]">{topic.description}</span> : null}
                  </Link>
                </li>
              ))}
            </ul>
          </nav>
        </aside>
      ) : null}
    </div>
  );
}
