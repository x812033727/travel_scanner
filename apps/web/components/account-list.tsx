"use client";

import { Bell, Luggage, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { api, twd } from "@/lib/api";

type Item = { id: string; name?: string; mode?: string; total_price?: number; resource_type?: string; target_price?: number; active?: boolean };
export function AccountList({ kind }: { kind: "trips" | "alerts" }) {
  const [items, setItems] = useState<Item[]>([]); const [error, setError] = useState<string>();
  useEffect(() => { api<Item[]>(`/${kind}`).then(setItems).catch((reason: Error) => setError(reason.message)); }, [kind]);
  async function remove(id: string) { await api(`/${kind}/${id}`, { method: "DELETE" }); setItems((current) => current.filter((item) => item.id !== id)); }
  if (error) return <p className="rounded-xl bg-red-50 p-4 text-red-700">{error}，請先登入。</p>;
  if (!items.length) return <div className="rounded-[2rem] border border-dashed border-[var(--line)] bg-white p-12 text-center text-[var(--muted)]">{kind === "trips" ? <Luggage className="mx-auto mb-3" /> : <Bell className="mx-auto mb-3" />}目前還沒有{kind === "trips" ? "已儲存旅程" : "價格通知"}。</div>;
  return <div className="space-y-3">{items.map((item) => <article key={item.id} className="flex items-center justify-between rounded-2xl border border-[var(--line)] bg-white p-5"><div><h2 className="font-semibold">{item.name || `${item.resource_type} 價格通知`}</h2><p className="mt-1 text-sm text-[var(--muted)]">{item.total_price ? twd.format(item.total_price) : item.target_price ? `低於 ${twd.format(item.target_price)} 時提醒` : "持續追蹤價格"}</p></div><button onClick={() => remove(item.id)} aria-label="刪除" className="rounded-xl border border-[var(--line)] p-2 text-[var(--muted)]"><Trash2 size={17} /></button></article>)}</div>;
}

