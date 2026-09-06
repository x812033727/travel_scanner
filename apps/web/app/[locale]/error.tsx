"use client";

import { RefreshCw, TriangleAlert } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect } from "react";
import { Link } from "@/i18n/navigation";

/**
 * Without this file a render error fell through to Next's own screen: English
 * only, on a site that ships five languages, and with no way back other than the
 * browser's own buttons. Two large controls and one sentence that says it is not
 * the reader's fault.
 */
export default function LocaleError({ error, reset }: { error: Error & { digest?: string }; reset: () => void }) {
  const t = useTranslations("errors");
  useEffect(() => {
    console.error(error);
  }, [error]);
  return (
    <main className="mx-auto flex min-h-[70vh] max-w-3xl flex-col items-center justify-center px-5 py-16 text-center md:px-8">
      <TriangleAlert aria-hidden className="text-[var(--coral)]" size={44} />
      <h1 className="mt-5 text-3xl font-bold">{t("pageTitle")}</h1>
      <p className="mx-auto mt-3 max-w-xl leading-8 text-[var(--muted)]">{t("pageBody")}</p>
      <div className="mt-8 flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
        <button
          type="button"
          onClick={reset}
          className="inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl bg-[var(--teal-fill)] px-6 text-base font-semibold text-white"
        >
          <RefreshCw aria-hidden size={19} />
          {t("retry")}
        </button>
        <Link
          href="/"
          className="inline-flex min-h-12 items-center justify-center rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-6 text-base font-semibold text-[var(--ink)]"
        >
          {t("backHome")}
        </Link>
      </div>
      {error.digest && <p className="mt-6 text-xs text-[var(--muted)]">{t("reference", { digest: error.digest })}</p>}
    </main>
  );
}
