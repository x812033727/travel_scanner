import { ContentBlocks } from "@/components/content-blocks";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { contentBlockLink } from "@/lib/content-blocks";
import { guideHref, type GuideArticleState } from "@/lib/guides";

export type GuideArticleLabels = {
  intel: string;
  howto: string;
  published: string;
  updated: string;
  expiredNotice: string;
  validUntil: string;
  sources: string;
  checkedOn: string;
  destination: string;
  otherLanguages: string;
};

/**
 * An article a reader can reach. Expiry is shown, not hidden: an `intel` notice keeps its
 * URL so existing links do not break, and says plainly what date it applied until.
 */
export function GuideArticle({
  state, labels,
}: {
  state: GuideArticleState & { document: NonNullable<GuideArticleState["document"]> };
  labels: GuideArticleLabels;
}) {
  const { document } = state;
  const published = document.published_at.slice(0, 10);
  const others = state.published_locales.filter((value) => value !== state.locale);
  return (
    <article className="space-y-6 break-words [overflow-wrap:anywhere]">
      <header>
        <p className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">
          <span className="rounded-full bg-[var(--line)] px-2 py-1 text-[var(--fg)]">
            {state.kind === "intel" ? labels.intel : labels.howto}
          </span>
          {state.destination_label ? (
            <Link className="underline" href={`/destinations/${state.destination_id}`}>
              {state.destination_label}
            </Link>
          ) : null}
        </p>
        <h1 className="mt-3 text-3xl font-bold">{document.title}</h1>
        <p className="mt-3 leading-7 text-[var(--muted)]">{document.description}</p>
        <p className="mt-3 text-sm text-[var(--muted)]">
          {labels.published}: <time dateTime={published}>{published}</time>
        </p>
        {state.expired && state.valid_until ? (
          <p role="status" className="mt-4 rounded-2xl border border-[var(--line)] bg-[var(--line)] px-4 py-3 text-sm leading-6">
            {labels.expiredNotice} {labels.validUntil}: <time dateTime={state.valid_until}>{state.valid_until}</time>
          </p>
        ) : null}
      </header>

      <ContentBlocks blocks={document.blocks} />

      {state.topics.length ? (
        <ul className="flex flex-wrap gap-2 border-t border-[var(--line)] pt-6">
          {state.topics.map((topic) => (
            <li key={topic.slug}>
              <Link
                className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] px-3 py-1 text-sm text-[var(--muted)]"
                href={`/guides/${state.kind}?topic=${encodeURIComponent(topic.slug)}`}
              >
                {topic.label}
              </Link>
            </li>
          ))}
        </ul>
      ) : null}

      {document.sources.length ? (
        <section className="border-t border-[var(--line)] pt-6">
          <h2 className="text-lg font-semibold">{labels.sources}</h2>
          <ul className="mt-3 space-y-2">
            {document.sources.map((source, index) => {
              const href = contentBlockLink(source.url);
              return href ? (
                <li key={index} className="text-sm leading-6">
                  <a className="text-[var(--teal)] underline" href={href} target="_blank" rel="noopener noreferrer">
                    {source.title}
                  </a>
                  {source.checked_on ? (
                    <span className="text-[var(--muted)]">
                      {" "}· {labels.checkedOn}: <time dateTime={source.checked_on}>{source.checked_on}</time>
                    </span>
                  ) : null}
                </li>
              ) : null;
            })}
          </ul>
        </section>
      ) : null}

      {others.length ? (
        <section className="border-t border-[var(--line)] pt-6">
          <h2 className="text-lg font-semibold">{labels.otherLanguages}</h2>
          <ul className="mt-3 flex flex-wrap gap-3">
            {others.map((value) => (
              <li key={value}>
                <a
                  className="inline-flex min-h-11 items-center text-[var(--teal)] underline"
                  href={`/${value}${guideHref(state.kind, state.slug)}`}
                  hrefLang={value}
                >
                  {localeLabels[value as Locale]}
                </a>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </article>
  );
}
