"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import { MERCHANT_STYLES, type MerchantStyle } from "@/lib/foods";

type Review = {
  style: MerchantStyle;
  status: "pending" | "approved" | "rejected";
  evidence_url: string;
  evidence_title: string;
  rationale: string;
  checked_on: string;
  updated_at?: string;
};

function emptyReview(style: MerchantStyle): Review {
  return { style, status: "pending", evidence_url: "", evidence_title: "", rationale: "", checked_on: "" };
}

/** Saved independently: classifying a shop cannot approve its location or publish it. */
export function AdminMerchantStyles({ merchantId }: { merchantId: string }) {
  const t = useTranslations("foods.styles");
  const [open, setOpen] = useState(false);
  const [loaded, setLoaded] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState(false);
  const [style, setStyle] = useState<MerchantStyle>("instagrammable");
  const [drafts, setDrafts] = useState<Record<MerchantStyle, Review>>({
    instagrammable: emptyReview("instagrammable"), artsy: emptyReview("artsy"),
  });
  const [reason, setReason] = useState("");
  const current = drafts[style];
  const update = (values: Partial<Review>) => {
    setDrafts((all) => ({ ...all, [style]: { ...all[style], ...values } }));
    setSuccess(false);
  };
  async function load() {
    setOpen(true); setBusy(true); setLoaded(false); setError(""); setSuccess(false);
    try {
      const data = await api<{ items: Review[] }>(`/admin/foods/merchants/${merchantId}/styles`);
      const next = { instagrammable: emptyReview("instagrammable"), artsy: emptyReview("artsy") };
      for (const item of data.items) next[item.style] = item;
      setDrafts(next); setLoaded(true);
    } catch (cause) { setError((cause as Error).message); }
    finally { setBusy(false); }
  }
  async function save() {
    setBusy(true); setError(""); setSuccess(false);
    const { updated_at, ...review } = current;
    // Only explicitly editable fields cross the boundary (GET may include review metadata).
    try {
      const saved = await api<Review>(`/admin/foods/merchants/${merchantId}/styles`, {
        method: "PUT", body: JSON.stringify({
          expected_updated_at: updated_at ?? null, reason,
          review: { style: review.style, status: review.status, evidence_url: review.evidence_url,
            evidence_title: review.evidence_title, rationale: review.rationale, checked_on: review.checked_on },
        }),
      });
      setDrafts((all) => ({ ...all, [style]: saved })); setReason(""); setSuccess(true);
    } catch (cause) { setError((cause as Error).message); }
    finally { setBusy(false); }
  }
  return (
    <section className="mt-5 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
      <button type="button" aria-expanded={open} disabled={busy}
        className="min-h-11 rounded-xl border px-4 font-semibold"
        onClick={() => open ? setOpen(false) : loaded ? setOpen(true) : void load()}>{t("reviewTitle")}</button>
      {open && <div className="mt-3 grid gap-3">
        <p className="text-sm text-[var(--muted)]">{t("reviewHelp")}</p>
        <button type="button" disabled={busy} onClick={() => void load()}
          className="min-h-11 justify-self-start rounded-xl border px-4">{t("reload")}</button>
        <fieldset disabled={busy || !loaded} className="grid gap-3 md:grid-cols-2">
          <label>{t("label")}<select value={style} onChange={(event) => { setStyle(event.target.value as MerchantStyle); setSuccess(false); }}
            className="mt-1 min-h-11 w-full rounded-xl border px-3">
            {MERCHANT_STYLES.map((item) => <option key={item} value={item}>{t(item)}</option>)}
          </select></label>
          <label>{t("status")}<select value={current.status} onChange={(event) => update({ status: event.target.value as Review["status"] })}
            className="mt-1 min-h-11 w-full rounded-xl border px-3">
            {(["pending", "approved", "rejected"] as const).map((item) => <option key={item} value={item}>{t(item)}</option>)}
          </select></label>
          <p className="text-sm md:col-span-2">{t(`${style}Criteria`)}</p>
          <label>{t("sourceUrl")}<input type="url" value={current.evidence_url}
            onChange={(event) => update({ evidence_url: event.target.value })} className="mt-1 min-h-11 w-full rounded-xl border px-3" /></label>
          <label>{t("sourceTitle")}<input value={current.evidence_title} maxLength={255}
            onChange={(event) => update({ evidence_title: event.target.value })} className="mt-1 min-h-11 w-full rounded-xl border px-3" /></label>
          <label>{t("checkedOn")}<input type="date" value={current.checked_on}
            onChange={(event) => update({ checked_on: event.target.value })} className="mt-1 min-h-11 w-full rounded-xl border px-3" /></label>
          <label>{t("reason")}<input value={reason} maxLength={500} onChange={(event) => setReason(event.target.value)}
            className="mt-1 min-h-11 w-full rounded-xl border px-3" /></label>
          <label className="md:col-span-2">{t("rationale")}<textarea value={current.rationale} maxLength={1000}
            onChange={(event) => update({ rationale: event.target.value })} className="mt-1 min-h-24 w-full rounded-xl border p-3" /></label>
          <button type="button" onClick={() => void save()}
            disabled={reason.trim().length < 3 || current.rationale.trim().length < 10 || !current.evidence_title.trim() || !current.evidence_url.startsWith("https://") || !current.checked_on}
            className="min-h-11 rounded-xl bg-[var(--teal)] px-4 text-white disabled:opacity-50">{t("save")}</button>
        </fieldset>
        {busy && <p role="status">{t("busy")}</p>}
        {success && <p role="status">{t("saved")}</p>}
        {error && <p role="alert">{error}</p>}
      </div>}
    </section>
  );
}
