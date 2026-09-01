"use client";

import {
  Bell,
  LoaderCircle,
  Luggage,
  Pause,
  Pencil,
  Play,
  Plus,
  RotateCw,
  Trash2,
  X,
} from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useCallback, useEffect, useState } from "react";
import { ApiError, api, twd } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { PriceAlertButton } from "@/components/price-alert-button";
import { formatCurrency } from "@/lib/locale-format";

type TripItem = {
  id: string;
  name: string;
  total_price?: number;
  currency?: string;
  destination_name?: string;
  start_date?: string;
  end_date?: string;
};
type AlertItem = {
  id: string;
  resource_type: "flight" | "hotel" | "trip";
  resource_id: string;
  title: string;
  subtitle?: string | null;
  target_price?: number | null;
  current_price?: number | null;
  currency: string;
  price_updated_at?: string | null;
  active: boolean;
  monitoring_mode?: "automatic" | "manual_only";
  monitoring_status?: string;
  last_checked_at?: string | null;
  next_check_at?: string | null;
};
type LoadFailure = { message: string; status?: number };

function money(value: number, currency: string) {
  return formatCurrency(value, currency);
}

function LoadError({
  error,
  path,
  retry,
}: {
  error: LoadFailure;
  path: string;
  retry: () => void;
}) {
  if (error.status === 401)
    return (
      <div className="rounded-2xl border border-[var(--line)] bg-white p-7 text-center">
        <p className="font-semibold">登入後才能查看這裡的內容</p>
        <Link
          href={loginPath(path)}
          className="mt-4 inline-flex rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white"
        >
          前往登入
        </Link>
      </div>
    );
  const detail =
    error.status === 403
      ? "目前帳號沒有查看這些資料的權限。"
      : "服務暫時無法載入資料，請稍後再試。";
  return (
    <div role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">
      <p className="font-semibold">{detail}</p>
      <p className="mt-1 text-sm">{error.message}</p>
      <button
        type="button"
        onClick={retry}
        className="mt-4 inline-flex items-center gap-2 rounded-xl border border-red-200 bg-white px-4 py-2 text-sm font-semibold"
      >
        <RotateCw size={15} />
        重新載入
      </button>
    </div>
  );
}

