"use client";

import { ArrowRight, CalendarDays, ChevronDown, MapPinned, SlidersHorizontal, Users } from "lucide-react";
import { useRouter } from "@/i18n/navigation";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useMemo, useRef, useState } from "react";
import { DateRangePicker } from "@/components/date-range-picker";
import { useHeaderSession } from "@/components/header-session";
import { automaticTripName, newTripCopy } from "@/components/planner/new-trip-copy";
import {
  NewTripPreferenceFields, NewTripTravelerFields, newTripFieldClass,
  newTripPreferenceError, newTripPreferencesPayload, validNewTripTravelers,
  type NewTripLodgingMode, type NewTripPreferenceValues, type NewTripTravelerValues,
} from "@/components/planner/new-trip-fields";
import { ApiError, api } from "@/lib/api";
import { dayCount, formatTripDay } from "@/lib/calendar";
import { interestCodes, localizeDestinations, shopThemeCodes } from "@/lib/destinations";
import { holidayCountriesFor } from "@/lib/holidays";
import { completedTripDestination } from "@/lib/frontend-flow";

type CreatedTrip = { id: string };
const lodgingModes = ["hotel", "vacation_rental", "both", "any"] as const;
const paces = ["relaxed", "balanced", "packed"] as const;
const routePreferences = ["FEWER_TRANSFERS", "FASTEST", "LESS_WALKING"] as const;
const MAX_TRIP_DAYS = 61;
const DRAFT_STORAGE_KEY = "mokaair-new-trip-draft";
// Stay inside the server's 24-hour cache window even with a slow connection.
const REPLAY_WINDOW_MS = 23 * 60 * 60 * 1000;
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
  pending?: CreationAttempt;
};
type CreationAttempt = { key: string; body: string; startedAt: number };
function creationAttempt(body: string): CreationAttempt {
  return { key: crypto.randomUUID(), startedAt: Date.now(), body };
}
function attemptExpired(attempt: CreationAttempt) {
  return Date.now() - attempt.startedAt >= REPLAY_WINDOW_MS;
}
function validAttempt(value: unknown): value is CreationAttempt {
  if (!value || typeof value !== "object") return false;
  const attempt = value as Partial<CreationAttempt>;
  if (typeof attempt.key !== "string" || !/^[0-9a-f-]{36}$/i.test(attempt.key)
    || typeof attempt.body !== "string" || typeof attempt.startedAt !== "number"
    || !Number.isFinite(attempt.startedAt) || attempt.startedAt > Date.now()) return false;
  try {
    const payload = JSON.parse(attempt.body);
    return payload.source === "blank" && payload.planning_mode === "manual_blank";
  } catch { return false; }
}
function oneOf<T extends string>(values: readonly T[], value: unknown): value is T {
  return typeof value === "string" && (values as readonly string[]).includes(value);
}
function validDay(value: string) {
  if (!/^\d{4}-\d{2}-\d{2}$/.test(value)) return false;
  const date = new Date(value + "T00:00:00Z");
  return Number.isFinite(date.getTime()) && date.toISOString().slice(0, 10) === value;
}
function readDraft(storageKey: string): DraftSnapshot | undefined {
  try {
    const raw = window.sessionStorage.getItem(storageKey);
    const parsed: unknown = raw ? JSON.parse(raw) : undefined;
    return parsed && typeof parsed === "object" ? parsed as DraftSnapshot : undefined;
  } catch { return undefined; }
}
function clearDraft(storageKey: string) {
  try { window.sessionStorage.removeItem(storageKey); } catch { /* Storage is best-effort. */ }
}

export function NewTripForm({ resumePlanning = false }: { resumePlanning?: boolean }) {
  const { status, user } = useHeaderSession();
  const locale = useLocale();
  const copy = newTripCopy(locale);
  if (status !== "authenticated" || !user) return <div role="status" className="premium-new-trip-card p-6">
    {status === "loading" ? copy.sessionLoading : status === "unavailable" ? copy.sessionUnavailable : copy.signInRequired}
    {status === "signed_out" && <a className="mt-3 block min-h-11 text-[var(--teal)]" href={`/${locale}/login?next=${encodeURIComponent(`/${locale}/trips/new${resumePlanning ? "?resume_plan=1" : ""}`)}`}>{copy.signIn}</a>}
  </div>;
  // Account changes must not restore another member's draft or deliver their
  // pending response to the new session. The global provider is the only auth read.
  return <NewTripFormForAccount key={user.id} accountId={user.id} />;
}

