"use client";

import { ExternalLink } from "lucide-react";
import type { GuidePartnerLink } from "@/lib/guides";

export type PartnerLinkLabels = {
  /** The word that marks the link as paid, shown beside it, not only in the article's opening note. */
  badge: string;
  newTab: string;
};

/**
 * One partner link in an article body.
 *
 * A direct link, not the same-origin clickout travel offers use. The partner's own terms
 * (Hostinger's affiliate agreement) forbid hiding the traffic source behind a redirect, so
 * the browser goes straight to the partner and sends this site's origin as the referrer:
 * `noopener` without `noreferrer`, and the policy pinned on the element. `sponsored` tells
 * search engines what the link is.
 *
 * The click is counted by a separate keepalive POST that never holds up the navigation and
 * whose failure nobody sees. `fetch` rather than `sendBeacon`: a beacon is a no-cors request
 * whose Origin follows the page's referrer policy, and the BFF refuses a write without one.
 */
export function PartnerLink({
  link, label, note, clickPath, labels,
}: {
  link: GuidePartnerLink;
  label: string;
  note?: string;
  clickPath: string;
  labels: PartnerLinkLabels;
}) {
  const count = () => {
    try {
      fetch(clickPath, { method: "POST", keepalive: true, credentials: "same-origin", cache: "no-store" })
        .catch(() => { /* an uncounted click is invisible to the reader */ });
    } catch { /* counting never stands between a reader and the link */ }
  };
  return (
    <aside className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] px-4 py-3">
      <p className="text-xs font-semibold text-[var(--muted)]">
        <span className="rounded-full bg-[var(--line)] px-2 py-0.5 text-[var(--fg)]">{labels.badge}</span>
        <span className="ml-2">{link.display_name}</span>
      </p>
      <a
        href={link.url}
        target="_blank"
        rel="sponsored noopener"
        referrerPolicy="strict-origin-when-cross-origin"
        aria-label={`${label} · ${link.display_name} · ${labels.newTab}`}
        onClick={count}
        onAuxClick={(event) => { if (event.button === 1) count(); }}
        className="mt-3 inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--teal)] bg-[var(--surface-raised)] px-4 py-3 text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)]"
      >
        {label}
        <ExternalLink size={15} aria-hidden="true" />
      </a>
      {note ? <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{note}</p> : null}
    </aside>
  );
}
