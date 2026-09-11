"use client";

import { useEffect, useId, useRef, useState } from "react";
import { useTranslations } from "next-intl";
import { api, ApiError } from "@/lib/api";
import { reservationPlatformHref, reservationPlatformIdentity } from "@/lib/reservation-platforms";

export type PlatformStatus = "verified" | "not_found" | "ambiguous" | "disabled";
export type MerchantPlatformLink = {
  id?: string;
  provider: string;
  provider_label: string;
  canonical_url: string | null;
  localized_urls: Partial<Record<"zh-TW" | "zh-CN" | "en" | "ja" | "ko", string>>;
  status: PlatformStatus;
  checked_at?: string;
  checked_by_user_id?: string | null;
  review_note: string | null;
};
export type PlatformOption = { provider: string; label: string };
export type MerchantPlatformFields = {
  platform_links?: MerchantPlatformLink[];
  platform_link: MerchantPlatformLink | null;
};

export function merchantPlatformLinks(value: MerchantPlatformFields): MerchantPlatformLink[] {
  return value.platform_links ?? (value.platform_link ? [value.platform_link] : []);
}

const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
type Draft = { value: MerchantPlatformLink; baseline: string };

function signature(value: MerchantPlatformLink) {
  return JSON.stringify([value.status, value.canonical_url ?? "", locales.map((locale) => value.localized_urls[locale] ?? ""), value.review_note ?? ""]);
}

function blankLink(option: PlatformOption): MerchantPlatformLink {
  return { provider: option.provider, provider_label: option.label, status: "not_found", canonical_url: null, localized_urls: {}, review_note: null };
}

