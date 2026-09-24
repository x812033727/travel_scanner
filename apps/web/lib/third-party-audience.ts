import { useSyncExternalStore } from "react";

/**
 * Whether the reader in this document may share it with a third-party script.
 *
 * An administrator never does. Cookies follow the request, not the page, so a vendor script
 * running on any page of an administrator's browser (an article, the home page) can call the
 * admin API same-origin and read the answer; keeping the scripts off the admin pages
 * (`lib/private-routes.ts`) does not stop that. The only document such a script cannot abuse
 * is one it never loaded into.
 *
 * - `pending`: not known yet (a session cookie exists and `/auth/me` has not answered).
 * - `allowed`: signed out, or signed in without admin rights.
 * - `blocked`: an administrator, or a signed-in reader whose role this document cannot know.
 *
 * Set by `components/third-party-audience.tsx`, read by `TravelpayoutsDrive` and
 * `AnalyticsProvider`. A module store rather than context because both readers sit above the
 * session provider in the layout.
 */
export type ThirdPartyAudience = "pending" | "allowed" | "blocked";

let audience: ThirdPartyAudience = "pending";
const listeners = new Set<() => void>();

/**
 * `blocked` is final for the document. The session provider remounts on sign-in and sign-out,
 * so this cannot live in component state: an administrator signing out in place must not let
 * a vendor script into a page that was just showing admin data.
 */
export function setThirdPartyAudience(next: ThirdPartyAudience) {
  if (next === audience || audience === "blocked") return;
  audience = next;
  listeners.forEach((listener) => listener());
}

/** Tests only: the module-level state outlives a single case otherwise. */
export function resetThirdPartyAudience(): void {
  audience = "pending";
  listeners.forEach((listener) => listener());
}

function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

export function useThirdPartyAudience(): ThirdPartyAudience {
  return useSyncExternalStore(subscribe, () => audience, () => "pending");
}
