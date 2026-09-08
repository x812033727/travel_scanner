"use client";

import { useCallback, useEffect, useState, useSyncExternalStore } from "react";
import { usePathname, useSearchParams } from "next/navigation";
import { useRouter } from "@/i18n/navigation";

type Destination = { tab: string; section?: string; pathname?: string };
export type AdminWorkspaceConfig = {
  tabs: Record<string, readonly string[]>;
  defaultTab: string;
  legacy?: Record<string, Destination>;
};
const eventName = "admin:location-change";
function subscribe(listener: () => void) {
  window.addEventListener("popstate", listener);
  window.addEventListener("hashchange", listener);
  window.addEventListener(eventName, listener);
  return () => {
    window.removeEventListener("popstate", listener);
    window.removeEventListener("hashchange", listener);
    window.removeEventListener(eventName, listener);
  };
}
const snapshot = () => window.location.href;
const serverSnapshot = () => "";

/** Pure URL adapter. Retains locale and unrelated filters when upgrading old bookmarks. */
export function resolveAdminWorkspaceLocation(raw: string, config: AdminWorkspaceConfig) {
  const url = new URL(raw || "https://admin.invalid/");
  const requested = url.searchParams.get("tab") || "";
  const hash = url.hash.slice(1);
  const alias = !Object.hasOwn(config.tabs, requested) ? config.legacy?.[hash] ?? config.legacy?.[requested] : undefined;
  const tab = alias?.tab ?? (Object.hasOwn(config.tabs, requested) ? requested : config.defaultTab);
  const sections = config.tabs[tab] ?? [];
  const desired = alias?.section ?? url.searchParams.get("section") ?? "";
  const section = sections.includes(desired) ? desired : sections[0] ?? "";
  if (alias?.pathname) {
    const localePrefix = url.pathname.split("/admin")[0];
    url.pathname = localePrefix + alias.pathname;
  }
  url.searchParams.set("tab", tab);
  if (section) url.searchParams.set("section", section);
  else url.searchParams.delete("section");
  if (config.legacy?.[hash]) url.hash = "";
  // Cross-workspace aliases carry destination sections, not this workspace's sections.
  if (alias?.pathname && alias.section) url.searchParams.set("section", alias.section);
  return { tab, section, url, redirect: Boolean(alias?.pathname) };
}

export function adminNavigate(url: URL, replace = false) {
  if (!window.dispatchEvent(new CustomEvent("admin:before-navigate", { cancelable: true, detail: { url: url.href } }))) return false;
  window.history[replace ? "replaceState" : "pushState"](null, "", url);
  window.dispatchEvent(new Event(eventName));
  return true;
}

export function useAdminWorkspaceNavigation(config: AdminWorkspaceConfig) {
  // Next's native-history integration also catches same-route <Link> transitions.
  const search = useSearchParams();
  const pathname = usePathname();
  const [ownerPath] = useState(pathname);
  const router = useRouter();
  const raw = useSyncExternalStore(subscribe, snapshot, serverSnapshot);
  const browser = new URL(raw || "https://admin.invalid/");
  const route = new URL(browser);
  // Next renders the destination before committing window.location. Using the
  // old browser URL here can reset a deep link or let an outgoing workspace
  // overwrite the incoming workspace's query with its own defaults.
  route.pathname = pathname ?? browser.pathname;
  route.search = search?.toString() ?? browser.search;
  if (route.pathname !== browser.pathname) route.hash = "";
  const ownsRoute = pathname === ownerPath;
  const routeSearch = route.searchParams.toString();
  const { tab, section, url, redirect } = resolveAdminWorkspaceLocation(route.href, config);
  const canonical = url.pathname + url.search + url.hash;
  useEffect(() => {
    window.dispatchEvent(new Event(eventName));
  }, [search, pathname]);
  useEffect(() => {
    // A popstate may commit between render and this effect. Never let an old
    // render normalize a newer browser entry (especially rapid mobile Back).
    const committed = new URL(window.location.href);
    if (!raw || !ownsRoute || route.pathname !== committed.pathname
      || routeSearch !== committed.searchParams.toString() || route.hash !== committed.hash) return;
    if (redirect) {
      if (window.dispatchEvent(new CustomEvent("admin:before-navigate", { cancelable: true, detail: { url: canonical } }))) {
        // next-intl owns the locale; the URL adapter already retained it for native history.
        router.replace(canonical.replace(/^\/(?:en|ja|ko|zh-TW|zh-CN)(?=\/admin)/, ""));
      }
    } else if (canonical !== window.location.pathname + window.location.search + window.location.hash) {
      adminNavigate(new URL(canonical, window.location.origin), true);
    }
  }, [canonical, raw, redirect, router, ownsRoute, route.pathname, routeSearch, route.hash]);
  const selectTab = useCallback((next: string) => {
    if (!Object.hasOwn(config.tabs, next)) return;
    const target = new URL(window.location.href);
    target.searchParams.set("tab", next);
    const first = config.tabs[next][0];
    if (first) target.searchParams.set("section", first);
    else target.searchParams.delete("section");
    target.hash = "";
    adminNavigate(target);
  }, [config]);
  const selectSection = useCallback((next: string) => {
    if (!config.tabs[tab]?.includes(next)) return;
    const target = new URL(window.location.href);
    target.searchParams.set("tab", tab);
    target.searchParams.set("section", next);
    target.hash = "";
    adminNavigate(target);
  }, [config, tab]);
  return { tab, section, ready: Boolean(raw) && ownsRoute && !redirect, selectTab, selectSection, query: url.searchParams };
}
