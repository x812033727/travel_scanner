"use client";

import { useLocale } from "next-intl";
import { usePathname } from "next/navigation";
import Script from "next/script";
import { useCallback, useEffect, useRef, useState } from "react";
import { ANALYTICS_SESSION_KEY, type AnalyticsEventName } from "@/lib/analytics";
import { isPrivateRoute } from "@/lib/private-routes";
import { useThirdPartyAudience } from "@/lib/third-party-audience";

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

const SESSION_KEY = ANALYTICS_SESSION_KEY;
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

// A published article's slug is public and is the one long segment the reports must tell
// apart, so these two shapes keep it; any other long segment may be a share token or an id.
// The API's `normalize_path` (apps/api/app/analytics/service.py) applies the same rule.
const articlePath = /^\/(?:(?:en|ja|ko|zh-TW|zh-CN)\/)?(?:guides\/(?:intel|howto)|life)\/[a-z0-9]+(?:-[a-z0-9]+)*\/?$/;

function sanitizedPath(pathname: string) {
  if (/\/(?:[^/]+\/)?admin(?:\/|$)/.test(pathname)) return null;
  if (articlePath.test(pathname)) return pathname.slice(0, 512);
  return pathname.replace(/[0-9a-f]{8}-[0-9a-f-]{27,}/gi, ":id").replace(/[A-Za-z0-9_-]{20,}/g, ":id").slice(0, 512);
}

type Campaign = { utm_source?: string; utm_medium?: string; utm_campaign?: string };

function initialCampaign(): Campaign {
  const params = new URLSearchParams(location.search);
  const safe = (name: string) => params.get(name)?.replace(/[^A-Za-z0-9._+\-/ ]/g, "").slice(0, 100) || undefined;
  return { utm_source: safe("utm_source"), utm_medium: safe("utm_medium"), utm_campaign: safe("utm_campaign") };
}

/**
 * The `page_location` GA4 is given: the sanitized path, plus the landing's campaign tags when
 * a caller passes them.
 *
 * GA4 reads a session's campaign from the `utm_*` parameters of this URL, not from the page
 * the reader actually opened, so a location without them files a video or newsletter visit
 * under its referrer at best. Only the three tags `initialCampaign` has already cleaned are ever
 * added: every other parameter of the real URL — search terms, ids, click identifiers — stays
 * out of GA4 as before.
 */
function ga4Location(path: string, campaign: Campaign | null = null) {
  const tags = new URLSearchParams();
  for (const [name, value] of Object.entries(campaign ?? {})) if (value) tags.set(name, value);
  const query = tags.toString();
  return `${location.origin}${path}${query ? `?${query}` : ""}`;
}

function initializeGa4(measurementId: string, campaign: Campaign) {
  window.dataLayer = window.dataLayer || [];
  window.gtag = (...args: unknown[]) => { window.dataLayer?.push(args); };
  window.gtag("consent", "default", { analytics_storage: "denied", ad_storage: "denied", ad_user_data: "denied", ad_personalization: "denied" });
  window.gtag("set", "ads_data_redaction", true);
  window.gtag("js", new Date());
  const cleanLocation = ga4Location(sanitizedPath(location.pathname) || "/", campaign);
  window.gtag("config", measurementId, { send_page_view: false, page_location: cleanLocation, allow_google_signals: false, allow_ad_personalization_signals: false });
}

function sendGa4Event(name: AnalyticsEventName, path: string, language: string, campaign: Campaign | null = null) {
  const mapped = { registration_completed: "sign_up", search_completed: "search", outbound_click: "click", page_view: "page_view", discover_requested: "generate_lead", login_resumed: "login" }[name];
  window.gtag?.("event", mapped, { page_path: path, page_location: ga4Location(path, campaign), language, transport_type: "beacon" });
}

export function AnalyticsProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const locale = useLocale();
  const [config, setConfig] = useState<Config | null>(null);
  const queue = useRef<PendingEvent[]>([]);
  const campaign = useRef<Campaign | null>(null);
  const lastPage = useRef<string | null>(null);
  const ga4Started = useRef(false);
  const ga4CampaignSent = useRef(false);
  // The landing's campaign rides on the first page view GA4 is sent in this document: that is
  // the view GA4 takes the session's source from, and the pages after it were reached from
  // inside the site, the way an ordinary address bar shows the tags on the landing page only.
  const ga4Campaign = useCallback((name: AnalyticsEventName) => {
    if (name !== "page_view" || ga4CampaignSent.current) return null;
    ga4CampaignSent.current = true;
    return campaign.current;
  }, []);
  // gtag.js is a third-party script: it stays off private pages (`lib/private-routes.ts`), and
  // a document that starts on one only brings it in once the reader reaches a public page. It
  // never loads for an administrator, and waits while a signed-in reader's role is unknown
  // (`lib/third-party-audience.ts`).
  const audience = useThirdPartyAudience();
  const ga4Allowed = audience === "allowed" && !isPrivateRoute(pathname);
  // The ID is admin-controlled: only a well-formed GA4 measurement ID may reach the script URL.
  const measurementId = config?.ga4_enabled && /^G-[A-Z0-9]{4,20}$/.test(config.ga4_measurement_id || "")
    ? config.ga4_measurement_id
    : null;

  useEffect(() => {
    if (config || privacyOptOut() || !sanitizedPath(pathname)) return;
    fetch("/api/travel/analytics/config", { cache: "no-store" })
      .then((response) => response.ok ? response.json() as Promise<Config> : null)
      .then((value) => {
        if (value) setConfig(value);
      })
      .catch(() => undefined);
  }, [config, pathname]);

  // Before the page-view effect below, so the first page view already finds `window.gtag`.
  // When GA4 starts later than that (a signed-in reader, cleared once `/auth/me` answers), the
  // page view already sent first-party is sent to GA4 as well, once.
  useEffect(() => {
    if (!measurementId || !ga4Allowed || ga4Started.current || privacyOptOut()) return;
    ga4Started.current = true;
    if (!campaign.current) campaign.current = initialCampaign();
    initializeGa4(measurementId, campaign.current);
    if (lastPage.current) sendGa4Event("page_view", lastPage.current, allowedLocales.has(locale) ? locale : "zh-TW", ga4Campaign("page_view"));
  }, [ga4Allowed, ga4Campaign, locale, measurementId]);

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
    if (config.ga4_enabled && config.ga4_measurement_id && window.gtag && ga4Allowed) {
      sendGa4Event(name, path, event.locale, ga4Campaign(name));
    }
  }, [config, flush, ga4Allowed, ga4Campaign, locale, pathname]);

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

  return <>
    {measurementId && !privacyOptOut() && ga4Allowed && <Script src={`https://www.googletagmanager.com/gtag/js?id=${measurementId}`} strategy="afterInteractive" />}
    {children}
  </>;
}
