"use client";
import { useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useSearchParams } from "next/navigation";
import { useHeaderSession } from "@/components/header-session";
import { Button, fieldClass, Tabs } from "@/components/community/ui";
import { AccountSavedItems } from "@/components/account-saved-items";
import { Link } from "@/i18n/navigation";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import { useDiscoveryResource, useDiscoveryStatus, type DiscoveryItem } from "@/lib/discovery";
import { loginPath } from "@/lib/navigation";
import { api } from "@/lib/api";
import { DiscoveryCard } from "./card";
export function DiscoveryCollections() {
  const c = getDiscoveryCopy(useLocale());
  const { enabled, loading } = useDiscoveryStatus();
  const { status, user } = useHeaderSession();
  const params = useSearchParams();
  return <main className="mx-auto min-h-[70vh] max-w-6xl space-y-6 px-5 py-10 md:px-8"><h1 className="text-3xl font-bold">{c.collections}</h1><p className="text-[var(--muted)]">{c.private}</p>{loading || status === "loading" ? <p role="status">{c.loading}</p> : !enabled ? <p>{c.unavailable}</p> : !user ? <Link href={loginPath(`/explore/collections${params.size ? `?${params}` : ""}`)} className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-5 font-semibold text-white">{c.login}</Link> : <CollectionWorkspace key={user.id} />}</main>;
}
function CollectionWorkspace() {
  const locale = useLocale();
  const c = getDiscoveryCopy(locale);
  const t = useTranslations("community");
  const [tab, setTab] = useState("collections");
  const [selected, setSelected] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const lists = useDiscoveryResource<{ items: Array<{ id: string; name: string }> }>("/discovery/collections");
  const result = useDiscoveryResource<{ id: string; name: string; items: Array<{ id: string; kind: string; target: string; discovery?: DiscoveryItem; unavailable?: boolean }> }>(selected ? `/discovery/collections/${selected}?locale=${locale}` : null);
  async function mutate(action: "create" | "delete" | "remove", id?: string) {
    setBusy(true); setError(false);
    try {
      if (action === "create") { const item = await api<{ id: string }>("/discovery/collections", { method: "POST", body: JSON.stringify({ name }) }); setName(""); setSelected(item.id); lists.reload(); }
      else if (action === "delete") { await api(`/discovery/collections/${selected}`, { method: "DELETE" }); setSelected(""); lists.reload(); }
      else { await api(`/discovery/collections/${selected}/items/${id}`, { method: "DELETE" }); result.reload(); }
    } catch { setError(true); } finally { setBusy(false); }
  }
  return <Tabs value={tab} onChange={setTab} label={c.collections} items={[{ value: "collections", label: c.collections }, { value: "savedPlaces", label: t("savedPlaces") }]}>{tab === "savedPlaces" ? <AccountSavedItems /> : <div className="space-y-5"><form onSubmit={(event) => { event.preventDefault(); void mutate("create"); }} className="flex flex-wrap items-end gap-3"><label className="min-w-0 flex-1 font-semibold">{t("newCollection")}<input className={fieldClass} required maxLength={80} value={name} onChange={(event) => setName(event.target.value)} /></label><Button type="submit" disabled={busy}>{t("create")}</Button></form>
    <div className="flex flex-wrap items-end gap-3"><label className="min-w-0 flex-1 font-semibold">{t("collection")}<select className={fieldClass} value={selected} onChange={(event) => setSelected(event.target.value)}><option value="">{t("chooseCollection")}</option>{lists.data?.items.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>{selected && <Button secondary disabled={busy} onClick={() => { if (window.confirm(t("deleteCollectionConfirm"))) void mutate("delete"); }}>{t("delete")}</Button>}</div>
    {(error || Boolean(lists.error) || Boolean(result.error)) && <p role="alert">{c.unavailable}</p>}{(lists.loading || result.loading) && <p role="status">{c.loading}</p>}
    {result.data?.items.length === 0 && <p className="rounded-2xl border border-dashed border-[var(--line)] p-8 text-center text-[var(--muted)]">{t("emptyCollection")}</p>}
    <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">{result.data?.items.map((item) => <div key={item.id} className="space-y-2">{item.discovery && !item.unavailable ? <DiscoveryCard item={item.discovery} /> : <p className="rounded-2xl bg-[var(--paper)] p-6">{t("contentUnavailable")}</p>}<Button secondary disabled={busy} onClick={() => void mutate("remove", item.id)}>{t("remove")}</Button></div>)}</div>
  </div>}</Tabs>;
}
