"use client";

import { useEffect, useId, useLayoutEffect, useRef, useState } from "react";
import { ArrowUp, List, X } from "lucide-react";
import { modalFocusTargets, registerModalLayer } from "@/lib/modal-sheet";

export type ArticleTocHeading = {
  id: string;
  text: string;
};

function useScrollProgress(newsReading: boolean): number {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    const story = newsReading ? document.querySelector<HTMLElement>("[data-news-body]") : null;
    let bottomNav: Element | null = null;
    function updateProgress() {
      const doc = document.documentElement;
      if (story) {
        const bounds = story.getBoundingClientRect();
        // The navigation can mount after its feature settings load.
        if (!bottomNav?.isConnected) bottomNav = document.querySelector(".app-bottom-nav");
        const nav = bottomNav?.getBoundingClientRect();
        const readingEdge = nav?.height ? Math.min(doc.clientHeight, nav.top) : doc.clientHeight;
        // Begin when the story enters view. Finish when its last line clears the bottom navigation.
        const start = Math.max(0, window.scrollY + bounds.top - readingEdge);
        const end = window.scrollY + bounds.bottom - readingEdge;
        const ratio = end <= start ? Number(window.scrollY >= end) : (window.scrollY - start) / (end - start);
        setProgress(Math.floor(Math.max(0, Math.min(1, ratio)) * 100));
        return;
      }
      const scrollable = doc.scrollHeight - doc.clientHeight;
      if (scrollable <= 0) {
        setProgress(0);
        return;
      }
      const ratio = Math.min(1, Math.max(0, window.scrollY / scrollable));
      setProgress(Math.round(ratio * 100));
    }

    updateProgress();
    window.addEventListener("scroll", updateProgress, { passive: true });
    window.addEventListener("resize", updateProgress);
    const observer = story && typeof ResizeObserver !== "undefined" ? new ResizeObserver(updateProgress) : null;
    if (story && observer) {
      observer.observe(story);
      const article = story.closest("article");
      if (article) observer.observe(article);
      if (bottomNav) observer.observe(bottomNav);
    }
    return () => {
      window.removeEventListener("scroll", updateProgress);
      window.removeEventListener("resize", updateProgress);
      observer?.disconnect();
    };
  }, [newsReading]);

  return progress;
}

function useActiveHeading(headings: readonly ArticleTocHeading[]) {
  const [activeId, setActiveId] = useState<string>(headings[0]?.id ?? "");

  useEffect(() => {
    if (!headings.length || typeof IntersectionObserver === "undefined") return;
    const elements = headings
      .map((heading) => document.getElementById(heading.id))
      .filter((el): el is HTMLElement => el !== null);
    if (!elements.length) return;

    const observer = new IntersectionObserver(
      (entries) => {
        const visible = entries
          .filter((entry) => entry.isIntersecting)
          .sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
        if (visible[0]?.target.id) {
          setActiveId(visible[0].target.id);
        }
      },
      { rootMargin: "-96px 0px -65% 0px", threshold: [0, 1] },
    );

    for (const el of elements) observer.observe(el);
    return () => observer.disconnect();
  }, [headings]);

  return [activeId, setActiveId] as const;
}

const EMPTY_HEADINGS: readonly ArticleTocHeading[] = [];

function focusHeading(heading: HTMLElement | null) {
  if (!heading) return;
  if (!heading.hasAttribute("tabindex")) heading.tabIndex = -1;
  heading.focus({ preventScroll: true });
}

function backToArticleTop() {
  focusHeading(document.querySelector("main article h1"));
  window.scrollTo({ top: 0, behavior: window.matchMedia?.("(prefers-reduced-motion: reduce)").matches ? "instant" : "smooth" });
}

/**
 * Mobile/tablet reading progress bar pinned under the viewport top edge plus floating
 * quick-jump TOC sheet and back-to-top actions that clear the bottom tab bar once the
 * reader is deep into an article.
 */
