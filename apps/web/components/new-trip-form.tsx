"use client";

import { ArrowRight, CalendarDays, Check, ChevronLeft, ChevronRight, Hotel, MapPinned, Route, Sparkles, Users } from "lucide-react";
import { useRouter } from "@/i18n/navigation";
import { useTranslations } from "next-intl";
import { useEffect, useMemo, useRef, useState } from "react";
import { PlacePicker } from "@/components/place-picker";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import { api, twd } from "@/lib/api";
import { trackAnalytics } from "@/lib/analytics";
import { interests } from "@/lib/destinations";

type CreatedTrip = { id: string };
type LodgingMode = "hotel" | "vacation_rental" | "both" | "any";
type Pace = "relaxed" | "balanced" | "packed";
type PlanningMode = "ai_draft" | "manual_blank";

const stepKeys = ["basics", "travelers", "stay", "review"] as const;
const fieldClass = "mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-4 py-3 font-normal outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

function optionClass(active: boolean) {
  return `rounded-xl border px-3 py-3 text-left text-sm transition ${active ? "border-[var(--teal)] bg-[var(--teal-soft)] font-semibold text-[var(--teal-dark)]" : "border-[var(--line)] bg-white hover:border-[var(--teal)]"}`;
}

function optionalNumber(value: string) {
  const parsed = Number(value);
  return value && Number.isFinite(parsed) ? parsed : null;
}

function tripDayCount(start: string, end: string) {
  if (!start || !end || end < start) return 0;
  return Math.round((Date.parse(`${end}T00:00:00Z`) - Date.parse(`${start}T00:00:00Z`)) / 86_400_000) + 1;
}

const DRAFT_STORAGE_KEY = "mokaair-new-trip-draft";

type DraftSnapshot = {
  step: number;
  lodgingMode: LodgingMode;
  planningMode: PlanningMode;
  selectedInterests: string[];
  form: Record<string, string | boolean>;
};

function readDraft(): DraftSnapshot | undefined {
  try {
    const raw = window.sessionStorage.getItem(DRAFT_STORAGE_KEY);
    if (!raw) return undefined;
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") return undefined;
    return parsed as DraftSnapshot;
  } catch {
    return undefined;
  }
}

function clearDraft() {
  try {
    window.sessionStorage.removeItem(DRAFT_STORAGE_KEY);
  } catch {
    // storage may be unavailable; losing the draft is acceptable
  }
}

