"use client";

import { CalendarDays, Check, ChevronLeft, ChevronRight, Hotel, LoaderCircle, MapPin, Sparkles, Users } from "lucide-react";
import { useRouter } from "@/i18n/navigation";
import { type FormEvent, useEffect, useMemo, useState } from "react";
import { api, twd } from "@/lib/api";
import { destinations, countries, interestLabel, interests, type CountryKey, type DestinationCity } from "@/lib/destinations";

const fieldClass = "mt-2 w-full rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-4 py-3 text-[var(--ink)] outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";
const steps = ["日期", "目的地", "旅伴", "住宿", "偏好"];

type Recommendation = {
  candidate_id: string; city: string; airport: string; country: string; country_code: CountryKey;
  areas: string[]; reason: string; departure_date: string; return_date: string;
  trip_length_days: number; estimated_flight_twd: number; estimated_lodging_twd: number;
  estimated_total_twd: number; score: number; matched_interests: string[]; relaxed_preferences: string[];
};
type DiscoveryResult = { recommendations: Recommendation[]; assumptions: string[] };
type CatalogDestination = {
  id: string; code: string; city: string; country_code: CountryKey; role: "primary" | "secondary" | "extension";
  parent_destination_id: string | null; gateway_codes: string[]; primary_gateway: string; areas: string[];
  recommended_days: { min: number; max: number }; timezone: string; currency: string; reason: string; searchable: boolean;
};
type CatalogResponse = { items: CatalogDestination[] };
type LodgingMode = "hotel" | "vacation_rental" | "both" | "any";

function futureDate(days: number) {
  const value = new Date(); value.setUTCDate(value.getUTCDate() + days);
  return value.toISOString().slice(0, 10);
}
function optionClass(active: boolean) {
  return `rounded-2xl border px-3 py-3 text-left transition ${active ? "border-[var(--teal)] bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "border-[var(--line)] bg-white hover:border-[var(--teal)]"}`;
}

