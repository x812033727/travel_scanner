"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { CITIES, KINDS, type Kind } from "./catalog";
import { HotelOptionsAdmin, type HotelOptionRow } from "./hotel-options-admin";
import { QuotePolicies, type QuotePolicy } from "./quote-policies";

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
type BrandRow = {
  id: string;
  code: string;
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
  hotel_quote_policies?: Record<string, QuotePolicy>;
  public_enabled: boolean;
  direct_hotel_links_enabled?: boolean;
  enabled_kinds: Kind[];
  enabled_destinations: string[];
  airalo_feed_enabled: boolean;
};
type Overview = {
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

export function TravelServicesAdmin() {
  const t = useTranslations("travelServices");
  const [data, setData] = useState<Overview>();
  const [config, setConfig] = useState<Config>();
  const [destination, setDestination] = useState("");
  const [kind, setKind] = useState("");
  const [status, setStatus] = useState("");
  const [offset, setOffset] = useState(0);
  const [tab, setTab] = useState("catalog");
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
  const [brandCode, setBrandCode] = useState("klook");
  const [approval, setApproval] = useState("pending");
  const [enabled, setEnabled] = useState(false);
  const [evidence, setEvidence] = useState("");
  const [destinationOfferBrand, setDestinationOfferBrand] = useState("");
  const [destinationOfferDestination, setDestinationOfferDestination] =
    useState("");
  const [destinationOfferModule, setDestinationOfferModule] =
    useState<AffiliateModule>("activities");
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
  const load = useCallback(async () => {
    const query = new URLSearchParams({ offset: String(offset) });
    if (destination) query.set("destination_id", destination);
    if (kind) query.set("type", kind);
    if (status) query.set("status", status);
    if (offerFilterModule) query.set("affiliate_module", offerFilterModule);
    if (offerFilterStatus) query.set("offer_status", offerFilterStatus);
    if (offerFilterBrand) query.set("offer_brand_id", offerFilterBrand);
    if (offerReviewDue) query.set("offer_review_due", "true");
    const result = await api<Overview>(`/admin/travel-services?${query}`);
    setData(result);
    setConfig(result.config);
  }, [
    destination,
    kind,
    status,
    offset,
    offerFilterModule,
    offerFilterStatus,
    offerFilterBrand,
    offerReviewDue,
  ]);
  useEffect(() => {
    void Promise.resolve()
      .then(load)
      .catch((e: Error) => setError(e.message));
  }, [load]);
  async function run(work: () => Promise<unknown>, reload = true) {
    setBusy(true);
    setError("");
    setNotice("");
    try {
      await work();
      if (reload) await load();
      setNotice(t("updated"));
    } catch (e) {
      setError((e as Error).message);
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
    setConfig({
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
    setConfig({
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
      <div
        role="tablist"
        aria-label={t("adminTitle")}
        className="flex flex-wrap gap-2"
      >
        {[
          "catalog",
          "destinationOffers",
          "brands",
          "importCsv",
          "coverage",
          "config",
        ].map(
          (name) => (
            <button
              role="tab"
              aria-selected={tab === name}
              key={name}
              className={`${button} ${tab === name ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]" : ""}`}
              onClick={() => setTab(name)}
            >
              {t(name)}
            </button>
          ),
        )}
      </div>
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
      {data && (
        <>
          {!data.network_configured && (
            <p className="rounded-2xl bg-[var(--coral-soft)] p-4 text-sm">
              {t("networkMissing")} {t("directIndependent")}{" "}
              <Link href="/admin/settings" className="underline">
                {t("config")}
              </Link>
            </p>
          )}
          {tab === "catalog" && (
            <section className="space-y-4">
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
                <label>
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
                    {KINDS.map((k) => (
                      <option key={k} value={k}>
                        {t(k)}
                      </option>
                    ))}
                  </select>
                </label>
                <label>
                  {t("pending")}
                  <select
                    value={status}
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
                    <button
                      disabled={busy}
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
                      disabled={busy}
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
                    <button className={button} onClick={() => edit(p)}>
                      {t("edit")}
                    </button>
                  </div>
                  {p.kind === "hotel" && (
                    <HotelOptionsAdmin
                      key={`${p.id}:${(p.booking_options || []).map((o) => o.version).join(",")}`}
                      productId={p.id}
                      options={p.booking_options || []}
                      brands={data.brand_definitions}
                      busy={busy}
                      run={run}
                    />
                  )}
                  {data.offers
                    .filter((o) => o.product_id === p.id)
                    .map((o) => (
                      <div
                        key={o.id}
                        className="mt-4 border-t border-[var(--line)] pt-3"
                      >
                        <p className="text-sm">
                          {data.brands.find((b) => b.id === o.brand_id)?.name} ·{" "}
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
                        <div className="flex flex-wrap gap-2">
                          <button
                            disabled={busy}
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
                                    }),
                                  },
                                ),
                              )
                            }
                          >
                            {t("verifyOffer")}
                          </button>
                          <button
                            disabled={busy}
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
                    disabled={busy}
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
              <details className="rounded-xl border border-[var(--line)] p-4">
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
                          {b.name}
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
                  <label className="sm:col-span-2">
                    {t("staticUrl")}
                    <input
                      type="url"
                      className={field}
                      value={offerStatic}
                      onChange={(e) => setOfferStatic(e.target.value)}
                    />
                  </label>
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
                  disabled={busy}
                  className={button}
                  onClick={() =>
                    void run(() =>
                      api("/admin/travel-services/offers", {
                        method: "POST",
                        body: JSON.stringify({
                          product_id: offerProduct,
                          brand_id: offerBrand,
                          target_url: offerTarget,
                          static_url: offerStatic || null,
                          scope: offerScope,
                        }),
                      }),
                    )
                  }
                >
                  {t("addOffer")}
                </button>
              </details>
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
                            {brand.name} · {t(brand.approval)}
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
                      {[
                        "flight",
                        "hotel",
                        "activities",
                        "transport",
                        "connectivity",
                      ].map((module) => (
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
                  <label className="sm:col-span-2">
                    {t("staticUrl")}
                    <input
                      type="url"
                      className={field}
                      value={destinationOfferStatic}
                      onChange={(event) =>
                        setDestinationOfferStatic(event.target.value)
                      }
                    />
                  </label>
                </div>
                <button
                  className={`${button} mt-4`}
                  disabled={
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
                          static_url: destinationOfferStatic || null,
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
                    {[
                      "flight",
                      "hotel",
                      "activities",
                      "transport",
                      "connectivity",
                    ].map((module) => (
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
                        {brand.name}
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
                    disabled={busy || !selectedDestinationOffers.length}
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
                            brand: brand?.name || offer.brand_id,
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
                          <strong>{brand?.name || offer.brand_id}</strong>
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
                              <label>
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
                              </label>
                              <button
                                className={button}
                                disabled={busy || !destinationOfferEditor.targetUrl}
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
                                          static_url:
                                            destinationOfferEditor.staticUrl || null,
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
                            disabled={busy}
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
                            disabled={busy}
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
                Travelpayouts · {data.project_id || t("unknownStatus")}
              </p>
              <div className="grid gap-3 sm:grid-cols-3">
                {Object.entries(data.brand_definitions).map(([code, b]) => {
                  const row = data.brands.find((r) => r.code === code);
                  return (
                    <button
                      key={code}
                      className={`${button} text-left ${brandCode === code ? "bg-[var(--teal-soft)]" : ""}`}
                      onClick={() => {
                        setBrandCode(code);
                        setApproval(row?.approval || "pending");
                        setEnabled(row?.enabled || false);
                        setEvidence(
                          row?.evidence_url ||
                            `https://app.travelpayouts.com/programs?source=${data.project_id || ""}`,
                        );
                      }}
                    >
                      <strong className="block">{b.name}</strong>
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
                })}
              </div>
              <div className="rounded-2xl border border-[var(--line)] p-5">
                <h3 className="font-bold">
                  {data.brand_definitions[brandCode]?.name}
                </h3>
                <p className="mt-2 text-xs">
                  {data.brand_definitions[brandCode]?.hosts.join(" · ")}
                </p>
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
                  {t("evidence")}
                  <input
                    type="url"
                    className={field}
                    value={evidence}
                    onChange={(e) => setEvidence(e.target.value)}
                  />
                </label>
                <button
                  disabled={busy || !evidence}
                  className={`${button} mt-4`}
                  onClick={() =>
                    void run(() =>
                      api("/admin/travel-services/brands", {
                        method: "PUT",
                        body: JSON.stringify({
                          code: brandCode,
                          approval,
                          enabled,
                          evidence_url: evidence,
                          version: data.brands.find((b) => b.code === brandCode)
                            ?.version,
                        }),
                      }),
                    )
                  }
                >
                  {t("apply")}
                </button>
              </div>
            </section>
          )}
          {tab === "importCsv" && (
            <section className="space-y-4">
              <p className="break-words text-sm leading-6">{t("csvHint")}</p>
              <label className="block">
                {t("importCsv")}
                <input
                  type="file"
                  accept=".csv,text/csv"
                  className={field}
                  onChange={(e) => {
                    const file = e.target.files?.[0];
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
                disabled={busy || !csv}
                className={button}
                onClick={() =>
                  void run(async () => {
                    setPreview(
                      await api<Preview>(
                        "/admin/travel-services/imports/preview",
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
                    disabled={busy || preview.rows_json.some((r) => r.error)}
                    className={button}
                    onClick={() =>
                      void run(async () => {
                        await api(
                          `/admin/travel-services/imports/${preview.id}/commit`,
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
              <p className="text-sm">{t("targets")}</p>
              <p className="text-sm">{t("hotelTargets")}</p>
              <div className="grid gap-3 sm:grid-cols-2">
                {data.coverage.map((c) => (
                  <article
                    key={c.destination_id}
                    className="rounded-2xl border border-[var(--line)] p-5"
                  >
                    <h3 className="font-bold">{t(c.destination_id)}</h3>
                    <dl className="my-3 grid grid-cols-2 gap-2 text-sm">
                      {KINDS.map((k) => (
                        <div key={k}>
                          <dt className="text-[var(--muted)]">{t(k)}</dt>
                          <dd className="font-semibold">{c.counts[k]}</dd>
                        </div>
                      ))}
                    </dl>
                    <p className="text-xs text-[var(--teal)]">
                      {t("hotelReady", { count: c.hotel_ready || 0 })} ·{" "}
                      {t(c.hotel_complete ? "complete" : "incomplete")}
                    </p>
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
          {tab === "config" && config && (
            <section className="space-y-5 rounded-2xl border border-[var(--line)] p-5">
              <QuotePolicies
                policies={config.hotel_quote_policies || {}}
                providers={data.quote_providers || {}}
                brands={data.brand_definitions}
                onChange={(policies) =>
                  setConfig({ ...config, hotel_quote_policies: policies })
                }
              />
              <label className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  checked={config.direct_hotel_links_enabled ?? false}
                  onChange={(e) =>
                    setConfig({
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
              <label className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  checked={config.public_enabled}
                  onChange={(e) =>
                    setConfig({ ...config, public_enabled: e.target.checked })
                  }
                />
                {t("publicEnabled")}
              </label>
              <fieldset>
                <legend className="font-semibold">{t("catalog")}</legend>
                <div className="mt-2 grid grid-cols-2 gap-2">
                  {KINDS.map((k) => (
                    <label className="flex min-h-11 items-center gap-2" key={k}>
                      <input
                        type="checkbox"
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
              <label className="flex min-h-11 items-center gap-3">
                <input
                  type="checkbox"
                  checked={config.airalo_feed_enabled}
                  onChange={(e) =>
                    setConfig({
                      ...config,
                      airalo_feed_enabled: e.target.checked,
                    })
                  }
                />
                {t("feedEnabled")}
              </label>
              <button
                className={button}
                disabled={busy}
                onClick={() =>
                  void run(() =>
                    api("/admin/travel-services/config", {
                      method: "PUT",
                      body: JSON.stringify({
                        ...config,
                        version: data.version,
                      }),
                    }),
                  )
                }
              >
                {t("apply")}
              </button>
            </section>
          )}
        </>
      )}
    </div>
  );
}
