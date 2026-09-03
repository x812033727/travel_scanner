"use client";

import { ArrowRight, CalendarDays, Check, ChevronLeft, ChevronRight, Hotel, MapPinned, Route, Sparkles, Users } from "lucide-react";
import { useRouter } from "@/i18n/navigation";
import { useEffect, useMemo, useRef, useState } from "react";
import { PlacePicker } from "@/components/place-picker";
import { useOperationCharge } from "@/components/usage-catalog-provider";
import { api, twd } from "@/lib/api";
import { trackAnalytics } from "@/lib/analytics";
import { interestLabel, interests } from "@/lib/destinations";

type CreatedTrip = { id: string };
type LodgingMode = "hotel" | "vacation_rental" | "both" | "any";
type Pace = "relaxed" | "balanced" | "packed";
type PlanningMode = "ai_draft" | "manual_blank";

const steps = ["基本資料", "旅伴預算", "住宿偏好", "路線與確認"];
const fieldClass = "mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-4 py-3 font-normal outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

function optionClass(active: boolean) {
  return `rounded-xl border px-3 py-3 text-left text-sm transition ${active ? "border-[var(--teal)] bg-[var(--teal-soft)] font-semibold text-[var(--teal-dark)]" : "border-[var(--line)] bg-white hover:border-[var(--teal)]"}`;
}

function optionalNumber(value: string) {
  const parsed = Number(value);
  return value && Number.isFinite(parsed) ? parsed : null;
}

function tripDayCount(start: string, end: string) {
  if (!start || !end || end < start) return 0;
  return Math.round((Date.parse(`${end}T00:00:00Z`) - Date.parse(`${start}T00:00:00Z`)) / 86_400_000) + 1;
}

const DRAFT_STORAGE_KEY = "mokaair-new-trip-draft";

type DraftSnapshot = {
  step: number;
  lodgingMode: LodgingMode;
  planningMode: PlanningMode;
  selectedInterests: string[];
  form: Record<string, string | boolean>;
};

function readDraft(): DraftSnapshot | undefined {
  try {
    const raw = window.sessionStorage.getItem(DRAFT_STORAGE_KEY);
    if (!raw) return undefined;
    const parsed: unknown = JSON.parse(raw);
    if (!parsed || typeof parsed !== "object") return undefined;
    return parsed as DraftSnapshot;
  } catch {
    return undefined;
  }
}

function clearDraft() {
  try {
    window.sessionStorage.removeItem(DRAFT_STORAGE_KEY);
  } catch {
    // storage may be unavailable; losing the draft is acceptable
  }
}

