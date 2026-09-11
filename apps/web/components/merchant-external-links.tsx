"use client";

import { CalendarCheck, ExternalLink, Globe, MapPin } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import type { FoodMerchant, ReservationLink } from "@/lib/foods";
import { availableMapLinks } from "@/lib/map-identities";
import { safeExternalHref } from "@/lib/navigation";

type MerchantLinkDetails = Pick<FoodMerchant, "name" | "map_links" | "reservation_links">
  & Partial<Pick<FoodMerchant, "official_website_url">>;

// Defense in depth for public responses. Branch identity and review status remain
// the server's responsibility in foods/platform_links.py; this does not approve URLs.
const reservationHosts: Record<string, readonly string[]> = {
  tablecheck: ["tablecheck.com", "www.tablecheck.com"],
  catchtable_global: ["catchtable.net", "www.catchtable.net"],
  eztable: ["eztable.com", "www.eztable.com"],
  chope: ["chope.co", "www.chope.co"],
  openrice: ["openrice.com", "www.openrice.com"],
  hungry_hub: ["hungryhub.com", "www.hungryhub.com", "web.hungryhub.com"],
  pasgo: ["pasgo.vn", "www.pasgo.vn"],
};

function reviewedExternalHref(value: string | null | undefined) {
  const href = safeExternalHref(value, ["https:"]);
  if (!href || /[\u0000-\u0020\u007f\\]/.test(href)) return undefined;
  const url = new URL(href);
  const host = url.hostname.toLowerCase().replace(/\.$/, "");
  if (url.username || url.password || url.port
    || !host.includes(".") || host.includes(":") || /^\d+(\.\d+){3}$/.test(host)
    || /(^|\.)(localhost|local|internal)$/.test(host)) return undefined;
  return href;
}

function reviewedReservations(links: ReservationLink[] | undefined) {
  const seen = new Set<string>();
  return (links ?? []).filter((link) => {
    const href = reviewedExternalHref(link.url);
    if (!href || !link.label?.trim() || !link.verified_at
      || !Number.isFinite(Date.parse(link.verified_at))) return false;
    const url = new URL(href);
    if (!Object.hasOwn(reservationHosts, link.provider)
      || !reservationHosts[link.provider].includes(url.hostname)
      || !merchantSpecificReservationPath(link.provider, url.pathname)) return false;
    const key = `${link.provider}:${url.href}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

/** Mirror the existing server branch-page shapes; never accept search or platform landing pages. */
function merchantSpecificReservationPath(provider: string, pathname: string) {
  const segments = pathname.toLowerCase().split("/").filter(Boolean);
  const last = segments.at(-1);
  if (!last || ["search", "ranking", "rankings", "discovery", "explore", "restaurants", "list_of_restaurants"].includes(last)) return false;
  const after = (token: string) => segments.includes(token) && segments.indexOf(token) + 1 < segments.length;
  switch (provider) {
    case "tablecheck": return after("shops") && segments.includes("reserve");
    case "catchtable_global": return segments.length >= 2 && ["shop", "restaurant", "restaurants"].some((token) => segments.includes(token));
    case "eztable": return segments.length >= 2 && ["restaurant", "restaurants"].some((token) => segments.includes(token));
    case "chope": return after("restaurant");
    case "openrice": return segments.some((segment) => /^(p-|r-).*\d/.test(segment));
    case "hungry_hub": return after("restaurants");
    case "pasgo": return after("nha-hang");
    default: return false;
  }
}

function differentLanguageLabel(languageCode: string | undefined, locale: string) {
  if (!languageCode) return undefined;
  try {
    const language = new Intl.Locale(languageCode).maximize();
    const current = new Intl.Locale(locale).maximize();
    if (language.language === current.language && language.script === current.script) return undefined;
    return new Intl.DisplayNames([locale], { type: "language", fallback: "none" }).of(languageCode);
  } catch {
    // Invalid provider metadata must not crash a food card or become a guessed language.
    return undefined;
  }
}

export function MerchantExternalLinks({ merchant, compact = false }: {
  merchant: MerchantLinkDetails;
  compact?: boolean;
}) {
  const t = useTranslations("foods");
  const locale = useLocale();
  const maps = availableMapLinks(merchant.map_links).filter((map) => reviewedExternalHref(map.url));
  const reservations = reviewedReservations(merchant.reservation_links);
  const websiteHref = reviewedExternalHref(merchant.official_website_url);
  const linkClass = `flex min-h-11 min-w-0 items-center gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold text-[var(--ink)] underline-offset-4 hover:underline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--teal)] ${compact ? "bg-[var(--surface)]" : "bg-[var(--paper)]"}`;
  const newTabLabel = (label: string) => t("externalLinkLabel", { label });

  return (
    <div className="min-w-0">
      <div className="flex min-w-0 flex-col gap-2 sm:flex-row sm:flex-wrap">
        {maps.map((map) => (
          <a key={map.url} href={map.url} target="_blank" rel="noopener noreferrer"
            aria-label={newTabLabel(t("navigateTo", { name: merchant.name, provider: map.label }))}
            className={linkClass}>
            <MapPin size={15} className="shrink-0 text-[var(--teal)]" aria-hidden />
            <span className="min-w-0 flex-1 break-words">{map.label} · {t("navigate")}</span>
            <ExternalLink size={13} className="shrink-0" aria-hidden />
          </a>
        ))}
        {reservations.map((reservation) => {
          const language = differentLanguageLabel(reservation.language_code, locale);
          return (
            <div key={`${reservation.provider}:${reservation.url}`} className="min-w-0">
              <a href={reservation.url} target="_blank" rel="noopener noreferrer"
                aria-label={newTabLabel(t("reserveAt", { name: merchant.name, provider: reservation.label }))}
                className={linkClass}>
                <CalendarCheck size={15} className="shrink-0 text-[var(--teal)]" aria-hidden />
                <span className="min-w-0 flex-1 break-words">{t("viewReservationInfo", { provider: reservation.label })}</span>
                <ExternalLink size={13} className="shrink-0" aria-hidden />
              </a>
              {language && <p className="mt-1 px-1 text-xs text-[var(--muted)]">{t("reservationLanguage", { language })}</p>}
            </div>
          );
        })}
        {websiteHref && (
          <a href={websiteHref} target="_blank" rel="noopener noreferrer"
            aria-label={newTabLabel(t("officialWebsiteFor", { name: merchant.name }))}
            className={linkClass}>
            <Globe size={15} className="shrink-0 text-[var(--teal)]" aria-hidden />
            <span className="min-w-0 flex-1 break-words">{t("officialWebsite")}</span>
            <ExternalLink size={13} className="shrink-0" aria-hidden />
          </a>
        )}
      </div>
      {reservations.length === 0 && <p className="mt-2 text-xs text-[var(--muted)]">{t("noVerifiedReservation")}</p>}
    </div>
  );
}
