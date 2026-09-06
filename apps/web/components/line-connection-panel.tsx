"use client";

import { CheckCircle2, LoaderCircle, MessageCircle, RotateCw, Unlink } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { ApiError, api } from "@/lib/api";

// The bot answers only three exact Traditional Chinese phrases, listed in
// apps/api/app/line/router.py, so this word stays Chinese in every locale. Translating it in
// the Japanese or Korean copy would tell a reader to send something the bot ignores, and they
// would have no way to tell that apart from the account simply not linking. It is passed to
// the message as a parameter rather than written into each translation, so no future editor
// can helpfully localise it.
const LINK_KEYWORD = "綁定";

type Connection = {
  configured: boolean;
  status: "unlinked" | "linked" | "blocked";
  display_name?: string | null;
  masked_user_id?: string | null;
  official_account_id?: string | null;
  add_friend_url?: string | null;
};

export function LineConnectionPanel() {
  const t = useTranslations("alerts.line");
  const [connection, setConnection] = useState<Connection>();
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState<string>();
  const [error, setError] = useState<string>();

  const load = useCallback(async () => {
    setLoading(true); setError(undefined);
    try { setConnection(await api<Connection>("/line/connection")); }
    catch (reason) {
      if (!(reason instanceof ApiError && reason.status === 401)) setError((reason as Error).message);
    } finally { setLoading(false); }
  }, []);
  useEffect(() => {
    let current = true;
    void api<Connection>("/line/connection")
      .then((value) => { if (current) setConnection(value); })
      .catch((reason: unknown) => {
        if (current && !(reason instanceof ApiError && reason.status === 401)) {
          setError((reason as Error).message);
        }
      })
      .finally(() => { if (current) setLoading(false); });
    return () => { current = false; };
  }, []);

  async function testMessage() {
    setMessage(undefined); setError(undefined);
    try { await api("/line/test-message", { method: "POST" }); setMessage(t("testSent")); }
    catch (reason) { setError((reason as Error).message); }
  }
  async function unlink() {
    setMessage(undefined); setError(undefined);
    try { await api("/line/connection", { method: "DELETE" }); await load(); setMessage(t("unlinkDone")); }
    catch (reason) { setError((reason as Error).message); }
  }

  return <section className="mb-8 rounded-2xl border border-[var(--line)] bg-white p-6">
    <div className="flex flex-wrap items-start justify-between gap-3"><div><p className="flex items-center gap-2 font-semibold"><MessageCircle className="text-[#06c755]" size={20} />{t("title")}</p><p className="mt-1 text-sm text-[var(--muted)]">{t("description")}</p></div>{loading && <LoaderCircle className="animate-spin text-[var(--muted)]" size={20} />}</div>
    {!loading && connection && !connection.configured && <p className="mt-4 rounded-xl bg-amber-50 p-3 text-sm text-amber-900">{t("notConfigured")}</p>}
    {!loading && connection?.configured && connection.status === "unlinked" && <div className="mt-4 flex flex-wrap items-center gap-3"><a href={connection.add_friend_url || "https://line.me/"} target="_blank" rel="noreferrer" className="rounded-xl bg-[#06c755] px-4 py-3 text-sm font-semibold text-white">{t("addFriend")}</a><p className="text-sm text-[var(--muted)]">{t("keywordHint", { account: connection.official_account_id || t("accountPending"), keyword: LINK_KEYWORD })}</p></div>}
    {!loading && connection?.status === "linked" && <div className="mt-4 flex flex-wrap items-center justify-between gap-3 rounded-xl bg-emerald-50 p-4"><p className="flex items-center gap-2 text-sm font-semibold text-emerald-900"><CheckCircle2 size={18} />{t("linked", { name: connection.display_name || "", id: connection.masked_user_id || "" })}</p><div className="flex gap-2"><button type="button" onClick={testMessage} className="rounded-lg border border-emerald-200 bg-white px-3 py-2 text-sm font-semibold">{t("sendTest")}</button><button type="button" onClick={unlink} aria-label={t("unlink")} className="rounded-lg border border-emerald-200 bg-white p-2"><Unlink size={17} /></button></div></div>}
    {!loading && connection?.status === "blocked" && <div className="mt-4 rounded-xl bg-amber-50 p-4 text-sm text-amber-900">{t("blocked", { keyword: LINK_KEYWORD })}</div>}
    {error && <p role="alert" className="mt-3 rounded-xl bg-red-50 p-3 text-sm text-red-800">{error} <button type="button" onClick={load} className="ml-2 inline-flex items-center gap-1 underline"><RotateCw size={13} />{t("retry")}</button></p>}
    {message && <p role="status" className="mt-3 text-sm text-emerald-800">{message}</p>}
  </section>;
}
