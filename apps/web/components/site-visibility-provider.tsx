"use client";

import { createContext, useContext, type ReactNode } from "react";
import {
  openSiteVisibility,
  type SiteVisibilityState,
} from "@/lib/site-features";

const SiteVisibilityContext = createContext<SiteVisibilityState>({
  status: "ready",
  features: openSiteVisibility,
});

export function SiteVisibilityProvider({
  state,
  children,
}: {
  state: SiteVisibilityState;
  children: ReactNode;
}) {
  return <SiteVisibilityContext.Provider value={state}>{children}</SiteVisibilityContext.Provider>;
}

export function useSiteVisibility() {
  return useContext(SiteVisibilityContext);
}
