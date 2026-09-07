"use client";

import { AlertCircle, CalendarPlus, Check, Heart, LoaderCircle, LogIn, Share2, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { Link, usePathname } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { useSavedItems, type SavedType } from "@/components/saved-items-provider";

type TripOption = {
  trip_id: string;
  name: string;
  version: number;
  start_date: string;
  end_date: string;
  destination_name?: string | null;
};
export function TravelCardActions({
  type,
  id,
  title,
  selectionPath,
  merchantId,
  shareRequiresAuth = false,
}: {
  type: SavedType;
  id: string;
  title: string;
  selectionPath: string;
  merchantId?: string;
  shareRequiresAuth?: boolean;
}) {
  const common = useTranslations("common");
  const savedItems = useSavedItems();
  const pathname = usePathname();
  const saved = savedItems.isSaved(type, id);
  const [sheet, setSheet] = useState<"login" | "trip" | null>(null);
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

  function requireAuth(action: () => void) {
    // "loading" is not "signed out". Acting on it threw an already-signed-in
    // reader into the login sheet whenever they tapped before /saved-items
    // came back, which on a phone is most of the time.
    if (savedItems.status === "loading") return;
    if (savedItems.status !== "authenticated") {
      setLoginHref(loginPath(`${pathname}${window.location.search}`));
      setSheet("login");
    }
    else action();
  }
  async function openTrip() {
    clearFeedback();
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
          onClick={() => requireAuth(() => void toggleSaved())}
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
          onClick={() => requireAuth(() => void openTrip())}
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
      {sheet && (
        <div
          className="app-sheet-backdrop"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setSheet(null);
          }}
        >
          <section
            role="dialog"
            aria-modal="true"
            aria-label={sheet === "login" ? common("cardActions.login") : common("cardActions.trip")}
            className="app-sheet"
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
            ) : (
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
        </div>
      )}
    </>
  );
}