export function NewTripForm() {
  const router = useRouter();
  const aiCharge = useOperationCharge("ai_itinerary_generation");
  const optimizationCharge = useOperationCharge("itinerary_optimization");
  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [lodgingMode, setLodgingMode] = useState<LodgingMode>("any");
  const [planningMode, setPlanningMode] = useState<PlanningMode>("ai_draft");
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [form, setForm] = useState({
    name: "", destination_name: "", destination_place_id: "", start_date: "", end_date: "",
    adults: "2", children: "0", rooms: "1", budget_twd: "", pace: "balanced" as Pace,
    route_preference: "FEWER_TRANSFERS", nightly_min: "", nightly_max: "", hotel_min_rating: "",
    preferred_area: "", max_station_walk_minutes: "", min_review_score: "", min_review_count: "",
    breakfast_required: false, refundable_required: false, avoid_red_eye: true, notes: "",
  });
  const errorRef = useRef<HTMLParagraphElement>(null);
  // One key per creation attempt, kept across retries so a proxy timeout
  // followed by a second click replays the same trip instead of duplicating it.
  const submitKey = useRef<string | undefined>(undefined);
  const today = useMemo(() => new Date().toLocaleDateString("sv"), []);
  const days = tripDayCount(form.start_date, form.end_date);
  const travelerCount = Number(form.adults) + Number(form.children);

  const [draftReady, setDraftReady] = useState(false);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      const draft = readDraft();
      if (draft) {
        if (typeof draft.step === "number") setStep(Math.min(Math.max(draft.step, 0), steps.length - 1));
        if (draft.lodgingMode) setLodgingMode(draft.lodgingMode);
        if (draft.planningMode) setPlanningMode(draft.planningMode);
        if (Array.isArray(draft.selectedInterests)) setSelectedInterests(draft.selectedInterests.filter((code) => typeof code === "string"));
        if (draft.form && typeof draft.form === "object") {
          setForm((current) => {
            const next = { ...current };
            for (const key of Object.keys(current) as (keyof typeof current)[]) {
              const value = draft.form[key];
              if (typeof value === typeof current[key]) (next as Record<string, string | boolean>)[key] = value;
            }
            return next;
          });
        }
      }
      setDraftReady(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (!draftReady) return;
    try {
      window.sessionStorage.setItem(DRAFT_STORAGE_KEY, JSON.stringify({ step, lodgingMode, planningMode, selectedInterests, form } satisfies DraftSnapshot));
    } catch {
      // storage may be unavailable; autosave is best-effort
    }
  }, [draftReady, form, step, lodgingMode, planningMode, selectedInterests]);

  useEffect(() => {
    if (error) errorRef.current?.focus();
  }, [error]);
  const propertyTypes = lodgingMode === "hotel" ? ["hotel"] : lodgingMode === "vacation_rental" ? ["vacation_rental"] : lodgingMode === "both" ? ["hotel", "vacation_rental"] : [];
  const summary = useMemo(() => [
    days ? `${days} 天` : null,
    `${travelerCount} 位旅客・${form.rooms} 間房`,
    form.budget_twd ? `總預算 ${twd.format(Number(form.budget_twd))}` : "總預算不設限",
    lodgingMode === "hotel" ? "只住飯店" : lodgingMode === "vacation_rental" ? "公寓／民宿" : lodgingMode === "both" ? "飯店或民宿" : "住宿類型不拘",
    ...selectedInterests.map(interestLabel),
  ].filter(Boolean) as string[], [days, form.budget_twd, form.rooms, lodgingMode, selectedInterests, travelerCount]);
  const nightlyMin = optionalNumber(form.nightly_min);
  const nightlyMax = optionalNumber(form.nightly_max);
  const nightlyLabel = nightlyMin != null && nightlyMax != null
    ? `${twd.format(nightlyMin)}～${twd.format(nightlyMax)}`
    : nightlyMin != null ? `${twd.format(nightlyMin)} 起` : nightlyMax != null ? `${twd.format(nightlyMax)} 以下` : "不設限";
  const routeLabel = form.route_preference === "FASTEST" ? "最快抵達" : form.route_preference === "LESS_WALKING" ? "少走路" : "少轉乘";
  const paceLabel = form.pace === "relaxed" ? "悠閒" : form.pace === "packed" ? "充實" : "適中";
  const reviewDetails = [
    ["旅伴與房間", `${travelerCount} 位旅客・${form.rooms} 間房`],
    ["整趟總預算", form.budget_twd ? twd.format(Number(form.budget_twd)) : "不設限"],
    ["旅行步調", paceLabel],
    ["興趣", selectedInterests.length ? selectedInterests.map(interestLabel).join("、") : "不介意"],
    ["住宿類型", summary.find((item) => item.includes("飯店") || item.includes("民宿") || item.includes("住宿類型")) || "住宿類型不拘"],
    ["每晚住宿預算", nightlyLabel],
    ["最低星級", form.hotel_min_rating ? `${form.hotel_min_rating} 星以上` : "不介意"],
    ["偏好住宿區域", form.preferred_area.trim() || "不介意"],
    ["車站步行上限", form.max_station_walk_minutes ? `${form.max_station_walk_minutes} 分鐘` : "不介意"],
    ["最低住客評分", form.min_review_score ? `${form.min_review_score}+` : "不介意"],
    ["最低評論數", form.min_review_count ? `${form.min_review_count} 則以上` : "不介意"],
    ["早餐", form.breakfast_required ? "需要含早餐" : "不要求"],
    ["取消政策", form.refundable_required ? "需要免費取消" : "不要求"],
    ["大眾運輸", routeLabel],
    ["航班時間", form.avoid_red_eye ? "避開紅眼航班" : "可接受紅眼航班"],
    ["起始方式", planningMode === "manual_blank" ? "空白手動規劃" : "AI 可編輯草稿"],
  ];

  function update<K extends keyof typeof form>(key: K, value: (typeof form)[K]) {
    setError(undefined);
    setForm((current) => ({ ...current, [key]: value }));
  }

  function chooseLodgingMode(value: LodgingMode) {
    setError(undefined);
    setLodgingMode(value);
  }

  function choosePlanningMode(value: PlanningMode) {
    setError(undefined);
    setPlanningMode(value);
  }

  function validate(targetStep = 3) {
    if (targetStep >= 1) {
      if (!form.name.trim()) return "請輸入旅程名稱。";
      if (!form.destination_name.trim()) return "請輸入目的地。";
      if (!form.start_date || !form.end_date) return "請選擇開始與結束日期。";
      if (form.start_date < today) return "開始日期不可早於今天。";
      if (form.end_date < form.start_date) return "結束日期不可早於開始日期。";
      if (days > 61) return "行程最多可建立 61 天。";
    }
    if (targetStep >= 2) {
      if (Number(form.rooms) > travelerCount) return "房間數不可多於旅客人數。";
      if (form.budget_twd && Number(form.budget_twd) <= 0) return "總預算必須大於 0。";
    }
    if (targetStep >= 3) {
      const min = optionalNumber(form.nightly_min);
      const max = optionalNumber(form.nightly_max);
      if (min != null && max != null && min > max) return "每晚最低價格不可高於最高價格。";
    }
    return undefined;
  }

  function next() {
    const message = validate(step + 1);
    if (message) { setError(message); return; }
    setError(undefined);
    setStep((current) => Math.min(current + 1, steps.length - 1));
  }

  function toggleInterest(code: string) {
    setError(undefined);
    setSelectedInterests((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]);
  }

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = validate();
    if (message) { setError(message); return; }
    setBusy(true);
    setError(undefined);
    if (!submitKey.current) submitKey.current = crypto.randomUUID();
    try {
      const trip = await api<CreatedTrip>("/trips", {
        method: "POST",
        headers: { "Idempotency-Key": submitKey.current },
        body: JSON.stringify({
          source: "blank",
          planning_mode: planningMode,
          name: form.name.trim(),
          destination_name: form.destination_name.trim(),
          destination_place_id: form.destination_place_id || null,
          start_date: form.start_date,
          end_date: form.end_date,
          route_preference: form.route_preference,
          routing: {
            auto_compute: planningMode === "ai_draft",
            default_travel_mode: "transit",
            default_buffer_minutes: 10,
          },
          travelers: { adults: Number(form.adults), children: Number(form.children), rooms: Number(form.rooms) },
          preferences: {
            budget_twd: optionalNumber(form.budget_twd), avoid_red_eye: form.avoid_red_eye,
            hotel_min_rating: optionalNumber(form.hotel_min_rating),
            hotel_min_nightly_twd: optionalNumber(form.nightly_min), hotel_max_nightly_twd: optionalNumber(form.nightly_max),
            accepted_property_types: propertyTypes, hotel_min_review_score: optionalNumber(form.min_review_score),
            hotel_min_review_count: optionalNumber(form.min_review_count), breakfast_required: form.breakfast_required,
            refundable_required: form.refundable_required, max_station_walk_minutes: optionalNumber(form.max_station_walk_minutes),
            preferred_area: form.preferred_area.trim() || null, pace: form.pace, interests: selectedInterests,
          },
          notes: form.notes.trim() || null,
        }),
      });
      trackAnalytics("trip_created");
      clearDraft();
      submitKey.current = undefined;
      router.push(`/trips/${trip.id}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "建立行程失敗，請稍後再試。");
    } finally { setBusy(false); }
  }

  return <form onSubmit={submit} className="grid gap-6 lg:grid-cols-[1.1fr_.9fr]">
    <section className="rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8">
      <div className="mb-6 flex items-start gap-4"><span className="grid h-12 w-12 shrink-0 place-items-center rounded-2xl bg-[var(--teal-soft)] text-[var(--teal)]"><MapPinned size={23} /></span><div><p className="text-sm font-semibold text-[var(--teal)]">建立自己的行程</p><h1 className="mt-1 text-3xl font-bold">把旅行條件先說清楚，排程會更準</h1></div></div>
      <ol aria-label="建立步驟" className="mb-7 grid grid-cols-4 gap-1">{steps.map((label, index) => <li key={label} className={`rounded-xl px-1 py-2 text-center text-xs font-semibold ${index === step ? "bg-[var(--teal)] text-white" : index < step ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "bg-[var(--paper)] text-[var(--muted)]"}`}><span className="hidden sm:inline">{index + 1}. </span>{label}</li>)}</ol>

      <div className={step === 0 ? "grid gap-5" : "hidden"}>
        <label className="text-sm font-semibold">旅程名稱<input required maxLength={255} value={form.name} onChange={(event) => update("name", event.target.value)} placeholder="例如：東京五日賞楓" className={fieldClass} /></label>
        <div><label htmlFor="trip-destination" className="text-sm font-semibold">目的地</label><div className="mt-2"><PlacePicker inputId="trip-destination" label="目的地" descriptionId="trip-destination-help" value={form.destination_name} confirmed={Boolean(form.destination_place_id)} countryCodes={["jp", "kr", "th"]} kinds="cities" placeholder="搜尋城市，例如：東京、首爾、曼谷" onTextChange={(value) => setForm((current) => ({ ...current, destination_name: value, destination_place_id: "" }))} onSelect={(place) => setForm((current) => ({ ...current, destination_name: place.name, destination_place_id: place.place_id }))} /></div><p id="trip-destination-help" className="mt-1 text-xs font-normal text-[var(--muted)]">由 Google Maps 搜尋日本、韓國與泰國城市；未啟用服務時仍可直接輸入。</p></div>
        <div className="grid gap-4 sm:grid-cols-2"><label className="text-sm font-semibold">開始日期<input required type="date" min={today} value={form.start_date} onChange={(event) => { setError(undefined); setForm((current) => ({ ...current, start_date: event.target.value, end_date: current.end_date && current.end_date < event.target.value ? "" : current.end_date })); }} className={fieldClass} /></label><label className="text-sm font-semibold">結束日期<input required type="date" min={form.start_date || today} value={form.end_date} onChange={(event) => update("end_date", event.target.value)} className={fieldClass} /></label></div>
        {days > 0 && <p className="rounded-xl bg-[var(--paper)] px-4 py-3 text-sm">共 <strong>{days} 天</strong>，建立後會自動產生每天的行程區段。</p>}
      </div>

      <div className={step === 1 ? "grid gap-5" : "hidden"}>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Users size={19} />這趟有誰一起去？</h2><p className="mt-1 text-sm text-[var(--muted)]">人數會保留給之後的機票、住宿與預算計算。</p></div>
        <div className="grid grid-cols-3 gap-3"><label className="text-sm font-semibold">成人<select aria-label="成人" value={form.adults} onChange={(event) => update("adults", event.target.value)} className={fieldClass}>{[1,2,3,4,5,6,7,8,9].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">兒童<select aria-label="兒童" value={form.children} onChange={(event) => update("children", event.target.value)} className={fieldClass}>{[0,1,2,3,4,5].map((value) => <option key={value}>{value}</option>)}</select></label><label className="text-sm font-semibold">房間<select aria-label="房間" value={form.rooms} onChange={(event) => update("rooms", event.target.value)} className={fieldClass}>{[1,2,3,4].map((value) => <option key={value}>{value}</option>)}</select></label></div>
        <label className="text-sm font-semibold">整趟總預算 TWD<input type="number" min="1" value={form.budget_twd} onChange={(event) => update("budget_twd", event.target.value)} placeholder="我不介意" className={fieldClass} /></label>
        <div><p className="text-sm font-semibold">旅行步調</p><div className="mt-2 grid grid-cols-3 gap-2">{([['relaxed','悠閒'],['balanced','適中'],['packed','充實']] as const).map(([value,label]) => <button key={value} type="button" aria-pressed={form.pace === value} onClick={() => update("pace", value)} className={optionClass(form.pace === value)}>{label}</button>)}</div></div>
        <div><p className="text-sm font-semibold">感興趣的內容（可複選）</p><div className="mt-2 flex flex-wrap gap-2">{interests.map((interest) => <button key={interest.code} type="button" aria-pressed={selectedInterests.includes(interest.code)} onClick={() => toggleInterest(interest.code)} className={optionClass(selectedInterests.includes(interest.code))}>{interest.label}</button>)}</div></div>
      </div>

      <div className={step === 2 ? "grid gap-5" : "hidden"}>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Hotel size={19} />偏好什麼住宿？</h2><p className="mt-1 text-sm text-[var(--muted)]">不確定的條件保持空白即可，不會強迫篩掉結果。</p></div>
        <div className="grid grid-cols-2 gap-2">{([['hotel','只住飯店'],['vacation_rental','接受公寓／民宿'],['both','兩種都接受'],['any','我不介意']] as const).map(([value,label]) => <button key={value} type="button" aria-pressed={lodgingMode === value} onClick={() => chooseLodgingMode(value)} className={optionClass(lodgingMode === value)}>{label}</button>)}</div>
        <div className="grid grid-cols-2 gap-3"><label className="text-sm font-semibold">每晚最低 TWD<input aria-label="每晚最低 TWD" type="number" min="0" value={form.nightly_min} onChange={(event) => update("nightly_min", event.target.value)} placeholder="我不介意" className={fieldClass} /></label><label className="text-sm font-semibold">每晚最高 TWD<input aria-label="每晚最高 TWD" type="number" min="1" value={form.nightly_max} onChange={(event) => update("nightly_max", event.target.value)} placeholder="我不介意" className={fieldClass} /></label><label className="text-sm font-semibold">最低星級<select aria-label="最低星級" value={form.hotel_min_rating} onChange={(event) => update("hotel_min_rating", event.target.value)} className={fieldClass}><option value="">我不介意</option>{[3,4,5].map((value) => <option key={value} value={value}>{value} 星以上</option>)}</select></label><label className="text-sm font-semibold">車站步行上限<select aria-label="車站步行上限" value={form.max_station_walk_minutes} onChange={(event) => update("max_station_walk_minutes", event.target.value)} className={fieldClass}><option value="">我不介意</option>{[5,10,15,20].map((value) => <option key={value} value={value}>{value} 分鐘</option>)}</select></label><label className="text-sm font-semibold">最低住客評分<select aria-label="最低住客評分" value={form.min_review_score} onChange={(event) => update("min_review_score", event.target.value)} className={fieldClass}><option value="">我不介意</option><option value="7">7.0+</option><option value="8">8.0+</option><option value="9">9.0+</option></select></label><label className="text-sm font-semibold">最低評論數<select aria-label="最低評論數" value={form.min_review_count} onChange={(event) => update("min_review_count", event.target.value)} className={fieldClass}><option value="">我不介意</option>{[20,50,100,300].map((value) => <option key={value} value={value}>{value} 則以上</option>)}</select></label></div>
        <label className="text-sm font-semibold">偏好住宿區域<input value={form.preferred_area} onChange={(event) => update("preferred_area", event.target.value)} placeholder="我不介意，例如：新宿、近地鐵站" className={fieldClass} /></label>
        <div className="grid gap-2 text-sm sm:grid-cols-2"><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.breakfast_required} onChange={(event) => update("breakfast_required", event.target.checked)} />需要含早餐</label><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.refundable_required} onChange={(event) => update("refundable_required", event.target.checked)} />需要免費取消</label></div>
      </div>

      <div className={step === 3 ? "grid gap-5" : "hidden"}>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Check size={19} />路線偏好與建立前確認</h2><p className="mt-1 text-sm text-[var(--muted)]">選擇先由 AI 建立草稿，或從只有航班、住宿與餐期卡的空白行程開始。</p></div>
        <fieldset><legend className="text-sm font-semibold">建立方式</legend><div className="mt-2 grid gap-3 sm:grid-cols-2"><button type="button" aria-pressed={planningMode === "ai_draft"} onClick={() => choosePlanningMode("ai_draft")} className={optionClass(planningMode === "ai_draft")}><strong className="block">AI 可編輯草稿</strong><span className="mt-1 block text-xs font-normal leading-5 text-[var(--muted)]">使用核准景點先排出每天內容，建立後仍可修改。</span></button><button type="button" aria-pressed={planningMode === "manual_blank"} onClick={() => choosePlanningMode("manual_blank")} className={optionClass(planningMode === "manual_blank")}><strong className="block">空白手動規劃</strong><span className="mt-1 block text-xs font-normal leading-5 text-[var(--muted)]">不呼叫 AI；逐項新增時不自動查路，排完再集中計算。</span></button></div></fieldset>
        <div className="grid gap-3 sm:grid-cols-2"><label className="text-sm font-semibold">大眾運輸偏好<select value={form.route_preference} onChange={(event) => update("route_preference", event.target.value)} className={fieldClass}><option value="FEWER_TRANSFERS">少轉乘</option><option value="FASTEST">最快抵達</option><option value="LESS_WALKING">少走路</option></select></label><label className="flex items-center gap-2 self-end rounded-xl bg-[var(--paper)] p-3 text-sm"><input type="checkbox" checked={form.avoid_red_eye} onChange={(event) => update("avoid_red_eye", event.target.checked)} />之後搜尋時避開紅眼航班</label></div>
        <label className="text-sm font-semibold">其他補充<textarea rows={3} maxLength={1000} value={form.notes} onChange={(event) => update("notes", event.target.value)} placeholder="例如：有長輩同行、不要一直換飯店、想安排生日晚餐。" className={fieldClass} /></label>
        <section role="region" aria-label="完整行程條件" className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5"><p className="text-xs font-semibold text-[var(--teal)]">{form.start_date} → {form.end_date}</p><h3 className="mt-1 text-2xl font-bold">{form.name.trim()}</h3><p className="mt-1 text-sm text-[var(--muted)]">{form.destination_name.trim()}</p><dl className="mt-5 grid gap-x-5 gap-y-3 sm:grid-cols-2">{reviewDetails.map(([label, value]) => <div key={label} className="border-t border-[var(--line)] pt-3"><dt className="text-xs font-semibold text-[var(--muted)]">{label}</dt><dd className="mt-1 text-sm font-medium">{value}</dd></div>)}</dl>{form.notes.trim() && <div className="mt-4 border-t border-[var(--line)] pt-4"><p className="text-xs font-semibold text-[var(--muted)]">其他補充</p><p className="mt-1 whitespace-pre-wrap text-sm">{form.notes.trim()}</p></div>}</section>
        {planningMode === "ai_draft" ? <p className="rounded-xl bg-amber-50 px-4 py-3 text-xs leading-5 text-amber-900">建立時會把目的地、日期、人數、旅行偏好及補充說明傳給後台選定的 AI 供應商；不會傳送 Email、姓名或帳號識別資料。AI 內容是可編輯草稿，景點營業時間與預約仍需確認。</p> : <p className="rounded-xl bg-emerald-50 px-4 py-3 text-xs leading-5 text-emerald-900">空白手動規劃不會呼叫 AI。系統只建立每天必要的航班、住宿與餐期卡；完成景點順序後，再按「計算當日路線」取得交通資訊。</p>}
      </div>

      {error && <p ref={errorRef} tabIndex={-1} role="alert" aria-live="polite" className="mt-5 rounded-xl bg-red-50 p-4 text-sm text-red-800 outline-none">{error}</p>}
      <div className="mt-7 flex gap-3">{step > 0 && <button type="button" disabled={busy} onClick={() => { setError(undefined); setStep((current) => current - 1); }} className="flex items-center gap-1 rounded-xl border border-[var(--line)] px-4 py-3 font-semibold disabled:opacity-40"><ChevronLeft size={18} />上一步</button>}{step < steps.length - 1 ? <button key="next-trip-step" type="button" onClick={(event) => { event.preventDefault(); next(); }} className="ml-auto flex items-center gap-1 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white">下一步<ChevronRight size={18} /></button> : <button key="submit-trip" type="submit" disabled={busy} className="ml-auto flex items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white disabled:opacity-60">{busy ? planningMode === "manual_blank" ? "正在建立空白行程…" : "AI 正在安排每天行程…" : planningMode === "manual_blank" ? "建立空白手動行程" : "交給 AI 排好行程"}<ArrowRight size={18} /></button>}</div>
    </section>

    <aside className="rounded-[2rem] bg-[var(--ink)] p-6 text-white md:p-8">
      <p className="text-xs font-semibold tracking-[.18em] text-emerald-200">行程設定摘要</p><h2 className="mt-2 text-2xl font-bold">{form.destination_name.trim() || "還沒決定目的地"}</h2><div className="mt-5 flex flex-wrap gap-2">{summary.map((item) => <span key={item} className="rounded-full bg-white/10 px-3 py-1.5 text-xs text-white/80">{item}</span>)}</div>
      <div className="mt-7 space-y-5"><div className="flex gap-3"><CalendarDays className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">{planningMode === "manual_blank" ? "從空白時間軸開始" : "AI 安排每天的景點"}</h3><p className="mt-1 text-sm leading-6 text-white/65">{planningMode === "manual_blank" ? "只保留航班、住宿與餐期卡，由你逐日加入精準地點。" : "建立後每一天都有可編輯草稿，可再新增、鎖定或調整時間。"}</p></div></div><div className="flex gap-3"><Route className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">計算移動路線</h3><p className="mt-1 text-sm leading-6 text-white/65">{planningMode === "manual_blank" ? "排完當天順序後再按一次查路，避免每次新增都呼叫地圖服務。" : "確認地點後，依少轉乘、最快或少走路偏好規劃每一段交通。"}</p></div></div><div className="flex gap-3"><Sparkles className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">保留旅行偏好</h3><p className="mt-1 text-sm leading-6 text-white/65">旅伴、預算、住宿及興趣會保存，之後仍可選擇讓 AI 重新編排。</p></div></div></div>
      <p className="mt-8 rounded-2xl bg-white/10 p-4 text-sm leading-6 text-white/75">首次 AI 草稿、手動編排與查路免費；真實 AI 重排為{aiCharge.label}，成功套用整日動線最佳化為{optimizationCharge.label}，內建備援不扣次。</p>
    </aside>
  </form>;
}
