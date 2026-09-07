"use client";

import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";

const LOCALES = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;

type Coverage = {
  locale: string;
  id: string | null;
  status: string | null;
  body: string | null;
  source: string | null;
};

type IntroRun = {
  run_id: string;
  status: "queued" | "running" | "partial" | "completed" | "failed";
  provider: string;
  model: string;
  requested_locales: string[];
  result: {
    created?: string[];
    kept_approved?: string[];
    rejected?: { locale: string; reason: string }[];
  } | null;
  error_code: string | null;
  error_message: string | null;
};

function isActive(run: IntroRun | null): boolean {
  return Boolean(run && (run.status === "queued" || run.status === "running"));
}

/**
 * Start one drafting run for one attraction, and watch it.
 *
 * The dialog reads the attraction's current coverage before it opens, because the two
 * questions an editor has — which languages are missing, and which are already approved
 * — are the ones that decide what to ask for. Approved paragraphs are left alone unless
 * "replace" is ticked: a redraft is not a reason to discard somebody's decision.
 */
export function AdminHotspotIntroGenerator({
  hotspotId,
  hotspotName,
  onFinished,
}: {
  hotspotId: string;
  hotspotName: string;
  onFinished?: () => void;
}) {
  const t = useTranslations("hotspotThemes");
  const [open, setOpen] = useState(false);
  const [coverage, setCoverage] = useState<Coverage[]>([]);
  const [chosen, setChosen] = useState<string[]>([]);
  const [replace, setReplace] = useState(false);
  const [loading, setLoading] = useState(false);
  const [run, setRun] = useState<IntroRun | null>(null);
  const [error, setError] = useState("");

  const active = isActive(run);

  useEffect(() => {
    if (!active || !run) return;
    const timer = window.setInterval(
      () =>
        void api<IntroRun>(`/admin/hotspots/intros/runs/${run.run_id}`)
          .then((next) => {
            setRun(next);
            if (!isActive(next)) onFinished?.();
          })
          .catch((reason: Error) => setError(reason.message)),
      1500,
    );
    return () => window.clearInterval(timer);
  }, [active, run, onFinished]);

  async function openDialog() {
    setLoading(true);
    setError("");
    try {
      const current = await api<{ locales: Coverage[] }>(`/admin/hotspots/${hotspotId}/intros`);
      const rows = current.locales ?? [];
      setCoverage(rows);
      // Default to the languages that have nothing yet: the common case is filling gaps,
      // and asking for a locale that is already written spends a model call to say the
      // same thing again.
      const missing = rows.filter((row) => !row.id).map((row) => row.locale);
      setChosen(missing.length ? missing : [...LOCALES]);
      setRun(null);
      setOpen(true);
    } catch {
      setError(t("intros.generateLoadFailed"));
    } finally {
      setLoading(false);
    }
  }

  async function start() {
    if (!chosen.length) return;
    setLoading(true);
    setError("");
    try {
      setRun(
        await api<IntroRun>(`/admin/hotspots/${hotspotId}/intros/generate`, {
          method: "POST",
          headers: { "Idempotency-Key": crypto.randomUUID() },
          body: JSON.stringify({ locales: chosen, force: replace }),
        }),
      );
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  const approved = coverage.filter((row) => row.status === "approved").map((row) => row.locale);
  const rejected = run?.result?.rejected ?? [];

  return (
    <>
      <button
        type="button"
        disabled={loading}
        onClick={() => void openDialog()}
        aria-label={t("intros.generateTitle", { name: hotspotName })}
        className="min-h-11 rounded-xl border border-[var(--line)] px-3 text-xs font-semibold disabled:opacity-60"
      >
        {loading && !open ? t("loading") : t("intros.generate")}
      </button>
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
            aria-label={t("intros.generateTitle", { name: hotspotName })}
            className="max-h-[90dvh] w-full max-w-xl overflow-y-auto rounded-3xl bg-[var(--paper)] p-6"
          >
            <h3 className="text-lg font-bold">{t("intros.generateTitle", { name: hotspotName })}</h3>
            <p className="mt-1 text-sm text-[var(--muted)]">{t("intros.generateDescription")}</p>

            {error && (
              <p role="alert" className="mt-2 rounded-xl bg-[var(--coral-soft)] p-2 text-sm">
                {error}
              </p>
            )}

            <fieldset className="mt-4" disabled={active}>
              <legend className="text-sm font-semibold">{t("intros.generateLocales")}</legend>
              <div className="mt-2 grid gap-2">
                {LOCALES.map((code) => {
                  const row = coverage.find((item) => item.locale === code);
                  return (
                    <label key={code} className="flex items-center gap-2 text-sm">
                      <input
                        type="checkbox"
                        checked={chosen.includes(code)}
                        onChange={() =>
                          setChosen((current) =>
                            current.includes(code)
                              ? current.filter((item) => item !== code)
                              : [...current, code],
                          )
                        }
                      />
                      <span className="font-semibold">{code}</span>
                      <span className="text-xs text-[var(--muted)]">
                        {row?.status
                          ? t(`intros.status.${row.status}`)
                          : t("intros.generateMissing")}
                      </span>
                    </label>
                  );
                })}
              </div>
            </fieldset>

            {approved.length > 0 && (
              <label className="mt-3 flex items-center gap-2 text-sm">
                <input
                  type="checkbox"
                  checked={replace}
                  disabled={active}
                  onChange={(event) => setReplace(event.target.checked)}
                />
                {t("intros.generateReplace", { locales: approved.join("、") })}
              </label>
            )}

            {run && (
              <div className="mt-4 rounded-2xl border border-[var(--line)] bg-white p-3 text-sm">
                <p className="font-semibold">
                  {t(`intros.runStatus.${run.status}`)} · {run.provider} / {run.model}
                </p>
                {run.result?.created?.length ? (
                  <p className="mt-1 text-[var(--teal-dark)]">
                    {t("intros.runCreated", { locales: run.result.created.join("、") })}
                  </p>
                ) : null}
                {run.result?.kept_approved?.length ? (
                  <p className="mt-1 text-[var(--muted)]">
                    {t("intros.runKept", { locales: run.result.kept_approved.join("、") })}
                  </p>
                ) : null}
                {rejected.length > 0 && (
                  <ul className="mt-1 list-disc pl-5 text-[var(--muted)]">
                    {rejected.map((item) => (
                      <li key={`${item.locale}-${item.reason}`}>
                        {t("intros.runRejected", { locale: item.locale, reason: item.reason })}
                      </li>
                    ))}
                  </ul>
                )}
                {run.error_code && (
                  <p role="alert" className="mt-1 text-[var(--coral)]">
                    {run.error_message || run.error_code}
                  </p>
                )}
              </div>
            )}

            <div className="mt-5 flex flex-wrap justify-end gap-2">
              <button
                type="button"
                onClick={() => setOpen(false)}
                disabled={active}
                className="min-h-11 rounded-xl border border-[var(--line)] px-4 text-sm font-semibold disabled:opacity-60"
              >
                {t("close")}
              </button>
              <button
                type="button"
                onClick={() => void start()}
                disabled={loading || active || !chosen.length}
                className="min-h-11 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white disabled:opacity-60"
              >
                {active ? t("intros.generateRunning") : t("intros.generateStart")}
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
