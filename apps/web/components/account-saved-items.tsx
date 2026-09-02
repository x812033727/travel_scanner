"use client";

import { ExternalLink, Heart, MapPin } from "lucide-react";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

type SavedItem = { type: "hotspot" | "food" | "restaurant"; id: string; title: string; subtitle: string; map_links: { url: string; label: string }[] };

export function AccountSavedItems() {
  const [items, setItems] = useState<SavedItem[]>([]);
  const [loaded, setLoaded] = useState(false);
  useEffect(() => { api<{ items: SavedItem[] }>("/saved-items?limit=100").then((result) => setItems(result.items)).catch(() => undefined).finally(() => setLoaded(true)); }, []);
  return <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8">
    <div className="flex items-center gap-3"><span className="grid h-10 w-10 place-items-center rounded-2xl bg-[var(--coral-soft)] text-[var(--coral)]"><Heart size={19} fill="currentColor" /></span><div><h2 className="text-xl font-bold">我的收藏</h2><p className="text-sm text-[var(--muted)]">景點、美食與餐廳會同步到這個帳號。</p></div></div>
    {!loaded ? <p className="mt-5 text-sm text-[var(--muted)]">正在載入收藏…</p> : items.length === 0 ? <p className="mt-5 rounded-2xl bg-[var(--paper)] p-4 text-sm text-[var(--muted)]">還沒有收藏。從景點或美食小卡按下愛心即可加入。</p> : <div className="mt-5 grid gap-2 sm:grid-cols-2">{items.map((item) => { const map = item.map_links[0]; const content = <><span className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-[var(--teal-soft)] text-[var(--teal-dark)]"><MapPin size={17} /></span><span className="min-w-0"><strong className="block truncate text-sm">{item.title}</strong><span className="block truncate text-xs text-[var(--muted)]">{item.subtitle}</span></span>{map && <ExternalLink className="ml-auto shrink-0" size={15} />}</>; return map ? <a key={`${item.type}:${item.id}`} href={map.url} target="_blank" rel="noopener noreferrer" className="flex min-h-14 items-center gap-3 rounded-2xl bg-[var(--paper)] px-3 transition hover:-translate-y-0.5 hover:shadow-sm">{content}</a> : <div key={`${item.type}:${item.id}`} className="flex min-h-14 items-center gap-3 rounded-2xl bg-[var(--paper)] px-3">{content}</div>; })}</div>}
  </section>;
}
