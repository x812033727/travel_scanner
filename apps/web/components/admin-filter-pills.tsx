"use client";

export type FilterPillOption = { code: string; label: string; count?: number };

type FilterPillsProps = {
  label: string;
  allLabel: string;
  allCount?: number;
  options: FilterPillOption[];
  value: string;
  onChange: (code: string) => void;
};

/**
 * One row of quick filters with live counts. Callers must always include the
 * currently selected code in `options`, even with a zero count, so it stays
 * visible and can be cleared.
 */
export function FilterPills({
  label,
  allLabel,
  allCount,
  options,
  value,
  onChange,
}: FilterPillsProps) {
  const pills: FilterPillOption[] = [{ code: "", label: allLabel, count: allCount }, ...options];
  return (
    <div role="group" aria-label={label} className="flex flex-wrap gap-2">
      {pills.map((option) => {
        const active = value === option.code;
        return (
          <button
            key={option.code || "__all"}
            type="button"
            aria-pressed={active}
            disabled={!active && option.count === 0}
            onClick={() => onChange(option.code)}
            className={`flex shrink-0 items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-semibold transition disabled:opacity-40 ${
              active
                ? "border-[var(--ink)] bg-[var(--ink)] text-white"
                : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--ink)]"
            }`}
          >
            {option.label}
            {option.count != null && (
              <span
                className={`rounded-full px-1.5 text-[.65rem] tabular-nums ${
                  active ? "bg-white/20" : "bg-[var(--paper)] text-[var(--muted)]"
                }`}
              >
                {option.count}
              </span>
            )}
          </button>
        );
      })}
    </div>
  );
}
