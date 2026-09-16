import { Link } from "@/i18n/navigation";
import { GuideImage } from "./guide-image";
import { guideHref, type GuideKind, type GuideSummary } from "@/lib/guides";

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
  const shell = featured
    ? "rounded-2xl border border-[var(--teal)] bg-[var(--paper)] p-4 sm:col-span-2 md:grid md:grid-cols-2 md:gap-5 md:p-5"
    : `rounded-2xl border border-[var(--line)] ${compact ? "p-3" : "p-4"}`;
  return (
    <li className={shell} data-variant={variant}>
      {article.hero && !compact ? (
        <GuideImage
          src={article.hero.src}
          alt={article.hero.alt}
          width={article.hero.width}
          height={article.hero.height}
          loading={featured ? "eager" : "lazy"}
          decoding="async"
          className={`aspect-video w-full rounded-xl object-cover ${featured ? "mb-3 md:mb-0" : "mb-3"}`}
        />
      ) : null}
      <div className="min-w-0">
        <p className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">
          <span className="rounded-full bg-[var(--line)] px-2 py-1 text-[var(--fg)]">
            {labels[article.kind]}
          </span>
          {article.destination_label ? <span>{article.destination_label}</span> : null}
        </p>
        <h3 className={`mt-2 font-bold ${featured ? "text-2xl leading-snug" : compact ? "text-base leading-6" : "text-lg"}`}>
          <Link className="text-[var(--teal)] underline" href={guideHref(article.kind, article.slug)}>
            {article.title}
          </Link>
        </h3>
        <p className={`text-sm leading-6 text-[var(--muted)] ${compact ? "mt-1 line-clamp-2" : "mt-2"}`}>{article.description}</p>
        {article.topics.length && !compact ? (
          <ul className="mt-3 flex flex-wrap gap-2">
            {article.topics.map((topic) => (
              <li key={topic.slug} className="rounded-full border border-[var(--line)] px-2 py-1 text-xs text-[var(--muted)]">
                {topic.label}
              </li>
            ))}
          </ul>
        ) : null}
      </div>
    </li>
  );
}
