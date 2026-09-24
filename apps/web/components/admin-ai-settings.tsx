"use client";

import { KeyRound, UsersRound } from "lucide-react";
import { useTranslations } from "next-intl";
import { AdminAiAccountsPanel } from "@/components/admin-ai-accounts-panel";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AI_PAGE_CATEGORIES, AdminSettingsPanel } from "@/components/admin-settings-panel";
import { useAdminQueryState } from "@/lib/admin-workspace-navigation";

const TABS = ["subscriptions", "api"] as const;
type Tab = (typeof TABS)[number];
const ICONS: Record<Tab, typeof KeyRound> = { subscriptions: UsersRound, api: KeyRound };

/**
 * One place for everything AI: the subscription accounts the host's Claude Code and
 * Codex CLIs sign in with, and the API keys and models the site's own features use.
 * The subscription tab signs root's CLIs in on the host, so like its API it is for the
 * owner only; everyone who may read settings gets the API tab.
 */
export function AdminAiSettings() {
  const t = useTranslations("admin.aiSettings");
  const owner = useAdminActionGuard("roles.manage").allowed;
  const [tab, setTab] = useAdminQueryState<Tab>("tab", TABS, owner ? "subscriptions" : "api");
  const active: Tab = owner ? tab : "api";

  function move(event: React.KeyboardEvent<HTMLButtonElement>, index: number) {
    if (!(["ArrowLeft", "ArrowRight", "Home", "End"] as string[]).includes(event.key)) return;
    event.preventDefault();
    const next = event.key === "Home" ? 0 : event.key === "End" ? TABS.length - 1 : (index + (event.key === "ArrowRight" ? 1 : -1) + TABS.length) % TABS.length;
    setTab(TABS[next]);
    requestAnimationFrame(() => document.getElementById(`ai-settings-tab-${TABS[next]}`)?.focus());
  }

  return <div className="mt-6">
    {owner && <div role="tablist" aria-label={t("tabLabel")} className="flex gap-2 overflow-x-auto border-b border-[var(--line)] pb-3">
      {TABS.map((name, index) => {
        const selected = name === active;
        const Icon = ICONS[name];
        return <button key={name} id={`ai-settings-tab-${name}`} type="button" role="tab" aria-selected={selected} aria-controls="ai-settings-panel" tabIndex={selected ? 0 : -1} onClick={() => setTab(name)} onKeyDown={(event) => move(event, index)} className={`inline-flex min-h-11 shrink-0 items-center gap-2 rounded-xl border px-4 text-sm font-bold transition ${selected ? "border-[var(--ink)] bg-[var(--ink)] text-white" : "border-[var(--line)] bg-white text-[var(--ink)] hover:border-[var(--ink)]"}`}><Icon size={16} />{t(`tabs.${name}`)}</button>;
      })}
    </div>}
    <p className="mt-4 max-w-3xl text-sm leading-6 text-[var(--muted)]">{t(`hints.${active}`)}</p>
    <div id="ai-settings-panel" role={owner ? "tabpanel" : undefined} aria-labelledby={owner ? `ai-settings-tab-${active}` : undefined}>
      {active === "subscriptions" ? <AdminAiAccountsPanel /> : <AdminSettingsPanel scope="providers" categories={AI_PAGE_CATEGORIES} />}
    </div>
  </div>;
}
