"use client";

import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useRef, useState } from "react";
import { Link, useRouter } from "@/i18n/navigation";
import { AdminReadOnlyNotice, useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminSettingsPanel } from "@/components/admin-settings-panel";
import { AdminMapIdentitiesPanel } from "@/components/admin-map-identities-panel";
import { useHeaderSession } from "@/components/header-session";
import { adminHotelsCopy } from "@/lib/admin-hotels-copy";
import { klookAffiliateCopy } from "@/lib/klook-affiliate-copy";
import { useAdminQueryValue, useAdminWorkspaceNavigation } from "@/lib/admin-workspace-navigation";
import { ApiError, api } from "@/lib/api";
import { CITIES, KINDS, type Kind } from "./catalog";
import { HotelOptionsAdmin, type HotelOptionRow } from "./hotel-options-admin";
import { QuotePolicies, type QuotePolicy } from "./quote-policies";
import { Stay22Admin, Stay22ReadinessPanel, type Stay22Config, type Stay22Readiness } from "./stay22-admin";

type RecordRow = {
  booking_options?: HotelOptionRow[];
  id: string;
  title: string;
  kind: Kind;
  source_key: string;
  source_url: string;
  names_json: Record<string, string>;
  destination_id: string;
  facts: Record<string, unknown>;
  status: string;
  version: number;
};
type AffiliateChannel = "travelpayouts" | "klook_direct";
type BrandRow = {
  id: string;
  code: string;
  channel?: AffiliateChannel;
  name: string;
  approval: string;
  enabled: boolean;
  evidence_url: string;
  verified_at: string | null;
  version: number;
};
type OfferRow = {
  id: string;
  product_id: string;
  brand_id: string;
  status: string;
  version: number;
  target_url: string;
  scope: string;
};
type AffiliateModule =
  | "flight"
  | "hotel"
  | "activities"
  | "transport"
  | "connectivity";
type DestinationOfferRow = {
  id: string;
  brand_id: string;
  destination_id: string;
  module: AffiliateModule;
  status: "pending" | "approved" | "disabled";
  version: number;
  target_url: string;
  static_url: string | null;
  verified_at: string | null;
};
type DestinationRow = {
  id: string;
  city: string;
  country: string;
  role: string;
};
type Config = {
  stay22?: Stay22Config;
  hotel_quote_policies?: Record<string, QuotePolicy>;
  public_enabled: boolean;
  direct_hotel_links_enabled?: boolean;
  enabled_kinds: Kind[];
  enabled_destinations: string[];
  airalo_feed_enabled: boolean;
};
type Overview = {
  can_manage_stay22?: boolean;
  stay22_readiness?: Stay22Readiness[];
  summary?: { total: number; pending: number; approved: number; disabled: number };
  quote_providers?: Record<string, { adapter_available: boolean }>;
  config: Config;
  version: number;
  products: RecordRow[];
  offers: OfferRow[];
  destination_offers: DestinationOfferRow[];
  destinations: DestinationRow[];
  brands: BrandRow[];
  project_id: string | null;
  network_configured: boolean;
  channels?: Partial<Record<AffiliateChannel, { configured: boolean; project_id: string | null }>>;
  review_due: number;
  hotel_option_review_due?: number;
  brand_definitions: Record<
    string,
    {
      name: string;
      kinds: Kind[];
      modules: AffiliateModule[];
      hosts: string[];
      api_supported: boolean;
    }
  >;
  coverage: {
    destination_id: string;
    counts: Record<Kind, number>;
    hotel_areas: number;
    hotel_ready?: number;
    hotel_complete?: boolean;
    complete: boolean;
  }[];
  operations: {
    ordinary_hotel_clicks?: number;
    affiliate_hotel_clicks?: number;
    hotel_affiliate_fallbacks?: number;
    outbound_clicks: number;
    self_reported_booked: number;
    confirmed_commission: null;
  };
  imports: {
    id: string;
    source: string;
    status: string;
    row_count: number;
    result_json: Record<string, unknown>;
  }[];
};
type Preview = {
  id: string;
  rows_json: {
    change?: string;
    missing_platforms?: string[];
    line: number;
    error?: string;
    product?: { title: string; kind: Kind; destination_id: string };
  }[];
};
const field =
  "mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3 text-sm";
const button =
  "min-h-11 rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-50";
type BrowserReview = { browser_verified: boolean; evidence_url: string };
function BrowserReviewFields({ value, target, onChange, disabled }: {
  value?: BrowserReview; target: string; onChange: (value: BrowserReview) => void; disabled: boolean;
}) {
  const copy = klookAffiliateCopy(useLocale());
  const current = value || { browser_verified: false, evidence_url: target };
  return <fieldset disabled={disabled} className="my-3 min-w-0 space-y-2 rounded-xl bg-[var(--paper)] p-3 text-sm">
    <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={current.browser_verified} onChange={(event) => onChange({ ...current, browser_verified: event.target.checked })} />{copy.browserVerified}</label>
    <p className="text-xs leading-5 text-[var(--muted)]">{copy.browserHint}</p>
    {current.browser_verified && <label className="block">{copy.browserEvidence}<input type="url" required className={field} value={current.evidence_url} onChange={(event) => onChange({ ...current, evidence_url: event.target.value })} /></label>}
  </fieldset>;
}

const hotelTabs = {
  catalog: ["catalog"], review: ["products", "platforms"],
  affiliates: ["products", "destinations"], imports: ["import", "coverage"],
  settings: ["catalog", "providers"],
};
const serviceTabs = {
  catalog: [], destinationOffers: [], importCsv: [], coverage: [], config: [],
};
const partnerTabs = { brands: [] };
const legacyServiceLinks = {
  hotel: { pathname: "/admin/hotels", tab: "catalog", section: "catalog" },
  hotels: { pathname: "/admin/hotels", tab: "catalog", section: "catalog" },
  brands: { pathname: "/admin/partners", tab: "brands" },
};
const hotelDraftKey = "mokaair:admin:hotel-config-draft:v1";
type HotelDraft = {
  version: number; hotel_enabled: boolean; direct_hotel_links_enabled: boolean;
  hotel_quote_policies: Record<string, QuotePolicy>;
};
function readHotelDraft(storageKey: string): HotelDraft | undefined {
  try {
    const draft = JSON.parse(sessionStorage.getItem(storageKey) || "null") as HotelDraft | null;
    if (!draft || !Number.isInteger(draft.version) || draft.version < 0 ||
      typeof draft.hotel_enabled !== "boolean" || typeof draft.direct_hotel_links_enabled !== "boolean" ||
      !draft.hotel_quote_policies || typeof draft.hotel_quote_policies !== "object" || Array.isArray(draft.hotel_quote_policies)) return;
    for (const [provider, policy] of Object.entries(draft.hotel_quote_policies)) {
      if (!["official", "booking", "trip_com", "agoda", "expedia", "rakuten", "klook", "kkday"].includes(provider) ||
        !policy || typeof policy.enabled !== "boolean" || typeof policy.comparison_allowed !== "boolean" ||
        !(policy.terms_url === null || typeof policy.terms_url === "string") ||
        ![policy.daily_limit, policy.per_minute_limit, policy.timeout_seconds, policy.cache_seconds].every(Number.isFinite)) return;
    }
    return draft;
  } catch { return; }
}

export function TravelServicesAdmin({ workspace = "services" }: {
  workspace?: "hotels" | "partners" | "services";
}) {
  const { user, status } = useHeaderSession();
  return <TravelServicesWorkspace key={user?.id ?? "anonymous"} workspace={workspace}
    storageUserId={status === "authenticated" ? user?.id : undefined} />;
}

