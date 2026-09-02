"use client";

import { AlertCircle, CalendarPlus, Check, Heart, LoaderCircle, LogIn, Share2, X } from "lucide-react";
import { useLocale } from "next-intl";
import { useState } from "react";
import { Link, usePathname } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { useSavedItems } from "@/components/saved-items-provider";

type SavedType = "hotspot" | "food";
type TripOption = {
  trip_id: string;
  name: string;
  version: number;
  start_date: string;
  end_date: string;
  destination_name?: string | null;
};
const labels = {
  "zh-TW": {
    save: "收藏",
    saved: "已收藏",
    add: "加入行程",
    share: "分享",
    login: "登入後繼續使用此功能",
    loginAction: "前往登入",
    close: "關閉",
    trip: "選擇旅程",
    date: "安排日期",
    meal: "用餐時段",
    lunch: "午餐",
    dinner: "晚餐",
    confirm: "加入",
    done: "已加入行程",
    empty: "尚未有可用旅程，請先建立旅程。",
  },
  "zh-CN": {
    save: "收藏",
    saved: "已收藏",
    add: "加入行程",
    share: "分享",
    login: "登录后继续使用此功能",
    loginAction: "前往登录",
    close: "关闭",
    trip: "选择旅程",
    date: "安排日期",
    meal: "用餐时段",
    lunch: "午餐",
    dinner: "晚餐",
    confirm: "加入",
    done: "已加入行程",
    empty: "尚无可用旅程，请先创建旅程。",
  },
  en: {
    save: "Save",
    saved: "Saved",
    add: "Add to trip",
    share: "Share",
    login: "Sign in to continue",
    loginAction: "Sign in",
    close: "Close",
    trip: "Choose a trip",
    date: "Date",
    meal: "Meal",
    lunch: "Lunch",
    dinner: "Dinner",
    confirm: "Add",
    done: "Added to trip",
    empty: "Create a trip first.",
  },
  ja: {
    save: "保存",
    saved: "保存済み",
    add: "旅程に追加",
    share: "共有",
    login: "ログインして続行",
    loginAction: "ログイン",
    close: "閉じる",
    trip: "旅行を選択",
    date: "日付",
    meal: "食事",
    lunch: "昼食",
    dinner: "夕食",
    confirm: "追加",
    done: "旅程に追加しました",
    empty: "先に旅行を作成してください。",
  },
  ko: {
    save: "저장",
    saved: "저장됨",
    add: "여행에 추가",
    share: "공유",
    login: "로그인하여 계속하기",
    loginAction: "로그인",
    close: "닫기",
    trip: "여행 선택",
    date: "날짜",
    meal: "식사",
    lunch: "점심",
    dinner: "저녁",
    confirm: "추가",
    done: "여행에 추가됨",
    empty: "먼저 여행을 만들어 주세요.",
  },
} as const;

