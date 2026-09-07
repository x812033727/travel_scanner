"use client";

import { ChevronDown, ChevronUp } from "lucide-react";
import { useState, type ReactNode } from "react";

/**
 * A wrapping row of filter chips.
 *
 * The row used to scroll sideways with its scrollbar hidden, so on a phone four
 * of the seven themes did not exist as far as the reader could tell. Now every
 * chip wraps into view, and a row long enough to bury the list keeps its first
 * `limit` chips and puts the rest behind a button that says how many are left —
 * what is hidden says so, instead of waiting for a swipe nobody knows to make.
 */
export function ChipRow({
  chips,
  activeIndex,
  leading,
  limit = 6,
  moreLabel,
  fewerLabel,
  className = "",
}: {
  chips: ReactNode[];
  /** Index of the selected chip in `chips`, or -1 when the selection is elsewhere. */
  activeIndex: number;
  leading?: ReactNode;
  limit?: number;
  moreLabel: (count: number) => string;
  fewerLabel: string;
  className?: string;
}) {
  const [expanded, setExpanded] = useState(false);
  // Never fold away the reader's own selection, and never trade one chip for a button.
  const collapsible = chips.length > limit + 1 && activeIndex < limit;
  const open = expanded || !collapsible;
  const hiddenCount = open ? 0 : chips.length - limit;
  return (
    <div className={`app-chip-row ${className}`}>
      {leading}
      {open ? chips : chips.slice(0, limit)}
      {collapsible && (
        <button
          type="button"
          aria-expanded={expanded}
          onClick={() => setExpanded((value) => !value)}
          className="app-filter-chip app-chip-more"
        >
          {hiddenCount > 0 ? moreLabel(hiddenCount) : fewerLabel}
          {hiddenCount > 0 ? <ChevronDown size={15} aria-hidden /> : <ChevronUp size={15} aria-hidden />}
        </button>
      )}
    </div>
  );
}
