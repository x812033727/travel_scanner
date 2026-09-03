"use client";

export type FilterChipItem = { key: string; label: string; count?: number };

export function FoodFilterChips({
  label,
  allLabel,
  items,
  value,
  onChange,
}: {
  label: string;
  allLabel: string;
  items: FilterChipItem[];
  value: string;
  onChange: (key: string) => void;
}) {
  const visible = items.filter(
    (item) => item.count === undefined || item.count > 0 || item.key === value,
  );
  return (
    <div role="group" aria-label={label} className="app-chip-row mt-3">
      <button
        type="button"
        aria-pressed={value === ""}
        onClick={() => onChange("")}
        className={`app-filter-chip ${value === "" ? "app-filter-chip-active" : ""}`}
      >
        {allLabel}
      </button>
      {visible.map((item) => (
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
      ))}
    </div>
  );
}
