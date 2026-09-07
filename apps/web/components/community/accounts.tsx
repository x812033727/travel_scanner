"use client";

import { useEffect, useRef, useState, type FormEvent } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link, useRouter } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { api } from "@/lib/api";
import { useCommunity } from "./provider";
import { Button, Empty, ErrorNotice, fieldClass, panelClass } from "./ui";

export function AccountSafety() {
  const t = useTranslations("community");
  const { user } = useHeaderSession();
  const { me } = useCommunity();
  const [error, setError] = useState<unknown>();
  const [sent, setSent] = useState(false);
  const [busy, setBusy] = useState(false);
  async function request(kind: "verification" | "deletion") {
    if (kind === "deletion" && !window.confirm(t("deleteAccountWarning"))) return;
    setBusy(true); setError(undefined); setSent(false);
    try { await api(`/auth/request-${kind}`, { method: "POST" }); setSent(true); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  if (!user) return null;
  const verified = me?.verified || user.email_verified;
  return <section className={`${panelClass} mb-6 space-y-4`}><h2 className="text-xl font-bold">{t("accountSafety")}</h2><p>{verified ? t("emailVerified") : t("verifyRequired")}</p>
    {!verified && <Button disabled={busy} onClick={() => void request("verification")}>{t("sendVerification")}</Button>}
    <div className="border-t border-[var(--line)] pt-4"><h3 className="font-semibold">{t("deleteAccount")}</h3><p className="my-3 text-sm leading-6 text-[var(--muted)]">{t("deleteAccountWarning")}</p><Button secondary disabled={busy || user.is_admin} onClick={() => void request("deletion")}>{t("requestDeletion")}</Button>{user.is_admin && <p className="mt-2 text-sm">{t("errors.community_admin_deletion")}</p>}</div>
    {sent && <p role="status">{t("mailSent")}</p>}<ErrorNotice error={error} />
  </section>;
}

export function ForgotPassword() {
  const t = useTranslations("community");
  const locale = useLocale();
  const [email, setEmail] = useState("");
  const [busy, setBusy] = useState(false);
  const [sent, setSent] = useState(false);
  const [error, setError] = useState<unknown>();
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(undefined);
    try { await api("/auth/forgot-password", { method: "POST", body: JSON.stringify({ email, locale }) }); setSent(true); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  return <form onSubmit={submit} className={`${panelClass} space-y-5`}><p>{t("resetNotice")}</p><label className="block font-semibold">{t("email")}<input type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} className={fieldClass} /></label><ErrorNotice error={error} />{sent && <p role="status">{t("resetSent")}</p>}<Button type="submit" disabled={busy}>{t("sendReset")}</Button><Link href="/login" className="ml-4 underline">{t("login")}</Link></form>;
}

export function AccountConfirmation({ purpose }: { purpose: string }) {
  const t = useTranslations("community");
  const router = useRouter();
  const [token, setToken] = useState("");
  const parsed = useRef(false);
  const [loaded, setLoaded] = useState(false);
  const [password, setPassword] = useState("");
  const [confirmation, setConfirmation] = useState("");
  const [busy, setBusy] = useState(false);
  const [done, setDone] = useState(false);
  const [error, setError] = useState<unknown>();
  useEffect(() => {
    if (parsed.current) return;
    parsed.current = true;
    setToken(new URLSearchParams(window.location.hash.slice(1)).get("token") || "");
    // Remove the secret before any subsequent navigation or accidental link sharing.
    window.history.replaceState(window.history.state, "", window.location.pathname + window.location.search);
    setLoaded(true);
  }, []);
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(undefined);
    const endpoint = purpose === "verify" ? "verify-email" : purpose === "reset" ? "reset-password" : "delete-account";
    try {
      await api(`/auth/${endpoint}`, { method: "POST", body: JSON.stringify({ token, ...(purpose === "reset" ? { password } : purpose === "delete" ? { confirmation } : {}) }) });
      setToken(""); setPassword(""); setDone(true);
      if (purpose !== "verify") {
        navigator.serviceWorker?.controller?.postMessage({ type: "signed-out" });
        router.replace("/login");
      }
      router.refresh();
    } catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  if (!loaded) return <Empty>{t("loading")}</Empty>;
  if (done) return <Empty>{t("accountActionDone")} <Link href={purpose === "verify" ? "/community" : "/login"} className="underline">{t(purpose === "verify" ? "feed" : "login")}</Link></Empty>;
  if (!token || !["verify", "reset", "delete"].includes(purpose)) return <Empty>{t("errors.community_token_invalid")}</Empty>;
  return <form onSubmit={submit} className={`${panelClass} space-y-5`}><h1 className="text-2xl font-bold">{t(`accountPurposes.${purpose}`)}</h1>
    {purpose === "reset" && <label className="block font-semibold">{t("newPassword")}<input type="password" autoComplete="new-password" required minLength={10} maxLength={128} value={password} onChange={(e) => setPassword(e.target.value)} className={fieldClass} /></label>}
    {purpose === "delete" && <><p>{t("deleteAccountWarning")}</p><label className="block font-semibold">{t("typeDelete")}<input required pattern="DELETE" value={confirmation} onChange={(e) => setConfirmation(e.target.value)} className={fieldClass} /></label></>}
    {purpose === "verify" && <p>{t("confirmEmailNotice")}</p>}<ErrorNotice error={error} /><Button type="submit" disabled={busy}>{t("confirm")}</Button>
  </form>;
}
