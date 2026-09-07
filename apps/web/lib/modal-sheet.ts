"use client";

import { useEffect, useRef } from "react";

/**
 * Make an element behave like the modal sheet it looks like.
 *
 * Measured on the live site before this existed: the filter panel on `/hotspots` reported
 * `role: null`, left focus on the button that opened it, ignored Escape, and let Tab walk
 * out into the page behind the scrim. It looked like a dialog and answered to none of the
 * things a reader expects one to answer to. `/foods` had the same panel and the same gap.
 *
 * The behaviour here matches the site's own working example, `mobile-nav`, and adds the one
 * thing that example is also missing: a real Tab trap. Without it `aria-modal="true"` is a
 * claim the page does not honour — a screen reader is told the rest of the document is
 * inert while the keyboard walks straight into it.
 *
 * Returns a ref to put on the sheet. Nothing happens while `open` is false, so the same
 * element can be an ordinary inline form on a wide screen and a sheet on a narrow one.
 */
export function useModalSheet<T extends HTMLElement>(open: boolean, onClose: () => void) {
  const sheetRef = useRef<T>(null);
  // Read through a ref so a caller passing an inline arrow does not re-run the effect on
  // every render, which would re-steal focus while somebody is typing in the sheet.
  const closeRef = useRef(onClose);
  // Assigned in an effect rather than during render: React forbids touching a ref while
  // rendering, and effects run in declaration order, so this lands before the one below.
  useEffect(() => {
    closeRef.current = onClose;
  });

  useEffect(() => {
    if (!open) return;
    const sheet = sheetRef.current;
    if (!sheet) return;

    // Whatever had focus when the sheet opened, not a ref to one particular button: the
    // sheet can be opened from more than one place, and focus has to go back where it was.
    const opener = document.activeElement as HTMLElement | null;

    // Not offsetParent: jsdom performs no layout, so every element reports null there and a
    // test would exercise an empty list while the browser exercised a full one — the trap
    // would look guarded and be guarded by nothing.
    const hiddenFromReaders = (element: HTMLElement) => {
      if (element.hasAttribute("hidden") || element.closest('[aria-hidden="true"]')) return true;
      const style = window.getComputedStyle(element);
      return style.display === "none" || style.visibility === "hidden";
    };

    const focusable = () =>
      Array.from(
        sheet.querySelectorAll<HTMLElement>(
          'a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex]:not([tabindex="-1"])',
        ),
      ).filter((element) => !hiddenFromReaders(element));

    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        event.stopPropagation();
        closeRef.current();
        return;
      }
      if (event.key !== "Tab") return;
      const items = focusable();
      if (items.length === 0) return;
      const first = items[0];
      const last = items[items.length - 1];
      const active = document.activeElement;
      // Wrapping only at the ends leaves normal tabbing alone; the third branch catches
      // focus that is already outside, which happens when the browser restores it after a
      // click on the scrim.
      if (!event.shiftKey && active === last) {
        event.preventDefault();
        first.focus();
      } else if (event.shiftKey && active === first) {
        event.preventDefault();
        last.focus();
      } else if (active instanceof Node && !sheet.contains(active)) {
        event.preventDefault();
        (event.shiftKey ? last : first).focus();
      }
    };

    document.addEventListener("keydown", onKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    // The close button first, like mobile-nav: the way out should be the first thing a
    // reader meets, not the last.
    const target =
      sheet.querySelector<HTMLElement>("button[aria-label]") ?? focusable()[0] ?? sheet;
    target.focus();

    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
      // Escape used to leave focus on <body>, which returns a keyboard reader to the top of
      // the document, several tabs from the control they had just used.
      opener?.focus?.();
    };
  }, [open]);

  return sheetRef;
}
