"use client";

import { useTranslations } from "next-intl";
import { useId, useState } from "react";

// Neither the server nor jsdom can measure whether text overflows three lines, so
// the toggle is decided from an estimate of how much room the text needs. A CJK
// character takes about twice the width of a Latin one, which is why this counts
// columns rather than characters — 90 English words and 90 kanji are not the same
// paragraph. At the card's width three lines hold roughly 200 columns.
const CLAMP_COLUMNS = 200;
const WIDE = /[ᄀ-ᅟ⺀-꓏가-힣豈-﫿︰-﹏＀-｠￠-￦]/;

export function approximateColumns(text: string): number {
  let columns = 0;
  for (const character of text) {
    columns += WIDE.test(character) ? 2 : 1;
  }
  return columns;
}

/** Mokaair's own paragraph about a place: what it is, and when to go. */
export function HotspotIntro({
  text,
  clamp = true,
  className = "",
}: {
  text: string | null | undefined;
  clamp?: boolean;
  className?: string;
}) {
  const t = useTranslations("hotspots");
  const id = useId();
  const [expanded, setExpanded] = useState(false);
  const body = text?.trim();
  if (!body) return null;
  const collapsible = clamp && approximateColumns(body) > CLAMP_COLUMNS;
  return (
    <div className={className}>
      <p className="text-xs font-bold uppercase tracking-[.14em] text-[var(--teal)]">
        {t("introLabel")}
      </p>
      <p
        id={id}
        className={`mt-1 whitespace-pre-line text-sm leading-6 ${
          collapsible && !expanded ? "line-clamp-3" : ""
        }`}
      >
        {body}
      </p>
      {collapsible && (
        <button
          type="button"
          aria-expanded={expanded}
          aria-controls={id}
          onClick={() => setExpanded((current) => !current)}
          className="mt-1 inline-flex min-h-11 items-center text-xs font-semibold text-[var(--teal)]"
        >
          {t(expanded ? "intro.readLess" : "intro.readMore")}
        </button>
      )}
    </div>
  );
}
