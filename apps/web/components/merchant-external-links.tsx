"use client";

import { CalendarCheck, ExternalLink, Globe, MapPin } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import type { FoodMerchant, ReservationLink } from "@/lib/foods";
import { availableMapLinks } from "@/lib/map-identities";
import { safeExternalHref } from "@/lib/navigation";
import { reservationPlatformDefinitions, reservationPlatformHref } from "@/lib/reservation-platforms";

type MerchantLinkDetails = Pick<FoodMerchant, "name" | "map_links" | "reservation_links">
  & Partial<Pick<FoodMerchant, "official_website_url">>;

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
  // One reviewed branch per provider. Provider order is explicit in the shared
  // registry; neither incoming array order nor commission can promote an option.
  const reviewed = new Map<string, ReservationLink>();
  for (const link of links ?? []) {
    if (!link || typeof link.label !== "string" || !link.label.trim()
      || typeof link.verified_at !== "string" || !Number.isFinite(Date.parse(link.verified_at))) continue;
    const href = reservationPlatformHref(link.provider, link.url);
    if (href && !reviewed.has(link.provider)) reviewed.set(link.provider, { ...link, url: href });
  }
  return reservationPlatformDefinitions.flatMap((definition) => {
    const link = reviewed.get(definition.provider);
    return link ? [{ ...link, label: definition.label }] : [];
  });
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
