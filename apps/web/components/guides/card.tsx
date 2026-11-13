import { Link } from "@/i18n/navigation";
import { GuideImage } from "./guide-image";
import { guideHref, visibleGuideHero, type GuideKind, type GuideSummary } from "@/lib/guides";

/** One label per kind: the badge in the corner. A card carries no dates — neither when the
 *  article was published nor how long it applies — so nothing here says "old" to a reader
 *  about copy that is still correct. */
export type GuideCardLabels = Record<GuideKind, string>;

/**
 * How dense a card is. `default` is the listing card: hero, badge, title, description,
 * topics. `compact` drops the hero and the topics for a row that scans -- the news block, a
 * "next to read" grid. `featured` is the one card a hub leads with: it spans the grid, sets
 * the hero beside the text from `md` up and loads it eagerly, since it is above the fold.
 */
export type GuideCardVariant = "default" | "compact" | "featured";

/**
 * A card's identity comes from the three things that actually tell a reader whether it is
 * for them: which section it is in, which city it is about and what it is about. The hero,
 * when the article has one, sits above them at the same 16:9 the article shows it in.
 */
export function GuideCard({
  article, labels, variant = "default",
}: {
  article: GuideSummary;
  labels: GuideCardLabels;
  variant?: GuideCardVariant;
}) {
  const compact = variant === "compact";
  const featured = variant === "featured";
  const hero = visibleGuideHero(article.hero);
  const shell = featured
    ? `group relative rounded-2xl border border-[var(--teal)] bg-[var(--surface)] p-4 shadow-[var(--shadow-md)] transition-all duration-200 hover:shadow-[var(--shadow-lg)] sm:col-span-2 ${hero ? "md:grid md:grid-cols-2 md:items-center md:gap-6" : "border-l-4"} md:p-6`
    : compact
      ? "group relative rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3.5 shadow-[var(--shadow-sm)] transition-all duration-200 hover:-translate-y-0.5 hover:border-[var(--teal)] hover:shadow-[var(--shadow-md)]"
      : "group relative flex flex-col justify-between rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4 shadow-[var(--shadow-sm)] transition-all duration-200 hover:-translate-y-0.5 hover:border-[var(--teal)] hover:shadow-[var(--shadow-md)]";
  return (
    <li className={shell} data-variant={variant}>
      {hero && !compact ? (
        <div className={`overflow-hidden rounded-xl bg-[var(--paper)] ${featured ? "mb-3.5 md:mb-0" : "mb-3.5"}`}>
          <GuideImage
            src={hero.src}
            alt={hero.alt}
            width={hero.width}
            height={hero.height}
            loading={featured ? "eager" : "lazy"}
            decoding="async"
            className="aspect-video w-full object-cover transition-transform duration-300 group-hover:scale-[1.02]"
          />
        </div>
      ) : null}
      <div className={`min-w-0 ${!compact && !featured ? "flex flex-1 flex-col" : ""}`}>
        <p className="flex flex-wrap items-center gap-2 text-[length:var(--text-xs)] font-semibold uppercase tracking-wide text-[var(--muted)]">
          <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[var(--teal-dark)]">
            {labels[article.kind]}
          </span>
          {article.news_date ? (
            <time dateTime={article.news_date} className="font-mono tabular-nums">
              {article.news_date}
            </time>
          ) : null}
          {article.destination_label ? <span>{article.destination_label}</span> : null}
        </p>
        <h3 className={`mt-2.5 font-bold tracking-tight ${featured ? "text-2xl leading-snug" : compact ? "text-base leading-6" : "text-lg leading-snug"}`}>
          <Link
            className="text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
            href={guideHref(article.kind, article.slug)}
          >
            {article.title}
          </Link>
        </h3>
        <p className={`text-sm leading-6 text-[var(--muted)] ${compact ? "mt-1.5 line-clamp-2" : "mt-2 line-clamp-3"}`}>{article.description}</p>
        {article.topics.length && !compact ? (
          <ul className="mt-auto flex flex-wrap gap-1.5 pt-3">
            {article.topics.map((topic) => (
              <li key={topic.slug} className="rounded-full border border-[var(--line)] bg-[var(--paper)]/70 px-2.5 py-0.5 text-[length:var(--text-xs)] font-medium text-[var(--muted)]">
                {topic.label}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </li>
  );
}
