"use client";

import {
  CalendarDays,
  ChevronDown,
  Hotel,
  MapPin,
  PlaneTakeoff,
  SlidersHorizontal,
  Sparkles,
  Users,
} from "lucide-react";
import { useRouter } from "next/navigation";
import { type FormEvent, useMemo, useState } from "react";
import {
  citiesForCountry,
  countries,
  destinations,
  interestLabel,
  interests,
  type CountryKey,
} from "@/lib/destinations";

const fieldClass =
  "mt-2 w-full rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3.5 text-[var(--ink)] outline-none transition focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

function futureDate(days: number) {
  const value = new Date();
  value.setUTCDate(value.getUTCDate() + days);
  return value.toISOString().slice(0, 10);
}

export function SearchWorkbench() {
  const router = useRouter();
  const [country, setCountry] = useState<CountryKey>("JP");
  const [destinationId, setDestinationId] = useState("tokyo");
  const [area, setArea] = useState("新宿");
  const [selectedInterests, setSelectedInterests] = useState(["food", "shopping", "culture"]);
  const [children, setChildren] = useState(0);
  const [childAges, setChildAges] = useState<number[]>([]);
  const countryCities = useMemo(() => citiesForCountry(country), [country]);
  const selectedCity = destinations.find((city) => city.id === destinationId) || countryCities[0];

  function chooseCountry(nextCountry: CountryKey) {
    const first = citiesForCountry(nextCountry)[0];
    setCountry(nextCountry);
    setDestinationId(first.id);
    setArea(first.areas[0]);
  }

  function chooseCity(cityId: string) {
    const city = destinations.find((item) => item.id === cityId);
    if (!city) return;
    setDestinationId(city.id);
    setArea(city.areas[0]);
  }

  function changeChildren(count: number) {
    setChildren(count);
    setChildAges((current) => Array.from({ length: count }, (_, index) => current[index] ?? 8));
  }

  function toggleInterest(code: string) {
    setSelectedInterests((current) =>
      current.includes(code) ? current.filter((item) => item !== code) : [...current, code],
    );
  }

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const data = new FormData(event.currentTarget);
    const origin = String(data.get("origin") || "TPE");
    const departure = String(data.get("departure") || "");
    const returning = String(data.get("returning") || "");
    const adults = String(data.get("adults") || "1");
    const rooms = String(data.get("rooms") || "1");
    const budget = String(data.get("budget") || "");
    const nightlyBudget = String(data.get("nightly_budget") || "");
    const pace = String(data.get("pace") || "balanced");
    const preferenceLabels = selectedInterests.map(interestLabel).join("、") || "自由探索";
    const description = `${adults} 位成人${children ? `、${children} 位兒童` : ""}從 ${origin} 前往${selectedCity.name}，${departure} 出發、${returning} 回程，住在${area}，偏好${preferenceLabels}。`;
    const query = new URLSearchParams({
      q: description,
      country,
      city: selectedCity.id,
      origin,
      destination: selectedCity.airport,
      departure_date: departure,
      return_date: returning,
      adults,
      children: String(children),
      children_ages: childAges.join(","),
      rooms,
      interests: selectedInterests.join(","),
      pace,
      preferred_area: area,
      hotel_min_rating: String(data.get("hotel_min_rating") || ""),
      max_station_walk_minutes: String(data.get("max_station_walk_minutes") || ""),
      avoid_red_eye: String(data.get("avoid_red_eye") === "on"),
      breakfast_required: String(data.get("breakfast_required") === "on"),
      refundable_required: String(data.get("refundable_required") === "on"),
      include_airbnb: String(data.get("include_airbnb") === "on"),
    });
    if (budget) query.set("budget_twd", budget);
    if (nightlyBudget) query.set("hotel_max_nightly_twd", nightlyBudget);
    router.push(`/search?${query.toString()}`);
  }

  return (
    <form id="trip-search" onSubmit={submit} className="rounded-[2rem] border border-[var(--line)] bg-white p-5 shadow-[var(--shadow-lg)] md:p-7">
      <div className="mb-5 flex flex-wrap items-start justify-between gap-3">
        <div>
          <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />日韓泰完整旅程搜尋</p>
          <h2 className="mt-1 text-2xl font-bold">先選城市，再比較整趟旅程</h2>
        </div>
        <span className="rounded-full bg-[var(--teal-soft)] px-3 py-1.5 text-xs font-semibold text-[var(--teal-dark)]">13 個重點目的地</span>
      </div>

      <div aria-label="選擇目的地國家" className="grid grid-cols-3 gap-2">
        {countries.map((item) => (
          <button key={item.key} type="button" aria-pressed={country === item.key} onClick={() => chooseCountry(item.key)} className={`rounded-2xl border px-3 py-3 text-left transition focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[var(--teal-soft)] ${country === item.key ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-[var(--surface)] hover:border-[var(--teal)]"}`}>
            <strong className="block">{item.label}</strong>
            <span className={`mt-1 hidden text-[11px] leading-4 md:block ${country === item.key ? "text-white/75" : "text-[var(--muted)]"}`}>{item.caption}</span>
          </button>
        ))}
      </div>

      <div className="mt-4 grid grid-cols-2 gap-2 sm:grid-cols-3">
        {countryCities.map((city) => (
          <button key={city.id} type="button" aria-pressed={selectedCity.id === city.id} onClick={() => chooseCity(city.id)} className={`rounded-2xl border p-3 text-left transition ${selectedCity.id === city.id ? "border-[var(--coral)] bg-[var(--coral-soft)]" : "border-[var(--line)] hover:border-[var(--coral)]"}`}>
            <span className="flex items-center justify-between gap-2"><strong>{city.name}</strong><span className="font-mono text-[11px] text-[var(--muted)]">{city.airport}</span></span>
            <span className="mt-1 block text-xs leading-5 text-[var(--muted)]">{city.recommendedStay} · {city.tags.slice(0, 2).join("／")}</span>
          </button>
        ))}
      </div>

      <p className="mt-3 flex items-start gap-2 rounded-xl bg-[var(--paper)] px-3 py-2.5 text-xs leading-5 text-[var(--muted)]"><MapPin className="mt-0.5 shrink-0 text-[var(--teal)]" size={15} /><span><strong className="text-[var(--ink)]">{selectedCity.name}</strong>：{selectedCity.summary}。當地時區 {selectedCity.timezone}，消費以 {selectedCity.currency} 為主，網站統一換算 TWD 比較。</span></p>

      <div className="mt-5 grid gap-4 md:grid-cols-2">
        <label className="text-sm font-semibold">
          出發機場
          <span className="relative block">
            <PlaneTakeoff className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <select className={`${fieldClass} pl-11`} name="origin" defaultValue="TPE" aria-label="出發機場">
              <option value="TPE">桃園國際機場 TPE</option>
              <option value="TSA">台北松山機場 TSA</option>
              <option value="KHH">高雄國際機場 KHH</option>
            </select>
          </span>
        </label>
        <label className="text-sm font-semibold">
          住宿區域
          <span className="relative block">
            <Hotel className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <select className={`${fieldClass} pl-11`} value={area} onChange={(event) => setArea(event.target.value)} aria-label="住宿區域">
              {selectedCity.areas.map((item) => <option key={item}>{item}</option>)}
            </select>
          </span>
        </label>
        <label className="text-sm font-semibold">
          出發日期
          <span className="relative block">
            <CalendarDays className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <input className={`${fieldClass} pl-11`} name="departure" type="date" defaultValue={futureDate(45)} min={futureDate(1)} required />
          </span>
        </label>
        <label className="text-sm font-semibold">
          回程日期
          <span className="relative block">
            <CalendarDays className="pointer-events-none absolute left-4 top-1/2 mt-1 -translate-y-1/2 text-[var(--muted)]" size={18} />
            <input className={`${fieldClass} pl-11`} name="returning" type="date" defaultValue={futureDate(50)} min={futureDate(2)} required />
          </span>
        </label>
      </div>

      <div className="mt-4 grid grid-cols-2 gap-4 md:grid-cols-4">
        <label className="text-sm font-semibold">
          <span className="flex items-center gap-2"><Users size={16} />成人</span>
          <select className={fieldClass} name="adults" defaultValue="2">
            {[1, 2, 3, 4, 5, 6].map((value) => <option key={value}>{value}</option>)}
          </select>
        </label>
        <label className="text-sm font-semibold">
          <span className="flex items-center gap-2"><Users size={16} />兒童</span>
          <select className={fieldClass} value={children} onChange={(event) => changeChildren(Number(event.target.value))} aria-label="兒童人數">
            {[0, 1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}
          </select>
        </label>
        <label className="text-sm font-semibold">
          <span className="flex items-center gap-2"><Hotel size={16} />房間</span>
          <select className={fieldClass} name="rooms" defaultValue="1">
            {[1, 2, 3, 4].map((value) => <option key={value}>{value}</option>)}
          </select>
        </label>
        <label className="text-sm font-semibold">
          總預算 TWD
          <input className={fieldClass} name="budget" inputMode="numeric" defaultValue="60000" />
        </label>
      </div>

      {children > 0 && <fieldset className="mt-4 rounded-2xl border border-[var(--line)] p-4"><legend className="px-1 text-sm font-semibold">兒童年齡（搜尋當日）</legend><div className="grid grid-cols-2 gap-3 sm:grid-cols-4">{childAges.map((age, index) => <label key={index} className="text-xs text-[var(--muted)]">第 {index + 1} 位<select aria-label={`第 ${index + 1} 位兒童年齡`} className={fieldClass} value={age} onChange={(event) => setChildAges((current) => current.map((item, childIndex) => childIndex === index ? Number(event.target.value) : item))}>{Array.from({ length: 18 }, (_, value) => <option key={value} value={value}>{value} 歲</option>)}</select></label>)}</div></fieldset>}

      <fieldset className="mt-5">
        <legend className="flex items-center gap-2 text-sm font-semibold"><SlidersHorizontal size={16} />想把時間留給什麼？</legend>
        <div className="mt-3 flex flex-wrap gap-2">{interests.map((interest) => <button key={interest.code} type="button" aria-pressed={selectedInterests.includes(interest.code)} onClick={() => toggleInterest(interest.code)} className={`rounded-full border px-3.5 py-2 text-sm font-medium transition ${selectedInterests.includes(interest.code) ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white text-[var(--muted)]"}`}>{interest.label}</button>)}</div>
      </fieldset>

      <details className="group mt-5 rounded-2xl border border-[var(--line)] bg-[var(--paper)]">
        <summary className="flex cursor-pointer list-none items-center justify-between gap-3 px-4 py-3.5 text-sm font-semibold">進階住宿與行程條件<ChevronDown className="transition group-open:rotate-180" size={18} /></summary>
        <div className="grid gap-4 border-t border-[var(--line)] p-4 sm:grid-cols-2">
          <label className="text-sm font-semibold">每晚住宿上限 TWD<input className={fieldClass} name="nightly_budget" inputMode="numeric" defaultValue="5000" /></label>
          <label className="text-sm font-semibold">最低星等<select className={fieldClass} name="hotel_min_rating" defaultValue="4"><option value="">不限</option>{[3, 4, 5].map((value) => <option key={value} value={value}>{value} 星以上</option>)}</select></label>
          <label className="text-sm font-semibold">到車站最多步行<select className={fieldClass} name="max_station_walk_minutes" defaultValue="10"><option value="">不限</option><option value="5">5 分鐘</option><option value="10">10 分鐘</option><option value="15">15 分鐘</option><option value="20">20 分鐘</option></select></label>
          <label className="text-sm font-semibold">每日步調<select className={fieldClass} name="pace" defaultValue="balanced"><option value="relaxed">悠閒 · 每天 1 個主要區域</option><option value="balanced">適中 · 每天 2 個主要區域</option><option value="packed">充實 · 每天 3 個主要區域</option></select></label>
          <div className="grid gap-3 text-sm sm:col-span-2 sm:grid-cols-2 lg:grid-cols-4">
            <label className="flex items-center gap-2 rounded-xl bg-white p-3"><input type="checkbox" name="avoid_red_eye" defaultChecked />避開紅眼航班</label>
            <label className="flex items-center gap-2 rounded-xl bg-white p-3"><input type="checkbox" name="breakfast_required" />住宿含早餐</label>
            <label className="flex items-center gap-2 rounded-xl bg-white p-3"><input type="checkbox" name="refundable_required" />住宿可免費取消</label>
            <label className="flex items-center gap-2 rounded-xl bg-white p-3"><input type="checkbox" name="include_airbnb" defaultChecked />準備 Airbnb 外站搜尋</label>
          </div>
        </div>
      </details>

      <button className="mt-5 flex w-full items-center justify-center gap-2 rounded-2xl bg-[var(--teal)] px-6 py-4 font-semibold text-white transition hover:-translate-y-0.5 hover:bg-[var(--teal-dark)] focus-visible:outline-none focus-visible:ring-4 focus-visible:ring-[var(--teal-soft)]">
        <PlaneTakeoff size={19} />比較完整旅程
      </button>
      <p className="mt-4 text-center text-xs leading-5 text-[var(--muted)]">正式環境只顯示已標明來源與擷取時間的報價；沒有金鑰時不會用模擬價格冒充即時結果。</p>
    </form>
  );
}
