"use client";

import { ArrowRight, CalendarDays, Check, ChevronLeft, ChevronRight, Hotel, MapPinned, Route, Sparkles, Users } from "lucide-react";
import { useRouter } from "next/navigation";
import { useMemo, useState } from "react";
import { PlacePicker } from "@/components/place-picker";
import { api, twd } from "@/lib/api";
import { interestLabel, interests } from "@/lib/destinations";

type CreatedTrip = { id: string };
type LodgingMode = "hotel" | "vacation_rental" | "both" | "any";
type Pace = "relaxed" | "balanced" | "packed";

const steps = ["基本資料", "旅伴預算", "住宿偏好", "確認建立"];
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

export function NewTripForm() {
  const router = useRouter();
  const [step, setStep] = useState(0);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [lodgingMode, setLodgingMode] = useState<LodgingMode>("any");
  const [selectedInterests, setSelectedInterests] = useState<string[]>([]);
  const [form, setForm] = useState({
    name: "", destination_name: "", destination_place_id: "", start_date: "", end_date: "",
    adults: "2", children: "0", rooms: "1", budget_twd: "", pace: "balanced" as Pace,
    route_preference: "FEWER_TRANSFERS", nightly_min: "", nightly_max: "", hotel_min_rating: "",
    preferred_area: "", max_station_walk_minutes: "", min_review_score: "", min_review_count: "",
    breakfast_required: false, refundable_required: false, avoid_red_eye: true, notes: "",
  });
  const days = tripDayCount(form.start_date, form.end_date);
  const travelerCount = Number(form.adults) + Number(form.children);
  const propertyTypes = lodgingMode === "hotel" ? ["hotel"] : lodgingMode === "vacation_rental" ? ["vacation_rental"] : lodgingMode === "both" ? ["hotel", "vacation_rental"] : [];
  const summary = useMemo(() => [
    days ? `${days} 天` : null,
    `${travelerCount} 位旅客・${form.rooms} 間房`,
    form.budget_twd ? `總預算 ${twd.format(Number(form.budget_twd))}` : "總預算不設限",
    lodgingMode === "hotel" ? "只住飯店" : lodgingMode === "vacation_rental" ? "公寓／民宿" : lodgingMode === "both" ? "飯店或民宿" : "住宿類型不拘",
    ...selectedInterests.map(interestLabel),
  ].filter(Boolean) as string[], [days, form.budget_twd, form.rooms, lodgingMode, selectedInterests, travelerCount]);

  function update<K extends keyof typeof form>(key: K, value: (typeof form)[K]) {
    setForm((current) => ({ ...current, [key]: value }));
  }

  function validate(targetStep = 3) {
    if (targetStep >= 1) {
      if (!form.name.trim()) return "請輸入旅程名稱。";
      if (!form.destination_name.trim()) return "請輸入目的地。";
      if (!form.start_date || !form.end_date) return "請選擇開始與結束日期。";
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
    setSelectedInterests((current) => current.includes(code) ? current.filter((item) => item !== code) : [...current, code]);
  }

  async function submit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const message = validate();
    if (message) { setError(message); return; }
    setBusy(true);
    setError(undefined);
    try {
      const trip = await api<CreatedTrip>("/trips", {
        method: "POST",
        body: JSON.stringify({
          source: "blank",
          name: form.name.trim(),
          destination_name: form.destination_name.trim(),
          destination_place_id: form.destination_place_id || null,
          start_date: form.start_date,
          end_date: form.end_date,
          route_preference: form.route_preference,
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
        <label className="text-sm font-semibold">目的地<div className="mt-2"><PlacePicker value={form.destination_name} confirmed={Boolean(form.destination_place_id)} countryCodes={["jp", "kr", "th"]} onTextChange={(value) => setForm((current) => ({ ...current, destination_name: value, destination_place_id: "" }))} onSelect={(place) => setForm((current) => ({ ...current, destination_name: place.name, destination_place_id: place.place_id }))} /></div><span className="mt-1 block text-xs font-normal text-[var(--muted)]">由 Google Maps 搜尋日本、韓國與泰國城市；未啟用服務時仍可直接輸入。</span></label>
        <div className="grid gap-4 sm:grid-cols-2"><label className="text-sm font-semibold">開始日期<input required type="date" value={form.start_date} onChange={(event) => setForm((current) => ({ ...current, start_date: event.target.value, end_date: current.end_date && current.end_date < event.target.value ? "" : current.end_date }))} className={fieldClass} /></label><label className="text-sm font-semibold">結束日期<input required type="date" min={form.start_date} value={form.end_date} onChange={(event) => update("end_date", event.target.value)} className={fieldClass} /></label></div>
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
        <div className="grid grid-cols-2 gap-2">{([['hotel','只住飯店'],['vacation_rental','接受公寓／民宿'],['both','兩種都接受'],['any','我不介意']] as const).map(([value,label]) => <button key={value} type="button" aria-pressed={lodgingMode === value} onClick={() => setLodgingMode(value)} className={optionClass(lodgingMode === value)}>{label}</button>)}</div>
        <div className="grid grid-cols-2 gap-3"><label className="text-sm font-semibold">每晚最低 TWD<input aria-label="每晚最低 TWD" type="number" min="0" value={form.nightly_min} onChange={(event) => update("nightly_min", event.target.value)} placeholder="我不介意" className={fieldClass} /></label><label className="text-sm font-semibold">每晚最高 TWD<input aria-label="每晚最高 TWD" type="number" min="1" value={form.nightly_max} onChange={(event) => update("nightly_max", event.target.value)} placeholder="我不介意" className={fieldClass} /></label><label className="text-sm font-semibold">最低星級<select aria-label="最低星級" value={form.hotel_min_rating} onChange={(event) => update("hotel_min_rating", event.target.value)} className={fieldClass}><option value="">我不介意</option>{[3,4,5].map((value) => <option key={value} value={value}>{value} 星以上</option>)}</select></label><label className="text-sm font-semibold">車站步行上限<select aria-label="車站步行上限" value={form.max_station_walk_minutes} onChange={(event) => update("max_station_walk_minutes", event.target.value)} className={fieldClass}><option value="">我不介意</option>{[5,10,15,20].map((value) => <option key={value} value={value}>{value} 分鐘</option>)}</select></label><label className="text-sm font-semibold">最低住客評分<select aria-label="最低住客評分" value={form.min_review_score} onChange={(event) => update("min_review_score", event.target.value)} className={fieldClass}><option value="">我不介意</option><option value="7">7.0+</option><option value="8">8.0+</option><option value="9">9.0+</option></select></label><label className="text-sm font-semibold">最低評論數<select aria-label="最低評論數" value={form.min_review_count} onChange={(event) => update("min_review_count", event.target.value)} className={fieldClass}><option value="">我不介意</option>{[20,50,100,300].map((value) => <option key={value} value={value}>{value} 則以上</option>)}</select></label></div>
        <label className="text-sm font-semibold">偏好住宿區域<input value={form.preferred_area} onChange={(event) => update("preferred_area", event.target.value)} placeholder="我不介意，例如：新宿、近地鐵站" className={fieldClass} /></label>
        <div className="grid gap-2 text-sm sm:grid-cols-2"><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.breakfast_required} onChange={(event) => update("breakfast_required", event.target.checked)} />需要含早餐</label><label className="flex items-center gap-2 rounded-xl bg-[var(--paper)] p-3"><input type="checkbox" checked={form.refundable_required} onChange={(event) => update("refundable_required", event.target.checked)} />需要免費取消</label></div>
      </div>

      <div className={step === 3 ? "grid gap-5" : "hidden"}>
        <div><h2 className="flex items-center gap-2 text-lg font-bold"><Check size={19} />建立前確認</h2><p className="mt-1 text-sm text-[var(--muted)]">這些條件會一起保存，之後排景點與查價格時可以沿用。</p></div>
        <div className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5"><p className="text-xs font-semibold text-[var(--teal)]">{form.start_date} → {form.end_date}</p><h3 className="mt-1 text-2xl font-bold">{form.name.trim()}</h3><p className="mt-1 text-sm text-[var(--muted)]">{form.destination_name.trim()}</p><div className="mt-4 flex flex-wrap gap-2">{summary.map((item) => <span key={item} className="rounded-full bg-white px-3 py-1.5 text-xs font-medium">{item}</span>)}</div></div>
        <div className="grid gap-3 sm:grid-cols-2"><label className="text-sm font-semibold">大眾運輸偏好<select value={form.route_preference} onChange={(event) => update("route_preference", event.target.value)} className={fieldClass}><option value="FEWER_TRANSFERS">少轉乘</option><option value="FASTEST">最快抵達</option><option value="LESS_WALKING">少走路</option></select></label><label className="flex items-center gap-2 self-end rounded-xl bg-[var(--paper)] p-3 text-sm"><input type="checkbox" checked={form.avoid_red_eye} onChange={(event) => update("avoid_red_eye", event.target.checked)} />之後搜尋時避開紅眼航班</label></div>
        <label className="text-sm font-semibold">其他補充<textarea rows={3} maxLength={1000} value={form.notes} onChange={(event) => update("notes", event.target.value)} placeholder="例如：有長輩同行、不要一直換飯店、想安排生日晚餐。" className={fieldClass} /></label>
      </div>

      {error && <p role="alert" aria-live="polite" className="mt-5 rounded-xl bg-red-50 p-4 text-sm text-red-800">{error}</p>}
      <div className="mt-7 flex gap-3">{step > 0 && <button type="button" onClick={() => { setError(undefined); setStep((current) => current - 1); }} className="flex items-center gap-1 rounded-xl border border-[var(--line)] px-4 py-3 font-semibold"><ChevronLeft size={18} />上一步</button>}{step < steps.length - 1 ? <button type="button" onClick={next} className="ml-auto flex items-center gap-1 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white">下一步<ChevronRight size={18} /></button> : <button type="submit" disabled={busy} className="ml-auto flex items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white disabled:opacity-60">{busy ? "建立中…" : "建立行程並開始編排"}<ArrowRight size={18} /></button>}</div>
    </section>

    <aside className="rounded-[2rem] bg-[var(--ink)] p-6 text-white md:p-8">
      <p className="text-xs font-semibold tracking-[.18em] text-emerald-200">行程設定摘要</p><h2 className="mt-2 text-2xl font-bold">{form.destination_name.trim() || "還沒決定目的地"}</h2><div className="mt-5 flex flex-wrap gap-2">{summary.map((item) => <span key={item} className="rounded-full bg-white/10 px-3 py-1.5 text-xs text-white/80">{item}</span>)}</div>
      <div className="mt-7 space-y-5"><div className="flex gap-3"><CalendarDays className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">安排每天的景點</h3><p className="mt-1 text-sm leading-6 text-white/65">建立後會按日期展開，可新增地點、停留時間與固定預約。</p></div></div><div className="flex gap-3"><Route className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">計算移動路線</h3><p className="mt-1 text-sm leading-6 text-white/65">依少轉乘、最快或少走路偏好規劃每一段交通。</p></div></div><div className="flex gap-3"><Sparkles className="mt-0.5 shrink-0 text-emerald-200" size={21} /><div><h3 className="font-semibold">保留給 AI 與價格搜尋</h3><p className="mt-1 text-sm leading-6 text-white/65">旅伴、預算、住宿及興趣會保存，不必每次重新輸入。</p></div></div></div>
      <p className="mt-8 rounded-2xl bg-white/10 p-4 text-sm leading-6 text-white/75">手動編排行程與查路免費；只有成功套用整日自動最佳化才扣 1 次。</p>
    </aside>
  </form>;
}
