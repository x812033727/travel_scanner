"use client";

import { PencilLine, RotateCcw, X } from "lucide-react";
import { type FormEvent, useState } from "react";
import { interests as destinationInterests, type DestinationCity } from "@/lib/destinations";

export type EditableSearchCriteria = {
  origin?: string;
  departure_date?: string;
  return_date?: string;
  travelers: { adults: number; children?: number; rooms?: number };
  budget_twd?: number;
  interests: string[];
  avoid_red_eye: boolean;
  hotel_max_nightly_twd?: number;
  breakfast_required?: boolean;
  refundable_required?: boolean;
  preferred_area?: string;
  pace?: "relaxed" | "balanced" | "packed";
};

export type CriteriaUpdate = {
  origin: string;
  departureDate: string;
  returnDate: string;
  adults: number;
  children: number;
  rooms: number;
  budget?: number;
  nightlyBudget?: number;
  preferredArea?: string;
  pace: "relaxed" | "balanced" | "packed";
  interests: string[];
  avoidRedEye: boolean;
  breakfastRequired: boolean;
  refundableRequired: boolean;
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
      setValidationError("回程日期必須晚於出發日期。");
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
      adults: Number(form.get("adults") || 1),
      children: Number(form.get("children") || 0),
      rooms: Number(form.get("rooms") || 1),
      budget: numberOrUndefined("budget_twd"),
      nightlyBudget: numberOrUndefined("hotel_max_nightly_twd"),
      preferredArea: String(form.get("preferred_area") || "") || undefined,
      pace: String(form.get("pace") || "balanced") as CriteriaUpdate["pace"],
      interests: selectedInterests,
      avoidRedEye: form.get("avoid_red_eye") === "on",
      breakfastRequired: form.get("breakfast_required") === "on",
      refundableRequired: form.get("refundable_required") === "on",
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
          {open ? "取消修改" : "修改搜尋條件"}
        </button>
        <span className="text-xs text-[var(--muted)]">套用後會清除舊結果，再由你確認是否重新搜尋。</span>
      </div>

      {open && (
        <form aria-label="修改搜尋條件" onSubmit={submit} className="mt-4 rounded-2xl bg-[var(--paper)] p-4">
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <label className="text-sm font-semibold">出發機場
              <select name="origin" defaultValue={criteria.origin || "TPE"} className={fieldClass}>
                <option value="TPE">桃園 TPE</option>
                <option value="TSA">松山 TSA</option>
                <option value="KHH">高雄 KHH</option>
              </select>
            </label>
            <label className="text-sm font-semibold">住宿區域
              {destination ? (
                <select name="preferred_area" defaultValue={criteria.preferred_area || destination.areas[0]} className={fieldClass}>
                  {destination.areas.map((area) => <option key={area}>{area}</option>)}
                </select>
              ) : (
                <input name="preferred_area" defaultValue={criteria.preferred_area} className={fieldClass} />
              )}
            </label>
            <label className="text-sm font-semibold">出發日期
              <input required type="date" name="departure_date" defaultValue={dates[0]} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">回程日期
              <input required type="date" name="return_date" defaultValue={dates[1]} className={fieldClass} />
            </label>
          </div>

          <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-6">
            <label className="text-sm font-semibold">成人
              <select name="adults" defaultValue={criteria.travelers.adults} className={fieldClass}>{[1, 2, 3, 4, 5, 6].map((value) => <option key={value}>{value}</option>)}</select>
            </label>
            <label className="text-sm font-semibold">兒童
              <select name="children" defaultValue={criteria.travelers.children || 0} className={fieldClass}>{[0, 1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}</select>
            </label>
            <label className="text-sm font-semibold">房間
              <select name="rooms" defaultValue={criteria.travelers.rooms || 1} className={fieldClass}>{[1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}</select>
            </label>
            <label className="text-sm font-semibold">總預算 TWD
              <input type="number" min="1" name="budget_twd" defaultValue={criteria.budget_twd} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">住宿每晚上限
              <input type="number" min="1" name="hotel_max_nightly_twd" defaultValue={criteria.hotel_max_nightly_twd} className={fieldClass} />
            </label>
            <label className="text-sm font-semibold">每日步調
              <select name="pace" defaultValue={criteria.pace || "balanced"} className={fieldClass}>
                <option value="relaxed">悠閒</option><option value="balanced">適中</option><option value="packed">充實</option>
              </select>
            </label>
          </div>

          <fieldset className="mt-4">
            <legend className="text-sm font-semibold">行程興趣</legend>
            <div className="mt-2 flex flex-wrap gap-2">
              {destinationInterests.map((interest) => (
                <button key={interest.code} type="button" aria-pressed={selectedInterests.includes(interest.code)} onClick={() => toggleInterest(interest.code)} className={`rounded-full border px-3 py-2 text-sm ${selectedInterests.includes(interest.code) ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white"}`}>{interest.label}</button>
              ))}
            </div>
          </fieldset>

          <div className="mt-4 grid gap-2 text-sm sm:grid-cols-3">
            <label className="flex items-center gap-2"><input type="checkbox" name="avoid_red_eye" defaultChecked={criteria.avoid_red_eye} />避開紅眼航班</label>
            <label className="flex items-center gap-2"><input type="checkbox" name="breakfast_required" defaultChecked={criteria.breakfast_required} />住宿含早餐</label>
            <label className="flex items-center gap-2"><input type="checkbox" name="refundable_required" defaultChecked={criteria.refundable_required} />住宿可退款</label>
          </div>

          {validationError && <p role="alert" className="mt-3 text-sm font-medium text-red-700">{validationError}</p>}
          <button className="mt-4 flex items-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 text-sm font-semibold text-white"><RotateCcw size={16} />套用並重新規劃</button>
        </form>
      )}
    </div>
  );
}