function NewTripFormForAccount({ accountId }: { accountId: string }) {
  const router = useRouter();
  const locale = useLocale();
  const t = useTranslations("newTrip");
  const catalog = useTranslations("search.catalog");
  const copy = newTripCopy(locale);
  const cities = useMemo(() => localizeDestinations(catalog), [catalog]);
  const today = useMemo(() => new Date().toLocaleDateString("sv"), []);
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const storageKey = `${DRAFT_STORAGE_KEY}:${accountId}`;
  const [error, setError] = useState<{ message: string; id: number; field?: "dates" }>();
  const errorId = useRef(0);
  const errorRef = useRef<HTMLParagraphElement>(null);
  const [pending, setPending] = useState<CreationAttempt>();
  const [recoveryBlocked, setRecoveryBlocked] = useState(false);
  const [expired, setExpired] = useState(false);
  const active = useRef(true);
  const submitted = useRef(false);
  const [calendarOpen, setCalendarOpen] = useState(false);
  const calendarButton = useRef<HTMLButtonElement>(null);
  const [travelersOpen, setTravelersOpen] = useState(false);
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

  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  useEffect(() => {
    if (!pending) return;
    const remaining = pending.startedAt + REPLAY_WINDOW_MS - Date.now();
    const timer = window.setTimeout(() => setExpired(true), Math.max(0, remaining));
    return () => window.clearTimeout(timer);
  }, [pending]);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const draft = readDraft(storageKey);
      if (draft) {
        if (draft.pending !== undefined) {
          if (validAttempt(draft.pending)) {
            setPending(draft.pending);
            setExpired(Date.now() - draft.pending.startedAt >= REPLAY_WINDOW_MS);
          } else setRecoveryBlocked(true);
        }
        if (oneOf(lodgingModes, draft.lodgingMode)) setLodgingMode(draft.lodgingMode);
        if (Array.isArray(draft.selectedInterests)) setSelectedInterests(draft.selectedInterests.filter((code) => (interestCodes as readonly string[]).includes(code)));
        if (Array.isArray(draft.selectedShopThemes)) setSelectedShopThemes(draft.selectedShopThemes.filter((code) => (shopThemeCodes as readonly string[]).includes(code)));
        const saved = draft.form && typeof draft.form === "object" ? draft.form : {};
        const start = typeof saved.start_date === "string" ? saved.start_date : "";
        const end = typeof saved.end_date === "string" ? saved.end_date : "";
        const datesValid = validDay(start) && validDay(end) && (start >= today || validAttempt(draft.pending)) && end >= start && dayCount(start, end) <= MAX_TRIP_DAYS;
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
  }, [today, storageKey]);

  useEffect(() => {
    if (!draftReady || submitted.current || pending || recoveryBlocked) return;
    try {
      window.sessionStorage.setItem(storageKey, JSON.stringify({
        step: 0, planningMode: "manual_blank", nameEdited, lodgingMode,
        selectedInterests, selectedShopThemes, form,
      } satisfies DraftSnapshot));
    } catch { /* Storage is best-effort. */ }
  }, [draftReady, form, nameEdited, lodgingMode, selectedInterests, selectedShopThemes, storageKey, pending, recoveryBlocked]);

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
    if (range.start && range.end) {
      setCalendarOpen(false);
      calendarButton.current?.focus();
    }
  }
  function showError(message: string, field?: "dates") {
    errorId.current += 1;
    setError({ message, id: errorId.current, field });
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
    if (!validDay(form.start_date) || !validDay(form.end_date)) return { message: t("errors.datesRequired"), field: "dates" as const };
    if (form.start_date < today) return { message: t("errors.startInPast"), field: "dates" as const };
    if (form.end_date < form.start_date) return { message: t("errors.endBeforeStart"), field: "dates" as const };
    if (days > MAX_TRIP_DAYS) return { message: t("errors.tooLong"), field: "dates" as const };
    if (!validNewTripTravelers(form)) { setTravelersOpen(true); return copy.invalidTravelers; }
    if (Number(form.rooms) > Number(form.adults) + Number(form.children)) { setTravelersOpen(true); return t("errors.roomsExceedTravelers"); }
    const preferenceError = newTripPreferenceError(form);
    if (preferenceError) {
      setAdvancedOpen(true);
      return preferenceError === "invalidNumbers" ? copy.invalidNumbers : t("errors." + preferenceError);
    }
  }
  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busyRef.current || !draftReady || recoveryBlocked) return;
    if (pending && attemptExpired(pending)) { setExpired(true); return; }
    const invalid = pending ? undefined : validate();
    if (invalid) {
      if (typeof invalid === "string") showError(invalid);
      else showError(invalid.message, invalid.field);
      return;
    }
    busyRef.current = true;
    setBusy(true);
    setError(undefined);
    let attempt = pending;
    try {
      if (!attempt) {
        attempt = creationAttempt(JSON.stringify({
          source: "blank", planning_mode: "manual_blank", name: tripName,
          destination_name: destinationName, destination_place_id: form.destination_place_id || null,
          start_date: form.start_date, end_date: form.end_date, route_preference: form.route_preference,
          routing: { auto_compute: false, default_travel_mode: "transit", default_buffer_minutes: 10 },
          travelers: { adults: Number(form.adults), children: Number(form.children), rooms: Number(form.rooms) },
          preferences: newTripPreferencesPayload(form, lodgingMode, selectedInterests, selectedShopThemes),
          notes: form.notes.trim() || null,
        }));
        // Persist before sending: refresh/timeout retries the exact same bytes.
        // If storage is unavailable, no POST is sent that we cannot recover.
        try {
          window.sessionStorage.setItem(storageKey, JSON.stringify({
            nameEdited, lodgingMode, selectedInterests, selectedShopThemes, form, pending: attempt,
          } satisfies DraftSnapshot));
        } catch { throw new Error(copy.storageUnavailable); }
        setPending(attempt);
      }
      const trip = await api<CreatedTrip>("/trips", {
        method: "POST", headers: { "Idempotency-Key": attempt.key }, body: attempt.body,
      });
      if (!active.current) return;
      submitted.current = true;
      clearDraft(storageKey);
      router.push(completedTripDestination(accountId, trip.id, new URLSearchParams(window.location.search).get("resume_plan") === "1"));
    } catch (reason) {
      if (!active.current) return;
      // Only a definitive rejection can unlock editing and retire the old key.
      if (!pending && reason instanceof ApiError && [400, 401, 403, 422, 429].includes(reason.status)) {
        setPending(undefined);
        clearDraft(storageKey);
      }
      if (reason instanceof ApiError && reason.status === 409) setRecoveryBlocked(true);
      showError(reason instanceof ApiError && reason.code?.startsWith("trip_create_")
        ? copy.recoveryExpired : reason instanceof Error ? reason.message : t("errors.createFailed"));
    } finally { busyRef.current = false; setBusy(false); }
  }

  return <form noValidate aria-busy={busy} onSubmit={submit} className="premium-new-trip">
    <header className="premium-new-trip-heading mb-6">
      <p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p>
      <h1 className="mt-2 text-3xl font-bold">{copy.title}</h1>
      <p className="mt-3 text-[var(--muted)]">{copy.subtitle}</p>
    </header>
    <section className="premium-new-trip-card rounded-[2rem] border border-[var(--line)] bg-[var(--surface)] p-6 md:p-8">
      <fieldset disabled={busy || !draftReady || Boolean(pending) || recoveryBlocked} className="min-w-0">
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
            <button ref={calendarButton} type="button" aria-expanded={calendarOpen} aria-controls="premium-new-trip-calendar" aria-invalid={error?.field === "dates" || undefined} aria-describedby={error?.field === "dates" ? "new-trip-date-error" : undefined} onClick={() => setCalendarOpen((open) => !open)} className="premium-new-trip-date-summary mt-2 flex min-h-12 w-full items-center gap-3 rounded-xl border border-[var(--line)] p-4 text-left">
              <CalendarDays size={20} className="shrink-0" /><span className="min-w-0 flex-1">{form.start_date && form.end_date ? formatTripDay(locale, form.start_date) + " → " + formatTripDay(locale, form.end_date) : copy.datePrompt}{days > 0 && <strong className="mt-1 block text-sm text-[var(--teal)]">{t("summary.days", { days })}</strong>}</span><ChevronDown size={16} className="shrink-0" />
            </button>
            {error?.field === "dates" && <p id="new-trip-date-error" ref={errorRef} tabIndex={-1} role="alert" className="mt-2 text-sm text-red-800 outline-none">{error.message}</p>}
          </fieldset>
        </div>
        <div id="premium-new-trip-calendar" hidden={!calendarOpen} className="premium-new-trip-calendar mt-5">
          {calendarOpen && <><p className="mb-3 text-xs text-[var(--muted)]">{t("basics.datesHelp", { maxDays: MAX_TRIP_DAYS })}</p><DateRangePicker start={form.start_date} end={form.end_date} today={today} maxDays={MAX_TRIP_DAYS} countries={holidayMarkets} onChange={chooseDates} /><button type="button" onClick={() => { setCalendarOpen(false); calendarButton.current?.focus(); }} className="mt-3 min-h-11 rounded-lg border border-[var(--line)] px-4 py-2 text-sm font-semibold">{copy.closeCalendar}</button></>}
        </div>
        <details className="calm-new-trip-name premium-new-trip-name mt-5">
          <summary className="flex min-h-11 cursor-pointer items-center justify-between gap-3 text-sm"><span><span className="block text-xs text-[var(--muted)]">{t("basics.name")}</span><strong>{tripName || copy.nameHelp}</strong></span><ChevronDown size={16} className="shrink-0" /></summary>
          <div className="mt-3">
          <label htmlFor="trip-name" className="text-sm font-semibold">{t("basics.name")}</label>
          <input id="trip-name" maxLength={255} value={nameEdited ? form.name : automaticName} onChange={(event) => { setNameEdited(true); update("name", event.target.value); }} aria-describedby="trip-name-help" className={fieldClass} />
          <div className="mt-2 flex flex-wrap items-center justify-between gap-2"><p id="trip-name-help" className="text-xs text-[var(--muted)]">{copy.nameHelp}</p>{nameEdited && <button type="button" onClick={() => { setNameEdited(false); update("name", ""); }} className="min-h-11 text-xs font-semibold text-[var(--teal)]">{copy.autoName}</button>}</div>
          </div>
        </details>
        <details open={travelersOpen} onToggle={(event) => setTravelersOpen(event.currentTarget.open)} className="calm-new-trip-travelers premium-new-trip-travelers mt-4">
          <summary className="flex min-h-11 cursor-pointer items-center gap-3 text-sm"><Users size={18} /><span className="flex-1"><span className="block text-xs text-[var(--muted)]">{t("travelers.title")}</span><strong>{t("summary.travelers", { count: Number(form.adults) + Number(form.children), rooms: Number(form.rooms) })}</strong></span><ChevronDown size={16} /></summary>
          <p className="mb-3 mt-1 text-xs text-[var(--muted)]">{copy.travelersHelp}</p>
          <NewTripTravelerFields values={form} onChange={update} />
        </details>
        <details open={advancedOpen} onToggle={(event) => setAdvancedOpen(event.currentTarget.open)} className="premium-new-trip-advanced mt-6 border-t border-[var(--line)] pt-5">
          <summary className="min-h-11 cursor-pointer text-sm font-semibold"><SlidersHorizontal size={16} className="mr-2 inline-block" />{copy.advanced}</summary>
          <div className="mt-5"><NewTripPreferenceFields values={form} onChange={updatePreference} lodgingMode={lodgingMode} onLodgingModeChange={(value) => { setError(undefined); setLodgingMode(value); }} interests={selectedInterests} onToggleInterest={toggleInterest} shopThemes={selectedShopThemes} onToggleShopTheme={toggleShopTheme} />
            <label className="mt-5 block text-sm font-semibold">{t("review.notes")}<textarea rows={3} maxLength={1000} value={form.notes} onChange={(event) => update("notes", event.target.value)} placeholder={t("review.notesPlaceholder")} className={fieldClass} /></label>
          </div>
        </details>
      </fieldset>
      {error && error.field !== "dates" && <p ref={errorRef} tabIndex={-1} role="alert" className="mt-5 rounded-xl bg-red-50 p-4 text-sm text-red-800 outline-none">{error.message}</p>}
      {(pending || recoveryBlocked) && !busy && <section aria-label={copy.recoveryTitle} className="mt-4 rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm">
        <h2 className="font-semibold">{copy.recoveryTitle}</h2>
        <p className="mt-2">{expired || recoveryBlocked ? copy.recoveryExpired : copy.recoveryHint}</p>
        <a href={`/${locale}/trips`} className="mt-2 inline-flex min-h-11 items-center font-semibold text-[var(--teal)]">{copy.myTrips}</a>
      </section>}
      <footer className="calm-new-trip-footer premium-new-trip-footer mt-6 flex flex-wrap items-center justify-between gap-4 border-t border-[var(--line)] pt-5">
        <p className="max-w-md text-xs leading-5 text-[var(--muted)]">{copy.notice}</p>
        <button type="submit" disabled={busy || !draftReady || expired || recoveryBlocked} className="premium-new-trip-submit flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-6 py-3 font-semibold text-white disabled:opacity-60">{busy ? copy.creating : pending ? copy.retryOriginal : copy.submit}<ArrowRight size={18} /></button>
      </footer>
    </section>
  </form>;
}
