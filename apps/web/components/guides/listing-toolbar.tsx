import { SearchForm, type SearchFormLabels } from "@/components/guides/search-form";
import { TopicChips, type TopicChipLabels } from "@/components/guides/topic-chips";
import { Link } from "@/i18n/navigation";
import type { GuideListSort, GuideSection, GuideTopic } from "@/lib/guides";

export type ListingToolbarLabels = TopicChipLabels & { sortLabel: string; sortCurated: string; sortLatest: string };

/** Featured first is the reader's default on the lists that offer a choice, so it leads.
 *  `news` is not a choice: a news list has that one order and draws no toggle. */
const SORTS = ["curated", "latest"] as const;
type ToggleSort = typeof SORTS[number];

/** The order the list is in and where each order's link goes, cursor dropped: a reader
 *  who changes the order starts from the top of it. */
export type ListingSort = { current: GuideListSort; hrefs: Record<ToggleSort, string> };

/**
 * What sits between a listing's heading and its cards, on the section listings and the
 * topic hubs alike: the topic chips (plain links to the topic hubs) and the order as two
 * links (`?sort=`, so a choice has a URL and works with JavaScript off). It sticks under
 * the site header on wider screens (`.app-listing-toolbar`), so the chips stay in reach
 * halfway down a long page.
 *
 * It used to carry the result count as well. A listing grows every week, so the figure was
 * out of date almost immediately, and it told a reader nothing they could act on.
 */
export function ListingToolbar({
  section, topics, active, allHref, sort = null, labels,
}: {
  section: GuideSection;
  topics: readonly GuideTopic[];
  active: string | null;
  allHref: string;
  /** Omitted on a listing with one order only. */
  sort?: ListingSort | null;
  labels: ListingToolbarLabels;
}) {
  const sortLabel = (value: ToggleSort) => (value === "curated" ? labels.sortCurated : labels.sortLatest);
  return (
    <div
      className="app-listing-toolbar -mx-5 mt-6 border-b border-[var(--line)] bg-[var(--surface)] px-5 py-3 md:-mx-8 md:px-8"
      data-testid="listing-toolbar"
    >
      <TopicChips section={section} topics={topics} active={active} allHref={allHref} labels={labels} className="grid gap-2" />
      {sort ? (
        <div className="mt-3 flex flex-wrap items-center justify-end gap-3">
          <nav aria-label={labels.sortLabel} className="flex flex-wrap gap-2">
            {SORTS.map((value) => (
              <Link
                key={value}
                href={sort.hrefs[value]}
                aria-current={sort.current === value ? "page" : undefined}
                className={`app-filter-chip ${sort.current === value ? "app-filter-chip-active" : ""}`}
              >
                {sortLabel(value)}
              </Link>
            ))}
          </nav>
        </div>
      ) : null}
    </div>
  );
}

export type ListingEmptyLabels = SearchFormLabels & { empty: string; hint: string };

/**
 * A listing with nothing under its filters: says so, points at the chips above, and offers
 * the section's search -- the results page's GET form, so it works with JavaScript off.
 */
export function ListingEmpty({ section, action, labels }: { section: GuideSection; action: string; labels: ListingEmptyLabels }) {
  return (
    <div className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-6" data-testid="listing-empty">
      <p className="leading-7">{labels.empty}</p>
      <p className="mt-1 text-[var(--muted)]">{labels.hint}</p>
      <SearchForm action={action} q="" section={section} labels={labels} />
    </div>
  );
}
