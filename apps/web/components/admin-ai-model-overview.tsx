"use client";

import { RefreshCw } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { STAGES, providerLabels as videoProviderLabels, type VideoSettingsView } from "@/components/admin-video-settings";
import { Link } from "@/i18n/navigation";
import { newsProviderLabels, type NewsSettings } from "@/lib/admin-news";
import { settingsHref } from "@/lib/admin-settings-ownership";
import { adminNavigate } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

type Option = { value: string; label?: string };
type Card = { provider: string; config: Record<string, string | number | boolean | null>; field_options?: Record<string, Option[]> };
type Snapshot = { providers: Card[] };
export type OverviewSources = { providers?: Snapshot; news?: NewsSettings; video?: VideoSettingsView };

const vendors = ["openai", "anthropic", "minimax", "gemini"] as const;
type Vendor = (typeof vendors)[number];
const isVendor = (value: unknown): value is Vendor => (vendors as readonly unknown[]).includes(value);
const vendorLabels: Record<Vendor, string> = { openai: "OpenAI", anthropic: "Anthropic Claude", minimax: "MiniMax", gemini: "Google Gemini" };

// How a feature's calls are paid for. "apiKey": the vendor key under the API keys tab.
// "subscription": the Claude subscription accounts signed in on the host. "subscriptionFallback":
// those accounts, and MiniMax once every account is at its cap.
export type Connection = "apiKey" | "subscription" | "subscriptionFallback" | "none";
// Whether the feature can run on a subscription account at all.
// "geminiApiKeyOnly": the row runs on Gemini. The owner signs the host's Antigravity CLI in to
// Google AI subscriptions for their own use over SSH only (2026-09-25): Antigravity's terms
// forbid driving it from other products, so the site's Gemini calls stay on the API key.
export type Support = "apiKeyOnly" | "claudeSubscription" | "claudeCode" | "geminiApiKeyOnly";

export type OverviewRow = {
  key: string;
  feature: string;
  vendor: string;
  model: string;
  inherited?: string;
  connection: Connection;
  support: Support;
  edit: string;
  open?: string;
  gemini?: boolean;
};

type Translate = (key: string, values?: Record<string, string>) => string;

// A reader may get another page's error body, or an older server's shape; a row is only built
// from a settings payload that has the fields it reads.
export function isNewsSettings(value: unknown): value is NewsSettings {
  const settings = value as NewsSettings | null;
  return typeof settings === "object" && settings !== null && (["writer_provider", "verifier_provider", "editor_provider"] as const).every((key) => typeof settings[key] === "string");
}
export function isVideoSettings(value: unknown): value is VideoSettingsView {
  const stages = (value as VideoSettingsView | null)?.stage_models;
  return typeof stages === "object" && stages !== null && STAGES.every((stage) => typeof stages[stage]?.provider === "string");
}

function text(value: unknown): string {
  return value == null ? "" : String(value).trim();
}

/**
 * One row per feature that calls a model: which vendor and model it runs on now, with an empty
 * choice resolved to the model it inherits, how the calls are paid for, and where to change it.
 * Pure, so the tests can pin every inheritance rule without a server.
 */
