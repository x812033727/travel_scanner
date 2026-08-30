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
};

export type Trip = {
  id: string;
  name: string;
  mode: string;
  total_price: number;
  currency: string;
  data: Record<string, unknown>;
  version: number;
  items: TripItem[];
  share_enabled?: boolean;
  created_at?: string;
  updated_at?: string;
};

export function formatTime(value?: string | null) {
  if (!value) return "彈性時段";
  return new Intl.DateTimeFormat("zh-TW", {
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
