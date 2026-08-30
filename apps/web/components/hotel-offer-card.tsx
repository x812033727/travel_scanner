import { BedDouble, Check, CircleDollarSign, Clock3, ExternalLink, Hotel, MapPin, Star, TrainFront, X } from "lucide-react";
import Image from "next/image";
import { twd } from "@/lib/api";

export type HotelOfferView = {
  id: string;
  hotel_name?: unknown;
  provider?: string;
  source_mode?: "live" | "test" | "mock" | "estimate";
  is_mock?: boolean;
  action_kind?: "deep_link" | "recheck" | "none";
  images?: string[];
  attributions?: string[];
  attribution_urls?: string[];
  retrieved_at?: string;
  expires_at?: string;
  freshness_status?: "fresh" | "expiring" | "expired";
  rating?: unknown;
  review_score?: unknown;
  review_count?: unknown;
  room_type?: unknown;
  nights?: unknown;
  base_price?: unknown;
  taxes?: unknown;
  fees?: unknown;
  total_price?: unknown;
  nightly_price?: unknown;
  breakfast_included?: boolean;
  refundable?: boolean;
  cancellation_policy?: unknown;
  station_walk_minutes?: unknown;
  distance_to_center_km?: unknown;
  address?: unknown;
  amenities?: unknown;
};

const sourceLabels = {
  live: "正式即時資料",
  test: "供應商測試資料",
  mock: "模擬資料",
  estimate: "估算資料",
};

function number(value: unknown) {
  const parsed = Number(value ?? 0);
  return Number.isFinite(parsed) ? parsed : 0;
}

function text(value: unknown, fallback = "") {
  return typeof value === "string" && value.trim() ? value : fallback;
}

export function hotelNightlyPrice(offer: HotelOfferView) {
  const explicit = number(offer.nightly_price);
  return explicit || number(offer.total_price) / Math.max(1, number(offer.nights));
}

export function hotelRating(offer: HotelOfferView) {
  return number(offer.review_score) || number(offer.rating);
}

