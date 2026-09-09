"use client";

import { Hotel } from "lucide-react";
import { useTranslations } from "next-intl";
import { interestCodes, shopThemeCodes } from "@/lib/destinations";

export type NewTripLodgingMode = "hotel" | "vacation_rental" | "both" | "any";
export type NewTripTravelerValues = { adults: string; children: string; rooms: string };
export type NewTripPreferenceValues = {
  budget_twd: string; pace: "relaxed" | "balanced" | "packed"; route_preference: string;
  nightly_min: string; nightly_max: string; hotel_min_rating: string; preferred_area: string;
  max_station_walk_minutes: string; min_review_score: string; min_review_count: string;
  breakfast_required: boolean; refundable_required: boolean; avoid_red_eye: boolean;
};
export const newTripFieldClass = "mt-2 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 font-normal outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";
const fieldClass = newTripFieldClass;
const reviewScores = [7, 8, 9];
// Existing trips can contain valid values between the quick-pick options. Keep them visible.
function numericOptions(options: number[], current: string) {
  const values = options.map(String);
  if (current.trim() && Number.isFinite(Number(current)) && !values.includes(current)) values.push(current);
  return values.sort((a, b) => Number(a) - Number(b));
}
function optionClass(active: boolean) {
  return `rounded-xl border px-3 py-3 text-left text-sm transition ${active ? "border-[var(--teal)] bg-[var(--teal-soft)] font-semibold text-[var(--teal-dark)]" : "border-[var(--line)] bg-[var(--surface)] hover:border-[var(--teal)]"}`;
}
export function newTripOptionalNumber(value: string) {
  const parsed = Number(value);
  return value && Number.isFinite(parsed) ? Math.round(parsed) : null;
}
export function validNewTripTravelers(values: NewTripTravelerValues) {
  return [[values.adults, 1, 9], [values.children, 0, 5], [values.rooms, 1, 4]].every(([value, min, max]) =>
    String(value).trim() !== "" && Number.isInteger(Number(value)) && Number(value) >= Number(min) && Number(value) <= Number(max));
}
export function newTripPreferenceError(values: NewTripPreferenceValues): "budgetPositive" | "nightlyInverted" | "invalidNumbers" | undefined {
  if (values.budget_twd && (!Number.isFinite(Number(values.budget_twd)) || Number(values.budget_twd) <= 0)) return "budgetPositive";
  if ([["nightly_min", 0], ["nightly_max", 1], ["hotel_min_rating", 0], ["max_station_walk_minutes", 0], ["min_review_score", 0], ["min_review_count", 0]].some(([key, min]) => {
    const value = values[key as keyof NewTripPreferenceValues];
    return value !== "" && (!Number.isFinite(Number(value)) || Number(value) < Number(min));
  })) return "invalidNumbers";
  const min = newTripOptionalNumber(values.nightly_min);
  const max = newTripOptionalNumber(values.nightly_max);
  if (min != null && max != null && min > max) return "nightlyInverted";
}
export function newTripPreferencesPayload(values: NewTripPreferenceValues, lodgingMode: NewTripLodgingMode, interests: string[], shopThemes: string[]) {
  return {
    budget_twd: newTripOptionalNumber(values.budget_twd), avoid_red_eye: values.avoid_red_eye,
    hotel_min_rating: newTripOptionalNumber(values.hotel_min_rating),
    hotel_min_nightly_twd: newTripOptionalNumber(values.nightly_min), hotel_max_nightly_twd: newTripOptionalNumber(values.nightly_max),
    accepted_property_types: lodgingMode === "hotel" ? ["hotel"] : lodgingMode === "vacation_rental" ? ["vacation_rental"] : lodgingMode === "both" ? ["hotel", "vacation_rental"] : [],
    hotel_min_review_score: newTripOptionalNumber(values.min_review_score), hotel_min_review_count: newTripOptionalNumber(values.min_review_count),
    breakfast_required: values.breakfast_required, refundable_required: values.refundable_required,
    max_station_walk_minutes: newTripOptionalNumber(values.max_station_walk_minutes), preferred_area: values.preferred_area.trim() || null,
    pace: values.pace, interests, shop_themes: interests.includes("shopping") ? shopThemes : [],
  };
}
export function NewTripTravelerFields({ values: form, onChange: update }: {
  values: NewTripTravelerValues;
  onChange: (key: keyof NewTripTravelerValues, value: string) => void;
}) {
  const t = useTranslations("newTrip");
  return (<div className="grid grid-cols-3 gap-3"><label className="text-sm font-semibold">{t("travelers.adults")}<select aria-label={t("travelers.adults")} value={form.adults} onChange={(event) => update("adults", event.target.value)} className={fieldClass}>{numericOptions([1,2,3,4,5,6,7,8,9], form.adults).map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">{t("travelers.children")}<select aria-label={t("travelers.children")} value={form.children} onChange={(event) => update("children", event.target.value)} className={fieldClass}>{numericOptions([0,1,2,3,4,5], form.children).map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">{t("travelers.rooms")}<select aria-label={t("travelers.rooms")} value={form.rooms} onChange={(event) => update("rooms", event.target.value)} className={fieldClass}>{numericOptions([1,2,3,4], form.rooms).map((value) => <option key={value}>{value}</option>)}</select></label></div>);
}
export function NewTripPreferenceFields({
  values: form, onChange: update, lodgingMode, onLodgingModeChange: chooseLodgingMode,
  interests: selectedInterests, onToggleInterest: toggleInterest,
  shopThemes: selectedShopThemes, onToggleShopTheme: toggleShopTheme, hideRoutePreference = false,
}: {
  hideRoutePreference?: boolean;
  values: NewTripPreferenceValues;
  onChange: <K extends keyof NewTripPreferenceValues>(key: K, value: NewTripPreferenceValues[K]) => void;
  lodgingMode: NewTripLodgingMode;
  onLodgingModeChange: (value: NewTripLodgingMode) => void;
  interests: string[]; onToggleInterest: (code: string) => void;
  shopThemes: string[]; onToggleShopTheme: (code: string) => void;
}) {
  const t = useTranslations("newTrip");
  return <div className="premium-new-trip-preferences grid gap-5">
        <label className="text-sm font-semibold">{t("travelers.budget")}<input type="number" inputMode="numeric" min="1" value={form.budget_twd} onChange={(event) => update("budget_twd", event.target.value)} placeholder={t("travelers.budgetPlaceholder")} className={fieldClass} /></label>
        <div><p className="text-sm font-semibold">{t("travelers.pace")}</p><div className="mt-2 grid grid-cols-3 gap-2">{([["relaxed", t("travelers.paceRelaxed")], ["balanced", t("travelers.paceBalanced")], ["packed", t("travelers.pacePacked")]] as const).map(([value, label]) => <button key={value} type="button" aria-pressed={form.pace === value} onClick={() => update("pace", value)} className={optionClass(form.pace === value)}>{label}</button>)}</div></div>
        <div><p className="text-sm font-semibold">{t("travelers.interests")}</p><div className="mt-2 flex flex-wrap gap-2">{interestCodes.map((code) => <button key={code} type="button" aria-pressed={selectedInterests.includes(code)} onClick={() => toggleInterest(code)} className={optionClass(selectedInterests.includes(code))}>{t(`interests.${code}`)}</button>)}</div>{selectedInterests.includes("shopping") && <div className="mt-3" role="group" aria-label={t("travelers.shopThemes")}><p className="text-xs font-semibold text-[var(--muted)]">{t("travelers.shopThemes")}</p><div className="mt-2 flex flex-wrap gap-2">{shopThemeCodes.map((code) => <button key={code} type="button" aria-pressed={selectedShopThemes.includes(code)} onClick={() => toggleShopTheme(code)} className={optionClass(selectedShopThemes.includes(code))}>{t(`shopThemes.${code}`)}</button>)}</div></div>}</div>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Hotel size={19} />{t("stay.title")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("stay.help")}</p></div>
        <div className="grid grid-cols-2 gap-2">{([["hotel", t("stay.hotelOnly")], ["vacation_rental", t("stay.vacationRental")], ["both", t("stay.both")], ["any", t("stay.any")]] as const).map(([value, label]) => <button key={value} type="button" aria-pressed={lodgingMode === value} onClick={() => chooseLodgingMode(value)} className={optionClass(lodgingMode === value)}>{label}</button>)}</div>
        <div className="grid grid-cols-2 gap-3"><label className="text-sm font-semibold">{t("stay.nightlyMin")}<input aria-label={t("stay.nightlyMin")} type="number" inputMode="numeric" min="0" value={form.nightly_min} onChange={(event) => update("nightly_min", event.target.value)} placeholder={t("stay.noPreference")} className={fieldClass} /></label><label className="text-sm font-semibold">{t("stay.nightlyMax")}<input aria-label={t("stay.nightlyMax")} type="number" inputMode="numeric" min="1" value={form.nightly_max} onChange={(event) => update("nightly_max", event.target.value)} placeholder={t("stay.noPreference")} className={fieldClass} /></label><label className="text-sm font-semibold">{t("stay.minRating")}<select aria-label={t("stay.minRating")} value={form.hotel_min_rating} onChange={(event) => update("hotel_min_rating", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option>{numericOptions([3,4,5], form.hotel_min_rating).map((value) => <option key={value} value={value}>{t("stay.starsPlus", { stars: value })}</option>)}</select></label><label className="text-sm font-semibold">{t("stay.stationWalk")}<select aria-label={t("stay.stationWalk")} value={form.max_station_walk_minutes} onChange={(event) => update("max_station_walk_minutes", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option>{numericOptions([5,10,15,20], form.max_station_walk_minutes).map((value) => <option key={value} value={value}>{t("stay.minutes", { minutes: value })}</option>)}</select></label><label className="text-sm font-semibold">{t("stay.minReviewScore")}<select aria-label={t("stay.minReviewScore")} value={form.min_review_score} onChange={(event) => update("min_review_score", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option>{numericOptions(reviewScores, form.min_review_score).map((score) => <option key={score} value={score}>{t("stay.scorePlus", { score: Number.isInteger(Number(score)) ? Number(score).toFixed(1) : score })}</option>)}</select></label><label className="text-sm font-semibold">{t("stay.minReviewCount")}<select aria-label={t("stay.minReviewCount")} value={form.min_review_count} onChange={(event) => update("min_review_count", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option>{numericOptions([20,50,100,300], form.min_review_count).map((value) => <option key={value} value={value}>{t("stay.reviewsPlus", { count: value })}</option>)}</select></label></div>
        <label className="text-sm font-semibold">{t("stay.preferredArea")}<input maxLength={120} value={form.preferred_area} onChange={(event) => update("preferred_area", event.target.value)} placeholder={t("stay.preferredAreaPlaceholder")} className={fieldClass} /></label>
        <div className="grid gap-2 text-sm sm:grid-cols-2"><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.breakfast_required} onChange={(event) => update("breakfast_required", event.target.checked)} />{t("stay.breakfast")}</label><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.refundable_required} onChange={(event) => update("refundable_required", event.target.checked)} />{t("stay.refundable")}</label></div>
        <div className="grid gap-3 sm:grid-cols-2">{!hideRoutePreference && <label className="text-sm font-semibold">{t("review.routePreference")}<select value={form.route_preference} onChange={(event) => update("route_preference", event.target.value)} className={fieldClass}><option value="FEWER_TRANSFERS">{t("review.fewerTransfers")}</option><option value="FASTEST">{t("review.fastest")}</option><option value="LESS_WALKING">{t("review.lessWalking")}</option></select></label>}<label className="flex items-center gap-2 self-end rounded-xl bg-[var(--paper)] p-3 text-sm"><input type="checkbox" checked={form.avoid_red_eye} onChange={(event) => update("avoid_red_eye", event.target.checked)} />{t("review.avoidRedEye")}</label></div>

  </div>;
}