export function overviewRows(sources: OverviewSources, t: Translate, stageName: (stage: string) => string): OverviewRow[] {
  const cards = new Map((sources.providers?.providers ?? []).map((card) => [card.provider, card]));
  const config = (provider: string) => cards.get(provider)?.config ?? {};
  const label = (provider: string, field: string, id: string) =>
    cards.get(provider)?.field_options?.[field]?.find((option) => option.value === id)?.label ?? id;
  const planner = config("ai_planner");
  const guide = config("ai_guide_search");
  const intro = config("hotspot_intros");
  // The Claude connection switch exists once the site can run Claude on the subscription accounts.
  const vendorsCard = config("ai_vendors");
  const canSubscribe = "anthropic_connection" in vendorsCard;
  const onSubscription = text(vendorsCard.anthropic_connection) === "subscription";
  const siteConnection = (vendor: string): Connection => vendor === "anthropic" && onSubscription ? "subscriptionFallback" : "apiKey";
  const siteSupport: Support = canSubscribe ? "claudeSubscription" : "apiKeyOnly";
  const rows: OverviewRow[] = [];

  if (sources.providers) {
    const plannerModel = (vendor: Vendor) => label("ai_planner", `${vendor}_model`, text(planner[`${vendor}_model`]));
    const mode = text(planner.ai_planner_mode);
    let vendor = "";
    let model = "";
    let connection: Connection = "apiKey";
    if (isVendor(mode)) {
      vendor = vendorLabels[mode];
      model = plannerModel(mode);
    } else if (mode === "auto") {
      const order = text(planner.ai_planner_priority).split(",").map((item) => item.trim().toLowerCase()).filter(isVendor);
      vendor = t("overview.plannerAuto");
      model = order.map((each) => `${vendorLabels[each]} ${plannerModel(each)}`).join(" → ");
    } else {
      vendor = t(mode === "disabled" ? "overview.plannerDisabled" : "overview.plannerFallback");
      connection = "none";
    }
    rows.push({ key: "planner", feature: t("overview.features.planner"), vendor, model, connection, support: "apiKeyOnly", gemini: mode === "gemini", edit: settingsHref("providers", "ai_planner", "ai_planner_mode"), open: "/trips/new" });

    const guideVendor = text(guide.hotspot_guide_ai_default_provider);
    if (isVendor(guideVendor)) {
      const own = text(guide[`hotspot_guide_ai_${guideVendor}_model`]);
      rows.push({
        key: "guideSearch", feature: t("overview.features.guideSearch"), vendor: vendorLabels[guideVendor],
        model: own ? label("ai_guide_search", `hotspot_guide_ai_${guideVendor}_model`, own) : plannerModel(guideVendor),
        inherited: own ? undefined : t("overview.features.planner"),
        connection: siteConnection(guideVendor), support: siteSupport, gemini: guideVendor === "gemini",
        edit: settingsHref("providers", "ai_guide_search", "hotspot_guide_ai_default_provider"), open: "/admin/hotspots?tab=content&section=guides",
      });
    }
    const introVendor = text(intro.hotspot_intro_ai_default_provider);
    if (isVendor(introVendor)) {
      const own = text(intro[`hotspot_intro_ai_${introVendor}_model`]);
      const fromGuide = text(guide[`hotspot_guide_ai_${introVendor}_model`]);
      rows.push({
        key: "intros", feature: t("overview.features.intros"), vendor: vendorLabels[introVendor],
        model: own ? label("hotspot_intros", `hotspot_intro_ai_${introVendor}_model`, own) : fromGuide ? label("ai_guide_search", `hotspot_guide_ai_${introVendor}_model`, fromGuide) : plannerModel(introVendor),
        inherited: own ? undefined : t(fromGuide ? "overview.features.guideSearch" : "overview.features.planner"),
        connection: siteConnection(introVendor), support: siteSupport, gemini: introVendor === "gemini",
        edit: settingsHref("providers", "hotspot_intros", "hotspot_intro_ai_default_provider"), open: "/admin/hotspots?tab=content&section=intros",
      });
    }
    const gemini = text(config("gemini_guides").hotspot_guide_gemini_model);
    if (gemini) rows.push({ key: "geminiSearch", feature: t("overview.features.geminiSearch"), vendor: vendorLabels.gemini, model: label("gemini_guides", "hotspot_guide_gemini_model", gemini), connection: "apiKey", support: "apiKeyOnly", gemini: true, edit: settingsHref("providers", "gemini_guides", "hotspot_guide_gemini_model"), open: "/admin/catalog-review" });
  }

  const news = sources.news;
  if (isNewsSettings(news)) {
    for (const kind of ["writer", "verifier", "editor"] as const) {
      const provider = news[`${kind}_provider`];
      const options = news.model_options?.[provider] ?? [];
      const chosen = news[`${kind}_model`];
      const id = chosen ?? news.default_models?.[provider] ?? "";
      rows.push({
        key: `news-${kind}`, feature: t(`overview.features.${({ writer: "newsWriter", verifier: "newsVerifier", editor: "newsEditor" } as const)[kind]}`), vendor: newsProviderLabels[provider],
        model: options.find((option) => option.value === id)?.label ?? id, inherited: chosen ? undefined : t("overview.features.guideSearch"),
        connection: siteConnection(provider), support: siteSupport, gemini: provider === "gemini", edit: "#ai-models-news", open: "/admin/news?tab=settings",
      });
    }
  }

  const video = sources.video;
  if (isVideoSettings(video)) {
    for (const stage of STAGES) {
      const choice = video.stage_models[stage];
      rows.push({
        key: `video-${stage}`, feature: t("overview.features.video", { stage: stageName(stage) }), vendor: videoProviderLabels[choice.provider],
        model: video.model_options?.[choice.provider]?.find((option) => option.value === choice.model)?.label ?? choice.model,
        connection: choice.provider === "claude_code" ? "subscription" : "apiKey", support: "claudeCode", gemini: choice.provider === "gemini", edit: "#ai-models-video", open: "/admin/videos?tab=settings",
      });
    }
  }
  return rows.map((row) => row.gemini ? { ...row, support: "geminiApiKeyOnly" } : row);
}

const connectionTone: Record<Connection, string> = {
  apiKey: "border-[var(--line)] bg-[var(--paper)]",
  subscription: "border-emerald-300 bg-emerald-50 text-emerald-900",
  subscriptionFallback: "border-emerald-300 bg-emerald-50 text-emerald-900",
  none: "border-[var(--line)] bg-[var(--paper)] text-[var(--muted)]",
};

