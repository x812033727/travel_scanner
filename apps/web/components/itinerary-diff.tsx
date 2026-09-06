"use client";

import { ArrowRight, ChevronDown, CircleAlert, Loader2, MinusCircle, MoveRight, PencilLine, PlusCircle, Sparkles, UtensilsCrossed, Wand2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useId, useRef, useState, type FormEvent, type ReactNode } from "react";
import { PlannerOverlay } from "@/components/planner-overlay";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import { api, ApiError } from "@/lib/api";
import type { Trip } from "@/lib/trip-types";
import type { UsageOperation } from "@/lib/usage-catalog";

export const INTENT_MAX_LENGTH = 400;

type IntentScope = "day" | "trip";

/** Fields apply would overwrite, in the vocabulary the sheet has copy for. */
type ChangedField = "title" | "place" | "duration" | "notes";

type DiffEntry = {
  candidate_key?: string | null;
  title: string;
  location_name?: string | null;
  day_date: string | null;
  start_time: string | null;
  duration_minutes?: number | null;
  fields?: ChangedField[];
  reason?: string | null;
};

type MovedEntry = {
  candidate_key: string;
  title: string;
  location_name?: string | null;
  from: { day_date: string | null; start_time: string | null };
  to: { day_date: string | null; start_time: string | null };
  fields?: ChangedField[];
  reason?: string | null;
};

type MealEntry = {
  system_role: string;
  day_date: string | null;
  before_title: string | null;
  after_title: string;
  fields?: ChangedField[];
  cleared: boolean;
};

export type IntentPreview = {
  preview_id: string;
  base_version: number;
  expires_at: string;
  scope: IntentScope;
  day_date?: string | null;
  planning: NonNullable<Trip["planning"]>;
  intent: { text: string };
  /** What apply will charge. Absent on envelopes cached before it existed. */
  usage_operation?: UsageOperation;
  diff: {
    removed: DiffEntry[];
    added: DiffEntry[];
    moved: MovedEntry[];
    changed?: DiffEntry[];
    meals: MealEntry[];
    unchanged_count: number;
    has_changes: boolean;
  };
  exhaustion: {
    exhausted: boolean;
    reason: "no_alternatives" | "no_change" | null;
    alternative_candidate_count: number;
    alternative_merchant_count?: number;
    pool_spent?: boolean;
    meal_pool_spent?: boolean;
    activity_delta: number;
    fewer_stops_without_alternatives: boolean;
  };
};

type ItineraryDiffProps = {
  trip: Trip;
  activeDay?: string;
  disabled?: boolean;
  /** Flush pending edits first; returns the freshest trip, or undefined on a conflict. */
  prepare?: () => Promise<Trip | undefined>;
  onApplied: (updated: Trip, scope: IntentScope, dayDate?: string | null) => void;
  onError?: (message: string) => void;
};

