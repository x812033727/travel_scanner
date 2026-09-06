"use client";

import { Bell, Check, X } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { ApiError, api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";
import { featureEnabled } from "@/lib/site-features";

export function PriceAlertButton({ resourceType, resourceId, currentPrice, currency = "TWD", returnPath }: { resourceType: "flight" | "hotel" | "trip"; resourceId: string; currentPrice?: number; currency?: string; returnPath?: string }) {
  const [editing, setEditing] = useState(false);
  const [targetPrice, setTargetPrice] = useState(currentPrice && currentPrice > 0 ? String(Math.round(currentPrice)) : "");
  const [busy, setBusy] = useState(false);
  const [created, setCreated] = useState(false);
  const [error, setError] = useState("");
  const [errorCode, setErrorCode] = useState("");
  const [loginRequired, setLoginRequired] = useState(false);
  const visibility = useSiteVisibility();
  const t = useTranslations("alerts.button");

  async function create() {
    setBusy(true); setError(""); setErrorCode(""); setLoginRequired(false);
    try {
      await api("/alerts", { method: "POST", body: JSON.stringify({ resource_type: resourceType, resource_id: resourceId, target_price: targetPrice.trim() ? Number(targetPrice) : null }) });
      setCreated(true); setEditing(false);
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 401) setLoginRequired(true);
      else { setError((reason as Error).message); setErrorCode(reason instanceof ApiError ? reason.code ?? "" : ""); }
    } finally { setBusy(false); }
  }

  if (!featureEnabled(visibility, "alerts")) return null;
  if (created) return <p role="status" className="mt-3 flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-800"><Check size={16} />{t("created")} · <Link className="underline" href="/alerts">{t("manage")}</Link></p>;
  return <div className="mt-3">
    {!editing ? <button type="button" onClick={() => setEditing(true)} className="flex w-full items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold text-[var(--teal)]"><Bell size={16} />{t("create")}</button> : <div className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3"><label className="text-sm font-semibold">{t("targetPrice", { currency })}<input aria-label={t("targetPrice", { currency })} min="1" step="1" inputMode="numeric" type="number" value={targetPrice} onChange={(event) => setTargetPrice(event.target.value)} placeholder={t("placeholder")} className="mt-2 w-full rounded-lg border border-[var(--line)] bg-white px-3 py-2 font-normal" /></label><p className="mt-1 text-xs text-[var(--muted)]">{t("placeholderHint")}</p><div className="mt-3 grid grid-cols-2 gap-2"><button type="button" onClick={create} disabled={busy || (targetPrice !== "" && Number(targetPrice) <= 0)} className="flex items-center justify-center gap-2 rounded-lg bg-[var(--teal)] px-3 py-2 text-sm font-semibold text-white disabled:opacity-50"><Bell size={15} />{busy ? t("creating") : t("confirm")}</button><button type="button" onClick={() => { setEditing(false); setError(""); setLoginRequired(false); }} className="flex items-center justify-center gap-2 rounded-lg border border-[var(--line)] px-3 py-2 text-sm"><X size={15} />{t("cancel")}</button></div></div>}
    {loginRequired && <p role="alert" className="mt-2 text-sm text-red-700">{t("loginRequired")}<Link className="ml-1 font-semibold underline" href={loginPath(returnPath || (typeof window !== "undefined" ? `${window.location.pathname}${window.location.search}` : "/"))}>{t("loginReturn")}</Link></p>}
    {error && <p role="alert" className="mt-2 text-sm text-red-700">{error}{errorCode === "alert_exists" ? <Link className="ml-1 underline" href="/alerts">{t("manage")}</Link> : null}</p>}
  </div>;
}
