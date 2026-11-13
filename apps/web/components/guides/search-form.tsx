import { Search } from "lucide-react";
import type { GuideSearchSort, GuideSection } from "@/lib/guides";

export type SearchFormLabels = { label: string; placeholder: string; submit: string };

/**
 * The results page's own search box: a plain GET form, so the page works with JavaScript
 * off, a result set has a URL, and the browser's back button does what a reader expects.
 * Active scope, topic and sort travel as hidden fields so changing keywords keeps them.
 */
export function SearchForm({
  action,
  q,
  section,
  topic,
  sort,
  labels,
}: {
  action: string;
  q: string;
  section: GuideSection | null;
  topic?: string | null;
  sort?: GuideSearchSort | null;
  labels: SearchFormLabels;
}) {
  return (
    <form role="search" method="get" action={action} className="mt-6 flex flex-wrap gap-2">
      <label className="sr-only" htmlFor="article-search-q">{labels.label}</label>
      <input
        id="article-search-q"
        className="app-field min-w-0 flex-1 basis-64 focus-visible:border-[var(--teal)] focus-visible:outline-none"
        type="search"
        name="q"
        defaultValue={q}
        placeholder={labels.placeholder}
        maxLength={100}
        autoComplete="off"
        required
      />
      {section ? <input type="hidden" name="section" value={section} /> : null}
      {topic ? <input type="hidden" name="topic" value={topic} /> : null}
      {sort && sort !== "relevance" ? <input type="hidden" name="sort" value={sort} /> : null}
      <button type="submit" className="app-primary-button min-h-12 px-5">
        <Search size={18} aria-hidden />
        {labels.submit}
      </button>
    </form>
  );
}
