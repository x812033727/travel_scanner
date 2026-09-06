"use client";

import { PencilLine, RotateCcw, X } from "lucide-react";
import { type FormEvent, useState } from "react";
import { useTranslations } from "next-intl";
import { interestCodes, type DestinationCity } from "@/lib/destinations";

export type EditableSearchCriteria = {
  origin?: string;
  departure_date?: string;
  return_date?: string;
  flex_days?: 0 | 3 | 7;
  travelers: { adults: number; children?: number; rooms?: number };
  budget_twd?: number;
  interests: string[];
  avoid_red_eye: boolean;
  hotel_max_nightly_twd?: number;
  hotel_min_nightly_twd?: number;
  hotel_min_rating?: number;
  accepted_property_types?: string[];
  hotel_min_review_score?: number;
  hotel_min_review_count?: number;
  breakfast_required?: boolean;
  refundable_required?: boolean;
  include_airbnb?: boolean;
  preferred_area?: string;
  pace?: "relaxed" | "balanced" | "packed";
};

export type CriteriaUpdate = {
  origin: string;
  departureDate: string;
  returnDate: string;
  flexDays: 0 | 3 | 7;
  adults: number;
  children: number;
  rooms: number;
  budget?: number;
  nightlyBudget?: number;
  nightlyMinimum?: number;
  hotelMinRating?: number;
  propertyTypes: string[];
  minReviewScore?: number;
  minReviewCount?: number;
  preferredArea?: string;
  pace: "relaxed" | "balanced" | "packed";
  interests: string[];
  avoidRedEye: boolean;
  breakfastRequired: boolean;
  refundableRequired: boolean;
  includeAirbnb: boolean;
};

const fieldClass = "mt-1.5 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

