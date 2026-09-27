"use client";

import { Boxes, KeyRound, UsersRound } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { AdminAiAccountsPanel } from "@/components/admin-ai-accounts-panel";
import { AdminAiModelOverview } from "@/components/admin-ai-model-overview";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminNewsModelSettings } from "@/components/admin-news-model-settings";
import { AI_PAGE_CATEGORIES, AdminSettingsPanel } from "@/components/admin-settings-panel";
import { AdminVideoModelSettings } from "@/components/admin-video-model-settings";
import { AI_KEY_PROVIDERS, AI_MODEL_PROVIDERS, aiSettingsTab } from "@/lib/admin-settings-ownership";
import { adminNavigate, useAdminQueryState, useAdminQueryValue } from "@/lib/admin-workspace-navigation";

const TABS = ["subscriptions", "api", "models"] as const;
type Tab = (typeof TABS)[number];
const ICONS: Record<Tab, typeof KeyRound> = { subscriptions: UsersRound, api: KeyRound, models: Boxes };
const SECTIONS = ["news", "video"] as const;

/**
 * One place for everything AI: the subscription accounts the host's Claude Code and
 * Codex CLIs sign in with, the API keys, and the model of every feature. The subscription
 * tab signs root's CLIs in on the host, so like its API it is for the owner only; everyone
 * who may read settings gets the keys and models tabs.
 */
export function AdminAiSettings() {
  const t = useTranslations("admin.aiSettings");
  const owner = useAdminActionGuard("roles.manage").allowed;
  const [tab] = useAdminQueryState<Tab>("tab", TABS, owner ? "subscriptions" : "api");
  const [provider] = useAdminQueryValue("provider", "", (value) => /^[a-z_]{1,64}$/.test(value));
  const [section] = useAdminQueryValue("section", "", (value) => (SECTIONS as readonly string[]).includes(value));
  // Links made while the model cards sat on the keys tab still name tab=api.
  const linked: Tab = tab === "api" && provider && aiSettingsTab(provider) === "models" ? "models" : tab;
  const active: Tab = owner || linked !== "subscriptions" ? linked : "api";
  const tabs = owner ? TABS : TABS.filter((name) => name !== "subscriptions");
  const [refresh, setRefresh] = useState(0);
  useEffect(() => {
    if (active !== "models" || !section) return;
    const frame = requestAnimationFrame(() => document.getElementById(`ai-models-${section}`)?.scrollIntoView({ block: "start" }));
    return () => cancelAnimationFrame(frame);
  }, [active, section]);

  // A tab click drops the card and section a link pointed at, which belong to the old tab.
  function setTab(name: Tab) {
    const target = new URL(window.location.href);
    target.searchParams.set("tab", name);
    for (const key of ["provider", "field", "section"]) target.searchParams.delete(key);
    adminNavigate(target);
  }

  function move(event: React.KeyboardEvent<HTMLButtonElement>, index: number) {
    if (!(["ArrowLeft", "ArrowRight", "Home", "End"] as string[]).includes(event.key)) return;
    event.preventDefault();
    const next = event.key === "Home" ? 0 : event.key === "End" ? tabs.length - 1 : (index + (event.key === "ArrowRight" ? 1 : -1) + tabs.length) % tabs.length;
    setTab(tabs[next]);
    requestAnimationFrame(() => document.getElementById(`ai-settings-tab-${tabs[next]}`)?.focus());
  }

  return <div className="mt-6">
    <div role="tablist" aria-label={t("tabLabel")} className="flex gap-2 overflow-x-auto border-b border-[var(--line)] pb-3">
      {tabs.map((name, index) => {
        const selected = name === active;
        const Icon = ICONS[name];
        return <button key={name} id={`ai-settings-tab-${name}`} type="button" role="tab" aria-selected={selected} aria-controls="ai-settings-panel" tabIndex={selected ? 0 : -1} onClick={() => setTab(name)} onKeyDown={(event) => move(event, index)} className={`inline-flex min-h-11 shrink-0 items-center gap-2 rounded-xl border px-4 text-sm font-bold transition ${selected ? "border-[var(--ink)] bg-[var(--ink)] text-white" : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--ink)]"}`}><Icon size={16} />{t(`tabs.${name}`)}</button>;
      })}
    </div>
    <p className="mt-4 max-w-3xl text-sm leading-6 text-[var(--muted)]">{t(`hints.${active}`)}</p>
    <div id="ai-settings-panel" role="tabpanel" aria-labelledby={`ai-settings-tab-${active}`}>
      {active === "subscriptions" && <AdminAiAccountsPanel />}
      {active === "api" && <AdminSettingsPanel key="api" scope="providers" categories={AI_PAGE_CATEGORIES} providers={AI_KEY_PROVIDERS} />}
      {active === "models" && <>
        <AdminAiModelOverview refresh={refresh} />
        <AdminSettingsPanel key="models" scope="providers" categories={AI_PAGE_CATEGORIES} providers={AI_MODEL_PROVIDERS} focusFirst={false} />
        <div className="mt-6 grid gap-5">
          <AdminNewsModelSettings onSaved={() => setRefresh((value) => value + 1)} />
          <AdminVideoModelSettings onSaved={() => setRefresh((value) => value + 1)} />
        </div>
      </>}
    </div>
  </div>;
}
