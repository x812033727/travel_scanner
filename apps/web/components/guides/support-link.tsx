/**
 * The owner's tip page. `null` hides the line on every article; setting the address is the
 * whole launch (task `2026-09-24-reader-support-link-at-the-end`).
 *
 * A plain link and nothing else: no platform widget, no iframe, no tracking parameter, so it
 * brings no third-party script, cookie or CSP change with it.
 */
export const READER_SUPPORT_URL: string | null = null;

export type SupportLinkLabels = {
  /** One sentence before the link. It must not ask readers to click ads or partner links. */
  text: string;
  action: string;
  newTab: string;
};

export function SupportLink({ labels, url = READER_SUPPORT_URL }: { labels: SupportLinkLabels; url?: string | null }) {
  if (!url) return null;
  return (
    <p className="border-t border-[var(--line)] pt-6 text-sm leading-6 text-[var(--muted)]">
      {labels.text}{" "}
      <a
        className="text-[var(--teal)] underline"
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        aria-label={`${labels.action} · ${labels.newTab}`}
      >
        {labels.action}
      </a>
    </p>
  );
}
