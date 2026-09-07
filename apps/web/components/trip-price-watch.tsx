"use client";

import { Bell, Check } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { Link } from "@/i18n/navigation";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { ApiError, api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { featureEnabled } from "@/lib/site-features";
import type { Trip } from "@/lib/trip-types";

/**
 * Watch the prices this trip actually has.
 *
 * A trip-level alert used to track `trip.total_price`, a number that mixes real
 * quotes with estimates and that no provider re-checks — so it could only ever be
 * "manual_only". What can be watched is each quoted offer the trip holds, so this
 * creates one alert per offer and says so. With nothing quoted there is nothing to
 * watch, and the button explains that instead of making a promise it cannot keep.
 */
export function TripPriceWatch({ trip }: { trip: Trip }) {
  const t = useTranslations("trips");
  const visibility = useSiteVisibility();
  const [busy, setBusy] = useState(false);
  const [watching, setWatching] = useState(0);
  const [error, setError] = useState("");
  const [loginRequired, setLoginRequired] = useState(false);

  // A round-trip offer sits on both flight anchors under one id, and the hotel is
  // watched as a hotel — the kind the pricing row already carries decides which.
  const offers = Array.from(
    new Map(
      (trip.pricing?.items || [])
        .filter((item) => Boolean(item.offer_id))
        .map((item) => [`${item.kind}:${item.offer_id}`, { kind: item.kind, id: item.offer_id as string }]),
    ).values(),
  );

  async function watch() {
    setBusy(true);
    setError("");
    setLoginRequired(false);
    const results = await Promise.all(
      offers.map((offer) =>
        api("/alerts", {
          method: "POST",
          body: JSON.stringify({ resource_type: offer.kind, resource_id: offer.id }),
        })
          .then(() => "created" as const)
          .catch((reason) => reason),
      ),
    );
    // An offer already being watched is the outcome this button wants, not a failure.
    const settled = results.filter(
      (result) => result === "created" || (result instanceof ApiError && result.code === "alert_exists"),
    ).length;
    const refused = results.find((result) => result instanceof ApiError && result.status === 401);
    const failure = results.find(
      (result) => result instanceof ApiError && result.status !== 401 && result.code !== "alert_exists",
    );
    if (refused) setLoginRequired(true);
    else if (settled) setWatching(settled);
    if (failure instanceof Error && !settled) setError(failure.message);
    setBusy(false);
  }

  if (!featureEnabled(visibility, "alerts")) return null;
  if (!offers.length) {
    return <p className="text-sm leading-6 text-[var(--muted)]">{t("watchNothingQuoted")}</p>;
  }
  if (watching) {
    return <p role="status" className="flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-800">
      <Check size={16} />{t("watchCreated", { count: watching })}
      <Link className="underline" href="/alerts">{t("watchManage")}</Link>
    </p>;
  }
  return <div>
    <button type="button" onClick={() => void watch()} disabled={busy} className="flex w-full items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold text-[var(--teal)] disabled:opacity-60">
      <Bell size={16} />{busy ? t("watchCreating") : t("watchQuoted", { count: offers.length })}
    </button>
    {loginRequired && <p role="alert" className="mt-2 text-sm text-red-700">
      {t("watchSignIn")}
      <Link className="ml-1 font-semibold underline" href={loginPath(`/trips/${trip.id}`)}>{t("backToTrip")}</Link>
    </p>}
    {error && <p role="alert" className="mt-2 text-sm text-red-700">{error}</p>}
  </div>;
}
