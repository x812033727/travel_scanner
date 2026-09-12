"use client";

import { ExternalLink, HandCoins, Wifi } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

export type AffiliateModule = "flight" | "hotel" | "activities" | "transport" | "connectivity";
type AffiliateOption = { partner: string; display_name: string; module: AffiliateModule; cta: string; clickout_url: string };
type AffiliateResponse = { module: AffiliateModule; disclosure: string; options: AffiliateOption[] };

// travelServices already names all five modules in all five languages; this file
// carried a second, zh-TW-only copy of the same list.
const moduleKeys: Record<AffiliateModule, string> = {
  flight: "affiliateFlight",
  hotel: "affiliateHotel",
  activities: "affiliateActivities",
  transport: "affiliateTransport",
  connectivity: "affiliateConnectivity",
};

export function AffiliatePartnerOptions({ searchId, tripId, modules, title }: { searchId?: string; tripId?: string; modules: AffiliateModule[]; title?: string }) {
  const t = useTranslations("travelServices");
  // Every caller passes a title of its own today, but the default it fell back to
  // was a Chinese literal, waiting for the first caller that stopped passing one.
  const heading = title ?? t("title");
  const [responses, setResponses] = useState<AffiliateResponse[]>([]);
  const moduleKey = modules.join(",");

  useEffect(() => {
    const requestedModules = moduleKey.split(",").filter(Boolean) as AffiliateModule[];
    if ((!searchId && !tripId) || !requestedModules.length) return;
    let active = true;
    const source = searchId ? `search_id=${encodeURIComponent(searchId)}` : `trip_id=${encodeURIComponent(tripId || "")}`;
    Promise.all(requestedModules.map((module) => api<AffiliateResponse>(`/affiliates/options?module=${module}&${source}`).catch(() => ({ module, disclosure: "", options: [] })))).then((values) => {
      if (active) setResponses(values.filter((value) => value?.options?.length));
    });
    return () => { active = false; };
  }, [moduleKey, searchId, tripId]);

  if ((!searchId && !tripId) || !moduleKey || !responses.length) return null;
  const disclosure = responses.find((response) => response.disclosure)?.disclosure;
  return <section aria-label={heading} className="mb-5 rounded-[1.5rem] border border-[var(--line)] bg-white p-5">
    <div className="flex items-start gap-3"><span className="rounded-xl bg-[var(--coral-soft)] p-2 text-[var(--coral)]">{responses.some((item) => item.module === "connectivity") ? <Wifi size={19} /> : <HandCoins size={19} />}</span><div><h2 className="font-bold">{heading}</h2><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("affiliatePanelHint")}</p></div></div>
    <div className="mt-4 space-y-4">{responses.map((response) => <div key={response.module}><p className="mb-2 text-xs font-bold text-[var(--teal-dark)]">{t(moduleKeys[response.module])}</p><div className="flex gap-2 overflow-x-auto pb-1">{response.options.map((option) => <form key={`${response.module}:${option.partner}`} action={option.clickout_url} method="post" target="_blank" className="shrink-0"><button type="submit" className="flex items-center gap-2 rounded-xl border border-[var(--teal)] bg-white px-4 py-3 text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)]">{option.cta}<ExternalLink size={15} /></button></form>)}</div></div>)}</div>
    {disclosure && <p className="mt-4 border-t border-[var(--line)] pt-3 text-xs text-[var(--muted)]">{disclosure}</p>}
  </section>;
}
