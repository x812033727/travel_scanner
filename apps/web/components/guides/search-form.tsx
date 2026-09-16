import { Search } from "lucide-react";
import type { GuideSection } from "@/lib/guides";

export type SearchFormLabels = { label: string; placeholder: string; submit: string };

/**
 * The results page's own search box: a plain GET form, so the page works with JavaScript
 * off, a result set has a URL, and the browser's back button does what a reader expects.
 * The section travels as a hidden field so changing the words keeps the scope.
 */
export function SearchForm({
  action, q, section, labels,
}: {
  action: string;
  q: string;
  section: GuideSection | null;
  labels: SearchFormLabels;
}) {
  return (
    <form role="search" method="get" action={action} className="mt-6 flex flex-wrap gap-2">
      <label className="sr-only" htmlFor="article-search-q">{labels.label}</label>
      <input
        id="article-search-q"
        className="app-field min-w-0 flex-1 basis-64"
        type="search"
        name="q"
        defaultValue={q}
        placeholder={labels.placeholder}
        maxLength={100}
        autoComplete="off"
        required
      />
      {section ? <input type="hidden" name="section" value={section} /> : null}
      <button type="submit" className="app-primary-button min-h-12 px-5">
        <Search size={18} aria-hidden />
        {labels.submit}
      </button>
    </form>
  );
}
