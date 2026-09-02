"use client";

import {
  AlertCircle,
  BadgeCheck,
  Check,
  Clock3,
  ExternalLink,
  Hotel,
  LoaderCircle,
  MapPinned,
  Plane,
  Save,
  Sparkles,
  TrainFront,
} from "lucide-react";
import Image from "next/image";
import { useLocale } from "next-intl";
import { useSearchParams } from "next/navigation";
import { Link, useRouter } from "@/i18n/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ApiError, api, isUsageInsufficient, twd } from "@/lib/api";
import { trackAnalytics } from "@/lib/analytics";
import { loginPath } from "@/lib/navigation";
import {
  destinationByAirport,
  interestLabel,
  interests as destinationInterests,
} from "@/lib/destinations";
import {
  BudgetBreakdown,
  type BudgetCost,
} from "@/components/budget-breakdown";
import { AirbnbSearchPanel } from "@/components/airbnb-search-panel";
import {
  HotelOfferCard,
  hotelNightlyPrice,
  hotelRating,
  hotelStarRating,
} from "@/components/hotel-offer-card";
import { FlightOfferCard } from "@/components/flight-offer-card";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import {
  FlightDateOptions,
  type FlightDateOption,
} from "@/components/flight-date-options";
import {
  AffiliatePartnerOptions,
  type AffiliateModule,
} from "@/components/affiliate-partner-options";
import {
  SearchCriteriaEditor,
  type CriteriaUpdate,
} from "@/components/search-criteria-editor";
import { featureEnabled } from "@/lib/site-features";

type Parsed = {
  origin?: string;
  destination?: string;
  departure_date?: string;
  return_date?: string;
  flex_days?: 0 | 3 | 7;
  departure_month?: string;
  travelers: {
    adults: number;
    children?: number;
    children_ages?: number[];
    rooms?: number;
  };
  trip_length_days?: number;
  budget_twd?: number;
  interests: string[];
  extension_destination_ids: string[];
  avoid_red_eye: boolean;
  hotel_min_rating?: number;
  hotel_min_nightly_twd?: number;
  hotel_max_nightly_twd?: number;
  accepted_property_types?: string[];
  hotel_min_review_score?: number;
  hotel_min_review_count?: number;
  breakfast_required?: boolean;
  refundable_required?: boolean;
  include_airbnb?: boolean;
  max_station_walk_minutes?: number;
  preferred_area?: string;
  preferred_areas?: string[];
  pace?: "relaxed" | "balanced" | "packed";
  confidence: number;
  missing_fields: string[];
};

type Offer = Record<string, unknown> & {
  id: string;
  provider?: string;
  source_mode?: "live" | "test" | "mock" | "estimate";
  is_mock?: boolean;
  is_bookable?: boolean;
  is_fallback?: boolean;
  action_kind?: "deep_link" | "recheck" | "none";
  booking_url?: string | null;
  images?: string[];
  attributions?: string[];
  attribution_urls?: string[];
  breakfast_included?: boolean;
  refundable?: boolean;
  retrieved_at?: string;
  expires_at?: string;
};

type ItineraryDay = {
  date: string;
  label: string;
  items: Array<{ title: string }>;
};

type Plan = {
  id: string;
  mode: string;
  title: string;
  duplicate: boolean;
  total_cost: BudgetCost;
  flight?: Offer;
  hotel?: Offer;
  activity?: Offer;
  transport?: Offer;
  itinerary?: ItineraryDay[];
  pros: string[];
  cons: string[];
  compared_with_cheapest: {
    price_difference: string | number;
    flight_minutes_saved: number;
  };
};

type ProviderStatus = {
  provider: string;
  mode: "live" | "test" | "mock" | "disabled";
  status: "ready" | "not_configured" | "disabled";
  modules: string[];
  message: string;
  module_statuses?: Record<
    string,
    {
      selected_provider: string;
      status: "ready" | "not_configured" | "disabled";
      available: boolean;
      configured: boolean;
      fallback_provider?: string | null;
      candidate_providers?: string[];
      strategy?: string | null;
      environment: string;
      message: string;
    }
  >;
};

type UsageStatus = {
  status: "reserved" | "charged" | "released";
  uses: number;
  reference: string;
};

type SearchResult = {
  status: string;
  result?: {
    modules?: Record<string, Offer[]>;
    plans?: Plan[];
    flight_date_options?: FlightDateOption[];
  };
  warnings?: string[];
  usage?: UsageStatus;
};

const stages = [
  { key: "flight", label: "機票", icon: Plane },
  { key: "hotel", label: "住宿", icon: Hotel },
  { key: "activities", label: "活動", icon: MapPinned },
  { key: "transport", label: "接送", icon: TrainFront },
];

const sourceLabels = {
  live: "正式即時資料",
  test: "供應商測試資料",
  mock: "模擬資料",
  estimate: "估算資料",
};

function amount(offer: Offer): number {
  return Number(offer.total_price ?? offer.price ?? 0);
}

function flightTimeSummary(offer: Offer) {
  const time = (value: unknown) =>
    typeof value === "string" ? value.match(/T(\d{2}:\d{2})/)?.[1] : undefined;
  const outbound = `${time(offer.departure_time) || "時間待確認"}–${time(offer.arrival_time) || "時間待確認"}`;
  const returning = offer.return_departure_time
    ? ` · 回程 ${time(offer.return_departure_time) || "時間待確認"}–${time(offer.return_arrival_time) || "時間待確認"}`
    : "";
  return `去程 ${outbound}${returning}`;
}

function titleFor(module: string, offer: Offer): string {
  if (module === "flight")
    return String(offer.airline ?? offer.flight_number ?? "航班");
  if (module === "hotel") return String(offer.hotel_name ?? "住宿方案");
  if (module === "activities") return String(offer.title ?? "在地活動");
  return String(offer.transport_type ?? "交通接送");
}

