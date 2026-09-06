"use client";

import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import {
  LocalizedNameFields,
  type LocalizedNames,
  blankNames,
  completeNames,
} from "./admin-food-taxonomy-panel";
import { FilterPills } from "./admin-filter-pills";
import { api } from "@/lib/api";
import { type ThemeKind, monthRangeLabel } from "@/lib/hotspot-themes";

export type AdminTheme = {
  id: string;
  slug: string;
  kind: ThemeKind;
  names: LocalizedNames;
  months: number[];
  display_order: number;
  is_active: boolean;
  source: string;
  hotspot_count: number;
};

const MONTHS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12];

/** The reader's own label, falling back the way the server does. */
function localizedName(theme: AdminTheme, locale: string): string {
  const names = theme.names as Record<string, string | undefined>;
  return names[locale] || names["zh-TW"] || names.en || theme.slug;
}

/** Twelve toggles; a season may wrap the year, so this is a set, not a range. */
export function MonthToggles({
  months,
  onChange,
  locale,
  label,
}: {
  months: number[];
  onChange: (next: number[]) => void;
  locale: string;
  label: string;
}) {
  const format = new Intl.DateTimeFormat(locale, { month: "short", timeZone: "UTC" });
  return (
    <div role="group" aria-label={label} className="flex flex-wrap gap-1.5">
      {MONTHS.map((month) => {
        const selected = months.includes(month);
        return (
          <button
            key={month}
            type="button"
            aria-pressed={selected}
            onClick={() =>
              onChange(
                selected
                  ? months.filter((item) => item !== month)
                  : [...months, month].sort((first, second) => first - second),
              )
            }
            className={`app-filter-chip ${selected ? "app-filter-chip-active" : ""}`}
          >
            {format.format(new Date(Date.UTC(2024, month - 1, 15, 12)))}
          </button>
        );
      })}
    </div>
  );
}

function readTheme(raw: Record<string, unknown>): AdminTheme {
  const months = (raw.months ?? raw.months_json ?? []) as number[];
  return {
    id: String(raw.id ?? ""),
    slug: String(raw.slug ?? ""),
    kind: (raw.kind === "shop" ? "shop" : "season") as ThemeKind,
    names: completeNames((raw.names ?? raw.names_json) as Partial<LocalizedNames>),
    months: Array.isArray(months) ? months : [],
    display_order: Number(raw.display_order ?? 100),
    is_active: raw.is_active !== false,
    source: String(raw.source ?? "admin"),
    hotspot_count: Number(raw.hotspot_count ?? 0),
  };
}

function blankTheme(): AdminTheme {
  return {
    id: "",
    slug: "",
    kind: "season",
    names: blankNames(),
    months: [],
    display_order: 100,
    is_active: true,
    source: "admin",
    hotspot_count: 0,
  };
}