export function NewTripForm() {
  const router = useRouter();
  const t = useTranslations("newTrip");
  const aiCharge = useOperationCharge("ai_itinerary_generation");
  const optimizationCharge = useOperationCharge("itinerary_optimization");
  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [lodgingMode, setLodgingMode] = useState<LodgingMode>("any");
  const [planningMode, setPlanningMode] = useState<PlanningMode>("ai_draft");
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [form, setForm] = useState({
    name: "", destination_name: "", destination_place_id: "", start_date: "", end_date: "",
    adults: "2", children: "0", rooms: "1", budget_twd: "", pace: "balanced" as Pace,
    route_preference: "FEWER_TRANSFERS", nightly_min: "", nightly_max: "", hotel_min_rating: "",
    preferred_area: "", max_station_walk_minutes: "", min_review_score: "", min_review_count: "",
    breakfast_required: false, refundable_required: false, avoid_red_eye: true, notes: "",
  });
  const errorRef = useRef<HTMLParagraphElement>(null);
  // One key per creation attempt, kept across retries so a proxy timeout
  // followed by a second click replays the same trip instead of duplicating it.
  const submitKey = useRef<string | undefined>(undefined);
  const today = useMemo(() => new Date().toLocaleDateString("sv"), []);
  const days = tripDayCount(form.start_date, form.end_date);
  const travelerCount = Number(form.adults) + Number(form.children);

  const [draftReady, setDraftReady] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const draft = readDraft();
      if (draft) {
        if (typeof draft.step === "number") setStep(Math.min(Math.max(draft.step, 0), stepKeys.length - 1));
        if (draft.lodgingMode) setLodgingMode(draft.lodgingMode);
        if (draft.planningMode) setPlanningMode(draft.planningMode);
        if (Array.isArray(draft.selectedInterests)) setSelectedInterests(draft.selectedInterests.filter((code) => typeof code === "string"));
        if (draft.form && typeof draft.form === "object") {
          setForm((current) => {
            const next = { ...current };
            for (const key of Object.keys(current) as (keyof typeof current)[]) {
              const value = draft.form[key];
              if (typeof value === typeof current[key]) (next as Record<string, string | boolean>)[key] = value;
            }
            return next;
          });
        }
      }
      setDraftReady(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (!draftReady) return;
    try {
      window.sessionStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify({ step, lodgingMode, planningMode, selectedInterests, form } satisfies DraftSnapshot));
    } catch {
      // storage may be unavailable; autosave is best-effort
    }
  }, [draftReady, form, step, lodgingMode, planningMode, selectedInterests]);

  useEffect(() => {
    if (error) errorRef.current?.focus();
  }, [error]);
  const propertyTypes = lodgingMode === "hotel" ? ["hotel"] : lodgingMode === "vacation_rental" ? ["vacation_rental"] : lodgingMode === "both" ? ["hotel", "vacation_rental"] : [];
  const lodgingSummary = lodgingMode === "hotel" ? t("summary.hotelOnly") : lodgingMode === "vacation_rental" ? t("summary.vacationRental") : lodgingMode === "both" ? t("summary.both") : t("summary.any");
  const interestLabels = selectedInterests.map((code) => t(`interests.${code}`));
  const summary = useMemo(() => [
    days ? t("summary.days", { days }) : null,
    t("summary.travelers", { count: travelerCount, rooms: form.rooms }),
    form.budget_twd ? t("summary.budget", { amount: twd.format(Number(form.budget_twd)) }) : t("summary.budgetUnlimited"),
    lodgingSummary,
    ...interestLabels,
  ].filter(Boolean) as string[], [days, form.budget_twd, form.rooms, interestLabels, lodgingSummary, t, travelerCount]);
  const nightlyMin = optionalNumber(form.nightly_min);
  const nightlyMax = optionalNumber(form.nightly_max);
  const nightlyLabel = nightlyMin != null && nightlyMax != null
    ? t("review.values.nightlyRange", { min: twd.format(nightlyMin), max: twd.format(nightlyMax) })
    : nightlyMin != null ? t("review.values.nightlyFrom", { min: twd.format(nightlyMin) }) : nightlyMax != null ? t("review.values.nightlyUpTo", { max: twd.format(nightlyMax) }) : t("review.values.unlimited");
  const routeLabel = form.route_preference === "FASTEST" ? t("review.fastest") : form.route_preference === "LESS_WALKING" ? t("review.lessWalking") : t("review.fewerTransfers");
  const paceLabel = form.pace === "relaxed" ? t("travelers.paceRelaxed") : form.pace === "packed" ? t("travelers.pacePacked") : t("travelers.paceBalanced");
  const noPreference = t("review.values.noPreference");
  const reviewDetails = [
    [t("review.labels.travelers"), t("review.values.travelers", { count: travelerCount, rooms: form.rooms })],
    [t("review.labels.budget"), form.budget_twd ? twd.format(Number(form.budget_twd)) : t("review.values.unlimited")],
    [t("review.labels.pace"), paceLabel],
    [t("review.labels.interests"), interestLabels.length ? interestLabels.join(t("review.values.listSeparator")) : noPreference],
    [t("review.labels.lodging"), lodgingSummary],
    [t("review.labels.nightly"), nightlyLabel],
    [t("review.labels.minRating"), form.hotel_min_rating ? t("stay.starsPlus", { stars: form.hotel_min_rating }) : noPreference],
    [t("review.labels.area"), form.preferred_area.trim() || noPreference],
    [t("review.labels.stationWalk"), form.max_station_walk_minutes ? t("stay.minutes", { minutes: form.max_station_walk_minutes }) : noPreference],
    [t("review.labels.reviewScore"), form.min_review_score ? `${form.min_review_score}+` : noPreference],
    [t("review.labels.reviewCount"), form.min_review_count ? t("stay.reviewsPlus", { count: form.min_review_count }) : noPreference],
    [t("review.labels.breakfast"), form.breakfast_required ? t("review.values.breakfastRequired") : t("review.values.notRequired")],
    [t("review.labels.cancellation"), form.refundable_required ? t("review.values.refundableRequired") : t("review.values.notRequired")],
    [t("review.labels.transit"), routeLabel],
    [t("review.labels.flights"), form.avoid_red_eye ? t("review.values.avoidRedEye") : t("review.values.allowRedEye")],
    [t("review.labels.start"), planningMode === "manual_blank" ? t("review.manualBlank") : t("review.aiDraft")],
  ];

  function update<K extends keyof typeof form>(key: K, value: (typeof form)[K]) {
    setError(undefined);
    setForm((current) => ({ ...current, [key]: value }));
  }

  function chooseLodgingMode(value: LodgingMode) {
    setError(undefined);
    setLodgingMode(value);
  }

  function choosePlanningMode(value: PlanningMode) {
    setError(undefined);
    setPlanningMode(value);
  }

  function validate(targetStep = 3) {
    if (targetStep >= 1) {
      if (!form.name.trim()) return t("errors.nameRequired");
      if (!form.destination_name.trim()) return t("errors.destinationRequired");
      if (!form.start_date || !form.end_date) return t("errors.datesRequired");
      if (form.start_date < today) return t("errors.startInPast");
      if (form.end_date < form.start_date) return t("errors.endBeforeStart");
      if (days > 61) return t("errors.tooLong");
    }
    if (targetStep >= 2) {
      if (Number(form.rooms) > travelerCount) return t("errors.roomsExceedTravelers");
      if (form.budget_twd && Number(form.budget_twd) <= 0) return t("errors.budgetPositive");
    }
    if (targetStep >= 3) {
      const min = optionalNumber(form.nightly_min);
      const max = optionalNumber(form.nightly_max);
      if (min != null && max != null && min > max) return t("errors.nightlyInverted");
    }
    return undefined;
  }

  function next() {
    const message = validate(step + 1);
    if (message) { setError(message); return; }
    setError(undefined);
    setStep((current) => Math.min(current + 1, stepKeys.length - 1));
  }

  function toggleInterest(code: string) {
    setError(undefined);
    setSelectedInterests((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]);
  }

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = validate();
    if (message) { setError(message); return; }
    setBusy(true);
    setError(undefined);
    if (!submitKey.current) submitKey.current = crypto.randomUUID();
    try {
      const trip = await api<CreatedTrip>("/trips", {
        method: "POST",
        headers: { "Idempotency-Key": submitKey.current },
        body: JSON.stringify({
          source: "blank",
          planning_mode: planningMode,
          name: form.name.trim(),
          destination_name: form.destination_name.trim(),
          destination_place_id: form.destination_place_id || null,
          start_date: form.start_date,
          end_date: form.end_date,
          route_preference: form.route_preference,
          routing: {
            auto_compute: planningMode === "ai_draft",
            default_travel_mode: "transit",
            default_buffer_minutes: 10,
          },
          travelers: { adults: Number(form.adults), children: Number(form.children), rooms: Number(form.rooms) },
          preferences: {
            budget_twd: optionalNumber(form.budget_twd), avoid_red_eye: form.avoid_red_eye,
            hotel_min_rating: optionalNumber(form.hotel_min_rating),
            hotel_min_nightly_twd: optionalNumber(form.nightly_min), hotel_max_nightly_twd: optionalNumber(form.nightly_max),
            accepted_property_types: propertyTypes, hotel_min_review_score: optionalNumber(form.min_review_score),
            hotel_min_review_count: optionalNumber(form.min_review_count), breakfast_required: form.breakfast_required,
            refundable_required: form.refundable_required, max_station_walk_minutes: optionalNumber(form.max_station_walk_minutes),
            preferred_area: form.preferred_area.trim() || null, pace: form.pace, interests: selectedInterests,
          },
          notes: form.notes.trim() || null,
        }),
      });
      trackAnalytics("trip_created");
      clearDraft();
      submitKey.current = undefined;
      router.push(`/trips/${trip.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : t("errors.createFailed"));
    } finally { setBusy(false); }
  }

  return <form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
    <section className="rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8">
      <div className="mb-6 flex items-start gap-4"><span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-[var(--teal-soft)] text-[var(--teal)]"><MapPinned size={23} /></span><div><p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p><h1 className="mt-1 text-3xl font-bold">{t("title")}</h1></div></div>
      <ol aria-label={t("stepsLabel")} className="mb-7 grid grid-cols-4 gap-1">{stepKeys.map((key, index) => <li key={key} className={`rounded-xl px-1 py-2 text-center text-xs font-semibold ${index === step ? "bg-[var(--teal)] text-white" : index < step ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "bg-[var(--paper)] text-[var(--muted)]"}`}><span className="hidden sm:inline">{index + 1}. </span>{t(`steps.${key}`)}</li>)}</ol>

      <div className={step === 0 ? "grid gap-5" : "hidden"}>
        <label className="text-sm font-semibold">{t("basics.name")}<input required maxLength={255} value={form.name} onChange={(event) => update("name", event.target.value)} placeholder={t("basics.namePlaceholder")} className={fieldClass} /></label>
        <div><label htmlFor="trip-destination" className="text-sm font-semibold">{t("basics.destination")}</label><div className="mt-2"><PlacePicker inputId="trip-destination" label={t("basics.destination")} descriptionId="trip-destination-help" value={form.destination_name} confirmed={Boolean(form.destination_place_id)} countryCodes={["jp", "kr", "th"]} kinds="cities" placeholder={t("basics.destinationPlaceholder")} onTextChange={(value) => setForm((current) => ({ ...current, destination_name: value, destination_place_id: "" }))} onSelect={(place) => setForm((current) => ({ ...current, destination_name: place.name, destination_place_id: place.place_id }))} /></div><p id="trip-destination-help" className="mt-1 text-xs font-normal text-[var(--muted)]">{t("basics.destinationHelp")}</p></div>
        <div className="grid gap-4 sm:grid-cols-2"><label className="text-sm font-semibold">{t("basics.startDate")}<input required type="date" min={today} value={form.start_date} onChange={(event) => { setError(undefined); setForm((current) => ({ ...current, start_date: event.target.value, end_date: current.end_date && current.end_date < event.target.value ? "" : current.end_date })); }} className={fieldClass} /></label><label className="text-sm font-semibold">{t("basics.endDate")}<input required type="date" min={form.start_date || today} value={form.end_date} onChange={(event) => update("end_date", event.target.value)} className={fieldClass} /></label></div>
        {days > 0 && <p className="rounded-xl bg-[var(--paper)] px-4 py-3 text-sm">{t("basics.dayCountBefore")}<strong>{t("basics.dayCount", { days })}</strong>{t("basics.dayCountAfter")}</p>}
      </div>

      <div className={step === 1 ? "grid gap-5" : "hidden"}>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Users size={19} />{t("travelers.title")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("travelers.help")}</p></div>
        <div className="grid grid-cols-3 gap-3"><label className="text-sm font-semibold">{t("travelers.adults")}<select aria-label={t("travelers.adults")} value={form.adults} onChange={(event) => update("adults", event.target.value)} className={fieldClass}>{[1,2,3,4,5,6,7,8,9].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">{t("travelers.children")}<select aria-label={t("travelers.children")} value={form.children} onChange={(event) => update("children", event.target.value)} className={fieldClass}>{[0,1,2,3,4,5].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">{t("travelers.rooms")}<select aria-label={t("travelers.rooms")} value={form.rooms} onChange={(event) => update("rooms", event.target.value)} className={fieldClass}>{[1,2,3,4].map((value) => <option key={value}>{value}</option>)}</select></label></div>
        <label className="text-sm font-semibold">{t("travelers.budget")}<input type="number" min="1" value={form.budget_twd} onChange={(event) => update("budget_twd", event.target.value)} placeholder={t("travelers.budgetPlaceholder")} className={fieldClass} /></label>
        <div><p className="text-sm font-semibold">{t("travelers.pace")}</p><div className="mt-2 grid grid-cols-3 gap-2">{([["relaxed", t("travelers.paceRelaxed")], ["balanced", t("travelers.paceBalanced")], ["packed", t("travelers.pacePacked")]] as const).map(([value, label]) => <button key={value} type="button" aria-pressed={form.pace === value} onClick={() => update("pace", value)} className={optionClass(form.pace === value)}>{label}</button>)}</div></div>
        <div><p className="text-sm font-semibold">{t("travelers.interests")}</p><div className="mt-2 flex flex-wrap gap-2">{interests.map((interest) => <button key={interest.code} type="button" aria-pressed={selectedInterests.includes(interest.code)} onClick={() => toggleInterest(interest.code)} className={optionClass(selectedInterests.includes(interest.code))}>{t(`interests.${interest.code}`)}</button>)}</div></div>
      </div>

      <div className={step === 2 ? "grid gap-5" : "hidden"}>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Hotel size={19} />{t("stay.title")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("stay.help")}</p></div>
        <div className="grid grid-cols-2 gap-2">{([["hotel", t("stay.hotelOnly")], ["vacation_rental", t("stay.vacationRental")], ["both", t("stay.both")], ["any", t("stay.any")]] as const).map(([value, label]) => <button key={value} type="button" aria-pressed={lodgingMode === value} onClick={() => chooseLodgingMode(value)} className={optionClass(lodgingMode === value)}>{label}</button>)}</div>
        <div className="grid grid-cols-2 gap-3"><label className="text-sm font-semibold">{t("stay.nightlyMin")}<input aria-label={t("stay.nightlyMin")} type="number" min="0" value={form.nightly_min} onChange={(event) => update("nightly_min", event.target.value)} placeholder={t("stay.noPreference")} className={fieldClass} /></label><label className="text-sm font-semibold">{t("stay.nightlyMax")}<input aria-label={t("stay.nightlyMax")} type="number" min="1" value={form.nightly_max} onChange={(event) => update("nightly_max", event.target.value)} placeholder={t("stay.noPreference")} className={fieldClass} /></label><label className="text-sm font-semibold">{t("stay.minRating")}<select aria-label={t("stay.minRating")} value={form.hotel_min_rating} onChange={(event) => update("hotel_min_rating", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option>{[3,4,5].map((value) => <option key={value} value={value}>{t("stay.starsPlus", { stars: value })}</option>)}</select></label><label className="text-sm font-semibold">{t("stay.stationWalk")}<select aria-label={t("stay.stationWalk")} value={form.max_station_walk_minutes} onChange={(event) => update("max_station_walk_minutes", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option>{[5,10,15,20].map((value) => <option key={value} value={value}>{t("stay.minutes", { minutes: value })}</option>)}</select></label><label className="text-sm font-semibold">{t("stay.minReviewScore")}<select aria-label={t("stay.minReviewScore")} value={form.min_review_score} onChange={(event) => update("min_review_score", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option><option value="7">7.0+</option><option value="8">8.0+</option><option value="9">9.0+</option></select></label><label className="text-sm font-semibold">{t("stay.minReviewCount")}<select aria-label={t("stay.minReviewCount")} value={form.min_review_count} onChange={(event) => update("min_review_count", event.target.value)} className={fieldClass}><option value="">{t("stay.noPreference")}</option>{[20,50,100,300].map((value) => <option key={value} value={value}>{t("stay.reviewsPlus", { count: value })}</option>)}</select></label></div>
        <label className="text-sm font-semibold">{t("stay.preferredArea")}<input value={form.preferred_area} onChange={(event) => update("preferred_area", event.target.value)} placeholder={t("stay.preferredAreaPlaceholder")} className={fieldClass} /></label>
        <div className="grid gap-2 text-sm sm:grid-cols-2"><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.breakfast_required} onChange={(event) => update("breakfast_required", event.target.checked)} />{t("stay.breakfast")}</label><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.refundable_required} onChange={(event) => update("refundable_required", event.target.checked)} />{t("stay.refundable")}</label></div>
      </div>

      <div className={step === 3 ? "grid gap-5" : "hidden"}>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Check size={19} />{t("review.title")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("review.help")}</p></div>
        <fieldset><legend className="text-sm font-semibold">{t("review.planningMode")}</legend><div className="mt-2 grid gap-3 sm:grid-cols-2"><button type="button" aria-pressed={planningMode === "ai_draft"} onClick={() => choosePlanningMode("ai_draft")} className={optionClass(planningMode === "ai_draft")}><strong className="block">{t("review.aiDraft")}</strong><span className="mt-1 block text-xs font-normal leading-5 text-[var(--muted)]">{t("review.aiDraftHelp")}</span></button><button type="button" aria-pressed={planningMode === "manual_blank"} onClick={() => choosePlanningMode("manual_blank")} className={optionClass(planningMode === "manual_blank")}><strong className="block">{t("review.manualBlank")}</strong><span className="mt-1 block text-xs font-normal leading-5 text-[var(--muted)]">{t("review.manualBlankHelp")}</span></button></div></fieldset>
        <div className="grid gap-3 sm:grid-cols-2"><label className="text-sm font-semibold">{t("review.routePreference")}<select value={form.route_preference} onChange={(event) => update("route_preference", event.target.value)} className={fieldClass}><option value="FEWER_TRANSFERS">{t("review.fewerTransfers")}</option><option value="FASTEST">{t("review.fastest")}</option><option value="LESS_WALKING">{t("review.lessWalking")}</option></select></label><label className="flex items-center gap-2 self-end rounded-xl bg-[var(--paper)] p-3 text-sm"><input type="checkbox" checked={form.avoid_red_eye} onChange={(event) => update("avoid_red_eye", event.target.checked)} />{t("review.avoidRedEye")}</label></div>
        <label className="text-sm font-semibold">{t("review.notes")}<textarea rows={3} maxLength={1000} value={form.notes} onChange={(event) => update("notes", event.target.value)} placeholder={t("review.notesPlaceholder")} className={fieldClass} /></label>
        <section role="region" aria-label={t("review.summaryRegion")} className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5"><p className="text-xs font-semibold text-[var(--teal)]">{form.start_date} → {form.end_date}</p><h3 className="mt-1 text-2xl font-bold">{form.name.trim()}</h3><p className="mt-1 text-sm text-[var(--muted)]">{form.destination_name.trim()}</p><dl className="mt-5 grid gap-x-5 gap-y-3 sm:grid-cols-2">{reviewDetails.map(([label, value]) => <div key={label} className="border-t border-[var(--line)] pt-3"><dt className="text-xs font-semibold text-[var(--muted)]">{label}</dt><dd className="mt-1 text-sm font-medium">{value}</dd></div>)}</dl>{form.notes.trim() && <div className="mt-4 border-t border-[var(--line)] pt-4"><p className="text-xs font-semibold text-[var(--muted)]">{t("review.notes")}</p><p className="mt-1 whitespace-pre-wrap text-sm">{form.notes.trim()}</p></div>}</section>
        {planningMode === "ai_draft" ? <p className="rounded-xl bg-amber-50 px-4 py-3 text-xs leading-5 text-amber-900">{t("review.aiNotice")}</p> : <p className="rounded-xl bg-emerald-50 px-4 py-3 text-xs leading-5 text-emerald-900">{t("review.manualNotice")}</p>}
      </div>

      {error && <p ref={errorRef} tabIndex={-1} role="alert" aria-live="polite" className="mt-5 rounded-xl bg-red-50 p-4 text-sm text-red-800 outline-none">{error}</p>}
      <div className="mt-7 flex gap-3">{step > 0 && <button type="button" disabled={busy} onClick={() => { setError(undefined); setStep((current) => current - 1); }} className="flex items-center gap-1 rounded-xl border border-[var(--line)] px-4 py-3 font-semibold disabled:opacity-40"><ChevronLeft size={18} />{t("actions.back")}</button>}{step < stepKeys.length - 1 ? <button key="next-trip-step" type="button" onClick={(event) => { event.preventDefault(); next(); }} className="ml-auto flex items-center gap-1 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white">{t("actions.next")}<ChevronRight size={18} /></button> : <button key="submit-trip" type="submit" disabled={busy} className="ml-auto flex items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white disabled:opacity-60">{busy ? planningMode === "manual_blank" ? t("actions.creatingManual") : t("actions.creatingAi") : planningMode === "manual_blank" ? t("actions.createManual") : t("actions.createAi")}<ArrowRight size={18} /></button>}</div>
    </section>

    <aside className="rounded-[2rem] bg-[var(--ink)] p-6 text-white md:p-8">
      <p className="text-xs font-semibold tracking-[.18em] text-emerald-200">{t("summary.eyebrow")}</p><h2 className="mt-2 text-2xl font-bold">{form.destination_name.trim() || t("summary.noDestination")}</h2><div className="mt-5 flex flex-wrap gap-2">{summary.map((item) => <span key={item} className="rounded-full bg-white/10 px-3 py-1.5 text-xs text-white/80">{item}</span>)}</div>
      <div className="mt-7 space-y-5"><div className="flex gap-3"><CalendarDays className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">{planningMode === "manual_blank" ? t("summary.manualTitle") : t("summary.aiTitle")}</h3><p className="mt-1 text-sm leading-6 text-white/65">{planningMode === "manual_blank" ? t("summary.manualBody") : t("summary.aiBody")}</p></div></div><div className="flex gap-3"><Route className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">{t("summary.routesTitle")}</h3><p className="mt-1 text-sm leading-6 text-white/65">{planningMode === "manual_blank" ? t("summary.routesManualBody") : t("summary.routesAiBody")}</p></div></div><div className="flex gap-3"><Sparkles className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">{t("summary.prefsTitle")}</h3><p className="mt-1 text-sm leading-6 text-white/65">{t("summary.prefsBody")}</p></div></div></div>
      <p className="mt-8 rounded-2xl bg-white/10 p-4 text-sm leading-6 text-white/75">{t("summary.pricing", { ai: aiCharge.label, optimization: optimizationCharge.label })}</p>
    </aside>
  </form>;
}
