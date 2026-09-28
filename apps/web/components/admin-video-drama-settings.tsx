"use client";

import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminVideoSettingsDrama } from "@/components/admin-video-settings-drama";
import { SettingsPermissionNotice, type StagePrompt, type VideoSettingsView } from "@/components/admin-video-settings";
import { panelClass } from "@/components/community/ui";
import { api } from "@/lib/api";

export { missingMediaKeys, SERIES_IN_FLIGHT_MAX } from "@/components/admin-video-settings-drama";

/**
 * The drama route's settings, on the drama tab beside the series and the one-off dramas
 * (docs/videos/DRAMA-FLOW.md, section 1). The parent reads the settings once and hands them in,
 * so the tab's minute-by-minute refresh never throws away what the owner is typing; a save sends
 * the drama object alone and the API keeps every other field as stored.
 */
export function AdminVideoDramaSettings({ view, onSaved }: { view: VideoSettingsView; onSaved: (view: VideoSettingsView) => void }) {
  const t = useTranslations("admin.videoSettings");
  const manage = useAdminActionGuard("settings.manage");
  // Open while the route is off, so the switch that starts everything is the first thing in view.
  const [open] = useState(!view.drama.drama_enabled);
  const [prompts, setPrompts] = useState<StagePrompt[]>([]);
  useEffect(() => {
    // The prompts as the worker last sent them; a site from before they were kept answers 404.
    api<{ prompts: StagePrompt[] }>("/admin/video-automation/prompts").then((value) => setPrompts(value.prompts ?? [])).catch(() => setPrompts([]));
  }, []);

  return <details className={panelClass} open={open}>
    <summary className="cursor-pointer text-lg font-bold">{t("dramaSettingsTitle")}</summary>
    <div className="mt-4 grid gap-4">
      <SettingsPermissionNotice capability="settings.manage" />
      <AdminVideoSettingsDrama view={view} prompts={prompts} canManage={manage.allowed} onSaved={onSaved} />
    </div>
  </details>;
}
