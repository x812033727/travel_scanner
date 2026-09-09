"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { useLocale } from "next-intl";
import { api } from "@/lib/api";
import { plannerCopy } from "@/lib/planner-copy";
import type { Trip } from "@/lib/trip-types";
import { calmEditCopy } from "./calm-edit-copy";
import {
  NewTripPreferenceFields, NewTripTravelerFields, newTripPreferenceError, newTripPreferencesPayload,
  type NewTripLodgingMode, type NewTripPreferenceValues, type NewTripTravelerValues,
} from "./new-trip-fields";

function record(value: unknown): Record<string, unknown> {
  return value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {};
}
function numberText(value: unknown, fallback = "") {
  if (typeof value === "number" && Number.isFinite(value)) return String(value);
  // Older JSON/Decimal serializers can retain valid numeric values as strings.
  if (typeof value === "string" && value.trim() !== "" && Number.isFinite(Number(value))) return value.trim();
  return fallback;
}
function strings(value: unknown): string[] {
  return Array.isArray(value) ? value.filter((item): item is string => typeof item === "string") : [];
}
function settings(trip: Trip) {
  // Search-created trips also expose these sections in data; search_criteria
  // remains source metadata and is never sent back by this form.
  const travelers = record(trip.data.travelers);
  const preferences = record(trip.data.preferences);
  const propertyTypes = strings(preferences.accepted_property_types);
  const lodgingMode: NewTripLodgingMode = propertyTypes.length === 1 && propertyTypes[0] === "hotel" ? "hotel"
    : propertyTypes.length === 1 && propertyTypes[0] === "vacation_rental" ? "vacation_rental"
      : propertyTypes.length === 2 && propertyTypes.includes("hotel") && propertyTypes.includes("vacation_rental") ? "both" : "any";
  const travelerValues: NewTripTravelerValues = {
    adults: numberText(travelers.adults, "1"), children: numberText(travelers.children, "0"), rooms: numberText(travelers.rooms, "1"),
  };
  const values: NewTripPreferenceValues = {
    budget_twd: numberText(preferences.budget_twd),
    pace: preferences.pace === "relaxed" || preferences.pace === "packed" ? preferences.pace : "balanced",
    route_preference: trip.route_preference || "FEWER_TRANSFERS",
    nightly_min: numberText(preferences.hotel_min_nightly_twd), nightly_max: numberText(preferences.hotel_max_nightly_twd),
    hotel_min_rating: numberText(preferences.hotel_min_rating),
    preferred_area: typeof preferences.preferred_area === "string" ? preferences.preferred_area : "",
    max_station_walk_minutes: numberText(preferences.max_station_walk_minutes),
    min_review_score: numberText(preferences.hotel_min_review_score), min_review_count: numberText(preferences.hotel_min_review_count),
    breakfast_required: preferences.breakfast_required === true, refundable_required: preferences.refundable_required === true,
    avoid_red_eye: preferences.avoid_red_eye === true,
  };
  return { travelers, preferences, travelerValues, values, lodgingMode, interests: strings(preferences.interests), shopThemes: strings(preferences.shop_themes) };
}

const preferenceKeys = {
  budget_twd: "budget_twd", pace: "pace", nightly_min: "hotel_min_nightly_twd", nightly_max: "hotel_max_nightly_twd",
  hotel_min_rating: "hotel_min_rating", preferred_area: "preferred_area", max_station_walk_minutes: "max_station_walk_minutes",
  min_review_score: "hotel_min_review_score", min_review_count: "hotel_min_review_count",
  breakfast_required: "breakfast_required", refundable_required: "refundable_required", avoid_red_eye: "avoid_red_eye",
} as const;
function same(left: unknown, right: unknown) {
  if (typeof left === "number" && typeof right === "string" && right.trim() !== "") return left === Number(right);
  return JSON.stringify(left) === JSON.stringify(right);
}
function toggle(values: string[], value: string) { return values.includes(value) ? values.filter((item) => item !== value) : [...values, value]; }

