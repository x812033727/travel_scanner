import { ArrowRight } from "lucide-react";
import { Link } from "@/i18n/navigation";
import type { ArticleReference } from "@/lib/guide-series";
import { guideHref, type GuideKind } from "@/lib/guides";

export const RELATED_GRID_LIMIT = 4;

function RelatedNewsRow({ item, lead, kindLabel }: { item: ArticleReference; lead: boolean; kindLabel: string }) {
  return (
    <li className={lead ? "mb-1" : "border-b border-[var(--line)]"}>
      <Link
        href={guideHref(item.kind, item.slug)}
        aria-label={item.title}
        className={`group flex min-h-11 items-center justify-between gap-3 text-[var(--ink)] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--teal)] ${lead
          ? "rounded-xl border-s-4 border-[var(--teal)] bg-[var(--teal-soft)] px-4 py-4 sm:px-5"
          : "rounded-sm px-1 py-3.5 hover:bg-[var(--surface-tint)]"}`}
      >
        <div className="min-w-0">
          {item.kind !== "life" ? <span className="mb-1 block text-xs font-semibold text-[var(--muted)]">{kindLabel}</span> : null}
          <h3 className={`[overflow-wrap:anywhere] font-bold tracking-tight underline-offset-4 group-hover:text-[var(--teal-dark)] group-hover:underline group-focus-visible:underline ${lead
            ? "text-xl leading-snug sm:text-2xl" : "text-base leading-6"}`}>
            {item.title}
          </h3>
          {lead && item.description ? <p className="mt-2 line-clamp-2 text-sm leading-6 text-[var(--muted)]">{item.description}</p> : null}
        </div>
        <ArrowRight size={18} aria-hidden="true" className="shrink-0 text-[var(--teal-dark)]" />
      </Link>
    </li>
  );
}

/**
 * What to read next, as the API ranked it: the editor's picks first, then the nearest
 * published neighbours. A reference carries a title and a description, not a card's hero
 * or topics, so this draws its own compact card rather than a `GuideCard`. `exclude` is
 * for the series navigation above it, which already lists a lesson's own related lessons.
 */
export function RelatedGrid({
  heading, items, kindLabels, exclude = [], layout = "cards",
}: {
  heading: string;
  items: readonly ArticleReference[];
  kindLabels: Record<GuideKind, string>;
  exclude?: readonly string[];
  layout?: "cards" | "news";
}) {
  const shown = items.filter((item) => !exclude.includes(item.slug)).slice(0, RELATED_GRID_LIMIT);
  if (!shown.length) return null;
  return (
    <section data-testid="related-grid" aria-labelledby="related-grid-heading" className="border-t border-[var(--line)] pt-8">
      <h2 id="related-grid-heading" className="portal-section-heading text-xl font-extrabold tracking-tight">{heading}</h2>
      <ul className={layout === "news" ? "mt-4" : "mt-4 grid grid-cols-1 gap-4 sm:grid-cols-2"}>
        {shown.map((item, index) => layout === "news" ? (
          <RelatedNewsRow key={`${item.kind}:${item.slug}`} item={item} lead={index === 0} kindLabel={kindLabels[item.kind]} />
        ) : (
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
