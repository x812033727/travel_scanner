"use client";

import { ChipRow } from "@/components/chip-row";

export type FilterChipItem = { key: string; label: string; count?: number };

export function FoodFilterChips({
  label,
  allLabel,
  items,
  value,
  onChange,
  moreLabel,
  fewerLabel,
}: {
  label: string;
  allLabel: string;
  items: FilterChipItem[];
  value: string;
  onChange: (key: string) => void;
  moreLabel: (count: number) => string;
  fewerLabel: string;
}) {
  const visible = items.filter(
    (item) => item.count === undefined || item.count > 0 || item.key === value,
  );
  const chips = [
    <button
      key="__all"
      type="button"
      aria-pressed={value === ""}
      onClick={() => onChange("")}
      className={`app-filter-chip ${value === "" ? "app-filter-chip-active" : ""}`}
    >
      {allLabel}
    </button>,
    ...visible.map((item) => (
      <button
        key={item.key}
        type="button"
        aria-pressed={value === item.key}
        onClick={() => onChange(value === item.key ? "" : item.key)}
        className={`app-filter-chip ${value === item.key ? "app-filter-chip-active" : ""}`}
      >
        <span>{item.label}</span>
        {item.count !== undefined && <span className="app-filter-count">{item.count}</span>}
      </button>
    )),
  ];
  const selected = visible.findIndex((item) => item.key === value);
  return (
    <div role="group" aria-label={label}>
      <ChipRow
        chips={chips}
        activeIndex={selected < 0 ? 0 : selected + 1}
        moreLabel={moreLabel}
        fewerLabel={fewerLabel}
        className="mt-3"
      />
    </div>
  );
}
