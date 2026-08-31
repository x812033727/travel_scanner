"use client";

import {
  ArrowLeft,
  ArrowDown,
  ArrowUp,
  Check,
  CircleAlert,
  Clock3,
  Copy,
  Edit3,
  GripVertical,
  Link2,
  Loader2,
  LockKeyhole,
  MapPin,
  Plus,
  RefreshCw,
  Route as RouteIcon,
  Save,
  Settings2,
  Sparkles,
  Trash2,
  Undo2,
  Unlock,
  WifiOff,
} from "lucide-react";
import { useRouter } from "next/navigation";
import {
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
  type CSSProperties,
} from "react";
import { AffiliatePartnerOptions } from "@/components/affiliate-partner-options";
import { PlacePicker } from "@/components/place-picker";
import { PlannerOverlay } from "@/components/planner-overlay";
import { PriceAlertButton } from "@/components/price-alert-button";
import { RouteMap } from "@/components/route-map";
import { RouteSegmentCard } from "@/components/route-segment-card";
import { api, ApiError, isUsageInsufficient, twd } from "@/lib/api";
import { formatTime, groupTripItems, type RouteSegment, type Trip, type TripItem } from "@/lib/trip-types";

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

function timeValue(value?: string | null) {
  return value?.match(/T(\d{2}:\d{2})/)?.[1] || "";
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

function dayLabel(day: string, index: number) {
  const date = new Date(`${day}T00:00:00Z`);
  return {
    eyebrow: `DAY ${index + 1}`,
    short: `${date.getUTCMonth() + 1}/${date.getUTCDate()}`,
    weekday: new Intl.DateTimeFormat("zh-TW", { weekday: "short", timeZone: "UTC" }).format(date),
  };
}

function todayForTimezone(timezone?: string | null) {
  return new Intl.DateTimeFormat("en-CA", { timeZone: timezone || "UTC" }).format(new Date());
}

type RouteResponse = { segments: RouteSegment[]; failed_pairs: unknown[]; partial: boolean };
type Place = { place_id: string; provider: string; name: string; address?: string | null; latitude?: number | null; longitude?: number | null; opening_hours?: string[]; google_maps_url?: string | null; attribution?: string };
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
type PlannerTheme = "forest" | "ocean" | "sunset" | "lavender";

const plannerThemes: Array<{ id: PlannerTheme; name: string; description: string; colors: [string, string, string] }> = [
  { id: "forest", name: "森旅", description: "沉靜墨綠與暖白", colors: ["#0d6b68", "#f5f7f2", "#ed735d"] },
  { id: "ocean", name: "海岸", description: "深海藍與霧灰", colors: ["#27658a", "#f1f6f8", "#e7785f"] },
  { id: "sunset", name: "夕照", description: "陶土橘與沙色", colors: ["#a94f38", "#fbf5ec", "#d9943b"] },
  { id: "lavender", name: "暮紫", description: "柔霧紫與米白", colors: ["#675587", "#f7f4f8", "#c36e7e"] },
];

const fieldClass = "mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2.5 text-sm text-[var(--ink)] outline-none transition focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

export function TripEditor({ tripId }: { tripId: string }) {
  const router = useRouter();
  const [trip, setTrip] = useState<Trip>();
  const [items, setItems] = useState<TripItem[]>([]);
  const [routes, setRoutes] = useState<RouteSegment[]>([]);
  const [selectedRoute, setSelectedRoute] = useState<RouteSegment>();
  const [activeDay, setActiveDay] = useState("");
  const [editingId, setEditingId] = useState<string>();
  const [routeDrawerOpen, setRouteDrawerOpen] = useState(false);
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();
  const [action, setAction] = useState<string>();
  const [shareUrl, setShareUrl] = useState("");
  const [dragged, setDragged] = useState<string>();
  const [saveState, setSaveState] = useState<SaveState>("saved");
  const [revision, setRevision] = useState(0);
  const [staleDays, setStaleDays] = useState<Set<string>>(new Set());
  const [undoItem, setUndoItem] = useState<TripItem>();
  const [preview, setPreview] = useState<OptimizationPreview>();
  const [previewOpen, setPreviewOpen] = useState(false);
  const [confirmAction, setConfirmAction] = useState<ConfirmAction>();
  const [desktopMapVisible, setDesktopMapVisible] = useState(false);
  const [reorderMode, setReorderMode] = useState(false);
  const [toolsOpen, setToolsOpen] = useState(false);
  const [plannerTheme, setPlannerTheme] = useState<PlannerTheme>("forest");

  const tripRef = useRef<Trip | undefined>(undefined);
  const itemsRef = useRef<TripItem[]>([]);
  const revisionRef = useRef(0);
  const persistedRevisionRef = useRef(0);
  const saveStateRef = useRef<SaveState>("saved");
  const savePromiseRef = useRef<Promise<Trip | undefined> | undefined>(undefined);
  const optimizationApplyRef = useRef<{ previewId: string; key: string } | undefined>(undefined);
  const repriceRequestRef = useRef<{ tripVersion: number; key: string } | undefined>(undefined);
  const routeHistoryTokenRef = useRef<string | undefined>(undefined);
  const draftKey = `trip-planner-draft:${tripId}`;

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
        setSelectedRoute(value.route_segments?.[0]);
        const availableDays = daysBetween(value.start_date, value.end_date);
        const localToday = todayForTimezone(value.timezone);
        setActiveDay(
          availableDays.includes(localToday)
            ? localToday
            : availableDays[0] || value.items[0]?.day_date || "",
        );
        if (hasDraft && stored) {
          revisionRef.current = 1;
          setRevision(1);
          if (stored.baseVersion === value.version) {
            updateSaveState("dirty");
            setNotice("已復原尚未同步的本機草稿，系統會自動儲存。");
          } else {
            updateSaveState("conflict");
            setError("本機草稿的基礎版本與雲端不同，請選擇要保留哪個版本。");
          }
        }
      })
      .catch((reason: Error) => setError(reason.message));
    return () => { active = false; };
  }, [draftKey, replaceTrip, tripId, updateSaveState]);

  useEffect(() => {
    if (!undoItem) return;
    const timer = window.setTimeout(() => setUndoItem(undefined), 8_000);
    return () => window.clearTimeout(timer);
  }, [undoItem]);

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
  const activeRows = groups.get(activeDay) || [];
  const placeCountryCodes = useMemo(() => countryCodesForTrip(trip), [trip]);
  const placeBias = useMemo(() => {
    const reference = items.find((item) => item.latitude != null && item.longitude != null);
    return reference?.latitude != null && reference.longitude != null
      ? { latitude: reference.latitude, longitude: reference.longitude }
      : undefined;
  }, [items]);
  const editingItem = items.find((item) => item.id === editingId);

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
          setError("這趟旅程已在其他分頁或裝置更新，請選擇要保留哪個版本。");
        } else {
          updateSaveState("offline");
          setError(`${reason instanceof Error ? reason.message : "暫時無法儲存"}；本機修改仍保留，可稍後重試。`);
        }
        return undefined;
      })
      .finally(() => { savePromiseRef.current = undefined; });
    savePromiseRef.current = request;
    return request;
  }, [draftKey, replaceTrip, updateSaveState]);

  const flushChanges = useCallback(async (showNotice = false): Promise<Trip | undefined> => {
    let didSave = false;
    for (let attempt = 0; attempt < 20; attempt += 1) {
      if (saveStateRef.current === "conflict") return undefined;
      if (revisionRef.current === persistedRevisionRef.current) {
        updateSaveState("saved");
        if (showNotice) setNotice(didSave ? "行程已儲存" : "所有變更都已儲存");
        return tripRef.current;
      }
      const updated = await persistOnce();
      if (!updated) return undefined;
      didSave = true;
    }
    updateSaveState("offline");
    setError("修改持續更新中，尚未完成同步；請停止輸入後再重試。");
    return undefined;
  }, [persistOnce, updateSaveState]);

  useEffect(() => {
    if (saveState !== "dirty") return;
    const timer = window.setTimeout(() => { void flushChanges(false); }, 1_000);
    return () => window.clearTimeout(timer);
  }, [flushChanges, revision, saveState]);

  function move(id: string, direction: -1 | 1) {
    const item = itemsRef.current.find((row) => row.id === id);
    if (!item) return;
    updateItems((current) => {
      const sameDay = current.filter((row) => row.day_date === item.day_date).sort((a, b) => a.position - b.position);
      const index = sameDay.findIndex((row) => row.id === id);
      const target = sameDay[index + direction];
      if (!target) return current;
      return current.map((row) => row.id === id
        ? { ...row, position: target.position }
        : row.id === target.id ? { ...row, position: item.position } : row);
    }, item.day_date);
    const ids = new Set(itemsRef.current.filter((row) => row.day_date === item.day_date).map((row) => row.id));
    if (selectedRoute && (ids.has(selectedRoute.from_item_id) || ids.has(selectedRoute.to_item_id))) {
      setSelectedRoute(undefined);
      closeRouteDrawer();
    }
    setRoutes((current) => current.filter((route) => !ids.has(route.from_item_id)));
  }

  function drop(targetId: string) {
    if (!dragged || dragged === targetId) return;
    const source = itemsRef.current.find((item) => item.id === dragged);
    const target = itemsRef.current.find((item) => item.id === targetId);
    if (!source || !target) return;
    updateItems((current) => current.map((item) => item.id === source.id
      ? { ...item, day_date: target.day_date, position: target.position }
      : item.id === target.id && source.day_date === target.day_date
        ? { ...item, position: source.position }
        : item), source.day_date);
    setStaleDays((current) => new Set([...current, source.day_date, target.day_date]));
    setRoutes([]);
    setSelectedRoute(undefined);
    closeRouteDrawer();
    setDragged(undefined);
  }

  function add(day: string) {
    const item: TripItem = {
      id: crypto.randomUUID(), item_type: "custom", day_date: day,
      position: itemsRef.current.filter((row) => row.day_date === day).length,
      title: "新的行程安排", location_name: "", locked: false, fixed_time: false,
      is_estimated: true, duration_minutes: 60, data: { source_mode: "manual" },
    };
    updateItems((current) => [...current, item], day);
    setActiveDay(day);
    setEditingId(item.id);
  }

  function choosePlace(item: TripItem, place: Place) {
    patchItem(item.id, {
      title: item.title === "新的行程安排" ? place.name : item.title,
      location_name: place.address || place.name,
      latitude: place.latitude,
      longitude: place.longitude,
      provider_place_id: place.place_id,
      location_source: place.provider,
      is_estimated: false,
      data: { ...item.data, opening_hours: place.opening_hours || [], google_maps_url: place.google_maps_url, attribution: place.attribution },
    });
  }

  function removeItem(item: TripItem) {
    updateItems((current) => current.filter((row) => row.id !== item.id), item.day_date);
    setRoutes((current) => current.filter((route) => route.from_item_id !== item.id && route.to_item_id !== item.id));
    if (selectedRoute?.from_item_id === item.id || selectedRoute?.to_item_id === item.id) {
      setSelectedRoute(undefined);
      closeRouteDrawer();
    }
    setEditingId(undefined);
    setUndoItem(item);
    setNotice("已刪除安排，可在 8 秒內復原。");
  }

  function undoDelete() {
    if (!undoItem) return;
    updateItems((current) => [...current, undoItem], undoItem.day_date);
    setActiveDay(undoItem.day_date);
    setUndoItem(undefined);
    setNotice("安排已復原");
  }

  async function computeRoutes(day: string, refresh = false) {
    const currentTrip = await flushChanges(false);
    if (!currentTrip || saveStateRef.current === "conflict") return;
    setAction(`route-${day}`);
    setError(undefined);
    try {
      const result = await api<RouteResponse>(`/trips/${currentTrip.id}/routes/${refresh ? "refresh" : "compute"}`, {
        method: "POST",
        body: JSON.stringify({ version: currentTrip.version, day_date: day, route_preference: currentTrip.route_preference }),
      });
      const dayIds = new Set(itemsRef.current.filter((item) => item.day_date === day).map((item) => item.id));
      setRoutes((current) => [...current.filter((route) => !dayIds.has(route.from_item_id)), ...result.segments]);
      setStaleDays((current) => { const next = new Set(current); next.delete(day); return next; });
      setSelectedRoute(result.segments[0]);
      const providers = [...new Set(result.segments.map((segment) => segment.attribution))].join("、");
      setNotice(result.partial
        ? `已透過 ${providers} 更新可取得的路線；部分地點尚未確認位置。`
        : `路線已透過 ${providers} 更新，本次不扣次。`);
    } catch (reason) {
      setError(`${reason instanceof Error ? reason.message : "路線計算失敗"}；本次未扣次。`);
    } finally { setAction(undefined); }
  }

  async function previewOptimization(day?: string) {
    const currentTrip = await flushChanges(false);
    if (!currentTrip || saveStateRef.current === "conflict") return;
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
      setError(`${reason instanceof Error ? reason.message : "無法建立最佳化預覽"}；本次未扣次。`);
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
        ? "已套用最佳動線並扣除 1 次；鎖定與固定時間項目保持不動。"
        : "已完成動線檢查，本次未扣次。");
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        optimizationApplyRef.current = undefined;
        router.push("/pricing");
        return;
      }
      if (reason instanceof ApiError) {
        optimizationApplyRef.current = undefined;
        setError(`${reason.message}；伺服器已確認未扣次。`);
      } else {
        setError(`${reason instanceof Error ? reason.message : "套用最佳化失敗"}；結果尚未確認，重試會沿用同一請求編號，不會重複扣次。`);
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
        method: "POST", headers: { "Idempotency-Key": requestIdentity.key },
      });
      replaceTrip(updated);
      setRoutes(updated.route_segments || []);
      setSelectedRoute(updated.route_segments?.[0]);
      repriceRequestRef.current = undefined;
      setNotice(updated.usage?.status === "charged" ? "已重新查價並扣除 1 次。" : "已重新檢查價格，本次未扣次。");
    } catch (reason) {
      if (isUsageInsufficient(reason)) {
        repriceRequestRef.current = undefined;
        router.push("/pricing");
      } else if (reason instanceof ApiError) {
        repriceRequestRef.current = undefined;
        setError(`${reason.message}；伺服器已確認未扣次。`);
      } else {
        setError(`${reason instanceof Error ? reason.message : "重新查價失敗"}；結果尚未確認，重試會沿用同一請求編號。`);
      }
    } finally { setAction(undefined); }
  }

  async function createShare() {
    if (!tripRef.current) return;
    setAction("share");
    try {
      const result = await api<{ share_url: string }>(`/trips/${tripRef.current.id}/share`, { method: "POST" });
      setShareUrl(result.share_url);
      replaceTrip({ ...tripRef.current, share_enabled: true }, false);
      await navigator.clipboard?.writeText(result.share_url);
      setNotice("新的唯讀連結已建立並複製。");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "建立分享連結失敗"); }
    finally { setAction(undefined); }
  }

  async function share() {
    if (shareUrl) {
      await navigator.clipboard?.writeText(shareUrl);
      setNotice("分享連結已複製");
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
      setNotice("分享連結已撤銷");
    } catch (reason) { setError(reason instanceof Error ? reason.message : "撤銷分享連結失敗"); }
    finally { setAction(undefined); }
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
      setNotice("已載入雲端最新版本");
    } finally { setAction(undefined); }
  }

  async function overwriteConflict() {
    setAction("conflict");
    try {
      const latest = await api<Trip>(`/trips/${tripId}`);
      replaceTrip({ ...latest, items: itemsRef.current }, false);
      updateSaveState("dirty");
      await flushChanges(true);
    } finally { setAction(undefined); }
  }

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

  const saveLabel = saveState === "saving" ? "儲存中"
    : saveState === "dirty" ? "尚未儲存"
      : saveState === "offline" ? "同步失敗"
        : saveState === "conflict" ? "版本衝突" : "已儲存";
  const saveIcon = saveState === "saving" ? <Loader2 size={15} className="animate-spin" />
    : saveState === "offline" ? <WifiOff size={15} />
      : saveState === "conflict" ? <CircleAlert size={15} /> : <Check size={15} />;
  const today = todayForTimezone(trip?.timezone);
  const activeHasRoutes = routes.some((route) => activeRows.some((item) => item.id === route.from_item_id));
  const confirmCopy: Record<ConfirmAction, { title: string; description: string; label: string; danger?: boolean }> = {
    reprice: { title: "重新查價整趟旅程？", description: "成功取得新的機票、住宿或活動結果後會扣 1 次；供應商失敗或沒有結果不扣次。", label: "確認重新查價" },
    "revoke-share": { title: "撤銷分享連結？", description: "目前持有連結的人將立即無法查看這趟旅程。", label: "撤銷連結", danger: true },
    "rotate-share": { title: "更新分享連結？", description: "系統無法再次顯示舊連結。建立新連結後，舊連結會立即失效。", label: "建立新連結" },
    "overwrite-conflict": { title: "以本機內容覆蓋雲端版本？", description: "其他分頁或裝置較新的編輯會被本機內容取代，這個動作無法自動復原。", label: "確認覆蓋", danger: true },
  };

  if (error && !trip) return <main className="mx-auto max-w-4xl px-5 py-16"><p role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">{error}，請先登入或確認旅程仍存在。</p></main>;
  if (!trip) return <main className="mx-auto max-w-4xl px-5 py-16"><div className="h-44 animate-pulse rounded-[2rem] bg-white/80" /><p className="mt-4 text-center text-sm text-[var(--muted)]">正在載入旅程…</p></main>;

  return <main data-planner-theme={plannerTheme} className="planner-app-shell mx-auto max-w-7xl px-4 pb-36 sm:px-5 md:px-8 lg:pb-20">
    <header className="planner-app-bar flex lg:hidden">
      <button type="button" aria-label="返回我的旅行" onClick={() => router.push("/trips")} className="planner-icon-button">
        <ArrowLeft size={20} />
      </button>
      <div className="min-w-0 flex-1 text-center">
        <p className="truncate text-[.68rem] font-semibold tracking-[.12em] text-[var(--muted)]">{trip.destination_name || "我的旅程"}</p>
        <h1 className="truncate text-base font-bold tracking-tight">{trip.name}</h1>
      </div>
      <button type="button" aria-label="開啟旅程工具" aria-expanded={toolsOpen} onClick={() => setToolsOpen(true)} className="planner-icon-button">
        <Settings2 size={20} />
      </button>
    </header>

    <section className="relative mb-5 hidden overflow-hidden rounded-[2rem] border border-white/70 bg-[linear-gradient(135deg,#ffffff_15%,#eaf5f0_68%,#fff0eb)] p-5 shadow-[var(--shadow-lg)] sm:p-7 lg:block">
      <div aria-hidden="true" className="absolute -right-12 -top-16 h-44 w-44 rounded-full bg-[var(--coral)]/10 blur-2xl" />
      <div className="relative flex flex-col gap-5 xl:flex-row xl:items-start xl:justify-between">
        <div>
          <div className="flex flex-wrap items-center gap-2 text-xs font-semibold"><span className="rounded-full bg-white/75 px-3 py-1.5 text-[var(--teal)]">行程規劃器 · 版本 {trip.version}</span><span aria-live="polite" className={`flex items-center gap-1.5 rounded-full px-3 py-1.5 ${saveState === "saved" ? "bg-emerald-50 text-emerald-800" : saveState === "dirty" || saveState === "saving" ? "bg-amber-50 text-amber-900" : "bg-red-50 text-red-800"}`}>{saveIcon}{saveLabel}</span></div>
          <h1 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">{trip.name}</h1>
          <p className="mt-2 text-sm leading-6 text-[var(--muted)] sm:text-base">{trip.destination_name || "旅程"}{trip.start_date ? ` · ${trip.start_date} 至 ${trip.end_date}` : ""}{Number(trip.total_price) > 0 ? ` · ${twd.format(Number(trip.total_price))}` : ""}</p>
          <p className="mt-2 text-xs text-[var(--muted)]">手動編輯與查路免費；最佳化先預覽，確認成功套用後才扣 1 次。</p>
          {desktopMapVisible && <div className="mt-3 max-w-xs"><PriceAlertButton resourceType="trip" resourceId={trip.id} currentPrice={Number(trip.total_price)} currency={trip.currency} returnPath={`/trips/${trip.id}`} /></div>}
        </div>
        <div className="grid grid-cols-2 gap-2 sm:flex sm:flex-wrap"><button type="button" onClick={() => setConfirmAction("reprice")} disabled={Boolean(action) || trip.mode === "manual"} className="flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] bg-white/75 px-4 py-3 text-sm font-semibold disabled:opacity-40"><RefreshCw size={16} />重新查價</button><button type="button" onClick={() => previewOptimization()} disabled={Boolean(action)} className="flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--teal)] bg-white/75 px-4 py-3 text-sm font-semibold text-[var(--teal)] disabled:opacity-40">{action === "preview-all" ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}最佳化整趟</button><button type="button" onClick={() => void flushChanges(true)} disabled={saveState === "saving"} className="col-span-2 flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white disabled:opacity-60"><Save size={16} />儲存變更</button></div>
      </div>
      {saveState === "conflict" && <div role="alert" className="relative mt-5 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950"><p className="font-semibold">偵測到其他版本</p><p className="mt-1 leading-6">本機修改仍保留。你可以載入雲端版本，或確認後以本機內容覆蓋。</p><div className="mt-3 flex flex-wrap gap-2"><button type="button" onClick={() => void loadCloudVersion()} className="min-h-11 rounded-xl border border-amber-300 bg-white px-4 font-semibold">載入雲端版本</button><button type="button" onClick={() => setConfirmAction("overwrite-conflict")} className="min-h-11 rounded-xl bg-amber-900 px-4 font-semibold text-white">保留本機修改</button></div></div>}
    </section>

    <section className="planner-day-strip sticky z-30 -mx-4 mb-4 border-y border-[var(--line)] px-4 py-3 lg:top-0 lg:mx-0 lg:mb-5 lg:rounded-2xl lg:border"><div className="planner-day-scroll flex gap-2 overflow-x-auto pb-1" aria-label="選擇行程日期">{days.map((day, index) => { const label = dayLabel(day, index); const count = groups.get(day)?.length || 0; return <button key={day} type="button" aria-pressed={activeDay === day} onClick={() => { setActiveDay(day); setReorderMode(false); }} className={`planner-day-chip min-h-14 min-w-[5.1rem] shrink-0 rounded-2xl border px-3 py-2 text-left ${activeDay === day ? "planner-day-chip-active" : ""}`}><span className="block text-[.65rem] font-semibold tracking-[.12em] opacity-75">{day === today ? "今天" : label.eyebrow}</span><span className="mt-0.5 block text-sm font-bold">{label.short} {label.weekday}</span><span className="block text-[.65rem] opacity-70">{count} 個安排</span></button>; })}</div></section>

    <section className="mb-5 hidden flex-col gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 lg:flex lg:flex-row lg:items-center lg:justify-between"><label className="flex min-h-11 items-center justify-between gap-3 text-sm font-semibold sm:justify-start">路線偏好<select aria-label="路線偏好" value={trip.route_preference || "FEWER_TRANSFERS"} onChange={(event) => updateRoutePreference(event.target.value as Trip["route_preference"])} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3"><option value="FEWER_TRANSFERS">少轉乘</option><option value="FASTEST">最快抵達</option><option value="LESS_WALKING">少走路</option></select></label><div className="flex flex-wrap items-center gap-2 text-sm"><span className="rounded-full bg-[var(--teal-soft)] px-3 py-2 text-xs font-semibold text-[var(--teal)]">Google Maps{placeCountryCodes[0] === "jp" ? " · NAVITIME 備援" : ""}</span><button type="button" onClick={() => void share()} className="flex min-h-11 items-center gap-2 rounded-xl px-3 font-semibold text-[var(--teal)]"><Link2 size={16} />{shareUrl ? "複製分享連結" : trip.share_enabled ? "更新分享連結" : "建立唯讀連結"}</button>{trip.share_enabled && <button type="button" onClick={() => setConfirmAction("revoke-share")} className="min-h-11 rounded-xl px-3 font-semibold text-red-700">撤銷</button>}</div>{shareUrl && <label className="flex min-w-0 items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm sm:max-w-sm"><input aria-label="唯讀分享連結" readOnly value={shareUrl} className="min-w-0 flex-1 bg-transparent outline-none" /><button type="button" aria-label="複製分享連結" onClick={() => void navigator.clipboard?.writeText(shareUrl)} className="grid min-h-11 min-w-11 place-items-center"><Copy size={16} /></button></label>}</section>

    {desktopMapVisible && <AffiliatePartnerOptions tripId={trip.id} modules={["flight", "hotel", "activities", "transport", "connectivity"]} title="這趟旅程的合作平台" />}

    <div className="mt-2 grid items-start gap-6 lg:mt-6 lg:grid-cols-[minmax(0,1.35fr)_minmax(320px,.65fr)]"><section className="planner-day-panel rounded-[1.75rem] border border-[var(--line)] bg-white p-4 shadow-sm sm:p-6"><header className="mb-4 flex items-center justify-between gap-3 sm:mb-5"><div><p className="text-xs font-semibold tracking-[.16em] text-[var(--teal)]">{days.indexOf(activeDay) >= 0 ? `DAY ${days.indexOf(activeDay) + 1}` : "ITINERARY"}{activeDay === today ? " · 今天" : ""}</p><h2 className="mt-1 text-xl font-bold sm:text-2xl">{activeDay || "尚未設定日期"}</h2></div><div className="flex items-center gap-2"><button type="button" aria-label="計算當日路線" onClick={() => void computeRoutes(activeDay, activeHasRoutes || activeDay === today)} disabled={Boolean(action) || activeRows.length < 2} className="planner-secondary-button flex">{action === `route-${activeDay}` ? <Loader2 size={17} className="animate-spin" /> : <RouteIcon size={17} />}<span className="hidden sm:inline">查路</span></button><button type="button" aria-pressed={reorderMode} onClick={() => setReorderMode((value) => !value)} disabled={activeRows.length < 2} className="planner-secondary-button flex md:hidden"><GripVertical size={17} /><span>{reorderMode ? "完成" : "排序"}</span></button>{desktopMapVisible && <><button type="button" onClick={() => void previewOptimization(activeDay)} disabled={Boolean(action) || activeRows.length < 2} className="hidden min-h-11 items-center justify-center gap-1.5 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold disabled:opacity-40 md:flex">{action === `preview-${activeDay}` ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}最佳化</button><button type="button" onClick={() => add(activeDay)} disabled={!activeDay} className="hidden min-h-11 items-center justify-center gap-1.5 rounded-xl bg-[var(--paper)] px-3 text-sm font-semibold disabled:opacity-40 md:flex"><Plus size={16} />新增</button></>}</div></header>
      {staleDays.has(activeDay) && activeRows.length > 1 && <button type="button" onClick={() => void computeRoutes(activeDay, true)} className="mb-4 flex min-h-11 w-full items-center justify-between gap-3 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-left text-sm text-amber-950"><span className="flex items-center gap-2"><CircleAlert size={17} />行程內容已變更，舊路線不再使用</span><span className="shrink-0 font-semibold">重新計算</span></button>}
      {reorderMode && <div className="mb-3 flex items-center gap-2 rounded-2xl bg-[var(--teal-soft)] px-4 py-3 text-sm font-semibold text-[var(--teal-dark)] md:hidden"><GripVertical size={17} /><span className="flex-1">使用箭頭調整順序</span><button type="button" onClick={() => setReorderMode(false)} className="min-h-11 rounded-xl px-3">完成</button></div>}
      {activeRows.length === 0 ? <button type="button" onClick={() => add(activeDay)} className="grid min-h-48 w-full place-items-center rounded-2xl border border-dashed border-[var(--line)] bg-[linear-gradient(135deg,#f8faf6,#edf5f1)] p-8 text-center"><span><MapPin size={28} className="mx-auto text-[var(--teal)]" /><strong className="mt-3 block">這天還沒有安排</strong><span className="mt-1 block text-sm text-[var(--muted)]">加入第一個地點，開始建立旅行時間軸</span></span></button> : <ol className="planner-timeline space-y-3">{activeRows.map((item, index) => {
        const nextItem = activeRows[index + 1];
        const segment = routes.find((route) => route.from_item_id === item.id && route.to_item_id === nextItem?.id);
        return <li key={item.id} className="planner-enter relative pl-9" style={{ "--planner-index": index } as CSSProperties}><span aria-hidden="true" className="absolute left-[.68rem] top-7 z-10 h-4 w-4 rounded-full border-[3px] border-white bg-[var(--teal)] shadow" /><article draggable={desktopMapVisible} onDragStart={() => setDragged(item.id)} onDragOver={(event) => event.preventDefault()} onDrop={() => drop(item.id)} className={`planner-itinerary-card group p-4 ${reorderMode ? "planner-itinerary-card-reordering" : ""}`}><div className="flex items-start gap-3"><span className="hidden cursor-grab pt-1 text-[var(--muted)] lg:block" title="拖曳排序"><GripVertical size={19} /></span><button type="button" onClick={() => setEditingId(item.id)} className="min-w-0 flex-1 text-left"><div className="flex flex-wrap items-center gap-2"><span className="planner-time-badge">{formatTime(item.start_time)}</span>{item.duration_minutes && <span className="text-xs text-[var(--muted)]">停留 {item.duration_minutes} 分鐘</span>}{item.locked && <span className="rounded-full bg-amber-50 px-2 py-1 text-[.68rem] font-semibold text-amber-800">已鎖定</span>}{item.fixed_time && <span className="rounded-full bg-violet-50 px-2 py-1 text-[.68rem] font-semibold text-violet-800">固定時間</span>}</div><h3 className="mt-2 truncate text-lg font-bold tracking-tight">{item.title}</h3><p className="mt-1 flex items-start gap-1.5 text-sm leading-5 text-[var(--muted)]"><MapPin size={15} className="mt-0.5 shrink-0" />{item.location_name || "尚未選擇地點"}</p>{item.notes && <p className="mt-2 line-clamp-2 text-xs leading-5 text-[var(--muted)]">{item.notes}</p>}</button><div className="flex shrink-0 items-center gap-1"><button type="button" aria-label={`上移 ${item.title}`} disabled={index === 0} onClick={() => move(item.id, -1)} className={`${reorderMode ? "grid" : "hidden"} planner-reorder-button md:grid`}><ArrowUp size={18} /></button><button type="button" aria-label={`下移 ${item.title}`} disabled={index === activeRows.length - 1} onClick={() => move(item.id, 1)} className={`${reorderMode ? "grid" : "hidden"} planner-reorder-button md:grid`}><ArrowDown size={18} /></button><button type="button" aria-label={`編輯 ${item.title}`} onClick={() => setEditingId(item.id)} className={`${reorderMode ? "hidden" : "grid"} min-h-11 min-w-11 place-items-center rounded-xl bg-[var(--teal-soft)] text-[var(--teal)] md:grid`}><Edit3 size={17} /></button></div></div></article>{nextItem && <div className="py-2 pl-2">{segment && !staleDays.has(activeDay) ? <button type="button" aria-label={`查看前往 ${nextItem.title} 的路線`} onClick={() => { setSelectedRoute(segment); setRouteDrawerOpen(true); }} className="planner-route-link flex min-h-11 w-full items-center gap-3 rounded-2xl px-3 py-2 text-left text-sm"><span className="grid h-8 w-8 shrink-0 place-items-center rounded-full bg-white text-sky-700"><RouteIcon size={16} /></span><span className="min-w-0 flex-1"><strong>移動約 {segment.duration_minutes} 分鐘</strong><span className="ml-2 text-xs text-[var(--muted)]">{segment.steps.filter((step) => step.travel_mode === "TRANSIT").map((step) => step.line_short_name || step.line_name).filter(Boolean).join(" → ") || "步行／大眾運輸"}</span></span><span className="font-semibold text-[var(--teal)]">查看</span></button> : <div className="flex min-h-11 items-center gap-2 px-3 text-xs text-[var(--muted)]"><span className="h-px flex-1 border-t border-dashed border-[var(--line)]" /><span>{staleDays.has(activeDay) ? "路線待更新" : "尚未計算路線"}</span><span className="h-px flex-1 border-t border-dashed border-[var(--line)]" /></div>}</div>}</li>;
      })}</ol>}
    </section>{desktopMapVisible && <aside className="space-y-4"><RouteMap items={items} segment={selectedRoute} />{selectedRoute && <RouteSegmentCard segment={selectedRoute} selected defaultExpanded />}</aside>}</div>

    <div className="planner-mobile-bar fixed inset-x-0 bottom-0 z-40 px-3 pt-3 lg:hidden"><div className="planner-mobile-dock mx-auto grid max-w-lg grid-cols-[auto_1fr_1.2fr] items-center gap-2"><button type="button" aria-label={saveState === "offline" ? "儲存失敗，點擊重試" : saveLabel} onClick={() => { if (saveState === "offline") void flushChanges(true); }} disabled={saveState !== "offline"} className={`planner-save-status ${saveState === "offline" ? "planner-save-status-error" : ""}`}>{saveIcon}<span className="sr-only">{saveLabel}</span></button><button type="button" onClick={() => add(activeDay)} disabled={!activeDay} className="planner-dock-button planner-dock-button-secondary"><Plus size={18} />新增安排</button><button type="button" aria-label="最佳化" onClick={() => void previewOptimization(activeDay)} disabled={Boolean(action) || activeRows.length < 2} className="planner-dock-button planner-dock-button-primary">{action === `preview-${activeDay}` ? <Loader2 size={18} className="animate-spin" /> : <Sparkles size={18} />}智慧調整</button></div></div>

    {(error || notice) && <div className="fixed bottom-24 left-1/2 z-50 w-[min(92vw,38rem)] -translate-x-1/2 lg:bottom-6" aria-live="polite">{error && <div role="alert" className="rounded-2xl border border-red-200 bg-red-50 p-4 text-sm text-red-900 shadow-lg">{error}{saveState === "offline" && <button type="button" onClick={() => void flushChanges(true)} className="ml-3 font-bold underline">重試</button>}</div>}{notice && <div className="mt-2 flex items-center justify-between gap-3 rounded-2xl border border-emerald-200 bg-emerald-50 p-4 text-sm text-emerald-900 shadow-lg"><span className="flex items-center gap-2"><Check size={16} />{notice}</span>{undoItem && <button type="button" onClick={undoDelete} className="flex min-h-11 shrink-0 items-center gap-1 font-bold"><Undo2 size={16} />復原</button>}</div>}</div>}

    <PlannerOverlay open={toolsOpen} onClose={() => setToolsOpen(false)} title="旅程工具" description="不常用的設定集中在這裡，規劃時間軸時保持畫面清爽。">
      <div className="space-y-4">
        <section className="planner-tool-card">
          <div className="mb-3"><h3 className="font-bold">行程色系</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">選擇喜歡的氣氛，之後開啟會沿用。</p></div>
          <div className="grid grid-cols-2 gap-2" role="radiogroup" aria-label="行程色系">
            {plannerThemes.map((theme) => <button key={theme.id} type="button" role="radio" aria-checked={plannerTheme === theme.id} onClick={() => selectPlannerTheme(theme.id)} className={`planner-theme-option ${plannerTheme === theme.id ? "planner-theme-option-active" : ""}`}><span className="flex gap-1.5" aria-hidden="true">{theme.colors.map((color) => <span key={color} className="planner-theme-swatch" style={{ backgroundColor: color }} />)}</span><strong className="mt-2 block text-sm">{theme.name}</strong><span className="mt-0.5 block text-[.68rem] text-[var(--muted)]">{theme.description}</span>{plannerTheme === theme.id && <Check size={16} className="planner-theme-check" />}</button>)}
          </div>
        </section>
        <section className="planner-tool-card">
          <div className="mb-3 flex items-center justify-between gap-3"><div><p className="font-bold">路線偏好</p><p className="mt-1 text-xs text-[var(--muted)]">套用到下一次查路與智慧調整</p></div><span className="rounded-full bg-[var(--teal-soft)] px-3 py-1.5 text-xs font-semibold text-[var(--teal)]">Google Maps{placeCountryCodes[0] === "jp" ? " · NAVITIME" : ""}</span></div>
          <div className="grid grid-cols-3 gap-2" role="group" aria-label="路線偏好">{([['FEWER_TRANSFERS', '少轉乘'], ['FASTEST', '最快'], ['LESS_WALKING', '少走路']] as const).map(([value, label]) => <button key={value} type="button" aria-pressed={(trip.route_preference || "FEWER_TRANSFERS") === value} onClick={() => updateRoutePreference(value)} className={`min-h-11 rounded-xl border px-2 text-sm font-semibold ${(trip.route_preference || "FEWER_TRANSFERS") === value ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-white"}`}>{label}</button>)}</div>
        </section>
        <section className="planner-tool-card grid gap-2">
          <button type="button" onClick={() => { setToolsOpen(false); setConfirmAction("reprice"); }} disabled={Boolean(action) || trip.mode === "manual"} className="planner-tool-row"><span className="planner-tool-icon"><RefreshCw size={18} /></span><span className="min-w-0 flex-1 text-left"><strong className="block">重新查價</strong><span className="mt-0.5 block text-xs font-normal text-[var(--muted)]">更新機票、住宿與活動結果</span></span></button>
          <button type="button" onClick={() => { setToolsOpen(false); void share(); }} className="planner-tool-row"><span className="planner-tool-icon"><Link2 size={18} /></span><span className="min-w-0 flex-1 text-left"><strong className="block">{shareUrl ? "複製分享連結" : trip.share_enabled ? "更新分享連結" : "建立唯讀連結"}</strong><span className="mt-0.5 block text-xs font-normal text-[var(--muted)]">讓同行者查看目前行程</span></span></button>
          {trip.share_enabled && <button type="button" onClick={() => { setToolsOpen(false); setConfirmAction("revoke-share"); }} className="planner-tool-row text-red-700"><span className="planner-tool-icon bg-red-50"><Link2 size={18} /></span><span className="flex-1 text-left font-semibold">撤銷目前分享連結</span></button>}
          {shareUrl && <label className="flex min-w-0 items-center gap-2 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm"><input aria-label="唯讀分享連結" readOnly value={shareUrl} className="min-w-0 flex-1 bg-transparent outline-none" /><button type="button" aria-label="複製分享連結" onClick={() => void navigator.clipboard?.writeText(shareUrl)} className="grid min-h-11 min-w-11 place-items-center"><Copy size={16} /></button></label>}
        </section>
        <section className="planner-tool-card"><PriceAlertButton resourceType="trip" resourceId={trip.id} currentPrice={Number(trip.total_price)} currency={trip.currency} returnPath={`/trips/${trip.id}`} /></section>
        <AffiliatePartnerOptions tripId={trip.id} modules={["flight", "hotel", "activities", "transport", "connectivity"]} title="這趟旅程的合作平台" />
      </div>
    </PlannerOverlay>

    <PlannerOverlay open={Boolean(editingItem)} onClose={() => setEditingId(undefined)} title="編輯安排" description="修改會自動儲存；變更地點或時間後需重新查路。">{editingItem && <div className="grid gap-5">
      <label className="text-sm font-semibold">安排名稱<input value={editingItem.title} maxLength={255} onChange={(event) => patchItem(editingItem.id, { title: event.target.value }, false)} className={fieldClass} /></label>
      <div><label className="text-sm font-semibold">地點</label><PlacePicker value={editingItem.location_name || ""} confirmed={Boolean(editingItem.provider_place_id && editingItem.latitude != null)} countryCodes={placeCountryCodes} bias={placeBias} onTextChange={(value) => patchItem(editingItem.id, { location_name: value, provider_place_id: null, latitude: null, longitude: null, is_estimated: true })} onSelect={(place) => choosePlace(editingItem, place)} /><p className="mt-2 flex items-center gap-1.5 text-xs text-[var(--muted)]">{editingItem.provider_place_id ? <><Check size={13} className="text-emerald-600" />地點已確認，可計算路線</> : <><CircleAlert size={13} />請從搜尋結果選取地點</>}</p></div>
      <div className="grid grid-cols-2 gap-3"><label className="text-sm font-semibold">日期<select value={editingItem.day_date} onChange={(event) => { const previousDay = editingItem.day_date; patchItem(editingItem.id, { day_date: event.target.value, start_time: withTime(event.target.value, timeValue(editingItem.start_time)) }); setActiveDay(event.target.value); setStaleDays((current) => new Set([...current, previousDay, event.target.value])); }} className={fieldClass}>{days.map((value) => <option key={value} value={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">開始時間<input type="time" value={timeValue(editingItem.start_time)} onChange={(event) => patchItem(editingItem.id, { start_time: withTime(editingItem.day_date, event.target.value) })} className={fieldClass} /></label><label className="col-span-2 text-sm font-semibold sm:col-span-1">停留時間<select value={editingItem.duration_minutes || 60} onChange={(event) => patchItem(editingItem.id, { duration_minutes: Number(event.target.value) })} className={fieldClass}><option value="30">30 分鐘</option><option value="60">1 小時</option><option value="90">1.5 小時</option><option value="120">2 小時</option><option value="180">3 小時</option></select></label></div>
      <details className="planner-advanced-settings"><summary>備註與進階設定</summary><div className="grid gap-4 px-4 pb-4"><label className="text-sm font-semibold">備註<textarea rows={4} maxLength={4000} value={editingItem.notes || ""} onChange={(event) => patchItem(editingItem.id, { notes: event.target.value }, false)} placeholder="票券、集合方式、入口或集合點" className={fieldClass} /></label><div className="grid gap-2"><button type="button" aria-pressed={editingItem.locked} onClick={() => patchItem(editingItem.id, { locked: !editingItem.locked }, false)} className={`flex min-h-12 items-center gap-3 rounded-xl border px-4 text-left text-sm font-semibold ${editingItem.locked ? "border-amber-300 bg-amber-50 text-amber-900" : "border-[var(--line)]"}`}>{editingItem.locked ? <LockKeyhole size={18} /> : <Unlock size={18} />}{editingItem.locked ? "已鎖定，不參與排序" : "鎖定這個安排"}</button><button type="button" aria-pressed={Boolean(editingItem.fixed_time)} onClick={() => patchItem(editingItem.id, { fixed_time: !editingItem.fixed_time }, false)} className={`flex min-h-12 items-center gap-3 rounded-xl border px-4 text-left text-sm font-semibold ${editingItem.fixed_time ? "border-violet-300 bg-violet-50 text-violet-900" : "border-[var(--line)]"}`}><Clock3 size={18} />{editingItem.fixed_time ? "已固定預約時間" : "設為固定預約時間"}</button></div></div></details>
      <button type="button" onClick={() => removeItem(editingItem)} className="flex min-h-12 items-center justify-center gap-2 rounded-xl border border-red-200 bg-red-50 font-semibold text-red-800"><Trash2 size={18} />刪除這個安排</button>
    </div>}</PlannerOverlay>

    <PlannerOverlay open={routeDrawerOpen && Boolean(selectedRoute)} onClose={closeRouteDrawer} title="這段路怎麼走" description={selectedRoute ? `預計 ${selectedRoute.duration_minutes} 分鐘，時間以當地交通資料為準。` : undefined} size="wide" expandable>{selectedRoute && <div className="space-y-4"><RouteMap items={items} segment={selectedRoute} /><RouteSegmentCard segment={selectedRoute} selected defaultExpanded /></div>}</PlannerOverlay>

    <PlannerOverlay open={previewOpen && Boolean(preview)} onClose={() => setPreviewOpen(false)} title="最佳化預覽" description="先比較調整前後，只有確認並成功套用才扣 1 次。" size="wide" footer={preview && <div className="flex gap-3"><button type="button" onClick={() => setPreviewOpen(false)} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold">先不套用</button><button type="button" onClick={() => void applyOptimization()} disabled={!preview.changed || action === "apply-preview"} className="flex min-h-12 flex-[1.4] items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-45">{action === "apply-preview" ? <Loader2 size={17} className="animate-spin" /> : <Sparkles size={17} />}{preview.changed ? "套用並扣 1 次" : "目前已是建議安排"}</button></div>}>{preview && <div className="space-y-5"><section className={`rounded-2xl p-5 ${preview.changed ? "bg-[var(--teal-soft)]" : "bg-emerald-50"}`}><p className="text-sm font-semibold text-[var(--teal-dark)]">{preview.changed ? "找到更順的移動方式" : "目前已是建議安排"}</p><div className="mt-3 grid grid-cols-3 gap-3 text-center"><div><span className="block text-xs text-[var(--muted)]">調整前</span><strong className="mt-1 block text-xl">{preview.total_duration_before_minutes} 分</strong></div><div><span className="block text-xs text-[var(--muted)]">調整後</span><strong className="mt-1 block text-xl">{preview.total_duration_after_minutes} 分</strong></div><div><span className="block text-xs text-[var(--muted)]">預計節省</span><strong className="mt-1 block text-xl text-[var(--teal)]">{Math.max(0, preview.total_duration_before_minutes - preview.total_duration_after_minutes)} 分</strong></div></div></section>{preview.days.map((day) => <section key={day.date} className="rounded-2xl border border-[var(--line)] p-4"><div className="flex items-center justify-between"><h3 className="font-bold">{day.date}</h3><span className="rounded-full bg-[var(--paper)] px-3 py-1 text-xs font-semibold">節省 {day.saved_minutes} 分鐘</span></div><div className="mt-4 grid gap-4 sm:grid-cols-2"><div><p className="text-xs font-semibold tracking-[.12em] text-[var(--muted)]">調整前</p><ol className="mt-2 space-y-2">{day.before.map((item, index) => <li key={item.id} className="flex items-center gap-2 text-sm"><span className="grid h-6 w-6 place-items-center rounded-full bg-[var(--paper)] text-xs font-bold">{index + 1}</span><span className="truncate">{item.title}</span></li>)}</ol></div><div><p className="text-xs font-semibold tracking-[.12em] text-[var(--teal)]">建議安排</p><ol className="mt-2 space-y-2">{day.after.map((item, index) => <li key={item.id} className="flex items-center gap-2 text-sm"><span className="grid h-6 w-6 place-items-center rounded-full bg-[var(--teal)] text-xs font-bold text-white">{index + 1}</span><span className="truncate font-medium">{item.title}</span></li>)}</ol></div></div></section>)}{preview.warnings.map((warning) => <p key={warning} className="rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-900">{warning}</p>)}</div>}</PlannerOverlay>

    <PlannerOverlay open={Boolean(confirmAction)} onClose={() => setConfirmAction(undefined)} title={confirmAction ? confirmCopy[confirmAction].title : "確認操作"} description={confirmAction ? confirmCopy[confirmAction].description : undefined} footer={confirmAction && <div className="flex gap-3"><button type="button" onClick={() => setConfirmAction(undefined)} className="min-h-12 flex-1 rounded-xl border border-[var(--line)] font-semibold">取消</button><button type="button" onClick={() => void runConfirmedAction()} className={`min-h-12 flex-1 rounded-xl font-semibold text-white ${confirmCopy[confirmAction].danger ? "bg-red-700" : "bg-[var(--teal)]"}`}>{confirmCopy[confirmAction].label}</button></div>}><div className="rounded-2xl bg-[var(--paper)] p-5 text-sm leading-7 text-[var(--muted)]"><CircleAlert size={24} className="mb-3 text-[var(--coral)]" />請確認這是你目前要執行的操作；關閉視窗不會產生任何變更。</div></PlannerOverlay>
  </main>;
}