export function ItineraryDiff({ trip, activeDay, disabled, prepare, onApplied, onError }: ItineraryDiffProps) {
  const t = useTranslations("trips");
  const refineCharge = useOperationCharge("ai_itinerary_refine");
  const generateCharge = useOperationCharge("ai_itinerary_generation");
  const inputId = useId();
  const [text, setText] = useState("");
  const [scope, setScope] = useState<IntentScope>("day");
  const [preview, setPreview] = useState<IntentPreview>();
  const [busy, setBusy] = useState<"submit" | "apply">();
  const [intentOpen, setIntentOpen] = useState(false);
  // Held across a failed attempt so an identical retry replays server-side
  // instead of spending another rate-limit slot and another provider call.
  const intentKeyRef = useRef<{ signature: string; key: string } | undefined>(undefined);

  const effectiveScope: IntentScope = scope === "day" && !activeDay ? "trip" : scope;
  const trimmed = text.trim();
  // Nudging one day is free; re-planning the whole trip is the same work the
  // paid planner does, so the button must not promise otherwise.
  const operation: UsageOperation =
    preview?.usage_operation ?? (effectiveScope === "day" ? "ai_itinerary_refine" : "ai_itinerary_generation");
  const charge = operation === "ai_itinerary_refine" ? refineCharge : generateCharge;

  function fail(reason: unknown, fallback: string) {
    onError?.(reason instanceof ApiError ? reason.message : reason instanceof Error ? reason.message : fallback);
  }

  async function submitIntent(event: FormEvent) {
    event.preventDefault();
    if (!trimmed || busy) return;
    const current = prepare ? await prepare() : trip;
    if (!current) return;
    setBusy("submit");
    // The server's replay key hashes the sentence, scope, day and version
    // alongside this header, so reusing it is only ever a replay of the very
    // same request. A new request — a different sentence, or a deliberate
    // second ask after a plan came back — gets a new key.
    const signature = `${current.id}|${current.version}|${effectiveScope}|${effectiveScope === "day" ? activeDay ?? "" : ""}|${trimmed}`;
    if (intentKeyRef.current?.signature !== signature) {
      intentKeyRef.current = { signature, key: crypto.randomUUID() };
    }
    try {
      const result = await api<IntentPreview>(`/trips/${current.id}/intents`, {
        method: "POST",
        headers: { "Idempotency-Key": intentKeyRef.current.key },
        body: JSON.stringify({
          version: current.version,
          text: trimmed.slice(0, INTENT_MAX_LENGTH),
          scope: effectiveScope,
          day_date: effectiveScope === "day" ? activeDay : null,
        }),
      });
      intentKeyRef.current = undefined;
      setPreview(result);
    } catch (reason) {
      fail(reason, t("intent.submit"));
    } finally {
      setBusy(undefined);
    }
  }

  async function applyIntent() {
    if (!preview || busy) return;
    setBusy("apply");
    try {
      const updated = await api<Trip>(`/trips/${trip.id}/itinerary/apply`, {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({ version: preview.base_version, preview_id: preview.preview_id }),
      });
      setPreview(undefined);
      setText("");
      onApplied(updated, preview.scope, preview.day_date);
    } catch (reason) {
      // The envelope is single-use and the apply is what bumps the version, so
      // a failure means the review has to start again rather than be retried.
      setPreview(undefined);
      fail(reason, t("intent.apply", { charge: charge.label }));
    } finally {
      setBusy(undefined);
    }
  }

  const examples = [t("intent.exampleRain"), t("intent.exampleWalk"), t("intent.exampleShopping")];
  const diff = preview?.diff;
  const exhaustion = preview?.exhaustion;
  const changedRows = diff?.changed ?? [];
  // "fallback" means every provider failed and the deterministic catalog
  // sorter produced this — it never reads the sentence. Offering Apply on a
  // plan that ignored the request would make the sheet a liar.
  const plannerUnavailable = preview?.planning.status === "fallback";
  const appliable = Boolean(diff?.has_changes) && !plannerUnavailable;
  const fieldList = (fields?: ChangedField[]) =>
    (fields || []).map((name) => t(`intent.field.${name}`)).join(t("intent.fieldSeparator"));

  return (
    <>
      <section aria-label={t("intent.barLabel")} className="planner-intent-bar sticky z-30 mt-5 rounded-2xl border border-violet-200 bg-white/95 p-3 shadow-[var(--shadow-lg)] backdrop-blur lg:p-4">
        {/* On a phone this bar floats above the dock, and open it is four rows
            tall - a third of the screen permanently over the itinerary, deep
            enough to cover the card the reader is reaching for. It opens on
            demand there and stays open on a desktop, where there is room. */}
        <button
          type="button"
          aria-expanded={intentOpen}
          onClick={() => setIntentOpen((open) => !open)}
          className="flex min-h-11 w-full items-center gap-2 text-sm font-bold text-violet-900 lg:hidden"
        >
          <Wand2 size={16} />
          {t("intent.eyebrow")}
          <ChevronDown size={16} className={`ml-auto transition ${intentOpen ? "rotate-180" : ""}`} />
        </button>
        <form onSubmit={submitIntent} className={`${intentOpen ? "grid" : "hidden lg:grid"} gap-3`}>
          <div className="flex flex-wrap items-center justify-between gap-2">
            <label htmlFor={inputId} className="hidden items-center gap-2 text-sm font-bold text-violet-900 lg:flex">
              <Wand2 size={16} />{t("intent.eyebrow")}
            </label>
            <label htmlFor={inputId} className="sr-only lg:hidden">{t("intent.eyebrow")}</label>
            <div role="radiogroup" aria-label={t("intent.scopeLegend")} className="flex gap-1 rounded-xl bg-[var(--paper)] p-1">
              {(["day", "trip"] as const).map((value) => (
                <button
                  key={value}
                  type="button"
                  role="radio"
                  aria-checked={effectiveScope === value}
                  disabled={value === "day" && !activeDay}
                  onClick={() => setScope(value)}
                  className={`min-h-9 rounded-lg px-3 text-xs font-semibold disabled:opacity-40 ${effectiveScope === value ? "bg-white text-violet-800 shadow-sm" : "text-[var(--muted)]"}`}
                >
                  {value === "day" ? t("intent.scopeDay") : t("intent.scopeTrip")}
                </button>
              ))}
            </div>
          </div>
          <div className="flex gap-2">
            <input
              id={inputId}
              value={text}
              maxLength={INTENT_MAX_LENGTH}
              onChange={(event) => setText(event.target.value)}
              placeholder={effectiveScope === "day" ? t("intent.placeholderDay") : t("intent.placeholderTrip")}
              disabled={disabled || busy === "submit"}
              className="min-h-11 min-w-0 flex-1 rounded-xl border border-[var(--line)] bg-white px-3 text-sm outline-none transition focus:border-violet-500 focus:ring-4 focus:ring-violet-100"
            />
            <button
              type="submit"
              disabled={disabled || !trimmed || Boolean(busy)}
              className="flex min-h-11 items-center justify-center gap-2 rounded-xl bg-violet-700 px-4 text-sm font-semibold text-white disabled:opacity-45"
            >
              {busy === "submit" ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
              <span className="hidden sm:inline">{busy === "submit" ? t("intent.submitting") : t("intent.submit")}</span>
            </button>
          </div>
          {!activeDay && <p className="text-xs text-[var(--muted)]">{t("intent.dayRequired")}</p>}
          <div className="flex flex-wrap items-center gap-2 text-xs">
            <span className="text-[var(--muted)]">{t("intent.examplesLabel")}</span>
            {examples.map((example) => (
              <button
                key={example}
                type="button"
                disabled={disabled || Boolean(busy)}
                onClick={() => setText(example)}
                className="min-h-8 rounded-full border border-[var(--line)] px-3 text-[var(--muted)] transition hover:border-violet-300 hover:text-violet-800 disabled:opacity-40"
              >
                {example}
              </button>
            ))}
          </div>
        </form>
      </section>

      <PlannerOverlay
        open={Boolean(preview)}
        onClose={() => { if (!busy) setPreview(undefined); }}
        title={exhaustion?.exhausted ? t("intent.exhaustedTitle") : t("intent.sheetTitle")}
        description={t("intent.sheetDescription")}
        size="wide"
        footer={
          <div className="flex gap-3">
            <button type="button" onClick={() => setPreview(undefined)} disabled={Boolean(busy)} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold disabled:opacity-40">
              {appliable ? t("intent.cancel") : t("intent.close")}
            </button>
            {appliable && (
              <button
                type="button"
                onClick={() => void applyIntent()}
                disabled={Boolean(busy) || charge.status !== "ready"}
                className="flex min-h-12 flex-[1.5] items-center justify-center gap-2 rounded-xl bg-violet-700 px-4 font-semibold text-white disabled:opacity-45"
              >
                {busy === "apply" ? <Loader2 size={17} className="animate-spin" /> : <Sparkles size={17} />}
                {busy === "apply" ? t("intent.applying") : t("intent.apply", { charge: charge.label })}
              </button>
            )}
          </div>
        }
      >
        {preview && diff && exhaustion && (
          <div className="space-y-4">
            <p className="rounded-2xl bg-[var(--paper)] px-4 py-3 text-sm leading-6">{t("intent.quoted", { text: preview.intent.text })}</p>

            {exhaustion.exhausted && (
              <p role="status" className="flex items-start gap-3 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-950">
                <CircleAlert size={18} className="mt-0.5 shrink-0" />
                {exhaustion.reason === "no_alternatives" ? t("intent.exhaustedNoAlternatives") : t("intent.exhaustedNoChange")}
              </p>
            )}

            {exhaustion.fewer_stops_without_alternatives && (
              <p role="status" className="rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-950">
                {t("intent.fewerStops", { count: Math.abs(exhaustion.activity_delta) })}
              </p>
            )}

            {plannerUnavailable && (
              <p role="status" className="flex items-start gap-3 rounded-2xl border border-amber-300 bg-amber-50 px-4 py-3 text-sm leading-6 text-amber-950">
                <CircleAlert size={18} className="mt-0.5 shrink-0" />
                {t("intent.fallbackNote")}
              </p>
            )}

            {preview.planning.status === "partial" && (
              <p className="rounded-2xl border border-[var(--line)] px-4 py-3 text-xs leading-5 text-[var(--muted)]">{t("intent.partialNote")}</p>
            )}

            <DiffGroup title={t("intent.removedTitle", { count: diff.removed.length })} tone="removed" icon={<MinusCircle size={16} />} entries={diff.removed.length}>
              {diff.removed.map((entry) => (
                <EntryRow key={`removed-${entry.candidate_key || entry.title}`} entry={entry} noTime={t("intent.noTime")} />
              ))}
            </DiffGroup>

            <DiffGroup title={t("intent.addedTitle", { count: diff.added.length })} tone="added" icon={<PlusCircle size={16} />} entries={diff.added.length}>
              {diff.added.map((entry) => (
                <EntryRow key={`added-${entry.candidate_key || entry.title}`} entry={entry} noTime={t("intent.noTime")} />
              ))}
            </DiffGroup>

            <DiffGroup title={t("intent.movedTitle", { count: diff.moved.length })} tone="moved" icon={<MoveRight size={16} />} entries={diff.moved.length}>
              {diff.moved.map((entry) => (
                <li key={`moved-${entry.candidate_key}`} className="rounded-xl bg-white px-3 py-2.5">
                  <p className="text-sm font-semibold">{entry.title}</p>
                  <p className="mt-1 flex items-center gap-1.5 text-xs text-[var(--muted)]">
                    {t("intent.movedFromTo", {
                      from: `${entry.from.day_date || ""} ${entry.from.start_time || t("intent.noTime")}`.trim(),
                      to: `${entry.to.day_date || ""} ${entry.to.start_time || t("intent.noTime")}`.trim(),
                    })}
                  </p>
                  {entry.fields?.length ? <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("intent.changedFields", { fields: fieldList(entry.fields) })}</p> : null}
                  {entry.reason && <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{entry.reason}</p>}
                </li>
              ))}
            </DiffGroup>

            <DiffGroup title={t("intent.changedTitle", { count: changedRows.length })} tone="changed" icon={<PencilLine size={16} />} entries={changedRows.length}>
              {changedRows.map((entry) => (
                <li key={`changed-${entry.candidate_key || entry.title}`} className="rounded-xl bg-white px-3 py-2.5">
                  <p className="text-sm font-semibold">{entry.title}</p>
                  <p className="mt-1 flex items-center gap-1.5 text-xs text-[var(--muted)]">
                    <span>{entry.day_date}</span>
                    <ArrowRight size={12} aria-hidden="true" />
                    <span>{entry.start_time || t("intent.noTime")}</span>
                  </p>
                  <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("intent.changedFields", { fields: fieldList(entry.fields) })}</p>
                </li>
              ))}
            </DiffGroup>

            <DiffGroup title={t("intent.mealsTitle", { count: diff.meals.length })} tone="meal" icon={<UtensilsCrossed size={16} />} entries={diff.meals.length}>
              {diff.meals.map((entry) => (
                <li key={`meal-${entry.day_date}-${entry.system_role}`} className="rounded-xl bg-white px-3 py-2.5 text-sm">
                  <p className="text-xs text-[var(--muted)]">{entry.day_date}</p>
                  <p className="mt-0.5 font-medium">
                    {entry.cleared
                      ? t("intent.mealCleared", { before: entry.before_title || "" })
                      : t("intent.mealChanged", { before: entry.before_title || "", after: entry.after_title })}
                  </p>
                  {entry.fields?.length ? <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("intent.changedFields", { fields: fieldList(entry.fields) })}</p> : null}
                </li>
              ))}
            </DiffGroup>

            {diff.unchanged_count > 0 && (
              <p className="text-xs text-[var(--muted)]">{t("intent.unchanged", { count: diff.unchanged_count })}</p>
            )}
            {exhaustion.reason !== "no_alternatives" && exhaustion.pool_spent && (
              <p className="text-xs text-[var(--muted)]">{t("intent.poolSpent")}</p>
            )}
            {exhaustion.reason !== "no_alternatives" && exhaustion.meal_pool_spent && (
              <p className="text-xs text-[var(--muted)]">{t("intent.mealPoolSpent")}</p>
            )}
            {!exhaustion.exhausted && exhaustion.alternative_candidate_count > 0 && (
              <p className="text-xs text-[var(--muted)]">{t("intent.alternativesLeft", { count: exhaustion.alternative_candidate_count })}</p>
            )}
          </div>
        )}
      </PlannerOverlay>
    </>
  );
}

