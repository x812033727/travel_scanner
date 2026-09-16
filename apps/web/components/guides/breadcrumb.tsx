import { Link } from "@/i18n/navigation";
import type { Crumb } from "@/lib/structured-data";

/**
 * Where the reader is: section › topic › (sub-topic) › (series) › this page. The same trail
 * the page hands to `breadcrumbs()` for its `BreadcrumbList`, so what the graph claims is
 * what the reader sees. The home crumb is left out of the visible row (the header logo is
 * that link) and the current page is text, not a link to itself.
 */
export function Breadcrumb({ trail, current, label }: { trail: readonly Crumb[]; current: string; label: string }) {
  const crumbs = trail.filter((crumb) => crumb.path !== "/");
  return (
    <nav aria-label={label} className="mb-6 text-[length:var(--text-meta)] text-[var(--muted)]">
      <ol className="flex flex-wrap items-center gap-1">
        {crumbs.map((crumb) => (
          <li key={crumb.path} className="flex items-center gap-1">
            <Link className="inline-flex min-h-11 items-center underline underline-offset-4" href={crumb.path}>{crumb.name}</Link>
            <span aria-hidden>›</span>
          </li>
        ))}
        <li aria-current="page" className="inline-flex min-h-11 items-center">{current}</li>
      </ol>
    </nav>
  );
}
