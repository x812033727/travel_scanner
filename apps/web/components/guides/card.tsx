import { Link } from "@/i18n/navigation";
import { GuideImage } from "./guide-image";
import { guideHref, type GuideKind, type GuideSummary } from "@/lib/guides";

/** One label per kind: the badge in the corner. A card carries no dates — neither when the
 *  article was published nor how long it applies — so nothing here says "old" to a reader
 *  about copy that is still correct. */
export type GuideCardLabels = Record<GuideKind, string>;

/**
 * A card's identity comes from the three things that actually tell a reader whether it is
 * for them: which section it is in, which city it is about and what it is about. The hero,
 * when the article has one, sits above them at the same 16:9 the article shows it in.
 */
export function GuideCard({ article, labels }: { article: GuideSummary; labels: GuideCardLabels }) {
  return (
    <li className="rounded-2xl border border-[var(--line)] p-4">
      {article.hero ? (
        <GuideImage
          src={article.hero.src}
          alt={article.hero.alt}
          width={article.hero.width}
          height={article.hero.height}
          loading="lazy"
          decoding="async"
          className="mb-3 aspect-video w-full rounded-xl object-cover"
        />
      ) : null}
      <p className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">
        <span className="rounded-full bg-[var(--line)] px-2 py-1 text-[var(--fg)]">
          {labels[article.kind]}
        </span>
        {article.destination_label ? <span>{article.destination_label}</span> : null}
      </p>
      <h3 className="mt-2 text-lg font-bold">
        <Link className="text-[var(--teal)] underline" href={guideHref(article.kind, article.slug)}>
          {article.title}
        </Link>
      </h3>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{article.description}</p>
      {article.topics.length ? (
        <ul className="mt-3 flex flex-wrap gap-2">
          {article.topics.map((topic) => (
            <li key={topic.slug} className="rounded-full border border-[var(--line)] px-2 py-1 text-xs text-[var(--muted)]">
              {topic.label}
            </li>
          ))}
        </ul>
      ) : null}
    </li>
  );
}
