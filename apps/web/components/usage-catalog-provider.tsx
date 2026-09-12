"use client";

import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import { defaultUsageCatalog, type UsageCatalogState, type UsageOperation } from "@/lib/usage-catalog";

const UsageCatalogContext = createContext<UsageCatalogState>({
  status: "ready",
  catalog: defaultUsageCatalog,
});

export function UsageCatalogProvider({
  state,
  children,
}: {
  state: UsageCatalogState;
  children: ReactNode;
}) {
  return <UsageCatalogContext.Provider value={state}>{children}</UsageCatalogContext.Provider>;
}

export function useUsageCatalog() {
  return useContext(UsageCatalogContext);
}

export function useOperationCharge(operation: UsageOperation) {
  const state = useUsageCatalog();
  const t = useTranslations("usage");
  const uses = state.status === "ready" ? state.catalog.operation_costs[operation] : null;
  return {
    status: state.status,
    uses,
    label: uses === null ? t("unavailable") : uses === 0 ? t("free") : t("charge", { uses }),
    unavailableHelp: t("unavailableHelp"),
  };
}

/**
 * What the member has left, as opposed to what an action costs.
 *
 * useOperationCharge answers "this will cost two uses"; nothing answered "you have
 * three" or "you are on your twentieth saved trip" until the request came back 402
 * or 403 — after the form was filled in, and in the search wizard's case after a
 * charge had already been spent. /usage returns the balance, the caps and the
 * current counts in one response, so one request covers both questions.
 */
export type AccountUsage = {
  status: "loading" | "ready" | "unavailable";
  availableUses: number | null;
  savedTrips: number | null;
  savedTripLimit: number | null;
};

type UsageResponse = {
  available_uses?: number;
  limits?: Record<string, number>;
  counts?: Record<string, number>;
};

const LOADING: AccountUsage = {
  status: "loading",
  availableUses: null,
  savedTrips: null,
  savedTripLimit: null,
};

export function useAccountUsage(enabled = true): AccountUsage {
  const [usage, setUsage] = useState<AccountUsage>(LOADING);
  useEffect(() => {
    // Nobody signed in means nobody to ask about: the layout makes the same call
    // for /auth/me and /saved-items rather than collecting a 401 on every visit.
    if (!enabled) return;
    let active = true;
    api<UsageResponse>("/usage")
      .then((summary) => {
        if (!active) return;
        setUsage({
          status: "ready",
          availableUses: typeof summary.available_uses === "number" ? summary.available_uses : null,
          savedTrips: typeof summary.counts?.saved_trips === "number" ? summary.counts.saved_trips : null,
          savedTripLimit: typeof summary.limits?.saved_trips === "number" ? summary.limits.saved_trips : null,
        });
      })
      .catch(() => {
        // A balance nobody can read must not block the form: the server still
        // enforces both caps, so an unreadable summary degrades to saying so.
        if (active) setUsage({ ...LOADING, status: "unavailable" });
      });
    return () => {
      active = false;
    };
  }, [enabled]);
  return usage;
}

/** True only when the cap is known and reached, never when the summary is missing. */
export function savedTripsAtCapacity(usage: AccountUsage) {
  return (
    usage.status === "ready"
    && usage.savedTrips !== null
    && usage.savedTripLimit !== null
    && usage.savedTrips >= usage.savedTripLimit
  );
}
