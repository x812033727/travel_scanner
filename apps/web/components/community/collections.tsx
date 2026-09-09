"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { AccountSavedItems } from "@/components/account-saved-items";
import { api } from "@/lib/api";
import type { Page, Post } from "@/lib/community/types";
import { Button, Empty, ErrorNotice, fieldClass, panelClass, Tabs } from "./ui";
import { Feed, PostCard } from "./feed";
import { useResource } from "./use-resource";
import { DiscoveryCard } from "@/components/discovery/card";
import type { DiscoveryItem } from "@/lib/discovery";

export function Collections() {
  const t = useTranslations("community");
  const [tab, setTab] = useState("savedPosts");
  const [selected, setSelected] = useState("");
  const [name, setName] = useState("");
  const [error, setError] = useState<unknown>();
  const lists = useResource<Page<{ id: string; name: string }>>("/community/collections");
  const items = useResource<Page<{ id: string; kind: string; target: string; post?: Post; discovery?: DiscoveryItem; unavailable?: boolean }>>(selected ? `/community/collections/${selected}/items` : null);
  async function create() {
    try { const result = await api<{ id: string }>("/community/collections", { method: "POST", body: JSON.stringify({ name }) }); setName(""); await lists.reload(); setSelected(result.id); }
    catch (reason) { setError(reason); }
  }
  async function edit(remove: boolean) {
    if (!selected) return;
    const value = remove ? null : window.prompt(t("name"), lists.data?.items.find((row) => row.id === selected)?.name);
    if ((!remove && !value) || (remove && !window.confirm(t("deleteCollectionConfirm")))) return;
    try { await api(`/community/collections/${selected}`, { method: remove ? "DELETE" : "PUT", ...(remove ? {} : { body: JSON.stringify({ name: value }) }) }); if (remove) setSelected(""); await lists.reload(); }
    catch (reason) { setError(reason); }
  }
  async function removeItem(id: string) {
    try { await api(`/community/collections/${selected}/items/${id}`, { method: "DELETE" }); await items.reload(); }
    catch (reason) { setError(reason); }
  }
  return <div className="space-y-5"><p className="text-sm text-[var(--muted)]">{t("privateCollections")}</p><Tabs value={tab} onChange={setTab} label={t("collections")} items={["savedPosts", "savedPlaces", "collections"].map((value) => ({ value, label: t(value) }))}>
    {tab === "savedPosts" && <Feed saved />}{tab === "savedPlaces" && <AccountSavedItems />}
    {tab === "collections" && <div className="space-y-5"><form onSubmit={(e) => { e.preventDefault(); void create(); }} className="flex flex-wrap items-end gap-3"><label className="min-w-0 flex-1 font-semibold">{t("newCollection")}<input required maxLength={80} value={name} onChange={(e) => setName(e.target.value)} className={fieldClass} /></label><Button type="submit">{t("create")}</Button></form>
      <label className="block font-semibold">{t("collection")}<select value={selected} onChange={(e) => setSelected(e.target.value)} className={fieldClass}><option value="">{t("chooseCollection")}</option>{lists.data?.items.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>
      {selected && <div className="flex gap-3"><Button secondary onClick={() => void edit(false)}>{t("rename")}</Button><Button secondary onClick={() => void edit(true)}>{t("delete")}</Button></div>}
      <ErrorNotice error={error || lists.error || items.error} />
      <div className="grid gap-4 md:grid-cols-2">{items.data?.items.map((item) => <div key={item.id} className="space-y-2">{item.unavailable ? <Empty>{t("contentUnavailable")}</Empty> : item.discovery ? <DiscoveryCard item={item.discovery} /> : item.post ? <PostCard post={item.post} /> : <Link className={`${panelClass} block`} href={item.kind === "pet_place" ? `/pet-friendly/${item.target}` : item.kind === "hotspot" ? `/hotspots?hotspot=${item.target}` : "/foods"}>{t("openPlace")}</Link>}<Button secondary onClick={() => void removeItem(item.id)}>{t("remove")}</Button></div>)}</div>
      {items.data?.items.length === 0 && <Empty>{t("emptyCollection")}</Empty>}
    </div>}
  </Tabs></div>;
}
