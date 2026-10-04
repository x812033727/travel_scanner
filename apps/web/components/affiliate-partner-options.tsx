"use client";

import { ExternalLink, HandCoins, Wifi } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
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
  const locale = useLocale();
  // Every caller passes a title of its own today, but the default it fell back to
  // was a Chinese literal, waiting for the first caller that stopped passing one.
  const heading = title ?? t("title");
  const moduleKey = [...new Set(modules)].filter((module) => Object.hasOwn(moduleKeys, module)).join(",");
  const source = searchId ? `search_id=${encodeURIComponent(searchId)}` : tripId ? `trip_id=${encodeURIComponent(tripId)}` : null;
  const requestKey = source && moduleKey ? JSON.stringify([source, moduleKey, locale]) : null;
  const [snapshot, setSnapshot] = useState<{ key: string; responses: AffiliateResponse[] }>();
  // Source and locale changes hide the previous buttons during render, before effects run.
  const responses = requestKey && snapshot?.key === requestKey ? snapshot.responses : [];

  useEffect(() => {
    if (!requestKey || !source) return;
    const controller = new AbortController();
    const requestedModules = moduleKey.split(",") as AffiliateModule[];
    void Promise.all(requestedModules.map((module) => api<AffiliateResponse>(`/affiliates/options?module=${module}&${source}`, {
      signal: controller.signal, headers: { "X-Travel-Locale": locale },
    }).catch(() => ({ module, disclosure: "", options: [] })))).then((values) => {
      if (!controller.signal.aborted) setSnapshot({ key: requestKey, responses: values.filter((value) => value?.options?.length) });
    });
    return () => { controller.abort(); };
  }, [locale, moduleKey, requestKey, source]);

  if ((!searchId && !tripId) || !moduleKey || !responses.length) return null;
  const disclosure = responses.find((response) => response.disclosure)?.disclosure;
  return <section aria-label={heading} className="mb-5 rounded-[1.5rem] border border-[var(--line)] bg-white p-5">
    <div className="flex items-start gap-3"><span className="shrink-0 rounded-xl bg-[var(--coral-soft)] p-2 text-[var(--coral)]">{responses.some((item) => item.module === "connectivity") ? <Wifi size={19} /> : <HandCoins size={19} />}</span><div className="min-w-0 break-words"><h2 className="font-bold">{heading}</h2><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("affiliatePanelHint")}</p></div></div>
    <div className="mt-4 space-y-4">{responses.map((response) => <div key={response.module}>
      <p className="mb-2 text-xs font-bold text-[var(--teal-dark)]">{t(moduleKeys[response.module])}</p>
      <div className="grid min-w-0 gap-2 sm:grid-cols-2">{response.options.map((option) => <form
        key={`${response.module}:${option.partner}`}
        action={`${option.clickout_url}${option.clickout_url.includes("?") ? "&" : "?"}locale=${encodeURIComponent(locale)}`}
        method="post" target="_blank" rel="noopener" className="min-w-0"
      ><button type="submit" aria-label={`${option.cta} · ${t("newTab")}`} className="flex min-h-11 w-full min-w-0 items-center justify-between gap-2 rounded-xl border border-[var(--teal)] bg-white px-4 py-3 text-left text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)]">
        <span className="min-w-0 break-words [overflow-wrap:anywhere]">{option.cta}</span><ExternalLink size={15} className="shrink-0" aria-hidden="true" />
      </button></form>)}</div>
    </div>)}</div>
    {disclosure && <p className="mt-4 border-t border-[var(--line)] pt-3 text-xs text-[var(--muted)]">{disclosure}</p>}
  </section>;
}
