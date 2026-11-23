"use client";

import { X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Link, usePathname } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { guideHref, type GuideSummary } from "@/lib/guides";
import { useModalSheet } from "@/lib/modal-sheet";
import { SiteSearch } from "./site-search";

export const OPEN_SEARCH_EVENT = "mokaair:open-search";

const QUICK_TOPICS: ReadonlyArray<{ labelKey: string; href: string }> = [
  { labelKey: "ai", href: "/ai" },
  { labelKey: "item_aiNews", href: "/life/topics/ai-news" },
  { labelKey: "item_techNews", href: "/life/topics/tech-news" },
  { labelKey: "item_software", href: "/life/topics/software" },
  { labelKey: "guides", href: "/guides" },
  { labelKey: "item_finance", href: "/life/topics/finance" },
];

/** Opens the search dialog from anywhere: the phone header's icon lives in a different
 *  component tree from the dialog, and a window event is lighter than a provider for a
 *  single verb. */
export function openSiteSearch() {
  window.dispatchEvent(new CustomEvent(OPEN_SEARCH_EVENT));
}

function isSearchShortcut(event: KeyboardEvent): boolean {
  return (event.metaKey || event.ctrlKey) && !event.altKey && !event.shiftKey && event.key.toLowerCase() === "k";
}

/**
 * The full-width search sheet: Cmd+K / Ctrl+K on a keyboard, the magnifier in the phone
 * header, or `openSiteSearch()` from anywhere. `useModalSheet` gives it Escape, a Tab trap
 * and the scroll lock; the one thing it does differently from the menu sheet is where
 * focus lands -- in the input, since typing is the whole point of opening it.
 */
export function SiteSearchDialog() {
  const nav = useTranslations("navigation");
  const locale = useLocale();
  const pathname = usePathname();
  // Open *for this path*, like the menu sheet: navigating away closes it by making the
  // stored path stale, with no effect that has to notice the change.
  const [openPath, setOpenPath] = useState<string | null>(null);
  const [trending, setTrending] = useState<GuideSummary[]>([]);
  const open = openPath === pathname;
  const setOpen = (value: boolean) => setOpenPath(value ? pathname : null);
  const input = useRef<HTMLInputElement>(null);
  const inflightLocale = useRef<string | null>(null);
  const loadedLocale = useRef<string | null>(null);
  const sheetRef = useModalSheet<HTMLDivElement>(open, () => setOpenPath(null));

  useEffect(() => {
    const show = () => setOpenPath(pathname);
    const onKeyDown = (event: KeyboardEvent) => {
      if (!isSearchShortcut(event) || event.defaultPrevented) return;
      event.preventDefault();
      setOpenPath((current) => (current === pathname ? null : pathname));
    };
    window.addEventListener(OPEN_SEARCH_EVENT, show);
    window.addEventListener("keydown", onKeyDown);
    return () => {
      window.removeEventListener(OPEN_SEARCH_EVENT, show);
      window.removeEventListener("keydown", onKeyDown);
    };
  }, [pathname]);

  // After the sheet's own focus pass (a layout effect that picks the close button).
  useEffect(() => { if (open) input.current?.focus(); }, [open]);

  useEffect(() => {
    if (!open || loadedLocale.current === locale || inflightLocale.current === locale) return;
    inflightLocale.current = locale;
    let cancelled = false;
    Promise.resolve(
      api<{ articles?: GuideSummary[] }>(`/guides/trending?locale=${encodeURIComponent(locale)}&limit=5`),
    )
      .then((result) => {
        inflightLocale.current = null;
        if (cancelled || !result || !Array.isArray(result.articles)) return;
        loadedLocale.current = locale;
        setTrending(result.articles);
      })
      .catch(() => {
        inflightLocale.current = null;
      });
    return () => {
      cancelled = true;
      inflightLocale.current = null;
    };
  }, [open, locale]);

  if (!open) return null;
  return createPortal(
    <div role="presentation" className="fixed inset-0 z-[90] bg-slate-950/45 backdrop-blur-sm" onMouseDown={(event) => { if (event.target === event.currentTarget) setOpen(false); }}>
      <div
        ref={sheetRef}
        role="dialog"
        aria-modal="true"
        aria-label={nav("search")}
        className="absolute inset-x-0 top-0 mx-auto max-h-[88dvh] w-full max-w-2xl overflow-y-auto rounded-b-[1.75rem] border-b border-[var(--line)] bg-[var(--surface)] px-4 pb-[calc(1.25rem+env(safe-area-inset-bottom))] pt-4 shadow-2xl sm:top-16 sm:max-h-[85vh] sm:rounded-[2rem] sm:border sm:p-6"
      >
        <div className="mb-3 flex items-center justify-between gap-3">
          <p className="text-sm font-bold text-[var(--muted)]">{nav("search")}</p>
          <button type="button" aria-label={nav("closeSearch")} onClick={() => setOpen(false)} className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)] bg-[var(--paper)]/60 transition-colors hover:border-[var(--teal)]">
            <X size={18} />
          </button>
        </div>
        <SiteSearch variant="dialog" inputRef={input} onNavigate={() => setOpen(false)} />
        {trending.length > 0 ? (
          <div data-testid="search-trending" className="mt-4 border-t border-[var(--line)] pt-3">
            <p className="text-[length:var(--text-xs)] font-semibold uppercase tracking-wide text-[var(--muted)]">{nav("searchTrending")}</p>
            <ol className="mt-2 grid gap-1">
              {trending.map((item, index) => (
                <li key={`${item.kind}:${item.slug}`}>
                  <Link
                    href={guideHref(item.kind, item.slug)}
                    onClick={() => setOpen(false)}
                    className="flex min-h-11 items-center gap-2.5 rounded-xl px-2.5 py-2 text-sm font-medium text-[var(--ink)] transition-colors hover:bg-[var(--paper)] hover:text-[var(--teal)]"
                  >
                    <span className="inline-grid h-6 w-6 flex-none place-items-center rounded-md bg-[var(--teal-soft)] font-mono text-[length:var(--text-xs)] font-bold tabular-nums text-[var(--teal-dark)]">{index + 1}</span>
                    <span className="line-clamp-1">{item.title}</span>
                  </Link>
                </li>
              ))}
            </ol>
          </div>
        ) : null}
        <div data-testid="search-hot-topics" className="mt-4 border-t border-[var(--line)] pt-3">
          <p className="text-[length:var(--text-xs)] font-semibold uppercase tracking-wide text-[var(--muted)]">{nav("searchHotTopics")}</p>
          <div className="portal-scroll-strip mt-2 flex items-center gap-2 sm:flex-wrap sm:overflow-visible">
            {QUICK_TOPICS.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setOpen(false)}
                className="inline-flex min-h-11 shrink-0 snap-start items-center whitespace-nowrap rounded-full border border-[var(--line)] bg-[var(--paper)] px-3.5 text-[length:var(--text-xs)] font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
              >
                {nav(item.labelKey)}
              </Link>
            ))}
          </div>
        </div>
        <p className="mt-3 hidden text-[length:var(--text-xs)] text-[var(--muted)] lg:block">{nav("searchShortcut", { keys: "⌘K / Ctrl+K" })}</p>
      </div>
    </div>,
    document.body,
  );
}
