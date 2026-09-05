"use client";

import { AlertCircle, LogIn, Route } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { ApiError, api } from "@/lib/api";
import { NewTripForm } from "@/components/new-trip-form";

type AuthState = "checking" | "authenticated" | "signed_out" | "unavailable" | "limit_reached";
type TripLimit = { count: number; limit: number };

// The API refuses the 21st trip only when the wizard is submitted; count the
// saved trips up front so the cap is explained before four steps of input.
async function savedTripLimit(): Promise<TripLimit | undefined> {
  const [trips, usage] = await Promise.all([
    api<unknown>("/trips").catch(() => undefined),
    api<{ limits?: { saved_trips?: unknown } }>("/usage").catch(() => undefined),
  ]);
  const limit = usage?.limits?.saved_trips;
  if (!Array.isArray(trips) || typeof limit !== "number") return undefined;
  return trips.length >= limit ? { count: trips.length, limit } : undefined;
}

export function NewTripAuthGate() {
  const t = useTranslations("newTrip.gate");
  const [state, setState] = useState<AuthState>("checking");
  const [tripLimit, setTripLimit] = useState<TripLimit>();

  useEffect(() => {
    let active = true;
    api("/auth/me")
      .then(async () => {
        const reached = await savedTripLimit();
        if (!active) return;
        setTripLimit(reached);
        setState(reached ? "limit_reached" : "authenticated");
      })
      .catch((reason) => {
        if (!active) return;
        setState(reason instanceof ApiError && reason.status === 401 ? "signed_out" : "unavailable");
      });
    return () => { active = false; };
  }, []);

  if (state === "checking") {
    return <div role="status" className="rounded-[2rem] border border-[var(--line)] bg-white p-8 text-[var(--muted)]">{t("checking")}</div>;
  }
  if (state === "signed_out") {
    return <section className="mx-auto max-w-xl rounded-[2rem] border border-[var(--line)] bg-white p-8 text-center shadow-[var(--shadow-lg)]">
      <LogIn className="mx-auto text-[var(--teal)]" size={36} />
      <h1 className="mt-4 text-3xl font-bold">{t("signInTitle")}</h1>
      <p className="mt-3 leading-7 text-[var(--muted)]">{t("signInBody")}</p>
      <Link href="/login" className="mt-6 inline-flex rounded-xl bg-[var(--teal)] px-6 py-3 font-semibold text-white">{t("signIn")}</Link>
    </section>;
  }
  if (state === "unavailable") {
    return <section role="alert" className="mx-auto max-w-xl rounded-[2rem] border border-red-200 bg-red-50 p-8 text-center text-red-900">
      <AlertCircle className="mx-auto" size={36} />
      <h1 className="mt-4 text-2xl font-bold">{t("unavailableTitle")}</h1>
      <p className="mt-3 leading-7">{t("unavailableBody")}</p>
    </section>;
  }
  if (state === "limit_reached" && tripLimit) {
    return <section className="mx-auto max-w-xl rounded-[2rem] border border-[var(--line)] bg-white p-8 text-center shadow-[var(--shadow-lg)]">
      <Route className="mx-auto text-[var(--teal)]" size={36} />
      <h1 className="mt-4 text-3xl font-bold">{t("limitTitle")}</h1>
      <p className="mt-3 leading-7 text-[var(--muted)]">{t("limitBody", { count: tripLimit.count, limit: tripLimit.limit })}</p>
      <Link href="/trips" className="mt-6 inline-flex rounded-xl bg-[var(--teal)] px-6 py-3 font-semibold text-white">{t("manageTrips")}</Link>
    </section>;
  }
  return <NewTripForm />;
}
