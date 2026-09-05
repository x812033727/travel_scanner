"use client";

import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type QueueMerchant = {
  id: string;
  slug: string;
  name: string;
  local_name: string;
  address: string | null;
  destination_id: string;
  country_code: string;
  latitude: number | null;
  longitude: number | null;
  map_match_status: string;
  review_status: string;
  needs_naver_url: boolean;
};

type QueueCandidate = {
  place_id: string;
  name: string;
  address: string | null;
  google_maps_url: string | null;
  latitude: number;
  longitude: number;
};

type QueueSignals = {
  verdict: "agree" | "check" | "no_result";
  name_score?: number;
  distance_km?: number | null;
  place_id_taken?: boolean;
};

type QueueItem = {
  merchant: QueueMerchant;
  candidate: QueueCandidate | null;
  signals: QueueSignals;
};

type QueueResponse = {
  configured: boolean;
  items: QueueItem[];
  total: number;
  page: number;
  limit: number;
};

type ApproveOutcome = { merchant_id: string; outcome: string };

const PAGE_SIZE = 10;

const OUTCOME_LABELS: Record<string, string> = {
  verified: "已驗證",
  coordinates_saved: "座標已存（待 Naver 連結）",
  candidate_changed: "Google 結果已改變，略過",
  place_id_taken: "Place ID 已被其他店家使用",
  no_result: "找不到結果",
  already_durable: "已有永久座標",
  not_found: "店家不存在",
};

function verdictBadge(signals: QueueSignals) {
  if (signals.verdict === "agree") {
    return (
      <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-800">
        一致
      </span>
    );
  }
  if (signals.verdict === "no_result") {
    return (
      <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">
        無結果
      </span>
    );
  }
  return (
    <span className="rounded-full bg-amber-100 px-2 py-1 text-xs font-semibold text-amber-800">
      需人工比對
    </span>
  );
}

