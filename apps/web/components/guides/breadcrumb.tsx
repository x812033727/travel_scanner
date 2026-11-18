import { Link } from "@/i18n/navigation";
import type { Crumb } from "@/lib/structured-data";

/**
 * Where the reader is: section › topic › (sub-topic) › (series) › this page. The same trail
 * the page hands to `breadcrumbs()` for its `BreadcrumbList`, so what the graph claims is
 * what the reader sees. The home crumb is left out of the visible row (the header logo is
 * that link) and the current page is text, not a link to itself.
 */
export function Breadcrumb({ trail, current, label, compact = false }: { trail: readonly Crumb[]; current: string; label: string; compact?: boolean }) {
  const crumbs = trail.filter((crumb) => crumb.path !== "/");
  return (
    <nav aria-label={label} className={`text-[length:var(--text-meta)] text-[var(--muted)] ${compact ? "mb-2" : "mb-4 sm:mb-6"}`}>
      <ol className="flex flex-wrap items-center gap-x-1.5 gap-y-0.5">
        {crumbs.map((crumb, index) => (
          <li key={crumb.path} className="flex items-center gap-1.5">
            <Link className="inline-flex min-h-11 items-center underline decoration-[var(--line)] underline-offset-4 transition-colors hover:text-[var(--teal)] hover:decoration-[var(--teal)]" href={crumb.path}>{crumb.name}</Link>
            {(!compact || index < crumbs.length - 1) && <span aria-hidden>›</span>}
          </li>
        ))}
        <li aria-current="page" className={compact ? "sr-only" : "line-clamp-1 py-1.5 font-medium text-[var(--ink)] sm:line-clamp-none"}>{current}</li>
      </ol>
    </nav>
  );
}
