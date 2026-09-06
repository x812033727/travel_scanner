"use client";

import {
  ArrowLeft,
  ArrowDown,
  ArrowUp,
  CalendarDays,
  CalendarPlus,
  CarFront,
  Check,
  CircleAlert,
  Clock3,
  Copy,
  Edit3,
  Footprints,
  GripVertical,
  Link2,
  Loader2,
  LockKeyhole,
  MapPin,
  NotebookPen,
  Plus,
  RefreshCw,
  Route as RouteIcon,
  Save,
  Settings2,
  Sparkles,
  Trash2,
  TrainFront,
  TriangleAlert,
  Undo2,
  Unlock,
  WifiOff,
  X,
} from "lucide-react";
import { useRouter } from "@/i18n/navigation";
import { useLocale, useTranslations } from "next-intl";
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from "react";
import { FlightAnchorCard, flightAnchorInfo } from "@/components/flight-anchor-card";
import { PlacePicker } from "@/components/place-picker";
import { TripCostPanel } from "@/components/trip-cost-panel";
import { TripNoteField } from "@/components/trip-note-field";
import { PlannerOverlay } from "@/components/planner-overlay";
import { PriceAlertButton } from "@/components/price-alert-button";
import { RouteModePanel } from "@/components/route-mode-panel";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { RouteTimelineLink } from "@/components/route-timeline-link";
import { StayAreaFlow, type StayArea, type StayHotel, type StaySelectResult } from "@/components/stay-area-flow";
import { SystemItineraryCard } from "@/components/system-itinerary-card";
import { ItineraryDiff } from "@/components/itinerary-diff";
import { TripMetaEditor } from "@/components/trip-meta-editor";
import { TripWeatherPanel } from "@/components/trip-weather-panel";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import { api, ApiError, isUsageInsufficient, twd } from "@/lib/api";
import { formatMoney } from "@/lib/locale-format";
import { formatTime, groupTripItems, isActiveRouteItem, isFlightAnchor, isLogisticsItem, missingSegmentCount, originalItemName, projectChainedStarts, segmentsForRows, type RouteSegment, type ScheduleDefaults, type TravelMode, type Trip, type TripItem, type TripRouting } from "@/lib/trip-types";

// Labels live in trips.editor.duration.m<minutes> and are resolved at render.
const activityDurationOptions = [20, 30, 45, 60, 90, 120, 150, 180, 240, 360, 540] as const;

/** The `trips.editor` message function, handed to the module-level formatters. */
type Te = (key: string, values?: Record<string, string | number>) => string;

function normalize(items: TripItem[]) {
  const positions = new Map<string, number>();
  return [...items]
    .sort((a, b) => a.day_date.localeCompare(b.day_date) || a.position - b.position)
    .map((item) => {
      const position = positions.get(item.day_date) || 0;
      positions.set(item.day_date, position + 1);
      return { ...item, position };
    });
}
function daysBetween(start?: string | null, end?: string | null) {
  if (!start || !end) return [];
  const days: string[] = [];
  const cursor = new Date(`${start}T00:00:00Z`);
  const last = new Date(`${end}T00:00:00Z`);
  while (cursor <= last && days.length < 62) {
    days.push(cursor.toISOString().slice(0, 10));
    cursor.setUTCDate(cursor.getUTCDate() + 1);
  }
  return days;
}

function timeValue(value?: string | null, timeZone?: string) {
  if (!value) return "";
  const localWallClock = value.match(
    /^\d{4}-\d{2}-\d{2}T(\d{2}:\d{2})(?::\d{2}(?:\.\d+)?)?$/,
  );
  if (localWallClock) return localWallClock[1];
  return new Intl.DateTimeFormat("en-GB", {
    hour: "2-digit",
    minute: "2-digit",
    hourCycle: "h23",
    timeZone,
  }).format(new Date(value));
}

function withTime(day: string, value: string) {
  return value ? `${day}T${value}:00` : null;
}

function countryCodesForTrip(trip?: Trip): string[] {
  if (!trip) return ["jp", "kr", "th"];
  if (trip.timezone === "Asia/Tokyo") return ["jp"];
  if (trip.timezone === "Asia/Seoul") return ["kr"];
  if (trip.timezone === "Asia/Bangkok") return ["th"];
  const destination = trip.destination_name || "";
  if (/日本|東京|大阪|京都|北海道|沖繩|福岡|名古屋/.test(destination)) return ["jp"];
  if (/韓國|首爾|釜山|濟州/.test(destination)) return ["kr"];
  if (/泰國|曼谷|清邁|普吉|喀比/.test(destination)) return ["th"];
  return ["jp", "kr", "th"];
}

function dayLabel(day: string, index: number, locale: string) {
  const date = new Date(`${day}T00:00:00Z`);
  return {
    eyebrow: `DAY ${index + 1}`,
    short: `${date.getUTCMonth() + 1}/${date.getUTCDate()}`,
    weekday: new Intl.DateTimeFormat(locale, { weekday: "short", timeZone: "UTC" }).format(date),
  };
}

function todayForTimezone(timezone?: string | null) {
  return new Intl.DateTimeFormat("en-CA", { timeZone: timezone || "UTC" }).format(new Date());
}

function mobileDayHeading(day: string, locale: string, te: Te) {
  if (!day) return te("noDate");
  return new Intl.DateTimeFormat(locale, {
    month: "long",
    day: "numeric",
    weekday: "short",
    timeZone: "UTC",
  }).format(new Date(`${day}T00:00:00Z`));
}

function durationSummary(minutes: number, te: Te) {
  if (minutes < 60) return te("durationMinutes", { minutes });
  const hours = Math.floor(minutes / 60);
  const remainder = minutes % 60;
  return remainder
    ? te("durationHoursMinutes", { hours, minutes: remainder })
    : te("durationHours", { hours });
}

function aiProviderLabel(provider: "openai" | "anthropic" | "minimax" | "catalog" | undefined, te: Te) {
  if (provider === "minimax") return "MiniMax";
  if (provider === "openai") return "OpenAI";
  if (provider === "anthropic") return "Anthropic";
  return te("providerFallback");
}

type RouteDayComputeResponse = {
  version: number;
  status: string;
  total: number;
  completed: number;
  job_id?: string;
  unresolved_items?: Array<{ item_id: string; title: string; reason: string }>;
};
type PublicRuntimeConfig = {
  google_routes_enabled?: boolean;
  google_places_enabled?: boolean;
  google_maps_embed_enabled?: boolean;
  navitime_enabled?: boolean;
  ekispert_enabled?: boolean;
  odsay_enabled?: boolean;
  naver_places_enabled?: boolean;
  naver_directions_enabled?: boolean;
  naver_dynamic_map_enabled?: boolean;
};
type Place = { place_id: string; provider: string; name: string; address?: string | null; latitude?: number | null; longitude?: number | null; opening_hours?: string[]; google_maps_url?: string | null; naver_maps_url?: string | null; external_url?: string | null; attribution?: string };
type LodgingDraft = { name: string; location_name: string; provider_place_id: string; latitude?: number; longitude?: number; location_source: string };
type FlightDraft = {
  airline: string;
  flight_number: string;
  origin: string;
  destination: string;
  departure_local: string;
  arrival_local: string;
  departure_timezone: string;
  arrival_timezone: string;
};
type SaveState = "saved" | "dirty" | "saving" | "offline" | "conflict";
type StoredTripDraft = {
  baseVersion: number;
  savedAt: string;
  items: TripItem[];
  routePreference: Trip["route_preference"];
};
type PreviewItem = { id: string; title: string; position: number; start_time?: string | null; locked: boolean; fixed_time: boolean };
type OptimizationPreview = {
  preview_id: string;
  expires_at: string;
  base_version: number;
  route_preference: string;
  changed: boolean;
  warnings: string[];
  segments: RouteSegment[];
  total_duration_before_minutes: number;
  total_duration_after_minutes: number;
  charge_on_apply: number;
  days: Array<{
    date: string;
    before: PreviewItem[];
    after: PreviewItem[];
    duration_before_minutes: number;
    duration_after_minutes: number;
    saved_minutes: number;
  }>;
};
type ConfirmAction = "reprice" | "revoke-share" | "rotate-share" | "overwrite-conflict";
type AIPlanningScope = "day" | "trip";
type AIItineraryPreview = {
  preview_id: string;
  base_version: number;
  expires_at: string;
  scope: AIPlanningScope;
  day_date?: string | null;
  planning: NonNullable<Trip["planning"]>;
  days: Array<{ date: string; label: string; items: TripItem[] }>;
  unscheduled_slots: Array<{ date: string; slot: "activity" | "lunch" | "dinner" }>;
  readiness: {
    status: "ready" | "partial" | "needs_setup" | "fallback";
    has_lodging: boolean;
    exact_item_count: number;
    hotspot_candidate_count: number;
    merchant_candidate_count: number;
    preserved_item_count: number;
    assumptions: string[];
  };
  routing_summary: {
    exact_items: number;
    eligible_pairs: number;
    hotel_pairs_deferred: number;
  };
};
type PlannerTheme = "forest" | "ocean" | "sunset" | "lavender";

// Names and descriptions live in trips.editor.theme.<id>.* and are resolved at render.
const plannerThemes: Array<{ id: PlannerTheme; colors: [string, string, string] }> = [
  { id: "forest", colors: ["#0d6b68", "#f5f7f2", "#ed735d"] },
  { id: "ocean", colors: ["#27658a", "#f1f6f8", "#e7785f"] },
  { id: "sunset", colors: ["#a94f38", "#fbf5ec", "#d9943b"] },
  { id: "lavender", colors: ["#675587", "#f7f4f8", "#c36e7e"] },
];

const fieldClass = "mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm text-[var(--ink)] outline-none transition focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";
const defaultSchedule: ScheduleDefaults = { day_start_time: "09:00", lunch_time: "12:00", lunch_duration_minutes: 60, dinner_time: "18:30", dinner_duration_minutes: 90 };
const emptyFlightDraft: FlightDraft = { airline: "", flight_number: "", origin: "", destination: "", departure_local: "", arrival_local: "", departure_timezone: "", arrival_timezone: "" };

