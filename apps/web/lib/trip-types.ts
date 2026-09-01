export type TripItem = {
  id: string;
  item_type: string;
  offer_id?: string | null;
  day_date: string;
  position: number;
  title: string;
  location_name?: string | null;
  start_time?: string | null;
  end_time?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  locked: boolean;
  is_estimated: boolean;
  data: Record<string, unknown>;
  provider_place_id?: string | null;
  location_source?: string | null;
  duration_minutes?: number | null;
  notes?: string | null;
  fixed_time?: boolean;
};

export type RouteStep = {
  travel_mode: string;
  instruction: string;
  duration_minutes?: number | null;
  distance_meters?: number | null;
  departure_stop?: string | null;
  arrival_stop?: string | null;
  departure_time?: string | null;
  arrival_time?: string | null;
  line_name?: string | null;
  line_short_name?: string | null;
  line_color?: string | null;
  headsign?: string | null;
  stop_count?: number | null;
  platform?: string | null;
  exit_name?: string | null;
  recommended_car?: string | null;
};

export type RouteSegment = {
  from_item_id: string;
  to_item_id: string;
  status: string;
  provider: string;
  attribution: string;
  generated_at: string;
  requested_departure_time?: string | null;
  schedule_mode: "scheduled" | "preview" | "live";
  preference: string;
  duration_minutes: number;
  distance_meters?: number | null;
  fare?: number | string | null;
  currency?: string | null;
  encoded_polyline?: string | null;
  maps_url?: string | null;
  steps: RouteStep[];
  details_available: string[];
  warnings: string[];
};

export type Trip = {
  id: string;
  name: string;
  mode: string;
  total_price: number;
  currency: string;
  data: Record<string, unknown>;
  planning?: {
    status: "live" | "fallback" | "partial";
    provider: "openai" | "anthropic" | "minimax" | "catalog";
    model?: string | null;
    generated_at: string;
    warnings: string[];
    scope?: "day" | "trip";
    day_date?: string | null;
  } | null;
  version: number;
  destination_name?: string | null;
  destination_place_id?: string | null;
  start_date?: string | null;
  end_date?: string | null;
  timezone?: string;
  route_preference?: "FEWER_TRANSFERS" | "LESS_WALKING" | "FASTEST";
  items: TripItem[];
  route_segments?: RouteSegment[];
  share_enabled?: boolean;
  created_at?: string;
  updated_at?: string;
  usage?: { status: "reserved" | "charged" | "released"; uses: number; reference: string };
};

export function formatTime(value?: string | null, locale?: string) {
  if (!value) return "彈性時段";
  return new Intl.DateTimeFormat(locale || activeLocale(), {
    hour: "2-digit",
    minute: "2-digit",
    hour12: false,
  }).format(new Date(value));
}

export function groupTripItems(items: TripItem[]) {
  const grouped = new Map<string, TripItem[]>();
  for (const item of [...items].sort((a, b) => a.day_date.localeCompare(b.day_date) || a.position - b.position)) {
    grouped.set(item.day_date, [...(grouped.get(item.day_date) || []), item]);
  }
  return [...grouped.entries()];
}
import { activeLocale } from "@/lib/locale-format";
