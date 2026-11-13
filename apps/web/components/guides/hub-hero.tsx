import { SearchForm, type SearchFormLabels } from "@/components/guides/search-form";
import type { GuideSection } from "@/lib/guides";

/**
 * The top of a section hub: the name, one sentence on what the section is, and a search box
 * scoped to the section.
 *
 * The search is the results page's own GET form (`SearchForm`), so a query has a URL and
 * works with JavaScript off; the section rides along as a hidden field.
 *
 * It used to carry a figures line ("639 篇文章 9 個主題"). The section grows every week, so
 * the number on the page was wrong more often than it was right; the catalogue's size is
 * not what a reader came for, and it is still on the wire for the code that needs it.
 */
export function HubHero({
  title, intro, section, action, labels,
}: {
  title: string;
  intro: string;
  section: GuideSection;
  /** Where the form submits: the locale-prefixed results page. */
  action: string;
  labels: SearchFormLabels;
}) {
  return (
    <header className="rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-6 shadow-[var(--shadow-sm)] md:p-10">
      <h1 className="text-3xl font-extrabold tracking-tight md:text-5xl">{title}</h1>
      <p className="mt-3.5 max-w-2xl text-base leading-7 text-[var(--muted)] md:text-lg md:leading-8">{intro}</p>
      <SearchForm action={action} q="" section={section} labels={labels} />
    </header>
  );
}
