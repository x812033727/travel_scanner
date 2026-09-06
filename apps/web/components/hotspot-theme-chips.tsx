"use client";

import { type HotspotTheme, isInSeason, monthRangeLabel } from "@/lib/hotspot-themes";

export type ThemeChipItem = { key: string; label: string; count?: number; marker?: string };
export type ThemeChipGroup = { key: string; label: string; items: ThemeChipItem[] };

/**
 * One row per theme kind (季節 / 購物), single-select like the category filter.
 * A theme nobody carries is hidden unless it is the current selection, so an empty
 * facet list renders nothing at all.
 */
export function HotspotThemeChips({
  label,
  allLabel,
  groups,
  value,
  onChange,
}: {
  label: string;
  allLabel: string;
  groups: ThemeChipGroup[];
  value: string;
  onChange: (key: string) => void;
}) {
  const visible = groups
    .map((group) => ({
      ...group,
      items: group.items.filter(
        (item) => item.count === undefined || item.count > 0 || item.key === value,
      ),
    }))
    .filter((group) => group.items.length > 0);
  if (!visible.length) return null;
  return (
    <div role="group" aria-label={label} className="mt-3 grid gap-2">
      {visible.map((group, index) => (
        <div key={group.key} className="app-chip-row items-center">
          <span className="shrink-0 pr-1 text-xs font-bold text-[var(--muted)]">{group.label}</span>
          {index === 0 && (
            <button
              type="button"
              aria-pressed={value === ""}
              onClick={() => onChange("")}
              className={`app-filter-chip ${value === "" ? "app-filter-chip-active" : ""}`}
            >
              {allLabel}
            </button>
          )}
          {group.items.map((item) => (
            <button
              key={item.key}
              type="button"
              aria-pressed={value === item.key}
              onClick={() => onChange(value === item.key ? "" : item.key)}
              className={`app-filter-chip ${value === item.key ? "app-filter-chip-active" : ""}`}
            >
              <span>{item.label}</span>
              {item.marker && (
                <span className="rounded-full bg-[var(--coral)] px-1.5 text-[.62rem] font-bold text-white">
                  {item.marker}
                </span>
              )}
              {item.count !== undefined && <span className="app-filter-count">{item.count}</span>}
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}

/** The themes of one attraction, seasons carrying the months they apply to. */
export function HotspotThemeBadges({
  themes,
  locale,
  currentMonth,
  label,
  inSeasonLabel,
}: {
  themes: HotspotTheme[] | undefined;
  locale: string;
  currentMonth: number;
  label: string;
  inSeasonLabel: string;
}) {
  if (!themes?.length) return null;
  return (
    <ul aria-label={label} className="mt-3 flex flex-wrap gap-1.5">
      {themes.map((theme) => {
        const span = theme.kind === "season" ? monthRangeLabel(theme.months, locale) : "";
        const live = isInSeason(theme, currentMonth);
        return (
          <li
            key={theme.slug}
            className={`inline-flex items-center gap-1 rounded-full px-2.5 py-1 text-xs font-semibold ${
              theme.kind === "season"
                ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]"
                : "bg-[var(--paper)] text-[var(--ink)]"
            }`}
          >
            {live && <span aria-hidden="true" className="h-1.5 w-1.5 rounded-full bg-[var(--coral)]" />}
            <span>{theme.name}</span>
            {span && <span className="font-normal text-[var(--muted)]">· {span}</span>}
            {live && <span className="sr-only">{inSeasonLabel}</span>}
          </li>
        );
      })}
    </ul>
  );
}