const TONE_CLASS: Record<string, string> = {
  removed: "border-red-200 bg-red-50",
  added: "border-emerald-200 bg-emerald-50",
  moved: "border-sky-200 bg-sky-50",
  changed: "border-violet-200 bg-violet-50",
  meal: "border-amber-200 bg-amber-50",
};

function DiffGroup({ title, tone, icon, entries, children }: { title: string; tone: string; icon: ReactNode; entries: number; children: ReactNode }) {
  if (!entries) return null;
  return (
    <section className={`rounded-2xl border p-4 ${TONE_CLASS[tone]}`}>
      <h3 className="flex items-center gap-2 text-sm font-bold">{icon}{title}</h3>
      <ul className="mt-3 space-y-2">{children}</ul>
    </section>
  );
}

function EntryRow({ entry, noTime }: { entry: DiffEntry; noTime: string }) {
  return (
    <li className="rounded-xl bg-white px-3 py-2.5">
      <p className="flex items-center gap-2 text-sm font-semibold">
        <span className="truncate">{entry.title}</span>
      </p>
      <p className="mt-1 flex items-center gap-1.5 text-xs text-[var(--muted)]">
        <span>{entry.day_date}</span>
        <ArrowRight size={12} aria-hidden="true" />
        <span>{entry.start_time || noTime}</span>
      </p>
      {entry.reason && <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{entry.reason}</p>}
    </li>
  );
}