function detailsFor(module: string, offer: Offer): string {
  if (module === "flight") {
    const stops = Number(offer.stops ?? 0);
    return `${offer.origin ?? ""} → ${offer.destination ?? ""} · ${stops ? `${stops} 次轉機` : "直飛"}`;
  }
  if (module === "hotel") {
    const rating = Number(offer.review_score ?? offer.rating ?? 0);
    const property =
      offer.property_type === "vacation_rental"
        ? "整套公寓／民宿"
        : offer.property_type === "serviced_apartment"
          ? "服務式公寓"
          : "飯店";
    const reviews = offer.review_count
      ? `${offer.review_count} 則評論`
      : "評論數未知";
    const extras = [
      property,
      reviews,
      offer.breakfast_included ? "含早餐" : null,
      offer.refundable ? "可退款" : null,
      offer.station_walk_minutes
        ? `步行 ${offer.station_walk_minutes} 分鐘到車站`
        : null,
    ]
      .filter(Boolean)
      .join(" · ");
    return `${rating ? `${rating.toFixed(1)} 分` : "尚無評分"} · ${offer.nights ?? "-"} 晚 · ${offer.room_type ?? "客房"}${extras ? ` · ${extras}` : ""}`;
  }
  if (module === "activities")
    return `${interestLabel(String(offer.category || ""))} · ${offer.duration_minutes ?? "-"} 分鐘 · ${offer.address ?? offer.city ?? ""}`;
  return `${offer.duration_minutes ?? "-"} 分鐘 · ${offer.origin ?? ""} → ${offer.destination ?? ""}`;
}

function recheckUrl(
  module: string,
  offer: Offer,
  parsed: Parsed | null,
  dates: string[],
  locale: string,
) {
  if (offer.action_kind === "deep_link" && offer.booking_url)
    return offer.booking_url;
  const query =
    module === "hotel"
      ? `${titleFor(module, offer)} ${parsed?.destination ?? ""} ${dates[0]} ${dates[1]}`
      : `${titleFor(module, offer)} ${parsed?.origin ?? ""} ${parsed?.destination ?? ""} ${dates[0]}`;
  return `https://www.google.com/travel/search?q=${encodeURIComponent(query)}&hl=${encodeURIComponent(locale)}`;
}

function parseInterests(raw: string): string[] {
  const mapping: Array<[string, string]> = [
    ["美食", "food"],
    ["購物", "shopping"],
    ["文化", "culture"],
    ["自然", "nature"],
    ["親子", "family"],
    ["夜生活", "nightlife"],
    ["溫泉", "spa"],
    ["SPA", "spa"],
    ["海灘", "beach"],
    ["跳島", "beach"],
  ];
  const supported = new Set(destinationInterests.map((item) => item.code));
  const codes = raw
    .split(",")
    .map((item) => item.trim())
    .filter((item) => supported.has(item));
  const labels = mapping
    .filter(([label]) => raw.includes(label))
    .map(([, code]) => code);
  return Array.from(new Set([...codes, ...labels]));
}

