"use client";

import { Award, ExternalLink, Globe, MapPin } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { TravelCardActions } from "@/components/travel-card-actions";
import { primaryMapLink, type FoodMerchant } from "@/lib/foods";
import { safeExternalHref } from "@/lib/navigation";

const distinctions = new Set([
  "three_star",
  "two_star",
  "one_star",
  "green_star",
  "bib_gourmand",
  "selected",
]);
const sourceTypes = new Set(["official_tourism", "merchant_official", "michelin_licensed"]);

export function FoodMerchantCard({
  merchant,
  onSelectArea,
  onSelectCategory,
}: {
  merchant: FoodMerchant;
  onSelectArea?: (slug: string) => void;
  onSelectCategory?: (slug: string) => void;
}) {
  const t = useTranslations("foods");
  const locale = useLocale();
  const map = primaryMapLink(merchant.map_links);
  const mapHref = map ? safeExternalHref(map.url) : undefined;
  const websiteHref = safeExternalHref(merchant.official_website_url);
  const primaryCategory = merchant.categories.find((item) => item.is_primary) ?? merchant.categories[0];
  const distinction = merchant.sources
    .map((source) => source.distinction)
    .find((value): value is string => Boolean(value && distinctions.has(value)));
  const verifiedOn = merchant.verified_at
    ? new Intl.DateTimeFormat(locale, { dateStyle: "medium" }).format(new Date(merchant.verified_at))
    : null;

  return (
    <article id={`merchant-${merchant.id}`} className="travel-result-card travel-result-card-food flex flex-col rounded-3xl border border-[var(--line)] bg-white p-5">
      <div className="flex items-start justify-between gap-4">
        <div className="min-w-0">
          <h3 className="text-2xl font-bold">{merchant.name}</h3>
          {merchant.local_name !== merchant.name && (
            <p className="mt-1 text-sm text-[var(--muted)]">{merchant.local_name}</p>
          )}
        </div>
        {primaryCategory && (
          <span className="shrink-0 rounded-full bg-[var(--teal-soft)] px-3 py-1 text-xs font-semibold text-[var(--teal-dark)]">
            {primaryCategory.name}
          </span>
        )}
      </div>
      <p className="mt-3 flex flex-wrap items-center gap-2 text-sm text-[var(--muted)]">
        <MapPin size={15} className="text-[var(--teal)]" />
        <span>{merchant.destination_name}</span>
        {merchant.area && (
          <button
            type="button"
            onClick={() => onSelectArea?.(merchant.area?.slug ?? "")}
            className="rounded-full border border-[var(--line)] px-2.5 py-1 text-xs font-semibold text-[var(--ink)]"
          >
            {merchant.area.name}
          </button>
        )}
        {distinction && (
          <span className="inline-flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1 text-xs font-semibold text-amber-950">
            <Award size={13} />
            {t(`distinctions.${distinction}`)}
          </span>
        )}
      </p>
      {merchant.categories.length > 0 && (
        <div className="mt-3 flex flex-wrap gap-2">
          {merchant.categories.map((category) => (
            <button
              key={category.slug}
              type="button"
              onClick={() => onSelectCategory?.(category.slug)}
              className="rounded-full bg-[var(--paper)] px-2.5 py-1 text-xs font-semibold"
            >
              {category.name}
            </button>
          ))}
        </div>
      )}
      {merchant.signature_dishes.length > 0 && (
        <div className="mt-4">
          <p className="text-xs font-semibold text-[var(--muted)]">{t("signatureDishes")}</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {merchant.signature_dishes.map((dish) => (
              <span key={dish.food_id} className="rounded-full border border-[var(--line)] px-2.5 py-1 text-xs">
                {dish.name}
                {dish.local_name !== dish.name && (
                  <span className="ml-1 text-[var(--muted)]">· {dish.local_name}</span>
                )}
              </span>
            ))}
          </div>
        </div>
      )}
      {merchant.address && (
        <p className="mt-4 text-sm text-[var(--muted)]">
          <span className="font-semibold text-[var(--ink)]">{t("address")}</span> {merchant.address}
        </p>
      )}
      <div className="mt-4 grid gap-2">
        {map && mapHref && (
          <a
            href={mapHref}
            target="_blank"
            rel="noopener noreferrer"
            aria-label={`${map.label}: ${merchant.name}`}
            className="flex min-h-11 items-center gap-2 rounded-2xl bg-[var(--paper)] px-3 py-2 text-sm font-semibold text-[var(--teal)] underline-offset-4 hover:underline"
          >
            <MapPin size={15} />
            <span className="mr-auto">{map.label}</span>
            <ExternalLink size={13} />
          </a>
        )}
        {websiteHref && (
          <a
            href={websiteHref}
            target="_blank"
            rel="noopener noreferrer"
            className="flex min-h-11 items-center gap-2 rounded-2xl border border-[var(--line)] px-3 py-2 text-sm font-semibold"
          >
            <Globe size={15} />
            <span className="mr-auto">{t("officialWebsite")}</span>
            <ExternalLink size={13} />
          </a>
        )}
      </div>
      {merchant.sources.length > 0 && (
        <details className="mt-4 rounded-2xl bg-[var(--paper)] px-3 py-2 text-xs text-[var(--muted)]">
          <summary className="cursor-pointer font-semibold">
            {t("sourcesSummary", { count: merchant.sources.length })}
          </summary>
          <ul className="mt-2 grid gap-1">
            {merchant.sources.map((source) => {
              const href = safeExternalHref(source.url);
              const typeLabel = sourceTypes.has(source.source_type)
                ? t(`sourceTypes.${source.source_type}`)
                : source.source_type;
              return (
                <li key={`${source.source_type}:${source.url}`}>
                  <span className="font-semibold text-[var(--ink)]">{typeLabel}</span>{" "}
                  {href ? (
                    <a href={href} target="_blank" rel="noopener noreferrer" className="underline underline-offset-4">
                      {source.title}
                    </a>
                  ) : (
                    source.title
                  )}
                </li>
              );
            })}
          </ul>
          {verifiedOn && <p className="mt-2">{t("verifiedOn", { date: verifiedOn })}</p>}
        </details>
      )}
      <TravelCardActions
        type="merchant"
        id={merchant.id}
        title={merchant.name}
        selectionPath={`/foods/merchants/${merchant.id}/trip-selections`}
        merchantId={merchant.id}
      />
    </article>
  );
}
