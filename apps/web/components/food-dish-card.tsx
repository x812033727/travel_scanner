"use client";

import { CalendarCheck, ExternalLink, MapPin } from "lucide-react";
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
            // Reservation links are additive. An older cached response should
            // hide this action, not take down the whole food catalogue.
            const reservation = merchant.reservation_links?.[0];
            const mapHref = map ? safeExternalHref(map.url) : undefined;
            const reservationHref = reservation ? safeExternalHref(reservation.url) : undefined;
            return (
              <div key={merchant.merchant_id} className="rounded-2xl bg-[var(--paper)] p-3">
                <p className="font-semibold text-[var(--ink)]">
                  {merchant.name}
                  {merchant.local_name !== merchant.name && <span className="ml-1 text-xs font-normal text-[var(--muted)]">· {merchant.local_name}</span>}
                </p>
                <p className="mt-1 text-xs text-[var(--muted)]">{merchant.destination_name}</p>
                <div className="mt-2 flex flex-wrap gap-2">
                  {map && mapHref && (
                    <a href={mapHref} target="_blank" rel="noopener noreferrer" aria-label={t("navigateTo", { name: merchant.name, provider: map.label })} className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold text-[var(--teal)]">
                      <MapPin size={15} />{t("navigate")}<ExternalLink size={13} />
                    </a>
                  )}
                  {reservation && reservationHref && (
                    <a href={reservationHref} target="_blank" rel="noopener noreferrer" aria-label={t("reserveAt", { name: merchant.name, provider: reservation.label })} className="inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-3 text-sm font-semibold text-white">
                      <CalendarCheck size={15} />{t("viewOrReserve", { provider: reservation.label })}<ExternalLink size={13} />
                    </a>
                  )}
                </div>
                {reservation?.language_code === "vi" && reservationHref && <p className="mt-1 text-xs text-[var(--muted)]">{t("externalLanguage.vi")}</p>}
              </div>
            );
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
