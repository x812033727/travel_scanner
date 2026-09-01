"use client";

import { createContext, useContext, type ReactNode } from "react";
import { useTranslations } from "next-intl";
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