export function ArticleMobileProgress({
  backToTopLabel,
  headings = EMPTY_HEADINGS,
  contentsLabel,
  closeLabel,
  newsReading = false,
}: {
  backToTopLabel: string;
  headings?: readonly ArticleTocHeading[];
  contentsLabel?: string;
  closeLabel?: string;
  newsReading?: boolean;
}) {
  const progress = useScrollProgress(newsReading);
  const [activeId, setActiveId] = useActiveHeading(headings);
  const [sheetOpen, setSheetOpen] = useState(false);
  const dialogRef = useRef<HTMLDialogElement>(null);
  const dialogId = useId();

  useLayoutEffect(() => {
    const dialog = dialogRef.current;
    if (!sheetOpen || !dialog) return;
    if (!dialog.open) dialog.showModal();
    dialog.querySelector("button")?.focus({ preventScroll: true });
    const unlock = registerModalLayer(dialog);
    const desktop = window.matchMedia?.("(min-width: 64rem)");
    const closeOnDesktop = () => {
      if (!desktop?.matches) return;
      dialog.close();
      document.querySelector<HTMLElement>("[data-article-toc] a[aria-current]")?.focus({ preventScroll: true });
    };
    closeOnDesktop();
    desktop?.addEventListener("change", closeOnDesktop);
    return () => {
      desktop?.removeEventListener("change", closeOnDesktop);
      unlock();
    };
  }, [sheetOpen]);

  const showTocTrigger = headings.length > 0 && Boolean(contentsLabel);

  return (
    <>
      <div
        aria-hidden="true"
        className="pointer-events-none fixed inset-x-0 z-40 h-[3px] bg-transparent lg:hidden"
        style={{ top: "var(--ad-anchor-top, 0px)" }}
      >
        <div
          className="h-full bg-[linear-gradient(90deg,var(--teal)_0%,var(--coral-bright)_100%)] transition-[width] duration-150 motion-reduce:transition-none"
          style={{ width: `${progress}%` }}
        />
      </div>
      {progress >= 28 && (!newsReading || progress < 100) ? (
        <div
          style={{ bottom: "calc(5.25rem + env(safe-area-inset-bottom) + var(--ad-anchor-bottom, 0px))" }}
          className="fixed right-4 z-40 flex items-center gap-2 lg:hidden"
        >
          {showTocTrigger ? (
            <button
              type="button"
              aria-haspopup="dialog"
              aria-controls={sheetOpen ? dialogId : undefined}
              aria-expanded={sheetOpen}
              onClick={(event) => {
                event.currentTarget.focus({ preventScroll: true });
                setSheetOpen(true);
              }}
              className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--surface)]/95 px-3.5 py-2 text-[length:var(--text-xs)] font-semibold text-[var(--ink)] shadow-[var(--shadow-md)] backdrop-blur-md transition-transform active:scale-95"
            >
              <List className="h-3.5 w-3.5 text-[var(--teal)]" aria-hidden="true" />
              <span>{contentsLabel}</span>
            </button>
          ) : null}
          {!showTocTrigger || !newsReading ? (
            <button
              type="button"
              onClick={backToArticleTop}
              className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--teal)] bg-[var(--surface)]/95 px-3.5 py-2 text-[length:var(--text-xs)] font-semibold text-[var(--teal-dark)] shadow-[var(--shadow-md)] backdrop-blur-md transition-transform active:scale-95"
            >
              <ArrowUp className="h-3.5 w-3.5" aria-hidden="true" />
              <span>{backToTopLabel}</span>
            </button>
          ) : null}
        </div>
      ) : null}

      {sheetOpen && showTocTrigger ? (
        <dialog
          ref={dialogRef}
          id={dialogId}
          aria-label={contentsLabel}
          onClose={() => setSheetOpen(false)}
          onKeyDown={(event) => {
            if (event.key !== "Tab") return;
            const items = modalFocusTargets(event.currentTarget);
            const first = items[0];
            const last = items.at(-1);
            if (event.shiftKey && document.activeElement === first) {
              event.preventDefault();
              last?.focus();
            } else if (!event.shiftKey && document.activeElement === last) {
              event.preventDefault();
              first?.focus();
            }
          }}
          onClick={(event) => {
            if (event.target === event.currentTarget) event.currentTarget.close();
          }}
          style={{
            paddingBottom: "calc(0.75rem + env(safe-area-inset-bottom) + var(--ad-anchor-bottom, 0px))",
            paddingTop: "calc(0.75rem + env(safe-area-inset-top) + var(--ad-anchor-top, 0px))",
          }}
          className="fixed inset-0 m-0 h-dvh max-h-none w-full max-w-none items-end bg-transparent p-3 text-[var(--ink)] open:flex backdrop:bg-black/45 backdrop:backdrop-blur-[2px]"
        >
          <div
            className="max-h-[min(72dvh,100%)] w-full overflow-y-auto overscroll-contain rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-4 shadow-[var(--shadow-lg)] sm:p-5"
          >
            <div className="flex items-center justify-between gap-3 border-b border-[var(--line)] pb-3">
              <div className="flex items-center gap-2.5">
                <p className="portal-section-heading text-sm font-extrabold uppercase tracking-wider text-[var(--teal-dark)]">
                  {contentsLabel}
                </p>
                <span className="rounded-full bg-[var(--teal-soft)] px-2 py-0.5 font-mono text-[length:var(--text-xs)] font-semibold tabular-nums text-[var(--teal-dark)]">
                  {progress}%
                </span>
              </div>
              <button
                type="button"
                aria-label={closeLabel ?? contentsLabel}
                onClick={() => dialogRef.current?.close()}
                className="inline-grid min-h-11 min-w-11 place-items-center rounded-full border border-[var(--line)] text-[var(--muted)] transition-colors hover:border-[var(--teal)] hover:text-[var(--ink)]"
              >
                <X size={18} aria-hidden="true" />
              </button>
            </div>
            <ol className="mt-3 space-y-1 text-sm leading-6">
              {headings.map((heading, index) => {
                const isActive = heading.id === activeId;
                return (
                  <li key={heading.id}>
                    <a
                      href={`#${heading.id}`}
                      aria-current={isActive ? "location" : undefined}
                      onClick={(event) => {
                        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
                        setActiveId(heading.id);
                        dialogRef.current?.close();
                        focusHeading(document.getElementById(heading.id));
                      }}
                      className={`flex min-h-11 items-center rounded-xl px-3 py-2 transition-colors ${
                        isActive
                          ? "bg-[var(--teal-soft)] font-semibold text-[var(--teal-dark)]"
                          : "text-[var(--ink)] hover:bg-[var(--paper)]"
                      }`}
                    >
                      <span className="mr-2 font-mono text-[length:var(--text-xs)] font-semibold text-[var(--muted)]">
                        {index + 1}.
                      </span>
                      <span className="min-w-0">{heading.text}</span>
                    </a>
                  </li>
                );
              })}
            </ol>
            {newsReading ? (
              <button
                type="button"
                onClick={() => { dialogRef.current?.close(); backToArticleTop(); }}
                className="mt-2 flex min-h-11 w-full items-center gap-2 border-t border-[var(--line)] px-3 pt-2 text-sm font-semibold text-[var(--teal-dark)]"
              >
                <ArrowUp className="h-4 w-4" aria-hidden="true" />
                {backToTopLabel}
              </button>
            ) : null}
          </div>
        </dialog>
      ) : null}
    </>
  );
}

