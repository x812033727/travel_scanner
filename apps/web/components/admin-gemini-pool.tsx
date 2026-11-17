"use client";

import { ExternalLink } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { geminiPoolCopy } from "@/lib/gemini-pool-copy";

export type GeminiPoolKey = {
  fingerprint_tail: string;
  position: number;
  site_key: boolean;
  active: boolean;
  resting: string | null;
  rest_seconds: number;
  month_usd: number;
  budget_usd: number | null;
};

export type GeminiPoolSnapshot = { keys: GeminiPoolKey[]; redis_ok: boolean };

const ENDPOINT = "/admin/provider-settings/ai_vendors/gemini-pool";
const BILLING_URL = "https://aistudio.google.com/billing";

function usd(value: number) {
  return `US$${value.toFixed(2)}`;
}

/**
 * The Gemini keys in the order the site uses them (app.ai.gemini_pool): which one takes calls
 * now, which rest after Google refused them for credit, and this month's estimated spend. Keys
 * are named by the last four characters of their fingerprint, never by themselves.
 */
export function AdminGeminiPool() {
  const locale = useLocale();
  const copy = geminiPoolCopy(locale).panel;
  const dateTime = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  const [snapshot, setSnapshot] = useState<GeminiPoolSnapshot | null>(null);
  const [loadedAt, setLoadedAt] = useState(0);
  const [failed, setFailed] = useState(false);

  useEffect(() => {
    let live = true;
    api<GeminiPoolSnapshot>(ENDPOINT)
      .then((result) => {
        if (!live) return;
        setSnapshot(result);
        setLoadedAt(Date.now());
      })
      .catch(() => {
        if (live) setFailed(true);
      });
    return () => {
      live = false;
    };
  }, []);

  function state(key: GeminiPoolKey) {
    const until = dateTime.format(new Date(loadedAt + key.rest_seconds * 1000));
    if (key.resting === "exhausted") return `${copy.exhausted} ${until}`;
    if (key.resting === "busy") return `${copy.busy} ${until}`;
    if (key.budget_usd !== null && key.month_usd >= key.budget_usd) return copy.over;
    return key.active ? copy.active : copy.ready;
  }

  return (
    <section className="mt-6 rounded-2xl bg-[var(--paper)] p-4" data-testid="gemini-pool">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 className="text-sm font-bold">{copy.title}</h3>
        <a href={BILLING_URL} target="_blank" rel="noreferrer" className="inline-flex min-h-11 items-center gap-1 text-xs font-semibold text-[var(--teal)] underline">
          {copy.billing}
          <ExternalLink size={13} aria-hidden />
        </a>
      </div>
      <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{copy.intro}</p>
      {failed && <p role="alert" className="mt-3 text-sm text-red-700">{copy.error}</p>}
      {snapshot && snapshot.keys.length < 2 && <p className="mt-3 text-sm text-[var(--muted)]">{copy.single}</p>}
      {snapshot && snapshot.keys.length > 1 && (
        <div className="mt-3 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs text-[var(--muted)]">
              <tr>
                <th className="py-2 pr-3">{copy.order}</th>
                <th className="py-2 pr-3">{copy.key}</th>
                <th className="py-2 pr-3">{copy.spent}</th>
                <th className="py-2 pr-3">{copy.budget}</th>
                <th className="py-2">{copy.state}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--line)]">
              {snapshot.keys.map((key) => (
                <tr key={key.position} className={key.active ? "font-semibold" : undefined}>
                  <td className="py-2 pr-3">{key.position + 1}</td>
                  <td className="py-2 pr-3 font-mono">
                    …{key.fingerprint_tail}
                    {key.site_key && <span className="ml-2 font-sans text-xs text-[var(--muted)]">{copy.siteKey}</span>}
                  </td>
                  <td className="py-2 pr-3">{usd(key.month_usd)}</td>
                  <td className="py-2 pr-3">{key.budget_usd === null ? copy.none : usd(key.budget_usd)}</td>
                  <td className="py-2">{state(key)}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}
