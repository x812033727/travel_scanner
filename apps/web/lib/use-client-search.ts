"use client";

import { useSyncExternalStore } from "react";

const subscribeToNothing = () => () => {};

/**
 * The query string only exists in the browser. Reading it through useSyncExternalStore keeps
 * server rendering and hydration consistent: the server snapshot is null, and the client value
 * arrives on the first client render without a mount effect.
 */
export function useClientSearch(): string | null {
  return useSyncExternalStore(
    subscribeToNothing,
    () => window.location.search,
    () => null,
  );
}