export function SearchCriteriaEditor({
  criteria,
  destination,
  dates,
  disabled,
  onApply,
}: {
  criteria: EditableSearchCriteria;
  destination?: DestinationCity;
  dates: string[];
  disabled?: boolean;
  onApply: (update: CriteriaUpdate) => void;
}) {
  const tc = useTranslations("search.catalog");
  const tcr = useTranslations("search.criteria");
  const [open, setOpen] = useState(false);
  const [selectedInterests, setSelectedInterests] = useState(criteria.interests);
  const [validationError, setValidationError] = useState<string>();

  function toggleInterest(code: string) {
    setSelectedInterests((current) => current.includes(code)
      ? current.filter((interest) => interest !== code)
      : [...current, code]);
  }

  function toggleEditor() {
    if (!open) {
      setSelectedInterests(criteria.interests);
      setValidationError(undefined);
    }
    setOpen((current) => !current);
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const departureDate = String(form.get("departure_date") || "");
    const returnDate = String(form.get("return_date") || "");
    if (!departureDate || !returnDate || returnDate <= departureDate) {
      setValidationError(tcr("returnAfterDeparture"));
      return;
    }
    const numberOrUndefined = (name: string) => {
      const value = Number(form.get(name) || 0);
      return value > 0 ? value : undefined;
    };
    onApply({
      origin: String(form.get("origin") || "TPE"),
      departureDate,
      returnDate,
      flexDays: Number(form.get("flex_days") || 0) as CriteriaUpdate["flexDays"],
      adults: Number(form.get("adults") || 1),
      children: Number(form.get("children") || 0),
      rooms: Number(form.get("rooms") || 1),
      budget: numberOrUndefined("budget_twd"),
      nightlyBudget: numberOrUndefined("hotel_max_nightly_twd"),
      nightlyMinimum: numberOrUndefined("hotel_min_nightly_twd"),
      hotelMinRating: numberOrUndefined("hotel_min_rating"),
      propertyTypes: String(form.get("accepted_property_types") || "").split(",").filter(Boolean),
      minReviewScore: numberOrUndefined("hotel_min_review_score"),
      minReviewCount: numberOrUndefined("hotel_min_review_count"),
      preferredArea: String(form.get("preferred_area") || "") || undefined,
      pace: String(form.get("pace") || "balanced") as CriteriaUpdate["pace"],
      interests: selectedInterests,
      avoidRedEye: form.get("avoid_red_eye") === "on",
      breakfastRequired: form.get("breakfast_required") === "on",
      refundableRequired: form.get("refundable_required") === "on",
      includeAirbnb: form.get("include_airbnb") === "on",
    });
    setValidationError(undefined);
    setOpen(false);
  }

  return (
    <div className="mt-5 border-t border-[var(--line)] pt-4">
      <div className="flex flex-wrap items-center gap-3">
        <button
          type="button"
          disabled={disabled}
          aria-expanded={open}
          onClick={toggleEditor}
          className="flex items-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-[var(--teal)] disabled:opacity-50"
        >
          {open ? <X size={16} /> : <PencilLine size={16} />}
          {open ? tcr("cancel") : tcr("edit")}
        </button>
        <span className="text-xs text-[var(--muted)]">{tcr("hint")}</span>
      </div>

      {open && (
        <form aria-label={tcr("edit")} onSubmit={submit} className="mt-4 rounded-2xl bg-[var(--paper)] p-4">
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-5">
            <label className="text-sm font-semibold">{tcr("origin")}
              <select name="origin" defaultValue={criteria.origin || "TPE"} className={fieldClass}>
                <option value="TPE">{tcr("originTPE")}</option>
                <option value="TSA">{tcr("originTSA")}</option>
                <option value="KHH">{tcr("originKHH")}</option>
              </select>
            </label>
            <label className="text-sm font-semibold">{tcr("area")}
              {destination ? (
                <select name="preferred_area" defaultValue={criteria.preferred_area || destination.areas[0]} className={fieldClass}>
                  {destination.areas.map((area) => <option key={area}>{area}</option>)}
                </select>
              ) : (
                <input name="preferred_area" defaultValue={criteria.preferred_area} className={fieldClass} />
              )}
            </label>
            <label className="text-sm font-semibold">{tcr("departure")}
              <input required type="date" name="departure_date" defaultValue={dates[0]} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">{tcr("return")}
              <input required type="date" name="return_date" defaultValue={dates[1]} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">{tcr("flex")}
              <select name="flex_days" defaultValue={criteria.flex_days || 0} className={fieldClass}>
                <option value="0">{tcr("flexFixed")}</option><option value="3">{tcr("flex3")}</option><option value="7">{tcr("flex7")}</option>
              </select>
            </label>
          </div>

          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
            <label className="text-sm font-semibold">{tcr("adults")}
              <select name="adults" defaultValue={criteria.travelers.adults} className={fieldClass}>{[1, 2, 3, 4, 5, 6].map((value) => <option key={value}>{value}</option>)}</select>
            </label>
            <label className="text-sm font-semibold">{tcr("children")}
              <select name="children" defaultValue={criteria.travelers.children || 0} className={fieldClass}>{[0, 1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}</select>
            </label>
            <label className="text-sm font-semibold">{tcr("rooms")}
              <select name="rooms" defaultValue={criteria.travelers.rooms || 1} className={fieldClass}>{[1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}</select>
            </label>
            <label className="text-sm font-semibold">{tcr("budget")}
              <input type="number" min="1" name="budget_twd" defaultValue={criteria.budget_twd} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">{tcr("nightlyMax")}
              <input type="number" min="1" name="hotel_max_nightly_twd" defaultValue={criteria.hotel_max_nightly_twd} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">{tcr("pace")}
              <select name="pace" defaultValue={criteria.pace || "balanced"} className={fieldClass}>
                <option value="relaxed">{tcr("paceRelaxed")}</option><option value="balanced">{tcr("paceBalanced")}</option><option value="packed">{tcr("pacePacked")}</option>
              </select>
            </label>
          </div>

          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-5">
            <label className="text-sm font-semibold">{tcr("nightlyMin")}
              <input type="number" min="0" name="hotel_min_nightly_twd" defaultValue={criteria.hotel_min_nightly_twd} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">{tcr("propertyType")}
              <select name="accepted_property_types" defaultValue={(criteria.accepted_property_types || []).join(",")} className={fieldClass}>
                <option value="">{tcr("any")}</option><option value="hotel">{tcr("hotelOnly")}</option><option value="vacation_rental">{tcr("rentalOnly")}</option><option value="hotel,vacation_rental">{tcr("both")}</option>
              </select>
            </label>
            <label className="text-sm font-semibold">{tcr("minRating")}
              <select name="hotel_min_rating" defaultValue={criteria.hotel_min_rating || ""} className={fieldClass}><option value="">{tcr("any")}</option>{[3,4,5].map((value) => <option key={value}>{value}</option>)}</select>
            </label>
            <label className="text-sm font-semibold">{tcr("minReviewScore")}
              <select name="hotel_min_review_score" defaultValue={criteria.hotel_min_review_score || ""} className={fieldClass}><option value="">{tcr("any")}</option><option value="7">7.0+</option><option value="8">8.0+</option><option value="9">9.0+</option></select>
            </label>
            <label className="text-sm font-semibold">{tcr("minReviewCount")}
              <select name="hotel_min_review_count" defaultValue={criteria.hotel_min_review_count || ""} className={fieldClass}><option value="">{tcr("any")}</option>{[20,50,100,300].map((value) => <option key={value}>{value}+</option>)}</select>
            </label>
          </div>

          <fieldset className="mt-4">
            <legend className="text-sm font-semibold">{tcr("interests")}</legend>
            <div className="mt-2 flex flex-wrap gap-2">
              {interestCodes.map((code) => (
                <button key={code} type="button" aria-pressed={selectedInterests.includes(code)} onClick={() => toggleInterest(code)} className={`rounded-full border px-3 py-2 text-sm ${selectedInterests.includes(code) ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white"}`}>{tc(`interests.${code}`)}</button>
              ))}
            </div>
          </fieldset>

          <div className="mt-4 grid gap-2 text-sm sm:grid-cols-2 lg:grid-cols-4">
            <label className="flex items-center gap-2"><input type="checkbox" name="avoid_red_eye" defaultChecked={criteria.avoid_red_eye} />{tcr("avoidRedEye")}</label>
            <label className="flex items-center gap-2"><input type="checkbox" name="breakfast_required" defaultChecked={criteria.breakfast_required} />{tcr("breakfast")}</label>
            <label className="flex items-center gap-2"><input type="checkbox" name="refundable_required" defaultChecked={criteria.refundable_required} />{tcr("refundable")}</label>
            <label className="flex items-center gap-2"><input type="checkbox" name="include_airbnb" defaultChecked={criteria.include_airbnb ?? true} />{tcr("includeAirbnb")}</label>
          </div>

          {validationError && <p role="alert" className="mt-3 text-sm font-medium text-red-700">{validationError}</p>}
          <button className="mt-4 flex items-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 text-sm font-semibold text-white"><RotateCcw size={16} />{tcr("apply")}</button>
        </form>
      )}
    </div>
  );
}
