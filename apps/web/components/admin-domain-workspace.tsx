"use client";

import type { ReactNode } from "react";
import { useLocale } from "next-intl";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import type { useAdminWorkspaceNavigation } from "@/lib/admin-workspace-navigation";
import { AdminTabPanel, AdminTabs, type AdminTab } from "./admin-tabs";

export function AdminDomainWorkspace({ id, tabs, sections, navigation, children, settings }: {
  id: string;
  tabs: AdminTab[];
  sections: AdminTab[];
  navigation: ReturnType<typeof useAdminWorkspaceNavigation>;
  children: ReactNode;
  settings: ReactNode;
}) {
  const copy = adminDomainsCopy(useLocale());
  const { tab, section, selectTab, selectSection, ready } = navigation;
  if (!ready) return <p role="status" className="mt-6 text-[var(--muted)]">{copy.loading}</p>;
  return <div className="mt-6 min-w-0">
    <div className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3 md:p-4">
      <AdminTabs idPrefix={id} label={copy.workspace} mobileLabel={copy.workspace} tabs={tabs} active={tab} onSelect={selectTab} />
    </div>
    {tabs.map((item) => <AdminTabPanel key={item.key} idPrefix={id} tabKey={item.key} active={tab}>
      {item.key === "settings" ? settings : item.key === tab && <div className="pt-5">
        {sections.length > 1 && <AdminTabs idPrefix={id + "-" + tab} label={copy.section} mobileLabel={copy.section} tabs={sections} active={section} onSelect={selectSection} />}
        {sections.length > 1 ? sections.map((entry) => <AdminTabPanel key={entry.key} idPrefix={id + "-" + tab} tabKey={entry.key} active={section}>{entry.key === section ? children : null}</AdminTabPanel>) : children}
      </div>}
    </AdminTabPanel>)}
  </div>;
}
