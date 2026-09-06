"use client";

import { useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/navigation";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible, type SiteFeature } from "@/lib/site-features";

const entries: ReadonlyArray<{ key: "hotspots" | "foods"; href: string; feature?: SiteFeature }> = [
  { key: "hotspots", href: "/hotspots", feature: "hotspots" },
  { key: "foods", href: "/foods" },
];

/**
 * The two public browse surfaces share one "explore" entry in the bottom bar,
 * so each page shows the other as a sibling tab. Without this, foods is only
 * reachable from the home quick card on a phone. Like the navigation bars, a
 * failed settings fetch keeps both tabs; only an explicit switch hides one.
 */
export function ExploreSwitch() {
  const t = useTranslations("navigation");
  const pathname = usePathname();
  const visibility = useSiteVisibility();
  const visible = entries.filter((entry) => !entry.feature || featureVisible(visibility, entry.feature));
  if (visible.length < 2) return null;
  return (
    <nav aria-label={t("bottomExplore")} className="mx-auto max-w-6xl px-5 pt-4 md:px-8">
      <div className="inline-grid grid-cols-2 rounded-2xl border border-[var(--line)] bg-white p-1.5">
        {visible.map((entry) => {
          const active = pathname.startsWith(entry.href);
          return (
            <Link
              key={entry.href}
              href={entry.href}
              aria-current={active ? "page" : undefined}
              className={`flex min-h-11 items-center justify-center rounded-xl px-5 text-sm font-semibold transition ${active ? "bg-[var(--teal)] text-white" : "text-[var(--muted)]"}`}
            >
              {t(entry.key)}
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
