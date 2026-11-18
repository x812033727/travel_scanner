import { Link } from "@/i18n/navigation";
import { guideHref, visibleGuideHero, type GuideSummary } from "@/lib/guides";
import { GuideImage } from "./guide-image";

function LeadRow({ article, heading: Heading, showTopic }: {
  article: GuideSummary;
  heading: "h3" | "h4";
  showTopic: boolean;
}) {
  const hero = visibleGuideHero(article.hero);
  return (
    <li className="py-2">
      <Link href={guideHref(article.kind, article.slug)} aria-label={article.title}
        className={`group grid min-w-0 gap-3 rounded-xl bg-[var(--teal-soft)] p-4 text-[var(--ink)] outline-offset-2 [overflow-wrap:anywhere] sm:p-5 ${hero ? "sm:grid-cols-[minmax(0,1fr)_11rem] sm:items-center" : ""}`}>
        <div className="min-w-0">
          <div className="flex flex-wrap items-center gap-2 text-sm font-semibold text-[var(--teal-dark)]">
            <time dateTime={article.news_date ?? undefined} className="tabular-nums">{article.news_date}</time>
            {showTopic && article.topics[0] ? <span>{article.topics[0].label}</span> : null}
          </div>
          <Heading className="mt-1 text-xl font-extrabold leading-snug tracking-tight underline-offset-4 group-hover:underline group-focus-visible:underline sm:text-2xl">
            {article.title}
          </Heading>
          {article.description ? (
            <p className="mt-2 line-clamp-3 text-sm leading-6 text-[var(--ink)]">{article.description}</p>
          ) : null}
        </div>
        {hero ? (
          <GuideImage src={hero.src} alt="" width={hero.width} height={hero.height} loading="lazy" decoding="async"
            className="aspect-video w-full rounded-lg object-contain" />
        ) : null}
      </Link>
    </li>
  );
}

function ChannelStory({ article, lead, showTopic, hasPair }: {
  article: GuideSummary;
  lead: boolean;
  showTopic: boolean;
  hasPair: boolean;
}) {
  const hero = visibleGuideHero(article.hero);
  const Heading = lead ? "h2" : "h3";
  return (
    <li className={`group relative min-w-0 [overflow-wrap:anywhere] ${lead
      ? "col-span-full border-y-2 border-t-[var(--teal)] border-b-[var(--line)] py-5 sm:py-7"
      : `border-b border-[var(--line)] py-4 sm:py-5 ${hasPair ? "" : "col-span-full"}`}`}>
      <div className={`grid min-w-0 gap-4 ${lead && hero ? "md:grid-cols-[1.15fr_1fr] md:items-center md:gap-8" : ""}`}>
        <div className="min-w-0">
          <div className="flex flex-wrap items-baseline gap-x-3 gap-y-1 text-xs font-semibold text-[var(--teal-dark)]">
            <time dateTime={article.news_date ?? undefined} className="font-mono tabular-nums">{article.news_date}</time>
            {showTopic && article.topics[0] ? <span>{article.topics[0].label}</span> : null}
          </div>
          <Heading className={`mt-2 text-pretty font-extrabold tracking-tight text-[var(--ink)] ${lead
            ? "max-w-[34ch] text-2xl leading-[1.27] sm:text-3xl lg:text-4xl"
            : "text-xl leading-snug sm:text-2xl"}`}>
            <Link href={guideHref(article.kind, article.slug)}
              className="underline-offset-4 after:absolute after:inset-0 group-hover:text-[var(--teal-dark)] group-hover:underline focus-visible:underline">
              {article.title}
            </Link>
          </Heading>
          {article.description ? (
            <p className={`mt-2 max-w-prose text-[var(--muted)] ${lead
              ? "text-base leading-7 sm:mt-3 sm:text-lg sm:leading-8"
              : "line-clamp-3 text-sm leading-6"}`}>{article.description}</p>
          ) : null}
        </div>
        {hero ? (
          <GuideImage src={hero.src} alt={hero.alt} width={hero.width} height={hero.height}
            loading={lead ? "eager" : "lazy"} decoding="async"
            className="aspect-video w-full rounded-lg bg-[var(--paper)] object-contain" />
        ) : null}
      </div>
    </li>
  );
}

