"use client";

import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { AdminBootstrap } from "@/lib/admin-operations";

type AdminOperationsContextValue = {
  bootstrap: AdminBootstrap;
  sidebarCollapsed: boolean;
  setSidebarCollapsed: (value: boolean) => void;
  commandOpen: boolean;
  setCommandOpen: (value: boolean) => void;
};

const AdminOperationsContext = createContext<AdminOperationsContextValue | null>(null);

export function AdminOperationsProvider({ bootstrap, children }: { bootstrap: AdminBootstrap; children: ReactNode }) {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [commandOpen, setCommandOpen] = useState(false);
  const value = useMemo(
    () => ({ bootstrap, sidebarCollapsed, setSidebarCollapsed, commandOpen, setCommandOpen }),
    [bootstrap, commandOpen, sidebarCollapsed],
  );
  return <AdminOperationsContext.Provider value={value}>{children}</AdminOperationsContext.Provider>;
}

export function useAdminOperations() {
  return useContext(AdminOperationsContext);
}
