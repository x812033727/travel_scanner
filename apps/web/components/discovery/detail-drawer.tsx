"use client";
import { createContext, useCallback, useContext, useEffect, useRef, useState, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "next/navigation";
import { useLocale } from "next-intl";
import { usePathname, useRouter } from "@/i18n/navigation";
import { Dialog } from "@/components/community/ui";
import { discoveryKinds } from "@/lib/discovery";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import { isTopModalLayer } from "@/lib/modal-sheet";
import { DiscoveryDetails } from "./card";
import styles from "./discovery.module.css";
type DetailNavigation = {
  remember: (trigger: HTMLElement, href: string) => void;
  restoreDetails: (element: HTMLDivElement | null) => void;
};
const Navigation = createContext<DetailNavigation | null>(null);
export function useDiscoveryDetailNavigation() { return useContext(Navigation); }
export function DiscoveryDetailBoundary({ children }: { children: ReactNode }) {
  const params = useSearchParams(); const pathname = usePathname(); const router = useRouter(); const c = getDiscoveryCopy(useLocale());
  const [origin, setOrigin] = useState<HTMLElement>();
  // Only links opened inside this boundary may close through browser history.
  // Direct URLs remove content locally rather than navigating off-site.
  const ownedRoutes = useRef(new Set<string>());
  const positions = useRef(new Map<string, { target: string; scrollTop: number }>());
  const closingRoute = useRef<string | null>(null);
  const identifier = params.get("content"); const [kind, id] = identifier?.split(":") || [];
  const valid = discoveryKinds.includes(kind as typeof discoveryKinds[number]) && /^[a-f0-9-]{36}$/i.test(id || "");
  const returnTo = `${pathname}${params.size ? `?${params}` : ""}`;
  useEffect(() => { closingRoute.current = null; }, [returnTo]);
  const restoreDetails = useCallback((element: HTMLDivElement | null) => {
    if (!element) return;
    // The parent detail reloads asynchronously; restore focus against its new DOM.
    const previous = positions.current.get(returnTo);
    requestAnimationFrame(() => {
      if (!element.isConnected) return;
      const target = previous && Array.from(element.querySelectorAll<HTMLElement>("[data-discovery-detail-target]"))
        .find((link) => link.dataset.discoveryDetailTarget === previous.target);
      (target || element.querySelector<HTMLElement>("h2"))?.focus({ preventScroll: true });
      element.scrollTop = previous?.scrollTop ?? 0;
    });
  }, [returnTo]);
  function remember(trigger: HTMLElement, href: string) {
    if (!identifier) {
      closingRoute.current = null;
      ownedRoutes.current.clear();
      setOrigin(trigger);
      positions.current.clear();
    } else {
      positions.current.set(returnTo, {
        target: trigger.dataset.discoveryDetailTarget || "",
        scrollTop: trigger.closest("[data-discovery-detail-body]")?.scrollTop || 0,
      });
    }
    ownedRoutes.current.add(href);
  }
  function close() {
    // Native cancel/close pairs and rapid taps must consume only one history entry.
    // The next committed route (or a fresh list journey) permits the next dismissal.
    if (closingRoute.current === returnTo) return;
    closingRoute.current = returnTo;
    if (ownedRoutes.current.has(returnTo)) router.back();
    else { const next = new URLSearchParams(params); next.delete("content"); router.replace(`${pathname}${next.size ? `?${next}` : ""}`, { scroll: false }); }
  }
  return <Navigation.Provider value={{ remember, restoreDetails }}>{children}{identifier && valid && <Drawer title={c.details} onClose={close} trigger={origin}><DiscoveryDetails key={`${kind}:${id}`} kind={kind} id={id} returnTo={returnTo} /></Drawer>}{identifier && !valid && <p role="alert">{c.unavailable}</p>}</Navigation.Provider>;
}
function Drawer({ title, onClose, trigger, children }: { title: string; onClose: () => void; trigger?: HTMLElement; children: ReactNode }) {
  if (typeof document === "undefined") return null;
  return createPortal(<div className={styles.drawer} onKeyDown={(event) => {
    if (event.key !== "Escape" || event.defaultPrevented || event.nativeEvent.isComposing) return;
    const dialog = event.currentTarget.querySelector<HTMLDialogElement>(":scope > dialog");
    if (!dialog || !isTopModalLayer(dialog)) return;
    // Consume the keyboard default before CloseWatcher can emit a non-cancelable
    // cancel followed by close. A nested detail stays in the same open dialog.
    event.preventDefault();
    event.stopPropagation();
    onClose();
  }}><Dialog title={title} returnFocusTo={trigger} onClose={onClose}>{children}</Dialog></div>, document.body);
}
