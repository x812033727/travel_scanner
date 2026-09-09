"use client";
import { createContext, useContext, useEffect, useState, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { useSearchParams } from "next/navigation";
import { useLocale } from "next-intl";
import { usePathname, useRouter } from "@/i18n/navigation";
import { Dialog } from "@/components/community/ui";
import { discoveryKinds } from "@/lib/discovery";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import { DiscoveryDetails } from "./card";
import styles from "./discovery.module.css";
const Navigation = createContext<{ remember: (trigger: HTMLElement, href: string) => void } | null>(null);
export function useDiscoveryDetailNavigation() { return useContext(Navigation); }
export function DiscoveryDetailBoundary({ children }: { children: ReactNode }) {
  const params = useSearchParams(); const pathname = usePathname(); const router = useRouter(); const c = getDiscoveryCopy(useLocale());
  const [origin, setOrigin] = useState<{ trigger: HTMLElement; href: string } | null>(null);
  const identifier = params.get("content"); const [kind, id] = identifier?.split(":") || [];
  const valid = discoveryKinds.includes(kind as typeof discoveryKinds[number]) && /^[a-f0-9-]{36}$/i.test(id || "");
  const returnTo = `${pathname}${params.size ? `?${params}` : ""}`;
  function close() {
    if (origin?.href === returnTo) router.back();
    else { const next = new URLSearchParams(params); next.delete("content"); router.replace(`${pathname}${next.size ? `?${next}` : ""}`, { scroll: false }); }
  }
  return <Navigation.Provider value={{ remember: (trigger, href) => setOrigin({ trigger, href }) }}>{children}{identifier && valid && <Drawer title={c.details} onClose={close} trigger={origin?.trigger}><DiscoveryDetails key={`${kind}:${id}`} kind={kind} id={id} returnTo={returnTo} /></Drawer>}{identifier && !valid && <p role="alert">{c.unavailable}</p>}</Navigation.Provider>;
}
function Drawer({ title, onClose, trigger, children }: { title: string; onClose: () => void; trigger?: HTMLElement; children: ReactNode }) {
  useEffect(() => { const previous = document.body.style.overflow; document.body.style.overflow = "hidden"; return () => { document.body.style.overflow = previous; }; }, []);
  if (typeof document === "undefined") return null;
  return createPortal(<div className={styles.drawer}><Dialog title={title} returnFocusTo={trigger} onClose={onClose}>{children}</Dialog></div>, document.body);
}
