"use client";

import { Coins } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { api, ApiError } from "@/lib/api";
import {
  currencies,
  currencyName,
  defaultCurrency,
  normalizeCurrency,
  type Currency,
} from "@/lib/currency";
import { formatMoney } from "@/lib/locale-format";

const SAMPLE_AMOUNT = 1234;

export function CurrencySwitcher() {
  const common = useTranslations("common");
  const account = useTranslations("account");
  const [currency, setCurrency] = useState<Currency | null>(null);
  const [signedOut, setSignedOut] = useState(false);
  const [syncFailed, setSyncFailed] = useState(false);
  // Only the newest change may write the select back on failure. Without this a
  // slow first request failing late would undo a second choice that did save.
  const pending = useRef(0);

  useEffect(() => {
    let cancelled = false;
    api<{ preferred_currency?: string }>("/auth/me")
      .then((me) => {
        if (!cancelled) setCurrency(normalizeCurrency(me.preferred_currency));
      })
      .catch((error) => {
        if (cancelled) return;
        // Only a signed-out visitor has nowhere to put a preference. Any other
        // failure still gets a working control showing the default.
        if (error instanceof ApiError && error.status === 401) setSignedOut(true);
        else setCurrency(defaultCurrency);
      });
    return () => {
      cancelled = true;
    };
  }, []);

  async function change(next: Currency) {
    const previous = currency;
    if (next === previous) return;
    const attempt = (pending.current += 1);
    setSyncFailed(false);
    setCurrency(next);
    try {
      await api("/auth/me", { method: "PATCH", body: JSON.stringify({ preferred_currency: next }) });
    } catch {
      if (attempt !== pending.current) return;
      // The language switcher can keep a local-only choice because the cookie
      // already drives the page. A currency that only exists in this component's
      // state would be a lie, so put the saved one back.
      setCurrency(previous);
      setSyncFailed(true);
    }
  }

  // The account panel below already asks a signed-out visitor to sign in.
  if (signedOut || currency === null) return null;

  return (
    <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8">
      <h2 className="mb-4 text-xl font-bold">{account("currencyTitle")}</h2>
      <div className="space-y-2">
        <label className="flex flex-wrap items-center gap-2 text-sm font-semibold">
          <Coins aria-hidden size={19} className="shrink-0 text-[var(--teal)]" />
          <span>{common("currency")}</span>
          <select
            aria-label={common("currency")}
            value={currency}
            onChange={(event) => void change(event.target.value as Currency)}
            className="min-h-11 min-w-0 max-w-full flex-1 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold text-[var(--ink)] outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]"
          >
            {currencies.map((value) => (
              <option key={value} value={value}>
                {value} · {currencyName(value)}
              </option>
            ))}
          </select>
        </label>
        <p className="text-xs leading-5 text-[var(--muted)]">{account("currencyHelp")}</p>
        <p className="text-xs leading-5 text-[var(--muted)]">
          {account("currencyPreview", { amount: formatMoney(SAMPLE_AMOUNT, currency) })}
        </p>
        {syncFailed && (
          <p role="status" className="text-xs text-amber-800">
            {account("currencySyncFailed")}
          </p>
        )}
      </div>
    </section>
  );
}