/**
 * A compact chronological wire. A section can give its first dated story a headline and
 * summary, while keeping the remaining rows short enough to scan on a phone.
 *
 * The date is `news_date`, never the publication or update time: stories are imported in
 * batches, so a whole week publishes in the same minute and corrections move `updated_at`.
 * A row without one (a news topic's evergreen piece, such as a sources list) keeps its line
 * with an empty date column; the API already sorts those after the dated stories.
 *
 * The rows are in the order given. The list is an `<ol>` because that order means something,
 * but it prints no numbers: a position in a list that grows every day is not worth reading.
 */
export function NewsList({
  articles,
  className = "mt-4",
  channelFront = false,
  leadHeading,
  showTopic = false,
  showDescription = false,
}: {
  articles: readonly GuideSummary[];
  className?: string;
  channelFront?: boolean;
  leadHeading?: "h3" | "h4";
  showTopic?: boolean;
  showDescription?: boolean;
}) {
  if (!articles.length) return null;
  const channelStories = channelFront ? articles.filter((article) => article.news_date).slice(0, 3) : [];
  const hasChannelStories = channelStories.length > 0;
  return (
    <ol
      className={`${className} ${hasChannelStories
        ? "grid min-w-0 gap-x-8 md:grid-cols-2"
        : "divide-y divide-[var(--line)] rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-1.5 shadow-[var(--shadow-sm)]"}`}
      data-testid="news-list"
    >
      {articles.map((article, index) => channelStories.includes(article) ? (
        <ChannelStory key={`${article.kind}:${article.slug}`} article={article} lead={article === channelStories[0]}
          showTopic={showTopic} hasPair={channelStories.length === 3} />
      ) : leadHeading && index === 0 && article.news_date ? (
        <LeadRow key={`${article.kind}:${article.slug}`} article={article} heading={leadHeading} showTopic={showTopic} />
      ) : (
        <li
          key={`${article.kind}:${article.slug}`}
          className={`group relative grid min-w-0 gap-x-4 transition-colors hover:bg-[var(--paper)]/75 sm:grid-cols-[7rem_minmax(0,1fr)] sm:items-baseline ${hasChannelStories
            ? "col-span-full border-b border-[var(--line)] py-3 [overflow-wrap:anywhere]"
            : "-mx-2 rounded-xl px-2 py-1.5"}`}
        >
          {article.news_date ? (
            <time
              dateTime={article.news_date}
              className="pt-1 font-mono text-[length:var(--text-meta)] font-medium tabular-nums text-[var(--muted)] sm:pt-0"
            >
              {article.news_date}
            </time>
          ) : (
            <span aria-hidden="true" className="hidden sm:block" />
          )}
          <div className="min-w-0">
            <div className="flex flex-wrap items-baseline gap-x-2.5 gap-y-1">
              {showTopic && article.topics[0] ? (
                <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[length:var(--text-xs)] font-semibold text-[var(--teal-dark)]">
                  {article.topics[0].label}
                </span>
              ) : null}
              <Link
                href={guideHref(article.kind, article.slug)}
                className="inline-flex min-h-11 min-w-0 items-center font-medium leading-7 text-[var(--ink)] underline-offset-4 [overflow-wrap:anywhere] after:absolute after:inset-0 group-hover:text-[var(--teal)] group-hover:underline focus-visible:underline"
              >
                {article.title}
              </Link>
            </div>
            {showDescription && article.description ? (
              <p className="mb-1.5 line-clamp-2 text-sm leading-6 text-[var(--muted)]">{article.description}</p>
            ) : null}
          </div>
        </li>
      ))}
    </ol>
  );
}
