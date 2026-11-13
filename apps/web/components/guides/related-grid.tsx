import { Link } from "@/i18n/navigation";
import type { ArticleReference } from "@/lib/guide-series";
import { guideHref, type GuideKind } from "@/lib/guides";

export const RELATED_GRID_LIMIT = 4;

/**
 * What to read next, as the API ranked it: the editor's picks first, then the nearest
 * published neighbours. A reference carries a title and a description, not a card's hero
 * or topics, so this draws its own compact card rather than a `GuideCard`. `exclude` is
 * for the series navigation above it, which already lists a lesson's own related lessons.
 */
export function RelatedGrid({
  heading, items, kindLabels, exclude = [],
}: {
  heading: string;
  items: readonly ArticleReference[];
  kindLabels: Record<GuideKind, string>;
  exclude?: readonly string[];
}) {
  const shown = items.filter((item) => !exclude.includes(item.slug)).slice(0, RELATED_GRID_LIMIT);
  if (!shown.length) return null;
  return (
    <section data-testid="related-grid" aria-labelledby="related-grid-heading" className="border-t border-[var(--line)] pt-8">
      <h2 id="related-grid-heading" className="portal-section-heading text-xl font-extrabold tracking-tight">{heading}</h2>
      <ul className="mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2">
        {shown.map((item) => (
          <li
            key={`${item.kind}:${item.slug}`}
            className="portal-card-surface group relative flex flex-col justify-between rounded-2xl p-4"
          >
            <div>
              <p className="text-[length:var(--text-xs)] font-semibold uppercase tracking-wide text-[var(--muted)]">
                <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[var(--teal-dark)]">{kindLabels[item.kind]}</span>
              </p>
              <h3 className="mt-2.5 text-base font-bold leading-snug tracking-tight">
                <Link
                  className="text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
                  href={guideHref(item.kind, item.slug)}
                >
                  {item.title}
                </Link>
              </h3>
              {item.description ? <p className="mt-2 line-clamp-2 text-sm leading-6 text-[var(--muted)]">{item.description}</p> : null}
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}

/** The articles whose text links here: a plain list, newest first, as the API sends them. */
export function Backlinks({ heading, items }: { heading: string; items: readonly ArticleReference[] }) {
  if (!items.length) return null;
  return (
    <section data-testid="backlinks" aria-labelledby="backlinks-heading" className="border-t border-[var(--line)] pt-8">
      <h2 id="backlinks-heading" className="portal-section-heading text-xl font-extrabold tracking-tight">{heading}</h2>
      <ul className="mt-3.5 flex flex-wrap gap-2">
        {items.map((item) => (
          <li key={`${item.kind}:${item.slug}`}>
            <Link
              className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] bg-[var(--paper)]/55 px-3.5 py-1 text-sm font-medium text-[var(--teal)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
              href={guideHref(item.kind, item.slug)}
            >
              {item.title}
            </Link>
          </li>
        ))}
      </ul>
    </section>
  );
}
