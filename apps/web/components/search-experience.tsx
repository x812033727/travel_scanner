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
import Link from "next/link";
import { useRouter, useSearchParams } from "next/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { api, twd } from "@/lib/api";
import { destinationByAirport, interestLabel, interests as destinationInterests } from "@/lib/destinations";

type Parsed = {
  origin?: string;
  destination?: string;
  departure_date?: string;
  return_date?: string;
  departure_month?: string;
  travelers: { adults: number; children?: number; children_ages?: number[]; rooms?: number };
  trip_length_days?: number;
  budget_twd?: number;
  interests: string[];
  avoid_red_eye: boolean;
  hotel_min_rating?: number;
  hotel_max_nightly_twd?: number;
  breakfast_required?: boolean;
  refundable_required?: boolean;
  max_station_walk_minutes?: number;
  preferred_area?: string;
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

type Cost = {
  confirmed_cost: string | number;
  estimated_cost: string | number;
  total_cost: string | number;
  components: Array<{ label: string; amount: string | number; confidence: string }>;
};

type ItineraryDay = { date: string; label: string; items: Array<{ title: string }> };

type Plan = {
  id: string;
  mode: string;
  title: string;
  duplicate: boolean;
  total_cost: Cost;
  flight?: Offer;
  hotel?: Offer;
  activity?: Offer;
  transport?: Offer;
  itinerary?: ItineraryDay[];
  pros: string[];
  cons: string[];
  compared_with_cheapest: { price_difference: string | number; flight_minutes_saved: number };
};

type ProviderStatus = {
  provider: string;
  mode: "live" | "test" | "mock" | "disabled";
  status: "ready" | "not_configured" | "disabled";
  modules: string[];
  message: string;
};

type SearchResult = {
  status: string;
  result?: { modules?: Record<string, Offer[]>; plans?: Plan[] };
  warnings?: string[];
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

function titleFor(module: string, offer: Offer): string {
  if (module === "flight") return String(offer.airline ?? offer.flight_number ?? "航班");
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
    const extras = [offer.breakfast_included ? "含早餐" : null, offer.refundable ? "可退款" : null, offer.station_walk_minutes ? `步行 ${offer.station_walk_minutes} 分鐘到車站` : null].filter(Boolean).join(" · ");
    return `${rating ? `${rating.toFixed(1)} 分` : "尚無評分"} · ${offer.nights ?? "-"} 晚 · ${offer.room_type ?? "客房"}${extras ? ` · ${extras}` : ""}`;
  }
  if (module === "activities") return `${interestLabel(String(offer.category || ""))} · ${offer.duration_minutes ?? "-"} 分鐘 · ${offer.address ?? offer.city ?? ""}`;
  return `${offer.duration_minutes ?? "-"} 分鐘 · ${offer.origin ?? ""} → ${offer.destination ?? ""}`;
}

function recheckUrl(module: string, offer: Offer, parsed: Parsed | null, dates: string[]) {
  if (offer.action_kind === "deep_link" && offer.booking_url) return offer.booking_url;
  const query = module === "hotel"
    ? `${titleFor(module, offer)} ${parsed?.destination ?? ""} ${dates[0]} ${dates[1]}`
    : `${titleFor(module, offer)} ${parsed?.origin ?? ""} ${parsed?.destination ?? ""} ${dates[0]}`;
  return `https://www.google.com/travel/search?q=${encodeURIComponent(query)}&hl=zh-TW`;
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
  const codes = raw.split(",").map((item) => item.trim()).filter((item) => supported.has(item));
  const labels = mapping.filter(([label]) => raw.includes(label)).map(([, code]) => code);
  return Array.from(new Set([...codes, ...labels]));
}

export function SearchExperience() {
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
      travelers: {
        adults: Number(params.get("adults") || 1),
        children: Number(params.get("children") || 0),
        children_ages: (params.get("children_ages") || "").split(",").filter(Boolean).map(Number),
        rooms: Number(params.get("rooms") || 1),
      },
      budget_twd: Number(params.get("budget_twd") || 0) || undefined,
      interests: parseInterests(rawInterests),
      avoid_red_eye: params.get("avoid_red_eye") === "true" || rawInterests.includes("紅眼"),
      hotel_min_rating: Number(params.get("hotel_min_rating") || 0) || undefined,
      hotel_max_nightly_twd: Number(params.get("hotel_max_nightly_twd") || 0) || undefined,
      breakfast_required: params.get("breakfast_required") === "true",
      refundable_required: params.get("refundable_required") === "true",
      max_station_walk_minutes: Number(params.get("max_station_walk_minutes") || 0) || undefined,
      preferred_area: params.get("preferred_area") || undefined,
      pace: (params.get("pace") as Parsed["pace"]) || "balanced",
      confidence: 1,
      missing_fields: [],
    };
  }, [params]);
  const [parsedResult, setParsedResult] = useState<Parsed | null>(null);
  const parsed = structuredParsed || parsedResult;
  const [providerStatus, setProviderStatus] = useState<ProviderStatus | null>(null);
  const [progress, setProgress] = useState(0);
  const [done, setDone] = useState<string[]>([]);
  const [plans, setPlans] = useState<Plan[]>([]);
  const [offers, setOffers] = useState<Record<string, Offer[]>>({});
  const [warnings, setWarnings] = useState<string[]>([]);
  const [searchId, setSearchId] = useState<string>();
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  const [activeTab, setActiveTab] = useState("plans");
  const [breakfastOnly, setBreakfastOnly] = useState(params.get("breakfast_required") === "true");
  const [refundableOnly, setRefundableOnly] = useState(params.get("refundable_required") === "true");
  const [directOnly, setDirectOnly] = useState(false);
  const [refundableFlightOnly, setRefundableFlightOnly] = useState(false);
  const [activityInterest, setActivityInterest] = useState("all");
  const [sortByPrice, setSortByPrice] = useState(false);
  const started = useRef(false);

  useEffect(() => {
    api<ProviderStatus>("/providers/status")
      .then(setProviderStatus)
      .catch(() => setError("目前無法確認即時資料服務狀態，請稍後再試。"));
  }, []);

  useEffect(() => {
    if (structuredParsed || started.current || !text) return;
    started.current = true;
    api<Parsed>("/ai/parse-trip", { method: "POST", body: JSON.stringify({ text }) })
      .then(setParsedResult)
      .catch((reason: Error) => setError(reason.message));
  }, [structuredParsed, text]);

  const dates = useMemo(() => {
    if (parsed?.departure_date) {
      const departure = parsed.departure_date;
      const returning = parsed.return_date || departure;
      return [departure, returning];
    }
    const departure = parsed?.departure_month ? new Date(parsed.departure_month) : new Date("2026-11-01");
    departure.setDate(10);
    const returning = new Date(departure);
    returning.setDate(departure.getDate() + (parsed?.trip_length_days || 5));
    return [departure.toISOString().slice(0, 10), returning.toISOString().slice(0, 10)];
  }, [parsed]);

  async function loadFinal(id: string) {
    const result = await api<SearchResult>(`/searches/${id}`);
    if (result.result?.modules) setOffers(result.result.modules);
    if (result.result?.plans) setPlans(result.result.plans);
    setWarnings(result.warnings || []);
  }

  async function begin() {
    if (!parsed || providerStatus?.status !== "ready") return;
    setBusy(true);
    setError(undefined);
    setProgress(2);
    try {
      const accepted = await api<{ search_id: string }>("/searches", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          trip_type: "round_trip",
          origin: parsed.origin || "TPE",
          destination: parsed.destination || "NRT",
          departure_date: dates[0],
          return_date: dates[1],
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
            hotel_max_nightly_twd: parsed.hotel_max_nightly_twd,
            breakfast_required: parsed.breakfast_required,
            refundable_required: parsed.refundable_required,
            max_station_walk_minutes: parsed.max_station_walk_minutes,
            preferred_area: parsed.preferred_area,
            optimization_mode: "balanced",
            interests: parsed.interests,
            pace: parsed.pace || "balanced",
          },
        }),
      });
      setSearchId(accepted.search_id);
      const stream = new EventSource(`/api/travel/searches/${accepted.search_id}/events`);
      stream.addEventListener("module.results", (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        setProgress(data.progress);
        setOffers((current) => ({ ...current, [data.module]: data.offers }));
      });
      stream.addEventListener("provider.completed", (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        if (data.status === "completed") {
          setDone((current) => current.includes(data.module) ? current : [...current, data.module]);
        }
      });
      stream.addEventListener("optimization.completed", (message) => {
        const data = JSON.parse((message as MessageEvent).data);
        setProgress(92);
        setPlans(data.plans);
      });
      stream.addEventListener("search.completed", async () => {
        setProgress(100);
        setBusy(false);
        stream.close();
        await loadFinal(accepted.search_id).catch(() => undefined);
      });
      stream.addEventListener("search.failed", async () => {
        setError("搜尋未能取得任何結果，請查看資料來源狀態後再試。");
        setBusy(false);
        stream.close();
        await loadFinal(accepted.search_id).catch(() => undefined);
      });
      stream.onerror = () => {
        setWarnings((current) => [
          ...current,
          "即時連線曾短暫中斷；完成後會從伺服器重新載入結果。",
        ]);
      };
    } catch (reason) {
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
      router.push(`/trips/${trip.id}`);
    } catch (reason) {
      setError((reason as Error).message);
    }
  }

  const visibleOffers = useMemo(() => {
    let rows = [...(offers[activeTab] || [])];
    if (activeTab === "flight") {
      rows = rows.filter((offer) => !directOnly || Number(offer.stops || 0) === 0)
        .filter((offer) => !refundableFlightOnly || Boolean(offer.refundable));
    }
    if (activeTab === "hotel") {
      rows = rows.filter((offer) => !breakfastOnly || Boolean(offer.breakfast_included))
        .filter((offer) => !refundableOnly || Boolean(offer.refundable));
    }
    if (activeTab === "activities" && activityInterest !== "all") {
      rows = rows.filter((offer) => offer.category === activityInterest);
    }
    if (sortByPrice) rows.sort((left, right) => amount(left) - amount(right));
    return rows;
  }, [activeTab, activityInterest, breakfastOnly, directOnly, offers, refundableFlightOnly, refundableOnly, sortByPrice]);

  const destination = destinationByAirport(parsed?.destination);

  const providerTone = providerStatus?.status === "ready"
    ? providerStatus.mode === "live" ? "bg-emerald-50 text-emerald-800" : "bg-amber-50 text-amber-900"
    : "bg-red-50 text-red-800";

  return (
    <main className="mx-auto max-w-6xl px-5 pb-20 md:px-8">
      <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <p className="mb-2 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />你的旅行需求</p>
            <h1 className="max-w-4xl text-2xl font-bold md:text-3xl">{destination ? `${destination.country === "JP" ? "日本" : destination.country === "KR" ? "韓國" : "泰國"}・${destination.name}完整旅程` : text || "完整旅程搜尋"}</h1>
            {destination && <p className="mt-2 text-sm text-[var(--muted)]">{destination.summary} · 當地時區 {destination.timezone} · 建議停留 {destination.recommendedStay}</p>}
          </div>
          {providerStatus && <span className={`rounded-full px-3 py-2 text-xs font-semibold ${providerTone}`}>{providerStatus.message}</span>}
        </div>
        {parsed && <div className="mt-5 flex flex-wrap gap-2 text-sm">
          {[`${parsed.travelers.adults + (parsed.travelers.children || 0)} 位旅客`, `${parsed.travelers.rooms || 1} 間房`, `${dates[0]} → ${dates[1]}`, parsed.preferred_area ? `住在 ${parsed.preferred_area}` : null, parsed.budget_twd ? `預算 ${twd.format(parsed.budget_twd)}` : null, parsed.hotel_max_nightly_twd ? `每晚 ≤ ${twd.format(parsed.hotel_max_nightly_twd)}` : null, parsed.avoid_red_eye ? "避開紅眼" : null, parsed.breakfast_required ? "含早餐" : null, parsed.refundable_required ? "可退款" : null, ...parsed.interests.map(interestLabel)].filter(Boolean).map((tag) => <span key={String(tag)} className="rounded-full bg-[var(--teal-soft)] px-3 py-1.5 text-[var(--teal-dark)]">{tag}</span>)}
        </div>}
        {!searchId && <button disabled={!parsed || busy || providerStatus?.status !== "ready"} onClick={begin} className="mt-6 rounded-2xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50">確認條件並開始搜尋</button>}
        {error && <div role="alert" className="mt-5 flex items-start gap-2 rounded-xl bg-red-50 p-4 text-sm text-red-800"><AlertCircle size={18} className="mt-0.5 shrink-0" /><span>{error} {error.includes("sign") || error.includes("登入") ? <Link className="underline" href="/login">前往登入</Link> : null}</span></div>}
        {warnings.map((warning) => <p key={warning} className="mt-3 rounded-xl bg-amber-50 px-4 py-3 text-sm text-amber-900">{warning}</p>)}
      </section>

      {searchId && <section aria-label="搜尋進度" className="mb-7 rounded-3xl border border-[var(--line)] bg-white p-6">
        <div className="mb-4 flex items-center justify-between"><strong>{progress === 100 ? "分析完成" : "正在組合你的旅程"}</strong><span className="font-mono text-sm text-[var(--muted)]">{progress}%</span></div>
        <div className="h-2 overflow-hidden rounded-full bg-[#e4ebe6]"><div className="h-full rounded-full bg-[var(--teal)] transition-all" style={{ width: `${progress}%` }} /></div>
        <div className="mt-5 grid grid-cols-2 gap-3 md:grid-cols-4">{stages.map(({ key, label, icon: Icon }) => <div key={key} className={`flex items-center gap-2 rounded-xl p-2 text-sm ${done.includes(key) ? "text-[var(--teal)]" : "text-[var(--muted)]"}`}>{done.includes(key) ? <Check size={17} /> : <LoaderCircle size={17} className={busy ? "animate-spin" : ""} />}<Icon size={17} />{label}</div>)}</div>
      </section>}

      {(plans.length > 0 || Object.keys(offers).length > 0) && <section>
        <div className="mb-5 flex gap-2 overflow-x-auto pb-1" role="tablist" aria-label="搜尋結果分類">
          {[{ key: "plans", label: "推薦組合" }, ...stages].map((tab) => <button key={tab.key} role="tab" aria-selected={activeTab === tab.key} onClick={() => setActiveTab(tab.key)} className={`whitespace-nowrap rounded-full border px-4 py-2 text-sm font-semibold ${activeTab === tab.key ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-white text-[var(--muted)]"}`}>{tab.label}</button>)}
        </div>

        {activeTab === "plans" && plans.length > 0 && <div className="grid gap-5 lg:grid-cols-3">{plans.map((plan, index) => <article key={plan.mode} className={`relative rounded-[1.75rem] border bg-white p-6 ${index === 0 ? "border-[var(--teal)] shadow-[0_20px_60px_rgba(13,107,104,.14)]" : "border-[var(--line)]"}`}>
          {index === 0 && <span className="absolute -top-3 left-6 rounded-full bg-[var(--teal)] px-3 py-1 text-xs font-semibold text-white">BEST OVERALL</span>}
          <div className="flex items-start justify-between gap-4"><div><p className="text-sm text-[var(--muted)]">{plan.title}</p><h2 className="mt-1 text-3xl font-bold">{twd.format(Number(plan.total_cost.total_cost))}</h2></div><button onClick={() => save(plan)} aria-label={`儲存${plan.title}`} className="rounded-xl border border-[var(--line)] p-2 text-[var(--teal)]"><Save size={18} /></button></div>
          <div className="my-5 space-y-3 border-y border-[var(--line)] py-5 text-sm">{plan.flight && <p className="flex justify-between gap-3"><span className="flex items-center gap-2"><Plane size={16} />{String(plan.flight.airline)}</span><span>{twd.format(amount(plan.flight))}</span></p>}{plan.hotel && <p className="flex justify-between gap-3"><span className="flex items-center gap-2"><Hotel size={16} />{String(plan.hotel.hotel_name)}</span><span>{twd.format(amount(plan.hotel))}</span></p>}{plan.transport && <p className="flex justify-between gap-3"><span className="flex items-center gap-2"><TrainFront size={16} />{String(plan.transport.transport_type)}</span><span>{twd.format(amount(plan.transport))}</span></p>}</div>
          {plan.itinerary?.length ? <p className="mb-4 flex items-center gap-2 rounded-xl bg-[var(--teal-soft)] p-3 text-sm text-[var(--teal-dark)]"><BadgeCheck size={16} />已安排 {plan.itinerary.length} 天可編輯行程</p> : null}
          <ul className="space-y-2 text-sm">{plan.pros.map((item) => <li key={item} className="flex gap-2"><Check size={16} className="mt-0.5 shrink-0 text-[var(--teal)]" />{item}</li>)}{plan.cons.map((item) => <li key={item} className="flex gap-2 text-[var(--muted)]"><Clock3 size={16} className="mt-0.5 shrink-0" />{item}</li>)}</ul>
          <button onClick={() => save(plan)} className="mt-5 w-full rounded-xl bg-[var(--teal)] px-4 py-3 font-semibold text-white">儲存並編輯行程</button>
        </article>)}</div>}

        {activeTab !== "plans" && <div className="mb-4 flex flex-wrap items-center gap-4 rounded-2xl border border-[var(--line)] bg-white px-4 py-3 text-sm">
          <strong className="text-[var(--teal-dark)]">快速篩選</strong>
          <label className="flex items-center gap-2"><input type="checkbox" checked={sortByPrice} onChange={(event) => setSortByPrice(event.target.checked)} />價格由低到高</label>
          {activeTab === "flight" && <><label className="flex items-center gap-2"><input type="checkbox" checked={directOnly} onChange={(event) => setDirectOnly(event.target.checked)} />只看直飛</label><label className="flex items-center gap-2"><input type="checkbox" checked={refundableFlightOnly} onChange={(event) => setRefundableFlightOnly(event.target.checked)} />可退款</label></>}
          {activeTab === "hotel" && <><label className="flex items-center gap-2"><input type="checkbox" checked={breakfastOnly} onChange={(event) => setBreakfastOnly(event.target.checked)} />含早餐</label><label className="flex items-center gap-2"><input type="checkbox" checked={refundableOnly} onChange={(event) => setRefundableOnly(event.target.checked)} />可退款</label></>}
          {activeTab === "activities" && <label className="flex items-center gap-2">興趣<select className="rounded-lg border border-[var(--line)] px-2 py-1.5" value={activityInterest} onChange={(event) => setActivityInterest(event.target.value)}><option value="all">全部</option>{destinationInterests.map((interest) => <option key={interest.code} value={interest.code}>{interest.label}</option>)}</select></label>}
        </div>}

        {activeTab !== "plans" && <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">{visibleOffers.map((offer) => {
          const image = offer.images?.[0];
          const mode = offer.source_mode || (offer.is_mock ? "mock" : "estimate");
          return <article key={offer.id} className="overflow-hidden rounded-[1.5rem] border border-[var(--line)] bg-white">
            {image ? <Image src={image} alt={titleFor(activeTab, offer)} width={720} height={400} unoptimized className="h-44 w-full object-cover" /> : <div className="grid h-28 place-items-center bg-gradient-to-br from-[var(--teal-soft)] to-[var(--coral-soft)] text-[var(--teal)]">{activeTab === "hotel" ? <Hotel size={34} /> : activeTab === "flight" ? <Plane size={34} /> : activeTab === "activities" ? <MapPinned size={34} /> : <TrainFront size={34} />}</div>}
            <div className="p-5"><div className="flex items-start justify-between gap-3"><div><p className="text-xs font-semibold uppercase tracking-wide text-[var(--teal)]">{sourceLabels[mode]}</p><h2 className="mt-1 text-xl font-bold">{titleFor(activeTab, offer)}</h2></div><strong>{twd.format(amount(offer))}</strong></div><p className="mt-3 text-sm leading-6 text-[var(--muted)]">{detailsFor(activeTab, offer)}</p><p className="mt-2 text-xs text-[var(--muted)]">來源：{offer.provider || "未標示"}{offer.retrieved_at ? ` · ${new Date(offer.retrieved_at).toLocaleString("zh-TW")}` : ""}</p>{offer.attributions?.length ? <p className="mt-1 text-xs text-[var(--muted)]">圖片：{offer.attributions.map((label, index) => offer.attribution_urls?.[index] ? <span key={label}>{index > 0 ? "、" : ""}<a className="underline" href={offer.attribution_urls[index]} target="_blank" rel="noreferrer">{label}</a></span> : <span key={label}>{index > 0 ? "、" : ""}{label}</span>)}</p> : null}<a href={recheckUrl(activeTab, offer, parsed, dates)} target="_blank" rel="noreferrer" className="mt-4 flex items-center justify-center gap-2 rounded-xl border border-[var(--teal)] px-4 py-3 text-sm font-semibold text-[var(--teal)]">{offer.action_kind === "deep_link" ? "前往供應商" : "外站重新確認"}<ExternalLink size={16} /></a></div>
          </article>;
        })}</div>}
        {activeTab !== "plans" && !visibleOffers.length && <p className="rounded-2xl border border-dashed border-[var(--line)] bg-white p-10 text-center text-[var(--muted)]">這個分類目前沒有符合條件的結果。</p>}
      </section>}
    </main>
  );
}