export function AdminMerchantCoordinateQueue() {
  const [page, setPage] = useState(1);
  const [version, setVersion] = useState(0);
  const [data, setData] = useState<QueueResponse | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    let stale = false;
    void api<QueueResponse>(
      `/admin/foods/merchants/coordinate-queue?page=${page}&limit=${PAGE_SIZE}`,
    )
      .then((response) => {
        if (stale) return;
        const lastPage = Math.max(1, Math.ceil(response.total / PAGE_SIZE));
        if (page > lastPage) {
          // Approvals shrank the queue underneath us; fall back to the real last page.
          setPage(lastPage);
          return;
        }
        setData(response);
        // Rows the server already judged as agreeing start selected; the admin's job
        // is to look at the amber ones, not to re-tick the obvious ones.
        setSelected(
          new Set(
            response.items
              .filter((item) => item.candidate && item.signals.verdict === "agree")
              .map((item) => item.merchant.id),
          ),
        );
      })
      .catch((reason: Error) => {
        if (!stale) setMessage(reason.message);
      });
    return () => {
      stale = true;
    };
  }, [page, version]);

  function toggle(id: string) {
    setSelected((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  async function approveSelected() {
    const items = (data?.items ?? [])
      .filter((item) => item.candidate && selected.has(item.merchant.id))
      .map((item) => ({
        merchant_id: item.merchant.id,
        place_id: item.candidate!.place_id,
      }));
    if (!items.length) return;
    setLoading(true);
    try {
      const result = await api<{ written: number; outcomes: ApproveOutcome[] }>(
        "/admin/foods/merchants/coordinate-queue/approve",
        { method: "POST", body: JSON.stringify({ items }) },
      );
      const skipped = result.outcomes.filter(
        (outcome) => !["verified", "coordinates_saved"].includes(outcome.outcome),
      );
      setMessage(
        `已寫入 ${result.written} 筆座標${
          skipped.length
            ? `；${skipped.length} 筆略過（${skipped
                .map((outcome) => OUTCOME_LABELS[outcome.outcome] ?? outcome.outcome)
                .join("、")}）`
            : ""
        }。`,
      );
      setVersion((current) => current + 1);
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  const totalPages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1;

  return (
    <section className="mt-6">
      <h2 className="text-lg font-bold">座標審核佇列</h2>
      <p className="mt-1 text-sm text-[var(--muted)]">
        列出還沒有永久座標的店家，並排 Google 找到的地點與比對訊號。核准會以
        admin_verified 來源寫入座標；伺服器會重新查詢確認，絕不採用瀏覽器送來的座標。
      </p>
      {message && (
        <p
          role="status"
          className="mt-3 rounded-xl bg-[var(--paper)] px-4 py-3 text-sm text-[var(--muted)]"
        >
          {message}
        </p>
      )}
      {data && !data.configured && (
        <p className="mt-3 rounded-xl border border-amber-300 bg-amber-50 px-4 py-3 text-sm">
          Google Places 金鑰未設定，無法解析候選。
        </p>
      )}
      <div className="mt-4 overflow-x-auto rounded-2xl border bg-white">
        <table className="w-full min-w-[960px] text-left text-sm">
          <thead className="bg-[var(--paper)]">
            <tr>
              <th className="p-3">選取</th>
              <th className="p-3">店家</th>
              <th className="p-3">Google 找到</th>
              <th className="p-3">訊號</th>
            </tr>
          </thead>
          <tbody>
            {(data?.items ?? []).map((item) => (
              <tr key={item.merchant.id} className="border-t align-top">
                <td className="p-3">
                  <input
                    type="checkbox"
                    aria-label={`選取 ${item.merchant.name}`}
                    className="h-5 w-5"
                    disabled={!item.candidate}
                    checked={selected.has(item.merchant.id)}
                    onChange={() => toggle(item.merchant.id)}
                  />
                </td>
                <td className="p-3">
                  <div className="font-semibold">{item.merchant.name}</div>
                  <div className="text-xs text-[var(--muted)]">
                    {item.merchant.local_name} · {item.merchant.destination_id.toUpperCase()} ·{" "}
                    {item.merchant.country_code}
                  </div>
                  {item.merchant.address && (
                    <div className="text-xs text-[var(--muted)]">{item.merchant.address}</div>
                  )}
                  {item.merchant.needs_naver_url && (
                    <div className="mt-1 text-xs text-amber-700">
                      韓國店家：座標可先寫入，發布仍需 Naver 精準地點頁
                    </div>
                  )}
                </td>
                <td className="p-3">
                  {item.candidate ? (
                    <>
                      <div className="font-semibold">{item.candidate.name}</div>
                      {item.candidate.address && (
                        <div className="text-xs text-[var(--muted)]">{item.candidate.address}</div>
                      )}
                      <a
                        href={
                          item.candidate.google_maps_url ??
                          `https://www.google.com/maps/place/?q=place_id:${item.candidate.place_id}`
                        }
                        target="_blank"
                        rel="noreferrer"
                        className="text-xs text-[var(--teal)] underline"
                      >
                        在 Google 地圖開啟
                      </a>
                    </>
                  ) : (
                    <span className="text-xs text-[var(--muted)]">找不到結果</span>
                  )}
                </td>
                <td className="p-3">
                  <div className="flex flex-wrap items-center gap-2">
                    {verdictBadge(item.signals)}
                    {typeof item.signals.name_score === "number" && (
                      <span className="text-xs text-[var(--muted)]">
                        名稱 {item.signals.name_score.toFixed(2)}
                      </span>
                    )}
                    {typeof item.signals.distance_km === "number" && (
                      <span className="text-xs text-[var(--muted)]">
                        距離 {item.signals.distance_km} km
                      </span>
                    )}
                    {item.signals.place_id_taken && (
                      <span className="text-xs text-red-700">Place ID 已被使用</span>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {data && data.configured && !data.items.length && (
              <tr>
                <td colSpan={4} className="p-6 text-center text-sm text-[var(--muted)]">
                  佇列已清空 — 所有店家都有永久座標了。
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-3">
        <button
          type="button"
          onClick={() => void approveSelected()}
          disabled={loading || !selected.size}
          className="min-h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-40"
        >
          批次核准（{selected.size}）
        </button>
        <button
          type="button"
          onClick={() => {
            setMessage("");
            setPage((current) => Math.max(1, current - 1));
          }}
          disabled={loading || page <= 1}
          className="min-h-11 rounded-xl border bg-white px-4 disabled:opacity-40"
        >
          上一頁
        </button>
        <span className="text-sm text-[var(--muted)]">
          第 {page} / {totalPages} 頁 · 待處理 {data?.total ?? 0} 筆
        </span>
        <button
          type="button"
          onClick={() => {
            setMessage("");
            setPage((current) => current + 1);
          }}
          disabled={loading || page >= totalPages}
          className="min-h-11 rounded-xl border bg-white px-4 disabled:opacity-40"
        >
          下一頁
        </button>
      </div>
    </section>
  );
}
