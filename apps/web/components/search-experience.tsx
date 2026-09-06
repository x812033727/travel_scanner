"use client";

import {
  AlertCircle,
  ArrowLeft,
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
import { useLocale, useTranslations } from "next-intl";
import { useSearchParams } from "next/navigation";
import { Link, useRouter } from "@/i18n/navigation";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { ApiError, api, isUsageInsufficient, twd } from "@/lib/api";
import { trackAnalytics } from "@/lib/analytics";
import { loginPath, safeExternalHref } from "@/lib/navigation";
import {
  destinationByAirport,
  interestLabel,
  localizeDestinations,
  interestCodes,
} from "@/lib/destinations";
import type { Trip, TripSearchCriteria } from "@/lib/trip-types";
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
import {
  FlightOfferCard,
  type FlightLegDirection,
  type FlightOfferTripActions,
} from "@/components/flight-offer-card";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import { UsageInsufficientNotice } from "@/components/usage-insufficient-notice";
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

// Only the modules the search page prices. A module the API grows later shows up in
// `providerAllUnavailable` rather than as an untranslated key.
const providerModuleKeys: Record<string, string> = {
  flight: "providerModuleFlight",
  hotel: "providerModuleHotel",
  activities: "providerModuleActivities",
  transport: "providerModuleTransport",
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

// Labels live in search.results.stages.* and are resolved at render.
const stages = [
  { key: "flight", icon: Plane },
  { key: "hotel", icon: Hotel },
  { key: "activities", icon: MapPinned },
  { key: "transport", icon: TrainFront },
];

/** The `search.results` message function, handed to the module-level formatters. */
type Translate = (key: string, values?: Record<string, string | number>) => string;

function amount(offer: Offer): number {
  return Number(offer.total_price ?? offer.price ?? 0);
}

function flightTimeSummary(offer: Offer, t: Translate) {
  const unknown = t("timeUnknown");
  const time = (value: unknown) =>
    typeof value === "string" ? value.match(/T(\d{2}:\d{2})/)?.[1] : undefined;
  const outbound = `${time(offer.departure_time) || unknown}–${time(offer.arrival_time) || unknown}`;
  const returning = offer.return_departure_time
    ? t("flightReturn", {
        times: `${time(offer.return_departure_time) || unknown}–${time(offer.return_arrival_time) || unknown}`,
      })
    : "";
  return t("flightOutbound", { outbound, returning });
}

function titleFor(module: string, offer: Offer, t: Translate): string {
  if (module === "flight")
    return String(offer.airline ?? offer.flight_number ?? t("fallbackFlight"));
  if (module === "hotel") return String(offer.hotel_name ?? t("fallbackHotel"));
  if (module === "activities") return String(offer.title ?? t("fallbackActivity"));
  return String(offer.transport_type ?? t("fallbackTransport"));
}

function detailsFor(module: string, offer: Offer, t: Translate, tc: Translate): string {
  if (module === "flight") {
    const stops = Number(offer.stops ?? 0);
    return `${offer.origin ?? ""} → ${offer.destination ?? ""} · ${stops ? t("stops", { count: stops }) : t("direct")}`;
  }
  if (module === "hotel") {
    const rating = Number(offer.review_score ?? offer.rating ?? 0);
    const property =
      offer.property_type === "vacation_rental"
        ? t("propertyRental")
        : offer.property_type === "serviced_apartment"
          ? t("propertyServiced")
          : t("propertyHotel");
    const reviews = offer.review_count
      ? t("reviews", { count: String(offer.review_count) })
      : t("reviewsUnknown");
    const extras = [
      property,
      reviews,
      offer.breakfast_included ? t("breakfast") : null,
      offer.refundable ? t("refundable") : null,
      offer.station_walk_minutes
        ? t("stationWalk", { minutes: String(offer.station_walk_minutes) })
        : null,
    ]
      .filter(Boolean)
      .join(" · ");
    return `${rating ? t("score", { score: rating.toFixed(1) }) : t("noScore")} · ${t("nights", { nights: String(offer.nights ?? "-") })} · ${offer.room_type ?? t("room")}${extras ? ` · ${extras}` : ""}`;
  }
  if (module === "activities")
    return `${interestLabel(String(offer.category || ""), tc)} · ${t("minutes", { minutes: String(offer.duration_minutes ?? "-") })} · ${offer.address ?? offer.city ?? ""}`;
  return `${t("minutes", { minutes: String(offer.duration_minutes ?? "-") })} · ${offer.origin ?? ""} → ${offer.destination ?? ""}`;
}

function recheckUrl(
  module: string,
  offer: Offer,
  parsed: Parsed | null,
  dates: string[],
  locale: string,
  t: Translate,
) {
  if (offer.action_kind === "deep_link" && offer.booking_url)
    return offer.booking_url;
  const query =
    module === "hotel"
      ? `${titleFor(module, offer, t)} ${parsed?.destination ?? ""} ${dates[0]} ${dates[1]}`
      : `${titleFor(module, offer, t)} ${parsed?.origin ?? ""} ${parsed?.destination ?? ""} ${dates[0]}`;
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
  const supported = new Set<string>(interestCodes);
  const codes = raw
    .split(",")
    .map((item) => item.trim())
    .filter((item) => supported.has(item));
  const labels = mapping
    .filter(([label]) => raw.includes(label))
    .map(([, code]) => code);
  return Array.from(new Set([...codes, ...labels]));
}

const TRIP_DATE_ISSUES = ["trip_dates_required", "trip_dates_past", "trip_dates_too_short"];

export function SearchExperience() {
  const params = useSearchParams();
  // `/search?trip_id=…`: a flight search for a saved trip. The trip supplies
  // the criteria and each result can be written back into its flight anchors.
  const tripId = params.get("trip_id") || undefined;
  const charge = useOperationCharge(tripId ? "travel_search" : "full_trip_search");
  const visibility = useSiteVisibility();
  const tripsEnabled = featureEnabled(visibility, "trips");
  const locale = useLocale();
  const usageText = useTranslations("usage");
  const t = useTranslations("search.results");
  const tc = useTranslations("search.catalog");
  const tripText = useTranslations("search.fromTrip");
  const workbenchText = useTranslations("search.workbench");
  const commonText = useTranslations("common");
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
  const [tripContext, setTripContext] = useState<TripSearchCriteria>();
  const [tripState, setTripState] = useState<
    "idle" | "loading" | "ready" | "signed_out" | "not_found" | "error"
  >(tripId ? "loading" : "idle");
  const [tripOriginChoice, setTripOriginChoice] = useState("TPE");
  const [savingOrigin, setSavingOrigin] = useState(false);
  const [tripDestinationChoice, setTripDestinationChoice] = useState("");
  const [attachState, setAttachState] = useState<{
    busy?: { direction: FlightLegDirection; offerId: string };
    done: Partial<Record<FlightLegDirection, string>>;
  }>({ done: {} });
  const tripParsed = useMemo<Parsed | null>(() => {
    if (!tripContext) return null;
    const { criteria } = tripContext;
    const preferences = criteria.preferences;
    const list = (value: unknown) => (Array.isArray(value) ? value.map(String) : []);
    const positive = (value: unknown) =>
      typeof value === "number" && value > 0 ? value : undefined;
    const pace = String(preferences.pace || "balanced");
    return {
      origin: criteria.origin || undefined,
      destination: tripDestinationChoice || criteria.destination || undefined,
      departure_date: criteria.departure_date || undefined,
      return_date: criteria.return_date || undefined,
      flex_days: 0,
      travelers: {
        adults: criteria.travelers.adults,
        children: criteria.travelers.children || 0,
        children_ages: criteria.travelers.children_ages || [],
        rooms: criteria.travelers.rooms || 1,
      },
      budget_twd: positive(preferences.budget_twd),
      interests: list(preferences.interests),
      extension_destination_ids: [],
      avoid_red_eye: Boolean(preferences.avoid_red_eye),
      hotel_min_rating: positive(preferences.hotel_min_rating),
      hotel_min_nightly_twd: positive(preferences.hotel_min_nightly_twd),
      hotel_max_nightly_twd: positive(preferences.hotel_max_nightly_twd),
      accepted_property_types: list(preferences.accepted_property_types),
      hotel_min_review_score: positive(preferences.hotel_min_review_score),
      hotel_min_review_count: positive(preferences.hotel_min_review_count),
      breakfast_required: Boolean(preferences.breakfast_required),
      refundable_required: Boolean(preferences.refundable_required),
      include_airbnb: false,
      max_station_walk_minutes: positive(preferences.max_station_walk_minutes),
      preferred_area:
        typeof preferences.preferred_area === "string" ? preferences.preferred_area : undefined,
      preferred_areas: list(preferences.preferred_areas),
      pace: (["relaxed", "balanced", "packed"].includes(pace) ? pace : "balanced") as Parsed["pace"],
      confidence: 1,
      missing_fields: [],
    };
  }, [tripContext, tripDestinationChoice]);
  const parsed = structuredParsed || tripParsed || parsedResult;
  // What the trip could not answer. An airport chosen here, or criteria edited
  // into the URL, settles the matching gap without a round trip to the server.
  const tripIssues = useMemo(() => {
    const codes = tripContext?.issues.map((issue) => issue.code) || [];
    return {
      origin: codes.includes("trip_origin_required") && !parsed?.origin,
      destination: codes.includes("trip_destination_unsupported"),
      destinationUnresolved:
        codes.includes("trip_destination_unsupported") && !parsed?.destination,
      dates: codes.some((code) => TRIP_DATE_ISSUES.includes(code)),
    };
  }, [tripContext, parsed]);
  const tripBlocked =
    Boolean(tripId) &&
    (!tripContext || tripIssues.origin || tripIssues.destinationUnresolved || tripIssues.dates);
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
  const [activeTab, setActiveTab] = useState(tripId ? "flight" : "plans");
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
  const resumed = useRef(false);
  const [insufficient, setInsufficient] = useState(false);
  // One key per plan so a retried save replays the trip instead of creating a twin
  // that also consumes a slot of the 20-trip cap.
  const saveKeys = useRef(new Map<string, string>());

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

  // Same shape as resolveAuth: state moves only once the request answers, so
  // the effect below stays a plain subscription to the trip id.
  const loadTripCriteria = useCallback(() => {
    if (!tripId) return Promise.resolve();
    return api<TripSearchCriteria>(`/trips/${tripId}/search-criteria?modules=flight`)
      .then((context) => {
        setTripContext(context);
        setTripState("ready");
      })
      .catch((reason) =>
        setTripState(
          reason instanceof ApiError && reason.status === 401
            ? "signed_out"
            : reason instanceof ApiError && reason.status === 404
              ? "not_found"
              : "error",
        ),
      );
  }, [tripId]);

  useEffect(() => {
    void loadTripCriteria();
  }, [loadTripCriteria]);

  useEffect(() => {
    api<ProviderStatus>("/providers/status")
      .then(setProviderStatus)
      .catch(() => setError(t("statusUnavailable")));
  }, [t]);

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

  // A visitor who signed in from this page comes back with `resume=search`. The
  // criteria survived the round trip already; this saves the second press of the
  // start button. Same gate as the button, fired once, then the marker is dropped
  // from the URL so a reload or a shared link never starts a paid search by itself.
  useEffect(() => {
    if (params.get("resume") !== "search" || resumed.current) return;
    if (!parsed || searchId || busy || tripBlocked) return;
    if (
      authState !== "signed_in" ||
      providerStatus?.status !== "ready" ||
      charge.status !== "ready"
    )
      return;
    resumed.current = true;
    const next = new URLSearchParams(params.toString());
    next.delete("resume");
    router.replace(`/search${next.toString() ? `?${next.toString()}` : ""}`);
    void begin();
    // `begin` reads the same state this effect depends on and is not memoised.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [params, parsed, searchId, busy, authState, providerStatus, charge.status, router, tripBlocked]);

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
        .map((item) => t("providerUnavailable", { provider: item.provider }));
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
    if (!parsed || providerStatus?.status !== "ready" || tripBlocked) return;
    setBusy(true);
    setError(undefined);
    setInsufficient(false);
    setProgress(2);
    try {
      const accepted = await api<{ search_id: string; usage: UsageStatus }>(
        "/searches",
        {
          method: "POST",
          headers: { "Idempotency-Key": crypto.randomUUID() },
          body: JSON.stringify({
            ...(tripId ? { trip_id: tripId } : {}),
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
            modules: tripId ? ["flight"] : ["flight", "hotel", "activities", "transport"],
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
        setError(t("searchFailed"));
        setBusy(false);
        stream.close();
        await loadFinal(accepted.search_id).catch(() => undefined);
      });
      stream.onerror = () => {
        // A CLOSED stream never fires search.completed, so without this the
        // spinner span forever after a tab switch or a dropped connection.
        // The browser reconnects CONNECTING streams on its own; only a closed
        // one needs us to go fetch whatever the server finished with.
        if (stream.readyState === EventSource.CLOSED) {
          setBusy(false);
          void loadFinal(accepted.search_id).catch(() => undefined);
          return;
        }
        const warning = t("streamInterrupted");
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
        // /pricing cannot sell anything yet; explain the balance here instead.
        setInsufficient(true);
        setProgress(0);
        setBusy(false);
        return;
      }
      setError((reason as Error).message);
      setBusy(false);
    }
  }

  async function save(plan: Plan) {
    if (!searchId) return;
    try {
      const saveKey = saveKeys.current.get(plan.id) ?? crypto.randomUUID();
      saveKeys.current.set(plan.id, saveKey);
      const trip = await api<{ id: string }>("/trips", {
        method: "POST",
        headers: { "Idempotency-Key": saveKey },
        body: JSON.stringify({
          search_id: searchId,
          plan_id: plan.id,
          name: t("tripName", {
            destination: parsed?.destination || t("destinationFallback"),
            title: plan.title,
          }),
        }),
      });
      trackAnalytics("trip_created");
      router.push(`/trips/${trip.id}`);
    } catch (reason) {
      setError((reason as Error).message);
    }
  }

  async function saveTripOrigin() {
    if (!tripContext) return;
    setSavingOrigin(true);
    setError(undefined);
    try {
      await api<Trip>(`/trips/${tripContext.trip.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          version: tripContext.trip.version,
          origin_airport: tripOriginChoice,
        }),
      });
      await loadTripCriteria();
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setSavingOrigin(false);
    }
  }

  async function attachOffer(direction: FlightLegDirection, offerId: string) {
    if (!tripId || !tripContext) return;
    setAttachState((state) => ({ ...state, busy: { direction, offerId } }));
    setError(undefined);
    const attempt = (version: number) =>
      api<Trip>(`/trips/${tripId}/flight-anchors/${direction}/from-offer`, {
        method: "POST",
        body: JSON.stringify({ version, offer_id: offerId }),
      });
    try {
      let updated: Trip;
      try {
        updated = await attempt(tripContext.trip.version);
      } catch (reason) {
        // Another tab moved the trip on; take its version once and try again.
        if (!(reason instanceof ApiError && reason.code === "trip_version_conflict")) throw reason;
        const fresh = await api<{ version: number }>(`/trips/${tripId}`);
        updated = await attempt(fresh.version);
      }
      setTripContext((context) =>
        context ? { ...context, trip: { ...context.trip, version: updated.version } } : context,
      );
      setAttachState((state) => ({ done: { ...state.done, [direction]: offerId } }));
    } catch (reason) {
      const message =
        reason instanceof ApiError && reason.code === "trip_version_conflict"
          ? tripText("attachConflict")
          : (reason as Error).message;
      setError(tripText("attachFailed", { message }));
      setAttachState((state) => ({ done: state.done }));
    }
  }

  function tripActionsFor(offer: Offer): FlightOfferTripActions | undefined {
    if (!tripId || !tripContext) return undefined;
    const state: FlightOfferTripActions["state"] = {};
    for (const direction of ["outbound", "return"] as const) {
      if (attachState.busy?.direction === direction && attachState.busy.offerId === offer.id) {
        state[direction] = "busy";
      } else if (attachState.done[direction] === offer.id) {
        state[direction] = "done";
      }
    }
    return {
      labels: {
        outbound: tripText("attachOutbound"),
        return: tripText("attachReturn"),
        busy: tripText("attaching"),
        doneOutbound: tripText("attachedOutbound"),
        doneReturn: tripText("attachedReturn"),
      },
      state,
      onAttach: (direction) => void attachOffer(direction, offer.id),
    };
  }

  function originLabel(code: string) {
    const key = `origin${code[0]}${code.slice(1).toLowerCase()}`;
    return ["TPE", "TSA", "KHH"].includes(code) ? workbenchText(key) : code;
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
    setActiveTab(tripId ? "flight" : "plans");
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
    setActiveTab(tripId ? "flight" : "plans");
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

  const destination = destinationByAirport(parsed?.destination, tc);
  const includeAirbnb =
    parsed?.include_airbnb ?? params.get("include_airbnb") !== "false";
  const countryName = destination ? t(`country.${destination.country}`) : "";
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
  const activeStages = tripId ? stages.filter((stage) => stage.key === "flight") : stages;
  const resultTabs = tripId
    ? activeStages.map(({ key }) => ({ key, label: t(`stages.${key}`) }))
    : [
        { key: "plans", label: t("tabPlans") },
        ...stages.map(({ key }) => ({ key, label: t(`stages.${key}`) })),
        { key: "connectivity", label: "eSIM" },
        ...(includeAirbnb ? [{ key: "airbnb", label: "Airbnb" }] : []),
      ];
  const attachedLegs = attachState.done.outbound && attachState.done.return
    ? tripText("legBoth")
    : attachState.done.outbound
      ? tripText("legOutbound")
      : attachState.done.return
        ? tripText("legReturn")
        : null;
  const searchReturnPath = `/search${params.toString() ? `?${params.toString()}` : ""}`;
  const resumeReturnPath = (() => {
    const next = new URLSearchParams(params.toString());
    next.set("resume", "search");
    return `/search?${next.toString()}`;
  })();

  const providerTone =
    providerStatus?.status === "ready"
      ? providerStatus.mode === "live"
        ? "bg-emerald-50 text-emerald-800"
        : "bg-amber-50 text-amber-900"
      : "bg-red-50 text-red-800";

  // The badge used to print the API's own `message`, which is Traditional Chinese prose
  // composed on the server — 「目前沒有可用的航班查價供應商。；目前沒有可用的飯店查價供應商。」
  // greeted every English, Japanese and Korean reader on /search. Everything that
  // sentence says is already in the structured fields next to it.
  const providerBadges = (() => {
    if (!providerStatus) return [];
    if (providerStatus.status === "ready") {
      const key = providerStatus.mode === "live" ? "providerReadyLive" : "providerReadyTest";
      return [t(key, { provider: providerStatus.provider })];
    }
    const paused = Object.entries(providerStatus.module_statuses || {})
      .filter(([name, module]) => !module.available && name in providerModuleKeys)
      .map(([name]) =>
        t("providerModuleUnavailable", { module: t(providerModuleKeys[name]) }),
      );
    return paused.length ? paused : [t("providerAllUnavailable")];
  })();

  return (
    <main className="mx-auto max-w-6xl px-5 pb-20 md:px-8">
      <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="mb-2 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]">
              <Sparkles size={16} />
              {t("yourRequest")}
            </p>
            <h1 className="max-w-4xl text-2xl font-bold md:text-3xl">
              {tripContext
                ? tripText("title", { name: tripContext.trip.name })
                : destination
                  ? t("fullTripTitle", {
                      country: t(`country.${destination.country}`),
                      city: destination.name,
                    })
                  : text || t("fullTripSearch")}
            </h1>
            {tripContext ? (
              <p className="mt-2 text-sm text-[var(--muted)]">
                {tripText("summary", {
                  destination: tripContext.trip.destination_name || "",
                  from: tripContext.trip.start_date || "",
                  to: tripContext.trip.end_date || "",
                })}
              </p>
            ) : destination && (
              <p className="mt-2 text-sm text-[var(--muted)]">
                {t("destinationMeta", {
                  summary: destination.summary,
                  timezone: destination.timezone,
                  stay: tc("recommendedStay", {
                    min: destination.recommendedDays.min,
                    max: destination.recommendedDays.max,
                  }),
                })}
              </p>
            )}
            {tripId && (
              <Link
                href={`/trips/${tripId}`}
                className="mt-3 inline-flex items-center gap-1.5 text-sm font-semibold text-[var(--teal)]"
              >
                <ArrowLeft size={15} />
                {tripText("backToTrip")}
              </Link>
            )}
          </div>
          {providerBadges.length > 0 && (
            <div className="flex flex-wrap gap-2">
              {providerBadges.map((badge) => (
                <span
                  key={badge}
                  className={`rounded-full px-3 py-2 text-xs font-semibold ${providerTone}`}
                >
                  {badge}
                </span>
              ))}
            </div>
          )}
        </div>
        {parsed && (
          <div className="mt-5 flex flex-wrap gap-2 text-sm">
            {[
              t("travelers", { count: parsed.travelers.adults + (parsed.travelers.children || 0) }),
              t("rooms", { count: parsed.travelers.rooms || 1 }),
              `${dates[0]} → ${dates[1]}`,
              parsed.flex_days
                ? t("flexDays", { days: parsed.flex_days })
                : t("fixedDates"),
              parsed.preferred_area ? t("stayIn", { area: parsed.preferred_area }) : null,
              parsed.budget_twd
                ? t("budget", { amount: twd.format(parsed.budget_twd) })
                : null,
              parsed.hotel_max_nightly_twd
                ? t("nightlyMax", { amount: twd.format(parsed.hotel_max_nightly_twd) })
                : null,
              parsed.avoid_red_eye ? t("avoidRedEye") : null,
              parsed.breakfast_required ? t("breakfast") : null,
              parsed.refundable_required ? t("refundable") : null,
              ...parsed.interests.map((code) => interestLabel(code, tc)),
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
        {tripId && tripState === "loading" && (
          <p role="status" className="mt-6 text-sm text-[var(--muted)]">
            {tripText("loading")}
          </p>
        )}
        {tripId && tripState === "signed_out" && (
          <div className="mt-6 rounded-2xl bg-amber-50 p-5 text-amber-950">
            <Link
              href={loginPath(searchReturnPath)}
              className="inline-flex rounded-xl bg-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-white"
            >
              {tripText("signIn")}
            </Link>
          </div>
        )}
        {tripId && tripState === "not_found" && (
          <div role="alert" className="mt-6 rounded-2xl bg-red-50 p-5 text-sm text-red-900">
            {tripText("notFound")}
          </div>
        )}
        {tripId && tripState === "error" && (
          <div role="alert" className="mt-6 rounded-2xl bg-red-50 p-5 text-sm text-red-900">
            {tripText("unavailable")}
            <button
              type="button"
              onClick={() => {
                setTripState("loading");
                void loadTripCriteria();
              }}
              className="ml-2 font-semibold underline"
            >
              {commonText("retry")}
            </button>
          </div>
        )}
        {tripContext && tripIssues.origin && (
          <section className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-5 text-amber-950">
            <p className="font-semibold">{tripText("originTitle")}</p>
            <p className="mt-1 text-sm leading-6">{tripText("originBody")}</p>
            <div role="radiogroup" aria-label={tripText("originTitle")} className="mt-3 flex flex-wrap gap-2">
              {tripContext.origin_options.map((code) => (
                <button
                  key={code}
                  type="button"
                  role="radio"
                  aria-checked={tripOriginChoice === code}
                  onClick={() => setTripOriginChoice(code)}
                  className={`rounded-full border px-4 py-2 text-sm font-semibold ${tripOriginChoice === code ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-white text-[var(--ink)]"}`}
                >
                  {originLabel(code)}
                </button>
              ))}
            </div>
            <button
              type="button"
              onClick={() => void saveTripOrigin()}
              disabled={savingOrigin}
              className="mt-4 rounded-xl bg-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-white disabled:opacity-50"
            >
              {savingOrigin ? tripText("originSaving") : tripText("originSave")}
            </button>
          </section>
        )}
        {tripContext && tripIssues.destination && (
          <section className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-5 text-amber-950">
            <p className="font-semibold">{tripText("destinationTitle")}</p>
            <p className="mt-1 text-sm leading-6">{tripText("destinationBody")}</p>
            <label className="mt-3 block text-sm font-semibold">
              {tripText("destinationSelect")}
              <select
                value={tripDestinationChoice}
                onChange={(event) => setTripDestinationChoice(event.target.value)}
                className="mt-1.5 block w-full max-w-sm rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 font-normal text-[var(--ink)]"
              >
                <option value="">{tripText("destinationPlaceholder")}</option>
                {localizeDestinations(tc).map((city) => (
                  <option key={city.id} value={city.airport}>
                    {city.name} · {city.airport}
                  </option>
                ))}
              </select>
            </label>
          </section>
        )}
        {tripContext && tripIssues.dates && (
          <section className="mt-6 rounded-2xl border border-amber-200 bg-amber-50 p-5 text-amber-950">
            <p className="font-semibold">{tripText("datesTitle")}</p>
            <p className="mt-1 text-sm leading-6">{tripText("datesBody")}</p>
            <Link
              href={`/trips/${tripId}`}
              className="mt-3 inline-flex rounded-xl bg-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-white"
            >
              {tripText("fixDates")}
            </Link>
          </section>
        )}
        {/* Also shown when parsing failed: the reader used to be left with one
            red sentence and no way anywhere. */}
        {!tripId && !parsed && (!text || error) && (
          <div className="mt-6 rounded-2xl bg-amber-50 p-5 text-amber-950">
            <p className="font-semibold">
              {t("missingCriteria")}
            </p>
            <Link
              href="/"
              className="mt-3 inline-flex rounded-xl bg-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-white"
            >
              {t("backHome")}
            </Link>
          </div>
        )}
        {!searchId && parsed && (
          <>
            <div className="mt-6 flex flex-col gap-3 sm:flex-row">
              {authState === "signed_out" ? (
                <Link
                  href={loginPath(resumeReturnPath)}
                  className="rounded-2xl bg-[var(--teal)] px-6 py-3.5 text-center font-semibold text-white"
                >
                  {t("signInToSearch")}
                </Link>
              ) : (
                <button
                  disabled={
                    busy ||
                    providerStatus?.status !== "ready" ||
                    authState !== "signed_in" ||
                    charge.status !== "ready" ||
                    tripBlocked
                  }
                  onClick={() => begin()}
                  className="rounded-2xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
                >
                  {authState === "checking"
                    ? t("authChecking")
                    : authState === "error"
                      ? t("authError")
                      : t("startSearch", { charge: charge.label })}
                </button>
              )}
              {includeAirbnb && airbnbCriteria && (
                <AirbnbSearchPanel criteria={airbnbCriteria} compact />
              )}
            </div>
            {insufficient && (
              <div className="mt-4">
                <UsageInsufficientNotice chargeLabel={charge.label} />
              </div>
            )}
            {authState === "error" && (
              <p role="alert" className="mt-2 text-sm text-red-700">
                {t("authErrorHelp")}
                <button
                  type="button"
                  onClick={checkAuth}
                  className="ml-1 font-semibold underline"
                >
                  {t("recheck")}
                </button>
              </p>
            )}
            <p className="mt-2 text-xs text-[var(--muted)]">
              {charge.status === "ready" ? t("chargeHelp", { charge: charge.label }) : charge.unavailableHelp}
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
          aria-label={t("progressLabel")}
          className="mb-7 rounded-3xl border border-[var(--line)] bg-white p-6"
        >
          <div className="mb-4 flex flex-wrap items-center justify-between gap-2">
            <strong>
              {progress === 100 ? t("analysisDone") : t("assembling")}
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
                ? t("charged", { uses: usageState.uses })
                : usageState.status === "released"
                  ? t("released")
                  : charge.uses === 0
                    ? t("freeOperation")
                    : t("reserved", { uses: charge.uses ?? usageState.uses })}
            </p>
          )}
          <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">
            {activeStages.map(({ key, icon: Icon }) => (
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
                {t(`stages.${key}`)}
              </div>
            ))}
          </div>
        </section>
      )}

      {(plans.length > 0 ||
        Object.keys(offers).length > 0 ||
        flightDateOptions.length > 0) && (
        <section>
          {tripId && attachedLegs && (
            <p
              role="status"
              className="mb-4 flex flex-wrap items-center gap-2 rounded-2xl bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-800"
            >
              <Check size={16} />
              {tripText("attachedNotice", { legs: attachedLegs })}
              <Link href={`/trips/${tripId}`} className="underline">
                {tripText("backToTrip")}
              </Link>
            </p>
          )}
          <div
            className="mb-5 flex gap-2 overflow-x-auto pb-1"
            role="tablist"
            aria-label={t("tabsLabel")}
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
                        {t("estimatedTotal")}
                      </p>
                    </div>
                    {tripsEnabled && <button
                      onClick={() => save(plan)}
                      aria-label={t("savePlan", { title: plan.title })}
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
                              {flightTimeSummary(plan.flight, t)}
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
                      {t("editableDays", { count: plan.itinerary.length })}
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
                    {t("saveAndEdit")}
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
                title={t("partnersTrip")}
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
                    <strong>{t("multiSourceTitle")}</strong>
                    <p className="text-xs text-[var(--muted)]">
                      {t("multiSourceHelp")}
                    </p>
                  </div>
                  <button
                    type="button"
                    disabled={expandingSources}
                    onClick={expandFlightSources}
                    className="rounded-xl border border-[var(--teal)] px-4 py-2.5 text-sm font-semibold text-[var(--teal)] disabled:opacity-50"
                  >
                    {expandingSources ? t("comparing") : t("compareMore", { noCharge: usageText("noCharge") })}
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
                activeTab === "connectivity" ? t("partnersConnectivity") : t("partnersMore")
              }
            />
          )}

          {activeTab !== "plans" &&
            activeTab !== "airbnb" &&
            activeTab !== "connectivity" && (
              <div className="mb-4 flex flex-wrap items-center gap-4 rounded-2xl border border-[var(--line)] bg-white px-4 py-3 text-sm">
                <strong className="text-[var(--teal-dark)]">{t("quickFilters")}</strong>
                {activeTab !== "hotel" && (
                  <label className="flex items-center gap-2">
                    <input
                      type="checkbox"
                      checked={sortByPrice}
                      onChange={(event) => setSortByPrice(event.target.checked)}
                    />
                    {t("sortPriceAsc")}
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
                      {t("directOnly")}
                    </label>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={refundableFlightOnly}
                        onChange={(event) =>
                          setRefundableFlightOnly(event.target.checked)
                        }
                      />
                      {t("refundable")}
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
                      {t("breakfast")}
                    </label>
                    <label className="flex items-center gap-2">
                      <input
                        type="checkbox"
                        checked={refundableOnly}
                        onChange={(event) =>
                          setRefundableOnly(event.target.checked)
                        }
                      />
                      {t("refundable")}
                    </label>
                    <label className="flex items-center gap-2">
                      {t("minStars")}
                      <select
                        aria-label={t("minStarsLabel")}
                        className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                        value={hotelMinRating}
                        onChange={(event) =>
                          setHotelMinRating(Number(event.target.value))
                        }
                      >
                        <option value="0">{t("anyOption")}</option>
                        <option value="3">{t("starsUp", { stars: 3 })}</option>
                        <option value="4">{t("starsUp", { stars: 4 })}</option>
                        <option value="5">{t("starsExact", { stars: 5 })}</option>
                      </select>
                    </label>
                    <label className="flex items-center gap-2">
                      {t("nightlyCap")}
                      <input
                        aria-label={t("nightlyCapLabel")}
                        className="w-24 rounded-lg border border-[var(--line)] px-2 py-1.5"
                        inputMode="numeric"
                        min="0"
                        type="number"
                        value={hotelNightlyMax || ""}
                        placeholder={t("anyOption")}
                        onChange={(event) =>
                          setHotelNightlyMax(Number(event.target.value))
                        }
                      />
                    </label>
                    <label className="flex items-center gap-2">
                      {t("stationWalkFilter")}
                      <select
                        aria-label={t("stationWalkLabel")}
                        className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                        value={hotelMaxWalk}
                        onChange={(event) =>
                          setHotelMaxWalk(Number(event.target.value))
                        }
                      >
                        <option value="0">{t("anyOption")}</option>
                        <option value="5">{t("withinMinutes", { minutes: 5 })}</option>
                        <option value="10">{t("withinMinutes", { minutes: 10 })}</option>
                        <option value="15">{t("withinMinutes", { minutes: 15 })}</option>
                        <option value="20">{t("withinMinutes", { minutes: 20 })}</option>
                      </select>
                    </label>
                    <label className="flex items-center gap-2">
                      {t("sort")}
                      <select
                        aria-label={t("sortLabel")}
                        className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                        value={hotelSort}
                        onChange={(event) =>
                          setHotelSort(event.target.value as typeof hotelSort)
                        }
                      >
                        <option value="recommended">{t("sortRecommended")}</option>
                        <option value="price">{t("sortPrice")}</option>
                        <option value="rating">{t("sortRating")}</option>
                        <option value="distance">{t("sortDistance")}</option>
                      </select>
                    </label>
                  </>
                )}
                {activeTab === "activities" && (
                  <label className="flex items-center gap-2">
                    {t("interest")}
                    <select
                      className="rounded-lg border border-[var(--line)] px-2 py-1.5"
                      value={activityInterest}
                      onChange={(event) =>
                        setActivityInterest(event.target.value)
                      }
                    >
                      <option value="all">{t("allOption")}</option>
                      {interestCodes.map((code) => (
                        <option key={code} value={code}>
                          {interestLabel(code, tc)}
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
                        {t("flightGroup", { index: groupIndex + 1 })}
                      </p>
                      <h2 className="font-bold">
                        {String(group[0].origin || "—")} →{" "}
                        {String(group[0].destination || "—")} ·{" "}
                        {String(group[0].cabin_class || "economy")}
                      </h2>
                    </div>
                    <p className="text-sm text-[var(--muted)]">
                      {t("sellersFrom", {
                        count: new Set(group.map((offer) => offer.provider)).size,
                        amount: twd.format(amount(group[0])),
                      })}
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
                          t,
                        )}
                        alertReturnPath={searchReturnPath}
                        tripActions={tripActionsFor(offer)}
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
                        actionUrl={recheckUrl(activeTab, offer, parsed, dates, locale, t)}
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
                          alt={titleFor(activeTab, offer, t)}
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
                              {t(`source.${mode}`)}
                            </p>
                            <h2 className="mt-1 text-xl font-bold">
                              {titleFor(activeTab, offer, t)}
                            </h2>
                          </div>
                          <strong>{twd.format(amount(offer))}</strong>
                        </div>
                        <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
                          {detailsFor(activeTab, offer, t, tc)}
                        </p>
                        <p className="mt-2 text-xs text-[var(--muted)]">
                          {t("sourceLine", { provider: offer.provider || t("unlabelled") })}
                          {offer.retrieved_at
                            ? ` · ${new Date(offer.retrieved_at).toLocaleString(locale)}`
                            : ""}
                        </p>
                        {offer.attributions?.length ? (
                          <p className="mt-1 text-xs text-[var(--muted)]">
                            {t("imageCredit")}
                            {offer.attributions.map((label, index) =>
                              offer.attribution_urls?.[index] ? (
                                <span key={label}>
                                  {index > 0 ? "、" : ""}
                                  <a
                                    className="underline"
                                    href={safeExternalHref(offer.attribution_urls[index])}
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
                          href={safeExternalHref(recheckUrl(activeTab, offer, parsed, dates, locale, t))}
                          target="_blank"
                          rel="noreferrer"
                          className="mt-4 flex items-center justify-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]"
                        >
                          {offer.action_kind === "deep_link"
                            ? t("goToProvider")
                            : t("recheckExternal")}
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
                {t("emptyCategory")}
              </p>
            )}
        </section>
      )}
    </main>
  );
}
