"use client";

import { useLocale, useTranslations } from "next-intl";
import { useState } from "react";
import { MonthToggles } from "./admin-hotspot-themes-panel";
import { api } from "@/lib/api";
import { type ThemeKind, monthRangeLabel } from "@/lib/hotspot-themes";

export type AssignedTheme = {
  slug: string;
  kind?: ThemeKind;
  name?: string;
  months?: number[] | null;
  months_overridden?: boolean;
  is_active?: boolean;
};

type CatalogTheme = { slug: string; kind: ThemeKind; name: string; months: number[] };

type Draft = { months: number[] | null };

/**
 * Assign themes to one attraction.
 *
 * PUT replaces the whole set, so the dialog will not open until it has read what
 * the attraction currently carries: saving a guess would silently drop themes it
 * never showed anybody.
 */
export function AdminHotspotThemeEditor({
  hotspotId,
  hotspotName,
  category,
  initial,
}: {
  hotspotId: string;
  hotspotName: string;
  category: string;
  initial?: AssignedTheme[];
}) {
  const t = useTranslations("hotspotThemes");
  const locale = useLocale();
  const [open, setOpen] = useState(false);
  const [catalog, setCatalog] = useState<CatalogTheme[]>([]);
  const [draft, setDraft] = useState<Map<string, Draft>>(new Map());
  const [assigned, setAssigned] = useState<AssignedTheme[]>(initial ?? []);
  const [loading, setLoading] = useState(false);
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  async function openEditor() {
    setLoading(true);
    setError("");
    try {
      const [themes, current] = await Promise.all([
        api<{ items: CatalogTheme[] }>("/admin/hotspots/themes?status=active"),
        api<{ themes: AssignedTheme[] }>(`/admin/hotspots/${hotspotId}/themes`),
      ]);
      setCatalog(themes.items ?? []);
      const live = (current.themes ?? []).filter((item) => item.is_active !== false);
      setAssigned(live);
      setDraft(
        new Map(
          live.map((item) => [
            item.slug,
            { months: item.months_overridden ? (item.months ?? null) : null },
          ]),
        ),
      );
      setOpen(true);
    } catch {
      setError(t("editor.loadFailed"));
    } finally {
      setLoading(false);
    }
  }

  async function save() {
    setSaving(true);
    setError("");
    try {
      const payload = [...draft.entries()].map(([slug, value]) =>
        value.months ? { slug, months: value.months } : { slug },
      );
      const result = await api<{ themes: AssignedTheme[] }>(
        `/admin/hotspots/${hotspotId}/themes`,
        { method: "PUT", body: JSON.stringify({ themes: payload }) },
      );
      setAssigned(result.themes ?? []);
      setNotice(t("editor.saved", { name: hotspotName }));
      setOpen(false);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }

  function toggle(theme: CatalogTheme) {
    setDraft((current) => {
      const next = new Map(current);
      if (next.has(theme.slug)) next.delete(theme.slug);
      else next.set(theme.slug, { months: null });
      return next;
    });
  }

  const shopAllowed = category === "shopping";

  return (
    <>
      <div className="flex flex-wrap items-center gap-1.5">
        {assigned.length === 0 ? (
          <span className="text-xs text-[var(--muted)]">{t("editor.none")}</span>
        ) : (
          assigned.map((item) => (
            <span
              key={item.slug}
              className="rounded-full bg-[var(--teal-soft)] px-2 py-0.5 text-xs font-semibold text-[var(--teal-dark)]"
            >
              {item.name ?? item.slug}
            </span>
          ))
        )}
        <button
          type="button"
          disabled={loading}
          aria-label={t("editor.title", { name: hotspotName })}
          onClick={() => void openEditor()}
          className="min-h-11 rounded-xl border border-[var(--line)] px-3 text-xs font-semibold disabled:opacity-60"
        >
          {loading ? t("loading") : t("editor.open")}
        </button>
      </div>
      {notice && <p className="mt-1 text-xs text-[var(--teal-dark)]">{notice}</p>}
      {error && !open && (
        <p role="alert" className="mt-1 text-xs text-[var(--coral)]">
          {error}
        </p>
      )}

      {open && (
        <div className="fixed inset-0 z-[80] grid place-items-center bg-slate-950/45 p-4">
          <div
            role="dialog"
            aria-modal="true"
            aria-label={t("editor.title", { name: hotspotName })}
            className="max-h-[90dvh] w-full max-w-xl overflow-y-auto rounded-3xl bg-[var(--paper)] p-6"
          >
            <h3 className="text-lg font-bold">{t("editor.title", { name: hotspotName })}</h3>
            <p className="mt-1 text-sm text-[var(--muted)]">{t("editor.description")}</p>
            {!shopAllowed && (
              <p className="mt-2 text-xs text-[var(--muted)]">{t("editor.shopOnly")}</p>
            )}
            {error && (
              <p role="alert" className="mt-2 rounded-xl bg-[var(--coral-soft)] p-2 text-sm">
                {error}
              </p>
            )}
            {catalog.length === 0 && (
              <p className="mt-3 text-sm text-[var(--muted)]">{t("editor.noThemes")}</p>
            )}

            <div className="mt-4 grid gap-3">
              {catalog.map((theme) => {
                const chosen = draft.get(theme.slug);
                const disabled = theme.kind === "shop" && !shopAllowed;
                return (
                  <div key={theme.slug} className="rounded-2xl border border-[var(--line)] bg-white p-3">
                    <label className="flex items-center gap-2 text-sm font-semibold">
                      <input
                        type="checkbox"
                        checked={draft.has(theme.slug)}
                        disabled={disabled}
                        onChange={() => toggle(theme)}
                      />
                      {theme.name}
                      <span className="text-xs font-normal text-[var(--muted)]">
                        {t(`kinds.${theme.kind}`)}
                      </span>
                    </label>
                    {chosen && theme.kind === "season" && (
                      <div className="mt-2 pl-6">
                        <label className="flex items-center gap-2 text-xs">
                          <input
                            type="checkbox"
                            checked={chosen.months === null}
                            onChange={(event) =>
                              setDraft((current) => {
                                const next = new Map(current);
                                next.set(theme.slug, {
                                  months: event.target.checked ? null : [...theme.months],
                                });
                                return next;
                              })
                            }
                          />
                          {t("editor.defaultMonths", {
                            months: monthRangeLabel(theme.months, locale) || t("months.none"),
                          })}
                        </label>
                        {chosen.months !== null && (
                          <div className="mt-2">
                            <MonthToggles
                              months={chosen.months}
                              onChange={(months) =>
                                setDraft((current) => {
                                  const next = new Map(current);
                                  next.set(theme.slug, { months });
                                  return next;
                                })
                              }
                              locale={locale}
                              label={t("months.label")}
                            />
                          </div>
                        )}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>

            <div className="mt-5 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="min-h-11 rounded-xl border border-[var(--line)] px-4 font-semibold"
              >
                {t("cancel")}
              </button>
              <button
                type="button"
                disabled={saving}
                onClick={() => void save()}
                className="min-h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-60"
              >
                {saving ? t("saving") : t("editor.save")}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
