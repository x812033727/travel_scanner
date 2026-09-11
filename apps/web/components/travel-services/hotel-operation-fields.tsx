"use client";

import { useId } from "react";
import { useTranslations } from "next-intl";
import {
  readHotelOperationDraft, writeHotelOperationDraft,
  type HotelOperatingRules, type HotelUnavailableStay,
} from "@/lib/hotel-operation-rules";

const field = "mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] px-3 py-2 text-sm";
const button = "min-h-11 rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-50";

export function HotelOperationFields({ json, onChange, disabled = false }: {
  json: string;
  onChange: (json: string) => void;
  disabled?: boolean;
}) {
  const t = useTranslations("travelServices.hotelOperation");
  const id = useId();
  const draft = readHotelOperationDraft(json);
  const rules = draft.rules ?? { unavailable_stays: [] };
  const hasCutoff = rules.last_checkout_date != null || rules.last_checkout_reason != null || rules.last_checkout_source_url != null;
  const change = (next: HotelOperatingRules | null) => onChange(writeHotelOperationDraft(json, next));
  function changeRange(index: number, patch: Partial<HotelUnavailableStay>) {
    change({ ...rules, unavailable_stays: rules.unavailable_stays.map((range, i) => i === index ? { ...range, ...patch } : range) });
  }
  function removeCutoff() {
    const next = { ...rules };
    delete next.last_checkout_date;
    delete next.last_checkout_reason;
    delete next.last_checkout_source_url;
    change(next);
  }

  return <fieldset disabled={disabled || !draft.editable} className="mb-5 min-w-0 space-y-4 rounded-xl border border-[var(--line)] p-4" aria-describedby={`${id}-help`}>
    <legend className="px-1 font-semibold">{t("title")}</legend>
    <p id={`${id}-help`} className="text-sm leading-6 text-[var(--muted)]">{t("hint")}</p>
    {draft.error && <p role="alert" className="text-sm text-red-700">{t(`errors.${draft.error}`)}</p>}
    {draft.editable && <>
      {rules.unavailable_stays.map((range, index) => <fieldset key={index} className="min-w-0 space-y-3 rounded-xl border border-[var(--line)] p-3">
        <legend className="px-1 text-sm font-semibold">{t("range", { number: index + 1 })}</legend>
        <div className="grid gap-3 sm:grid-cols-2">
          <label className="block text-sm">{t("startDate")}<input type="date" required className={field} value={range.start_date} onChange={(event) => changeRange(index, { start_date: event.target.value })} /></label>
          <label className="block text-sm">{t("endDate")}<input type="date" required className={field} value={range.end_date} onChange={(event) => changeRange(index, { end_date: event.target.value })} /></label>
        </div>
        <p className="text-xs leading-5 text-[var(--muted)]">{t("rangeHint")}</p>
        <label className="block text-sm">{t("reason")}<textarea required maxLength={1000} rows={2} className={field} value={range.reason} onChange={(event) => changeRange(index, { reason: event.target.value })} /></label>
        <label className="block text-sm">{t("source")}<input type="url" required className={field} value={range.source_url} placeholder="https://" onChange={(event) => changeRange(index, { source_url: event.target.value })} /></label>
        <button type="button" className={button} onClick={() => change({ ...rules, unavailable_stays: rules.unavailable_stays.filter((_, i) => i !== index) })}>{t("removeRange", { number: index + 1 })}</button>
      </fieldset>)}
      <button type="button" className={button} disabled={rules.unavailable_stays.length >= 50} onClick={() => change({ ...rules, unavailable_stays: [...rules.unavailable_stays, { start_date: "", end_date: "", reason: "", source_url: "" }] })}>{t("addRange")}</button>
      {hasCutoff ? <fieldset className="min-w-0 space-y-3 rounded-xl border border-[var(--line)] p-3">
        <legend className="px-1 text-sm font-semibold">{t("cutoffTitle")}</legend>
        <label className="block text-sm">{t("lastCheckoutDate")}<input type="date" required className={field} value={rules.last_checkout_date ?? ""} onChange={(event) => change({ ...rules, last_checkout_date: event.target.value })} /></label>
        <p className="text-xs leading-5 text-[var(--muted)]">{t("cutoffHint")}</p>
        <label className="block text-sm">{t("reason")}<textarea required maxLength={1000} rows={2} className={field} value={rules.last_checkout_reason ?? ""} onChange={(event) => change({ ...rules, last_checkout_reason: event.target.value })} /></label>
        <label className="block text-sm">{t("source")}<input type="url" required className={field} value={rules.last_checkout_source_url ?? ""} placeholder="https://" onChange={(event) => change({ ...rules, last_checkout_source_url: event.target.value })} /></label>
        <button type="button" className={button} onClick={removeCutoff}>{t("removeCutoff")}</button>
      </fieldset> : <button type="button" className={`${button} block`} onClick={() => change({ ...rules, last_checkout_date: "", last_checkout_reason: "", last_checkout_source_url: "" })}>{t("addCutoff")}</button>}
      <p className="text-sm text-[var(--muted)]">{t("saveHint")}</p>
    </>}
  </fieldset>;
}