export function SearchExperience() {
  const charge = useOperationCharge("full_trip_search");
  const visibility = useSiteVisibility();
  const tripsEnabled = featureEnabled(visibility, "trips");
  const locale = useLocale();
  const params = useSearchParams();
  const router = useRouter();
  const text = params.get("q") || "";
  const structuredParsed = useMemo<Parsed | null>(() => {
    const origin = params.get("origin");
    const destination = params.get("destination");
    if (!origin || !destination || !params.get("departure_date")) return null;
    const rawInterests = params.get("interests") || "";
    return {
      origin,
      destination,
      departure_date: params.get("departure_date") || undefined,
      return_date: params.get("return_date") || undefined,
      flex_days: Number(params.get("flex_days") || 0) as Parsed["flex_days"],
      travelers: {
        adults: Number(params.get("adults") || 1),
        children: Number(params.get("children") || 0),
        children_ages: (params.get("children_ages") || "")
          .split(",")
          .filter(Boolean)
          .map(Number),
        rooms: Number(params.get("rooms") || 1),
      },
      budget_twd: Number(params.get("budget_twd") || 0) || undefined,
      interests: parseInterests(rawInterests),
      extension_destination_ids: (params.get("extension_destination_ids") || "")
        .split(",")
        .filter(Boolean),
      avoid_red_eye:
        params.get("avoid_red_eye") === "true" || rawInterests.includes("紅眼"),
      hotel_min_rating:
        Number(params.get("hotel_min_rating") || 0) || undefined,
      hotel_min_nightly_twd:
        Number(params.get("hotel_min_nightly_twd") || 0) || undefined,
      hotel_max_nightly_twd:
        Number(params.get("hotel_max_nightly_twd") || 0) || undefined,
      accepted_property_types: (params.get("accepted_property_types") || "")
        .split(",")
        .filter(Boolean),
      hotel_min_review_score:
        Number(params.get("hotel_min_review_score") || 0) || undefined,
      hotel_min_review_count:
        Number(params.get("hotel_min_review_count") || 0) || undefined,
      breakfast_required: params.get("breakfast_required") === "true",
      refundable_required: params.get("refundable_required") === "true",
      include_airbnb: params.get("include_airbnb") !== "false",
      max_station_walk_minutes:
        Number(params.get("max_station_walk_minutes") || 0) || undefined,
      preferred_area:
        params.get("preferred_area") ||
        params.get("preferred_areas") ||
        undefined,
      preferred_areas: (params.get("preferred_areas") || "")
        .split(",")
        .filter(Boolean),
      pace: (params.get("pace") as Parsed["pace"]) || "balanced",
      confidence: 1,
      missing_fields: [],
    };
  }, [params]);
  const [parsedResult, setParsedResult] = useState<Parsed | null>(null);
  const parsed = structuredParsed || parsedResult;
  const [providerStatus, setProviderStatus] = useState<ProviderStatus | null>(
    null,
  );
  const [authState, setAuthState] = useState<
    "checking" | "signed_in" | "signed_out" | "error"
  >("checking");
  const [progress, setProgress] = useState(0);
  const [done, setDone] = useState<string[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [offers, setOffers] = useState<Record<string, Offer[]>>({});
  const [warnings, setWarnings] = useState<string[]>([]);
  const [searchId, setSearchId] = useState<string>();
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  const [expandingSources, setExpandingSources] = useState(false);
  const [usageState, setUsageState] = useState<UsageStatus>();
  const [flightDateOptions, setFlightDateOptions] = useState<
    FlightDateOption[]
  >([]);
  const [selectedDateOption, setSelectedDateOption] =
    useState<FlightDateOption>();
  const [activeTab, setActiveTab] = useState("plans");
  const [breakfastOnly, setBreakfastOnly] = useState(
    params.get("breakfast_required") === "true",
  );
  const [refundableOnly, setRefundableOnly] = useState(
    params.get("refundable_required") === "true",
  );
  const [directOnly, setDirectOnly] = useState(false);
  const [refundableFlightOnly, setRefundableFlightOnly] = useState(false);
  const [activityInterest, setActivityInterest] = useState("all");
  const [sortByPrice, setSortByPrice] = useState(false);
  const [hotelMinRating, setHotelMinRating] = useState(
    Number(params.get("hotel_min_rating") || 0),
  );
  const [hotelNightlyMax, setHotelNightlyMax] = useState(
    Number(params.get("hotel_max_nightly_twd") || 0),
  );
  const [hotelMaxWalk, setHotelMaxWalk] = useState(
    Number(params.get("max_station_walk_minutes") || 0),
  );
  const [hotelSort, setHotelSort] = useState<
    "recommended" | "price" | "rating" | "distance"
  >("recommended");
  const started = useRef(false);

  const resolveAuth = useCallback(() => {
    return api<{ id: string }>("/auth/me")
      .then(() => setAuthState("signed_in"))
      .catch((reason) =>
        setAuthState(
          reason instanceof ApiError && reason.status === 401
            ? "signed_out"
            : "error",
        ),
      );
  }, []);

  const checkAuth = useCallback(() => {
    setAuthState("checking");
    void resolveAuth();
  }, [resolveAuth]);

  useEffect(() => {
    void resolveAuth();
  }, [resolveAuth]);

  useEffect(() => {
    api<ProviderStatus>("/providers/status")
      .then(setProviderStatus)
      .catch(() => setError("目前無法確認即時資料服務狀態，請稍後再試。"));
  }, []);

  useEffect(() => {
    if (structuredParsed || started.current || !text) return;
    started.current = true;
    api<Parsed>("/ai/parse-trip", {
      method: "POST",
      body: JSON.stringify({ text }),
    })
      .then(setParsedResult)
      .catch((reason: Error) => setError(reason.message));
  }, [structuredParsed, text]);

  const dates = useMemo(() => {
    if (parsed?.departure_date) {
      const departure = parsed.departure_date;
      const returning = parsed.return_date || departure;
      return [departure, returning];
    }
    const departure = parsed?.departure_month
      ? new Date(parsed.departure_month)
      : new Date("2026-11-01");
    departure.setDate(10);
    const returning = new Date(departure);
    returning.setDate(departure.getDate() + (parsed?.trip_length_days || 5));
    return [
      departure.toISOString().slice(0, 10),
      returning.toISOString().slice(0, 10),
    ];
  }, [parsed]);

  async function loadFinal(id: string) {
    const result = await api<SearchResult>(`/searches/${id}`);
    if (result.result?.modules) setOffers(result.result.modules);
    if (result.result?.plans) setPlans(result.result.plans);
    setFlightDateOptions(result.result?.flight_date_options || []);
    setWarnings(result.warnings || []);
    if (result.usage) setUsageState(result.usage);
  }

  async function expandFlightSources() {
    if (!searchId) return;
    setExpandingSources(true);
    setError(undefined);
    try {
      const result = await api<{
        offers: Offer[];
        provider_statuses: Array<{ provider: string; status: string }>;
      }>(`/searches/${searchId}/flight-sources/expand`, {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
      });
      setOffers((current) => ({ ...current, flight: result.offers }));
      const failed = result.provider_statuses
        .filter((item) => item.status === "failed")
        .map((item) => `${item.provider} 暫時無法取得`);
      if (failed.length)
        setWarnings((current) => Array.from(new Set([...current, ...failed])));
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setExpandingSources(false);
    }
  }

  async function begin(
    requestedDates: string[] = dates,
    requestedFlexDays: 0 | 3 | 7 = parsed?.flex_days || 0,
  ) {
    if (!parsed || providerStatus?.status !== "ready") return;
    setBusy(true);
    setError(undefined);
    setProgress(2);
    try {
      const accepted = await api<{ search_id: string; usage: UsageStatus }>(
        "/searches",
        {
          method: "POST",
          headers: { "Idempotency-Key": crypto.randomUUID() },
          body: JSON.stringify({
            trip_type: "round_trip",
            origin: parsed.origin || "TPE",
            destination: parsed.destination || "NRT",
            departure_date: requestedDates[0],
            return_date: requestedDates[1],
            flexible_dates: requestedFlexDays > 0,
            flex_days: requestedFlexDays,
            travelers: {
              adults: parsed.travelers.adults,
              children: parsed.travelers.children || 0,
              children_ages: parsed.travelers.children_ages || [],
              rooms: parsed.travelers.rooms || 1,
            },
            modules: ["flight", "hotel", "activities", "transport"],
            preferences: {
              budget_twd: parsed.budget_twd,
              avoid_red_eye: parsed.avoid_red_eye,
              hotel_min_rating: parsed.hotel_min_rating,
              hotel_min_nightly_twd: parsed.hotel_min_nightly_twd,
              hotel_max_nightly_twd: parsed.hotel_max_nightly_twd,
              accepted_property_types: parsed.accepted_property_types || [],
              hotel_min_review_score: parsed.hotel_min_review_score,
              hotel_min_review_count: parsed.hotel_min_review_count,
              breakfast_required: parsed.breakfast_required,
              refundable_required: parsed.refundable_required,
              max_station_walk_minutes: parsed.max_station_walk_minutes,
              preferred_area: parsed.preferred_area,
              preferred_areas:
                parsed.preferred_areas ||
                (parsed.preferred_area ? [parsed.preferred_area] : []),
              optimization_mode: "balanced",
              interests: parsed.interests,
              extension_destination_ids: parsed.extension_destination_ids,
              pace: parsed.pace || "balanced",
            },
          }),
        },
      );
      setSearchId(accepted.search_id);
      setUsageState(accepted.usage);
      const stream = new EventSource(
        `/api/travel/searches/${accepted.search_id}/events`,
      );
      stream.addEventListener("module.results", (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        setProgress(data.progress);
        setOffers((current) => {
          const combined = [
            ...(current[data.module] || []),
            ...data.offers,
          ] as Offer[];
          const unique = new Map(combined.map((offer) => [offer.id, offer]));
          return { ...current, [data.module]: Array.from(unique.values()) };
        });
      });
      stream.addEventListener("flight.date_options", (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        setFlightDateOptions(data.options || []);
        setSelectedDateOption(undefined);
      });
      stream.addEventListener("provider.completed", (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        if (
          [
            "complete",
            "completed",
            "partial",
            "timeout",
            "rate_limited",
          ].includes(data.status)
        ) {
          setDone((current) =>
            current.includes(data.module) ? current : [...current, data.module],
          );
        }
      });
      stream.addEventListener("optimization.completed", (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        setProgress(92);
        setPlans(data.plans);
      });
      stream.addEventListener("search.completed", async (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        if (data.usage) setUsageState(data.usage);
        setProgress(100);
        setBusy(false);
        stream.close();
        trackAnalytics("search_completed");
        await loadFinal(accepted.search_id).catch(() => undefined);
      });
      stream.addEventListener("search.failed", async (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        if (data.usage) setUsageState(data.usage);
        setError("搜尋未能取得任何結果，請查看資料來源狀態後再試。");
        setBusy(false);
        stream.close();
        await loadFinal(accepted.search_id).catch(() => undefined);
      });
      stream.onerror = () => {
        const warning = "即時連線曾短暫中斷；完成後會從伺服器重新載入結果。";
        setWarnings((current) =>
          current.includes(warning) ? current : [...current, warning],
        );
      };
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 401) {
        setAuthState("signed_out");
        setBusy(false);
        return;
      }
      if (isUsageInsufficient(reason)) {
        router.push("/pricing");
        return;
      }
      setError((reason as Error).message);
      setBusy(false);
    }
  }

  async function save(plan: Plan) {
    if (!searchId) return;
    try {
      const trip = await api<{ id: string }>("/trips", {
        method: "POST",
        body: JSON.stringify({
          search_id: searchId,
          plan_id: plan.id,
          name: `${parsed?.destination || "目的地"}・${plan.title}旅程`,
        }),
      });
      trackAnalytics("trip_created");
      router.push(`/trips/${trip.id}`);
    } catch (reason) {
      setError((reason as Error).message);
    }
  }

  function applyCriteria(update: CriteriaUpdate) {
    const next = new URLSearchParams(params.toString());
    const setOptional = (key: string, value: string | number | undefined) => {
      if (value === undefined || value === "") next.delete(key);
      else next.set(key, String(value));
    };
    next.set("origin", update.origin);
    if (parsed?.destination) next.set("destination", parsed.destination);
    next.set("departure_date", update.departureDate);
    next.set("return_date", update.returnDate);
    next.set("flex_days", String(update.flexDays));
    next.set("adults", String(update.adults));
    next.set("children", String(update.children));
    next.set("rooms", String(update.rooms));
    next.set(
      "children_ages",
      Array.from(
        { length: update.children },
        (_, index) => parsed?.travelers.children_ages?.[index] ?? 8,
      ).join(","),
    );
    next.set("interests", update.interests.join(","));
    next.set("pace", update.pace);
    next.set("avoid_red_eye", String(update.avoidRedEye));
    next.set("breakfast_required", String(update.breakfastRequired));
    next.set("refundable_required", String(update.refundableRequired));
    next.set("include_airbnb", String(update.includeAirbnb));
    setOptional("budget_twd", update.budget);
    setOptional("hotel_max_nightly_twd", update.nightlyBudget);
    setOptional("hotel_min_nightly_twd", update.nightlyMinimum);
    setOptional("hotel_min_rating", update.hotelMinRating);
    setOptional("accepted_property_types", update.propertyTypes.join(","));
    setOptional("hotel_min_review_score", update.minReviewScore);
    setOptional("hotel_min_review_count", update.minReviewCount);
    setOptional("preferred_area", update.preferredArea);
    setSearchId(undefined);
    setOffers({});
    setPlans([]);
    setWarnings([]);
    setFlightDateOptions([]);
    setSelectedDateOption(undefined);
    setError(undefined);
    setDone([]);
    setProgress(0);
    setActiveTab("plans");
    setBreakfastOnly(update.breakfastRequired);
    setRefundableOnly(update.refundableRequired);
    setHotelNightlyMax(update.nightlyBudget || 0);
    setHotelSort("recommended");
    setDirectOnly(false);
    setRefundableFlightOnly(false);
    setActivityInterest("all");
    setSortByPrice(false);
    router.replace(`/search?${next.toString()}`);
  }

  function applyDateOption(option: FlightDateOption) {
    if (!option.return_date) return;
    const next = new URLSearchParams(params.toString());
    next.set("departure_date", option.departure_date);
    next.set("return_date", option.return_date);
    next.set("flex_days", "0");
    router.replace(`/search?${next.toString()}`);
    setSearchId(undefined);
    setOffers({});
    setPlans([]);
    setWarnings([]);
    setFlightDateOptions([]);
    setSelectedDateOption(undefined);
    setDone([]);
    setProgress(0);
    setActiveTab("plans");
    void begin([option.departure_date, option.return_date], 0);
  }

  const visibleOffers = useMemo(() => {
    let rows = [...(offers[activeTab] || [])];
    if (activeTab === "flight") {
      rows = rows
        .filter((offer) => !directOnly || Number(offer.stops || 0) === 0)
        .filter((offer) => !refundableFlightOnly || Boolean(offer.refundable));
    }
    if (activeTab === "hotel") {
      rows = rows
        .filter((offer) => !breakfastOnly || Boolean(offer.breakfast_included))
        .filter((offer) => !refundableOnly || Boolean(offer.refundable))
        .filter(
          (offer) =>
            !hotelMinRating || hotelStarRating(offer) >= hotelMinRating,
        )
        .filter(
          (offer) =>
            !hotelNightlyMax || hotelNightlyPrice(offer) <= hotelNightlyMax,
        )
        .filter(
          (offer) =>
            !hotelMaxWalk ||
            Number(offer.station_walk_minutes || 0) <= hotelMaxWalk,
        );
      if (hotelSort === "price")
        rows.sort(
          (left, right) => hotelNightlyPrice(left) - hotelNightlyPrice(right),
        );
      if (hotelSort === "rating")
        rows.sort((left, right) => hotelRating(right) - hotelRating(left));
      if (hotelSort === "distance")
        rows.sort(
          (left, right) =>
            Number(left.distance_to_center_km ?? Number.MAX_SAFE_INTEGER) -
            Number(right.distance_to_center_km ?? Number.MAX_SAFE_INTEGER),
        );
    }
    if (activeTab === "activities" && activityInterest !== "all") {
      rows = rows.filter((offer) => offer.category === activityInterest);
    }
    if (sortByPrice && activeTab !== "hotel")
      rows.sort((left, right) => amount(left) - amount(right));
    return rows;
  }, [
    activeTab,
    activityInterest,
    breakfastOnly,
    directOnly,
    hotelMaxWalk,
    hotelMinRating,
    hotelNightlyMax,
    hotelSort,
    offers,
    refundableFlightOnly,
    refundableOnly,
    sortByPrice,
  ]);

  const flightGroups = useMemo(() => {
    const grouped = new Map<string, Offer[]>();
    for (const offer of visibleOffers) {
      const key = String(offer.itinerary_key || offer.id);
      grouped.set(key, [...(grouped.get(key) || []), offer]);
    }
    return [...grouped.entries()]
      .map(
        ([key, values]) =>
          [
            key,
            values.sort((left, right) => amount(left) - amount(right)),
          ] as const,
      )
      .sort((left, right) => amount(left[1][0]) - amount(right[1][0]));
  }, [visibleOffers]);

  const destination = destinationByAirport(parsed?.destination);
  const includeAirbnb =
    parsed?.include_airbnb ?? params.get("include_airbnb") !== "false";
  const countryName =
    destination?.country === "JP"
      ? "日本"
      : destination?.country === "KR"
        ? "韓國"
        : destination?.country === "TH"
          ? "泰國"
          : "";
  const airbnbCriteria = parsed
    ? {
        location: [
          parsed.preferred_area,
          destination?.name || parsed.destination,
          countryName,
        ]
          .filter(Boolean)
          .join(", "),
        checkIn: dates[0],
        checkOut: dates[1],
        adults: parsed.travelers.adults,
        children: parsed.travelers.children || 0,
      }
    : null;
  const resultTabs = [
    { key: "plans", label: "推薦組合" },
    ...stages,
    { key: "connectivity", label: "eSIM" },
    ...(includeAirbnb ? [{ key: "airbnb", label: "Airbnb" }] : []),
  ];
  const searchReturnPath = `/search${params.toString() ? `?${params.toString()}` : ""}`;

  const providerTone =
    providerStatus?.status === "ready"
      ? providerStatus.mode === "live"
        ? "bg-emerald-50 text-emerald-800"
        : "bg-amber-50 text-amber-900"
      : "bg-red-50 text-red-800";

  return (
    <main className="mx-auto max-w-6xl px-5 pb-20 md:px-8">
      <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="mb-2 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]">
              <Sparkles size={16} />
              你的旅行需求
            </p>
            <h1 className="max-w-4xl text-2xl font-bold md:text-3xl">
              {destination
                ? `${destination.country === "JP" ? "日本" : destination.country === "KR" ? "韓國" : "泰國"}・${destination.name}完整旅程`
                : text || "完整旅程搜尋"}
            </h1>
            {destination && (
              <p className="mt-2 text-sm text-[var(--muted)]">
                {destination.summary} · 當地時區 {destination.timezone} ·
                建議停留 {destination.recommendedStay}
              </p>
            )}
          </div>
          {providerStatus && (
            <span
              className={`rounded-full px-3 py-2 text-xs font-semibold ${providerTone}`}
            >
              {providerStatus.message}
            </span>
          )}
        </div>
        {parsed && (
          <div className="mt-5 flex flex-wrap gap-2 text-sm">
            {[
              `${parsed.travelers.adults + (parsed.travelers.children || 0)} 位旅客`,
              `${parsed.travelers.rooms || 1} 間房`,
              `${dates[0]} → ${dates[1]}`,
              parsed.flex_days
                ? `日期前後可移動 ${parsed.flex_days} 日`
                : "指定日期",
              parsed.preferred_area ? `住在 ${parsed.preferred_area}` : null,
              parsed.budget_twd
                ? `預算 ${twd.format(parsed.budget_twd)}`
                : null,
              parsed.hotel_max_nightly_twd
                ? `每晚 ≤ ${twd.format(parsed.hotel_max_nightly_twd)}`
                : null,
              parsed.avoid_red_eye ? "避開紅眼" : null,
              parsed.breakfast_required ? "含早餐" : null,
              parsed.refundable_required ? "可退款" : null,
              ...parsed.interests.map(interestLabel),
            ]
              .filter(Boolean)
              .map((tag) => (
                <span
                  key={String(tag)}
                  className="rounded-full bg-[var(--teal-soft)] px-3 py-1.5 text-[var(--teal-dark)]"
                >
                  {tag}
                </span>
              ))}
          </div>
        )}
        {parsed && (
          <SearchCriteriaEditor
            criteria={{
              ...parsed,
              flex_days: parsed.flex_days || 0,
              include_airbnb: includeAirbnb,
            }}
            destination={destination}
            dates={dates}
            disabled={busy}
            onApply={applyCriteria}
          />
        )}
        {!parsed && !text && (
          <div className="mt-6 rounded-2xl bg-amber-50 p-5 text-amber-950">
            <p className="font-semibold">
              缺少出發地、目的地或出發日期，還不能建立搜尋。
            </p>
            <Link
              href="/"
              className="mt-3 inline-flex rounded-xl bg-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-white"
            >
              回首頁設定條件
            </Link>
          </div>
        )}
        {!searchId && parsed && (
          <>
            <div className="mt-6 flex flex-col gap-3 sm:flex-row">
              {authState === "signed_out" ? (
                <Link
                  href={loginPath(searchReturnPath)}
                  className="rounded-2xl bg-[var(--teal)] px-6 py-3.5 text-center font-semibold text-white"
                >
                  登入後開始搜尋
                </Link>
              ) : (
                <button
                  disabled={
                    busy ||
                    providerStatus?.status !== "ready" ||
                    authState !== "signed_in" ||
                    charge.status !== "ready"
                  }
                  onClick={() => begin()}
                  className="rounded-2xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {authState === "checking"
                    ? "確認登入狀態…"
                    : authState === "error"
                      ? "暫時無法確認登入狀態"
                      : `確認條件並開始搜尋 · ${charge.label}`}
                </button>
              )}
              {includeAirbnb && airbnbCriteria && (
                <AirbnbSearchPanel criteria={airbnbCriteria} compact />
              )}
            </div>
            {authState === "error" && (
              <p role="alert" className="mt-2 text-sm text-red-700">
                登入服務暫時無法確認，請稍後再試。
                <button
                  type="button"
                  onClick={checkAuth}
                  className="ml-1 font-semibold underline"
                >
                  重新確認
                </button>
              </p>
            )}
            <p className="mt-2 text-xs text-[var(--muted)]">
              {charge.status === "ready" ? `站內比較成功取得至少一筆可用結果才${charge.label}；Airbnb 官方外站搜尋不扣次。` : charge.unavailableHelp}
            </p>
          </>
        )}
        {error && (
          <div
            role="alert"
            className="mt-5 flex items-start gap-2 rounded-xl bg-red-50 p-4 text-sm text-red-800"
          >
            <AlertCircle size={18} className="mt-0.5 shrink-0" />
            <span>{error}</span>
          </div>
        )}
        {warnings.map((warning) => (
          <p
            key={warning}
            className="mt-3 rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-900"
          >
            {warning}
          </p>
        ))}
      </section>

      {searchId && (
        <section
          aria-label="搜尋進度"
          className="mb-7 rounded-3xl border border-[var(--line)] bg-white p-6"
        >
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <strong>
              {progress === 100 ? "分析完成" : "正在組合你的旅程"}
            </strong>
            <span className="font-mono text-sm text-[var(--muted)]">
              {progress}%
            </span>
          </div>
          <div className="h-2 overflow-hidden rounded-full bg-[#e4ebe6]">
            <div
              className="h-full rounded-full bg-[var(--teal)] transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
          {usageState && (
            <p
              className={`mt-3 text-sm font-semibold ${usageState.status === "charged" ? "text-[#9d4e3f]" : usageState.status === "released" ? "text-emerald-700" : "text-[var(--teal)]"}`}
            >
              {usageState.status === "charged"
                ? `已成功扣除 ${usageState.uses} 次`
                : usageState.status === "released"
                  ? "本次未扣次（保留次數已退回）"
                  : charge.uses === 0
                    ? "本次為免費操作，完成後仍會留下使用紀錄"
                    : `已暫時保留 ${charge.uses ?? usageState.uses} 次，完成後才會正式扣除`}
            </p>
          )}
          <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
            {stages.map(({ key, label, icon: Icon }) => (
              <div
                key={key}
                className={`flex items-center gap-2 rounded-xl p-2 text-sm ${done.includes(key) ? "text-[var(--teal)]" : "text-[var(--muted)]"}`}
              >
                {done.includes(key) ? (
                  <Check size={17} />
                ) : (
                  <LoaderCircle
                    size={17}
                    className={busy ? "animate-spin" : ""}
                  />
                )}
                <Icon size={17} />
                {label}
              </div>
            ))}
          </div>
        </section>
      )}

      {(plans.length > 0 ||
        Object.keys(offers).length > 0 ||
        flightDateOptions.length > 0) && (
        <section>
          <div
            className="mb-5 flex gap-2 overflow-x-auto pb-1"
            role="tablist"
            aria-label="搜尋結果分類"
          >
            {resultTabs.map((tab) => (
              <button
                key={tab.key}
                role="tab"
                aria-selected={activeTab === tab.key}
                onClick={() => setActiveTab(tab.key)}
                className={`whitespace-nowrap rounded-full border px-4 py-2 text-sm font-semibold ${activeTab === tab.key ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-white text-[var(--muted)]"}`}
              >
                {tab.label}
              </button>
            ))}
          </div>

          {activeTab === "plans" && plans.length > 0 && (
            <div className="grid gap-5 lg:grid-cols-3">
              {plans.map((plan, index) => (
                <article
                  key={plan.mode}
                  className={`relative rounded-[1.75rem] border bg-white p-6 ${index === 0 ? "border-[var(--teal)] shadow-[0_20px_60px_rgba(13,107,104,.14)]" : "border-[var(--line)]"}`}
                >
                  {index === 0 && (
                    <span className="absolute -top-3 left-6 rounded-full bg-[var(--teal)] px-3 py-1 text-xs font-semibold text-white">
                      BEST OVERALL
                    </span>
                  )}
                  <div className="flex items-start justify-between gap-4">
                    <div>
                      <p className="text-sm text-[var(--muted)]">
                        {plan.title}
                      </p>
                      <h2 className="mt-1 text-3xl font-bold">
                        {twd.format(Number(plan.total_cost.total_cost))}
                      </h2>
                      <p className="mt-1 text-xs text-[var(--muted)]">
                        整趟旅程預估總額
                      </p>
                    </div>
                    {tripsEnabled && <button
                      onClick={() => save(plan)}
                      aria-label={`儲存${plan.title}`}
                      className="rounded-xl border border-[var(--line)] p-2 text-[var(--teal)]"
                    >
                      <Save size={18} />
                    </button>}
                  </div>
                  <BudgetBreakdown
                    cost={plan.total_cost}
                    budget={parsed?.budget_twd}
                  />
                  <div className="my-5 space-y-3 border-y border-[var(--line)] py-5 text-sm">
                    {plan.flight && (
                      <div className="flex justify-between gap-3">
                        <span className="flex gap-2">
                          <Plane size={16} className="mt-0.5 shrink-0" />
                          <span>
                            {String(plan.flight.airline)}
                            <small className="mt-1 block text-[var(--muted)]">
                              {flightTimeSummary(plan.flight)}
                            </small>
                          </span>
                        </span>
                        <span>{twd.format(amount(plan.flight))}</span>
                      </div>
                    )}
                    {plan.hotel && (
                      <p className="flex justify-between gap-3">
                        <span className="flex items-center gap-2">
                          <Hotel size={16} />
                          {String(plan.hotel.hotel_name)}
                        </span>
                        <span>{twd.format(amount(plan.hotel))}</span>
                      </p>
                    )}
                    {plan.activity && (
                      <p className="flex justify-between gap-3">
                        <span className="flex items-center gap-2">
                          <MapPinned size={16} />
                          {String(plan.activity.title)}
                        </span>
                        <span>{twd.format(amount(plan.activity))}</span>
                      </p>
                    )}
                    {plan.transport && (
                      <p className="flex justify-between gap-3">
                        <span className="flex items-center gap-2">
                          <TrainFront size={16} />
                          {String(plan.transport.transport_type)}
                        </span>
                        <span>{twd.format(amount(plan.transport))}</span>
                      </p>
                    )}
                  </div>
                  {plan.itinerary?.length ? (
                    <p className="mb-4 flex items-center gap-2 rounded-xl bg-[var(--teal-soft)] p-3 text-sm text-[var(--teal-dark)]">
                      <BadgeCheck size={16} />
                      已安排 {plan.itinerary.length} 天可編輯行程
                    </p>
                  ) : null}
                  <ul className="space-y-2 text-sm">
                    {plan.pros.map((item) => (
                      <li key={item} className="flex gap-2">
                        <Check
                          size={16}
                          className="mt-0.5 shrink-0 text-[var(--teal)]"
                        />
                        {item}
                      </li>
                    ))}
                    {plan.cons.map((item) => (
                      <li key={item} className="flex gap-2 text-[var(--muted)]">
                        <Clock3 size={16} className="mt-0.5 shrink-0" />
                        {item}
                      </li>
                    ))}
                  </ul>
                  {tripsEnabled && <button
                    onClick={() => save(plan)}
                    className="mt-5 w-full rounded-xl bg-[var(--teal)] px-4 py-3 font-semibold text-white"
                  >
                    儲存並編輯行程
                  </button>}
                </article>
              ))}
            </div>
          )}

          {searchId && activeTab === "plans" && (
            <div className="mt-5">
              <AffiliatePartnerOptions
                searchId={searchId}
                modules={[
                  "flight",
                  "hotel",
                  "activities",
                  "transport",
                  "connectivity",
                ]}
                title="整趟旅程合作平台"
              />
            </div>
          )}

          {activeTab === "airbnb" && airbnbCriteria && (
            <AirbnbSearchPanel criteria={airbnbCriteria} />
          )}

          {activeTab === "flight" && (
            <>
              <FlightDateOptions
                options={flightDateOptions}
                selected={selectedDateOption}
                busy={busy}
                onSelect={setSelectedDateOption}
                onApply={applyDateOption}
              />
              {searchId && (
                <div className="mb-4 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-white p-4">
                  <div>
                    <strong>多來源售票比較</strong>
                    <p className="text-xs text-[var(--muted)]">
                      同一班次依艙等分組，保留各售票來源的稅費、行李與退改條件。
                    </p>
                  </div>
                  <button
                    type="button"
                    disabled={expandingSources}
                    onClick={expandFlightSources}
                    className="rounded-xl border border-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-[var(--teal)] disabled:opacity-50"
                  >
                    {expandingSources ? "比較中…" : "比較更多來源"}
                  </button>
                </div>
              )}
            </>
          )}

          {searchId && !["plans", "airbnb"].includes(activeTab) && (
            <AffiliatePartnerOptions
              searchId={searchId}
              modules={[activeTab as AffiliateModule]}
              title={
                activeTab === "connectivity" ? "旅途中保持連線" : "更多合作平台"
              }
            />
          )}

          {activeTab !== "plans" &&
            activeTab !== "airbnb" &&
            activeTab !== "connectivity" && (
              <div className="mb-4 flex flex-wrap items-center gap-4 rounded-2xl border border-[var(--line)] bg-white px-4 py-3 text-sm">
                <strong className="text-[var(--teal-dark)]">快速篩選</strong>
                {activeTab !== "hotel" && (
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={sortByPrice}
                      onChange={(event) => setSortByPrice(event.target.checked)}
                    />
                    價格由低到高
                  </label>
                )}
                {activeTab === "flight" && (
                  <>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={directOnly}
                        onChange={(event) =>
                          setDirectOnly(event.target.checked)
                        }
                      />
                      只看直飛
                    </label>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={refundableFlightOnly}
                        onChange={(event) =>
                          setRefundableFlightOnly(event.target.checked)
                        }
                      />
                      可退款
                    </label>
                  </>
                )}
                {activeTab === "hotel" && (
                  <>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={breakfastOnly}
                        onChange={(event) =>
                          setBreakfastOnly(event.target.checked)
                        }
                      />
                      含早餐
                    </label>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={refundableOnly}
                        onChange={(event) =>
                          setRefundableOnly(event.target.checked)
                        }
                      />
                      可退款
                    </label>
                    <label className="flex items-center gap-2">
                      最低星等
                      <select
                        aria-label="飯店最低星等"
                        className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                        value={hotelMinRating}
                        onChange={(event) =>
                          setHotelMinRating(Number(event.target.value))
                        }
                      >
                        <option value="0">不限</option>
                        <option value="3">3 星以上</option>
                        <option value="4">4 星以上</option>
                        <option value="5">5 星</option>
                      </select>
                    </label>
                    <label className="flex items-center gap-2">
                      每晚上限
                      <input
                        aria-label="飯店每晚上限"
                        className="w-24 rounded-lg border border-[var(--line)] px-2 py-1.5"
                        inputMode="numeric"
                        min="0"
                        type="number"
                        value={hotelNightlyMax || ""}
                        placeholder="不限"
                        onChange={(event) =>
                          setHotelNightlyMax(Number(event.target.value))
                        }
                      />
                    </label>
                    <label className="flex items-center gap-2">
                      車站步行
                      <select
                        aria-label="飯店車站步行上限"
                        className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                        value={hotelMaxWalk}
                        onChange={(event) =>
                          setHotelMaxWalk(Number(event.target.value))
                        }
                      >
                        <option value="0">不限</option>
                        <option value="5">5 分內</option>
                        <option value="10">10 分內</option>
                        <option value="15">15 分內</option>
                        <option value="20">20 分內</option>
                      </select>
                    </label>
                    <label className="flex items-center gap-2">
                      排序
                      <select
                        aria-label="飯店排序"
                        className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                        value={hotelSort}
                        onChange={(event) =>
                          setHotelSort(event.target.value as typeof hotelSort)
                        }
                      >
                        <option value="recommended">推薦順序</option>
                        <option value="price">每晚價格</option>
                        <option value="rating">旅客評分最高</option>
                        <option value="distance">距市中心最近</option>
                      </select>
                    </label>
                  </>
                )}
                {activeTab === "activities" && (
                  <label className="flex items-center gap-2">
                    興趣
                    <select
                      className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                      value={activityInterest}
                      onChange={(event) =>
                        setActivityInterest(event.target.value)
                      }
                    >
                      <option value="all">全部</option>
                      {destinationInterests.map((interest) => (
                        <option key={interest.code} value={interest.code}>
                          {interest.label}
                        </option>
                      ))}
                    </select>
                  </label>
                )}
              </div>
            )}

          {activeTab === "flight" && (
            <div className="space-y-6">
              {flightGroups.map(([key, group], groupIndex) => (
                <section
                  key={key}
                  className="rounded-[1.75rem] border border-[var(--line)] bg-[var(--paper)] p-3 md:p-4"
                >
                  <div className="mb-3 flex flex-wrap items-center justify-between gap-2 px-2">
                    <div>
                      <p className="text-xs font-bold uppercase tracking-wide text-[var(--teal)]">
                        行程組 {groupIndex + 1}
                      </p>
                      <h2 className="font-bold">
                        {String(group[0].origin || "—")} →{" "}
                        {String(group[0].destination || "—")} ·{" "}
                        {String(group[0].cabin_class || "economy")}
                      </h2>
                    </div>
                    <p className="text-sm text-[var(--muted)]">
                      {new Set(group.map((offer) => offer.provider)).size}{" "}
                      個售票來源 · 最低 {twd.format(amount(group[0]))}
                    </p>
                  </div>
                  <div className="space-y-3">
                    {group.map((offer) => (
                      <FlightOfferCard
                        key={offer.id}
                        offer={offer}
                        fallbackUrl={recheckUrl(
                          activeTab,
                          offer,
                          parsed,
                          dates,
                          locale,
                        )}
                        alertReturnPath={searchReturnPath}
                      />
                    ))}
                  </div>
                </section>
              ))}
            </div>
          )}

          {activeTab !== "plans" &&
            activeTab !== "airbnb" &&
            activeTab !== "connectivity" &&
            activeTab !== "flight" && (
              <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
                {visibleOffers.map((offer) => {
                  if (activeTab === "hotel")
                    return (
                      <HotelOfferCard
                        key={offer.id}
                        offer={offer}
                        actionUrl={recheckUrl(activeTab, offer, parsed, dates, locale)}
                        alertReturnPath={searchReturnPath}
                      />
                    );
                  const image = offer.images?.[0];
                  const mode =
                    offer.source_mode || (offer.is_mock ? "mock" : "estimate");
                  return (
                    <article
                      key={offer.id}
                      className="overflow-hidden rounded-[1.5rem] border border-[var(--line)] bg-white"
                    >
                      {image ? (
                        <Image
                          src={image}
                          alt={titleFor(activeTab, offer)}
                          width={720}
                          height={400}
                          unoptimized
                          className="h-44 w-full object-cover"
                        />
                      ) : (
                        <div className="grid h-28 place-items-center bg-gradient-to-br from-[var(--teal-soft)] to-[var(--coral-soft)] text-[var(--teal)]">
                          {activeTab === "hotel" ? (
                            <Hotel size={34} />
                          ) : activeTab === "flight" ? (
                            <Plane size={34} />
                          ) : activeTab === "activities" ? (
                            <MapPinned size={34} />
                          ) : (
                            <TrainFront size={34} />
                          )}
                        </div>
                      )}
                      <div className="p-5">
                        <div className="flex items-start justify-between gap-3">
                          <div>
                            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--teal)]">
                              {sourceLabels[mode]}
                            </p>
                            <h2 className="mt-1 text-xl font-bold">
                              {titleFor(activeTab, offer)}
                            </h2>
                          </div>
                          <strong>{twd.format(amount(offer))}</strong>
                        </div>
                        <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                          {detailsFor(activeTab, offer)}
                        </p>
                        <p className="mt-2 text-xs text-[var(--muted)]">
                          來源：{offer.provider || "未標示"}
                          {offer.retrieved_at
                            ? ` · ${new Date(offer.retrieved_at).toLocaleString(locale)}`
                            : ""}
                        </p>
                        {offer.attributions?.length ? (
                          <p className="mt-1 text-xs text-[var(--muted)]">
                            圖片：
                            {offer.attributions.map((label, index) =>
                              offer.attribution_urls?.[index] ? (
                                <span key={label}>
                                  {index > 0 ? "、" : ""}
                                  <a
                                    className="underline"
                                    href={offer.attribution_urls[index]}
                                    target="_blank"
                                    rel="noreferrer"
                                  >
                                    {label}
                                  </a>
                                </span>
                              ) : (
                                <span key={label}>
                                  {index > 0 ? "、" : ""}
                                  {label}
                                </span>
                              ),
                            )}
                          </p>
                        ) : null}
                        <a
                          href={recheckUrl(activeTab, offer, parsed, dates, locale)}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-4 flex items-center justify-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]"
                        >
                          {offer.action_kind === "deep_link"
                            ? "前往供應商"
                            : "外站重新確認"}
                          <ExternalLink size={16} />
                        </a>
                      </div>
                    </article>
                  );
                })}
              </div>
            )}
          {activeTab !== "plans" &&
            activeTab !== "airbnb" &&
            activeTab !== "connectivity" &&
            !visibleOffers.length && (
              <p className="rounded-2xl border border-dashed border-[var(--line)] bg-white p-10 text-center text-[var(--muted)]">
                這個分類目前沒有符合條件的結果。
              </p>
            )}
        </section>
      )}
    </main>
  );
}