export function HotelOfferCard({ offer, actionUrl }: { offer: HotelOfferView; actionUrl: string }) {
  const image = offer.images?.[0];
  const mode = offer.source_mode || (offer.is_mock ? "mock" : "estimate");
  const total = number(offer.total_price);
  const nightly = hotelNightlyPrice(offer);
  const rating = hotelRating(offer);
  const amenities = Array.isArray(offer.amenities) ? offer.amenities.filter((item): item is string => typeof item === "string").slice(0, 4) : [];
  const retrievedAt = offer.retrieved_at ? new Date(offer.retrieved_at).toLocaleString("zh-TW") : undefined;
  const expiresAt = offer.expires_at ? new Date(offer.expires_at).toLocaleString("zh-TW") : undefined;

  return (
    <article className="overflow-hidden rounded-[1.5rem] border border-[var(--line)] bg-white">
      {image ? <Image src={image} alt={text(offer.hotel_name, "住宿照片")} width={720} height={400} unoptimized className="h-48 w-full object-cover" /> : <div className="grid h-36 place-items-center bg-gradient-to-br from-[var(--teal-soft)] to-[var(--coral-soft)] text-[var(--teal)]"><Hotel size={38} /></div>}
      <div className="p-5">
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--teal)]">{sourceLabels[mode]}</p>
            <h2 className="mt-1 text-xl font-bold">{text(offer.hotel_name, "住宿方案")}</h2>
          </div>
          <div className="shrink-0 text-right"><strong className="block text-lg">{twd.format(nightly)}</strong><span className="text-xs text-[var(--muted)]">每晚</span></div>
        </div>

        <div className="mt-4 flex flex-wrap gap-2 text-xs">
          {rating > 0 && <span className="flex items-center gap-1 rounded-full bg-amber-50 px-2.5 py-1.5 font-semibold text-amber-900"><Star size={14} fill="currentColor" />{rating.toFixed(1)}{number(offer.review_count) ? `（${number(offer.review_count).toLocaleString("zh-TW")} 則）` : ""}</span>}
          <span className="flex items-center gap-1 rounded-full bg-[var(--paper)] px-2.5 py-1.5"><BedDouble size={14} />{text(offer.room_type, "客房")} · {number(offer.nights) || "-"} 晚</span>
          {number(offer.station_walk_minutes) > 0 && <span className="flex items-center gap-1 rounded-full bg-[var(--paper)] px-2.5 py-1.5"><TrainFront size={14} />車站步行 {number(offer.station_walk_minutes)} 分</span>}
        </div>

        {(text(offer.address) || number(offer.distance_to_center_km) > 0) && <p className="mt-3 flex items-start gap-2 text-sm leading-6 text-[var(--muted)]"><MapPin className="mt-1 shrink-0" size={15} />{text(offer.address)}{text(offer.address) && number(offer.distance_to_center_km) ? " · " : ""}{number(offer.distance_to_center_km) ? `距市中心 ${number(offer.distance_to_center_km).toFixed(1)} 公里` : ""}</p>}

        {amenities.length > 0 && <ul className="mt-3 flex flex-wrap gap-2 text-xs text-[var(--muted)]">{amenities.map((amenity) => <li key={amenity} className="rounded-lg border border-[var(--line)] px-2 py-1">{amenity}</li>)}</ul>}

        <div className="mt-4 grid gap-2 rounded-2xl bg-[var(--paper)] p-4 text-sm">
          <div className="flex justify-between gap-3"><span>房價</span><span>{twd.format(number(offer.base_price))}</span></div>
          <div className="flex justify-between gap-3 text-[var(--muted)]"><span>稅金與費用</span><span>{twd.format(number(offer.taxes) + number(offer.fees))}</span></div>
          <div className="flex justify-between gap-3 border-t border-[var(--line)] pt-2 font-bold"><span>住宿總價</span><span>{twd.format(total)}</span></div>
        </div>

        <div className="mt-4 space-y-2 text-sm">
          <p className={`flex items-start gap-2 ${offer.breakfast_included ? "text-emerald-800" : "text-[var(--muted)]"}`}>{offer.breakfast_included ? <Check className="mt-0.5 shrink-0" size={16} /> : <X className="mt-0.5 shrink-0" size={16} />}早餐{offer.breakfast_included ? "已包含" : "未標示為包含"}</p>
          <p className={`flex items-start gap-2 ${offer.refundable ? "text-emerald-800" : "text-[var(--muted)]"}`}>{offer.refundable ? <Check className="mt-0.5 shrink-0" size={16} /> : <CircleDollarSign className="mt-0.5 shrink-0" size={16} />}{offer.refundable ? "可退款" : "非退款或條件未確認"}{text(offer.cancellation_policy) ? ` · ${text(offer.cancellation_policy)}` : ""}</p>
        </div>

        <p className="mt-4 flex items-start gap-2 text-xs leading-5 text-[var(--muted)]"><Clock3 className="mt-0.5 shrink-0" size={14} />來源：{offer.provider || "未標示"}{retrievedAt ? ` · 取得 ${retrievedAt}` : ""}{expiresAt ? ` · 報價期限 ${expiresAt}` : ""}{offer.freshness_status === "expired" ? " · 已過期，必須重新確認" : ""}</p>
        {offer.attributions?.length ? <p className="mt-1 text-xs text-[var(--muted)]">圖片：{offer.attributions.map((label, index) => offer.attribution_urls?.[index] ? <span key={`${label}-${index}`}>{index > 0 ? "、" : ""}<a className="underline" href={offer.attribution_urls[index]} target="_blank" rel="noreferrer">{label}</a></span> : <span key={`${label}-${index}`}>{index > 0 ? "、" : ""}{label}</span>)}</p> : null}
        <a href={actionUrl} target="_blank" rel="noopener noreferrer" className="mt-5 flex items-center justify-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]">{offer.action_kind === "deep_link" ? "前往供應商" : "外站重新確認"}<ExternalLink size={16} /></a>
      </div>
    </article>
  );
}
