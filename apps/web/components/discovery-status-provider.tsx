"use client";

import { createContext, useContext, type ReactNode } from "react";

/**
 * Server-resolved discovery switch for the layout tree.
 *
 * Undefined outside the layout (for example in standalone unit tests), so
 * `resolveDiscoveryStatus(live, initialEnabled)` falls back to the client store
 * unchanged while every full-page SSR render immediately knows the switch state.
 */
const DiscoveryStatusContext = createContext<boolean | undefined>(undefined);

export function DiscoveryStatusProvider({
  initialEnabled,
  children,
}: {
  initialEnabled: boolean;
  children: ReactNode;
}) {
  return (
    <DiscoveryStatusContext.Provider value={initialEnabled}>
      {children}
    </DiscoveryStatusContext.Provider>
  );
}

export function useInitialDiscoveryEnabled(): boolean | undefined {
  return useContext(DiscoveryStatusContext);
}
