"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";

const LOCALES = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
const STATUSES = ["pending", "approved", "rejected", "disabled"] as const;
const BODY_MAX = 1500;

type IntroStatus = (typeof STATUSES)[number];

type IntroItem = {
  id: string;
  hotspot_id: string;
  hotspot_name: string | null;
  locale: string;
  body: string;
  status: IntroStatus;
  source: string;
  ai_provider: string | null;
  ai_model: string | null;
  updated_at: string | null;
};

type IntroResponse = {
  items: IntroItem[];
  total: number;
  status_counts?: Record<string, number>;
};

export function AdminHotspotIntrosPanel() {
  const t = useTranslations("hotspotThemes");
  const [items, setItems] = useState<IntroItem[]>([]);
  const [counts, setCounts] = useState<Record<string, number>>({});
  const [status, setStatus] = useState<string>("pending");
  const [locale, setLocale] = useState("");
  const [nameFilter, setNameFilter] = useState("");
  const [selected, setSelected] = useState<string[]>([]);
  const [editing, setEditing] = useState<string>("");
  const [editBody, setEditBody] = useState("");
  const [loading, setLoading] = useState(true);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const params = new URLSearchParams({ limit: "50" });
      if (status) params.set("status", status);
      if (locale) params.set("locale", locale);
      const result = await api<IntroResponse>(`/admin/hotspots/intros?${params}`);
      setItems(result.items ?? []);
      setCounts(result.status_counts ?? {});
      setSelected([]);
    } catch {
      setError(t("loadFailed"));
    } finally {
      setLoading(false);
    }
  }, [status, locale, t]);

  useEffect(() => {
    // Deferred a tick: the panels' loaders set state synchronously, and calling one
    // straight from an effect body trips react-hooks/set-state-in-effect.
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function review(action: "approve" | "reject") {
    if (!selected.length) return;
    setBusy(true);
    setError("");
    try {
      const result = await api<{ updated: number }>("/admin/hotspots/intros/review", {
        method: "POST",
        body: JSON.stringify({ ids: selected, action }),
      });
      setNotice(t("intros.reviewed", { count: result.updated }));
      await load();
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  async function saveBody(id: string) {
    setBusy(true);
    setError("");
    try {
      await api(`/admin/hotspots/intros/${id}`, {
        method: "PATCH",
        body: JSON.stringify({ body: editBody }),
      });
      setNotice(t("intros.saved"));
      setEditing("");
      await load();
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy(false);
    }
  }

  // Filtering by name is done here rather than server-side: the queue is one page,
  // and an editor scanning it wants the list to narrow as they type.
  const visible = nameFilter.trim()
    ? items.filter((item) => (item.hotspot_name ?? "").includes(nameFilter.trim()))
    : items;

  return (
    <section className="mt-6">
      <h2 className="text-xl font-bold">{t("intros.title")}</h2>
      <p className="mt-1 max-w-3xl text-sm text-[var(--muted)]">{t("intros.description")}</p>
      <p className="mt-1 text-sm text-[var(--muted)]">
        {t("intros.counts", { pending: counts.pending ?? 0, approved: counts.approved ?? 0 })}
      </p>

      <div className="mt-4 flex flex-wrap items-end gap-3">
        <label className="text-sm font-semibold">
          {t("intros.statusFilter")}
          <select
            aria-label={t("intros.statusFilter")}
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            className="mt-1 block h-11 rounded-xl border px-3"
          >
            <option value="">{t("intros.allStatuses")}</option>
            {STATUSES.map((code) => (
              <option key={code} value={code}>
                {t(`intros.status.${code}`)}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm font-semibold">
          {t("intros.localeFilter")}
          <select
            aria-label={t("intros.localeFilter")}
            value={locale}
            onChange={(event) => setLocale(event.target.value)}
            className="mt-1 block h-11 rounded-xl border px-3"
          >
            <option value="">{t("intros.allLocales")}</option>
            {LOCALES.map((code) => (
              <option key={code} value={code}>
                {code}
              </option>
            ))}
          </select>
        </label>
        <label className="text-sm font-semibold">
          {t("intros.hotspotFilter")}
          <input
            aria-label={t("intros.hotspotFilter")}
            value={nameFilter}
            onChange={(event) => setNameFilter(event.target.value)}
            className="mt-1 block h-11 rounded-xl border px-3"
          />
        </label>
        <button
          type="button"
          onClick={() => void load()}
          className="min-h-11 rounded-xl border border-[var(--line)] px-4 font-semibold"
        >
          {t("refresh")}
        </button>
      </div>

      {visible.length > 0 && (
        <div className="mt-4 flex flex-wrap items-center gap-3 rounded-2xl bg-[var(--paper)] p-3">
          <button
            type="button"
            onClick={() =>
              setSelected(
                selected.length === visible.length ? [] : visible.map((item) => item.id),
              )
            }
            className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold"
          >
            {selected.length === visible.length ? t("intros.clearSelection") : t("intros.selectAll")}
          </button>
          <span className="text-sm">{t("intros.selected", { count: selected.length })}</span>
          <button
            type="button"
            disabled={!selected.length || busy}
            onClick={() => void review("approve")}
            className="ml-auto min-h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-50"
          >
            {t("intros.approve")}
          </button>
          <button
            type="button"
            disabled={!selected.length || busy}
            onClick={() => void review("reject")}
            className="min-h-11 rounded-xl border border-[var(--coral)] px-4 font-semibold text-[var(--coral)] disabled:opacity-50"
          >
            {t("intros.reject")}
          </button>
        </div>
      )}

      {notice && <p className="mt-3 rounded-xl bg-[var(--teal-soft)] p-3 text-sm">{notice}</p>}
      {error && (
        <p role="alert" className="mt-3 rounded-xl bg-[var(--coral-soft)] p-3 text-sm">
          {error}
        </p>
      )}
      {loading && <p className="mt-4 text-sm text-[var(--muted)]">{t("loading")}</p>}
      {!loading && visible.length === 0 && (
        <p className="mt-4 text-sm text-[var(--muted)]">{t("intros.empty")}</p>
      )}

      <div className="mt-4 grid gap-3">
        {visible.map((item) => (
          <article key={item.id} className="rounded-2xl border border-[var(--line)] bg-white p-4">
            <div className="flex flex-wrap items-center gap-2">
              <input
                type="checkbox"
                aria-label={t("intros.selectItem", {
                  name: item.hotspot_name ?? item.hotspot_id,
                  locale: item.locale,
                })}
                checked={selected.includes(item.id)}
                onChange={(event) =>
                  setSelected((current) =>
                    event.target.checked
                      ? [...current, item.id]
                      : current.filter((id) => id !== item.id),
                  )
                }
              />
              <strong>{item.hotspot_name ?? item.hotspot_id}</strong>
              <span className="rounded-full bg-[var(--teal-soft)] px-2 py-0.5 text-xs font-semibold text-[var(--teal-dark)]">
                {item.locale}
              </span>
              <span className="rounded-full bg-[var(--paper)] px-2 py-0.5 text-xs">
                {t(`intros.status.${item.status}`)}
              </span>
              <span className="text-xs text-[var(--muted)]">
                {item.source === "ai" ? t("intros.sourceAi") : t("intros.sourceManual")}
                {item.ai_model ? ` · ${item.ai_model}` : ""}
              </span>
            </div>

            {editing === item.id ? (
              <div className="mt-3">
                <textarea
                  aria-label={t("intros.body")}
                  value={editBody}
                  maxLength={BODY_MAX}
                  rows={5}
                  onChange={(event) => setEditBody(event.target.value)}
                  className="w-full rounded-xl border p-3 text-sm"
                />
                <div className="mt-2 flex items-center gap-2">
                  <span className="text-xs text-[var(--muted)]">
                    {t("intros.bodyCount", { count: editBody.length })}
                  </span>
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => void saveBody(item.id)}
                    className="ml-auto min-h-11 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white disabled:opacity-60"
                  >
                    {t("intros.save")}
                  </button>
                  <button
                    type="button"
                    onClick={() => setEditing("")}
                    className="min-h-11 rounded-xl border border-[var(--line)] px-4 text-sm font-semibold"
                  >
                    {t("cancel")}
                  </button>
                </div>
              </div>
            ) : (
              <>
                <p className="mt-2 whitespace-pre-line text-sm leading-6">{item.body}</p>
                <button
                  type="button"
                  onClick={() => {
                    setEditing(item.id);
                    setEditBody(item.body);
                  }}
                  className="mt-2 min-h-11 text-sm font-semibold text-[var(--teal)]"
                >
                  {t("intros.edit")}
                </button>
              </>
            )}
          </article>
        ))}
      </div>
    </section>
  );
}
