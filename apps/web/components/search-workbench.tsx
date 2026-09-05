"use client";

import { CalendarDays, Check, ChevronLeft, ChevronRight, Hotel, LoaderCircle, MapPin, Sparkles, Users } from "lucide-react";
import { useTranslations } from "next-intl";
import { useRouter } from "@/i18n/navigation";
import { type FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { api, twd } from "@/lib/api";
import { destinations, countries, interestLabel, interests, type CountryKey, type DestinationCity } from "@/lib/destinations";

const fieldClass = "mt-2 w-full rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 text-[var(--ink)] outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";
const stepKeys = ["dates", "destination", "party", "lodging", "preferences"] as const;

type Recommendation = {
  candidate_id: string; city: string; airport: string; country: string; country_code: CountryKey;
  areas: string[]; reason: string; departure_date: string; return_date: string;
  trip_length_days: number; estimated_flight_twd: number; estimated_lodging_twd: number;
  estimated_total_twd: number; score: number; matched_interests: string[]; relaxed_preferences: string[];
};
type DiscoveryResult = { recommendations: Recommendation[]; assumptions: string[] };
type CatalogDestination = {
  id: string; code: string; city: string; country_code: CountryKey; role: "primary" | "secondary" | "extension";
  parent_destination_id: string | null; gateway_codes: string[]; primary_gateway: string; areas: string[];
  recommended_days: { min: number; max: number }; timezone: string; currency: string; reason: string; searchable: boolean;
};
type CatalogResponse = { items: CatalogDestination[] };
type LodgingMode = "hotel" | "vacation_rental" | "both" | "any";

function futureDate(days: number) {
  const value = new Date(); value.setUTCDate(value.getUTCDate() + days);
  return value.toISOString().slice(0, 10);
}
function optionClass(active: boolean) {
  return `rounded-2xl border px-3 py-3 text-left transition ${active ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white hover:border-[var(--teal)]"}`;
}
// The visible sentinel used to group dynamic secondary cities.
const SECONDARY_TAG = "二線城市";

export function SearchWorkbench() {
  const t = useTranslations("search.workbench");
  const router = useRouter();
  const [step, setStepState] = useState(0);
  const [dateAny, setDateAny] = useState(false);
  const [lengthAny, setLengthAny] = useState(false);
  const [countriesSelected, setCountriesSelected] = useState<CountryKey[]>(["JP"]);
  const [destinationCode, setDestinationCode] = useState("");
  const [catalog, setCatalog] = useState<CatalogDestination[]>([]);
  const [selectedExtensions, setSelectedExtensions] = useState<string[]>([]);
  const [children, setChildren] = useState(0);
  const [childAges, setChildAges] = useState<number[]>([]);
  const [lodgingMode, setLodgingMode] = useState<LodgingMode>("hotel");
  const [selectedInterests, setSelectedInterests] = useState(["food", "shopping", "culture"]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [selectedAreas, setSelectedAreas] = useState<Record<string, string>>({});
  const [assumptions, setAssumptions] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [dateError, setDateError] = useState<string>();
  const stepHeadingRef = useRef<HTMLHeadingElement>(null);
  const stepChangedByUser = useRef(false);
  useEffect(() => {
    void api<CatalogResponse>("/destinations")
      .then((response) => setCatalog(response.items || []))
      .catch(() => undefined);
  }, []);
  useEffect(() => {
    // Move focus with the step so keyboard and screen-reader users land inside
    // the section that just appeared instead of tabbing out of the form.
    if (!stepChangedByUser.current) return;
    stepChangedByUser.current = false;
    stepHeadingRef.current?.focus();
    stepHeadingRef.current?.scrollIntoView?.({ block: "center", behavior: "smooth" });
  }, [step]);
  function setStep(next: number) {
    stepChangedByUser.current = true;
    setStepState(next);
  }
  const dynamicCities = useMemo<DestinationCity[]>(() => catalog.filter((item) => item.searchable).map((item) => ({
    id: item.id, country: item.country_code, name: item.city, airport: item.primary_gateway,
    airportName: item.gateway_codes.join("／"), summary: item.reason,
    recommendedStay: t("recommendedStay", { min: item.recommended_days.min, max: item.recommended_days.max }), areas: item.areas,
    tags: item.role === "secondary" ? [SECONDARY_TAG] : [], timezone: item.timezone, currency: item.currency,
  })), [catalog, t]);
  const availableCities = useMemo(
    () => (dynamicCities.length ? dynamicCities : destinations).filter((item) => countriesSelected.includes(item.country)),
    [countriesSelected, dynamicCities],
  );
  const selectedDestination = catalog.find((item) => item.primary_gateway === destinationCode);
  const availableExtensions = catalog.filter((item) => item.parent_destination_id === selectedDestination?.id);

  function toggleCountry(country: CountryKey) {
    setCountriesSelected((current) => current.includes(country) ? current.filter((item) => item !== country) : [...current, country]);
    setDestinationCode("");
    setSelectedExtensions([]);
  }
  function changeChildren(count: number) {
    setChildren(count); setChildAges((current) => Array.from({ length: count }, (_, index) => current[index] ?? 8));
  }
  function toggleInterest(code: string) {
    setSelectedInterests((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]);
  }
  function propertyTypes() {
    if (lodgingMode === "hotel") return ["hotel"];
    if (lodgingMode === "vacation_rental") return ["vacation_rental"];
    if (lodgingMode === "both") return ["hotel", "vacation_rental"];
    return [];
  }

  // The date and day-count rules used to fire only on the final submit, four
  // steps after the fields they complain about. Check them where they happen.
  function validateStepOne(form: HTMLFormElement | null): boolean {
    if (!form) return true;
    const data = new FormData(form);
    const startDate = String(data.get("window_start") || "");
    const endDate = String(data.get("window_end") || "");
    const minDays = Number(data.get("min_days") || 0);
    const maxDays = Number(data.get("max_days") || 0);
    if (!dateAny && (!startDate || !endDate || endDate <= startDate)) {
      setDateError(t("dateOrderError"));
      return false;
    }
    if (!lengthAny && (!minDays || !maxDays || maxDays < minDays)) {
      setDateError(t("dayOrderError"));
      return false;
    }
    setDateError(undefined);
    return true;
  }

  function goNext(form: HTMLFormElement | null) {
    if (step === 0 && !validateStepOne(form)) return;
    setStep(step + 1);
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    if (!validateStepOne(event.currentTarget)) { setStep(0); return; }
    const minDays = Number(form.get("min_days") || 0); const maxDays = Number(form.get("max_days") || 0);
    const startDate = String(form.get("window_start") || ""); const endDate = String(form.get("window_end") || "");
    const numberOrNull = (name: string) => { const value = Number(form.get(name) || 0); return value > 0 ? value : null; };
    setBusy(true); setError(undefined);
    try {
      const result = await api<DiscoveryResult>("/destinations/discover", { method: "POST", body: JSON.stringify({
        origin: String(form.get("origin") || "TPE"), destination_region: null,
        destination_countries: countriesSelected, destination_codes: destinationCode ? [destinationCode] : [],
        travel_window: dateAny ? null : { start_date: startDate, end_date: endDate },
        trip_length_range: lengthAny ? null : { min_days: minDays, max_days: maxDays },
        travelers: { adults: Number(form.get("adults") || 1), children, children_ages: childAges, rooms: Number(form.get("rooms") || 1) },
        budget_twd: numberOrNull("budget_twd"),
        lodging_preferences: { accepted_property_types: propertyTypes(), nightly_price_min_twd: numberOrNull("nightly_min"), nightly_price_max_twd: numberOrNull("nightly_max"), min_star_rating: numberOrNull("hotel_min_rating"), min_review_score: numberOrNull("min_review_score"), min_review_count: numberOrNull("min_review_count"), max_station_walk_minutes: numberOrNull("max_station_walk_minutes"), breakfast_required: form.get("breakfast_required") === "on" ? true : null, refundable_required: form.get("refundable_required") === "on" ? true : null },
        interests: selectedInterests, pace: String(form.get("pace") || "balanced"), notes: String(form.get("notes") || "") || null, top_n: 3,
      }) });
      setRecommendations(result.recommendations); setAssumptions(result.assumptions || []);
    } catch (reason) { setError((reason as Error).message); } finally { setBusy(false); }
  }

  function chooseRecommendation(item: Recommendation, form: HTMLFormElement) {
    const data = new FormData(form);
    const query = new URLSearchParams({ q: String(data.get("notes") || ""), country: item.country_code, origin: String(data.get("origin") || "TPE"), destination: item.airport, departure_date: item.departure_date, return_date: item.return_date, adults: String(data.get("adults") || "1"), children: String(children), children_ages: childAges.join(","), rooms: String(data.get("rooms") || "1"), interests: selectedInterests.join(","), pace: String(data.get("pace") || "balanced"), accepted_property_types: propertyTypes().join(","), preferred_areas: selectedAreas[item.candidate_id] || "", avoid_red_eye: String(data.get("avoid_red_eye") === "on"), breakfast_required: String(data.get("breakfast_required") === "on"), refundable_required: String(data.get("refundable_required") === "on"), include_airbnb: String(lodgingMode !== "hotel") });
    const recommendationProfile = catalog.find((profile) => profile.primary_gateway === item.airport);
    const validExtensions = selectedExtensions.filter((id) => catalog.find((profile) => profile.id === id)?.parent_destination_id === recommendationProfile?.id);
    if (validExtensions.length) query.set("extension_destination_ids", validExtensions.join(","));
    for (const [source, target] of [["budget_twd","budget_twd"],["nightly_min","hotel_min_nightly_twd"],["nightly_max","hotel_max_nightly_twd"],["hotel_min_rating","hotel_min_rating"],["min_review_score","hotel_min_review_score"],["min_review_count","hotel_min_review_count"],["max_station_walk_minutes","max_station_walk_minutes"]]) { const value = String(data.get(source) || ""); if (value) query.set(target, value); }
    router.push(`/search?${query.toString()}`);
  }

  return <form id="trip-search" onSubmit={submit} className="rounded-[2rem] border border-[var(--line)] bg-white p-5 shadow-[var(--shadow-lg)] md:p-7">
    <div className="mb-5"><p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />{t("eyebrow")}</p><h2 className="mt-1 text-2xl font-bold">{t("title")}</h2></div>
    {/* The pills wear a segmented-control look, so they must actually be
        buttons: completed steps reopen on tap, future steps stay disabled. */}
    <ol className="mb-6 grid grid-cols-5 gap-1" aria-label={t("stepsLabel")}>{stepKeys.map((key, index) => { const label = t(`steps.${key}`); return <li key={key}><button type="button" aria-current={index === step ? "step" : undefined} aria-label={index < step ? t("stepGoTo", { label }) : label} disabled={index > step} onClick={() => { if (index <= step) setStep(index); }} className={`min-h-11 w-full rounded-xl px-1 py-2 text-center text-xs font-semibold transition ${index === step ? "bg-[var(--teal)] text-white" : index < step ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "cursor-default bg-[var(--paper)] text-[var(--muted)]"}`}><span className="hidden sm:inline">{index + 1}. </span>{label}</button></li>; })}</ol>

    <section className={step === 0 ? "block" : "hidden"}><h3 ref={step === 0 ? stepHeadingRef : undefined} tabIndex={-1} className="flex items-center gap-2 text-lg font-bold outline-none"><CalendarDays size={19} />{t("datesTitle")}</h3><label className="mt-3 flex min-h-11 items-center gap-2.5 text-sm"><input type="checkbox" className="h-5 w-5 accent-[var(--teal)]" checked={dateAny} onChange={(event) => { setDateAny(event.target.checked); setDateError(undefined); }} />{t("dateAny")}</label><div className="mt-3 grid gap-3 sm:grid-cols-2"><label className="text-sm font-semibold">{t("earliestDeparture")}<input disabled={dateAny} aria-invalid={dateError ? true : undefined} onChange={() => setDateError(undefined)} name="window_start" type="date" defaultValue={futureDate(30)} min={futureDate(1)} className={fieldClass} /></label><label className="text-sm font-semibold">{t("latestReturn")}<input disabled={dateAny} aria-invalid={dateError ? true : undefined} onChange={() => setDateError(undefined)} name="window_end" type="date" defaultValue={futureDate(120)} min={futureDate(3)} className={fieldClass} /></label></div><label className="mt-4 flex min-h-11 items-center gap-2.5 text-sm"><input type="checkbox" className="h-5 w-5 accent-[var(--teal)]" checked={lengthAny} onChange={(event) => { setLengthAny(event.target.checked); setDateError(undefined); }} />{t("lengthAny")}</label><div className="mt-3 grid grid-cols-2 gap-3"><label className="text-sm font-semibold">{t("minDays")}<select disabled={lengthAny} onChange={() => setDateError(undefined)} name="min_days" defaultValue="4" className={fieldClass}>{Array.from({ length: 12 }, (_, index) => index + 2).map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">{t("maxDays")}<select disabled={lengthAny} onChange={() => setDateError(undefined)} name="max_days" defaultValue="6" className={fieldClass}>{Array.from({ length: 16 }, (_, index) => index + 2).map((value) => <option key={value}>{value}</option>)}</select></label></div>{dateError && <p role="alert" className="mt-3 rounded-xl bg-red-50 p-3 text-sm font-medium text-red-700">{dateError}</p>}</section>

    <section className={step === 1 ? "block" : "hidden"}><h3 ref={step === 1 ? stepHeadingRef : undefined} tabIndex={-1} className="flex items-center gap-2 text-lg font-bold outline-none"><MapPin size={19} />{t("destinationTitle")}</h3><p className="mt-1 text-sm text-[var(--muted)]">{t("destinationHint")}</p><div className="mt-4 grid grid-cols-3 gap-2">{countries.map((item) => <button key={item.key} type="button" aria-pressed={countriesSelected.includes(item.key)} onClick={() => toggleCountry(item.key)} className={optionClass(countriesSelected.includes(item.key))}><strong>{item.label}</strong><span className="mt-1 hidden text-xs sm:block">{item.caption}</span></button>)}</div><label className="mt-4 block text-sm font-semibold">{t("cityLabel")}<select aria-label={t("citySelect")} value={destinationCode} onChange={(event) => { setDestinationCode(event.target.value); setSelectedExtensions([]); }} className={fieldClass}><option value="">{t("cityAny")}</option><optgroup label={t("cityGroupPrimary")}>{availableCities.filter((city) => !city.tags.includes(SECONDARY_TAG)).map((city) => <option key={city.id} value={city.airport}>{city.name} · {city.airport}</option>)}</optgroup><optgroup label={t("cityGroupSecondary")}>{availableCities.filter((city) => city.tags.includes(SECONDARY_TAG)).map((city) => <option key={city.id} value={city.airport}>{city.name} · {city.airport}</option>)}</optgroup></select></label>{availableExtensions.length > 0 && <fieldset className="mt-4 rounded-2xl border border-violet-200 bg-violet-50 p-4"><legend className="px-1 text-sm font-semibold">{t("extensionsLegend")}</legend><div className="mt-2 flex flex-wrap gap-2">{availableExtensions.map((item) => <label key={item.id} className="flex min-h-11 items-center gap-2 rounded-xl bg-white px-3 py-2 text-sm"><input type="checkbox" className="h-5 w-5 accent-[var(--teal)]" checked={selectedExtensions.includes(item.id)} onChange={(event) => setSelectedExtensions((current) => event.target.checked ? [...current, item.id].slice(0, 2) : current.filter((id) => id !== item.id))} />{item.city}</label>)}</div></fieldset>}</section>

    <section className={step === 2 ? "block" : "hidden"}><h3 ref={step === 2 ? stepHeadingRef : undefined} tabIndex={-1} className="flex items-center gap-2 text-lg font-bold outline-none"><Users size={19} />{t("partyTitle")}</h3><div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4"><label className="text-sm font-semibold">{t("origin")}<select name="origin" defaultValue="TPE" className={fieldClass}><option value="TPE">{t("originTpe")}</option><option value="TSA">{t("originTsa")}</option><option value="KHH">{t("originKhh")}</option></select></label><label className="text-sm font-semibold">{t("adults")}<select name="adults" defaultValue="2" className={fieldClass}>{[1,2,3,4,5,6,7,8,9].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">{t("childrenLabel")}<select aria-label={t("childrenCount")} value={children} onChange={(event) => changeChildren(Number(event.target.value))} className={fieldClass}>{[0,1,2,3,4].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">{t("rooms")}<select name="rooms" defaultValue="1" className={fieldClass}>{[1,2,3,4].map((value) => <option key={value}>{value}</option>)}</select></label></div>{children > 0 && <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">{childAges.map((age, index) => <label key={index} className="text-sm font-semibold">{t("childAge", { index: index + 1 })}<select aria-label={t("childAge", { index: index + 1 })} value={age} onChange={(event) => setChildAges((current) => current.map((item, childIndex) => childIndex === index ? Number(event.target.value) : item))} className={fieldClass}>{Array.from({ length: 18 }, (_, value) => <option key={value} value={value}>{t("ageYears", { age: value })}</option>)}</select></label>)}</div>}<label className="mt-4 block text-sm font-semibold">{t("budget")}<input name="budget_twd" type="number" min="1" placeholder={t("anyPlaceholder")} className={fieldClass} /></label></section>

    <section className={step === 3 ? "block" : "hidden"}><h3 ref={step === 3 ? stepHeadingRef : undefined} tabIndex={-1} className="flex items-center gap-2 text-lg font-bold outline-none"><Hotel size={19} />{t("lodgingTitle")}</h3><div className="mt-4 grid grid-cols-2 gap-2">{([["hotel", t("lodgingHotel")], ["vacation_rental", t("lodgingRental")], ["both", t("lodgingBoth")], ["any", t("lodgingAny")]] as const).map(([value, label]) => <button key={value} type="button" aria-pressed={lodgingMode === value} onClick={() => setLodgingMode(value)} className={optionClass(lodgingMode === value)}>{label}</button>)}</div><div className="mt-4 grid grid-cols-2 gap-3"><label className="text-sm font-semibold">{t("nightlyMin")}<input name="nightly_min" type="number" min="0" placeholder={t("anyPlaceholder")} className={fieldClass} /></label><label className="text-sm font-semibold">{t("nightlyMax")}<input name="nightly_max" type="number" min="1" placeholder={t("anyPlaceholder")} className={fieldClass} /></label><label className="text-sm font-semibold">{t("minRating")}<select name="hotel_min_rating" className={fieldClass}><option value="">{t("anyPlaceholder")}</option>{[3,4,5].map((value) => <option key={value} value={value}>{t("ratingOption", { stars: value })}</option>)}</select></label><label className="text-sm font-semibold">{t("stationWalk")}<select name="max_station_walk_minutes" className={fieldClass}><option value="">{t("anyPlaceholder")}</option>{[5,10,15,20].map((value) => <option key={value} value={value}>{t("walkOption", { minutes: value })}</option>)}</select></label><label className="text-sm font-semibold">{t("minReviewScore")}<select name="min_review_score" className={fieldClass}><option value="">{t("anyPlaceholder")}</option><option value="7">7.0+</option><option value="8">8.0+</option><option value="9">9.0+</option></select></label><label className="text-sm font-semibold">{t("minReviewCount")}<select name="min_review_count" className={fieldClass}><option value="">{t("anyPlaceholder")}</option>{[20,50,100,300].map((value) => <option key={value} value={value}>{t("reviewCountOption", { count: value })}</option>)}</select></label></div><div className="mt-4 grid gap-2 text-sm sm:grid-cols-2"><label className="flex min-h-12 items-center gap-2.5 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" name="breakfast_required" className="h-5 w-5 accent-[var(--teal)]" />{t("breakfast")}</label><label className="flex min-h-12 items-center gap-2.5 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" name="refundable_required" className="h-5 w-5 accent-[var(--teal)]" />{t("refundable")}</label></div></section>

    <section className={step === 4 ? "block" : "hidden"}><h3 ref={step === 4 ? stepHeadingRef : undefined} tabIndex={-1} className="flex items-center gap-2 text-lg font-bold outline-none"><Sparkles size={19} />{t("preferencesTitle")}</h3><div className="mt-4 flex flex-wrap gap-2">{interests.map((interest) => <button key={interest.code} type="button" aria-pressed={selectedInterests.includes(interest.code)} onClick={() => toggleInterest(interest.code)} className={optionClass(selectedInterests.includes(interest.code))}>{interest.label}</button>)}</div><div className="mt-4 grid gap-3 sm:grid-cols-2"><label className="text-sm font-semibold">{t("pace")}<select name="pace" defaultValue="balanced" className={fieldClass}><option value="relaxed">{t("paceRelaxed")}</option><option value="balanced">{t("paceBalanced")}</option><option value="packed">{t("pacePacked")}</option></select></label><label className="mt-7 flex min-h-12 items-center gap-2.5 rounded-xl bg-[var(--paper)] p-3 text-sm"><input type="checkbox" name="avoid_red_eye" defaultChecked className="h-5 w-5 accent-[var(--teal)]" />{t("avoidRedEye")}</label></div><label className="mt-4 block text-sm font-semibold">{t("notes")}<textarea name="notes" rows={3} placeholder={t("notesPlaceholder")} className={fieldClass} /></label></section>

    {error && <p role="alert" className="mt-4 rounded-xl bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>}
    <div className="mt-5 flex gap-3">{step > 0 && <button type="button" onClick={() => setStep(step - 1)} className="flex min-h-12 flex-1 items-center justify-center gap-1 rounded-xl border border-[var(--line)] px-4 py-3 font-semibold sm:flex-none">{<ChevronLeft size={18} />}{t("back")}</button>}{step < stepKeys.length - 1 ? <button type="button" onClick={(event) => goNext(event.currentTarget.form)} className="ml-auto flex min-h-12 flex-[2] items-center justify-center gap-1 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white sm:flex-none">{t("next")}<ChevronRight size={18} /></button> : <button disabled={busy} className="ml-auto flex min-h-12 flex-[2] items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white disabled:opacity-60 sm:flex-none">{busy ? <LoaderCircle className="animate-spin" size={18} /> : <Sparkles size={18} />}{t("submit")}</button>}</div>

    {recommendations.length > 0 && <section aria-labelledby="recommendations-title" className="mt-7 border-t border-[var(--line)] pt-6"><h3 id="recommendations-title" className="text-xl font-bold">{t("recommendationsTitle")}</h3><p className="mt-1 text-sm text-[var(--muted)]">{t("recommendationsHint")}</p><div className="mt-4 grid gap-4">{recommendations.map((item, index) => <article key={item.candidate_id} className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4"><div className="flex items-start justify-between gap-3"><div><p className="text-xs font-semibold text-[var(--teal)]">{index === 0 ? t("bestPick") : t("candidateN", { rank: index + 1 })} · {t("matchScore", { score: item.score })}</p><h4 className="mt-1 text-xl font-bold">{item.country}・{item.city}</h4><p className="mt-1 text-sm text-[var(--muted)]">{t("tripDates", { from: item.departure_date, to: item.return_date, days: item.trip_length_days })}</p></div><strong className="text-right text-lg">{t("approx", { amount: twd.format(item.estimated_total_twd) })}</strong></div><p className="mt-3 text-sm leading-6">{item.reason}</p><div className="mt-3 flex flex-wrap gap-2 text-xs"><span className="rounded-full bg-white px-2.5 py-1">{t("flightEstimate", { amount: twd.format(item.estimated_flight_twd) })}</span><span className="rounded-full bg-white px-2.5 py-1">{t("lodgingEstimate", { amount: twd.format(item.estimated_lodging_twd) })}</span>{item.matched_interests.map((interest) => <span key={interest} className="rounded-full bg-[var(--teal-soft)] px-2.5 py-1">{t("matchesInterest", { interest: interestLabel(interest) })}</span>)}</div>{item.relaxed_preferences.length > 0 && <p className="mt-3 text-xs text-amber-800">{t("needsConfirm", { items: item.relaxed_preferences.join("、") })}</p>}<label className="mt-3 block text-sm font-semibold">{t("preferredArea")}<select value={selectedAreas[item.candidate_id] || ""} onChange={(event) => setSelectedAreas((current) => ({ ...current, [item.candidate_id]: event.target.value }))} className={fieldClass}><option value="">{t("anyPlaceholder")}</option>{item.areas.map((area) => <option key={area}>{area}</option>)}</select></label><button type="button" onClick={(event) => chooseRecommendation(item, event.currentTarget.form!)} className="mt-4 flex min-h-12 w-full items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-4 py-3 font-semibold text-white"><Check size={18} />{t("useThis")}</button></article>)}</div>{assumptions.map((item) => <p key={item} className="mt-2 text-xs text-[var(--muted)]">・{item}</p>)}</section>}
    <p className="mt-4 text-center text-xs leading-5 text-[var(--muted)]">{t("disclaimer")}</p>
  </form>;
}
