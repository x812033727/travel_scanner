"use client";

import { ChevronDown } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useId, useRef, useState, type KeyboardEvent as ReactKeyboardEvent } from "react";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link, usePathname } from "@/i18n/navigation";
import { navItemLabelKey, type NavGroup } from "@/lib/nav-links";
import { featureVisible } from "@/lib/site-features";

const linkClass = "-mx-2 inline-flex min-h-11 items-center rounded-lg px-2 transition hover:text-[var(--ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]";

/** The items of a group the owner has not switched off, in the list's order. */
export function useVisibleItems(group: NavGroup) {
  const visibility = useSiteVisibility();
  return group.items.filter((item) => !item.feature || featureVisible(visibility, item.feature));
}

/**
 * One group of the desktop header: the group's label links to its hub, and the chevron beside
 * it opens the group's pages.
 *
 * The panel's links are always in the document and only CSS hides them, so a crawler reaches
 * every page the menu names, and pointing at the group opens it with no script at all. The
 * button opens it for touch and the keyboard; Escape and a click elsewhere close it. Escape
 * also holds the hover off until the pointer leaves, or a menu under a resting pointer would
 * refuse to close.
 */
export function NavMenu({ group }: { group: NavGroup }) {
  const t = useTranslations("navigation");
  const items = useVisibleItems(group);
  const pathname = usePathname();
  const [openPath, setOpenPath] = useState<string | null>(null);
  const [dismissed, setDismissed] = useState(false);
  const open = openPath === pathname;
  const root = useRef<HTMLDivElement>(null);
  const panelId = useId();
  const label = t(group.key);
  const current = (href: string) => pathname === href || pathname.startsWith(`${href}/`);

  useEffect(() => {
    if (!open) return;
    const close = (event: MouseEvent) => {
      if (!root.current?.contains(event.target as Node)) setOpenPath(null);
    };
    document.addEventListener("mousedown", close);
    return () => document.removeEventListener("mousedown", close);
  }, [open]);

  const onKeyDown = (event: ReactKeyboardEvent) => {
    if (event.key !== "Escape") return;
    setOpenPath(null);
    setDismissed(true);
  };

  if (!items.length) {
    return group.href ? <Link href={group.href} aria-current={current(group.href) ? "page" : undefined} className={linkClass}>{label}</Link> : null;
  }

  return (
    <div
      ref={root}
      className="group relative flex items-center"
      data-open={open || undefined}
      onKeyDown={onKeyDown}
      onMouseLeave={() => setDismissed(false)}
    >
      {group.href ? (
        <Link href={group.href} aria-current={current(group.href) ? "page" : undefined} className={linkClass}>{label}</Link>
      ) : (
        <span className="inline-flex min-h-11 items-center">{label}</span>
      )}
      <button
        type="button"
        aria-expanded={open}
        aria-controls={panelId}
        aria-label={t("groupMenu", { group: label })}
        onClick={() => { setDismissed(false); setOpenPath(open ? null : pathname); }}
        className="grid h-11 w-7 place-items-center rounded-lg hover:text-[var(--ink)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]"
      >
        <ChevronDown size={15} aria-hidden className="transition group-data-[open]:rotate-180" />
      </button>
      <div
        id={panelId}
        className={`invisible absolute left-0 top-full z-50 min-w-56 pt-1 opacity-0 transition group-data-[open]:visible group-data-[open]:opacity-100 ${dismissed ? "" : "group-hover:visible group-hover:opacity-100"}`}
      >
        <ul className="grid gap-0.5 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-2 shadow-xl">
          {items.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                aria-current={current(item.href) ? "page" : undefined}
                onClick={() => setOpenPath(null)}
                className="flex min-h-11 items-center rounded-xl px-3 text-[var(--ink)] hover:bg-[var(--teal-soft)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]"
              >
                {t(navItemLabelKey(group.key, item.key))}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}
