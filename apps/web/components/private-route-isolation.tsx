"use client";

import { usePathname } from "next/navigation";
import { useEffect } from "react";
import { documentNavigation, hasThirdPartyScript, isPrivateRoute } from "@/lib/private-routes";

const RELOADED_KEY = "travel:private-route-reload";

/**
 * Keeps a private page out of any document a third-party script has already run in.
 *
 * `TravelpayoutsDrive` and `AnalyticsProvider` refuse to load their scripts on a private route,
 * but that only helps a document that starts there. A reader who opens an article (script
 * loaded) and then taps "My trips" would otherwise carry the script into the trip page, because
 * the app router swaps pages inside the same document. So:
 *
 * - a same-origin link into a private section becomes a full load, before the router renders
 *   anything (the capture listener runs ahead of `Link`, which skips a prevented click);
 * - a navigation no link started (`router.push` after saving a trip, say) has already rendered
 *   when the pathname changes, so the page reloads once to finish the visit in a clean document.
 */
export function PrivateRouteIsolation() {
  const pathname = usePathname();

  useEffect(() => {
    const click = (event: MouseEvent) => {
      if (event.defaultPrevented || event.button !== 0) return;
      if (event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const anchor = event.target instanceof Element ? event.target.closest("a[href]") : null;
      if (!(anchor instanceof HTMLAnchorElement) || anchor.hasAttribute("download")) return;
      if (anchor.target && anchor.target !== "_self") return;
      const url = new URL(anchor.href, location.href);
      if (url.origin !== location.origin || !isPrivateRoute(url.pathname) || !hasThirdPartyScript()) return;
      event.preventDefault();
      documentNavigation.assign(url.href);
    };
    document.addEventListener("click", click, true);
    return () => document.removeEventListener("click", click, true);
  }, []);

  useEffect(() => {
    if (!isPrivateRoute(pathname)) return;
    try {
      if (!hasThirdPartyScript()) {
        // A clean document: whatever reload led here did its job.
        sessionStorage.removeItem(RELOADED_KEY);
        return;
      }
      // Once per path: if something still loads a script on a private page, reloading again
      // would never end. The page stays usable; only the isolation is lost.
      if (sessionStorage.getItem(RELOADED_KEY) === pathname) return;
      sessionStorage.setItem(RELOADED_KEY, pathname);
    } catch {
      return;
    }
    documentNavigation.reload();
  }, [pathname]);

  return null;
}