export function AdminHotspotThemesPanel() {
  const t = useTranslations("hotspotThemes");
  const locale = useLocale();
  const [themes, setThemes] = useState<AdminTheme[]>([]);
  const [kind, setKind] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [draft, setDraft] = useState<AdminTheme | null>(null);
  const [saving, setSaving] = useState(false);

  const load = useCallback(async () => {
    setLoading(true);
    setError("");
    try {
      const result = await api<{ items: Record<string, unknown>[] }>("/admin/hotspots/themes");
      setThemes((result.items ?? []).map(readTheme));
    } catch {
      setError(t("loadFailed"));
    } finally {
      setLoading(false);
    }
  }, [t]);

  useEffect(() => {
    // Deferred a tick: the panels' loaders set state synchronously, and calling one
    // straight from an effect body trips react-hooks/set-state-in-effect.
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function save() {
    if (!draft) return;
    if (Object.values(draft.names).some((value) => !value.trim())) {
      setError(t("themes.nameRequired"));
      return;
    }
    if (draft.kind === "season" && draft.months.length === 0) {
      setError(t("themes.monthsRequired"));
      return;
    }
    setSaving(true);
    setError("");
    try {
      const body = {
        names: draft.names,
        months: draft.kind === "shop" ? [] : draft.months,
        display_order: draft.display_order,
        is_active: draft.is_active,
      };
      if (draft.id) {
        await api(`/admin/hotspots/themes/${draft.id}`, {
          method: "PATCH",
          body: JSON.stringify(body),
        });
        setNotice(t("themes.updated"));
      } else {
        await api("/admin/hotspots/themes", {
          method: "POST",
          body: JSON.stringify({ ...body, slug: draft.slug.trim(), kind: draft.kind }),
        });
        setNotice(t("themes.created"));
      }
      setDraft(null);
      await load();
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }

  const visible = kind ? themes.filter((theme) => theme.kind === kind) : themes;
  const monthsLabel = (theme: AdminTheme) => {
    if (theme.kind === "shop") return "—";
    if (theme.months.length === 12) return t("months.allYear");
    return monthRangeLabel(theme.months, locale) || t("months.none");
  };

  return (
    <section className="mt-6">
      <h2 className="text-xl font-bold">{t("themes.title")}</h2>
      <p className="mt-1 max-w-3xl text-sm text-[var(--muted)]">{t("themes.description")}</p>

      <div className="mt-4 flex flex-wrap items-center gap-3">
        <FilterPills
          label={t("themes.kindFilter")}
          allLabel={t("themes.allKinds")}
          options={[
            { code: "season", label: t("kinds.season") },
            { code: "shop", label: t("kinds.shop") },
          ]}
          value={kind}
          onChange={setKind}
        />
        <button
          type="button"
          onClick={() => {
            setError("");
            setDraft(blankTheme());
          }}
          className="min-h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white"
        >
          {t("themes.add")}
        </button>
        <button
          type="button"
          onClick={() => void load()}
          className="min-h-11 rounded-xl border border-[var(--line)] px-4 font-semibold"
        >
          {t("refresh")}
        </button>
      </div>

      {notice && <p className="mt-3 rounded-xl bg-[var(--teal-soft)] p-3 text-sm">{notice}</p>}
      {error && (
        <p role="alert" className="mt-3 rounded-xl bg-[var(--coral-soft)] p-3 text-sm">
          {error}
        </p>
      )}
      {loading && <p className="mt-4 text-sm text-[var(--muted)]">{t("loading")}</p>}
      {!loading && visible.length === 0 && (
        <p className="mt-4 text-sm text-[var(--muted)]">{t("themes.empty")}</p>
      )}

      {visible.length > 0 && (
        <ul className="mt-4 grid gap-2">
          {visible.map((theme) => (
            <li
              key={theme.id}
              className="flex flex-wrap items-center gap-3 rounded-2xl border border-[var(--line)] bg-white p-3"
            >
              <span className="min-w-40 font-semibold">{localizedName(theme, locale)}</span>
              <span className="text-xs text-[var(--muted)]">{theme.slug}</span>
              <span className="rounded-full bg-[var(--paper)] px-2 py-0.5 text-xs">
                {t(`kinds.${theme.kind}`)}
              </span>
              <span className="text-xs text-[var(--muted)]">{monthsLabel(theme)}</span>
              <span className="text-xs text-[var(--muted)]">
                {t("themes.hotspotCount", { count: theme.hotspot_count })}
              </span>
              <span className="text-xs">{theme.is_active ? t("active") : t("inactive")}</span>
              <button
                type="button"
                onClick={() => {
                  setError("");
                  setDraft(theme);
                }}
                className="ml-auto min-h-11 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"
              >
                {t("edit")}
              </button>
            </li>
          ))}
        </ul>
      )}

      {draft && (
        <div className="fixed inset-0 z-[80] grid place-items-center bg-slate-950/45 p-4">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="theme-editor-title"
            className="max-h-[90dvh] w-full max-w-2xl overflow-y-auto rounded-3xl bg-[var(--paper)] p-6"
          >
            <h3 id="theme-editor-title" className="text-lg font-bold">
              {draft.id
                ? t("themes.editTitle", { name: draft.names["zh-TW"] || draft.slug })
                : t("themes.createTitle")}
            </h3>
            <div className="mt-4 grid gap-4">
              <label className="text-sm font-semibold">
                {t("themes.slug")}
                <input
                  value={draft.slug}
                  disabled={Boolean(draft.id)}
                  onChange={(event) => setDraft({ ...draft, slug: event.target.value })}
                  className="mt-1 h-11 w-full rounded-xl border px-3 disabled:opacity-60"
                />
                <span className="mt-1 block text-xs font-normal text-[var(--muted)]">
                  {t("themes.slugHelp")}
                </span>
              </label>
              <label className="text-sm font-semibold">
                {t("themes.kind")}
                <select
                  value={draft.kind}
                  disabled={Boolean(draft.id)}
                  onChange={(event) =>
                    setDraft({ ...draft, kind: event.target.value as ThemeKind })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3 disabled:opacity-60"
                >
                  <option value="season">{t("kinds.season")}</option>
                  <option value="shop">{t("kinds.shop")}</option>
                </select>
              </label>
              {draft.kind === "season" && (
                <div>
                  <p className="text-sm font-semibold">{t("months.label")}</p>
                  <div className="mt-2">
                    <MonthToggles
                      months={draft.months}
                      onChange={(months) => setDraft({ ...draft, months })}
                      locale={locale}
                      label={t("months.label")}
                    />
                  </div>
                  <p className="mt-1 text-xs text-[var(--muted)]">{t("months.help")}</p>
                </div>
              )}
              <LocalizedNameFields
                names={draft.names}
                onChange={(names) => setDraft({ ...draft, names })}
                label={(item) => t("localizedName", { locale: item })}
              />
              <label className="text-sm font-semibold">
                {t("themes.displayOrder")}
                <input
                  type="number"
                  value={draft.display_order}
                  onChange={(event) =>
                    setDraft({ ...draft, display_order: Number(event.target.value) })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="flex items-center gap-2 text-sm font-semibold">
                <input
                  type="checkbox"
                  checked={draft.is_active}
                  onChange={(event) => setDraft({ ...draft, is_active: event.target.checked })}
                />
                {t("active")}
              </label>
            </div>
            <div className="mt-5 flex justify-end gap-2">
              <button
                type="button"
                onClick={() => setDraft(null)}
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
                {saving ? t("saving") : t("themes.save")}
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
