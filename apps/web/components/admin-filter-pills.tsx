"use client";

import { ChevronDown } from "lucide-react";
import { useSyncExternalStore, type ReactNode } from "react";

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
                className={`rounded-full px-1.5 text-xs tabular-nums ${
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


/**
 * Filters folded away behind one line saying what they are currently set to.
 *
 * The hotspot review page put about thirty controls above the first candidate: two rows of
 * pills, six fields, and three batch buttons that do nothing until something is selected.
 * Someone clearing hundreds of rows a day rarely changes the filters and always needs the
 * first decision, so the filters start closed and the choice is remembered per browser.
 */const listeners = new Set<() => void>();

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

function isOpen(storageKey: string) {
  try {
    return window.localStorage.getItem(storageKey) === "open";
  } catch {
    // A browser that refuses storage still gets a working panel, just always closed.
    return false;
  }
}

export function FilterDisclosure({
  label,
  summary,
  showLabel,
  hideLabel,
  storageKey,
  children,
}: {
  label: string;
  summary: string;
  showLabel: string;
  hideLabel: string;
  storageKey: string;
  children: ReactNode;
}) {
  // The server has no localStorage, so it renders closed and the browser corrects it on
  // hydration; useSyncExternalStore is how React wants that read done.
  const open = useSyncExternalStore(
    subscribe,
    () => isOpen(storageKey),
    () => false,
  );

  function toggle() {
    try {
      window.localStorage.setItem(storageKey, open ? "closed" : "open");
    } catch {
      // Not remembering the choice is better than not being able to make it.
    }
    for (const listener of listeners) listener();
  }

  return (
    <div className="rounded-2xl border border-[var(--line)] bg-white">
      <button
        type="button"
        onClick={toggle}
        aria-expanded={open}
        aria-label={open ? hideLabel : showLabel}
        className="flex min-h-12 w-full items-center gap-3 px-4 text-left"
      >
        <span className="font-semibold">{label}</span>
        <span className="min-w-0 flex-1 truncate text-sm text-[var(--muted)]">{summary}</span>
        <ChevronDown
          size={18}
          className={`shrink-0 transition-transform ${open ? "rotate-180" : ""}`}
          aria-hidden="true"
        />
      </button>
      {open && <div className="border-t border-[var(--line)] p-4">{children}</div>}
    </div>
  );
}