export function ArticleTocRail({
  headings,
  contentsLabel,
  backToTopLabel,
  progressLabel,
  seriesBackHref,
  seriesBackLabel,
  newsReading = false,
}: {
  headings: readonly ArticleTocHeading[];
  contentsLabel: string;
  backToTopLabel: string;
  progressLabel: string;
  seriesBackHref?: string | null;
  seriesBackLabel?: string | null;
  newsReading?: boolean;
}) {
  const [activeId, setActiveId] = useActiveHeading(headings);
  const progress = useScrollProgress(newsReading);

  return (
    <nav
      data-article-toc
      aria-label={contentsLabel}
      className="sticky top-24 hidden rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] lg:block"
    >
      {seriesBackHref && seriesBackLabel ? (
        <a
          href={seriesBackHref}
          className="mb-3 inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline underline-offset-4"
        >
          {seriesBackLabel}
        </a>
      ) : null}

      {headings.length > 0 ? (
        <>
          <div className="flex items-center justify-between gap-2">
            <h2 className="portal-section-heading text-sm font-extrabold uppercase tracking-wider text-[var(--teal-dark)]">
              {contentsLabel}
            </h2>
            <span className="font-mono text-[length:var(--text-xs)] tabular-nums text-[var(--muted)]">
              {progress}%
            </span>
          </div>

          <div
            role="progressbar"
            aria-label={progressLabel}
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={progress}
            className="mt-2.5 h-1.5 w-full overflow-hidden rounded-full bg-[var(--line)]"
          >
            <div
              className="h-full rounded-full bg-[var(--teal)] transition-[width] duration-150 motion-reduce:transition-none"
              style={{ width: `${progress}%` }}
            />
          </div>

          <ol className="mt-3.5 space-y-1 text-sm leading-6">
            {headings.map((heading, index) => {
              const isActive = heading.id === activeId;
              return (
                <li key={heading.id}>
                  <a
                    href={`#${heading.id}`}
                    aria-current={isActive ? "location" : undefined}
                    onClick={() => setActiveId(heading.id)}
                    className={`block rounded-lg px-2.5 py-1.5 transition-colors ${
                      isActive
                        ? "bg-[var(--teal-soft)] font-semibold text-[var(--teal-dark)]"
                        : "text-[var(--ink)] hover:bg-[var(--teal-soft)]/55 hover:text-[var(--teal-dark)]"
                    }`}
                  >
                    <span className="mr-1.5 font-mono text-[length:var(--text-xs)] font-semibold text-[var(--muted)]">
                      {index + 1}.
                    </span>
                    {heading.text}
                  </a>
                </li>
              );
            })}
          </ol>

          <div className="mt-3.5 border-t border-[var(--line)] pt-2">
            <button
              type="button"
              onClick={backToArticleTop}
              className="inline-flex min-h-11 items-center gap-1.5 text-[length:var(--text-xs)] font-semibold text-[var(--muted)] transition-colors hover:text-[var(--teal-dark)]"
            >
              <ArrowUp className="h-3.5 w-3.5" aria-hidden="true" />
              <span>{backToTopLabel}</span>
            </button>
          </div>
        </>
      ) : null}
    </nav>
  );
}