export function TripEditor({ tripId }: { tripId: string }) {
  const aiCharge = useOperationCharge("ai_itinerary_generation");
  const optimizationCharge = useOperationCharge("itinerary_optimization");
  const repriceCharge = useOperationCharge("price_reoptimization");
  const locale = useLocale();
  const t = useTranslations("trips");
  const tStay = useTranslations("stayAreas");
  const tTrips = useTranslations("trips");
  const te = useTranslations("trips.editor");
  const router = useRouter();
  const [trip, setTrip] = useState<Trip>();
  const [items, setItems] = useState<TripItem[]>([]);
  const [routes, setRoutes] = useState<RouteSegment[]>([]);
  const [selectedRoute, setSelectedRoute] = useState<RouteSegment>();
  const [activeDay, setActiveDay] = useState("");
  const [editingId, setEditingId] = useState<string>();
  const [routeDrawerOpen, setRouteDrawerOpen] = useState(false);
  const [routeTarget, setRouteTarget] = useState<{ fromItemId: string; toItemId: string }>();
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();
  // Days the optimiser would refuse, kept out of the toast state so the offer to
  // lock the extra stops stays on screen until it is used or dismissed.
  const [optimizeBlock, setOptimizeBlock] = useState<{ limit: number; label: string; days: Array<{ date: string; excess: number }> }>();
  const [action, setAction] = useState<string>();
  const [shareUrl, setShareUrl] = useState("");
  const [dragged, setDragged] = useState<string>();
  const [saveState, setSaveState] = useState<SaveState>("saved");
  const [revision, setRevision] = useState(0);
  const [reloadToken, setReloadToken] = useState(0);
  const [staleDays, setStaleDays] = useState<Set<string>>(new Set());
  const [undoItem, setUndoItem] = useState<TripItem>();
  const [preview, setPreview] = useState<OptimizationPreview>();
  const [previewOpen, setPreviewOpen] = useState(false);
  const [confirmAction, setConfirmAction] = useState<ConfirmAction>();
  const [desktopMapVisible, setDesktopMapVisible] = useState(false);
  const [reorderMode, setReorderMode] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [aiMenuOpen, setAIMenuOpen] = useState(false);
  const [aiScope, setAIScope] = useState<AIPlanningScope>("day");
  const [aiPreview, setAIPreview] = useState<AIItineraryPreview>();
  const [plannerTheme, setPlannerTheme] = useState<PlannerTheme>("forest");
  const [draftItem, setDraftItem] = useState<TripItem>();
  const [recentItemId, setRecentItemId] = useState<string>();
  const [runtimeConfig, setRuntimeConfig] = useState<PublicRuntimeConfig>({});
  const [lodgingOpen, setLodgingOpen] = useState(false);
  const [stayOpen, setStayOpen] = useState(false);
  const [lodgingDraft, setLodgingDraft] = useState<LodgingDraft>({ name: "", location_name: "", provider_place_id: "", location_source: "google_places" });
  const [scheduleDraft, setScheduleDraft] = useState<ScheduleDefaults>(defaultSchedule);
  const [flightRole, setFlightRole] = useState<"outbound_flight" | "return_flight">();
  const [flightDraft, setFlightDraft] = useState<FlightDraft>(emptyFlightDraft);

  const tripRef = useRef<Trip | undefined>(undefined);
  const itemsRef = useRef<TripItem[]>([]);
  const revisionRef = useRef(0);
  const persistedRevisionRef = useRef(0);
  const saveStateRef = useRef<SaveState>("saved");
  const savePromiseRef = useRef<Promise<Trip | undefined> | undefined>(undefined);
  const optimizationApplyRef = useRef<{ previewId: string; key: string } | undefined>(undefined);
  const repriceRequestRef = useRef<{ tripVersion: number; key: string } | undefined>(undefined);
  const aiRequestRef = useRef<{ signature: string; key: string } | undefined>(undefined);
  const aiApplyRef = useRef<{ previewId: string; key: string } | undefined>(undefined);
  const routeHistoryTokenRef = useRef<string | undefined>(undefined);
  const dayScrollRef = useRef<HTMLDivElement>(null);
  const activeDayChipRef = useRef<HTMLButtonElement>(null);
  const draftKey = `trip-planner-draft:${tripId}`;

  useEffect(() => {
    let active = true;
    api<PublicRuntimeConfig>("/runtime/public-config")
      .then((value) => { if (active) setRuntimeConfig(value); })
      .catch(() => { /* capability labels stay hidden when runtime config is unavailable */ });
    return () => { active = false; };
  }, []);

  useEffect(() => {
    const restoreTheme = window.setTimeout(() => {
      try {
        const stored = window.localStorage.getItem("travel-planner-theme");
        if (plannerThemes.some((theme) => theme.id === stored)) setPlannerTheme(stored as PlannerTheme);
      } catch { /* storage can be blocked */ }
    }, 0);
    return () => window.clearTimeout(restoreTheme);
  }, []);

  function selectPlannerTheme(value: PlannerTheme) {
    setPlannerTheme(value);
    try { window.localStorage.setItem("travel-planner-theme", value); } catch { /* storage can be blocked */ }
  }

  useEffect(() => {
    const container = dayScrollRef.current;
    const chip = activeDayChipRef.current;
    if (!container || !chip) return;
    const left = chip.offsetLeft - (container.clientWidth - chip.offsetWidth) / 2;
    container.scrollTo?.({ left: Math.max(0, left), behavior: "smooth" });
  }, [activeDay]);

  const updateSaveState = useCallback((value: SaveState) => {
    saveStateRef.current = value;
    setSaveState(value);
  }, []);

  const replaceTrip = useCallback((value: Trip, replaceItems = true) => {
    tripRef.current = value;
    setTrip(value);
    if (replaceItems) {
      itemsRef.current = value.items;
      setItems(value.items);
    }
  }, []);

  const closeRouteDrawer = useCallback(() => {
    const token = routeHistoryTokenRef.current;
    if (token && window.history.state?.tripRouteDrawer === token) {
      window.history.back();
      return;
    }
    routeHistoryTokenRef.current = undefined;
    setRouteDrawerOpen(false);
    setRouteTarget(undefined);
  }, []);

  useEffect(() => {
    let active = true;
    api<Trip>(`/trips/${tripId}`)
      .then((value) => {
        if (!active) return;
        let stored: StoredTripDraft | undefined;
        try {
          const raw = window.localStorage.getItem(draftKey);
          if (raw) stored = JSON.parse(raw) as StoredTripDraft;
        } catch {
          try { window.localStorage.removeItem(draftKey); } catch { /* storage can be blocked */ }
        }
        const hasDraft = Boolean(stored?.items?.length && stored.routePreference);
        const loaded = hasDraft && stored
          ? { ...value, items: normalize(stored.items), route_preference: stored.routePreference }
          : value;
        replaceTrip(loaded);
        setRoutes(value.route_segments || []);
        const availableDays = daysBetween(value.start_date, value.end_date);
        const localToday = todayForTimezone(value.timezone);
        const initialDay = availableDays.includes(localToday)
          ? localToday
          : availableDays[0] || value.items[0]?.day_date || "";
        setActiveDay(initialDay);
        const initialIds = new Set(
          value.items.filter((item) => item.day_date === initialDay).map((item) => item.id),
        );
        setSelectedRoute(
          value.route_segments?.find((route) => initialIds.has(route.from_item_id)),
        );
        if (hasDraft && stored) {
          revisionRef.current = 1;
          setRevision(1);
          if (stored.baseVersion === value.version) {
            updateSaveState("dirty");
            setNotice(te("draftRestored"));
          } else {
            updateSaveState("conflict");
            setError(te("draftConflict"));
          }
        }
      })
      .catch((reason: Error) => setError(reason.message));
    return () => { active = false; };
  }, [draftKey, reloadToken, replaceTrip, tripId, updateSaveState, te]);

  useEffect(() => {
    if (!trip || !["queued", "processing"].includes(trip.routing?.status || "")) return;
    let active = true;
    let running = false;
    const poll = async () => {
      if (running || saveStateRef.current !== "saved") return;
      running = true;
      try {
        const status = await api<{ version: number; status: string }>(`/trips/${trip.id}/routes/status`);
        if (!active) return;
        if (!["queued", "processing"].includes(status.status)) {
          const latest = await api<Trip>(`/trips/${trip.id}`);
          if (!active) return;
          replaceTrip(latest);
          setRoutes(latest.route_segments || []);
          setSelectedRoute((current) => latest.route_segments?.find((route) =>
            route.from_item_id === current?.from_item_id && route.to_item_id === current?.to_item_id,
          ) || latest.route_segments?.[0]);
          setStaleDays(new Set());
          if (status.status === "partial") setNotice(te("routesPartial"));
          if (status.status === "complete") setNotice(te("routesComplete"));
        }
      } catch {
        // The itinerary remains usable while a background status check is unavailable.
      } finally {
        running = false;
      }
    };
    void poll();
    const timer = window.setInterval(() => void poll(), 1_800);
    return () => { active = false; window.clearInterval(timer); };
  }, [replaceTrip, trip, te]);

  useEffect(() => {
    if (!undoItem) return;
    const timer = window.setTimeout(() => setUndoItem(undefined), 8_000);
    return () => window.clearTimeout(timer);
  }, [undoItem]);

  useEffect(() => {
    if (!notice) return;
    const timer = window.setTimeout(() => setNotice(undefined), undoItem ? 8_000 : 4_000);
    return () => window.clearTimeout(timer);
  }, [notice, undoItem]);

  useEffect(() => {
    if (!recentItemId) return;
    const scrollTimer = window.setTimeout(() => {
      document.getElementById(`trip-item-${recentItemId}`)?.scrollIntoView?.({
        behavior: "smooth",
        block: "center",
      });
    }, 100);
    const timer = window.setTimeout(() => setRecentItemId(undefined), 1_800);
    return () => {
      window.clearTimeout(scrollTimer);
      window.clearTimeout(timer);
    };
  }, [recentItemId]);

  useEffect(() => {
    if (!trip || revisionRef.current === persistedRevisionRef.current) return;
    try {
      window.localStorage.setItem(draftKey, JSON.stringify({
        baseVersion: trip.version,
        savedAt: new Date().toISOString(),
        items: normalize(items),
        routePreference: trip.route_preference,
      } satisfies StoredTripDraft));
    } catch {
      // The in-memory draft and unload warning remain available when storage is blocked.
    }
  }, [draftKey, items, revision, trip]);

  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const query = window.matchMedia("(min-width: 1024px)");
    const update = () => setDesktopMapVisible(query.matches);
    update();
    query.addEventListener?.("change", update);
    return () => query.removeEventListener?.("change", update);
  }, []);

  useEffect(() => {
    if (!routeDrawerOpen || typeof window.matchMedia !== "function"
      || !window.matchMedia("(max-width: 1023px)").matches) return;
    const token = crypto.randomUUID();
    routeHistoryTokenRef.current = token;
    window.history.pushState({ ...window.history.state, tripRouteDrawer: token }, "", window.location.href);
    const closeFromBack = () => {
      if (routeHistoryTokenRef.current !== token) return;
      routeHistoryTokenRef.current = undefined;
      setRouteDrawerOpen(false);
      setRouteTarget(undefined);
    };
    window.addEventListener("popstate", closeFromBack);
    return () => window.removeEventListener("popstate", closeFromBack);
  }, [routeDrawerOpen]);

  useEffect(() => {
    function warnBeforeLeaving(event: BeforeUnloadEvent) {
      if (!["dirty", "saving", "offline", "conflict"].includes(saveStateRef.current)) return;
      event.preventDefault();
    }
    window.addEventListener("beforeunload", warnBeforeLeaving);
    return () => window.removeEventListener("beforeunload", warnBeforeLeaving);
  }, []);

  const days = useMemo(() => {
    const explicit = daysBetween(trip?.start_date, trip?.end_date);
    return explicit.length ? explicit : [...new Set(items.map((item) => item.day_date))].sort();
  }, [items, trip?.end_date, trip?.start_date]);
  const groups = useMemo(() => new Map(groupTripItems(normalize(items))), [items]);
  const activeDayItems = groups.get(activeDay) || [];
  const allLogistics = items.filter(isLogisticsItem);
  const activeRows = activeDayItems.filter((item) => !isLogisticsItem(item));
  const lodgingReady = trip?.primary_lodging?.latitude != null && trip.primary_lodging.longitude != null;
  const activeDisplayRows = activeRows.filter(
    (item) => lodgingReady || item.system_role !== "hotel_end",
  );
  const activeRouteRows = activeRows.filter(isActiveRouteItem);
  const movable = activeRows.filter((item) => !item.system_role);
  const activeArrangementCount = activeRouteRows.filter((item) => !item.system_role?.startsWith("hotel_")).length;
  const activeDurationMinutes = activeRouteRows.reduce((total, item) => total + (item.duration_minutes || 0), 0);
  const tripRouteItemCount = items.filter(isActiveRouteItem).length;
  const placeCountryCodes = useMemo(() => countryCodesForTrip(trip), [trip]);
  const placeBias = useMemo(() => {
    const reference = items.find((item) => item.latitude != null && item.longitude != null);
    return reference?.latitude != null && reference.longitude != null
      ? { latitude: reference.latitude, longitude: reference.longitude }
      : undefined;
  }, [items]);
  const editingItem = draftItem || items.find((item) => item.id === editingId);
  const editingMeal = editingItem?.system_role === "lunch" || editingItem?.system_role === "dinner";
  const editingFlightItem = items.find((item) => item.system_role === flightRole);
  const flightDraftReady = Boolean(
    flightDraft.airline.trim()
    && flightDraft.flight_number.trim()
    && flightDraft.origin.trim()
    && flightDraft.destination.trim()
    && flightDraft.departure_local
    && flightDraft.arrival_local,
  );

  // One background action runs at a time, but only the controls that belong to
  // it should lock. `action` used to disable six whole button rows at once,
  // which read as "the planner froze" whenever anything was in flight.
  const busy = (...scopes: string[]) =>
    Boolean(action && scopes.some((scope) => action === scope || action.startsWith(`${scope}-`)));

  function markEdited(staleDay?: string) {
    revisionRef.current += 1;
    setRevision(revisionRef.current);
    updateSaveState("dirty");
    if (staleDay) setStaleDays((current) => new Set(current).add(staleDay));
  }

  function updateItems(updater: (current: TripItem[]) => TripItem[], staleDay?: string) {
    setItems((current) => {
      const next = normalize(updater(current));
      itemsRef.current = next;
      return next;
    });
    markEdited(staleDay);
  }

  function patchItem(id: string, patch: Partial<TripItem>, routeImpact = true) {
    if (draftItem?.id === id) {
      setDraftItem((current) => current ? { ...current, ...patch } : current);
      return;
    }
    const currentItem = itemsRef.current.find((item) => item.id === id);
    const affectedDays = new Set([currentItem?.day_date, patch.day_date].filter(Boolean) as string[]);
    updateItems(
      (current) => current.map((item) => item.id === id ? { ...item, ...patch } : item),
      routeImpact ? currentItem?.day_date : undefined,
    );
    if (routeImpact) {
      setRoutes((current) => current.filter((route) => route.from_item_id !== id && route.to_item_id !== id));
      if (selectedRoute?.from_item_id === id || selectedRoute?.to_item_id === id) {
        setSelectedRoute(undefined);
        closeRouteDrawer();
      }
      setStaleDays((current) => new Set([...current, ...affectedDays]));
    }
  }

  const persistOnce = useCallback(async (): Promise<Trip | undefined> => {
    if (savePromiseRef.current) return savePromiseRef.current;
    const currentTrip = tripRef.current;
    if (!currentTrip) return undefined;
    if (revisionRef.current === persistedRevisionRef.current && saveStateRef.current === "saved") {
      return currentTrip;
    }
    const snapshotRevision = revisionRef.current;
    const snapshotItems = normalize(itemsRef.current);
    updateSaveState("saving");
    setError(undefined);
    const request = api<Trip>(`/trips/${currentTrip.id}/itinerary`, {
      method: "PUT",
      body: JSON.stringify({
        version: currentTrip.version,
        items: snapshotItems,
        route_preference: currentTrip.route_preference,
      }),
    })
      .then((updated) => {
        persistedRevisionRef.current = snapshotRevision;
        replaceTrip(updated, revisionRef.current === snapshotRevision);
        if (revisionRef.current === snapshotRevision) {
          updateSaveState("saved");
          try { window.localStorage.removeItem(draftKey); } catch { /* storage can be blocked */ }
        } else {
          updateSaveState("dirty");
        }
        return updated;
      })
      .catch((reason: unknown) => {
        if (reason instanceof ApiError && reason.code === "trip_version_conflict") {
          updateSaveState("conflict");
          setError(te("versionConflict"));
        } else {
          updateSaveState("offline");
          setError(te("saveFailedKept", { message: reason instanceof Error ? reason.message : te("saveFailedFallback") }));
        }
        return undefined;
      })
      .finally(() => { savePromiseRef.current = undefined; });
    savePromiseRef.current = request;
    return request;
  }, [draftKey, replaceTrip, updateSaveState, te]);

  const flushChanges = useCallback(async (showNotice = false): Promise<Trip | undefined> => {
    let didSave = false;
    for (let attempt = 0; attempt < 20; attempt += 1) {
      if (saveStateRef.current === "conflict") return undefined;
      if (revisionRef.current === persistedRevisionRef.current) {
        updateSaveState("saved");
        if (showNotice) setNotice(didSave ? te("saved") : te("allSaved"));
        return tripRef.current;
      }
      const updated = await persistOnce();
      if (!updated) return undefined;
      didSave = true;
    }
    updateSaveState("offline");
    setError(te("stillSyncing"));
    return undefined;
  }, [persistOnce, updateSaveState, te]);

  useEffect(() => {
    if (saveState !== "dirty") return;
    const timer = window.setTimeout(() => { void flushChanges(false); }, 1_000);
    return () => window.clearTimeout(timer);
  }, [flushChanges, revision, saveState]);

  function movableRows(day: string) {
    return itemsRef.current
      .filter((row) => row.day_date === day && !row.system_role && !isLogisticsItem(row))
      .sort((a, b) => a.position - b.position);
  }

  function move(id: string, direction: -1 | 1) {
    const item = itemsRef.current.find((row) => row.id === id);
    if (!item || item.system_role) return;
    const sameDay = movableRows(item.day_date);
    const index = sameDay.findIndex((row) => row.id === id);
    const target = sameDay[index + direction];
    // At the edge there is nothing to swap with. Returning early matters: the
    // old code still marked the trip dirty and threw away the day's computed
    // routes for a move that visibly did nothing.
    if (!target) return;
    const reordered = itemsRef.current.map((row) => row.id === id
      ? { ...row, position: target.position }
      : row.id === target.id ? { ...row, position: item.position } : row);
    updateItems(() => reordered, item.day_date);
    // Only the legs around the swapped stops changed; every other segment (and its
    // real travel time) survives, exactly like the server-side invalidation.
    setRoutes((current) => segmentsForRows(current, reordered));
    if (selectedRoute && segmentsForRows([selectedRoute], reordered).length === 0) {
      setSelectedRoute(undefined);
      closeRouteDrawer();
    }
  }

  function drop(targetId: string) {
    if (!dragged || dragged === targetId) return;
    const source = itemsRef.current.find((item) => item.id === dragged);
    const target = itemsRef.current.find((item) => item.id === targetId);
    if (!source || !target || source.system_role || target.system_role) return;
    const dropped = itemsRef.current.map((item) => item.id === source.id
      ? { ...item, day_date: target.day_date, position: target.position }
      : item.id === target.id && source.day_date === target.day_date
        ? { ...item, position: source.position }
        : item);
    updateItems(() => dropped, source.day_date);
    setStaleDays((current) => new Set([...current, source.day_date, target.day_date]));
    // A drop only breaks the legs around the moved stop, on both days involved.
    setRoutes((current) => segmentsForRows(current, dropped));
    if (selectedRoute && segmentsForRows([selectedRoute], dropped).length === 0) {
      setSelectedRoute(undefined);
      closeRouteDrawer();
    }
    setDragged(undefined);
  }

  function add(day: string, atPosition?: number) {
    const item: TripItem = {
      id: crypto.randomUUID(), item_type: "custom", day_date: day,
      // By default the new stop goes to the end; an insertion point between two
      // cards hands us the position it should take instead.
      position: atPosition ?? itemsRef.current.filter((row) => row.day_date === day).length,
      title: "", location_name: "", locked: false, fixed_time: false,
      is_estimated: true, duration_minutes: 60, data: { source_mode: "manual" },
    };
    setActiveDay(day);
    setDraftItem(item);
  }

  function closeEditor() {
    setDraftItem(undefined);
    setEditingId(undefined);
  }

  function commitDraftItem() {
    if (!draftItem?.title.trim()) return;
    const item = { ...draftItem, title: draftItem.title.trim() };
    updateItems((current) => [
      ...current.map((row) => row.day_date === item.day_date && row.position >= item.position
        ? { ...row, position: row.position + 1 }
        : row),
      item,
    ], item.day_date);
    setActiveDay(item.day_date);
    setRecentItemId(item.id);
    setDraftItem(undefined);
    setNotice(te("added"));
  }

  function choosePlace(item: TripItem, place: Place) {
    patchItem(item.id, {
      title: item.title.trim() ? item.title : place.name,
      location_name: place.address || place.name,
      latitude: place.latitude,
      longitude: place.longitude,
      provider_place_id: place.place_id,
      location_source: "confirmed",
      location_provider: place.provider,
      is_estimated: false,
      data: { ...item.data, opening_hours: place.opening_hours || [], google_maps_url: place.google_maps_url, naver_maps_url: place.naver_maps_url || place.external_url, place_provider: place.provider, attribution: place.attribution, place_match_status: "confirmed", needs_place_confirmation: false, ...(item.system_role === "lunch" || item.system_role === "dinner" ? { meal_selection_source: "user" } : {}) },
    });
  }

  function openLodgingEditor() {
    const lodging = tripRef.current?.primary_lodging;
    setLodgingDraft({
      name: lodging?.name || "",
      location_name: lodging?.location_name || "",
      provider_place_id: lodging?.provider_place_id || "",
      latitude: lodging?.latitude ?? undefined,
      longitude: lodging?.longitude ?? undefined,
      location_source: lodging?.location_source || "google_places",
    });
    setLodgingOpen(true);
  }

  function openStayFlow() {
    setStayOpen(true);
  }

  async function selectStayHotel(area: StayArea, hotel: StayHotel): Promise<StaySelectResult> {
    const currentTrip = await flushChanges(false);
    if (!currentTrip) return "error";
    setAction("lodging");
    setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${currentTrip.id}/stay-areas/${area.code}/select`, {
        method: "POST",
        body: JSON.stringify({ version: currentTrip.version, provider: hotel.provider, hotel_id: hotel.hotel_id }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(undefined);
      setStayOpen(false);
      setStaleDays(new Set(days));
      setNotice(tStay("notice.chosen", { hotel: hotel.hotel_name }));
      return "ok";
    } catch (reason) {
      if (reason instanceof ApiError && reason.code === "hotel_offer_expired") return "expired";
      if (reason instanceof ApiError && reason.code === "trip_version_conflict") {
        updateSaveState("conflict");
        setError(tStay("notice.versionConflict"));
        return "error";
      }
      setError(reason instanceof Error ? reason.message : tStay("notice.selectFailed"));
      return "error";
    } finally { setAction(undefined); }
  }

  function openFlightEditor(item: TripItem) {
    if (!isFlightAnchor(item)) return;
    const info = flightAnchorInfo(item);
    setFlightRole(item.system_role);
    setFlightDraft({
      airline: info?.airline || "",
      flight_number: info?.flight_number || "",
      origin: info?.origin || "",
      destination: info?.destination || "",
      departure_local: info?.departure_local || item.start_time?.slice(0, 16) || "",
      arrival_local: info?.arrival_local || item.end_time?.slice(0, 16) || "",
      departure_timezone: info?.departure_timezone || "",
      arrival_timezone: info?.arrival_timezone || "",
    });
  }

  async function saveFlightAnchor(clear = false) {
    const currentTrip = await flushChanges(false);
    if (!currentTrip || !flightRole) return;
    const direction = flightRole === "outbound_flight" ? "outbound" : "return";
    setAction(`flight-${direction}`);
    setError(undefined);
    try {
      const flight = clear ? null : {
        ...flightDraft,
        airline: flightDraft.airline.trim(),
        flight_number: flightDraft.flight_number.trim(),
        origin: flightDraft.origin.trim().toUpperCase(),
        destination: flightDraft.destination.trim().toUpperCase(),
        departure_timezone: flightDraft.departure_timezone.trim() || null,
        arrival_timezone: flightDraft.arrival_timezone.trim() || null,
      };
      const updated = await api<Trip>(`/trips/${currentTrip.id}/flight-anchors/${direction}`, {
        method: "PUT",
        body: JSON.stringify({ version: currentTrip.version, flight }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setFlightRole(undefined);
      setNotice(te(clear ? "flightCleared" : "flightUpdated", { direction: te(direction === "outbound" ? "outbound" : "returnLeg") }));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : te("flightUpdateFailed"));
    } finally { setAction(undefined); }
  }

  function chooseLodgingPlace(place: Place) {
    setLodgingDraft((current) => ({
      ...current,
      name: current.name.trim() || place.name,
      location_name: place.address || place.name,
      provider_place_id: place.place_id,
      latitude: place.latitude ?? undefined,
      longitude: place.longitude ?? undefined,
      location_source: place.provider,
    }));
  }

  async function savePrimaryLodging() {
    const currentTrip = await flushChanges(false);
    if (!currentTrip || !lodgingDraft.name.trim() || !lodgingDraft.location_name.trim()) return;
    setAction("lodging");
    setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${currentTrip.id}/primary-lodging`, {
        method: "PUT",
        body: JSON.stringify({ ...lodgingDraft, name: lodgingDraft.name.trim(), location_name: lodgingDraft.location_name.trim() || lodgingDraft.name.trim(), provider_place_id: lodgingDraft.provider_place_id || null, version: currentTrip.version }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(undefined);
      setLodgingOpen(false);
      setStaleDays(new Set(days));
      setNotice(te(lodgingDraft.latitude == null ? "lodgingSyncedNoLocation" : "lodgingSynced"));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : te("lodgingFailed"));
    } finally { setAction(undefined); }
  }

  function openTools() {
    setScheduleDraft(tripRef.current?.schedule_defaults || defaultSchedule);
    setToolsOpen(true);
  }

  async function saveScheduleDefaults() {
    const currentTrip = await flushChanges(false);
    if (!currentTrip) return;
    setAction("schedule-defaults");
    setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${currentTrip.id}/schedule-defaults`, {
        method: "PUT",
        body: JSON.stringify({ ...scheduleDraft, version: currentTrip.version }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(undefined);
      setStaleDays(new Set(days));
      setNotice(te("scheduleApplied"));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : te("scheduleFailed"));
    } finally { setAction(undefined); }
  }

  async function saveDepartureTime(value: string) {
    const defaults = tripRef.current?.schedule_defaults || defaultSchedule;
    if (value >= defaults.lunch_time) {
      setError(te("departureBeforeLunchAt", { time: defaults.lunch_time }));
      return;
    }
    const currentTrip = await flushChanges(false);
    if (!currentTrip) return;
    setAction("departure-time");
    setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${currentTrip.id}/schedule-defaults`, {
        method: "PUT",
        body: JSON.stringify({ ...defaults, day_start_time: value, version: currentTrip.version }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(undefined);
      setStaleDays(new Set(days));
      setScheduleDraft({ ...defaults, day_start_time: value });
      setNotice(te("departureUpdated", { time: value }));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : te("departureFailed"));
    } finally { setAction(undefined); }
  }

  async function toggleMealSkip(item: TripItem) {
    const currentTrip = await flushChanges(false);
    if (!currentTrip) return;
    setAction(`skip-${item.id}`);
    setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${currentTrip.id}/items/${item.id}/skip`, {
        method: "PATCH",
        body: JSON.stringify({ version: currentTrip.version, skipped: !item.is_skipped }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(undefined);
      setStaleDays((current) => new Set(current).add(item.day_date));
      setNotice(te(item.is_skipped ? "mealRestored" : "mealSkipped"));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : te("mealFailed"));
    } finally { setAction(undefined); }
  }

  function removeItem(item: TripItem) {
    if (item.system_role) return;
    updateItems((current) => current.filter((row) => row.id !== item.id), item.day_date);
    setRoutes((current) => current.filter((route) => route.from_item_id !== item.id && route.to_item_id !== item.id));
    if (selectedRoute?.from_item_id === item.id || selectedRoute?.to_item_id === item.id) {
      setSelectedRoute(undefined);
      closeRouteDrawer();
    }
    setEditingId(undefined);
    setUndoItem(item);
    setNotice(te("deletedUndo"));
  }

  function undoDelete() {
    if (!undoItem) return;
    updateItems((current) => [...current, undoItem], undoItem.day_date);
    setActiveDay(undoItem.day_date);
    setUndoItem(undefined);
    setNotice(te("restored"));
  }

  async function computeRoutes(
    day: string,
    refresh = false,
    override?: { mode?: TravelMode; buffer?: number },
  ) {
    const currentTrip = await flushChanges(false);
    if (!currentTrip || saveStateRef.current === "conflict") return;
    setAction(`route-${day}`);
    setError(undefined);
    try {
      const daySetting = currentTrip.routing?.day_settings.find((setting) => setting.day_date === day);
      const selectedMode = override?.mode || daySetting?.default_travel_mode || "transit";
      const selectedBuffer = override?.buffer ?? daySetting?.default_buffer_minutes ?? 10;
      const result = await api<RouteDayComputeResponse>(`/trips/${currentTrip.id}/routes/compute-day`, {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          version: currentTrip.version,
          day_date: day,
          default_travel_mode: selectedMode,
          default_buffer_minutes: selectedBuffer,
          route_preference: currentTrip.route_preference,
          refresh,
        }),
      });
      replaceTrip({
        ...currentTrip,
        version: result.version,
        routing: {
          status: result.status as TripRouting["status"],
          total: result.total,
          completed: result.completed,
          warnings: result.unresolved_items?.map((item) => `${item.title}：${item.reason}`) || [],
          unresolved_items: result.unresolved_items,
          day_settings: [
            ...(currentTrip.routing?.day_settings || []).filter((setting) => setting.day_date !== day),
            {
              day_date: day,
              default_travel_mode: selectedMode,
              default_buffer_minutes: selectedBuffer,
              route_preference: currentTrip.route_preference || "FEWER_TRANSFERS",
              auto_compute: true,
            },
          ].sort((a, b) => a.day_date.localeCompare(b.day_date)),
        },
      }, false);
      setNotice(te(result.status === "needs_locations" ? "routesNeedLocations" : "routesQueued"));
    } catch (reason) {
      setError(te("notChargedSuffix", { message: reason instanceof Error ? reason.message : te("routesFailed") }));
    } finally { setAction(undefined); }
  }

  function crowdedDays(current: Trip, day?: string) {
    const summary = current.optimization;
    if (!summary) return [];
    return summary.days
      .filter((entry) => (!day || entry.date === day) && entry.movable_count > summary.movable_limit)
      .map((entry) => ({ date: entry.date, excess: entry.movable_count - summary.movable_limit }));
  }

  function lockCrowdedDays() {
    if (!optimizeBlock) return;
    let locked = 0;
    for (const entry of optimizeBlock.days) {
      const movableRows = itemsRef.current.filter((item) =>
        item.day_date === entry.date
        && isActiveRouteItem(item)
        && !item.locked
        && !item.fixed_time
        && (item.latitude != null || item.provider_place_id));
      for (const item of movableRows.slice(Math.max(0, movableRows.length - entry.excess))) {
        patchItem(item.id, { locked: true }, false);
        locked += 1;
      }
    }
    setOptimizeBlock(undefined);
    setNotice(te("optimizeLockedExtras", { count: locked }));
  }

  async function previewOptimization(day?: string) {
    const currentTrip = await flushChanges(false);
    if (!currentTrip || saveStateRef.current === "conflict") return;
    const crowded = crowdedDays(currentTrip, day);
    if (crowded.length > 0 && currentTrip.optimization) {
      // The API answers 422 for a day with too many movable stops. Say so before spending
      // the request, and offer the lock that makes the optimiser runnable.
      setOptimizeBlock({
        limit: currentTrip.optimization.movable_limit,
        label: day || te("optimizeAllDays"),
        days: crowded,
      });
      return;
    }
    setOptimizeBlock(undefined);
    setAction(`preview-${day || "all"}`);
    setError(undefined);
    try {
      const value = await api<OptimizationPreview>(`/trips/${currentTrip.id}/itinerary/optimize/preview`, {
        method: "POST",
        body: JSON.stringify({ version: currentTrip.version, day_date: day || null, route_preference: currentTrip.route_preference }),
      });
      optimizationApplyRef.current = {
        previewId: value.preview_id,
        key: crypto.randomUUID(),
      };
      setPreview(value);
      setPreviewOpen(true);
    } catch (reason) {
      setError(te("notChargedSuffix", { message: reason instanceof Error ? reason.message : te("previewFailed") }));
    } finally { setAction(undefined); }
  }

  async function applyOptimization() {
    if (!tripRef.current || !preview) return;
    const requestIdentity = optimizationApplyRef.current?.previewId === preview.preview_id
      ? optimizationApplyRef.current
      : { previewId: preview.preview_id, key: crypto.randomUUID() };
    optimizationApplyRef.current = requestIdentity;
    setAction("apply-preview");
    setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${tripRef.current.id}/itinerary/optimize/apply`, {
        method: "POST",
        headers: { "Idempotency-Key": requestIdentity.key },
        body: JSON.stringify({ preview_id: preview.preview_id, version: tripRef.current.version }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(updated.route_segments?.[0]);
      setStaleDays(new Set());
      persistedRevisionRef.current = revisionRef.current;
      updateSaveState("saved");
      setPreviewOpen(false);
      setPreview(undefined);
      optimizationApplyRef.current = undefined;
      try { window.localStorage.removeItem(draftKey); } catch { /* storage can be blocked */ }
      setNotice(updated.usage?.status === "charged"
        ? te("optimizationApplied", { uses: updated.usage.uses })
        : te("optimizationChecked"));
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        optimizationApplyRef.current = undefined;
        router.push("/pricing");
        return;
      }
      if (reason instanceof ApiError) {
        optimizationApplyRef.current = undefined;
        setError(te("serverNotCharged", { message: reason.message }));
      } else {
        setError(te("retrySameKeyNoDouble", { message: reason instanceof Error ? reason.message : te("optimizationApplyFailed") }));
      }
    } finally { setAction(undefined); }
  }

  async function reoptimizePrices() {
    const currentTrip = await flushChanges(false);
    if (!currentTrip) return;
    const requestIdentity = repriceRequestRef.current?.tripVersion === currentTrip.version
      ? repriceRequestRef.current
      : { tripVersion: currentTrip.version, key: crypto.randomUUID() };
    repriceRequestRef.current = requestIdentity;
    setAction("reprice");
    setError(undefined);
    try {
      const updated = await api<Trip>(`/trips/${currentTrip.id}/reoptimize`, {
        method: "POST",
        headers: { "Idempotency-Key": requestIdentity.key },
        // The server compares this before touching a row, like every other trip write.
        body: JSON.stringify({ version: currentTrip.version }),
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(updated.route_segments?.[0]);
      repriceRequestRef.current = undefined;
      setNotice(updated.usage?.status === "charged" ? te("repriced", { uses: updated.usage.uses }) : te("repriceNotCharged"));
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        repriceRequestRef.current = undefined;
        router.push("/pricing");
      } else if (reason instanceof ApiError) {
        repriceRequestRef.current = undefined;
        setError(te("serverNotCharged", { message: reason.message }));
      } else {
        setError(te("retrySameKey", { message: reason instanceof Error ? reason.message : te("repriceFailed") }));
      }
    } finally { setAction(undefined); }
  }

  function openAIPlanner(defaultScope: AIPlanningScope) {
    setAIScope(defaultScope === "day" && !activeDay ? "trip" : defaultScope);
    setAIPreview(undefined);
    aiApplyRef.current = undefined;
    setAIMenuOpen(true);
  }

  async function generateAIItinerary(scope: AIPlanningScope) {
    const dayDate = scope === "day" ? activeDay : undefined;
    if (scope === "day" && !dayDate) {
      setError(te("pickDayFirst"));
      return;
    }
    const currentTrip = await flushChanges(false);
    if (!currentTrip || saveStateRef.current === "conflict") return;
    const signature = `${currentTrip.version}:${scope}:${dayDate || "all"}`;
    const requestIdentity = aiRequestRef.current?.signature === signature
      ? aiRequestRef.current
      : { signature, key: crypto.randomUUID() };
    aiRequestRef.current = requestIdentity;
    setAction(`ai-${scope}`);
    setError(undefined);
    setNotice(undefined);
    try {
      const previewResult = await api<AIItineraryPreview>(`/trips/${currentTrip.id}/itinerary/preview`, {
        method: "POST",
        headers: { "Idempotency-Key": requestIdentity.key },
        body: JSON.stringify({
          version: currentTrip.version,
          scope,
          day_date: dayDate || null,
        }),
      });
      setAIPreview(previewResult);
      aiRequestRef.current = undefined;
      setNotice(te("previewReady"));
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        aiRequestRef.current = undefined;
        setAIMenuOpen(false);
        router.push("/pricing");
      } else if (reason instanceof ApiError) {
        aiRequestRef.current = undefined;
        setError(te("unchangedNotCharged", { message: reason.message }));
      } else {
        setError(te("retrySameKey", { message: reason instanceof Error ? reason.message : te("aiFailed") }));
      }
    } finally { setAction(undefined); }
  }

  async function applyAIItinerary() {
    if (!trip || !aiPreview) return;
    const requestIdentity = aiApplyRef.current?.previewId === aiPreview.preview_id
      ? aiApplyRef.current
      : { previewId: aiPreview.preview_id, key: crypto.randomUUID() };
    aiApplyRef.current = requestIdentity;
    setAction("ai-apply");
    setError(undefined);
    setNotice(undefined);
    try {
      const updated = await api<Trip>(`/trips/${trip.id}/itinerary/apply`, {
        method: "POST",
        headers: { "Idempotency-Key": requestIdentity.key },
        body: JSON.stringify({
          version: aiPreview.base_version,
          preview_id: aiPreview.preview_id,
        }),
      });
      replaceTrip(updated);
      setRoutes([]);
      setSelectedRoute(undefined);
      closeRouteDrawer();
      setStaleDays(new Set(aiPreview.scope === "day" && aiPreview.day_date ? [aiPreview.day_date] : days));
      revisionRef.current = 0;
      persistedRevisionRef.current = 0;
      setRevision(0);
      updateSaveState("saved");
      aiApplyRef.current = undefined;
      setAIPreview(undefined);
      setAIMenuOpen(false);
      try { window.localStorage.removeItem(draftKey); } catch { /* storage can be blocked */ }
      const provider = aiProviderLabel(updated.planning?.provider, te);
      const scopeLabel = aiPreview.scope === "day"
        ? mobileDayHeading(aiPreview.day_date || "", locale, te)
        : te("allDays", { count: days.length });
      setNotice(updated.usage?.status === "charged"
        ? te("aiAppliedCharged", { provider, scope: scopeLabel, uses: updated.usage.uses })
        : te("aiAppliedFree", { provider, scope: scopeLabel }));
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        aiApplyRef.current = undefined;
        setAIMenuOpen(false);
        router.push("/pricing");
      } else if (reason instanceof ApiError) {
        aiApplyRef.current = undefined;
        setError(te("unchangedRepreview", { message: reason.message }));
      } else {
        setError(te("unchangedSuffix", { message: reason instanceof Error ? reason.message : te("applyFailed") }));
      }
    } finally { setAction(undefined); }
  }

  async function createShare() {
    if (!tripRef.current) return;
    setAction("share");
    try {
      const result = await api<{ token: string; share_url: string }>(`/trips/${tripRef.current.id}/share`, { method: "POST" });
      const localizedShareUrl = `${window.location.origin}/${locale}/share/${result.token}`;
      setShareUrl(localizedShareUrl);
      replaceTrip({ ...tripRef.current, share_enabled: true }, false);
      await navigator.clipboard?.writeText(localizedShareUrl);
      setNotice(te("shareCreated"));
    } catch (reason) { setError(reason instanceof Error ? reason.message : te("shareCreateFailed")); }
    finally { setAction(undefined); }
  }

  async function share() {
    if (shareUrl) {
      await navigator.clipboard?.writeText(shareUrl);
      setNotice(te("shareCopied"));
    } else if (tripRef.current?.share_enabled) setConfirmAction("rotate-share");
    else await createShare();
  }

  async function revokeShare() {
    if (!tripRef.current) return;
    setAction("share");
    try {
      await api(`/trips/${tripRef.current.id}/share`, { method: "DELETE" });
      setShareUrl("");
      replaceTrip({ ...tripRef.current, share_enabled: false }, false);
      setNotice(te("shareRevoked"));
    } catch (reason) { setError(reason instanceof Error ? reason.message : te("shareRevokeFailed")); }
    finally { setAction(undefined); }
  }

  async function saveTripNotes(next: string) {
    const current = tripRef.current;
    if (!current) return;
    // Notes ride the same optimistic lock as every other trip write, so flush
    // any pending itinerary edit first — otherwise the version we send is one
    // the server has already moved past.
    await flushChanges();
    const base = tripRef.current;
    if (!base) return;
    const updated = await api<Trip>(`/trips/${base.id}`, {
      method: "PATCH",
      body: JSON.stringify({ version: base.version, notes: next || null }),
    });
    replaceTrip(updated, false);
  }

  async function saveDayNotes(day: string, next: string) {
    const current = tripRef.current;
    if (!current) return;
    await flushChanges();
    const base = tripRef.current;
    if (!base) return;
    const updated = await api<Trip>(`/trips/${base.id}/days/${day}/notes`, {
      method: "PUT",
      body: JSON.stringify({ version: base.version, notes: next || null }),
    });
    replaceTrip(updated, false);
  }

  async function withTripVersion<T>(call: (trip: Trip) => Promise<T>): Promise<T | undefined> {
    // The ledger shares the trip's optimistic lock, so any queued itinerary
    // edit has to land first or the version we send is already stale.
    await flushChanges();
    const base = tripRef.current;
    if (!base) return undefined;
    return call(base);
  }

  async function saveBudget(amount: string | null) {
    await withTripVersion(async (base) => {
      const updated = await api<Trip>(`/trips/${base.id}`, {
        method: "PATCH",
        body: JSON.stringify({ version: base.version, budget_amount: amount }),
      });
      replaceTrip(updated, false);
    });
  }

  async function saveCostCurrency(currency: string) {
    await withTripVersion(async (base) => {
      const updated = await api<Trip>(`/trips/${base.id}`, {
        method: "PATCH",
        body: JSON.stringify({ version: base.version, cost_currency: currency }),
      });
      replaceTrip(updated, false);
    });
  }

  async function addExpense(entry: { day_date: string; label: string; amount: string; category: string }) {
    await withTripVersion(async (base) => {
      const updated = await api<Trip>(`/trips/${base.id}/expenses`, {
        method: "POST",
        body: JSON.stringify({ version: base.version, ...entry }),
      });
      replaceTrip(updated, false);
    });
  }

  async function deleteExpense(expenseId: string) {
    await withTripVersion(async (base) => {
      const updated = await api<Trip>(
        `/trips/${base.id}/expenses/${expenseId}?version=${base.version}`,
        { method: "DELETE" },
      );
      replaceTrip(updated, false);
    });
  }

  async function seedExpenses(): Promise<number> {
    const before = tripRef.current?.cost?.items.length ?? 0;
    const after = await withTripVersion(async (base) => {
      const updated = await api<Trip>(`/trips/${base.id}/expenses/seed`, {
        method: "POST",
        body: JSON.stringify({ version: base.version }),
      });
      replaceTrip(updated, false);
      return updated.cost?.items.length ?? 0;
    });
    return Math.max(0, (after ?? before) - before);
  }

  async function loadCloudVersion() {
    setAction("conflict");
    try {
      const latest = await api<Trip>(`/trips/${tripId}`);
      replaceTrip(latest);
      setRoutes(latest.route_segments || []);
      setSelectedRoute(latest.route_segments?.[0]);
      revisionRef.current = 0;
      persistedRevisionRef.current = 0;
      setRevision(0);
      updateSaveState("saved");
      try { window.localStorage.removeItem(draftKey); } catch { /* storage can be blocked */ }
      setError(undefined);
      setNotice(te("cloudLoaded"));
    } catch (reason) {
      // Without this, a network hiccup here was an unhandled rejection: the
      // button un-disabled itself and nothing on screen changed.
      setError(t("cloudLoadFailed", { message: reason instanceof Error ? reason.message : t("cloudLoadFallback") }));
    } finally { setAction(undefined); }
  }

  async function overwriteConflict() {
    setAction("conflict");
    try {
      const latest = await api<Trip>(`/trips/${tripId}`);
      replaceTrip({ ...latest, items: itemsRef.current }, false);
      updateSaveState("dirty");
      await flushChanges(true);
    } catch (reason) {
      setError(t("overwriteFailed", { message: reason instanceof Error ? reason.message : t("overwriteFallback") }));
    } finally { setAction(undefined); }
  }

  const applyMetaUpdate = useCallback((updated: Trip) => {
    // A date change rebuilt the day grid server-side: route segments are gone,
    // system slots moved, and the version advanced. Resync the editor the way
    // loadCloudVersion does so the next autosave sends the new version.
    replaceTrip(updated);
    setRoutes(updated.route_segments || []);
    setSelectedRoute(undefined);
    revisionRef.current = 0;
    persistedRevisionRef.current = 0;
    setRevision(0);
    updateSaveState("saved");
    try { window.localStorage.removeItem(draftKey); } catch { /* storage can be blocked */ }
    setStaleDays(new Set());
    setError(undefined);
    const nextDays = daysBetween(updated.start_date, updated.end_date);
    setActiveDay((current) => (nextDays.includes(current) ? current : nextDays[0] || updated.items[0]?.day_date || ""));
  }, [draftKey, replaceTrip, updateSaveState]);

  async function runConfirmedAction() {
    const selected = confirmAction;
    setConfirmAction(undefined);
    if (selected === "reprice") await reoptimizePrices();
    if (selected === "revoke-share") await revokeShare();
    if (selected === "rotate-share") await createShare();
    if (selected === "overwrite-conflict") await overwriteConflict();
  }

  function updateRoutePreference(value: Trip["route_preference"]) {
    if (!tripRef.current) return;
    const updated = { ...tripRef.current, route_preference: value };
    tripRef.current = updated;
    setTrip(updated);
    setRoutes([]);
    setSelectedRoute(undefined);
    closeRouteDrawer();
    setStaleDays(new Set(days));
    markEdited();
  }

  const saveLabel = te(`saveState.${saveState}`);
  const saveIcon = saveState === "saving" ? <Loader2 size={15} className="animate-spin" />
    : saveState === "dirty" ? <Clock3 size={15} />
      : saveState === "offline" ? <WifiOff size={15} />
        : saveState === "conflict" ? <CircleAlert size={15} /> : <Check size={15} />;
  const today = todayForTimezone(trip?.timezone);
  const missingLegs = missingSegmentCount(activeRouteRows, routes);
  const activeDayRouteSetting = trip?.routing?.day_settings.find((setting) => setting.day_date === activeDay);
  const activeTravelMode = activeDayRouteSetting?.default_travel_mode || "transit";
  const activeTravelBuffer = activeDayRouteSetting?.default_buffer_minutes ?? 10;
  // Surviving segments keep their real times; only legs without one fall back to a
  // distance estimate, so an edit no longer turns the whole day into guesses.
  const chainedStarts = projectChainedStarts(activeDisplayRows, routes, activeTravelBuffer, activeTravelMode);
  const scheduleOrderError = scheduleDraft.day_start_time >= scheduleDraft.lunch_time
    ? te("departureBeforeLunch")
    : scheduleDraft.lunch_time >= scheduleDraft.dinner_time
      ? te("lunchBeforeDinner")
      : undefined;
  const outboundReady = items.some((item) => item.system_role === "outbound_flight" && item.data.flight_selection_source !== "unset");
  const returnReady = items.some((item) => item.system_role === "return_flight" && item.data.flight_selection_source !== "unset");
  const unresolvedRouteItems = items.filter((item) => !item.is_skipped && !isFlightAnchor(item) && !isLogisticsItem(item) && !item.system_role?.startsWith("hotel_") && item.latitude == null && item.longitude == null);
  const routeWarnings = trip?.routing?.warnings || [];
  const routeNeedsLocations = trip?.routing?.status === "needs_locations" || routeWarnings.some((warning) => warning.includes("缺少已確認地點"));
  const confirmCopy: Record<ConfirmAction, { title: string; description: string; label: string; danger?: boolean }> = {
    reprice: { title: te("confirm.reprice.title"), description: repriceCharge.status === "ready" ? te("confirm.reprice.description", { charge: repriceCharge.label }) : repriceCharge.unavailableHelp, label: te("confirm.reprice.label", { charge: repriceCharge.label }) },
    "revoke-share": { title: te("confirm.revokeShare.title"), description: te("confirm.revokeShare.description"), label: te("confirm.revokeShare.label"), danger: true },
    "rotate-share": { title: te("confirm.rotateShare.title"), description: te("confirm.rotateShare.description"), label: te("confirm.rotateShare.label") },
    "overwrite-conflict": { title: te("confirm.overwrite.title"), description: te("confirm.overwrite.description"), label: te("confirm.overwrite.label"), danger: true },
  };

  if (error && !trip) return <main className="mx-auto max-w-4xl px-5 py-16"><div role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800"><p>{te("loadFailedHint", { error })}</p><div className="mt-4 flex flex-wrap gap-2"><button type="button" onClick={() => { setError(undefined); setReloadToken((value) => value + 1); }} className="min-h-11 rounded-xl border border-red-200 bg-white px-4 font-semibold">{t("retry")}</button><button type="button" onClick={() => router.push("/trips")} className="min-h-11 rounded-xl bg-[var(--ink)] px-4 font-semibold text-white">{t("backToTrips")}</button></div></div></main>;
  if (!trip) return <main className="mx-auto max-w-4xl px-5 py-16"><div className="h-44 animate-pulse rounded-[2rem] bg-white/80" /><p className="mt-4 text-center text-sm text-[var(--muted)]">{te("loading")}</p></main>;

  return <main data-planner-theme={plannerTheme} className="planner-app-shell mx-auto max-w-7xl px-4 pb-36 sm:px-5 md:px-8 lg:pb-20">
    <header className="planner-app-bar flex lg:hidden">
      <button type="button" aria-label={te("backToTripsLabel")} onClick={() => router.push("/trips")} className="planner-icon-button">
        <ArrowLeft size={20} />
      </button>
      <div className="min-w-0 flex-1 text-center">
        <p className="truncate text-[.68rem] font-semibold tracking-[.12em] text-[var(--muted)]">{trip.destination_name || te("myTrip")}</p>
        <h1 className="truncate text-base font-bold tracking-tight">{trip.name}</h1>
      </div>
      <button type="button" aria-label={te("openTools")} aria-expanded={toolsOpen} onClick={openTools} className="planner-icon-button">
        <Settings2 size={20} />
      </button>
    </header>

    <section className="planner-hero-panel relative mb-5 hidden overflow-hidden rounded-[2rem] border p-5 shadow-[var(--shadow-lg)] sm:p-7 lg:block">
      <div aria-hidden="true" className="absolute -right-12 -top-16 h-44 w-44 rounded-full bg-[var(--coral)]/10 blur-2xl" />
      <div className="relative flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold"><span className="rounded-full bg-white/75 px-3 py-1.5 text-[var(--teal)]">{te("plannerVersion", { version: trip.version })}</span><span aria-live="polite" className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 ${saveState === "saved" ? "bg-emerald-50 text-emerald-800" : saveState === "dirty" || saveState === "saving" ? "bg-amber-50 text-amber-900" : "bg-red-50 text-red-800"}`}>{saveIcon}{saveLabel}</span></div>
          <div className="mt-3 flex items-center gap-3"><h1 className="text-3xl font-bold tracking-tight sm:text-4xl">{trip.name}</h1><TripMetaEditor trip={trip} variant="hero" disabled={saveState === "conflict" || Boolean(action)} prepare={() => flushChanges()} onUpdated={applyMetaUpdate} /></div>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)] sm:text-base">{trip.destination_name || te("tripFallback")}{trip.start_date ? te("dateRange", { start: trip.start_date, end: trip.end_date ?? "" }) : ""}{Number(trip.total_price) > 0 ? (trip.price_status === "stale" ? te("stalePrice", { amount: twd.format(Number(trip.total_price)) }) : ` · ${twd.format(Number(trip.total_price))}`) : ""}</p>
          <p className="mt-2 text-xs text-[var(--muted)]">{aiCharge.status === "ready" ? te("aiChargeHelp", { charge: aiCharge.label }) : aiCharge.unavailableHelp}</p>
          {desktopMapVisible && trip.price_status !== "stale" && <div className="mt-3 max-w-xs"><PriceAlertButton resourceType="trip" resourceId={trip.id} currentPrice={Number(trip.total_price)} currency={trip.currency} returnPath={`/trips/${trip.id}`} /></div>}
        </div>
        <div className="grid grid-cols-2 gap-2 sm:flex sm:flex-wrap"><button type="button" onClick={() => setConfirmAction("reprice")} disabled={busy("reprice") || trip.mode === "manual" || repriceCharge.status !== "ready"} className="flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] bg-white/75 px-4 py-3 text-sm font-semibold disabled:opacity-40"><RefreshCw size={16} />{te("repriceButton", { charge: repriceCharge.label })}</button><button type="button" onClick={() => openAIPlanner("trip")} disabled={busy("ai") || aiCharge.status !== "ready"} className="flex min-h-11 items-center justify-center gap-2 rounded-xl border border-violet-300 bg-violet-50/90 px-4 py-3 text-sm font-semibold text-violet-900 disabled:opacity-40"><Sparkles size={16} />{te("aiPlanButton", { charge: aiCharge.label })}</button><button type="button" onClick={() => previewOptimization()} disabled={busy("preview", "apply")} className="flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--teal)] bg-white/75 px-4 py-3 text-sm font-semibold text-[var(--teal)] disabled:opacity-40">{action === "preview-all" ? <Loader2 size={16} className="animate-spin" /> : <RouteIcon size={16} />}{te("optimizeButton", { charge: optimizationCharge.label })}</button><button type="button" onClick={() => void flushChanges(true)} disabled={saveState === "saving"} className="flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white disabled:opacity-60"><Save size={16} />{te("saveChanges")}</button><button type="button" aria-expanded={toolsOpen} onClick={openTools} className="flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] bg-white/75 px-4 py-3 text-sm font-semibold"><Settings2 size={16} />{t("tools")}</button></div>
      </div>
    </section>
    {saveState === "conflict" && <div role="alert" className="mb-4 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="font-semibold">{te("conflictTitle")}</p><p className="mt-1 leading-6">{te("conflictBody")}</p><div className="mt-3 flex flex-wrap gap-2"><button type="button" onClick={() => void loadCloudVersion()} disabled={busy("conflict")} className="flex min-h-11 items-center gap-2 rounded-xl border border-amber-300 bg-white px-4 font-semibold disabled:opacity-50">{busy("conflict") && <Loader2 size={15} className="animate-spin" />}{te("loadCloud")}</button><button type="button" onClick={() => setConfirmAction("overwrite-conflict")} disabled={busy("conflict")} className="min-h-11 rounded-xl bg-amber-900 px-4 font-semibold text-white disabled:opacity-50">{te("keepLocal")}</button></div></div>}
    {trip.planning && <section aria-label={te("aiStatusLabel")} className={`mb-4 flex items-start gap-3 rounded-2xl border px-4 py-3 text-sm ${trip.planning.readiness === "partial" || trip.planning.readiness === "needs_setup" || trip.planning.status === "fallback" ? "border-amber-200 bg-amber-50 text-amber-950" : "border-violet-200 bg-violet-50 text-violet-950"}`}><span className="mt-0.5 grid h-8 w-8 shrink-0 place-items-center rounded-full bg-white/80"><Sparkles size={16} /></span><div className="min-w-0 flex-1"><p className="font-semibold">{trip.planning.readiness === "needs_setup" ? te("aiNeedsSetup") : trip.planning.status === "fallback" ? te("aiFallbackApplied") : trip.planning.readiness === "partial" ? te("aiPartialApplied") : te("aiApplied", { provider: aiProviderLabel(trip.planning.provider, te) })}</p><p className="mt-0.5 text-xs leading-5 opacity-75">{te("lastPlannedNote", { scope: trip.planning.scope === "day" && trip.planning.day_date ? te("lastPlannedDay", { day: trip.planning.day_date }) : te("lastPlannedTrip") })}</p>{trip.planning.warnings.length > 0 && <ul aria-label={te("aiWarningsLabel")} className="mt-2 grid gap-1 text-xs leading-5">{trip.planning.warnings.map((warning, index) => <li key={`${index}-${warning}`} className="flex gap-1.5"><TriangleAlert size={13} className="mt-0.5 shrink-0" aria-hidden />{warning}</li>)}</ul>}{(trip.planning.unscheduled_slots || []).length > 0 && <div className="mt-2.5"><p className="text-xs font-semibold">{te("unscheduledSlots")}</p><div className="mt-1.5 flex flex-wrap gap-1.5">{(trip.planning.unscheduled_slots || []).map((slot, index) => <button key={`${slot.date}-${slot.slot}-${index}`} type="button" onClick={() => setActiveDay(slot.date)} className="min-h-8 rounded-full border border-amber-300 bg-white/75 px-2.5 py-1 text-xs font-semibold">{slot.date.slice(5).replace("-", "/")} {te(`slot.${slot.slot}`)}</button>)}</div></div>}</div><button type="button" onClick={() => openAIPlanner(activeDay ? "day" : "trip")} className="min-h-10 shrink-0 rounded-xl bg-white/80 px-3 text-xs font-bold">{te("replan")}</button></section>}

    {trip.routing && ["queued", "processing"].includes(trip.routing.status) && <section aria-live="polite" className="mb-4 flex items-center gap-3 rounded-2xl border border-sky-200 bg-sky-50 px-4 py-3 text-sm text-sky-950"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-full bg-white"><Loader2 size={18} className="animate-spin text-sky-700" /></span><div className="min-w-0 flex-1"><p className="font-semibold">{te("routingTitle")}</p><p className="mt-0.5 text-xs opacity-75">{te("routingProgress", { completed: trip.routing.completed, total: trip.routing.total })}</p></div></section>}
    {allLogistics.length > 0 && <details className="planner-logistics-panel mb-4 px-4 py-3"><summary className="min-h-11 cursor-pointer py-2 text-sm font-bold">{te("logisticsSummary", { count: allLogistics.length })}</summary><p className="mb-3 text-xs leading-5 text-[var(--muted)]">{te("logisticsHint")}</p><div className="grid gap-2 pb-1 sm:grid-cols-2">{allLogistics.map((item) => <div key={item.id} className="rounded-xl bg-white px-3 py-2.5"><p className="text-xs font-semibold text-[var(--muted)]">{item.day_date} · {formatTime(item.start_time, locale, trip.timezone)}</p><p className="mt-1 text-sm font-bold">{item.title}</p>{item.location_name && <p className="mt-1 text-xs text-[var(--muted)]">{item.location_name}</p>}</div>)}</div></details>}

    <section className="planner-day-strip sticky z-30 -mx-4 mb-4 border-y border-[var(--line)] px-4 py-3 lg:top-0 lg:mx-0 lg:mb-5 lg:rounded-2xl lg:border"><div ref={dayScrollRef} className="planner-day-scroll flex gap-2 overflow-x-auto pb-1" aria-label={te("pickDayLabel")}>{days.map((day, index) => { const label = dayLabel(day, index, locale); const count = (groups.get(day) || []).filter((item) => isActiveRouteItem(item) && !item.system_role?.startsWith("hotel_")).length; const selected = activeDay === day; return <button key={day} ref={selected ? activeDayChipRef : undefined} type="button" aria-current={selected ? "date" : undefined} aria-pressed={selected} onClick={() => { const dayIds = new Set((groups.get(day) || []).filter(isActiveRouteItem).map((item) => item.id)); setActiveDay(day); setSelectedRoute(routes.find((route) => dayIds.has(route.from_item_id))); setRouteDrawerOpen(false); setRouteTarget(undefined); setReorderMode(false); }} className={`planner-day-chip min-h-14 min-w-[5.1rem] shrink-0 rounded-2xl border px-3 py-2 text-left ${selected ? "planner-day-chip-active" : ""}`}><span className="block text-[.65rem] font-semibold tracking-[.12em] opacity-75">{day === today ? te("today") : label.eyebrow}</span><span className="mt-0.5 block text-sm font-bold">{label.short} {label.weekday}</span><span className="block text-[.65rem] opacity-70">{te("arrangedCount", { count })}</span></button>; })}</div></section>

    {trip.destination_name && trip.start_date && <TripWeatherPanel tripId={trip.id} activeDay={activeDay} />}

    <section className="mb-5 hidden flex-col gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 lg:flex lg:flex-row lg:items-center lg:justify-between"><label className="flex min-h-11 items-center justify-between gap-3 text-sm font-semibold sm:justify-start">{te("routePreference")}<select aria-label={te("routePreference")} value={trip.route_preference || "FEWER_TRANSFERS"} onChange={(event) => updateRoutePreference(event.target.value as Trip["route_preference"])} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3"><option value="FEWER_TRANSFERS">{te("pref.fewerTransfers")}</option><option value="FASTEST">{te("pref.fastest")}</option><option value="LESS_WALKING">{te("pref.lessWalking")}</option></select></label><div className="flex flex-wrap items-center gap-2 text-sm">{trip.destination_country_code === "JP" && runtimeConfig.ekispert_enabled && <span className="rounded-full bg-indigo-50 px-3 py-2 text-xs font-semibold text-indigo-800">{te("provider.ekispert")}</span>}{trip.destination_country_code === "JP" && !runtimeConfig.ekispert_enabled && runtimeConfig.navitime_enabled && <span className="rounded-full bg-sky-50 px-3 py-2 text-xs font-semibold text-sky-800">{te("provider.navitime")}</span>}{trip.destination_country_code === "KR" && runtimeConfig.odsay_enabled && <span className="rounded-full bg-fuchsia-50 px-3 py-2 text-xs font-semibold text-fuchsia-800">{te("provider.odsay")}</span>}{trip.destination_country_code === "KR" && runtimeConfig.naver_directions_enabled && <span className="rounded-full bg-[#e8f8ee] px-3 py-2 text-xs font-semibold text-[#087a3f]">{te("provider.naverCar")}</span>}{runtimeConfig.google_routes_enabled && <span className="rounded-full bg-[var(--teal-soft)] px-3 py-2 text-xs font-semibold text-[var(--teal)]">{te("provider.google")}</span>}{!runtimeConfig.google_routes_enabled && !runtimeConfig.ekispert_enabled && !runtimeConfig.navitime_enabled && !runtimeConfig.odsay_enabled && !(trip.destination_country_code === "KR" && runtimeConfig.naver_directions_enabled) && <span className="rounded-full bg-amber-50 px-3 py-2 text-xs font-semibold text-amber-800">{te("provider.none")}</span>}<button type="button" onClick={() => void share()} className="flex min-h-11 items-center gap-2 rounded-xl px-3 font-semibold text-[var(--teal)]"><Link2 size={16} />{te(shareUrl ? "share.copy" : trip.share_enabled ? "share.rotate" : "share.create")}</button>{trip.share_enabled && <button type="button" onClick={() => setConfirmAction("revoke-share")} className="min-h-11 rounded-xl px-3 font-semibold text-red-700">{te("share.revoke")}</button>}</div>{shareUrl && <label className="flex min-w-0 items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm sm:max-w-sm"><input aria-label={te("share.linkLabel")} readOnly value={shareUrl} className="min-w-0 flex-1 bg-transparent outline-none" /><button type="button" aria-label={te("share.copy")} onClick={() => void navigator.clipboard?.writeText(shareUrl)} className="grid min-h-11 min-w-11 place-items-center"><Copy size={16} /></button></label>}</section>


    <div className={`mt-2 grid items-start gap-6 lg:mt-6 ${desktopMapVisible && selectedRoute ? "lg:grid-cols-[minmax(0,1.35fr)_minmax(320px,.65fr)]" : "lg:grid-cols-1"}`}>
      <section className="planner-day-panel rounded-[1.75rem] border border-[var(--line)] bg-white p-4 shadow-sm sm:p-6">
        <header className="mb-4 flex items-start justify-between gap-3 sm:mb-5">
          <div className="min-w-0"><p className="text-xs font-semibold tracking-[.16em] text-[var(--teal)]">{days.indexOf(activeDay) >= 0 ? `DAY ${days.indexOf(activeDay) + 1}` : "ITINERARY"}{activeDay === today ? te("todaySuffix") : ""}</p><h2 className="mt-1 text-xl font-bold sm:text-2xl"><span className="lg:hidden">{mobileDayHeading(activeDay, locale, te)}</span><span className="hidden lg:inline">{activeDay || te("noDate")}</span></h2><p className="planner-day-summary mt-1.5 text-xs font-semibold text-[var(--muted)]">{activeArrangementCount ? te("daySummary", { count: activeArrangementCount, duration: activeDurationMinutes ? te("daySummaryDuration", { duration: durationSummary(activeDurationMinutes, te) }) : "" }) : te("dayEmpty")}</p>{trip.cost?.by_day?.[activeDay] && <p className="mt-1 text-xs font-semibold text-[var(--teal)]">{t("costDayTotal", { amount: formatMoney(Number(trip.cost.by_day[activeDay]), trip.cost.currency) })}</p>}</div>
          <div className="flex shrink-0 items-center gap-2"><button type="button" aria-label={te("computeDayRoutes")} onClick={() => void computeRoutes(activeDay, activeDay === today)} disabled={busy("route", "departure-time") || activeRouteRows.length < 2} className="planner-secondary-button flex">{action === `route-${activeDay}` ? <Loader2 size={17} className="animate-spin" /> : <RouteIcon size={17} />}<span className="hidden sm:inline">{te("routeShort")}</span></button><button type="button" aria-label={te(reorderMode ? "sortDone" : "sortItems")} aria-pressed={reorderMode} onClick={() => setReorderMode((value) => !value)} disabled={activeRows.filter((item) => !item.system_role).length < 2} className="planner-secondary-button flex md:hidden">{reorderMode ? <Check size={17} /> : <GripVertical size={17} />}<span className="planner-sort-label">{te(reorderMode ? "done" : "sort")}</span></button>{desktopMapVisible && <><button type="button" onClick={() => void previewOptimization(activeDay)} disabled={busy("preview", "apply") || activeRouteRows.length < 2} className="hidden min-h-11 items-center justify-center gap-1.5 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold disabled:opacity-40 md:flex">{action === `preview-${activeDay}` ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}{te("optimize")}</button><button type="button" onClick={() => add(activeDay)} disabled={!activeDay} className="hidden min-h-11 items-center justify-center gap-1.5 rounded-xl bg-[var(--paper)] px-3 text-sm font-semibold disabled:opacity-40 md:flex"><Plus size={16} />{te("addShort")}</button></>}</div>
        </header>
        {activeRouteRows.length > 1 && <section className="route-day-settings mb-4"><div><p className="text-xs font-semibold text-[var(--muted)]">{te("dayTravelTitle")}</p><div className="mt-2 flex gap-1.5" role="radiogroup" aria-label={te("dayTravelLabel")}>{([['transit', TrainFront], ['walk', Footprints], ['drive', CarFront]] as const).map(([value, Icon]) => <button key={value} type="button" role="radio" aria-checked={activeTravelMode === value} onClick={() => void computeRoutes(activeDay, false, { mode: value })} disabled={busy("route")} className={`route-day-mode ${activeTravelMode === value ? "route-day-mode-active" : ""}`}><Icon size={15} /><span>{te(`mode.${value}`)}</span></button>)}</div></div><label className="shrink-0 text-xs font-semibold text-[var(--muted)]">{te("transferBuffer")}<select aria-label={te("bufferLabel")} value={activeTravelBuffer} onChange={(event) => void computeRoutes(activeDay, false, { buffer: Number(event.target.value) })} disabled={busy("route")} className="mt-2 block min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-bold text-[var(--ink)]">{[0, 5, 10, 15, 30].map((minutes) => <option key={minutes} value={minutes}>{te("minutesShort", { minutes })}</option>)}</select></label></section>}
        {activeDay && <details open={Boolean(trip.day_notes?.[activeDay])} className="planner-day-note mb-4"><summary className="flex min-h-11 cursor-pointer list-none items-center gap-2 text-sm font-semibold"><NotebookPen size={16} className="text-[var(--teal)]" />{trip.day_notes?.[activeDay] ? t("dayNotesLabel") : t("dayNotesAdd")}</summary><div className="mt-2"><TripNoteField label={t("dayNotesLabel")} placeholder={t("dayNotesPlaceholder")} value={trip.day_notes?.[activeDay] || ""} onSave={(next) => saveDayNotes(activeDay, next)} /></div></details>}
        {staleDays.has(activeDay) && missingLegs > 0 && <button type="button" onClick={() => void computeRoutes(activeDay)} className="mb-4 flex min-h-11 w-full items-center justify-between gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-left text-sm text-amber-950"><span className="flex items-center gap-2"><CircleAlert size={17} />{t("routes.missingLegs", { count: missingLegs })}</span><span className="shrink-0 font-semibold">{t("routes.computeMissing")}</span></button>}
        {reorderMode && <div className="mb-3 flex min-h-12 items-center gap-2 rounded-2xl bg-[var(--teal-soft)] px-4 py-3 text-sm font-semibold text-[var(--teal-dark)] md:hidden"><GripVertical size={17} /><span>{te("reorderHint")}</span></div>}
        {days.length === 0 && <div className="app-empty-state mb-4"><CalendarDays size={22} aria-hidden /><p className="font-semibold">{t("noDatesTitle")}</p><p className="text-xs leading-5">{t("noDatesBody")}</p><button type="button" onClick={() => router.push("/trips")} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-4 text-sm font-semibold text-[var(--teal)]">{t("backToTrips")}</button></div>}
        <ol className="planner-timeline space-y-3">{activeDisplayRows.map((item, index) => {
          const routeIndex = activeRouteRows.findIndex((row) => row.id === item.id);
          const nextRouteItem = routeIndex >= 0 ? activeRouteRows[routeIndex + 1] : undefined;
          const nextItem = nextRouteItem || activeDisplayRows.slice(index + 1).find((row) => !row.is_skipped);
          const segment = nextRouteItem ? routes.find((route) => route.from_item_id === item.id && route.to_item_id === nextRouteItem.id) : undefined;
          const routeBlocker = nextRouteItem || !nextItem
            ? undefined
            : [item, nextItem].find((row) => !isActiveRouteItem(row));
          const needsSetup = routeBlocker
            ? routeBlocker.system_role?.startsWith("hotel_") ? "lodging" as const : "location" as const
            : undefined;
          const itemConflict = trip.routing?.conflicts?.find((conflict) => conflict.item_id === item.id);
          const catalogLocation = ["hotspot_catalog", "food_merchant_catalog"].includes(item.location_source || "")
            && item.latitude != null
            && item.longitude != null;
          const itemLocationConfirmed = item.location_source === "confirmed"
            || ((catalogLocation || ["google_places", "naver_local"].includes(item.location_source || "")) && item.data.needs_place_confirmation !== true);
          const autoLocation = item.location_source?.endsWith("_auto");
          const locationStatus = itemLocationConfirmed
            ? te("location.confirmed")
            : autoLocation ? te("location.auto", { provider: item.location_provider === "naver_local" || item.location_source === "naver_local_auto" ? "NAVER" : "Google" }) : te("location.unset");
          const marker = item.system_role ? "•" : activeDisplayRows.slice(0, index + 1).filter((row) => !row.system_role).length;
          const projectedStart = chainedStarts.get(item.id);
          const chainedTime = projectedStart
            ? te("chained", { kind: te(projectedStart.estimated ? "chainedApprox" : "chainedExpected"), time: formatTime(projectedStart.start, locale, trip.timezone) })
            : te("chainedPending");
          return <li id={`trip-item-${item.id}`} key={item.id} className={`planner-enter relative ${isFlightAnchor(item) ? "" : "pl-9"}`} style={{ "--planner-index": index } as CSSProperties}>{!reorderMode && !isFlightAnchor(item) && !item.system_role && <button type="button" aria-label={t("insertBefore", { title: item.title || t("insertFallback") })} onClick={() => add(activeDay, item.position)} className="planner-insert-point"><span className="planner-insert-line" aria-hidden="true" /><span className="planner-insert-plus"><Plus size={14} /></span><span className="planner-insert-line" aria-hidden="true" /></button>}{!isFlightAnchor(item) && <span aria-hidden="true" className="planner-timeline-marker absolute top-6 z-10">{marker}</span>}{isFlightAnchor(item) ? <FlightAnchorCard item={item} busy={action === `flight-${item.system_role === "outbound_flight" ? "outbound" : "return"}`} onEdit={() => openFlightEditor(item)} /> : item.system_role ? <SystemItineraryCard item={item} locale={locale} timezone={trip.timezone} busy={action === `skip-${item.id}`} routeStale={!item.fixed_time && !routes.some((route) => route.to_item_id === item.id)} chainedStart={projectedStart} departureTime={trip.schedule_defaults?.day_start_time || defaultSchedule.day_start_time} departureBusy={action === "departure-time"} onDepartureTimeChange={(value) => void saveDepartureTime(value)} onEdit={() => item.system_role?.startsWith("hotel_") ? openStayFlow() : setEditingId(item.id)} onSkip={item.system_role === "lunch" || item.system_role === "dinner" ? () => void toggleMealSkip(item) : undefined} /> : <article draggable={desktopMapVisible} onDragStart={() => setDragged(item.id)} onDragOver={(event) => event.preventDefault()} onDrop={() => drop(item.id)} className={`planner-itinerary-card group p-4 ${reorderMode ? "planner-itinerary-card-reordering" : ""} ${recentItemId === item.id ? "planner-itinerary-card-new" : ""}`}><div className="flex items-start gap-3"><span className="hidden cursor-grab pt-1 text-[var(--muted)] lg:block" title={te("dragToSort")}><GripVertical size={19} /></span><button type="button" onClick={() => setEditingId(item.id)} className="min-w-0 flex-1 text-left"><div className="flex flex-wrap items-center gap-2"><span className="planner-time-badge">{item.fixed_time ? te("fixedTimeAt", { time: formatTime(item.start_time, locale, trip.timezone) }) : chainedTime}</span>{item.duration_minutes ? <span className="text-xs text-[var(--muted)]">{te("stayMinutes", { minutes: item.duration_minutes })}</span> : null}{item.data.generated_by === "ai_planner" && <span className="rounded-full bg-violet-100 px-2 py-1 text-[.68rem] font-semibold text-violet-800">{te("aiSuggested")}</span>}{item.locked && <span className="rounded-full bg-amber-50 px-2 py-1 text-[.68rem] font-semibold text-amber-800">{te("locked")}</span>}</div><h3 className="mt-2 line-clamp-2 text-lg font-bold leading-snug tracking-tight">{item.title}</h3>{originalItemName(item) && <p className="mt-0.5 truncate text-sm text-[var(--muted)]" lang={item.names?.title?.original_locale}>{originalItemName(item)}</p>}<p className="mt-1 flex items-start gap-1.5 text-sm leading-5 text-[var(--muted)]"><MapPin size={15} className="mt-0.5 shrink-0" />{item.location_name || te("noLocation")}</p><span className={`mt-2 inline-flex rounded-full px-2 py-1 text-[.68rem] font-semibold ${itemLocationConfirmed ? "bg-emerald-50 text-emerald-800" : autoLocation ? "bg-sky-50 text-sky-800" : "bg-amber-50 text-amber-800"}`}>{locationStatus}{autoLocation ? te("location.tapToFix") : ""}</span>{itemConflict && <p className="mt-2 rounded-xl bg-red-50 px-3 py-2 text-xs font-semibold leading-5 text-red-800">{te("conflictLate", { scheduled: formatTime(itemConflict.scheduled_start_time, locale, trip.timezone), projected: formatTime(itemConflict.projected_start_time, locale, trip.timezone), minutes: itemConflict.late_minutes })}</p>}{item.notes && <p className="mt-2 line-clamp-2 text-xs leading-5 text-[var(--muted)]">{item.notes}</p>}</button><div className={`flex shrink-0 items-center gap-1 ${reorderMode ? "flex-col md:flex-row" : ""}`}><button type="button" aria-label={te("moveUp", { title: item.title })} onClick={() => move(item.id, -1)} disabled={movable.findIndex((row) => row.id === item.id) <= 0} className={`${reorderMode ? "grid" : "hidden"} planner-reorder-button md:grid`}><ArrowUp size={18} /></button><button type="button" aria-label={te("moveDown", { title: item.title })} onClick={() => move(item.id, 1)} disabled={movable.findIndex((row) => row.id === item.id) === movable.length - 1} className={`${reorderMode ? "grid" : "hidden"} planner-reorder-button md:grid`}><ArrowDown size={18} /></button><button type="button" aria-label={te("editItem", { title: item.title })} onClick={() => setEditingId(item.id)} className={`${reorderMode ? "hidden" : "grid"} min-h-11 min-w-11 place-items-center rounded-xl bg-[var(--teal-soft)] text-[var(--teal)] md:grid`}><Edit3 size={17} /></button></div></div></article>}{nextItem && !item.is_skipped && <div className="py-2 pl-2"><RouteTimelineLink segment={segment} nextTitle={nextItem.title} loading={!needsSetup && ["queued", "processing"].includes(trip.routing?.status || "")} stale={segment?.status === "stale"} timezone={trip.timezone} needsSetup={needsSetup} onClick={() => { if (routeBlocker) { if (routeBlocker.system_role?.startsWith("hotel_")) openStayFlow(); else setEditingId(routeBlocker.id); return; } setRouteTarget({ fromItemId: item.id, toItemId: nextItem.id }); setSelectedRoute(segment); setRouteDrawerOpen(true); }} /></div>}</li>;
        })}</ol>
        {trip.routing && ["partial", "failed", "unavailable", "needs_locations"].includes(trip.routing.status) && routeWarnings.length ? <details className="mt-5 rounded-2xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-950"><summary className="flex min-h-11 cursor-pointer list-none items-center justify-between gap-3 font-semibold"><span className="flex items-center gap-2"><TriangleAlert size={17} />{te("routeIssuesTitle")}</span><span className="rounded-full bg-white/80 px-2.5 py-1 text-xs">{te("routeIssuesCount", { count: routeWarnings.length })}</span></summary><div className="mt-2 grid gap-2 border-t border-amber-200/70 pt-3">{routeWarnings.map((warning) => <p key={warning} className="rounded-xl bg-white/70 px-3 py-2 text-xs leading-5">{warning}</p>)}<div className="flex flex-wrap gap-2">{!lodgingReady && <button type="button" onClick={openStayFlow} className="min-h-11 rounded-xl bg-amber-900 px-4 text-xs font-bold text-white">{te("setMainHotel")}</button>}{routeNeedsLocations && unresolvedRouteItems[0] && <button type="button" onClick={() => setEditingId(unresolvedRouteItems[0].id)} className="min-h-11 rounded-xl bg-white px-4 text-xs font-bold text-[var(--teal)]">{te("pickOfficialPlace")}</button>}{!routeNeedsLocations && activeRouteRows.length > 1 && <button type="button" onClick={() => void computeRoutes(activeDay, true)} className="min-h-11 rounded-xl bg-white px-4 text-xs font-bold text-[var(--teal)]">{te("retryRoutes")}</button>}</div></div></details> : null}
      </section>
      {desktopMapVisible && selectedRoute && <aside className="min-w-0 space-y-4 lg:sticky lg:top-24 lg:self-start"><RouteSegmentCard segment={selectedRoute} selected defaultExpanded timezone={trip.timezone} /></aside>}
    </div>

    <ItineraryDiff trip={trip} activeDay={activeDay} disabled={saveState === "conflict" || Boolean(action)} prepare={() => flushChanges(false)} onError={setError} onApplied={(updated, scope, dayDate) => { replaceTrip(updated); setRoutes([]); setSelectedRoute(undefined); closeRouteDrawer(); setStaleDays(new Set(scope === "day" && dayDate ? [dayDate] : days)); revisionRef.current = 0; persistedRevisionRef.current = 0; setRevision(0); updateSaveState("saved"); try { window.localStorage.removeItem(draftKey); } catch { /* storage can be blocked */ } setNotice(tTrips("intent.applied")); }} />

    <div role="toolbar" aria-label={te("quickActions")} className="planner-mobile-bar fixed inset-x-0 bottom-0 z-40 px-3 pt-3 lg:hidden"><div className={`planner-mobile-dock mx-auto grid max-w-lg items-center gap-2 ${reorderMode ? "grid-cols-[auto_1fr]" : "grid-cols-[auto_1fr_1.2fr]"}`}><button type="button" aria-live="polite" aria-label={saveState === "offline" ? te("saveFailedRetry") : saveLabel} onClick={() => { if (saveState === "offline") void flushChanges(true); }} disabled={saveState !== "offline"} className={`planner-save-status ${saveState === "offline" ? "planner-save-status-error" : ""} ${saveState === "dirty" || saveState === "saving" ? "planner-save-status-pending" : ""}`}>{saveIcon}<span className="sr-only">{saveLabel}</span></button>{reorderMode ? <button type="button" aria-label={t("doneSorting")} onClick={() => setReorderMode(false)} className="planner-dock-button planner-dock-button-primary"><Check size={18} />{t("doneSorting")}</button> : <><button type="button" aria-label={te("addItem")} onClick={() => add(activeDay)} disabled={!activeDay} className="planner-dock-button planner-dock-button-secondary"><Plus size={18} /><span className="planner-add-label-long">{te("addItem")}</span><span className="planner-add-label-short">{te("addShort")}</span></button><button type="button" aria-label={te("aiPlanButton", { charge: aiCharge.label })} onClick={() => openAIPlanner(activeDay ? "day" : "trip")} disabled={busy("ai") || aiCharge.status !== "ready"} className="planner-dock-button planner-dock-button-primary"><Sparkles size={18} />{te("aiDock", { charge: aiCharge.label })}</button></>}</div></div>

    {(error || notice || optimizeBlock) && <div className="planner-toast-stack fixed left-1/2 z-[80] w-[min(92vw,38rem)] -translate-x-1/2" aria-live="polite">{error && <div role="alert" className="flex items-start justify-between gap-3 rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-900 shadow-lg"><span className="min-w-0 flex-1">{error}{saveState === "offline" && <button type="button" onClick={() => void flushChanges(true)} className="ml-3 font-bold underline">{te("retry")}</button>}</span><button type="button" aria-label={t("dismissError")} onClick={() => setError(undefined)} className="grid h-11 w-11 shrink-0 place-items-center rounded-xl text-red-900/70 hover:bg-red-100"><X size={16} /></button></div>}{notice && <div className="mt-2 flex items-center justify-between gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900 shadow-lg"><span className="flex items-center gap-2"><Check size={16} />{notice}</span>{undoItem && <button type="button" onClick={undoDelete} className="flex min-h-11 shrink-0 items-center gap-1 font-bold"><Undo2 size={16} />{te("undo")}</button>}</div>}{optimizeBlock && <div role="status" className="mt-2 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950 shadow-lg"><p className="font-semibold">{te("optimizeTooMany", { day: optimizeBlock.label, count: optimizeBlock.days.reduce((total, entry) => total + entry.excess, 0) + optimizeBlock.limit, limit: optimizeBlock.limit })}</p><p className="mt-1 text-xs leading-5">{te("optimizeTooManyHint", { count: optimizeBlock.days.reduce((total, entry) => total + entry.excess, 0) })}</p><div className="mt-3 flex flex-wrap gap-2"><button type="button" onClick={lockCrowdedDays} className="flex min-h-11 items-center gap-1.5 rounded-xl bg-amber-900 px-4 text-sm font-semibold text-white">{te("optimizeLockExtras", { count: optimizeBlock.days.reduce((total, entry) => total + entry.excess, 0) })}</button><button type="button" onClick={() => setOptimizeBlock(undefined)} className="flex min-h-11 items-center rounded-xl px-4 text-sm font-semibold">{t("dismissError")}</button></div></div>}</div>}

    <PlannerOverlay open={aiMenuOpen} onClose={() => { if (!busy("ai")) { setAIMenuOpen(false); setAIPreview(undefined); } }} title={te(aiPreview ? "aiPreviewTitle" : "aiTitle")} description={aiPreview ? te("aiPreviewDescription") : te("aiDescription", { charge: aiCharge.label })} size={aiPreview ? "wide" : "default"} footer={<div className="flex gap-3"><button type="button" onClick={() => { if (aiPreview) setAIPreview(undefined); else setAIMenuOpen(false); }} disabled={busy("ai")} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold disabled:opacity-40">{te(aiPreview ? "backAdjust" : "cancel")}</button><button type="button" onClick={() => void (aiPreview ? applyAIItinerary() : generateAIItinerary(aiScope))} disabled={busy("ai") || (!aiPreview && ((aiScope === "day" && !activeDay) || aiCharge.status !== "ready")) || (aiPreview?.readiness.status === "needs_setup")} className="flex min-h-12 flex-[1.5] items-center justify-center gap-2 rounded-xl bg-violet-700 px-4 font-semibold text-white disabled:opacity-45">{action?.startsWith("ai-") ? <Loader2 size={17} className="animate-spin" /> : <Sparkles size={17} />}{aiPreview ? te("applyPlanCharge", { charge: aiPreview.planning.provider === "catalog" ? te("noCharge") : aiCharge.label }) : te("generatePreview")}</button></div>}>
      {!aiPreview ? <div className="space-y-5">
        <div role="radiogroup" aria-label={te("aiScopeLabel")} className="grid gap-3 sm:grid-cols-2">
          <button type="button" role="radio" aria-checked={aiScope === "day"} onClick={() => setAIScope("day")} disabled={!activeDay || busy("ai")} className={`min-h-36 rounded-2xl border p-4 text-left transition disabled:opacity-45 ${aiScope === "day" ? "border-violet-500 bg-violet-50 text-violet-950 ring-2 ring-violet-100" : "border-[var(--line)] bg-white"}`}><span className="flex items-center justify-between gap-3"><span className="grid h-10 w-10 place-items-center rounded-xl bg-white text-violet-700"><CalendarDays size={20} /></span><span className={`h-5 w-5 rounded-full border-2 ${aiScope === "day" ? "border-violet-600 bg-violet-600 shadow-[inset_0_0_0_4px_white]" : "border-[var(--line)]"}`} /></span><strong className="mt-3 block">{te("scopeDay")}</strong><span className={`mt-1 block text-xs leading-5 ${aiScope === "day" ? "text-violet-700" : "text-[var(--muted)]"}`}>{activeDay ? te("scopeDayHint", { day: mobileDayHeading(activeDay, locale, te), count: activeArrangementCount }) : te("pickDay")}</span></button>
          <button type="button" role="radio" aria-checked={aiScope === "trip"} onClick={() => setAIScope("trip")} disabled={busy("ai")} className={`min-h-36 rounded-2xl border p-4 text-left transition disabled:opacity-45 ${aiScope === "trip" ? "border-violet-500 bg-violet-50 text-violet-950 ring-2 ring-violet-100" : "border-[var(--line)] bg-white"}`}><span className="flex items-center justify-between gap-3"><span className="grid h-10 w-10 place-items-center rounded-xl bg-white text-violet-700"><Sparkles size={20} /></span><span className={`h-5 w-5 rounded-full border-2 ${aiScope === "trip" ? "border-violet-600 bg-violet-600 shadow-[inset_0_0_0_4px_white]" : "border-[var(--line)]"}`} /></span><strong className="mt-3 block">{te("scopeTrip")}</strong><span className={`mt-1 block text-xs leading-5 ${aiScope === "trip" ? "text-violet-700" : "text-[var(--muted)]"}`}>{te("scopeTripHint", { count: days.length })}</span></button>
        </div>
        <section aria-label={te("preflightTitle")} className="rounded-2xl border border-[var(--line)] bg-white p-4"><div className="flex items-center justify-between gap-3"><p className="font-semibold">{te("preflightTitle")}</p><span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-1 text-xs font-bold text-[var(--teal)]">{te("previewFirst")}</span></div><ul className="mt-3 grid gap-2 text-xs"><li className="flex items-center gap-2"><span className={`h-2 w-2 rounded-full ${lodgingReady ? "bg-emerald-500" : "bg-amber-500"}`} />{te(lodgingReady ? "preflight.lodgingOk" : "preflight.lodgingMissing")}</li><li className="flex items-center gap-2"><span className={`h-2 w-2 rounded-full ${outboundReady ? "bg-emerald-500" : "bg-amber-500"}`} />{te(outboundReady ? "preflight.arrivalOk" : "preflight.arrivalMissing")}</li><li className="flex items-center gap-2"><span className={`h-2 w-2 rounded-full ${returnReady ? "bg-emerald-500" : "bg-amber-500"}`} />{te(returnReady ? "preflight.departureOk" : "preflight.departureMissing")}</li></ul>{!lodgingReady && <button type="button" onClick={() => { setAIMenuOpen(false); openStayFlow(); }} className="mt-3 min-h-11 rounded-xl border border-[var(--line)] bg-white px-4 text-xs font-bold text-[var(--teal)]">{te("setHotelFirst")}</button>}</section>
        <section className="rounded-2xl bg-[var(--paper)] p-4 text-sm leading-6"><p className="font-semibold">{te("keepTitle")}</p><ul className="mt-2 grid gap-1.5 text-xs text-[var(--muted)]"><li>{te("keep.manual")}</li><li>{te("keep.locked")}</li><li>{te("keep.otherDays")}</li></ul></section>
        <button type="button" onClick={() => { setAIMenuOpen(false); void previewOptimization(aiScope === "day" ? activeDay : undefined); }} disabled={busy("preview", "apply") || (aiScope === "day" ? activeRouteRows.length < 2 : tripRouteItemCount < 2)} className="flex min-h-12 w-full items-center justify-between gap-3 rounded-xl border border-[var(--line)] bg-white px-4 text-left text-sm disabled:opacity-40"><span><strong className="block">{te("reorderOnlyTitle")}</strong><span className="mt-0.5 block text-xs font-normal text-[var(--muted)]">{te("reorderOnlyHint")}</span></span><RouteIcon size={18} className="shrink-0 text-[var(--teal)]" /></button>
      </div> : <div className="space-y-5"><section className={`rounded-2xl border p-4 ${aiPreview.readiness.status === "ready" || aiPreview.readiness.status === "fallback" ? "border-emerald-200 bg-emerald-50" : "border-amber-200 bg-amber-50"}`}><div className="flex flex-wrap items-center justify-between gap-2"><div><p className="font-bold">{aiPreview.readiness.status === "needs_setup" ? te("preview.needsSetup") : aiPreview.readiness.status === "partial" ? te("preview.partial") : aiPreview.planning.provider === "catalog" ? te("preview.catalog") : te("preview.provider", { provider: aiProviderLabel(aiPreview.planning.provider, te) })}</p><p className="mt-1 text-xs text-[var(--muted)]">{te("preview.counts", { items: aiPreview.readiness.exact_item_count, pairs: aiPreview.routing_summary.eligible_pairs })}</p></div><span className="rounded-full bg-white px-3 py-1.5 text-xs font-bold">{te("preview.candidates", { hotspots: aiPreview.readiness.hotspot_candidate_count, merchants: aiPreview.readiness.merchant_candidate_count })}</span></div></section>{aiPreview.readiness.assumptions.length > 0 && <section className="rounded-2xl bg-[var(--paper)] p-4"><p className="text-sm font-bold">{te("preview.assumptions")}</p><ul className="mt-2 grid gap-1.5 text-xs leading-5 text-[var(--muted)]">{aiPreview.readiness.assumptions.map((assumption) => <li key={assumption}>• {assumption}</li>)}</ul></section>}<div className="grid gap-3 sm:grid-cols-2">{aiPreview.days.map((day, index) => <section key={day.date} className="rounded-2xl border border-[var(--line)] bg-white p-4"><div className="flex items-center justify-between"><div><p className="text-[.65rem] font-bold tracking-[.14em] text-violet-700">DAY {days.indexOf(day.date) >= 0 ? days.indexOf(day.date) + 1 : index + 1}</p><h3 className="mt-1 font-bold">{mobileDayHeading(day.date, locale, te)}</h3><p className="mt-1 text-xs text-[var(--muted)]">{day.label}</p></div><span className="rounded-full bg-violet-50 px-2.5 py-1 text-xs font-semibold text-violet-800">{te("preview.itemsCount", { count: day.items.length })}</span></div><ol className="mt-3 grid gap-2">{day.items.map((item) => <li key={item.id} className="flex gap-3 rounded-xl bg-[var(--paper)] px-3 py-2.5"><span className="shrink-0 text-xs font-bold text-[var(--teal)]">{formatTime(item.start_time, locale, trip.timezone)}</span><span className="min-w-0 flex-1"><strong className="block truncate text-sm">{item.title}</strong><span className="mt-0.5 block truncate text-xs text-[var(--muted)]">{item.location_name}</span><span className="mt-1 block text-[.68rem] font-semibold text-[var(--teal)]">{te("stayMinutes", { minutes: item.duration_minutes || 60 })}</span></span></li>)}</ol>{day.items.length === 0 && <p className="mt-3 rounded-xl bg-amber-50 px-3 py-3 text-xs text-amber-900">{te("preview.dayEmpty")}</p>}</section>)}</div>{aiPreview.unscheduled_slots.length > 0 && <details className="rounded-2xl border border-amber-200 bg-amber-50 p-4"><summary className="min-h-8 cursor-pointer text-sm font-bold">{te("preview.unscheduled", { count: aiPreview.unscheduled_slots.length })}</summary><ul className="mt-2 grid gap-1 text-xs text-amber-950">{aiPreview.unscheduled_slots.map((slot, index) => <li key={`${slot.date}-${slot.slot}-${index}`}>• {slot.date} · {te(`slot.${slot.slot}`)}</li>)}</ul></details>}</div>}
    </PlannerOverlay>

    <PlannerOverlay open={toolsOpen} onClose={() => setToolsOpen(false)} title={te("toolsTitle")} description={te("toolsDescription")}>
      <div className="space-y-4">
        <TripMetaEditor trip={trip} variant="tools" disabled={saveState === "conflict" || Boolean(action)} prepare={() => flushChanges()} onUpdated={(updated) => { applyMetaUpdate(updated); setToolsOpen(false); }} />
        <section className="planner-tool-card">
          <div className="mb-3"><h3 className="font-bold">{te("calendarTitle")}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{te("calendarHint")}</p></div>
          <a href={`/api/travel/trips/${trip.id}/export.ics`} download className="flex min-h-11 w-fit items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-4 text-sm font-semibold"><CalendarPlus size={16} />{te("calendarDownload")}</a>
        </section>
        <section className="planner-tool-card">
          <div className="mb-3"><h3 className="font-bold">{t("notesTitle")}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("notesHint")}</p></div>
          <TripNoteField label={t("notesTitle")} placeholder={t("notesPlaceholder")} rows={4} value={trip.notes || ""} onSave={saveTripNotes} />
        </section>
        <section className="planner-tool-card">
          <div className="mb-3"><h3 className="font-bold">{t("costTitle")}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("costHint")}</p></div>
          <TripCostPanel
            trip={trip}
            days={days}
            activeDay={activeDay}
            onSaveBudget={saveBudget}
            onSaveCurrency={saveCostCurrency}
            onAdd={addExpense}
            onDelete={(id) => deleteExpense(id)}
            onSeed={seedExpenses}
          />
        </section>
        <section className="planner-tool-card">
          <div className="mb-3"><h3 className="font-bold">{te("themeTitle")}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{te("themeHint")}</p></div>
          <div className="grid grid-cols-2 gap-2" role="radiogroup" aria-label={te("themeTitle")}>
            {plannerThemes.map((theme) => <button key={theme.id} type="button" role="radio" aria-checked={plannerTheme === theme.id} onClick={() => selectPlannerTheme(theme.id)} className={`planner-theme-option ${plannerTheme === theme.id ? "planner-theme-option-active" : ""}`}><span className="flex gap-1.5" aria-hidden="true">{theme.colors.map((color) => <span key={color} className="planner-theme-swatch" style={{ backgroundColor: color }} />)}</span><strong className="mt-2 block text-sm">{te(`theme.${theme.id}.name`)}</strong><span className="mt-0.5 block text-[.68rem] text-[var(--muted)]">{te(`theme.${theme.id}.description`)}</span>{plannerTheme === theme.id && <Check size={16} className="planner-theme-check" />}</button>)}
          </div>
        </section>
        <section className="planner-tool-card">
          <div className="mb-3"><h3 className="font-bold">{te("scheduleTitle")}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{te("scheduleHint")}</p></div>
          <fieldset className="mb-3 rounded-xl border border-[var(--line)] bg-[var(--paper)]/60 p-3"><legend className="px-1 text-sm font-bold">{te("leaveHotel")}</legend><label className="text-xs font-semibold">{te("time")}<input type="time" aria-label={te("dailyDepartureLabel")} value={scheduleDraft.day_start_time} onChange={(event) => setScheduleDraft((current) => ({ ...current, day_start_time: event.target.value }))} className={fieldClass} /></label><p className="mt-2 text-xs leading-5 text-[var(--muted)]">{te("leaveHotelHint")}</p></fieldset>
          <div className="grid gap-3 sm:grid-cols-2">
            <fieldset className="rounded-xl border border-amber-200 bg-amber-50/60 p-3"><legend className="px-1 text-sm font-bold text-amber-950">{te("slot.lunch")}</legend><div className="grid grid-cols-2 gap-2"><label className="text-xs font-semibold">{te("time")}<input type="time" value={scheduleDraft.lunch_time} onChange={(event) => setScheduleDraft((current) => ({ ...current, lunch_time: event.target.value }))} className={fieldClass} /></label><label className="text-xs font-semibold">{te("stay")}<select value={scheduleDraft.lunch_duration_minutes} onChange={(event) => setScheduleDraft((current) => ({ ...current, lunch_duration_minutes: Number(event.target.value) }))} className={fieldClass}>{[30, 60, 90, 120, 150, 180].map((minutes) => <option key={minutes} value={minutes}>{te("minutesShort", { minutes })}</option>)}</select></label></div></fieldset>
            <fieldset className="rounded-xl border border-orange-200 bg-orange-50/60 p-3"><legend className="px-1 text-sm font-bold text-orange-950">{te("slot.dinner")}</legend><div className="grid grid-cols-2 gap-2"><label className="text-xs font-semibold">{te("time")}<input type="time" value={scheduleDraft.dinner_time} onChange={(event) => setScheduleDraft((current) => ({ ...current, dinner_time: event.target.value }))} className={fieldClass} /></label><label className="text-xs font-semibold">{te("stay")}<select value={scheduleDraft.dinner_duration_minutes} onChange={(event) => setScheduleDraft((current) => ({ ...current, dinner_duration_minutes: Number(event.target.value) }))} className={fieldClass}>{[30, 60, 90, 120, 150, 180].map((minutes) => <option key={minutes} value={minutes}>{te("minutesShort", { minutes })}</option>)}</select></label></div></fieldset>
          </div>
          <button type="button" onClick={() => void saveScheduleDefaults()} disabled={busy("schedule-defaults") || Boolean(scheduleOrderError)} className="mt-3 flex min-h-11 w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 text-sm font-bold text-white disabled:opacity-45">{action === "schedule-defaults" ? <Loader2 size={16} className="animate-spin" /> : <Clock3 size={16} />}{te("applyAllDays")}</button>
          {scheduleOrderError && <p className="mt-2 text-xs font-semibold text-red-700">{scheduleOrderError}</p>}
        </section>
        <section className="planner-tool-card">
          <div className="mb-3 flex items-center justify-between gap-3"><div><p className="font-bold">{te("routePreference")}</p><p className="mt-1 text-xs text-[var(--muted)]">{te("preferenceHint")}</p></div><span className="rounded-full bg-[var(--teal-soft)] px-3 py-1.5 text-xs font-semibold text-[var(--teal)]">{trip.destination_country_code === "JP" ? runtimeConfig.ekispert_enabled ? te("providerBadge.ekispert") : runtimeConfig.navitime_enabled ? te("providerBadge.navitime") : te("providerBadge.jpNone") : trip.destination_country_code === "KR" ? runtimeConfig.odsay_enabled ? te("providerBadge.odsay") : runtimeConfig.naver_directions_enabled ? te("providerBadge.naverCar") : te("providerBadge.krNone") : runtimeConfig.google_routes_enabled ? "Google Maps" : te("providerBadge.none")}</span></div>
          <div className="grid grid-cols-3 gap-2" role="group" aria-label={te("routePreference")}>{([['FEWER_TRANSFERS', 'pref.fewerTransfers'], ['FASTEST', 'pref.fastestShort'], ['LESS_WALKING', 'pref.lessWalking']] as const).map(([value, labelKey]) => <button key={value} type="button" aria-pressed={(trip.route_preference || "FEWER_TRANSFERS") === value} onClick={() => updateRoutePreference(value)} className={`min-h-11 rounded-xl border px-2 text-sm font-semibold ${(trip.route_preference || "FEWER_TRANSFERS") === value ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-white"}`}>{te(labelKey)}</button>)}</div>
        </section>
        <section className="planner-tool-card grid gap-2">
          <button type="button" onClick={() => { setToolsOpen(false); setConfirmAction("reprice"); }} disabled={busy("reprice") || trip.mode === "manual" || repriceCharge.status !== "ready"} className="planner-tool-row"><span className="planner-tool-icon"><RefreshCw size={18} /></span><span className="min-w-0 flex-1 text-left"><strong className="block">{te("repriceButton", { charge: repriceCharge.label })}</strong><span className="mt-0.5 block text-xs font-normal text-[var(--muted)]">{te("repriceHint")}</span></span></button>
          <button type="button" onClick={() => { setToolsOpen(false); void share(); }} className="planner-tool-row"><span className="planner-tool-icon"><Link2 size={18} /></span><span className="min-w-0 flex-1 text-left"><strong className="block">{te(shareUrl ? "share.copy" : trip.share_enabled ? "share.rotate" : "share.create")}</strong><span className="mt-0.5 block text-xs font-normal text-[var(--muted)]">{te("shareHint")}</span></span></button>
          {trip.share_enabled && <button type="button" onClick={() => { setToolsOpen(false); setConfirmAction("revoke-share"); }} className="planner-tool-row text-red-700"><span className="planner-tool-icon bg-red-50"><Link2 size={18} /></span><span className="flex-1 text-left font-semibold">{te("revokeCurrentShare")}</span></button>}
          {shareUrl && <label className="flex min-w-0 items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm"><input aria-label={te("share.linkLabel")} readOnly value={shareUrl} className="min-w-0 flex-1 bg-transparent outline-none" /><button type="button" aria-label={te("share.copy")} onClick={() => void navigator.clipboard?.writeText(shareUrl)} className="grid min-h-11 min-w-11 place-items-center"><Copy size={16} /></button></label>}
        </section>
        {trip.price_status === "stale"
          ? <section className="planner-tool-card text-sm text-amber-900">{te("stalePriceHint")}</section>
          : <section className="planner-tool-card"><PriceAlertButton resourceType="trip" resourceId={trip.id} currentPrice={Number(trip.total_price)} currency={trip.currency} returnPath={`/trips/${trip.id}`} /></section>}
      </div>
    </PlannerOverlay>

    <PlannerOverlay open={stayOpen} onClose={() => { if (!action) setStayOpen(false); }} title={tStay("title")} description={tStay("description")} size="wide" expandable>
      {stayOpen && <StayAreaFlow tripId={trip.id} busy={action === "lodging"} onSelectHotel={selectStayHotel} onManualLodging={() => { setStayOpen(false); window.setTimeout(openLodgingEditor, 0); }} />}
    </PlannerOverlay>

    <PlannerOverlay open={lodgingOpen} onClose={() => { if (!busy("lodging")) setLodgingOpen(false); }} title={te("lodgingTitle")} description={te("lodgingDescription")} footer={<div className="flex gap-3"><button type="button" onClick={() => setLodgingOpen(false)} disabled={busy("lodging")} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold disabled:opacity-40">{te("cancel")}</button><button type="button" onClick={() => void savePrimaryLodging()} disabled={busy("lodging") || !lodgingDraft.name.trim() || !lodgingDraft.location_name.trim()} className="flex min-h-12 flex-[1.4] items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-45">{action === "lodging" ? <Loader2 size={17} className="animate-spin" /> : <Check size={17} />}{te("syncAllDays")}</button></div>}>
      <div className="grid gap-5">
        <label className="text-sm font-semibold">{te("hotelName")}<input value={lodgingDraft.name} maxLength={255} onChange={(event) => setLodgingDraft((current) => ({ ...current, name: event.target.value }))} placeholder={te("hotelNamePlaceholder")} className={fieldClass} /></label>
        <div><label className="text-sm font-semibold">{te("hotelPlaceSearch")}</label><PlacePicker label={te("hotelPlace")} value={lodgingDraft.location_name} confirmed={Boolean(lodgingDraft.provider_place_id && lodgingDraft.latitude != null && lodgingDraft.longitude != null)} countryCodes={placeCountryCodes} bias={placeBias} onTextChange={(value) => setLodgingDraft((current) => ({ ...current, location_name: value, provider_place_id: "", latitude: undefined, longitude: undefined, location_source: "manual" }))} onSelect={chooseLodgingPlace} /><p className="mt-2 flex items-center gap-1.5 text-xs text-[var(--muted)]">{lodgingDraft.latitude != null && lodgingDraft.longitude != null ? <><Check size={13} className="text-emerald-600" />{te("hotelPlaceConfirmed")}</> : <><CircleAlert size={13} />{te("hotelPlacePending")}</>}</p></div>
      </div>
    </PlannerOverlay>

    <PlannerOverlay open={Boolean(editingItem)} onClose={closeEditor} title={editingMeal ? te("editMeal", { meal: te(editingItem?.system_role === "lunch" ? "slot.lunch" : "slot.dinner") }) : te(draftItem ? "addItem" : "editItemTitle")} description={te(editingMeal ? "editMealDescription" : draftItem ? "addItemDescription" : "editItemDescription")} footer={draftItem && <div className="flex gap-3"><button type="button" onClick={closeEditor} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold">{te("cancel")}</button><button type="button" onClick={commitDraftItem} disabled={!draftItem.title.trim()} className="min-h-12 flex-[1.4] rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-40">{te("addToItinerary")}</button></div>}>{editingItem && <div className="grid gap-5">
      <label className="text-sm font-semibold">{te(editingMeal ? "restaurantName" : "itemName")}<input value={editingItem.title} maxLength={255} onChange={(event) => patchItem(editingItem.id, { title: event.target.value, ...(editingMeal ? { data: { ...editingItem.data, meal_selection_source: "user" } } : {}) }, false)} placeholder={te(editingMeal ? "restaurantPlaceholder" : "itemPlaceholder")} className={fieldClass} /></label>
      <div><label className="text-sm font-semibold">{te(editingMeal ? "restaurantPlace" : "place")}</label><PlacePicker label={te(editingMeal ? "restaurantPlace" : "place")} value={editingItem.location_name || ""} confirmed={editingItem.location_source === "confirmed" || (["google_places", "naver_local"].includes(editingItem.location_source || "") && editingItem.data.needs_place_confirmation !== true)} countryCodes={placeCountryCodes} bias={placeBias} onTextChange={(value) => patchItem(editingItem.id, { location_name: value, provider_place_id: null, latitude: null, longitude: null, location_source: null, is_estimated: true, data: { ...editingItem.data, place_match_status: "unresolved", needs_place_confirmation: true, ...(editingMeal ? { meal_selection_source: "user" } : {}) } })} onSelect={(place) => choosePlace(editingItem, place)} /><p className="mt-2 flex items-center gap-1.5 text-xs text-[var(--muted)]">{editingItem.location_source === "confirmed" || (["google_places", "naver_local"].includes(editingItem.location_source || "") && editingItem.data.needs_place_confirmation !== true) ? <><Check size={13} className="text-emerald-600" />{te("placeConfirmed")}</> : editingItem.location_source?.endsWith("_auto") ? <><CircleAlert size={13} className="text-sky-700" />{te("placeAutoFix", { provider: editingItem.location_provider === "naver_local" || editingItem.location_source === "naver_local_auto" ? "NAVER" : "Google" })}</> : editingItem.location_name ? <><CircleAlert size={13} />{te("placePickFromResults")}</> : <><MapPin size={13} />{te("placeLater")}</>}</p></div>
      {!editingItem.system_role && <div className="grid gap-4">
        <label className="text-sm font-semibold">{te("date")}<select value={editingItem.day_date} onChange={(event) => { const previousDay = editingItem.day_date; patchItem(editingItem.id, { day_date: event.target.value, start_time: editingItem.start_time ? withTime(event.target.value, timeValue(editingItem.start_time, trip.timezone)) : null, end_time: null }); setActiveDay(event.target.value); if (!draftItem) setStaleDays((current) => new Set([...current, previousDay, event.target.value])); }} className={fieldClass}>{days.map((value) => <option key={value} value={value}>{value}</option>)}</select></label>
        <fieldset><legend className="text-sm font-semibold">{te("timeMode")}</legend><div className="mt-2 grid grid-cols-2 gap-2" role="radiogroup" aria-label={te("timeMode")}><button type="button" role="radio" aria-checked={Boolean(editingItem.fixed_time)} onClick={() => patchItem(editingItem.id, { fixed_time: true, start_time: editingItem.start_time || withTime(editingItem.day_date, "09:00"), end_time: null })} className={`min-h-12 rounded-xl border px-3 text-sm font-bold ${editingItem.fixed_time ? "border-violet-500 bg-violet-50 text-violet-900" : "border-[var(--line)] bg-white"}`}><Clock3 size={16} className="mr-1.5 inline" />{te("fixedTime")}</button><button type="button" role="radio" aria-checked={!editingItem.fixed_time} onClick={() => patchItem(editingItem.id, { fixed_time: false, start_time: null, end_time: null })} className={`min-h-12 rounded-xl border px-3 text-sm font-bold ${!editingItem.fixed_time ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white"}`}><RouteIcon size={16} className="mr-1.5 inline" />{te("chainedMode")}</button></div><p className="mt-2 text-xs leading-5 text-[var(--muted)]">{te(editingItem.fixed_time ? "fixedTimeHint" : "chainedHint")}</p></fieldset>
        <div className="grid grid-cols-2 gap-3">{editingItem.fixed_time && <label className="text-sm font-semibold">{te("fixedStart")}<input type="time" value={timeValue(editingItem.start_time, trip.timezone)} onChange={(event) => patchItem(editingItem.id, { start_time: withTime(editingItem.day_date, event.target.value), end_time: null })} className={fieldClass} /></label>}<label className="text-sm font-semibold">{te("stayDuration")}<select value={editingItem.duration_minutes || 60} onChange={(event) => patchItem(editingItem.id, { duration_minutes: Number(event.target.value), end_time: null })} className={fieldClass}>{activityDurationOptions.map((minutes) => <option key={minutes} value={minutes}>{te(`duration.m${minutes}`)}</option>)}</select></label></div>
      </div>}
      {editingMeal ? <label className="text-sm font-semibold">{te("notes")}<textarea rows={4} maxLength={4000} value={editingItem.notes || ""} onChange={(event) => patchItem(editingItem.id, { notes: event.target.value }, false)} placeholder={te("mealNotesPlaceholder")} className={fieldClass} /></label> : <details className="planner-advanced-settings"><summary>{te("advanced")}</summary><div className="grid gap-4 px-4 pb-4"><label className="text-sm font-semibold">{te("notes")}<textarea rows={4} maxLength={4000} value={editingItem.notes || ""} onChange={(event) => patchItem(editingItem.id, { notes: event.target.value }, false)} placeholder={te("itemNotesPlaceholder")} className={fieldClass} /></label><button type="button" aria-pressed={editingItem.locked} onClick={() => patchItem(editingItem.id, { locked: !editingItem.locked }, false)} className={`flex min-h-12 items-center gap-3 rounded-xl border px-4 text-left text-sm font-semibold ${editingItem.locked ? "border-amber-300 bg-amber-50 text-amber-900" : "border-[var(--line)]"}`}>{editingItem.locked ? <LockKeyhole size={18} /> : <Unlock size={18} />}{te(editingItem.locked ? "lockedNoSort" : "lockItem")}</button></div></details>}
      {!draftItem && !editingItem.system_role && <button type="button" onClick={() => removeItem(editingItem)} className="flex min-h-12 items-center justify-center gap-2 rounded-xl border border-red-200 bg-red-50 font-semibold text-red-800"><Trash2 size={18} />{te("deleteItem")}</button>}
    </div>}</PlannerOverlay>

    <PlannerOverlay open={routeDrawerOpen && Boolean(routeTarget)} onClose={closeRouteDrawer} title={te("routeTitle")} description={te("routeDescription")} size="wide" expandable>{routeTarget && <RouteModePanel key={`${routeTarget.fromItemId}-${routeTarget.toItemId}-${trip.version}`} trip={trip} items={items} fromItemId={routeTarget.fromItemId} toItemId={routeTarget.toItemId} initialSegment={selectedRoute} onError={setError} onResolved={(updated) => { replaceTrip(updated); setRoutes(updated.route_segments || []); setSelectedRoute(updated.route_segments?.find((route) => route.from_item_id === routeTarget.fromItemId && route.to_item_id === routeTarget.toItemId)); persistedRevisionRef.current = revisionRef.current; updateSaveState("saved"); setNotice(te("placeAutoFilled")); }} onEditItem={(itemId) => { closeRouteDrawer(); window.setTimeout(() => setEditingId(itemId), 0); }} onApplied={(updated) => { replaceTrip(updated); setRoutes(updated.route_segments || []); const applied = updated.route_segments?.find((route) => route.from_item_id === routeTarget.fromItemId && route.to_item_id === routeTarget.toItemId); setSelectedRoute(applied); setStaleDays((current) => { const next = new Set(current); const day = updated.items.find((item) => item.id === routeTarget.fromItemId)?.day_date; if (day) next.delete(day); return next; }); persistedRevisionRef.current = revisionRef.current; updateSaveState("saved"); setNotice(te("routeApplied")); }} />}</PlannerOverlay>

    <PlannerOverlay open={previewOpen && Boolean(preview)} onClose={() => setPreviewOpen(false)} title={te("previewTitle")} description={optimizationCharge.status === "ready" ? te("previewDescription", { charge: optimizationCharge.label }) : optimizationCharge.unavailableHelp} size="wide" footer={preview && <div className="flex gap-3"><button type="button" onClick={() => setPreviewOpen(false)} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold">{te("notNow")}</button><button type="button" onClick={() => void applyOptimization()} disabled={!preview.changed || action === "apply-preview" || optimizationCharge.status !== "ready"} className="flex min-h-12 flex-[1.4] items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-45">{action === "apply-preview" ? <Loader2 size={17} className="animate-spin" /> : <Sparkles size={17} />}{preview.changed ? te("applyCharge", { charge: optimizationCharge.label }) : te("alreadyOptimal")}</button></div>}>{preview && <div className="space-y-5"><section className={`rounded-2xl p-5 ${preview.changed ? "bg-[var(--teal-soft)]" : "bg-emerald-50"}`}><p className="text-sm font-semibold text-[var(--teal-dark)]">{te(preview.changed ? "foundBetter" : "alreadyOptimal")}</p><div className="mt-3 grid grid-cols-3 gap-3 text-center"><div><span className="block text-xs text-[var(--muted)]">{te("before")}</span><strong className="mt-1 block text-xl">{te("minutesShort", { minutes: preview.total_duration_before_minutes })}</strong></div><div><span className="block text-xs text-[var(--muted)]">{te("after")}</span><strong className="mt-1 block text-xl">{te("minutesShort", { minutes: preview.total_duration_after_minutes })}</strong></div><div><span className="block text-xs text-[var(--muted)]">{te("savings")}</span><strong className="mt-1 block text-xl text-[var(--teal)]">{te("minutesShort", { minutes: Math.max(0, preview.total_duration_before_minutes - preview.total_duration_after_minutes) })}</strong></div></div></section>{preview.days.map((day) => <section key={day.date} className="rounded-2xl border border-[var(--line)] p-4"><div className="flex items-center justify-between"><h3 className="font-bold">{day.date}</h3><span className="rounded-full bg-[var(--paper)] px-3 py-1 text-xs font-semibold">{te("savedMinutes", { minutes: day.saved_minutes })}</span></div><div className="mt-4 grid gap-4 sm:grid-cols-2"><div><p className="text-xs font-semibold tracking-[.12em] text-[var(--muted)]">{te("before")}</p><ol className="mt-2 space-y-2">{day.before.map((item, index) => <li key={item.id} className="flex items-center gap-2 text-sm"><span className="grid h-6 w-6 place-items-center rounded-full bg-[var(--paper)] text-xs font-bold">{index + 1}</span><span className="truncate">{item.title}</span></li>)}</ol></div><div><p className="text-xs font-semibold tracking-[.12em] text-[var(--teal)]">{te("suggested")}</p><ol className="mt-2 space-y-2">{day.after.map((item, index) => <li key={item.id} className="flex items-center gap-2 text-sm"><span className="grid h-6 w-6 place-items-center rounded-full bg-[var(--teal)] text-xs font-bold text-white">{index + 1}</span><span className="truncate font-medium">{item.title}</span></li>)}</ol></div></div></section>)}{preview.warnings.map((warning) => <p key={warning} className="rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-900">{warning}</p>)}</div>}</PlannerOverlay>

    <PlannerOverlay open={Boolean(confirmAction)} onClose={() => setConfirmAction(undefined)} title={confirmAction ? confirmCopy[confirmAction].title : te("confirmTitle")} description={confirmAction ? confirmCopy[confirmAction].description : undefined} footer={confirmAction && <div className="flex gap-3"><button type="button" onClick={() => setConfirmAction(undefined)} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold">{te("cancel")}</button><button type="button" disabled={confirmAction === "reprice" && repriceCharge.status !== "ready"} onClick={() => void runConfirmedAction()} className={`min-h-12 flex-1 rounded-xl font-semibold text-white disabled:opacity-45 ${confirmCopy[confirmAction].danger ? "bg-red-700" : "bg-[var(--teal)]"}`}>{confirmCopy[confirmAction].label}</button></div>}><div className="rounded-2xl bg-[var(--paper)] p-5 text-sm leading-7 text-[var(--muted)]"><CircleAlert size={24} className="mb-3 text-[var(--coral)]" />{te("confirmBody")}</div></PlannerOverlay>
    <PlannerOverlay open={Boolean(flightRole)} onClose={() => { if (!busy("flight")) setFlightRole(undefined); }} title={te("flightTitle", { direction: te(flightRole === "return_flight" ? "returnLeg" : "outbound") })} description={te("flightDescription")} footer={<div className="flex gap-3"><button type="button" onClick={() => setFlightRole(undefined)} disabled={busy("flight")} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold disabled:opacity-40">{te("cancel")}</button><button type="button" onClick={() => void saveFlightAnchor()} disabled={busy("flight") || !flightDraftReady} className="flex min-h-12 flex-[1.4] items-center justify-center gap-2 rounded-xl bg-sky-800 px-4 font-semibold text-white disabled:opacity-45">{action?.startsWith("flight-") ? <Loader2 size={17} className="animate-spin" /> : <Check size={17} />}{te("saveFlight")}</button></div>}>
      <div className="grid gap-5">
        <div className="grid grid-cols-2 gap-3"><label className="text-sm font-semibold">{te("airline")}<input value={flightDraft.airline} maxLength={120} onChange={(event) => setFlightDraft((current) => ({ ...current, airline: event.target.value }))} placeholder={te("airlinePlaceholder")} className={fieldClass} /></label><label className="text-sm font-semibold">{te("flightNumber")}<input value={flightDraft.flight_number} maxLength={32} onChange={(event) => setFlightDraft((current) => ({ ...current, flight_number: event.target.value }))} placeholder={te("flightNumberPlaceholder")} className={fieldClass} /></label></div>
        <div className="grid grid-cols-2 gap-3"><label className="text-sm font-semibold">{te("originAirport")}<input value={flightDraft.origin} maxLength={16} onChange={(event) => setFlightDraft((current) => ({ ...current, origin: event.target.value }))} placeholder="TPE" className={fieldClass} /></label><label className="text-sm font-semibold">{te("arrivalAirport")}<input value={flightDraft.destination} maxLength={16} onChange={(event) => setFlightDraft((current) => ({ ...current, destination: event.target.value }))} placeholder="NRT" className={fieldClass} /></label></div>
        <fieldset className="rounded-2xl border border-sky-100 bg-sky-50/70 p-4"><legend className="px-1 text-sm font-bold text-sky-950">{te("airportLocalTime")}</legend><div className="grid gap-4 sm:grid-cols-2"><label className="text-sm font-semibold">{te("localDeparture")}<input type="datetime-local" value={flightDraft.departure_local} onChange={(event) => setFlightDraft((current) => ({ ...current, departure_local: event.target.value }))} className={fieldClass} /></label><label className="text-sm font-semibold">{te("departureTz")}<input value={flightDraft.departure_timezone} maxLength={64} onChange={(event) => setFlightDraft((current) => ({ ...current, departure_timezone: event.target.value }))} placeholder={te("tzPlaceholderTpe")} className={fieldClass} /></label><label className="text-sm font-semibold">{te("localArrival")}<input type="datetime-local" value={flightDraft.arrival_local} onChange={(event) => setFlightDraft((current) => ({ ...current, arrival_local: event.target.value }))} className={fieldClass} /></label><label className="text-sm font-semibold">{te("arrivalTz")}<input value={flightDraft.arrival_timezone} maxLength={64} onChange={(event) => setFlightDraft((current) => ({ ...current, arrival_timezone: event.target.value }))} placeholder={te("tzPlaceholderNrt")} className={fieldClass} /></label></div><p className="mt-3 text-xs leading-5 text-sky-900/70">{te("tzHint")}</p></fieldset>
        {editingFlightItem && flightAnchorInfo(editingFlightItem) && <button type="button" onClick={() => void saveFlightAnchor(true)} disabled={busy("flight")} className="min-h-11 rounded-xl border border-slate-300 bg-slate-50 px-4 text-sm font-semibold text-slate-700 disabled:opacity-40">{te("clearFlight")}</button>}
      </div>
    </PlannerOverlay>
  </main>;
}
