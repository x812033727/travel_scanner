"use client";

import {
  BedDouble,
  Bus,
  Compass,
  ExternalLink,
  Heart,
  LoaderCircle,
  Smartphone,
  X,
} from "lucide-react";
import { useFormatter, useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useId, useRef, useState } from "react";
import { Link, useRouter } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { api, ApiError } from "@/lib/api";
import { useModalSheet } from "@/lib/modal-sheet";
import { useSavedItems } from "@/components/saved-items-provider";

import { KINDS, type Kind } from "./options";
export { KINDS, CITIES, type Kind } from "./options";
const ICONS = {
  hotel: BedDouble,
  transfer: Bus,
  tour: Compass,
  esim: Smartphone,
};
export type Product = {
  id: string;
  kind: Kind;
  destination_id: string;
  title: string;
  source_url: string;
  distance_km: number | null;
  reason: string;
  facts: {
    area_code: string | null;
    country_codes: string[];
    facilities: string[];
    airport: string | null;
    direction: string | null;
    passengers: number | null;
    luggage: number | null;
    languages: Locale[];
    duration_minutes: number | null;
    meeting_point: string | null;
    data_gb: number | null;
    validity_days: number | null;
    unlimited: boolean | null;
    tethering: boolean | null;
    reference_price: number | null;
    currency: string | null;
  };
  offers: {
    id: string;
    brand: string;
    brand_name: string;
    scope: "product" | "destination";
  }[];
};
type Selection = {
  id: string;
  product_id: string;
  kind: Kind;
  title: string;
  status: "planned" | "booked" | "cancelled";
  available: boolean;
  item_id: string | null;
};
type Results = {
  enabled: boolean;
  items: Product[];
  enabled_kinds: Kind[];
  destinations?: string[];
  selections?: Selection[];
  version?: number;
  start_date?: string;
  end_date?: string;
  timezone?: string;
  areas: { code: string; names: Record<string, string> }[];
};
type Config = {
  public_enabled: boolean;
  enabled_kinds: Kind[];
  enabled_destinations: string[];
};
type TripOption = {
  trip_id: string;
  name: string;
  version: number;
  start_date?: string;
  end_date?: string;
};
type Props = {
  destinationId?: string;
  hotspotId?: string;
  tripId?: string;
  initialKind?: Kind;
  initialRadius?: string;
  areaCode?: string;
  day?: string;
  prepare?: () => Promise<{ version: number } | null | undefined | false>;
  onChanged?: () => Promise<void>;
  onBusy?: (busy: boolean) => void;
  initialFilters?: Record<string, string | undefined>;
  compact?: boolean;
};
const field =
  "mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] px-3 py-2 text-sm";
const button =
  "inline-flex min-h-11 min-w-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold disabled:opacity-50";

