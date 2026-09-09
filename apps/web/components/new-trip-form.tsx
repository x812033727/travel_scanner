"use client";

import { ArrowRight, CalendarDays, ChevronDown, MapPinned, SlidersHorizontal, Users } from "lucide-react";
import { useRouter } from "@/i18n/navigation";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useMemo, useRef, useState } from "react";
import { DateRangePicker } from "@/components/date-range-picker";
import { automaticTripName, newTripCopy } from "@/components/planner/new-trip-copy";
import {
  NewTripPreferenceFields, NewTripTravelerFields, newTripFieldClass,
  newTripPreferenceError, newTripPreferencesPayload, validNewTripTravelers,
  type NewTripLodgingMode, type NewTripPreferenceValues, type NewTripTravelerValues,
} from "@/components/planner/new-trip-fields";
import { api } from "@/lib/api";
import { dayCount, formatTripDay } from "@/lib/calendar";
import { interestCodes, localizeDestinations, shopThemeCodes } from "@/lib/destinations";
import { holidayCountriesFor } from "@/lib/holidays";

type CreatedTrip = { id: string };
const lodgingModes = ["hotel", "vacation_rental", "both", "any"] as const;
const paces = ["relaxed", "balanced", "packed"] as const;
const routePreferences = ["FEWER_TRANSFERS", "FASTEST", "LESS_WALKING"] as const;
const MAX_TRIP_DAYS = 61;
const DRAFT_STORAGE_KEY = "mokaair-new-trip-draft";
const fieldClass = newTripFieldClass;

type FormValues = NewTripTravelerValues & NewTripPreferenceValues & {
  name: string; destination_name: string; destination_place_id: string; destination_catalog_id: string;
  start_date: string; end_date: string; notes: string;
};
type DraftSnapshot = {
  // Retain legacy fields so older drafts can be restored, but never restore AI mode.
  step?: number; planningMode?: string; nameEdited?: boolean;
  lodgingMode: NewTripLodgingMode; selectedInterests: string[]; selectedShopThemes: string[];
  form: Record<string, string | boolean>;
};
function oneOf<T extends string>(values: readonly T[], value: unknown): value is T {
  return typeof value === "string" && (values as readonly string[]).includes(value);
}
function validDay(value: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(value + "T00:00:00Z");
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}
function readDraft(): DraftSnapshot | undefined {
  try {
    const raw = window.sessionStorage.getItem(DRAFT_STORAGE_KEY);
    const parsed: unknown = raw ? JSON.parse(raw) : undefined;
    return parsed && typeof parsed === "object" ? parsed as DraftSnapshot : undefined;
  } catch { return undefined; }
}
function clearDraft() {
  try { window.sessionStorage.removeItem(DRAFT_STORAGE_KEY); } catch { /* Storage is best-effort. */ }
}

