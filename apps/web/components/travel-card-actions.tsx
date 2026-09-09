"use client";

import { AlertCircle, CalendarPlus, Check, Heart, Hotel, LoaderCircle, LogIn, Share2, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { Link, usePathname, useRouter } from "@/i18n/navigation";
import { useSearchParams } from "next/navigation";
import { ApiError, api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { useSavedItems, type SavedType } from "@/components/saved-items-provider";
import { useHeaderSession } from "@/components/header-session";
import { Button, Dialog, fieldClass } from "@/components/community/ui";
import { SavedContentAction } from "@/components/discovery/saved-content-action";
import { useDiscoveryStatus, type DiscoveryItem } from "@/lib/discovery";
import { frontendCopy } from "@/lib/frontend-navigation";
import { planningResumeUrl, rememberPlanningIntent, tripDayOptions } from "@/lib/frontend-flow";

type TripOption = {
  trip_id: string;
  name: string;
  version: number;
  start_date: string;
  end_date: string;
  destination_name?: string | null;
  destination_id?: string | null;
};
type PlanningCapability = { kind: "hotspot" | "food" | "merchant" | "hotel"; id: string; destination_id?: string; selection_path?: string; product_id?: string; merchants?: Array<{id: string; name: string; destination_id?: string; selection_path?: string}> };
type PlanningDetails = DiscoveryItem & { detail?: { planning?: PlanningCapability | null } };
type TripOptions = { items: TripOption[]; can_create?: boolean; count?: number; limit?: number };
const normalizedDestination = (value: string | null | undefined) => value?.trim().toLocaleLowerCase();
function sameDestination(trip: TripOption, content?: PlanningDetails) {
  const destinationId = content?.detail?.planning?.destination_id || content?.destination?.id;
  if (trip.destination_id && destinationId) return trip.destination_id === destinationId;
  return Boolean(trip.destination_name && [content?.destination?.name, destinationId].some((name) => normalizedDestination(name) === normalizedDestination(trip.destination_name)));
}

/** One planning-only action across reading, saved items and legacy catalog cards. */
export function TravelPlanAction({ item, returnTo, compact = false, resumeEnabled = true }: { item: DiscoveryItem; returnTo: string; compact?: boolean; resumeEnabled?: boolean }) {
  const { sessionIdentity } = useHeaderSession();
  const [owner, setOwner] = useState(sessionIdentity);
  const [epoch, setEpoch] = useState(0);
  if (owner !== sessionIdentity) { setOwner(sessionIdentity); setEpoch(epoch + 1); return null; }
  return <TravelPlanSession key={`${item.id}:${epoch}`} item={item} returnTo={returnTo} compact={compact} resumeEnabled={resumeEnabled} />;
}

function TravelPlanSession({ item, returnTo, compact, resumeEnabled }: { item: DiscoveryItem; returnTo: string; compact: boolean; resumeEnabled: boolean }) {
  const locale = useLocale();
  const copy = frontendCopy(locale);
  const router = useRouter();
  const params = useSearchParams();
  const { user, status } = useHeaderSession();
  const id = item.id.split(":").at(-1)!;
  const resumeKey = `${item.kind}:${id}`;
  const resume = resumeEnabled && params.get("resume_action") === "trip" && [item.id, resumeKey].includes(params.get("resume_item") || "");
  const [open, setOpen] = useState(resume);
  const [attempt, setAttempt] = useState(0);
  const [loaded, setLoaded] = useState<{ content: PlanningDetails; options: TripOptions }>();
  const [tripId, setTripId] = useState("");
  const [day, setDay] = useState("");
  const [merchantId, setMerchantId] = useState("");
  const [meal, setMeal] = useState<"lunch" | "dinner">("lunch");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [failed, setFailed] = useState(false);
  const [authExpired, setAuthExpired] = useState(false);
  const [notice, setNotice] = useState<string>();
  const [blocked, setBlocked] = useState(false);
  const [locked, setLocked] = useState(false);
  const [uncertain, setUncertain] = useState(false);
  const active = useRef(true);
  const operation = useRef<{ path: string; body: string; key: string } | null>(null);
  const [trigger, setTrigger] = useState<HTMLElement | null>(null);
  const capability = loaded?.content.detail?.planning;
  const selected = loaded?.options.items.find((trip) => trip.trip_id === tripId);
  const matches = (trip: TripOption, content = loaded?.content) => sameDestination(trip, content);
  const options = [...(loaded?.options.items || [])].sort((a, b) => Number(matches(b)) - Number(matches(a)));
  const days = selected ? tripDayOptions(selected.start_date, selected.end_date, locale) : [];
  const isHotel = capability?.kind === "hotel" || item.kind === "hotel";
  const isMeal = capability?.kind === "food" || capability?.kind === "merchant";
  const canPlan = Boolean(capability && selected && day && (!isMeal || merchantId));
  const originalTripId = params.get("resume_trip");

  useEffect(() => { active.current = true; return () => { active.current = false; }; }, []);
  useEffect(() => {
    if (!open || !user) return;
    const controller = new AbortController();
    Promise.all([
      api<PlanningDetails>(`/discovery/content/${item.kind}/${encodeURIComponent(id)}`, { signal: controller.signal }),
      api<TripOptions>("/trips/options", { signal: controller.signal }),
    ]).then(([content, tripOptions]) => {
      if (controller.signal.aborted) return;
      const matching = tripOptions.items.filter((trip) => sameDestination(trip, content));
      const preferred = tripOptions.items.find((trip) => trip.trip_id === originalTripId) || (matching.length === 1 ? matching[0] : undefined);
      setLoaded({ content, options: tripOptions });
      if (!operation.current) { setTripId(preferred?.trip_id || ""); setDay(preferred?.start_date || ""); }
      const plan = content.detail?.planning;
      if (!operation.current) setMerchantId(plan?.kind === "merchant" ? plan.id : "");
      setFailed(false); setBlocked(false); setAuthExpired(false);
    }).catch((reason: unknown) => { if (!controller.signal.aborted) { setFailed(true); setAuthExpired(reason instanceof ApiError && reason.status === 401); setError(reason instanceof ApiError && reason.status === 401 ? copy.login : copy.error); } });
    return () => controller.abort();
  }, [open, user, item.kind, id, attempt, originalTripId, copy.login, copy.error]);

  function close() {
    setOpen(false);
    if (resume) {
      const url = new URL(window.location.href);
      for (const key of ["resume_action", "resume_item", "resume_kind", "resume_trip"]) url.searchParams.delete(key);
      window.history.replaceState(null, "", url.pathname + url.search + url.hash);
    }
  }
  function createTrip() {
    if (!user || !rememberPlanningIntent(user.id, item.kind, id, returnTo)) { setError(copy.error); return; }
    router.push("/trips/new?resume_plan=1");
  }
  async function confirm() {
    if (!canPlan || !selected || !capability || busy || blocked || (uncertain && !isHotel)) return;
    const selectionPath = capability.selection_path;
    if (!isHotel && (!selectionPath || !/^\/(hotspots|foods(?:\/merchants)?)\/[a-f0-9-]+\/trip-selections$/i.test(selectionPath))) { setError(copy.unavailable); return; }
    const path = isHotel ? `/trips/${selected.trip_id}/travel-services` : selectionPath!;
    const body = JSON.stringify(isHotel ? { product_id: capability.product_id, version: selected.version } : { trip_id: selected.trip_id, version: selected.version, day_date: day, ...(isMeal ? { ...(capability.kind === "food" ? { merchant_id: merchantId } : {}), meal_role: meal } : {}) });
    if (operation.current && !uncertain && (operation.current.path !== path || operation.current.body !== body)) { setBlocked(true); setError(copy.conflict); return; }
    operation.current ||= { path, body, key: crypto.randomUUID() };
    setBusy(true); setLocked(true); setError("");
    try {
      // Hotel selections support replay. Keep the exact original version and key
      // when a response is lost, including after closing and reopening the panel.
      await api(operation.current.path, { method: "POST", body: operation.current.body, headers: { "Idempotency-Key": operation.current.key } });
      if (!active.current) return;
      operation.current = null; setLocked(false); setUncertain(false); setNotice(selected.trip_id); close();
    } catch (reason) {
      if (!active.current) return;
      if (reason instanceof ApiError && [400, 401, 403, 404, 409, 422, 429].includes(reason.status)) { operation.current = null; setLocked(false); setUncertain(false); }
      else { setUncertain(true); }
      if (reason instanceof ApiError && reason.status === 409) { setBlocked(true); setError(copy.conflict); }
      else setError(copy.error);
    } finally { if (active.current) setBusy(false); }
  }
  return <>
    <Button secondary={compact} disabled={status === "loading" || status === "unavailable"} onClick={(event) => { setTrigger(event.currentTarget); setError(""); setOpen(true); }}>{isHotel ? <Hotel size={17} aria-hidden /> : <CalendarPlus size={17} aria-hidden />}{isHotel ? copy.hotel : copy.plan}</Button>
    {notice && <p role="status" className="flex min-h-11 flex-wrap items-center gap-2 text-sm">{copy.added}<Link href={`/trips/${notice}`} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{copy.openTrip}</Link></p>}
    {open && <Dialog title={isHotel ? copy.hotel : copy.plan} returnFocusTo={trigger} onClose={close}>
      <p className="mb-4 text-sm text-[var(--muted)]">{copy.selected} · <strong className="text-[var(--ink)]">{item.title}</strong></p>
      {!user ? <Link href={loginPath(planningResumeUrl(returnTo, item.kind, id))} className="inline-flex min-h-12 items-center rounded-xl bg-[var(--teal)] px-5 font-semibold text-white">{copy.login}</Link> : <>
        {authExpired && <Link href={loginPath(planningResumeUrl(returnTo, item.kind, id))} className="inline-flex min-h-12 items-center rounded-xl bg-[var(--teal)] px-5 font-semibold text-white">{copy.login}</Link>}
        {!loaded && !failed && <p role="status">{copy.loading}</p>}
        {uncertain && !isHotel ? <div role="alert" className="my-3 rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3"><p>{copy.uncertain}</p><Link href={`/trips/${tripId}`} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{copy.openTrip}</Link></div> : error && <div role="alert" className="my-3 rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3"><p>{error}</p>{(failed || blocked) && <Button secondary className="mt-3" onClick={() => { setLoaded(undefined); setFailed(false); setError(""); setAttempt((value) => value + 1); }}>{copy.retry}</Button>}</div>}
        {loaded && (!capability ? <p className="py-5 leading-7">{item.kind === "food" ? copy.noMerchant : copy.unavailable}</p> : <div className="space-y-5">
          {loaded.options.items.length === 0 ? <p>{copy.empty}</p> : <>
            <label className="block font-semibold">{copy.chooseTrip}<select className={fieldClass} value={tripId} disabled={busy || locked} onChange={(event) => { const trip = options.find((row) => row.trip_id === event.target.value); setTripId(trip?.trip_id || ""); setDay(trip?.start_date || ""); }}><option value="">{copy.chooseTrip}</option>{options.map((trip) => <option key={trip.trip_id} value={trip.trip_id}>{matches(trip) ? `${copy.destinationMatch} · ` : ""}{trip.name} · {trip.destination_name} · {trip.start_date} – {trip.end_date}</option>)}</select></label>
            {!isHotel && <label className="block font-semibold">{copy.chooseDay}<select className={fieldClass} disabled={!selected || busy || locked} value={day} onChange={(event) => setDay(event.target.value)}><option value="">{copy.chooseDay}</option>{days.map((entry) => <option key={entry.value} value={entry.value}>{copy.day} {entry.number} · {entry.label}</option>)}</select></label>}
            {capability.kind === "food" && <label className="block font-semibold">{copy.chooseMerchant}<select className={fieldClass} value={merchantId} disabled={busy || locked} onChange={(event) => setMerchantId(event.target.value)}><option value="">{copy.chooseMerchant}</option>{capability.merchants?.map((merchant) => <option key={merchant.id} value={merchant.id}>{merchant.name}</option>)}</select></label>}
            {isMeal && <label className="block font-semibold">{copy.meal}<select className={fieldClass} value={meal} disabled={busy || locked} onChange={(event) => setMeal(event.target.value as "lunch" | "dinner")}><option value="lunch">{copy.lunch}</option><option value="dinner">{copy.dinner}</option></select></label>}
            {(isHotel || isMeal) && <p className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6">{isHotel ? copy.hotelWarning : copy.mealWarning}</p>}
            <Button disabled={!canPlan || busy || blocked || (uncertain && !isHotel)} onClick={() => void confirm()} className="w-full">{busy ? copy.loading : isHotel ? copy.confirmHotel : copy.confirm}</Button>
          </>}
          {loaded.options.can_create !== false && <Button secondary disabled={busy || locked} onClick={createTrip}>{copy.create}</Button>}
        </div>)}
      </>}
    </Dialog>}
  </>;
}
export function TravelCardActions(props: Parameters<typeof LegacyTravelCardActions>[0]) {
  const discovery = useDiscoveryStatus();
  const pathname = usePathname();
  const params = useSearchParams();
  const returnTo = `${pathname}${params?.size ? `?${params}` : ""}`;
  if (!discovery.enabled || !["hotspot", "food", "merchant"].includes(props.type)) return <LegacyTravelCardActions {...props} />;
  const item: DiscoveryItem = { id: `${props.type}:${props.id}`, kind: props.type as "hotspot" | "food" | "merchant", title: props.title, summary: "", locale: "", href: returnTo, destination: null, source: { label: "", url: null, kind: "editorial" }, published_at: null, updated_at: null, thumbnail_url: null };
  return <div className="mt-4 flex flex-wrap gap-2"><SavedContentAction item={{ type: props.type, id: props.id, title: props.title }} returnTo={returnTo} /><TravelPlanAction item={item} returnTo={returnTo} compact /></div>;
}

function LegacyTravelCardActions({
  type,
  id,
  title,
  selectionPath,
  merchantId,
  shareRequiresAuth = false,
  resumeAfterLogin = false,
}: {
  type: SavedType;
  id: string;
  title: string;
  selectionPath: string;
  merchantId?: string;
  shareRequiresAuth?: boolean;
  resumeAfterLogin?: boolean;
}) {
  const common = useTranslations("common");
  const savedItems = useSavedItems();
  const pathname = usePathname();
  const saved = savedItems.isSaved(type, id);
  const [sheet, setSheet] = useState<"login" | "trip" | "save" | null>(null);
  const dialog = useRef<HTMLElement>(null);
  const [resumed, setResumed] = useState(false);
  const [resumeTrip, setResumeTrip] = useState(false);
  const [trips, setTrips] = useState<TripOption[]>([]);
  const [tripId, setTripId] = useState("");
  const [dayDate, setDayDate] = useState("");
  const [mealRole, setMealRole] = useState<"lunch" | "dinner">("lunch");
  const [busy, setBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [noticeHref, setNoticeHref] = useState("");
  const [error, setError] = useState("");
  const [loginHref, setLoginHref] = useState(() => loginPath(pathname));

  function clearFeedback() {
    setNotice("");
    setNoticeHref("");
    setError("");
  }

  function requireAuth(action: () => void, intent?: "save" | "trip") {
    // "loading" is not "signed out". Acting on it threw an already-signed-in
    // reader into the login sheet whenever they tapped before /saved-items
    // came back, which on a phone is most of the time.
    if (savedItems.status === "loading") return;
    if (savedItems.status !== "authenticated") {
      const query = new URLSearchParams(window.location.search);
      if (resumeAfterLogin && intent) { query.set("resume_action", intent); query.set("resume_item", `${type}:${id}`); }
      setLoginHref(loginPath(`${pathname}${query.size ? `?${query}` : ""}`));
      setSheet("login");
    }
    else action();
  }
  const openTrip = useCallback(async () => {
    setNotice(""); setNoticeHref(""); setError("");
    setSheet("trip");
    setBusy(true);
    try {
      const result = await api<{ items: TripOption[] }>("/trips/options");
      setTrips(result.items);
      const first = result.items[0];
      if (first) {
        setTripId(first.trip_id);
        setDayDate(first.start_date);
      }
    } catch (reason) {
      setSheet(null);
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }, []);
  // A resolved login changes which modal is rendered; the effect below performs
  // only the read-only trip lookup. It never confirms a saved item or itinerary.
  if (resumeAfterLogin && !resumed && savedItems.status === "authenticated" && typeof window !== "undefined") {
    const query = new URLSearchParams(window.location.search);
    const action = query.get("resume_action");
    if (query.get("resume_item") === `${type}:${id}` && (action === "save" || action === "trip")) {
      setResumed(true); setSheet(action);
      if (action === "trip") { setResumeTrip(true); setBusy(true); }
    }
  }
  useEffect(() => {
    if (!resumeTrip) return;
    const controller = new AbortController();
    api<{ items: TripOption[] }>("/trips/options", { signal: controller.signal }).then(({ items }) => {
      if (controller.signal.aborted) return;
      setTrips(items); if (items[0]) { setTripId(items[0].trip_id); setDayDate(items[0].start_date); }
    }).catch((reason: unknown) => { if (!controller.signal.aborted) setError((reason as Error).message); })
      .finally(() => { if (!controller.signal.aborted) setBusy(false); });
    return () => controller.abort();
  }, [resumeTrip]);
  useEffect(() => {
    if (!sheet) return;
    const previous = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const focusable = () => Array.from(dialog.current?.querySelectorAll<HTMLElement>('a[href],button:not([disabled]),input:not([disabled]),select:not([disabled]),textarea:not([disabled]),[tabindex="0"]') || []);
    focusable()[0]?.focus();
    function keyboard(event: KeyboardEvent) {
      if (event.key === "Escape") { event.preventDefault(); setSheet(null); }
      if (event.key !== "Tab") return;
      const items = focusable();
      const first = items[0], last = items.at(-1);
      if (!first) { event.preventDefault(); return; }
      if (!dialog.current?.contains(document.activeElement) || (event.shiftKey && document.activeElement === first)) { event.preventDefault(); (event.shiftKey ? last : first)?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
    }
    document.addEventListener("keydown", keyboard);
    return () => { document.removeEventListener("keydown", keyboard); document.body.style.overflow = overflow; if (previous?.isConnected) previous.focus(); };
  }, [sheet]);
  async function confirmSave() {
    setSaving(true); clearFeedback();
    try { await savedItems.setSaved(type, id, true); setSheet(null); setNotice(common("cardActions.saved")); }
    catch (reason) { setError((reason as Error).message); }
    finally { setSaving(false); }
  }
  async function submitTrip() {
    const trip = trips.find((item) => item.trip_id === tripId);
    if (!trip || !dayDate) return;
    setBusy(true);
    clearFeedback();
    try {
      await api(selectionPath, {
        method: "POST",
        body: JSON.stringify({
          trip_id: trip.trip_id,
          version: trip.version,
          day_date: dayDate,
          ...(merchantId
            ? { merchant_id: merchantId, meal_role: mealRole }
            : {}),
        }),
      });
      // A toast alone was a dead end: the reader had no way to see where the
      // place landed. Keep the link on screen long enough to be tapped.
      setNotice(common("cardActions.done"));
      setNoticeHref(`/trips/${trip.trip_id}`);
      setSheet(null);
      window.setTimeout(() => {
        setNotice("");
        setNoticeHref("");
      }, 8000);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function share() {
    clearFeedback();
    try {
      // window.location.href is the list, which is the same URL for every card
      // on the page. The anchor matches the id each card renders, so the link
      // lands on this one with the reader's filters still applied.
      const { origin, pathname: path, search } = window.location;
      const url = `${origin}${path}${search}#${type}-${id}`;
      if (navigator.share) await navigator.share({ title, url });
      else if (navigator.clipboard) {
        await navigator.clipboard.writeText(url);
        setNotice(common("cardActions.copied"));
        window.setTimeout(() => setNotice(""), 1600);
      } else {
        // No clipboard on http:// or in an old browser; show the link instead
        // of throwing an error the reader cannot act on.
        setError(url);
      }
    } catch (reason) {
      if ((reason as DOMException).name !== "AbortError") setError((reason as Error).message);
    }
  }
  async function toggleSaved() {
    setSaving(true);
    clearFeedback();
    try {
      await savedItems.toggle(type, id);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }
  return (
    <>
      <div className="travel-card-actions" aria-label={`${title} actions`}>
        <button
          type="button"
          aria-pressed={saved}
          disabled={saving}
          onClick={() => requireAuth(() => void toggleSaved(), "save")}
          className={
            saved
              ? "travel-card-action travel-card-action-active"
              : "travel-card-action"
          }
        >
          {saving ? <LoaderCircle className="animate-spin" size={18} /> : <Heart size={18} fill={saved ? "currentColor" : "none"} />}
          <span>{saved ? common("cardActions.saved") : common("cardActions.save")}</span>
        </button>
        <button
          type="button"
          disabled={(type === "food" || type === "merchant") && !merchantId}
          onClick={() => requireAuth(() => void openTrip(), "trip")}
          className="travel-card-action disabled:cursor-not-allowed disabled:opacity-35"
        >
          <CalendarPlus size={18} />
          <span>{common("cardActions.add")}</span>
        </button>
        <button
          type="button"
          disabled={shareRequiresAuth && savedItems.status === "loading"}
          onClick={() => shareRequiresAuth ? requireAuth(() => void share()) : void share()}
          className="travel-card-action disabled:cursor-wait disabled:opacity-60"
        >
          <Share2 size={18} />
          <span>{common("cardActions.share")}</span>
        </button>
      </div>
      {notice && (
        <div role="status" className="app-toast">
          <Check size={17} />
          {notice}
          {noticeHref && (
            <Link href={noticeHref} className="ml-1 underline underline-offset-2">
              {common("openTrip")}
            </Link>
          )}
        </div>
      )}
      {error && <div role="alert" className="app-toast app-toast-error"><AlertCircle size={17} />{error}</div>}
      {sheet && createPortal(
        <div
          className="app-sheet-backdrop"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setSheet(null);
          }}
        >
          <section
            ref={dialog}
            role="dialog"
            aria-modal="true"
            aria-label={sheet === "login" ? common("cardActions.login") : sheet === "save" ? common("cardActions.save") : common("cardActions.trip")}
            className="app-sheet"
            style={{ background: "var(--surface)", color: "var(--ink)" }}
          >
            <div className="app-sheet-handle" />
            <button
              type="button"
              aria-label={common("cardActions.close")}
              onClick={() => setSheet(null)}
              className="absolute right-4 top-4 grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]"
            >
              <X size={20} />
            </button>
            {sheet === "login" ? (
              <div className="py-8 text-center">
                <LogIn className="mx-auto text-[var(--teal)]" size={30} />
                <h3 className="mt-4 text-xl font-bold">{common("cardActions.login")}</h3>
                <Link
                  href={loginHref}
                  className="mt-6 inline-flex min-h-12 items-center rounded-2xl bg-[var(--teal)] px-6 font-bold text-white"
                >
                  {common("cardActions.loginAction")}
                </Link>
              </div>
            ) : sheet === "save" ? <div className="space-y-5 py-8"><h3 className="pr-12 text-xl font-bold">{title}</h3><button type="button" disabled={saving} onClick={() => void confirmSave()} className="min-h-12 rounded-xl bg-[var(--teal)] px-5 font-semibold text-white disabled:opacity-50">{saved ? common("cardActions.saved") : common("cardActions.save")}</button></div> : (
              <div className="pt-4">
                <h3 className="pr-12 text-2xl font-bold">{common("cardActions.add")}</h3>
                {busy && trips.length === 0 ? (
                  <p className="mt-5 text-[var(--muted)]">…</p>
                ) : trips.length === 0 ? (
                  <div className="mt-5 rounded-2xl bg-[var(--paper)] p-4">
                    <p>{common("cardActions.empty")}</p>
                    <Link
                      href="/trips/new"
                      className="mt-4 inline-flex min-h-12 items-center rounded-2xl bg-[var(--teal)] px-6 font-bold text-white"
                    >
                      {common("createTrip")}
                    </Link>
                  </div>
                ) : (
                  <div className="mt-5 grid gap-4">
                    <label className="grid gap-2 text-sm font-bold">
                      {common("cardActions.trip")}
                      <select
                        value={tripId}
                        onChange={(event) => {
                          const trip = trips.find(
                            (item) => item.trip_id === event.target.value,
                          );
                          setTripId(event.target.value);
                          if (trip) setDayDate(trip.start_date);
                        }}
                        className="app-field"
                      >
                        {trips.map((trip) => (
                          <option key={trip.trip_id} value={trip.trip_id}>
                            {trip.name}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label className="grid gap-2 text-sm font-bold">
                      {common("cardActions.date")}
                      <input
                        type="date"
                        value={dayDate}
                        min={
                          trips.find((item) => item.trip_id === tripId)
                            ?.start_date
                        }
                        max={
                          trips.find((item) => item.trip_id === tripId)
                            ?.end_date
                        }
                        onChange={(event) => setDayDate(event.target.value)}
                        className="app-field"
                      />
                    </label>
                    {merchantId && (
                      <label className="grid gap-2 text-sm font-bold">
                        {common("cardActions.meal")}
                        <select
                          value={mealRole}
                          onChange={(event) =>
                            setMealRole(
                              event.target.value as "lunch" | "dinner",
                            )
                          }
                          className="app-field"
                        >
                          <option value="lunch">{common("cardActions.lunch")}</option>
                          <option value="dinner">{common("cardActions.dinner")}</option>
                        </select>
                      </label>
                    )}
                    <button
                      type="button"
                      disabled={busy}
                      onClick={() => void submitTrip()}
                      className="min-h-12 rounded-2xl bg-[var(--teal)] px-5 font-bold text-white disabled:opacity-50"
                    >
                      {common("cardActions.confirm")}
                    </button>
                  </div>
                )}
              </div>
            )}
          </section>
        </div>, document.body
      )}
    </>
  );
}