export function AccountList({ kind }: { kind: "trips" | "alerts" }) {
  const [items, setItems] = useState<Array<TripItem | AlertItem>>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<LoadFailure>();
  const [pendingDelete, setPendingDelete] = useState<string>();
  const [rowError, setRowError] = useState<Record<string, string>>({});
  const [editing, setEditing] = useState<string>();
  const [draftPrice, setDraftPrice] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError(undefined);
    try {
      setItems(await api<Array<TripItem | AlertItem>>(`/${kind}`));
    } catch (reason) {
      setError({
        message: (reason as Error).message,
        status:
          reason instanceof ApiError
            ? reason.status
            : (reason as { status?: number }).status,
      });
    } finally {
      setLoading(false);
    }
  }, [kind]);
  useEffect(() => {
    void load();
  }, [load]);

  async function remove(id: string) {
    setRowError((current) => ({ ...current, [id]: "" }));
    try {
      await api(`/${kind}/${id}`, { method: "DELETE" });
      setItems((current) => current.filter((item) => item.id !== id));
      setPendingDelete(undefined);
    } catch (reason) {
      setRowError((current) => ({
        ...current,
        [id]: (reason as Error).message,
      }));
    }
  }

  async function patchAlert(
    item: AlertItem,
    patch: { target_price?: number | null; active?: boolean },
  ) {
    setRowError((current) => ({ ...current, [item.id]: "" }));
    try {
      const updated = await api<AlertItem>(`/alerts/${item.id}`, {
        method: "PATCH",
        body: JSON.stringify(patch),
      });
      setItems((current) =>
        current.map((row) => (row.id === item.id ? updated : row)),
      );
      setEditing(undefined);
    } catch (reason) {
      setRowError((current) => ({
        ...current,
        [item.id]: (reason as Error).message,
      }));
    }
  }

  if (loading)
    return (
      <p
        role="status"
        className="flex items-center justify-center gap-2 rounded-2xl border border-[var(--line)] bg-white p-10 text-[var(--muted)]"
      >
        <LoaderCircle className="animate-spin" size={19} />
        正在載入…
      </p>
    );
  if (error)
    return (
      <LoadError
        error={error}
        path={kind === "trips" ? "/trips" : "/alerts"}
        retry={load}
      />
    );
  if (!items.length)
    return (
      <div className="rounded-[2rem] border border-dashed border-[var(--line)] bg-white p-12 text-center text-[var(--muted)]">
        {kind === "trips" ? (
          <Luggage className="mx-auto mb-3" />
        ) : (
          <Bell className="mx-auto mb-3" />
        )}
        目前還沒有{kind === "trips" ? "已儲存旅程" : "價格通知"}。
        {kind === "trips" && (
          <div>
            <Link
              href="/trips/new"
              className="mt-5 inline-flex items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white"
            >
              <Plus size={16} />
              建立第一個行程
            </Link>
          </div>
        )}
      </div>
    );

  return (
    <div className="space-y-3">
      {items.map((row) => {
        const isAlert = kind === "alerts";
        const alert = row as AlertItem;
        const trip = row as TripItem;
        return (
          <article
            key={row.id}
            className="rounded-2xl border border-[var(--line)] bg-white p-5"
          >
            <div className="flex flex-wrap items-start justify-between gap-4">
              <div className="min-w-0 flex-1">
                {isAlert ? (
                  <>
                    <div className="flex flex-wrap items-center gap-2">
                      <h2 className="font-semibold">{alert.title}</h2>
                      <span
                        className={`rounded-full px-2 py-1 text-xs font-semibold ${alert.active ? "bg-emerald-50 text-emerald-800" : "bg-slate-100 text-slate-600"}`}
                      >
                        {alert.active ? "追蹤中" : "已暫停"}
                      </span>
                      <span
                        className={`rounded-full px-2 py-1 text-xs font-semibold ${alert.monitoring_mode === "automatic" ? "bg-sky-50 text-sky-800" : "bg-amber-50 text-amber-800"}`}
                      >
                        {alert.monitoring_mode === "automatic"
                          ? "每 6 小時自動查價"
                          : "僅手動查看"}
                      </span>
                    </div>
                    <p className="mt-1 text-sm text-[var(--muted)]">
                      {alert.subtitle || "價格項目"}
                    </p>
                    <p className="mt-2 text-sm">
                      {alert.target_price
                        ? `目標低於 ${money(Number(alert.target_price), alert.currency)}`
                        : "刷新低價時通知"}
                      {alert.current_price
                        ? ` · 目前 ${money(Number(alert.current_price), alert.currency)}`
                        : " · 目前價格待更新"}
                    </p>
                    {alert.price_updated_at && (
                      <p className="mt-1 text-xs text-[var(--muted)]">
                        報價時間{" "}
                        {new Date(alert.price_updated_at).toLocaleString(
                          "zh-TW",
                        )}
                      </p>
                    )}
                    {alert.monitoring_mode === "manual_only" && (
                      <p className="mt-2 text-xs text-amber-800">
                        此來源不允許背景定期重查或自動通知；請在搜尋頁手動查看最新價格。
                      </p>
                    )}
                  </>
                ) : (
                  <>
                    <Link
                      href={`/trips/${trip.id}`}
                      className="font-semibold text-[var(--teal)] hover:underline"
                    >
                      {trip.name}
                    </Link>
                    <p className="mt-1 text-sm text-[var(--muted)]">
                      {[
                        trip.destination_name,
                        trip.start_date && trip.end_date
                          ? `${trip.start_date} 至 ${trip.end_date}`
                          : undefined,
                      ]
                        .filter(Boolean)
                        .join(" · ") ||
                        (trip.total_price
                          ? twd.format(trip.total_price)
                          : "尚未安排")}
                    </p>
                  </>
                )}
              </div>
              <div className="flex flex-wrap gap-2">
                {isAlert && (
                  <>
                    <button
                      type="button"
                      onClick={() => {
                        setEditing(alert.id);
                        setDraftPrice(
                          alert.target_price ? String(alert.target_price) : "",
                        );
                      }}
                      aria-label={`編輯 ${alert.title}`}
                      className="rounded-xl border border-[var(--line)] p-2 text-[var(--muted)]"
                    >
                      <Pencil size={17} />
                    </button>
                    <button
                      type="button"
                      onClick={() =>
                        patchAlert(alert, { active: !alert.active })
                      }
                      aria-label={
                        alert.active
                          ? `暫停 ${alert.title}`
                          : `啟用 ${alert.title}`
                      }
                      className="rounded-xl border border-[var(--line)] p-2 text-[var(--muted)]"
                    >
                      {alert.active ? <Pause size={17} /> : <Play size={17} />}
                    </button>
                  </>
                )}
                <button
                  type="button"
                  onClick={() => setPendingDelete(row.id)}
                  aria-label={`刪除${isAlert ? "通知" : "旅程"}`}
                  className="rounded-xl border border-[var(--line)] p-2 text-[var(--muted)]"
                >
                  <Trash2 size={17} />
                </button>
              </div>
            </div>
            {!isAlert && Number(trip.total_price) > 0 && (
              <div className="max-w-sm">
                <PriceAlertButton
                  resourceType="trip"
                  resourceId={trip.id}
                  currentPrice={Number(trip.total_price)}
                  currency={trip.currency || "TWD"}
                  returnPath="/trips"
                />
              </div>
            )}
            {isAlert && editing === alert.id && (
              <div className="mt-4 rounded-xl bg-[var(--paper)] p-4">
                <label className="text-sm font-semibold">
                  目標價格（{alert.currency}）
                  <input
                    aria-label={`編輯 ${alert.title} 的目標價格`}
                    min="1"
                    type="number"
                    value={draftPrice}
                    onChange={(event) => setDraftPrice(event.target.value)}
                    placeholder="留空代表任何降價"
                    className="mt-2 w-full rounded-lg border border-[var(--line)] bg-white px-3 py-2 font-normal"
                  />
                </label>
                <div className="mt-3 flex gap-2">
                  <button
                    type="button"
                    disabled={draftPrice !== "" && Number(draftPrice) <= 0}
                    onClick={() =>
                      patchAlert(alert, {
                        target_price: draftPrice ? Number(draftPrice) : null,
                      })
                    }
                    className="rounded-lg bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
                  >
                    儲存價格
                  </button>
                  <button
                    type="button"
                    onClick={() => setEditing(undefined)}
                    className="flex items-center gap-1 rounded-lg border border-[var(--line)] px-4 py-2 text-sm"
                  >
                    <X size={15} />
                    取消
                  </button>
                </div>
              </div>
            )}
            {pendingDelete === row.id && (
              <div className="mt-4 flex flex-wrap items-center justify-between gap-3 rounded-xl bg-red-50 p-4 text-sm text-red-900">
                <span>
                  確定刪除這筆{isAlert ? "價格通知" : "旅程"}？刪除後無法復原。
                </span>
                <span className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => remove(row.id)}
                    className="rounded-lg bg-red-700 px-3 py-2 font-semibold text-white"
                  >
                    確定刪除
                  </button>
                  <button
                    type="button"
                    onClick={() => setPendingDelete(undefined)}
                    className="rounded-lg border border-red-200 bg-white px-3 py-2"
                  >
                    取消
                  </button>
                </span>
              </div>
            )}
            {rowError[row.id] && (
              <p role="alert" className="mt-3 text-sm text-red-700">
                操作失敗：{rowError[row.id]}
              </p>
            )}
          </article>
        );
      })}
    </div>
  );
}
