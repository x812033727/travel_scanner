"use client";

import { Bell, Check, X } from "lucide-react";
import Link from "next/link";
import { useState } from "react";
import { ApiError, api } from "@/lib/api";
import { loginPath } from "@/lib/navigation";

export function PriceAlertButton({ resourceType, resourceId, currentPrice, currency = "TWD", returnPath }: { resourceType: "flight" | "hotel" | "trip"; resourceId: string; currentPrice?: number; currency?: string; returnPath?: string }) {
  const [editing, setEditing] = useState(false);
  const [targetPrice, setTargetPrice] = useState(currentPrice && currentPrice > 0 ? String(Math.round(currentPrice)) : "");
  const [busy, setBusy] = useState(false);
  const [created, setCreated] = useState(false);
  const [error, setError] = useState("");
  const [loginRequired, setLoginRequired] = useState(false);

  async function create() {
    setBusy(true); setError(""); setLoginRequired(false);
    try {
      await api("/alerts", { method: "POST", body: JSON.stringify({ resource_type: resourceType, resource_id: resourceId, target_price: targetPrice.trim() ? Number(targetPrice) : null }) });
      setCreated(true); setEditing(false);
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 401) setLoginRequired(true);
      else setError((reason as Error).message);
    } finally { setBusy(false); }
  }

  if (created) return <p role="status" className="mt-3 flex items-center gap-2 rounded-xl bg-emerald-50 px-4 py-3 text-sm font-semibold text-emerald-800"><Check size={16} />價格通知已建立 · <Link className="underline" href="/alerts">前往管理</Link></p>;
  return <div className="mt-3">
    {!editing ? <button type="button" onClick={() => setEditing(true)} className="flex w-full items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-4 py-3 text-sm font-semibold text-[var(--teal)]"><Bell size={16} />建立價格通知</button> : <div className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3"><label className="text-sm font-semibold">目標價格（{currency}）<input aria-label={`目標價格（${currency}）`} min="1" step="1" inputMode="numeric" type="number" value={targetPrice} onChange={(event) => setTargetPrice(event.target.value)} placeholder="留空代表追蹤任何降價" className="mt-2 w-full rounded-lg border border-[var(--line)] bg-white px-3 py-2 font-normal" /></label><p className="mt-1 text-xs text-[var(--muted)]">留空代表追蹤任何降價。</p><div className="mt-3 grid grid-cols-2 gap-2"><button type="button" onClick={create} disabled={busy || (targetPrice !== "" && Number(targetPrice) <= 0)} className="flex items-center justify-center gap-2 rounded-lg bg-[var(--teal)] px-3 py-2 text-sm font-semibold text-white disabled:opacity-50"><Bell size={15} />{busy ? "建立中…" : "確認建立"}</button><button type="button" onClick={() => { setEditing(false); setError(""); setLoginRequired(false); }} className="flex items-center justify-center gap-2 rounded-lg border border-[var(--line)] px-3 py-2 text-sm"><X size={15} />取消</button></div></div>}
    {loginRequired && <p role="alert" className="mt-2 text-sm text-red-700">請先登入才能建立通知。<Link className="ml-1 font-semibold underline" href={loginPath(returnPath || (typeof window !== "undefined" ? `${window.location.pathname}${window.location.search}` : "/"))}>登入後返回此頁</Link></p>}
    {error && <p role="alert" className="mt-2 text-sm text-red-700">{error}{error.includes("已經建立") ? <Link className="ml-1 underline" href="/alerts">前往管理</Link> : null}</p>}
  </div>;
}
