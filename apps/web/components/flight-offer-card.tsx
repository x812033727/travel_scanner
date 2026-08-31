"use client";

import { ExternalLink, Plane, RefreshCw } from "lucide-react";
import { useState } from "react";
import { api, twd } from "@/lib/api";

export type FlightCardOffer = {
  id: string;
  provider?: string;
  source_mode?: "live" | "test" | "mock" | "estimate";
  airline?: unknown;
  marketing_airline?: unknown;
  operating_airlines?: unknown;
  selling_agent?: unknown;
  origin?: unknown;
  destination?: unknown;
  stops?: unknown;
  total_price?: unknown;
  retrieved_at?: string;
  last_verified_at?: string;
  clickout_available?: boolean;
  baggage_summary?: unknown;
  checked_baggage_kg?: unknown;
  carry_on?: unknown;
  arrival_day_offset?: unknown;
};

type RefreshResult = {
  new_price: string | number;
  price_change: string | number;
  still_available: boolean;
  refreshed_at: string;
};

export function FlightOfferCard({
  offer,
  fallbackUrl,
}: {
  offer: FlightCardOffer;
  fallbackUrl: string;
}) {
  const [price, setPrice] = useState(Number(offer.total_price || 0));
  const [verifiedAt, setVerifiedAt] = useState(
    offer.last_verified_at || offer.retrieved_at,
  );
  const [refreshing, setRefreshing] = useState(false);
  const [message, setMessage] = useState("");
  const stops = Number(offer.stops || 0);
  const dayOffset = Number(offer.arrival_day_offset || 0);
  const operating = Array.isArray(offer.operating_airlines)
    ? offer.operating_airlines.join("、")
    : "";
  const baggage = offer.baggage_summary
    ? String(offer.baggage_summary)
    : Number(offer.checked_baggage_kg || 0) > 0
      ? `托運 ${offer.checked_baggage_kg} kg`
      : offer.carry_on
        ? "含手提行李"
        : "行李需向售票端確認";

  async function refresh() {
    setRefreshing(true);
    setMessage("");
    try {
      const result = await api<RefreshResult>(`/offers/${offer.id}/refresh`, {
        method: "POST",
      });
      setPrice(Number(result.new_price));
      setVerifiedAt(result.refreshed_at);
      setMessage(result.still_available ? "已更新為供應商最新價格" : "此票價目前已售罄");
    } catch (error) {
      setMessage((error as Error).message);
    } finally {
      setRefreshing(false);
    }
  }

  return (
    <article className="overflow-hidden rounded-[1.5rem] border border-[var(--line)] bg-white">
      <div className="grid h-28 place-items-center bg-gradient-to-br from-[var(--teal-soft)] to-[var(--coral-soft)] text-[var(--teal)]">
        <Plane size={34} />
      </div>
      <div className="p-5">
        <div className="flex items-start justify-between gap-3">
          <div>
            <p className="text-xs font-semibold uppercase tracking-wide text-[var(--teal)]">
              {offer.source_mode === "estimate" ? "彈性日期估算" : "即時航班價格"}
            </p>
            <h2 className="mt-1 text-xl font-bold">
              {String(offer.marketing_airline || offer.airline || "航班")}
            </h2>
          </div>
          <strong>{twd.format(price)}</strong>
        </div>
        <p className="mt-3 text-sm text-[var(--muted)]">
          {String(offer.origin || "")} → {String(offer.destination || "")} · {stops ? `${stops} 次轉機` : "直飛"}
          {dayOffset ? ` · 抵達 +${dayOffset} 日` : ""}
        </p>
        {operating && <p className="mt-2 text-sm text-[var(--muted)]">實際承運：{operating}</p>}
        <p className="mt-1 text-sm text-[var(--muted)]">售票端：{String(offer.selling_agent || "重新確認時顯示")}</p>
        <p className="mt-1 text-sm text-[var(--muted)]">行李：{baggage}</p>
        <p className="mt-2 text-xs text-[var(--muted)]">
          來源：{offer.provider || "未標示"}{verifiedAt ? ` · 驗價 ${new Date(verifiedAt).toLocaleString("zh-TW")}` : ""}
        </p>
        {offer.provider === "skyscanner" && (
          <p className="mt-2 text-xs text-[var(--muted)]">
            Powered by <a className="font-semibold underline" href="https://www.skyscanner.net" target="_blank" rel="noreferrer">Skyscanner</a>
          </p>
        )}
        {message && <p className="mt-3 text-sm text-[var(--coral)]" role="status">{message}</p>}
        <div className="mt-4 grid gap-2 sm:grid-cols-2">
          <button type="button" onClick={refresh} disabled={refreshing || offer.source_mode === "estimate"} className="flex items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold disabled:opacity-50">
            <RefreshCw size={16} className={refreshing ? "animate-spin" : ""} />
            {refreshing ? "驗價中" : "重新驗價"}
          </button>
          {offer.clickout_available ? (
            <form action={`/api/travel/offers/${offer.id}/clickout`} method="post" target="_blank">
              <button className="flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white" type="submit">
                前往訂票 <ExternalLink size={16} />
              </button>
            </form>
          ) : (
            <a href={fallbackUrl} target="_blank" rel="noreferrer" className="flex items-center justify-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]">
              {offer.source_mode === "estimate" ? "選定日期後查即時價格" : "外站重新確認"}<ExternalLink size={16} />
            </a>
          )}
        </div>
      </div>
    </article>
  );
}