function TravelServicesWorkspace({ workspace, storageUserId }: {
  workspace: "hotels" | "partners" | "services"; storageUserId?: string;
}) {
  const t = useTranslations("travelServices");
  const copy = adminHotelsCopy(useLocale());
  const affiliateCopy = klookAffiliateCopy(useLocale());
  const router = useRouter();
  const manage = useAdminActionGuard("content.manage");
  const isHotel = workspace === "hotels";
  const storageKey = storageUserId ? `${hotelDraftKey}:${storageUserId}` : undefined;
  const navigation = useAdminWorkspaceNavigation({
    tabs: isHotel ? hotelTabs : workspace === "partners" ? partnerTabs : serviceTabs,
    defaultTab: workspace === "partners" ? "brands" : "catalog",
    legacy: workspace === "services" ? legacyServiceLinks : undefined,
  });
  const { tab: workspaceTab, section, ready } = navigation;
  const tab = !isHotel ? workspaceTab : workspaceTab === "review" ? "catalog"
    : workspaceTab === "affiliates" ? section === "products" ? "catalog" : "destinationOffers"
    : workspaceTab === "imports" ? section === "coverage" ? "coverage" : "importCsv"
    : workspaceTab === "settings" ? section === "providers" ? "providers" : "config" : "catalog";
  const endpoint = isHotel ? "/admin/hotels" : "/admin/travel-services";
  const visibleKinds = isHotel ? ["hotel"] as const : KINDS.filter((value) => value !== "hotel");
  const visibleModules = isHotel ? ["hotel"] : ["flight", "activities", "transport", "connectivity"];
  const [data, setData] = useState<Overview>();
  const [config, setConfig] = useState<Config>();
  const [configVersion, setConfigVersion] = useState(0);
  const [hasConfigDraft, setHasConfigDraft] = useState(false);
  const [configConflict, setConfigConflict] = useState(false);
  const configDirty = useRef(false);
  const draftHydrated = useRef(false);
  const activeRequest = useRef<AbortController | null>(null);
  const [destination, setDestination] = useAdminQueryValue("destination_id", "", (value) => CITIES.some((city) => city === value));
  const [kind, setKind] = useState("");
  const [status, setStatus] = useAdminQueryValue("status", "", (value) => ["pending", "approved", "disabled"].includes(value));
  const reviewProducts = isHotel && workspaceTab === "review" && section === "products";
  const effectiveStatus = reviewProducts ? "pending" : status;
  const missingOptions = isHotel && navigation.query.get("missing_options") === "true";
  const bookingProvider = isHotel ? navigation.query.get("booking_provider") ?? "" : "";
  const bookingReadiness = isHotel ? navigation.query.get("booking_readiness") ?? "" : "";
  const pageKey = `${workspaceTab}:${section}:${destination}:${kind}:${effectiveStatus}:${missingOptions}:${bookingProvider}:${bookingReadiness}`;
  const [pagination, setPagination] = useState({ key: "", offset: 0 });
  const offset = pagination.key === pageKey ? pagination.offset : 0;
  function setOffset(value: number | ((previous: number) => number)) {
    setPagination({ key: pageKey, offset: typeof value === "function" ? value(offset) : value });
  }
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [busy, setBusy] = useState(false);
  const [csv, setCsv] = useState("");
  const [preview, setPreview] = useState<Preview>();
  const [editor, setEditor] = useState<{ row: RecordRow; json: string }>();
  const [offerProduct, setOfferProduct] = useState("");
  const [offerBrand, setOfferBrand] = useState("");
  const [offerTarget, setOfferTarget] = useState("");
  const [offerStatic, setOfferStatic] = useState("");
  const [offerScope, setOfferScope] = useState("product");
  const [brandCode, setBrandCode] = useState("");
  const [brandChannel, setBrandChannel] = useState<AffiliateChannel>("travelpayouts");
  const [brandVersion, setBrandVersion] = useState<number>();
  const [browserReviews, setBrowserReviews] = useState<Record<string, BrowserReview>>({});
  const [approval, setApproval] = useState("pending");
  const [enabled, setEnabled] = useState(false);
  const [evidence, setEvidence] = useState("");
  const [destinationOfferBrand, setDestinationOfferBrand] = useState("");
  const [destinationOfferDestination, setDestinationOfferDestination] =
    useState("");
  const [destinationOfferModule, setDestinationOfferModule] =
    useState<AffiliateModule>(isHotel ? "hotel" : "activities");
  const [destinationOfferTarget, setDestinationOfferTarget] = useState("");
  const [destinationOfferStatic, setDestinationOfferStatic] = useState("");
  const [offerFilterModule, setOfferFilterModule] = useState("");
  const [offerFilterStatus, setOfferFilterStatus] = useState("");
  const [offerFilterBrand, setOfferFilterBrand] = useState("");
  const [offerReviewDue, setOfferReviewDue] = useState(false);
  const [selectedDestinationOffers, setSelectedDestinationOffers] = useState<
    string[]
  >([]);
  const [destinationOfferEditor, setDestinationOfferEditor] = useState<{
    row: DestinationOfferRow;
    targetUrl: string;
    staticUrl: string;
  }>();
  const channelLabel = (channel?: AffiliateChannel) => channel === "klook_direct"
    ? affiliateCopy.klook : affiliateCopy.travelpayouts;
  const brandLabel = (brand?: BrandRow) => brand
    ? `${brand.name} · ${channelLabel(brand.channel)}` : "";
  function selectBrand(code: string, channel: AffiliateChannel) {
    const row = data?.brands.find((brand) => brand.code === code && (brand.channel || "travelpayouts") === channel);
    setBrandCode(code);
    setBrandChannel(channel);
    setBrandVersion(row?.version);
    setApproval(row?.approval || "pending");
    setEnabled(row?.enabled || false);
    setEvidence(row?.evidence_url || "");
  }
  const load = useCallback(async () => {
    activeRequest.current?.abort();
    const controller = new AbortController();
    activeRequest.current = controller;
    const query = new URLSearchParams({ offset: String(offset) });
    if (destination) query.set("destination_id", destination);
    if (!isHotel && kind) query.set("type", kind);
    if (workspace === "services") query.set("exclude_hotels", "true");
    if (effectiveStatus) query.set("status", effectiveStatus);
    if (missingOptions) query.set("missing_options", "true");
    if (bookingProvider) query.set("booking_provider", bookingProvider);
    if (bookingReadiness) query.set("booking_readiness", bookingReadiness);
    if (!isHotel && offerFilterModule) query.set("affiliate_module", offerFilterModule);
    if (offerFilterStatus) query.set("offer_status", offerFilterStatus);
    if (offerFilterBrand) query.set("offer_brand_id", offerFilterBrand);
    if (offerReviewDue) query.set("offer_review_due", "true");
    const result = await api<Overview>(`${endpoint}?${query}`, { signal: controller.signal });
    if (controller.signal.aborted) return;
    setData(result);
    if (!configDirty.current) {
      const draft = isHotel && storageKey && !draftHydrated.current ? readHotelDraft(storageKey) : undefined;
      draftHydrated.current = true;
      if (draft) {
        configDirty.current = true;
        setHasConfigDraft(true);
        setConfig({ ...result.config, enabled_kinds: draft.hotel_enabled ? ["hotel"] : [],
          direct_hotel_links_enabled: draft.direct_hotel_links_enabled,
          hotel_quote_policies: draft.hotel_quote_policies });
        setConfigVersion(draft.version);
      } else {
        setConfig(result.config);
        setConfigVersion(result.version);
      }
    }
  }, [
    endpoint, isHotel, workspace, storageKey,
    destination,
    kind,
    effectiveStatus, missingOptions, bookingProvider, bookingReadiness,
    offset,
    offerFilterModule,
    offerFilterStatus,
    offerFilterBrand,
    offerReviewDue,
  ]);
  const legacyHotel = workspace === "services" && navigation.query.get("type") === "hotel";
  useEffect(() => {
    if (legacyHotel) router.replace("/admin/hotels?tab=catalog&section=catalog");
  }, [legacyHotel, router]);
  useEffect(() => {
    if (!ready || legacyHotel) return;
    void Promise.resolve()
      .then(load)
      .catch((e: Error) => { if (e.name !== "AbortError") setError(e.message); });
    return () => activeRequest.current?.abort();
  }, [load, ready, legacyHotel]);
  useEffect(() => {
    if (!isHotel || !storageKey || !draftHydrated.current) return;
    try {
      if (hasConfigDraft && config) {
        // Only the non-secret hotel-owned fields are persisted, never provider credentials.
        sessionStorage.setItem(storageKey, JSON.stringify({ version: configVersion,
          hotel_enabled: config.enabled_kinds.includes("hotel"),
          direct_hotel_links_enabled: config.direct_hotel_links_enabled ?? false,
          hotel_quote_policies: config.hotel_quote_policies || {} }));
      } else sessionStorage.removeItem(storageKey);
    } catch { /* Storage can be disabled; the leave guard still protects the in-memory draft. */ }
  }, [isHotel, storageKey, hasConfigDraft, config, configVersion]);
  useEffect(() => {
    if (!isHotel || !hasConfigDraft) return;
    const leavesPage = (url: string) => new URL(url, window.location.href).pathname !== window.location.pathname;
    const beforeUnload = (event: BeforeUnloadEvent) => { event.preventDefault(); event.returnValue = ""; };
    const beforeNavigate = (event: Event) => {
      const target = (event as CustomEvent<{ url?: string }>).detail?.url;
      if (!event.defaultPrevented && target && leavesPage(target) && !window.confirm(copy.leave)) event.preventDefault();
    };
    const click = (event: MouseEvent) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const anchor = event.target instanceof Element ? event.target.closest("a[href]") : null;
      if (!(anchor instanceof HTMLAnchorElement) || anchor.target === "_blank" || anchor.hasAttribute("download")) return;
      if (leavesPage(anchor.href) && !window.confirm(copy.leave)) { event.preventDefault(); event.stopPropagation(); }
    };
    window.addEventListener("beforeunload", beforeUnload);
    window.addEventListener("admin:before-navigate", beforeNavigate);
    document.addEventListener("click", click, true);
    return () => {
      window.removeEventListener("beforeunload", beforeUnload);
      window.removeEventListener("admin:before-navigate", beforeNavigate);
      document.removeEventListener("click", click, true);
    };
  }, [isHotel, hasConfigDraft, copy.leave]);
  function changeConfig(next: Config) {
    configDirty.current = true;
    setHasConfigDraft(true);
    setConfig(next);
  }
  async function run(work: () => Promise<unknown>, reload = true) {
    if (!manage.allowed) {
      setError(manage.disabledReason);
      return;
    }
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await work();
      if (reload) await load();
      setNotice(t("updated"));
    } catch (e) {
      if ((e as Error).name !== "AbortError") setError((e as Error).message);
    } finally {
      setBusy(false);
    }
  }
  function toggle<K extends "enabled_kinds" | "enabled_destinations">(
    key: K,
    value: Config[K][number],
  ) {
    if (!config) return;
    const values = config[key] as string[];
    changeConfig({
      ...config,
      [key]: values.includes(value)
        ? values.filter((v) => v !== value)
        : [...values, value],
    });
  }
  function toggleDestination(value: string) {
    if (!config) return;
    const linked = value === "osaka-kyoto" ? [value, "osaka", "kyoto"] : [value];
    const remove = linked.every((item) =>
      config.enabled_destinations.includes(item),
    );
    changeConfig({
      ...config,
      enabled_destinations: remove
        ? config.enabled_destinations.filter((item) => !linked.includes(item))
        : [...new Set([...config.enabled_destinations, ...linked])],
    });
  }
  function edit(row: RecordRow) {
    const {
      source_key,
      kind,
      destination_id,
      title,
      source_url,
      names_json,
      facts,
    } = row;
    setEditor({
      row,
      json: JSON.stringify(
        {
          source_key,
          kind,
          destination_id,
          title,
          source_url,
          names_json,
          facts,
        },
        null,
        2,
      ),
    });
  }
  return (
    <div className="mt-7 min-w-0 space-y-5">
      <AdminReadOnlyNotice capability="content.manage" />
      {isHotel && workspaceTab === "catalog" && <AdminMapIdentitiesPanel initialKind="hotel" canManage={manage.allowed} />}
      <div
        role="tablist"
        aria-label={isHotel ? copy.title : workspace === "partners" ? copy.partnersTitle : t("adminTitle")}
        className="flex flex-wrap gap-2"
      >
        {Object.keys(isHotel ? hotelTabs : workspace === "partners" ? partnerTabs : serviceTabs).map(
          (name) => (
            <button
              role="tab"
              id={`${workspace}-tab-${name}`}
              aria-controls={`${workspace}-workspace-panel`}
              aria-selected={workspaceTab === name}
              tabIndex={workspaceTab === name ? 0 : -1}
              key={name}
              className={`${button} ${workspaceTab === name ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]" : ""}`}
              onClick={() => navigation.selectTab(name)}
              onKeyDown={(event) => {
                const names = Object.keys(isHotel ? hotelTabs : workspace === "partners" ? partnerTabs : serviceTabs);
                const index = names.indexOf(name);
                const next = event.key === "Home" ? names[0] : event.key === "End" ? names[names.length - 1]
                  : event.key === "ArrowRight" ? names[(index + 1) % names.length]
                  : event.key === "ArrowLeft" ? names[(index - 1 + names.length) % names.length] : undefined;
                if (!next) return;
                event.preventDefault();
                navigation.selectTab(next);
                document.getElementById(`${workspace}-tab-${next}`)?.focus();
              }}
            >
              {isHotel ? copy[name as keyof typeof copy] : t(name)}
            </button>
          ),
        )}
      </div>
      {isHotel && hotelTabs[workspaceTab as keyof typeof hotelTabs]?.length > 1 && (
        <nav aria-label={copy[workspaceTab as keyof typeof copy]} className="flex flex-wrap gap-2">
          {hotelTabs[workspaceTab as keyof typeof hotelTabs].map((name) => <button
            key={name} className={button} aria-current={section === name ? "page" : undefined}
            onClick={() => navigation.selectSection(name)}
          >{copy[name as keyof typeof copy]}</button>)}
        </nav>
      )}
      <div className="flex flex-wrap gap-3 text-sm">
        {!isHotel && <Link className={`${button} inline-flex items-center`} href="/admin/hotels">{copy.title}</Link>}
        {workspace !== "partners" && <Link className={`${button} inline-flex items-center`} href="/admin/partners">{copy.partners}</Link>}
        {isHotel && <Link className={`${button} inline-flex items-center`} href="/admin/travel-services">{copy.other}</Link>}
      </div>
      {isHotel && data?.summary && <dl className="grid grid-cols-2 gap-3 lg:grid-cols-4">
        {(["total", "pending", "approved", "disabled"] as const).map((key) => <div key={key} className="rounded-2xl border border-[var(--line)] p-4">
          <dt className="text-sm text-[var(--muted)]">{copy[key === "disabled" ? "unavailable" : key]}</dt>
          <dd className="mt-1 text-2xl font-semibold">{data.summary![key]}</dd>
        </div>)}
      </dl>}
      {error && (
        <p role="alert" className="rounded-xl bg-[var(--coral-soft)] p-4">
          {error}
          <button
            className={`${button} ml-3`}
            onClick={() => void run(load, false)}
          >
            {t("retry")}
          </button>
        </p>
      )}
      {notice && (
        <p role="status" className="text-sm text-[var(--teal)]">
          {notice}
        </p>
      )}
      {!data && !error && <p role="status">{t("loading")}</p>}
      <div role="tabpanel" id={`${workspace}-workspace-panel`} aria-labelledby={`${workspace}-tab-${workspaceTab}`}>
      {data && (
        <>
          {!data.network_configured && (
            <p className="rounded-2xl bg-[var(--coral-soft)] p-4 text-sm">
              {affiliateCopy.networkMissing}{isHotel && <> {t("directIndependent")}</>}{" "}
              <Link href="/admin/settings" className="underline">
                {t("config")}
              </Link>
            </p>
          )}
          {(tab === "catalog" || isHotel) && (
            <section className="space-y-4" hidden={tab !== "catalog"}>
              {isHotel && data.stay22_readiness && (workspaceTab === "affiliates" || bookingProvider) && <Stay22ReadinessPanel rows={data.stay22_readiness} provider={bookingProvider} readiness={bookingReadiness} destination={destination} status={effectiveStatus} />}
              {missingOptions && <p className="flex flex-wrap items-center gap-3 rounded-xl bg-[var(--teal-soft)] p-3 text-sm">
                {copy.missingOptions}
                <Link href="/admin/hotels?tab=review&section=platforms" className={`${button} inline-flex items-center`}>{copy.showAllHotels}</Link>
              </p>}
              <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
                <label>
                  {t("destinationLink")}
                  <select
                    value={destination}
                    className={field}
                    onChange={(e) => {
                      setDestination(e.target.value);
                      setOffset(0);
                    }}
                  >
                    <option value="">{t("all")}</option>
                    {CITIES.map((c) => (
                      <option key={c} value={c}>
                        {t(c)}
                      </option>
                    ))}
                  </select>
                </label>
                {!isHotel && <label>
                  {t("catalog")}
                  <select
                    value={kind}
                    className={field}
                    onChange={(e) => {
                      setKind(e.target.value);
                      setOffset(0);
                    }}
                  >
                    <option value="">{t("all")}</option>
                    {visibleKinds.map((k) => (
                      <option key={k} value={k}>
                        {t(k)}
                      </option>
                    ))}
                  </select>
                </label>}
                <label>
                  {t("pending")}
                  <select
                    value={effectiveStatus}
                    disabled={reviewProducts}
                    className={field}
                    onChange={(e) => {
                      setStatus(e.target.value);
                      setOffset(0);
                    }}
                  >
                    <option value="">{t("all")}</option>
                    {["pending", "approved", "disabled"].map((s) => (
                      <option value={s} key={s}>
                        {t(s === "disabled" ? "disabledStatus" : s)}
                      </option>
                    ))}
                  </select>
                </label>
              </div>
              {data.products.length === 0 && <p>{t("empty")}</p>}
              {data.products.map((p) => (
                <article
                  className="rounded-2xl border border-[var(--line)] p-4"
                  key={p.id}
                >
                  <p className="text-xs text-[var(--muted)]">
                    {t(p.kind)} · {t(p.destination_id)} ·{" "}
                    {t(p.status === "disabled" ? "disabledStatus" : p.status)}
                  </p>
                  <h3 className="mt-1 break-words text-lg font-semibold">
                    {p.title}
                  </h3>
                  <a
                    className="inline-flex min-h-11 items-center text-sm underline"
                    href={p.source_url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`${t("source")} · ${t("newTab")}`}
                  >
                    {t("source")}
                  </a>
                  <div className="flex flex-wrap gap-2">
                    {(!isHotel || workspaceTab === "review" && section === "products") && <>
                    <button
                      disabled={!manage.allowed || busy}
                      title={!manage.allowed ? manage.disabledReason : undefined}
                      className={button}
                      onClick={() =>
                        void run(() =>
                          api(
                            `/admin/travel-services/products/${p.id}/review`,
                            {
                              method: "POST",
                              body: JSON.stringify({
                                version: p.version,
                                status: "approved",
                              }),
                            },
                          ),
                        )
                      }
                    >
                      {t("approve")}
                    </button>
                    <button
                      disabled={!manage.allowed || busy}
                      title={!manage.allowed ? manage.disabledReason : undefined}
                      className={button}
                      onClick={() =>
                        void run(() =>
                          api(
                            `/admin/travel-services/products/${p.id}/review`,
                            {
                              method: "POST",
                              body: JSON.stringify({
                                version: p.version,
                                status: "disabled",
                              }),
                            },
                          ),
                        )
                      }
                    >
                      {t("disable")}
                    </button>
                    </>}
                    {(!isHotel || workspaceTab === "catalog") &&
                    <button className={button} disabled={!manage.allowed} title={!manage.allowed ? manage.disabledReason : undefined} onClick={() => edit(p)}>
                      {t("edit")}
                    </button>
                    }
                  </div>
                  {p.kind === "hotel" && (<div hidden={isHotel && !(workspaceTab === "review" && section === "platforms")}>
                    <HotelOptionsAdmin
                      key={`${p.id}:${(p.booking_options || []).map((o) => o.version).join(",")}`}
                      productId={p.id}
                      options={p.booking_options || []}
                      brands={data.brand_definitions}
                      busy={busy || !manage.allowed}
                      run={run}
                    />
                    </div>
                  )}
                  {data.offers
                    .filter((o) => o.product_id === p.id && (!isHotel || workspaceTab === "affiliates"))
                    .map((o) => (
                      <div
                        key={o.id}
                        className="mt-4 border-t border-[var(--line)] pt-3"
                      >
                        <p className="text-sm">
                          {brandLabel(data.brands.find((b) => b.id === o.brand_id))} ·{" "}
                          {t(
                            o.status === "disabled"
                              ? "disabledStatus"
                              : o.status,
                          )}
                        </p>
                        <a
                          href={o.target_url}
                          target="_blank"
                          rel="noopener noreferrer"
                          className="block break-all py-3 text-xs underline"
                        >
                          {o.target_url}
                        </a>
                        {data.brands.find((brand) => brand.id === o.brand_id)?.channel === "klook_direct" && <BrowserReviewFields
                      target={o.target_url} disabled={!manage.allowed || busy} value={browserReviews[`product:${o.id}:${o.version}`]}
                          onChange={(value) => setBrowserReviews((previous) => ({ ...previous, [`product:${o.id}:${o.version}`]: value }))}
                        />}
                        <div className="flex flex-wrap gap-2">
                          <button
                            disabled={!manage.allowed || busy}
                            title={!manage.allowed ? manage.disabledReason : undefined}
                            className={button}
                            onClick={() =>
                              void run(() =>
                                api(
                                  `/admin/travel-services/offers/${o.id}/review`,
                                  {
                                    method: "POST",
                                    body: JSON.stringify({
                                      version: o.version,
                                      status: "approved",
                                      ...(browserReviews[`product:${o.id}:${o.version}`]?.browser_verified ? browserReviews[`product:${o.id}:${o.version}`] : {}),
                                    }),
                                  },
                                ),
                              )
                            }
                          >
                            {t("verifyOffer")}
                          </button>
                          <button
                            disabled={!manage.allowed || busy}
                            title={!manage.allowed ? manage.disabledReason : undefined}
                            className={button}
                            onClick={() =>
                              void run(() =>
                                api(
                                  `/admin/travel-services/offers/${o.id}/review`,
                                  {
                                    method: "POST",
                                    body: JSON.stringify({
                                      version: o.version,
                                      status: "disabled",
                                    }),
                                  },
                                ),
                              )
                            }
                          >
                            {t("disable")}
                          </button>
                        </div>
                      </div>
                    ))}
                </article>
              ))}
              {data.products.length === 60 && (
                <button
                  className={button}
                  onClick={() => setOffset((v) => v + 60)}
                >
                  {t("more")}
                </button>
              )}
              {editor && (
                <section className="rounded-2xl bg-[var(--paper)] p-4">
                  <label className="font-semibold">
                    {t("productJson")}
                    <textarea
                      className={`${field} min-h-80 font-mono`}
                      value={editor.json}
                      onChange={(e) =>
                        setEditor({ ...editor, json: e.target.value })
                      }
                    />
                  </label>
                  <button
                    className={button}
                    disabled={!manage.allowed || busy}
                    title={!manage.allowed ? manage.disabledReason : undefined}
                    onClick={() =>
                      void run(async () => {
                        await api(
                          `/admin/travel-services/products/${editor.row.id}?version=${editor.row.version}`,
                          {
                            method: "PUT",
                            body: JSON.stringify(JSON.parse(editor.json)),
                          },
                        );
                        setEditor(undefined);
                      })
                    }
                  >
                    {t("edit")}
                  </button>
                </section>
              )}
              {(!isHotel || workspaceTab === "affiliates") && <details className="rounded-xl border border-[var(--line)] p-4">
                <summary className="min-h-11 cursor-pointer">
                  {t("addOffer")}
                </summary>
                <div className="grid gap-3 py-3 sm:grid-cols-2">
                  <label>
                    {t("catalog")}
                    <select
                      className={field}
                      value={offerProduct}
                      onChange={(e) => setOfferProduct(e.target.value)}
                    >
                      <option value="">{t("catalog")}</option>
                      {data.products.map((p) => (
                        <option key={p.id} value={p.id}>
                          {p.title}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    {t("brands")}
                    <select
                      className={field}
                      value={offerBrand}
                      onChange={(e) => setOfferBrand(e.target.value)}
                    >
                      <option value="">{t("brands")}</option>
                      {data.brands.map((b) => (
                        <option key={b.id} value={b.id}>
                          {brandLabel(b)}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label className="sm:col-span-2">
                    {t("originalUrl")}
                    <input
                      type="url"
                      className={field}
                      value={offerTarget}
                      onChange={(e) => setOfferTarget(e.target.value)}
                    />
                  </label>
                  {data.brands.find((brand) => brand.id === offerBrand)?.channel !== "klook_direct" && <label className="sm:col-span-2">
                    {t("staticUrl")}
                    <input
                      type="url"
                      className={field}
                      value={offerStatic}
                      onChange={(e) => setOfferStatic(e.target.value)}
                    />
                  </label>}
                  <label>
                    {t("offers")}
                    <select
                      className={field}
                      value={offerScope}
                      onChange={(e) => setOfferScope(e.target.value)}
                    >
                      <option value="product">{t("productScope")}</option>
                      <option value="destination">
                        {t("destinationScope")}
                      </option>
                    </select>
                  </label>
                </div>
                <button
                  disabled={!manage.allowed || busy}
                  title={!manage.allowed ? manage.disabledReason : undefined}
                  className={button}
                  onClick={() =>
                    void run(() =>
                      api("/admin/travel-services/offers", {
                        method: "POST",
                        body: JSON.stringify({
                          product_id: offerProduct,
                          brand_id: offerBrand,
                          target_url: offerTarget,
                          ...(data.brands.find((brand) => brand.id === offerBrand)?.channel === "klook_direct" ? {} : { static_url: offerStatic || null }),
                          scope: offerScope,
                        }),
                      }),
                    )
                  }
                >
                  {t("addOffer")}
                </button>
              </details>}
            </section>
          )}
          {tab === "destinationOffers" && (
            <section className="space-y-5">
              <div className="rounded-2xl border border-[var(--line)] p-5">
                <h3 className="font-bold">{t("destinationOfferCreate")}</h3>
                <p className="mt-2 text-sm text-[var(--muted)]">
                  {t("destinationOfferIdentityHint")}
                </p>
                <div className="mt-4 grid gap-3 sm:grid-cols-2">
                  <label>
                    {t("brands")}
                    <select
                      className={field}
                      value={destinationOfferBrand}
                      onChange={(event) =>
                        setDestinationOfferBrand(event.target.value)
                      }
                    >
                      <option value="">{t("brands")}</option>
                      {data.brands
                        .filter((brand) =>
                          data.brand_definitions[
                            brand.code
                          ]?.modules.includes(destinationOfferModule),
                        )
                        .map((brand) => (
                          <option key={brand.id} value={brand.id}>
                            {brandLabel(brand)} · {t(brand.approval)}
                          </option>
                        ))}
                    </select>
                  </label>
                  <label>
                    {t("destinationLink")}
                    <select
                      className={field}
                      value={destinationOfferDestination}
                      onChange={(event) =>
                        setDestinationOfferDestination(event.target.value)
                      }
                    >
                      <option value="">{t("destinationLink")}</option>
                      {data.destinations.map((item) => (
                        <option key={item.id} value={item.id}>
                          {item.country} · {item.city} · {t(item.role)}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    {t("affiliateModule")}
                    <select
                      className={field}
                      value={destinationOfferModule}
                      onChange={(event) => {
                        setDestinationOfferModule(
                          event.target.value as AffiliateModule,
                        );
                        setDestinationOfferBrand("");
                      }}
                    >
                      {visibleModules.map((module) => (
                        <option key={module} value={module}>
                          {t(`affiliate${module[0].toUpperCase()}${module.slice(1)}`)}
                        </option>
                      ))}
                    </select>
                  </label>
                  <label>
                    {t("originalUrl")}
                    <input
                      type="url"
                      className={field}
                      value={destinationOfferTarget}
                      onChange={(event) =>
                        setDestinationOfferTarget(event.target.value)
                      }
                    />
                  </label>
                  {data.brands.find((brand) => brand.id === destinationOfferBrand)?.channel !== "klook_direct" && <label className="sm:col-span-2">
                    {t("staticUrl")}
                    <input
                      type="url"
                      className={field}
                      value={destinationOfferStatic}
                      onChange={(event) =>
                        setDestinationOfferStatic(event.target.value)
                      }
                    />
                  </label>}
                </div>
                <button
                  className={`${button} mt-4`}
                  disabled={
                    !manage.allowed ||
                    busy ||
                    !destinationOfferBrand ||
                    !destinationOfferDestination ||
                    !destinationOfferTarget
                  }
                  onClick={() =>
                    void run(async () => {
                      await api("/admin/travel-services/destination-offers", {
                        method: "POST",
                        body: JSON.stringify({
                          brand_id: destinationOfferBrand,
                          destination_id: destinationOfferDestination,
                          module: destinationOfferModule,
                          target_url: destinationOfferTarget,
                          ...(data.brands.find((brand) => brand.id === destinationOfferBrand)?.channel === "klook_direct" ? {} : { static_url: destinationOfferStatic || null }),
                        }),
                      });
                      setDestinationOfferTarget("");
                      setDestinationOfferStatic("");
                    })
                  }
                >
                  {t("addDestinationOffer")}
                </button>
              </div>

              <div className="grid gap-3 sm:grid-cols-3">
                <label>
                  {t("destinationLink")}
                  <select
                    className={field}
                    value={destination}
                    onChange={(event) => setDestination(event.target.value)}
                  >
                    <option value="">{t("all")}</option>
                    {data.destinations.map((item) => (
                      <option key={item.id} value={item.id}>
                        {item.country} · {item.city}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  {t("affiliateModule")}
                  <select
                    className={field}
                    value={offerFilterModule}
                    onChange={(event) => setOfferFilterModule(event.target.value)}
                  >
                    <option value="">{t("all")}</option>
                    {visibleModules.map((module) => (
                      <option key={module} value={module}>
                        {t(`affiliate${module[0].toUpperCase()}${module.slice(1)}`)}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  {t("status")}
                  <select
                    className={field}
                    value={offerFilterStatus}
                    onChange={(event) => setOfferFilterStatus(event.target.value)}
                  >
                    <option value="">{t("all")}</option>
                    {['pending', 'approved', 'disabled'].map((value) => (
                      <option key={value} value={value}>{t(value)}</option>
                    ))}
                  </select>
                </label>
                <label>
                  {t("brands")}
                  <select
                    className={field}
                    value={offerFilterBrand}
                    onChange={(event) => setOfferFilterBrand(event.target.value)}
                  >
                    <option value="">{t("all")}</option>
                    {data.brands.map((brand) => (
                      <option key={brand.id} value={brand.id}>
                        {brandLabel(brand)}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3 sm:col-span-2 lg:col-span-4">
                  <input
                    type="checkbox"
                    checked={offerReviewDue}
                    onChange={(event) => setOfferReviewDue(event.target.checked)}
                  />
                  {t("showReviewDueOnly")}
                </label>
              </div>

              <div className="flex flex-wrap items-center gap-2">
                <label className="flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3">
                  <input
                    type="checkbox"
                    checked={
                      !!data.destination_offers.length &&
                      data.destination_offers.every((item) =>
                        selectedDestinationOffers.includes(item.id),
                      )
                    }
                    onChange={(event) =>
                      setSelectedDestinationOffers(
                        event.target.checked
                          ? data.destination_offers.map((item) => item.id)
                          : [],
                      )
                    }
                  />
                  {t("selectAll")}
                </label>
                {['approved', 'disabled'].map((reviewStatus) => (
                  <button
                    key={reviewStatus}
                    className={button}
                    disabled={!manage.allowed || busy || !selectedDestinationOffers.length}
                    title={!manage.allowed ? manage.disabledReason : undefined}
                    onClick={() =>
                      void run(async () => {
                        await api(
                          "/admin/travel-services/destination-offers/batch-review",
                          {
                            method: "POST",
                            body: JSON.stringify({
                              status: reviewStatus,
                              offers: data.destination_offers
                                .filter((item) =>
                                  selectedDestinationOffers.includes(item.id),
                                )
                                .map((item) => ({
                                  id: item.id,
                                  version: item.version,
                                })),
                            }),
                          },
                        );
                        setSelectedDestinationOffers([]);
                      })
                    }
                  >
                    {t(reviewStatus === "approved" ? "batchApprove" : "batchDisable")}
                  </button>
                ))}
              </div>

              <div className="space-y-3">
                {data.destination_offers.map((offer) => {
                  const brand = data.brands.find(
                    (item) => item.id === offer.brand_id,
                  );
                  const destinationItem = data.destinations.find(
                    (item) => item.id === offer.destination_id,
                  );
                  return (
                    <article
                      key={offer.id}
                      className="rounded-2xl border border-[var(--line)] p-4"
                    >
                      <div className="flex items-start gap-3">
                        <input
                          aria-label={t("selectOffer", {
                            brand: brandLabel(brand) || offer.brand_id,
                          })}
                          type="checkbox"
                          checked={selectedDestinationOffers.includes(offer.id)}
                          onChange={(event) =>
                            setSelectedDestinationOffers((current) =>
                              event.target.checked
                                ? [...current, offer.id]
                                : current.filter((id) => id !== offer.id),
                            )
                          }
                        />
                        <div className="min-w-0 flex-1">
                          <strong>{brandLabel(brand) || offer.brand_id}</strong>
                          <p className="text-sm text-[var(--muted)]">
                            {destinationItem?.city || offer.destination_id} · {offer.module} · {t(offer.status)}
                          </p>
                          <a
                            className="mt-2 block truncate text-sm text-[var(--teal)] underline"
                            href={offer.target_url}
                            target="_blank"
                            rel="noopener noreferrer"
                          >
                            {offer.target_url}
                          </a>
                          {offer.verified_at && (
                            <p className="mt-1 text-xs text-[var(--muted)]">
                              {t("verifiedAt")}: {new Date(offer.verified_at).toLocaleDateString()}
                            </p>
                          )}
                          {brand?.channel === "klook_direct" && offer.status !== "approved" && <BrowserReviewFields
                            target={offer.target_url} disabled={busy || !manage.allowed} value={browserReviews[`destination:${offer.id}:${offer.version}`]}
                            onChange={(value) => setBrowserReviews((previous) => ({ ...previous, [`destination:${offer.id}:${offer.version}`]: value }))}
                          />}
                          {destinationOfferEditor?.row.id === offer.id && (
                            <div className="mt-3 grid gap-3 sm:grid-cols-2">
                              <label>
                                {t("originalUrl")}
                                <input
                                  type="url"
                                  className={field}
                                  value={destinationOfferEditor.targetUrl}
                                  onChange={(event) =>
                                    setDestinationOfferEditor({
                                      ...destinationOfferEditor,
                                      targetUrl: event.target.value,
                                    })
                                  }
                                />
                              </label>
                              {brand?.channel !== "klook_direct" && <label>
                                {t("staticUrl")}
                                <input
                                  type="url"
                                  className={field}
                                  value={destinationOfferEditor.staticUrl}
                                  onChange={(event) =>
                                    setDestinationOfferEditor({
                                      ...destinationOfferEditor,
                                      staticUrl: event.target.value,
                                    })
                                  }
                                />
                              </label>}
                              <button
                                className={button}
                                disabled={!manage.allowed || busy || !destinationOfferEditor.targetUrl}
                                title={!manage.allowed ? manage.disabledReason : undefined}
                                onClick={() =>
                                  void run(async () => {
                                    await api(
                                      `/admin/travel-services/destination-offers/${offer.id}?version=${offer.version}`,
                                      {
                                        method: "PUT",
                                        body: JSON.stringify({
                                          brand_id: offer.brand_id,
                                          destination_id: offer.destination_id,
                                          module: offer.module,
                                          target_url:
                                            destinationOfferEditor.targetUrl,
                                          ...(brand?.channel === "klook_direct" ? {} : { static_url: destinationOfferEditor.staticUrl || null }),
                                        }),
                                      },
                                    );
                                    setDestinationOfferEditor(undefined);
                                  })
                                }
                              >
                                {t("saveAndReverify")}
                              </button>
                            </div>
                          )}
                        </div>
                        <div className="flex flex-col gap-2">
                          <button
                            className={button}
                            disabled={!manage.allowed || busy}
                            title={!manage.allowed ? manage.disabledReason : undefined}
                            onClick={() =>
                              setDestinationOfferEditor({
                                row: offer,
                                targetUrl: offer.target_url,
                                staticUrl: offer.static_url || "",
                              })
                            }
                          >
                            {t("edit")}
                          </button>
                          <button
                            className={button}
                            disabled={!manage.allowed || busy}
                            title={!manage.allowed ? manage.disabledReason : undefined}
                            onClick={() =>
                              void run(() =>
                                api(
                                  `/admin/travel-services/destination-offers/${offer.id}/review`,
                                  {
                                    method: "POST",
                                    body: JSON.stringify({
                                      version: offer.version,
                                      status:
                                        offer.status === "approved"
                                          ? "disabled"
                                          : "approved",
                                      ...(offer.status !== "approved" && browserReviews[`destination:${offer.id}:${offer.version}`]?.browser_verified ? browserReviews[`destination:${offer.id}:${offer.version}`] : {}),
                                    }),
                                  },
                                ),
                              )
                            }
                          >
                            {t(
                              offer.status === "approved" ? "disable" : "approve",
                            )}
                          </button>
                        </div>
                      </div>
                    </article>
                  );
                })}
              </div>
            </section>
          )}
          {tab === "brands" && (
            <section className="space-y-4">
              <p className="text-sm">
                {affiliateCopy.independent}
              </p>
              <dl className="grid gap-3 sm:grid-cols-2">
                {(["travelpayouts", "klook_direct"] as const).map((channel) => <div key={channel} className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm">
                  <dt className="font-semibold">{channelLabel(channel)}</dt>
                  <dd className="mt-1 text-[var(--muted)]">{data.channels?.[channel]?.configured || (channel === "travelpayouts" && data.network_configured) ? t("complete") : t("unknownStatus")}</dd>
                </div>)}
              </dl>
              <div className="grid gap-3 sm:grid-cols-3">
                {Object.entries(data.brand_definitions).flatMap(([code, b]) =>
                  (code === "klook" ? ["travelpayouts", "klook_direct"] as const : ["travelpayouts"] as const).map((channel) => {
                  const row = data.brands.find((r) => r.code === code && (r.channel || "travelpayouts") === channel);
                  return (
                    <button
                      key={`${code}:${channel}`}
                      disabled={!manage.allowed || busy}
                      title={!manage.allowed ? manage.disabledReason : undefined}
                      aria-label={`${b.name} · ${channelLabel(channel)}`}
                      aria-pressed={brandCode === code && brandChannel === channel}
                      className={`${button} text-left ${brandCode === code && brandChannel === channel ? "bg-[var(--teal-soft)]" : ""}`}
                      onClick={() => selectBrand(code, channel)}
                    >
                      <strong className="block">{b.name}</strong>
                      <span className="block text-xs">{channelLabel(channel)}</span>
                      <span className="text-xs">
                        {t(
                          row?.approval === "unknown" || !row
                            ? "unknownStatus"
                            : row.approval,
                        )}
                      </span>
                      <span className="mt-1 block text-xs text-[var(--muted)]">
                        {b.modules.map((module) =>
                          t(`affiliate${module[0].toUpperCase()}${module.slice(1)}`),
                        ).join(" · ")}
                      </span>
                      <span className="mt-1 block text-xs text-[var(--muted)]">
                        {row?.verified_at
                          ? `${t("verifiedAt")}: ${new Date(row.verified_at).toLocaleDateString()}`
                          : t("verificationRequired")}
                      </span>
                    </button>
                  );
                }))}
              </div>
              {brandCode && <div className="rounded-2xl border border-[var(--line)] p-5">
                <h3 className="font-bold">
                  {data.brand_definitions[brandCode]?.name}
                  {" · "}{channelLabel(brandChannel)}
                </h3>
                <p className="mt-2 text-xs">
                  {data.brand_definitions[brandCode]?.hosts.join(" · ")}
                </p>
                {brandCode === "klook" && <div className="mt-3 rounded-xl bg-[var(--paper)] p-4 text-sm leading-6">
                  <p>{affiliateCopy.noApi}</p>
                  {brandChannel === "klook_direct" && <Link href="/admin/settings?provider=klook&field=klook_affiliate_id" className="mt-2 inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{affiliateCopy.configure}</Link>}
                </div>}
                <label className="mt-3 block">
                  {t("approval")}
                  <select
                    value={approval}
                    className={field}
                    onChange={(e) => {
                      setApproval(e.target.value);
                      setEnabled(false);
                    }}
                  >
                    {["pending", "approved", "rejected"].map((s) => (
                      <option key={s} value={s}>
                        {t(s)}
                      </option>
                    ))}
                  </select>
                </label>
                <label className="my-3 flex min-h-11 items-center gap-2">
                  <input
                    type="checkbox"
                    checked={enabled}
                    disabled={approval !== "approved"}
                    onChange={(e) => setEnabled(e.target.checked)}
                  />
                  {t("enabled")}
                </label>
                <label>
                  {affiliateCopy.evidence}
                  <input
                    type="url"
                    className={field}
                    value={evidence}
                    onChange={(e) => setEvidence(e.target.value)}
                  />
                </label>
                <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{affiliateCopy.evidenceHint}</p>
                <button
                  disabled={!manage.allowed || busy || !evidence}
                  title={!manage.allowed ? manage.disabledReason : undefined}
                  className={`${button} mt-4`}
                  onClick={() =>
                    void run(async () => {
                      const saved = await api<BrandRow>("/admin/travel-services/brands", {
                        method: "PUT",
                        body: JSON.stringify({
                          code: brandCode,
                          channel: brandChannel,
                          approval,
                          enabled,
                          evidence_url: evidence,
                          version: brandVersion,
                        }),
                      });
                      if (saved.code === brandCode && (saved.channel || "travelpayouts") === brandChannel) setBrandVersion(saved.version);
                    })
                  }
                >
                  {t("apply")}
                </button>
              </div>}
            </section>
          )}
          {tab === "importCsv" && (
            <section className="space-y-4">
              {isHotel && <p className="rounded-xl bg-[var(--teal-soft)] p-4 text-sm">{copy.hotelOnly}</p>}
              <p className="break-words text-sm leading-6">{t("csvHint")}</p>
              <label className="block">
                {t("importCsv")}
                <input
                  type="file"
                  accept=".csv,text/csv"
                  className={field}
                  onChange={(e) => {
                    const file = e.target.files?.[0];
                    setPreview(undefined);
                    if (file && file.size <= 500000)
                      void file.text().then(setCsv);
                  }}
                />
                <textarea
                  className={`${field} min-h-40 font-mono`}
                  value={csv}
                  onChange={(e) => {
                    setCsv(e.target.value);
                    setPreview(undefined);
                  }}
                />
              </label>
              <button
                disabled={!manage.allowed || busy || !csv}
                title={!manage.allowed ? manage.disabledReason : undefined}
                className={button}
                onClick={() =>
                  void run(async () => {
                    setPreview(
                      await api<Preview>(
                        `${endpoint}/imports/preview`,
                        { method: "POST", body: JSON.stringify({ csv }) },
                      ),
                    );
                  }, false)
                }
              >
                {t("preview")}
              </button>
              {preview && (
                <div className="space-y-3">
                  <ul className="max-h-80 overflow-y-auto rounded-2xl border border-[var(--line)] p-4">
                    {preview.rows_json.map((r) => (
                      <li
                        className="border-b border-[var(--line)] py-2 text-sm"
                        key={r.line}
                      >
                        {r.line} · {r.product?.title || t("incomplete")} ·{" "}
                        {r.error ? t("incomplete") : t("pending")}
                        {r.change && (
                          <span> · {t(`importChange.${r.change}`)}</span>
                        )}
                        {!!r.missing_platforms?.length && (
                          <p>
                            {t("missingPlatforms")}:{" "}
                            {r.missing_platforms
                              .map((code) =>
                                code === "official"
                                  ? t("officialHotel")
                                  : data.brand_definitions[code]?.name || code,
                              )
                              .join(" · ")}
                          </p>
                        )}
                      </li>
                    ))}
                  </ul>
                  <button
                    disabled={!manage.allowed || busy || preview.rows_json.some((r) => r.error)}
                    title={!manage.allowed ? manage.disabledReason : undefined}
                    className={button}
                    onClick={() =>
                      void run(async () => {
                        await api(
                          `${endpoint}/imports/${preview.id}/commit`,
                          { method: "POST" },
                        );
                        setPreview(undefined);
                      })
                    }
                  >
                    {t("commit")}
                  </button>
                </div>
              )}
              <h3 className="pt-5 font-bold">{t("imports")}</h3>
              {data.imports.map((r) => (
                <div
                  className="rounded-xl border border-[var(--line)] p-3 text-sm"
                  key={r.id}
                >
                  {r.source} · {r.status} · {r.row_count}
                  <pre className="mt-2 overflow-x-auto text-xs">
                    {JSON.stringify(r.result_json)}
                  </pre>
                </div>
              ))}
            </section>
          )}
          {tab === "coverage" && (
            <section className="space-y-4">
              <p className="text-sm">{t(isHotel ? "hotelTargets" : "targets")}</p>
              <div className="grid gap-3 sm:grid-cols-2">
                {data.coverage.map((c) => (
                  <article
                    key={c.destination_id}
                    className="rounded-2xl border border-[var(--line)] p-5"
                  >
                    <h3 className="font-bold">{t(c.destination_id)}</h3>
                    <dl className="my-3 grid grid-cols-2 gap-2 text-sm">
                      {visibleKinds.map((k) => (
                        <div key={k}>
                          <dt className="text-[var(--muted)]">{t(k)}</dt>
                          <dd className="font-semibold">{c.counts[k]}</dd>
                        </div>
                      ))}
                    </dl>
                    {isHotel && <p className="text-xs text-[var(--teal)]">
                      {t("hotelReady", { count: c.hotel_ready || 0 })} ·{" "}
                      {t(c.hotel_complete ? "complete" : "incomplete")}
                    </p>}
                    <p className="text-xs text-[var(--teal)]">
                      {t(c.complete ? "complete" : "incomplete")}
                    </p>
                  </article>
                ))}
              </div>
              <p>{t("reviewDue", { count: data.review_due })}</p>
              <p>
                {t("optionReviewDue", {
                  count: data.hotel_option_review_due || 0,
                })}
              </p>
              <section className="rounded-2xl bg-[var(--paper)] p-5">
                <h3 className="font-semibold">{t("metrics")}</h3>
                <p className="mt-3">
                  {t("clicks")}: {data.operations.outbound_clicks}
                </p>
                <p>
                  {t("ordinaryClicks")}:{" "}
                  {data.operations.ordinary_hotel_clicks || 0}
                </p>
                <p>
                  {t("affiliateHotelClicks")}:{" "}
                  {data.operations.affiliate_hotel_clicks || 0}
                </p>
                <p>
                  {t("hotelFallbackClicks")}:{" "}
                  {data.operations.hotel_affiliate_fallbacks || 0}
                </p>
                <p>
                  {t("booked")}: {data.operations.self_reported_booked}
                </p>
                <p className="mt-3 text-sm text-[var(--muted)]">
                  {t("commission")}
                </p>
              </section>
            </section>
          )}
          {isHotel && <div hidden={tab !== "config"}><Stay22Admin value={data.config.stay22} version={data.version} allowed={data.can_manage_stay22 === true} onSaved={load} /></div>}
          {tab === "config" && isHotel && data.stay22_readiness && <Stay22ReadinessPanel rows={data.stay22_readiness} destination={destination} status={effectiveStatus} />}
          {tab === "config" && config && (
            <section className="space-y-5 rounded-2xl border border-[var(--line)] p-5">
              {isHotel && <>
              <p className="text-sm text-[var(--muted)]">{copy.shared}</p>
              <QuotePolicies
                disabled={!manage.allowed}
                policies={config.hotel_quote_policies || {}}
                providers={data.quote_providers || {}}
                brands={data.brand_definitions}
                onChange={(policies) =>
                  changeConfig({ ...config, hotel_quote_policies: policies })
                }
              />
              <label className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  disabled={!manage.allowed}
                  checked={config.direct_hotel_links_enabled ?? false}
                  onChange={(e) =>
                    changeConfig({
                      ...config,
                      direct_hotel_links_enabled: e.target.checked,
                    })
                  }
                />
                {t("directEnabled")}
              </label>
              <p className="text-sm text-[var(--muted)]">
                {t("directIndependent")}
              </p>
              </>}
              <label className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  checked={config.public_enabled}
                  disabled={!manage.allowed || isHotel}
                  onChange={(e) =>
                    changeConfig({ ...config, public_enabled: e.target.checked })
                  }
                />
                {t("publicEnabled")}
              </label>
              <fieldset>
                <legend className="font-semibold">{t("catalog")}</legend>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  {visibleKinds.map((k) => (
                    <label className="flex min-h-11 items-center gap-2" key={k}>
                      <input
                        type="checkbox"
                        disabled={!manage.allowed}
                        checked={config.enabled_kinds.includes(k)}
                        onChange={() => toggle("enabled_kinds", k)}
                      />
                      {t(k)}
                    </label>
                  ))}
                </div>
              </fieldset>
              <fieldset>
                <legend className="font-semibold">
                  {t("destinationLink")}
                </legend>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  {data.destinations.map((destinationItem) => (
                    <label
                      className="flex min-h-11 items-center gap-2"
                      key={destinationItem.id}
                    >
                      <input
                        type="checkbox"
                        disabled={!manage.allowed || isHotel}
                        checked={config.enabled_destinations.includes(
                          destinationItem.id,
                        )}
                        onChange={() => toggleDestination(destinationItem.id)}
                      />
                      {destinationItem.country} · {destinationItem.city}
                    </label>
                  ))}
                </div>
              </fieldset>
              {!isHotel && <label className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  disabled={!manage.allowed}
                  checked={config.airalo_feed_enabled}
                  onChange={(e) =>
                    changeConfig({
                      ...config,
                      airalo_feed_enabled: e.target.checked,
                    })
                  }
                />
                {t("feedEnabled")}
              </label>}
              {isHotel && hasConfigDraft && <p role="status" className="text-sm text-[var(--muted)]">{copy.draft}</p>}
              {configConflict && <div role="alert" className="rounded-xl bg-[var(--coral-soft)] p-4 text-sm">
                <p>{copy.conflict}</p>
                <button type="button" className={`${button} mt-3`} disabled={busy} onClick={() => {
                  if (!window.confirm(copy.discard)) return;
                  configDirty.current = false;
                  setHasConfigDraft(false);
                  void run(async () => { await load(); setConfigConflict(false); }, false);
                }}>{copy.reload}</button>
              </div>}
              <button
                className={button}
                disabled={!manage.allowed || busy}
                title={!manage.allowed ? manage.disabledReason : undefined}
                onClick={() =>
                  void run(async () => {
                    const legacyConfig = { ...config };
                    delete legacyConfig.stay22;
                    try { await api(`${endpoint}/config`, {
                      method: isHotel ? "PATCH" : "PUT",
                      body: JSON.stringify(isHotel ? {
                        version: configVersion,
                        hotel_enabled: config.enabled_kinds.includes("hotel"),
                        direct_hotel_links_enabled: config.direct_hotel_links_enabled ?? false,
                        hotel_quote_policies: config.hotel_quote_policies || {},
                      } : {
                        ...legacyConfig,
                        version: configVersion,
                      }),
                    }); } catch (reason) {
                      if (isHotel && reason instanceof ApiError && reason.code === "service_version_conflict") setConfigConflict(true);
                      throw reason;
                    }
                    configDirty.current = false;
                    setHasConfigDraft(false);
                    setConfigConflict(false);
                  })
                }
              >
                {t("apply")}
              </button>
            </section>
          )}
        </>
      )}
      {isHotel && ready && <div hidden={tab !== "providers"}><AdminSettingsPanel scope="hotels" provider={navigation.query.get("provider") ?? undefined} field={navigation.query.get("field") ?? undefined} /></div>}
      </div>
    </div>
  );
}