export function TravelCardActions({
  type,
  id,
  title,
  selectionPath,
  merchantId,
  shareRequiresAuth = false,
}: {
  type: SavedType;
  id: string;
  title: string;
  selectionPath: string;
  merchantId?: string;
  shareRequiresAuth?: boolean;
}) {
  const locale = useLocale() as keyof typeof labels;
  const text = labels[locale] ?? labels.en;
  const savedItems = useSavedItems();
  const pathname = usePathname();
  const saved = savedItems.isSaved(type, id);
  const [sheet, setSheet] = useState<"login" | "trip" | null>(null);
  const [trips, setTrips] = useState<TripOption[]>([]);
  const [tripId, setTripId] = useState("");
  const [dayDate, setDayDate] = useState("");
  const [mealRole, setMealRole] = useState<"lunch" | "dinner">("lunch");
  const [busy, setBusy] = useState(false);
  const [saving, setSaving] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");
  const [loginHref, setLoginHref] = useState(() => loginPath(pathname));

  function clearFeedback() {
    setNotice("");
    setError("");
  }

  function requireAuth(action: () => void) {
    if (savedItems.status !== "authenticated") {
      setLoginHref(loginPath(`${pathname}${window.location.search}`));
      setSheet("login");
    }
    else action();
  }
  async function openTrip() {
    clearFeedback();
    setSheet("trip");
    setBusy(true);
    try {
      const result = await api<{ items: TripOption[] }>("/trips/options");
      setTrips(result.items);
      const first = result.items[0];
      if (first) {
        setTripId(first.trip_id);
        setDayDate(first.start_date);
      }
    } catch (reason) {
      setSheet(null);
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function submitTrip() {
    const trip = trips.find((item) => item.trip_id === tripId);
    if (!trip || !dayDate) return;
    setBusy(true);
    clearFeedback();
    try {
      await api(selectionPath, {
        method: "POST",
        body: JSON.stringify({
          trip_id: trip.trip_id,
          version: trip.version,
          day_date: dayDate,
          ...(merchantId
            ? { merchant_id: merchantId, meal_role: mealRole }
            : {}),
        }),
      });
      setNotice(text.done);
      setSheet(null);
      window.setTimeout(() => setNotice(""), 2200);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }
  async function share() {
    clearFeedback();
    try {
      const url = window.location.href;
      if (navigator.share) await navigator.share({ title, url });
      else {
        await navigator.clipboard.writeText(url);
        setNotice(text.share);
        window.setTimeout(() => setNotice(""), 1600);
      }
    } catch (reason) {
      if ((reason as DOMException).name !== "AbortError") setError((reason as Error).message);
    }
  }
  async function toggleSaved() {
    setSaving(true);
    clearFeedback();
    try {
      await savedItems.toggle(type, id);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }
  return (
    <>
      <div className="travel-card-actions" aria-label={`${title} actions`}>
        <button
          type="button"
          aria-pressed={saved}
          disabled={saving}
          onClick={() => requireAuth(() => void toggleSaved())}
          className={
            saved
              ? "travel-card-action travel-card-action-active"
              : "travel-card-action"
          }
        >
          {saving ? <LoaderCircle className="animate-spin" size={18} /> : <Heart size={18} fill={saved ? "currentColor" : "none"} />}
          <span>{saved ? text.saved : text.save}</span>
        </button>
        <button
          type="button"
          disabled={type === "food" && !merchantId}
          onClick={() => requireAuth(() => void openTrip())}
          className="travel-card-action disabled:cursor-not-allowed disabled:opacity-35"
        >
          <CalendarPlus size={18} />
          <span>{text.add}</span>
        </button>
        <button
          type="button"
          disabled={shareRequiresAuth && savedItems.status === "loading"}
          onClick={() => shareRequiresAuth ? requireAuth(() => void share()) : void share()}
          className="travel-card-action disabled:cursor-wait disabled:opacity-60"
        >
          <Share2 size={18} />
          <span>{text.share}</span>
        </button>
      </div>
      {notice && (
        <div role="status" className="app-toast">
          <Check size={17} />
          {notice}
        </div>
      )}
      {error && <div role="alert" className="app-toast app-toast-error"><AlertCircle size={17} />{error}</div>}
      {sheet && (
        <div
          className="app-sheet-backdrop"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) setSheet(null);
          }}
        >
          <section
            role="dialog"
            aria-modal="true"
            aria-label={sheet === "login" ? text.login : text.trip}
            className="app-sheet"
          >
            <div className="app-sheet-handle" />
            <button
              type="button"
              aria-label={text.close}
              onClick={() => setSheet(null)}
              className="absolute right-4 top-4 grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]"
            >
              <X size={20} />
            </button>
            {sheet === "login" ? (
              <div className="py-8 text-center">
                <LogIn className="mx-auto text-[var(--teal)]" size={30} />
                <h3 className="mt-4 text-xl font-bold">{text.login}</h3>
                <Link
                  href={loginHref}
                  className="mt-6 inline-flex min-h-12 items-center rounded-2xl bg-[var(--teal)] px-6 font-bold text-white"
                >
                  {text.loginAction}
                </Link>
              </div>
            ) : (
              <div className="pt-4">
                <h3 className="pr-12 text-2xl font-bold">{text.add}</h3>
                {busy && trips.length === 0 ? (
                  <p className="mt-5 text-[var(--muted)]">…</p>
                ) : trips.length === 0 ? (
                  <p className="mt-5 rounded-2xl bg-[var(--paper)] p-4">
                    {text.empty}
                  </p>
                ) : (
                  <div className="mt-5 grid gap-4">
                    <label className="grid gap-2 text-sm font-bold">
                      {text.trip}
                      <select
                        value={tripId}
                        onChange={(event) => {
                          const trip = trips.find(
                            (item) => item.trip_id === event.target.value,
                          );
                          setTripId(event.target.value);
                          if (trip) setDayDate(trip.start_date);
                        }}
                        className="app-field"
                      >
                        {trips.map((trip) => (
                          <option key={trip.trip_id} value={trip.trip_id}>
                            {trip.name}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label className="grid gap-2 text-sm font-bold">
                      {text.date}
                      <input
                        type="date"
                        value={dayDate}
                        min={
                          trips.find((item) => item.trip_id === tripId)
                            ?.start_date
                        }
                        max={
                          trips.find((item) => item.trip_id === tripId)
                            ?.end_date
                        }
                        onChange={(event) => setDayDate(event.target.value)}
                        className="app-field"
                      />
                    </label>
                    {merchantId && (
                      <label className="grid gap-2 text-sm font-bold">
                        {text.meal}
                        <select
                          value={mealRole}
                          onChange={(event) =>
                            setMealRole(
                              event.target.value as "lunch" | "dinner",
                            )
                          }
                          className="app-field"
                        >
                          <option value="lunch">{text.lunch}</option>
                          <option value="dinner">{text.dinner}</option>
                        </select>
                      </label>
                    )}
                    <button
                      type="button"
                      disabled={busy}
                      onClick={() => void submitTrip()}
                      className="min-h-12 rounded-2xl bg-[var(--teal)] px-5 font-bold text-white disabled:opacity-50"
                    >
                      {text.confirm}
                    </button>
                  </div>
                )}
              </div>
            )}
          </section>
        </div>
      )}
    </>
  );
}