export function SearchWorkbench() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [dateAny, setDateAny] = useState(false);
  const [lengthAny, setLengthAny] = useState(false);
  const [countriesSelected, setCountriesSelected] = useState<CountryKey[]>(["JP"]);
  const [destinationCode, setDestinationCode] = useState("");
  const [catalog, setCatalog] = useState<CatalogDestination[]>([]);
  const [selectedExtensions, setSelectedExtensions] = useState<string[]>([]);
  const [children, setChildren] = useState(0);
  const [childAges, setChildAges] = useState<number[]>([]);
  const [lodgingMode, setLodgingMode] = useState<LodgingMode>("hotel");
  const [selectedInterests, setSelectedInterests] = useState(["food", "shopping", "culture"]);
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [selectedAreas, setSelectedAreas] = useState<Record<string, string>>({});
  const [assumptions, setAssumptions] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  useEffect(() => {
    void api<CatalogResponse>("/destinations")
      .then((response) => setCatalog(response.items || []))
      .catch(() => undefined);
  }, []);
  const dynamicCities = useMemo<DestinationCity[]>(() => catalog.filter((item) => item.searchable).map((item) => ({
    id: item.id, country: item.country_code, name: item.city, airport: item.primary_gateway,
    airportName: item.gateway_codes.join("／"), summary: item.reason,
    recommendedStay: `${item.recommended_days.min}–${item.recommended_days.max} 天`, areas: item.areas,
    tags: item.role === "secondary" ? ["二線城市"] : [], timezone: item.timezone, currency: item.currency,
  })), [catalog]);
  const availableCities = useMemo(
    () => (dynamicCities.length ? dynamicCities : destinations).filter((item) => countriesSelected.includes(item.country)),
    [countriesSelected, dynamicCities],
  );
  const selectedDestination = catalog.find((item) => item.primary_gateway === destinationCode);
  const availableExtensions = catalog.filter((item) => item.parent_destination_id === selectedDestination?.id);

  function toggleCountry(country: CountryKey) {
    setCountriesSelected((current) => current.includes(country) ? current.filter((item) => item !== country) : [...current, country]);
    setDestinationCode("");
    setSelectedExtensions([]);
  }
  function changeChildren(count: number) {
    setChildren(count); setChildAges((current) => Array.from({ length: count }, (_, index) => current[index] ?? 8));
  }
  function toggleInterest(code: string) {
    setSelectedInterests((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]);
  }
  function propertyTypes() {
    if (lodgingMode === "hotel") return ["hotel"];
    if (lodgingMode === "vacation_rental") return ["vacation_rental"];
    if (lodgingMode === "both") return ["hotel", "vacation_rental"];
    return [];
  }

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const form = new FormData(event.currentTarget);
    const minDays = Number(form.get("min_days") || 0); const maxDays = Number(form.get("max_days") || 0);
    const startDate = String(form.get("window_start") || ""); const endDate = String(form.get("window_end") || "");
    if (!dateAny && (!startDate || !endDate || endDate <= startDate)) { setError("可旅行結束日必須晚於開始日。"); setStep(0); return; }
    if (!lengthAny && (!minDays || !maxDays || maxDays < minDays)) { setError("最長旅行天數不得少於最短天數。"); setStep(0); return; }
    const numberOrNull = (name: string) => { const value = Number(form.get(name) || 0); return value > 0 ? value : null; };
    setBusy(true); setError(undefined);
    try {
      const result = await api<DiscoveryResult>("/destinations/discover", { method: "POST", body: JSON.stringify({
        origin: String(form.get("origin") || "TPE"), destination_region: null,
        destination_countries: countriesSelected, destination_codes: destinationCode ? [destinationCode] : [],
        travel_window: dateAny ? null : { start_date: startDate, end_date: endDate },
        trip_length_range: lengthAny ? null : { min_days: minDays, max_days: maxDays },
        travelers: { adults: Number(form.get("adults") || 1), children, children_ages: childAges, rooms: Number(form.get("rooms") || 1) },
        budget_twd: numberOrNull("budget_twd"),
        lodging_preferences: { accepted_property_types: propertyTypes(), nightly_price_min_twd: numberOrNull("nightly_min"), nightly_price_max_twd: numberOrNull("nightly_max"), min_star_rating: numberOrNull("hotel_min_rating"), min_review_score: numberOrNull("min_review_score"), min_review_count: numberOrNull("min_review_count"), max_station_walk_minutes: numberOrNull("max_station_walk_minutes"), breakfast_required: form.get("breakfast_required") === "on" ? true : null, refundable_required: form.get("refundable_required") === "on" ? true : null },
        interests: selectedInterests, pace: String(form.get("pace") || "balanced"), notes: String(form.get("notes") || "") || null, top_n: 3,
      }) });
      setRecommendations(result.recommendations); setAssumptions(result.assumptions || []);
    } catch (reason) { setError((reason as Error).message); } finally { setBusy(false); }
  }

  function chooseRecommendation(item: Recommendation, form: HTMLFormElement) {
    const data = new FormData(form);
    const query = new URLSearchParams({ q: String(data.get("notes") || ""), country: item.country_code, origin: String(data.get("origin") || "TPE"), destination: item.airport, departure_date: item.departure_date, return_date: item.return_date, adults: String(data.get("adults") || "1"), children: String(children), children_ages: childAges.join(","), rooms: String(data.get("rooms") || "1"), interests: selectedInterests.join(","), pace: String(data.get("pace") || "balanced"), accepted_property_types: propertyTypes().join(","), preferred_areas: selectedAreas[item.candidate_id] || "", avoid_red_eye: String(data.get("avoid_red_eye") === "on"), breakfast_required: String(data.get("breakfast_required") === "on"), refundable_required: String(data.get("refundable_required") === "on"), include_airbnb: String(lodgingMode !== "hotel") });
    const recommendationProfile = catalog.find((profile) => profile.primary_gateway === item.airport);
    const validExtensions = selectedExtensions.filter((id) => catalog.find((profile) => profile.id === id)?.parent_destination_id === recommendationProfile?.id);
    if (validExtensions.length) query.set("extension_destination_ids", validExtensions.join(","));
    for (const [source, target] of [["budget_twd","budget_twd"],["nightly_min","hotel_min_nightly_twd"],["nightly_max","hotel_max_nightly_twd"],["hotel_min_rating","hotel_min_rating"],["min_review_score","hotel_min_review_score"],["min_review_count","hotel_min_review_count"],["max_station_walk_minutes","max_station_walk_minutes"]]) { const value = String(data.get(source) || ""); if (value) query.set(target, value); }
    router.push(`/search?${query.toString()}`);
  }

  return <form id="trip-search" onSubmit={submit} className="rounded-[2rem] border border-[var(--line)] bg-white p-5 shadow-[var(--shadow-lg)] md:p-7">
    <div className="mb-5"><p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />AI 選項式旅行規劃</p><h2 className="mt-1 text-2xl font-bold">不用寫完整句子，也能把條件說清楚</h2></div>
    <ol className="mb-6 grid grid-cols-5 gap-1" aria-label="規劃步驟">{steps.map((label, index) => <li key={label} className={`rounded-xl px-1 py-2 text-center text-xs font-semibold ${index === step ? "bg-[var(--teal)] text-white" : index < step ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "bg-[var(--paper)] text-[var(--muted)]"}`}><span className="hidden sm:inline">{index + 1}. </span>{label}</li>)}</ol>

    <section className={step === 0 ? "block" : "hidden"}><h3 className="flex items-center gap-2 text-lg font-bold"><CalendarDays size={19} />你大概什麼時候能出發？</h3><label className="mt-3 flex items-center gap-2 text-sm"><input type="checkbox" checked={dateAny} onChange={(event) => setDateAny(event.target.checked)} />日期我不介意（由 AI 看未來 30–180 天）</label><div className="mt-3 grid gap-3 sm:grid-cols-2"><label className="text-sm font-semibold">最早出發日<input disabled={dateAny} name="window_start" type="date" defaultValue={futureDate(30)} min={futureDate(1)} className={fieldClass} /></label><label className="text-sm font-semibold">最晚回程日<input disabled={dateAny} name="window_end" type="date" defaultValue={futureDate(120)} min={futureDate(3)} className={fieldClass} /></label></div><label className="mt-4 flex items-center gap-2 text-sm"><input type="checkbox" checked={lengthAny} onChange={(event) => setLengthAny(event.target.checked)} />旅行天數我不介意</label><div className="mt-3 grid grid-cols-2 gap-3"><label className="text-sm font-semibold">最短天數<select disabled={lengthAny} name="min_days" defaultValue="4" className={fieldClass}>{Array.from({ length: 12 }, (_, index) => index + 2).map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">最長天數<select disabled={lengthAny} name="max_days" defaultValue="6" className={fieldClass}>{Array.from({ length: 16 }, (_, index) => index + 2).map((value) => <option key={value}>{value}</option>)}</select></label></div></section>

    <section className={step === 1 ? "block" : "hidden"}><h3 className="flex items-center gap-2 text-lg font-bold"><MapPin size={19} />想去哪個國家？</h3><p className="mt-1 text-sm text-[var(--muted)]">可複選；全部取消就是「我不介意」。</p><div className="mt-4 grid grid-cols-3 gap-2">{countries.map((item) => <button key={item.key} type="button" aria-pressed={countriesSelected.includes(item.key)} onClick={() => toggleCountry(item.key)} className={optionClass(countriesSelected.includes(item.key))}><strong>{item.label}</strong><span className="mt-1 hidden text-xs sm:block">{item.caption}</span></button>)}</div><label className="mt-4 block text-sm font-semibold">指定城市（可不選）<select aria-label="指定城市" value={destinationCode} onChange={(event) => { setDestinationCode(event.target.value); setSelectedExtensions([]); }} className={fieldClass}><option value="">我不介意，讓 AI 推薦</option><optgroup label="主要與熱門城市">{availableCities.filter((city) => !city.tags.includes("二線城市")).map((city) => <option key={city.id} value={city.airport}>{city.name} · {city.airport}</option>)}</optgroup><optgroup label="二線城市">{availableCities.filter((city) => city.tags.includes("二線城市")).map((city) => <option key={city.id} value={city.airport}>{city.name} · {city.airport}</option>)}</optgroup></select></label>{availableExtensions.length > 0 && <fieldset className="mt-4 rounded-2xl border border-violet-200 bg-violet-50 p-4"><legend className="px-1 text-sm font-semibold">加入跨城延伸（至少四天）</legend><div className="mt-2 flex flex-wrap gap-2">{availableExtensions.map((item) => <label key={item.id} className="flex items-center gap-2 rounded-xl bg-white px-3 py-2 text-sm"><input type="checkbox" checked={selectedExtensions.includes(item.id)} onChange={(event) => setSelectedExtensions((current) => event.target.checked ? [...current, item.id].slice(0, 2) : current.filter((id) => id !== item.id))} />{item.city}</label>)}</div></fieldset>}</section>

    <section className={step === 2 ? "block" : "hidden"}><h3 className="flex items-center gap-2 text-lg font-bold"><Users size={19} />這趟有誰一起去？</h3><div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4"><label className="text-sm font-semibold">出發機場<select name="origin" defaultValue="TPE" className={fieldClass}><option value="TPE">桃園 TPE</option><option value="TSA">松山 TSA</option><option value="KHH">高雄 KHH</option></select></label><label className="text-sm font-semibold">成人<select name="adults" defaultValue="2" className={fieldClass}>{[1,2,3,4,5,6,7,8,9].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">兒童<select aria-label="兒童人數" value={children} onChange={(event) => changeChildren(Number(event.target.value))} className={fieldClass}>{[0,1,2,3,4].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">房間<select name="rooms" defaultValue="1" className={fieldClass}>{[1,2,3,4].map((value) => <option key={value}>{value}</option>)}</select></label></div>{children > 0 && <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">{childAges.map((age, index) => <label key={index} className="text-sm font-semibold">第 {index + 1} 位兒童年齡<select aria-label={`第 ${index + 1} 位兒童年齡`} value={age} onChange={(event) => setChildAges((current) => current.map((item, childIndex) => childIndex === index ? Number(event.target.value) : item))} className={fieldClass}>{Array.from({ length: 18 }, (_, value) => <option key={value} value={value}>{value} 歲</option>)}</select></label>)}</div>}<label className="mt-4 block text-sm font-semibold">整趟總預算 TWD（可留空）<input name="budget_twd" type="number" min="1" placeholder="我不介意" className={fieldClass} /></label></section>

    <section className={step === 3 ? "block" : "hidden"}><h3 className="flex items-center gap-2 text-lg font-bold"><Hotel size={19} />偏好什麼住宿？</h3><div className="mt-4 grid grid-cols-2 gap-2">{([['hotel','只住飯店'],['vacation_rental','整套公寓／民宿'],['both','兩種都接受'],['any','我不介意']] as const).map(([value,label]) => <button key={value} type="button" aria-pressed={lodgingMode === value} onClick={() => setLodgingMode(value)} className={optionClass(lodgingMode === value)}>{label}</button>)}</div><div className="mt-4 grid grid-cols-2 gap-3"><label className="text-sm font-semibold">每晚最低 TWD<input name="nightly_min" type="number" min="0" placeholder="我不介意" className={fieldClass} /></label><label className="text-sm font-semibold">每晚最高 TWD<input name="nightly_max" type="number" min="1" placeholder="我不介意" className={fieldClass} /></label><label className="text-sm font-semibold">最低星級<select name="hotel_min_rating" className={fieldClass}><option value="">我不介意</option>{[3,4,5].map((value) => <option key={value} value={value}>{value} 星以上</option>)}</select></label><label className="text-sm font-semibold">車站步行上限<select name="max_station_walk_minutes" className={fieldClass}><option value="">我不介意</option>{[5,10,15,20].map((value) => <option key={value} value={value}>{value} 分鐘</option>)}</select></label><label className="text-sm font-semibold">最低住客評分<select name="min_review_score" className={fieldClass}><option value="">我不介意</option><option value="7">7.0+</option><option value="8">8.0+</option><option value="9">9.0+</option></select></label><label className="text-sm font-semibold">最低評論筆數<select name="min_review_count" className={fieldClass}><option value="">我不介意</option>{[20,50,100,300].map((value) => <option key={value} value={value}>{value} 則以上</option>)}</select></label></div><div className="mt-4 grid gap-2 text-sm sm:grid-cols-2"><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" name="breakfast_required" />需要含早餐</label><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" name="refundable_required" />需要免費取消</label></div></section>

    <section className={step === 4 ? "block" : "hidden"}><h3 className="flex items-center gap-2 text-lg font-bold"><Sparkles size={19} />最後補上旅行偏好</h3><div className="mt-4 flex flex-wrap gap-2">{interests.map((interest) => <button key={interest.code} type="button" aria-pressed={selectedInterests.includes(interest.code)} onClick={() => toggleInterest(interest.code)} className={optionClass(selectedInterests.includes(interest.code))}>{interest.label}</button>)}</div><div className="mt-4 grid gap-3 sm:grid-cols-2"><label className="text-sm font-semibold">每日步調<select name="pace" defaultValue="balanced" className={fieldClass}><option value="relaxed">悠閒</option><option value="balanced">適中</option><option value="packed">充實</option></select></label><label className="mt-7 flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3 text-sm"><input type="checkbox" name="avoid_red_eye" defaultChecked />避開紅眼航班</label></div><label className="mt-4 block text-sm font-semibold">其他補充（可留空）<textarea name="notes" rows={3} placeholder="例如：想安排生日晚餐、不要一直換飯店。選項與文字衝突時，以選項為準。" className={fieldClass} /></label></section>

    {error && <p role="alert" className="mt-4 rounded-xl bg-red-50 p-3 text-sm font-medium text-red-700">{error}</p>}
    <div className="mt-5 flex gap-3">{step > 0 && <button type="button" onClick={() => setStep((value) => value - 1)} className="flex items-center gap-1 rounded-xl border border-[var(--line)] px-4 py-3 font-semibold"><ChevronLeft size={18} />上一步</button>}{step < steps.length - 1 ? <button type="button" onClick={() => setStep((value) => value + 1)} className="ml-auto flex items-center gap-1 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white">下一步<ChevronRight size={18} /></button> : <button disabled={busy} className="ml-auto flex items-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white disabled:opacity-60">{busy ? <LoaderCircle className="animate-spin" size={18} /> : <Sparkles size={18} />}請 AI 推薦 3 組</button>}</div>

    {recommendations.length > 0 && <section aria-labelledby="recommendations-title" className="mt-7 border-t border-[var(--line)] pt-6"><h3 id="recommendations-title" className="text-xl font-bold">AI 推薦的三組旅行</h3><p className="mt-1 text-sm text-[var(--muted)]">目前是估算與條件符合度；選定後才查即時供應資料。</p><div className="mt-4 grid gap-4">{recommendations.map((item, index) => <article key={item.candidate_id} className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4"><div className="flex items-start justify-between gap-3"><div><p className="text-xs font-semibold text-[var(--teal)]">{index === 0 ? "最佳建議" : `候選 ${index + 1}`} · 符合度 {item.score}%</p><h4 className="mt-1 text-xl font-bold">{item.country}・{item.city}</h4><p className="mt-1 text-sm text-[var(--muted)]">{item.departure_date} → {item.return_date} · {item.trip_length_days} 天</p></div><strong className="text-right text-lg">約 {twd.format(item.estimated_total_twd)}</strong></div><p className="mt-3 text-sm leading-6">{item.reason}</p><div className="mt-3 flex flex-wrap gap-2 text-xs"><span className="rounded-full bg-white px-2.5 py-1">機票估算 {twd.format(item.estimated_flight_twd)}</span><span className="rounded-full bg-white px-2.5 py-1">住宿估算 {twd.format(item.estimated_lodging_twd)}</span>{item.matched_interests.map((interest) => <span key={interest} className="rounded-full bg-[var(--teal-soft)] px-2.5 py-1">符合{interestLabel(interest)}</span>)}</div>{item.relaxed_preferences.length > 0 && <p className="mt-3 text-xs text-amber-800">需確認：{item.relaxed_preferences.join("、")}</p>}<label className="mt-3 block text-sm font-semibold">偏好住宿區域<select value={selectedAreas[item.candidate_id] || ""} onChange={(event) => setSelectedAreas((current) => ({ ...current, [item.candidate_id]: event.target.value }))} className={fieldClass}><option value="">我不介意</option>{item.areas.map((area) => <option key={area}>{area}</option>)}</select></label><button type="button" onClick={(event) => chooseRecommendation(item, event.currentTarget.form!)} className="mt-4 flex w-full items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-4 py-3 font-semibold text-white"><Check size={18} />用這組條件搜尋</button></article>)}</div>{assumptions.map((item) => <p key={item} className="mt-2 text-xs text-[var(--muted)]">・{item}</p>)}</section>}
    <p className="mt-4 text-center text-xs leading-5 text-[var(--muted)]">公寓／民宿只顯示實際 Provider 回傳資料，不直接爬取 Airbnb，也不以模擬資料冒充即時庫存。</p>
  </form>;
}
