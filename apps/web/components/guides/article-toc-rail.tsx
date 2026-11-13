"use client";

import { useEffect, useState } from "react";
import { ArrowUp, List, X } from "lucide-react";

export type ArticleTocHeading = {
  id: string;
  text: string;
};

function useScrollProgress(): number {
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    function updateProgress() {
      const doc = document.documentElement;
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
    return () => window.removeEventListener("scroll", updateProgress);
  }, []);

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
}: {
  backToTopLabel: string;
  headings?: readonly ArticleTocHeading[];
  contentsLabel?: string;
  closeLabel?: string;
}) {
  const progress = useScrollProgress();
  const [activeId, setActiveId] = useActiveHeading(headings);
  const [sheetOpen, setSheetOpen] = useState(false);

  useEffect(() => {
    if (!sheetOpen) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setSheetOpen(false);
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
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
          className="h-full bg-[linear-gradient(90deg,var(--teal)_0%,var(--coral-bright)_100%)] transition-[width] duration-150"
          style={{ width: `${progress}%` }}
        />
      </div>
      {progress >= 28 ? (
        <div
          style={{ bottom: "calc(5.25rem + env(safe-area-inset-bottom) + var(--ad-anchor-bottom, 0px))" }}
          className="fixed right-4 z-40 flex items-center gap-2 lg:hidden"
        >
          {showTocTrigger ? (
            <button
              type="button"
              aria-expanded={sheetOpen}
              onClick={() => setSheetOpen((open) => !open)}
              className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--surface)]/95 px-3.5 py-2 text-[length:var(--text-xs)] font-semibold text-[var(--ink)] shadow-[var(--shadow-md)] backdrop-blur-md transition-transform active:scale-95"
            >
              <List className="h-3.5 w-3.5 text-[var(--teal)]" aria-hidden="true" />
              <span>{contentsLabel}</span>
            </button>
          ) : null}
          <button
            type="button"
            onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
            className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--teal)] bg-[var(--surface)]/95 px-3.5 py-2 text-[length:var(--text-xs)] font-semibold text-[var(--teal-dark)] shadow-[var(--shadow-md)] backdrop-blur-md transition-transform active:scale-95"
          >
            <ArrowUp className="h-3.5 w-3.5" aria-hidden="true" />
            <span>{backToTopLabel}</span>
          </button>
        </div>
      ) : null}

      {sheetOpen && showTocTrigger ? (
        <div
          role="dialog"
          aria-modal="true"
          aria-label={contentsLabel}
          onClick={(event) => {
            if (event.target === event.currentTarget) setSheetOpen(false);
          }}
          className="fixed inset-0 z-50 flex items-end bg-black/45 p-3 backdrop-blur-[2px] lg:hidden"
        >
          <div
            style={{ marginBottom: "env(safe-area-inset-bottom)" }}
            className="max-h-[72dvh] w-full overflow-y-auto rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-4 shadow-[var(--shadow-lg)] sm:p-5"
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
                onClick={() => setSheetOpen(false)}
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
                      onClick={() => {
                        setActiveId(heading.id);
                        setSheetOpen(false);
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
          </div>
        </div>
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
}: {
  headings: readonly ArticleTocHeading[];
  contentsLabel: string;
  backToTopLabel: string;
  progressLabel: string;
  seriesBackHref?: string | null;
  seriesBackLabel?: string | null;
}) {
  const [activeId, setActiveId] = useActiveHeading(headings);
  const progress = useScrollProgress();

  return (
    <nav
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
              className="h-full rounded-full bg-[var(--teal)] transition-[width] duration-150"
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
              onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
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
