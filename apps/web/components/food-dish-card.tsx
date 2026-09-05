"use client";

import { ExternalLink, MapPin } from "lucide-react";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { TravelCardActions } from "@/components/travel-card-actions";
import { primaryMapLink, type FoodItem } from "@/lib/foods";
import { safeExternalHref } from "@/lib/navigation";

export function FoodDishCard({ food }: { food: FoodItem }) {
  const t = useTranslations("foods");
  return (
    <article id={`food-${food.id}`} className="travel-result-card travel-result-card-food flex flex-col rounded-3xl border border-[var(--line)] bg-white p-5">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs font-bold uppercase tracking-[.14em] text-[var(--coral)]">{food.country_name}</p>
          <h3 className="mt-1 text-2xl font-bold">{food.name}</h3>
          <p className="mt-1 text-sm text-[var(--muted)]">{food.local_name}{food.romanized_name !== food.name && ` · ${food.romanized_name}`}</p>
        </div>
        <span className="rounded-full bg-[var(--teal-soft)] px-3 py-1 text-xs font-semibold text-[var(--teal-dark)]">{t(`kinds.${food.food_kind}`)}</span>
      </div>
      <p className="mt-4 leading-7 text-[var(--muted)]">{food.summary}</p>
      <div className="mt-4 flex flex-wrap gap-2">
        {food.meal_types.map((item) => <span key={item} className="rounded-full border border-[var(--line)] px-2.5 py-1 text-xs">{t(`meals.${item}`)}</span>)}
        {food.dietary_notes.map((item) => <span key={item} className="rounded-full bg-amber-50 px-2.5 py-1 text-xs text-amber-950">{item}</span>)}
      </div>
      <div className="mt-5 border-t border-[var(--line)] pt-4">
        <p className="text-xs font-semibold text-[var(--muted)]">{t("cities")}</p>
        <p className="mt-1 text-sm font-semibold">{food.destinations.map((item) => item.name).join("、")}</p>
      </div>
      <div className="mt-4">
        <p className="text-xs font-semibold text-[var(--muted)]">{t("recommendedMerchants")}</p>
        <div className="mt-2 grid gap-2">
          {food.recommended_merchants.slice(0, 3).map((merchant) => {
            const map = primaryMapLink(merchant.map_links);
            return map ? (
              <a key={merchant.merchant_id} href={safeExternalHref(map.url)} target="_blank" rel="noopener noreferrer" aria-label={`${map.label}: ${merchant.name}`} className="flex min-h-11 items-center gap-2 rounded-2xl bg-[var(--paper)] px-3 py-2 text-sm font-semibold text-[var(--teal)] underline-offset-4 hover:underline">
                <MapPin size={15} />
                <span className="mr-auto text-[var(--ink)]">{merchant.name}{merchant.local_name !== merchant.name && <span className="ml-1 text-xs font-normal text-[var(--muted)]">· {merchant.local_name}</span>}</span>
                <ExternalLink size={13} />
              </a>
            ) : null;
          })}
          {food.recommended_merchants.length === 0 && <p className="rounded-2xl bg-[var(--paper)] px-3 py-3 text-sm text-[var(--muted)]">{t("noVerifiedMerchant")}</p>}
        </div>
      </div>
      {food.food_hotspots.length > 0 && (
        <div className="mt-4">
          <p className="text-xs font-semibold text-[var(--muted)]">{t("foodAreas")}</p>
          <p className="mt-1 text-sm text-[var(--muted)]">{food.food_hotspots.slice(0, 3).map((area) => area.name).join("、")}</p>
        </div>
      )}
      <div className="mt-auto flex flex-wrap items-center gap-2 pt-5">
        {food.destinations[0] && <Link href={`/hotspots?category=food&destination_id=${encodeURIComponent(food.destinations[0].id)}`} className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white">{t("viewFoodAreas")}</Link>}
        {food.source_urls[0] && <a href={safeExternalHref(food.source_urls[0])} target="_blank" rel="noopener noreferrer" className="ml-auto inline-flex min-h-11 items-center gap-1 px-2 text-xs font-semibold text-[var(--muted)]">{t("source")}<ExternalLink size={13} /></a>}
      </div>
      <TravelCardActions type="food" id={food.id} title={food.name} selectionPath={`/foods/${food.id}/trip-selections`} merchantId={food.recommended_merchants[0]?.merchant_id} />
    </article>
  );
}