export function ServiceCatalog({
  destinationId,
  hotspotId,
  tripId,
  initialKind,
  initialRadius,
  areaCode,
  day,
  prepare,
  onChanged,
  onBusy,
  initialFilters,
  compact,
}: Props) {
  const t = useTranslations("travelServices");
  const locale = useLocale();
  const fmt = useFormatter();
  const router = useRouter();
  const saved = useSavedItems();
  const [kind, setKind] = useState<Kind | "all">(initialKind || "all");
  const [area, setArea] = useState(areaCode || "");
  const [radius, setRadius] = useState(initialRadius || "3");
  const [facility, setFacility] = useState(initialFilters?.facility || "");
  const [language, setLanguage] = useState(initialFilters?.language || "");
  const [airport, setAirport] = useState(initialFilters?.airport || "");
  const [direction, setDirection] = useState(initialFilters?.direction || "");
  const [passengers, setPassengers] = useState(
    initialFilters?.passengers || "",
  );
  const [days, setDays] = useState(initialFilters?.days || "");
  const [flightNumber, setFlightNumber] = useState("");
  const [expanded, setExpanded] = useState(false);
  const [data, setData] = useState<Results>();
  const [finishedRequest, setFinishedRequest] = useState("");
  const [error, setError] = useState("");
  const [attempt, setAttempt] = useState(0);
  const [selected, setSelected] = useState<Product>();
  const [showPlatforms, setShowPlatforms] = useState<string>();
  const [trips, setTrips] = useState<TripOption[]>([]);
  const [chosenTrip, setChosenTrip] = useState(tripId || "");
  const [schedule, setSchedule] = useState(false);
  const [date, setDate] = useState(day || "");
  const [start, setStart] = useState("09:00");
  const [end, setEnd] = useState("10:00");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [savedIds, setSavedIds] = useState<string[]>([]);
  const operation = useRef<{ hash: string; key: string } | null>(null);

  const requestKey = JSON.stringify([
    destinationId,
    tripId,
    hotspotId,
    kind,
    area,
    radius,
    facility,
    language,
    airport,
    direction,
    passengers,
    days,
    locale,
    attempt,
  ]);
  const loading = requestKey !== finishedRequest;

  useEffect(() => {
    const abort = new AbortController();
    const params = new URLSearchParams();
    if (destinationId) params.set("destination_id", destinationId);
    if (kind !== "all") params.set("type", kind);
    if (area) params.set("area", area);
    if (facility && !tripId) params.set("facility", facility);
    if (language) params.set("language", language);
    if (airport) params.set("airport", airport);
    if (direction) params.set("direction", direction);
    if (passengers) params.set("passengers", passengers);
    if (days && !tripId) params.set("days", days);
    if (hotspotId && !tripId) {
      params.set("hotspot_id", hotspotId);
      params.set("radius_km", radius);
    }
    const endpoint = tripId
      ? `/trips/${tripId}/travel-services`
      : "/travel-services";
    api<Results>(`${endpoint}?${params}`, { signal: abort.signal })
      .then((result) => {
        if (!abort.signal.aborted) {
          setData(result);
          setError("");
        }
      })
      .catch((reason: unknown) => {
        if (!abort.signal.aborted)
          setError(reason instanceof Error ? reason.message : t("empty"));
      })
      .finally(() => {
        if (!abort.signal.aborted) setFinishedRequest(requestKey);
      });
    if (!tripId) {
      const url = new URL(window.location.href);
      for (const key of [
        "type",
        "area",
        "radius_km",
        "facility",
        "language",
        "airport",
        "direction",
        "passengers",
        "days",
      ]) {
        if (params.has(key)) url.searchParams.set(key, params.get(key)!);
        else url.searchParams.delete(key);
      }
      window.history.replaceState(window.history.state, "", url);
    }
    return () => abort.abort();
  }, [
    destinationId,
    tripId,
    hotspotId,
    kind,
    area,
    radius,
    facility,
    language,
    airport,
    direction,
    passengers,
    days,
    locale,
    attempt,
    requestKey,
    t,
  ]);

  function login(product: Product, intent: "save" | "add") {
    const next = new URL(window.location.href);
    next.searchParams.set("product", product.id);
    next.searchParams.set("intent", intent);
    const local = next.pathname.replace(/^\/(en|ja|ko|zh-TW|zh-CN)(?=\/)/, "");
    router.push(`/login?next=${encodeURIComponent(local + next.search)}`);
  }

  async function save(product: Product) {
    setBusy(true);
    setError("");
    try {
      if (saved.status === "authenticated")
        await saved.setSaved("service", product.id, true);
      else await api(`/saved-items/service/${product.id}`, { method: "PUT" });
      setSavedIds((ids) => [...ids, product.id]);
      setNotice(t("saved"));
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 401)
        login(product, "save");
      else setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function choose(product: Product) {
    setError("");
    setSelected(product);
    setDate(day || data?.start_date || "");
    setSchedule(false);
    setNotice("");
    if (!tripId) {
      setBusy(true);
      try {
        const result = await api<{ items: TripOption[] }>("/trips/options");
        setTrips(result.items);
        setChosenTrip(result.items[0]?.trip_id || "");
        setDate(result.items[0]?.start_date || "");
      } catch (reason) {
        if (reason instanceof ApiError && reason.status === 401)
          login(product, "add");
        else setError((reason as Error).message);
      } finally {
        setBusy(false);
      }
    }
  }

  const resumed = useRef(false);
  useEffect(() => {
    if (tripId || !data?.items.length || resumed.current) return;
    const url = new URL(window.location.href);
    const product = data.items.find(
      (p) => p.id === url.searchParams.get("product"),
    );
    if (!product) return;
    resumed.current = true;
    const intent = url.searchParams.get("intent");
    url.searchParams.delete("intent");
    window.history.replaceState(window.history.state, "", url);
    if (intent === "save")
      void Promise.resolve().then(() => {
        setExpanded(true);
        return save(product);
      });
    else if (intent === "add")
      void Promise.resolve().then(() => {
        setExpanded(true);
        return choose(product);
      });
    else
      document
        .getElementById(`service-${product.id}`)
        ?.scrollIntoView({ block: "center" });
    // Resume a user-requested action once; event handlers deliberately retain current state.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [data, tripId]);

  async function confirm() {
    if (!selected || !chosenTrip) return;
    setBusy(true);
    onBusy?.(true);
    setError("");
    try {
      const prepared = prepare ? await prepare() : undefined;
      if (prepare && !prepared) return;
      const context = await api<Results>(
        `/trips/${chosenTrip}/travel-services`,
      );
      const version = prepared ? prepared.version : context.version;
      // Initial release destinations use fixed JST/KST/Taipei offsets, never the device timezone.
      const offset = selected.destination_id === "taipei" ? "+08:00" : "+09:00";
      const payload = {
        product_id: selected.id,
        version,
        ...(schedule && ["tour", "transfer"].includes(selected.kind)
          ? {
              day_date: date,
              start_time: `${date}T${start}:00${offset}`,
              end_time: `${date}T${end}:00${offset}`,
            }
          : {}),
        ...(selected.kind === "transfer" && schedule
          ? {
              airport: selected.facts.airport,
              direction: selected.facts.direction,
              passengers: Number(passengers),
              flight_number: flightNumber,
            }
          : {}),
      };
      const hash = JSON.stringify({ ...payload, version: undefined });
      if (operation.current?.hash !== hash)
        operation.current = { hash, key: crypto.randomUUID() };
      await api(`/trips/${chosenTrip}/travel-services`, {
        method: "POST",
        headers: { "Idempotency-Key": operation.current.key },
        body: JSON.stringify(payload),
      });
      operation.current = null;
      await onChanged?.();
      setSelected(undefined);
      setNotice(t("updated"));
      setAttempt((value) => value + 1);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
      onBusy?.(false);
    }
  }

  async function status(selection: Selection, value: Selection["status"]) {
    setBusy(true);
    onBusy?.(true);
    setError("");
    try {
      const prepared = prepare ? await prepare() : undefined;
      if (prepare && !prepared) return;
      await api(`/trips/${tripId}/travel-services/${selection.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          status: value,
          version: prepared ? prepared.version : data?.version,
        }),
      });
      await onChanged?.();
      setAttempt((value) => value + 1);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
      onBusy?.(false);
    }
  }

  const selectedTrip = trips.find((trip) => trip.trip_id === chosenTrip);
  if (!loading && data && !data.enabled && compact) return null;
  return (
    <div className="min-w-0 space-y-5">
      <div className="flex flex-wrap gap-2" aria-label={t("title")}>
        {(["all", ...KINDS] as const).map((value) => (
          <button
            type="button"
            className={`${button} ${kind === value ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : ""}`}
            key={value}
            aria-pressed={kind === value}
            onClick={() => {
              setKind(value);
              setExpanded(false);
            }}
          >
            {t(value)}
          </button>
        ))}
      </div>
      <div className="grid min-w-0 gap-5 lg:grid-cols-[180px_minmax(0,1fr)]">
        <aside className="grid grid-cols-2 content-start gap-3 text-sm lg:sticky lg:top-0 lg:grid-cols-1 lg:self-start">
          {(kind === "hotel" || kind === "all") && (
            <>
              <label>
                {t("area")}
                <select
                  className={field}
                  value={area}
                  onChange={(e) => setArea(e.target.value)}
                >
                  <option value="">{t("all")}</option>
                  {Array.from(
                    new Map(
                      (data?.areas || []).map((a) => [a.code, a]),
                    ).values(),
                  ).map((a) => (
                    <option key={a.code} value={a.code}>
                      {a.names[locale] || a.names.en || a.code}
                    </option>
                  ))}
                </select>
              </label>
              {hotspotId && (
                <label>
                  {t("radius")}
                  <select
                    className={field}
                    value={radius}
                    onChange={(e) => setRadius(e.target.value)}
                  >
                    {[1, 3, 5].map((km) => (
                      <option value={km} key={km}>
                        {fmt.number(km, { style: "unit", unit: "kilometer" })}
                      </option>
                    ))}
                  </select>
                </label>
              )}
              {!tripId && (
                <label>
                  {t("facility")}
                  <select
                    className={field}
                    value={facility}
                    onChange={(e) => setFacility(e.target.value)}
                  >
                    <option value="">{t("all")}</option>
                    {[
                      "wifi",
                      "breakfast",
                      "accessible",
                      "family",
                      "laundry",
                    ].map((f) => (
                      <option key={f} value={f}>
                        {t(f)}
                      </option>
                    ))}
                  </select>
                </label>
              )}
            </>
          )}
          {kind === "transfer" && (
            <>
              <label>
                {t("airport")}
                <select
                  className={field}
                  value={airport}
                  onChange={(e) => setAirport(e.target.value)}
                >
                  <option value="">{t("all")}</option>
                  {[
                    "NRT",
                    "HND",
                    "KIX",
                    "ITM",
                    "ICN",
                    "GMP",
                    "PUS",
                    "TPE",
                    "TSA",
                  ].map((a) => (
                    <option key={a}>{a}</option>
                  ))}
                </select>
              </label>
              <label>
                {t("direction")}
                <select
                  className={field}
                  value={direction}
                  onChange={(e) => setDirection(e.target.value)}
                >
                  <option value="">{t("all")}</option>
                  {["arrival", "departure", "roundtrip"].map((a) => (
                    <option value={a} key={a}>
                      {t(a)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t("passengers")}
                <input
                  type="number"
                  min={1}
                  max={100}
                  className={field}
                  value={passengers}
                  onChange={(e) => setPassengers(e.target.value)}
                />
              </label>
            </>
          )}
          {kind === "tour" && (
            <label>
              {t("language")}
              <select
                className={field}
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                <option value="">{t("all")}</option>
                {Object.entries(localeLabels).map(([code, label]) => (
                  <option value={code} key={code}>
                    {label}
                  </option>
                ))}
              </select>
            </label>
          )}
          {kind === "esim" && !tripId && (
            <label>
              {t("days")}
              <input
                type="number"
                min={1}
                max={365}
                className={field}
                value={days}
                onChange={(e) => setDays(e.target.value)}
              />
            </label>
          )}
        </aside>
        <div className="min-w-0 space-y-5" aria-busy={loading}>
          {loading && (
            <p role="status" className="flex items-center gap-2">
              <LoaderCircle className="animate-spin" size={18} />
              {t("loading")}
            </p>
          )}
          {error && (
            <div
              role="alert"
              className="rounded-xl bg-[var(--coral-soft)] p-4 text-sm"
            >
              {error}
              <button
                type="button"
                onClick={() => setAttempt((v) => v + 1)}
                className={`${button} ml-2`}
              >
                {t("retry")}
              </button>
            </div>
          )}
          {notice && (
            <p
              role="status"
              className="rounded-xl bg-[var(--teal-soft)] p-3 text-sm"
            >
              {notice}
            </p>
          )}
          {!loading && data && !data.enabled && <p>{t("disabled")}</p>}
          {!loading && data?.enabled && data.items.length === 0 && (
            <p className="rounded-2xl border border-dashed border-[var(--line)] p-6">
              {t("empty")}
            </p>
          )}
          {!loading &&
            KINDS.filter((k) => kind === "all" || kind === k).map((k) => {
              const products = data?.items.filter((p) => p.kind === k) || [];
              if (!products.length) return null;
              const Icon = ICONS[k];
              return (
                <section key={k} className="space-y-3" aria-label={t(k)}>
                  <h3 className="flex items-center gap-2 text-lg font-bold">
                    <Icon size={20} className="text-[var(--teal)]" />
                    {t(k)}
                  </h3>
                  {(expanded ? products : products.slice(0, 3)).map(
                    (product) => (
                      <article
                        id={`service-${product.id}`}
                        key={product.id}
                        className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface-raised)] p-4 sm:p-5"
                      >
                        <p className="mb-2 text-xs font-semibold text-[var(--teal)]">
                          {t(product.destination_id)} · {t(product.reason)}
                        </p>
                        <h4 className="break-words text-lg font-bold leading-snug">
                          {product.title}
                        </h4>
                        <div className="mt-2 space-y-1 text-sm text-[var(--muted)]">
                          {product.distance_km != null && (
                            <p>
                              {t("distance", {
                                km: fmt.number(product.distance_km, {
                                  maximumFractionDigits: 1,
                                }),
                              })}
                            </p>
                          )}
                          {k === "hotel" && (
                            <>
                              {product.facts.area_code && (
                                <p>
                                  {t("area")}:{" "}
                                  {(() => {
                                    const area = data?.areas.find(
                                      (a) => a.code === product.facts.area_code,
                                    );
                                    return (
                                      area?.names[locale] ||
                                      area?.names.en ||
                                      product.facts.area_code
                                    );
                                  })()}
                                </p>
                              )}
                              <p>{t("externalPrices")}</p>
                            </>
                          )}
                          {k === "transfer" && (
                            <p>
                              {product.facts.airport} ·{" "}
                              {t(product.facts.direction || "unknown")} ·{" "}
                              {t("passengers")}:{" "}
                              {product.facts.passengers ?? t("unknown")}
                            </p>
                          )}
                          {k === "tour" && (
                            <p>
                              {t("language")}:{" "}
                              {product.facts.languages.length
                                ? product.facts.languages
                                    .map((l) => localeLabels[l])
                                    .join(" · ")
                                : t("unknown")}
                            </p>
                          )}
                          {k === "esim" && (
                            <>
                              <p>
                                {product.facts.country_codes.join(" · ")} ·{" "}
                                {product.facts.validity_days
                                  ? t("validity", {
                                      days: product.facts.validity_days,
                                    })
                                  : t("unknown")}{" "}
                                ·{" "}
                                {product.facts.unlimited
                                  ? t("unlimited")
                                  : product.facts.data_gb
                                    ? t("data", { gb: product.facts.data_gb })
                                    : t("unknown")}
                              </p>
                              {product.facts.reference_price != null &&
                                product.facts.currency && (
                                  <p>
                                    {t("reference")}:{" "}
                                    {fmt.number(product.facts.reference_price, {
                                      style: "currency",
                                      currency: product.facts.currency,
                                    })}
                                  </p>
                                )}
                            </>
                          )}
                        </div>
                        <div className="mt-4 flex flex-wrap gap-2">
                          <button
                            type="button"
                            disabled={busy}
                            className={`${button} bg-[var(--teal)] text-white`}
                            onClick={() => void choose(product)}
                          >
                            {t(
                              k === "hotel"
                                ? "selectHotel"
                                : k === "esim"
                                  ? "addChecklist"
                                  : "add",
                            )}
                          </button>
                          <button
                            type="button"
                            aria-expanded={showPlatforms === product.id}
                            className={button}
                            onClick={() =>
                              setShowPlatforms(
                                showPlatforms === product.id
                                  ? undefined
                                  : product.id,
                              )
                            }
                          >
                            {t("platforms")}
                          </button>
                          <button
                            type="button"
                            disabled={busy}
                            className={button}
                            onClick={() => void save(product)}
                            aria-label={`${t("save")} · ${product.title}`}
                          >
                            <Heart
                              size={17}
                              fill={
                                saved.isSaved("service", product.id) ||
                                savedIds.includes(product.id)
                                  ? "currentColor"
                                  : "none"
                              }
                            />
                          </button>
                        </div>
                        {showPlatforms === product.id && (
                          <div className="mt-4 space-y-3 border-t border-[var(--line)] pt-4">
                            <p className="text-xs text-[var(--muted)]">
                              {t("disclosure")}
                            </p>
                            {product.offers.length === 0 && (
                              <p className="text-sm">{t("noOffers")}</p>
                            )}
                            {product.offers.map((offer) => (
                              <form
                                key={offer.id}
                                action={`/api/travel/affiliates/offers/${offer.id}/clickout?locale=${locale}&placement=${tripId ? "trip" : hotspotId ? "hotspot" : "destination"}`}
                                method="post"
                                target="_blank"
                                rel="noopener noreferrer"
                              >
                                <button
                                  className={`${button} w-full justify-between text-left`}
                                  type="submit"
                                  aria-label={`${offer.brand_name} · ${t(offer.scope === "product" ? "productScope" : "destinationScope")} · ${t("newTab")}`}
                                >
                                  <span>
                                    {offer.brand_name}
                                    <small className="block text-xs font-normal">
                                      {t(
                                        offer.scope === "product"
                                          ? "productScope"
                                          : "destinationScope",
                                      )}
                                    </small>
                                  </span>
                                  <ExternalLink size={16} />
                                </button>
                              </form>
                            ))}
                            {k === "esim" && (
                              <p className="text-xs">
                                {t("tethering")}:{" "}
                                {product.facts.tethering == null
                                  ? t("unknown")
                                  : t(product.facts.tethering ? "yes" : "no")}
                              </p>
                            )}
                            {k === "transfer" && (
                              <p className="text-xs">
                                {t("luggage")}:{" "}
                                {product.facts.luggage ?? t("unknown")}
                              </p>
                            )}
                            {k === "tour" && (
                              <p className="text-xs">
                                {t("meeting")}:{" "}
                                {product.facts.meeting_point || t("unknown")} ·{" "}
                                {t("duration")}:{" "}
                                {product.facts.duration_minutes ?? t("unknown")}
                              </p>
                            )}
                            <a
                              href={product.source_url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="inline-flex min-h-11 items-center text-sm underline"
                              aria-label={`${t("source")} · ${t("newTab")}`}
                            >
                              {t("source")}
                            </a>
                          </div>
                        )}
                        {selected?.id === product.id && (
                          <div className="mt-4 space-y-3 rounded-2xl bg-[var(--paper)] p-4">
                            {!tripId && (
                              <label className="block text-sm">
                                {t("chooseTrip")}
                                <select
                                  className={field}
                                  value={chosenTrip}
                                  onChange={(e) => {
                                    setChosenTrip(e.target.value);
                                    setDate(
                                      trips.find(
                                        (tr) => tr.trip_id === e.target.value,
                                      )?.start_date || "",
                                    );
                                  }}
                                >
                                  <option value="">{t("chooseTrip")}</option>
                                  {trips.map((tr) => (
                                    <option key={tr.trip_id} value={tr.trip_id}>
                                      {tr.name}
                                    </option>
                                  ))}
                                </select>
                              </label>
                            )}
                            {!tripId && trips.length === 0 && !busy && (
                              <Link href="/trips/new" className={button}>
                                {t("noTrips")}
                              </Link>
                            )}
                            {k === "hotel" ? (
                              <p className="text-sm">
                                {t("lodgingImpact", {
                                  start:
                                    selectedTrip?.start_date ||
                                    data?.start_date ||
                                    t("unknown"),
                                  end:
                                    selectedTrip?.end_date ||
                                    data?.end_date ||
                                    t("unknown"),
                                })}
                              </p>
                            ) : ["transfer", "tour"].includes(k) ? (
                              <>
                                <label className="flex min-h-11 items-center gap-2 text-sm">
                                  <input
                                    type="checkbox"
                                    checked={schedule}
                                    onChange={(e) =>
                                      setSchedule(e.target.checked)
                                    }
                                  />
                                  {t("schedule")}
                                </label>
                                <p className="text-xs text-[var(--muted)]">
                                  {t("unscheduled")}
                                </p>
                                {schedule && (
                                  <div className="grid grid-cols-2 gap-3">
                                    <label className="col-span-2 text-sm">
                                      {t("day")}
                                      <input
                                        type="date"
                                        min={
                                          selectedTrip?.start_date ||
                                          data?.start_date
                                        }
                                        max={
                                          selectedTrip?.end_date ||
                                          data?.end_date
                                        }
                                        value={date}
                                        onChange={(e) =>
                                          setDate(e.target.value)
                                        }
                                        className={field}
                                      />
                                    </label>
                                    <label>
                                      {t("start")}
                                      <input
                                        type="time"
                                        value={start}
                                        onChange={(e) =>
                                          setStart(e.target.value)
                                        }
                                        className={field}
                                      />
                                    </label>
                                    <label>
                                      {t("end")}
                                      <input
                                        type="time"
                                        value={end}
                                        onChange={(e) => setEnd(e.target.value)}
                                        className={field}
                                      />
                                    </label>
                                    {k === "transfer" && (
                                      <>
                                        <label>
                                          {t("passengers")}
                                          <input
                                            type="number"
                                            min={1}
                                            max={
                                              product.facts.passengers || 100
                                            }
                                            value={passengers}
                                            onChange={(e) =>
                                              setPassengers(e.target.value)
                                            }
                                            className={field}
                                          />
                                        </label>
                                        <label>
                                          {t("flightNumber")}
                                          <input
                                            className={field}
                                            value={flightNumber}
                                            maxLength={8}
                                            autoCapitalize="characters"
                                            autoComplete="off"
                                            onChange={(e) =>
                                              setFlightNumber(
                                                e.target.value
                                                  .toUpperCase()
                                                  .replace(/\s/g, ""),
                                              )
                                            }
                                          />
                                        </label>
                                      </>
                                    )}
                                  </div>
                                )}
                              </>
                            ) : null}
                            <div className="sticky bottom-0 bg-[var(--paper)] pb-[env(safe-area-inset-bottom)] pt-2">
                              <button
                                type="button"
                                disabled={
                                  busy ||
                                  !chosenTrip ||
                                  (schedule &&
                                    (!date ||
                                      (selected?.kind === "transfer" &&
                                        (!passengers || !flightNumber))))
                                }
                                className={`${button} w-full bg-[var(--teal)] text-white`}
                                onClick={() => void confirm()}
                              >
                                {busy ? (
                                  <LoaderCircle
                                    size={18}
                                    className="animate-spin"
                                  />
                                ) : null}
                                {t("confirm")}
                              </button>
                            </div>
                          </div>
                        )}
                      </article>
                    ),
                  )}
                  {!expanded && products.length > 3 && (
                    <button
                      className={`${button} w-full`}
                      onClick={() => setExpanded(true)}
                    >
                      {t("viewAll", { count: products.length })}
                    </button>
                  )}
                </section>
              );
            })}
          {data?.selections && data.selections.length > 0 && (
            <section className="space-y-3 border-t border-[var(--line)] pt-4">
              <h3 className="font-bold">{t("selections")}</h3>
              <p className="text-xs leading-5 text-[var(--muted)]">
                {t("statusHint")}
              </p>
              {data.selections.map((s) => (
                <div
                  key={s.id}
                  className="rounded-xl border border-[var(--line)] p-3"
                >
                  <p className="font-semibold">{s.title}</p>
                  {!s.item_id &&
                    s.available &&
                    ["tour", "transfer"].includes(s.kind) &&
                    data.items.some((p) => p.id === s.product_id) && (
                      <button
                        type="button"
                        className={button}
                        disabled={busy}
                        onClick={() => {
                          const product = data.items.find(
                            (p) => p.id === s.product_id,
                          );
                          if (product) {
                            setExpanded(true);
                            void choose(product).then(() => {
                              setSchedule(true);
                              document
                                .getElementById(`service-${product.id}`)
                                ?.scrollIntoView({ block: "center" });
                            });
                          }
                        }}
                      >
                        {t("schedule")}
                      </button>
                    )}
                  {!s.available && (
                    <p className="text-xs">{t("unavailable")}</p>
                  )}
                  <label className="text-sm">
                    {t(s.kind)}
                    <select
                      className={field}
                      value={s.status}
                      disabled={busy}
                      onChange={(e) =>
                        void status(s, e.target.value as Selection["status"])
                      }
                    >
                      {["planned", "booked", "cancelled"].map((value) => (
                        <option key={value} value={value}>
                          {t(value)}
                        </option>
                      ))}
                    </select>
                  </label>
                </div>
              ))}
            </section>
          )}
        </div>
      </div>
    </div>
  );
}

export function TripTravelServices(
  props: Props & { tripId: string; disabled?: boolean },
) {
  const t = useTranslations("travelServices");
  const common = useTranslations("common");
  const [config, setConfig] = useState<Config>();
  const [open, setOpen] = useState<Kind>();
  const id = useId();
  const touch = useRef<number | undefined>(undefined);
  const close = useCallback(() => {
    if (window.history.state?.serviceSheet === id) window.history.back();
    else setOpen(undefined);
  }, [id]);
  const ref = useModalSheet<HTMLDivElement>(Boolean(open), close);
  useEffect(() => {
    api<Config>("/travel-services/config")
      .then(setConfig)
      .catch(() => undefined);
  }, []);
  useEffect(() => {
    const back = () => setOpen(undefined);
    window.addEventListener("popstate", back);
    return () => window.removeEventListener("popstate", back);
  }, []);
  if (!config?.enabled_kinds?.length) return null;
  return (
    <section
      className="mb-4 rounded-2xl border border-[var(--line)] bg-[var(--surface-raised)] p-3"
      aria-label={t("title")}
    >
      <div className="grid grid-cols-2 gap-2 sm:grid-cols-4">
        {KINDS.filter((k) => config.enabled_kinds.includes(k)).map((k) => {
          const Icon = ICONS[k];
          return (
            <button
              className={`${button} justify-start`}
              key={k}
              disabled={props.disabled}
              onClick={() => {
                window.history.pushState(
                  { ...window.history.state, serviceSheet: id },
                  "",
                );
                setOpen(k);
              }}
            >
              <Icon className="shrink-0 text-[var(--teal)]" size={18} />
              {t(k)}
            </button>
          );
        })}
      </div>
      {open && (
        <div
          className="planner-overlay"
          onMouseDown={(e) => {
            if (e.target === e.currentTarget) close();
          }}
        >
          <div
            ref={ref}
            role="dialog"
            aria-modal="true"
            aria-labelledby={id}
            className="planner-sheet planner-sheet-wide planner-sheet-expanded h-dvh"
          >
            <header
              className="flex items-center justify-between gap-3 border-b border-[var(--line)] px-5 pb-4 pt-[max(1rem,env(safe-area-inset-top))]"
              onTouchStart={(e) => {
                touch.current = e.touches[0].clientY;
              }}
              onTouchEnd={(e) => {
                if (
                  touch.current != null &&
                  e.changedTouches[0].clientY - touch.current > 100
                )
                  close();
              }}
            >
              <h2 id={id} className="text-xl font-bold">
                {t(open)}
              </h2>
              <button
                className={button}
                type="button"
                aria-label={common("close")}
                onClick={close}
              >
                <X size={20} />
              </button>
            </header>
            <div className="planner-sheet-body">
              <ServiceCatalog {...props} initialKind={open} />
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export function DestinationServicesLink({
  destinationId,
  hotspotId,
}: {
  destinationId: string;
  hotspotId?: string;
}) {
  const t = useTranslations("travelServices");
  const [config, setConfig] = useState<Config>();
  useEffect(() => {
    api<Config>("/travel-services/config")
      .then(setConfig)
      .catch(() => undefined);
  }, []);
  const cities =
    destinationId === "osaka-kyoto" ? ["osaka", "kyoto"] : [destinationId];
  if (!config?.public_enabled) return null;
  return (
    <div className="my-4 flex flex-wrap gap-2">
      {cities
        .filter((city) => config.enabled_destinations.includes(city))
        .map((city) => (
          <Link
            key={city}
            href={`/destinations/${city}/services${hotspotId ? `?type=hotel&hotspot_id=${hotspotId}` : ""}`}
            className={button}
          >
            <BedDouble size={18} />
            {t(hotspotId ? "nearby" : "destinationLink")} · {t(city)}
          </Link>
        ))}
    </div>
  );
}
