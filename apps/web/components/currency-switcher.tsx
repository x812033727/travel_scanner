"use client";

import { Coins } from "lucide-react";
import { useTranslations } from "next-intl";
import { useRef, useState } from "react";
import { useHeaderSession } from "@/components/header-session";
import { api } from "@/lib/api";
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
  const { status, user, setUser } = useHeaderSession();
  const [chosen, setChosen] = useState<Currency | null>(null);
  const [syncFailed, setSyncFailed] = useState(false);
  // Only the newest change may write the select back on failure. Without this a
  // slow first request failing late would undo a second choice that did save.
  const pending = useRef(0);

  // The provider asked /auth/me for the whole page, so this no longer asks again.
  // Any failure other than "signed out" still gets a working control showing the
  // default: a 500 must not delete the section from a signed-in member's page.
  const currency = chosen ?? (user ? normalizeCurrency(user.preferred_currency) : defaultCurrency);

  async function change(next: Currency) {
    const previous = currency;
    if (next === previous) return;
    const attempt = (pending.current += 1);
    setSyncFailed(false);
    setChosen(next);
    try {
      await api("/auth/me", { method: "PATCH", body: JSON.stringify({ preferred_currency: next }) });
      if (attempt === pending.current && user) setUser({ ...user, preferred_currency: next });
    } catch {
      if (attempt !== pending.current) return;
      // The language switcher can keep a local-only choice because the cookie
      // already drives the page. A currency that only exists in this component's
      // state would be a lie, so put the saved one back.
      setChosen(previous);
      setSyncFailed(true);
    }
  }

  // The account panel below already asks a signed-out visitor to sign in.
  if (status === "loading" || status === "signed_out") return null;

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
