"use client";

import { useLocale } from "next-intl";
import { usePathname } from "next/navigation";
import Script from "next/script";
import { useCallback, useEffect, useRef, useState } from "react";
import type { AnalyticsEventName } from "@/lib/analytics";

type Config = { first_party_enabled: boolean; ga4_enabled: boolean; ga4_measurement_id?: string | null };
type PendingEvent = {
  event_id: string;
  name: AnalyticsEventName;
  occurred_at: string;
  path: string;
  locale: string;
  referrer?: string;
  utm_source?: string;
  utm_medium?: string;
  utm_campaign?: string;
};

declare global {
  interface Window {
    dataLayer?: unknown[][];
    gtag?: (...args: unknown[]) => void;
  }
}

const SESSION_KEY = "travel_analytics_session";
const allowedLocales = new Set(["en", "ja", "ko", "zh-TW", "zh-CN"]);

function privacyOptOut() {
  return navigator.doNotTrack === "1" || (navigator as Navigator & { globalPrivacyControl?: boolean }).globalPrivacyControl === true;
}

function sessionId() {
  let value = sessionStorage.getItem(SESSION_KEY);
  if (!value) {
    value = crypto.randomUUID();
    sessionStorage.setItem(SESSION_KEY, value);
  }
  return value;
}

function sanitizedPath(pathname: string) {
  if (/\/(?:[^/]+\/)?admin(?:\/|$)/.test(pathname)) return null;
  return pathname.replace(/[0-9a-f]{8}-[0-9a-f-]{27,}/gi, ":id").replace(/[A-Za-z0-9_-]{20,}/g, ":id").slice(0, 512);
}

function initialCampaign() {
  const params = new URLSearchParams(location.search);
  const safe = (name: string) => params.get(name)?.replace(/[^A-Za-z0-9._+\-/ ]/g, "").slice(0, 100) || undefined;
  return { utm_source: safe("utm_source"), utm_medium: safe("utm_medium"), utm_campaign: safe("utm_campaign") };
}

function initializeGa4(measurementId: string) {
  window.dataLayer = window.dataLayer || [];
  window.gtag = (...args: unknown[]) => { window.dataLayer?.push(args); };
  window.gtag("consent", "default", { analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
  window.gtag("set", "ads_data_redaction", true);
  window.gtag("js", new Date());
  const cleanLocation = `${location.origin}${sanitizedPath(location.pathname) || "/"}`;
  window.gtag("config", measurementId, { send_page_view: false, page_location: cleanLocation, allow_google_signals: false, allow_ad_personalization_signals: false });
}

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const locale = useLocale();
  const [config, setConfig] = useState<Config | null>(null);
  const queue = useRef<PendingEvent[]>([]);
  const campaign = useRef<{ utm_source?: string; utm_medium?: string; utm_campaign?: string } | null>(null);
  const lastPage = useRef<string | null>(null);

  useEffect(() => {
    if (config || privacyOptOut() || !sanitizedPath(pathname)) return;
    fetch("/api/travel/analytics/config", { cache: "no-store" })
      .then((response) => response.ok ? response.json() as Promise<Config> : null)
      .then((value) => {
        if (!value) return;
        if (value.ga4_enabled && value.ga4_measurement_id) initializeGa4(value.ga4_measurement_id);
        setConfig(value);
      })
      .catch(() => undefined);
  }, [config, pathname]);

  const flush = useCallback((keepalive = false) => {
    if (!config?.first_party_enabled || queue.current.length === 0 || privacyOptOut()) return;
    const events = queue.current.splice(0, 20);
    fetch("/api/travel/analytics/events", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId(), events }),
      keepalive,
    }).catch(() => { /* Analytics never blocks product actions. */ });
  }, [config?.first_party_enabled]);

  const emit = useCallback((name: AnalyticsEventName) => {
    if (!config || privacyOptOut()) return;
    const path = sanitizedPath(pathname);
    if (!path) return;
    if (!campaign.current) campaign.current = initialCampaign();
    const event: PendingEvent = {
      event_id: crypto.randomUUID(),
      name,
      occurred_at: new Date().toISOString(),
      path,
      locale: allowedLocales.has(locale) ? locale : "zh-TW",
      referrer: document.referrer || undefined,
      ...campaign.current,
    };
    if (config.first_party_enabled) {
      queue.current.push(event);
      queueMicrotask(() => flush());
    }
    if (config.ga4_enabled && config.ga4_measurement_id && window.gtag) {
      const mapped = { registration_completed: "sign_up", search_completed: "search", trip_created: "trip_created", outbound_click: "click", page_view: "page_view" }[name];
      window.gtag("event", mapped, { page_path: path, page_location: `${location.origin}${path}`, language: event.locale, transport_type: "beacon" });
    }
  }, [config, flush, locale, pathname]);

  useEffect(() => {
    if (!config) return;
    const page = sanitizedPath(pathname);
    if (!page || lastPage.current === page) return;
    lastPage.current = page;
    emit("page_view");
  }, [config, emit, pathname]);

  useEffect(() => {
    if (!config || !document.cookie.split("; ").includes("travel_oauth_registered=1")) return;
    document.cookie = "travel_oauth_registered=; path=/; max-age=0; samesite=lax";
    emit("registration_completed");
  }, [config, emit]);

  useEffect(() => {
    const listener = (event: Event) => {
      const name = (event as CustomEvent<{ name?: AnalyticsEventName }>).detail?.name;
      if (name && name !== "page_view") emit(name);
    };
    const click = (event: MouseEvent) => {
      const target = event.target instanceof Element ? event.target.closest("a,form") : null;
      if (!target) return;
      const href = target instanceof HTMLAnchorElement ? target.href : target instanceof HTMLFormElement ? target.action : "";
      const opensNew = target.getAttribute("target") === "_blank";
      try {
        if (href && (opensNew || new URL(href, location.href).origin !== location.origin)) emit("outbound_click");
      } catch { /* Ignore malformed third-party links. */ }
    };
    window.addEventListener("travel:analytics", listener);
    document.addEventListener("click", click, true);
    return () => {
      window.removeEventListener("travel:analytics", listener);
      document.removeEventListener("click", click, true);
    };
  }, [emit]);

  useEffect(() => {
    const timer = window.setInterval(() => flush(), 5_000);
    const pageHide = () => flush(true);
    window.addEventListener("pagehide", pageHide);
    return () => { window.clearInterval(timer); window.removeEventListener("pagehide", pageHide); };
  }, [flush]);

  const measurementId = config?.ga4_enabled ? config.ga4_measurement_id : null;
  return <>
    {measurementId && !privacyOptOut() && <Script src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`} strategy="afterInteractive" />}
    {children}
  </>;
}
