"use client";

import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type Translator = ReturnType<typeof useTranslations>;

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

// The outcomes the approve endpoint can report. An outcome this build does not know is
// shown as its own code rather than dropped: the admin needs to see that something was
// skipped even when a newer server is the one naming the reason.
const OUTCOMES = [
  "verified",
  "coordinates_saved",
  "candidate_changed",
  "place_id_taken",
  "no_result",
  "already_durable",
  "not_found",
] as const;

function outcomeLabel(t: Translator, outcome: string) {
  return (OUTCOMES as readonly string[]).includes(outcome) ? t(`outcome.${outcome}`) : outcome;
}

function verdictBadge(t: Translator, signals: QueueSignals) {
  if (signals.verdict === "agree") {
    return (
      <span className="rounded-full bg-emerald-100 px-2 py-1 text-xs font-semibold text-emerald-800">
        {t("verdictAgree")}
      </span>
    );
  }
  if (signals.verdict === "no_result") {
    return (
      <span className="rounded-full bg-slate-100 px-2 py-1 text-xs font-semibold text-slate-600">
        {t("verdictNoResult")}
      </span>
    );
  }
  return (
    <span className="rounded-full bg-amber-100 px-2 py-1 text-xs font-semibold text-amber-800">
      {t("verdictCheck")}
    </span>
  );
}

// One list for the header and for every cell's `data-label`, so the phone layout cannot
// drift out of step with the columns it is labelling.
const COLUMN_KEYS = ["columnSelect", "columnMerchant", "columnCandidate", "columnSignals"] as const;

export function AdminMerchantCoordinateQueue() {
  const t = useTranslations("admin.merchantCoordinateQueue");
  // The reasons are a list, and every language punctuates a list differently — "、" is
  // right in Chinese and wrong everywhere else.
  const reasonList = new Intl.ListFormat(useLocale(), { style: "long", type: "unit" });
  const columns = COLUMN_KEYS.map((key) => t(key));
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
        skipped.length
          ? t("writtenWithSkipped", {
              count: result.written,
              skipped: skipped.length,
              reasons: reasonList.format(
                skipped.map((outcome) => outcomeLabel(t, outcome.outcome)),
              ),
            })
          : t("written", { count: result.written }),
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
      <h2 className="text-lg font-bold">{t("title")}</h2>
      <p className="mt-1 text-sm text-[var(--muted)]">{t("description")}</p>
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
          {t("notConfigured")}
        </p>
      )}
      <div className="mt-4 overflow-x-auto rounded-2xl border bg-white">
        <table className="admin-responsive-table w-full min-w-[960px] text-left text-sm">
          <thead className="bg-[var(--paper)]">
            <tr>
              {columns.map((column) => <th key={column} className="p-3">{column}</th>)}
            </tr>
          </thead>
          <tbody>
            {(data?.items ?? []).map((item) => (
              <tr key={item.merchant.id} className="border-t align-top">
                <td data-label={columns[0]} className="p-3">
                  <input
                    type="checkbox"
                    aria-label={t("selectMerchant", { name: item.merchant.name })}
                    className="h-5 w-5"
                    disabled={!item.candidate}
                    checked={selected.has(item.merchant.id)}
                    onChange={() => toggle(item.merchant.id)}
                  />
                </td>
                <td data-label={columns[1]} className="p-3">
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
                      {t("koreaNote")}
                    </div>
                  )}
                </td>
                <td data-label={columns[2]} className="p-3">
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
                        {t("openInGoogleMaps")}
                      </a>
                    </>
                  ) : (
                    <span className="text-xs text-[var(--muted)]">{t("noResult")}</span>
                  )}
                </td>
                <td data-label={columns[3]} className="p-3">
                  <div className="flex flex-wrap items-center gap-2">
                    {verdictBadge(t, item.signals)}
                    {typeof item.signals.name_score === "number" && (
                      <span className="text-xs text-[var(--muted)]">
                        {t("nameScore", { score: item.signals.name_score.toFixed(2) })}
                      </span>
                    )}
                    {typeof item.signals.distance_km === "number" && (
                      <span className="text-xs text-[var(--muted)]">
                        {t("distanceKm", { km: item.signals.distance_km })}
                      </span>
                    )}
                    {item.signals.place_id_taken && (
                      <span className="text-xs text-red-700">{t("placeIdTaken")}</span>
                    )}
                  </div>
                </td>
              </tr>
            ))}
            {data && data.configured && !data.items?.length && (
              <tr>
                <td colSpan={4} className="p-6 text-center text-sm text-[var(--muted)]">
                  {t("queueEmpty")}
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
          {t("approveSelected", { count: selected.size })}
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
          {t("previousPage")}
        </button>
        <span className="text-sm text-[var(--muted)]">
          {t("pageStatus", { page, total: totalPages, pending: data?.total ?? 0 })}
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
          {t("nextPage")}
        </button>
      </div>
    </section>
  );
}
