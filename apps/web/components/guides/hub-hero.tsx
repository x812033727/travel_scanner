import { SearchForm, type SearchFormLabels } from "@/components/guides/search-form";
import type { GuideSection } from "@/lib/guides";

/**
 * The top of a section hub: the name, one sentence on what the section is, a search box
 * scoped to the section, and the figures that tell a reader how much is here.
 *
 * The search is the results page's own GET form (`SearchForm`), so a query has a URL and
 * works with JavaScript off; the section rides along as a hidden field. The figures are
 * pre-formatted by the page, which owns the translations, and a figure the page could not
 * learn (the API did not answer the count) is simply left out rather than shown as zero.
 */
export function HubHero({
  title, intro, section, action, stats, labels,
}: {
  title: string;
  intro: string;
  section: GuideSection;
  /** Where the form submits: the locale-prefixed results page. */
  action: string;
  stats: readonly (string | null)[];
  labels: SearchFormLabels;
}) {
  const shown = stats.filter((value): value is string => Boolean(value));
  return (
    <header className="rounded-3xl border border-[var(--line)] bg-[var(--paper)] p-6 md:p-10">
      <h1 className="text-4xl font-bold tracking-tight md:text-5xl">{title}</h1>
      <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{intro}</p>
      <SearchForm action={action} q="" section={section} labels={labels} />
      {shown.length ? (
        <p className="mt-4 flex flex-wrap gap-x-5 gap-y-1 text-[length:var(--text-meta)] text-[var(--muted)]" data-testid="hub-stats">
          {shown.map((value) => <span key={value}>{value}</span>)}
        </p>
      ) : null}
    </header>
  );
}
