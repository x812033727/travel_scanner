"use client";

import { useEffect, useRef, useState, useSyncExternalStore } from "react";
import { Check, Link2, Share2 } from "lucide-react";

export type ArticleShareLabels = {
  shareLabel: string;
  copyLink: string;
  linkCopied: string;
  shareLine: string;
  shareSystem: string;
};

const noopSubscribe = () => () => {};
const getCanShareSnapshot = () => typeof navigator !== "undefined" && typeof navigator.share === "function";
const getServerCanShareSnapshot = () => false;

/**
 * Zero-external-script share toolbar for editorial articles.
 *
 * Uses no third-party SDKs so CSP stays locked down and zero network requests fire on render;
 * LINE sharing opens as a plain outbound anchor only when clicked.
 */
export function ArticleShareBar({
  url,
  title,
  labels,
}: {
  url: string;
  title: string;
  labels: ArticleShareLabels;
}) {
  const [copied, setCopied] = useState(false);
  const canShare = useSyncExternalStore(noopSubscribe, getCanShareSnapshot, getServerCanShareSnapshot);
  const timerRef = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (timerRef.current) clearTimeout(timerRef.current);
    };
  }, []);

  async function handleCopy() {
    try {
      await navigator.clipboard?.writeText(url);
      setCopied(true);
      if (timerRef.current) clearTimeout(timerRef.current);
      timerRef.current = setTimeout(() => setCopied(false), 2_000);
    } catch {
      // Clipboard API unavailable or denied; fail silently.
    }
  }

  async function handleWebShare() {
    try {
      await navigator.share({ title, url });
    } catch {
      // User dismissed native share sheet.
    }
  }

  const lineShareHref = `https://social-plugins.line.me/lineit/share?url=${encodeURIComponent(url)}`;

  return (
    <div
      role="group"
      aria-label={labels.shareLabel}
      className="mt-3.5 flex flex-wrap items-center gap-2"
    >
      <button
        type="button"
        onClick={handleCopy}
        aria-live="polite"
        className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/80 px-4 py-1.5 text-xs font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]/60 hover:text-[var(--teal-dark)]"
      >
        {copied ? (
          <Check className="h-3.5 w-3.5 text-[var(--teal)]" aria-hidden="true" />
        ) : (
          <Link2 className="h-3.5 w-3.5 text-[var(--muted)]" aria-hidden="true" />
        )}
        <span>{copied ? labels.linkCopied : labels.copyLink}</span>
      </button>

      <a
        href={lineShareHref}
        target="_blank"
        rel="noopener noreferrer"
        className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/80 px-4 py-1.5 text-xs font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]/60 hover:text-[var(--teal-dark)]"
      >
        <span>{labels.shareLine}</span>
      </a>

      {canShare ? (
        <button
          type="button"
          onClick={handleWebShare}
          className="inline-flex min-h-11 items-center gap-1.5 rounded-full border border-[var(--line)] bg-[var(--paper)]/80 px-4 py-1.5 text-xs font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]/60 hover:text-[var(--teal-dark)]"
        >
          <Share2 className="h-3.5 w-3.5 text-[var(--muted)]" aria-hidden="true" />
          <span>{labels.shareSystem}</span>
        </button>
      ) : null}
    </div>
  );
}
