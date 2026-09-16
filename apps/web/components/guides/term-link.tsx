"use client";

import { useEffect, useId, useRef, useState, type KeyboardEvent, type MouseEvent } from "react";

export type TermLinkLabels = { card: string; readMore: string };

const HOVER_DELAY_MS = 150;

/**
 * An in-text link to the article that defines a term, with the definition shown in place.
 *
 * The anchor is a real `<a>` with the article's URL, so a crawler and a reader without
 * JavaScript get the link and nothing else. With JavaScript the card opens after a short
 * pause on hover (so a pointer crossing the paragraph does not open every term), at once
 * on keyboard focus, and closes on blur, Escape or a pointer landing elsewhere. On a
 * device without hover the first tap opens the card and the second follows the link,
 * since a tap cannot hover. The card is a note beside the link, never a modal: nothing
 * else on the page is locked while it shows.
 */
export function TermLink({
  href, text, title, description, labels,
}: {
  href: string;
  text: string;
  title: string;
  description: string;
  labels: TermLinkLabels;
}) {
  const id = useId();
  const cardId = `${id}-card`;
  const root = useRef<HTMLSpanElement>(null);
  const timer = useRef<number | null>(null);
  const [open, setOpen] = useState(false);

  const cancel = () => {
    if (timer.current !== null) window.clearTimeout(timer.current);
    timer.current = null;
  };
  const show = () => { cancel(); setOpen(true); };
  const hide = () => { cancel(); setOpen(false); };
  const showSoon = () => {
    cancel();
    timer.current = window.setTimeout(() => { timer.current = null; setOpen(true); }, HOVER_DELAY_MS);
  };

  useEffect(() => {
    if (!open) return;
    const outside = (event: PointerEvent) => {
      if (event.target instanceof Node && !root.current?.contains(event.target)) setOpen(false);
    };
    document.addEventListener("pointerdown", outside);
    return () => document.removeEventListener("pointerdown", outside);
  }, [open]);
  useEffect(() => cancel, []);

  const onKeyDown = (event: KeyboardEvent<HTMLAnchorElement>) => {
    if (event.key === "Escape" && open) {
      event.preventDefault();
      event.stopPropagation();
      hide();
    }
  };
  const onClick = (event: MouseEvent<HTMLAnchorElement>) => {
    // A tap cannot hover: the first one shows the definition, the next one follows the link.
    const touch = typeof window.matchMedia === "function" && window.matchMedia("(hover: none)").matches;
    if (touch && !open) {
      event.preventDefault();
      show();
    }
  };

  return (
    <span ref={root} className="relative inline">
      <a
        href={href}
        className="app-term-link"
        aria-expanded={open}
        aria-controls={cardId}
        onPointerEnter={showSoon}
        onPointerLeave={hide}
        onFocus={show}
        onBlur={hide}
        onKeyDown={onKeyDown}
        onClick={onClick}
      >
        {text}
      </a>
      <span
        id={cardId}
        role="note"
        aria-label={labels.card}
        hidden={!open}
        className="app-term-card absolute left-0 top-full z-50 mt-2 w-72 max-w-[calc(100vw-2rem)] rounded-2xl p-3 text-sm leading-6"
      >
        <span className="block font-bold">{title}</span>
        <span className="mt-1 block text-[var(--muted)]">{description}</span>
        <span className="mt-2 block font-semibold text-[var(--teal)]">{labels.readMore}</span>
      </span>
    </span>
  );
}
