"use client";

import { useEffect, useState } from "react";
import { ArrowUp } from "lucide-react";

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

/**
 * Mobile/tablet reading progress bar pinned under the viewport top edge plus a floating
 * back-to-top button that clears the bottom tab bar once the reader is deep into an article.
 */
export function ArticleMobileProgress({ backToTopLabel }: { backToTopLabel: string }) {
  const progress = useScrollProgress();

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
        <button
          type="button"
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          style={{ bottom: "calc(5.25rem + env(safe-area-inset-bottom) + var(--ad-anchor-bottom, 0px))" }}
          className="fixed right-4 z-40 inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--teal)] bg-[var(--surface)] px-3.5 py-2 text-xs font-semibold text-[var(--teal-dark)] shadow-[var(--shadow-md)] transition-transform active:scale-95 lg:hidden"
        >
          <ArrowUp className="h-3.5 w-3.5" aria-hidden="true" />
          <span>{backToTopLabel}</span>
        </button>
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
  const [activeId, setActiveId] = useState<string>(headings[0]?.id ?? "");
  const progress = useScrollProgress();

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
            <h2 className="border-l-4 border-[var(--teal)] pl-3 text-sm font-extrabold uppercase tracking-wider text-[var(--teal-dark)]">
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
              className="inline-flex min-h-11 items-center gap-1.5 text-xs font-semibold text-[var(--muted)] transition-colors hover:text-[var(--teal-dark)]"
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