/**
 * Every feature's model in one table, on the AI settings page's models tab. Each source loads on
 * its own, so a reader without the news or video permission still sees the other rows.
 */
export function AdminAiModelOverview({ refresh = 0 }: { refresh?: number }) {
  const t = useTranslations("admin.aiSettings");
  const locale = useLocale();
  const stages = useTranslations("admin.videoSettings.stages");
  const [sources, setSources] = useState<OverviewSources>({});
  const [missing, setMissing] = useState<string[]>([]);
  const [tick, setTick] = useState(0);
  useEffect(() => {
    let live = true;
    void Promise.allSettled([
      api<Snapshot>("/admin/provider-settings"),
      api<NewsSettings>("/admin/news/settings"),
      api<VideoSettingsView>("/admin/video-automation/settings"),
    ]).then(([providers, news, video]) => {
      if (!live) return;
      const value = <T,>(result: PromiseSettledResult<T>) => result.status === "fulfilled" ? result.value : undefined;
      const snapshot = value(providers);
      const loaded = {
        providers: Array.isArray(snapshot?.providers) ? snapshot : undefined,
        news: isNewsSettings(value(news)) ? value(news) : undefined,
        video: isVideoSettings(value(video)) ? value(video) : undefined,
      };
      setSources(loaded);
      setMissing((["providers", "news", "video"] as const).filter((name) => !loaded[name]));
    });
    return () => { live = false; };
  }, [refresh, tick]);

  const rows = overviewRows(sources, (key, values) => t(key, values), (stage) => stages(stage));
  // Every editor is on this page. The settings panel follows the URL through the admin
  // location event, which a Next <Link> to the same page does not send.
  function edit(event: React.MouseEvent<HTMLAnchorElement>, target: string) {
    if (event.metaKey || event.ctrlKey || event.shiftKey || event.button !== 0) return;
    event.preventDefault();
    if (target.startsWith("#")) {
      document.getElementById(target.slice(1))?.scrollIntoView({ block: "start" });
      return;
    }
    const url = new URL(`/${locale}${target}`, window.location.href);
    adminNavigate(url);
  }
  return <section className="mt-4 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-5" aria-labelledby="ai-models-overview">
    <div className="flex flex-wrap items-baseline justify-between gap-2">
      <h2 id="ai-models-overview" className="text-xl font-bold">{t("overview.title")}</h2>
      <button type="button" onClick={() => setTick((value) => value + 1)} className="inline-flex min-h-11 items-center gap-2 text-sm font-semibold text-[var(--teal)]"><RefreshCw aria-hidden size={16} />{t("overview.refresh")}</button>
    </div>
    <p className="mt-2 max-w-3xl text-sm leading-6 text-[var(--muted)]">{t("overview.help")}</p>
    {missing.length > 0 && <p className="mt-2 text-sm text-amber-800">{t("overview.missing", { sources: missing.map((name) => t(`overview.sources.${name}`)).join("、") })}</p>}
    <div className="mt-4 hidden grid-cols-[minmax(10rem,1.2fr)_minmax(12rem,2fr)_minmax(9rem,1fr)_minmax(10rem,1fr)_auto] gap-x-4 border-b border-[var(--line)] pb-2 text-xs font-bold text-[var(--muted)] md:grid" aria-hidden>
      <span>{t("overview.columns.feature")}</span><span>{t("overview.columns.model")}</span><span>{t("overview.columns.connection")}</span><span>{t("overview.columns.support")}</span><span />
    </div>
    <ul className="divide-y divide-[var(--line)]">{rows.map((row) => <li key={row.key} data-overview-row={row.key} className="grid gap-2 py-3 text-sm md:grid-cols-[minmax(10rem,1.2fr)_minmax(12rem,2fr)_minmax(9rem,1fr)_minmax(10rem,1fr)_auto] md:items-center md:gap-x-4">
      <span className="font-semibold">{row.feature}</span>
      <span className="min-w-0 break-words">{row.vendor}{row.model ? ` · ${row.model}` : ""}{row.inherited && <span className="block text-xs text-[var(--muted)]">{t("overview.inherits", { source: row.inherited })}</span>}</span>
      <span><span className={`inline-block rounded-full border px-2 py-0.5 text-xs font-semibold ${connectionTone[row.connection]}`}>{t(`overview.connection.${row.connection}`)}</span></span>
      <span className={`text-xs leading-5 ${row.support === "apiKeyOnly" || row.support === "geminiApiKeyOnly" ? "font-semibold text-amber-800" : "text-[var(--muted)]"}`}>{t(`overview.support.${row.support}`)}</span>
      <span className="flex flex-wrap gap-x-4">
        <a href={row.edit.startsWith("#") ? row.edit : `/${locale}${row.edit}`} onClick={(event) => edit(event, row.edit)} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{t("overview.edit")}</a>
        {row.open && <Link href={row.open} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{t("overview.open")}</Link>}
      </span>
    </li>)}</ul>
  </section>;
}