export function PlannerPreferences({ trip, prepare, onUpdated, onBusy, onDirtyChange, onCancel }: {
  trip: Trip;
  prepare: () => Promise<Trip | undefined>;
  onUpdated: (trip: Trip) => void;
  onBusy?: (busy: boolean) => void;
  onDirtyChange?: (dirty: boolean) => void;
  /** Parent may guard leaving; do not discard the draft until it confirms. */
  onCancel?: () => void;
}) {
  const locale = useLocale();
  const copy = plannerCopy(locale);
  const editCopy = calmEditCopy(locale);
  // Itinerary autosaves must not erase an in-progress settings edit. The save
  // action obtains the newest version and sends only fields changed here.
  const [initial] = useState(() => settings(trip));
  const [baseline, setBaseline] = useState(initial);
  const [travelers, setTravelers] = useState(initial.travelerValues);
  const [values, setValues] = useState(initial.values);
  const [lodgingMode, setLodgingMode] = useState(initial.lodgingMode);
  const [lodgingEdited, setLodgingEdited] = useState(false);
  const [interests, setInterests] = useState(initial.interests);
  const [shopThemes, setShopThemes] = useState(initial.shopThemes);
  const [busy, setBusy] = useState(false);
  const busyRef = useRef(false);
  const [error, setError] = useState<string>();
  const [saved, setSaved] = useState(false);

  const dirty = !same(travelers, baseline.travelerValues) || !same(values, baseline.values)
    || lodgingMode !== baseline.lodgingMode || !same(interests, baseline.interests) || !same(shopThemes, baseline.shopThemes);
  useEffect(() => { onDirtyChange?.(dirty); }, [dirty, onDirtyChange]);

  function changed() { setError(undefined); setSaved(false); }
  function reset(next: ReturnType<typeof settings>) {
    setBaseline(next);
    setTravelers(next.travelerValues); setValues(next.values); setLodgingMode(next.lodgingMode); setLodgingEdited(false);
    setInterests(next.interests); setShopThemes(next.shopThemes);
    onDirtyChange?.(false);
  }
  async function save(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (busyRef.current) return;
    setError(undefined); setSaved(false);
    const travelerValid = ([["adults", 1, 9], ["children", 0, 9], ["rooms", 1, 4]] as const).every(([key, min, max]) =>
      travelers[key].trim() !== "" && Number.isInteger(Number(travelers[key])) && Number(travelers[key]) >= min && Number(travelers[key]) <= max);
    const integerFields = ["budget_twd", "nightly_min", "nightly_max", "hotel_min_rating", "max_station_walk_minutes", "min_review_count"] as const;
    if (!travelerValid || newTripPreferenceError(values) || integerFields.some((key) => values[key] !== "" && !Number.isInteger(Number(values[key])))
      || Number(values.min_review_score) > 10 || Number(values.max_station_walk_minutes) > 120 || Number(values.hotel_min_rating) > 5
      || (values.hotel_min_rating !== "" && Number(values.hotel_min_rating) < 1) || interests.length > 10 || shopThemes.length > 8) {
      setError(copy.invalidPreferences);
      return;
    }
    const travelerPatch: Record<string, unknown> = {};
    for (const key of ["adults", "children", "rooms"] as const) {
      if (Number(travelers[key]) !== Number(baseline.travelerValues[key])) travelerPatch[key] = Number(travelers[key]);
    }
    const preferencePatch: Record<string, unknown> = {};
    const payload = { ...newTripPreferencesPayload(values, lodgingMode, interests, shopThemes), hotel_min_review_score: values.min_review_score === "" ? null : Number(values.min_review_score) };
    for (const key of Object.keys(preferenceKeys) as (keyof typeof preferenceKeys)[]) {
      const apiKey = preferenceKeys[key];
      if (values[key] !== baseline.values[key] && !same(payload[apiKey], baseline.preferences[apiKey])) preferencePatch[apiKey] = payload[apiKey];
    }
    if (lodgingEdited && !same(payload.accepted_property_types, baseline.preferences.accepted_property_types || [])) preferencePatch.accepted_property_types = payload.accepted_property_types;
    if (!same(interests, baseline.interests)) preferencePatch.interests = interests;
    if (!same(shopThemes, baseline.shopThemes) || (baseline.interests.includes("shopping") && !interests.includes("shopping"))) preferencePatch.shop_themes = payload.shop_themes;
    if (!Object.keys(travelerPatch).length && !Object.keys(preferencePatch).length) { reset(baseline); return; }

    busyRef.current = true; setBusy(true);
    try {
      onBusy?.(true);
      const latest = await prepare();
      if (!latest || latest.id !== trip.id) return;
      // Changing the number of children makes a previously complete age list
      // incomplete. Keep ages for adult/room edits; never invent missing ages.
      if ("children" in travelerPatch) {
        const latestAges = record(latest.data.travelers).children_ages;
        if (Array.isArray(latestAges) && latestAges.length && latestAges.length !== travelerPatch.children) travelerPatch.children_ages = [];
      }
      const updated = await api<Trip>(`/trips/${trip.id}`, {
        method: "PATCH", body: JSON.stringify({ version: latest.version,
          ...(Object.keys(travelerPatch).length ? { travelers: travelerPatch } : {}),
          ...(Object.keys(preferencePatch).length ? { preferences: preferencePatch } : {}),
        }),
      });
      reset(settings(updated)); setSaved(true); onUpdated(updated);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : copy.invalidPreferences);
    } finally {
      busyRef.current = false; setBusy(false);
      onBusy?.(false);
    }
  }
  return <section className="premium-planner-preferences rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <h4 className="font-semibold">{copy.preferences}</h4>
    <p className="my-3 text-sm text-[var(--muted)]">{copy.preferencesHint}</p>
    <form onSubmit={(event) => { void save(event); }} noValidate aria-label={copy.preferences}>
      <fieldset disabled={busy} className="space-y-5">
        <NewTripTravelerFields values={travelers} onChange={(key, value) => { changed(); setTravelers((previous) => ({ ...previous, [key]: value })); }} />
        <NewTripPreferenceFields values={values} hideRoutePreference onChange={(key, value) => { changed(); setValues((previous) => ({ ...previous, [key]: value })); }}
          lodgingMode={lodgingMode} onLodgingModeChange={(value) => { changed(); setLodgingEdited(true); setLodgingMode(value); }}
          interests={interests} onToggleInterest={(code) => { changed(); setInterests((previous) => toggle(previous, code)); }}
          shopThemes={shopThemes} onToggleShopTheme={(code) => { changed(); setShopThemes((previous) => toggle(previous, code)); }} />
      </fieldset>
      {error && <p role="alert" className="mt-3 text-sm text-red-700">{error}</p>}
      {saved && <p role="status" className="mt-3 text-sm text-[var(--teal-dark)]">{copy.preferencesSaved}</p>}
      <div className="calm-preferences-actions mt-4 flex items-center justify-end gap-3 bg-[var(--surface)] py-3">
        {dirty && <span className="mr-auto text-xs text-[var(--muted)]">{editCopy.unsaved}</span>}
        <button type="button" disabled={busy} className="rounded-xl border border-[var(--line)] px-4 py-3 font-semibold" onClick={() => {
          if (onCancel) onCancel(); else { reset(baseline); changed(); }
        }}>{editCopy.cancel}</button>
        <button type="submit" disabled={busy} aria-busy={busy} className="rounded-xl bg-[var(--teal-dark)] px-4 py-3 font-semibold text-white">{copy.savePreferences}</button>
      </div>
    </form>
  </section>;
}
