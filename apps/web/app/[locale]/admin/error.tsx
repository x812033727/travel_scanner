"use client";

import { RefreshCw, TriangleAlert } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect } from "react";
import { Link } from "@/i18n/navigation";

/**
 * One admin panel reading a field the API did not send used to blank the whole
 * console. The rest of the admin still works, so say which part failed and keep
 * a way into the other pages.
 */
export default function AdminError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  const t = useTranslations("errors");
  useEffect(() => {
    console.error(error);
  }, [error]);
  return (
    <main className="mx-auto flex min-h-[60vh] max-w-2xl flex-col items-center justify-center px-5 py-16 text-center">
      <TriangleAlert aria-hidden className="text-[var(--coral)]" size={40} />
      <h1 className="mt-5 text-2xl font-bold">{t("adminTitle")}</h1>
      <p className="mx-auto mt-3 max-w-xl leading-8 text-[var(--muted)]">{t("adminBody")}</p>
      <div className="mt-8 flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
        <button
          type="button"
          onClick={reset}
          className="inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl bg-[var(--ink)] px-6 text-base font-semibold text-white"
        >
          <RefreshCw aria-hidden size={19} />
          {t("retry")}
        </button>
        <Link
          href="/admin"
          className="inline-flex min-h-12 items-center justify-center rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-6 text-base font-semibold text-[var(--ink)]"
        >
          {t("adminBack")}
        </Link>
      </div>
      {error.digest && <p className="mt-6 text-xs text-[var(--muted)]">{t("reference", { digest: error.digest })}</p>}
    </main>
  );
}
