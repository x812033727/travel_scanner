"use client";
import { useTranslations } from "next-intl";

export type QuotePolicy = {
  enabled: boolean;
  comparison_allowed: boolean;
  terms_url: string | null;
  daily_limit: number;
  per_minute_limit: number;
  timeout_seconds: number;
  cache_seconds: number;
};
const defaults: QuotePolicy = {
  enabled: false,
  comparison_allowed: false,
  terms_url: null,
  daily_limit: 0,
  per_minute_limit: 10,
  timeout_seconds: 8,
  cache_seconds: 0,
};
const field =
  "mt-1 min-h-11 w-full min-w-0 rounded-xl border border-[var(--line)] bg-[var(--surface-raised)] p-3 text-sm";
export function QuotePolicies({
  policies,
  providers,
  brands,
  onChange,
  disabled = false,
}: {
  policies: Record<string, QuotePolicy>;
  providers: Record<string, { adapter_available: boolean }>;
  brands: Record<string, { name: string }>;
  onChange: (value: Record<string, QuotePolicy>) => void;
  disabled?: boolean;
}) {
  const t = useTranslations("travelServices");
  return (
    <details className="rounded-2xl border border-[var(--line)] p-4">
      <summary className="min-h-11 cursor-pointer py-3 font-semibold">
        {t("quotePermissions")}
      </summary>
      <p className="mb-4 text-sm text-[var(--muted)]">{t("quoteNoCache")}</p>
      {["booking", "trip_com", "agoda", "expedia", "rakuten"].map((code) => {
        const policy = policies[code] || defaults;
        const change = (patch: Partial<QuotePolicy>) =>
          onChange({ ...policies, [code]: { ...policy, ...patch } });
        return (
          <fieldset
            key={code}
            disabled={disabled}
            className="mb-4 min-w-0 space-y-3 rounded-xl border border-[var(--line)] p-3"
          >
            <legend className="px-2 font-semibold">
              {brands[code]?.name || code}
            </legend>
            {!providers[code]?.adapter_available && (
              <p className="text-sm">{t("quoteNotConfigured")}</p>
            )}
            <label className="flex min-h-11 items-center gap-2">
              <input
                type="checkbox"
                disabled={!providers[code]?.adapter_available}
                checked={policy.enabled}
                onChange={(e) => change({ enabled: e.target.checked })}
              />
              {t("enabled")}
            </label>
            <label className="flex min-h-11 items-center gap-2">
              <input
                type="checkbox"
                checked={policy.comparison_allowed}
                onChange={(e) =>
                  change({
                    comparison_allowed: e.target.checked,
                    enabled: false,
                  })
                }
              />
              {t("comparisonAllowed")}
            </label>
            <label className="block text-sm">
              {t("termsUrl")}
              <input
                type="url"
                className={field}
                value={policy.terms_url || ""}
                onChange={(e) =>
                  change({ terms_url: e.target.value || null, enabled: false })
                }
              />
            </label>
            <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
              {(
                [
                  ["daily_limit", "dailyLimit", 0, 100000],
                  ["per_minute_limit", "minuteLimit", 1, 1000],
                  ["timeout_seconds", "timeoutSeconds", 1, 20],
                ] as const
              ).map(([key, label, min, max]) => (
                <label key={key} className="block text-sm">
                  {t(label)}
                  <input
                    type="number"
                    min={min}
                    max={max}
                    className={field}
                    value={policy[key]}
                    onChange={(e) => change({ [key]: Number(e.target.value) })}
                  />
                </label>
              ))}
            </div>
          </fieldset>
        );
      })}
    </details>
  );
}