/** Each provider has its own draft and concurrency token; merchant fields never cross this boundary. */
export function AdminMerchantPlatformEditor({
  merchantId, links, availablePlatforms, disabled = false, onSaved, onBusyChange, onDirtyChange,
}: {
  merchantId: string;
  links: MerchantPlatformLink[];
  availablePlatforms: readonly PlatformOption[];
  disabled?: boolean;
  onSaved: (saved: MerchantPlatformFields) => void;
  onBusyChange: (busy: boolean) => void;
  onDirtyChange: (dirty: boolean) => void;
}) {
  const t = useTranslations("admin.foodMerchantsPanel");
  const titleId = useId();
  const [provider, setProvider] = useState(links[0]?.provider ?? availablePlatforms[0]?.provider ?? "");
  const [drafts, setDrafts] = useState<Record<string, Draft>>({});
  const [busy, setBusy] = useState(false);
  const inFlight = useRef(false);
  const restoreFocus = useRef<HTMLElement | null>(null);
  const noticeElement = useRef<HTMLParagraphElement | null>(null);
  const saveButton = useRef<HTMLButtonElement | null>(null);
  const restoreRetryFocus = useRef(false);
  const [notice, setNotice] = useState<{ provider: string; text: string; error: boolean } | null>(null);
  const [conflicts, setConflicts] = useState<Record<string, { loaded: boolean; latest: MerchantPlatformLink | null }>>({});
  const savedLink = links.find((link) => link.provider === provider);
  const option = availablePlatforms.find((item) => item.provider === provider);
  const current = drafts[provider]?.value ?? savedLink ?? blankLink(option ?? { provider, label: provider });
  const dirtyProviders = Object.entries(drafts).filter(([, draft]) => signature(draft.value) !== draft.baseline).map(([key]) => key);
  const hasDirtyDraft = dirtyProviders.length > 0;
  const currentDirty = dirtyProviders.includes(provider);
  const canonicalHref = reservationPlatformHref(provider, current.canonical_url);
  const canonicalIdentity = reservationPlatformIdentity(provider, current.canonical_url);
  const invalidLocales = locales.filter((locale) => {
    const url = current.localized_urls[locale]?.trim();
    return url && (!reservationPlatformHref(provider, url) || reservationPlatformIdentity(provider, url) !== canonicalIdentity);
  });
  const invalidVerified = current.status === "verified" && (!canonicalHref || invalidLocales.length > 0 || !current.review_note?.trim());

  useEffect(() => { onDirtyChange(hasDirtyDraft); }, [hasDirtyDraft, onDirtyChange]);
  useEffect(() => {
    if (!busy && restoreFocus.current) {
      const active = document.activeElement;
      const target = restoreFocus.current.matches(":disabled") ? noticeElement.current : restoreFocus.current;
      if (target?.isConnected && (active === document.body || active === restoreFocus.current)) target.focus({ preventScroll: true });
      restoreFocus.current = null;
    }
  }, [busy]);
  useEffect(() => {
    if (restoreRetryFocus.current && !conflicts[provider]) {
      saveButton.current?.focus({ preventScroll: true });
      restoreRetryFocus.current = false;
    }
  }, [conflicts, provider]);

  function update(patch: Partial<MerchantPlatformLink>) {
    setDrafts((all) => ({ ...all, [provider]: { baseline: all[provider]?.baseline ?? signature(current), value: { ...current, ...patch } } }));
    setNotice(null);
  }

  async function save() {
    if (!merchantId || !option || disabled || inFlight.current || invalidVerified || conflicts[provider]) return;
    inFlight.current = true;
    restoreFocus.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    setBusy(true);
    onBusyChange(true);
    setNotice(null);
    try {
      const saved = await api<MerchantPlatformFields>(`/admin/foods/merchants/${merchantId}/platform-link`, {
        method: "PUT",
        body: JSON.stringify({
          provider,
          status: current.status,
          canonical_url: current.canonical_url,
          localized_urls: Object.fromEntries(locales.flatMap((locale) => {
            const value = current.localized_urls[locale]?.trim();
            return value ? [[locale, value]] : [];
          })),
          review_note: current.review_note,
          expected_checked_at: current.checked_at ?? null,
        }),
      });
      onSaved(saved);
      setDrafts((all) => Object.fromEntries(Object.entries(all).filter(([key]) => key !== provider)));
      setNotice({ provider, text: t("platformSaved", { provider: option.label }), error: false });
    } catch (reason) {
      const stale = reason instanceof ApiError && reason.status === 409 && reason.code === "reservation_platform_version_conflict";
      if (stale) {
        setDrafts((all) => ({ ...all, [provider]: all[provider] ?? { value: current, baseline: signature(current) } }));
        setConflicts((all) => ({ ...all, [provider]: { loaded: false, latest: null } }));
      }
      setNotice({ provider, text: stale ? t("platformStale") : (reason as Error).message, error: true });
    } finally {
      inFlight.current = false;
      setBusy(false);
      onBusyChange(false);
    }
  }

  async function reloadConflict() {
    if (inFlight.current || disabled) return;
    inFlight.current = true;
    restoreFocus.current = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    setBusy(true);
    onBusyChange(true);
    try {
      const saved = await api<MerchantPlatformFields>(`/admin/foods/merchants/${merchantId}/platform-links`);
      onSaved(saved);
      setConflicts((all) => ({ ...all, [provider]: { loaded: true, latest: merchantPlatformLinks(saved).find((link) => link.provider === provider) ?? null } }));
      setNotice(null);
    } catch (reason) {
      setNotice({ provider, text: (reason as Error).message, error: true });
    } finally {
      inFlight.current = false;
      setBusy(false);
      onBusyChange(false);
    }
  }

  function confirmRetry() {
    if (!conflicts[provider]?.loaded || inFlight.current || disabled) return;
    const latest = conflicts[provider]?.latest;
    restoreRetryFocus.current = true;
    setDrafts((all) => ({ ...all, [provider]: { value: { ...current, checked_at: latest?.checked_at }, baseline: signature(latest ?? blankLink(option!)) } }));
    setConflicts((all) => Object.fromEntries(Object.entries(all).filter(([key]) => key !== provider)));
  }

  return (
    <section aria-labelledby={titleId} aria-busy={busy} className="mt-5 rounded-2xl border border-[var(--teal)] bg-[var(--teal-soft)] p-4">
      <h4 id={titleId} className="font-bold">{t("platformEditorTitle")}</h4>
      <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{t("platformEditorHelp")}</p>
      {!merchantId && <p role="status" className="mt-3 font-semibold">{t("platformCreateFirst")}</p>}
      <fieldset disabled={!merchantId || busy || disabled} className="mt-3 grid min-w-0 gap-3 md:grid-cols-2">
        <label className="text-sm font-semibold">
          {t("platformProvider")}
          <select value={provider} onChange={(event) => setProvider(event.target.value)} className="mt-1 h-11 w-full rounded-xl border bg-white px-3">
            {availablePlatforms.map((item) => <option key={item.provider} value={item.provider}>{item.label}</option>)}
          </select>
        </label>
        <label className="text-sm font-semibold">
          {t("platformReviewStatus")}
          <select value={current.status} onChange={(event) => update({ status: event.target.value as PlatformStatus })} className="mt-1 h-11 w-full rounded-xl border bg-white px-3">
            {(["verified", "not_found", "ambiguous", "disabled"] as const).map((status) => <option key={status} value={status}>{t(`platformStatus.${status}`)}</option>)}
          </select>
        </label>
        <ul aria-label={t("platformSavedList")} className="flex flex-wrap gap-2 text-xs md:col-span-2">
          {links.map((link) => <li key={link.provider} className="rounded-lg border bg-white px-3 py-2">{link.provider_label} · {t(`platformStatus.${link.status}`)}</li>)}
        </ul>
        {hasDirtyDraft && <p role="status" className="text-sm font-semibold md:col-span-2">{t("platformDraftsKept", { providers: dirtyProviders.map((key) => availablePlatforms.find((item) => item.provider === key)?.label ?? key).join(", ") })}</p>}
        <label className="text-sm font-semibold md:col-span-2">
          {t("platformCanonicalUrl")}
          <input value={current.canonical_url ?? ""} onChange={(event) => update({ canonical_url: event.target.value || null })} placeholder="https://" className="mt-1 h-11 w-full rounded-xl border bg-white px-3" />
        </label>
        {canonicalHref && <a href={canonicalHref} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center justify-self-start rounded-xl border bg-white px-3 py-2 text-sm font-semibold md:col-span-2">{t("platformOpenCheck")}</a>}
        {locales.map((locale) => <label key={locale} className="text-xs font-semibold">
          {t("platformLocalizedUrl", { locale })}
          <input value={current.localized_urls[locale] ?? ""} onChange={(event) => update({ localized_urls: { ...current.localized_urls, [locale]: event.target.value } })} placeholder="https://" className="mt-1 h-11 w-full rounded-xl border bg-white px-3" />
        </label>)}
        <label className="text-sm font-semibold md:col-span-2">
          {t("platformReviewNote")}
          <textarea value={current.review_note ?? ""} onChange={(event) => update({ review_note: event.target.value || null })} className="mt-1 min-h-24 w-full rounded-xl border bg-white p-3" />
        </label>
        <p className="text-xs leading-5 text-[var(--muted)] md:col-span-2">{t("platformIndividualOnly")}</p>
        {invalidVerified && <p className="text-sm text-red-800 md:col-span-2">{t("platformValidationHelp")}</p>}
        <div className="flex flex-wrap gap-3 md:col-span-2">
          <button ref={saveButton} type="button" onClick={() => void save()} disabled={!option || invalidVerified || !!conflicts[provider]} className="min-h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-40">{busy ? t("platformSaving") : t("platformSaveOnly")}</button>
          {currentDirty && <button type="button" onClick={() => { setDrafts((all) => Object.fromEntries(Object.entries(all).filter(([key]) => key !== provider))); setConflicts((all) => Object.fromEntries(Object.entries(all).filter(([key]) => key !== provider))); setNotice(null); }} className="min-h-11 rounded-xl border bg-white px-4">{t("platformDiscardDraft")}</button>}
        </div>
      </fieldset>
      {notice?.provider === provider && <p ref={noticeElement} tabIndex={-1} role={notice.error ? "alert" : "status"} className={`mt-3 rounded-xl px-4 py-3 text-sm font-semibold ${notice.error ? "bg-red-50 text-red-800" : "bg-white text-[var(--teal)]"}`}>{notice.text}</p>}
      {conflicts[provider] && <div className="mt-3 rounded-xl border bg-white p-3 text-sm">
        <button type="button" disabled={busy || disabled} onClick={() => void reloadConflict()} className="min-h-11 rounded-xl border px-3">{t("platformReloadDraft")}</button>
        {conflicts[provider].loaded && <div className="mt-3">
          <p className="font-semibold">{t("platformLatestSaved")}</p>
          <p>{conflicts[provider].latest ? t(`platformStatus.${conflicts[provider].latest!.status}`) : t("platformUnreviewed")}</p>
          <p className="break-all">{conflicts[provider].latest?.canonical_url ?? "—"}</p>
          <p className="whitespace-pre-wrap">{conflicts[provider].latest?.review_note ?? "—"}</p>
          {locales.map((locale) => <p key={locale} className="break-all">{locale}: {conflicts[provider].latest?.localized_urls[locale] ?? "—"}</p>)}
          <button type="button" disabled={busy || disabled} onClick={confirmRetry} className="mt-3 min-h-11 rounded-xl border px-3">{t("platformConfirmRetry")}</button>
        </div>}
      </div>}
    </section>
  );
}