export function NewTripForm() {
  const router = useRouter();
  const locale = useLocale();
  const t = useTranslations("newTrip");
  const catalog = useTranslations("search.catalog");
  const copy = newTripCopy(locale);
  const cities = useMemo(() => localizeDestinations(catalog), [catalog]);
  const today = useMemo(() => new Date().toLocaleDateString("sv"), []);
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const [error, setError] = useState<{ message: string; id: number }>();
  const errorId = useRef(0);
  const errorRef = useRef<HTMLParagraphElement>(null);
  const submitKey = useRef<string | undefined>(undefined);
  const submitted = useRef(false);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const [advancedOpen, setAdvancedOpen] = useState(false);
  const [nameEdited, setNameEdited] = useState(false);
  const [lodgingMode, setLodgingMode] = useState<NewTripLodgingMode>("any");
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [selectedShopThemes, setSelectedShopThemes] = useState<string[]>([]);
  const [form, setForm] = useState<FormValues>({
    name: "", destination_name: "", destination_place_id: "", destination_catalog_id: "", start_date: "", end_date: "",
    adults: "2", children: "0", rooms: "1", budget_twd: "", pace: "balanced", route_preference: "FEWER_TRANSFERS",
    nightly_min: "", nightly_max: "", hotel_min_rating: "", preferred_area: "", max_station_walk_minutes: "",
    min_review_score: "", min_review_count: "", breakfast_required: false, refundable_required: false, avoid_red_eye: true, notes: "",
  });
  const [draftReady, setDraftReady] = useState(false);
  const selectedCity = cities.find((city) => city.id === form.destination_catalog_id);
  const destinationName = selectedCity?.name ?? form.destination_name.trim();
  const count = dayCount(form.start_date, form.end_date);
  const days = Number.isFinite(count) ? count : 0;
  const automaticName = automaticTripName(locale, destinationName, days);
  const tripName = (nameEdited ? form.name.trim() : "") || automaticName;
  const holidayMarkets = holidayCountriesFor(destinationName, locale, cities);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const draft = readDraft();
      if (draft) {
        if (oneOf(lodgingModes, draft.lodgingMode)) setLodgingMode(draft.lodgingMode);
        if (Array.isArray(draft.selectedInterests)) setSelectedInterests(draft.selectedInterests.filter((code) => (interestCodes as readonly string[]).includes(code)));
        if (Array.isArray(draft.selectedShopThemes)) setSelectedShopThemes(draft.selectedShopThemes.filter((code) => (shopThemeCodes as readonly string[]).includes(code)));
        const saved = draft.form && typeof draft.form === "object" ? draft.form : {};
        const start = typeof saved.start_date === "string" ? saved.start_date : "";
        const end = typeof saved.end_date === "string" ? saved.end_date : "";
        const datesValid = validDay(start) && validDay(end) && start >= today && end >= start && dayCount(start, end) <= MAX_TRIP_DAYS;
        setForm((current) => {
          const next = { ...current };
          for (const key of Object.keys(current) as (keyof FormValues)[]) {
            const value = saved[key];
            if (typeof value !== typeof current[key]) continue;
            if (key === "pace" && !oneOf(paces, value)) continue;
            if (key === "route_preference" && !oneOf(routePreferences, value)) continue;
            (next as Record<string, string | boolean>)[key] = value;
          }
          if (!datesValid) { next.start_date = ""; next.end_date = ""; }
          return next;
        });
        setNameEdited(typeof draft.nameEdited === "boolean" ? draft.nameEdited : Boolean(typeof saved.name === "string" && saved.name.trim()));
      }
      setDraftReady(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, [today]);

  useEffect(() => {
    if (!draftReady || submitted.current) return;
    try {
      window.sessionStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify({
        step: 0, planningMode: "manual_blank", nameEdited, lodgingMode,
        selectedInterests, selectedShopThemes, form,
      } satisfies DraftSnapshot));
    } catch { /* Storage is best-effort. */ }
  }, [draftReady, form, nameEdited, lodgingMode, selectedInterests, selectedShopThemes]);

  useEffect(() => { if (error) errorRef.current?.focus(); }, [error]);

  function update<K extends keyof FormValues>(key: K, value: FormValues[K]) {
    setError(undefined);
    setForm((current) => ({ ...current, [key]: value }));
  }
  function updatePreference<K extends keyof NewTripPreferenceValues>(key: K, value: NewTripPreferenceValues[K]) {
    setError(undefined);
    setForm((current) => ({ ...current, [key]: value }));
  }
  function chooseDestination(value: string) {
    setError(undefined);
    const city = cities.find((entry) => entry.name.toLowerCase() === value.trim().toLowerCase() || entry.id === value.trim().toLowerCase());
    // A catalog id is not a provider Place ID. Never fabricate geocoding data.
    setForm((current) => ({ ...current, destination_name: value, destination_catalog_id: city?.id ?? "", destination_place_id: "" }));
  }
  function chooseDates(range: { start: string; end: string }) {
    setError(undefined);
    setForm((current) => ({ ...current, start_date: range.start, end_date: range.end }));
  }
  function showError(message: string) {
    errorId.current += 1;
    setError({ message, id: errorId.current });
  }
  function toggleInterest(code: string) {
    setError(undefined);
    setSelectedInterests((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]);
    if (code === "shopping" && selectedInterests.includes(code)) setSelectedShopThemes([]);
  }
  function toggleShopTheme(code: string) {
    setError(undefined);
    setSelectedShopThemes((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]);
  }
  function validate() {
    if (!destinationName) return t("errors.destinationRequired");
    if (!validDay(form.start_date) || !validDay(form.end_date)) return t("errors.datesRequired");
    if (form.start_date < today) return t("errors.startInPast");
    if (form.end_date < form.start_date) return t("errors.endBeforeStart");
    if (days > MAX_TRIP_DAYS) return t("errors.tooLong");
    if (!validNewTripTravelers(form)) return copy.invalidTravelers;
    if (Number(form.rooms) > Number(form.adults) + Number(form.children)) return t("errors.roomsExceedTravelers");
    const preferenceError = newTripPreferenceError(form);
    if (preferenceError) {
      setAdvancedOpen(true);
      return preferenceError === "invalidNumbers" ? copy.invalidNumbers : t("errors." + preferenceError);
    }
  }
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busyRef.current) return;
    const message = validate();
    if (message) { showError(message); return; }
    busyRef.current = true;
    setBusy(true);
    setError(undefined);
    // Keep the key on a failed/uncertain request so retry cannot create another trip.
    if (!submitKey.current) submitKey.current = crypto.randomUUID();
    try {
      const trip = await api<CreatedTrip>("/trips", {
        method: "POST", headers: { "Idempotency-Key": submitKey.current },
        body: JSON.stringify({
          source: "blank", planning_mode: "manual_blank", name: tripName,
          destination_name: destinationName, destination_place_id: form.destination_place_id || null,
          start_date: form.start_date, end_date: form.end_date, route_preference: form.route_preference,
          routing: { auto_compute: false, default_travel_mode: "transit", default_buffer_minutes: 10 },
          travelers: { adults: Number(form.adults), children: Number(form.children), rooms: Number(form.rooms) },
          preferences: newTripPreferencesPayload(form, lodgingMode, selectedInterests, selectedShopThemes),
          notes: form.notes.trim() || null,
        }),
      });
      submitted.current = true;
      clearDraft();
      submitKey.current = undefined;
      router.push("/trips/" + trip.id);
    } catch (reason) {
      showError(reason instanceof Error ? reason.message : t("errors.createFailed"));
    } finally { busyRef.current = false; setBusy(false); }
  }

  return <form noValidate aria-busy={busy} onSubmit={submit} className="premium-new-trip">
    <header className="premium-new-trip-heading mb-6">
      <p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p>
      <h1 className="mt-2 text-3xl font-bold">{copy.title}</h1>
      <p className="mt-3 text-[var(--muted)]">{copy.subtitle}</p>
    </header>
    <section className="premium-new-trip-card rounded-[2rem] border border-[var(--line)] bg-[var(--surface)] p-6 md:p-8">
      <fieldset disabled={busy} className="min-w-0">
        <div className="premium-new-trip-basics grid gap-5 md:grid-cols-2">
          <div>
            <label htmlFor="trip-destination" className="flex items-center gap-2 text-sm font-semibold"><MapPinned size={18} />{t("basics.destination")}</label>
            <input id="trip-destination" list="premium-new-trip-city-list" aria-describedby="trip-destination-help" value={selectedCity?.name ?? form.destination_name} maxLength={255} onChange={(event) => chooseDestination(event.target.value)} placeholder={t("basics.destinationPlaceholder")} className={fieldClass} />
            <datalist id="premium-new-trip-city-list">{cities.map((city) => <option key={city.id} value={city.name} />)}</datalist>
            <p id="trip-destination-help" className="mt-2 text-xs text-[var(--muted)]">{copy.cityHelp}</p>
            <div className="premium-new-trip-cities mt-3 flex flex-wrap gap-2">{cities.filter((city) => ["tokyo", "osaka-kyoto", "seoul", "bangkok"].includes(city.id)).map((city) => <button key={city.id} type="button" aria-pressed={selectedCity?.id === city.id} onClick={() => chooseDestination(city.name)} className="rounded-full border border-[var(--line)] px-3 py-2 text-xs hover:border-[var(--teal)]">{city.name}</button>)}</div>
          </div>
          <fieldset className="min-w-0">
            <legend className="text-sm font-semibold">{t("basics.datesLegend")}</legend>
            <button type="button" aria-expanded={calendarOpen} aria-controls="premium-new-trip-calendar" onClick={() => setCalendarOpen((open) => !open)} className="premium-new-trip-date-summary mt-2 flex min-h-12 w-full items-center gap-3 rounded-xl border border-[var(--line)] p-4 text-left">
              <CalendarDays size={20} className="shrink-0" /><span className="min-w-0 flex-1">{form.start_date && form.end_date ? formatTripDay(locale, form.start_date) + " → " + formatTripDay(locale, form.end_date) : copy.datePrompt}{days > 0 && <strong className="mt-1 block text-sm text-[var(--teal)]">{t("summary.days", { days })}</strong>}</span><ChevronDown size={16} className="shrink-0" />
            </button>
          </fieldset>
        </div>
        <div id="premium-new-trip-calendar" hidden={!calendarOpen} className="premium-new-trip-calendar mt-5">
          {calendarOpen && <><p className="mb-3 text-xs text-[var(--muted)]">{t("basics.datesHelp", { maxDays: MAX_TRIP_DAYS })}</p><DateRangePicker start={form.start_date} end={form.end_date} today={today} maxDays={MAX_TRIP_DAYS} countries={holidayMarkets} onChange={chooseDates} /><button type="button" onClick={() => setCalendarOpen(false)} className="mt-3 rounded-lg border border-[var(--line)] px-4 py-2 text-sm font-semibold">{copy.closeCalendar}</button></>}
        </div>
        <div className="premium-new-trip-name mt-6">
          <label htmlFor="trip-name" className="text-sm font-semibold">{t("basics.name")}</label>
          <input id="trip-name" maxLength={255} value={nameEdited ? form.name : automaticName} onChange={(event) => { setNameEdited(true); update("name", event.target.value); }} aria-describedby="trip-name-help" className={fieldClass} />
          <div className="mt-2 flex flex-wrap items-center justify-between gap-2"><p id="trip-name-help" className="text-xs text-[var(--muted)]">{copy.nameHelp}</p>{nameEdited && <button type="button" onClick={() => { setNameEdited(false); update("name", ""); }} className="text-xs font-semibold text-[var(--teal)]">{copy.autoName}</button>}</div>
        </div>
        <section className="premium-new-trip-travelers mt-6">
          <h2 className="flex items-center gap-2 text-lg font-bold"><Users size={18} />{t("travelers.title")}</h2>
          <p className="mb-3 mt-1 text-xs text-[var(--muted)]">{copy.travelersHelp}</p>
          <NewTripTravelerFields values={form} onChange={update} />
        </section>
        <details open={advancedOpen} onToggle={(event) => setAdvancedOpen(event.currentTarget.open)} className="premium-new-trip-advanced mt-6 border-t border-[var(--line)] pt-5">
          <summary className="cursor-pointer text-sm font-semibold"><SlidersHorizontal size={16} className="mr-2 inline-block" />{copy.advanced}</summary>
          <div className="mt-5"><NewTripPreferenceFields values={form} onChange={updatePreference} lodgingMode={lodgingMode} onLodgingModeChange={(value) => { setError(undefined); setLodgingMode(value); }} interests={selectedInterests} onToggleInterest={toggleInterest} shopThemes={selectedShopThemes} onToggleShopTheme={toggleShopTheme} />
            <label className="mt-5 block text-sm font-semibold">{t("review.notes")}<textarea rows={3} maxLength={1000} value={form.notes} onChange={(event) => update("notes", event.target.value)} placeholder={t("review.notesPlaceholder")} className={fieldClass} /></label>
          </div>
        </details>
      </fieldset>
      {error && <p ref={errorRef} tabIndex={-1} role="alert" className="mt-5 rounded-xl bg-red-50 p-4 text-sm text-red-800 outline-none">{error.message}</p>}
      <footer className="premium-new-trip-footer mt-6 flex flex-wrap items-center justify-between gap-4 border-t border-[var(--line)] pt-5">
        <p className="max-w-md text-xs leading-5 text-[var(--muted)]">{copy.notice}</p>
        <button type="submit" disabled={busy} className="premium-new-trip-submit flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-6 py-3 font-semibold text-white disabled:opacity-60">{busy ? copy.creating : copy.submit}<ArrowRight size={18} /></button>
      </footer>
    </section>
  </form>;
}
