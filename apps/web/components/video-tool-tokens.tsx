"use client";

import { Check, Copy, KeyRound, LoaderCircle, Trash2 } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useState } from "react";
import { ApiError, api } from "@/lib/api";

export type VideoToolToken = {
  id: string;
  name: string;
  token_prefix: string;
  created_at: string;
  last_used_at: string | null;
  revoked_at: string | null;
};

const ENDPOINT = "/admin/provider-settings/azure_speech/video-tool-tokens";

/**
 * The credentials the local video pipeline (tools/video) uses to have this server narrate. A new
 * token is shown once, with a copy button; afterwards only its first characters are listed.
 */
export function VideoToolTokens({ canManage }: { canManage: boolean }) {
  const t = useTranslations("admin.videoTools");
  const locale = useLocale();
  const dateTime = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  const [tokens, setTokens] = useState<VideoToolToken[] | null>(null);
  const [name, setName] = useState("");
  const [created, setCreated] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);
  const [confirming, setConfirming] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = useCallback(async () => {
    try {
      setTokens(await api<VideoToolToken[]>(ENDPOINT));
      setError(null);
    } catch (problem) {
      setError(problem instanceof ApiError ? problem.message : t("loadFailed"));
    }
  }, [t]);

  useEffect(() => {
    // Loaded after mount: the list is private and not part of the settings snapshot.
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function create() {
    setBusy(true);
    try {
      const result = await api<VideoToolToken & { token: string }>(ENDPOINT, {
        method: "POST",
        body: JSON.stringify({ name: name.trim() || t("namePlaceholder") }),
      });
      setCreated(result.token);
      setCopied(false);
      setName("");
      await load();
    } catch (problem) {
      setError(problem instanceof ApiError ? problem.message : t("loadFailed"));
    } finally {
      setBusy(false);
    }
  }

  async function revoke(id: string) {
    setBusy(true);
    try {
      await api<VideoToolToken>(`${ENDPOINT}/${id}`, { method: "DELETE" });
      setConfirming(null);
      await load();
    } catch (problem) {
      setError(problem instanceof ApiError ? problem.message : t("loadFailed"));
    } finally {
      setBusy(false);
    }
  }

  async function copy() {
    if (!created) return;
    try {
      await navigator.clipboard.writeText(created);
      setCopied(true);
    } catch {
      // Clipboard access can be refused; the token stays selectable on screen.
    }
  }

  return <section className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5" aria-labelledby="video-tool-tokens-title">
    <h3 id="video-tool-tokens-title" className="flex items-center gap-2 text-base font-bold"><KeyRound size={17} />{t("title")}</h3>
    <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("intro")}</p>

    {created && <div role="status" className="mt-4 rounded-xl border border-amber-300 bg-amber-50 p-4">
      <p className="text-sm font-bold text-amber-900">{t("createdTitle")}</p>
      <p className="mt-1 text-xs leading-5 text-amber-900">{t("createdHelp")}</p>
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <code data-testid="new-video-tool-token" className="min-w-0 flex-1 break-all rounded-lg bg-white px-3 py-2 text-sm">{created}</code>
        <button type="button" onClick={copy} className="flex min-h-11 items-center gap-2 rounded-xl border border-amber-300 bg-white px-3 text-sm font-semibold">{copied ? <Check size={15} /> : <Copy size={15} />}{copied ? t("copied") : t("copy")}</button>
        <button type="button" onClick={() => setCreated(null)} className="min-h-11 rounded-xl px-3 text-sm font-semibold text-amber-900 underline">{t("dismiss")}</button>
      </div>
    </div>}

    {canManage && <form className="mt-4 flex flex-wrap items-end gap-3" onSubmit={(event) => { event.preventDefault(); void create(); }}>
      <label className="grid min-w-0 flex-1 gap-1 text-sm font-semibold">{t("nameLabel")}
        <input value={name} maxLength={80} placeholder={t("namePlaceholder")} onChange={(event) => setName(event.target.value)} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 font-normal" />
      </label>
      <button type="submit" disabled={busy} className="flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white disabled:opacity-50">{busy && <LoaderCircle size={15} className="animate-spin" />}{busy ? t("creating") : t("create")}</button>
    </form>}

    {error && <p role="alert" className="mt-3 text-sm font-semibold text-red-700">{error}</p>}

    {tokens && tokens.length === 0 && <p className="mt-4 text-sm text-[var(--muted)]">{t("empty")}</p>}
    {tokens && tokens.length > 0 && <ul className="mt-4 divide-y divide-[var(--line)] rounded-xl border border-[var(--line)] bg-white">
      {tokens.map((token) => <li key={token.id} className="flex flex-wrap items-center justify-between gap-3 px-4 py-3 text-sm">
        <div className="min-w-0">
          <p className="font-semibold">{token.name}{token.revoked_at && <span className="ml-2 rounded-full bg-gray-100 px-2 py-0.5 text-xs font-semibold text-[var(--muted)]">{t("revoked")}</span>}</p>
          <p className="mt-0.5 text-xs text-[var(--muted)]">{t("prefix")} <code>{token.token_prefix}…</code> · {t("createdAt")} {dateTime.format(new Date(token.created_at))} · {t("lastUsed")} {token.last_used_at ? dateTime.format(new Date(token.last_used_at)) : t("never")}</p>
        </div>
        {canManage && !token.revoked_at && (confirming === token.id
          ? <div className="flex gap-2"><button type="button" disabled={busy} onClick={() => void revoke(token.id)} className="min-h-11 rounded-xl bg-red-700 px-3 text-sm font-semibold text-white disabled:opacity-50">{t("confirmRevoke")}</button><button type="button" onClick={() => setConfirming(null)} className="min-h-11 rounded-xl px-3 text-sm font-semibold">{t("cancel")}</button></div>
          : <button type="button" onClick={() => setConfirming(token.id)} className="flex min-h-11 items-center gap-2 rounded-xl border border-red-200 px-3 text-sm font-semibold text-red-700"><Trash2 size={15} />{t("revoke")}</button>)}
      </li>)}
    </ul>}
  </section>;
}
