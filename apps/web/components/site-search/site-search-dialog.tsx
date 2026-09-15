"use client";

import { X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { usePathname } from "@/i18n/navigation";
import { useModalSheet } from "@/lib/modal-sheet";
import { SiteSearch } from "./site-search";

export const OPEN_SEARCH_EVENT = "mokaair:open-search";

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
 * The full-width search sheet: ⌘K / Ctrl+K on a keyboard, the magnifier in the phone
 * header, or `openSiteSearch()` from anywhere. `useModalSheet` gives it Escape, a Tab trap
 * and the scroll lock; the one thing it does differently from the menu sheet is where
 * focus lands -- in the input, since typing is the whole point of opening it.
 */
export function SiteSearchDialog() {
  const nav = useTranslations("navigation");
  const pathname = usePathname();
  // Open *for this path*, like the menu sheet: navigating away closes it by making the
  // stored path stale, with no effect that has to notice the change.
  const [openPath, setOpenPath] = useState<string | null>(null);
  const open = openPath === pathname;
  const setOpen = (value: boolean) => setOpenPath(value ? pathname : null);
  const input = useRef<HTMLInputElement>(null);
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

  if (!open) return null;
  return createPortal(
    <div role="presentation" className="fixed inset-0 z-[90] bg-slate-950/45 backdrop-blur-sm" onMouseDown={(event) => { if (event.target === event.currentTarget) setOpen(false); }}>
      <div
        ref={sheetRef}
        role="dialog"
        aria-modal="true"
        aria-label={nav("search")}
        className="absolute inset-x-0 top-0 mx-auto max-h-[90vh] w-full max-w-2xl overflow-y-auto rounded-b-[2rem] bg-[var(--surface)] p-5 shadow-2xl sm:top-16 sm:rounded-[2rem]"
      >
        <div className="mb-3 flex items-center justify-between gap-3">
          <p className="text-sm font-bold text-[var(--muted)]">{nav("search")}</p>
          <button type="button" aria-label={nav("closeSearch")} onClick={() => setOpen(false)} className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]">
            <X size={18} />
          </button>
        </div>
        <SiteSearch variant="dialog" inputRef={input} onNavigate={() => setOpen(false)} />
        <p className="mt-3 hidden text-xs text-[var(--muted)] lg:block">{nav("searchShortcut", { keys: "⌘K / Ctrl+K" })}</p>
      </div>
    </div>,
    document.body,
  );
}
